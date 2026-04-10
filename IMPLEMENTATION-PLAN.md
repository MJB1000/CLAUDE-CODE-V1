# Implementation Plan: Dana Produces Figma Wireframes via MCP

**Handoff document for Claude Code / Cowork implementation**
**Date:** 2026-04-10
**Repo:** `github.com/MJB1000/CLAUDE-CODE-V1`
**Branch:** `main`

---

## What to Build

Dana (Designer) reviews copy AND produces Figma wireframes in one pass. Design requirements flow from Sofia's strategy through to Dana's Figma production. Charlie writes copy only — no wireframes.

## Updated Workflow

```
Sofia (strategy + brief with design requirements derived from strategy)
  → Charlie (copy ONLY — structured by section with content hierarchy notes)
  → Dana (review copy + produce Figma wireframes for locked sections)
  → Charlie (fix copy if must-fix)
  → Dana (re-review changed sections + update Figma wireframes)
  → Sofia (launch gate: Figma link + Campaign Summary + execution checklists)
```

Design is NOT a separate optional step. Dana reviews AND wireframes in one pass. When she locks a section, she builds the Figma wireframe for it.

---

## Figma MCP Setup (prerequisite)

### In Cowork
```
claude plugin install figma@claude-plugins-official
```
Or manually:
```
claude mcp add --transport http figma https://mcp.figma.com/mcp
```
Then: `/mcp` → `figma` → Authenticate (OAuth)

### Figma MCP Tools Dana Uses

| Tool | Purpose |
|---|---|
| `create_new_file` | Create a new Figma file for the campaign |
| `use_figma` | Build frames, text, auto-layout, components, variables — ONE section per call |
| `generate_figma_design` | Generate full design layers from a description |
| `search_design_system` | Find existing components in connected Figma libraries |
| `get_screenshot` | Capture current state for CD review |
| `get_metadata` | Read existing Figma file structure |
| `get_design_context` | Extract design data as structured code |
| `get_variable_defs` | Extract color/spacing/typography variables |

### Critical `use_figma` Rules (from official Figma MCP docs)

1. Colors are 0–1 range, NOT 0–255. Red = `{r: 1, g: 0, b: 0}`
2. Load fonts before ANY text operation: `await figma.loadFontAsync({family, style})`
3. ONE section per `use_figma` call — don't build entire page in one script
4. Return ALL created/mutated node IDs from every call
5. Set FILL sizing AFTER `appendChild()`, not before
6. Position new frames away from (0,0) — scan existing content first
7. Await every Promise — unawaited async = silent failures
8. Scripts are atomic — on failure, file state doesn't change (safe to retry)

---

## Files to Modify

### 1. `skills/marketing-team.md` (portable skill — primary target)

#### Session Orchestration
Replace current flow with:
```
Sofia (brief) → Charlie (write) → Dana (review + wireframe) → Charlie (fix) → Dana (clear + final wireframe) → Sofia (publish)
```

#### Sofia's Brief — Design Requirements (derived from strategy)
Replace current "Design Specs" with "Design Requirements (derived from strategy)":

```
### Design Requirements (derived from strategy)

*Sofia derives these FROM the strategy — they are not a separate exercise.*

| Strategy element | Design implication |
|---|---|
| Positioning | Layout feel (clean/bold/playful/minimal) |
| Audience | Font size, contrast, mobile priority |
| Channel | Dimensions (600px email, 1080x1080 feed, 1080x1920 stories, 1440px LP) |
| Tone | Color warmth, CTA style (rounded/sharp, subtle/bold) |
| Key message | Visual hierarchy — what's biggest, what's above the fold |

**Specifics:**
- Font: [from brand or defaults: Inter, 32px headline, 16px body]
- Colors: bg [#], text [#], CTA [#], accent [#]
- CTA style: [height, radius, text style]
- Section padding: [e.g., 40px vertical]
- Design system: [design-systems/client.md or "none — use defaults"]
- Figma file: [existing URL or "create new"]
```

#### Charlie's Role — Copy Only
- DELETE the entire "Wireframe Layout" section (all email/ad/LP templates + design spec blocks)
- Charlie writes copy structured by section with content hierarchy notes:
  ```
  Sections (in priority order):
  1. Hero (most prominent): headline + subhead + CTA
  2. Value Props (3 equal weight): heading + body each
  3. Social Proof: stats with attribution
  4. Offer Block: discount details + CTA
  ```
- Charlie does NOT produce visual layouts

#### Dana's Role — Review + Wireframe Production
Replace Dana's current review-only section with a merged section:

