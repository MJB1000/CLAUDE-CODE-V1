---
title: DiggerLid — Cohort CLTV & Cross-Purchase Analysis
generated: 2026-08-17
window: 2025-05-01 .. 2026-08-17 (15 months)
basis: ex-GST (line price ÷ 1.10), AUD
source: Shopify native Orders export (3 files, line-item level, full history 2019→2026)
customer_key: md5(lowercased email) — no raw PII stored
status: analysis (research) — decision-grade
---

# DiggerLid — Cohort CLTV & Cross-Purchase Analysis

**Question:** For each product category we acquire a customer through, what is that customer
worth over 12 months (margin-weighted), and what do they buy next?

## Methodology

- **Data:** Shopify native Orders export, line-item level, full order history (2019→2026-08-17).
  In-window analysis scope = **2025-05-01 .. 2026-08-17**. The pre-window history is used only to
  classify customers as **new vs returning** (dates only).
- **Reconciliation:** File covers the **completed-orders** set (99.4% `paid`). It runs ~3.5% below
  a raw `ordersCount` because that count includes unpaid/voided/expired attempts we exclude anyway.
  Coverage of real paid orders is effectively complete.
- **Categorisation:** DiggerLid §4 rulebook (finalised 2026-08-17). Bundles **explode to component
  line items** (confirmed), so revenue sits in component categories; there is no separate "bundle" line.
- **Revenue basis:** ex-GST = (Lineitem price × qty − Lineitem discount) ÷ 1.10.
- **Contribution:** ex-GST revenue × per-category margin
  (Diggershield 80% · Hauler 68% · Excavator Covers 62% · Pro Enclosure 63% · Pro Mats 59% ·
  Accessories 50% · Grease 25%).
- **Entry category:** the **hero** (highest ex-GST revenue) category of a customer's **first in-window
  order**. Acquisition economics measured on **NEW customers only** (first-ever order falls in window).
- **12-month cohort:** new entrants with entry date ≤ 2025-08-17, so every customer has a full
  365 days observed. Subsequent purchases counted within 365 days of entry.
- **Customer key:** md5(lowercased email). 207 guest (blank-email) orders unlinkable (0.9%).

---

## 1. Revenue rollup by category (in-window, ex-GST — $5.61M over 15 months)

Contribution overlay included because the reordering is the story.

| Category | Revenue | Rev % | Contribution | Contr. % |
|---|--:|--:|--:|--:|
| **Grease** (Packs+Adaptors+Guns+Coupler) | $2,638k | **47.0%** | $660k @25% | 26.1% |
| **Pro Enclosure** | $1,089k | 19.4% | **$686k @63%** | **27.1%** |
| **Excavator Covers** (Std+Draw Bar) | $803k | 14.3% | $498k @62% | 19.7% |
| **Pro Mats** | $617k | 11.0% | $364k @59% | 14.4% |
| **Diggershield** (Kits+Screens) | $278k | 4.9% | $222k @80% | 8.8% |
| **Accessories** | $153k | 2.7% | $77k @50% | 3.0% |
| **Hauler** | $31k | 0.6% | $21k @68% | 0.8% |
| Uncategorised | $3k | 0.1% | — | — |
| **Total** | **$5,612k** | | **~$2,527k** | **45% blended** |

### Subcategory detail

| Category / Sub | ex-GST revenue | Share |
|---|--:|--:|
| Grease / Packs | $1,891,598 | 33.7% |
| Pro Enclosure | $1,088,545 | 19.4% |
| Excavator Covers / Standard | $686,253 | 12.2% |
| Pro Mats | $617,065 | 11.0% |
| Grease / Adaptors | $391,338 | 7.0% |
| Diggershield / Full Kits | $251,391 | 4.5% |
| Grease / Guns | $189,424 | 3.4% |
| Grease / Coupler | $166,129 | 3.0% |
| Accessories | $153,222 | 2.7% |
| Excavator Covers / Draw Bar | $116,295 | 2.1% |
| Hauler | $31,390 | 0.6% |
| Diggershield / Rear Screens | $26,245 | 0.5% |
| Uncategorised | $3,175 | 0.1% |

---

## 2. Customer base: new vs returning (in-window entrants, linked)

| Segment | Customers | Share |
|---|--:|--:|
| **New** (first-ever order in window) | 14,478 | **89%** |
| **Returning** (had pre-window orders) | 1,701 | 11% |
| **Total in-window entrants** | 16,179 | 100% |

**DiggerLid is overwhelmingly acquisition-driven — only 11% of buyers are returning.**

---

## 3. 12-month contribution per acquisition (NEW customers, mature cohort N=2,182)

Mature cohort = entered May–Aug 2025 (full 12 months observed).

| Entry category | New custs | Repeat % | Subseq orders/cust | Entry $contrib | Subseq $contrib | **Total 12-mo $contrib/acq** | Entry $rev | Subseq $rev |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| **Diggershield** | 52 | 14% | 0.15 | $1,027 | $36 | **$1,063** | $1,334 | $67 |
| **Pro Enclosure** | 415 | 11% | 0.14 | $385 | $24 | **$409** | $626 | $50 |
| **Excavator Covers** | 445 | 15% | 0.18 | $174 | $19 | **$193** | $289 | $41 |
| **Grease** | 1,138 | **25%** | **0.35** | $82 | $36 | **$118** | $321 | $106 |
| **Accessories** | 132 | 17% | 0.20 | $31 | $36 | **$67** | $63 | $57 |
| **Blended** | 2,182 | | | $178 | $30 | **$208** | | |

**New-product lines (shorter horizon — not comparable to the 12-mo figures above):**

