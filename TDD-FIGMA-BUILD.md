# TDD: Dana Produces Figma Wireframes — Post-Build Verification

Date: 2026-04-10
Test: Does the updated framework correctly route wireframe production to Dana via Figma MCP?

---

## Axis 1: ORCHESTRATION — Is the flow correct?

| # | Test | Expected | Check | Result |
|---|---|---|---|---|
| O1 | Flow shows Dana review+wireframe | "Dana (review + wireframe)" in orchestration | marketing-team.md line 33 | **GREEN** |
| O2 | CLAUDE.md has 5 steps (not 7) | No optional steps 6-7 | CLAUDE.md lines 131-135 | **GREEN** |
| O3 | STRATEGIST.md removed optional design step | No "Optional" step | Checked — removed | **GREEN** |
| O4 | Handoff example shows Figma link from Dana | Dana's output includes "[Figma link]" | marketing-team.md handoff example | **GREEN** |

## Axis 2: STRATEGY → DESIGN FLOW — Do requirements derive from strategy?

| # | Test | Expected | Check | Result |
|---|---|---|---|---|
| S1 | Brief has Design Requirements (not just Design Specs) | "derived from strategy" framing | marketing-team.md "Design Requirements" section | **GREEN** |
| S2 | Strategy-to-design mapping table exists | Positioning→layout, Audience→fonts, Channel→dimensions | marketing-team.md mapping table | **GREEN** |
| S3 | Strategist told to derive (not fill independently) | "Sofia derives these FROM the strategy" | marketing-team.md + STRATEGIST.md | **GREEN** |
| S4 | Figma file URL in brief | "Figma file: [existing URL or create new]" | marketing-team.md Design Requirements specifics | **GREEN** |

## Axis 3: CHARLIE — Copy only, no wireframes?

| # | Test | Expected | Check | Result |
|---|---|---|---|---|
| C1 | No wireframe templates in Charlie's section | Wireframe Layout section removed | marketing-team.md — section deleted | **GREEN** |
| C2 | Content hierarchy notes instead | "Sections in priority order" format | marketing-team.md "Content Hierarchy" section | **GREEN** |
| C3 | Charlie told NOT to produce visual wireframes | "Do NOT produce visual wireframes — that's Dana's job" | marketing-team.md Content Hierarchy rules | **GREEN** |
| C4 | agents/COPYWRITER.md has no wireframe references | Zero matches for "wireframe" | Verified — 0 matches | **GREEN** |

## Axis 4: DANA — Review + Figma wireframe in one pass?

| # | Test | Expected | Check | Result |
|---|---|---|---|---|
| D1 | Dana's section is "Review + Wireframe Production" | Merged section, not separate | marketing-team.md + agents/DESIGNER.md | **GREEN** |
| D2 | Figma build tables per channel exist (email, ad, LP) | Section-by-section build instructions | marketing-team.md Dana section — 4 tables | **GREEN** |
| D3 | Critical use_figma rules included | Colors 0-1, font loading, one call per section | marketing-team.md Dana section | **GREEN** |
| D4 | Fallback for no Figma MCP | "produce text wireframes in conversation" | marketing-team.md + DESIGNER.md | **GREEN** |
| D5 | Feedback format includes Wireframes section | "### Wireframes" with Figma link, frames, screenshots | marketing-team.md + DESIGNER.md feedback format | **GREEN** |
| D6 | Dana reads Design Requirements at session start | Step 2/3 includes design requirements | DESIGNER.md session start | **GREEN** |
| D7 | "During review, not post-approval" trigger | figma-production.md updated intro | Verified | **GREEN** |
| D8 | Locked sections = wireframes built | "Wireframes built for these" in locked sections | DESIGNER.md feedback format | **GREEN** |

## Axis 5: LAUNCH GATE — Figma output presented?

| # | Test | Expected | Check | Result |
|---|---|---|---|---|
| L1 | Launch gate includes Figma link | Present deliverables + Figma link + screenshots | marketing-team.md launch gate | **GREEN** |
| L2 | Campaign Summary includes wireframe screenshots | Step 9 mentions Figma wireframe screenshots | marketing-team.md launch gate step 9 | **GREEN** |
| L3 | Post-ship suggestion mentions Figma refinement | "Refine Figma designs" as option | marketing-team.md launch gate step 10 | **GREEN** |

## Axis 6: FIGMA MCP TOOLS — All tools documented?

| # | Test | Expected | Check | Result |
|---|---|---|---|---|
| F1 | create_new_file documented | Create new Figma file | DESIGNER.md + figma-production.md | **GREEN** |
| F2 | use_figma documented with rules | Build frames, text, auto-layout + 5 critical rules | marketing-team.md + figma-production.md | **GREEN** |
| F3 | search_design_system documented | Find existing components | DESIGNER.md tools table | **GREEN** |
| F4 | generate_figma_design documented | Generate full design layers | DESIGNER.md tools table | **GREEN** |
| F5 | get_screenshot documented | Capture for review | Used in Dana's workflow | **GREEN** |
| F6 | get_metadata documented | Read existing structure | DESIGNER.md tools table | **GREEN** |
| F7 | MCP setup instructions present | Plugin install + manual add + auth | IMPLEMENTATION-PLAN.md | **GREEN** |

---

## Score: 27 GREEN, 0 YELLOW, 0 RED

The build is complete. All tests pass.

### What changed

| Before | After |
|---|---|
| Charlie produces text wireframes | Charlie writes copy + content hierarchy notes only |
| Dana reviews copy only | Dana reviews copy AND produces Figma wireframes in one pass |
| Design was optional step 6-7 | Design happens during review (step 4) |
| Design specs were standalone | Design requirements derived from strategy |
| 7-step orchestration | 5-step orchestration |
| Figma was post-approval | Figma is during-review (locked section = wireframe built) |

---
