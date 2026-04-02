# Marketing Team

A structured AI marketing framework with three specialized agents — **Strategist**, **Copywriter**, and **Designer** — working through disciplined handoffs to produce on-brand, on-strategy content.

Adapted from [Three Man Team](https://github.com/russelleNVy/three-man-team) by russelleNVy.

---

## How It Works

```
Strategist (plan) → Copywriter (write) → Designer (review) → Strategist (publish)
```

Each agent has a defined role, reads only what it needs, and communicates through structured handoff files. Nothing publishes without sign-off from both the Strategist and the Creative Director (you).

## The Three Roles

| Role | Job | Equivalent |
|---|---|---|
| **Strategist** | Plans campaigns, writes briefs, owns the launch gate | Architect |
| **Copywriter** | Writes content based on strategy briefs | Builder |
| **Designer** | Reviews for brand, audience, clarity, and channel fit | Reviewer |

## Handoff Files

| File | Written by | Read by |
|---|---|---|
| `STRATEGY-BRIEF.md` | Strategist | Copywriter, Designer |
| `REVIEW-REQUEST.md` | Copywriter | Designer |
| `REVIEW-FEEDBACK.md` | Designer | Copywriter, Strategist |
| `CAMPAIGN-LOG.md` | All (Strategist owns) | All |
| `SESSION-CHECKPOINT.md` | Strategist | All |

## Quick Start

1. Clone this repo into your project or `~/.claude/skills/`
2. Copy `config/team.yml.example` → `config/team.yml`
3. Customize agent personas in `agents/`
4. Copy handoff templates from `handoff/` to your project root
5. Start a session and spin up the Strategist

See [INSTALL.md](INSTALL.md) for detailed setup.

## Workflow

1. **Strategist** talks with the Creative Director, identifies the need, writes `STRATEGY-BRIEF.md`
2. **Copywriter** reads the brief, writes the content, submits `REVIEW-REQUEST.md`
3. **Designer** reviews against brand, audience, and brief — writes `REVIEW-FEEDBACK.md`
4. **Copywriter** addresses feedback, re-submits if needed
5. **Strategist** confirms with Creative Director, publishes, logs to `CAMPAIGN-LOG.md`

## Token Discipline

Five rules baked into every session:
- Trust skills/memory — skip redundant reads
- Kill speculative tool calls
- Parallelize independent operations
- Route verbose output to subagents
- Never restate what was already said

## Customization

- [Customizing Your Team](docs/customizing-your-team.md) — personas, domains, brand assets
- [Token Optimization](docs/token-optimization.md) — efficiency patterns for marketing

## Why Three?

Research shows structured teams of 3-5 agents with defined handoffs outperform solo agents and larger teams. Three is the sweet spot: meaningful review with minimal coordination overhead. See [METHODOLOGY.md](METHODOLOGY.md).

## License

MIT — adapted from [Three Man Team](https://github.com/russelleNVy/three-man-team).
