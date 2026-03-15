---
name: notion-sync
description: Sync Notion Projects, Engineering Specs, Design Briefs, and Launch Planning to PM workspace. Use when running /sync-notion or /sync-dev commands, or creating initiatives from Notion projects.
---

# Notion Sync Skill

Procedural knowledge for synchronizing Notion project data with PM workspace initiatives. Makes initiatives the central hub by pulling from Notion as a source of truth.

## When to Use

- Running `/sync-notion` command
- Running `/sync-dev` for unified dev status
- Creating new initiatives from Notion projects
- Syncing design briefs and engineering specs
- Checking launch dates and ship timelines
- Cross-referencing Linear via Engineering Specs' "Linear Epic" field

## Prerequisites

Requires Notion MCP tools. Two options available:

### Option 1: Dedicated Notion MCP

- `notion-fetch` - Fetch database/page content
- `notion-search` - Search across workspace

### Option 2: Composio MCP (composio-config)

**Server:** `composio-config`

The unified Composio MCP provides Notion tools with different naming:

- `NOTION_QUERY_DATABASE` - Query database content
- `NOTION_SEARCH_NOTION_PAGE` - Search across workspace
- `NOTION_FETCH_DATABASE` - Fetch database schema
- `NOTION_RETRIEVE_PAGE` - Get page content
- `NOTION_CREATE_NOTION_PAGE` - Create new pages
- `NOTION_UPDATE_PAGE` - Update pages

**Note:** The `composio-config` server also provides Slack, Linear, HubSpot, and PostHog tools (700+ total).

## Data Sources

### Notion Databases (V2 Structure)

The Product teamspace follows a 4-layer system. Full architecture: `pm-workspace-docs/runbooks/notion-v2-implementation-guide.md`

| Database | ID | Purpose |
|---|---|---|
| Projects | `2c0f79b2-c8ac-802c-8b15-c84a8fce3513` | Layer 2 - shippable work items |
| Roadmap | `310f79b2-c8ac-8151-980c-c74fd238daa0` | High-level what/when view |
| Initiatives | `310f79b2-c8ac-816b-8abd-f8fcd3824f31` | Strategic bets containing projects |
| Teams Roster | `310f79b2-c8ac-814a-b8e4-f525b17e2750` | Layer 1 - cross-functional squads |
| Weekly Updates | `310f79b2-c8ac-8169-9d3f-f2bcebdc3d15` | Layer 4 - company-wide updates |
| Engineering Specs | `7321cbcb-31a9-470f-b15d-0f472d2c5eb8` | Technical specifications |
| Design Specs | `310f79b2-c8ac-81d1-a39a-e26426a12b30` | Design deliverables and Figma links |
| Research | `310f79b2-c8ac-812c-bc08-d580369ff0d8` | User research, market research |
| Companies | `310f79b2-c8ac-81b8-907b-cb0fe95378cd` | Customer accounts (seeded from HubSpot) |
| Contacts | `310f79b2-c8ac-8182-b8d9-cbacddc200c5` | People at customer companies |
| Feedback Triage | `310f79b2-c8ac-8102-ad47-cc8111174e47` | Raw customer feedback |
| Feature Requests | `310f79b2-c8ac-8190-9713-dc5cfc78d976` | Aggregated feature requests |
| Meeting Notes | `309f79b2-c8ac-804d-b319-f83c1d017074` | Meeting notes content |
| Decision Log | `310f79b2-c8ac-813b-b2d5-cfbfe324f418` | Extracted decisions |
| Insights | `310f79b2-c8ac-814f-a075-ebf99b75211c` | Data observations |
| Experiments | `310f79b2-c8ac-814c-9feb-e4b10eefb1b4` | A/B tests and experiments |
| Retrospectives | `310f79b2-c8ac-817d-80bc-dc9aaebba0d7` | Post-launch reviews |
| Tasks | `38fa1709-c988-40a6-908a-a8927657b0b4` | Layer 3 - day-to-day work items |

### Local Data

- `pm-workspace-docs/initiatives/active/*/_meta.json` - Active initiative metadata with Notion links
- `pm-workspace-docs/initiatives/done/*/_meta.json` - Completed initiative metadata
- `pm-workspace-docs/initiatives/archived/*/_meta.json` - Archived (local-only) initiatives
- `pm-workspace-docs/signals/` - Processed signals storage
- `pm-workspace-docs/status/` - Status reports

## Initiative Mapping

### Strategy: Notion as Source of Truth

Notion Projects database drives initiative structure. For each Notion project:

