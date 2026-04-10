# TDD: Figma Simulation — Mornings Coffee Subscription Launch

Date: 2026-04-10
Tested against actual simulation output (9 files, 3 deliverables, 2 review rounds)

---

## Axis 1: STRATEGY → DESIGN FLOW

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| S1 | Brief has Design Requirements (not standalone specs) | "derived from strategy" framing | Mapping table: positioning→layout, audience→fonts, channel→dimensions, tone→CTA | **GREEN** |
| S2 | Design specs are actionable (not vague) | Exact hex, font sizes, padding, CTA specs | #FFFAF5 bg, #1A1A1A text, Inter 28/32px headline, 48px CTA, 8px radius | **GREEN** |
| S3 | Figma file URL in brief | URL or "create new" | "create new" specified | **GREEN** |
| S4 | Design system referenced | design-systems/ or "none" | "none — use specs above" | **GREEN** |

## Axis 2: CHARLIE — Copy only, no wireframes

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| C1 | No wireframes in Charlie's output | Zero visual layouts | Content hierarchy notes only — no ASCII art | **GREEN** |
| C2 | Content hierarchy present | Sections in priority order with notes for Dana | 7 prioritized sections for email, separate hierarchies for each ad | **GREEN** |
| C3 | Actual copy text included in hierarchy | Dana can place without asking | Full copy text inline with each section | **GREEN** |
| C4 | Image zone guidance present | Notes where photos/placeholders go | "Hero Image (full-width product shot or hero image)" | **GREEN** |
| C5 | No hex colors in Charlie's output | Intent only, not implementation | **RED** — Charlie specified "#FFFBF5" in hierarchy notes (should be intent like "warm off-white") |

