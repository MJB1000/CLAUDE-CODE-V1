# PRO Mat conversion and purchase windows (12 Oct 2026)

**Source.** Shopify Admin API order customer journeys. This is every order containing a PRO Mat SKU:

- DLPROM1980 (OG)
- DLPROM1984 to DLPROM1987 (PLUS)

It covers 23 Mar to 12 Oct 2026: 2,249 paid orders, after excluding 55 $0 orders. 2,164 of them have journey data. The output is aggregates only. No PII was stored.

**Definition.** "Days to conversion" is Shopify's count from the first tracked visit, where day 1 means the same day.

**Caveat.** Shopify tracking is cookie- and device-based and looks back about 30 days. Anything longer than about 28 days is undercounted.

## Headline numbers

| Measure | Value |
|---|---|
| Same day | 73.9% |
| Within 7 days | 83.7% |
| Within 14 days | 90.4% |
| Within 28 days | 99.4% |
| Median | 1 day |
| P75 | 2 days |
| P90 | 14 days |
| Single-visit purchases | 52.5% |
| P90 visits | 4 |

## By segment

| Segment | Same day | Within 7 days | P90 days |
|---|---|---|---|
| Meta paid (new customers) | 70.4% | 80.1% | 18 |
| Google organic | 78.9% | 88.6% | 9 |
| Email | 74.1% | 87.1% | 8.6 |
| OG | 74.8% | 84.4% | 13 |
| PLUS | 71.9% | 82.0% | 16 |
| BAU | 76.2% | 85.8% | 13.9 |
| EOFY | 72.0% | 82.8% | 12.4 |
| Father's Day | 68.1% | 78.6% | 18 |

## Returning customers

91% of PRO Mat buyers are new customers. For the 205 returning buyers, the gap from their first DiggerLid order to buying a PRO Mat is:

| Measure | Value |
|---|---|
| Median | 269 days |
| P25 | 75 days |
| P75 | 545 days |
| Within 30 days | 13% |
| Over 1 year | 37% |

Full numbers are in `summary-2026-10-12.json`. To re-run, use `pm_analyse.py` over the extract CSVs.