1. **Check if local initiative exists** - Match by `notion_project_id` in `_meta.json` (search in `active/`, `done/`, `archived/`)
2. **Create initiative if missing** - Generate folder in `active/`, create `_meta.json`
3. **Sync metadata** - Update phase, stakeholders, links
4. **Extract Linear connection** - Via Projects DB "Linear Link" OR Engineering Specs "Linear Epic"
5. **Fetch related artifacts** - Design Briefs, Eng Specs, Launch Planning

### \_meta.json Schema for Notion

```json
{
  "name": "Global Chat",
  "slug": "global-chat",
  "phase": "build",
  "parent_initiative": null,
  "roadmap_theme": "AI-First UX",
  "notion_project_id": "abc123-...",
  "notion_project_url": "https://www.notion.so/ask-elephant/Global-Chat-abc123",
  "linear_project_id": "05066db9-89d7-432c-bffd-234ca92af024",
  "linear_project_url": "https://linear.app/askelephant/project/global-chat-05066db9",
  "slack_channel": "https://askelephant.slack.com/archives/C12345678",
  "notion_artifacts": {
    "documents": [
      {
        "id": "doc-id",
        "title": "Global Chat PRD",
        "doc_type": "prd",
        "stage": "Approved"
      }
    ],
    "engineering_specs": [
      {
        "id": "spec-id",
        "name": "Chat Architecture Spec",
        "status": "Complete",
        "linear_epic_url": "https://linear.app/askelephant/issue/ASK-1234",
        "complexity": "Large"
      }
    ],
    "design_briefs": [
      {
        "id": "brief-id",
        "name": "Chat UX Brief",
        "status": "In Progress",
        "figma_link": "https://figma.com/...",
        "due_date": "2026-02-01"
      }
    ],
    "launch_planning": [
      {
        "id": "launch-id",
        "name": "Chat v2 Launch",
        "date": "2026-02-15",
        "tier": "P2",
        "status": "Not started"
      }
    ]
  },
  "milestones": [
    {
      "id": "milestone-1",
      "title": "Beta Release",
      "status": "Shipped",
      "target_date": "2026-02-01",
      "eta_confidence": "High"
    }
  ],
  "outcomes": {
    "baseline": 1500,
    "target": 3000,
    "actual": 1800,
    "confidence": "High",
    "target_date": "2026-03-01",
    "status": "On Track"
  },
  "customer_requests": [
    {
      "hubspot_company": "Acme Corp",
      "slack_signal": "https://askelephant.slack.com/archives/C.../p...",
      "status": "Notified"
    }
  ],
  "metric_links": [
    {
      "posthog_dashboard": "https://app.posthog.com/dashboard/...",
      "stripe_metric": "MRR Impact"
    }
  ],
  "stakeholders": {
    "pm_owner": ["person-id-1"],
    "engineering_lead": ["person-id-2"],
    "design_lead": ["person-id-3"],
    "revenue_lead": ["person-id-4"]
  },
  "dev_activity": {
    "last_synced": "2026-01-23T18:00:00Z"
  }
}
```

## Sync Procedures

### Step 1: Fetch Active Projects

Use `notion-search` with Projects database to get active projects:

```
Query: Projects DB (collection://2c0f79b2-c8ac-802c-8b15-c84a8fce3513)
Filter: Project Phase NOT IN ["Done", "Cancelled", "On Hold"]
```

For each project, extract:

- **Project name** → initiative name
- **Project Phase** → map to lifecycle phase
- **Linear Link** → `linear_project_url` (first Linear connection)
- **Engineering** → engineering stakeholders
- **Design** → design stakeholders
- **Sponsors** → PM/leadership sponsors
- **Feedback** relation → research signals to sync

### Step 2: Fetch Engineering Specs

For each project, fetch related Engineering Specs:

```
Query: Eng Specs DB (collection://2c4afb5d-2729-439b-8a07-c2243d7c60a7)
Filter: Related Project = [project_id]
```

Extract:

- **Spec Name** → artifact name
- **Linear Epic** → **SECONDARY LINEAR CONNECTION** (URL to Linear)
- **Complexity** → effort estimation (Small/Medium/Large/XL)
- **Status** → Not Started/In Progress/Review/Complete
- **Engineering Lead** → assignee

**Key insight**: The `Linear Epic` field in Engineering Specs provides another way to connect to Linear, independent of the Projects DB "Linear Link".

### Step 3: Fetch Design Briefs

For each project, fetch related Design Briefs:

