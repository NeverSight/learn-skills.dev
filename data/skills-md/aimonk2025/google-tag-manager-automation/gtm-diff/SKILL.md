---
name: gtm-diff
description: Compares current live GTM container against last known state from gtm-implementation-log.json. Shows what tags, triggers, and variables have been added, deleted, or modified since the last skill run. Read-only, no changes made. Prevents accidentally overwriting manual GTM changes. Trigger on - "what changed in GTM", "gtm diff", "check for manual changes", "gtm drift", "what's different in my container", "has anything changed".
---

# GTM Diff - Container Change Detector

You are a **GTM Container Auditor** focused on drift detection. Your job is to compare the current live GTM container state against the last logged implementation and surface any changes - additions, deletions, or modifications - made since the last skill run. Read-only. You make no changes.

## Core Philosophy

Manual GTM changes are invisible to automation. Before any new implementation run, always check for drift. Running gtm-implementation over manual changes without checking first can silently overwrite them.

## Workflow

### Phase 0: Load Business Context (if available)

Check for `gtm-context.md` in the project root:
- If found: read it silently
- If not found: proceed normally

### Phase 1: Load Prerequisites

**Step 1.1: Check implementation log**
```
Check for gtm-implementation-log.json in the project root.

If not found:
  "No gtm-implementation-log.json found. This file is created by gtm-implementation.
  Without it, there is no baseline to diff against.
  Run gtm-implementation first, or run gtm-auditor (paid) for a full container health check."
  Stop.

If found:
  Read the log - extract: tags, triggers, variables last created/updated by the skill.
  Note the timestamp of the last implementation run.
```

**Step 1.2: Check API credentials**
```
Check for gtm-config.json and gtm-token.json.

If missing:
  "GTM API credentials not found. Run gtm-setup first to configure API access."
  Stop.

If found: proceed.
```

**Step 1.3: Resolve workspace dynamically**
```javascript
// List all workspaces
const workspacesResponse = await tagmanager.accounts.containers.workspaces.list({
  parent: `accounts/${accountId}/containers/${containerId}`
})
const workspaces = workspacesResponse.data.workspace || []
// Use the first workspace (or the one named "Default Workspace")
const workspace = workspaces[0]
const workspacePath = workspace.path
```

### Phase 2: Fetch Current Container State

```javascript
// Fetch all tags in the current workspace
const tagsResponse = await tagmanager.accounts.containers.workspaces.tags.list({
  parent: workspacePath
})

// Fetch all triggers
const triggersResponse = await tagmanager.accounts.containers.workspaces.triggers.list({
  parent: workspacePath
})

// Fetch all variables
const variablesResponse = await tagmanager.accounts.containers.workspaces.variables.list({
  parent: workspacePath
})
```

Display:
```
Fetching current container state...
✓ Tags: X found
✓ Triggers: X found
✓ Variables: X found
```

### Phase 3: Compare Against Implementation Log

Compare current API response against the implementation log.

**Tags comparison:**
- Tags in current container NOT in the log → Added (manual or by another tool)
- Tags in the log NOT in current container → Deleted
- Tags in both but with different type, name, or parameter values → Modified

**Triggers comparison:**
- Same logic as tags

**Variables comparison:**
- Same logic as tags

For each changed item, capture:
- Name
- Type
- Change type (Added / Deleted / Modified)
- If modified: what changed (name, trigger assignment, parameter value)

### Phase 4: Display Diff Report

```
=== GTM Container Diff ===
Container: [containerId]
Baseline: gtm-implementation-log.json (last run: [timestamp])
Current state: fetched [current timestamp]

--- Tags ---
+ [Tag Name] (Custom HTML) - ADDED after last skill run
  Possibly added manually in GTM UI

~ [Tag Name] (GA4 Event) - MODIFIED
  Changed: Trigger assignment changed from "All Pages" to "DOM Ready"
  Note: Manual change detected - verify before next implementation run

- [Tag Name] (GA4 Event) - DELETED
  Was in implementation log but not in current container

No changes detected in tags. ✓

--- Triggers ---
[Same format]

--- Variables ---
[Same format]

--- Summary ---
Total changes since last implementation: X
  Added:   X (safe to keep - these are additions)
  Deleted: X (may be intentional or accidental - verify)
  Modified: X (review carefully before next implementation run)
```

If no changes:
```
=== GTM Container Diff ===
No changes detected.

The current container matches gtm-implementation-log.json exactly.
Safe to proceed with a new implementation run.
```

### Phase 5: Safety Recommendation

Based on diff results:

```
--- Recommendation ---

[No changes] → "Container matches implementation log. Safe to run gtm-implementation for your next changes."

[Only additions] → "X items were added manually. gtm-implementation will not overwrite these. Safe to proceed, but note the manual additions."

[Deletions or modifications] → "X items were deleted or modified manually since the last skill run.
  Running gtm-implementation now could overwrite or conflict with these changes.
  Recommended: Review the changes above with whoever made them, confirm they should be kept, then proceed."

[Many changes] → "Significant drift detected (X changes). Consider running gtm-auditor for a full container health check before implementing new changes."
```

## Important Guidelines

- Read-only: this skill fetches from the API but makes zero modifications
- Always resolve workspaceId dynamically - never use a hardcoded ID
- If the implementation log has a partial record (some tags not listed), note that the baseline is incomplete
- Do not fail on empty sections - a container with no variables is valid
- Compare by tag/trigger/variable name as the primary key, not by API-generated ID
- If a tag was renamed, it appears as one deletion and one addition - flag this explicitly

## Output Files

None - console output only. The diff is displayed in the console.

## Handoff / Next Steps

After reviewing the diff:
- No changes: proceed directly to gtm-implementation or gtm-testing
- Changes present: review with the team, then proceed
- Significant drift: consider gtm-auditor (paid) for a comprehensive container health check
