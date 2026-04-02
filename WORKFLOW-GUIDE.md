# Workflow Guide — Briefing & Communication

How to actually use the Marketing Team framework day-to-day.

---

## Your Role: Creative Director

You are the Creative Director (CD). You own the brand, the business context, and the
final say on what publishes. The framework gives you three AI agents that do the work —
you make the decisions.

**You do not need to manage the agents directly.** Talk to the Strategist. The Strategist
manages Copywriter and Designer for you.

---

## Starting a Campaign

### Step 1: Open a session and spin up the Strategist

Copy-paste this prompt:

```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
Report campaign status in one paragraph, then wait for me.
```

Sofia will read her files, check for any existing campaign state, and report back.
If this is a new project, she will tell you there is nothing in progress.

### Step 2: Brief the Strategist in plain language

You do not need to fill out templates. Talk to Sofia like a colleague:

> "We're launching a new Vitamin C serum. I need a 3-email launch sequence
> targeting women 25-40 who buy premium skincare. Brand voice is warm and
> knowledgeable — like a friend who happens to be a dermatologist. We have
> a launch offer: 20% off with code GLOW20, expires in 7 days."

**That is enough.** Sofia will ask clarifying questions if she needs more, then
she will write the formal STRATEGY-BRIEF.md for the team.

### Step 3: Make decisions when Sofia asks

Sofia will surface decisions she cannot make alone:
- "Do you want to segment by feature or by plan tier?"
- "The data team hasn't approved ROI claims. Should we publish with qualitative-only copy?"
- "Charlie wants to lead with ingredient education instead of the discount. Your call."

Answer these. Sofia logs your decisions to CAMPAIGN-LOG.md automatically.

### Step 4: Review at the launch gate

Sofia will present the finished work:
- What was created
- What the Designer caught and how it was fixed
- Any known gaps (placeholders, unverified data)

Say "Ship it" or give specific redirects. Sofia publishes and logs everything.

---

## Daily Workflow

### If you have 5 minutes
Open a Strategist session. Sofia reads the checkpoint and gives you a one-paragraph
status update. You review, make any decisions, and close.

### If you have 30 minutes
Open a Strategist session. Sofia runs a full deliverable cycle:
brief → copy → review → fix → re-review → launch gate. You make decisions at the start
(brief direction) and end (launch gate sign-off).

### If you are hands-off
Give Sofia the campaign direction in one session. Close. Come back later.
Sofia will have the checkpoint waiting. Pick up where you left off.

---

## Communication Rules

### What you say goes through files

Every decision you make is logged by Sofia to CAMPAIGN-LOG.md. This means:
- If your session crashes, your decisions survive
- If you come back a week later, Sofia reads the log and knows what you decided
- If you bring in a different AI tool later, the log is readable by anyone

### You never talk to Copywriter or Designer directly

If you want to give Charlie a note on tone, tell Sofia. She adds it to the brief as a Flag.
If you want to redirect Dana's review focus, tell Sofia. She adds it to the review instructions.

This prevents conflicting instructions. One channel: you → Sofia → team.

### Disagreements escalate to you

If Dana flags something and Charlie disagrees, Sofia arbitrates. If Sofia cannot resolve it
(brand decision, business call), she escalates to you with the context and options.

---

## Briefing Tips

### What makes a good brief (for Sofia)

| Do | Don't |
|---|---|
| State the audience and what they care about | List demographics without context |
| Name the one thing the reader should take away | Give 5 key messages ("pick the best one") |
| Set constraints (word count, channel, compliance) | Leave format open ("whatever works") |
| Flag what does NOT exist (no quotes, no data) | Assume the team knows what you have |
| Say what the tone should feel like ("smart friend") | Say "professional but fun" (meaningless) |
| Reference a comparable piece if one exists | Describe the style in abstract terms |

### What to NOT brief

- Don't write the copy yourself and ask the team to "polish" it. Brief the objective and let Charlie write.
- Don't prescribe the structure. Say what needs to be communicated; Charlie decides how.
- Don't brief more than one campaign at a time. Finish one, learn from it, brief the next.

---

## Handling Multi-Deliverable Campaigns

### When to batch
Batch related items that share audience, message, and tone:
- Email sequence (3-5 emails in one brief)
- Landing page + paid ads (same messaging, different formats)
- Social posts for a single campaign moment

### When NOT to batch
Do not batch items that serve different audiences or different campaign stages:
- Awareness content + bottom-funnel sales content
- Customer-facing copy + internal sales enablement
- Content for different products or segments

### How batching works for you
You brief it the same way — one conversation with Sofia. She writes one brief
with labeled sub-deliverables (2a, 2b, 2c). The team handles the rest.

---

## The Learning Loop

### You do not need to manage this

Sofia handles the learning loop automatically:
1. **After publish:** Writes a retrospective (what worked, what the brief missed)
2. **7 days later:** Checks metrics, updates the retro
3. **30 days later:** Final metrics check, updates the Playbook

### What you see
Next time you brief a similar campaign, Sofia's brief will include a Learned Patterns
section with rules from previous campaigns. For example:

> **Learned Patterns:**
> - DTC skincare audience: education-first tone outperforms discount-first (validated, Dewdrop campaign)
> - Email subject lines under 45 chars get higher open rates (observed, not yet validated)

You review these patterns and confirm or override them. The framework gets smarter
with every campaign you run.

---

## When Things Go Wrong

| Situation | What to do |
|---|---|
| Sofia asks too many questions | Brief more completely up front. Include Flags for anything she should not guess at. |
| Charlie's copy is off-tone | Check if the brief tone guidance was specific enough. "Professional but engaging" is not enough. |
| Dana is too strict | Review Dana's persona in DESIGNER.md. Adjust the "Who You Are" section to match your review standards. |
| Dana is too lenient | Add specific review criteria to the Definition of Done (review-dependent section). |
| Campaign is taking too long | Check if you are briefing sequentially when you could batch. Check if the brief has ambiguities causing back-and-forth. |
| Old patterns are wrong | Override them in the brief. Tell Sofia "ignore the pattern about X, we are trying Y this time." At the 30-day retro, the data will update the Playbook. |

---

## Quick Reference: Session Prompts

### Start a new campaign
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
Report campaign status in one paragraph, then wait for me.
```

### Resume an existing campaign
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md,
then CAMPAIGN-LOG.md. Tell me where we stand and what is next.
```

### Check metrics (7-day or 30-day)
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
It is time for the [7-day / 30-day] metrics check-in for Deliverable [N].
Read retros/RETRO-[N].md and update the metrics section.
```

---