```
Query: Design Briefs DB (collection://52148f9a-fe0b-4d8f-a666-e89fc6f3c504)
Filter: Related Project = [project_id]
```

Extract:

- **Brief Name** → artifact name
- **Figma Link** → design artifact URL
- **Status** → design progress
- **Type** → UI/UX Design, User Research, Prototype, Visual Design, Design System
- **Design Lead** → assignee
- **Due Date** → deadline

### Step 4: Fetch Launch Planning

For each project, fetch related Launch Planning:

```
Query: Launch Planning DB (collection://296f79b2-c8ac-8002-9aae-000bf14c5a26)
Filter: Projects Database = [project_id]
```

Extract:

- **Launch Planning** → launch name
- **Date** → ship/launch date
- **Launch Tier** → P1 (major) to P5 (minor)
- **Status** → Not started/In progress/Done

### Step 5: Map Notion Phase to Initiative Phase

| Notion Phase | Initiative Phase |
| ------------ | ---------------- |
| Discovery    | discovery        |
| Definition   | define           |
| Build        | build            |
| Test         | validate         |
| Done         | launch           |
| Cancelled    | cancelled        |
| On Hold      | paused           |

### Step 6: Extract Linear Connections

Two sources for Linear project links:

1. **Projects DB "Linear Link" field** - Direct URL to Linear project
2. **Eng Specs DB "Linear Epic" field** - URL to Linear epic/issue

Extract `linear_project_id` from URL patterns:

- `https://linear.app/askelephant/project/[slug]-[id]` → extract `id`
- `https://linear.app/askelephant/issue/ASK-[num]` → lookup issue → get project

### Step 7: Update or Create Initiative

**If initiative exists** (matched by `notion_project_id`):

```
1. Update phase from Notion
2. Update stakeholders
3. Merge notion_artifacts arrays
4. Update dev_activity.last_synced
```

**If initiative doesn't exist**:

```
1. Create initiative folder: pm-workspace-docs/initiatives/active/[slug]/
2. Create _meta.json with full schema (including notion_project_id)
3. Create empty research.md, prd.md placeholders
4. Add to sync-queue.md for user confirmation
```

### Step 8: Update Sync Queue (for ambiguous mappings)

When confidence is low or conflicts detected:

```markdown
## New Initiative from Notion

**Notion Project:** "Customer Health Scoring"
**Suggested Slug:** customer-health-scoring
**Phase:** Discovery
**Linear Connection:** Not found (no Linear Link in Notion)

**Action:** [Create initiative] [Map to existing] [Skip]

---

## Multiple Linear Connections Found

**Initiative:** global-chat
**Source 1:** Projects DB "Linear Link" → Global Chat project (05066db9)
**Source 2:** Eng Specs "Linear Epic" → ASK-4500 issue (in different project)

**Action:** [Use Projects DB link] [Use Eng Specs link] [Manual review]
```

## Output Formats

### Notion Sync Status Report

```markdown
# Notion Sync Status

**Generated:** 2026-01-23 18:00
**Source:** Notion Product Command Center

---

## Projects Synced

| Project       | Phase     | Initiative    | Linear Connected | Artifacts        |
| ------------- | --------- | ------------- | ---------------- | ---------------- |
| Global Chat   | Build     | global-chat   | ✅               | 2 specs, 1 brief |
| CRM Agent     | Build     | crm-exp-ete   | ✅               | 1 spec, 2 briefs |
| Rep Workspace | Discovery | rep-workspace | ❌               | 0 specs, 1 brief |

---

## Initiatives Created

- **customer-health-scoring** - Created from Notion, pending confirmation
- **partner-onboarding-v2** - Created from Notion, pending confirmation

---

## Artifacts Synced

### Engineering Specs

| Spec              | Project     | Status      | Linear Epic | Complexity |
| ----------------- | ----------- | ----------- | ----------- | ---------- |
| Chat Architecture | Global Chat | Complete    | ASK-4200    | Large      |
| CRM Sync Engine   | CRM Agent   | In Progress | ASK-4350    | XL         |

### Design Briefs

| Brief         | Project     | Status      | Figma | Due Date |
| ------------- | ----------- | ----------- | ----- | -------- |
| Chat UX v2    | Global Chat | Review      | ✅    | Feb 1    |
| CRM Dashboard | CRM Agent   | In Progress | ✅    | Feb 15   |

### Launch Planning

| Launch         | Project     | Date   | Tier | Status      |
| -------------- | ----------- | ------ | ---- | ----------- |
| Chat v2 Launch | Global Chat | Feb 15 | P2   | Not started |
| CRM Beta       | CRM Agent   | Mar 1  | P3   | Not started |

---

## Sync Queue (Needs Attention)

3 items need your input:

- `pm-workspace-docs/sync-queue.md`

---

## Linear Cross-Reference

Projects with Linear connections found via Engineering Specs:

- Global Chat: ASK-4200 (Chat Architecture spec)
- CRM Agent: ASK-4350 (CRM Sync Engine spec)

This provides validation for Linear sync mappings.
```

