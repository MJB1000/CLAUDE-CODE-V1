# DiggerLid — Daily Scorecard Format (standing)

The daily brief scorecard **always** uses these columns and rows. Persistent — do not drop
columns between briefs. Numbers must be pulled live (Shopify MCP), never estimated.

## Columns
| Metric | Yesterday | 7-day avg | MTD | Target | Projected EOM | Trend |

- **Yesterday** = last complete sales day (Shopify store-local / AEST).
- **7-day avg** = mean of the last 7 complete days (per-day for $/orders; blended rate for %).
- **MTD** = month-to-date through yesterday.
- **Target** = standing benchmark (below).
- **Projected EOM** = run-rate: `MTD ÷ completed_days × days_in_month` for net sales & orders;
  rates (AOV, CVR, returning) carried at the MTD level. **Excludes** any un-launched promo
  (e.g. Father's Day, BFCM) — flag those as upside on top.
- **Trend** = ▲/▼/▬ comparing Yesterday vs 7-day avg vs MTD direction.

## Rows (metrics)
Net sales · Orders · AOV · CVR · Returning-customer rate · **MER** · **GPAM**

- **MER / GPAM** need ad spend. If spend not supplied at fire time → mark **ASSUMED** and
  reference last known; never fabricate. GPAM% = (1 − VCR) − MER; VCR 0.468 BAU / 0.503 sale.

## Targets (benchmarks)
- AOV **$315** · CVR **≥2.2%** BAU · GPAM **26%** · MER **≤25%** (sale months ≤28%).

## Experiments row (always include)
One line pulled from `experiments/EXPERIMENT-LOG.md`: each Running/recent experiment with status.
Current: **EXP-001 Flow Holdout** (go-live 2026-08-17) · **EXP-002 Alia Reward Test** (Done).

## Source queries (ShopifyQL)
- Yesterday + 7-day: `FROM sales SHOW net_sales, orders, average_order_value TIMESERIES day SINCE -8d UNTIL yesterday`
- MTD sales: `FROM sales SHOW orders, net_sales, average_order_value, returning_customer_rate SINCE <month-1st> UNTIL yesterday`
- MTD sessions/CVR: `FROM sessions SHOW sessions, conversion_rate SINCE <month-1st> UNTIL yesterday`
- Daily CVR (7-day/yesterday): `FROM sessions SHOW conversion_rate TIMESERIES day SINCE -8d UNTIL yesterday`

## Notes
- Scorecard shows **Shopify net_sales** (incl. GST, excl. shipping). The forecast engine
  converts to ex-GST via ×1.0437 — keep the scorecard raw for day-to-day consistency.
- Deployed Scorekeeper (Paperclip) pulls Shopify/Meta itself, incl. live MER.
