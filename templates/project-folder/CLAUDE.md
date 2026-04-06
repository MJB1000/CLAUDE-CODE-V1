# [Project Name] — Session Router
*[Your Name] — [your-brand.com] — Confidential*

> Three AI agents (Strategist, Copywriter, Designer) that produce reviewed, on-brand
> marketing content through structured handoffs. You are the Creative Director.

## Quick Start

**New campaign — paste this:**
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
Report campaign status in one paragraph, then wait for me.
```

**Resume after a break:**
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md, then CAMPAIGN-LOG.md.
Tell me where we stand and what is next.
```

**Your output lives in:** `deliverables/` — that's your publishable copy after each campaign cycle.

**Need more help?** Read `HOW-TO-GET-STARTED.md` — everything else is optional.

---

## Token Rules — Always Active

```
Is this in a skill or memory?   → Trust it. Skip the file read.
Is this speculative?            → Kill the tool call.
Can calls run in parallel?      → Parallelize them.
Output > 20 lines you won't use → Route to subagent.
About to restate what user said → Delete it.
```

Grep before Read. Never read a whole file to find one thing.
Do not re-read files already in context this session.

---

## Session Start — Every Role

1. Load `skills/token-optimizer.md` — first, before anything else.
2. Check `SESSION-CHECKPOINT.md` — if dated within 7 days, read it. That is your state.
3. Load your role file: STRATEGIST.md · COPYWRITER.md · DESIGNER.md
4. If no checkpoint — Sofia reads `CAMPAIGN-LOG.md` + `STRATEGY-BRIEF.md` only.
5. If `STRATEGY-BRIEF.md` is a blank template, skip it.

Creative Director is [Your Name]. Do not ask their role.

---

## Reference Files — On Demand Only

| File | Load when |
|---|---|
| Campaign spec | Sofia needs it; checkpoint doesn't cover it |
| STRATEGY-BRIEF.md | Charlie and Dana load at task start |
| CAMPAIGN-LOG.md | Sofia checks status; Charlie updates when done |
| REVIEW-REQUEST.md | Dana loads at review start |
| REVIEW-FEEDBACK.md | Charlie loads after Dana signals done |
| DESIGN-BRIEF.md | Dana loads at design production start |
| DESIGN-REQUEST.md | Sofia reads after Dana completes Figma work |

| `clients/[name].md` | Sofia loads at session start for returning clients |
| `knowledge/CHANNELS.md` | Charlie loads channel section when writing |
| `knowledge/SWIPE-FILE.md` | Charlie greps for channel/audience when writing |

Add project-specific reference files here as your campaign grows.

---

## Handoff Files

All team communication flows through files in `handoff/`:
- `STRATEGY-BRIEF.md` — Sofia writes, Charlie reads
- `REVIEW-REQUEST.md` — Charlie writes, Dana reads
- `REVIEW-FEEDBACK.md` — Dana writes, Charlie reads
- `CAMPAIGN-LOG.md` — shared record, Sofia owns
- `SESSION-CHECKPOINT.md` — Sofia writes at session end
- `DESIGN-BRIEF.md` — Sofia writes (after copy approved), Dana reads
- `DESIGN-REQUEST.md` — Dana writes (Figma output), Sofia reads
- `RETRO.md` — Sofia writes after publish (never overwritten — one per deliverable)

Copy templates from `handoff/` into your project root to get started.

### Review Feedback Versioning

Dana appends to `REVIEW-FEEDBACK.md` rather than overwriting. Each round gets a
dated section header (`## Round N — [date]`). This preserves review history for
retrospectives and learning.

## Deliverable Artifacts

Store deliverable files in `deliverables/`:
```
deliverables/01-landing-page.md
deliverables/02-email-sequence.md
deliverables/03-social-ads.md
```

---

## Skills — On Demand Only

Load the skill the task needs. Not at session start.

`skills/token-optimizer.md` — always first. Controls how the team reads, thinks, and responds.

`skills/notion-publish.md` — load when publishing deliverables to Notion.

`skills/design-systems.md` — load when Dana is producing visual assets. References DESIGN.md files in `design-systems/`.

`skills/research.md` — load when Sofia needs market/competitor intelligence before writing a brief.

`skills/notion-knowledge.md` — load when querying or updating the team's shared knowledge in Notion (clients, patterns, swipe file, campaign tracker).

`skills/brief-quality.md` — load after writing a brief, before spinning up Charlie. Scores brief 0-10.

Add your marketing-specific skills below:
[your skills here]

---

## Session Orchestration

Agents run sequentially, not concurrently. One active session at a time:

1. **Sofia session** — plans, writes brief, spins up Charlie as a sub-agent.
2. **Charlie session** — writes content, signals done, session ends.
3. **Sofia session** — reads Charlie's output, spins up Dana as a sub-agent.
4. **Dana session** — reviews, writes feedback, session ends.
5. **Sofia session** — manages fixes, launch gate, publish.
6. **(Optional) Sofia session** — writes design brief, spins up Dana for Figma production.
7. **Dana session** — produces Figma designs from approved copy, session ends.

Sofia is the orchestrator. Charlie and Dana sessions start and end within
Sofia's workflow. They do not run concurrently and do not communicate directly.

---

## Creative Director Decisions

All Creative Director decisions must be captured in files, not just conversation:
- Sofia logs CD decisions to `CAMPAIGN-LOG.md` under Brand & Strategy Decisions.
- Launch gate sign-offs are recorded in `CAMPAIGN-LOG.md` under the deliverable entry.
- If a session ends before logging a CD decision, it is lost. Log immediately.
