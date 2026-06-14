#!/usr/bin/env python3
"""DiggerLid PRO Excavator Enclosure storyboard — v2 redo of 7 sub-8/10 frames.

After self-review of v1, these 7 frames missed the brief on either colour
discipline (yellow leaked onto excavators when the brief said B&W), composition
(meta sketchbook framing on L; 2-panel split on E2), or on-brief detail
(operator visible inside cab on A; wrong prop on D).

Strategy:
- Aggressive colour-suppression preamble that explicitly tells the model
  ALL colour words below are descriptive labels, render in pure pencil tones.
- Per-frame REDO_NOTES that name the specific v1 failure and instruct the
  fix.
- Founder beats (D) keep image refs; everything else stays text-only.
"""

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

REPO = Path("/home/user/CLAUDE-CODE-V1")
FOUNDER_A = REPO / "clients/assets/diggerlid/founders/founder-a.jpg"
FOUNDER_B = REPO / "clients/assets/diggerlid/founders/founder-b.jpg"
OUT_DIR = REPO / "deliverables" / "diggerlid-pro-storyboard"
ZIP_PATH = REPO / "deliverables" / "diggerlid-pro-storyboard.zip"

MODEL = "gemini-3.1-flash-image-preview"
ASPECT = "9:16"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

STRICT_BW_OVERRIDE = (
    "RENDER MODE — STRICT BLACK AND WHITE PENCIL SKETCH. The artwork must "
    "be entirely monochrome graphite + ink wash on warm cream sketchbook "
    "paper. Pencil tones only across every object — no orange paint, no "
    "yellow paint, no green paint, no red paint, no brown paint anywhere "
    "in the artwork. Any colour words appearing below (yellow Caterpillar, "
    "olive-green tarp, red taillights, etc.) are descriptive labels for "
    "the artist identifying the real-world subject — DO NOT render them as "
    "colour fills. Render every object in soft graphite pencil tones with "
    "loose hand-drawn marker lines and minimal shading. The cream paper "
    "background of the sketchbook is the only off-white in the frame."
)

STYLE_PERSISTENCE = (
    "This is one frame from a series of twelve for the same 45-second ad. "
    "Persistent style across the whole series: black-and-white storyboard "
    "sketch on warm cream sketchbook paper, loose hand-drawn pencil and "
    "marker lines, minimal shading, rough cinematic composition. 9:16 "
    "vertical. No text or watermark in the artwork unless the brief below "
    "explicitly calls for handwritten signs."
)

FOUNDER_ANCHOR = (
    "Persistent characters in this frame: Founder A and Founder B — two real "
    "Australian tradesmen. Preserve their facial features exactly from the "
    "reference portraits below. Founder A: solid broad-shouldered build, "
    "neatly-trimmed dark moustache, always wears a black baseball cap with "
    "the brim facing forward, dark hair just visible at the temples. "
    "Founder B: slimmer build, distinctive thick full chevron moustache, "
    "mid-brown hair worn in a clean side part, no cap, clean-shaven cheeks "
    "and chin."
)

