# QLD PRO Mat buyers by business type (final, 13 Oct 2026)

> **Final numbers (13 Oct, postcode-level recount): 173 of 639 orders (27%)**: 92 business domain, 60 company name on a personal email, 21 trade word. Mechanical 34, other services 34, civil 33, farming 23, building 16, engineering 15, govt/corporate 8, transport 6, mining 4. City business share 34% (Brisbane), 38% (Gold Coast); regional about 24%. Report page: `qld-business-buyers.html`. The tables below are the earlier name-matched pass (178) and are kept for the method.

**Headline: about 27% of QLD PRO Mat orders are likely businesses (173 of 639).** Diesel and
mechanical workshops, civil, earthmoving and plant hire, and farming make up just over half of them.
Business orders average about 1.9 mats against 1.2 for everyone else.

**Scope:** all 639 QLD PRO Mat orders, 1 Mar to 13 Oct 2026 (ShopifyQL, `product_title CONTAINS 'PRO Mat'`,
shipping region Queensland). Built entirely from aggregates. No individual emails or addresses were pulled,
and no names are stored here. Business names stay in the session scratchpad. Data: `business_types_qld.json`.

## How businesses were found (each tier only adds orders not already counted)

| Tier | Signal | Orders added |
|---|---|---|
| 1 | Business or organisation email domain (not gmail, hotmail, bigpond etc.) | 92 |
| 2 | Company name entered at checkout, on a generic email | 65 |
| 3 | Trade word in a generic email address, 33 words (civil, diesel, plumb, farm, hire...) | 15 |
| 4 | Expanded pass, 80+ more words: rural (cattle, station, downs), mechanical (motor, tyre, workshop), trades (paint, weld, solar), business inbox (info@, admin@, accounts@, pty, group) | 6 |
| | **Total likely businesses** | **178 (28%)** |

Tiers 3 and 4 use `customer_email CONTAINS '<word>'` limited to the 25 generic domains, so only counts come
back. Tier 4 excludes every tier 3 word, so nothing is double counted. Words that commonly appear in
surnames (hay, steel, glass, pool, ute) were left out on purpose.

**Generic emails with a business attached:** 86 of the 547 orders on gmail, hotmail, bigpond, outlook and
similar (16%) are businesses.

**Searched but not available:** web lookups of business names (blocked as customer data leaving the
store) and shipping address text such as "X Station" (not a field in ShopifyQL).

## Business type

| Business type | Clear from name | + Estimated | Total | Share |
|---|---|---|---|---|
| Mechanical, diesel & automotive | 33 | 3 | **36** | 20% |
| Other services (landscaping, IT, consulting, hospitality, security, sole traders) | 20 | 16 | **36** | 20% |
| Civil, earthmoving & plant hire | 31 | 2 | **33** | 19% |
| Farming, grazing & agriculture | 15 | 8 | **23** | 13% |
| Building, plumbing & electrical | 16 | 1 | **17** | 10% |
| Engineering, fabrication & industrial | 11 | 4 | **15** | 8% |
| Government, education & corporate | 7 | 1 | **8** | 4% |
| Transport & haulage | 5 | 1 | **6** | 3% |
| Mining, resources & energy | 3 | 1 | **4** | 2% |
| **Total** | 141 | 37 | **178** | 100% |

**Estimated** = 37 names too opaque to classify confidently, guessed from the name pattern alone (low confidence):
- Initials or couple-name partnerships, holdings, creeks and gates were read as farming (8).
- "Fits" or custom names were read as mechanical (3), and group or site names as civil (2).
- Tech-style names were read as engineering (4).
- Personal-name domains and generic "enterprises" names went to other services (16).

Tiers 3 and 4 carry the most uncertainty: a word match is a strong hint, not proof. Domain and company
matches were deduplicated by name, so allow about ±5 on the type counts.

## What it means (hypotheses, small N per type)
1. **28% is a floor.** Sole traders who use a plain name address on Gmail look identical to personal
   buyers. The real business share is likely around 30% or more.
2. **The core trades are diesel and mechanical workshops plus civil, earthmoving and plant hire**: 39% of
   business buyers (45% of those classified clearly). Farming and grazing is third at 13%, and higher once the
   estimates are included. This matches the regional QLD hot spots (Darling Downs, Central Highlands, Mackay).
3. **Business buyers buy bigger baskets.** About 1.9 mats per order with a company name against 1.2 without.
   Several workshop and fleet orders took 6 to 13 mats.
4. **Most businesses buy like consumers.** 86 of the 178 (48%) checked out with a generic email, so B2B
   accounts or trade portals aren't needed. Consumer checkout plus a multi-mat offer is the path.

## Actions to test
- **Multi-mat or fleet bundle** (e.g. 3 or 5 mats) with "kit out every service ute" framing.
- **Meta audiences** in regional QLD: diesel fitters and heavy-vehicle mechanics, plant hire and earthmoving
  owners, graziers and cattle stations. Use the bundle as the offer.
- **Checkout:** a clearly labelled "Business name (for your tax invoice)" field. More businesses would identify
  themselves, which sharpens this analysis and lookalike seeds.

## Re-run (any state or period)
1. `GROUP BY customer_email_domain` and `GROUP BY billing_company, shipping_company` (ShopifyQL, aggregates).
2. Trade-word counts with `customer_email CONTAINS` limited to the generic domains, `GROUP BY` the company
   fields to separate new finds.
3. For a raw Shopify export on your own machine: `python3 business_types.py orders_export.csv QLD`.
