# Keys & Access — What the New Account Needs

> **Values NEVER go in this repo or in chat.** This is the shopping list — names, scopes,
> where each value lives. A key pasted into chat is burned: rotate it.

## A. Keys to place server-side (Vercel `diggerlid-mer` → Settings → Environment Variables)

| # | Env var | What it is | Scope needed | Status |
|---|---|---|---|---|
| 1 | `META_TOKEN` | Meta system-user token | `ads_read` on the DiggerLid ad account | ✅ already set (powers /api/mer) |
| 2 | `META_ACCOUNT_ID` | `act_…` ad account id | — | ✅ already set |
| 3 | `KLAVIYO_API_KEY` | Klaviyo private key | read metrics/profiles | ✅ already set (powers /api/emails) |
| 4 | `SHOPIFY_SHOP` | `digger-lid.myshopify.com` | — | optional (lets /api/mer compute revenue itself) |
| 5 | `SHOPIFY_TOKEN` | Admin API token | `read_orders` | optional, pairs with #4 |
| 6 | `ALIA_API_KEY` | Alia popup API bearer | read events/stats | ⚠️ **ROTATE** (old one pasted in chat) then set — unlocks /api/popup (task #7) |
| 7 | `POSTHOG_API_KEY` | PostHog personal API key | read (project 475333, US cloud) | ⚠️ **ROTATE** (pasted in chat) then set — unlocks automated experiment reads |

## B. Per-person connector access (no shared keys — each Claude account connects its own)

| Connector | Who needs it | Grants |
|---|---|---|
| **GitHub** (this repo) | everyone using the agent | read (analysts) / write (CoS + Scorekeeper owner) |
| **Shopify MCP** | anyone running scorecards/analytics | their own Shopify staff login |
| Gmail / Calendar / Notion / Figma / Canva | optional, per workflow | per-person |

## C. Explicitly NOT needed by the new account

- Raw Meta / Klaviyo / Shopify tokens — everything flows through the public Vercel endpoints
  (`/api/mer`, `/api/emails`, `/api/campaigns`) which hold the secrets server-side.
- The old account's chat history — everything durable is in this repo
  (`MIGRATION-BOOTSTRAP.md`, `LEARNINGS.md`, logs, deliverables).

## D. Rotation log

| Key | Last rotated | Reason |
|---|---|---|
| Alia | pending | pasted in chat 2026-08-16 |
| PostHog | pending | pasted in chat 2026-08-20 |

Update this table whenever a key is rotated.
