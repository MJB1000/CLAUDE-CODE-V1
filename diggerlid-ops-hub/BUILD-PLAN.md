# Build Plan — DiggerLid Ops Hub on Paperclip

Phased so value lands early and safely. Human-in-the-loop from day one: read-first, draft-only,
approval gate on outbound. Don't block the hub on the two missing wires (Meta, Klaviyo) — launch on
live Shopify + the EE baseline, MER/CAC as labelled manual inputs until wired.

## Phase 0 — Decisions & prerequisites
- [ ] **GPAM target:** adopt ≥28%, or keep 40% + open a cost-structure workstream (see OBJECTIVES).
- [ ] **Backfill FY25/26 revenue** → commit "+20%" to a dollar plan (fills EE Aug–Dec).
- [ ] **Pick host:** Railway / Fly / VM. Postgres on Supabase.
- [ ] **Repo home:** promote this folder to a private `diggerlid-ops-hub` under DigBoi2026 (optional now).
**Exit:** targets are real numbers; host + repo chosen.

## Phase 1 — Chief of Staff, solo (MVP) · ~week 1
- [ ] Deploy Paperclip on host → Supabase Postgres → dashboard up → telemetry off.
- [ ] Create company **DiggerLid**; add Shopify token to the secret store.
- [ ] Hire **Chief of Staff** (Claude Code adapter, context-repo workspace, budget, outbound-approval, read-only scopes).
- [ ] Load specs + `ee-baseline.json` into its workspace.
- [ ] Share the Projects & Experiments board to the connected account for board hygiene.
- [ ] Routines: Mon 07:00 scorecard + agenda; daily scorecard refresh (alerts only).
**Deliverable:** a real Monday brief + daily scorecard, drafted, awaiting approval.
**Exit:** one full week's brief reviewed and trusted.

## Phase 2 — Close the data gaps · ~week 2–3
- [ ] **Meta** System User token (`ads_read`) → secret store → daily spend/ROAS/CPP → live MER, CAC.
- [ ] **Klaviyo** private key → flow/campaign revenue + list growth → retention (Obj 5).
- [ ] **Per-SKU COGS** (Shopify Admin `InventoryItem.unitCost`) → sharpen GPAM.
- [ ] **Data layer:** Supabase schema storing EE baseline + daily actuals; month-end writeback.
**Deliverable:** morning scorecard with MER, GPAM, ROAS, CAC, retention — no manual inputs.
**Exit:** a full week with no metric flagged "unmeasured."

## Phase 3 — The cabinet · ~week 3–5
- [ ] Hire **Scorekeeper** (daily; owns the six-metric pull + decompositions + alerts).
- [ ] Hire **Launch Marshal** — **first job: Zip Mat (Aug 5) T-pack**, then Father's Day (Aug 26).
- [ ] Hire **Voice of Customer** (weekly; insight ledger + monthly Friction Report).
- [ ] Set budgets, reporting lines, read-only scopes. CoS synthesises; you still get one brief, ≤3 decisions.
**Exit:** a major launch runs through the Marshal end-to-end (prep → go/no-go → hot-wash).

## Phase 4 — Oversight & CRM · ~week 5+
- [ ] Stand up the **Watchlist** register + escalation matrix; turn on the seven watch duties.
- [ ] **Migrate the DL CRM** off the local Cowork artifact → cloud store → CoS ages threads, drafts follow-ups.
**Exit:** an aged watch item and a stale partner thread both surface automatically.

## Governance (all phases)
Approval policy on outbound · budgets are hard caps · pause/terminate always available · all CD
decisions logged · every agent passes the board gate or is killed · MJB1000 as a second company only
after DiggerLid is stable.

## Forcing function
**Zip Mat launches Aug 5** — natural deadline to have Phase 1 (CoS) done and the Marshal (Phase 3)
live by early August.
