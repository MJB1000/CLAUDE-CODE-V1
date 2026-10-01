# DiggerLid — Research Projects

Standing register of research projects (analyses, not controlled experiments). Each project keeps
its own section and **stays until you update it**. Durable across sessions — this is the source of truth.

## How to use it
- **Start one:** *"new research project: …"* → I add the next `RP-###`.
- **Update:** *"update RP-001: …"* → I append findings / refresh the data.
- **Experiments** (controlled tests) live in `experiments/EXPERIMENT-LOG.md`; **research** (data pulls / analysis) lives here.

**Status:** `Open` · `Parked` · `Complete`

---

## Register
| ID | Project | Status | Last updated | Headline |
|---|---|---|---|---|
| RP-001 | Signup volume, cost & signup→conversion economics | Open | 2026-08-16 | Popup CAPTURE stable ~5–6% (Alia, empirical) → slowdown is a REACH problem, not conversion. Cause (device/page) + view-rate trend PENDING segmented pull. Conversion ~29% stable. |
| RP-002 | 2K Giveaway 2026 — acquisition P&L | Open (re-run post-BFCM) | 2026-08-25 | **Ad-driven cut: −$1,770 net to date** (11 new buyers, $1,595 contribution vs $3,365 cost). Whole-list "+$6.4k" = owned-audience activation, not acquisition. ~380 new emails not yet bought = the tail. |
| RP-003 | Repeat rate (EE definition) & Style-of-Sale classification | Complete | 2026-09-22 | **LOW REPEAT, on the Hybrid boundary**: 17.7% of all customers ever bought twice; TTM Shopify returning-customer rate 21.4%. **Ex-grease: 13.9% / 16.4% = Low, unambiguous. PRO Mat only: 2-8% = Low, deep; 93.5% of its buyers are new-to-brand.** Grease is the only consumable (≈27% product repeat); every durable ≤11%. Reorderers switch variant (size up / second battery platform). |
| RP-004 | Sale curve shape: Hybrid or Low? (EOFY 26 vs BFCM 25) | Complete | 2026-09-22 | **Hybrid-SHAPED curve on a Low-repeat base.** Mid-sale plateau ~5%/day (Low curve = 8-9%); hype spike ≈30% of revenue - front-loaded at BFCM (31% first 48h), back-loaded at EOFY (32% last 48h, tax deadline). But returning-customer share during sales (22-29%) = BAU (24.5%): the spikes are NEW customers, so the shape comes from urgency on acquisition, not repeat. |
| RP-005 | Sale landing pages: BFCM 25 vs EOFY 26 (+ FD 26) | Complete | 2026-09-22 | **EOFY page converted 62% better (3.38% vs 2.09%) on 37% fewer sessions and delivered more orders (382 vs 373).** Driver = traffic mix + a day-2 cold-social flood at BFCM (4,628 sessions @ 0.99%). Homepage landers out-convert both LPs 3-4x (warm traffic). Pre-launch hype traffic to the LP converts ~0.6% - capture it. |
| RP-006 | Popup signup → purchase conversion, long run (Oct 25–Sep 26) | Complete | 2026-09-22 | **Conversion is constant (submit ~5% of viewers, signup→buyer 29.4%, ~85% in month one); REACH is the broken link: popup seen by 67–80% of sessions Jan–Apr → 23% in Sep as paid scaled. ~3× signups available at today's traffic. Signup ≈ $120 net / $65 contribution. Pre-sale signups don't bank for the sale (4–7%); in-sale submit collapses (2.3%). Fix reach first.** |

---

## RP-001 — Signup volume, cost & signup→conversion economics
**Status:** Open · **Owner:** Matt · **Last updated:** 2026-08-16
**Question:** What does an email signup cost, how many convert, and what drives the variation?

### Data sources
- **Klaviyo** signups (`$source = "Alia sign-up"`) via `/api/emails` (Vercel; key in env).
- **Shopify** sessions (ShopifyQL) and `tag:Alia` customers' lifetime `numberOfOrders` (conversion).
- **Meta** spend via `/api/campaigns` (live Graph API).
- Popup launched ~**Oct 2025** (signups jump 53 → 1,248); Aug/Sep 2025 are pre-popup.

### Monthly view (13 months, popup life)
| Month | Sessions | Signups | Meta spend | Cost/signup | Visitor→signup |
|---|--:|--:|--:|--:|--:|
| Oct 25 | 43,955 | 1,248 | $108,109 | $87 | 2.84% |
| Nov 25 | 78,359 | 2,073 | $166,140 | $80 | 2.65% |
| Dec 25 | 50,255 | 1,269 | $94,286 | $74 | 2.53% |
| Jan 26 | 29,663 | 923 | $48,184 | **$52** | 3.11% |
| Feb 26 | 39,299 | 1,165 | $84,730 | $73 | 2.96% |
| Mar 26 | 36,747 | 1,158 | $100,202 | $87 | 3.15% |
| Apr 26 | 31,845 | 1,213 | $108,317 | $89 | **3.81%** |
| May 26 | 76,386 | 1,481 | $122,931 | $83 | 1.94% |
| Jun 26 | 125,171 | 1,406 | $197,656 | $141 | 1.12% |
| Jul 26 | 116,420 | 1,354 | $162,325 | $120 | 1.16% |
| Aug 26* | 31,404 | 303 | $34,440 | $114 | 0.96% |
*partial. Pre-popup: Aug25 72 / Sep25 53 (cost/signup ~$1,000 = artifact, ignore).
**Popup-era blended: ~2.12% visitor→signup, ~$90/signup.**

### Weekly view (14 weeks, May–Aug 2026) — with conversion
| Week | Sessions | Signups (Klaviyo) | Cost/signup | Visitor→signup | Alia custs (Shopify) | Buyers | **Conv.** |
|---|--:|--:|--:|--:|--:|--:|--:|
| May 04 | 16,117 | 310 | $92 | 1.92% | 344 | 119 | 34.6% |
| May 11 | 22,182 | 335 | $84 | 1.51% | 359 | 102 | 28.4% |
| May 18 | 15,667 | 310 | $88 | 1.98% | 347 | 104 | 30.0% |
| May 25 | 18,792 | 394 | **$69** | 2.10% | 432 | 127 | 29.4% |
| Jun 01 | 20,346 | 444 | $73 | **2.18%** | 490 | 127 | 25.9% |
| Jun 08 | 22,946 | 447 | $74 | 1.95% | 474 | 144 | 30.4% |
| Jun 15 | 37,715 | 189 | **$271** | 0.50% | 200 | 66 | 33.0% |
| Jun 22 | 29,411 | 187 | **$278** | 0.64% | 196 | 68 | 34.7% |
| Jun 29 | 41,287 | 431 | $147 | 1.04% | 451 | 120 | 26.6% |
| Jul 06 | 24,002 | 258 | $122 | 1.07% | 284 | 69 | 24.3% |
| Jul 13 | 24,570 | 362 | $97 | 1.47% | 379 | 114 | 30.1% |
| Jul 20 | 24,108 | 272 | $136 | 1.13% | 295 | 86 | 29.2% |
| Jul 27 | 24,897 | 223 | $147 | 0.90% | 252 | 66 | 26.2% |
| Aug 03* | 23,668 | 144 | $111 | 0.61% | 152 | 20 | 13.2%* |
*partial & immature. **Blended: 345,708 sessions · 4,306 Klaviyo signups (1.25% submit) · $115/signup.**
**Pooled conversion (mature W1–13): 1,312 buyers / 4,503 Alia customers = ~29.1%.**

