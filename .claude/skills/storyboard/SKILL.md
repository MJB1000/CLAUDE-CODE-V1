---
name: storyboard
description: "Generate a 3-frame social-media storyboard from a narrative prompt + dropped images or video. Triggers on /storyboard, '3-frame storyboard', '3-frame social board', 'pencil sketch storyboard', 'social board from this'. User drops a prompt and source media; this skill produces a single 1920x1080 landscape PNG: cream sketch-paper background with a thin hi-vis yellow border, three character-consistent 9:16 portrait pencil-sketch frames sitting side-by-side, two-line-capable caption strips beneath each, brand wordmark footer at the bottom, plus optional Trello attachment."
argument-hint: "<narrative — describe the 3 beats with arrows or commas>"
---

# Storyboard — 3-Frame Social Board Generator

## What this skill does

User drops 1+ images (or a short MP4) into the chat with a prompt describing a 3-beat narrative. This skill generates 3 character-consistent 9:16 portrait pencil-sketch frames featuring the configured founders + machine reference, composites them side-by-side into a single 1920×1080 landscape image — cream sketch-paper background, thin hi-vis yellow border, per-frame caption strips that wrap to a second line when the beat is long, brand wordmark in the bottom yellow strip — and renders the result inline so the user can download it. Optionally attaches to a Trello card.

**Default client:** `diggerlid`. Override with the `--client` flag if the user names another preset.

## Trigger conditions

Activate this skill when the user:
- Types `/storyboard` (with or without arguments)
- Says "3-frame storyboard", "3-frame social board", "social board from this", "pencil sketch storyboard"
- Drops 1+ images and asks for a "storyboard" / "board" / "3 panels" / "3 frames"

If the user just says "make a storyboard" with no narrative, ask for the 3-beat arc in one short message before generating. Don't auto-fill.

## Step-by-step

### 1. Confirm intent and gather inputs

Locate from the conversation:
- **Narrative prompt** — the user's text describing the story.
- **Dropped attachments** — image and/or video paths shown in the conversation.
- **Trello card** — if the user pasted a Trello URL or card ID, extract the card ID (the segment after `/c/` and before the next `/` in `https://trello.com/c/<ID>/...`).
- **Client** — default `diggerlid` unless the user names another.

If the prompt has no clear 3-beat structure (no arrows, no semicolons, no "then", no commas), ask the user one short question:
> "Quick beat split? E.g. *opening shot → action → payoff*."

Then continue once they answer.

### 2. Pre-flight check

Before calling the orchestrator, confirm both founder portraits exist:

```bash
ls clients/assets/diggerlid/founders/founder-a.* clients/assets/diggerlid/founders/founder-b.* 2>/dev/null
```

If either is missing, stop and tell the user:
> "Setup needed: drop two founder portraits at `clients/assets/diggerlid/founders/founder-a.jpg` and `founder-b.jpg` (head-and-shoulders, faces clearly visible). One-time setup — every storyboard after that is one drop + one prompt away."

### 3. Run the orchestrator

```bash
python3 .claude/skills/storyboard/scripts/storyboard.py \
  --prompt "<the user's narrative, exactly as given>" \
  --client diggerlid \
  --source <path1> [--source <path2> ...] \
  [--resolution 1K|2K] \
  [--trello-card-id <ID>]
```

Pass `GOOGLE_AI_API_KEY` via env (already set in this environment per the banana skill setup). The script prints a JSON object on stdout with `path`, `beats`, `frames`, `resolution`, `trello_url`, `trello_error`.

**Resolution:** defaults to `1K` — the efficient default for composite boards. Pass `--resolution 2K` only when the user explicitly wants an HQ final. `imageSize` is the real API resolution lever; do not raise it speculatively.

### 4. Render the output inline

Read the PNG with the Read tool so the image renders inline in chat:

```
Read(file_path: "<path from the JSON output>")
```

This is the "downloadable image" UX — the user can right-click → save from the chat surface, and the file is also persisted at `deliverables/<date>-storyboard-<slug>.png` for git/Trello.

### 5. Report

One concise paragraph:
- File path (relative to repo root)
- The 3 beats the orchestrator used (so the user can sanity-check the split)
- Cost note: `Frames generated: 3 (~$0.117 total at 1K, gemini-3.1-flash-image-preview)` — at 1K each frame is $0.039; 2K is $0.078
- Trello status: ✓ URL, or "skipped — TRELLO_API_KEY not set", or the error message

