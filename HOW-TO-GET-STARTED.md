# How to Get Started — From Setup to Published Content

A step-by-step guide to getting the Marketing Team framework running and producing output.

---

## Prerequisites

- [Claude Code CLI](https://claude.ai/code) installed
- A project folder (any folder — this framework is file-based, not code-based)
- Git (optional, for version control)

---

## Setup (5 minutes)

### Step 1: Get the framework into your project

```bash
# Option A: Clone into your project
git clone https://github.com/MJB1000/CLAUDE-CODE-V1.git my-marketing-project
cd my-marketing-project

# Option B: Clone as a skill (available in all projects)
git clone https://github.com/MJB1000/CLAUDE-CODE-V1.git ~/.claude/skills/marketing-team
```

### Step 2: Choose your personas

**Quick start (use pre-built personas):**
```bash
cp templates/project-folder/STRATEGIST.md agents/STRATEGIST.md
cp templates/project-folder/COPYWRITER.md agents/COPYWRITER.md
cp templates/project-folder/DESIGNER.md agents/DESIGNER.md
```
This gives you Sofia (Strategist), Charlie (Copywriter), and Dana (Designer) — ready to go.

**Custom personas:** Edit the `[CUSTOMIZE THIS SECTION]` blocks in `agents/*.md` with your own names and backstories.

### Step 3: Create working directories

```bash
mkdir -p deliverables retros
```

### Step 4: Verify the structure

You should have:
```
your-project/
├── agents/STRATEGIST.md, COPYWRITER.md, DESIGNER.md   ← role definitions
├── handoff/STRATEGY-BRIEF.md, REVIEW-REQUEST.md, ...   ← handoff templates
├── skills/token-optimizer.md                            ← loaded every session
├── deliverables/                                        ← your output goes here
├── retros/                                              ← post-publish learning
├── CLAUDE.md                                            ← session router
├── PLAYBOOK.md                                          ← cross-campaign memory
└── WORKFLOW-GUIDE.md                                    ← your reference
```

**That's it. No dependencies. No config files required. No build step.**

---

## Your First Campaign (30 minutes)

### Step 1: Open Claude Code and spin up the Strategist

Open Claude Code in your project folder. Paste this prompt:

```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
Report campaign status in one paragraph, then wait for me.
```

Sofia will read her files, see there's no existing campaign, and report back:
> "No active campaign. CAMPAIGN-LOG and STRATEGY-BRIEF are blank templates. Ready for your first brief."

### Step 2: Brief Sofia in plain language

Just talk to her. For example:

> "We're launching a new product — a hydrating face mist called 'Dew Drop.'
> I need a product description for our Shopify store. Target audience is
> women 25-35 who care about clean ingredients. Tone should be warm and
> approachable, like talking to a knowledgeable friend. Keep it under
> 200 words. We have no customer reviews yet."

**What happens next:**
- Sofia asks any clarifying questions she needs
- Sofia writes a formal `STRATEGY-BRIEF.md` with audience, objective, key message, tone, constraints, flags, and Definition of Done
- Sofia shows you the brief for approval

### Step 3: Approve the brief

Review what Sofia wrote. If it looks right:
> "Looks good. Proceed."

If something needs changing:
> "Change the tone to more playful. And add a flag — don't mention competitors."

### Step 4: Sofia spins up Charlie (Copywriter)

Sofia creates a Copywriter session automatically. Charlie will:

1. Read the brief
2. Check the brief date (must be <14 days old)
3. Write a plan (approach, decisions, uncertainties)
4. Wait for Sofia's approval
5. Write the copy
6. Self-check against the Definition of Done
7. Submit a Review Request to Dana

**You do not need to do anything during this step.** Sofia manages it.

### Step 5: Sofia spins up Dana (Designer/Reviewer)

Dana reads Charlie's work and the brief, then writes feedback:

- **Must Fix** — blocks publishing (e.g., "headline contradicts the brief's key message")
- **Should Fix** — nice to have (e.g., "CTA could be punchier")
- **Escalate** — needs your decision (e.g., "brief says warm tone but the CTA is aggressive — which wins?")

If Dana escalates, Sofia asks you. Otherwise, Charlie fixes and re-submits.

### Step 6: Launch gate

When Dana clears, Sofia presents the final work to you:

> "Product description is done. Dana caught one issue — Charlie used a claim
> about hydration that needs sourcing. Charlie replaced it with a benefit
> statement. No other issues. Ready to publish?"

You say:
> "Ship it."

Sofia saves the final copy to `deliverables/01-product-description.md`, updates the Campaign Log, and writes a Session Checkpoint.

### Step 7: Done

Your output is in `deliverables/01-product-description.md`. Copy it to Shopify, your CMS, wherever it goes.

---

## What You Get at the End

After one deliverable cycle, your project contains:

| File | What's in it |
|---|---|
| `deliverables/01-product-description.md` | Your finished, reviewed copy |
| `handoff/CAMPAIGN-LOG.md` | Full record: what was built, what was caught, what was decided |
| `handoff/SESSION-CHECKPOINT.md` | Where things stand (for resuming later) |
| `retros/RETRO-1.md` | What worked, what the brief should have included, rules for next time |
| `PLAYBOOK.md` | Patterns learned from this deliverable |

---

## Running Your Second Deliverable

Open Claude Code. Paste:

```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
Report campaign status in one paragraph, then wait for me.
```

Sofia reads the checkpoint and the campaign log. She knows what was done, what was learned, and what gaps exist. She reports status, then waits for your next brief.

Brief her again:
> "Now I need a 3-email welcome sequence for new subscribers."

Sofia writes the brief — this time with **Learned Patterns** from the first deliverable included. The framework is already smarter.

---

## Resuming After a Break

If you close Claude Code and come back days later, the checkpoint has everything.
Just spin up Sofia again — she reads the checkpoint and picks up where you left off.

If the checkpoint is older than 7 days, Sofia reads the full Campaign Log instead.

If the brief is older than 14 days, Charlie will flag it for Sofia to reconfirm with you before writing.

---

## Multiple Deliverables at Once (Batching)

For related items (e.g., landing page + 3 ads), brief Sofia:

> "I need a landing page and 3 Facebook ads for the same product launch.
> Same audience, same message."

Sofia writes one brief with sub-deliverables (2a, 2b, 2c, 2d). Charlie writes them all. Dana reviews them as a batch — checking cross-piece consistency. They ship together.

---

## The Learning Loop (Automatic)

You don't manage this — Sofia does.

```
Publish → Retro (day 0) → 7-day metrics → 30-day metrics → Playbook updated
                                                                    ↓
                                                          Next brief informed
```

To trigger a metrics check-in:
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
It is time for the 7-day metrics check-in for Deliverable 1.
Read retros/RETRO-1.md and update the metrics section.
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Sofia asks too many questions | Brief more completely. Include constraints and flags. |
| Copy is off-tone | Check if your tone guidance was specific. "Professional" is not enough. Give a comparison: "like a smart friend" or "like a Wall Street Journal editorial." |
| Review is too strict/lenient | Edit Dana's persona in `agents/DESIGNER.md`. Adjust the "Who You Are" section. |
| Framework feels slow | Batch related deliverables instead of running them one at a time. |
| Checkpoint is stale | Sofia will read CAMPAIGN-LOG instead. No data is lost. |
| Brief expired (>14 days) | Charlie blocks automatically. Tell Sofia to reconfirm or rewrite the brief. |

---

## Quick Reference: Session Prompts

**New campaign:**
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
Report campaign status in one paragraph, then wait for me.
```

**Resume:**
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md,
then CAMPAIGN-LOG.md. Tell me where we stand and what is next.
```

**7-day metrics:**
```
You are Sofia on this project. Read CLAUDE.md, then STRATEGIST.md.
It is time for the 7-day metrics check-in for Deliverable [N].
Read retros/RETRO-[N].md and update the metrics section.
```

---

## That's It

1. Spin up Sofia
2. Brief her in plain language
3. Approve the brief
4. Make decisions when she asks
5. Say "Ship it" at the launch gate
6. Repeat

The framework handles everything else: structured briefs, copy production, brand review, feedback loops, learning, and metrics tracking. You just make the decisions.
