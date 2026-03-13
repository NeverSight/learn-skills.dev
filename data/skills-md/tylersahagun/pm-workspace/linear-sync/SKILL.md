---
name: linear-sync
description: Sync Linear projects, cycles, and issues to PM workspace initiatives. Use when running /sync-linear or /sync-dev commands, or when checking development progress.
---

# Linear Sync Skill

Procedural knowledge for synchronizing Linear project data with PM workspace initiatives.

## When to Use

- Running `/sync-linear` command
- Running `/sync-dev` for unified dev status
- Checking cycle progress for a team
- Mapping Linear issues to initiatives
- Generating dev activity reports

## Prerequisites

Requires Linear MCP tools. Two options available:

### Option 1: Dedicated Linear MCP

- `linear_getTeams` - List teams
- `linear_getProjects` - List projects
- `linear_getActiveCycle` - Get current cycle
- `linear_searchIssues` - Search issues by criteria
- `linear_getProjectIssues` - Get issues for a project

### Option 2: Composio MCP (composio-config)

**Server:** `composio-config`

The unified Composio MCP provides Linear tools with slightly different naming:

- `LINEAR_LIST_LINEAR_TEAMS` - List teams
- `LINEAR_LIST_LINEAR_PROJECTS` - List projects
- `LINEAR_LIST_LINEAR_CYCLES` - List cycles
- `LINEAR_SEARCH_ISSUES` - Search issues
- `LINEAR_GET_LINEAR_ISSUE` - Get issue details
- `LINEAR_CREATE_LINEAR_ISSUE` - Create new issues
- `LINEAR_UPDATE_ISSUE` - Update issues

**Note:** The `composio-config` server also provides Slack, Notion, HubSpot, and PostHog tools (700+ total).

## Data Sources

### Linear Data

- **Teams**: ASK (Development), VAN (Vanguard), CEX (Core Experience), EPD (Product)
- **Projects**: Linked to initiatives via `linear_project_id` in `_meta.json`
- **Cycles**: Two-week sprints with progress tracking
- **Issues**: Work items with state, assignee, priority

### Local Data

- `pm-workspace-docs/initiatives/active/*/_meta.json` - Initiative metadata with Linear links
- `pm-workspace-docs/signals/issues/` - Processed issue signals
- `pm-workspace-docs/status/dev-status-*.md` - Development status reports

## Initiative Mapping

### Smart Inference Strategy (No Labels Required)

**Reality check from 2026-01-23 audit:** Explicit labels and prefixes have 0% adoption. Use what exists:

1. **Notion "Linear Link"** - Projects DB has direct Linear project URLs
2. **Notion "Linear Epic"** - Engineering Specs DB has Linear epic/issue URLs
3. **Issue titles & descriptions** - Parse for initiative keywords
4. **Existing `_meta.json` mappings** - Use established `linear_project_id`
5. **Smart inference** - Match project names to initiatives

### \_meta.json Schema

```json
{
  "linear_project_id": "05066db9-89d7-432c-bffd-234ca92af024",
  "linear_project_url": "https://linear.app/askelephant/project/global-chat-05066db9",
  "notion_project_id": "abc123-def456",
  "dev_activity": {
    "last_synced": "2026-01-23T18:00:00Z",
    "linear_issues_total": 57,
    "linear_issues_completed": 23,
    "linear_issues_in_progress": 10,
    "github_prs_merged_30d": null
  }
}
```

### Mapping Priority (Smart Inference)

1. **Existing `linear_project_id` in `_meta.json`** (100% confidence)
   - Already mapped, use directly
2. **Notion Projects DB "Linear Link"** (90% confidence)
   - Cross-reference with `notion-sync` skill
   - Extract project ID from URL
3. **Notion Eng Specs "Linear Epic"** (80% confidence)
   - Secondary Linear connection
   - Look up issue → get project → map to initiative
4. **Project name → Initiative name match** (70% confidence)
   - "Global Chat" project → "internal-search" initiative (semantic match)
   - Use keyword overlap scoring
5. **Issue title keywords** (50% confidence)
   - Parse issue titles for initiative-related terms
   - Add to sync-queue.md for confirmation

### Confidence Scoring

| Signal                                   | Confidence      |
| ---------------------------------------- | --------------- |
| `linear_project_id` in `_meta.json`      | 100% (definite) |
| Notion "Linear Link" matches             | 90%             |
| Notion "Linear Epic" resolves to project | 80%             |
| Project name ≈ initiative name           | 70%             |
| Keyword overlap > 60%                    | 50%             |
| No match found                           | 0% → sync-queue |

**Thresholds:**

- ≥80%: Auto-map without confirmation
- 50-79%: Auto-map, note in sync report
- <50%: Add to `sync-queue.md` for user confirmation

### Known Project-Initiative Relationships

These are established mappings (verified in `_meta.json`):

