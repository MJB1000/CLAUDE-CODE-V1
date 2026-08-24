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
| EXP-002 | Alia popup reward test (Mystery vs $35 vs 10% vs none) | Done | 2026-07-28 | 2026-08-05 | Email submit rate + 14d attributed rev | Mystery wins capture (**High**); 10%-off "revenue win" unproven (**Low**) |
| EXP-003 | PRO Mat colour-selector change | Running (before/after, live 19 Aug) | 2026-08-19 | TBD | Within-PLUS colour mix + PDP conversion | pending |
| EXP-004 | LP: Pro Mat hero — video vs image (PostHog) | Running | 2026-08-13 | TBD | PDP CTR → purchase | test/video +5–11% dir., **n.s.** (underpowered) |
| EXP-005 | LP: Father's Day gift page A/B (PostHog) | Running | 2026-08-17 | TBD | PDP CTR → purchase | mixed (+7% purchase, flat ATC), **n.s.** |

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

## EXP-002 — Alia popup reward A/B/C/D test
**Status:** Done · **Owner:** Matt · **Window:** 28 Jul – 5 Aug 2026 (9 days)
**Full report:** `experiments/EXP-002-alia-reward-test-report.md`

**Hypothesis:** The popup reward offer (Mystery Discount vs $35 off vs 10% off vs none) changes email capture and downstream revenue.

**Design:** 4-way Alia split, ~6,200 visitors/variant. Note Alia's labels mislead — "Control" = Mystery Discount (incumbent); "Control 10%" = the 10%-off test variant.

**Primary metrics:** email submit rate (capture) + 14-day attributed revenue.

**Result / Verdict:**
- **Capture winner: Mystery Discount** — 4.98% email submit rate vs 3.67% (10%-off); ~39% more emails. **Certainty: High** (p≈0.02; Alia prob-to-win 87%).
- **Alia's "10%-off won on revenue" (+48% sales, 42.6% CVR): NOT trustworthy. Certainty: Low** — rests on 40 orders and vanishes in the well-powered sitewide 7-day CVR (Mystery/$35/10% all tied ~1.0%; only "no reward" worse at 0.78%).
- **Any reward >> no reward** (submit 3.7–5% vs 1.65%). **Certainty: High.**
- **Flat $35-off dragged AOV −16%** ($210 vs $251) — prefer % over $ discounts. **Certainty: Medium.**

**Certainty (overall):** the *capture* read is solid; the *revenue* read is under-powered noise.

**Recommendation for next test:** Decide the objective first — if list growth (BFCM feed), keep Mystery Discount and don't re-test. If chasing revenue-quality, re-run **Mystery vs 10%-off head-to-head only**, pre-declare 14-day attributed revenue/visitor as the primary metric, and power to **~150–200 orders/variant (~4–6 wks)** — not 9 days/40 orders. Segment new-vs-returning and track margin/AOV as guardrails.

**Updates**
- **2026-08-13** — Decoded and logged. Report attached. Verdict: Mystery wins capture (High); 10%-off revenue win unproven (Low); avoid flat-$ discounts (AOV drag). Cross-links to Father's Day offer decision (% + GWP protects AOV).

---

## EXP-003 — PRO Mat colour-selector change
**Status:** Proposed (design pending) · **Owner:** Matt

**Hypothesis:** Changing the PRO Mat colour selector (STYLE PLUS/OG + the four colour swatches)
changes how buyers choose — moving **PDP conversion** and/or the **colour / PLUS-vs-OG mix**.
Because PLUS colours carry a higher AOV than OG/Grey, a mix shift toward PLUS is an AOV tailwind.

**Design (confirmed):** **Before/after, 100% switch. Went live Wed 2026-08-19.** Primary goal = colour/PLUS
mix. Exact change = colour-selector UI (STYLE PLUS/OG + four swatches, default Signature Grey).

**⚠️ Confound — PLUS is a 2-week-old launch, not a stable baseline.** Weekly PRO Mat orders show PLUS
variants **did not exist until the week of Aug 3** (= Zipper Pro Mat V2 launch, Aug 5); before that,
PRO Mat was 100% OG/Signature Grey. PLUS is on a steep adoption ramp:

| Week | OG/Grey | PLUS total | **PLUS share** | Within-PLUS: Org / Gry / Camo / Pink |
|---|--:|--:|--:|---|
| ≤ Jul 27 | all | 0 | **0%** | — (PLUS not launched) |
| Aug 3 | 32 | 49 | **60%** | 49% / 18% / 16% / 16% |
| Aug 10 | 28 | 91 | **76%** | 27% / 34% / 25% / 13% |
| Aug 17 | 15 | 69 | **82%** | 33% / 36% / 22% / 9% |

The selector change (Aug 19) sits **on top of this ramp**, so a naïve before/after on **total PLUS share
is confounded** by launch adoption — it would rise regardless. Attribute only what deviates from the ramp.

**Primary metric (revised):**
1. **Within-PLUS colour distribution** (Orange/Grey/Camo/Pink share among PLUS buyers) — least
   confounded by the launch ramp; most directly moved by a colour selector (default/prominence).
