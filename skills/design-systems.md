# Design Systems Skill

Load this skill when Designer is producing visual assets (Figma, HTML, or mockups).

---

## What DESIGN.md Files Are

DESIGN.md files are plain-text design system documents that encode a brand's complete
visual identity: colors, typography, spacing, components, elevation, responsive behavior.
They follow the Google Stitch DESIGN.md format specification (9 sections).

AI agents use them to generate UI that matches a specific visual identity without
Figma exports, JSON schemas, or special tooling.

## When to Use

- Designer is producing Figma layouts (via Figma MCP)
- Designer is generating HTML mockups or wireframes
- Strategist is briefing a campaign for a known brand
- Client does not have a formal style guide — use an industry reference as a starting point

## How to Use

### Option 1: Client has a brand — create a custom DESIGN.md

Extract the client's visual system from their website or brand guide into a DESIGN.md file:

```
design-systems/[client-name].md
```

Follow the 9-section format:
1. Visual theme / mood
2. Color palette (with semantic naming)
3. Typography hierarchy
4. Component styling
5. Layout principles / spacing scale
6. Elevation / shadow system
7. Responsive breakpoints
8. Design guardrails (what NOT to do)
9. Dark mode variants (if applicable)

### Option 2: Use a reference system

Browse the awesome-design-md collection for inspiration:
https://github.com/VoltAgent/awesome-design-md

55+ design systems from brands like Stripe, Notion, Figma, Airbnb, Linear, etc.
Copy a relevant DESIGN.md into `design-systems/` and adapt it for the client.

### Option 3: No brand exists yet — start from a reference

For new brands without visual identity, pick a reference closest to the desired feel:

| Client type | Reference suggestion |
|---|---|
| Fintech / SaaS | Stripe, Linear |
| Creative / Design | Figma, Framer |
| Developer tools | Vercel, Raycast |
| Consumer / Marketplace | Airbnb, Uber |
| Productivity | Notion, Miro |
| AI / Tech | Claude, Cohere |

## Integration with DESIGN-BRIEF.md

When Strategist writes DESIGN-BRIEF.md, reference the design system:

```
### Design System
- File: design-systems/[client-name].md
- Override: [any deviations from the system for this deliverable]
```

Designer reads the DESIGN.md file at the start of design production, alongside
DESIGN-BRIEF.md and the approved copy from deliverables/.

## Rules

- **DESIGN.md is a reference, not a constraint.** Client brand decisions override it.
- **One DESIGN.md per client.** Do not mix systems within a campaign.
- **Create, don't copy, for real clients.** The awesome-design-md collection is for
  inspiration and starting points. Real client work needs a custom DESIGN.md extracted
  from their actual brand.
- **Store in `design-systems/`.** Not in handoff/ or deliverables/.
