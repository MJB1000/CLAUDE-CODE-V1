#!/usr/bin/env python3
"""DiggerLid PRO Excavator Enclosure — V6 storyboard.

V6 breaks from V5's uniform sketch style. Each beat uses the visual style
most appropriate to its rhetorical job: cinematic editorial product photo,
documentary realism, fashion editorial, UGC mosaic, action documentary, etc.

Machine in scope: XCMG XE17U compact mini excavator (1.7t, $45k).
Cover fabric: grey 490 GSM PVC-coated polyester ripstop.
DiggerLid yellow (#f5eb19) is reserved for tie-down tethers, on-screen
typography, REJECTED stamps, and brand-accent overlays — never on the
cover body itself.

Founders appear in E1, H, L, M — image refs attached on all four.
Logo lockup attached as ref on M.

Output: deliverables/diggerlid-pro-storyboard-v6/<NN>-<id>-<slug>.png
        deliverables/diggerlid-pro-storyboard-v6.zip
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
LOGO = REPO / "clients/assets/diggerlid/logo-primary.png"
OUT_DIR = REPO / "deliverables" / "diggerlid-pro-storyboard-v6"
ZIP_PATH = REPO / "deliverables" / "diggerlid-pro-storyboard-v6.zip"

MODEL = "gemini-3.1-flash-image-preview"
ASPECT = "9:16"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

V6_PREAMBLE = (
    "This is one frame from a 12-frame storyboard series for a 45-second "
    "Meta ad. V6 of this series breaks from a uniform style: each beat uses "
    "the visual style most appropriate to its rhetorical function. Render "
    "THIS frame in the specific style described in the [Style] block at the "
    "end — do NOT default to a generic illustration or sketch aesthetic. "
    "9:16 vertical aspect ratio is mandatory."
)

FOUNDER_ANCHOR = (
    "Persistent characters in this frame: the two DiggerLid founders — "
    "two real Australian tradesmen. Preserve their facial features exactly "
    "from the reference portraits below. Founder A: solid broad-shouldered "
    "build, neatly-trimmed dark moustache, dark hair, often wears a black "
    "baseball cap. Founder B: slimmer build, distinctive thick full chevron "
    "moustache, mid-brown hair worn in a clean side part, no cap, clean-"
    "shaven cheeks and chin. The brief refers to them as 'in their forties' — "
    "preserve their actual appearance from the reference portraits."
)

# (beat_id, slug, founders, logo_ref, brief_prompt)
BEATS = [
    ("A", "hero-hook", False, False, """
[Context] Opening hero shot of a Mous-style technical-explainer ad — establishes the machine at stake before any product is shown. The XCMG XE17U is a 1.7-tonne compact mini excavator, popular with Australian owner-operators and hire fleets. DiggerLid yellow accent lines layered on top signal we're entering DiggerLid's editorial space.
[Visual] A brand-new yellow XCMG XE17U compact mini excavator parked dead-centre in a clean, brightly-lit industrial warehouse. The machine sits on polished concrete floor with the boom and bucket lowered into rest position, tracks aligned squarely to camera. Hangar-style steel shelving and pallets visible in the background, slightly out of focus. Crisp, soft, overhead industrial lighting reveals every panel, decal, and hydraulic line — the machine looks straight off the factory floor, immaculate. Overlaid in DiggerLid yellow #f5eb19: three or four bold geometric accent lines tracing the silhouette of the excavator — a thin diagonal across the cab roof, a horizontal bar under the tracks, an angled line over the boom. The lines are flat, clean vector graphics in editorial composition, not hand-drawn.
[Format] 9:16 vertical aspect ratio.
[Style] Cinematic editorial product photography, hyperreal detail, neutral cool warehouse lighting, machine-yellow + DiggerLid-yellow palette dominant, polished concrete grey base. Flat vector accent lines layered on top of the photograph in editorial graphics style. No text or watermark.
""".strip()),
    ("B", "problem-expansion", False, False, """
