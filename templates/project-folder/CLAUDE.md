# [Project Name] — Session Router
*[Your Name] — [your-brand.com] — Confidential*

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

1. Load token-optimizer skill — first, before anything else.
2. Check SESSION-CHECKPOINT.md — if dated within 7 days, read it. That is your state.
3. Load your role file: STRATEGIST.md · COPYWRITER.md · DESIGNER.md
4. If no active checkpoint — Strategist reads CAMPAIGN-LOG.md + STRATEGY-BRIEF.md only.

Creative Director is [Your Name]. Do not ask their role.

---

## Reference Files — On Demand Only

| File | Load when |
|---|---|
| Campaign spec | Strategist only, when no checkpoint covers it |
| STRATEGY-BRIEF.md | Copywriter and Designer load at task start |
| CAMPAIGN-LOG.md | Strategist checks status; Copywriter updates when done |
| REVIEW-REQUEST.md | Designer loads at review start |
| REVIEW-FEEDBACK.md | Copywriter loads after Designer signals done |

Add project-specific reference files here as your campaign grows.

---

## Skills — On Demand Only

Load the skill the task needs. Not at session start.

`token-optimizer` — always first. Controls how the team reads, thinks, and responds.

Add your marketing-specific skills below:
[your skills here]
