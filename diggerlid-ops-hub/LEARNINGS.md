# DiggerLid — Condensed Learnings & Account Data

> The knowledge base: everything material we've learned about this business, verified from
> primary data. Each item names its source doc for the full detail. Last updated **2026-08-20**.

---

## 1. The economic model (the frame everything hangs on)

- **The Ecommerce Equation (ex-GST):** GPAM% = (1 − VCR) − MER. VCR **0.468** BAU / **0.503**
  sale months (2026 actuals). Fixed costs **$74,831/mo**. Shopify net_sales × **1.0437** = ex-GST
  revenue. Targets: **GPAM 26% · MER ≤25%** (≤28% sale months). → `data/ee-baseline.json`
- **13-month benchmarks (Jul 25–Jul 26):** MER 29.6% · GPAM 20.2% · profit +$11.4k/mo · AOV
  $312.86 · CVR 2.39% · CPA $85.88. **Only 5 of 13 months profitable — EOFY + BFCM carry the
  year.** → `data/history/BENCHMARKS.md`
- **MER is the single lever.** H2-2026 scenarios differ ~$149k in net profit purely on spend
  discipline (25% vs 36% MER), with identical revenue. → `data/FORECAST.md`
- 2026 so far: Jan–Jun rev ex-GST $241k→$807k (EOFY); **Jul = worst MER in window (42.4%),
  net −$25k**; Aug tracking ~$397k at MER ~37%, GPAM ~13%.

## 2. Customer economics (cohort CLTV, 15-mo, 24k customers)

→ `deliverables/cohort-cltv-cross-purchase-2026-08-17.md`

- **89% of buyers are brand-new; 11% returning.** DiggerLid is an acquisition machine — the
  12-month LTV is basically the first order (subsequent contribution = $30 of $208, ~14%).
- **12-mo contribution per acquisition by entry category:** Diggershield **$1,063** · Pro
  Enclosure **$409** · Excavator Covers **$193** · Grease **$118** · Accessories $67. (Pro Mats
  ~$139 at 6-mo; launched Aug-25.) **A Diggershield customer is worth ~9× a Grease customer.**
- **Grease = 52% of acquisitions but lowest value** (25% margin, best repeat 25%, buyers loop
  on Grease and almost never ladder up: Grease→Pro Enclosure 1%).
- **Cross-sell is diagonal-dominant and weak everywhere** — customers rebuy their entry
  category. The unbuilt ladder into high-margin lines is the biggest untapped lever.
- **Revenue vs contribution mix:** Grease 47% of revenue but 26% of contribution; Pro
  Enclosure 19% of revenue but **#1 at 27% of contribution**.
- Margins used: Diggershield 80% · Hauler 68% · Pro Enclosure 63% · Exc Covers 62% · Pro Mats
  59% · Accessories 50% · Grease 25%.

## 3. Traffic & efficiency (RPV story)

→ `deliverables/rpv-weekly-2026-ytd.html`, `rpv-vs-sessions-2026.html`, `rpv-vs-spend-2026.html`, `metric-correlations-2026.html`

- **Revenue per visitor halved when paid social scaled:** Jan–Apr avg **$8.26** → May–Aug
  **$4.53** (July trough $2.95). Sessions 6–11k/wk → 16–41k/wk (+188% social).
- **RPV is governed by conversion (r = +0.92)**, not AOV, not traffic mix. Decomposition of the
  −44%: ~63% conversion drop, ~37% AOV drop. Social *share* (~75–77%) barely moved — it's paid
  **volume**, not mix.
- **Spend alone is a weak predictor (r = −0.39) — demand is the hidden variable.** June spent
  the most ($198k) and stayed efficient (MER 25%) because EOFY demand absorbed it; July spent
  $162k with no sale → RPV $3.15, MER 44%. **Spend into demand, not into a vacuum.**
- Benchmark: RPV ≈ $6.9 implied by AOV $315 × CVR 2.2% targets.
- ⚠️ Data artifact: wk 2026-04-27 sessions under-tracked (3,855 sessions vs 323 orders) —
  exclude from trend fits.

## 4. Signup economics (RP-001)

→ `research/RESEARCH-PROJECTS.md`

- **Signup→conversion is remarkably flat ~29%** (26–35% weekly) regardless of cost/signup —
  ~1 in 3 email signups eventually buys. Signup *quality* barely moves; **cost** is the volatile
  lever ($52–$278/signup; blended ~$90–115).
- **The 2026 list-growth slowdown is a REACH problem, not popup conversion** (Alia empirical:
  submit-among-viewers stable ~5–6%; view-rate collapsed as high-bounce paid traffic scaled).
- Expensive EOFY signups converted *highest* (33–35%) — paying more ≠ worse signups.
- Recommendation standing: extend/activate popup targeting first (proven 5–6% capture);
  embedded forms only if bounce-before-trigger is confirmed. Segmented view-rate pull is
  blocked on Alia rate limits (~2 calls → 429) + rotated key in Vercel.

## 5. Experiments (register: `experiments/EXPERIMENT-LOG.md`)