[Context] Problem expansion beat — names the asset value as a floating typographic price tag. $45,000 is a meaningful figure for the owner-operator audience: a serious purchase that demands serious protection.
[Visual] The same brand-new yellow XCMG XE17U compact mini excavator from Beat A, now framed slightly tighter (medium shot, three-quarter angle) on the warehouse floor. Floating above the cab in mid-air: the text "$45,000" rendered in massive bold sans-serif type in DiggerLid yellow #f5eb19, set against a clean horizontal black underlay bar. The number is the dominant visual element of the frame, sized roughly 30% of frame height. The machine sits in soft warehouse light below the floating price tag. No other text on screen.
[Format] 9:16 vertical aspect ratio.
[Style] Cinematic editorial product photography with a typographic overlay. The "$45,000" type rendered in a heavy condensed sans-serif (Bahnschrift Bold or Impact), DiggerLid yellow #f5eb19 on a clean DiggerLid-black underlay bar. The machine photography is hyperreal and crisp; the type overlay is bold, flat, editorial — like a price card placed in a product catalogue.
""".strip()),
    ("C", "villain-reveal", False, False, """
[Context] Villain reveal — visualises the default "solution" most operators reach for: a cheap canvas tarp draped roughly over the machine. Sets up the contrast for what DiggerLid offers instead.
[Visual] Tight three-quarter angle close-up of the yellow XCMG XE17U excavator, now in a dimmer worksite-shed environment (not the bright Beat A/B warehouse). The machine is covered with a cheap olive-green canvas tarpaulin draped haphazardly over the cab and engine compartment. The tarp is visibly too small — gaping at the boom mount, sagging at the tracks, frayed at the edges. Mismatched rope ties and bungee cords secure it roughly. Yellow machine paint peeks through the gaps. Cool grey shed light, end-of-day mood, dust on the floor, a broom leaning in the background. Honest worksite reality.
[Format] 9:16 vertical aspect ratio.
[Style] Documentary photographic realism, slightly desaturated, cooler colour temperature than Beat A. The tarp looks lived-in, used, half-arsed. Mood is pitiful — this is what most operators settle for. No text.
""".strip()),
    ("D", "tarp-blows-off", False, False, """
[Context] Transitional beat — the villain (the tarp) fails in real time. The wind makes the visual argument: cheap tarps don't even stay on. Sets up the solution reveal.
[Visual] The same yellow XCMG XE17U excavator from Beat C, still in the shed/worksite, but now the olive-green canvas tarp is mid-air — peeled off the cab by a strong wind gust and being carried sideways out of frame. The tarp is twisted and partially folded, ropes trailing, motion-blurred against the sharp excavator behind it. The cab is now fully exposed beneath. Dust and small debris swept along with the tarp. Dramatic motion blur on the tarp; the excavator stays tack-sharp. Late afternoon harsh light, hard shadows.
[Format] 9:16 vertical aspect ratio.
[Style] Documentary action photography, dramatic motion blur on the tarp, sharp focus on the exposed machine. Slight wide-angle distortion to emphasise wind force. Honest worksite reality, kinetic energy. No text.
""".strip()),
    ("E1", "founders-prototyping", True, False, """
[Context] Skunkworks reveal — the founders' R&D moment, showing the actual development process. Establishes the makers behind the brand and the realness of the engineering work.
[Visual] Founder A and Founder B (from the reference portraits) at an outdoor worksite, working on fitting a prototype DiggerLid PRO Enclosure cover onto a yellow mid-size earthmover (a Caterpillar 305 or similar compact excavator). Founder A kneels at the rear of the machine with a tape measure pulled across the cab roof; Founder B stands on the tracks adjusting the cover's front panel. They are clearly mid-problem-solving — pointing at a seam, comparing notes. Scattered tools, fabric offcuts, and a clipboard on the ground beside them. Bright overcast Australian sky, dust haze, eucalyptus visible in background. Navy work shirts with sleeves rolled, dust on forearms. Preserve each founder's facial features from the reference portraits — Founder A's cap and dark moustache, Founder B's chevron moustache and side-part hair.
[Format] 9:16 vertical aspect ratio.
[Style] Documentary maker photography, candid moment, slightly handheld feel. Warm authentic tones, hyperreal detail on the founders and the prototype cover. No staged poses; this looks like a real working moment captured by accident. No text.
""".strip()),
    ("E2", "component-triptych", False, False, """
