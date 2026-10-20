# DiggerLid Content Kit: Full Context

Everything a fresh Claude session (or a teammate) needs to pick up the Meta copy and blog SEO work without re-researching. Compiled on 8 Oct 2026 by Matt Bedwell (Head of Growth).

## 1. Business

- **What DiggerLid sells.** An Australian e-commerce brand (Shopify, diggerlid.com) selling machinery covers and work gear:
  - Pro Excavator Enclosure, $699
  - PRO Mat, $219, and PRO Mat Plus, $299
  - KAJO screw-top grease (German made), with adapters and guns
  - DiggerShield polycarbonate kits
  - Quicky, Micro, Mini Loader and Skid Steer covers
  - Draw Bar Cover
  - The Hauler (FIFO luggage)
  - Digger Wipes and merch
- **Founders.** Joel and Luke, landscaping tradies, founded the business in 2018. Owner-supplied fact: the Grease VS Clone brief calls them "two brothers".
- **Core customer.** An Australian male owner-operator earthmover, 28 to 50, running 1 to 3 mini excavators. Secondary buyers:
  - maintenance-minded operators
  - farmers
  - truckies
  - FIFO workers
  - 4WD owners
  - gift buyers (partners), the top PRO Mat review theme
- **Channels.** Meta is the main paid channel. The blog at `/blogs/news` had 0 articles as of Oct 2026.

## 2. House rules (apply to everything)

- Never use em dashes in any deliverable.
- Never use the phrase "we're diggin' it". It's banned, even though old brand material uses it.
- **Shipping:** say "Fast shipping Australia wide". Never use free-shipping claims or thresholds. This is the owner rule from 7 Oct 2026. The live site says free over $399, and that conflicts with the rule.
- Product names are exact:
  - DiggerLid
  - PRO Mat and PRO Mat Plus
  - Pro Enclosure
  - KAJO
  - DiggerShield
  - Quicky Cover
  - Draw Bar Cover
  - The Hauler
  - Digger Wipes
- Never fabricate numbers, reviews, customers or specs. **The live site wins over any reference file.** Verify on `diggerlid.com/products/<handle>` before using a claim.
- Reflective strips "help you be seen". They never "keep you safe".
- Use "Australia's first", not "world's first", unless the claim is verified.
- No model identity goes into commits, PRs or published artifacts.
- **Secrets.** Never put API keys in files or chat.
  - META_TOKEN lives only in Vercel env on the diggerlid-mer project.
  - The Alia and PostHog keys used earlier are pending rotation.

## 3. Skills in this kit

| Skill | Job | Status |
|---|---|---|
| `diggerlid-meta-copy` | BAU (non-sale) Meta ad copy from any source: 3 primary texts (Short, Medium, Long), 5 headlines, 3 descriptions | Built and tested. Defaults will be tuned once the top 30 BAU ads data is pulled (section 6). |
| `diggerlid-blog-seo` | Turns a transcript, post or product into an SEO blog article for Shopify, with keyword research, live fact checks, Frame.io images, branded HTML, Shopify fields, an SEO checker, a preview and a TOV score | Built, tested end to end (2,168 words, 0 FAIL, TOV 24/30). Upgrades 1 to 6 in section 8 are proposed. |
| `diggerlid-ad-copy` (existing, not in this kit) | Sale-period copy: BFCM, EOFY, Father's Day | Has stale facts: $249 shipping, "100+ machines" (now 200+), Magnetic Mat $39 (now $79) |

## 4. Verified product facts (7 Oct 2026)

These are summarised here. The full detail is in `skills/*/references/product-catalogue.md` and `usp-bank.md`.

**Pro Enclosure.** $699.

- 490 GSM PVC ripstop
- YKK zips and buckles
- windows on the left, right, rear and lower front
- 6 universal sizes covering 200+ mini excavator models
- 2 Year Warranty
- 4.7 from 246 reviews

The 12V port, "-20°C" and install time claims are **not** on the current product page.

**PRO Mat.**

