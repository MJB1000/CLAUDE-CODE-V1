# DiggerLid — August & September 2026 Profitability Plan
### Final report for commitment
Prepared 1 August 2026 · Head of Growth
Data: Shopify (live), Meta Graph API (live), EE models 2025 (v6.0) + 2026 (v7.1) — **all restated ex‑GST**

---

# PART 1 — The language, explained properly

Before any numbers, here is what every term means and exactly how it is calculated. If you only read one section, read this one — every decision in this report follows from these four formulas.

## 1.1 The order, from the customer's money to yours

When someone pays you $300, that money leaves in a specific order:

```
   $300.00   what the customer pays (incl GST)
 −  $27.28   GST (we never owned this)
 ─────────
   $272.72   REVENUE EX-GST  ← everything below is measured against this
 −  $93.30   product cost      (34.21% — what the goods cost us)
 −  $24.00   shipping          (FLAT — same whether the order is $50 or $500)
 −   $6.25   merchant fees     (2.29%)
 −   $1.50   packaging         (FLAT)
 −   $0.30   transaction fee   (FLAT)
 ─────────
   $147.37   CONTRIBUTION — what this order leaves behind before advertising
 −  $97.07   CPA (what we paid in ads to win this customer)
 ─────────
    $50.30   this order's contribution to GPAM
```

Then, once a month, **fixed costs of $74,831** arrive regardless of how many orders you took. You need enough of those $50.30 slices to cover it — about **1,488 orders a month at these economics** just to break even.

## 1.2 GPAM — Gross Profit After Marketing

**GPAM is what's left after you've paid to make the product and paid to sell it — but before rent, salaries and software.**

Two ways to write it. They give the same answer.

**As dollars:**
```
GPAM$ = Revenue − Variable Costs − Marketing Spend
```
July 2026: `$382,884 − $182,435 − $160,554 = $39,895`

**As a percentage:**
```
GPAM% = (1 − VCR) − MER
```
July 2026: `(1 − 47.65%) − 41.93% = 10.42%`

**Why the percentage version matters more:** it separates the two things you control. VCR is how efficiently you *serve* a customer; MER is how efficiently you *buy* one.

**Then:**
```
NET PROFIT = GPAM$ − Fixed Costs
```
July 2026: `$39,895 − $74,831 = −$34,936`

> **The single most useful number in this report:** your fixed costs are **19.5% of revenue**. So **GPAM% must exceed 19.5% to make any profit at all.** July delivered 10.4%. The 26% target isn't arbitrary — it's break‑even (19.5%) plus a real margin.

## 1.3 VCR — Variable Cost Ratio

**The share of each revenue dollar spent making and shipping that specific order.**

```
VCR = Variable Costs ÷ Revenue ex-GST
```
July 2026: `$182,435 ÷ $382,884 = 47.65%`

**The critical nuance:** $25.80 of every order (shipping $24.00 + packaging $1.50 + transaction $0.30) is **flat — it does not change with order size.** So:

| AOV | Flat cost as % | VCR |
|--:|--:|--:|
| $251 (July) | 11.1% | 47.65% |
| $285 | 9.8% | 46.34% |
| $300 | 9.3% | 45.84% |
| $315 | 8.9% | 45.40% |

**Bigger baskets automatically lower VCR.** This is why AOV is a margin lever, not just a revenue lever.

## 1.4 MER — Marketing Efficiency Ratio

**What share of your sales revenue goes back out to Meta.**

```
MER = Ad Spend ÷ Revenue ex-GST
```
July 2026: `$160,554 ÷ $382,884 = 41.93%`

You may be used to seeing this as a **ratio** — they're the same number flipped:

```
Ratio (ROAS) = 1 ÷ MER
```
July 2026: `1 ÷ 41.93% = 2.38×` — every $1 of ads returned $2.38 of revenue.

| MER % | Ratio | $1 of ads returns |
|--:|--:|--:|
| 25% | 4.00× | $4.00 |
| **28%** ← target | **3.57×** | $3.57 |
| 33% | 3.00× | $3.00 |
| **41.9%** ← July | **2.38×** | $2.38 |

**And the version that drives every decision in this report:**

```
MER = CPA ÷ AOV(ex-GST)
```