[Context] MIDPOINT SEMIOTIC ANCHOR. Spec credentialing — extreme macros of three engineered components. Equivalent to Mous's aramid/bulletproof-vest moment. Establishes engineering rigor through visible craftsmanship + named-component borrowed authority.
[Visual] A horizontal triptych split frame, three panels stacked vertically, all in extreme macro. Top panel: a black YKK plastic side-release buckle mid-clip, the embossed "YKK" letters crisp on the buckle face, grey heavy-duty nylon strap threading through, rugged hand grip just visible. Middle panel: the LEAR FRONT lower vision panel — a clear PVC viewing window stitched into the front of the grey cover with reinforced black trim edges, light passing through the panel revealing the operator cab interior softly visible behind it. Bottom panel: extreme macro of grey 490 GSM PVC-coated polyester ripstop fabric, cross-hatched ripstop reinforcement weave pattern catching dramatic side lighting, glossy PVC surface revealing texture and reinforcement threads. Each panel labelled in small handwritten white sharpie text at the bottom edge: "YKK BUCKLE", "LEAR FRONT VISION PANEL", "490 GSM RIPSTOP".
[Format] 9:16 vertical aspect ratio, three stacked panels.
[Style] Hyperreal macro product photography, studio softbox lighting, shallow depth of field on each panel, dark moody backgrounds, premium component focus. Each panel a distinct hyper-tight component reveal. Render this frame with the most care of any in the ad — it carries the engineering credentialing weight.
""".strip()),
    ("F", "ykk-fashion-editorial", False, False, """
[Context] Connotative leap — moves the YKK hardware from "industrial accessory" to "premium designer apparel" register. Borrowed authority from fashion.
[Visual] Editorial fashion-photography close-up of an anonymous model wearing premium dark indigo denim jeans, shot waist-down with face strictly out of frame. Three-quarter side angle, the model standing in a soft beam of natural side window light, one hand resting casually in a back pocket, the other thumb tucked into the waistband. The shot is tight enough to read "person in great-looking designer jeans" without being identifiable. Crisp denim texture, contrast stitching, classic five-pocket cut. The brass YKK zipper pull on the jeans fly is in sharp macro focus, dead-centre composition — the embossed "YKK" letters crisp on the brass tab. Premium, considered, high-fashion editorial mood. Soft warm-grey studio backdrop.
[Format] 9:16 vertical aspect ratio.
[Style] Editorial fashion photography, beautiful natural side light, hyperreal denim detail, anonymous model (face strictly out of frame). The YKK zipper pull is the visual focus — same hardware mark as on the excavator cover, now recontextualised in a luxury fashion frame. Premium magazine-editorial palette: warm neutrals, deep indigo, brass.
""".strip()),
    ("G", "nullarbor-truck", False, False, """
[Context] Materials credentialing connotative leap — same fabric class as the tarpaulins covering long-haul freight across Australia in every weather condition. The Nullarbor backdrop dramatises distance, isolation, and relentless conditions.
[Visual] Wide cinematic landscape shot of a B-double semi-trailer truck driving along a long, dead-straight stretch of the Eyre Highway across the Nullarbor Plain in central southern Australia. Grey or charcoal tarp-covered freight on the trailers, tension straps cinched tight across the load. Endless flat red-brown saltbush plain stretches to the horizon on both sides; sky is pale washed blue with high cirrus cloud. The truck is mid-distance, dust kicked up behind the trailers. Power poles paralleling the road into the vanishing point. Heat haze shimmering above the bitumen surface. Sense of immense distance and relentless conditions.
[Format] 9:16 vertical aspect ratio.
[Style] Cinematic landscape photography, anamorphic lens feel, slightly dusty palette, hyperreal Australian outback aesthetic. Honest road-photography mood — like a still from a Wim Wenders road documentary. Long focal length compresses the distance. No text.
""".strip()),
    ("H", "lear-front-thumbs-up", True, False, """