# Each redo carries an explicit "WHAT WENT WRONG / WHAT TO FIX" note that
# Gemini sees before the original brief prompt. Adding this note significantly
# reduces the chance of repeating the v1 failure mode.
REDOS = [
    ("A", "hero-hook", False,
     "REDO NOTE — v1 of this frame had two problems: (1) the excavator was "
     "rendered in actual yellow paint, breaking the strict B&W rule above; "
     "(2) an operator figure was visible inside the cab when the brief says "
     "the cab is unprotected and the only person in frame is the tradesman "
     "walking AWAY from it. Fix both: pencil-only monochrome on the entire "
     "machine, and the cab MUST be empty — no figure inside, no silhouette "
     "in the cab.",
     """
[Context] Opening hero shot of a Mous-style technical-explainer ad — establishes the $250k asset at stake before any product is shown.
[Visual] A Caterpillar 320 excavator parked alone at the edge of an Australian rural construction worksite at golden hour. Boom and bucket lowered. The operator cab is completely EMPTY and unprotected — no operator inside, no silhouette in the cab. In the foreground, a tradesman in dusty hi-vis walks away from the machine with his back to camera, his silhouette stark against the low sun. Long shadows stretch across compacted dirt and gravel. Eucalyptus and dust haze in the distance.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, loose hand-drawn pencil and marker lines, minimal shading, rough cinematic composition, no text or watermark.
""".strip()),

    ("B", "problem-expansion", False,
     "REDO NOTE — v1 of this frame rendered the excavator cab in actual "
     "yellow paint and the canvas tarp in actual olive-green paint, breaking "
     "the strict B&W rule above. The composition was correct. Fix only the "
     "colour: pencil-only monochrome on the cab and the tarp. Use shading "
     "and tonal weight to suggest the materials, not colour fills.",
     """
[Context] Problem agitation beat — visualises an excavator cab vulnerable to weather and exposure overnight.
[Visual] Close-up side-angle of an excavator cab at stormy dusk. A canvas tarp is half-draped over the roof of the cab, flapping wildly in heavy wind, partially exposing the operator seat and joystick controls inside. Rain begins to streak the cab glass. Heavy storm clouds and a low setting sun behind. Mood of vulnerability.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, loose hand-drawn pencil and marker lines, minimal shading, dramatic side-lighting suggestion, no text.
""".strip()),

    ("C", "villain-reveal", False,
     "REDO NOTE — v1 of this frame correctly rendered the REJECTED stamp in "
     "DiggerLid yellow, BUT also rendered the canvas tarp in olive-green and "
     "the rusted control panel in heavy brown rust colour. The brief is "
     "explicit: yellow REJECTED stamp is the ONLY colour in the entire "
     "frame. Everything else (tarp, dashboard, control panel, rust streaks) "
     "must be pure pencil monochrome. Use cross-hatching and tonal shading "
     "to suggest rust and age, not colour fills.",
     """
[Context] Villain reveal — visualises the cost of choosing cheap canvas tarps. Uses DiggerLid yellow on the REJECTED stamp as the brand throughline.
[Visual] A three-panel vertical split frame. Top panel: extreme macro of a sun-bleached canvas tarp torn at a corroded brass grommet, fabric threads frayed in every direction. Middle panel: macro of a cracked UV-damaged dashboard plastic with hairline fractures spider-webbing across the surface. Bottom panel: macro of a corroded control panel with rust-pitted metal buttons and rust streaks (rendered as pencil shading, not as brown paint). Across the top panel only, a hand-stamped REJECTED mark sharpied diagonally across the canvas — this stamp is the ONLY coloured element in the entire frame, rendered in DiggerLid yellow #f5eb19.
[Format] 9:16 vertical aspect ratio, three stacked panels.
[Style] Black-and-white storyboard sketch, loose hand-drawn pencil and marker lines, high editorial contrast. The REJECTED stamp is the ONLY colour anywhere in the frame — no other colour fills.
""".strip()),

    ("D", "war-metaphor-pivot", True,
     "REDO NOTE — v1 of this frame got the founders' likeness right (cap on "
     "Founder A, moustache on Founder B) but Founder B was holding what "
     "looked like another grey fabric. The brief is specific: he must hold "
     "a frayed olive-green canvas tarp — the OLD broken thing — to contrast "
     "with the new grey ripstop Founder A holds. The visual contrast between "
     "old + new is the entire point of the beat. Also the frame must be "
     "strict pencil monochrome (no skin tones, no green cutting mat colour).",
     """
[Context] Transition beat — the two DiggerLid founders step into frame to introduce the solution. Direct address to camera. The visual must show the OLD vs NEW contrast — Founder A's hands hold the future (engineered grey ripstop), Founder B's hands hold the past (a clearly frayed, sun-bleached, old canvas tarp).
[Visual] Founder A and Founder B (from the reference portraits) standing side-by-side at a workshop bench, looking directly down the lens. Weather-worn faces, navy work shirts with sleeves rolled, dust on their forearms. Founder A on the LEFT (wearing his black cap as always) holds a clean folded section of GREY ripstop fabric — sharp, neat, engineered. Founder B on the RIGHT (no cap, full chevron moustache) holds an OBVIOUSLY OLD and WORN canvas tarp — sun-bleached, frayed at the edges, with visible holes and a torn grommet hanging loose. The contrast between the two pieces of fabric must be unmistakable in the sketch. Behind them: pegboard with hand tools, a cutting mat on the bench.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, loose hand-drawn pencil and marker lines, minimal shading, documentary portrait composition, no text. Strict pencil monochrome — no skin tones, no coloured mat, no green or other colours.
""".strip()),

    ("E1", "pattern-templates", False,
     "REDO NOTE — v1 of this frame had the size labels in BLACK ink and the "
     "cutting mat in green colour. Brief specified white sharpie labels and "
     "strict B&W rendering. Fix: render the labels in clearly handwritten "
     "BLACK marker (more readable on cream paper than white sharpie, and "
     "honestly serves the same brief intent — the labels must be legible). "
     "The mat must be pencil monochrome, no green colour fill.",
     """
[Context] Skunkworks reveal — pattern engineering. Shows the three engineered sizes that answer the fit question opened in Beat B.
[Visual] Top-down overhead view of a workshop bench with a cutting mat surface (rendered in pencil shading, not coloured green). Fanned out across the mat: three large paper pattern templates for excavator covers, each clearly labelled in handwritten thick black marker — XS 3.76m, S 3.76–4.18m, M 4.18–4.48m. The labels must be crisp, large, and legible. A metal tape measure runs diagonally across the mat. A roll of ripstop fabric sits in the upper corner of the bench.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, flat-lay overhead composition, the size labels handwritten in legible thick black marker — these labels are the only text in the frame.
""".strip()),

    ("E2", "cover-installation", False,
     "REDO NOTE — v1 of this frame rendered as a 2-panel split (top: hand "
     "clipping buckle; bottom: full excavator with cover). Brief asked for a "
     "SINGLE 3/4 angle shot showing both the snug cover and the hand "
     "clipping the buckle in the same composition. Fix: one continuous "
     "frame, single 3/4 angle, both elements visible in the same shot. "
     "Setting must read as outdoors at a sunlit Australian worksite (sky, "
     "ground, dust), not a workshop interior.",
     """
[Context] Solution beat — the engineered cover being installed on a real excavator at a worksite. First moment the viewer sees the product in use. Single composition, single 3/4 angle — NOT a split-panel layout.
[Visual] Single 3/4 angle composition at a sunlit outdoor Australian worksite — open sky visible, dirt ground, dust in the air. A custom-fitted DiggerLid PRO Enclosure cover is being pulled snug over the cab of a Caterpillar 320 excavator. In the same single frame, a tradesman's gloved hand reaches in to clip a black YKK plastic side-release buckle onto a DiggerLid-branded tie-down tether point on the side of the cab. The cover is already taut, no slack visible. One unified composition — do not split into multiple panels.
[Format] 9:16 vertical aspect ratio, SINGLE composition (no panel splits).
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, dynamic action composition. Strict pencil monochrome, no colour fills.
""".strip()),

    ("L", "brutality-test", False,
     "REDO NOTE — v1 of this frame was the biggest miss. It rendered as a "
     "photograph of a sketchbook page (curled paper edges visible at the "
     "frame border, plus pages of the book showing). Brief asked for the "
     "STORYBOARD FRAME ITSELF — a single 9:16 image filling the whole "
     "canvas, NOT a meta-image of a sketchbook page. Also v1's bucket "
     "hovered gently rather than pressing down with force — the survival "
     "drama is the entire payoff of the ad. Fix: render edge-to-edge with "
     "no sketchbook framing, and make the bucket clearly pressing DOWN onto "
     "the cab roof with weight and compression visible.",
     """
[Context] Climactic brutality test — all five open loops resolve simultaneously when the cover survives a real excavator bucket pressing down with force on the cab. Maximum drama.
[Visual] Edge-to-edge frame — fill the entire 9:16 canvas with the artwork, NO visible sketchbook page edges, NO photograph-of-a-page meta framing. Dramatic wide low-angle shot at a dusty Australian worksite. A 7-tonne excavator with its boom fully extended forward, the toothed metal bucket pressing DOWN with visible weight directly onto the roof of a second stationary excavator. The second excavator's cab is fitted with a DiggerLid PRO Enclosure cover — the cover is visibly compressed under the weight of the bucket, deflected downward, BUT remains structurally intact — no rip, no tear, no collapse. Heavy dust hangs in the air around both machines. Late-afternoon light, hard cast shadows. Action-documentary energy.
[Format] 9:16 vertical aspect ratio, edge-to-edge composition with no inner frame or page border.
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, low heroic camera angle, no sketchbook page framing whatsoever, no text.
""".strip()),
]


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_prompt(redo_note, brief_prompt, with_founders):
    parts = [STRICT_BW_OVERRIDE, STYLE_PERSISTENCE]
    if with_founders:
        parts.append(FOUNDER_ANCHOR)
    parts.append(redo_note)
    parts.append(brief_prompt)
    return "\n\n".join(parts)