**MER is not really about ad spend. It is the ratio of what a customer costs to what a customer spends.** You can improve it by paying less (CPA) or selling more per order (AOV). Nothing else moves it.

## 1.5 The master equation

Substituting, everything collapses to:

```
GPAM% = (1 − VCR) − CPA ÷ AOV
```

**This is why CVR is not a margin lever.** More visitors converting at the same basket and the same acquisition cost gives you the *same* GPAM% — just more of it. **CVR multiplies the dollars; AOV and CPA change the percentage.**

---

# PART 2 — Where we actually are

## 2.1 Overall performance: July 2026 vs PCP and May 2026

| Metric | **Jul 2025 (PCP)** | **May 2026** | **Jul 2026** | vs PCP | vs May |
|---|--:|--:|--:|--:|--:|
| Net sales | $251,726 | $400,329 | **$366,852** | **+45.7%** | −8.4% |
| Revenue ex‑GST | $259,812 | $416,322 | $382,884 | +47.4% | −8.0% |
| Orders | 699 | 1,551 | **1,654** | **+136.6%** | +6.6% |
| Sessions | 25,636 | 76,386 | **116,420** | **+354.2%** | +52.4% |
| **AOV** | **$395.67** | $291.67 | **$251.54** | **−36.4%** | −13.8% |
| CVR (orders/sessions) | 2.73% | 2.03% | **1.42%** | −48.0% | −30.0% |
| CPA | $132.14 | $79.24 | **$97.07** | **−26.5%** ✅ | +22.5% |
| **Revenue per session** | **$9.82** | $5.24 | **$3.15** | **−67.9%** | −39.9% |

**The one-sentence version:** we are buying **4.5× the traffic** to make **1.46× the revenue**.

## 2.2 Product mix — the actual root cause

| Category | **Jul 2025** | **May 2026** | **Jul 2026** | Shift vs PCP |
|---|--:|--:|--:|--:|
| GREASE – tubes | 31.9% | 40.8% | 33.3% | +1.5pt |
| GREASE – hardware | 16.0% | 17.0% | 15.0% | −0.9pt |
| **COVERS** | **49.2%** | 27.6% | **24.3%** | **−24.9pt** ⚠️ |
| **PORTABLE (mats/hauler)** | **0.0%** | 11.6% | **23.3%** | **+23.3pt** |
| ACCESSORIES | 3.0% | 3.0% | 4.1% | +1.1pt |

**Price per item, July 2026:** Covers **$250.01** · Portable **$186.27** · Grease hardware **$39.06** · Grease tubes **$14.13**

### What actually happened to AOV — corrected with the full 13‑month history

A Jul‑2025‑vs‑Jul‑2026 snapshot *looks* like covers collapsed (Pro Enclosure 112 → 75, −33%). **When you plot all 13 months, that is a mirage.** Cover units are flat around a stable baseline — July 2025 was simply an unusually strong month and July 2026 is a normal one.

**Pro Excavator Enclosure — the $649–725 hero — BAU months (sale months excluded):**

| Jul25 | Aug | Sep | Oct | Dec | Jan | Feb | Mar | Apr | May | Jul26 |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **112** | 84 | 59 | 97 | 82 | 59 | 71 | 73 | 48 | 87 | **75** |

Mean of the BAU months ≈ **77 units**. Jul 2025 (112) was the outlier high; Jul 2026 (75) sits right on the baseline. It wobbles between ~48 and ~97 with **no downward trend**. The low‑volume SKUs ("Skid Steer to zero", "Mini Loader −76%") are just noise — Skid Steer sells ~5/month and did 24 in June; Mini Loader did 76 in June.

**So what diluted AOV was not covers leaving — it was cheap new volume arriving on top of a flat cover business:**

| Line | Jul 25 units | Jul 26 units |
|---|--:|--:|
| Hero enclosures | 213 | 129 *(≈ baseline)* |
| **PRO Mat** ($219) | **0** | **407** |
| **Quick Release Coupler** ($29) | 179 | **976** |

