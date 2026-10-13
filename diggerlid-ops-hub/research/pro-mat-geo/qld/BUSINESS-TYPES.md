# QLD PRO Mat buyers by likely business type (interim, 13 Oct 2026)

**Status: early sample only.** The live Shopify pull was blocked by the session permission
checker after 5 pages (250 orders nationally, 56 shipped to QLD, all from late March to early
May 2026, so Original-era buyers only). Finish it with `business_types.py` on a Shopify export.

## Method
Per order, first match wins:
1. **Shopify Company field** (shipping or billing). Primary. Only fetched for pages 1 and 2.
2. **Business email domain** (anything that is not gmail, bigpond, hotmail etc.).
3. **Trade word in the email** on a personal domain (e.g. a "civil" or "farmer" address). Flagged as *likely*.

No names, emails or company names are stored. Counts only.

## Sample result (QLD, n = 56)

| | Orders | Share |
|---|---|---|
| Likely business buyers | 11 | 20% |
| Personal or no signal | 45 | 80% |

| Business type | Orders |
|---|---|
| Civil, earthmoving & contracting | 3 |
| Farming, agriculture & turf | 3 |
| Mechanical, engine & service | 2 |
| Animal & equine | 1 |
| Hospitality | 1 |
| Unclear | 1 |

Evidence: Company field 4, business domain 4, trade word in email 3.

**Coverage matters.** Pages with the Company field found 25% business (6 of 24). Pages without
it found 16% (5 of 32). So 20% is a floor, likely nearer a quarter.

## National read from the same 250 orders (directional)
Where the Company field was filled nationally, mechanical, heavy diesel, hydraulics and automotive
workshops were the single biggest group, ahead of farming and civil. QLD shows the same three
groups in a different order: civil and farming first, then mechanical.

## What it suggests (hypothesis, small N)
- PRO Mat is mainly bought on personal email, so most buyers are owner-operators or employees
  buying for themselves, not businesses buying through accounts.
- The business minority clusters in **civil/earthmoving, farming and mechanical workshops**.
  These match the regional QLD hot spots (Darling Downs, Central Highlands, Mackay).
- Worth testing: Meta interest and lookalike audiences around diesel fitters, mechanics and
  farm operators, and a "tax-deductible tool for your ute" angle for the business minority.

## To finish
Shopify admin → Orders → filter date from 23 Mar 2026 → Export (CSV, plain). Then run:
```
python3 business_types.py orders_export.csv QLD
python3 business_types.py orders_export.csv NSW   # any state
```