| | PRO Mat (OG) | PRO Mat Plus |
|---|---|---|
| Price | $219 | $299 |
| Colours | Grey | Grey, Safety Orange, Safety Pink, High Country Camo |
| Extras | | YKK side zips, reflective strips on Orange and Pink only |

Both versions share:

- 490 GSM PVC
- 10mm closed-cell foam
- 2 rare-earth magnets
- 196 × 95 cm open
- 4 kg
- 2 Year Warranty

**KAJO grease.**

- 500g screw-top tubes from $16.70 (LZR2, LC002, HD800, CASX, MoS2, Hammer Paste)
- Made in Germany, KAJO founded 1976
- Uses 100% of the grease
- Changeover in under 20 seconds (gun product page)
- The live product title is "KAJO Grease Packs"
- Adapter $79 (18V Milwaukee, Makita, DeWALT, Ryobi, Metabo, AEG, Macnaught; no 12V)
- Coupler $39 (10,000 PSI)
- Earthmovers Bundle $375

**Other products.**

| Product | Price |
|---|---|
| Magnetic Tool Mat (12 magnets) | $79 |
| Draw Bar Cover | $129 |
| Digger Wipes | $15 |
| DiggerShield | $899 rear, $1,599 full |
| The Hauler | $599 (check the live price) |

**Proof.**

- 61 of 62 Google reviews are 5-star.
- The site shows "Rated 4.71 by 1,290 DigHeads". The PRO Mat page shows "4.69 by 965", which is inconsistent.

## 5. Meta ad learnings (BAU)

- The two pillars are covers and enclosures (11 of the top 25 by impressions) and KAJO (8). PRO Mat is under-indexed at 1 of 25.
- Video is 18 of the top 25. The median top ad runs 205 days. The Milwaukee adapter static ran 605+ days.
- BAU ads carry no discounts. The offer mechanic is shipping, warranty and proof.
- Evergreen ROAS:

  | Ad | ROAS | Pattern |
  |---|---|---|
  | Milwaukee_ASMR | 7.55x | personalisation |
  | BJP | 4.52x | problem-frame |
  | POV | 4.26x | emoji benefit stack |

- **Locked emoji sets**, always in this order:

  | Product | Set |
  |---|---|
  | PRO Mat | 💪 🛠️ 🧎 🪗 ✅ |
  | Enclosure and KAJO | 💪 🛠️ ⚡ 🪣 ✅ |

- Headlines are 40 characters maximum. Descriptions are 30 characters maximum.
- Meta's personal-attributes policy: never write "you have bad knees". Write "your knees know it" instead.

## 6. Pending: top 30 BAU ads pull

- `tools/api-ads.js` is a read-only Vercel function that returns ad-level ROAS plus the creative copy, with sale windows excluded.
- Deploy it as `api/ads.js` in the **diggerlid-mer** Vercel project. That project sits in a different Vercel account from the one Claude reached.

```
cd ~/diggerlid-mer && mkdir -p api && cp api-ads.js api/ads.js && vercel --prod
curl -s https://diggerlid-mer.vercel.app/api/ads > top-ads.json
python3 tools/analyse_top_ads.py top-ads.json   # writes skills/diggerlid-meta-copy/references/bau-top-30.md
```

Default sale windows excluded:

- BFCM 2025: 16 Nov to 1 Dec
- Christmas
- EOFY 2026: 15 to 30 Jun
- Father's Day 2026: 23 Aug to 7 Sep

Edit `DEFAULT_WINDOWS` if other sales ran.

## 7. SEO audit (8 Oct 2026)

The full report is `context/seo-blog-readiness-audit.html`, and it's also an artifact on claude.ai.

**Critical**

1. **Canonicals point at a 404.** All 49 product and collection pages canonicalise to `/a/shop/...`, which returns 404 for Googlebot too.
   - Cause: the `dl-bc-v2` block in `layout/theme.liquid` (DeepLumen app, `ap_deployed` metafield).
   - The same block covers blog articles.
2. **llms.txt is wrong.** `/llms.txt` describes "lids for excavator buckets" and links to 404s.
3. **The blog isn't ready.** It's empty, "You may also like" shows placeholders, and the author is hidden.

