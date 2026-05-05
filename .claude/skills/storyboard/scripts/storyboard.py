#!/usr/bin/env python3
"""3-Frame Social Storyboard Orchestrator

One call: takes a narrative prompt + dropped source media + a client preset,
generates 3 character-consistent pencil-sketch frames via Gemini, composites
them into a 9:16 1080x1920 PNG, optionally attaches to a Trello card.

Designed to be invoked by the project's `storyboard` skill, never by hand.

Usage:
    storyboard.py --prompt "<narrative>" --client diggerlid \
                  [--source PATH ...] [--trello-card-id ID] \
                  [--api-key KEY] [--output DIR]
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Repo paths
REPO_ROOT = Path(__file__).resolve().parents[4]
PRESETS_DIR = Path.home() / ".banana" / "presets"
SKILLS_DIR = REPO_ROOT / ".claude" / "skills" / "storyboard"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "deliverables"
COST_TRACKER = Path.home() / ".claude" / "skills" / "banana" / "scripts" / "cost_tracker.py"
FONT_PATH = Path("/tmp/fonts/Outfit.ttf")

# Gemini config
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
RESOLUTION = "2K"
ASPECT = "9:16"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

# Layout (1920x1080 landscape) — three 9:16 portrait frames side-by-side.
# v5 amendments: thin yellow border around the canvas, cream paper background
# (no more flooded yellow), taller 2-line-capable caption strips, smaller footer.
# See references/style-recipes.md for the diagram.
CANVAS_W, CANVAS_H = 1920, 1080
BORDER_PX = 8           # thin yellow border on top/left/right
FRAME_W = 502
FRAME_H = 892
CAPTION_H = 100         # accommodates up to 2 lines of caption text at 28pt
CAPTION_LINE_H = 34     # rendered line height for the 28pt caption font
GUTTER = 24             # cream gap between frames
FOOTER_H = 48           # yellow footer strip with brand wordmark (replaces the bottom border)
OUTER_PAD = 175         # cream padding on each outer side of the 3-frame strip
TOP_GAP = 16            # cream breathing room below the top border
CAPTION_TO_FOOTER_GAP = 16   # cream gap between captions and footer
# Math W: 2*8 + 2*175 + 3*502 + 2*24 = 1920 ✓
# Math H: 8 + 16 + 892 + 100 + 16 + 48 = 1080 ✓
HIVIS_YELLOW = (255, 230, 0)
CREAM_BG = (250, 248, 240)   # warm off-white, evokes pencil-sketch paper
NAVY = (26, 31, 46)
WHITE = (255, 255, 255)

PENCIL_STYLE = (
    "Render this beat as a soft graphite pencil sketch on warm cream sketchbook paper, "
    "fully monochrome with no colour anywhere in the artwork. Loose hand-drawn pencil lines, "
    "gentle hatched shading and feathered edges, subtle paper grain. Simplified facial "
    "features in the style of a director's pre-production storyboard. The kind of thumbnail "
    "board pulled from an artist's sketchbook. 9:16 vertical/portrait framing for social "
    "media — composed for a tall narrow panel with the key subject vertically dominant."
)

# Run on the brand-context descriptor before injecting it into a monochrome beat
# prompt. Strips obvious render-as-color cues so the model doesn't paint an
# orange excavator into a pencil sketch (regression observed on db0adc8).
_COLOR_SANITISER = [
    (r"\borange\b", "compact"),
    (r"\bdark navy-black\b", "dark"),
    (r"\bnavy-black\b", "dark"),
    (r"\bnavy\b", "dark"),
    (r"\bhi-vis safety-yellow\b", "high-visibility"),
    (r"\bhi-vis yellow\b", "high-visibility"),
    (r"\bsafety-yellow\b", "high-visibility"),
    (r"\bvivid hazard yellow\b", "high-visibility"),
    (r"\(#[0-9A-Fa-f]{3,8}\)", ""),
    (r"#[0-9A-Fa-f]{6}", ""),
]


def _strip_color_cues(text):
    out = text
    for pattern, repl in _COLOR_SANITISER:
        out = re.sub(pattern, repl, out, flags=re.IGNORECASE)
    return out


def _measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def _wrap_caption(draw, label, beat, font, max_width, max_lines=2):
    """Return a list of caption lines that fit within max_width pixels.

    Strategy:
    1. If `<label>  ·  <beat>` fits on one line, return it.
    2. Otherwise, the first line is `<label>  ·  <words…>` filling as much
       of the beat as fits. The remaining beat words go on line 2. If line 2
       still overflows, chop characters off and append `…`.
    3. If even max_lines don't accommodate the whole beat, the last line is
       ellipsised. Lines beyond max_lines are dropped.

    The label always sits on line 1, intact. The user asked specifically that
    overflow drops onto a second line and that line is shown — so we preserve
    as much of the beat as possible across both lines before ellipsising.
    """
    one_line = f"{label}  ·  {beat}"
    if _measure(draw, one_line, font) <= max_width:
        return [one_line]

    if max_lines < 2:
        # Single-line caller — fall back to ellipsis behaviour
        trimmed = beat
        while trimmed:
            candidate = f"{label}  ·  {trimmed}…"
            if _measure(draw, candidate, font) <= max_width:
                return [candidate]
            trimmed = trimmed[:-1].rstrip()
        return [f"{label}  ·  …"]

    # Two-line wrap: greedy word fill on line 1, remainder on line 2.
    words = beat.split()
    line1_words, line2_words = [], list(words)
    line1_prefix = f"{label}  ·  "
    while line2_words:
        candidate = line1_prefix + " ".join(line1_words + [line2_words[0]])
        if _measure(draw, candidate, font) <= max_width:
            line1_words.append(line2_words.pop(0))
        else:
            break

    if not line1_words:
        # Couldn't fit even one word after the label — let line 1 take the first word anyway
        line1_words = [line2_words.pop(0)] if line2_words else [""]

    line1 = line1_prefix + " ".join(line1_words)
    line2_text = " ".join(line2_words)

    if _measure(draw, line2_text, font) <= max_width:
        return [line1] if not line2_text else [line1, line2_text]

    # Line 2 still too long — ellipsise it
    while line2_text:
        candidate = line2_text + "…"
        if _measure(draw, candidate, font) <= max_width:
            return [line1, candidate]
        line2_text = line2_text[:-1].rstrip()
    return [line1, "…"]


# ------------------------- Helpers -------------------------


def fail(msg, **extra):
    """Emit a JSON error and exit non-zero."""
    payload = {"error": True, "message": msg}
    payload.update(extra)
    print(json.dumps(payload), file=sys.stderr)
    sys.exit(1)


def load_preset(client):
    path = PRESETS_DIR / f"{client}.json"
    if not path.exists():
        fail(f"Preset not found: {path}. Run /banana preset create or place a JSON there.")
    with open(path) as f:
        return json.load(f)


def discover_founders(client):
    """Return [(name, path), ...] for founder reference images that exist on disk."""
    base = REPO_ROOT / "clients" / "assets" / client / "founders"
    found = []
    for slot, label in [("a", "Founder A"), ("b", "Founder B")]:
        for ext in ("jpg", "jpeg", "png", "webp"):
            p = base / f"founder-{slot}.{ext}"
            if p.exists():
                found.append((label, p))
                break
    return found


def load_founder_anchors(client):
    """Extract verbatim face-anchor blockquotes from clients/<client>.md.

    Looks for the pattern:
        ### Founder A — ...
        ...
        **Face anchor — repeat verbatim in every beat prompt:**
        > <one or more blockquote lines>

    Returns {"Founder A": "<anchor text>", "Founder B": "<anchor text>"}, or {}
    if the profile file is missing or unparseable. Missing anchors are silently
    skipped — image refs alone still work, just with weaker likeness lock.
    """
    profile = REPO_ROOT / "clients" / f"{client}.md"
    if not profile.exists():
        return {}
    text = profile.read_text(encoding="utf-8")
    anchors = {}
    pattern = re.compile(
        r"###\s+(Founder\s+[AB])\b.*?"
        r"\*\*Face anchor[^*]*\*\*[^\n]*\n((?:>[^\n]*\n?)+)",
        re.DOTALL | re.IGNORECASE,
    )
    for match in pattern.finditer(text):
        name = match.group(1).strip()
        block = match.group(2)
        anchor_lines = [line.lstrip("> ").rstrip() for line in block.splitlines() if line.startswith(">")]
        anchor = " ".join(anchor_lines).strip()
        if anchor:
            anchors[name] = anchor
    return anchors


def discover_machine(client):
    base = REPO_ROOT / "clients" / "assets" / client
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = base / f"excavator.{ext}"
        if p.exists():
            return ("the excavator", p)
    return None


def split_beats(prompt):
    """Split a narrative into exactly 3 beats. Honour explicit user delimiters."""
    text = prompt.strip()
    for delim in ["→", " -> ", ";"]:
        if delim in text:
            parts = [p.strip() for p in text.split(delim) if p.strip()]
            if len(parts) >= 3:
                return parts[:3]
    parts = [p.strip() for p in re.split(r"\b then\b|, then ", text, flags=re.IGNORECASE) if p.strip()]
    if len(parts) >= 3:
        return parts[:3]
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if len(parts) >= 3:
        return parts[:3]
    # Last resort: auto-suffix if user gave a single sentence
    return [
        f"Establishing wide shot — opening of: {text}",
        f"Mid shot — the action of: {text}",
        f"Close shot — the payoff of: {text}",
    ]


def encode_image(path):
    """Return (mime, base64_str) for an image on disk."""
    mime, _ = mimetypes.guess_type(str(path))
    mime = mime or "image/jpeg"
    with open(path, "rb") as f:
        return mime, base64.b64encode(f.read()).decode("utf-8")


def extract_video_frame(video_path):
    """Extract a representative frame from a video. Requires ffmpeg."""
    if not _has_ffmpeg():
        fail(f"Video input requires ffmpeg: {video_path}. Install ffmpeg or pass a still image.")
    out = Path(f"/tmp/storyboard-frame-{uuid.uuid4().hex[:8]}.png")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path), "-vf", "select=eq(pict_type\\,I)",
         "-vframes", "1", str(out)],
        check=False, capture_output=True,
    )
    if not out.exists():
        # Fallback: first frame
        subprocess.run(["ffmpeg", "-y", "-i", str(video_path), "-vframes", "1", str(out)],
                       check=False, capture_output=True)
    if not out.exists():
        fail(f"Could not extract any frame from video: {video_path}")
    return out


def _has_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


# ------------------------- Gemini -------------------------


def generate_frame(beat_prompt, reference_images, preset, api_key, model):
    """Single REST call to Gemini with multi-image character references. Returns PNG bytes."""
    parts = [{"text": beat_prompt}]
    for label, path in reference_images:
        mime, data = encode_image(path)
        parts.append({"text": f"Reference image — {label}:"})
        parts.append({"inlineData": {"mimeType": mime, "data": data}})

    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": ASPECT},
        },
    }
    url = f"{API_BASE}/{model}:generateContent?key={api_key}"
    data = json.dumps(body).encode("utf-8")

    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, data=data, headers={"Content-Type": "application/json"}, method="POST"
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            if e.code == 429 and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue
            if "FAILED_PRECONDITION" in err_body:
                fail("Billing not enabled. Enable at https://aistudio.google.com/apikey",
                     status=400)
            fail(f"Gemini HTTP {e.code}: {err_body[:400]}", status=e.code)
        except urllib.error.URLError as e:
            fail(f"Network error: {e.reason}")
    else:
        fail("Max retries exceeded for Gemini call")

    candidates = result.get("candidates", [])
    if not candidates:
        reason = result.get("promptFeedback", {}).get("blockReason", "UNKNOWN")
        fail(f"Gemini returned no candidates. blockReason: {reason}")

    for part in candidates[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])

    finish_reason = candidates[0].get("finishReason", "UNKNOWN")
    fail(f"Gemini returned no image. finishReason: {finish_reason}. "
         "If IMAGE_SAFETY, try less violent/dramatic phrasing.")


# ------------------------- Composition -------------------------


def compose_storyboard(frame_pngs, beats, brand_name, output_path):
    """Composite 3 portrait frames side-by-side on a 1920x1080 cream canvas
    with a thin hi-vis yellow border and a small yellow brand footer."""
    # Start with the canvas painted yellow, then paint the cream interior on top.
    # Result: an 8-px yellow border around the entire canvas with cream inside.
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), HIVIS_YELLOW)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [BORDER_PX, BORDER_PX, CANVAS_W - BORDER_PX, CANVAS_H - BORDER_PX],
        fill=CREAM_BG,
    )

    try:
        caption_font = ImageFont.truetype(str(FONT_PATH), 28)
        footer_font = ImageFont.truetype(str(FONT_PATH), 26)
    except (OSError, IOError):
        caption_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    labels = ["1. Setup", "2. Action", "3. Resolution"]
    caption_max_w = FRAME_W - 32  # 16 px text padding on each side
    y_frame = BORDER_PX + TOP_GAP
    y_caption = y_frame + FRAME_H
    x = BORDER_PX + OUTER_PAD

    for idx, png_bytes in enumerate(frame_pngs):
        # Frame artwork
        frame = Image.open(__import__("io").BytesIO(png_bytes)).convert("RGB")
        frame = frame.resize((FRAME_W, FRAME_H), Image.LANCZOS)
        canvas.paste(frame, (x, y_frame))

        # Caption strip directly under the frame
        draw.rectangle([x, y_caption, x + FRAME_W, y_caption + CAPTION_H], fill=NAVY)
        lines = _wrap_caption(draw, labels[idx], beats[idx],
                              caption_font, caption_max_w, max_lines=2)
        total_h = len(lines) * CAPTION_LINE_H
        first_line_y = y_caption + (CAPTION_H - total_h) // 2 - 2
        for i, line in enumerate(lines):
            draw.text((x + 16, first_line_y + i * CAPTION_LINE_H),
                      line, fill=WHITE, font=caption_font)

        x += FRAME_W + GUTTER

    # Footer brand strip — sits flush against the bottom border (both yellow,
    # so they read as a single 56-px brand strip with the wordmark centred).
    footer_y = CANVAS_H - BORDER_PX - FOOTER_H
    draw.rectangle([0, footer_y, CANVAS_W, CANVAS_H], fill=HIVIS_YELLOW)
    bbox = draw.textbbox((0, 0), brand_name, font=footer_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((CANVAS_W - tw) // 2, footer_y + (FOOTER_H - th) // 2),
              brand_name, fill=NAVY, font=footer_font)

    canvas.save(output_path, "PNG", optimize=True)


# ------------------------- Trello -------------------------


def trello_attach(card_id, file_path):
    """Multipart upload of a file to a Trello card. Returns the attachment URL or raises."""
    api_key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")
    if not (api_key and token):
        return None, "TRELLO_API_KEY or TRELLO_TOKEN not set"

    boundary = f"----storyboard{uuid.uuid4().hex}"
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'
        "Content-Type: image/png\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"https://api.trello.com/1/cards/{card_id}/attachments?key={api_key}&token={token}"
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("url"), None
    except urllib.error.HTTPError as e:
        return None, f"Trello HTTP {e.code}: {e.read().decode('utf-8')[:200]}"
    except urllib.error.URLError as e:
        return None, f"Trello network error: {e.reason}"


# ------------------------- Cost log -------------------------


def log_cost(model, prompt_summary):
    if not COST_TRACKER.exists():
        return
    try:
        subprocess.run(
            ["python3", str(COST_TRACKER), "log",
             "--model", model, "--resolution", RESOLUTION,
             "--prompt", prompt_summary[:100]],
            capture_output=True, check=False,
        )
    except Exception:
        pass  # cost logging is best-effort


# ------------------------- Main -------------------------


def main():
    p = argparse.ArgumentParser(description="Generate a 3-frame storyboard.")
    p.add_argument("--prompt", required=True, help="Narrative for the 3 beats")
    p.add_argument("--client", default="diggerlid", help="Client preset name")
    p.add_argument("--source", action="append", default=[],
                   help="Source image or video (repeatable)")
    p.add_argument("--trello-card-id", default=None, help="Trello card ID for attachment")
    p.add_argument("--api-key", default=None, help="Google AI API key (or env GOOGLE_AI_API_KEY)")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = p.parse_args()

    api_key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        fail("No API key. Set GOOGLE_AI_API_KEY or pass --api-key.")

    preset = load_preset(args.client)
    founders = discover_founders(args.client)
    if len(founders) < 2:
        fail(
            f"Need 2 founder portraits at clients/assets/{args.client}/founders/founder-a.* "
            f"and founder-b.*. Found: {len(founders)}.",
            setup_required=True,
        )
    machine = discover_machine(args.client)

    # Resolve source media (extract a frame if a video was dropped)
    extra_refs = []
    for src in args.source:
        path = Path(src).expanduser().resolve()
        if not path.exists():
            fail(f"Source not found: {path}")
        if path.suffix.lower() in (".mp4", ".mov", ".mkv", ".webm"):
            path = extract_video_frame(path)
        extra_refs.append(("source context image", path))

    # Build reference image set: founders first, then machine (optional), then extras
    reference_images = list(founders)
    if machine:
        reference_images.append(machine)
    reference_images.extend(extra_refs)

    beats = split_beats(args.prompt)
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate 3 frames
    style_descriptor = _strip_color_cues(preset.get("style", ""))
    anchors = load_founder_anchors(args.client)
    anchor_clause = ""
    if anchors:
        bits = [f"**{name}** — {text}" for name, text in anchors.items()]
        anchor_clause = (
            "\n\nPersistent characters (preserve these traits exactly across all frames, "
            "even when the beat changes pose, action, or setting):\n" + "\n".join(bits)
        )
    machine_clause = (
        " Persistent object: the same compact mini-excavator with its dark protective "
        "canopy mounted on the operator cab, as in the reference image."
    )
    frame_pngs = []
    for idx, beat in enumerate(beats):
        beat_prompt = (
            f"{PENCIL_STYLE}\n\n"
            f"Beat {idx+1} of 3 — {beat}.\n\n"
            "SETTING PRECEDENCE: take the location and environment cues directly "
            "from the beat sentence above. If the beat names a specific place "
            "(bush, beach, warehouse, depot, indoors, etc.) render THAT place. "
            "Do NOT default to the brand's typical environment when the beat "
            "specifies a different one.\n\n"
            f"Brand visual identity (apply only when the beat doesn't fix a "
            f"different setting): {style_descriptor[:500]}.\n"
            f"{machine_clause}{anchor_clause}\n\n"
            "RENDER MODE OVERRIDE: any colour words appearing above (orange, "
            "yellow, navy, etc.) are identifying labels only — they describe what "
            "the brand looks like in real life. For THIS render the artwork is "
            "fully monochrome graphite pencil — no colour fills, no orange paint, "
            "no yellow accents. Pencil tones only across every object and figure. "
            "Do NOT render any logos, brand names, or printed text on the machine "
            "or in the scene."
        )
        png_bytes = generate_frame(beat_prompt, reference_images, preset, api_key, args.model)
        frame_pngs.append(png_bytes)
        log_cost(args.model, f"storyboard {args.client} beat {idx+1}: {beat[:60]}")

    # Compose
    slug = re.sub(r"[^a-z0-9]+", "-", args.prompt.lower())[:40].strip("-") or "storyboard"
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = output_dir / f"{today}-storyboard-{slug}.png"
    brand_name = preset.get("name", args.client).upper()
    compose_storyboard(frame_pngs, beats, brand_name, output_path)

    # Trello (optional)
    trello_url, trello_err = (None, None)
    if args.trello_card_id:
        trello_url, trello_err = trello_attach(args.trello_card_id, output_path)

    print(json.dumps({
        "ok": True,
        "path": str(output_path),
        "beats": beats,
        "frames": len(frame_pngs),
        "model": args.model,
        "resolution": RESOLUTION,
        "trello_url": trello_url,
        "trello_error": trello_err,
    }, indent=2))


if __name__ == "__main__":
    main()
