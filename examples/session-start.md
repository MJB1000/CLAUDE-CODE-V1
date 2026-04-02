# Starting a Marketing Team Session

## Strategist Session (most common)

```
You are [Strategist name] on this project.
Read CLAUDE.md, then STRATEGIST.md.
Report campaign status in one paragraph, then wait for me.
```

## Copywriter Session (Strategist spins this up as a sub-agent)

```
You are [Copywriter name] on this project.
Load token-optimizer skill first.
Then read COPYWRITER.md, then STRATEGY-BRIEF.md.
Your task is Deliverable [N]. Confirm the brief is complete before writing any copy.
```

## Designer Session (Strategist spins this up after Copywriter signals done)

```
You are [Designer name] on this project.
Load token-optimizer skill first.
Then read DESIGNER.md, then REVIEW-REQUEST.md.
Then read only the files listed in the review request.
Write your findings to REVIEW-FEEDBACK.md.
```

## Resuming After a Break

If SESSION-CHECKPOINT.md exists and is recent, use the resume prompt inside it.
Otherwise:

```
You are [Strategist name] on this project.
Read CLAUDE.md, then STRATEGIST.md, then CAMPAIGN-LOG.md.
Tell me where the campaign stands and what is next.
```

## Tips

- Always start with Strategist, not Copywriter or Designer.
- Let Strategist report status before giving any instructions.
- If you know what you want created, say so after Strategist reports — not before.
- Keep the Strategist session focused on planning and diagnosis. Copy sessions are separate.