> **The AOV collapse is mix dilution, not cover decline.** PRO Mat went 0 → 407/month and couplers 179 → 976 — roughly **1,100 sub‑$220 units a year ago didn't exist**. They pulled the average basket down. Grease's *share* is unchanged (47.8% → 48.3%); the enclosure business is *flat*. Nothing structural broke — the product range simply added two big low‑price lines and never bundled anything onto them.
>
> **That is the AOV story, corrected. It matters because the fix is not "sell more covers" (Plan A, fighting a flat baseline) — it is "attach a second item to the cheap orders you're already winning" (Plan C, fixing dilution at its source).**

---

# PART 3 — The 80/20: what actually moves GPAM and fixed costs

## 3.1 The GPAM bridge — July 2025 → July 2026

This is the most important table in the report.

| | GPAM$ |
|---|--:|
| **GPAM$ July 2025** | **$24,059** *(9.26% of $259,812)* |
| **+ Revenue growth** (+47.4% at old margin) | **+$11,396** |
| **+ VCR improvement** (55.2% → 47.6%) | **+$28,869** ← biggest positive |
| **− MER worsening** (35.5% → 41.9%) | **−$24,428** ← biggest negative |
| **= GPAM$ July 2026** | **$39,897** *(10.42%)* |

### The top 3 movements in GPAM

1. **VCR improvement: +$28,869.** Variable costs fell 7.5 points. This is the biggest single positive movement in the business year-on-year, and nobody has been talking about it. Operations delivered.
2. **MER worsening: −$24,428.** Advertising efficiency fell 6.4 points. This more than consumed the operational win.
3. **Revenue growth: +$11,396.** Growing the top line at the old margin added real dollars — but it's the *smallest* of the three effects.

> **GPAM$ actually IMPROVED by $15,838 year-on-year.**

### So why did profit fall?

| | |
|---|--:|
| GPAM$ change | **+$15,838** |
| Fixed cost change | **−$25,489** |
| **Net profit change** | **−$9,651** |

Profit went from −$25,283 to −$34,934.

> **The trading engine got better. The cost base outgrew it.** This reframes the whole problem: it is not only a marketing failure. Fixed costs rose 51.7% while GPAM$ rose 66% off a very small base — and in absolute dollars the cost base won.

## 3.2 Why MER worsened even though CPA improved

`MER = CPA ÷ AOV`

| | CPA | AOV (ex‑GST) | MER |
|---|--:|--:|--:|
| Jul 2025 | $132.14 | $364.13 | 36.29% |
| Jul 2026 | $97.07 | $231.49 | **41.93%** |

**Decomposition:**

| Effect | Impact on MER |
|---|--:|
| CPA improving $132.14 → $97.07 | **−9.63pt** ✅ |
| AOV falling $364.13 → $231.49 | **+15.27pt** ❌ |
| **Net** | **+5.64pt** |

> **The media team improved CPA by 26.5% and still lost, because AOV fell 36.4%. AOV moved roughly 1.6× harder than CPA did.**
>
> This is the single strongest argument for making AOV the primary lever: **you already proved you can move CPA, and it wasn't enough.**

## 3.3 The 80/20 on fixed costs

| Line | Jul 2026 | % of fixed | vs PCP | Change |
|---|--:|--:|--:|--:|
| **Salaries & Contractors** | **$49,594** | **76.1%** | $36,530 | **+35.8%** |
| **Office & Operating** | $14,272 | 21.9% | $11,309 | +26.2% |
| Subscriptions & Software | $1,309 | 2.0% | $1,503 | −12.9% |
| **TOTAL** | **$65,175** *(27d)* | 100% | $49,342 | **+32.1%** |

*Full-month equivalent: $74,831 vs $49,342 PCP = **+51.7%***

**The 80/20:**
- **Salaries are 76% of fixed costs and drove 83% of the entire increase.**
- **Salaries + Office = 98% of the base.** Software is a rounding error — cutting subscriptions is theatre.
- **Every $1,000/month of fixed cost requires 0.26 percentage points of GPAM to cover.** So the $25,489 increase raised your break-even GPAM by **6.7 points** — from ~12.8% to 19.5%.

> **Put bluntly: the fixed-cost increase alone moved the break-even bar by 6.7 points of GPAM. That is larger than any single marketing lever in this report.** It is not in scope for August, but it is the quietest and largest profitability lever in the business.

## 3.4 The 80/20 on variable costs