| PM Initiative           | Linear Project      | Notes                                |
| ----------------------- | ------------------- | ------------------------------------ |
| internal-search         | Global Chat         | Name differs - semantic relationship |
| crm-exp-ete             | CRM Agent Upgrades  | Direct match                         |
| call-import-engine      | Call & Data Imports | Direct match                         |
| universal-signal-tables | Universal Signals   | Direct match                         |
| hubspot-agent-config-ui | HubSpot Integration | Direct match                         |

### Unmapped Work Handling

When Linear issues/projects can't be mapped:

1. **Check if Notion project exists** - May need `/sync-notion` first
2. **Suggest new initiative** - If active Linear project has no PM tracking
3. **Add to sync-queue.md** - For user decision

```markdown
## Unmapped Linear Project Detected

**Project:** "Mobile App v2" (ID: xyz789)
**Active Issues:** 15
**Last Activity:** 2 days ago

**No matching PM initiative found.**

Options:

- [Create "mobile-app-v2" initiative]
- [Map to existing initiative: ___]
- [Skip - not PM-tracked work]
```

## Sync Procedures

### Step 1: Load Initiative Metadata

```
1. Glob all initiatives: pm-workspace-docs/initiatives/active/*/_meta.json
2. Extract linear_project_id from each
3. Build mapping: { project_id: initiative_slug }
4. Identify unmapped initiatives for suggestions
```

### Step 2: Fetch Linear Data

**For Cycle Sync (`--cycle` flag):**

```
1. Call linear_getActiveCycle(teamId: "2b25052e-675d-4530-90c6-f2b6085d15e2")
2. Extract: cycle name, progress %, issue counts
3. Search issues in cycle with states: "In Progress", "In Review"
```

**For Project Sync (`--project [name]` flag):**

```
1. Find project by name or ID
2. Call linear_getProjectIssues(projectId)
3. Group by state: Todo, In Progress, Done
```

**For Team Sync (`--team [key]` flag):**

```
1. Get team ID from key (ASK, VAN, CEX, EPD)
2. Search all in-progress issues for team
3. Group by project → initiative
```

### Step 3: Update Initiative Metadata

For each mapped initiative:

```json
{
  "dev_activity": {
    "last_synced": "2026-01-23T18:00:00Z",
    "linear_issues_total": <count>,
    "linear_issues_completed": <done_count>,
    "linear_issues_in_progress": <active_count>,
    "github_prs_merged_30d": null
  }
}
```

### Step 4: Generate Status Output

**Cycle Progress Section:**

```markdown
## Cycle Progress

**Cycle 79** (Jan 13 - Jan 27)

- Progress: 28% (14/50 issues completed)
- In Progress: 10 issues
- In Review: 3 issues
```

**By Initiative Section:**

```markdown
## Work by Initiative

### Global Chat

**Linear Project:** [Global Chat](https://linear.app/...)

- Total Issues: 57
- Completed: 23 (40%)
- In Progress: 8

Active Work:

- [ ] ASK-4592: Global Chat first time experience (@Skylar)
- [ ] ASK-4477: New condensed chat input (@Skylar)
```

**Unlinked Work Section:**

```markdown
## Unlinked Work

Issues without initiative mapping:

- [ ] ASK-4583: BBL - Internal CLI POC (@Matt)
- [ ] ASK-4575: Engagement card re-design (@Adam)
```

## Issue Signal Generation

When processing issues for signals (`/ingest issue`):

### Signal Output Format

```markdown
# Issue: [Issue Key] - [Title]

**Date:** YYYY-MM-DD
**Source:** Linear
**Project:** [Project Name]
**Assignee:** [Name]
**State:** [State]

## Summary

[Issue description summary]

## Work Type

- [ ] Bug fix
- [ ] Feature
- [ ] Improvement
- [ ] Tech debt

## Initiative Link

**Mapped to:** [initiative-slug] (via project)

## Labels

[List of labels]

## Related Issues

[Parent, blockers, related]
```

### Save Location

`pm-workspace-docs/signals/issues/YYYY-MM-DD-[issue-key].md`

## Team Reference

| Team            | Key | ID                                   | Focus                 |
| --------------- | --- | ------------------------------------ | --------------------- |
| Development     | ASK | 2b25052e-675d-4530-90c6-f2b6085d15e2 | Core development      |
| Vanguard        | VAN | 51c213c2-9404-4fc8-846a-22c456fc2691 | Experimental features |
| Core Experience | CEX | ab724e37-e2b5-48a2-91dd-cfb11d648e09 | UX/UI polish          |
| Product         | EPD | ff631bc1-8b68-4900-937f-969fe4a3b532 | Product direction     |

## Output Formats

### Dev Status Report

Save to: `pm-workspace-docs/status/dev-status-YYYY-MM-DD.md`

```markdown
# Development Status Report

**Generated:** YYYY-MM-DD HH:MM
**Cycle:** Cycle 79 (28% complete)

## Summary

| Metric               | Value                |
| -------------------- | -------------------- |
| Active Issues        | X                    |
| Completed This Cycle | X                    |
| By Initiative        | X linked, Y unlinked |

## Cycle Progress

[cycle details]

## Work by Initiative

[per-initiative breakdown]

## Unlinked Work

[issues without mapping]

## Team Activity

[per-team breakdown if requested]
```

