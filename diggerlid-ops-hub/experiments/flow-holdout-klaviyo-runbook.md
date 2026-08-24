# Flow Holdout Test — Klaviyo Build Instructions

**Goal:** Measure the incremental $ that Klaviyo **flows** drive, by holding a random 10% of the active list out of **all flows** for 10 weeks and comparing revenue per profile.

**Design:** Global/persistent · 10% control (~3,258) / 90% treatment · 10 weeks · control still receives **campaigns, SMS, and transactional** — only flows are withheld.

> Hand this to whoever has Klaviyo admin access, or run it yourself top to bottom. Do the steps in order. Klaviyo occasionally renames UI labels — match on meaning if a label differs.

---

## Phase 0 — Prerequisites
- Klaviyo **admin** access.
- Your **Active** segment exists (the 32,579 profiles).
- `holdout_out.csv` generated from the active export:
  `python3 scripts/holdout_assign.py active_export.csv --pct 10 --prop ho_flow`
  (columns: `Email, ho_flow, ho_bucket`; ~10% `control`, ~90% `treatment`).

---

## Phase 1 — Write the `ho_flow` property to profiles (CSV import)
1. Klaviyo → **Audience → Import** (or **Profiles → Import**).
2. Upload **`holdout_out.csv`**.
3. Column mapping:
   - `Email` → **Email**
   - `ho_flow` → **Create custom property** named exactly **`ho_flow`**
   - `ho_bucket` → import as custom property `ho_bucket` (optional, handy for QA)
4. When asked which list to add to, choose your **existing main newsletter list** (they're already members, so membership doesn't change — the import only updates the property). Do **not** create a new list.
5. Run the import. Wait for it to finish (a few minutes).

**Checkpoint:** open any profile from the CSV and confirm it now shows `ho_flow = control` or `treatment`.

---

## Phase 2 — Build the segments
Klaviyo → **Audience → Lists & Segments → Create Segment.**

**Segment 1 — `🚫 FLOW HOLDOUT — SKIP ALL FLOWS`** (the control / exclusion segment)
- Condition: **Properties about someone** → `ho_flow` → **equals** → `control`
- AND: **If someone is or is not in a segment** → **is in** → *Active*
- Save. Note the size — it should be **≈ 3,200–3,300**.

**Segment 2 — `FLOW TEST — Treatment`**
- **Properties about someone** → `ho_flow` → **equals** → `treatment`
- AND **is in** → *Active*
- Save (≈ 29,300).

**Segment 3 — `FLOW TEST — Control (measure)`**
- **Properties about someone** → `ho_flow` → **equals** → `control`
- AND **is in** → *Active*
- Save. (Same members as Segment 1; kept separate so the exclusion segment is never edited during analysis.)

---

## Phase 3 — Gate EVERY live flow (the critical step)
Flows have no "don't send to." You add a filter to each flow so control profiles are held.

For **each** live flow:
1. Klaviyo → **Flows** → open the flow.
2. Click **Flow Filters** (top of the flow canvas).
3. **Add filter** → **If someone is or is not in a segment** → **is not in a segment** → select **`🚫 FLOW HOLDOUT — SKIP ALL FLOWS`**.
4. **Save**. Confirm the flow status stays **Live**.

**Gate all of these (tick each):**
- ☐ Welcome / sign-up
- ☐ Abandoned Cart
- ☐ Checkout / Browse Abandonment
- ☐ Post-Purchase / Thank-you
- ☐ Win-back / Lapsed
- ☐ Back-in-stock
- ☐ Any other live flow (birthday, review request, cross-sell, etc.)

> A flow filter re-evaluates at each step, so a control profile who somehow entered is still held. **Every live flow must be gated — one missed flow invalidates the test.**

---

## Phase 4 — QA before you call it live
1. **Segment size:** `🚫 FLOW HOLDOUT` ≈ 3,258 (±). Treatment ≈ 29,321.
2. **Spot check a control profile:** pick an email with `ho_flow = control`; confirm it's in `🚫 FLOW HOLDOUT`.
3. **Live trigger test:** with a test profile you've set to `control`, trigger a flow (e.g. start a checkout and abandon). Confirm in the flow's **Analytics → Recipients** that the control profile was **skipped/filtered**, not sent.
4. **Reverse check:** a `treatment` test profile should proceed through the flow normally.
5. Confirm **campaigns and SMS are unchanged** — do NOT add the holdout to any campaign exclusion or SMS this quarter.

---

## Phase 5 — Launch & log
Record and keep:
- **Start date** (test runs 10 weeks from here).
- **Segment sizes** at launch (control / treatment).
- **List of flows gated** (the ticked checklist above).
- The frozen **`holdout_out.csv`** roster.

Do not re-run the assignment or change the segments during the window. (Re-running the script is safe/stable, but for the cleanest read keep the start cohort fixed.)

---

## Phase 6 — Measurement (weeks 4, 8, 10)
Metric: **revenue per profile (RPR)** = total Placed Order value ÷ profiles, per arm.

Pull, per arm (Control ≈3,258 vs Treatment ≈29,321):
- **Purchase rate** (chi-square) — did more of treatment buy?
- **AOV among buyers**
- **RPR** with a **bootstrap confidence interval** (revenue is skewed; a plain t-test isn't valid)
- **Unsub / spam-complaint rate** per arm (holding out can *reduce* fatigue — part of net value)

**Incremental $ from flows = (RPR_treatment − RPR_control) × N_treatment.**

Bonus (flows only): filter each arm to people who hit a specific **trigger** (abandoned a cart, signed up, etc.) to get **per-flow** incremental $ — control who triggered but got no flow vs treatment who did.

Source: Shopify (join Klaviyo `user_id` → orders) for P&L-clean numbers, or Klaviyo per-segment revenue for speed.

---

## Guardrails (keep the test valid)
- Gate **every** live flow; never send a flow to control.
- Control **keeps** campaigns + SMS + transactional — don't touch those.
- Analyse **intention-to-treat** — keep unsubscribers in their assigned arm.
- Keep campaigns + SMS identical across both arms (any difference confounds the flow read).
- Fixed 10-week window; don't peek-and-stop early on a noisy week-2 number.
