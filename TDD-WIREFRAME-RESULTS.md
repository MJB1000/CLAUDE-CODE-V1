# TDD: End-to-End Creative Pipeline

Date: 2026-04-10
Test: Can the framework produce a strategy document, email wireframes, ad wireframes,
Figma-ready output, and a process overview as a single deliverable package?

---

## Pipeline Being Tested

```
CD briefs Sofia → Sofia writes strategy → Charlie writes copy + wireframes
→ Dana reviews → Charlie fixes → Dana clears → Sofia packages:
  1. Strategy & process overview document
  2. Email design wireframes (text + Figma-ready specs)
  3. Ad design wireframes (text + Figma-ready specs)
  4. Process summary for the CD
```

---

## Axis 1: STRATEGY DOCUMENT — Does it exist as a deliverable?

### TEST-SD1: Does the skill produce a strategy document, not just a brief?
**Expected:** The CD gets a document they can share with stakeholders — not just
internal handoff files, but an actual strategy doc with positioning, audience,
channels, timeline, budget allocation, and KPIs.
**Check against skill:** The brief template has Campaign Context, Audience, Objective,
Key Message, Tone, Channel, Constraints. But these are internal fields — not a
shareable strategy document.
**Result: RED** — The skill produces a brief for the internal team. It does NOT produce
a standalone strategy document that a CD could present to a client, board, or
stakeholder. The Strapsicle session produced one (Marketing Strategy & GTM Plan),
but that was Charlie going beyond the skill spec. The skill doesn't describe a
"strategy document" as a deliverable type.

### TEST-SD2: Does the process overview exist as a document?
**Expected:** After the campaign is complete, the CD gets a one-page summary of:
what was produced, what the strategy was, what was reviewed, what the process looked like.
**Result: RED** — The skill describes a retro (what Dana caught, what worked) but
NOT a process overview document. The CD gets deliverables and a launch gate summary,
but no document that explains the end-to-end process. If a CD wants to show their
team "here's how this was produced," nothing exists.

---

## Axis 2: EMAIL WIREFRAMES — Are they complete enough for design production?

### TEST-EW1: Does Charlie produce email wireframes with actual copy placed?
**Expected:** Text wireframe showing email structure with real copy in position.
**Check against skill:** Wireframe Layout section says "include a text wireframe with
your copy" and shows a format example. Email is listed.
**Result: GREEN** — The skill specifies wireframes for emails. Format exists.

### TEST-EW2: Does the email wireframe include all necessary structural elements?
**Expected:** Preheader, header/logo area, body sections, CTA buttons, footer/unsubscribe.
**Check against skill:** The wireframe format example shows a landing page structure
(hero, VPs, social proof, offer). No email-specific wireframe template.
**Result: RED** — Only a generic wireframe example exists. No email-specific template
showing: preheader position, header with logo, body paragraphs, inline CTA, footer
with unsubscribe link. Charlie has to invent the email structure each time.

### TEST-EW3: Does the email wireframe spec what maps to Figma production?
**Expected:** Dimensions (600px wide), section heights, font hierarchy, CTA button
styling, spacing between sections — enough for Dana to build in Figma without guessing.
**Check against skill:** Charlie's wireframe is "content structure, not design."
Figma-production.md has an email build table (5 steps).
**Result: YELLOW** — Charlie's wireframe shows content hierarchy. Figma-production.md
shows the Figma build steps. But there's a GAP between them: Charlie's wireframe
doesn't include the technical specs (600px, padding, font sizes) that Dana needs.
Dana has to add those herself from the channel specs.

### TEST-EW4: Can Dana take Charlie's email wireframe and build it in Figma without asking questions?
**Expected:** Wireframe + production specs = zero questions for Figma build.
**Result: RED** — Charlie's wireframe shows content structure. The brief has Production
Specs (platform, dimensions). But nobody specifies: font sizes per section, padding
between sections, CTA button dimensions, background colors. Dana would need to
make design decisions or ask the CD. There's no wireframe-to-Figma spec bridge.

---

## Axis 3: AD WIREFRAMES — Are they complete enough for design production?

