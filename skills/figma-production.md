# Figma Design Production Skill

Load this skill when Designer is producing visual assets in Figma.
**Must be loaded BEFORE any `use_figma` tool call.**

---

## Prerequisites

- Figma MCP server connected (remote: `https://mcp.figma.com/mcp`)
- Authenticated via `/mcp` → `figma` → Authenticate
- Edit access to target Figma file
- Approved copy from `deliverables/` (never edit copy — place exactly as written)
- `DESIGN-BRIEF.md` from Strategist (layout direction, brand assets, channel specs)

## Tools Available

| Tool | Purpose | When to use |
|---|---|---|
| `use_figma` | Create/modify frames, text, auto-layout, components, variables | Building layouts section by section |
| `generate_figma_design` | Generate full design layers from a description or live UI | Quick full-page generation from approved copy |
| `search_design_system` | Find existing components, variables, styles in connected libraries | ALWAYS search before creating anything new |
| `create_new_file` | Create a blank Figma file in drafts | When no file exists yet |
| `get_screenshot` | Capture current state for review | After each section, and for final review |
| `get_metadata` | Read existing design structure (layer names, IDs, positions) | Before modifying existing files |

---

## Critical Rules (from Figma official docs)

### use_figma — MUST follow these

1. **Return values only** — use `return` for output. Never call `figma.closePlugin()`.
2. **No console.log()** — it won't reach the agent. Only `return` statements work.
3. **Color range is 0–1** — NOT 0–255. Red = `{r: 1, g: 0, b: 0}`.
4. **Load fonts before text** — `await figma.loadFontAsync({family, style})` before ANY text operation.
5. **Page switching is async** — `await figma.setCurrentPageAsync(page)`. Sync setter throws.
6. **FILL sizing AFTER append** — set `layoutSizingHorizontal/Vertical = 'FILL'` AFTER `appendChild()`.
7. **Position away from (0,0)** — new top-level nodes default to origin. Scan existing nodes, offset.
8. **Return ALL node IDs** — mandatory: collect and return every created/mutated node ID.
9. **Await every Promise** — unawaited async = silent failures.
10. **One action per call** — create variables in one call, components in the next, layouts in another. Don't build an entire page in one script.

### Common Mistakes

| Wrong | Correct |
|---|---|
| `{r: 255, g: 0, b: 0}` | `{r: 1, g: 0, b: 0}` |
| Setting text without loading font | `await figma.loadFontAsync({family: 'Inter', style: 'Regular'})` first |
| Building full page in one call | One section per `use_figma` call |
| Hardcoding colors | Use variables: search design system first |
| Creating new components when library has them | `search_design_system` first, import by key |

---

## Marketing Design Workflow (6 steps)

### Step 1: Read the DESIGN-BRIEF.md

Extract:
- Approved copy files → which text goes where
- Channel specs → dimensions, platform
- Brand assets → colors, fonts, logo location
- Design system → `design-systems/[client].md` if referenced
- Layout direction → hierarchy, style, reference examples
- Production specs from STRATEGY-BRIEF.md → image direction, visual treatment

### Step 2: Inspect or create the Figma file

**If file exists (client provided URL):**
```
get_metadata → understand existing structure, pages, naming conventions
```

**If no file:**
```
create_new_file → returns Figma URL → share with Strategist
```

**Then:** Search for existing design system assets:
```
search_design_system → "button", "header", "card", colors, typography
```
Use existing components before creating new ones.

### Step 3: Create page wrapper frame

One `use_figma` call:
- Create a single wrapper frame at the correct dimensions (from channel specs)
- Position away from existing content
- Set auto-layout vertical for the page
- Return the frame ID — all sections will be children of this frame

### Step 4: Build sections incrementally (one per use_figma call)

For each section in the approved copy, make ONE `use_figma` call:

**Landing page example:**
| Call | Section | What to build |
|---|---|---|
| 1 | Page wrapper | Frame at 1440px (or channel spec), auto-layout vertical |
| 2 | Hero | Headline text + subhead text + CTA button. Auto-layout vertical, centered. |
| 3 | Value Props | 3 cards in auto-layout horizontal. Each: heading + body text. |
| 4 | Social Proof | Stats row. Bold numbers + context text. Attribution line. |
| 5 | Offer Block | Background fill + offer text + CTA button. |
| 6 | Footer CTA | Closing line + CTA button. |

**Email example:**
| Call | Section | What to build |
|---|---|---|
| 1 | Email wrapper | Frame at 600px wide, auto-layout vertical |
| 2 | Header | Logo + preheader |
| 3 | Body | Paragraphs of body copy, formatted |
| 4 | CTA | Button component, centered |
| 5 | Footer | Sign-off text + legal/unsubscribe |

**Social ad example:**
| Call | Section | What to build |
|---|---|---|
| 1 | Ad frame | 1080x1080 (feed) or 1080x1920 (stories) |
| 2 | Background | Color fill or image placeholder |
| 3 | Copy | Primary text overlay + headline |
| 4 | CTA | Button or text CTA overlay |
| 5 | Logo | Brand logo placement |

### Step 5: Validate

After building each section:
```
get_screenshot → check for: cropped text, overlaps, wrong colors, misalignment
```

After full page:
```
get_screenshot → full page review
get_metadata → verify structure (correct nesting, naming)
```

Fix any issues with targeted `use_figma` calls.

### Step 6: Hand off

Write `DESIGN-REQUEST.md` with:
- Figma file URL
- List of frames created
- Design decisions made (and why)
- Assets used (from library vs created)
- Known gaps (missing photos, icons, etc.)

---

## Channel-Specific Dimensions

| Channel | Format | Dimensions |
|---|---|---|
| Landing page (desktop) | Web | 1440px wide, auto-height |
| Landing page (mobile) | Web | 375px wide, auto-height |
| Email | Email | 600px wide, auto-height |
| Facebook/Instagram feed | Image | 1080x1080 |
| Facebook/Instagram stories | Image | 1080x1920 |
| Facebook link ad | Image | 1200x628 |
| Google Display | Banner | 300x250, 728x90, 160x600 |
| LinkedIn | Image | 1200x627 |

## Typography Loading

Common marketing fonts — load before use:
```javascript
await figma.loadFontAsync({family: 'Inter', style: 'Regular'})
await figma.loadFontAsync({family: 'Inter', style: 'Bold'})
await figma.loadFontAsync({family: 'Inter', style: 'Semi Bold'})
```

If client has custom fonts, they must be available in the Figma file/team.
Check with `search_design_system` for available text styles.

## Rules

- **Never edit copy.** Place exactly what was approved. Character for character.
- **Search before creating.** Always check design system for existing components.
- **One section per call.** Don't build the whole page in one script.
- **Validate visually.** Screenshot after each section.
- **Return node IDs.** Every `use_figma` call returns created/mutated IDs.
- **Use variables over hardcoded values.** Bind colors and spacing to design tokens.
- **Flag missing assets.** Log to CAMPAIGN-LOG Known Gaps if you need images/icons that don't exist.
