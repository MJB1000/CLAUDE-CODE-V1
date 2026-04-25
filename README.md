# Marketing Team

Three AI agents (Strategist, Copywriter, Designer) that produce reviewed, on-brand marketing content with Figma wireframes through structured handoffs.

## Quick Start

### In Claude Cowork
1. Connect this repo
2. Paste: `You are Sofia on this project. Read CLAUDE.md, then marketing-team.md. Report status, then wait for me.`

### In Claude.ai Projects
1. Create a Project → add `marketing-team.md` as knowledge
2. Say: `You are Sofia. Report status, then wait for me.`

### In any Claude conversation
1. Paste the contents of `marketing-team.md` at the start
2. Say: `You are Sofia. Report status, then wait for me.`

## What it produces

- Strategy documents with execution checklists
- Email copy (paste-ready for Klaviyo/Mailchimp)
- Landing page copy with content hierarchy
- Social ad copy (Facebook, Instagram — feed + stories)
- Google Ads (responsive search — 15 headlines + 4 descriptions)
- Figma wireframes (email, ad, landing page layouts via MCP)
- Campaign summary documents (shareable with stakeholders)

## How it works

```
You brief Sofia → Sofia asks questions → writes strategy + brief
→ Charlie writes copy → Dana reviews + builds Figma wireframes
→ Charlie fixes → Dana clears → Sofia presents → you say "ship"
```

## Files

| File | What it does |
|---|---|
| `marketing-team.md` | The complete skill — all 3 agents, workflow, templates |
| `CLAUDE.md` | Session router for Cowork (auto-loaded) |
| `knowledge/COPYWRITING-PRINCIPLES.md` | Charlie's Schwartz/Breakthrough Advertising reference |

## Adapted from

[Three Man Team](https://github.com/russelleNVy/three-man-team) by russelleNVy — adapted for marketing with Figma MCP integration, learning loops, and Breakthrough Advertising principles.