### TEST-AW1: Does Charlie produce social ad wireframes?
**Expected:** Text wireframe showing 1080x1080 or 1080x1920 ad structure.
**Check against skill:** "For social ads: show text overlay positioning on the frame."
**Result: GREEN** — The skill specifies ad wireframes with overlay positioning.

### TEST-AW2: Does the ad wireframe show text positioning on the visual frame?
**Expected:** Where the headline sits, where the CTA sits, where the logo goes,
what's left for product imagery.
**Result: RED** — The skill says "show text overlay positioning" but doesn't give
an ad-specific wireframe template. The only template is the LP grid. No ad template
showing: top third (headline zone), center (product/image zone), bottom third
(CTA + offer zone), logo placement corner.

### TEST-AW3: Does the ad wireframe specify visual zones (text vs image)?
**Expected:** Clear zones — "this area is text overlay, this area is product photo
or placeholder." Designer needs to know what's copy and what's visual.
**Result: RED** — No concept of text vs image zones in the wireframe format. Copy
is placed but there's no indication of where photography, product shots, or
background imagery goes relative to the text.

### TEST-AW4: Are ad variant wireframes produced (not just one)?
**Expected:** If brief has 3 ad variants, 3 wireframes showing different copy placement.
**Result: YELLOW** — The skill doesn't specify per-variant wireframes. Charlie
produces variant copy (different primary text + headline per variant), but the
wireframe format doesn't show how each variant's copy is laid out differently.

---

## Axis 4: FIGMA READINESS — Can the wireframes feed directly into Figma?

### TEST-FR1: Do wireframes include Figma-ready dimensions?
**Expected:** Pixel dimensions per deliverable type.
**Check against skill:** figma-production.md has a channel dimensions table.
**Result: GREEN** — Dimensions exist in figma-production.md. But they're in a
separate skill file, not in Charlie's wireframe output.

### TEST-FR2: Do wireframes include typography specs?
**Expected:** Font family, weight, size for headline/body/CTA.
**Result: RED** — No typography specs in Charlie's wireframe. Figma-production.md
mentions loading fonts but doesn't specify a font hierarchy for marketing deliverables.
The wireframe shows WHAT text goes where but not HOW it should look.

### TEST-FR3: Do wireframes include color specs?
**Expected:** Background color, text color, CTA button color, accent colors.
**Result: RED** — No color specs in Charlie's wireframe. Design system references exist
(design-systems.md) but nothing connects Charlie's wireframe to specific color values.

### TEST-FR4: Is there a spec block that bridges wireframe → Figma?
**Expected:** A "Design Spec" section at the bottom of each wireframe with:
dimensions, colors, fonts, spacing, CTA button style.
**Result: RED** — This doesn't exist. The wireframe is content-only. The design specs
live in separate files (brief Production Specs, figma-production.md, design-systems/).
Nobody assembles them into a single "here's everything Dana needs to build this."

---

## Axis 5: PROCESS OVERVIEW — Does the CD get a summary document?

### TEST-PO1: After shipping, does the CD get a one-page process summary?
**Expected:** "What we produced, how it was produced, what was caught, what to do next."
**Result: RED** — The launch gate presents a verbal summary. The retro captures
learnings. But no "Process Overview" document exists as a deliverable.

### TEST-PO2: Is the process overview shareable with stakeholders?
**Expected:** A non-technical document a CD can share with their boss or client.
**Result: RED** — Nothing in the skill produces a stakeholder-facing process doc.

---

## Summary

| # | Test | Axis | Result |
|---|---|---|---|
| SD1 | Strategy document as deliverable | Strategy | RED |
| SD2 | Process overview document | Strategy | RED |
| EW1 | Email wireframes produced | Email | GREEN |
| EW2 | Email wireframe has all structural elements | Email | RED |
| EW3 | Email wireframe specs for Figma | Email | YELLOW |
| EW4 | Email wireframe → Figma without questions | Email | RED |
| AW1 | Social ad wireframes produced | Ads | GREEN |
| AW2 | Ad wireframe shows text positioning | Ads | RED |
| AW3 | Ad wireframe specifies visual zones | Ads | RED |
| AW4 | Per-variant wireframes | Ads | YELLOW |
| FR1 | Figma-ready dimensions | Figma | GREEN |
| FR2 | Typography specs in wireframe | Figma | RED |
| FR3 | Color specs in wireframe | Figma | RED |
| FR4 | Wireframe-to-Figma spec bridge | Figma | RED |
| PO1 | Process overview document | Process | RED |
| PO2 | Shareable process doc | Process | RED |