| Line | Jul 2026 | % of variable | % of revenue |
|---|--:|--:|--:|
| **Product cost** | $114,766 | **72.3%** | 34.21% |
| **Shipping** | $33,840 | **21.3%** | 10.09% |
| Merchant fees | $7,692 | 4.8% | 2.29% |
| Packaging | $2,115 | 1.3% | 0.63% |
| Transaction fees | $423 | 0.3% | 0.13% |

**Product cost + shipping = 94% of all variable cost.**

**And the structural insight:** shipping is **$24.00 flat per order**. It does not scale with order value. So at $251 AOV it's 10.1% of revenue; at $315 AOV it's 8.3%. **Raising AOV cuts VCR automatically without renegotiating a single supplier contract.**

---

# PART 4 — The four plans, in detail

**Baseline:** July carried into August = 1,676 orders, AOV $251.54, CPA $97.07, GPAM 10.4%, **net −$34,405**, ~1,284 new customers/month.
**Targets:** August **+$20,000** · September **+$40,000** · audience must grow into BFCM.

---

## PLAN A — MIX-ONLY

### The simple version
> **Shift the product mix from mats back to covers. Change nothing else.**
> Sell more Pro Excavator Enclosures and 1.7T Covers ($582–$699) instead of leaning on PRO Mats ($219).

### What has to change

| Lever | From | To | Change |
|---|--:|--:|--:|
| **AOV** | $251.54 | **$308** | **+22.4%** |
| CVR | 1.42% | 1.42% | unchanged |
| CPA | $97.07 | $97.07 | unchanged |

**In practical terms:** cover revenue share must go from 24.3% back toward ~40%. That means roughly **+50 cover units per month** — reversing the −33% enclosure decline.

### The numbers

| | August | September |
|---|--:|--:|
| Orders | 1,676 | 2,012 |
| Revenue ex‑GST | $475,167 | $572,000 |
| Ad spend | **$162,650** ($5,247/day) | $162,650 |
| MER / ROAS | 34.2% / 3.17× | 29.3% / 3.42× |
| **GPAM%** | **20.2%** | 22.2% |
| **NET PROFIT** | **+$20,881** | **+$51,094** |
| New customers | 1,284 (flat) | 1,540 |

**Two-month total: +$71,975**

### Impact and risk
- ✅ **Simplest to run** — one owner, one metric, no media or site changes.
- ❌ **Biggest single ask of the four** (+22.4% AOV in one month).
- ❌ **Covers are flat, not declining — so there is no rebound to ride.** To lift AOV to $308 you must *grow* enclosure demand above a stable ~130/month baseline, which is a genuine marketing lift, not a recovery. Nothing pulls covers up on their own.
- ❌ **Audience flat.** You enter BFCM with no more customers than today.

---

## PLAN B — MIX + EFFICIENCY

### The simple version
> **Shift some mix back to covers, AND pay less per customer.**
> A smaller mix change than Plan A, paid for by tightening media.

### What has to change

| Lever | From | To | Change |
|---|--:|--:|--:|
| **AOV** | $251.54 | **$290** | **+15.3%** |
| CVR | 1.42% | 1.42% | unchanged |
| **CPA** | $97.07 | **$87.00** | **−10.4%** |

### The numbers

| | August | September |
|---|--:|--:|
| Orders | 1,676 | 2,012 |
| Ad spend | **$145,777** ($4,702/day) | $138,500 |
| MER / ROAS | **32.6% / 3.33×** | 26.7% / 3.74× |
| **GPAM%** | **21.2%** ← best | **24.8%** ← best |
| **NET PROFIT** | **+$20,129** | **+$58,511** |
| New customers | 1,284 (flat) | 1,540 |

**Two-month total: +$78,639**

### Impact and risk
- ✅ **Lowest spend of all four** — $145,777, **$17k below July**. Best cash profile.
- ✅ **Best margin** (21.2% GPAM, 32.6% MER). Closest to the 26% goal.
- ✅ CPA $87 is well above June's proven $62.15 — a modest ask.
- ❌ **Audience flat.** Same BFCM problem as Plan A.

---

## PLAN C — ATTACH + EFFICIENCY ★ RECOMMENDED

