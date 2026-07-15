# scripts/

## forecast_engine.py
The Scorekeeper's weekly forecast engine. Re-forecasts MER + sales for each month as the month
progresses, checks against the 26% GPAM target, and prints a Markdown block.

**Weekly use (Scorekeeper, every Monday):**
1. Edit the `INPUTS` at the top: lock any finished month into `ACTUALS`; refresh `CURRENT`
   (`mtd_net`, `days_elapsed`) from Shopify; set `ad_spend_mtd` from Meta (or leave `None`).
2. `python3 forecast_engine.py > ../data/forecast/$(python3 -c "import datetime;print(datetime.date.today().strftime('%Y-W%V'))").md`
3. Refresh `../data/FORECAST.md` and note drift vs last week in the Monday brief.

**Inputs are pure data** — no network. The Shopify/Meta *fetch* is done by the agent (MCP) each
week; the engine just does the math, so it's testable and deterministic. Revenue = Shopify
`net_sales` (after discounts/returns, before GST). Model: GPAM% = (1 − VCR) − MER.

Until Meta is wired, MER for the in-progress month is an **assumption** (flagged on every snapshot);
sales are live-actual-to-date. Wiring Meta turns MER actual — the highest-value data upgrade.
