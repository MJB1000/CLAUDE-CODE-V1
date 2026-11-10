---
name: diggerlid-meta-copy
description: Write business-as-usual (non-sale) Meta ad copy for DiggerLid from any source, such as a video transcript, a script, a creative description, a product name, a customer review or a product page URL. Produces primary text, headlines and descriptions in DiggerLid's tested tradie voice, built from the top-performing evergreen ads, a verified product catalogue and USP bank, with a live website check before any price, spec or offer claim. Use whenever the user asks for Meta, Facebook or Instagram ad copy, primary text, headlines, hooks or captions for DiggerLid, PRO Mat, Pro Enclosure, KAJO, DiggerShield, Quicky, Draw Bar Cover, Hauler, Digger Wipes or any DiggerLid product. For sale-period copy (BFCM, EOFY, Father's Day) use the sale playbook in the diggerlid-ad-copy skill instead.
---

# DiggerLid Meta Copy (BAU)

Turn any input into Meta ad copy that sounds like DiggerLid's best evergreen ads: an Aussie operator talking to one bloke on site. The voice is short, punchy and a bit cheeky, built on real numbers. The copy is creative, but every claim is true.

## The workflow

Follow these steps in order. Steps 1 to 3 happen silently. Only step 5 is shown to the user.

### 1. Read the input and name the job

Work out four things from whatever arrives:

- **Source type.** A transcript, a script, a creative description, a product name, a review, a URL or a loose idea. `references/input-recipes.md` gives the extraction steps for each.
- **Product.** If the product is unclear, infer it from the visuals or words. If it is still unclear, ask one question.
- **Audience.** Pick one: owner-operator earthmover (default), maintenance-minded operator, site mechanic, farmer, truckie or tower, FIFO worker, 4WD and camping, or gift buyer. Profiles are in `references/voice-and-rules.md`.
- **Angle.** Choose one archetype from `references/bau-copy-patterns.md`. If the input is a transcript, the archetype is usually already in the script. Find it, don't invent a new one.

Fix transcription errors silently:

| Heard | Write |
|---|---|
| work map | work mat |
| Pro Map, primer, primate | PRO Mat |
| Cudjoe, Khodro, cargo, Cajo | KAJO |
| Digger Lidcombe, Dig a Little, digger lead | DiggerLid |
| grey scone | grease gun |

### 2. Load the facts

- Always read `references/bau-copy-patterns.md` and `references/voice-and-rules.md` in full. They hold the emoji system, archetypes and compliance rules every ad needs.
- Grep `references/product-catalogue.md` and `references/usp-bank.md` for the product in play. Don't read the whole catalogue.

### 3. Verify on the website (mandatory for claims)

Check the live product page with WebFetch **before** you use any of the following:

- a price
- dispatch or delivery claims
- a review count or star rating
- a customer count
- warranty wording
- a spec number (GSM, sizes, models covered, magnets, dimensions)
- a compatibility claim
- anything marked ⚠️ in the catalogue

The URL pattern is `https://diggerlid.com/products/<handle>`. Handles are in the catalogue.

The site beats this skill. If they disagree:

1. Use the site.
2. Add one line to the uncertainty flag at the end of the output.
3. Tell the user so the catalogue can be updated.

If the site can't be reached, keep the claim out of the copy or mark it `[CHECK]`.

Copy that uses no hard claims (pure hook plus feel) can skip the fetch. It still needs the catalogue read.

### 4. Draft, then self-check

Write to the BAU body shapes in `references/bau-copy-patterns.md`. Then run the checklist below before showing anything.

### 5. Output (locked format)

- **No preamble.** Copy first.
- Every piece sits in its own fenced code block, with nothing else inside the block.
- Order: primary texts, then headlines, then descriptions.
- Put a one-word label line above each primary text block: **Short**, **Medium** or **Long**.
- Default counts when the user doesn't specify:
  - 3 primary texts: one Short, one Medium, one Long, each on a different angle or hook.
  - 5 headlines.
  - 3 descriptions.
- If the user names counts, follow them exactly.
- After the copy, add at most three lines:
  - which archetype and audience you used
  - what you verified on the site
  - anything uncertain

## Length tiers (BAU)

| Tier | Characters | Shape | Use for |
|---|---|---|---|
| Short | 90 to 220 | Hook line, one proof line, CTA. Emoji: 1 to 2, not counting the CTA ⬇. Skip 🤩 on Short. | Statics, retargeting, 15s cutdowns, warm audiences |
| Medium | 300 to 600 | Hook, product intro, 5-line emoji checklist, close, CTA. 6 to 9 emoji in total. | The default evergreen shape |
| Long | 600 to 1,100 | Story or maths or old-vs-new narrative, then checklist, close, CTA. | Cold audiences, founder or customer story, cost maths, UGC talking heads |

