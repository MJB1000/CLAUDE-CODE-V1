# V3 Scope — Deeper, More Relevant Insights

## The Problem V3 Solves

V1/V2 agents are disciplined executors. V3 agents are strategic thinkers.

The framework follows process perfectly but doesn't generate insight. Sofia formats
your direction into a brief. Charlie writes competent copy. Dana catches mechanical
errors. None of them challenge the strategy, discover unexpected angles, or bring
market intelligence that changes the approach.

A senior marketing team doesn't just execute — they push back, surprise you, and
make the work better than what you briefed.

---

## The 5 Depth Upgrades

### 1. Strategic Intelligence Layer (Sofia)

**Current:** Sofia asks "what's the offer?" and formats your answer into a brief.

**V3:** Sofia researches the market BEFORE asking questions, then challenges your
direction with data.

**How it works:**

When a new campaign starts, before Sofia writes anything, she runs a strategic analysis:

```
## Pre-Brief Intelligence Report

### Market State
- What competitors are running right now (fetched live)
- What messaging angles are saturated vs untapped
- What the audience is hearing from everyone else

### Opportunity Analysis
- Where the whitespace is (what nobody is saying that this brand could own)
- What emotional territory is available
- What seasonal/cultural moments are approaching that could be leveraged

### Strategic Recommendation
- Recommended angle and WHY (based on competitive gap, not just brief direction)
- What to avoid (because competitors already own it)
- Risk assessment (what could go wrong with this angle)
```

Sofia stores this in `clients/[name]-intelligence.md` and references it when writing
briefs. Each campaign updates it. Over time, Sofia builds a genuine understanding of
the competitive landscape — not just a list of competitors, but what they're doing
and where the gaps are.

