# Notion Publishing Skill

Load this skill when Strategist is publishing deliverables to Notion.

---

## When to Use

After the launch gate is approved and the CD says "ship," Strategist publishes
deliverables to Notion using the Notion MCP tools.

## Available Tools

| Tool | Use for |
|---|---|
| `search-notion` | Find existing pages/databases in the workspace |
| `create-a-page` | Create new pages under a parent page or database |
| `append-a-block` | Add content blocks (text, headings, lists, dividers) to a page |
| `update-a-page` | Modify page properties |
| `query-data-source` | Query databases for campaign tracking |

## Formatting Rules

Notion MCP accepts Markdown. Use these conventions for consistent output:

### Page Structure

Every deliverable page follows this structure:
1. **Page title** — deliverable name + campaign name
2. **Properties** (if in a database) — Status, Channel, Campaign, Date, Deliverable #
3. **Metadata block** — campaign, deliverable number, date, status
4. **Content** — the actual deliverable copy
5. **Compliance notes** — flags, placeholders, source tags
6. **Review history** — summary of what was caught and fixed

### Markdown → Notion Block Mapping

| Markdown | Notion Block |
|---|---|
| `# Heading` | Heading 1 |
| `## Heading` | Heading 2 |
| `### Heading` | Heading 3 |
| `**bold**` | Bold text |
| `*italic*` | Italic text |
| `- item` | Bulleted list |
| `1. item` | Numbered list |
| `> quote` | Quote block |
| `---` | Divider |
| `[text](url)` | Link |
| `` `code` `` | Inline code |

### Deliverable-Specific Formatting

**Email deliverables:**
```
# [Campaign] — Email: [Name]

## Subject Line
**[subject line text]**

## Preview Text
*[preview text]*

---

## Email Body

[body copy with formatting preserved]

---

## CTA
**[CTA text]**

---

## Compliance Notes
- [notes]
```

**Landing page deliverables:**
```
# [Campaign] — Landing Page: [Name]

## Hero Section
### Headline
**[headline]**

### Subhead
[subhead text]

### CTA
**[CTA text]**

---

## Value Propositions

### 1. [VP heading]
[VP body]

### 2. [VP heading]
[VP body]

### 3. [VP heading]
[VP body]

---

## Social Proof
- **[stat]** — [context]
- **[stat]** — [context]

*[attribution line]*

---

## Offer Details
[offer copy]

---

## Compliance Notes
- [notes]
```

**Google Ads deliverables:**
```
# [Campaign] — Google Ads: [Name]

## Ad Group 1: [Name]
**Keywords:** [keywords]

### Headlines
| # | Headline | Chars |
|---|---|---|
| 1 | [text] | [n] |

### Descriptions
| # | Description | Chars |
|---|---|---|
| 1 | [text] | [n] |

---

[Repeat for each ad group]

## Compliance Notes
- [notes]
```

**Social ad deliverables:**
```
# [Campaign] — Social Ads: [Name]

## Variant 1 — [Angle]
**Primary text:** [text] *(chars)*
**Headline:** [text] *(chars)*

---

[Repeat for each variant]

## Compliance Notes
- [notes]
```

## Publishing Workflow

1. **Find or create the campaign parent page** in Notion
   - Search for existing campaign page: `search-notion`
   - If none exists: `create-a-page` under the marketing workspace
2. **Create a page for each deliverable** under the campaign parent
   - Use the appropriate format template above
   - Set page properties if publishing to a database (Status: Published, Channel, Date)
3. **Append the formatted content** using `append-a-block`
4. **Add a review history section** at the bottom summarizing what the Designer caught
5. **Log the Notion page URL** to CAMPAIGN-LOG under the deliverable entry

## Notion Workspace Structure (Recommended)

```
Marketing /
├── Campaigns /
│   ├── WiperTech Winter Sale /
│   │   ├── 01a — Email: Launch Announcement
│   │   ├── 01b — Landing Page: Winter Sale
│   │   ├── 01c — Social Ads: Winter Sale
│   │   ├── 02a — Google Ads: Winter Sale
│   │   └── 02b — Landing Page: Google Ads
│   └── [Next Campaign] /
├── Playbook (synced from PLAYBOOK.md)
└── Campaign Tracker (database)
```

## Rules

- **Never edit deliverable copy during publishing.** Place exactly what was approved.
- **Preserve all formatting.** Headlines stay as headings, lists stay as lists.
- **Include compliance notes on every page.** They are part of the deliverable.
- **Log the Notion URL.** Strategist updates CAMPAIGN-LOG with the published page link.
