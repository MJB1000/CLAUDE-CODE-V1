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
