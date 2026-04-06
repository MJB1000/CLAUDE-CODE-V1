# Notion Knowledge Layer — Shared Agent Memory

Load this skill when any agent needs to query or update the team's shared knowledge.
This replaces flat-file knowledge (PLAYBOOK.md, SWIPE-FILE.md, clients/) with
queryable Notion databases.

---

## Setup (one-time)

Before first use, Strategist creates four Notion databases under a "Marketing Team" parent page.
Use `mcp__notion__API-create-a-data-source` for each.

### Database Schemas

**1. Clients DB**
| Property | Type | Purpose |
|---|---|---|
| Name | title | Client name |
| Brand Voice | rich_text | How the brand sounds |
| Voice Dos | rich_text | Specific tone qualities |
| Voice Donts | rich_text | Things the brand avoids |
| Primary Audience | rich_text | Who buys |
| Competitors | rich_text | Key competitors |
| Approved Stats | rich_text | Verified claims |
| Unapproved Claims | rich_text | Needs verification |
| Industry | select | DTC / SaaS / Services / etc. |
| Last Updated | date | When profile was last updated |

**2. Patterns DB**
| Property | Type | Purpose |
|---|---|---|
| Pattern | title | The lesson learned |
| Category | select | audience / review / channel / brief / anti-pattern |
| Channel | multi_select | email / landing-page / google-ads / social-ads / etc. |
| Audience | rich_text | Which audience type this applies to |
| Status | select | observed / validated / invalidated |
| Source | rich_text | Who caught it, which campaign |
| Campaign | rich_text | Campaign name |
| Metric | rich_text | Performance data that validated/invalidated it |
| Date | date | When pattern was logged |

**3. Swipe File DB**
| Property | Type | Purpose |
|---|---|---|
| Copy | title | The actual copy text |
| Type | select | headline / subject-line / CTA / value-prop / ad-copy / social-proof |
| Channel | select | email / landing-page / google-ads / social-ads |
| Audience | rich_text | Who this was written for |
| Campaign | rich_text | Which campaign |
| Metric | rich_text | Performance result (or "pending") |
| Status | select | validated / pending / underperformed |
| Date | date | When saved |

**4. Campaign Tracker DB**
| Property | Type | Purpose |
|---|---|---|
| Campaign | title | Campaign name |
| Client | relation | → Clients DB |
| Status | select | planning / in-progress / published / measuring / complete |
| Channel | multi_select | Channels used |
| Deliverables | number | Count of deliverables |
| Publish Date | date | When campaign went live |
| 7-Day Check | checkbox | 7-day retro done? |
| 30-Day Check | checkbox | 30-day retro done? |
| Outcome | rich_text | Summary of results |

---

## Agent-Specific Queries

### Strategist — reads at brief-writing time

**Get client profile:**
```
Query Clients DB → filter: Name = "[client name]"
→ Returns: brand voice, approved assets, competitors, audience
```

**Get relevant patterns for this brief:**
```
Query Patterns DB → filter: Channel = "[target channel]" AND Status = "validated"
→ Returns: proven patterns to include in Learned Patterns section
```

**Get campaign history for returning client:**
```
Query Campaign Tracker DB → filter: Client = "[client]" → sort: Publish Date desc
→ Returns: past campaigns, outcomes, open metric check-ins
```

### Copywriter — reads at writing time

**Get swipe file for this channel + audience:**
```
Query Swipe File DB → filter: Channel = "[channel]" AND Status = "validated"
→ sort: Date desc → limit: 10
→ Returns: best-performing copy for this channel
```

**Get channel patterns:**
```
Query Patterns DB → filter: Channel = "[channel]" AND Category = "channel"
→ Returns: constraints + patterns specific to this channel
```

### Designer — reads at review time

**Get review patterns for this channel:**
```
Query Patterns DB → filter: Category = "review" AND Channel = "[channel]"
→ Returns: what to look for in this specific channel
```

---

## Auto-Populate After Each Campaign

### Post-retro (Strategist runs this after writing RETRO.md):

**1. Save patterns to Patterns DB:**
- Read retros/RETRO-[N].md "Rules to Carry Forward" section
- For each rule: create row in Patterns DB with:
  - Pattern = rule text
  - Category = [infer from context: review/channel/brief/audience]
  - Channel = [from brief]
  - Status = "observed"
  - Source = "Campaign [name], Designer Round [N]" or "Retro"
  - Date = today

**2. Save winning copy to Swipe File DB:**
- Read the cleared deliverable files
- Extract: headlines, CTAs, subject lines, value props that Designer locked in Round 1
  (these are the sections that passed first time — strongest copy)
- For each: create row in Swipe File DB with:
  - Copy = the actual text
  - Type = [headline/CTA/subject-line/etc.]
  - Channel = [from brief]
  - Audience = [from brief]
  - Status = "pending" (becomes "validated" at 30-day retro if metrics confirm)
  - Date = today

**3. Update client profile:**
- Query Clients DB for the client
- Update: Approved Stats (if new stats were confirmed), Last Updated
- Add campaign to Campaign Tracker DB

### At 30-day retro (Strategist runs this):

**4. Promote or invalidate patterns:**
- Query Patterns DB → filter: Campaign = "[this campaign]" AND Status = "observed"
- For each: if metric confirms the pattern → update Status to "validated"
  If metric contradicts → update Status to "invalidated"
- Query Swipe File DB → same logic for copy entries

---

## Fallback: Local Files

If Notion is not connected (no MCP available), fall back to the local markdown files:
- `clients/[name].md` instead of Clients DB
- `PLAYBOOK.md` instead of Patterns DB
- `knowledge/SWIPE-FILE.md` instead of Swipe File DB
- `handoff/CAMPAIGN-LOG.md` instead of Campaign Tracker DB

The markdown files are the offline backup. Notion is the live source of truth when connected.

---

## Rules

- **Query, don't dump.** Never load an entire Notion database. Filter to what's relevant.
- **Always specify channel and audience in queries.** Generic queries return too much.
- **Validated > observed.** When patterns conflict, validated patterns win.
- **Auto-populate is not optional.** After every retro, run the post-retro steps. If you skip it, the knowledge layer degrades.