**What changes for the CD:** Instead of "I need a winter sale campaign," you get
"Here's what I found: Supercheap Auto is running 20% off generic blades with fear
messaging ('Don't risk it this winter'). Repco is doing buy-one-get-one. Neither
mentions fit, warranty, or Australian-made. The whitespace is quality + convenience.
I recommend leading with 'Skip the auto store' positioning, not just a discount.
Your 15% off is smaller than competitors — the angle needs to be why WiperTech is
worth more, not just cheaper right now."

That's a strategist. That's V3.

---

### 2. Creative Intelligence Layer (Charlie)

**Current:** Charlie writes what the brief says. Competently.

**V3:** Charlie studies how the best copy in the brand's space actually sounds, then
writes with informed creative instincts.

**How it works:**

Before writing, Charlie runs a creative analysis:

```
## Creative Context

### How this audience talks (gathered from reviews, forums, social)
- Actual phrases, vocabulary, complaints, desires
- What makes them click (based on swipe file validated entries)
- What makes them bounce (based on anti-patterns)

### What's working in this channel right now
- Fetched: top-performing ad copy in this category (via Meta Ad Library, Google Ads Transparency)
- What hooks are working (problem-first? offer-first? social proof?)
- What's oversaturated (everyone uses "don't miss out" — it's noise now)

### Creative direction
- Unexpected angle the brief didn't specify but the data supports
- Specific language borrowed from audience's own vocabulary
- What NOT to write (because it sounds like every competitor)
```

**What changes for the CD:** Charlie doesn't just hit the word count. He writes
"Sort your wipers before winter hits" because he researched that Australians say
"sort it" not "fix it" when talking about practical tasks. He knows the audience
says "no drama" in reviews, so he uses it. His copy sounds like the audience
talking to themselves, not like a brand talking at them.

---

### 3. Review Intelligence Layer (Dana)

**Current:** Dana reviews against the brief. Did Charlie follow instructions?

**V3:** Dana reviews against the brief AND the market. Does this work beat the
competition, not just match the brief?

**How it works:**

Dana adds a competitive review dimension:

```
## Competitive Review

### Differentiation check
- Does this copy say something the audience hasn't heard from 3 other brands?
- Would this stop someone who has already seen competitor ads this week?

### Audience-reality check
- Is this how the audience actually makes this decision?
- Does the CTA match what the audience wants to do next (not what we want them to do)?

### Channel-performance check
- Based on validated patterns, does this copy structure match what performs?
- Is the hook format (problem-first, offer-first, social) the right one for this
  audience + channel combination?
```

**What changes for the CD:** Dana doesn't just say "this headline is too long." She
says "this headline leads with fit, which is strong — but Supercheap's current campaign
also leads with fit ('Right blade for your car'). We should lead with the convenience
angle ('Skip the auto store') to differentiate. The fit message works better as VP1."

---

### 4. Client Intelligence That Compounds

**Current:** Client profile stores facts: brand voice, stats, competitors.

**V3:** Client intelligence stores understanding: why the brand wins, what emotional
territory it owns, what the audience cares about beyond the product, how the market
is shifting.

**New client profile sections:**

```
## Brand Position Map
- What this brand owns in the audience's mind
- What it should own (and doesn't yet)
- What competitors own
- White space: unclaimed territory

## Audience Psychology
- Purchase triggers (what makes them buy NOW vs later)
- Decision blockers (what stops them even when interested)
- Trust signals (what makes them believe claims)
- Information sources (where they research before buying)

## Messaging Hierarchy (validated over time)
- Primary message that always works for this brand: [validated]
- Secondary messages that test well: [validated/observed]
- Messages that consistently underperform: [invalidated]

## Campaign Performance Memory
| Campaign | Channel | Angle | Result | Insight |
|---|---|---|---|---|
| Winter Sale | Email | practical-prep | 32% open rate | Outcome-led subject lines beat offer-led |
| Winter Sale | Google Ads | fit-first | 4.2% CTR | Fit message + vehicle specificity = best combo |

## Competitive Movement Log
| Date | Competitor | What Changed | Impact on Us |
|---|---|---|---|
| 2026-04 | Supercheap | New "fit guarantee" campaign | Our fit message is no longer differentiated |
```

**What changes:** After 3 campaigns, Sofia doesn't start from scratch. She knows
that practical-prep outperforms discount-first for this audience, that fit messaging
needs to be paired with convenience to differentiate from Supercheap's new campaign,
and that email subject lines with the brand name get 15% higher open rates. She briefs
Charlie with genuine insight, not just formatting.

---

### 5. Knowledge MCPs That Feed Real Intelligence

**Current:** WebSearch and WebFetch for generic research. No structured market data.

**V3:** Targeted MCPs that deliver specific marketing intelligence:

| MCP | What It Feeds | Agent |
|---|---|---|
| **Meta Ad Library API** | Live competitor ad copy, spend estimates, creative formats | Sofia + Dana |
| **Google Ads Transparency** | Competitor search ads, keywords, landing pages | Sofia + Charlie |
| **Google Trends** | Search volume trends, seasonal patterns, rising queries | Sofia |
| **Reddit/Forum scraper** | Actual audience language, complaints, desires | Charlie |
| **Review aggregator** | Customer sentiment, common praise/complaints | Sofia + Charlie |
| **GA4 / analytics** | Own campaign performance data for retros | Sofia |
| **Email platform API** | Open rates, CTR, send times for metrics loop | Sofia |

**The key difference:** V2 knowledge is stored and retrieved. V3 knowledge is
*gathered, analyzed, and applied*. The agents don't just read a file — they go
find what they need, extract the insight, and apply it to the current campaign.

---

## What Changes for the User

| V2 Experience | V3 Experience |
|---|---|
| "I need a winter sale campaign" → Sofia writes a brief from what you said | "I need a winter sale campaign" → Sofia researches the market, challenges your angle, recommends a differentiated approach, THEN writes the brief |
| Charlie writes competent copy matching the brief | Charlie writes copy that sounds like the audience talking, using language he found in their reviews |
| Dana catches mechanical errors | Dana catches strategic errors — "this doesn't differentiate from what Supercheap is running" |
| Playbook stores "no superlatives" | Intelligence layer stores "practical-prep outperforms discount-first for Aussie drivers by 2:1" |
| Each campaign starts with "what do you want?" | Each campaign starts with "here's what I found — and here's what I recommend" |

---

## Build Priority

| Phase | What | Impact |
|---|---|---|
| **3.1** | Pre-brief intelligence report (Sofia researches before briefing) | Transforms Sofia from formatter to strategist |
| **3.2** | Audience language mining (Charlie studies how audience talks) | Copy sounds like the audience, not like a brand |
| **3.3** | Competitive review dimension (Dana reviews against market) | Catches strategic misses, not just mechanical ones |
| **3.4** | Deep client intelligence (position map, psychology, performance memory) | Each campaign genuinely smarter than the last |
| **3.5** | Targeted MCPs (Meta Ad Library, Google Trends, review scraping) | Real data instead of training-data guesses |

Phase 3.1 is the highest leverage — it changes every downstream deliverable because the
brief itself becomes smarter.

---
