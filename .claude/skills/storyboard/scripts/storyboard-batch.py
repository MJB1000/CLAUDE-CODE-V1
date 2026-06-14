#!/usr/bin/env python3
"""storyboard-batch.py — manifest-driven multi-frame storyboard generator.

Generate a numbered sequence of standalone storyboard frames from a JSON
manifest. The manifest is the persistent source of truth: it holds every
frame's prompt, reference images, and resolution. Because the manifest
persists, you can regenerate ONE frame at a time without re-running the
whole set or re-typing its prompt.

USAGE
  # Generate / regenerate the whole sequence
  storyboard-batch.py --manifest path/to/frames.json

  # Regenerate ONLY frame 7 (after editing frame 7's prompt in the manifest)
  storyboard-batch.py --manifest path/to/frames.json --frame 7

  # Frame 7 can be addressed by number (7) or by beat id (F)
  storyboard-batch.py --manifest path/to/frames.json --frame F

  # Regenerate every frame inside a single beat group (only valid when the
  # manifest is organised under "beats"). Useful for re-rendering "Act 2"
  # without touching the rest.
  storyboard-batch.py --manifest path/to/frames.json --beat act-2-cover

  # Resolution: 1K default. Opt into HQ per run.
  storyboard-batch.py --manifest path/to/frames.json --frame 7 --resolution 2K

PER-FRAME EDIT WORKFLOW
  1. Open the manifest JSON, find the frame (by "n" or "id").
  2. Edit its "prompt" string (or its "refs"/"resolution").
  3. Run with --frame <n>. Only that PNG is regenerated; the zip is rebuilt.

MANIFEST SCHEMA
  Two equivalent shapes — flat or beat-grouped. Beat-grouped is preferred
  because it powers both `--beat <id>` filtering here AND the beat-section
  pagination in pdf-export.py from the same single file.

  Flat shape:
  {
    "project": "diggerlid-pro-storyboard",
    "output_dir": "deliverables/diggerlid-pro-storyboard",
    "default_resolution": "1K",          # 512 | 1K | 2K | 4K
    "aspect": "9:16",
    "asset_refs": {                      # named reference images
      "founder-a": "clients/assets/diggerlid/founders/founder-a.jpg",
      "logo":      "clients/assets/diggerlid/logo-primary.png"
    },
    "auto_refs": [                       # OPTIONAL: content-triggered ref rules
      {
        "id": "product-enclosure",
        "triggers": ["diggershield", "pro enclosure"],
        "refs": ["product-enclosure-1", "product-enclosure-2"]
      }
    ],
    "frames": [
      {
        "n": 1,                          # frame number (1-based, stable)
        "id": "A",                       # short beat id
        "slug": "hero-hook",             # filename slug
        "refs": ["founder-a"],           # explicit keys into asset_refs
        "skip_auto_refs": false,         # OPTIONAL: opt out of auto_refs
        "resolution": null,              # null = use default_resolution
        "prompt": "<full self-contained prompt>",
        "title":   "HERO HOOK",          # OPTIONAL: PDF display title
        "caption": "XE17U lands clean."  # OPTIONAL: PDF one-line caption
      }
    ]
  }

  Beat-grouped shape (preferred):
  {
    "project": ..., "output_dir": ..., "default_resolution": ...,
    "aspect": ..., "asset_refs": {...}, "auto_refs": [...],
    "beats": [
      {
        "id": "act-1-arrival",
        "title": "ACT 1 — ARRIVAL",
        "description": "The machine arrives.",     # OPTIONAL
        "frames": [
          { "n": 1, "id": "A1", "slug": "pallet-stop", "refs": [],
            "prompt": "...", "title": "PALLET STOP",
            "caption": "XE17U dragged to a stop." },
          ...
        ]
      },
      { "id": "act-2-cover", "title": "ACT 2 — THE COVER",
        "frames": [...] }
    ]
  }

  Beat-grouped manifests are auto-flattened into a "frames" list on load,
  preserving each frame's parent beat id (in the internal "_beat" field).

AUTO_REFS
  Each auto_ref rule scans every frame's prompt for any of its trigger words
  (case-insensitive substring match). When a rule matches, its `refs` are
  added to that frame's effective reference image list (deduplicated against
  the frame's explicit `refs`). Auto-refs whose asset key is not registered
  in `asset_refs` are silently skipped — the rule stays DORMANT until you
  populate the asset. This lets you wire the rule up before pushing assets;
  the moment the asset key appears in `asset_refs`, the rule starts firing.

Output files are named `<NN>-<id>-<slug>.png` (zero-padded). The zip is
`<output_dir>.zip`.
"""