2. **PRO Mat PDP conversion** — best measured in **PostHog** (Shopify has no PDP-level session cut),
   incl. selector-interaction events. This is the cleanest selector-attributable read.
**Tracked but de-weighted:** total PLUS share (launch-driven) · AOV (PLUS ~$310–335 vs OG ~$223, so a
real mix shift toward PLUS is an AOV tailwind).
**Guardrail:** total PRO Mat units + net revenue must not drop.

**Decision rule:**
- Within-PLUS colour split shifts materially post-Aug-19 **beyond** the pre-ramp trajectory, and/or
  PostHog PDP conversion rises with no volume loss → keep the new selector; document the winning layout.
- No deviation above trend / conversion flat or down → revert or iterate the selector.
- ⚠️ **Father's Day sale (26 Aug–4 Sep)** overlaps the post window — fence those dates (or read them
  separately), since promo traffic can shift both volume and mix.

**Updates**
- **2026-08-20** — Design confirmed (before/after, live Wed 19 Aug, mix goal). Pulled weekly trajectory
  → discovered PLUS is a 2-week-old launch on a steep ramp (0→60→76→82%); re-scoped primary to
  within-PLUS colour split + PostHog PDP conversion (total PLUS share confounded by launch). FD-sale
  overlap flagged. Next: confirm PostHog is capturing the PDP + selector events so conversion is readable.

**Result / Verdict:** *pending*

---

## EXP-004 — LP: Pro Mat hero, video vs image (PostHog)
**Status:** Running · **Owner:** Matt · **Tool:** PostHog (project 475333, US) · flag `landing-hero-test` · exp 418163
**Hypothesis:** A **video** hero on the Pro Mat landing beats the **image** hero on click-through → purchase.
**Design:** 50/50 control(image)/test(video), start **2026-08-13**. Primary = CTR to `/products/pro-mat`;
secondary = add-to-cart / purchase (person-stitched, see gotcha).
**First read (2026-08-20, since 13 Aug):**
| Variant | Exposed | PDP CTR | Add-to-cart | Purchase |
|---|--:|--:|--:|--:|
| control (image) | 4,330 | 9.3% | 8.9% | 4.16% |
| test (video) | 4,345 | 9.8% | 9.3% | **4.60%** |
- **test/video is directionally ahead on every step (+5% CTR, +5% ATC, +11% purchase) — but none significant** (p 0.31–0.51). Randomisation clean (~50/50).
**Verdict:** promising lean toward video, **underpowered**. To confirm the ~+11% purchase lift at 80% power needs ~**35k/arm** (now ~4.3k) → **several more weeks**. Don't call it yet.

## EXP-005 — LP: Father's Day gift page A/B (PostHog)
**Status:** Running · **Owner:** Matt · **Tool:** PostHog · flag `fathers-day-test` · exp 425510
**Hypothesis:** Redesigned FD gift page (Design B/test) lifts click-through → purchase vs A/control.
**Design:** 50/50, start **2026-08-17**. Primary = CTR to `/products/pro-mat`; secondary = ATC / purchase.
**First read (2026-08-20, since 17 Aug):**
| Variant | Exposed | PDP CTR | Add-to-cart | Purchase |
|---|--:|--:|--:|--:|
| control | 2,306 | 8.0% | 9.0% | 4.47% |
| test | 2,354 | 8.8% | 8.9% | 4.76% |
- **Mixed:** test +11% on PDP CTR and +7% purchase, but **flat/−1% on add-to-cart**; nothing significant (p 0.29–0.94). Very early (3 days).
**Verdict:** inconclusive, underpowered — keep running through/after the FD sale, but note sale traffic will change the page's audience.

### ⚠️ Measurement gotcha (applies to both — important)
Commerce events (`Product Added`, `Order Completed`) come from the **Shopify pipe and do NOT carry the
`$feature/<flag>` enrolment property** — only client events ($pageview/autocapture) do. So **PostHog's
built-in experiment results will show ~0 for the add-to-cart / purchase secondary metrics** (it filters by
that property). Reads above are computed by **person-stitching** in HogQL (enrol persons via client events,
then join their Shopify purchase events by `person_id`). **Fix to make PostHog's own UI correct:** forward
the active feature-flag values onto the Shopify→PostHog events (or add `$feature/*` in the Shopify pixel).

### ℹ️ Also present
- **exp 379241 `product-addtocart-webview-fix`** — "webview-safe add-to-cart", **not started** (no start date). Draft.
- **Overlap:** EXP-004 (hero) and **EXP-003 (colour selector)** both change the **same Pro Mat PDP** in the
  same window (hero 13 Aug, selector 19 Aug) — they can interact; read each with the other in mind.

### Monitoring
Point-in-time read via personal API key (used transiently, **not stored** — user is rotating it). For recurring
auto-reads in the daily brief, set a durable PostHog key server-side (e.g. Vercel env) and I'll wire a cached pull.

**Updates**
- **2026-08-20** — First read pulled + logged for both. Found the Shopify-events flag-property gap (person-stitched around it). Both underpowered/n.s.; video hero the most promising. Flagged EXP-003↔EXP-004 PDP overlap.

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
