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
| `RETRO.md` | Strategist (post-publish) | All |
| `DESIGN-BRIEF.md` | Strategist (after copy approved) | Designer |
| `DESIGN-REQUEST.md` | Designer (Figma output) | Strategist |
| `PLAYBOOK.md` | Strategist | Strategist (at project start) |

## Quick Start

1. Clone this repo into your project or `~/.claude/skills/`
2. Copy `config/team.yml.example` → `config/team.yml`
3. Customize agent personas in `agents/`
4. Copy handoff templates from `handoff/` to your project root
5. Start a session and spin up the Strategist

See [INSTALL.md](INSTALL.md) for detailed setup.

## Repository Structure

```
marketing-team/
├── agents/                    # Agent definitions (generic, customizable)
│   ├── STRATEGIST.md
│   ├── COPYWRITER.md
│   └── DESIGNER.md
├── config/
│   └── team.yml.example       # Team names, publish targets, brand assets
├── docs/
│   ├── customizing-your-team.md
│   └── token-optimization.md
├── examples/
│   ├── session-start.md       # Copy-paste session prompts
│   └── campaign-walkthrough.md # Full deliverable from brief to publish
├── handoff/                   # Inter-agent handoff templates
│   ├── STRATEGY-BRIEF.md
│   ├── REVIEW-REQUEST.md
│   ├── REVIEW-FEEDBACK.md
│   ├── CAMPAIGN-LOG.md
│   ├── SESSION-CHECKPOINT.md
│   ├── DESIGN-BRIEF.md
│   ├── DESIGN-REQUEST.md
│   └── RETRO.md
├── skills/
│   ├── token-optimizer.md     # 5 behavioral rules for token discipline
│   ├── notion-publish.md      # Format templates for Notion publishing
│   ├── notion-knowledge.md    # Shared knowledge layer (Notion databases)
│   ├── brief-quality.md       # 10-point brief scoring rubric
│   ├── research.md            # Market/competitor intelligence via web
│   └── design-systems.md      # DESIGN.md integration for visual production
├── design-systems/            # Client visual systems (DESIGN.md format)
├── clients/                   # Client profiles (persist across campaigns)
├── knowledge/
│   ├── CHANNELS.md            # Channel constraints + patterns (grows over time)
│   └── SWIPE-FILE.md          # Copy reference library (grows over time)
├── deliverables/              # Published content artifacts
├── retros/                    # Retrospective archive (one per deliverable)
├── templates/
│   ├── project-folder/        # Named personas (Sofia, Charlie, Dana)
│   └── generic/               # Blank slate with [CUSTOMIZE] placeholders
├── CLAUDE.md                  # Session router — token rules, file loading
├── METHODOLOGY.md             # Framework philosophy and research
├── INSTALL.md                 # Installation guide
├── PLAYBOOK.md                # Cross-campaign memory (validated/observed patterns)
├── CHANGELOG.md               # Version history
├── README.md
└── setup                      # Installation script
```

## Templates

Two starting points:
- **`templates/project-folder/`** — Named personas (Sofia the Strategist, Charlie the Copywriter, Dana the Designer) with full backstories ready to use
- **`templates/generic/`** — Clean slate with `[CUSTOMIZE THIS SECTION]` placeholders for your own personas

## Workflow

1. **Strategist** talks with Creative Director, writes `STRATEGY-BRIEF.md` (with split DoD)
2. **Copywriter** writes plan, gets approval, writes content, self-checks DoD, submits `REVIEW-REQUEST.md`
3. **Designer** reviews (Round 1), locks passing sections, writes `REVIEW-FEEDBACK.md`
4. **Copywriter** fixes must-fix items, re-submits with change log
5. **Designer** reviews only changed sections (Round 2), clears
6. **Strategist** presents to CD, logs decision, publishes, writes `RETRO.md`
7. **Strategist** checks metrics at 7 days and 30 days, updates `PLAYBOOK.md`

### Learning Loop
```
Publish → Retro (day 0) → 7-day metrics → 30-day metrics → Playbook updated → Next brief informed
```

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