**Score: 3 GREEN, 2 YELLOW, 11 RED**

---

# Re-Run After Fixes

## Fixes Applied

| Test | Before | After | Fix |
|---|---|---|---|
| SD1 | RED | **GREEN** | Campaign Summary Document added as launch gate step 9: strategy, deliverables, quality process, wireframes, checklists, metrics |
| SD2 | RED | **GREEN** | Same Campaign Summary Document serves as shareable process overview |
| EW2 | RED | **GREEN** | Email wireframe template added: preheader, header/logo, hero image zone, body, CTA, footer/unsubscribe — all structural elements present |
| EW3 | YELLOW | **GREEN** | Design Spec block added to wireframe bottom — dimensions, fonts, colors, spacing. Bridges content structure → Figma build. |
| EW4 | RED | **GREEN** | Design Spec block + Design Specs section in brief = zero questions for Dana. Fonts, colors, padding, CTA style all specified. |
| AW2 | RED | **GREEN** | Ad wireframe templates added for 1080x1080 (feed) and 1080x1920 (stories) — show text positioning: headline bottom third, product center, logo top left, CTA bottom, offer badge |
| AW3 | RED | **GREEN** | Image zones clearly marked in templates — "PRODUCT / IMAGE ZONE" center, text overlay zone bottom, logo zone top. Designer knows what's copy vs what's visual. |
| AW4 | YELLOW | **GREEN** | Rule added: "For ad variants: produce one wireframe per variant if copy positioning differs" |
| FR2 | RED | **GREEN** | Design Specs in brief + Design Spec block in wireframe both specify font family, headline size, body size, CTA text style |
| FR3 | RED | **GREEN** | Design Specs in brief + Design Spec block specify bg color, text color, CTA color, accent color — with defaults if no brand specs exist |
| FR4 | RED | **GREEN** | Design Spec block IS the wireframe-to-Figma bridge. Assembles dimensions + colors + fonts + spacing + image zones in one block at the bottom of each wireframe. |
| PO1 | RED | **GREEN** | Campaign Summary Document (launch gate step 9) serves as process overview |
| PO2 | RED | **GREEN** | Campaign Summary Document is designed to be shareable — includes strategy, deliverables, quality process, wireframes |

## Final Score

| # | Test | Axis | Before | After |
|---|---|---|---|---|
| SD1 | Strategy document | Strategy | RED | **GREEN** |
| SD2 | Process overview | Strategy | RED | **GREEN** |
| EW1 | Email wireframes produced | Email | GREEN | GREEN |
| EW2 | Email structural elements | Email | RED | **GREEN** |
| EW3 | Email specs for Figma | Email | YELLOW | **GREEN** |
| EW4 | Email → Figma zero questions | Email | RED | **GREEN** |
| AW1 | Social ad wireframes | Ads | GREEN | GREEN |
| AW2 | Ad text positioning | Ads | RED | **GREEN** |
| AW3 | Ad visual zones | Ads | RED | **GREEN** |
| AW4 | Per-variant wireframes | Ads | YELLOW | **GREEN** |
| FR1 | Figma dimensions | Figma | GREEN | GREEN |
| FR2 | Typography specs | Figma | RED | **GREEN** |
| FR3 | Color specs | Figma | RED | **GREEN** |
| FR4 | Wireframe-to-Figma bridge | Figma | RED | **GREEN** |
| PO1 | Process overview document | Process | RED | **GREEN** |
| PO2 | Shareable process doc | Process | RED | **GREEN** |

**Score: 16 GREEN, 0 YELLOW, 0 RED**

---
