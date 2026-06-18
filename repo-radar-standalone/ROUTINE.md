# The Claude Code curation routine

The GitHub Action (`.github/workflows/radar.yml`) does the *scouting* — it finds
repos and commits a raw digest on **Mon, Wed & Sat at 08:00 AEST** (Sun/Tue/Fri
22:00 UTC). This routine adds the *judgment*: a Claude session reads the fresh
digest and emails you a curated shortlist of what actually matters. Two ways to
run it.

---

## Path 1 — scheduled Claude Code session (recommended)

In Claude Code on the web: connect this repo, then create a **scheduled Action**.

- **Schedule:** `0 23 * * 0`, `0 23 * * 2`, `0 23 * * 5` (Sun/Tue/Fri 23:00 UTC =
  Mon/Wed/Sat 09:00 AEST — one hour after the radar Action commits the digest).
- **Repo / branch:** `MJB1000/repo-radar` · `main`
- **Connectors:** enable **Gmail** (to draft the email). GitHub is in scope.
- **Network policy:** one that allows GitHub + Google APIs.

Paste this as the prompt:

```
You are my Repo Radar curator for the MJB1000/repo-radar repo, run Mon/Wed/Sat.
A GitHub Action runs Mon, Wed & Sat at 08:00 AEST and commits a fresh digest to
digests/latest.md. Your job runs after it and adds the judgment the script
can't. Work read-only: do NOT commit, push, or open PRs.

Steps:
1. Read digests/latest.md. If it's missing or older than 5 days, run
   `python radar.py --selftest` to confirm the script is healthy, then read the
   newest file in digests/.
2. Read watchlist.md and interests.yml for my priorities.
3. From the digest, pick the 5-8 repos that genuinely matter to me this week.
   Priority order:
     (a) Meta inbox / omnichannel AI agents that classify, route, and draft
         initial replies — anything for triaging customers vs influencer/collab
         prospects across Messenger/Instagram/WhatsApp.
     (b) Claude & agent design craft — skills, subagents, prompt/context
         engineering, evals.
     (c) Self-development / PKM tooling.
     (d) Customer-service and community/social AI agents.
   Ignore crypto/trading noise.
4. For each pick: one line on what it is + one line on why it matters to me or
   what I'd do with it. Flag any repo that could replace a custom build I'm
   weighing — especially the Meta-inbox classify/route/respond stack.
5. Call out any NEW entrant in the Meta-inbox niche measured against the
   watchlist.md baseline. That's the highest-signal event of the week.
6. Create a Gmail draft to matthewjbedwell@gmail.com, subject
   "Repo Radar — curated <today's date>", body = the curated brief in clean
   markdown. Leave it as a DRAFT; do not send.
7. End your reply with the shortlist and the single action you'd recommend.
```

The prompt is self-contained — scheduled sessions start fresh.

---

## Path 2 — GitHub Action that calls Claude (fully in-repo)

If you'd rather it live entirely in the repo with no web-UI step, add a second
workflow using the official Claude Code action. This needs an
`ANTHROPIC_API_KEY` repo secret (a scheduled Action can't use a Claude
subscription). Treat the snippet below as a **starting template — test a manual
run before trusting the schedule**:

```yaml
name: Repo Radar — curate
on:
  schedule:
    - cron: "0 23 * * 0"    # Mon 09:00 AEST — 1h after the scout run
    - cron: "0 23 * * 2"    # Wed 09:00 AEST — 1h after the scout run
    - cron: "0 23 * * 5"    # Sat 09:00 AEST — 1h after the scout run
  workflow_dispatch: {}
permissions:
  contents: read
jobs:
  curate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Read digests/latest.md and watchlist.md. Pick the 5-8 repos that
            matter most for: Meta-inbox/omnichannel AI agents (classify, route,
            respond; customers vs influencer prospects); Claude & agent design
            craft; self-development; customer-service/community AI. Ignore
            crypto/trading. For each: what it is + why it matters. Flag new
            Meta-inbox entrants vs the watchlist baseline. Output a clean
            markdown brief. Do not commit or push.
```

Email from Path 2 would need an extra send step (e.g. reuse the Gmail SMTP
secrets from the scout workflow) or have the action write the brief to a file
the scout job emails. Path 1 is simpler because the Claude session can draft
Gmail directly via the connector.
