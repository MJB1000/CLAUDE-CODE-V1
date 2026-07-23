# DiggerLid Growth Dashboard — live MER / GPAM

Shows the month-to-date scorecard and computes **MER** and **GPAM** live. The Meta/Shopify
tokens stay **server-side** in a tiny feed (`/api/mer`); the dashboard renders computed numbers
only. **Nothing is read from or written to any spreadsheet.**

```
your phone/ads         Vercel /api/mer (holds secrets)         dashboard (this page)
Meta + Shopify  ──────▶  computes MER, GPAM, net profit  ──────▶  renders numbers only
```

## Files
- `index.html` — the dashboard. Works **today** in manual mode (type ad spend). Set `FEED_URL` to go live.
- `api-mer.js` — the Vercel serverless feed. Holds the secrets; returns JSON.

---

## Part A — Get a Meta token (long-lived, `ads_read`)

Use a **System User** token — it doesn't expire like the Graph Explorer one does.

1. **Business Settings → System users:** https://business.facebook.com/settings/system-users
   - **Add** → name it `diggerlid-ops` → role **Employee** → Create.
2. **Assign the ad account:** with the system user selected → **Add Assets** → **Ad Accounts** →
   pick your DiggerLid ad account → toggle **Manage campaigns / View performance** → Save.
3. **Generate token:** click **Generate new token** →
   - App: pick (or create) an app at https://developers.facebook.com/apps/
   - Permissions: tick **`ads_read`** → Generate.
   - **Copy it now** (shown once). This is the secret — it goes into Vercel, never into chat or the repo.
4. **Get your ad account ID:** https://business.facebook.com/settings/ad-accounts —
   it's the number shown; the API wants it prefixed, e.g. `act_1234567890`.

> Quick one-off test instead of a system user: Graph API Explorer
> (https://developers.facebook.com/tools/explorer/) → add `ads_read` → Generate Access Token.
> Fine for a test call, but it expires in ~1–2 h — don't use it for the live feed.

## Part B — Deploy the feed

1. Copy `api-mer.js` into your Vercel calendar project as **`api/mer.js`**
   (the repo behind `diggerlid-calendar-henna.vercel.app`).
2. **Vercel → your project → Settings → Environment Variables**
   (https://vercel.com/dashboard → project → Settings → Environment Variables). Add:
   | Name | Value |
   |---|---|
   | `META_TOKEN` | the system-user token from A3 |
   | `META_ACCOUNT_ID` | `act_...` from A4 |
   | `SHOPIFY_SHOP` | `digger-lid.myshopify.com` |
   | `SHOPIFY_TOKEN` | your `shpat_...` (Admin API, `read_orders`) |
3. **Redeploy** (Deployments → ⋯ → Redeploy).
4. **Test:** open `https://<your-app>.vercel.app/api/mer` → you should see JSON with `mer` and `gpam`.

## Part C — Point the dashboard at it

1. In `index.html`, set:
   ```js
   var FEED_URL = "https://<your-app>.vercel.app/api/mer";
   ```
2. Host `index.html` anywhere (drop it in the same Vercel project as `/dashboard`, or open locally).
   MER/GPAM now populate automatically. *(A claude.ai Artifact sandbox blocks the external fetch —
   host it normally for the live feed; the manual spend box always works.)*

---

## No token yet? It still works
Open `index.html` and type your **MTD Meta spend** into the spend box — MER and GPAM compute
instantly against the live Shopify revenue already baked in. Part A/B just makes it automatic.

**Security:** never paste `META_TOKEN` / `SHOPIFY_TOKEN` into chat, code, or the repo — only into
Vercel's env var UI. If a token ever leaks, rotate it (regenerate the system-user token / reinstall
the Shopify app).