### Key findings
1. **Conversion is remarkably flat (~26–35%, pooled ~29%) regardless of what a signup cost.** ~1 in 3 email signups eventually buys. Signup *quality* barely moves week to week.
2. **Cost/signup is the volatile lever ($52–$278).** Cheapest in lean BAU/prospecting months (Jan $52; May-wk ~$69–90); worst during the **EOFY sale (Jun 15–28, $271–278)** when spend rose ~55% while signups *halved*.
3. **Counter-intuitive:** the expensive EOFY signups converted *highest* (33–35%) — fewer, pricier, higher-intent. So paying more per signup did **not** buy worse signups.
4. **Submission rate is inversely related to paid-traffic volume.** ~2–3.8% in leaner months (Jan–Apr), collapses to ~0.5–1% when paid social floods the site (EOFY, July). The popup does **not** capture the paid surge — the marginal paid visitor barely engages it.
5. **Mechanism:** cost/signup = spend ÷ (sessions × submit rate). The submit-rate collapse during sales is what drives the cost/signup spikes.
6. Absolute signups grew as the popup matured (Oct 1,248 → peak), but *submit rate* degraded as paid scaled.

### UPDATE 2026-08-16 — Alia API data (empirical) + open diagnosis
Distinguishing what the data proves from what it doesn't. Sources labelled.

**A. Confirmed — direct from Alia `/events/stats`:**
- **Submit-among-viewers** (`emailSignupRate` = email submits ÷ popup **views**), monthly:
  Apr **6.27%** · May **6.01%** · Jun **2.93%** · Jul **5.17%** · Aug **6.00%** (partial). Apr–Aug aggregate **4.74%**.
- **View rate** (`popupViewRate` = views ÷ Alia users): **April only** (429 rate-limited before more) = **40.4%** on `usersCount` 64,824.

**B. Our proxy** (Klaviyo signups ÷ Shopify sessions), monthly: Apr 3.81% · May 1.94% · Jun 1.12% · Jul 1.16% · Aug 0.96%.

**C. What the data establishes (empirical):**
1. **Submit-among-viewers is stable ~5–6%** (June the lone exception, 2.93%). The popup converts people who see it at a steady, healthy rate — it did **not** degrade.
2. The proxy fell ~4× while (1) held. By identity `proxy = submit_rate × view_rate`, the fall is therefore in **reach** (popup views per site visit). → **The list-growth slowdown is a REACH problem, not a popup-conversion problem.**

**D. What is NOT established (do not treat as fact):**
- **The monthly view-rate trend from Alia's own metric.** Only April (40.4%) was pulled before the 429. A derived "views ÷ Shopify sessions" gives Apr ~61%, but that **disagrees** with Alia's 40.4% (different denominators — Alia `usersCount` 64,824 ≈ 2× Shopify sessions 31,845), so treat any derived view-rate level as **indicative only**, not measured.
- **The cause** of the reach drop (device / landing page / source / trigger timing). The device-split call **failed** (filter ignored → identical mobile/desktop results), then rate-limited. **No segment-level view-rate data exists yet.**