[Context] Feature demonstration moment — the LEAR FRONT clear PVC vision panel in working use. The founder visible through the unzipped vision panel proves the cover works for visibility AND operator entry, AND gives the ad a warm human moment.
[Visual] Three-quarter angle medium shot of a yellow XCMG XE17U excavator cab fitted with the grey DiggerLid PRO Enclosure cover. The LEAR FRONT clear PVC lower vision panel at the front of the cab is unzipped and rolled open, secured at the top with UV-protected black Velcro tabs. Inside the cab, in the operator seat, one of the DiggerLid founders (use Founder A from the reference — dark moustache, black cap, weathered face) leans slightly forward to wave a friendly thumbs-up out through the open vision panel, grinning broadly at the camera. He looks relaxed, happy, slightly weather-worn. Australian worksite background in golden-hour afternoon light, dust haze visible. The cover is taut, branded yellow tie-down tether points catch the sun.
[Format] 9:16 vertical aspect ratio.
[Style] Candid documentary photography, warm golden-hour tones, natural light, hyperreal detail on the founder's expression. Honest, friendly, on-brand DiggerLid warmth. The covered excavator is the hero; the founder is the human anchor. No text.
""".strip()),
    ("I", "ugc-weather-mosaic", False, False, """
[Context] Heritage credentialing through customer evidence — a UGC mosaic showing real operators across Australia using DiggerLid covers in extreme conditions. Establishes the "every day, on every site" claim with visible proof.
[Visual] A clean 3x3 grid mosaic of nine authentic user-generated-content style photographs, each panel showing a different earthmoving operator using a digger or excavator fitted with a grey DiggerLid PRO Enclosure cover in adverse weather. Top row: (1) operator in pouring rain on a muddy worksite, headlights catching the wet ripstop; (2) snow falling on a Tasmanian mountain construction site, cover dusted white; (3) hail storm with visible ice pellets on the cover. Middle row: (4) operator on a dusty drought-stricken farm; (5) tropical Far North Queensland monsoon downpour, water sheeting off the cover; (6) outback dust storm with red-orange haze obscuring everything but the machine outline. Bottom row: (7) cold misty morning fog in the Snowy Mountains, cover damp with dew; (8) Tasmanian sleet on the bucket; (9) golden-hour worksite after a storm cleared, cover steaming as it dries. Each panel has the candid raw look of a smartphone photo — slightly imperfect framing, varied colour temperature, authentic. Thin black gutters between panels.
[Format] 9:16 vertical aspect ratio, 3x3 grid layout.
[Style] User-generated content aesthetic across all nine panels — smartphone-photography quality, authentic and varied. Honest, unstaged, candid. Hyperreal across the grid. Each panel looks like a real operator's iPhone shot sent to DiggerLid as a testimonial. No text, no watermarks, no captions.
""".strip()),
    ("L", "paintball-test", True, False, """
