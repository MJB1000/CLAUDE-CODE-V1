# DiggerLid Ops Hub

An AI operating team for the **Head of Growth**, run on [Paperclip](https://github.com/paperclipai/paperclip).
It keeps the growth scorecard live, runs the weekly operating rhythm, keeps the projects board
honest, and each Monday hands the Head of Growth a short list of evidence-backed decisions.

> **It measures, prepares, remembers, and alerts. The Head of Growth decides.**
> It never sends, spends, or ships without approval.

## The org (v1)
```
YOU (Head of Growth) — decides
        │  Monday brief, ≤3 decisions
  CHIEF OF STAFF — synthesizes, remembers, runs cadence, enforces the gate
   ┌──────┼─────────────┐
SCOREKEEPER  LAUNCH MARSHAL  VOICE OF CUSTOMER
(the truth)  (the ship)      (the signal)
```

## What's here
```
diggerlid-ops-hub/
├── OBJECTIVES.md            # the six-metric scorecard: targets + floors (+ open GPAM decision)
├── BUILD-PLAN.md            # phased plan to stand it up on Paperclip
├── WATCHLIST.md             # oversight register + escalation matrix (nothing slips)
├── agents/
│   ├── CHIEF-OF-STAFF.md
│   ├── SCOREKEEPER.md
│   ├── LAUNCH-MARSHAL.md
│   └── VOICE-OF-CUSTOMER.md
├── data/
│   ├── ee-baseline.json     # parsed Ecommerce Equation model — the GPAM engine
│   └── SOURCES.md           # data-source registry: live vs to-wire, how each connects
└── paperclip/
    ├── SETUP.md             # how to run it on Paperclip (observe + interact)
    └── roles.seed.json      # design seed for the Paperclip roles (map to its API at deploy)
```

## Status of prerequisites (from BUILD-PLAN Phase 0)
- [ ] **GPAM target decision** — adopt ≥28%, or keep 40% + open a cost-structure workstream (see OBJECTIVES).
- [ ] **Backfill FY25/26 revenue** → commit the "+20%" to a dollar plan.
- [ ] **Pick a host** — Railway / Fly / VM (persistent, runs heartbeats). Postgres on Supabase.

## Ownership / promotion
Scaffolded in-tree for versioning. Intended home is a **private repo under DigBoi2026**
(`diggerlid-ops-hub`). Promote by lifting this folder into that repo (same pattern as `blitzos/`).
Member data (Shopify/Meta/Klaviyo keys) lives in the **hub's secret store**, never in this repo.

Modeled on the DiggerLid Operating System + Playing-to-Win strategy. Built to run on Paperclip; not a fork of it.
