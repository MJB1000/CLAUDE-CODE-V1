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

1. Load your token-optimizer skill if you have one — first, before anything else.
2. Check `SESSION-CHECKPOINT.md` — if dated within 7 days, read it. That is your state.
3. Load your role file: `agents/STRATEGIST.md` · `agents/COPYWRITER.md` · `agents/DESIGNER.md`
4. If no checkpoint — Strategist reads `CAMPAIGN-LOG.md` + `STRATEGY-BRIEF.md` only.

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

Copy templates from `handoff/` into your project root to get started.

---

## Skills — On Demand Only

Load the skill the task needs. Not at session start.

`token-optimizer` — always first. Controls how the team reads, thinks, and responds.

Add your marketing-specific skills below:
[your skills here]
