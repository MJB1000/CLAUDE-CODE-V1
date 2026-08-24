# Data-source registry

How the hub gets its numbers. **Live** = reachable now; **to-wire** = needs a key in the hub's
secret store (you generate it; never pasted into chat or this repo).

## Live now
| Source | Provides | Access |
|---|---|---|
| **Shopify** (Advanced, AUD) | revenue, orders, AOV, CVR, sessions, returning-customer rate, product/channel mix | MCP / Admin API (connected) |
| **Ecommerce Equation baseline** | cost ratios → GPAM engine; 2026 monthly actuals; targets | `data/ee-baseline.json` (this repo) |
| **Marketing calendar** | 62 dated items, `tier: major` launches, `goLive[]` times | `https://diggerlid-calendar-henna.vercel.app/plan.json` (public, no auth) |
| **Weekly Meeting doc** | scorecard history, decisions, action items | Google Doc `18fx…AZ2VM` (shared to matthewjbedwell@gmail.com) |
| **Projects & Experiments board** | ICE-scored projects, owners, status | Google Sheet `1LL_…Pk6UI` (shared) |

## To wire (into the hub secret store)
| Source | Unlocks | Auth |
|---|---|---|
| **Meta Marketing API** | live **MER, blended CAC, ROAS**, CPP by campaign | System User token, scope `ads_read` |
| **Klaviyo API** | email/SMS attributed revenue + flow revenue → **retention (Obj 5)**; fixes Shopify's "email = 2 orders" | private read key |
| **Shopify Admin — per-SKU COGS** | sharpen GPAM beyond flat 40% | `InventoryItem.unitCost` (existing Shopify auth) |
| **Yotpo** (optional) | VoC review mining via API | Yotpo API key |

## Not reachable from cloud
| Source | Why | Fix |
|---|---|---|
| **DL CRM Dashboard** | local Mac file / Cowork-space artifact; no cloud filesystem access | migrate partner data to a Sheet / Notion DB / hub Supabase, then the CoS can sync + age threads |

## Secret handling
All to-wire keys live in the **Paperclip company secret store** (encrypted), injected at heartbeat.
Never committed here, never pasted into a ticket/comment/chat. The BlitzOS `bootstrap.sh` credential
scan applies to any context repo the agents use.
