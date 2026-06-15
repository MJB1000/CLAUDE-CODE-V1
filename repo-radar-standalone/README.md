# 🛰️ Repo Radar

Self-running GitHub trend radar. Finds **new repos that are gaining stars fast**
in the areas you actually work in, ranks them by momentum, writes a weekly
digest, emails it — and (optionally) has a Claude Code routine curate the digest
down to what matters for you.

## Interest lanes

Configured in `interests.yml` (edit anytime):

1. AI agents & LLM tooling
2. Multimodal AI
3. Marketing & analytics tech
4. Web/app dev stack
5. Self-development & productivity
6. Claude & agent design craft
7. Community & social media management
8. Customer-service AI agents
9. **Meta inbox & omnichannel AI agents** — Messenger/Instagram-DM/WhatsApp
   agents that classify, route, and draft initial replies (customers vs
   influencer prospects). See `watchlist.md` for the established baseline.

## How it works

1. A scheduled GitHub Action (`.github/workflows/radar.yml`) runs every
   **Monday 08:00 UTC** (and on-demand from the Actions tab).
2. `radar.py` reads `interests.yml`, runs each lane's search queries against the
   GitHub Search API, filtered to repos **created in the last 120 days** above a
   star floor (global `min_stars`, or a per-lane override).
3. Results are **ranked by momentum** — *stars per day* since creation.
4. Anything already in `seen.json` is dropped, so each digest is only new repos.
5. The digest is written to `digests/YYYY-MM-DD.md` (+ `digests/latest.md`),
   committed back, and **emailed to you**.
6. *(Optional)* A Claude Code routine reads the fresh digest and emails you a
   curated, opinionated shortlist. See **`ROUTINE.md`**.

## Set up email (once)

Add three repo secrets (**Settings → Secrets and variables → Actions**):

| Secret | Value |
|---|---|
| `GMAIL_USERNAME` | your full Gmail address |
| `GMAIL_APP_PASSWORD` | a Google **App Password** — <https://myaccount.google.com/apppasswords> (needs 2-Step Verification). Not your normal password. |
| `EMAIL_TO` | *(optional)* where to send; defaults to `GMAIL_USERNAME` |

Until set, the email step logs "not configured" and skips; the digest is still
committed to `digests/`.

## Run it yourself

```bash
pip install -r requirements.txt
GITHUB_TOKEN=<your_token> python radar.py     # writes a digest
python radar.py --selftest                    # offline sanity check
```

`GITHUB_TOKEN` is optional for searching (raises rate limits); the GitHub Action
supplies one automatically.

## Files

| File | Purpose |
|---|---|
| `interests.yml` | What to hunt for. **The knob you turn.** |
| `radar.py` | Search + rank + digest engine (stdlib + PyYAML only). |
| `seen.json` | Memory of repos already surfaced — prevents repeats. |
| `watchlist.md` | Baseline of known players in the Meta-inbox niche. |
| `digests/` | Dated digests; `latest.md` mirrors the newest. |
| `ROUTINE.md` | The Claude Code curation routine — prompt + setup. |