import argparse
import base64
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MODEL = "gemini-3.1-flash-image-preview"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
VALID_RESOLUTIONS = {"512", "1K", "2K", "4K"}
COST_TRACKER = Path.home() / ".claude" / "skills" / "banana" / "scripts" / "cost_tracker.py"


def fail(msg, **extra):
    payload = {"error": True, "message": msg}
    payload.update(extra)
    print(json.dumps(payload), file=sys.stderr)
    sys.exit(1)


def resolve_path(p):
    """Resolve a manifest path: absolute as-is, else relative to the repo root."""
    path = Path(p)
    return path if path.is_absolute() else (REPO_ROOT / path)


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_frame(prompt, ref_pairs, aspect, resolution, api_key):
    """One Gemini generateContent call. ref_pairs is [(label, Path), ...]."""
    parts = [{"text": prompt}]
    for label, path in ref_pairs:
        path = Path(path)
        if not path.exists():
            fail(f"Reference image not found: {path}")
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        parts.append({"text": f"Reference image — {label}:"})
        parts.append({"inlineData": {"mimeType": mime, "data": encode_image(path)}})

    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            # imageSize is the real resolution lever — must be uppercase.
            "imageConfig": {"aspectRatio": aspect, "imageSize": resolution},
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
            with urllib.request.urlopen(req, timeout=240) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            if e.code == 429 and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue
            if "FAILED_PRECONDITION" in err_body:
                fail("Billing not enabled. Enable at https://aistudio.google.com/apikey")
            fail(f"Gemini HTTP {e.code}: {err_body[:400]}")
        except urllib.error.URLError as e:
            fail(f"Network error: {e.reason}")
    else:
        fail("Max retries exceeded")

    for part in result.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    reason = result.get("candidates", [{}])[0].get("finishReason", "UNKNOWN")
    fail(f"No image returned (finishReason={reason}). "
         "If IMAGE_SAFETY, rephrase the frame's prompt in the manifest.")


def log_cost(resolution, summary):
    if not COST_TRACKER.exists():
        return
    try:
        subprocess.run(
            ["python3", str(COST_TRACKER), "log",
             "--model", MODEL, "--resolution", resolution,
             "--prompt", summary[:100]],
            capture_output=True, check=False,
        )
    except Exception:
        pass


def rebuild_zip(output_dir):
    zip_path = output_dir.parent / f"{output_dir.name}.zip"
    pngs = sorted(p for p in output_dir.iterdir() if p.is_file() and p.suffix == ".png")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in pngs:
            z.write(p, arcname=p.name)
    return zip_path, len(pngs)


