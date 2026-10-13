# QLD PRO Mat buyers by likely business type (13 Oct 2026)

**Scope:** all 639 QLD PRO Mat orders, 1 Mar to 13 Oct 2026 (ShopifyQL, `product_title CONTAINS 'PRO Mat'`,
shipping region Queensland). Full coverage, built from aggregates only: orders grouped by
`customer_email_domain` and by `billing_company` / `shipping_company`. No individual emails were pulled.
Business names stay in the scratchpad. This file holds counts only (`business_types_qld.json`).

## Method
1. **Email domain.** 547 orders (86%) use standard personal domains (gmail, hotmail, bigpond, outlook,
   live, icloud, yahoo, ISPs). The other 92 orders use a business or organisation domain.
2. **Shopify Company field.** 103 orders have one. 65 of those are on a personal email, so they add
   businesses the domain pass misses.
3. **Type inferred from the business name or domain only.** A web lookup of the names was blocked as
   data leaving the store, so 37 orders with opaque names stay "unclear".
Domain and company matches are deduplicated by name, so expect a small (±5) margin.

## Result

| | Orders | Share |
|---|---|---|
| Likely business buyers | **157** | **25%** |
| Personal, no business signal | 482 | 75% |

| Business type | Orders | Share of classified |
|---|---|---|
| Mechanical, diesel & automotive | 28 | 23% |
| Civil, earthmoving & plant hire | 24 | 20% |
| Other services (landscaping, IT, consulting, hospitality, tree work) | 17 | 14% |
| Farming, grazing & agriculture | 13 | 11% |
| Building, plumbing & electrical | 12 | 10% |
| Engineering, fabrication & industrial | 11 | 9% |
| Government, education & corporate | 7 | 6% |
| Transport & haulage | 5 | 4% |
| Mining, resources & energy | 3 | 2% |
| Unclear from name | 37 | n/a |

**Basket size:** orders with a company name average about **1.9 mats**, against **1.2** for orders without
one. Several business orders bought 6 to 13 mats (fleet and workshop kit-outs).

## What it means (hypothesis, label as such)
- One in four QLD PRO Mat orders is likely a business. That is a floor: trade words in personal email
  addresses (e.g. a "civil" Gmail address) can't be seen in aggregates and aren't counted.
- **Diesel mechanics and workshops** plus **civil, earthmoving and plant hire** make up 43% of identified
  business buyers. Farming and grazing (cattle companies, stations, cropping) is next.
- Business buyers order bigger baskets. That supports a **multi-mat or fleet bundle** and a
  "kit out the crew / every service ute" angle.
- Meta: test interest audiences for diesel fitters, heavy-vehicle mechanics, plant hire and earthmoving
  owners, and graziers in regional QLD. Pair them with the multi-mat offer.

## Re-run
- Any state or date range: rerun the two ShopifyQL groupings (domain, company) and re-classify.
- Order-level classifier for a raw Shopify export (adds the trade-word-in-email tier): `business_types.py`.
