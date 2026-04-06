# Brief Quality Score — Pre-Flight Check

Load this skill after Strategist writes the brief and BEFORE spinning up Copywriter.

---

## When to Run

Every time Sofia finishes writing STRATEGY-BRIEF.md, before saying "spinning up Charlie."
This is a 30-second self-check, not a full review.

## Quality Score (must pass 8/10 to proceed)

Score the brief against these 10 criteria. Mark each PASS or FAIL.

### Completeness (required fields filled, not template placeholders)

| # | Criterion | Check |
|---|---|---|
| 1 | **Audience is specific** — names a real segment, not "people who buy things" | Contains demographics OR psychographics OR funnel stage |
| 2 | **Audience Context filled** — what they already know, competitors, objections | At least 2 of 3 sub-fields populated |
| 3 | **Key Message is one sentence** — not three messages or a paragraph | Single sentence, under 30 words |
| 4 | **Tone guidance is actionable** — not "professional but fun" | Contains a comparison ("like a...") OR specific voice qualities OR example reference |
| 5 | **Constraints have numbers** — word counts, char limits, deadlines | At least one quantified constraint per deliverable |

### Safety (prevents downstream waste)

| # | Criterion | Check |
|---|---|---|
| 6 | **Available Brand Assets filled** — what exists AND what does NOT exist | Both "exists" and "does not exist" sections populated |
| 7 | **Flags present** — at least one Flag per deliverable | No empty Flags section |
| 8 | **Learned Patterns included** — relevant patterns from Playbook/Notion | If patterns exist for this channel/audience, they are in the brief |

### Structure (framework compliance)

| # | Criterion | Check |
|---|---|---|
| 9 | **Definition of Done has both types** — self-checkable AND review-dependent | Both sections have at least 2 items each |
| 10 | **Brief date is set** — not "[date]" placeholder | Actual date present |

## Scoring

- **8-10 PASS:** Proceed to Copywriter.
- **6-7 PASS:** Fix the failing items before proceeding. Takes 2 minutes.
- **Below 6:** Brief needs significant rework. Do not spin up Copywriter.

## Sofia runs this herself

This is not a separate agent or tool. Sofia reads the brief she just wrote, scores it
against the 10 criteria, and fixes any failures before continuing. It's a self-discipline
check, not an external gate.

```
## Brief Quality Score
Scored: [date]
Result: [N]/10 — [PROCEED / FIX BEFORE PROCEEDING / REWORK]

| # | Criterion | Result |
|---|---|---|
| 1 | Audience specific | PASS / FAIL |
| 2 | Audience context | PASS / FAIL |
| ... | ... | ... |
```

Add this score to the bottom of STRATEGY-BRIEF.md before spinning up Copywriter.