| Entry category | Note | New custs | Repeat % | Total $contrib/acq |
|---|---|--:|--:|--:|
| *Pro Mats* | launched 25 Aug 2025 · 6-month read | 853 | 4% | *$139* |
| *Hauler* | launched Jan 2026 · ~40 customers total | — | — | *insufficient data* |

> N.B. Diggershield (N=52) and Accessories (N=132) are small-N — treat as directional.

---

## 4. Cross-purchase attach matrix (12-month, NEW mature cohort)

Row = entry category. Cell = % of those customers who bought the column category in a
**subsequent** order within 12 months.

| entry ↓ / then → | Grease | Pro Encl | Exc Covers | Pro Mats | Diggershld | Access. | Hauler |
|---|--:|--:|--:|--:|--:|--:|--:|
| **Grease** | **21%** | 1% | 3% | 1% | 0% | 4% | 0% |
| **Pro Enclosure** | 6% | **3%** | 3% | 1% | 0% | 3% | 0% |
| **Excavator Covers** | 8% | 1% | **6%** | 0% | 0% | 5% | 0% |
| **Diggershield** | 8% | 0% | 6% | 0% | **2%** | 4% | 0% |
| **Accessories** | 5% | 1% | 5% | 1% | 2% | **9%** | 1% |
| *Pro Mats* | — | — | — | — | — | — | — |
| *Hauler* | — | — | — | — | — | — | — |

*(Pro Mats/Hauler have no 12-month cohort — see Appendix A for a 6-month matrix that includes them.)*

---

## 5. Findings (empirical)

1. **Grease is 52% of new acquisitions but the lowest value per customer ($118).** Best repeat
   (25%) and most re-orders (0.35/cust), but 25% margin + weak cross-sell caps it. **Grease buyers
   rebuy Grease (21%) and ladder into high-margin lines almost never (Grease→Pro Enclosure 1%).**
   It is a self-contained low-value loop, not an on-ramp.
2. **A Diggershield acquisition is worth ~9× a Grease one; Pro Enclosure ~3.5×.** Yet Grease
   dominates acquisition volume. **CAC tolerance should differ wildly by entry category** — a
   blended-CAC/MER view hides this entirely.
3. **The 12-month LTV is basically the first order.** Blended subsequent contribution is $30 of the
   $208 total (~14%). Little repeat annuity — **growth math must work on first-order economics.**
4. **Cross-sell is diagonal-dominant and weak.** Customers rebuy their entry category; the only
   consistent cross-flow is into low-value Accessories. **Nothing meaningfully feeds the high-margin
   enclosure/Diggershield lines** — the biggest untapped lever is laddering that doesn't yet exist.

## 6. Caveats

- Refunds not netted (185 refunded/partially-refunded orders, ~0.6% — immaterial).
- Diggershield/Accessories small-N; Pro Mats/Hauler shorter-horizon or too new.
- Returning-customer value not modelled (this is acquisition economics).
- Guest (blank-email) orders (207, 0.9%) can't be linked and are excluded from the cohort.
- Contribution margins are the standard per-category assumptions supplied by the business.

## 7. Recommended next step

**CAC-by-entry-category:** overlay Meta spend against these per-acquisition values to find which
entry products DiggerLid over/under-pays to acquire. High-value low-volume lines (Pro Enclosure,
Diggershield) can likely justify far higher CAC than the blended target implies; Grease's blended
CAC should be judged against $118, not the portfolio average.

---

## Appendix A — 6-month cohort (includes Pro Mats/Hauler, N=7,104)

Shorter horizon → lower subsequent contribution; **not comparable** to the 12-month table.

| Entry category | New custs | Repeat % | Subseq orders/cust | Entry $contrib | Subseq $contrib | Total 6-mo $contrib/acq |
|---|--:|--:|--:|--:|--:|--:|
| Diggershield | 114 | 7% | 0.08 | $1,070 | $32 | $1,101 |
| Pro Enclosure | 1,030 | 7% | 0.08 | $415 | $13 | $428 |
| Excavator Covers | 1,283 | 8% | 0.09 | $164 | $10 | $175 |
| Pro Mats | 853 | 4% | 0.04 | $135 | $5 | $139 |
| Grease | 3,126 | 16% | 0.19 | $77 | $17 | $94 |
| Accessories | 696 | 10% | 0.13 | $28 | $16 | $44 |
| Hauler | 2 | (N too small) | — | — | — | — |
| Blended | 7,104 | | | $160 | $14 | $174 |

### 6-month cross-purchase matrix

| entry ↓ / then → | Grease | Pro Encl | Exc Covers | Pro Mats | Diggershld | Access. | Hauler |
|---|--:|--:|--:|--:|--:|--:|--:|
| Grease | 14% | 0% | 2% | 1% | 0% | 2% | 0% |
| Pro Enclosure | 3% | 2% | 1% | 0% | 0% | 2% | 0% |
| Excavator Covers | 3% | 0% | 4% | 0% | 0% | 2% | 0% |
| Pro Mats | 1% | 0% | 1% | 2% | 0% | 1% | 0% |
| Diggershield | 4% | 0% | 2% | 0% | 3% | 2% | 0% |
| Accessories | 2% | 1% | 3% | 1% | 1% | 6% | 0% |

## Appendix B — Machine-readable data files

Aggregate CSVs (no PII), generated alongside this report:

- `cohort_summary.csv` — per-entry-category 12-month CLTV (columns: entry_category, new_customers,
  repeat_pct, subseq_orders_per_cust, entry_contrib_per_cust, subseq_contrib_per_cust,
  total_12mo_contrib_per_acq, entry_rev_per_cust, subseq_rev_per_cust).
- `cross_purchase_matrix.csv` — 12-month attach-rate matrix (entry_category, new_customers,
  attach_<category> …).
