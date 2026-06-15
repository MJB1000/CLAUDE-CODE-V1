# Watchlist — Meta inbox & omnichannel AI agents

Baseline of established/known players for the **Meta inbox** routine (Messenger ·
Instagram DM + comments · WhatsApp → classify · route · draft initial reply,
splitting customers from influencer/collab prospects).

These are tracked here as the *known* set. Most are too old to clear Repo Radar's
`created_within_days` window, so the radar's "Meta inbox & omnichannel AI agents"
lane is for catching **new** entrants against this baseline — not re-reporting these.

> Reminder: "Meta Business Suite" has no public API. Integrations hit the underlying
> Messenger Platform API, Instagram Graph API, and WhatsApp Cloud API.

## Anchor — omnichannel inbox + Meta channels
- **[chatwoot/chatwoot](https://github.com/chatwoot/chatwoot)** — OSS support desk; native Messenger/IG/WhatsApp, routing + auto-assignment, "Captain" AI for triage + initial responses. The recommended base to build on.

## AI-native customer-service platforms (rising)
- **[tgoai/tgo](https://github.com/tgoai/tgo)** — AI agent customer-service platform: LLM orchestration, RAG, multi-channel, human handoff. Agent-first architecture.
- **[evolution-foundation/evo-crm-community](https://github.com/evolution-foundation/evo-crm-community)** — self-hosted AI support platform, Chatwoot/WhatsApp-style.
- **[WuKongOpenSource/AI_CRM](https://github.com/WuKongOpenSource/AI_CRM)** — AI conversational CRM.

## Channel plumbing
- **[evolution-foundation/evolution-api](https://github.com/evolution-foundation/evolution-api)** — WhatsApp integration API; bridges to Chatwoot/dify/typebot/n8n.

## LLM brain — classify / route / draft (build layer)
- **[langgenius/dify](https://github.com/langgenius/dify)** — production agentic-workflow platform; encode the customer-vs-influencer-vs-spam router here.
- **[FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise)** — visual AI-agent builder.
- **[baptisteArno/typebot.io](https://github.com/baptisteArno/typebot.io)** — self-host conversational-flow builder.

## Social-side agents (prospect/outreach context)
- **[brightbeanxyz/brightbean-studio](https://github.com/brightbeanxyz/brightbean-studio)** — self-hostable social management across 10+ platforms.
- **[LocoreMind/locoagent](https://github.com/LocoreMind/locoagent)** — AI social-media agent with real browser automation.

## Known gap (your build opportunity)
No OSS project does **influencer/collab-prospect qualification** as a first-class
route off Meta inbound — intent classifier (support vs collab vs spam) + a
qualifying opener + lead score. That's the differentiated piece to build on top
of Chatwoot + dify.
