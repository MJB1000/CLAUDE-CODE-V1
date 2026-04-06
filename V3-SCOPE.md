# V3 Scope — Sofia Asks Better Questions

## The Principle

Sofia doesn't need to become a researcher. She needs to **ask you the right questions
at the right time**, using real data to make those questions specific.

You have the context. You know your brand, your market, your customers.
Sofia's job is to pull signal from connected data sources, ask you pointed questions
about what it means, then make sure Charlie and Dana act on your answers.

---

## How it works

### Step 1: Sofia pulls signal before asking you anything

Instead of "what's the offer?" she connects to your data and opens with:

> "I pulled your GA4 data. The landing page had a 4.2% conversion rate
> in the first week, dropping to 1.8% by week 3. Email open rates held
> at 32% but CTR dropped from 3.1% to 1.4%.
>
> This looks like the offer lost urgency after the initial push.
> Two questions:
> 1. Do you want to extend the sale with refreshed messaging, or let it end?
> 2. The email CTR drop — is this audience fatigue or did something change
>    in the send schedule?"

That's a strategist. She's not researching for you — she's reading the data you
already have and asking you what it means.

### Step 2: Your answers become the brief

You say: "Extend with refreshed messaging. The email drop is fatigue — we sent
too many in week 2."

Sofia writes the brief with YOUR context baked in:
- Refreshed angle (not a new campaign — a refresh of the existing one)
- Reduced email frequency flagged as a constraint
- Performance data included so Charlie knows what's working and what isn't

### Step 3: All agents know what Sofia knows

The critical fix. Right now Sofia talks to you, then writes a brief. But the brief
only captures WHAT to do — not WHY. Charlie doesn't know the CTR dropped. Dana
doesn't know the offer lost urgency.

V3 adds a **Context Block** to the brief:

```
### Campaign Context (from Sofia — all agents read this)
- This is a refresh of Deliverable 1, not a new campaign
- Landing page conversion dropped from 4.2% → 1.8% (offer lost urgency)
- Email CTR dropped from 3.1% → 1.4% (audience fatigue from over-sending)
- CD decision: extend sale with refreshed messaging, reduce email frequency
- What worked: practical-prep angle held. "Sort your wipers" headline performed.
- What didn't: urgency faded without a new hook after week 1
```

Charlie reads this and knows: keep the practical angle, find a new hook, don't
repeat the same subject lines. Dana reads this and reviews against it: does the
refreshed copy actually feel different, or is it the same campaign with a new date?

### Step 4: Learning loops close automatically

After each campaign:
1. Sofia pulls performance data from connected MCPs (GA4, email platform, ad manager)
2. Sofia asks you ONE question: "Here's what the data shows. What does it mean?"
3. Your answer + the data become a retro entry
4. Patterns get logged. Validated by data. Fed into the next brief.

The agents don't interpret the data — you do. They just make sure the
interpretation is captured, stored, and applied next time.

---

## What Sofia asks at each stage

### At campaign start (pulling from MCPs)

| MCP | What Sofia sees | What Sofia asks you |
|---|---|---|
| GA4 | Landing page bounce rate is 65% | "Bounce rate is high. Is the traffic mismatched, or is the page not converting?" |
| Klaviyo | Last 3 emails averaged 28% open, 2.1% CTR | "Your email engagement is above benchmark. Want to lean heavier on email for this campaign?" |
| Google Ads | CPC for 'wiper blades' is $1.40, 'Toyota wiper blades' is $0.85 | "Vehicle-specific keywords are cheaper. Should we shift more budget there?" |
| Meta Ads | Your last 3 ads averaged 1.2% CTR, competitor benchmark is 0.9% | "Your social ads outperform category average. Worth testing more variants?" |

She's not analysing — she's surfacing. You provide the meaning.

### At review time (context for Dana)

| What Sofia passes to Dana | Why it matters |
|---|---|
| "Last email subject line with brand name got 32% open vs 24% without" | Dana checks: does this email have the brand name in the subject? |
| "CPC on 'best wiper blades' is 3x 'wiper blade replacement'" | Dana checks: are the ad headlines aligned to the cheaper keywords? |
| "Landing page conversion dropped week over week last campaign" | Dana checks: does the refreshed page actually feel different? |

### At retro time (closing the loop)

Sofia pulls metrics, then asks you:

> "Email 1 got 35% open rate (above your 28% average). Email 3 got 18%
> (below average). The landing page converted at 3.8% (up from 1.8% on
> the old version).
>
> Three questions:
> 1. Email 3 underperformed — was it the subject line, the timing, or the content?
> 2. The LP improvement — do you attribute that to the refreshed copy or
>    the new vehicle selector we added?
> 3. Any patterns here you want me to lock in for next time?"

Your answers become the learned patterns. Not Sofia's interpretation — yours.

---

## What changes in the framework

### Brief template — add Context Block

```
### Campaign Context
*Sofia fills this from MCP data + CD conversation. All agents read it.*
- Performance context: [what the data shows from previous campaigns]
- CD interpretation: [what the data means, in CD's words]
- Strategic direction: [what to do differently this time and why]
```

### Agent knowledge flow

```
                    MCP Data (GA4, Klaviyo, Meta, Google Ads)
                              ↓
                    Sofia surfaces signal
                              ↓
                    Asks CD specific questions
                              ↓
                    CD answers with context
                              ↓
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
     Brief Context     Brief Context     Brief Context
     Block             Block             Block
              ↓               ↓               ↓
          Charlie          Dana           Next brief
       (writes with     (reviews        (patterns
        full context)    against data)   captured)
```

### Learning loop

```
Campaign runs → Sofia pulls MCP metrics → Asks CD "what does this mean?"
→ CD answers → Retro captures data + interpretation
→ Patterns logged (observed) → Next campaign: data confirms/denies
→ Patterns promoted to validated → Brief pre-fills with proven strategy
```

---

## MCP connections needed (same list, different purpose)

| MCP | Not for "research" — for asking better questions |
|---|---|
| GA4 | "Your bounce rate is X. What's causing it?" |
| Klaviyo / Mailchimp | "Open rates dropped week 2. Over-sending or content fatigue?" |
| Google Ads | "Vehicle-specific CPCs are half the generic ones. Shift budget?" |
| Meta Ads | "Ad variant B outperformed A by 2x. Why do you think?" |

Sofia doesn't interpret the data. She surfaces it, asks you what it means,
and makes sure the answer flows to every agent who needs it.

---

## What this ISN'T

- Not autonomous research (Sofia doesn't crawl the internet for insights)
- Not automated decision-making (you make every strategic call)
- Not a dashboard (Sofia asks questions, doesn't present charts)
- Not complex (it's the same framework + one Context Block + MCP data pulls)

## What this IS

- Sofia with better questions
- Charlie and Dana with full context
- Learning loops that close with real data + your interpretation
- A framework that gets smarter because YOU teach it, not because it teaches itself
