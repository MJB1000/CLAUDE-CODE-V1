# Storyboard — Style Recipes & Layout Math

*Loaded on demand by the storyboard skill. Keep edits surgical.*

---

## Pencil-sketch style descriptor (default)

> Soft graphite pencil sketch on warm cream sketchbook paper, fully monochrome
> with no colour anywhere in the artwork. Loose hand-drawn pencil lines, gentle
> hatched shading and feathered edges, subtle paper grain. Simplified facial
> features in the style of a director's pre-production storyboard. The kind of
> thumbnail board pulled from an artist's sketchbook. 16:9 cinematic framing.

**Why monochrome:** brand colour belongs in the *frame around* the artwork (margins, captions, footer), not inside it. Keeps the deliverable looking like a director's board, not an over-coloured ad.

**Banned phrasing:** "high quality", "8K", "professional photography", "ultra-realistic" — Gemini's internal system prompt penalises these (see `~/.claude/skills/banana/references/prompt-engineering.md` line 177).

---

## Beat decomposition heuristics

The orchestrator splits a single narrative into exactly 3 beats. Order of precedence:

1. **Explicit arrows or `→`** — "shot A → shot B → shot C". Honoured directly.
2. **`;` semicolons** — same.
3. **`then` / `, then`** — common in spoken-style prompts.
4. **Comma split** when 3+ commas present.
5. **Auto-suffix** as last resort:
   - Beat 1: "Establishing wide shot — opening of: …"
   - Beat 2: "Mid shot — the action of: …"
   - Beat 3: "Close shot — the payoff of: …"

If the user's prompt is too vague to split into 3 (e.g. one short noun phrase), the **skill** asks one clarifying question rather than letting the orchestrator auto-suffix into something flat.

---

## Character consistency — image references

Per `~/.claude/skills/banana/references/prompt-engineering.md` lines 127–137:

- Up to 4–5 character refs per call on Nano Banana 2.
- Name each ref ("Founder A", "Founder B", "the excavator").
- Restate the names in the beat prompt: *"Persistent characters: Founder A and Founder B from the reference portraits."*
- Ref images attached as `inlineData` parts in the same `contents` array as the text.

The orchestrator sends all reference images on **every** frame call (3 calls total), not via a chat session. This is more deterministic than chat-based continuity and avoids dependence on the `gemini_chat` MCP being installed.

If likeness fidelity is poor in v1 boards, the documented next lever is **textual anchors** alongside image refs — describe each founder in 2–3 invariant traits ("Founder A: dark hair, square-cut beard, navy work shirt") and repeat verbatim in every beat prompt.

---

## Layout math — 1920×1080 (landscape, three 9:16 portraits)

```
+------------------------- 1920 wide -------------------------+
| 16 px hi-vis yellow border (top)                            |
|                                                             |
| 167 px |+--------+  24  +--------+  24  +--------+| 167 px  |
|  pad   ||FRAME 1 |  px  |FRAME 2 |  px  |FRAME 3 ||  pad    |
|        || 502×892|gutter| 502×892|gutter| 502×892||         |
|        ||  9:16  |      |  9:16  |      |  9:16  ||         |
|        |+--------+      +--------+      +--------+|         |
|        ||  CAP 1 |      |  CAP 2 |      |  CAP 3 || 60 px navy |
|        |+--------+      +--------+      +--------+|         |
|                                                             |
| 16 px hi-vis gap                                            |
+-------------------------------------------------------------+
|  80 px hi-vis yellow footer — DIGGERLID wordmark in navy    |
+-------------------------------------------------------------+
| 16 px hi-vis yellow border (bottom)                         |
+-------------------------------------------------------------+
1080 tall

Width:   2*16 + 2*167 + 3*502 + 2*24 = 32 + 334 + 1506 + 48 = 1920 ✓
Height:  16 + 892 + 60 + 16 + 80 + 16 = 1080 ✓
```

Each Gemini generation now requests `aspectRatio: "9:16"` so the model returns
portrait-composed artwork. PIL just resizes to 502×892 and pastes.

The brand colour treatment stays the same as the original vertical layout —
hi-vis yellow lives in the margins/gutters/footer, never inside the artwork.
Per-frame caption strips are flush under each portrait (502 px wide each)
rather than spanning the full canvas — keeps each frame visually self-contained.

If you change any of FRAME_W / FRAME_H / GUTTER / OUTER_PAD / FOOTER_H,
recompute both sums and verify with a quick stub-frame composition test
before shipping. The orchestrator pins the footer at
`CANVAS_H − BORDER − FOOTER_H`, so over-tall content silently gets painted
over by the footer rectangle.

---

## Brand colour usage

| Surface | Colour | Why |
|---|---|---|
| Outer 16 px border | `#FFE600` hi-vis yellow | Brand frame |
| 24 px gutters between frames | `#FFE600` | Continues the frame |
| 60 px caption strips | `#1A1F2E` navy + white text | High contrast read on stories |
| 80 px footer | `#FFE600` + navy text | Wordmark slot |
| **Inside the artwork** | *No colour — pencil only* | Director's board aesthetic |

For non-DiggerLid clients, the orchestrator pulls colours from `~/.banana/presets/<client>.json`. If a preset has no brand colour, fall back to neutral grey margins (TODO: not yet implemented — v1 assumes the preset has at least one colour).

---

## Output naming

`deliverables/<YYYY-MM-DD>-storyboard-<slug>.png`

`<slug>` is a 40-char snake/kebab fragment of the prompt, lowercased. If two storyboards generate on the same day with similar prompts, the second overwrites the first — that's intentional for fast iteration. If a board is locked, copy it sideways to `deliverables/locked/` before generating again.
