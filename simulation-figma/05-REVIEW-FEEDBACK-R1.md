# Review Feedback — Mornings Subscription Launch

## Round 1 — 2026-04-10

**Reviewer:** Dana
**Ready for Copywriter:** YES (1 Must Fix, 2 Should Fix)

---

### Must Fix

**1. [03-COPY-ADS.md: Deliverable 1b — Feed Ad CTA]** — CTA text "Shop Now" is generic and misaligned with the campaign message. Every DTC brand on Instagram uses "Shop Now." The email uses "Get Your Free Bag" which is specific, benefit-driven, and differentiated. The feed ad CTA should match.
- **Fix:** Change CTA from "Shop Now" to "Get Your Free Bag" (or confirm with CD if Instagram allows custom CTA text in this ad format — if not, "Shop Now" is acceptable as a platform constraint, but flag it in the campaign summary).

---

### Should Fix

**1. [02-COPY-EMAIL.md: Subhead]** — "That's the whole pitch." is the witty beat and it works. But "Good coffee showing up before you've had to think about it" is 12 words for a subhead in a minimal email. Consider tightening to under 10. Suggestion: "Good coffee, before you've had to think about it. That's the pitch." (11 words, slightly tighter). Not blocking — current version works.

**2. [03-COPY-ADS.md: Deliverable 1c — Stories supporting text]** — "First bag free. No strings." is strong for glance format. However, "No strings" is slightly more ambiguous than "Cancel whenever" — it could imply no strings attached to the free bag specifically rather than the subscription model. Not blocking because context makes it clear, but worth considering "Cancel whenever." for consistency across all three deliverables.

---

### Escalate to Sofia

None. Brief was well-specified. Charlie's creative choices are within brand voice boundaries.

---

### Wireframes

Dana loads `skills/figma-production.md` before any Figma work. Figma MCP is connected.

**Email (600px):**

1. `create_new_file` -> "Mornings-Subscription-Launch" -> returns file URL (e.g., figma.com/file/abc123)
2. `search_design_system` -> search for "button", "email", "header" components -> none found (new client, no library)
3. `use_figma` -> **Email wrapper frame:** Create frame 600px wide, auto-layout vertical, padding 0, background fill #FFFAF5 (rgb: {r: 1.0, g: 0.98, b: 0.96}). Name: "Email-Launch-1a". Position at x:100, y:100 (offset from origin).
   - Returns: `emailFrameId`
4. `use_figma` -> **Header section:** Inside emailFrameId, create auto-layout horizontal frame, 600px wide, 80px tall, padding 40px left, 20px top/bottom. Add rectangle 120x30 as logo placeholder, fill #1A1A1A. Name: "Header". Set layoutSizingHorizontal = 'FILL' after appendChild.
   - Returns: `headerFrameId`, `logoPlaceholderId`
5. `use_figma` -> **Hero image section:** Inside emailFrameId, create frame 600px wide, 300px tall, fill #E8DDD3 (warm neutral placeholder, rgb: {r: 0.91, g: 0.87, b: 0.83}). Name: "Hero-Image-Placeholder". Center text "Product Image" in 14px Inter Regular, #999999.
   - Load fonts: `await figma.loadFontAsync({family: 'Inter', style: 'Regular'})`
   - Returns: `heroFrameId`
6. `use_figma` -> **Headline + Subhead section:** Inside emailFrameId, create auto-layout vertical frame, padding 40px horizontal, 40px top, 16px bottom. Gap 12px.
   - Load fonts: `await figma.loadFontAsync({family: 'Inter', style: 'Bold'})`, `await figma.loadFontAsync({family: 'Inter', style: 'Regular'})`
   - Text node: "Your Morning, Sorted." — 32px Inter Bold, fill #1A1A1A (rgb: {r: 0.1, g: 0.1, b: 0.1})
   - Text node: "Good coffee showing up before you've had to think about it. That's the whole pitch." — 18px Inter Regular, fill #4A4A4A (rgb: {r: 0.29, g: 0.29, b: 0.29})
   - Set layoutSizingHorizontal = 'FILL' on both text nodes after append.
   - Returns: `headlineFrameId`, `headlineTextId`, `subheadTextId`
