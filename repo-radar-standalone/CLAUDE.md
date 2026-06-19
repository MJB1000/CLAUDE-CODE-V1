# Repo Radar — project context for Claude

This repo is a self-running GitHub trend radar. A scheduled GitHub Action runs
`radar.py` daily, which searches GitHub for new, fast-rising repos in the
interest lanes defined in `interests.yml`, ranks them by momentum (stars/day),
and writes a digest to `digests/`. A Claude Code routine (see `ROUTINE.md`) then
curates that digest into an emailed shortlist.

## What you'll be asked to do here

Usually one of:
- **Curate the daily digest** — read `digests/latest.md`, pick what matters,
  draft an email. This is the routine in `ROUTINE.md`; follow it exactly.
- **Tune the radar** — add/remove lanes or queries in `interests.yml`, adjust
  star floors. After any change, run `python radar.py --selftest` (offline) to
  confirm the script still parses and renders.
- **Add a delivery channel** — the engine emits clean markdown; wiring it to
  Notion/Slack is a small follow-up.

## Owner's priorities (for curation)

In rough order: (1) Meta-inbox / omnichannel AI agents that classify, route, and
draft initial replies — customers vs influencer/collab prospects across
Messenger/Instagram/WhatsApp; (2) Claude & agent design craft (skills, subagents,
prompt/context engineering, evals); (3) self-development / PKM tooling;
(4) customer-service and community/social AI agents. Ignore crypto/trading noise.

## Working rules

- `radar.py` is stdlib + PyYAML only — keep it dependency-free.
- Don't commit `digests/`, `seen.json`, or `stars.json` by hand; the Action owns those.
- `seen.json` is the de-dupe memory — never clear it unless deliberately
  re-seeding, or the next digest will repeat everything.
- `stars.json` is the rolling star-count history powering the 7-day "rising fast"
  group. Clearing it just resets that signal to the cold-start proxy for a week.
- Grep before Read; don't re-read files already in context.
- `watchlist.md` is the human baseline for the Meta-inbox lane — new entrants are
  measured against it.

## Quick commands

```bash
python radar.py --selftest                 # offline sanity check (no network)
GITHUB_TOKEN=<token> python radar.py       # full run → writes a digest
```
