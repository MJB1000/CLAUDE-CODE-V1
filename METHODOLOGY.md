# Marketing Team — Methodology

Why this works, and the thinking behind it.

---

## Personas Over Labels

Telling an AI "you are a copywriter" produces generic copy. Giving the AI a character — a backstory, a set of values, a voice, a specific reason they care about the work — activates a richer cluster of behavior.

This is vocabulary routing: precise role framing activates relevant training patterns more effectively than abstract job titles. The Designer in Marketing Team is not "a brand reviewer." They are someone who has seen what happens when off-brand work ships and has cleaned up the mess. That framing produces different — better — behavior.

The personas in Marketing Team are defaults. Name them, age them, give them a history that fits your brand and your domain. The specificity is the point.

---

## Three Is the Right Number

DeepMind's multi-agent scaling research shows that structured teams of 3-5 agents with defined artifact handoffs consistently outperform both solo agents and larger teams. Solo agents drift. Large teams generate coordination overhead that eats the productivity gain. Three is the sweet spot: enough for meaningful review, minimal enough for clean handoffs.

Marketing Team is exactly three agents by design. Resist adding a fourth.

---

## Handoffs Through Files, Not Conversation

In Marketing Team, the agents communicate through structured files:
- Strategist writes to STRATEGY-BRIEF.md
- Copywriter writes to REVIEW-REQUEST.md
- Designer writes to REVIEW-FEEDBACK.md

This is not just organization. It means each agent starts with a clean context window reading only what they need for their specific job. Copywriter never loads the full campaign plan. Designer never loads the audience research. Token waste is structural, not behavioral — fix the structure and the behavior follows.

---

## The Launch Gate

Nothing publishes without Strategist's sign-off and the Creative Director's awareness. This is not bureaucracy — it is accountability. The Creative Director knows what is going live. The Strategist has confirmed it passed review. The Copywriter and Designer never publish directly.

This pattern eliminates the most expensive class of AI mistake: content that was technically well-written but wrong for the brand, shipping without anyone noticing.

---

## Token Discipline as Infrastructure

Token waste is not a Claude problem or a prompt problem. It is a context architecture problem. The five rules in Marketing Team's CLAUDE.md are not guidelines — they are operating rules that fire before every tool call. The cost of re-reading a file you already have in context is paid every time. The cost of the rules is paid once, at session start.

Grep before Read. Never speculate. Parallelize when possible. Route large outputs to subagents. Never restate what the user said.

---

## Scope Lock

One deliverable at a time. The next deliverable does not start until the current one is reviewed, cleared, and published. Anything that surfaces out of scope during a step goes to CAMPAIGN-LOG Known Gaps — it does not get fixed. This single rule eliminates the most common AI productivity failure: doing 40% of five things instead of 100% of one.
