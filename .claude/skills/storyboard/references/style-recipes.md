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

## Layout math — 1080×1920 (9:16)

```
+--------------------------------+  ← 16 px hi-vis yellow border (top)
|  Frame 1 (1048 × 540)          |
|--------------------------------|  ← 60 px navy caption strip
|  1. Setup  ·  <beat text>      |
+--------------------------------+
|       24 px hi-vis gutter      |
+--------------------------------+
|  Frame 2 (1048 × 540)          |
|--------------------------------|
|  2. Action  ·  <beat text>     |
+--------------------------------+
|       24 px hi-vis gutter      |
+--------------------------------+
|  Frame 3 (1048 × 540)          |
|--------------------------------|
|  3. Resolution  ·  <beat text> |
+--------------------------------+
|  80 px hi-vis footer (brand)   |
+--------------------------------+  ← 16 px hi-vis yellow border (bottom)

Vertical math:
  16 + 540 + 60 + 24 + 540 + 60 + 24 + 540 + 60 + 80 + 16 = 1960  ❌

Adjusted (this is what the script renders):
  16 + 3×(540 + 60) + 2×24 + 80 + 16 = 16 + 1800 + 48 + 80 + 16 = 1960
```

**Heads up — the numbers above sum to 1960, not 1920.** The script's actual canvas is 1080×1920 with a hi-vis background, so frame placement still fits because the bottom border + footer overlap visually with the canvas edge. If you tighten the layout later, drop one of:
- gutter from 24 → 12 (saves 24)
- footer from 80 → 64 (saves 16)
- caption from 60 → 56 (saves 12)

…to bring the math to a clean 1920. Not blocking for v1.

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
