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
Net sales · Orders · AOV · CVR · **Revenue per visitor (RPV)** · Returning-customer rate · **MER** · **GPAM**

- **Revenue per visitor (RPV)** = `net_sales ÷ sessions` (equivalently AOV × order-conversion).
  One number that moves when either AOV or conversion moves — the cleanest single health metric.
  Populate all three cells: yesterday = day net ÷ day sessions; 7-day = 7-day net ÷ 7-day sessions;
  MTD = MTD net ÷ MTD sessions.

- **MER / GPAM** need ad spend. If spend not supplied at fire time → mark **ASSUMED** and
  reference last known; never fabricate. GPAM% = (1 − VCR) − MER; VCR 0.468 BAU / 0.503 sale.

## Targets (benchmarks)
- AOV **$315** · CVR **≥2.2%** BAU · GPAM **26%** · MER **≤25%** (sale months ≤28%).
- **RPV implied benchmark ≈ $6.9** (AOV target $315 × CVR target 2.2%) — derived, not a hard target;
  it frames how much of the AOV×conversion gap RPV is closing.

## Experiments row (always include)
One line pulled from `experiments/EXPERIMENT-LOG.md`: each Running/recent experiment with status.
Current: **EXP-001 Flow Holdout** (go-live 2026-08-17) · **EXP-002 Alia Reward Test** (Done).

## Source queries (ShopifyQL)
- Yesterday + 7-day: `FROM sales SHOW net_sales, orders, average_order_value TIMESERIES day SINCE -8d UNTIL yesterday`
- MTD sales: `FROM sales SHOW orders, net_sales, average_order_value, returning_customer_rate SINCE <month-1st> UNTIL yesterday`
- MTD sessions/CVR: `FROM sessions SHOW sessions, conversion_rate SINCE <month-1st> UNTIL yesterday`
- Daily CVR (7-day/yesterday): `FROM sessions SHOW conversion_rate TIMESERIES day SINCE -8d UNTIL yesterday`
- Daily sessions (for RPV = net ÷ sessions): `FROM sessions SHOW sessions TIMESERIES day SINCE -8d UNTIL yesterday`

## Notes
- Scorecard shows **Shopify net_sales** (incl. GST, excl. shipping). The forecast engine
  converts to ex-GST via ×1.0437 — keep the scorecard raw for day-to-day consistency.
- Deployed Scorekeeper (Paperclip) pulls Shopify/Meta itself, incl. live MER.
