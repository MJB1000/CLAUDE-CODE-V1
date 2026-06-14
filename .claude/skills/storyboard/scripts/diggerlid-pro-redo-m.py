#!/usr/bin/env python3
"""Frame M v3 redo — uses the actual DiggerLid logo as a Gemini image reference
so the wordmark renders faithfully (not Gemini's approximation).
"""
import base64, json, os, sys, time, urllib.error, urllib.request, zipfile
from pathlib import Path

REPO = Path("/home/user/CLAUDE-CODE-V1")
LOGO = REPO / "clients/assets/diggerlid/logo-primary.png"
OUT_DIR = REPO / "deliverables" / "diggerlid-pro-storyboard"
ZIP_PATH = REPO / "deliverables" / "diggerlid-pro-storyboard.zip"
MODEL = "gemini-3.1-flash-image-preview"
ASPECT = "9:16"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

PROMPT = """RENDER MODE — STRICT BLACK AND WHITE PENCIL SKETCH base, with two specific colour accents allowed: DiggerLid yellow (#f5eb19) on the logo strikethrough bar AND on the cab tie-down tether points. Everything else in the artwork must be pure pencil monochrome.

Persistent style: soft graphite pencil sketch on warm cream sketchbook paper, loose hand-drawn marker lines, minimal shading. 9:16 vertical aspect. One frame from a 12-frame series for a single 45-second ad.

LOGO REFERENCE — the DiggerLid wordmark/logo lockup attached as a reference image is the OFFICIAL company logo: a horizontal black bar containing the white "DiggerLid" wordmark with a thick DiggerLid-yellow horizontal strikethrough bar across the upper portion of the letterforms, plus a small ® registered mark at the end. Render the lockup in storyboard sketch style faithfully matching the structure of the reference: same letter spacing, same yellow strikethrough position cutting through the upper portion of the letters, same ® placement.

[Context] Brand outro — DiggerLid wordmark and tagline lockup over the surviving covered cab from Beat L.
[Visual] Tight medium shot of an excavator cab fitted with the grey 490 GSM ripstop DiggerLid PRO Enclosure cover (cover rendered in pencil monochrome). DiggerLid-branded tie-down tether points are visible around the cab — render these tether points in DiggerLid yellow as small accent details. Across the lower third of the frame: the horizontal DiggerLid wordmark/logo lockup as shown in the reference image — black bar background, white "DiggerLid" letterforms with the thick DiggerLid yellow strikethrough across the upper portion of the letters, small ® at the end. Below the logo bar, the tagline "WE'RE DIGGIN' IT!" in a distressed grunge stamp typeface, slightly weathered, in solid black ink.
[Format] 9:16 vertical aspect ratio, edge-to-edge composition.
[Style] Black-and-white storyboard sketch base. The only colours allowed: DiggerLid yellow #f5eb19 on the logo strikethrough bar and on the small tie-down tether-point accents on the cab. Everything else in pencil monochrome.
"""

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate(prompt, refs, api_key):
    parts = [{"text": prompt}]
    for label, p in refs:
        parts.append({"text": f"Reference image — {label}:"})
        parts.append({"inlineData": {"mimeType": "image/png", "data": encode_image(p)}})
    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": ASPECT}},
    }
    url = f"{API_BASE}/{MODEL}:generateContent?key={api_key}"
    data = json.dumps(body).encode("utf-8")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=180) as r:
                result = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(2 ** (attempt+1)); continue
            sys.exit(f"HTTP {e.code}: {e.read().decode()[:300]}")
    for part in result.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    sys.exit(f"No image returned: {json.dumps(result)[:500]}")

api_key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key: sys.exit("GOOGLE_AI_API_KEY not set")

out = OUT_DIR / "12-M-tagline-drop.png"
print(f"Generating Frame M v3 with logo reference...")
png = generate(PROMPT, [("DiggerLid logo lockup", LOGO)], api_key)
out.write_bytes(png)
print(f"  -> {out} ({len(png):,} bytes)")

# Rebuild zip with all 12 frames
ORDER = [("A",1),("B",2),("C",3),("D",4),("E1",5),("E2",6),("F",7),("G",8),("H",9),("I",10),("L",11),("M",12)]
saved = []
for bid, idx in ORDER:
    for p in OUT_DIR.iterdir():
        if p.is_file() and p.name.startswith(f"{idx:02d}-{bid}-"):
            saved.append(p); break
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
    for p in saved:
        z.write(p, arcname=p.name)
print(f"\nZip rebuilt: {ZIP_PATH} ({ZIP_PATH.stat().st_size:,} bytes), {len(saved)}/12 frames")
