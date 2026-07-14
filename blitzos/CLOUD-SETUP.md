# Cloud Setup — launching agents against this context

There are two ways to give a cloud agent access to the member repos. Prefer the first.

## A. Native rail (recommended — zero credentials)

Anthropic's GitHub integration selects the member repos for you at launch. No token
touches this repo or any VM. This is the default BlitzOS path.

1. In Claude Code on the web, start a new session and select the **`blitzos-context`**
   repository (this repo, once promoted to a standalone private repo — see `README.md`).
2. The agent reads `CLAUDE.md`, then the latest `sessions/` entry, and works warm.
3. When it needs a specific member repo's source, add that repo to the session via the
   GitHub rail. Source stays off BlitzOS servers.

## B. Power mode (bootstrap submodules yourself)

Only when you need the member repos checked out inside this monorepo (e.g. cross-repo
edits in one tree).

1. Create a **fine-grained personal access token** at
   https://github.com/settings/tokens?type=beta
   - Resource owner: **MJB1000**
   - Repository access: **Only select repositories** → the 15 member repos in `.gitmodules`
   - Permissions: **Contents: Read-only** (Read/Write only if the agent will push)
   - Short expiry (7–30 days).
2. Export it and run bootstrap — never paste it into a file in this repo:
   ```bash
   export BLITZOS_GIT_TOKEN=github_pat_xxxxx
   ./bootstrap.sh
   ```
3. `bootstrap.sh` refuses to run if it finds credential-like content committed here,
   uses the token only for its fetches, and never writes it into the repo.

## Token hygiene

- One token per **resource owner**. The `DigBoi2026` cluster (see `CLAUDE.md` §1) needs
  its own token / its own context repo — do not widen this token to cover it.
- Revoke and reissue on the expiry cadence above; treat any leaked token as burned.
- This repo must stay credential-free. `bootstrap.sh` enforces it; keep it that way.
