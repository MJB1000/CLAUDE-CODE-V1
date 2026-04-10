# Simulation Report — Figma Wireframe Workflow Test

**Date:** 2026-04-10
**Scenario:** Mornings DTC coffee subscription launch — email + 2 Instagram ads
**Framework version:** Marketing Team with Dana review + wireframe combined workflow
**Personas tested:** Sofia (Strategist), Charlie (Copywriter), Dana (Designer)

---

## What Was Tested

The updated workflow where Dana reviews copy AND produces Figma wireframes in a single pass, rather than a separate post-approval design step. Specifically:

1. Sofia derives Design Requirements FROM strategy (positioning -> layout, audience -> fonts, etc.)
2. Charlie writes copy with content hierarchy notes but NO wireframes
3. Dana reviews copy and builds wireframes for locked sections simultaneously
4. Dana's feedback includes a Wireframes section with Figma build details
5. Handoff protocol: confirm -> lock -> suggest next step at every transition
6. Campaign Summary Document at launch gate includes wireframe outputs

---

## What Worked

### 1. Design Requirements derived from strategy (Sofia)

The strategy-to-design derivation table is strong. Mapping positioning -> layout feel, audience -> font choices, tone -> CTA style, and channel -> dimensions produces specific, actionable design specs without requiring a separate design brief step. Dana had everything she needed to build wireframes without asking questions.

**Specific win:** The brief's Design Specs table (font sizes per channel, exact hex colors, CTA radius, padding values) eliminated ambiguity. Dana never had to guess at a design decision — she could build directly from the specs.

### 2. Content hierarchy from Charlie (no wireframes)

Charlie's content hierarchy notes were the critical bridge between copy and wireframes. By listing sections in priority order with actual copy text and layout guidance, Charlie gave Dana everything needed to build the wireframe without any back-and-forth.

**Specific win:** Charlie's note "CTA appears once, after the body. It is the primary action." told Dana exactly where to place the button and that there should be no duplicate CTA. This kind of structural intent is exactly what the hierarchy format captures that raw copy alone does not.

### 3. Combined review + wireframe production (Dana)

The combined pass works. Dana reviews a section, and if it passes, she builds the wireframe immediately. This eliminates the old workflow where copy had to be fully approved before any design work started. In this simulation:
- Round 1: Dana built wireframes for 22/23 sections (1 held back due to Must Fix)
- Round 2: Only 2 Figma calls needed to update the fixed sections
- Total delay from combined workflow: zero rounds. Design production happened alongside review.

**Specific win:** The feed ad CTA was held back in R1 (Must Fix) while all other sections were built. In R2, only the CTA badge text needed updating — a single `use_figma` call. No full rebuild.

### 4. Handoff protocol

Every transition followed confirm -> lock -> suggest next step:
- Sofia: "Brief is complete, scores 9/10. Ready to spin up Charlie. Shall I proceed?"
- Charlie: "Copy is done. 3 deliverables written, all self-checked. Ready for Dana. Proceed?"
- Dana (R1): "Review complete. 1 Must Fix. 22/23 wireframe sections built. Sending Charlie back. Proceed?"
- Charlie: "Fixes applied. Changes listed. Ready for Dana Round 2. Proceed?"
- Dana (R2): "All clear. Wireframes complete. Back to Sofia for launch gate."
- Sofia: "Campaign summary attached. Ready to ship?"

The CD never had to ask "what's next?" at any point.

### 5. Campaign Summary with wireframe outputs

The launch gate document includes wireframe section counts, screenshot references, production stats (25 use_figma calls, 7 screenshots), and per-section build status. A stakeholder reading this document understands not just what copy was written but what the visual layouts look like.

---

## What Broke / Friction Points

### 1. Charlie's email word count fell below the constraint floor

**Issue:** Brief specified 150-word max for email body. Charlie wrote 68 words. The brief said "max 150" — no minimum was specified. Charlie flagged it as an open question, which was correct behavior. But the constraint in the brief was ambiguous: "max 150 words" could imply a reasonable length range (e.g., 100-150), not "as short as possible."

**Impact:** Low. The copy is strong at 68 words and the brand voice demands brevity. But a Copywriter in a real engagement might interpret "max 150" as a target range.

**Fix:** Briefs should specify a range (e.g., "100-150 words") when there is an implicit minimum, or explicitly state "no minimum — brevity is preferred."

### 2. Feed ad CTA platform constraint was unknown

**Issue:** Charlie used "Shop Now" as a default for the feed ad CTA. Dana caught it as a Must Fix. But the real question — whether Instagram even allows custom CTA button text for this ad format — was never resolved. The fix assumed custom text is possible, but it may not be.

**Impact:** Medium. If Meta Ads Manager forces "Shop Now" as the only CTA option for this format, the Must Fix is moot and the campaign summary should document it as a platform constraint, not a creative choice.

**Fix:** The brief should include platform-specific CTA constraints. Sofia should research ad format constraints during the brief phase, not leave it for Charlie or Dana to discover.

### 3. No design system = 100% manual Figma builds

**Issue:** All 25 `use_figma` calls built from scratch because no design system exists for this client. Every button, text style, and spacing value was hardcoded. In a real production environment, this means no reusable components for future campaigns.

**Impact:** Medium for this sprint (it works). High for the next sprint (everything gets rebuilt from scratch again).

