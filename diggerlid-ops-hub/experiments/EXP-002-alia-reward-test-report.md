# EXP-002 Report — Alia popup reward A/B/C/D test

**Tool:** Alia · **Campaign:** BAU (Latest) · **Window:** 28 Jul – 5 Aug 2026 (9 days)
**Test:** Mystery Discount vs $35 off vs 10% off vs No Reward · ~6,200 visitors/variant

## Variant naming (Alia's labels are misleading)
| Alia label | Actually is |
|---|---|
| "Control" | **Mystery Discount** (incumbent) |
| "$35 Off" | $35 flat off |
| "Control 10%" | **10% off** (a test variant — not a control) |
| "No offer" | No reward |

## Results (Δ vs Mystery Discount)
| Metric | Mystery (incumbent) | $35 off | 10% off | No reward |
|---|--:|--:|--:|--:|
| Visitors | 6,175 | 6,324 | 6,205 | 6,275 |
| Popup views | 2,632 | 2,666 | 2,558 | 2,604 |
| **Email submit rate** | **4.98%** | 3.90% (−22%) | 3.67% (−26%) | 1.65% (−67%) |
| Email submissions | 131 | 104 | 94 | 43 |
| Phone submit rate | 4.07% | 3.19% | 3.01% | 1.08% |
| Attributed sales (14d) | $7,531 | $5,877 (−22%) | **$11,124 (+48%)** | $2,185 (−71%) |
| Attributed sales / visitor | $1.22 | $0.93 | **$1.79 (+47%)** | $0.35 |
| Attributed CVR (14d) | 22.9% | 26.9% | **42.6% (+86%)** | 23.3% |
| Attributed AOV (14d) | $251 | $210 (−16%) | **$278 (+11%)** | $218 |
| Attributed orders (14d) | 30 | 28 | **40** | 10 |
| **Sitewide CVR (7d)** | **1.00%** | 1.03% | 1.02% | 0.78% (−22%) |
| Sitewide orders (7d) | 62 | 65 | 63 | 49 |
| Alia "prob. to win" | 87.0% | 12.9% | 0.09% | 0.00% |

## The paradox — two different "winners"
- **Capture winner: Mystery Discount.** Highest email submit rate (4.98%), 131 emails — ~39% more than 10%-off. This is why Alia's probability-to-win = 87% Mystery (Alia optimises on capture rate).
- **Revenue winner (as Alia's summary claims): 10% off.** +48% attributed sales, 42.6% conversion, +11% AOV.

They diverge because of a **quantity-vs-quality trade-off**: Mystery hooks curiosity → most signups but lower intent (22.9% buy); 10%-off attracts fewer but higher-intent buyers (42.6% buy) and its shallow % protects AOV.

## Statistical read
- **Email submit rate — SIGNIFICANT.** Mystery 4.98% vs 10%-off 3.67% over ~2,600 views each → z ≈ 2.3, p ≈ 0.02. Mystery genuinely captures more emails.
- **14-day attributed revenue — UNDERPOWERED.** The 10%-off "win" rests on **40 orders**; a few large orders swing the +48%.
- **Contradicted by the well-powered metric:** sitewide 7-day CVR is **tied (~1.0%)** across all three reward variants (62/65/63 orders); only *no reward* is clearly worse (0.78%). So the offer type barely moves total site conversion — the big attributed gap lives only in the small signup slice.

## Findings & certainty
| # | Finding | Certainty |
|---|---|---|
| 1 | Any reward >> no reward (submit 3.7–5% vs 1.65%; sitewide CVR 1.0% vs 0.78%) | **High** |
| 2 | Mystery Discount captures the most emails — best for list growth | **High** (p≈0.02) |
| 3 | Flat $35-off drags AOV down (−16%) — prefer % over $ | **Medium** |
| 4 | 10%-off drives *more revenue* (+48%) | **Low** — 40 orders, invisible sitewide; likely noise |

**Overall verdict:** On the metric with enough sample (email capture) **Mystery Discount wins**. The "10% off won" revenue headline is **not trustworthy** at this sample size. Alia over-claims on the thin 14-day slice.

## Recommendation for the next test
- **Decide the objective first.** If list growth (BFCM feed) → keep Mystery Discount, no re-test needed. If revenue-quality → re-test properly.
- **Re-run head-to-head: Mystery Discount vs 10% off only** (drop $35-off and No-reward — both clearly lose).
- **Pre-declare the primary metric** as 14-day attributed revenue per visitor (with submit rate secondary), so there's one unambiguous winner.
- **Power it:** run until **~150–200 attributed orders per variant** (≈4–6 weeks at this traffic), not 9 days / 40 orders.
- **Segment** new vs returning, and check margin (10%-off costs margin that Mystery's average discount may not).
- **Guardrail:** watch AOV and blended discount cost, not just top-line attributed sales.
