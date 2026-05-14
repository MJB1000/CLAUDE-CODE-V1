#!/usr/bin/env python3
"""DiggerLid PRO Excavator Enclosure — 45s Meta ad storyboard.

Generates all 12 standalone 9:16 B&W pencil/marker storyboard sketches per the
production brief. Beats D and I attach the two founder portraits as character
references; every other frame is text-only. Writes each PNG to
`deliverables/diggerlid-pro-storyboard/` with sequential naming and bundles a
zip of the whole folder for one-click download.
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

STYLE_PERSISTENCE = (
    "This is one frame from a series of twelve for the same 45-second ad. "
    "Persistent style across the whole series: black-and-white storyboard "
    "sketch on warm cream sketchbook paper, loose hand-drawn pencil and "
    "marker lines, minimal shading, rough cinematic composition. 9:16 "
    "vertical. No text or watermark in the artwork unless the brief below "
    "explicitly calls for handwritten signs. Render the frame described:"
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

# (beat_id, slug, includes_founders, brief_prompt)
BEATS = [
    ("A", "hero-hook", False, """
[Context] Opening hero shot of a Mous-style technical-explainer ad — establishes the $250k asset at stake before any product is shown.
[Visual] A yellow Caterpillar 320 excavator parked alone at the edge of an Australian rural construction worksite at golden hour. Boom and bucket lowered, operator cab unprotected with no cover. In the foreground, a tradesman in dusty hi-vis walks away from the machine with his back to camera, silhouette stark against the low sun. Long shadows stretch across compacted dirt and gravel. Eucalyptus and dust haze in the distance.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, loose hand-drawn pencil and marker lines, minimal shading, rough cinematic composition, no text or watermark.
""".strip()),
    ("B", "problem-expansion", False, """
[Context] Problem agitation beat — visualises an excavator cab vulnerable to weather and exposure overnight.
[Visual] Close-up side-angle of a yellow excavator cab at stormy dusk. An olive-green canvas tarp is half-draped over the roof of the cab, flapping wildly in heavy wind, partially exposing the operator seat and joystick controls inside. Rain begins to streak the cab glass. Heavy storm clouds and a low setting sun behind. Mood of vulnerability.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, loose hand-drawn pencil and marker lines, minimal shading, dramatic side-lighting suggestion, no text.
""".strip()),
    ("C", "villain-reveal", False, """
[Context] Villain reveal — visualises the cost of choosing cheap canvas tarps. Uses DiggerLid yellow on the villain object as a brand throughline.
[Visual] A three-panel vertical split frame. Top panel: extreme macro of a sun-bleached olive-green canvas tarp torn at a corroded brass grommet, fabric threads frayed in every direction. Middle panel: macro of a cracked UV-damaged black excavator dashboard plastic with hairline fractures spider-webbing across the surface. Bottom panel: macro of a rusted excavator control panel with corroded metal buttons and brown rust streaks. Across the top panel, a hand-stamped yellow REJECTED mark sharpied diagonally across the canvas.
[Format] 9:16 vertical aspect ratio, three stacked panels.
[Style] Black-and-white storyboard sketch, loose hand-drawn pencil and marker lines, high editorial contrast, the REJECTED stamp rendered in DiggerLid yellow #f5eb19 as the only colour in the frame, no other text.
""".strip()),
    ("D", "war-metaphor-pivot", True, """
[Context] Transition beat — the two DiggerLid founders step into frame to introduce the solution. Direct address to camera.
[Visual] Founder A and Founder B (from the reference portraits) standing side-by-side at a workshop bench, looking directly down the lens. Weather-worn faces, navy work shirts with sleeves rolled, dust on their forearms. Founder A on the left (wearing his black cap as always) holds a folded section of grey ripstop fabric; Founder B on the right (no cap, full moustache) holds a frayed olive-green canvas tarp. Behind them: pegboard with hand tools, a green cutting mat on the bench.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, loose hand-drawn pencil and marker lines, minimal shading, documentary portrait composition, no text.
""".strip()),
    ("E1", "pattern-templates", False, """
[Context] Skunkworks reveal — pattern engineering. Shows the three engineered sizes that answer the fit question opened in Beat B.
[Visual] Top-down overhead view of a workshop bench with a green cutting mat surface. Fanned out across the mat: three large paper pattern templates for excavator covers, each labelled in handwritten white sharpie with size names and measurements — XS 3.76m, S 3.76–4.18m, M 4.18–4.48m. A metal tape measure runs diagonally across the mat. A roll of grey ripstop fabric sits in the upper corner of the bench.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, flat-lay overhead composition, sharpie size labels handwritten and legible, no other text.
""".strip()),
    ("E2", "cover-installation", False, """
[Context] Solution beat — the engineered cover being installed on a real excavator. First moment the viewer sees the product in use.
[Visual] Three-quarter angle at a sunlit Australian worksite. A grey custom-fitted DiggerLid PRO Enclosure is being pulled snug over the cab of a yellow Caterpillar 320 excavator. A tradesman's hand clips a black YKK plastic buckle onto a DiggerLid-branded tie-down tether point on the side of the cab. The cover already taut, no slack.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, dynamic action composition, no text.
""".strip()),
    ("F", "ykk-hardware", False, """
[Context] Hardware tech credentialing — YKK buckle hyper-sync moment. Borrowed authority from an industry-recognised premium hardware brand.
[Visual] Extreme macro of a black plastic YKK side-release buckle being clipped together by two rugged hands. The embossed YKK letters are crisp and legible on the buckle face. A grey heavy-duty nylon strap threads through the buckle. The background is dark and out of focus.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, extreme hyper-tight macro composition, premium component focus, only the embossed YKK letters are legible — no other text.
""".strip()),
    ("G", "materials-credentialing", False, """
