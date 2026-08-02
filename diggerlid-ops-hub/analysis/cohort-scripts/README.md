# Cohort / retention analysis — reproducible scripts

Deterministic classifiers behind **Part 7** of `AUG-SEP-FINAL-REPORT.md` (retention by
first‑purchase category) and the grease→non‑grease cross‑sell finding.

## Data source
Customer order histories pulled live from the **Shopify Admin GraphQL API** (2 Aug 2026) with:

```graphql
customers(query:"customer_date:>=<lo> customer_date:<<hi> orders_count:>=1", sortKey:CREATED_AT){
  nodes{ id numberOfOrders
    orders(first:12, sortKey:CREATED_AT){ nodes{ createdAt
      lineItems(first:12){ nodes{ title originalTotalSet{shopMoney{amount}} } } } } } }
```

Raw page JSON is written to `pages/` (Aug–Oct 2025 cohort) and `pages_dec/` (Dec 2025–Feb 2026 cohort).
**Those raw pages are intentionally NOT committed** — they contain customer order data. Re‑pull them
into a local scratch dir to reproduce. The scripts here contain no customer data.

## Method
- **Category** is assigned by product‑title keyword (grease / covers / portable(mats) / accessory / merch),
  ignoring `$0` GWP gifts, Package Protection, return‑shipping and test lines.
- **First‑purchase category** = the highest‑value line in the earliest real order.
- **Repurchase** = ≥1 later real order. **Cross‑sell** = a later order in a different category.
  **High‑value repurchase** = a later order with any item >$100.
- CIs are **Wilson 95%**; group differences use a **two‑proportion z‑test**.

## Scripts
| File | Purpose |
|---|---|
| `categorize.py` | Aug–Oct cohort: repurchase / cross‑sell / HV cross‑sell by first‑purchase category |
| `augoct_metrics.py` | Aug–Oct cohort: repurchase / cross‑sell / HV‑repurchase (Part 7.1) |
| `dec_categorize.py` | Dec–Feb cohort: per‑category metrics (running check during the pull) |
| `final_compare.py` | Covers vs Mats, horizon‑matched (~8mo cap) + significance (Part 7.2) |

Run from the directory that contains `pages/` and `pages_dec/`: `python3 final_compare.py`.

## Headline results
- Retention ladder: **grease 27% ▸▸ covers 12–14% ▸ mats 2.6%**.
- Mats vs covers (8mo‑matched): repurchase 2.6% vs 12.0% (p=0.014); HV‑repurchase 2.6% vs 10.4% (p=0.030).
- Grease→(>$100 non‑grease) = 5.2% ±2pt (n=462) — not above a cover buyer's own repeat rate; sub‑types
  indistinguishable (coupler‑only 6.4% vs bundle 5.6%, p=0.78).
