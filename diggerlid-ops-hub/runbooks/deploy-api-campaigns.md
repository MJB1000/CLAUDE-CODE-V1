# Runbook — Deploy `/api/campaigns` (Meta spend time-series)

**Status:** ☐ not deployed · Code ready at `dashboard/api-campaigns.js`
**Unlocks:** weekly MER · true RPV-vs-spend efficiency curves at week level · per-campaign
spend breakdowns (tasks #4–5 in the hub task list).

## Steps (~2 min)
1. Copy `dashboard/api-campaigns.js` into the **diggerlid-mer** Vercel project as
   **`api/campaigns.js`** (same project that serves `/api/mer`).
2. No new secrets — it reuses the existing `META_TOKEN` + `META_ACCOUNT_ID` env vars.
3. Redeploy.
4. Test:
   ```
   https://diggerlid-mer.vercel.app/api/campaigns?since=2026-01-01&until=2026-08-19&increment=1
   ```
   Expect JSON `{ account, since, until, total, points, series:[{date_start, spend}…] }`.

## Params
`since`/`until` (YYYY-MM-DD) · `increment` = `1` daily (default — bucket to ISO weeks
downstream to align with Shopify Mon–Sun) / `7` / `monthly` · `level=campaign` for
per-campaign rows (adds `campaign_id`, `campaign_name`).

## After deploy
Tell the agent: *"api/campaigns is live — pull the daily series since Jan 1, bucket to ISO
weeks, and rebuild the RPV-vs-spend analysis at weekly resolution with weekly MER."*
Then tick the box above and commit.