7. `use_figma` -> **Body section:** Inside emailFrameId, create auto-layout vertical frame, padding 40px horizontal, 24px vertical. Gap 20px.
   - Load font: Inter Regular, 16px
   - Text node 1: "We made ordering coffee the thing you never have to do again." — 16px Inter Regular, #1A1A1A
   - Text node 2: "Pick your roast. Tell us how often. We ship it fresh." — 16px Inter Regular, #1A1A1A
   - Text node 3: "Change it whenever you want. Skip a delivery. Cancel anytime. No penalties, no guilt trips, no \"are you sure?\" pop-ups." — 16px Inter Regular, #1A1A1A
   - Text node 4: "Your first bag is on us." — 20px Inter Bold, #1A1A1A (larger, emphasis)
   - Set layoutSizingHorizontal = 'FILL' on all text nodes after append.
   - Returns: `bodyFrameId`, `bodyText1Id`, `bodyText2Id`, `bodyText3Id`, `offerTextId`
8. `use_figma` -> **CTA button:** Inside emailFrameId, create auto-layout horizontal frame centered. Inner frame: auto-layout horizontal, padding 16px vertical, 48px horizontal, cornerRadius 4, fill #3D2B1F (rgb: {r: 0.24, g: 0.17, b: 0.12}).
   - Load font: Inter Semi Bold
   - Text node: "Get Your Free Bag" — 16px Inter Semi Bold, fill #FFFAF5 (rgb: {r: 1.0, g: 0.98, b: 0.96})
   - Wrapper frame: center-aligned, padding 40px vertical.
   - Returns: `ctaWrapperId`, `ctaButtonId`, `ctaTextId`
9. `use_figma` -> **Sign-off + Footer:** Inside emailFrameId, create auto-layout vertical frame, padding 40px horizontal, 32px top, 40px bottom. Gap 24px.
   - Text node: "Mornings. Coffee that shows up." — 14px Inter Regular, #4A4A4A
   - Divider: rectangle 520px x 1px, fill #E0D5C9 (rgb: {r: 0.88, g: 0.84, b: 0.79})
   - Text node: "Unsubscribe | Manage preferences | Mornings Pty Ltd, Melbourne AU" — 12px Inter Regular, #999999
   - Returns: `footerFrameId`, `signoffTextId`, `dividerId`, `footerTextId`
10. `get_screenshot` -> capture full email frame -> "Email-Launch-1a-R1.png"

**Instagram Feed Ad (1080x1080):**

11. `use_figma` -> **Ad frame:** Create frame 1080x1080, fill #FFFAF5. Name: "Feed-Ad-1b". Position at x:800, y:100 (offset from email frame).
    - Returns: `feedFrameId`
12. `use_figma` -> **Logo:** Inside feedFrameId, create rectangle 100x28 as logo placeholder at top-left, padding 48px from edges. Fill #1A1A1A.
    - Returns: `feedLogoId`
13. `use_figma` -> **Product zone:** Inside feedFrameId, create frame 600x600 centered (x:240, y:140). Fill #E8DDD3 (image placeholder). Add text "Product Image" centered, 16px Inter Regular, #999999.
    - Returns: `productZoneId`
14. `use_figma` -> **Text overlay — bottom third:** Inside feedFrameId, create auto-layout vertical frame at bottom, 1080px wide, padding 48px horizontal, 60px bottom. Gap 8px. Background: linear gradient from transparent to rgba(0,0,0,0.03) for subtle grounding.
    - Load fonts: Inter Bold 64px, Inter Regular 24px
    - Text node: "Your Morning, Sorted." — 64px Inter Bold, #1A1A1A
    - Text node: "First bag free. Cancel whenever." — 24px Inter Regular, #4A4A4A
    - Returns: `textOverlayId`, `feedHeadlineId`, `feedSupportId`
15. `use_figma` -> **CTA badge:** Inside feedFrameId, bottom-right area above text. Auto-layout frame, padding 12px vertical, 24px horizontal, cornerRadius 4, fill #3D2B1F.
    - Text: "Get Your Free Bag" — 14px Inter Semi Bold, #FFFAF5
    - Position: right-aligned, y: 880 (above text overlay).
    - Returns: `feedCtaId`, `feedCtaTextId`
16. `get_screenshot` -> capture full feed ad frame -> "Feed-Ad-1b-R1.png"

**Instagram Stories Ad (1080x1920):**

17. `use_figma` -> **Stories frame:** Create frame 1080x1920, fill #FFFAF5. Name: "Stories-Ad-1c". Position at x:2000, y:100.
    - Returns: `storiesFrameId`