### The simple version
> **Stop selling one thing at a time. Bundle a second product onto every order — and pay a little less per customer.**
> Instead of raising prices or reversing the cover decline, sell *two* items where you currently sell one.

### What has to change

| Lever | From | To | Change |
|---|--:|--:|--:|
| **AOV** | $251.54 | **$283** | **+12.5%** ← smallest ask |
| **CVR** | 1.42% | **1.55%** | +9.2% |
| **CPA** | $97.07 | **$87.50** | −9.9% |

### Why the AOV ask is the smallest
The evidence from 233 July orders:

| | Orders | AOV |
|---|--:|--:|
| Single-SKU orders | **161 (69%)** | $250.85 |
| Multi-SKU orders | 72 (31%) | $379.82 |

> **Attaching one more product is worth +$128.98 (+51%).** You do not need to sell more expensive things — you need to sell *two* things.

**The specific opportunity:**
- **PRO Mat sells alone 91% of the time** (51 of 56 orders). Your #2 revenue line has no cross-sell at all.
- **Digger Wipes, Hydraulic Cap Sets and Bottle Openers *never* sell alone** — 0% solo across the sample. They are proven attach items that are simply never offered alongside mats.
- **Coupler-only orders are 16.3% of all orders but 2.4% of revenue** — removing them from *paid acquisition* alone lifts AOV ~16.6%.

### The numbers

| | August | September |
|---|--:|--:|
| Orders | 1,829 | 2,266 |
| Revenue ex‑GST | $438,000 | $604,000 |
| Ad spend | $160,038 ($5,162/day) | $188,000 |
| MER / ROAS | 33.6% / 3.23× | 27.1% / 3.69× |
| **GPAM%** | **20.0%** | 24.1% |
| **NET PROFIT** | **+$20,426** | **+$69,167** ← best |
| **New customers** | **1,401 (+9%)** | **1,735 (+35%)** |

**Two-month total: +$89,592 — best of the four**
**New customers: 3,136 vs 2,824 for A/B — +11%**

### Impact and risk
- ✅ **Highest two-month profit** (+$89,592).
- ✅ **Only plan that meaningfully grows the BFCM audience** (+11% new customers).
- ✅ **Smallest AOV ask** ($283 vs $308 for Plan A) — because bundling lifts AOV and CVR together.
- ✅ Doesn't depend on reversing the cover decline.
- ❌ **Execution is untested** — you have never run a systematic attach programme.
- ❌ Requires site/offer work (bundles, post-add-to-cart offers) alongside media changes.

---

## PLAN D — BALANCED

### The simple version
> **Move all four levers a little, rather than any one of them a lot.**

### What has to change

| Lever | From | To | Change |
|---|--:|--:|--:|
| AOV | $251.54 | **$285** | +13.3% |
| CVR | 1.42% | **1.50%** | +5.6% |
| CPA | $97.07 | **$87.00** | −10.4% |

### The numbers

| | August | September |
|---|--:|--:|
| Ad spend | $153,990 ($4,967/day) | $161,000 |
| MER / ROAS | 33.2% / 3.28× | 27.6% / 3.62× |
| **GPAM%** | **20.5%** | 24.1% |
| **NET PROFIT** | **+$20,307** | **+$65,222** |
| New customers | 1,356 (+6%) | 1,681 (+31%) |

**Two-month total: +$85,528**

### Impact and risk
- ✅ **Lowest execution risk per lever** — nothing moves more than 13%.
- ✅ Grows audience 8%.
- ❌ **Four workstreams running at once** needs real coordination; no single owner.

---

## 4.5 Side by side

| Plan | Aug net | Sep net | **Aug+Sep** | Aug GPAM | Aug spend | New custs | Biggest ask |
|---|--:|--:|--:|--:|--:|--:|---|
| **A** MIX-ONLY | +$20,881 | +$51,094 | +$71,975 | 20.2% | $162,650 | flat | AOV +22.4% |
| **B** MIX + EFFICIENCY | +$20,129 | +$58,511 | +$78,639 | **21.2%** | **$145,777** | flat | AOV +15.3% |
| **C** ATTACH + EFF ★ | +$20,426 | **+$69,167** | **+$89,592** | 20.0% | $160,038 | **+11%** | attach execution |
| **D** BALANCED | +$20,307 | +$65,222 | +$85,528 | 20.5% | $153,990 | +8% | coordination |