If likeness fidelity looks off in the rendered frames (founder faces don't match the reference portraits), tell the user once: "Likeness can drift on stylised output. If this happens repeatedly, we have a documented v2 lever — adding 2-line textual anchors per founder. Want me to wire that in?" Don't volunteer it more than once per session.

## Multi-frame sequence mode (manifest-driven, per-frame regeneration)

The composite mode above produces ONE 3-panel board. For longer storyboards —
a full ad with N individually-numbered frames (e.g. the 12-beat DiggerLid PRO
ad) — use `scripts/storyboard-batch.py`, which is driven by a JSON **manifest**.

The manifest is the persistent source of truth: it holds every frame's number,
beat id, slug, prompt, reference images, and resolution. Because it persists,
**a single frame can be regenerated without re-running the whole set or
re-typing its prompt.**

### Generating the whole sequence

```bash
python3 .claude/skills/storyboard/scripts/storyboard-batch.py \
  --manifest deliverables/<project>.json [--resolution 1K|2K]
```

### Regenerating ONE frame — the "image 7, change X" workflow

When the user says *"image 7, make the sky darker"* (or any per-frame edit):

1. Open the manifest JSON, find the frame by its `n` (number) or `id` (beat).
2. Edit that frame's `prompt` string with the requested change. Edit only the
   one frame's entry — leave the other 11 untouched.
3. Regenerate just that frame:
   ```bash
   python3 .claude/skills/storyboard/scripts/storyboard-batch.py \
     --manifest deliverables/<project>.json --frame 7
   ```
   `--frame` accepts the number (`7`) or the beat id (`F`). Only that PNG is
   re-rendered; the zip is rebuilt automatically; the other frames are not
   touched and not re-billed.
4. Read the regenerated PNG inline so the user sees the result.

### Auto-attached product references (content-triggered)

The manifest can declare `auto_refs` rules that scan each frame's prompt for
trigger words and auto-attach reference images on match. This is how product
photos get pulled in automatically — e.g. "any frame mentioning the DiggerLid
PRO Enclosure attaches the product reference images."

Manifest shape:
```json
"auto_refs": [
  {
    "id": "product-pro-enclosure",
    "triggers": ["diggershield", "pro enclosure", "lear front"],
    "refs": ["product-enclosure-front", "product-enclosure-side"]
  }
]
```

How it behaves:
- Any frame whose prompt contains at least one trigger word (case-insensitive)
  gets the rule's `refs` appended to its effective reference list.
- Auto-refs whose asset key is NOT yet in `asset_refs` are silently skipped —
  the rule stays DORMANT until you register the asset. This lets you wire up
  the rules before pushing product photos; activation is automatic the moment
  the asset key appears.
- Per-frame opt-out: set `"skip_auto_refs": true` on a frame to suppress all
  auto-attaches for just that frame.
- The batch tool prints which auto-refs fired (and which are dormant) in the
  per-frame log line, so you can sanity-check the matching.

When the user pushes new product photos, the workflow is: drop the files into
`asset_refs`, then re-run `storyboard-batch.py --frame <n>` on each affected
frame to pick up the now-active references.

### Resolution in batch mode

`storyboard-batch.py` defaults to the manifest's `default_resolution` (set to
`1K`). Override per run with `--resolution 2K` for an HQ pass. Recommended
flow: draft the whole sequence at 1K, review, then re-run only the approved
frames at 2K. Never pay 2K for frames that may be discarded.

### Manifest location & creation

Manifests live next to their output, e.g. `deliverables/diggerlid-pro-storyboard.json`
drives `deliverables/diggerlid-pro-storyboard/`. The schema is documented in the
header of `storyboard-batch.py`. To start a new multi-frame project, write a
manifest with one entry per frame (each with a complete self-contained prompt).

## Decision rules — what NOT to do

- **Do not** read `style-recipes.md` for every run. Only load it if the user asks about the style, the layout math, or non-default colour treatment.
- **Do not** call Gemini directly from the skill. The orchestrator owns all API calls and cost logging.
- **Do not** write to `deliverables/` directly — let the orchestrator name and place the file.
- **Do not** invent a Trello card ID. If the user didn't supply one, omit the flag and let it skip cleanly.
- **Do not** modify the orchestrator's beat split unless the user explicitly redirects (e.g. "actually split it into A → B → C").

## Failure modes — recognise and respond

| Symptom | Action |
|---|---|
| `setup_required: true` in stderr | User needs to add founder portraits — show the setup message from step 2. |
| `Billing not enabled` | Send the user to https://aistudio.google.com/apikey. |
| `finishReason: IMAGE_SAFETY` | Suggest rephrasing the beat (Gemini blocked it). E.g. avoid violent/dramatic wording. |
| `TRELLO_API_KEY or TRELLO_TOKEN not set` | Report Trello as skipped, do not block the deliverable. |
| Video dropped but no ffmpeg | Tell the user to drop a still image instead, or install ffmpeg. |
| Likeness drift across 3 frames | One-time offer to add textual anchors (see Reporting above). |

## On-demand references

Load these only when the situation requires:
- `references/style-recipes.md` — pencil style descriptor, beat decomposition heuristics, layout math, brand colour rules.
- `~/.claude/skills/banana/references/prompt-engineering.md` — for advanced prompt tuning if a frame keeps failing.
- `~/.claude/skills/banana/references/gemini-models.md` — for resolution/model trade-offs.

## Quick example (user-facing)

User drops 2 founder photos + 1 site photo, types:

```
/storyboard founders pull up to the property → customer hands over the keys → walk back together to inspect the new lid on the digger
```

Skill runs, generates 3 frames, composites, displays inline:

```
Generated 3-frame storyboard: deliverables/2026-05-04-storyboard-founders-pull-up-to-the-property.png

Beats used:
  1. founders pull up to the property
  2. customer hands over the keys
  3. walk back together to inspect the new lid on the digger

Frames generated: 3 (~$0.234 total at 2K)
Trello: skipped — no card ID in your message
```

Then the inline PNG renders, downloadable from the chat surface.