| ID | What | Status | Learning |
|---|---|---|---|
| EXP-001 | Klaviyo FLOW holdout (10% control, md5-hash buckets, 32,579 profiles) | Running since 17 Aug · reads wk4/8/10 (14 Sep / 12 Oct / 26 Oct) | Measures true flow incrementality ($/profile) |
| EXP-002 | Alia popup reward test | Done | **Mystery Discount wins capture** (+39% emails, High certainty); "10% off wins revenue" was 40-order noise (Low); any reward ≫ none; flat-$ discounts drag AOV −16% → prefer % + GWP |
| EXP-003 | PRO Mat colour-selector (before/after, live 19 Aug) | Running | ⚠️ PLUS variants are a 2-wk-old launch ramping 0→82% share — total PLUS share is confounded; judge on **within-PLUS colour split** + PostHog PDP conversion |
| EXP-004 | LP hero video vs image (PostHog `landing-hero-test`) | Running since 13 Aug | **Video hero: PDP CTR 32% vs 20% (+62%), ~3× purchase among true viewers** — most promising lever found; underpowered pending de-dilution |
| EXP-005 | FD gift page A/B (PostHog `fathers-day-test`) | Running since 17 Aug | Muddy; the page itself is the weak LP (0.69% purchase, 11% CTR→PDP) |

**PostHog gotchas (both cost real signal):**
1. **Enrollment dilution** — flags enroll site-wide but variants render only on their LP →
   ~96% of "enrolled" users never saw the change; aggregate reads were washed out. Fix: scope
   experiment exposure/flag conditions to the LP URL.
2. **Shopify events lack `$feature/*` flags** — `Product Added` / `Order Completed` come from
   the Shopify pipe without enrolment properties, so PostHog's UI shows ~0 conversions. Fix:
   bridge flag values through cart attributes (runbook in chat log / to be committed). Until
   then, person-stitch in HogQL.
3. PostHog history starts **2026-06-18** — "returning" is undercounted before ~2 months.

## 6. Page & funnel benchmarks (PostHog, person-stitched, Aug 2026)

- **Pro Mat PDP:** 9.5% ATC · 4.40% purchase (new 3.9% / returning 8.4%) — beats site-wide 3.71%.
- **Returning visitors convert ~2.2× new** (and are ~11% of traffic).
- Campaign LPs convert low on their own (1.3% / 0.7%) — **their job is hand-off to the PDP**;
  judge on CTR-to-PDP (currently 20–32% Pro Mat LP; 11–12% gift LP).
- Grease pages: high-intent (`/products/kajo-adapter` 29.9% ATC; `/collections/bundles` 48.8%
  ATC, 25% purchase — small N but striking).

## 7. Audience & product facts

- **Pro Mat Plus buyers (2-wk sample): ~34% female-certain first names, 55% male, 11% unknown** —
  strong female gift-buyer skew vs the base; male AOV $481 vs female $338. Validated the FD
  women-gift-buyer targeting + bundles-to-lift-AOV.
- **PRO Mat variant mix:** OG/Grey was 100% until PLUS launched Aug 5 (Zipper Pro Mat V2);
  PLUS took 60→76→82% of PRO Mat orders in 3 weeks. Within PLUS: Orange ~33% · Grey ~35% ·
  Camo ~22% · Pink ~10%. PLUS AOV ~$310–335 vs OG ~$223.
- **Payments:** Shopify Payments 76% · PayPal 20% · BNPL ~3%. Historic refund rate strikingly
  low (190 refund transactions all-time; ~0.6% of recent orders).
- **Father's Day 2026 campaign:** 15% off mats + GWP + tiered bundles; sale 26 Aug–4 Sep
  (ends 2 days pre-FD); shipping cutoffs QLD/SA/NT/WA/TAS −4d, VIC/NSW −3d; post-sale
  "didn't get what you wanted" offer; briefs in `deliverables/fathers-day-2026-*`.

## 8. Data-pull gotchas (save yourself the re-discovery)

- **Shopify `ordersCount` counts unpaid/voided attempts** — runs ~3.5% above the real
  completed-orders set (worse in sale months). Reconcile LTV on paid orders.
- ShopifyQL: `FROM sales/sessions SHOW … TIMESERIES … SINCE … UNTIL` — no PDP-level session
  cut (use PostHog for page-level). `customersCount` ignores tag filters, caps at 10k.
- **Klaviyo filters:** `created` only accepts `greater-than`/`less-than` (NOT `greater-or-equal`).
- **Alia API:** needs `groupByInterval`; hard 429s after ~2 quick calls; device filter silently
  ignored with wrong rhs syntax. Token cost = 20 × stats × days.
- Native Shopify Orders CSV export: line-item level, order fields blank on 2nd+ rows
  (forward-fill), variant folded into `Lineitem name`. Transactions export ≠ orders export.
- SKU→category rulebook (final, patched): `analysis/cohort-scripts/categorize.py` — priority
  order matters (Adaptors before Guns; "adapter" US spelling; PRO Mat guard before Accessories;
  GWP/$0/Protection/Returns excluded entirely; 3 named bundles hero-mapped).

## 9. Standing decisions & preferences (Matt)

- Empirical over conjecture — label **fact vs hypothesis**, separate confirmed data from
  inference; small-N "wins" get certainty labels (High/Medium/Low).
- % discounts + GWP over flat-$ (AOV protection). Never "we're diggin' it".
- Scorecard = persistent full-column format incl. RPV + projected EOM + experiments row.
- Charts: on-brand, theme-aware, interactive HTML in `deliverables/` (committed).
- Keys pasted in chat are burned → rotate. PII never committed.
```
