# Running the Ops Hub on Paperclip

Paperclip is a self-hosted Node + React orchestrator (MIT). It's **task-centric, not a chat**: you
assign tickets, it wakes on a heartbeat, works under a budget, and you review the result.

## Install
Prereqs: Node 20+, pnpm 9.15+, a **persistent host** (Railway / Fly / VM — not Vercel; heartbeats
need an always-on process). Postgres via Supabase for production.
```bash
npx paperclipai onboard --yes          # guided
# or
git clone https://github.com/paperclipai/paperclip.git && cd paperclip
pnpm install && pnpm dev                # API + UI at http://localhost:3100
```
Disable telemetry: `PAPERCLIP_TELEMETRY_DISABLED=1`. Config via `paperclipai configure`.

## Stand up the DiggerLid company
1. Create company **DiggerLid** (Paperclip is multi-company; MJB1000 can be a second one later).
2. Add company secrets (encrypted store): Shopify token now; Meta/Klaviyo keys at Phase 2.
3. Hire the **Chief of Staff** (see `agents/CHIEF-OF-STAFF.md`) — Claude Code adapter, workspace =
   BlitzOS context repo, monthly budget, **approval policy on all outbound**, read-only tool scopes.
4. Load specs into its workspace: `OBJECTIVES.md`, `agents/*.md`, `data/ee-baseline.json`, `WATCHLIST.md`.
5. Routines: **Mon 07:00 → scorecard + meeting brief**; **daily → scorecard refresh (alerts only)**.
6. After it's trusted, hire **Scorekeeper, Launch Marshal, Voice of Customer** reporting to the CoS.

## Observe
Dashboard (+ mobile): **activity log** (actions, heartbeats, cost, approvals, work products),
**ticket board**, **org chart**, **budget/cost tracking** per agent. No live console — read events
and work products.

## Interact
Assign tickets · comment on issues to steer · approve at review gates · set per-agent budgets (hard
caps) · pause/terminate anytime · Routines for recurring work.

## Day-one safety
Approval policy on every outbound action · conservative budgets · secrets in the company store only
· start read-only (write limited to the agent's own drafts/scorecard/board).

See `roles.seed.json` for a design seed of the four roles — map its fields to Paperclip's actual
role API at deploy (it is a plan, not Paperclip's schema).
