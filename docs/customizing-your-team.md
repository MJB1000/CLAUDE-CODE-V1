# Customizing Your Marketing Team

## Rename Your Agents

The default names (Sofia, Charlie, Dana) are placeholders. Give your agents names, backstories, and personalities that fit your brand.

### How to Customize

1. Open `config/team.yml` and change the names.
2. Open each agent file in `agents/` and edit the **Who You Are** section.

### What to Include in a Persona

- **Name and age** — specificity activates richer behavior
- **Experience** — what they have seen and done
- **Values** — what they care about and refuse to compromise on
- **Voice** — how they communicate (direct, warm, analytical, etc.)
- **Domain knowledge** — what industry or brand type they know best

### Example: E-Commerce Copywriter

> You are Jamie, 34, a direct-response copywriter who cut their teeth writing for DTC brands.
> You know that every word in a product description is either selling or stalling. You write
> headlines that stop thumbs and CTAs that close. You have zero patience for corporate fluff
> and believe the best copy sounds like a smart friend recommending something they love.

### What NOT to Change

- The **Session Start** steps — these ensure proper file loading
- The **handoff format** — other agents depend on the structure
- The **escalation rules** — these prevent scope drift

## Adapting for Your Domain

### B2B Marketing
- Strategist focuses on funnel stage, ICP alignment, sales enablement
- Copywriter emphasizes value propositions, proof points, technical accuracy
- Designer reviews for professional tone, data presentation, compliance

### Consumer Brand
- Strategist focuses on emotional positioning, cultural relevance, channel mix
- Copywriter emphasizes voice consistency, scroll-stopping hooks, relatability
- Designer reviews for brand feel, visual language alignment, audience resonance

### Content Marketing
- Strategist focuses on SEO strategy, content pillars, distribution plan
- Copywriter emphasizes readability, authority, search intent match
- Designer reviews for structure, scannability, internal linking, CTA placement

## Adding Brand Assets

Point your `team.yml` to existing brand documents:

```yaml
brand:
  voice_guide: "docs/brand-voice.md"
  style_guide: "docs/style-guide.md"
  audience_personas: "docs/personas/"
```

Agents will reference these when the brief calls for it — they will not load them by default (token discipline).
