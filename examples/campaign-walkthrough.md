# A Complete Marketing Team Sprint

This is what a full deliverable looks like from brief to publish.

## 1. Creative Director describes a need to Strategist

> "Our trial-to-paid conversion is dropping. The onboarding email sequence
> hasn't been updated since launch and it's generic — same emails whether
> they signed up for feature A or feature B."

## 2. Strategist diagnoses

Strategist reviews the existing sequence, confirms the gap: no segmentation,
no feature-specific value messaging, weak CTAs pointing to a generic dashboard
instead of the feature they signed up for.

Asks: "Do you want to segment by signup feature only, or also by plan tier?"

Creative Director: "Feature only for now. Two segments: feature A and feature B."

## 3. Strategist writes the brief

Updates STRATEGY-BRIEF.md:

```
## Deliverable 4 — Segmented onboarding email sequence
- Audience: Trial users, segmented by signup feature (A vs B)
- Objective: Increase trial-to-paid conversion by 15%
- Key message: Show how their specific feature solves their problem within 7 days
- Tone: Helpful, direct, no corporate speak. Like a smart colleague showing them around.
- Channel: Email — 5-email drip over 7 days, per segment
- Constraints: Each email under 200 words. Subject lines under 50 chars. One CTA per email.
- Flag: Do not reference pricing. CTA goes to feature-specific dashboard, not generic.
```

## 4. Strategist spins up Copywriter

> You are Charlie on this project. Load token-optimizer skill first.
> Then read COPYWRITER.md, then STRATEGY-BRIEF.md.
> Your task is Deliverable 4.

## 5. Copywriter writes

Charlie reads the brief, writes a one-paragraph approach ("leading each sequence with
the #1 job-to-be-done for each feature, progressive disclosure across 5 emails"),
gets Sofia's nod, and writes the sequence. Updates CAMPAIGN-LOG. Writes REVIEW-REQUEST.md.

## 6. Strategist spins up Designer

> You are Dana on this project. Load token-optimizer skill first.
> Then read DESIGNER.md, then REVIEW-REQUEST.md.
> Review only the files Charlie listed.

## 7. Designer reviews

Dana reads the sequence. Confirms tone matches brand guidelines. Confirms CTAs
point to feature-specific dashboards. Flags: Email 3 in the Feature B sequence
uses a claim ("saves 2 hours per week") that needs substantiation — must fix.
Also: subject line on Email 5 is 53 characters — should fix (brief says under 50).
Sets Ready for Copywriter: NO.

## 8. Copywriter fixes

Charlie replaces the unsubstantiated claim with a benefit statement that doesn't
require proof ("see exactly where your time goes"). Trims the subject line to 48
characters. Re-submits.

## 9. Designer clears

"Deliverable 4 is clear." Sets Ready for Copywriter: YES.

## 10. Strategist publishes

Tells Creative Director: "Segmented onboarding sequence done — 10 emails total,
5 per feature. Dana flagged an unsubstantiated claim in the Feature B sequence —
Charlie replaced it with a benefit statement. Subject line trimmed to fit. Clean."

Creative Director: "Ship it."

Sofia commits, pushes to the email platform, confirms delivery is scheduled,
updates CAMPAIGN-LOG and SESSION-CHECKPOINT.