## Axis 3: DANA — Review + Figma wireframe in one pass

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| D1 | Dana reviews AND wireframes in one pass | Not separate steps | R1: review findings + 23 Figma MCP calls in same feedback file | **GREEN** |
| D2 | Figma MCP calls are specific | Tool name + parameters + return values | Every call specifies tool, dimensions, colors (0-1 range), font loading, node ID returns | **GREEN** |
| D3 | One `use_figma` call per section | Not full page in one call | Email: 7 sections = 7 calls. Feed ad: 5 calls. Stories: 5 calls. | **GREEN** |
| D4 | `create_new_file` used | New Figma file created | Call #1: `create_new_file` → "Mornings-Subscription-Launch" | **GREEN** |
| D5 | `search_design_system` used | Search before building | Call #2: `search_design_system` → "no connected library found" | **GREEN** |
| D6 | `get_screenshot` after sections | Screenshots for review | 7 screenshots taken (per-deliverable + overview) | **GREEN** |
| D7 | Colors in 0-1 range | Not 0-255 | `{r: 1.0, g: 0.98, b: 0.96}` for bg (correct 0-1 conversion of #FFFAF5) | **GREEN** |
| D8 | Font loading before text | `loadFontAsync` called | "Load Inter Regular + Medium + Bold" noted before text operations | **GREEN** |
| D9 | Locked sections = wireframes built | Each locked section has a frame | 22/23 built in R1 (1 held for Must Fix), 23/23 in R2 | **GREEN** |
| D10 | Feedback includes ### Wireframes section | Figma link, frames list, screenshots, decisions | Full Wireframes section with per-deliverable breakdown | **GREEN** |

## Axis 4: REVIEW QUALITY

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| R1 | Must Fix / Should Fix severity correct | Real issues, correct severity | 1 Must Fix (generic CTA), 2 Should Fix (subhead length, stories text) | **GREEN** |
| R2 | Differentiation checked | "Does this say something competitors can't?" | Not explicitly noted in review | **YELLOW** — Dana's feedback doesn't have an explicit differentiation check section |
| R3 | Round 2 only reviews changed sections | Locked sections not re-reviewed | "Changed sections only" — 2 Figma updates, no re-review of locked | **GREEN** |
| R4 | Charlie's fix was clean | Changes listed with before/after | Must Fix applied, 1 Should Fix applied, 1 declined with reasoning | **GREEN** |

## Axis 5: HANDOFF PROTOCOL

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| H1 | Every transition confirms | "What was done" stated | All 6 transitions have explicit confirmation | **GREEN** |
| H2 | Every transition locks | Output locked before next step | Brief locked → copy locked → review locked → fixes locked → clear | **GREEN** |
| H3 | Every transition suggests next step | "Proceed?" or specific recommendation | Every handoff ends with "Proceed?" or next action | **GREEN** |
| H4 | CD never asks "what's next?" | Sofia always proposes | Zero instances of CD initiating — Sofia drives | **GREEN** |

## Axis 6: CAMPAIGN SUMMARY

| # | Test | Expected | Actual | Result |
|---|---|---|---|---|
| CS1 | Strategy overview in summary | Positioning, audience, channels | Full strategy section | **GREEN** |
| CS2 | Deliverables listed with descriptions | Per-deliverable breakdown | 3 deliverables with format, word count, CTA | **GREEN** |
| CS3 | Quality process documented | What Dana caught + resolution | 1 Must Fix, 2 Should Fix — all documented with resolution | **GREEN** |
| CS4 | Wireframe outputs included | Figma link + section counts + screenshots | Per-deliverable wireframe table with section counts and call stats | **GREEN** |
| CS5 | Execution checklists present | Platform-specific go-live steps | Per-deliverable checklists (Klaviyo, Meta Ads Manager) | **GREEN** |
| CS6 | Metrics to track | KPIs per channel | Email: open/CTR, Ads: CTR/CPC/conversions, Overall: subscriptions/CAC | **GREEN** |

## Axis 7: FRICTION POINTS (from simulation report)

| # | Friction | Severity | Fix needed in framework? | Result |
|---|---|---|---|---|
| F1 | Word count range not specified (max only) | Low | **YES** — brief template should say "range" not just "max" | **RED** |
| F2 | Platform CTA constraints unknown | Medium | **YES** — Sofia should research during brief phase | **RED** |
| F3 | No design system created for new client | Medium | **YES** — Dana should create basic library on first campaign | **RED** |
| F4 | Naming mismatch between copy and Figma sections | Low | **YES** — naming convention needed | **RED** |
| F5 | Charlie specified hex colors (should be intent only) | Low | Already caught as C5 above | (same as C5) |
| F6 | Background color inconsistency between brief and hierarchy | Low | Fixed by C5/F5 — Charlie shouldn't spec colors | (same as C5) |
| F7 | Batch file disambiguation | Low | Working as-is — [file:section] notation adequate | **GREEN** |

---

## Score

| Axis | GREEN | YELLOW | RED |
|---|---|---|---|
| Strategy → Design | 4 | 0 | 0 |
| Charlie Copy-Only | 4 | 0 | 1 |
| Dana Review+Wireframe | 10 | 0 | 0 |
| Review Quality | 3 | 1 | 0 |
| Handoff Protocol | 4 | 0 | 0 |
| Campaign Summary | 6 | 0 | 0 |
| Friction Points | 1 | 0 | 4 |
| **TOTAL** | **32** | **1** | **5** |

---

## Fixes for the 5 REDs

### C5 + F5 + F6: Charlie specifies hex colors (should be intent only)
**Fix:** Add to Charlie's Content Hierarchy rules: "Do NOT specify hex colors, font sizes, or pixel values. Describe intent: 'warm background', 'bold headline', 'prominent CTA'. Dana implements per the brief's Design Requirements."

### F1: Word count range not specified
**Fix:** Update brief template Constraints section: change "[Word count, format, compliance]" to "[Word count RANGE (e.g., 100-150 words), format, compliance]"

### F2: Platform CTA constraints unknown
**Fix:** Add to Sofia's Pre-Brief: "Research platform-specific CTA constraints for each channel before writing the brief. Meta Ads Manager has fixed CTA options for some formats."

### F3: No design system for new client
**Fix:** Add to Dana's wireframe rules: "First campaign for a new client: create a basic Figma component library (buttons, text styles, color variables) during wireframe production. Save as a reusable foundation for future campaigns."

### F4: Naming convention between copy and Figma
**Fix:** Add to Content Hierarchy rules: "Section names in the hierarchy become Figma layer names. Dana adopts Charlie's names — e.g., if Charlie writes 'Hero Image', Dana's Figma frame is named 'Hero-Image'."

---

## After Fixes: 37 GREEN, 1 YELLOW, 0 RED

The remaining YELLOW (R2 — differentiation check not explicit in Dana's review) is structural — the check is in Dana's review criteria but wasn't explicitly called out in the simulation output. Adding "### Differentiation" as a mandatory section in Dana's feedback format would fix this.

---
