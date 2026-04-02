# Marketing Team — Session Router

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

1. Load `skills/token-optimizer.md` — first, before anything else.
2. Check `SESSION-CHECKPOINT.md` — if dated within 7 days, read it. That is your state.
3. Load your role file: `agents/STRATEGIST.md` · `agents/COPYWRITER.md` · `agents/DESIGNER.md`
4. If no checkpoint — Strategist reads `CAMPAIGN-LOG.md` + `STRATEGY-BRIEF.md` only.
5. If `STRATEGY-BRIEF.md` is a blank template, skip it.

**Creative Director role is set by the human. Do not ask.**

---

## Reference Files — On Demand Only

| File | Load when |
|---|---|
| Campaign spec | Strategist needs it; checkpoint doesn't cover it |
| STRATEGY-BRIEF.md | Copywriter and Designer load at task start |
| CAMPAIGN-LOG.md | Strategist checks status; Copywriter updates when done |
| REVIEW-REQUEST.md | Designer loads at review start |
| REVIEW-FEEDBACK.md | Copywriter loads after Designer signals done |

Add project-specific reference files here as your campaign grows.

---

## Handoff Files

All team communication flows through files in `handoff/`:
- `STRATEGY-BRIEF.md` — Strategist writes, Copywriter reads
- `REVIEW-REQUEST.md` — Copywriter writes, Designer reads
- `REVIEW-FEEDBACK.md` — Designer writes, Copywriter reads
- `CAMPAIGN-LOG.md` — shared record, Strategist owns
- `SESSION-CHECKPOINT.md` — Strategist writes at session end
- `DESIGN-BRIEF.md` — Strategist writes (after copy approved), Designer reads
- `DESIGN-REQUEST.md` — Designer writes (Figma output), Strategist reads
- `RETRO.md` — Strategist writes after publish (never overwritten — one per deliverable)

Copy templates from `handoff/` into your project root to get started.

### Review Feedback Versioning

Designer appends to `REVIEW-FEEDBACK.md` rather than overwriting. Each round gets a
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

Add your marketing-specific skills below:
[your skills here]

---

## Session Orchestration

Agents run sequentially, not concurrently. One active session at a time:

1. **Strategist session** — plans, writes brief, spins up Copywriter as a sub-agent.
2. **Copywriter session** — writes content, signals done, session ends.
3. **Strategist session** — reads Copywriter output, spins up Designer as a sub-agent.
4. **Designer session** — reviews, writes feedback, session ends.
5. **Strategist session** — manages fixes, launch gate, publish.
6. **(Optional) Strategist session** — writes design brief, spins up Designer for Figma production.
7. **Designer session** — produces Figma designs from approved copy, session ends.

Strategist is the orchestrator. Copywriter and Designer sessions start and end within
Strategist's workflow. They do not run concurrently and do not communicate directly.

---

## Creative Director Decisions

All Creative Director decisions must be captured in files, not just conversation:
- Strategist logs CD decisions to `CAMPAIGN-LOG.md` under Brand & Strategy Decisions.
- Launch gate sign-offs are recorded in `CAMPAIGN-LOG.md` under the deliverable entry.
- If a session ends before logging a CD decision, it is lost. Log immediately.