**Fix:** Dana should create reusable components during the first campaign and save them as a design system file (`design-systems/mornings.md` + Figma library). The framework mentions `search_design_system` but does not mandate creating one when none exists. Add a rule: "First campaign for a new client: Dana creates a basic component library (buttons, text styles, color variables) during wireframe production."

### 4. Wireframe sections vs copy sections naming mismatch

**Issue:** Charlie's content hierarchy uses descriptive names ("Hero Image," "Offer Block," "Text Zone") while Dana's Figma sections use technical names ("Hero-Image-Placeholder," "textOverlayId," "storiesTextId"). There is no enforced naming convention between the two.

**Impact:** Low for this sprint. Could cause confusion in larger campaigns with 10+ sections where Charlie references "Value Props" and Dana has to figure out which Figma frame that maps to.

**Fix:** Establish a naming convention in the brief. Content hierarchy section names should match Figma frame names. Charlie names the sections; Dana uses those names as Figma layer names.

### 5. Screenshot references are fictional in simulation

**Issue:** Dana references screenshots (e.g., "Email-Launch-1a-R1.png") but in simulation mode, no actual Figma MCP calls are made, so no screenshots exist. The Campaign Summary references screenshots that don't exist.

**Impact:** Expected for simulation. In a real workflow with Figma MCP connected, this is a non-issue. But it means the CD cannot actually see the wireframes during simulation — they must trust the Figma call descriptions.

**Fix:** For simulation mode, Dana should produce ASCII text wireframes as fallback (per DESIGNER.md: "If Figma MCP is NOT connected, produce text wireframes using ASCII layout with design spec blocks"). This simulation did not do that — it described the calls instead. The description approach is more useful for testing the workflow, but less useful for a real CD reviewing outputs.

### 6. Brief background color inconsistency

**Issue:** Sofia's brief specifies #FFFAF5 as the background color. Charlie's content hierarchy notes reference #FFFBF5 (note the B vs A). This is a minor hex code difference (nearly invisible visually) but it is an inconsistency between the brief and the copy hierarchy notes.

**Impact:** Very low. The colors are virtually identical. But in production, Dana should follow the brief specs, not Charlie's notes.

**Fix:** Charlie should not specify hex colors in content hierarchy notes — those are Dana's domain per the brief specs. Content hierarchy should describe intent ("warm off-white background") not implementation ("#FFFBF5").

### 7. Batch review format for ads file

**Issue:** Charlie put both ad deliverables (1b feed + 1c stories) in a single file (03-COPY-ADS.md). This is efficient for the batch workflow, but when Dana needs to reference specific sections, the file paths are ambiguous (both are "03-COPY-ADS.md").

**Impact:** Low. Dana uses section headers to disambiguate. But the Review Request and Review Feedback files have to use "[03-COPY-ADS.md: Deliverable 1b]" notation rather than simple file paths.

**Fix:** For batched deliverables that share a file, the framework works fine. The "[file:section]" notation in feedback is adequate. No change needed — just noting the pattern.

---

## Comparison to Previous Simulations (Pre-Figma Workflow)

| Aspect | Previous (no wireframes) | Current (Dana wireframes) | Assessment |
|---|---|---|---|
| Total agent handoffs | 5 (Sofia -> Charlie -> Dana -> Charlie -> Sofia) | 5 (same) | No change |
| Dana's output | Review feedback only | Review feedback + wireframe builds | More valuable per pass |
| Design production step | Separate (after copy approved) | Combined with review | Eliminated one full round |
| Time to visual output | After all copy rounds complete | During first review round | Significantly faster |
| Brief requirements | Copy specs only | Copy specs + design specs | More upfront work for Sofia |
| Charlie's output | Copy only | Copy + content hierarchy | Slightly more work, but structured and useful |
| CD launch gate | Copy + review summary | Copy + review + wireframe screenshots + production stats | Much richer stakeholder artifact |
| Figma calls per sprint | 0 (separate step) | 25 (integrated) | New production load on Dana |

**Net assessment:** The combined workflow is strictly better. It does not add rounds or handoffs. It front-loads design production into the review pass, which means wireframes are ready when copy is approved — no waiting. The only added cost is the Design Requirements section in Sofia's brief (marginal) and the content hierarchy in Charlie's output (moderate but valuable).

---

## Rules to Carry Forward

1. **Briefs must specify word count ranges, not just maximums,** when there is an implicit minimum length expectation.
2. **Platform CTA constraints should be researched during brief phase,** not discovered during review.
3. **First campaign for new client: Dana creates a basic component library** (buttons, text styles, color variables) during wireframe production.
4. **Charlie does not specify hex colors in content hierarchy notes.** Describe intent; Dana implements per brief specs.
5. **Content hierarchy section names should match Figma layer names.** Charlie names; Dana adopts.
6. **When Figma MCP is not connected, produce ASCII text wireframes** as fallback — do not just describe the calls.

---

## Verdict

The updated workflow (Dana reviews copy AND produces wireframes in one pass) works as designed. It eliminates a full production round, produces richer launch gate artifacts, and does not add friction to the existing handoff protocol. The six friction points identified are all edge cases or first-campaign setup costs, not structural problems with the workflow.

**Recommendation:** Ship this workflow as the default. The Design Requirements derivation from strategy and the content hierarchy from Copywriter are the two structural additions that make the combined pass possible — both should be mandatory, not optional.
