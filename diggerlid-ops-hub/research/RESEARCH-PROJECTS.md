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
| RP-001 | Signup volume, cost & signup→conversion economics | Open | 2026-08-16 | Popup CAPTURE is stable (~5–6% of viewers); the *view rate* collapsed 61%→~20% — a visibility, not traffic-quality, problem. Conversion ~29% stable. |

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

### ⭐ UPDATE 2026-08-16 — TRUE view→submit rate (Alia API) corrects finding #4
Pulled Alia's `emailSignupRate` (submit ÷ popup **views**) via `/events/stats`. It reframes the whole story:

| Month | Proxy (signups ÷ sessions) | **TRUE (submit ÷ views)** | Implied **view rate** |
|---|--:|--:|--:|
| Apr | 3.81% | **6.27%** | ~61% |
| May | 1.94% | **6.01%** | ~32% |
| Jun | 1.12% | **2.93%** | ~38% |
| Jul | 1.16% | **5.17%** | ~22% |
| Aug* | 0.96% | **6.00%** | ~16% |
*partial. Alia aggregate (Apr–Aug) true rate ≈ **4.74%**.

- **The popup's capture rate is stable ~5–6% of viewers — it never collapsed.** Proxy = true_rate × view_rate.
- **What collapsed is the VIEW RATE: ~61% (Apr) → ~16–22% (Jul–Aug).** The popup stopped being *shown* to the paid surge.
- **Correction to finding #4:** paid visitors who see the popup submit normally (~5–6%). The problem is **popup visibility/targeting on paid traffic**, NOT traffic quality — a far more fixable lever (trigger timing, page/source targeting, frequency caps, bounces before the popup fires).
- **June exception:** decent view rate (~38%) but true submit dropped to 2.9% — EOFY sale shoppers saw it but didn't opt in.
- **Open question this answers:** the earlier "is it a popup problem or a traffic-intent problem?" → **popup visibility problem.** Next: pull Alia popup *view rate* by source/page to find where views are being lost.

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
