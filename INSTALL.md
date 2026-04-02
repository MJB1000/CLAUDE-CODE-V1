# Installing Marketing Team

## Global Install — All Your Projects

Marketing Team installs into `~/.claude/skills/marketing-team` and is available in every project.

```bash
git clone <this-repo> ~/.claude/skills/marketing-team
```

Then add to your global `~/.claude/CLAUDE.md`:
```
## Marketing Team
Available agents: /strategist, /copywriter, /designer
Token rules always active — see marketing-team/CLAUDE.md
```

## Per-Project Install

Marketing Team installs into `.claude/skills/marketing-team` inside your repo and only applies to that project.

```bash
git clone <this-repo> .claude/skills/marketing-team
```

Add to your project's `CLAUDE.md`:
```
## Marketing Team
Available agents: /strategist, /copywriter, /designer
```

## Quick Start

1. Copy `config/team.yml.example` to `config/team.yml` and customize.
2. Copy handoff templates from `handoff/` into your project root.
3. Edit the **Who You Are** section in each agent file under `agents/`.
4. Start a session and load the Strategist role.

## VS Code / Cursor / Codex

Marketing Team uses the SKILL.md standard and works with any agent that supports context files.
Copy the `agents/` directory and `CLAUDE.md` into your project root.

## Requirements

- Claude Code CLI (for slash command support)
- Git
- Any agent supporting CLAUDE.md / SKILL.md context (for other tools)