```
## Review + Wireframe Production

Dana reviews copy AND produces wireframes in one pass. When a section passes review,
Dana builds the wireframe for it immediately.

### Workflow per deliverable

1. Read copy + Campaign Context + Design Requirements from brief
2. Review copy section by section (Must Fix / Should Fix / Escalate)
3. For each LOCKED section: build the Figma wireframe
4. Screenshot each section after building
5. Signal done with copy review + wireframe status

### If Figma MCP is connected

Load `skills/figma-production.md` for critical MCP rules, then:

1. `create_new_file` or open existing file (from brief's Figma URL)
2. `search_design_system` — find existing brand components
3. Build sections (one `use_figma` call per section):

   **Email (600px):**
   | Call | Section |
   |---|---|
   | 1 | Email wrapper — 600px wide, auto-layout vertical |
   | 2 | Header — logo placeholder + preheader |
   | 3 | Hero zone — image placeholder or color block |
   | 4 | Body — headline text + body paragraphs |
   | 5 | CTA — button component, centered |
   | 6 | Footer — sign-off + unsubscribe links |

   **Social Ad Feed (1080x1080):**
   | Call | Section |
   |---|---|
   | 1 | Ad frame — 1080x1080, background fill |
   | 2 | Logo — top left corner placement |
   | 3 | Product zone — center frame, image placeholder |
   | 4 | Text overlay — bottom third, headline + supporting line |
   | 5 | CTA — button at bottom |
   | 6 | Offer badge — corner tag with offer text |

   **Social Ad Stories (1080x1920):**
   | Call | Section |
   |---|---|
   | 1 | Ad frame — 1080x1920, background fill |
   | 2 | Logo — top center |
   | 3 | Visual zone — top half, image placeholder |
   | 4 | Text zone — bottom half, headline + supporting line |
   | 5 | CTA — swipe-up or button |

   **Landing Page (1440px):**
   | Call | Section |
   |---|---|
   | 1 | Page wrapper — 1440px wide, auto-layout vertical |
   | 2 | Header — logo + nav + CTA button |
   | 3 | Hero — headline + subhead + CTA, centered |
   | 4 | Value Props — 3-column auto-layout, heading + body each |
   | 5 | Social Proof — stats row with attribution |
   | 6 | Offer block — background fill + offer text + CTA |
   | 7 | Footer — links + legal |

4. `get_screenshot` after each section
5. `get_screenshot` of full deliverable

### If Figma MCP is NOT connected (fallback)

Produce text wireframes with design spec blocks (same templates but in ASCII art).

### Feedback format with wireframes

```
## Round [N] — [date]

Ready for Copywriter: YES / NO

### Must Fix
[copy issues]

### Should Fix
[copy issues]

### Wireframes
- [Deliverable name]: [Figma file link or "text wireframe below"]
- Frames built: [list of sections]
- Screenshots: [attached or inline]
- Design decisions: [any layout choices made and why]

### Locked Sections
[sections that passed — wireframes built for these]

### Cleared
[summary]
```
```

#### Handoff Protocol Updates

After Dana Round 1:
```
"Review complete. 2 must-fix in copy, 10 sections locked.
Wireframes built in Figma for all locked sections.
[Figma link] — screenshots attached.
Sending Charlie back for copy fixes. Proceed?"
```

After Dana Round 2 (all clear):
```
"All clear. Wireframes complete — all sections built in Figma.
[Figma link] — final screenshots attached.
Ready for launch gate?"
```

#### Sofia's Launch Gate
- Present: deliverables, Dana's findings, Figma file link + screenshots
- Campaign Summary Document includes Figma wireframe screenshots
- Final: "Shipped. Refine Figma designs, start next deliverable, or write retro?"

---

### 2. `agents/DESIGNER.md`

- Merge "What You Review" section with "Design Production (Figma)" section
- Dana's session start: read copy → read design requirements → review + wireframe simultaneously
- Add critical `use_figma` rules inline (the 8 rules listed above)
- Remove the trigger "After copy is cleared and launch gate approved" — design happens DURING review

### 3. `agents/STRATEGIST.md`

- Remove optional design steps (6-7) from session orchestration
- Update "Briefing Designer" — Dana reviews AND wireframes, not just reviews
- Add: Sofia derives Design Requirements from strategy elements (positioning → layout feel, audience → font size, etc.)
- Launch gate step: include Figma link and screenshots

### 4. `agents/COPYWRITER.md`

- Remove ALL wireframe references (the "Wireframe Layout" section if any exists)
- Charlie's "When Done" includes content hierarchy notes: section order + priority, but NO visual wireframes

### 5. `CLAUDE.md`

- Update orchestration flow: remove optional steps 6-7, update step 4 to: "Designer session — reviews copy, writes feedback, produces Figma wireframes for locked sections"
- Keep DESIGN-BRIEF.md and DESIGN-REQUEST.md in handoff list (used when CD wants additional Figma refinement after launch)

### 6. `skills/figma-production.md`

- Update intro: Dana produces wireframes DURING review, not as a separate post-approval step
- Keep all critical MCP rules (they're correct and essential)
- Add: section-by-section build tables for email, ad feed, ad stories, landing page

---

## How Strategy → Design Requirements Flow

```
Sofia's Strategy                        Dana's Figma Build
─────────────────                       ───────────────────
Positioning: "practical"          →     Layout: clean, minimal, no decorative elements
Audience: "women 25-40, mobile"   →     Fonts: large (mobile-scan), high contrast
Channel: "email + Instagram"      →     Frames: 600px email + 1080x1080 + 1080x1920
Tone: "warm friend"               →     Colors: warm palette, approachable CTA
Key message: "works with any case" →    Hierarchy: product shot > headline > CTA
Brand assets: "[logo, colors]"    →     Design system: bind to brand variables
```

Sofia writes this mapping in the brief's Design Requirements section. Dana reads it and builds accordingly. The strategy IS the design brief.

---

## Verification Steps

1. Brief a campaign with visual deliverables (email + social ads)
2. Charlie writes copy only — verify no wireframes in his output
3. Dana reviews AND produces Figma wireframes — verify Figma file has correct frames
4. Verify design requirements in brief trace back to strategy decisions
5. Verify handoff protocol: every transition confirms, locks, suggests next step
6. Verify Campaign Summary includes Figma link + screenshots
7. Test Figma fallback: disconnect Figma → Dana produces text wireframes instead
8. Test in Cowork: full pipeline runs from GitHub repo connection

---

## Implementation Order

1. Update `skills/marketing-team.md` first (this is the portable skill — if it works here, everything else follows)
2. Update `agents/DESIGNER.md` to match
3. Update `agents/STRATEGIST.md` to match
4. Update `agents/COPYWRITER.md` to remove wireframe references
5. Update `CLAUDE.md` orchestration
6. Update `skills/figma-production.md` trigger language
7. Sync templates (generic + project-folder)
8. Run TDD to verify
9. Commit and push
