# Automations — Rebuild List & Instructions

> Scheduled jobs live **per Claude account** — none of them migrate with the repo.
> Rebuild each on whichever account owns it. **One owner per job** (two owners = duplicate
> briefs + racing git pushes; we've had the collision once already).

## How to schedule on the new account
In Claude Code: ask the agent to *"create a Routine: <name>, schedule <cron/time>, prompt: <prompt>"*
(uses the built-in scheduler; times are stored in UTC — Brisbane is UTC+10, no DST).
Alternative for one-shots: *"remind me on <date> to <prompt>"*.

---

## 1. Daily brief — weekdays ~07:30 AEST (21:30 UTC prior day)
**Owner:** CoS account · **Needs:** Shopify MCP + repo (read-only)
**Prompt:** use verbatim from `MIGRATION-BOOTSTRAP.md` §4-A.
**Rules:** read-only (no push) · never fabricate · full scorecard columns per
`data/DAILY-SCORECARD-FORMAT.md` incl. RPV + projected EOM + live-experiments row.
**Email option:** render into `templates/daily-brief-email.html` and send/paste (see template header).

## 2. Weekly forecast — Mondays ~08:00 AEST
**Owner:** Scorekeeper account · **Needs:** Shopify MCP + repo **write** + `/api/mer`
**Prompt:** verbatim from `MIGRATION-BOOTSTRAP.md` §4-B.
**Steps it performs:** update `scripts/forecast_engine.py` INPUTS (lock finished months to
ACTUALS; refresh MTD net/days/live spend) → run → save `data/forecast/2026-Www.md` → refresh
`data/FORECAST.md` with drift notes → commit + push.

## 3. EXP-001 flow-holdout check-ins — one-shots: **14 Sep · 12 Oct · 26 Oct 2026**
⚠️ These were timers on the OLD account — they will NOT fire elsewhere. Recreate as three
one-shot reminders.
**Prompt:** *"EXP-001 flow holdout analysis (wk N): pull Klaviyo revenue per profile for
control (`ho_flow=control`) vs treatment since 17 Aug; purchase rate chi-square, AOV among
buyers, bootstrap CI on RPR, incremental $ = (RPR_t − RPR_c) × N_treatment; guardrails unsub/
spam by arm. Log to EXPERIMENT-LOG.md, commit."* (Design: `flow-holdout-klaviyo-runbook.md`.)

## 4. Weekly experiment reads (PostHog) — e.g. Thursdays
**Needs:** `POSTHOG_API_KEY` server-side (see `SECRETS-AND-KEYS.md` A7) or paste-in results.
**Prompt:** *"Weekly experiment read: for flags `landing-hero-test` and `fathers-day-test`
(PostHog project 475333, US), compute per-variant PDP CTR / ATC / purchase person-stitched in
HogQL, restricted to the landing-page viewers (see EXPERIMENT-LOG.md gotchas — enrollment is
diluted and Shopify events lack $feature/*). Update EXPERIMENT-LOG.md, flag significance
honestly, commit."*
Also covers **EXP-003**: within-PLUS colour split via ShopifyQL
(`GROUP BY product_variant_title WHERE product_title='PRO Mat'`), vs the 19-Aug baseline.

## 5. PR watching
Subscribe the working session to the open PR (ask: *"watch PR #11"*) or rely on GitHub
notifications. Re-subscribe per new session/account.

## 6. Monthly retro (recommended, new)
First business day of month: lock previous month into ACTUALS, write a 10-line month retro in
`analysis/`, refresh `data/history/BENCHMARKS.md`. Prompt: *"Monthly close: lock <month> into
forecast_engine ACTUALS from the EE model + /api/mer, append month retro (what beat/missed
forecast and why), commit."*

---

## Ownership matrix (fill in when accounts exist)

| Job | Owner account | Status |
|---|---|---|
| Daily brief | ___ | ☐ rebuilt |
| Weekly forecast | ___ | ☐ rebuilt |
| EXP-001 check-ins ×3 | ___ | ☐ rebuilt |
| Weekly experiment reads | ___ | ☐ new |
| Monthly retro | ___ | ☐ new |
