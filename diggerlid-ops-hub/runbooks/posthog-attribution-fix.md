# Runbook — PostHog experiment attribution fixes

Two defects currently corrupt PostHog experiment reads (found 2026-08-20, EXP-004/005).
Until both ship, trust only the person-stitched HogQL reads in `EXPERIMENT-LOG.md` — NOT the
PostHog experiment UI.

## Fix 1 — Enrollment dilution (the big one)

**Problem:** experiment flags (`landing-hero-test`, `fathers-day-test`) enroll visitors
**site-wide** on any page load, but each variant only renders on its landing page. Result:
~96% of "enrolled" users never saw the change → effects washed out ~25–30×; tests look flat
when the on-page effect is large (video hero: +62% PDP CTR among true viewers).

**Fix (PostHog UI):** for each experiment, scope exposure to the landing page:
- Experiment → **Exposure criteria** (or the feature flag's **release conditions**): add a
  condition so the flag only evaluates/enrolls when `Current URL` / `$pathname` contains the
  LP path — `/pages/pro-mat-plus-2026` (hero test) · `/pages/gift` (FD test).
- Alternative if using code: call `posthog.getFeatureFlag(...)` only on the LP template, and
  set the experiment's exposure event to a `$pageview` filtered to that pathname.
- **Do this for every future LP experiment at creation time.**

**Effect:** enrolled N drops to true viewers; the same traffic reaches significance in days
instead of months.

## Fix 2 — Shopify events carry no `$feature/*` properties

**Problem:** `Product Added` / `Order Completed` arrive from the Shopify pipe (server-side)
without the `$feature/<flag>` enrolment property — PostHog's experiment metrics count ~0
conversions even when purchases happened.

**Fix — bridge the variant through the Shopify cart:**

Step 1 — storefront theme, after flags load (writes variant + id onto the cart):
```js
posthog.onFeatureFlags(function () {
  fetch('/cart/update.js', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ attributes: {
      ph_distinct_id: posthog.get_distinct_id(),
      'ph_ff_landing-hero-test': posthog.getFeatureFlag('landing-hero-test'),
      'ph_ff_fathers-day-test':  posthog.getFeatureFlag('fathers-day-test')
      // add one line per running experiment flag
    }})
  });
});
```

Step 2 — wherever `Order Completed` / `Product Added` is sent to PostHog (server-side /
Elevar / Segment / web pixel), read the cart/order attributes and set:
```
distinct_id = order.attributes.ph_distinct_id
properties['$feature/landing-hero-test'] = order.attributes['ph_ff_landing-hero-test']
properties['$feature/fathers-day-test']  = order.attributes['ph_ff_fathers-day-test']
```

**Verify** (PostHog → SQL/HogQL, after shipping):
```sql
SELECT count() FROM events
WHERE event = 'Order Completed' AND timestamp > now() - interval 7 day
  AND properties.`$feature/landing-hero-test` IN ('control','test')
-- expect > 0; the experiment's purchase/ATC metrics then populate natively
```

## Interim workaround (works today, no code changes)
Person-stitch in HogQL: enrol persons via client events carrying `$feature/*`, LEFT JOIN their
`Product Added` / `Order Completed` by `person_id`, restricted to landing-page viewers.
Query patterns are in `EXPERIMENT-LOG.md` (EXP-004/005 section) and `AUTOMATIONS.md` §4.

## Context notes
- PostHog history starts **2026-06-18** → "returning visitor" undercounted beyond ~2 months.
- Experiment `product-addtocart-webview-fix` exists but was never started — confirm intent.
- EXP-003 (colour selector) and EXP-004 (hero) both touch the Pro Mat PDP in the same window —
  read them with each other in mind; avoid stacking PDP tests in future.