**High**

- Homepage has 2 H1s and a generic title.
- Test and junk pages are in the sitemap (`/collections/pro-enclosure-luke-pdp-au-copy`, `/pages/faq-test`, `/pages/size-guideold`, `/pages/https-www-diggerlid-com-au*`).
- 44 pages have no meta description (28 of 30 collections).
- The size guide has no H1 or meta and no crawlable inbound links.
- Product schema lacks aggregateRating, shipping and returns. There is no Organization schema.
- The About page is 147 words.
- 17 cross-page fact conflicts. The top ones:
  - fits 60 vs 200 machines
  - 650 vs 490 GSM
  - 3 vs 4 colours
  - unlimited vs 420 mats
  - inconsistent ratings
  - "FREE shipping" on product pages
  - 6 spellings of the brand name

**Medium**

- 209 of 1,338 images have no alt text.
- Landing pages have H1 problems.
- Shipping messages conflict.
- Pages are heavy (about 600KB HTML, about 100 scripts). Core Web Vitals were not measured because the API quota ran out.

**Owned content to move into the blog** (with 301 redirects):

- `/pages/6-reasons-why-its-time-to-ditch-cardboard` (the title says 5)
- `/pages/gift` (2,468 words)
- `/pages/pro-mat-plus-2026` (keep it, and add a comparison article)

**Decisions still open (Matt):**

1. Is DeepLumen meant to be live?
2. Rename the blog from "News"?
3. Approve the page migration?
4. Search Console access or a query export?
5. Build skill upgrades 1 to 6?

## 8. Proposed blog skill upgrades

1. **Vendor 4 claude-seo stdlib scripts** (MIT, keep the license notice) as a post-draft gate:
   - `content_quality.py`, threshold 60, ignore `low-density` on how-to copy
   - `content_verify.py`, review only, not a gate
   - `metadata_template.py`
   - `content_humanize.py`, text only, never HTML
2. **Pre-write mini audit.** Run `tools/site_inventory.py`, and re-crawl if the inventory is over 7 days old. Check four things:
   - cannibalisation
   - link targets
   - health of the linked product pages
   - template defects
3. **TOV self-score** against `references/tov-guide.md`. The pass mark is 24/30 with no dimension below 3. This is done, but not yet enforced as a hard step.
4. **Two-way interlinking.** 5 to 10 outbound links, plus an inbound list of 3 to 5 existing pages, each with the exact sentence and anchor to add. Fewer than 3 inbound links means not launched.
5. **`content-map.md` registry.** One primary keyword per article, plus cluster, pillar and links.
6. **Keyword scoring, out of 100:**

   | Factor | Points |
   |---|---|
   | source fit (under 15 disqualifies) | 25 |
   | intent fit (blog share of top 10, under 40% is a mismatch) | 20 |
   | business value | 20 |
   | demand | 15 |
   | winnability | 15 |
   | cluster gap | 5 |
7. **Connect Google Search Console.** Quick wins are queries at position 4 to 10 with over 50 impressions.

## 9. Keyword data

`context/data/keyword-planner-grease.md` holds Google Keyword Planner data for AU, March and May 2026, grease and KAJO only:

- 146 keywords
- 26 at 500/mo, e.g. kajo grease, grease gun adapter, battery grease gun, wheel bearing grease
- 10 comp-zero educational topics, e.g. lithium vs calcium grease, how often to grease an excavator, when to use moly grease
- a drop list

There is no validated volume data yet for covers, enclosures or PRO Mat.

## 10. Sources

- Shopify Admin API: products, blog, theme files
- Live crawl of diggerlid.com: 88 pages, with the corpus in `context/site-crawl/`
- Meta Ad Library teardown (Drive, Apr 2026)
- DiggerLid SEO Audit (Apr 2026)
- Google review export
- Grease Plan v4 (Keyword Planner)
- Video briefs (Grease VS Clone, Tradie Wife, PRO Mat Plus)
- claude-seo toolkit (MIT, github.com/AgriciDaniel/claude-seo; FLOW prompts are CC BY 4.0)
