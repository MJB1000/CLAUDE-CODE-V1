---
name: vertical-storyboard
description: Repeatable vertical-storyboard process. Produces a 9:16 B&W pencil-sketch (or photoreal) storyboard from a single unified manifest, with beat-grouped frames, per-frame reprompt support, and an A4 PDF export that paginates by beat section. Use whenever the user asks for a storyboard cut, a shotlist PDF, reprompt this frame, add a beat, etc.
---

# Vertical Storyboard — Repeatable Process

## What this skill produces

- A **9:16 vertical storyboard**: one PNG per frame, B&W pencil-sketch on cream (default) or whatever render-mode the prompt specifies.
- An **A4 PDF shotlist**: 3-wide grid of frames, each cell with beat-ID badge + scene title + one-line caption. Pages are grouped by beat section — each beat gets its own page (or pages, if it has more than 6 frames).
- Per-frame iteration: reprompt one frame without re-rendering the rest.
- Per-beat iteration: re-render every frame in one beat group, leaving the others untouched.

## One file, two consumers

Everything lives in a single **unified manifest** JSON. Both the renderer and the PDF exporter read the same file — there is no second config to maintain.

```
deliverables/<project>/storyboard.json   ← the unified manifest
deliverables/<project>/images/            ← rendered frame PNGs land here
deliverables/<project>/pdf/<version>.pdf  ← PDF outputs land here
```

## Unified manifest schema

```json
{
  "project":      "diggerlid-pro-60s-v4",
  "title":        "DIGGERLID PRO · 60s STORYBOARD",
  "version":      "v1",
  "aspect":       "9:16",
  "default_resolution": "1K",
  "output_dir":   "deliverables/diggerlid-pro-60s-v4/images",
  "pdf_dir":      "deliverables/diggerlid-pro-60s-v4/pdf",
  "asset_refs":   {
    "founder-a":  "clients/assets/diggerlid/founders/founder-a.jpg",
    "founder-b":  "clients/assets/diggerlid/founders/founder-b.jpg"
  },
  "auto_refs":    [
    {
      "id":       "product-pro-enclosure",
      "triggers": ["pro enclosure", "the cover"],
      "refs":     ["product-enclosure-side", "product-enclosure-front"]
    }
  ],
  "beats": [
    {
      "id":          "act-1-arrival",
      "title":       "ACT 1 — ARRIVAL",
      "description": "The hero machine arrives.",
      "frames": [
        {
          "n":       1,
          "id":      "A1",
          "slug":    "pallet-stop",
          "refs":    [],
          "title":   "PALLET STOP",
          "caption": "XE17U dragged to a stop on the warehouse floor.",
          "prompt":  "RENDER MODE — STRICT BLACK AND WHITE PENCIL STORYBOARD SKETCH …"
        }
      ]
    },
    {
      "id":    "act-2-the-cover",
      "title": "ACT 2 — THE COVER",
      "frames": [ ... ]
    }
  ]
}
```

### Field reference

**Top level**
- `project` — slug used in PDF filenames and cost-tracker logs.
- `title` — human-readable header drawn at the top of every PDF page.
- `version` — appended to PDF filename (`<project>-<version>.pdf`). Bump for cuts/variants.
- `aspect` — `9:16` for vertical storyboards. Other values (`4:5`, `16:9`) work too.
- `default_resolution` — `512` / `1K` / `2K` / `4K`. Per-frame `resolution: "2K"` overrides.
- `output_dir` — where rendered frame PNGs land.
- `pdf_dir` — where PDF + page PNGs land. Defaults to `output_dir` if omitted.
- `asset_refs` — named map of reference-image keys → repo-relative paths.
- `auto_refs` — content-triggered ref rules (see storyboard-batch.py docstring).

**Beat**
- `id` — slug used for `--beat <id>` filtering (e.g. `act-1-arrival`).
- `title` — large heading drawn at the top of the beat's PDF page(s).
- `description` *(optional)* — one-line subtitle under the beat heading.
- `frames` — list of frame entries in playback order.

