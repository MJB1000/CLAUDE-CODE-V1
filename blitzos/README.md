# BlitzOS Context — `blitzos/`

Your personal **context monorepo**, built on the [BlitzOS](https://github.com/blitzdotdev/blitzos)
model: cloud agents that boot already knowing your work and keep going with your laptop closed.

It is **thin** — it pins your repos by reference and carries the shared work log. It never
vendors source code or credentials.

```
blitzos/
├── CLAUDE.md          # the context map — read this first (6 sections)
├── .gitmodules        # member repos pinned as gitlinks (source never vendored)
├── bootstrap.sh       # power-mode: init members with a fine-grained token
├── CLOUD-SETUP.md     # native-rail (zero-cred) + power-mode token setup
├── plan.json          # thin build plan: selected repos + connectors
├── docs/
│   └── conventions.md # advanced cross-repo conventions
└── sessions/
    ├── TEMPLATE.md    # copy this at the start of every cloud session
    └── 2026-07-14-bootstrap.md
```

## Launch an agent (native rail — recommended)

1. In Claude Code on the web, start a session and select this context repo.
2. The agent reads `CLAUDE.md`, then the latest `sessions/` entry, and works warm.
3. Add specific member repos to the session via the GitHub rail when it needs their source.

See `CLOUD-SETUP.md` for the token-based "power mode" alternative.

## Promote to a standalone private repo (optional)

This scaffold lives inside `CLAUDE-CODE-V1` so it wouldn't clobber that repo's existing
`CLAUDE.md`. To run it as a real BlitzOS context repo, lift `blitzos/` into its own **private**
repo:

```bash
# from the repo root
git subtree split --prefix=blitzos -b blitzos-context           # isolate blitzos/ history
# create an EMPTY private repo named blitzos-context on GitHub first, then:
git push git@github.com:MJB1000/blitzos-context.git blitzos-context:main
```

Or simply copy the `blitzos/` folder into a fresh private repo. Keep it **private** — it maps
your whole setup. Then update `plan.json` / `CLOUD-SETUP.md` if the owner or name changes.

## Maintenance

- Add/remove members: edit `.gitmodules` + `CLAUDE.md` §1 (steps in `docs/conventions.md`).
- One fine-grained token per repo **owner**. The `DigBoi2026` DiggerLid cluster needs its own
  context — don't fold it into the MJB1000 token.
- Log every cloud session under `sessions/`. That log is the point: work compounds instead of
  evaporating.

---
Modeled on BlitzOS by blitzdotdev. This is a personal instance, not a fork of their tooling.
