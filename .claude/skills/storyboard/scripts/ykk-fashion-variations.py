#!/usr/bin/env python3
"""Frame F — YKK fashion editorial, 3 variations to choose from.

Brief from user:
- Match the visual style of their reference (clean white seamless backdrop,
  full-body Australian/European designer-brand editorial, light wash relaxed
  denim, white tee, cognac suede shoes, considered minimalist).
- Model BLURRED out (face out of focus / soft figure).
- Sharp focus on the YKK zip at the front of the jeans.
- 9:16 vertical, fashion editorial style preserved.
"""
import base64, json, os, sys, time, urllib.error, urllib.request, zipfile
from pathlib import Path

REPO = Path("/home/user/CLAUDE-CODE-V1")
OUT_DIR = REPO / "deliverables" / "diggerlid-pro-storyboard-v6" / "07-F-variations"
ZIP_PATH = REPO / "deliverables" / "07-F-ykk-fashion-variations.zip"

MODEL = "gemini-3.1-flash-image-preview"
ASPECT = "9:16"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

SHARED_STYLE = (
    "Visual reference for all three variations: a clean minimalist Australian/European designer-brand "
    "fashion editorial. PURE WHITE seamless studio backdrop, no shadows on the wall behind the model. "
    "Model wears a soft, slightly-loose-fit pure white cotton crew-neck tee tucked at the waist over "
    "light wash medium-weight relaxed/wide-leg blue denim jeans with classic five-pocket construction "
    "and tonal contrast stitching, plus burnt-cognac suede flat shoes. Soft daylight lighting, even "
    "and shadow-free. Hair pulled back. Considered, premium, minimalist register. Hyperreal denim "
    "texture and stitching. The brass YKK zipper pull at the front fly of the jeans must be "
    "TACK-SHARP and clearly legible — embossed 'YKK' letters crisp on the brass tab, even when the "
    "model's body is out of focus. The model's face and upper body must be SOFT-FOCUSED OR BLURRED — "
    "anonymous, identity not readable. Premium magazine editorial palette: warm whites, light indigo "
    "denim, brass, cognac. 9:16 vertical aspect ratio."
)

VARIATIONS = [
    ("v1-full-body",
     "VARIATION 1 — full-body composition. Standing front-facing pose, full figure visible from head "
     "to feet, perfectly centred on the white backdrop. Hands relaxed at sides. Photographed with a "
     "shallow-depth-of-field 85mm lens with the focal plane sharp on the front fly zipper at hip "
     "height — the YKK brass pull is the hyper-sharp anchor of the frame. EVERYTHING else (face, "
     "torso, shoes, backdrop) softens into a creamy bokeh. The composition matches the reference "
     "of a clean Australian designer-brand lookbook page."),

    ("v2-waist-medium",
     "VARIATION 2 — medium shot from chest down to mid-thigh. Tighter than full body. Model "
     "standing front-facing, shown from sternum to upper thigh. The white tee fills the upper "
     "third of the frame; the jeans waistband and front fly fill the centre. Tack-sharp macro "
     "focus on the YKK brass zipper pull at the fly. The tee, waistband fabric, and any visible "
     "skin all softened into bokeh — everything except the YKK pull is OUT OF FOCUS. Studio "
     "backdrop also blurred behind. The brass YKK letters are unmistakably the only sharp thing."),

    ("v3-tight-zip-macro",
     "VARIATION 3 — tight three-quarter angle close-up cropped from upper thigh to lower belt "
     "line. The brass YKK zipper pull at the front fly fills approximately 25% of the frame, "
     "perfectly sharp with the embossed 'YKK' letters legible. The denim weave around the fly is "
     "in soft focus, getting dreamier toward the edges of the frame. A blur of the model's hand "
     "or thumb hovers near the pocket out of focus. Same minimalist editorial palette — clean "
     "denim wash, brass hardware, soft white backdrop visible at the edges."),
]

def generate(prompt, api_key):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": ASPECT}}}
    url = f"{API_BASE}/{MODEL}:generateContent?key={api_key}"
    data = json.dumps(body).encode("utf-8")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=180) as r:
                result = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 2:
                time.sleep(2 ** (attempt+1)); continue
            sys.exit(f"HTTP {e.code}: {e.read().decode()[:300]}")
    for part in result.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    sys.exit(f"No image returned: {json.dumps(result)[:500]}")

api_key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key: sys.exit("GOOGLE_AI_API_KEY not set")

OUT_DIR.mkdir(parents=True, exist_ok=True)
saved = []
for slug, var_text in VARIATIONS:
    full_prompt = SHARED_STYLE + "\n\n" + var_text
    out = OUT_DIR / f"07-F-ykk-fashion-{slug}.png"
    print(f"Generating {slug}...", flush=True)
    png = generate(full_prompt, api_key)
    out.write_bytes(png)
    saved.append(out)
    print(f"  -> {out.name} ({len(png):,} bytes)", flush=True)

with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
    for p in saved: z.write(p, arcname=p.name)
print(f"\nZip: {ZIP_PATH} ({ZIP_PATH.stat().st_size:,} bytes), {len(saved)}/3 variations")