18. `use_figma` -> **Logo:** Inside storiesFrameId, centered at top, y:120 (below Stories UI safe zone). Rectangle 100x28, fill #1A1A1A, centered horizontally.
    - Returns: `storiesLogoId`
19. `use_figma` -> **Visual zone (top half):** Inside storiesFrameId, create frame 900x800, centered, y:200. Fill #E8DDD3 (product image placeholder). Text "Product Image" centered, 16px Inter Regular, #999999. Rounded corners 8px.
    - Returns: `storiesProductId`
20. `use_figma` -> **Text zone (bottom half):** Inside storiesFrameId, auto-layout vertical frame at y:1100, 1080px wide, padding 60px horizontal. Gap 12px.
    - Load fonts: Inter Bold 72px, Inter Regular 28px
    - Text node: "Your Morning, Sorted." — 72px Inter Bold, #1A1A1A
    - Text node: "First bag free. No strings." — 28px Inter Regular, #4A4A4A
    - Returns: `storiesTextId`, `storiesHeadlineId`, `storiesSupportId`
21. `use_figma` -> **CTA zone:** Inside storiesFrameId, centered at y:1600 (above swipe-up zone). Auto-layout frame, padding 16px vertical, 40px horizontal, cornerRadius 4, fill #3D2B1F.
    - Text: "Get Your Free Bag" — 18px Inter Semi Bold, #FFFAF5
    - Returns: `storiesCtaId`, `storiesCtaTextId`
22. `get_screenshot` -> capture full stories ad frame -> "Stories-Ad-1c-R1.png"
23. `get_screenshot` -> capture all three frames at zoom-out -> "Full-Campaign-Overview-R1.png"

**Design decisions:**
- Background #FFFAF5 across all three deliverables for campaign consistency
- Product image placeholder in warm neutral (#E8DDD3) rather than grey — maintains the coffee warmth even without final photography
- CTA buttons use sharp 4px radius per brief specs — premium feel, not playful
- Email body text uses generous 20px gap between paragraphs per Charlie's hierarchy note about intentional short paragraphs
- Feed ad text in bottom third — product shot dominates center, text grounds the composition
- Stories ad text in lower 40% — product fills upper space, headline hits at eye-level for vertical scroll
- All fonts loaded with `loadFontAsync` before each text creation call
- All node IDs returned and tracked per Figma MCP rules

**Assets used:** All built from scratch (no design system library for this client).

**Known gaps:**
- All product images are placeholders — real photography needed before production
- Logo is a rectangle placeholder — actual Mornings wordmark file needed
- No design tokens/variables created yet — hardcoded values used for this wireframe pass

---

### Locked Sections

**Email (1a):**
- Header (logo + layout) — passed, wireframe built
- Hero image placeholder — passed, wireframe built
- Headline "Your Morning, Sorted." — passed, wireframe built
- Subhead — passed (Should Fix noted, not blocking), wireframe built
- Body copy (all three paragraphs + offer line) — passed, wireframe built
- CTA "Get Your Free Bag" — passed, wireframe built
- Sign-off + footer — passed, wireframe built

**Feed Ad (1b):**
- Logo placement — passed, wireframe built
- Product zone — passed, wireframe built
- Headline "Your Morning, Sorted." — passed, wireframe built
- Supporting text "First bag free. Cancel whenever." — passed, wireframe built
- CTA — **NOT locked** (Must Fix: change from "Shop Now")

**Stories Ad (1c):**
- Logo placement — passed, wireframe built
- Visual zone — passed, wireframe built
- Headline "Your Morning, Sorted." — passed, wireframe built
- Supporting text "First bag free. No strings." — passed (Should Fix noted, not blocking), wireframe built
- CTA zone — passed, wireframe built

---

### Cleared

**Overall assessment:** Strong work from Charlie. Brand voice is nailed — confident, minimal, witty in exactly the right places. The "are you sure? pop-ups" line is genuinely clever and audience-specific. Content hierarchies are clear and buildable. One Must Fix on the feed ad CTA (generic "Shop Now" needs to match the campaign-specific "Get Your Free Bag"). Two non-blocking Should Fixes for tightening.

The copy would NOT work for a generic coffee subscription competitor — "That's the whole pitch," the cancel-anxiety specifics, and the overall restraint are distinctly Mornings. Differentiation: PASS.

**Wireframes built for 22/23 sections across all three deliverables.** Feed ad CTA wireframe uses placeholder pending the Must Fix. All other sections are locked and built in Figma.
