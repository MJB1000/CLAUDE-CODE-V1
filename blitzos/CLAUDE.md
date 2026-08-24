# BlitzOS Context — matthewjbedwell

> Cloud agents that boot already knowing this work, and keep working with the laptop closed.
> This is a **thin context monorepo**: it pins member repos by reference (gitlinks) and carries
> the shared work log. It never vendors source code or credentials.

**Context repo host:** DigBoi2026 (github.com/DigBoi2026) · **Member repos owner:** MJB1000
· **Generated:** 2026-07-14

> Note: this context repo is hosted under the DigBoi2026 account, but every pinned member below
> is MJB1000-owned. The bootstrap token is therefore an **MJB1000**-scoped fine-grained token —
> repo hosting and member access are independent.

When you launch a cloud agent against this repo, read this file first, then read the latest file
in `sessions/`. That tells you what the fleet already did so your work compounds instead of
starting cold.

---

## 1. Repositories (member repos)

These are pinned as gitlinks in `.gitmodules`. `bootstrap.sh` initializes them with a
fine-grained token in the cloud (or Anthropic's native GitHub rail selects them at launch).
Source code and history stay in the member repos — this monorepo only points at them.

### Active core (pinned as submodules)

| Repo | Owner | Default | Workstream | What it is |
|---|---|---|---|---|
| `CLAUDE-CODE-V1` | MJB1000 | main | Marketing System | Marketing-team session router (Strategist/Copywriter/Designer) + Repo Radar |
| `marketing-team` | MJB1000 | main | Marketing System | Companion / public marketing-team assets |
| `repo-radar` | MJB1000 | main | Marketing System | Daily repo-activity digest tooling |
| `ACTUAL_BUDGET_V1` | MJB1000 | main | Family/Finance | Budgeting app |
| `family-finance` | MJB1000 | main | Family/Finance | Household finance tooling |
| `family-dashboard-app` | MJB1000 | main | Family/Finance | Family dashboard |
| `knowledge-vault` | MJB1000 | main | Knowledge | Personal knowledge base |
| `knowledge-vault-mcp-server` | MJB1000 | main | Knowledge | MCP server exposing the vault to agents |
| `BOOK_INGEST` | MJB1000 | main | Knowledge | Book/document ingestion pipeline |
| `framedrop` | MJB1000 | main | Video/Vision | Video tooling |
| `video-vision` | MJB1000 | main | Video/Vision | Vision/video analysis |
| `supereyesee` | MJB1000 | main | Video/Vision | Vision project |
| `CLAUDE_MEMORY` | MJB1000 | main | Claude Tooling | Cross-session memory store |
| `session-signal` | MJB1000 | main | Claude Tooling | Session signaling utility |
| `claude-mcp-setup` | MJB1000 | main | Claude Tooling | MCP setup / bootstrap |

### Separate-owner cluster (needs its own token/context)

BlitzOS pins one fine-grained token per resource owner. These are `DigBoi2026`-owned, so they
live in their own context — do not mix them into the MJB1000 token. Launch them as a second
BlitzOS context (`blitzos-context-diggerlid`) or add a second token.

| Repo | Owner | Workstream |
|---|---|---|
| `CREATIVEOS` | DigBoi2026 | DiggerLid |
| `digger-lid-marketing` | DigBoi2026 | DiggerLid |
| `diggerlid-countdown` | MJB1000 | DiggerLid |

### Inventory (available to pin, not currently in core)

`CHEXT`, `operator-system-builder`, `figma-edit-mcp-setup`, `MEETING-EMOTION-ANALYSER`,
`wipertech-comment-dashboard`, `wipertech-analytics-templates`, `figma-email-studio-recovery-20260405`,
`family-dashboard-app-recovery`, `family-finance` recoveries, `PERSONALPROJECT1`,
`park-it-melbourne-now` (last active 2025 — likely archive).

To add one: append a stanza to `.gitmodules`, add a row above, then re-run `bootstrap.sh`.

---

## 2. Relationships

- **Marketing System** — `CLAUDE-CODE-V1` is the hub (the CLAUDE.md session router). `marketing-team`
  mirrors public assets; `repo-radar` feeds it daily activity digests. Agents launched here should
  read `CLAUDE-CODE-V1/CLAUDE.md` before writing marketing deliverables.
- **Knowledge** — `knowledge-vault` is the data; `knowledge-vault-mcp-server` is the interface agents
  use to query it; `BOOK_INGEST` feeds it. If an agent needs recall, it goes through the MCP server,
  not by reading the vault repo directly.
- **Video/Vision** — `framedrop`, `video-vision`, `supereyesee` are sibling experiments; share
  conventions but no hard dependency yet.
- **Family/Finance** — `ACTUAL_BUDGET_V1`, `family-finance`, `family-dashboard-app` cover the same
  household domain; the dashboard consumes the finance data.
- **Claude Tooling** — `CLAUDE_MEMORY`, `session-signal`, `claude-mcp-setup` are cross-cutting; any
  workstream may depend on them for memory/MCP wiring.

---

## 3. Conventions

Evidence-based defaults observed across the member repos. Confirm per-repo `CLAUDE.md` when present
(it overrides this file for that repo).

- **Branching:** feature branches named `claude/<slug>-<id>`; develop there, PR into `main`. Never
  push straight to `main`.
- **PRs:** open as **draft** after the first push; mirror any `.github/pull_request_template.md`.
- **Default branch:** `main` across the fleet.
- **Secrets:** never commit values. `.env.example`/`.env.template` files declare variable *names*
  only. This context repo must stay credential-free (enforced by `bootstrap.sh` scanning).
- **Docs:** each repo owns a `CLAUDE.md`; treat it as the source of truth for that repo's workflow.
- **Session hygiene:** log decisions and PRs to `sessions/` before the container is reclaimed —
  unlogged work evaporates.

---

## 4. Available connectors

Connectors that agents in this fleet commonly use (wire per session as needed):

- **github** — repo/PR/issue access (also the native launch rail).
- **Notion** — knowledge + campaign tracking (marketing system).
- **Figma / Canva / Gamma** — design production (marketing/DiggerLid).
- **Google Drive / Gmail / Google Calendar** — docs, mail, scheduling.
- **Supabase / Vercel** — app backends + deploys (finance/dashboard/video apps).
- **Knowledge Vault / Knowledge Library** — recall via `knowledge-vault-mcp-server`.
- **Granola** — meeting transcripts.
- **Shopify** — commerce (DiggerLid).

Pin only what a given launch needs — fewer connectors, tighter scope.

---

## 5. Cross-repo workflows

- **Ship a marketing campaign:** launch against the Marketing System core → agent reads
  `CLAUDE-CODE-V1/CLAUDE.md`, drives the Strategist→Copywriter→Designer handoff, publishes to
  `deliverables/`, logs the cycle. `repo-radar` surfaces what changed since last time.
- **Knowledge-backed build:** any agent needing recall queries `knowledge-vault-mcp-server`; new
  source docs go through `BOOK_INGEST` → `knowledge-vault`.
- **Fleet status sweep:** open the latest `sessions/` entry to see which repos are working/quiet/done,
  then pick up the next item without re-discovering state.

---

## 6. Session logging

Every cloud agent records what it did so the next one starts warm.

- Copy `sessions/TEMPLATE.md` to `sessions/YYYY-MM-DD-<slug>.md` at the **start** of a session.
- Fill in as you go: repos touched, branch, decisions, PRs opened, and status (`working`/`quiet`/`done`).
- Commit the session file before the container is reclaimed. This log is the fleet's shared memory —
  it is the whole point of the context repo.
- Never overwrite a prior session file; one file per session, append-only history.