### JSON Output (`--json` flag)

```json
{
  "generated_at": "ISO8601",
  "cycle": {
    "name": "Cycle 79",
    "progress": 28,
    "total_issues": 50,
    "completed": 14
  },
  "by_initiative": [
    {
      "slug": "global-chat",
      "linear_project_id": "...",
      "issues_total": 57,
      "issues_completed": 23,
      "issues_in_progress": 8,
      "active_issues": [...]
    }
  ],
  "unlinked_issues": [...],
  "team_summary": {...}
}
```

## Error Handling

### No Linear Access

```
⚠️ Linear MCP tools not available.

Ensure Linear integration is configured in MCP settings.
```

### No Mapped Initiatives

```
ℹ️ No initiatives have linear_project_id configured.

Suggest mappings:
- universal-signal-tables → Universal Signals (978cd60b...)
- call-import-engine → Call & Data Imports (f4f924a8...)

Run `/sync-linear --map` to configure mappings.
```

### Project Not Found

```
⚠️ Linear project not found for initiative: [name]

The linear_project_id in _meta.json may be invalid.
Current ID: [id]

Run `/sync-linear --verify` to check all mappings.
```

## Integration Points

### After Sync

- Update `_meta.json` dev_activity for each initiative
- Update `signals/_index.json` if issues were ingested
- Generate dev status report

### With Notion Sync

- **Primary**: Use Notion "Linear Link" from Projects DB for mapping
- **Secondary**: Use Notion "Linear Epic" from Eng Specs for validation
- Cross-reference: If Linear project found but no Notion link, suggest adding in Notion
- Notion phase → Initiative phase updates

### With Portfolio Status

- `portfolio-status` skill reads dev_activity from `_meta.json`
- Include dev progress in artifact matrix
- Surface initiatives with high activity but stale docs

### With GitHub Sync

- Combined in `/sync-dev` command
- Correlate Linear issues with PR references (via ASK-XXXX in branch names)
- Build complete work-to-ship pipeline view

### With Sync Queue

- Ambiguous mappings → add to `sync-queue.md`
- User confirms/rejects → update `_meta.json`
- New Linear projects → suggest initiative creation

---

## Bidirectional Sync (Enhanced)

### Sync Commands

| Command                 | Direction     | Description                                    |
| ----------------------- | ------------- | ---------------------------------------------- |
| `/sync-linear`          | Linear → PM   | Pull Linear data into PM workspace             |
| `/sync-linear --push`   | PM → Linear   | Push initiative data to Linear (create/update) |
| `/sync-linear --full`   | Bidirectional | Full sync both directions                      |
| `/sync-linear --labels` | PM → Linear   | Create/update workflow labels                  |

### Push to Linear (`--push`)

Creates or updates Linear projects from PM workspace initiatives:

1. Read all `_meta.json` files with `priority` P0 or P1
2. For each initiative without `linear_project_id`:
   - Create Linear project with same name
   - Set description from PRD summary
   - Create "Release Criteria" issue from template
3. For each initiative with `linear_project_id`:
   - Update project status/priority if changed
   - Sync blockers to Linear issues

### Workflow Labels

The following labels exist in Linear Development team:

| Label                      | ID                                     | Purpose                            |
| -------------------------- | -------------------------------------- | ---------------------------------- |
| `workflow/needs-prd`       | `1bb0f920-3bc3-4f44-97a6-c010fabe7083` | PM work required                   |
| `workflow/needs-design`    | `905ec3cd-e8c4-49e5-9e13-9fcb6c9f3d6a` | Design work required               |
| `workflow/needs-eng-spec`  | `42efd000-50b9-4e5d-883e-b70193dc9c23` | Engineering spec required          |
| `workflow/needs-decisions` | `2f77b3aa-333c-4388-b77b-af18f0737d31` | Open questions blocking progress   |
| `workflow/ready-to-build`  | `81299a18-f7cd-454c-91f6-e6c2651b56b6` | All inputs ready, passes Ivan Test |
| `workflow/in-review`       | `9cb83f70-f260-4451-ae6a-e127d6f7b34d` | Stakeholder review needed          |
| `workflow/blocked`         | `615742cf-d765-4359-a090-cab7e3dda246` | External blocker                   |

### MCP Tools for Sync

| Tool                           | Purpose                        |
| ------------------------------ | ------------------------------ |
| `LINEAR_CREATE_LINEAR_PROJECT` | Create new project             |
| `LINEAR_UPDATE_LINEAR_PROJECT` | Update project status/priority |
| `LINEAR_CREATE_LINEAR_ISSUE`   | Create release criteria issue  |
| `LINEAR_UPDATE_ISSUE`          | Update issue labels/status     |

### With Team Dashboard

- `/sync-linear` updates data for `/team` command
- Share mappings and project IDs
- Avoid duplicate MCP calls