**Frame**
- `n` — stable 1-based frame number. Used in the PNG filename.
- `id` — short beat code (`A1`, `B`, `F2b`, etc.). Used for `--frame <id>` filtering and as the PDF badge.
- `slug` — filename-safe scene slug. Output PNG is `<NN>-<id>-<slug>.png`.
- `refs` — explicit list of `asset_refs` keys to attach as reference images.
- `resolution` — `null` to use the manifest default, or override (`"2K"`, etc.).
- `title` — short scene title drawn in the PDF cell beside the badge.
- `caption` — one-line plain-English description drawn under the cell.
- `prompt` — the actual Gemini prompt for this frame. Self-contained.

## Commands

```bash
# Render the WHOLE set (all beats, all frames)
python3 .claude/skills/storyboard/scripts/storyboard-batch.py \
  --manifest deliverables/<project>/storyboard.json

# Reprompt a SINGLE frame after editing its prompt in the manifest
python3 .claude/skills/storyboard/scripts/storyboard-batch.py \
  --manifest deliverables/<project>/storyboard.json --frame F1b

# Re-render every frame in ONE beat group
python3 .claude/skills/storyboard/scripts/storyboard-batch.py \
  --manifest deliverables/<project>/storyboard.json --beat act-2-the-cover

# Force a higher-resolution one-off (default is the manifest's default_resolution)
python3 .claude/skills/storyboard/scripts/storyboard-batch.py \
  --manifest deliverables/<project>/storyboard.json --frame F1b --resolution 2K

# Build the A4 PDF with beat-section pagination
python3 .claude/skills/storyboard/scripts/pdf-export.py \
  --config deliverables/<project>/storyboard.json
```

The same manifest file is the `--manifest` arg for the renderer and the `--config` arg for the PDF exporter. The renderer ignores `title`/`caption`/`beats[].description`; the PDF exporter ignores `prompt`/`refs`. They co-exist in one file by design.

## Repeatable workflow

1. **Brief** — the user describes a new storyboard or revisions.
2. **Manifest** — write or edit `deliverables/<project>/storyboard.json` so each beat group + frame entry mirrors the brief. Prompts include the render-mode header, character anchors where founders appear, and explicit feature/object details from the brand profile (`clients/diggerlid.md`).
3. **Render** — run `storyboard-batch.py` for the full set (first cut) or `--frame`/`--beat` (revisions).
4. **PDF** — run `pdf-export.py` against the same manifest. Bump `version` in the manifest if you want a parallel PDF (`v1`, `v2`, etc.).
5. **Iterate** — edit prompts in the manifest, re-run targeted renders, rebuild PDF. The manifest is the source of truth between runs.

## Style defaults for vertical storyboards

- **Render mode** — strict B&W pencil-sketch on cream sketchbook paper (matches the existing 60s DiggerLid cut). Open with:
  > RENDER MODE — STRICT BLACK AND WHITE PENCIL STORYBOARD SKETCH. The whole artwork is monochrome graphite + ink wash on warm cream sketchbook paper…
- **Composition** — full-bleed 9:16 portrait, no horizontal sub-frame, no letterboxing. Subjects framed head-near-top to feet-near-bottom for human shots; full vertical hero stack for product/machine shots.
- **Text overlays** — if a frame needs typography (numbered list, price tag, etc.), place it as a horizontal **bottom band** or **top band**, not a side bar, so the 9:16 composition stays portrait.
- **Brand-yellow accents** — `#f5eb19`, used sparingly: tether tabs, chest logos, pin markers, accent bars. Never the only colour on the machine itself; the cover stays grey.
- **Character anchors** — for founder shots, always include the verbatim "Persistent character" block from `clients/diggerlid.md`. CAP LOCK on Luke is non-negotiable.

## Worked example

`deliverables/diggerlid-pro-60s-v4/storyboard.json` is the canonical example of this format in the repo, with the V4 60s ad cut beat-grouped into ARRIVAL / PROBLEM / REVEAL / FEATURES / MATERIALS / GLOBAL / CONDITIONS / TESTS / RANGE / FINISHER. Use it as the template when starting a new project.
