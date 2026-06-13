# 🛰️ Repo Radar

Finds **new GitHub repos that are gaining stars fast** in the areas you actually
work in — AI agents & LLM tooling, multimodal AI, marketing/analytics tech, and
your web/app dev stack. Runs itself weekly and hands you a ranked digest.

Your interests were inferred from your repos (`CLAUDE_MEMORY`,
`knowledge-vault-mcp-server`, `claude-mcp-setup`, `video-vision`,
`MEETING-EMOTION-ANALYSER`, `marketing-team`, `wipertech-comment-dashboard`,
`session-signal`, `family-dashboard` …). Edit `interests.yml` anytime to retune.

## How it works

1. A scheduled GitHub Action (`.github/workflows/repo-radar.yml`) runs every
   **Monday 08:00 UTC** (and on-demand from the Actions tab).
2. `radar.py` reads `interests.yml`, runs each theme's search queries against the
   GitHub Search API, filtered to repos **created in the last 120 days** with
   **≥50★**.
3. Results are **ranked by momentum** — *stars per day* since creation — so a
   3-week-old repo at 1.8k★ beats a stale one that's been coasting.
4. Anything already in `seen.json` is dropped, so each digest shows only repos
   you haven't been shown before.
5. The digest is written to `digests/YYYY-MM-DD.md` (+ `digests/latest.md`),
   committed back to the repo, and posted as a **GitHub issue** you can read.

## Tuning it — `interests.yml`

```yaml
settings:
  created_within_days: 120   # how "new" a repo must be
  min_stars: 50              # noise floor — raise to be pickier
  per_theme: 6               # how many repos per theme per digest
  languages: []              # e.g. [Python, TypeScript] to restrict
  exclude_owners: [MJB1000]  # skip your own repos
  exclude_keywords: [awesome, roadmap, ...]   # kill listicles/courses

themes:
  - name: AI agents & LLM tooling
    queries:
      - "topic:mcp"
      - "claude anthropic in:name,description,readme"
      # add/remove queries freely — GitHub repo-search syntax
```

Each query gets `created:>=<date> stars:>=<min_stars>` appended automatically.

## Running it yourself

```bash
pip install pyyaml
GITHUB_TOKEN=<your_token> python repo-radar/radar.py     # writes a digest
python repo-radar/radar.py --selftest                    # offline sanity check
```

`GITHUB_TOKEN` is optional for searching (it just raises rate limits) but
required to open the issue. In CI the Action supplies it automatically.

## Files

| File | Purpose |
|---|---|
| `interests.yml` | What to hunt for. **This is the knob you turn.** |
| `radar.py` | The search + rank + digest engine (stdlib + PyYAML only). |
| `seen.json` | Memory of repos already surfaced — prevents repeats. |
| `digests/` | Dated digests; `latest.md` always mirrors the newest. |

## Want a different delivery channel?

The engine already produces clean markdown. Easy follow-ups if you want them:
email the digest via the Gmail integration, push it to a Notion "Repo Radar"
page, or post to Slack — say the word and I'll wire it in.