Meta truncates primary text at about 125 characters in feed. **The first 125 characters must work alone:** hook plus reason to tap "more".

These tiers come from the locked structure and the evergreen ads that have run. Once `references/bau-top-30.md` exists (built by `scripts/analyse_top_ads.py` from the live Meta pull), its measured medians override this table.

## Body shape (Medium, the default)

1. **Hook.** One emoji matched to the concept, then a pain line or a bold claim. Add 🤩 at the end of the line on evergreen product ads.
2. **Product intro.** "Meet the PRO Mat Plus." or "The DiggerLid Pro Enclosure."
3. **Feature checklist.** Use the locked emoji set for the product, in the locked order. Wording can flex. The emoji and their order cannot. The ✅ line is the trust or hero line: 2 Year Warranty by default. For the PRO Mat Plus, ✅ carries the YKK zip join and the warranty moves to the close.
4. **Benefit close.** One short line. Never repeat the hook unless it's a deliberate bookend.
5. **CTA and URL.** `Shop Now ⬇`, then the product URL on its own line. Use the base product URL (`diggerlid.com/products/<handle>`), not variant URLs, unless asked.

### Locked feature emoji sets

| Product | Set |
|---|---|
| PRO Mat, PRO Mat Plus | 💪 🛠️ 🧎 🪗 ✅ |
| Pro Enclosure, KAJO | 💪 🛠️ ⚡ 🪣 ✅ |

Other products use the general checklist set in `references/bau-copy-patterns.md`.

## Shipping language (owner rule, 7 Oct 2026)

- Say **"Fast shipping Australia wide"** (or "Fast shipping Australia-wide 🚚" in a checklist line). This is the default shipping line in every BAU ad.
- **Do not** lead with free shipping, and do not quote a free-shipping threshold, in copy, unless the user asks for it for a specific ad.
- Supporting facts you can use: "Same day dispatch before 12PM AEST" (verify on site).

## Headlines and descriptions

- Headlines are **40 characters maximum**. Count them.
  - Give five, each from a different lens: pain, proof, promise, product, brand.
  - Two-punch rhythm works best, e.g. "Stay dry. Stay padded."
  - Pull the strongest line from the script when there is one. It has already been tested on camera.
- Descriptions are **30 characters maximum**. Count them.
  - Defaults are `2 Year Warranty`, `Fast Shipping Australia Wide` and `Australian Owned`.
  - On objection ads, answer the objection, e.g. `6 Sizes. 200+ Machines.`
- Headline libraries for each product are in `references/bau-copy-patterns.md`.

## Self-check (run every time)

- [ ] No em dashes anywhere. Use full stops or commas.
- [ ] Product names are exact: DiggerLid, PRO Mat, PRO Mat Plus, Pro Enclosure, KAJO, DiggerShield, Quicky Cover, Draw Bar Cover, The Hauler, Digger Wipes.
- [ ] Every number, price and spec matches the catalogue **and** the live site.
- [ ] The first 125 characters hook on their own.
- [ ] The headline is 40 characters or fewer, and the description is 30 or fewer, counted.
- [ ] No banned words: elevate, unlock, revolutionary, game-changing, seamless, solution, ultimate, cutting-edge.
- [ ] Shipping is "Fast shipping Australia wide". No free-shipping claims or thresholds unless asked.
- [ ] There is no sale language (%, "sale", "deal", countdowns) in BAU copy unless the user asked for it.
- [ ] Meta policy holds:
  - No "f**k" in any form.
  - No direct claims about the reader's personal attributes, such as age or health conditions. "Your knees know it" is fine. "You have bad knees" is not.
  - Keep hard swearing out of headlines.
- [ ] Superlatives are defensible. Prefer "Australia's first" over "world's first" unless the latter is verified.
- [ ] The phrase "we're diggin' it" does not appear.
- [ ] The three primary texts use three different hooks. Never send three variations of one opener.

## Reference files

| File | Read when |
|---|---|
| `references/product-catalogue.md` | Always, for the product in play (grep the section) |
| `references/usp-bank.md` | You need proof points, brand claims or reviews |
| `references/bau-copy-patterns.md` | Choosing an archetype, emoji, headlines or body shape |
| `references/voice-and-rules.md` | Voice, villains, audiences, compliance |
| `references/input-recipes.md` | Turning a specific source type into copy |
| `references/creative-angles.md` | You need fresh hooks or the user asks for more creative options |
| `references/bau-top-30.md` | Exists after the Meta pull. Measured length, emoji and style stats from the top 30 BAU ads |

## Refreshing the data

`scripts/analyse_top_ads.py` turns the `/api/ads` JSON from the diggerlid-mer Vercel project into `references/bau-top-30.md`. Re-run it each quarter, or after a big creative refresh, so the skill keeps learning from what is actually winning.