**E. Context consistent with — but NOT proof of — a paid-traffic reach hypothesis:**
- Traffic mix shifted hard to paid social over the same window: Shopify `social` sessions **7,912 (Aug'25) → 95,742 (Jun'26) / 90,238 (Jul'26)**; organic search held ~5–6k/mo.
- EXP-002 (Alia BAU campaign, 28 Jul–5 Aug) measured **bounce 54–56%**.
These are *consistent with* "high-bounce paid traffic leaves before the popup fires," but do not prove it. Segmented `popupViewRate` is required to confirm.

**F. Decision pending diagnosis — embed vs activate (data does not yet resolve this):**
- **Targeting gap** (popup not set on the paid landing pages) → **activate/extend popup targeting**; no embed needed.
- **Bounce-before-trigger** (fast mobile exits) → activate **+ fast/scroll trigger**, plus an **embedded inline form** on dedicated paid LPs (visible on load; catches fast-bouncers a popup can't).
- **Blocked on:** `popupViewRate` split by `device` / `utmMedium` / `currentPath` via the cached `/api/popup` endpoint (needs rotated key in Vercel; Alia rate-limits ~2 live calls). Until that pull, F is a framework, not a recommendation.

### Attribution / profile facts
- Klaviyo profile props: `user_id` (= Shopify customer id, the join key), `alia_popup`, `alia_campaign`, `alia_flow_name`, `"What do you need for your machine?"` (poll intent), `alia_offer`, `$source`, `$sms_consent_method`, `$phone_number_region`, `Shopify Tags`.
- **No Meta `campaign_id` on the profile** → Meta attribution comes via Shopify `customerJourneySummary` UTM (`utm_campaign` = Meta campaign_id, `utm_term` = adset, `utm_content` = ad).
- **Email vs SMS:** some signups are SMS-dual; whether any are SMS-only is unresolved.

### Caveats
- "Submit rate" here = **visitor→signup proxy** (Shopify sessions denominator), **not** true popup **view→submit** (needs Alia impressions — Alia API, task #7 `/api/popup`).
- Conversion denominator = Shopify `tag:Alia` (~10% higher than Klaviyo source count); conversion is **lifetime-to-date**, so recent weeks under-count.
- Cost/signup = **all** Meta spend ÷ Alia signups (blended marketing $ per signup, per the agreed metric definition).

### Linked artifacts
- `deliverables/cost-per-signup-weekly.html` — weekly cost/signup vs conversion (dual-axis).
- `deliverables/popup-signup-report-365.html` — 365-day submission rate + cost/signup (mobile).
- Endpoint: `/api/emails` (Klaviyo). Assignment/analysis scripts under `scripts/` and `analysis/`.

### Open questions / next
- **True view→submit rate + email-vs-SMS split** → wire Alia API `/api/popup` (task #7).
- **Per-Meta-campaign cost-per-signup** → add `campaign_id` to `/api/campaigns` + UTM join (tasks #4–5).
- **Non-purchaser attribution** → `/api/events` (task #6).

---

## RP-002 — 2K Giveaway 2026: acquisition P&L
**Status:** Open (re-run after BFCM) · **Owner:** Matt · **Last updated:** 2026-08-25
**Question:** Did the 2K Giveaway make money from customers it *newly attracted* to the brand?

### Setup
- Giveaway list: 1,017 entrants, joins 27 May → 24 Jun 2026 (Klaviyo export 2026-08-25).
- **Cost: $3,365** ($2,000 prize + $1,365 Meta ads). Ads ran to ~Jun 10; after that the entry
  push went to the existing email list.
- **Attribution frame (chosen):** the **ad-driven segment** — entrants who joined before
  **Jun 10 2026, 7:00 AM AEST** (= 2026-06-09 21:00 UTC on Klaviyo's "Date Added"). 399 profiles.
  Validated: 85% of this segment were brand-new Klaviyo profiles (median profile age at entry
  0 days) vs the after-cutoff group being 73% pre-existing subscribers (median 137 days) —
  i.e. before-cutoff ≈ newly attracted by ads; after-cutoff ≈ own audience.
- Purchases: Shopify order export (full history → **17 Aug 2026**), matched by email.
  New-to-brand = no orders before their join date. Contribution = line ex-GST × category margins
  (Diggershield 80 / Hauler 68 / Pro Enclosure 63 / Exc Covers 62 / Pro Mats 59 / Access 50 / Grease 25).

### Headline P&L (ad-driven cut, to 17 Aug 2026)
| | |
|---|--:|
| Segment | 399 entrants (85% brand-new profiles) |
| New-to-brand buyers | **11** (12 orders) |
| Revenue (incl GST) | $2,751 |
| Contribution | $1,361 (Pro Enclosure $900 led) |
| + Direct ad purchases ($570.76 rev @45% blended) | +$233 |
| **Net vs $3,365 cost** | **−$1,770** |
| Cost per new customer (~13) | ~$260 (vs ~$86 blended CPA benchmark) |

### Sensitivity — the three attribution cuts
| Cut | Net | Reading |
|---|--:|---|
| Whole list (1,017) | +$6,375 | Inflated — 73% of late joiners were existing audience; counts activation as acquisition |
| **Ad-driven segment (399)** ✅ chosen | **−$1,770** | Ads-as-acquisition; conservative (misses 169 late organic new profiles) |
| All new profiles (510) | −$539 | Broadest honest cut; near break-even |

### Findings
1. **As an acquisition channel the giveaway has not paid back** (−$1,770 on the chosen cut,
   −$539 on the most generous honest cut). The apparent whole-list profit was own-audience buying.
2. **Giveaway entrants convert ~3–4% in 10 weeks** vs popup signups' ~29% lifetime — classic
   prize-hunter quality gap. Median 16 days to first purchase → the *sale* (EOFY), not the
   giveaway, triggered buying.
3. What it did buy: ~380–495 genuinely new emails at ~$7–8.40 each (cheap list growth), and the
   buyers it produced skewed **high-margin (Pro Enclosure-led, not Grease)**.

### Open / next
- **Re-run after BFCM 2026** (tail could close the gap — ~$1.8k more contribution needed on the
  chosen cut). Note in `AUTOMATIONS.md` §6 monthly-retro scope or set a one-shot reminder.
- Order data ends 17 Aug — refresh the export before the re-run.
- If repeating the play: build in a 10% entrant holdout so incrementality answers itself, and
  target buyers (offer/creative), not entry volume.
- Raw segment files live in session scratchpad only — **PII, never committed**. Method here is
  sufficient to reproduce from a fresh Klaviyo list export + Shopify orders export.

---

## RP-003 — Repeat rate (Ecommerce Equation definition) & Style-of-Sale classification
**Status:** Complete · **Owner:** Matt · **Last updated:** 2026-09-22
**Question:** On the Ecommerce Equation definition — *share of customers who have purchased more
than once* — what is DiggerLid's repeat rate, and which Style of Sale band are we in?
EE bands: **Low repeat 0–19% (25% of EE cohort) · Hybrid 20–39% (48%) · High repeat 40%+ (27%).**

### Data sources
- ShopifyQL `sales` dataset, `GROUP BY new_or_returning_customer` — distinct customers under
  "Returning" = customers who placed a non-first order in the window (exact, no export needed).
- Product/variant repeat = distinct orders containing the product ÷ distinct buyers of it, −1
  ("repeat orders per buyer"; upper bound on % of buyers with 2+ orders of that product).
- Window: all-time (2019 → 20 Sep 2026) and TTM (1 Sep 2025 → 31 Aug 2026). Completed sales;
  GWPs and Package Protection excluded from product tables.

### Headline — classification
| Definition | Customers | Repeat customers | Repeat rate | EE band |
|---|--:|--:|--:|---|
| Lifetime: bought 2+ times, ever | 27,060 | 4,790 | **17.7%** | Low repeat |
| TTM Shopify returning-customer rate (Sep 25–Aug 26) | 14,552 | 3,112 | **21.4%** | Hybrid (bottom edge) |

**Verdict: LOW-REPEAT store sitting on the Hybrid boundary.** Returning customers supply 21% of
lifetime orders / 20% of lifetime net sales (TTM: 24% / 24%). Strip grease out and the machine-
protection business repeats at <10% — a pure low-repeat durable. Grease is what lifts the blend
to the line. Read: run the business on **first-order economics** (AOV, first-order GPAM, immediate
CAC payback) — consistent with RP/cohort finding that 12-mo LTV ≈ first order — and treat grease
reorder as the one lever that could move us into Hybrid proper.

### Ex-grease: what are we without the consumable? (added 2026-09-22)
Same EE definition, grease system + GWPs + Package Protection filtered out of every order.

| Definition | Non-grease buyers | Returning | Repeat rate | EE band |
|---|--:|--:|--:|---|
| Lifetime | 17,926 | 2,485 | **13.9%** | Low repeat |
| TTM (Sep 25-Aug 26) | 8,316 | 1,362 | **16.4%** | Low repeat |

**Ex-grease verdict: LOW REPEAT, unambiguously** (vs 17.7% / 21.4% with grease). Grease adds
~4-5 points of repeat rate and is the only thing that gets the blend to the Hybrid line. Within
the TTM window alone, non-grease buyers generated just 6.7% extra orders per buyer (8,870 orders
/ 8,316 buyers) - the 16.4% is mostly older customers coming back for a second machine/accessory.
Returning non-grease customers = 12% of non-grease net sales lifetime ($764k of $6.26M).
Caveat: "returning" is store-level, so a grease-first customer buying one cover later counts as
returning here - true ex-grease 2+ rate is at or slightly below these figures.

### PRO Mat customers only (added 2026-09-22)
Source: ShopifyQL `customers` dataset (`products_purchased MATCHES (id = 8213717909674)`,
`GROUP BY customer_number_of_orders`) + `sales` new/returning split. PRO Mat live since 25 Aug 2025.

| Definition | Customers | Bought 2+ | Repeat rate | EE band |
|---|--:|--:|--:|---|
| PRO Mat as a standalone store (bought PRO Mat twice+) | 3,168 | ~64-80 | **~2.0-2.5%** | Low repeat |
| PRO Mat-first customers who bought *anything* again | 2,962 | 141 | **4.8%** | Low repeat |
| PRO Mat buyers acquired since launch, any 2nd order | 3,055 | 235 | **7.7%** | Low repeat |
| Same-age benchmark: ALL customers acquired since 25 Aug 2025 | 13,650 | 1,440 | 10.5% | Low repeat |
| PRO Mat buyers, lifetime store orders (incl. pre-PRO-Mat history) | 3,167 | 347 | 11.0% | Low repeat |

**PRO Mat verdict: LOW REPEAT, deep in the band - and below the store's same-age average.**
It is a pure acquisition product: **93.5% of PRO Mat buyers (2,962 of 3,168) were new to
DiggerLid on that order**, only 206 were existing customers adding it. Once bought, ~2% buy
another mat and ~5% buy anything else within the product's 13-month life. Run PRO Mat entirely
on first-order economics (AOV via PLUS/colour mix, bundles, GPAM at first order); it has no
retention layer to invest in. Cross-sell after PRO Mat is the only repeat path and it is small.

### Category & product repeat (all-time, repeat orders per buyer)
| Set | Buyers | Orders | Repeat |
|---|--:|--:|--:|
| Whole store | 27,061 | 34,301 | 26.8% |
| Grease system (packs, gun, adapter, coupler, coupling caps) | 13,300 | 17,419 | **31.0%** |
| Grease products only (packs, gun, adapter, coupler) | 12,539 | 16,408 | 30.9% |
| Machine protection (7 covers + Enclosure + DiggerShield + PRO Mat) | 13,262 | 14,556 | 9.8% |
| Covers only (7 cover products) | 7,035 | 7,813 | 11.1% |
| Accessories (10 products) | 6,236 | 6,895 | 10.6% |
| Portable protection (PRO Mat) | 3,168 | 3,249 | 2.6% |

Product level: KAJO Grease Packs **26.8%** · Universal/Engine Covers 9.3% · Battery Gun Adapter
8.4% · KAJO Gun 8.3% · Coupling Cap Set 8.2% · Quicky Cover 7.2% · Skid Steer Cover 6.4% ·
Mini Loader Cover 6.1% · Phone Cradle 5.3% · Coupler 4.0% · DiggerShield 3.5% · Pro Enclosure 3.2%
· PRO Mat 2.6% · 1.7T Cover 2.2% · Micro Cover 1.5% · Hauler 1.4%.

### Outliers (variant drilldown)
1. **Reorderers switch variant.** Grease Packs repeat 26.8% at product level but every variant
   only 7–15% (LZR2 13.7%, LC002 10.3%, HD800 8.1%) → second orders change size or grade.
   40-pc packs are the stickiest variants (LZR2/40 14.0%, LC002/40 15.2%, 2050/40 14.1%) —
   bulk buyers = the loyal fleet/contractor segment. **Hammer Paste: 0% repeat on 93 buyers.**
2. **Battery adapter 8.4% is a second-platform effect, not a consumable.** Milwaukee 7.1%,
   Makita 3.1%, DeWALT 0.9%, AEG 0% → product-level repeat comes from buying a second adapter
   for another battery system. Milwaukee users are the heaviest repeaters.
3. **Cheap/universal covers repeat like multi-machine fleets.** Universal covers 9.3% at product
   level vs 5.7–5.9% per size; Quicky default 6.5% vs colours ≤2% → buyers cover additional
   machines / sizes, not replacements. The premium 1.7T cover (2.2%) and Micro (1.5%) are
   one-and-done.
4. Accessory outliers: Coupling Cap Set 8.2% (caps get lost — treat as grease-system consumable);
   Trucker Cap 6.0% (merch repeat); Boom Bottle Opener 1.5% (gift, never reorders).

### Caveats
- "Repeat orders per buyer" (product tables) ≥ true % of buyers with 2+ orders of that product;
  the gap only matters for grease (Aug-2026 cohort measured 24.8% exact vs 26.8% here).
- ~3,000 buyers sit under a blank/legacy product title and are unattributed in product tables.
- Lifetime rate is depressed by the 88% of TTM customers who are <12 months old and haven't had
  time to repeat; TTM returning-customer rate (21.4%) is the fairer like-for-like with EE peers.
- ShopifyQL analytics endpoint rate-limits to roughly one query per 2 minutes when chained.

### Linked artifacts
- `deliverables/cohort-cltv-cross-purchase-2026-08-17.md` (entry-cohort exact repeat %, margins).

### Open questions / next
- Re-run TTM returning-customer rate quarterly; crossing 25% = genuinely Hybrid.
- Grease reorder programme (subscription / 40-pc nudge / restock email at ~90 days) is the only
  repeat lever with mass; size the opportunity before BFCM planning.
- Hammer Paste 0% repeat — confirm whether use-rate or product issue (VoC).

## RP-004 — Sale curve shape: do we sell like a Hybrid or a Low-repeat store?
**Status:** Complete · **Owner:** Matt · **Last updated:** 2026-09-22
**Question:** RP-003 says our repeat rate is Low/borderline-Hybrid. Our sales *feel* Hybrid. Which
EE "Style of Sale" curve (% of total sale revenue by day on sale) do we actually follow, and why?
EE reference curves (12-day sale): High repeat ≈40% day 1, ~2-3%/day mid, small end bump ·
Hybrid ≈30% day 1, ~5%/day mid, ~6% end · Low ≈20% day 1, ~8-9%/day flat mid, ~5-6% end.

### Data sources
- ShopifyQL `sales` net_sales/orders TIMESERIES day, `GROUP BY new_or_returning_customer`.
- Sale windows from Klaviyo send log: **EOFY 2026** hype 15 Jun → launch 17 Jun (1:55 PM) → close
  30 Jun (14 days). **BFCM 2025** hype 15-16 Nov → launch 18 Nov (3:05 PM) → Cyber Monday 1 Dec
  (14 days). BAU reference = Aug 2026.

### Curves (% of total sale net revenue by day on sale)
| Day | EOFY 26 | BFCM 25 | | Day | EOFY 26 | BFCM 25 |
|--:|--:|--:|---|--:|--:|--:|
| 1 | 12.6% | 17.9% | | 8 | 5.4% | 5.5% |
| 2 | 6.8% | 13.5% | | 9 | 4.9% | 5.4% |
| 3 | 5.7% | 7.6% | | 10 | 4.7% | 4.3% |
| 4 | 4.1% | 6.4% | | 11 | 3.7% | 4.0% |
| 5 | 5.2% | 5.4% | | 12 | 6.7% | 5.2% |
| 6 | 4.7% | 5.4% | | 13 | 11.6% | 5.6% |
| 7 | 4.0% | 4.1% | | 14 | **20.0%** | 9.7% |

Totals: EOFY $543k net / 2,107 orders · BFCM $535k / 1,759 orders. Pre-sale baseline ~$11k/day
(EOFY) and ~$7k/day (BFCM) ≈ 2%/day of sale total.

| Phase | EOFY 26 | BFCM 25 | EE Low | EE Hybrid |
|---|--:|--:|--:|--:|
| Launch 48h | 19.4% | **31.4%** | ~25% | ~35% |
| Mid-sale plateau (d3-12, per day) | **4.9%** | **5.3%** | 8-9% | ~5% |
| Last 48h | **31.6%** | 15.2% | ~10% | ~10% |

### Who buys at the spikes (returning-customer share of net revenue)
| | EOFY 26 | BFCM 25 | BAU Aug 26 |
|---|--:|--:|--:|
| Whole sale | 28.7% | 22.0% | 24.5% |
| Launch 48h | 30.9% | 24.4% | |
| Mid-sale d3-12 | 30.1% | 17.7% | |
| Last 48h | 25.1% | 32.4% | |
| Peak day | 31.6% (launch) / 26.0% (close) | 29.6% (launch) / 42.9% (Cyber Mon) | |

### Findings
1. **The curve is Hybrid-shaped.** The diagnostic EE uses to separate Low from Hybrid is the
   mid-sale plateau: Low-repeat stores sit at 8-9%/day because steady new-customer demand isn't
   pulled forward by hype; ours sits at **~5%/day in both sales** - the Hybrid signature. The hype
   spike is ≈30% of revenue in both sales (BFCM 31% front, EOFY 32% back).
2. **But the mechanism is not the EE one.** Hybrid/High curves spike because the loyal base
   buys on launch. Our returning share during sales (22-29%) is the same as BAU (24.5%), and the
   peak days are **70-74% new customers**. The spike is *urgency acting on acquisition traffic*
   (paid social + list reach), not the base returning. → **Hybrid-shaped sale on a Low-repeat
   customer base.** Forecast with the Hybrid curve; pull the levers of a Low-repeat store.
3. **EOFY and BFCM are mirror images because the urgency sits at opposite ends.** BFCM's
   urgency is the launch (scarcity of the deal); EOFY's is the 30 June tax deadline (external, so
   customers wait - last 48h = 32%, last day alone $109k / 356 orders, 74% new). Same total, same
   plateau, opposite skew. Plan the two sales differently: BFCM front-loads spend + inventory;
   EOFY back-loads them.
4. **Email to the engaged base does move returning share** - Cyber Monday (43% returning, after
   the 25 Nov Engaged-30D send drove 37%) and EOFY day 9 (42%). The full-database sends do not.
   Segmented sends to engaged/grease buyers are the only tool that changes *who* buys.
5. Anomaly: BFCM day 11 (Black Friday itself) shows 18 returning orders but only $411 net
   returning revenue - refunds/heavy discounts netted; treat that cell as noise.

### Implications for BFCM 2026 (feeds the concept board + forecast)
- Expect ~30% of sale revenue in the first 48h, ~5%/day plateau, ~10-15% in the last 48h if
  Cyber Monday closes it. Nov forecast $605k → ~$180k launch weekend, ~$30k/day plateau.
- The plateau is the upside: the Knock-Off 3:30 daily-drop mechanic (concept #5) is a
  plateau-lifter; measure it against the 5%/day baseline.
- Launch-day buyers are 70% new → launch creative and paid budget are acquisition plays; don't
  starve prospecting on day 1 to "protect" retargeting.
- One Engaged-segment send mid-sale and one at close are worth more than another full-database
  blast (finding 4).

### Caveats
- Two sales only; 14-day windows vs EE's 12-day reference (shares rescale but shape holds).
- Launch-day % depends on launch hour (both launched early-mid afternoon → day 1 is ~10 hours).
- Net sales include same-day refunds netting; day-level returning revenue is noisy at small N.

### Linked artifacts
- RP-003 (repeat rate); `deliverables/bfcm-2026-concept-board.md`; `data/FORECAST.md`.

### Open questions / next
- Rebuild after BFCM 2026 with three sales; test whether the Knock-Off drops lift the plateau.
- Pull FD 2026 (Father's Day, Aug 17-Sep 6) curve for a third data point on a gift-driven sale.

## RP-005 — Sale landing pages: BFCM 2025 vs EOFY 2026 (and Father's Day 2026)
**Status:** Complete · **Owner:** Matt · **Last updated:** 2026-09-22
**Question:** How did the sale landing pages perform - `/pages/blackfriday` (BFCM 2025) vs
`/pages/eofy-2026` (EOFY 2026) - and what does it mean for the BFCM 2026 page? Father's Day
2026 (`/pages/fathers-day-2026`) included as a third, smaller data point.

### Data sources
- ShopifyQL `sessions` dataset, `landing_page_path` dimension (sessions, conversion, cart adds,
  checkout reached/completed), by day and by `referrer_source`. Windows: BFCM 15 Nov-1 Dec 2025;
  EOFY 15-30 Jun 2026; FD 18 Aug-7 Sep 2026.
- PostHog HogQL (project 475333) for EOFY and FD only - history starts 18 Jun 2026, so it misses
  EOFY launch day and has nothing for BFCM 2025. Person-stitched funnel (LP viewers → PDP view →
  Product Added → Order Completed within window), next-page products, referring domain, UTM, device.

### Headline
| | BFCM 2025 `/pages/blackfriday` | EOFY 2026 `/pages/eofy-2026` | FD 2026 `/pages/fathers-day-2026` |
|---|--:|--:|--:|
| Landing sessions | 17,870 | 11,304 | 4,464 |
| Conversion (session → order) | **2.09%** | **3.38%** | 2.33% |
| Orders from LP-landing sessions | 373 | 382 | 104 |
| Share of all sale-window sessions landing on LP | 37% | 15% | n/a |
| Share of sale orders | ~21% | ~18% | n/a |
| Add-to-cart rate | n/a (tracking gap: 315 ATC < 373 orders) | 9.9% | 7.5% |
| Reached checkout | 2.8% | 4.7% | n/a |
| Peak day | 19 Nov: 4,628 sessions @ 0.99% | 30 Jun: 1,387 @ 5.84% (launch 17 Jun: 1,379 @ 5.37%) | 25 Aug: 620 @ 2.4% |

**EOFY's page converted 62% better on 37% fewer sessions and produced more orders.**

### By traffic source (Shopify referrer_source)
| Source | BFCM sessions | BFCM CVR | EOFY sessions | EOFY CVR |
|---|--:|--:|--:|--:|
| Social (paid + organic) | 14,882 (83%) | 1.37% | 7,980 (71%) | 2.04% |
| Direct | 2,775 (16%) | 5.48% | 3,133 (28%) | 6.58% |
| Email (Shopify-classified; PostHog UTM shows ~725 EOFY email sessions) | 71 | 0% | 156 | 6.4% |

Both sources converted better on the EOFY page (social +49%, direct +20%) AND the mix was
warmer (28% direct vs 16%). So it is both a better page/offer and a better audience.

### Findings
1. **The BFCM page was flooded with cold social on day 2.** 19 Nov: 4,628 sessions (26% of all
   LP traffic) at 0.99% - half the page's average. Launch day itself was 3,190 @ 2.6%. That one
   day of broad prospecting dragged the page from ~2.6% to 2.09%.
2. **Homepage landers out-convert both sale pages 3-4x** (BFCM `/` 5,404 @ 8.4%, 456 orders;
   EOFY `/` 4,880 @ 10.2%, 499 orders). The homepage catches returning/brand/email traffic; the
   LP catches cold social. Judge the LP on source-matched conversion, not against the homepage.
3. **Hype-phase traffic to the LP is wasted.** Pre-launch days sent 2,328 (BFCM) and 2,019
   (EOFY) sessions to a page with nothing to buy: ~0.6% conversion, 13 and 12 orders. That is
   ~4,300 warm sessions with no email/SMS capture in front of them.
4. **PostHog, EOFY (18-30 Jun):** 5,282 viewers, 5.7 pages per session (engaged, not a bounce
   page); 36% went on to a PDP, 21% added to cart, 10% ordered within the window (person-level,
   any session). 87% mobile. The page pushed grease first (LZR2 449 sessions), then Pro Enclosure
   381, DiggerShield 354, PRO Mat 278, coupler 276 - a broad-range page. Sources: Meta ~3,500
   sessions, direct 1,668, on-site navigation 1,196, email ~725, Google 202.
5. **PostHog, FD (21 Aug-7 Sep):** 3,892 viewers, 5.4 pages/session; 45% to PDP, 21% ATC, 10.5%
   ordered - the same person-level funnel as EOFY despite lower Shopify session CVR. 12% of
   viewers were existing customers. PRO Mat dominated the next click (817 sessions, 3x the next
   product) - a single-hero page. By contrast the FD **gift** page (`/pages/gift`, EXP-005)
   was a dud: 999 viewers, 7% to PDP, 1.3% ATC, 0.5% ordered, 2.3 pages/session.
6. **FD page went live 4 days after the sale started** (first traffic 21 Aug; sale 17 Aug).
7. **Data gaps:** BFCM 2025 cart-add tracking is broken (fewer cart adds than orders), so ATC
   rates can't be compared; PostHog new/existing for EOFY is unusable (history starts inside the
   window, everyone looks new).

### Implications for the BFCM 2026 page
- Keep the LP as the paid-social destination, but **split cold prospecting from warm**: broad
  prospecting → category/PDP destinations (grease, PRO Mat) that convert social at 2-5%; LP for
  retargeting, email, direct. Day-2 floods at 1% are the single biggest drag.
- **Lead with grease and PRO Mat**, the two categories social traffic actually buys; big-ticket
  enclosure/DiggerShield lower on the page (EOFY ordering worked).
- **Pre-launch LP = capture page** (email/SMS "first access" form + countdown), not a preview of
  a sale that isn't live. ~2,000-2,300 hype sessions each sale are currently thrown away.
- **Build and QA the page before the hype sends**, not after launch (FD lesson).
- Verify cart-add tracking on the LP before 15 Nov; without it the funnel can't be read.
- Benchmarks to beat: 3.4% session conversion, 10% ATC, 5+ pages/session, social ≥2%, direct ≥6%.

### Findings with confidence (added 2026-09-22)
| # | Finding | Confidence | Why |
|---|---|---|---|
| 1 | EOFY page out-converted BFCM page (3.38% vs 2.09%; 382 vs 373 orders on 37% fewer sessions) | **High** | Direct Shopify measure, N = 11k / 18k sessions, difference far outside noise |
| 2 | Both mix (28% vs 16% direct) and within-source conversion (social +49%, direct +20%) improved | **High** | Same source split on both pages; social N = 8k / 15k |
| 3 | 19 Nov cold-social flood (4,628 @ 0.99%) was the biggest single drag; ex that day BFCM ran ~2.6% | **Medium-high** | Day-level data is exact; "broad prospecting" as the cause is inferred, not confirmed from Ads Manager |
| 4 | Homepage landers out-convert both LPs 3-4x because they carry warm traffic | **High** on the numbers, **Medium** on the cause | Conversion exact; warm-traffic explanation consistent with direct/email CVR but not source-split for `/` |
| 5 | Pre-launch hype traffic to the LP converts ~0.6% (2.3k + 2.0k sessions, 25 orders) | **High** | Exact day-level counts on both sales |
| 6 | EOFY page is engaged, not a bounce page (5.7 pages/session; 36% to PDP, 21% ATC, 10% ordered person-level) | **Medium** | PostHog covers 18-30 Jun only (misses launch day); person-level funnel is any-session, not attributed |
| 7 | EOFY page pushed grease first; FD page was a PRO Mat single-hero page | **High** | Next-click counts, large N |
| 8 | FD gift page (`/pages/gift`) was a dud (0.5% ordered, 2.3 pages/session) | **Medium-high** | N = 999 viewers; consistent with EXP-005 read |
| 9 | FD page launched 4 days after the sale started | **High** | First traffic 21 Aug in both Shopify and PostHog |
| 10 | BFCM 2025 cart-add tracking was broken | **High** | Fewer cart-add sessions than completed checkouts is impossible under correct tracking |
| 11 | Recommendation: split cold prospecting to PDP/category, LP for warm; pre-launch capture page | **Medium** | Sound inference from 1-5, but untested - needs a designed split at BFCM 2026 |

### Caveats
- Shopify landing-page conversion attributes the order to the session that landed on the page;
  later sessions that convert are not credited (PostHog person-level funnel shows ~3x higher).
- Windows include hype days for LP totals; sale-order shares use the sale windows from RP-004.
- Referrer classification differs between Shopify (email 156) and PostHog UTM (~725).

### Linked artifacts
- RP-004 (sale curves), `experiments/EXPERIMENT-LOG.md` EXP-005 (gift page), `deliverables/bfcm-2026-concept-board.md`.

### Open questions / next
- Rebuild after BFCM 2026 with source-split LP vs PDP destinations as a designed test.
- Add `/pages/<sale>` pre-launch capture-rate as a scorecard row during hype phases.

## RP-006 — Popup signup → purchase conversion over the popup's life
**Status:** Complete · **Owner:** Matt · **Last updated:** 2026-09-22
**Question:** Over a long period, what share of popup (Alia) email signups go on to buy, how fast,
what is a signup worth, and do signups collected before a sale convert during it? (Sets the value
of an email for the pre-BFCM "traffic + emails" push.)

### Data sources
- **Shopify segment counts** (`customerSegmentMembers.totalCount`, query language:
  `customer_tags CONTAINS 'Alia' AND customer_added_date … AND number_of_orders …`). Alia creates a
  Shopify customer for every signup and tags it `Alia`, so added-date = signup month. Zero records
  pulled, zero PII. Verified: 6,219 Alia-tagged buyers matches ShopifyQL exactly.
- Klaviyo `/api/emails` (`$source = Alia sign-up`) monthly as a denominator cross-check
  (Shopify runs ~8% higher: SMS-only and duplicate-email signups).
- ShopifyQL `sales WHERE customer_tag = 'Alia' GROUP BY new_or_returning_customer` for revenue.
- **Not** the Alia API (key pending rotation; rate-limited; knows views/submits, not purchases).
- Gotchas learned: `customersCount(query:)` only honours `created_at`/`id`/`updated_at` — it
  silently ignores `tag:` and `orders_count:` (returned all 44,836 customers). Segment counts cost
  ~112 query points each → max 8 per call. `customer_date` in the customers search = created date.

### Cohorts (Shopify Alia-tagged customers by signup month, as at 22 Sep 2026)
| Signup month | Signups | Bought | Conv. | 2+ orders | Age (mo) |
|---|--:|--:|--:|--:|--:|
| Oct 2025 | 1,346 | 442 | 32.8% | 104 | 11 |
| Nov 2025 | 2,280 | 659 | 28.9% | 129 | 10 |
| Dec 2025 | 1,393 | 302 | **21.7%** | 40 | 9 |
| Jan 2026 | 959 | 276 | 28.8% | 41 | 8 |
| Feb 2026 | 1,233 | 370 | 30.0% | 41 | 7 |
| Mar 2026 | 1,219 | 378 | 31.0% | 43 | 6 |
| Apr 2026 | 1,315 | 391 | 29.7% | 49 | 5 |
| May 2026 | 1,624 | 520 | 32.0% | 62 | 4 |
| Jun 2026 | 1,541 | 516 | 33.5% | 77 | 3 |
| Jul 2026 | 1,469 | 425 | 28.9% | 40 | 2 |
| Aug 2026 | 1,711 | 467 | 27.3% | 21 | 1 |
| Sep 2026 (to 22nd) | 921 | 252 | 27.4% | 7 | 0 |
| **Popup era total** | **17,011** | **4,998** | **29.4%** | 654 (3.8%) | |

Pre-popup Alia-tagged (added before Aug 2025): 1,246, 89% buyers — Alia tagging existing customers
who identified on-site; excluded. Klaviyo signups same months: 15,701 (see appendix in file).

### What a signup is worth (popup era)
- Alia-tagged customers' net sales Aug 25–21 Sep 26: **$2.13M** ($1.57M first orders on 5,159
  customers = **$305 first-order AOV**; $0.56M returning). ≈ **$120 net revenue per signup**,
  ≈ $90 of it first-order; contribution at (1−VCR 0.468) ≈ **$65 per signup**.
- Spend distribution: 58% of signup-buyers spend ≥$250 lifetime, 25% ≥$500, 4.8% ≥$1,000.
- Signup-buyers repeat more than the store (13.1% of buyers have 2+ orders within ≤11 months vs
  17.7% lifetime store-wide; Oct cohort already 23.5%).

### Do pre-sale signups convert in the sale?
| | Signed up before the sale | Bought before sale | **Bought during sale** | Ever bought |
|---|--:|--:|--:|--:|
| BFCM 2025 (signups 1 Oct–14 Nov) | 2,170 | 391 (18.0%) | **128 = 5.9% of cohort, 7.2% of not-yet-buyers** | 684 (31.5%) |
| EOFY 2026 (signups 1 Jan–14 Jun) | 7,330 | 1,773 (24.2%) | **227 = 3.1% of cohort, 4.1% of not-yet-buyers** | 2,231 (30.4%) |
| Signups **during** BFCM (15 Nov–1 Dec) | 1,529 | | | 436 (28.5%) |
| Signups **during** EOFY (15–30 Jun) | 561 | | | 220 (**39.2%**) |
("Bought during sale" = last order date inside the sale window; slightly undercounts people who
ordered in-sale and again later.)

### Popup offer / interest tags (popup era, signups → buyers)
| Tag | Signups | Conv. | Note |
|---|--:|--:|---|
| Control (no offer) | 3,254 | 31.6% | |
| Control 10% | 86 | 44.2% | tiny N |
| $35 Off | 207 | 31.9% | |
| Free Shipping over $399 | 1,375 | 36.8% | co-occurs with other tags; treat as indicative |
| Interest: Maintenance gear | 5,719 | **35.1%** | grease intent converts best |
| Interest: Not sure yet | 3,577 | 31.5% | |
| Interest: Weather covers | 3,735 | 27.8% | |

### Findings (with confidence)
1. **Long-run signup → buyer conversion is ~30% and remarkably stable** (27–34% every cohort bar
   Dec 2025's 21.7%). *High* — exact counts, N = 17k.
2. **Conversion is fast and front-loaded.** One-month-old cohorts sit at ~27%; eleven-month-old at
   ~33%. Roughly 85% of the conversion that will ever happen happens in the first month — i.e. at
   the welcome offer. *High* (cross-sectional cohort ages; consistent with RP-002's median 16 days).
3. **Signups do not "bank" for the sale.** Among people who signed up before a sale and had not yet
   bought, only 4–7% bought during it. The sale is not what converts the list; the welcome flow is.
   *High* on the numbers; *Medium-high* on the interpretation (last-order-date proxy).
4. **Signups made during a sale convert at least as well as normal (28–39%)** — but capture
   collapses in sales (EOFY: 561 signups in 16 days vs ~1,500/month), per RP-001. *High*.
5. **A signup is worth ≈$120 net revenue / ≈$65 contribution** over its first year. *Medium* —
   revenue window mixes cohorts; contribution uses blended VCR; incrementality unknown (no
   popup holdout — Alia's "Control" tag is an offer control, not a no-popup control).
6. **Grease-intent signups convert best (35%); cover-intent worst (28%).** *High* on counts.
7. Dec 2025 signups (post-BFCM) are the worst cohort (21.7%) — sale-hangover signups. *Medium*.

### Decision read for the "traffic + emails until BFCM" direction
- **Yes to emails now, for the right reason:** each signup pays back ~30% × $305 within weeks
  via the welcome offer, not at BFCM. Collect emails from now until mid-Nov and they monetise
  *now*; the BFCM lift on the residual list is only ~5–7 points of the unconverted ~70%.
- **Value ceiling for an incremental email ≈ $65 contribution** (first year). RP-001's blended
  "$90–115/signup" is Meta spend ÷ signups, not the marginal cost — a dedicated lead campaign
  should be judged against $65, with a discount for non-incrementality.
- **Bias capture toward grease intent** (35% vs 28%) — the popup's interest question is a usable
  qualifier; grease-intent signups also feed the one repeat lever (RP-003).
- **Protect capture during the sale itself** (in-sale signups convert 28–39% but volume dies):
  the pre-launch LP capture page (RP-005) and a sale-specific popup are the fix.
- Dec cohort is weak: don't over-spend on post-BFCM list growth.

### Alia reach layer (added 2026-09-22, partial pull — API budget exhausted)
Alia `usersCount` by month Oct 25–Mar 26 + Aug 26 `popupViewsCount` (35,059) were obtained before
the API's cost budget ran out (monthly one-stat calls succeed; half-year calls 429). Combined with
Shopify sessions, Shopify Alia signups (RP-006) and buyers:

| Month | Shopify sessions | Alia users | Alia users ÷ sessions | Signups | Signups ÷ Alia users | Buyers | Buyers ÷ Alia users |
|---|--:|--:|--:|--:|--:|--:|--:|
| Oct 25 | 43,955 | 58,928 | 1.34 | 1,346 | 2.28% | 442 | 0.75% |
| Nov 25 | 78,359 | 96,645 | 1.23 | 2,280 | 2.36% | 659 | 0.68% |
| Dec 25 | 50,255 | 61,949 | 1.23 | 1,393 | 2.25% | 302 | 0.49% |
| Jan 26 | 29,663 | 36,509 | 1.23 | 959 | 2.63% | 276 | 0.76% |
| Feb 26 | 39,299 | 51,091 | 1.30 | 1,233 | 2.41% | 370 | 0.72% |
| Mar 26 | 36,747 | 42,329 | 1.15 | 1,219 | 2.88% | 378 | 0.89% |
| Apr 26 | 31,845 | 64,824 (RP-001) | 2.04 | 1,315 | 2.03% | 391 | 0.60% |
| Aug 26 | 103,965 | n/a · **35,059 popup views** | | 1,711 | **4.9% of views** · 1.6% of sessions | 467 | |

**Measured popup views (Alia `popupViewsCount`, pulled 22 Sep 2026 — full popup era Oct 25–Sep 26):**
| Month | Sessions | Popup views | **Views ÷ sessions (reach)** | Signups (Shopify) | Signups ÷ views (submit) | Signups ÷ sessions |
|---|--:|--:|--:|--:|--:|--:|
| Oct 25 | 43,955 | 29,322 | **67%** | 1,346 | 4.6% | 3.06% |
| Nov 25 (BFCM) | 78,359 | 59,762 | **76%** | 2,280 | 3.8% | 2.91% |
| Dec 25 | 50,255 | 33,877 | **67%** | 1,393 | 4.1% | 2.77% |
| Jan 26 | 29,663 | 19,923 | **67%** | 959 | 4.8% | 3.23% |
| Feb 26 | 39,299 | 27,526 | **70%** | 1,233 | 4.5% | 3.14% |
| Mar 26 | 36,747 | 23,426 | **64%** | 1,219 | 5.2% | 3.32% |
| Apr 26 | 31,845 | 25,330 | **80%** | 1,315 | 5.2% | 4.13% |
| May 26 | 76,386 | 33,302 | **44%** | 1,624 | 4.9% | 2.13% |
| Jun 26 (EOFY) | 125,171 | 66,430 | **53%** | 1,541 | 2.3% | 1.23% |
| Jul 26 | 116,420 | 38,704 | **33%** | 1,469 | 3.8% | 1.26% |
| Aug 26 | 103,965 | 35,059 | **34%** | 1,711 | 4.9% | 1.65% |
| Sep 26 (to 21st) | 82,013 | 18,636 | **23%** | 921 | 4.9% | 1.12% |

**Alia&#39;s own denominator (popup views ÷ Alia `usersCount`), for the same months:** Oct 50% · Nov 62% ·
Dec 55% · Jan 55% · Feb 54% · Mar 55% · Apr 39% · May 48% · Jun 64% · Jul 39% · Aug 41% · Sep 27%.
Alia users: May 70,018 · Jun 103,327 · Jul 98,560 · Aug 86,553 · Sep (to 21st) 70,028. The ratio of
Alia users to Shopify sessions is unstable (1.2× through March, 2.0× in April, 0.85× by July), so the
two denominators disagree on the level; both agree on the direction — Alia&#39;s view rate halved from
~55% to 27%.

**Alia&#39;s own attribution (30-day window, `maxMsSinceSignup` = 2592000000), three sample months:**

| Signup month | Alia submits | Orders within 30 days | Alia 30-day conv. | Shopify cohort conv. (any time, RP-006 table) |
|---|--:|--:|--:|--:|
| Nov 2025 (BFCM) | 2,672 | 672 | **25.2%** | 28.9% |
| Mar 2026 | 1,483 | 456 | **30.8%** | 31.0% |
| Aug 2026 | 2,371 | 681 | **28.7%** | 27.3% |

Independent cross-check of the 29.4% signup→buyer rate measured from Shopify customer records. Alia
counts submits, so its denominator runs above Shopify&#39;s deduplicated customer count (Aug: 2,371 vs
1,711), yet the rates agree within a few points, and Alia&#39;s 30-day figure lands almost on the
all-time cohort figure — direct confirmation that conversion happens inside the first month.
Alia&#39;s August `popupViewRate` on its own `userFlows` denominator: 45.9% (36,143 views / 78,821 flows);
Alia August `bounceRate` 48.1% (21,522 engaged of 41,479 sessions), consistent with the paid-traffic
bounce behind the reach drop. Alia pull complete 22 Sep 2026; key used transiently and removed.

**This settles RP-001's open question: the signup slowdown is reach, and the collapse is large.**
- Reach ran **64–80% of sessions for eight straight months (Oct 25–Apr 26), including 76% in the
  BFCM 2025 sale month**, then fell to 44–53% through May–June, **33–34% in Jul–Aug, and 23% in
  September** — a two-thirds drop while paid traffic tripled. The break dates from May 2026, so
  it is not a property of sale months: something changed in traffic mix, pages or popup settings
  around then.
- Submit-among-viewers is flat at **4.5–5.2%** every month except June (2.3%, sale mode). The
  popup converts the people who see it exactly as well as it always did.
- Capture per session therefore fell from 3.1% (Feb) to 1.1% (Sep). At February's reach on
  September's traffic, September would have produced ~2,800 signups instead of 921 — roughly
  **3× the emails, ~550 more buyers, ~$170k more first-order revenue in a single month**.
- The paid surge is the mechanism: sessions that arrive from Meta bounce or leave before the
  popup fires (RP-001's EXP-002 bounce 54–56%; RP-005's 0.99% cold-social LP conversion).

**Immediate action (feeds the BFCM inputs note):** fix reach before buying traffic. Check the
popup's trigger rules (delay / scroll / exit-intent / page targeting) against the paid landing
pages (`/pages/*`, PRO Mat PDP, grease PDPs), and confirm the popup fires on them at all.
Target: back above 50% reach on paid traffic by mid-October; measure weekly with one Alia call.

Inferences (labelled):
- **Capture per Alia user is stable at ~2.0–2.9%** (fact, 7 months) — the same stability RP-001
  saw in submit-among-viewers (5–6%). The popup is not the variable.
- **Reach halved when paid traffic surged.** Aug 26: 35k popup views on 104k sessions = ~34% of
  sessions saw the popup, vs an implied ~50–60% in Jan–Apr (signups ÷ sessions 2.6–3.8% at a
  5–6% submit rate). *Inference* — Jan–Apr views are derived, not measured; Alia's Apr
  popupViewRate (40% of Alia users) and the 2× users/sessions ratio that month show the
  denominators differ, so treat the *level* as indicative and the *direction* as solid.
- **End-to-end: ~0.5–0.9% of Alia users become signup-buyers**; Dec 25 lowest (0.49%).
- Aug 26 full funnel: 104k sessions → 35k popup views (34%) → 1.7k signups (4.9% of views) →
  ~470 buyers (27–29%) → ~0.45% of sessions; at $305 AOV ≈ **$1.4 net revenue per session via
  the popup path**, ≈ 13% of that month's RPV (~$4.4).
- Alia's `emailSignupRate` (6.0% Aug) runs above signups÷views (4.9%) — Alia counts submits,
  Shopify/Klaviyo count deduplicated profiles.

**Decision read (adds to above):** the cheapest email growth is *reach*, not conversion — every
extra 10 points of popup view share on Aug traffic ≈ +500 signups/month ≈ +145 buyers ≈ +$44k
revenue. Fix reach (trigger timing / paid landing pages that fire the popup) before paying for
more traffic to feed a popup a third of visitors never see.

### FINAL — analysis & insights (2026-09-22)
**The popup→purchase system has two constants and one broken variable.**

| Funnel per 100 sessions | Jan–Apr 26 (healthy) | Sep 26 (now) |
|---|--:|--:|
| Popup reach (views ÷ sessions) | **67–80%** | **23%** |
| Submit among viewers | 4.5–5.2% | 4.9% |
| Signups per 100 sessions | 3.1–4.1 | 1.1 |
| Signup → buyer (first month ≈ 27%, matures to ~33%) | ~30% | ~30% |
| Buyers per 100 sessions via the popup path | ~1.0 | ~0.33 |
| Revenue per session via the popup path (× $305 first-order AOV) | ~$3.1 | ~$1.0 |

Popup-era totals (Oct 25–Sep 26): 17,011 signups → 4,998 buyers (29.4%) → ≈$1.5M first-order
and ≈$2.1M total net revenue from Alia-tagged customers; ≈$120 net / ≈$65 contribution per signup.

**Insights**
1. **Conversion is not the problem and never was.** Submit-among-viewers (~5%) and signup→buyer
   (~30%) have not moved in twelve months, across sale and non-sale months, cheap and expensive
   traffic. *High.*
2. **Reach is the broken link.** The share of sessions that see the popup fell from ~70% to 23%
   as paid social scaled — the paid visitor bounces before the trigger fires. At today's traffic
   that is ~1,900 signups, ~550 buyers and ~$170k first-order revenue a month left on the table.
   *High (measured, 9 months).*
3. **Emails monetise immediately, not at the sale.** ~85% of a cohort's lifetime conversion
   happens in month one via the welcome flow; pre-sale signups who haven't bought convert only
   4–7% during a sale. Capture is a now-revenue lever, and the reason to keep it running to BFCM
   is compounding, not a launch-day payload. *High.*
4. **In-sale capture is a different problem: the popup is seen but ignored.** June (EOFY) reach
   was 53% but submit collapsed to 2.3% — a discount popup on top of a sale has no offer.
   In-sale signups still convert 28–39% when they do submit. *High on numbers; Medium on cause.*
5. **Email-captured customers are the better customers**: 35% conversion for grease-intent
   signups (vs 28% covers), higher repeat than store average (Oct cohort 23.5% with 2+ orders),
   and they are the base of the only repeat lever (grease, RP-003). *High.*
6. **Value ceiling for an incremental email ≈ $65 contribution**, before any incrementality
   haircut (no holdout has ever run). RP-001's $90–115 "cost per signup" is a blended ratio, not
   a price. *Medium.*

**Recommendations, in order**
1. **Restore reach on paid traffic before spending on more traffic.** Audit Alia trigger rules
   (delay, scroll depth, exit-intent, session-count caps) and page targeting on the paid
   destinations (`/pages/*`, PRO Mat and grease PDPs); confirm the popup fires there. Target ≥50%
   reach by mid-October; track weekly with one Alia call (`popupViewsCount` ÷ Shopify sessions).
2. **Keep the welcome offer as the engine** and test its variants on *buyers*, not submits: the
   free-shipping-over-$399 tag reads 36.8% vs 31.6% control — worth a clean Alia A/B.
3. **Pre-BFCM capture plan:** continuous capture Oct–mid-Nov (cheapest emails, RP-001); the
   pre-launch sale LP as a first-access capture page (RP-005); a sale-specific popup during the
   sale (early-access / bonus-gift, not a discount) so submit doesn't collapse to 2%.
4. **Segment the welcome flow by the popup's interest answer** (grease-intent → grease
   offer + reorder cadence; covers → machine-fit guide). Highest-converting cohort, cheapest win.
5. **Don't buy list growth via giveaways (RP-002) or in December** (weakest cohort, 21.7%).
6. **Run a one-month popup holdout pre-BFCM** to price incrementality once.
7. **Scorecard rows (monthly):** popup reach %, submit-among-viewers %, 30-day signup→buyer %.

### Caveats
- Shopify signup counts ≈ Klaviyo +8%; conversion on the Klaviyo denominator would read ~32%.
- No popup holdout exists, so "30% convert" ≠ "30% incremental"; some would have bought anyway.
- "Bought during sale" uses last-order-date; true in-sale purchase share is slightly higher.
- Revenue per signup blends cohorts of different ages (window Aug 25–Sep 26).

### Linked artifacts
- RP-001 (capture and cost per signup), RP-002 (giveaway entrants 3–4%), RP-005 (pre-launch LP
  capture), `research/BFCM-2026-REPORT-INPUTS.md`.

### Open questions / next
- Run a true popup holdout (Alia supports it) for one month pre-BFCM to measure incrementality.
- Finish the Alia reach series (popupViewsCount Oct 25–Sep 26, usersCount Apr–Sep 26) with monthly
  one-stat calls spaced across a day; then split views by device/path via `/events/distributions`.
- Re-cut Dec 2025 cohort by source once RP-001's segmented pull exists.
- Add "signup → buyer 30-day %" as a monthly scorecard row (segment count, 1 query).

---

## Template (copy for a new research project)
```
## RP-00X — <title>
**Status:** Open · **Owner:** · **Last updated:** <date>
**Question:** <what we're trying to learn>

### Data sources
### Findings
### Caveats
### Linked artifacts
### Open questions / next
```

## RP-007 · Reach and Media Report, last 12 months vs previous 12 (2026-09-23)
**Question:** media reach, video views, spend, grease growth and email-list growth, 23 Sep 2025 to 22 Sep 2026 against the year before.
**Deliverables:** `deliverables/reach-media-report-2026-09-23/` (report page, workbook, source JSON and monthly email counts). Report artifact published from the page.
**Verified here:** Meta spend $791,220 to $1,472,929 (+86%); impressions 64.5M to 126.8M (+97%); link clicks 601,561 to 1,657,607 (+176%); attributed purchases 6,464 to 13,855; CPM $12.26 to $11.61; CTR 0.93% to 1.31%; CPC $1.32 to $0.89; AU spend +116%, international −29%. Grease net sales $1,515,282 to $2,184,885 (+44%), orders 8,988 to 15,396 (+71%); coupler orders 3.4x; grease-gun sales −13%. Covers (titles containing Cover or Enclosure, GWP rows excluded) net sales $1,135,969 to $1,402,610 (+23%), orders 3,111 to 4,462 (+43%); Draw Bar Cover orders 79 to 865; every cover line up. Machine operators (distinct orders containing grease or a cover) 7,559 to 13,359 (+77%), net sales $2.65M to $3.59M (+35%), 75% of store net sales. Australian orders by billing state 7,307 to 16,495 (+126%); every state grew, NT +241%, SA +157%, WA +154%, VIC slowest +113%. Monthly Meta spend: average $66k to $121k, peak $198k Jun 2026, nine months over $100k. Klaviyo list size 18,618 to 44,804 (+141%; 10,948 profiles predate Oct 2024); new profiles 7,670 to 26,186 (+241%); Alia popup 680 to 15,317; popup share 9% to 58%.
**From the same-day Ads Manager pull (not re-run here; spend and impressions match to the dollar):** reach 3.01M to 6.77M; frequency 21.4 to 18.7; video plays 26.5M to 71.8M; ThruPlays 1.85M to 4.85M; watched 100% 307k to 1.10M; hook rate 41% to 57%.
**Gotchas:** the live `/api/campaigns` requests no reach or video fields; `dashboard/api-reach.js` adds them (deploy to diggerlid-mer, which is not in the Vercel account this workspace can see). KAJO pack items are counted per tube since Aug 2025, so grease unit counts are not comparable year on year. The `/api/emails` endpoint can drop a month on an SSL reset; re-run that month.