def main():
    ap = argparse.ArgumentParser(description="Manifest-driven storyboard frame generator")
    ap.add_argument("--manifest", required=True, help="Path to the frames manifest JSON")
    ap.add_argument("--frame", default=None,
                    help="Regenerate only this frame (number or id). Omit for the full set.")
    ap.add_argument("--beat", default=None,
                    help="Regenerate every frame inside this beat group (id from beats[].id). "
                         "Only valid for manifests that use the beats shape.")
    ap.add_argument("--resolution", default=None,
                    help="Override resolution: 512 | 1K | 2K | 4K. Default: manifest default_resolution or 1K.")
    ap.add_argument("--api-key", default=None, help="Google AI API key (or env GOOGLE_AI_API_KEY)")
    args = ap.parse_args()

    import os
    api_key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        fail("No API key. Set GOOGLE_AI_API_KEY or pass --api-key.")

    manifest_path = resolve_path(args.manifest)
    if not manifest_path.exists():
        fail(f"Manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if args.resolution and args.resolution not in VALID_RESOLUTIONS:
        fail(f"Invalid resolution '{args.resolution}'. Valid: {sorted(VALID_RESOLUTIONS)}")

    default_res = manifest.get("default_resolution", "1K")
    aspect = manifest.get("aspect", "9:16")
    asset_refs = manifest.get("asset_refs", {})
    output_dir = resolve_path(manifest["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Auto-flatten "beats" shape into a "frames" list, tagging each frame with
    # its parent beat id so --beat filtering works.
    if "beats" in manifest and "frames" not in manifest:
        flat = []
        for beat in manifest["beats"]:
            for fr in beat.get("frames", []):
                fr.setdefault("_beat", beat.get("id"))
                flat.append(fr)
        manifest["frames"] = flat
    frames = manifest["frames"]

    # Select which frames to generate
    if args.frame is not None:
        target = str(args.frame).strip()
        selected = [f for f in frames
                    if str(f.get("n")) == target or str(f.get("id")).upper() == target.upper()]
        if not selected:
            available = ", ".join(f"{fr['n']}/{fr['id']}" for fr in frames)
            fail(f"No frame matching '{args.frame}'. Available: {available}")
    elif args.beat is not None:
        target = args.beat.strip()
        selected = [f for f in frames if str(f.get("_beat", "")) == target]
        if not selected:
            beats = ", ".join(b.get("id", "?") for b in manifest.get("beats", []))
            fail(f"No frames inside beat '{args.beat}'. Available beats: {beats or '(none — manifest has no beats)'}")
    else:
        selected = frames

    results = []
    for f in selected:
        n, fid, slug = f["n"], f["id"], f["slug"]
        resolution = args.resolution or f.get("resolution") or default_res

        # Explicit refs from the frame entry (strict — fail if key unknown)
        explicit_refs = list(f.get("refs", []))

        # Auto-applied refs from manifest-level rules that match the prompt.
        # Each rule: {"id": "...", "triggers": ["word1", ...], "refs": ["asset-key", ...]}
        # A rule fires when ANY trigger word appears (case-insensitive) in the
        # frame's prompt. Auto-refs whose asset key is not yet registered are
        # silently skipped — the rule stays dormant until you add the asset.
        # Set per-frame "skip_auto_refs": true to opt a single frame out.
        auto_applied = []
        auto_dormant = []
        if not f.get("skip_auto_refs", False):
            prompt_lower = f["prompt"].lower()
            for rule in manifest.get("auto_refs", []):
                triggers = [t.lower() for t in rule.get("triggers", [])]
                if any(t in prompt_lower for t in triggers):
                    for k in rule.get("refs", []):
                        if k in explicit_refs or k in auto_applied:
                            continue
                        if k in asset_refs:
                            auto_applied.append(k)
                        else:
                            auto_dormant.append(k)

        ref_pairs = []
        for key in explicit_refs:
            if key not in asset_refs:
                fail(f"Frame {n} ({fid}) references unknown asset '{key}'. "
                     f"Known: {sorted(asset_refs)}")
            ref_pairs.append((key, resolve_path(asset_refs[key])))
        for key in auto_applied:
            ref_pairs.append((key, resolve_path(asset_refs[key])))

        ref_summary = ", ".join(k for k, _ in ref_pairs) if ref_pairs else "no refs"
        auto_note = f"  [auto: {','.join(auto_applied)}]" if auto_applied else ""
        dormant_note = f"  [dormant auto-refs: {','.join(auto_dormant)}]" if auto_dormant else ""
        print(f"[{n:02d}/{fid}] {slug} — {resolution}, {ref_summary}{auto_note}{dormant_note}",
              flush=True)

        png = generate_frame(f["prompt"], ref_pairs, aspect, resolution, api_key)
        out = output_dir / f"{n:02d}-{fid}-{slug}.png"
        out.write_bytes(png)
        log_cost(resolution, f"{manifest.get('project','storyboard')} frame {n} {fid}")
        results.append({"n": n, "id": fid, "path": str(out), "resolution": resolution,
                        "auto_refs_applied": auto_applied, "bytes": len(png)})
        print(f"  saved {out.name} ({len(png):,} bytes)", flush=True)

    zip_path, count = rebuild_zip(output_dir)

    print(json.dumps({
        "ok": True,
        "regenerated": results,
        "frames_in_zip": count,
        "zip": str(zip_path),
        "output_dir": str(output_dir),
    }, indent=2))


if __name__ == "__main__":
    main()