[Context] Climactic brutality test — proves the cover survives extreme abuse. The founder INSIDE the cab during a live paintball assault is the spectacle moment. All five open loops resolve here when the cover holds.
[Visual] Action-documentary wide shot at an Australian worksite. A yellow XCMG XE17U excavator parked centre-frame, fitted with the grey DiggerLid PRO Enclosure cover. Three or four people in full paintball protective gear (helmets, ballistic eye protection, padded vests) stand 5–8 metres away firing paintball markers at the covered excavator. Bright neon paint splatters in yellow, pink, blue, and orange cover large patches of the grey ripstop fabric; several paintballs are mid-flight visible as colourful streaks in the air. Inside the cab, dimly visible through the LEAR FRONT clear PVC vision panel, one of the DiggerLid founders (use Founder B from the reference — chevron moustache, no cap) sits at the controls looking calm and slightly amused, giving the camera a thumbs-up through the panel. Late-afternoon harsh Australian sun, dust kicked up around the shooters, kinetic chaotic energy.
[Format] 9:16 vertical aspect ratio.
[Style] Action-documentary photography, slight motion blur on paintballs mid-flight, sharp focus on the excavator and shooters. Dynamic composition. Colourful, kinetic, slightly chaotic — but the covered cab is the hero, holding centre-frame steady against the assault. No text.
""".strip()),
    ("M", "tagline-drop", True, True, """
[Context] Brand outro — the two DiggerLid founders, standing next to the freshly torture-tested excavator, looking stoked. The tagline lockup lands here.
[Visual] Founder A and Founder B (from the reference portraits) standing side-by-side directly next to the yellow XCMG XE17U excavator. The excavator's grey DiggerLid PRO Enclosure cover is splattered with bright paintball residue from Beat L — vivid yellow, pink, blue, and orange splashes across the grey fabric. Both founders grin broadly at the camera. Weathered hands, navy DiggerLid-branded work shirts with sleeves rolled, dust on forearms and faces. Founder A (with his cap, dark moustache) has arms crossed; Founder B (chevron moustache, no cap) rests an open hand on the cover affectionately. Golden-hour Australian worksite light behind them, long shadows stretching, end-of-day satisfaction. Across the lower third of the frame: the DiggerLid wordmark logo lockup exactly matching the reference image attached — black horizontal bar containing white "DiggerLid" letterforms with a thick DiggerLid-yellow strikethrough bar across the upper portion of the letters, small ® at the end. Below the wordmark lockup, the tagline "WE'RE DIGGIN' IT!" in a distressed grunge stamp typeface, slightly weathered, in solid black ink.
[Format] 9:16 vertical aspect ratio.
[Style] Warm portrait photography, golden-hour light, candid stoked expressions, authentic maker brand outro. Hyperreal detail on the paint splatter and the founders' faces. The logo lockup at the bottom is the only on-screen typography.
""".strip()),
]


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_prompt(brief_prompt, with_founders):
    parts = [V6_PREAMBLE]
    if with_founders:
        parts.append(FOUNDER_ANCHOR)
    parts.append(brief_prompt)
    return "\n\n".join(parts)


def generate_frame(prompt, refs, api_key):
    parts = [{"text": prompt}]
    for label, p in refs:
        parts.append({"text": f"Reference image — {label}:"})
        mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        parts.append({"inlineData": {"mimeType": mime, "data": encode_image(p)}})

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

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    saved = []

    for i, (bid, slug, with_founders, with_logo, brief_prompt) in enumerate(BEATS, 1):
        prompt = build_prompt(brief_prompt, with_founders)
        refs = []
        if with_founders:
            refs.append(("Founder A", FOUNDER_A))
            refs.append(("Founder B", FOUNDER_B))
        if with_logo:
            refs.append(("DiggerLid logo lockup", LOGO))
        ref_summary = ", ".join(label for label, _ in refs) if refs else "no refs"
        print(f"[{i:02d}/12] {bid} — {slug} ({ref_summary})...", flush=True)
        try:
            png = generate_frame(prompt, refs, api_key)
        except Exception as e:
            print(f"  FAILED: {e}", flush=True)
            continue
        out = OUT_DIR / f"{i:02d}-{bid}-{slug}.png"
        out.write_bytes(png)
        saved.append(out)
        print(f"  saved {out.name} ({len(png):,} bytes)", flush=True)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for p in saved:
            z.write(p, arcname=p.name)

    print(f"\nGenerated {len(saved)}/12 frames")
    print(f"Folder: {OUT_DIR}")
    print(f"Zip:    {ZIP_PATH} ({ZIP_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
