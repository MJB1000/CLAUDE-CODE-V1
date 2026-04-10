# Review Feedback — Mornings Subscription Launch

## Round 2 — 2026-04-10

**Reviewer:** Dana
**Ready for Copywriter:** N/A — ALL CLEAR

---

### Must Fix

None.

### Should Fix

None.

### Escalate to Sofia

None.

---

### Wireframes

**Round 2 wireframe updates — only sections that changed:**

**Feed Ad CTA (1b) — previously unlocked, now fixed:**

1. `use_figma` -> **Update Feed CTA badge:** Select node `feedCtaTextId` from Round 1. Update text content from "Shop Now" to "Get Your Free Bag".
   - Load font: `await figma.loadFontAsync({family: 'Inter', style: 'Semi Bold'})`
   - Set characters: "Get Your Free Bag"
   - Auto-layout parent will resize automatically.
   - Returns: `feedCtaTextId` (updated)
2. `get_screenshot` -> capture updated feed ad frame -> "Feed-Ad-1b-R2.png"

**Stories Supporting Text (1c) — locked section updated per copy fix:**

3. `use_figma` -> **Update Stories supporting text:** Select node `storiesSupportId` from Round 1. Update text from "First bag free. No strings." to "First bag free. Cancel whenever."
   - Load font: `await figma.loadFontAsync({family: 'Inter', style: 'Regular'})`
   - Set characters: "First bag free. Cancel whenever."
   - Returns: `storiesSupportId` (updated)
4. `get_screenshot` -> capture updated stories ad frame -> "Stories-Ad-1c-R2.png"

**Final campaign overview:**

5. `get_screenshot` -> capture all three frames at zoom-out -> "Full-Campaign-Overview-R2-FINAL.png"

**Wireframe status — all deliverables:**

| Deliverable | Sections Built | Status |
|---|---|---|
| Email (1a) | 7/7 — Header, Hero, Headline, Subhead, Body, CTA, Footer | COMPLETE |
| Feed Ad (1b) | 6/6 — Frame, Logo, Product, Headline, Support, CTA | COMPLETE (CTA updated R2) |
| Stories Ad (1c) | 5/5 — Frame, Logo, Visual, Text, CTA | COMPLETE (Support text updated R2) |

**Figma file:** "Mornings-Subscription-Launch" — [figma.com/file/abc123]
**Total `use_figma` calls across R1 + R2:** 23 (R1) + 2 (R2) = 25 calls
**Total `get_screenshot` calls:** 4 (R1) + 3 (R2) = 7 screenshots

**Design decisions (Round 2):**
- No layout changes needed — only text content swaps
- CTA badge on feed ad auto-resized cleanly with longer text ("Get Your Free Bag" vs "Shop Now") thanks to auto-layout padding
- Stories supporting text swap was same character count range — no layout impact

---

### Locked Sections (cumulative)

**Email (1a) — all locked Round 1:**
- Header (logo + layout) — locked R1
- Hero image placeholder — locked R1
- Headline "Your Morning, Sorted." — locked R1
- Subhead — locked R1 (Charlie kept original, reasoning accepted)
- Body copy — locked R1
- CTA "Get Your Free Bag" — locked R1
- Sign-off + footer — locked R1

**Feed Ad (1b) — all locked:**
- Logo placement — locked R1
- Product zone — locked R1
- Headline "Your Morning, Sorted." — locked R1
- Supporting text "First bag free. Cancel whenever." — locked R1
- CTA "Get Your Free Bag" — **locked R2** (Must Fix resolved)

**Stories Ad (1c) — all locked:**
- Logo placement — locked R1
- Visual zone — locked R1
- Headline "Your Morning, Sorted." — locked R1
- Supporting text "First bag free. Cancel whenever." — **updated R2** (Should Fix applied)
- CTA zone — locked R1

---

### Cleared

**All three deliverables are cleared for launch gate.**

Charlie resolved the Must Fix (feed CTA) and voluntarily applied the Should Fix on stories supporting text. The email subhead was kept as-is with solid reasoning — the conversational cadence serves the brand voice. No objection.

**Copy quality:** Consistent voice across all three deliverables. "Your Morning, Sorted." works as a unifying headline across channels. The cancel-anxiety messaging is now consistent ("Cancel whenever." in email body, feed supporting text, and stories supporting text). CTA is aligned ("Get Your Free Bag") across email and feed — stories uses platform swipe-up but the on-screen CTA text matches.

**Wireframe quality:** All 18 sections across 3 deliverables are built in Figma. Layouts follow the brief's Design Requirements. Product image placeholders are warm-toned (#E8DDD3) to maintain brand warmth even without final photography. Typography hierarchy is clear: headline > subhead/supporting > body > footer across all formats.

**Recommendation:** Send to Sofia for launch gate. All deliverables clear. Figma wireframes complete.