## 4.6 Recommendation

**Run Plan C. Hold Plan B as the fallback.**

C wins on the two things that matter past August: **$89,592 over two months** and **the only meaningful BFCM audience growth (+11%)**. It also has the **smallest AOV ask** of the four, because bundling moves AOV and CVR at the same time.

**B is the fallback** if bundle execution slips by mid-August — it delivers $78,639 on **$17k less spend** and the best margin of the four, at the cost of a flat audience.

**Do not run A.** Largest AOV ask, depends on reversing a 12-month unit decline, and contributes nothing to BFCM.

### Decision gates

| Date | Check | If missed |
|---|---|---|
| **4 Aug** | Bundles live? Coupler-only paused in paid? | Plan hasn't started — escalate same day |
| **10 Aug** | AOV ≥ $270 | Switch to Plan B, cut spend cap to $146k |
| **10 Aug** | CPA ≤ $92 | Don't deploy the full spend cap |
| **20 Aug** | GPAM ≥ 18% | Reset September to a +$40k floor, not a target |

---

# PART 5 — Meta spend by campaign ⏳ PENDING

**Status: blocked on a deploy — needs ~2 minutes from you.**

The current `/api/mer` feed returns **total** Meta spend only. To attribute spend to product categories properly I need **campaign‑ and ad‑set‑level** data (ad set names typically carry the product).

Until then, the allocation in earlier analysis is **inferred from order share, not measured** — directionally useful, not decision-grade.

### To unblock

```bash
cd ~/diggerlid-mer && mkdir -p api
# save dashboard/api-mer-campaigns.js from the repo as api/campaigns.js
vercel --prod
curl -s "https://diggerlid-mer.vercel.app/api/campaigns?level=adset"
```

It uses the **same `META_TOKEN` / `META_ACCOUNT_ID`** already on that project — no new credentials.

**It returns per campaign / ad set:** spend, share of total, impressions, clicks, purchases, purchase value, derived CPA and ROAS — for July (`?since=2026-07-01&until=2026-07-31`) and August to date.

**Once deployed, this report gains:** true spend split by product category, real CPA per product line, and a measured (not inferred) reallocation recommendation.

---

# PART 6 — What still isn't answered

1. ~~Why are cover units down 33%?~~ **RESOLVED (this revision).** The 13‑month data shows covers are *flat*, not declining — the −33% was a base‑effect artefact of comparing a peak month to a normal one. The AOV fall is mix dilution by PRO Mat and couplers, not a cover problem. No further investigation needed; this *strengthens* the case for Plan C (fix dilution) over Plan A (grow a flat line).
2. **Actual product cost by category.** All GPAM maths uses the blended 34.21%. If covers and mats differ materially, every plan shifts.
3. **Fixed costs.** Up 51.7% vs PCP; salaries are 76% of the base and drove 83% of the increase. This raised break-even GPAM by 6.7 points — **larger than any marketing lever in this report.** Out of scope for August, but it belongs on the agenda.
4. **The coupler-only cohort.** Whether coupler-only buyers ever convert to non-grease is unresolved (n=4). ~500 more customers would settle it.
5. **Cash flow.** August spend $146k–163k lands before month-end revenue; BFCM will need ~$225k inside a 10-day window.

---

## Appendix — verification

- Shopify pulled live 1 Aug 2026. July final: $366,852 net · 1,654 orders · 116,420 sessions · AOV $221.82 (net‑sales basis) = **$251.54 model basis**.
- Meta spend live via `/api/mer`: July $160,554 (full-month run rate from $155,375 through 30 Jul).
- EE model P&L identity verified to the cent: `$335,474.95 − $362,033.32 = −$26,558.38`.
- **Both EE models display MER and VCR divided by GST-inclusive revenue, flattering both by ~9%, while their own P&L uses ex-GST. Every figure in this report is ex-GST.**
- Cohort: n=100 customers (43 grease-first). Order sample: n=233 across five July windows. Small-sample caveats stated inline.
- CVR is quoted on an **orders ÷ sessions** basis (1.42%). Shopify's own CVR (1.27%) counts completed-checkout *sessions* and is not the right denominator for order-count modelling.
