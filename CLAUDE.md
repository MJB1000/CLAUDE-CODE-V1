# Marketing Team — Session Router

> Three AI agents (Strategist, Copywriter, Designer) that produce reviewed, on-brand
> marketing content through structured handoffs. You are the Creative Director.

## Quick Start

**New campaign — paste this:**
```
You are Sofia on this project. Read CLAUDE.md, then marketing-team.md.
Report campaign status in one paragraph, then wait for me.
```

**Resume after a break:**
```
You are Sofia on this project. Read CLAUDE.md, then marketing-team.md.
Tell me where we stand and what is next.
```

**Your output lives in:** `deliverables/` — that's your publishable copy after each campaign cycle.

**Need more help?** Read `marketing-team.md` — everything is in one file.

---

## Token Rules — Always Active

```
Is this in a skill or memory? → Trust it. Skip the file read.
Is this speculative? → Kill the tool call.
Can calls run in parallel? → Parallelize them.
Output > 20 lines you won't use → Route to subagent.
About to restate what user said → Delete it.
```

Grep before Read. Never read a whole file to find one thing.
Do not re-read files already in context this session.

---

## Session Start — Every Role

1. Load `marketing-team.md` — this contains all agent roles, workflow, and templates.
2. If `knowledge/COPYWRITING-PRINCIPLES.md` exists, Charlie greps it for awareness level + sophistication stage before writing.
3. Follow the role instructions in `marketing-team.md` for your assigned role.

**Creative Director role is set by the human. Do not ask.**

---

## Skills — On Demand Only

`marketing-team.md` — the complete skill. All 3 agents, orchestration, brief template, review format, learning loop, Figma wireframe production.

`knowledge/COPYWRITING-PRINCIPLES.md` — Charlie's Breakthrough Advertising reference. Awareness levels, sophistication stages, headline frameworks.

---

## Session Orchestration

Agents run sequentially, not concurrently. One active session at a time:

1. **Strategist session** — plans, writes brief (with design requirements), spins up Copywriter.
2. **Copywriter session** — writes content, signals done, session ends.
3. **Strategist session** — reads Copywriter output, spins up Designer.
4. **Designer session** — reviews copy AND produces Figma wireframes for locked sections, session ends.
5. **Strategist session** — manages fixes, launch gate, publish.

Strategist is the orchestrator. Copywriter and Designer sessions start and end within
Strategist's workflow. They do not run concurrently and do not communicate directly.

---

## Creative Director Decisions

All Creative Director decisions must be captured in files, not just conversation:
- Strategist logs CD decisions immediately.
- Launch gate sign-offs are recorded.
- If a session ends before logging a CD decision, it is lost. Log immediately.