[Context] Materials credentialing with the big connotative leap — DiggerLid's fabric is the same class used on commercial transport trucks. The leap moves the product from cover to industrial-grade.
[Visual] A two-panel vertical split frame. Top panel: extreme macro of grey 490 GSM PVC-coated polyester ripstop fabric, light catching the characteristic cross-hatched ripstop reinforcement weave pattern. Bottom panel: a B-double semi-trailer truck driving along a wet rural Australian highway in heavy rain at dusk, the truck's grey tarpaulin-covered freight catching headlights from oncoming traffic, wet bitumen reflecting red taillights.
[Format] 9:16 vertical aspect ratio, two stacked panels.
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, hyperreal weave detail on the fabric panel, gritty atmospheric mood on the truck panel, no text.
""".strip()),
    ("H", "spec-litany", False, """
[Context] Feature-dense montage beat — proves the PRO Enclosure does everything a cheap canvas tarp cannot. Closes the villain-outcome loop.
[Visual] A four-panel grid composition. Top-left: a tradesman climbing into an excavator cab through a clear PVC front window panel that has been unzipped and rolled upward on a fitted grey cover. Top-right: extreme macro of a hand pressing UV-protected black Velcro onto grey ripstop fabric. Bottom-left: three-quarter rear view of a yellow excavator with a roll-up cooling vent panel open on the covered engine compartment, heat shimmer rising from inside. Bottom-right: interior cab POV looking down at a smartphone plugged into a black 12-volt accessory port on the dashboard.
[Format] 9:16 vertical aspect ratio, four-panel grid layout (2x2).
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, each panel a distinct feature demonstration, no text.
""".strip()),
    ("I", "heritage-credentialing", True, """
[Context] Heritage credentialing — the makers and the years that license the brand promise. Terminates the secret-build loop.
[Visual] Wide workshop interior shot. Founder A and Founder B (from the reference portraits) working at a long wooden bench: Founder A (always in his black cap) threading grey ripstop fabric through a heavy-duty industrial sewing machine; Founder B (full moustache, no cap) inspecting a folded finished excavator cover. Behind them on a brick wall hangs a large piece of brown cardboard with the words SEVEN YEARS handwritten in thick white sharpie. A pegboard of hand tools above the bench, a green cutting mat on the surface, dust motes drifting in the air.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, warm authentic maker aesthetic, the SEVEN YEARS sign clear and legible — no other text.
""".strip()),
    ("L", "brutality-test", False, """
[Context] Climactic brutality test — all five open loops resolve simultaneously when the cover survives a real excavator bucket pressing down on the cab.
[Visual] Dramatic wide shot at a dusty Australian worksite. A yellow 7-tonne excavator with its boom fully extended, bucket pressing directly down onto the roof of a second stationary yellow excavator. The second excavator's cab is fitted with a grey DiggerLid PRO Enclosure cover. The cover is visibly compressed under the weight of the bucket but remains structurally intact — no rip, no tear. Dust hangs in the air around both machines. Late-afternoon harsh light, hard cast shadows.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch, hand-drawn pencil and marker lines, low heroic camera angle, action-documentary energy, no text.
""".strip()),
    ("M", "tagline-drop", False, """
[Context] Brand outro — DiggerLid wordmark and tagline lockup over the surviving covered cab from Beat L.
[Visual] Tight medium shot of a yellow excavator cab fitted with the grey 490 GSM ripstop DiggerLid PRO Enclosure cover. Yellow DiggerLid-branded tie-down tether points catch warm light. Across the lower third of the frame: a clean horizontal black bar containing the DiggerLid wordmark logo — white letterforms with a thick DiggerLid-yellow strikethrough bar across the upper portion of the letters. Below the wordmark, the tagline WE'RE DIGGIN' IT! in a distressed grunge stamp typeface, slightly weathered.
[Format] 9:16 vertical aspect ratio.
[Style] Black-and-white storyboard sketch base with DiggerLid yellow #f5eb19 accent on the logo strikethrough bar and on the tie-down tether points. No other text outside the wordmark and tagline.
""".strip()),
]


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_prompt(brief_prompt, with_founders):
    parts = [STYLE_PERSISTENCE]
    if with_founders:
        parts.append(FOUNDER_ANCHOR)
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


def main():
    api_key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("GOOGLE_AI_API_KEY not set")
    if not FOUNDER_A.exists() or not FOUNDER_B.exists():
        sys.exit(f"Founder portraits missing at {FOUNDER_A.parent}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    founder_refs = [("Founder A", FOUNDER_A), ("Founder B", FOUNDER_B)]
    saved = []

    for i, (bid, slug, with_founders, brief_prompt) in enumerate(BEATS, 1):
        prompt = build_prompt(brief_prompt, with_founders)
        refs = founder_refs if with_founders else []
        print(f"[{i:02d}/12] {bid} — {slug} ({'with founders' if refs else 'no refs'})...", flush=True)
        try:
            png = generate_frame(prompt, refs, api_key)
        except Exception as e:
            print(f"  FAILED: {e}", flush=True)
            continue
        out = OUT_DIR / f"{i:02d}-{bid}-{slug}.png"
        out.write_bytes(png)
        saved.append(out)
        print(f"  saved {out.name} ({len(png):,} bytes)", flush=True)

    # Bundle the zip
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for p in saved:
            z.write(p, arcname=p.name)

    print(f"\nGenerated {len(saved)}/12 frames")
    print(f"Folder: {OUT_DIR}")
    print(f"Zip:    {ZIP_PATH} ({ZIP_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