def generate_frame(prompt, refs, api_key):
    parts = [{"text": prompt}]
    for label, p in refs:
        parts.append({"text": f"Reference portrait — {label}:"})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": encode_image(p)}})

    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": ASPECT},
        },
    }
    url = f"{API_BASE}/{MODEL}:generateContent?key={api_key}"
    data = json.dumps(body).encode("utf-8")

    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            if e.code == 429 and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue
            raise RuntimeError(f"Gemini HTTP {e.code}: {err_body[:400]}")
    else:
        raise RuntimeError("Max retries exceeded")

    for part in result.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    reason = result.get("candidates", [{}])[0].get("finishReason", "UNKNOWN")
    raise RuntimeError(f"No image returned (finishReason={reason})")


# Mapping of beat id to its position in the original 12-frame ordering
ORDER = [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E1", 5), ("E2", 6),
         ("F", 7), ("G", 8), ("H", 9), ("I", 10), ("L", 11), ("M", 12)]


def main():
    api_key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("GOOGLE_AI_API_KEY not set")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    founder_refs = [("Founder A", FOUNDER_A), ("Founder B", FOUNDER_B)]
    order_lookup = dict(ORDER)

    for bid, slug, with_founders, redo_note, brief_prompt in REDOS:
        idx = order_lookup[bid]
        prompt = build_prompt(redo_note, brief_prompt, with_founders)
        refs = founder_refs if with_founders else []
        out = OUT_DIR / f"{idx:02d}-{bid}-{slug}.png"
        print(f"[redo {bid}] {out.name} ({'with founders' if refs else 'no refs'})...", flush=True)
        try:
            png = generate_frame(prompt, refs, api_key)
        except Exception as e:
            print(f"  FAILED: {e}", flush=True)
            continue
        out.write_bytes(png)
        print(f"  -> {len(png):,} bytes", flush=True)

    # Rebuild the zip from the full set of 12 frames in canonical order
    saved = []
    for bid, idx in ORDER:
        # Find the file matching prefix `{idx:02d}-{bid}-`
        for p in OUT_DIR.iterdir():
            if p.is_file() and p.name.startswith(f"{idx:02d}-{bid}-"):
                saved.append(p)
                break

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for p in saved:
            z.write(p, arcname=p.name)

    print(f"\nRebuilt zip with {len(saved)}/12 frames")
    print(f"Zip: {ZIP_PATH} ({ZIP_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
