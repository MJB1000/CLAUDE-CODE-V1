"""Patch B, E, I, K in the 60s storyboard manifest per user amendments."""
import json
from pathlib import Path

SKETCH_STYLE = (
    "RENDER MODE — STRICT BLACK AND WHITE PENCIL STORYBOARD SKETCH. The whole "
    "artwork is monochrome graphite + ink wash on warm cream sketchbook paper: "
    "loose hand-drawn pencil and marker lines, minimal shading, rough cinematic "
    "composition. Pencil tones only — no colour fills anywhere unless the [Visual] "
    "block below explicitly calls out a DiggerLid yellow accent. The cream paper "
    "is the only off-white. One frame from an 11-frame storyboard series for a "
    "60-second ad."
)

FOUNDER_ANCHOR = (
    "Persistent characters: Luke and Joel — the two DiggerLid founders, two real "
    "Australian tradesmen. Preserve their faces exactly from the reference "
    "portraits attached. LUKE = broad-shouldered build, neatly-trimmed dark "
    "moustache, ALWAYS wears a black baseball cap with the brim facing forward, "
    "dark hair just visible at the temples below the cap line. JOEL = slimmer "
    "build, distinctive thick full chevron moustache, mid-brown hair worn in a "
    "clean side part, NO cap, clean-shaven on the cheeks and chin."
)

NEW_B = """[Context] Problem agitation — the unprotected machine alone against the elements.
[Visual] The XCMG XE17U excavator standing alone outdoors, hammered by extreme weather. Diagonal rain streaks pouring down, scattered hail-pellet dots bouncing off the cab roof, swirling wind lines around the boom, heavy storm clouds packed thick above. The operator cab is fully exposed and unprotected — no cover, no tarp, nothing between the cab and the elements. Wet ground around the tracks. Mood of pure vulnerability — the machine alone against the weather.
[Format] 9:16 vertical, single composition (no panels, no people).
[Style] B&W storyboard sketch on cream paper, dramatic weather, dynamic line work, kinetic. No colour, no text."""

NEW_E = """[Context] Midpoint anchor — the moment the DiggerLid exists. Single reverent shot, no cuts. Comic-epic register, played straight.
[Visual] Low heroic camera angle. The XCMG XE17U excavator centred on a dusty worksite floor, the grey DiggerLid PRO Enclosure cover ALREADY SETTLED snugly onto the operator cab — taut, fitted, no slack, no parachute, no mid-air descent. From above, heavenly god-rays of light stream down through atmospheric dust, illuminating the covered cab from directly overhead. Lens-flare hint at the top of the frame where the rays converge. Around the cab, four DiggerLid-yellow tether points catch the light, glowing as the only coloured highlights — small but distinct. Dust motes drift in the rays. The cover is the hero — quiet, fitted, blessed by light.
[Format] 9:16 vertical, single composition.
[Style] B&W storyboard sketch on cream paper, dramatic god-ray lighting suggested with directional pencil strokes, cinematic awe. DiggerLid yellow #f5eb19 ONLY on the four tether-point accents around the cab — every other element pencil monochrome. No text."""

NEW_I = """[Context] Challenge experiment — the survival test. The cover takes a real excavator track and lives. No on-screen copy.
[Visual] A two-panel vertical split frame. TOP PANEL: low-angle worksite shot. The grey DiggerLid PRO Enclosure cover lies FLAT on the dirt directly in front of the XCMG XE17U. The machine is mid-action — slowly tracking forward, the front edge of the rubber/metal track just rolling ONTO the surface of the cover, fabric visibly compressed under the track. Dust kicked up, light catching the track edge. BOTTOM PANEL: a moment after, Luke (black cap) crouches and lifts the cover by ONE corner, holding it up at chest height — visible diagonal track-mark imprints across the grey fabric, but NO rips, no tears, no holes. Cover intact. Joel stands next to him in the background, arms crossed, nodding.
[Format] 9:16 vertical, two stacked panels. NO TEXT OVERLAY, no copy, no captions anywhere in the frame.
[Style] B&W storyboard sketch on cream paper. Heavy weight on the track-grind, action-documentary energy on the top panel; quiet documentary on the bottom panel. No colour, no text."""

NEW_K = """[Context] Finisher — both founders with the cover trophy. Single hero shot, NO brand frame, NO logo lockup in this image.
[Visual] Single composition — no panel splits, no brand-frame panel, no wordmark anywhere. Luke (black cap, dark moustache) and Joel (chevron moustache, no cap) standing shoulder-to-shoulder directly in front of the XCMG XE17U, both holding the dusty track-marked grey DiggerLid PRO Enclosure cover UP between them at shoulder height like a trophy, grinning at the camera. Track marks clearly visible across the cover surface as diagonal imprints. Worksite setting behind them — dirt ground, low workshop wall, golden-hour light suggested with directional pencil strokes. The frame ends on this trophy moment.
[Format] 9:16 vertical, single composition.
[Style] B&W storyboard sketch on cream paper, warm portraiture, hyperreal sketch detail on the founders' faces and the track-marked cover. No colour, no text, no logo, no wordmark."""

UPDATES = {
    "B": {"refs": [],                            "content": NEW_B, "founders": False},
    "E": {"refs": [],                            "content": NEW_E, "founders": False},
    "I": {"refs": ["founder-a", "founder-b"],    "content": NEW_I, "founders": True},
    "K": {"refs": ["founder-a", "founder-b"],    "content": NEW_K, "founders": True},
}

p = Path("/home/user/CLAUDE-CODE-V1/deliverables/diggerlid-pro-60s-storyboard.json")
manifest = json.loads(p.read_text())

for frame in manifest["frames"]:
    if frame["id"] in UPDATES:
        u = UPDATES[frame["id"]]
        prompt = SKETCH_STYLE + "\n\n"
        if u["founders"]:
            prompt += FOUNDER_ANCHOR + "\n\n"
        prompt += u["content"]
        frame["refs"] = u["refs"]
        frame["prompt"] = prompt

p.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Patched B, E, I, K in {p}")
