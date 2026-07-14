# Fleet conventions (advanced)

Cross-repo defaults for agents launched from this context. A member repo's own `CLAUDE.md`
always wins for that repo.

## Git
- Feature branches: `claude/<slug>-<id>`. Develop there; PR into `main`.
- Never push directly to `main`. Open PRs as **draft** after first push.
- Mirror `.github/pull_request_template.md` when a repo has one.

## Secrets
- No values in git, ever. `.env.example` / `.env.template` declare names only.
- This context repo stays credential-free — enforced by `bootstrap.sh`.

## Sessions
- One `sessions/` file per cloud session, append-only. Log before the container is reclaimed.
- Record: repos + branches touched, decisions, PRs, and a concrete handoff for the next agent.

## Adding a member repo
1. Add a `[submodule "..."]` stanza to `.gitmodules` (path `repos/<name>`, https url, `branch = main`).
2. Add a row to `CLAUDE.md` §1 with its workstream.
3. Keep the same resource owner as the token, or spin up a separate context.
4. Re-run `bootstrap.sh` (power mode) or just re-launch via the native rail.

## Removing / archiving
- Drop the `.gitmodules` stanza and the `CLAUDE.md` row. Move stale repos (e.g. 2025 and
  older) to the inventory note rather than pinning them.
