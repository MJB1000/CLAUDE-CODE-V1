# DiggerLid — Experiment Log

The running record of every growth/marketing experiment: hypothesis, design, dates, result.
Durable across sessions — this is the source of truth, not chat.

## How to use it
- **Log a new one:** tell me *"log an experiment: …"* (or copy the template at the bottom). I'll assign the next `EXP-###` and fill it in.
- **Give a progress update:** tell me *"update EXP-002: shipped the variant, CVR looks flat"* — I append a dated line to that experiment's **Updates**.
- **Close it out:** when it ends I fill **Result / Verdict** and set status.
- You can also edit this file directly; I'll keep it tidy.

**Status values:** `Proposed` · `Running` · `Analyzing` · `Done` · `Killed`
**Decision discipline:** every experiment states a **decision rule** up front (what result → what action) so we don't rationalise after the fact.

---

## Register

| ID | Experiment | Status | Start | End | Primary metric | Result |
|---|---|---|---|---|---|---|
| EXP-001 | Email FLOW holdout | Running (go-live 17 Aug) | 2026-08-17 | 2026-10-26 | Revenue per profile (flow incrementality) | pending |

---

## EXP-001 — Email FLOW holdout
**Status:** Running (go-live Mon 17 Aug 2026) · **Owner:** Matt

**Hypothesis:** Klaviyo flows drive net-new revenue (not just revenue that would have happened anyway). A 10% flow-holdout will show a measurable positive uplift in revenue per profile.

**Design:** Global/persistent. 10% control (~3,258) excluded from **all flows**; 90% treatment (~29,321) get flows. Control still receives campaigns + SMS + transactional. Random assignment by deterministic email hash (`scripts/holdout_assign.py --prop ho_flow`). Window: 10 weeks. Exclusion via a flow filter ("not in `🚫 FLOW HOLDOUT`") on every live flow. Full build steps: `experiments/flow-holdout-klaviyo-runbook.md`.

**Dates:** Start **2026-08-17** · Planned end **2026-10-26** (10 weeks). Analysis check-ins scheduled wk4 (14 Sep), wk8 (12 Oct), wk10 (26 Oct).

**Primary metric:** Revenue per profile (RPR), Control vs Treatment.
**Reads:** purchase rate (chi-square) · AOV among buyers · RPR (bootstrap CI) · **incremental $ = (RPR_t − RPR_c) × N_treatment** · per-trigger cohort lift.
**Guardrail metrics:** unsub / spam-complaint rate by arm (holding out can reduce fatigue — part of net value).

**Decision rule:**
- Significant positive incremental $ → quantify flow value, keep a small always-on holdout, then run the CAMPAIGN holdout (Test 2).
- Negligible / negative → audit and rework the underperforming flows before scaling send volume.

**Updates**
- **2026-08-13** — Designed (sequential holdouts, flows first). Committed `holdout_assign.py` (tested: 3,246/29,333 on 32,579) + Klaviyo runbook. Scheduled wk4/8/10 analyses. Awaiting go-live Mon 17 Aug: build segments, gate every flow, log launch sizes.

---

## Template (copy for a new experiment)
```
## EXP-00X — <name>
**Status:** Proposed · **Owner:**

**Hypothesis:** We believe <change> will cause <effect>, measured by <metric>.
**Design:** <arms / % / mechanism / duration>
**Dates:** Start <date> · Planned end <date>
**Primary metric:** <metric>   **Guardrails:** <metrics that must not get worse>
**Decision rule:** <result → action>

**Updates**
- <date> — <what happened>

**Result / Verdict:** <filled at close>
```
