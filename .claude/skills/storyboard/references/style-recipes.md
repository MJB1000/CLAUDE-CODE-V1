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

## Layout math — 1920×1080 (v6: adaptive frame sizing)

v6 made the layout adaptive: caption strips can wrap to as many lines as
needed (after a 50-word truncation), and the portrait frames shrink while
preserving 9:16 aspect to make room. v5's brand-colour treatment is
preserved — thin yellow border, cream sketch-paper interior, brand
wordmark in a small yellow strip at the bottom.

```
+------------------------- 1920 wide -------------------------+
| 8 px hi-vis yellow border (top, also left + right)          |
|------------------------- cream interior --------------------|
|                  16 px cream top breathing room             |
| 175 px |+--------+  24  +--------+  24  +--------+| 175 px  |
|  cream ||FRAME 1 |  px  |FRAME 2 |  px  |FRAME 3 ||  cream  |
|  pad   || 502×892|cream | 502×892|cream | 502×892||  pad    |
|        ||  9:16  |gutter|  9:16  |gutter|  9:16  ||         |
|        |+--------+      +--------+      +--------+|         |
|        || CAP 1  |      | CAP 2  |      | CAP 3  || 100 px navy
|        || up to 2|      | up to 2|      | up to 2|| (room for 2-line wrap)
|        || lines  |      | lines  |      | lines  ||         |
|        |+--------+      +--------+      +--------+|         |
|              16 px cream gap                                |
+-------------------------------------------------------------+
|        48 px hi-vis yellow footer — DIGGERLID wordmark      |
+-------------------------------------------------------------+
1080 tall

Width:   2*8 + 2*175 + 3*502 + 2*24 = 16 + 350 + 1506 + 48 = 1920 ✓
Height:  8 + 16 + 892 + 100 + 16 + 48 = 1080 ✓
```

**Adaptive sizing (`_resolve_layout`):**

Caption width depends on frame width, which depends on caption height, which
depends on caption line count, which depends on caption width. The function
iterates up to 5 times until `frame_w` stops shrinking — at that point the
wrap is computed at the same width we'll render with, so captions never
overflow horizontally.

- Initial guess: `frame_w = MAX_FRAME_W = 502` (the v5 width).
- Each iteration: re-wrap all 3 beats at the current `caption_max_w =
  frame_w − 32`, find the longest wrap (`max_lines`), recompute
  `caption_h = max_lines × 34 + 16`, recompute `frame_h` from the
  remaining vertical budget (capped at MAX_FRAME_H = 892, floored at 200),
  recompute `frame_w = round(frame_h × 9/16)`.
- Loop exits as soon as the new `frame_w` is no longer shrinking.

For real-world beats this converges in 1–2 passes:

| Caption lines (longest beat) | caption_h | frame_h | frame_w |
|---|---|---|---|
| 1 | 50 | 892 | 502 |
| 2 | 84 | 892 | 502 |
| 3 | 118 | 874 | 492 |
| 4 | 152 | 840 | 472 |
| 5 | 186 | 806 | 453 |
| 6 | 220 | 772 | 434 |
| 8 | 288 | 704 | 396 |

**Caption wrapping (`_wrap_caption`):**
1. Truncate the beat to MAX_CAPTION_WORDS (50) up front. Excess words drop
   off the end with a `…`.
2. If `<label>  ·  <beat>` fits one line at `caption_max_w`, return it.
3. Otherwise greedy word-fill line by line. Line 1 carries the label
   prefix; subsequent lines are beat-text only.
4. Only chop a word character-by-character (with `…`) if a single word is
   wider than `caption_max_w` — vanishingly rare with normal English at
   the layout's strip widths.

**Brand presence:** hi-vis yellow now appears only in (a) the 8-px perimeter
border and (b) the 48-px brand-wordmark footer at the bottom. The footer + the
bottom border merge visually into one 56-px yellow strip. Inside the working
area everything sits on cream — closer to a real director's storyboard sheet,
less ad-magazine billboard.

If you change any of FRAME_W / FRAME_H / GUTTER / OUTER_PAD / FOOTER_H /
CAPTION_H / TOP_GAP, recompute both sums and verify with a stub-frame test
before shipping. The footer is anchored at `CANVAS_H − BORDER − FOOTER_H`,
so over-tall content silently gets painted over by the footer rectangle.

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