### JSON Output

```json
{
  "generated_at": "2026-01-23T18:00:00Z",
  "source": "notion",
  "projects_synced": [
    {
      "notion_id": "abc123",
      "name": "Global Chat",
      "phase": "build",
      "initiative_slug": "global-chat",
      "linear_connected": true,
      "linear_sources": ["projects_db", "eng_specs"],
      "artifacts": {
        "engineering_specs": 2,
        "design_briefs": 1,
        "launch_planning": 1
      }
    }
  ],
  "initiatives_created": [],
  "sync_queue_items": 3,
  "linear_cross_refs": [
    {
      "initiative": "global-chat",
      "eng_spec": "Chat Architecture",
      "linear_epic": "ASK-4200"
    }
  ]
}
```

## Smart Inference Engine

### Mapping Confidence Scoring

| Signal                                          | Confidence Boost |
| ----------------------------------------------- | ---------------- |
| Exact `notion_project_id` match in `_meta.json` | +100% (definite) |
| Project name matches initiative name            | +60%             |
| Linear Link matches `linear_project_id`         | +80%             |
| Eng Spec Linear Epic in same Linear project     | +70%             |
| Keyword overlap > 50%                           | +40%             |
| Same stakeholders                               | +30%             |

**Thresholds:**

- ≥80%: Auto-map without confirmation
- 60-79%: Auto-map, note in sync report
- <60%: Add to sync-queue.md for user confirmation

### Handling New Notion Projects

When a Notion project has no matching local initiative:

1. **Check existing initiatives** for similar names/keywords
2. **If close match found** (>60% confidence): Suggest mapping in sync-queue
3. **If no match**: Offer to create new initiative

```markdown
## New Notion Project Detected

**Project:** Customer Health Scoring
**Phase:** Discovery
**Engineering:** @Palmer
**Design:** @Adam

**Similar existing initiatives:**

- customer-journey-map (45% match - different focus)

**Recommended action:** Create new initiative "customer-health-scoring"

[Create Initiative] [Map to Existing] [Skip]
```

## Error Handling

### Notion Access Error

```
⚠️ Cannot access Notion database.

Ensure Notion MCP is configured with access to:
- Projects DB (2c0f79b2-c8ac-802c-8b15-c84a8fce3513)
- Engineering Specs DB (2c4afb5d-2729-439b-8a07-c2243d7c60a7)
- Design Briefs DB (52148f9a-fe0b-4d8f-a666-e89fc6f3c504)
- Launch Planning DB (296f79b2-c8ac-8002-9aae-000bf14c5a26)
```

### Missing Related Project Link

```
ℹ️ Engineering Spec "Auth Migration" has no Related Project link.

This spec cannot be automatically mapped to an initiative.
Add a Related Project in Notion or manually link in sync-queue.md.
```

### Conflicting Linear Connections

```
⚠️ Multiple Linear connections found for "Global Chat":

1. Projects DB "Linear Link": https://linear.app/.../project-a
2. Eng Specs "Linear Epic": https://linear.app/.../project-b (different project!)

Added to sync-queue.md for manual resolution.
```

## Integration Points

### With Linear Sync

- Notion "Linear Link" provides primary Linear project mapping
- Eng Specs "Linear Epic" provides secondary validation
- Cross-reference to verify initiative-to-project mappings

### With GitHub Sync

- Extract Linear issue IDs from Eng Specs for PR correlation
- Design Brief Figma links inform prototype tracking

### With Portfolio Status

- Phase from Notion updates initiative lifecycle
- Artifact counts (specs, briefs) inform completeness scoring
- Launch dates inform timeline tracking

### Save Locations

| Output               | Location                              |
| -------------------- | ------------------------------------- |
| Initiative metadata  | `initiatives/active/*/_meta.json`     |
| Sync report          | `status/notion-sync-YYYY-MM-DD.md`    |
| Sync queue           | `sync-queue.md`                       |
| Signal from feedback | `signals/notion/YYYY-MM-DD-[name].md` |
