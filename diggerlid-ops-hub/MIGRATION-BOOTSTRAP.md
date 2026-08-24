# DiggerLid Ops Hub — Migration & Bootstrap Guide

> Everything needed to run the Chief-of-Staff / business-intelligence system on a new Claude
> account (or hand it to a teammate). The **repo is the source of truth** — chat context dies,
> files persist. If it matters, it's in a file here.

**Repo:** `MJB1000/CLAUDE-CODE-V1` · working branch `claude/blitzos-build-qhutfl` (PR #11 draft)
**Owner:** Matt (Head of Growth, DiggerLid) · **Business:** digger-lid.myshopify.com (AUD, ex-GST reporting)

---

## 1. What this system is

An AI Chief-of-Staff for DiggerLid e-commerce growth:

| Function | What it does | Where |
|---|---|---|
| **Daily brief** | Calendar + live Shopify scorecard + flags, every morning | prompt in §4; format `data/DAILY-SCORECARD-FORMAT.md` |
| **Weekly forecast** | EE-model forecast (MER/GPAM/net) refreshed Mondays | `scripts/forecast_engine.py` → `data/forecast/` + `data/FORECAST.md` |
| **Experiment tracking** | Register + rigor (power, significance, decision rules) | `experiments/EXPERIMENT-LOG.md` |
| **Research projects** | Durable analyses (signup economics, cohort CLTV…) | `research/RESEARCH-PROJECTS.md` |
| **Deliverables** | On-brand charts/reports/briefs | `deliverables/` |
| **Launch/campaign support** | Briefs (GACC), calendars, sale plans | `deliverables/fathers-day-*`, calendar app |

Agent role files (persona + duties): `agents/CHIEF-OF-STAFF.md`, `agents/SCOREKEEPER.md`,
`agents/LAUNCH-MARSHAL.md`, `agents/VOICE-OF-CUSTOMER.md`.
Objectives & thresholds: `OBJECTIVES.md` · watchlist categories: `WATCHLIST.md`.

**Note:** the repo root `CLAUDE.md` is a separate *marketing-team* system (Sofia / Strategist /
Copywriter / Designer). The CoS hub is self-contained under `diggerlid-ops-hub/`.

## 2. Repo structure (ops hub)

```
diggerlid-ops-hub/
├── OBJECTIVES.md              # North-star metrics: MER ≤25%, GPAM ≥26%, targets
├── WATCHLIST.md               # Flag categories the daily brief scans for
├── agents/                    # CoS, Scorekeeper, Launch Marshal, VoC role files
├── data/
│   ├── DAILY-SCORECARD-FORMAT.md   # STANDING scorecard columns (persistent contract)
│   ├── FORECAST.md                 # Latest forecast summary
│   ├── forecast/2026-Www.md        # Weekly snapshots (W29–W34…)
│   ├── history/BENCHMARKS.md       # 13-month trailing benchmarks (ex-GST restated)
│   └── ee-baseline.json            # EE model baseline params
├── scripts/
│   ├── forecast_engine.py     # Weekly forecast generator (edit INPUTS, run, save)
│   └── holdout_assign.py      # Deterministic md5-bucket holdout assignment (EXP-001)
├── experiments/
│   ├── EXPERIMENT-LOG.md      # Register EXP-001…005 + decision rules + updates
│   ├── EXP-002-alia-reward-test-report.md
│   └── flow-holdout-klaviyo-runbook.md
├── research/RESEARCH-PROJECTS.md   # RP-001 signup economics (+ future RPs)
├── deliverables/              # Charts (theme-aware HTML), reports, briefs, CSVs
├── dashboard/
│   ├── index.html             # MER/GPAM dashboard (client-side, no secrets)
│   ├── api-mer.js             # Vercel fn: MTD Meta spend + Shopify net → MER/GPAM
│   └── api-campaigns.js       # Vercel fn: Meta spend TIME-SERIES (daily/weekly)
└── analysis/                  # Dated action plans, cohort scripts
```

## 3. External infrastructure

| Service | What | Access |
|---|---|---|
| **Vercel `diggerlid-mer`** | `/api/mer` (live MTD Meta spend + MER/GPAM) · `/api/emails` (Klaviyo signups) · `/api/campaigns` (Meta series — file in repo, deploy pending) | Public URLs; secrets in Vercel env |
| **Vercel calendar** | `diggerlid-calendar-henna.vercel.app/ai` — public JSON campaign calendar (151+ items) | Public, no auth |
| **Shopify** | digger-lid.myshopify.com — ShopifyQL analytics + Admin GraphQL | **Shopify MCP connector** (per Claude account) |
| **Klaviyo** | Email/SMS; signups metric via `/api/emails` | Key in Vercel env ONLY |
| **Meta** | Ad spend via `/api/mer` (`META_TOKEN`, `META_ACCOUNT_ID` in Vercel env) | Via Vercel fns |
| **Alia** | Popup platform, `api.alia-prod.com/v1` (Bearer). ⚠️ HARD rate limits (~2 calls then 429) | Key rotated by Matt; use transiently |
| **PostHog** | US cloud, project **475333**. Experiments: `landing-hero-test`, `fathers-day-test` | Personal API key (transient) or server-side env |
| **GitHub** | This repo — source of truth, PR #11 | GitHub connector / repo access |

### Secrets inventory (NAMES only — values live in Vercel env or password manager, NEVER in repo/chat)
| Secret | Lives in | Used by |
|---|---|---|
| `META_TOKEN`, `META_ACCOUNT_ID` | Vercel diggerlid-mer env | api-mer.js, api-campaigns.js |
| `KLAVIYO_API_KEY` | Vercel env | api/emails.js |
| `SHOPIFY_SHOP`, `SHOPIFY_TOKEN` | Vercel env (optional) | api-mer.js revenue |
| Alia API key | Matt (rotate after any chat paste) | ad-hoc popup analytics |
| PostHog personal API key | Matt (rotate after any chat paste) | experiment reads |

**Rule:** a key pasted into chat is burned — rotate it. New account should never need raw keys;
it reads public endpoints + MCP connectors.

## 4. Automations (recreate on the new account)

These do NOT transfer automatically — they live per-account:

**A. Daily brief (weekday mornings)** — paste as a scheduled Routine or manual prompt:
```
Daily DiggerLid brief (Chief of Staff stand-in). Keep it tight — lead with ≤3 things that
need attention, then the rest terse.
1. CALENDAR (auto, public): curl https://diggerlid-calendar-henna.vercel.app/ai . Report:
   status changes vs the last brief, anything with goLive today or next 7 days (with send
   times), and the next tier:major or In Progress launch with T-minus days.
2. SCORECARD: if Shopify MCP is available, pull yesterday + 7-day + MTD net_sales, orders,
   AOV, CVR, RPV and returning-customer rate per data/DAILY-SCORECARD-FORMAT.md (incl.
   projected EOM + trend + live experiments row); report vs targets (CVR ≥2.2% BAU; GPAM 26%).
   MER needs ad spend — pull /api/mer or mark ASSUMED. If Shopify MCP is unavailable, ask for
   yesterday's numbers but STILL deliver the calendar section.
3. FLAGS: watchlist categories (promo reset overdue, launch prep slipping, stale board items).
4. Do NOT fabricate numbers. Read-only (no git push in the daily brief).
```

**B. Weekly forecast (Mondays)**:
```
Weekly DiggerLid forecast update (Scorekeeper routine): update scripts/forecast_engine.py
INPUTS (lock finished months into ACTUALS; refresh in-progress month MTD net + days + live
Meta spend from /api/mer), run it, save data/forecast/2026-Www.md, refresh data/FORECAST.md
with drift-vs-last-week notes, commit and push.
```

**C. Experiment check-ins** — EXP-001 flow holdout analyses at wk4 (14 Sep), wk8 (12 Oct),
wk10 (26 Oct 2026). ⚠️ These were `send_later` timers on the OLD account's session — they will
NOT fire elsewhere. Recreate as Routines/calendar reminders on whichever account owns them.

**D. PR watching** — the working branch pushes to PR #11; subscribe the session to PR activity
if you want CI/review events.

## 5. Standing conventions (the contract)

- **Revenue basis:** Shopify `net_sales` (incl. GST, excl. shipping) for the daily scorecard;
  the EE model converts ex-GST via ×1.0437. GPAM% = (1−VCR)−MER; VCR 0.468 BAU / 0.503 sale;
  fixed $74,831/mo; GPAM target 26%; MER ≤25% (≤28% sale months).
- **Scorecard columns** (persistent): Yesterday · 7-day avg · MTD · Target · Projected EOM ·
  Trend, + RPV row + live-experiments row. Spec: `data/DAILY-SCORECARD-FORMAT.md`.
- **No fabricated numbers, ever.** Missing spend → "ASSUMED"; missing data → ask.
- **PII:** raw order exports (emails/addresses) NEVER enter the repo. Aggregate outputs only.
  Customer joins use md5-hashed emails.
- **Experiments:** every experiment gets a pre-declared decision rule; re-check power before
  calling winners; log everything in `EXPERIMENT-LOG.md`, not chat.
- **Brand:** never use the phrase "we're diggin' it" (retired tagline).
- **Model identity** never goes into commits/PRs/artifacts.

## 6. Bootstrap prompt for the NEW account

Connect the GitHub repo + Shopify MCP connector first, then paste:

```
You are the DiggerLid Chief of Staff. Read, in order:
1. diggerlid-ops-hub/MIGRATION-BOOTSTRAP.md   (this file — system map)
2. diggerlid-ops-hub/LEARNINGS.md             (condensed knowledge base)
3. diggerlid-ops-hub/OBJECTIVES.md + WATCHLIST.md
4. diggerlid-ops-hub/data/DAILY-SCORECARD-FORMAT.md
5. diggerlid-ops-hub/experiments/EXPERIMENT-LOG.md (register + live experiments)
6. diggerlid-ops-hub/research/RESEARCH-PROJECTS.md (RP-001)
Then report: system status in one paragraph, live experiments, next scheduled obligations
(forecast Monday, EXP-001 check-ins), and wait for instructions.
Rules: never fabricate numbers; PII never in repo; commit durable state to the repo.
```

## 7. Team access model

- **Source of truth = this GitHub repo.** Give teammates repo access (read or write) via
  GitHub; their Claude accounts attach it with the GitHub connector.
- **Connectors are per-account:** each teammate connects their own Shopify MCP (+ any others
  they need). Access follows their GitHub/Shopify permissions — not shared keys.
- **Write discipline:** one branch per person (or PR-based flow into main). Two sessions
  pushing the same branch has already caused a force-update conflict once.
- **Read-only teammates:** the daily brief, dashboards and deliverables work fine from a
  read-only clone; only the Scorekeeper/CoS owner needs push access.
```
