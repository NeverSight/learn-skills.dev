---
name: wt-status
version: 2.0.0
description: Show comprehensive status of git worktrees and database-tracked story associations, including orphaned and untracked detection.
---

# /wt:status - Show Worktree Status

## Description

Show comprehensive status of the current worktree and all worktrees, including both git-level worktree state and database-tracked story worktrees (active, orphaned, and untracked detection).

## Usage

```
/wt:status
```

## What It Does

This slash command:
1. Shows git-level worktree status (current location, uncommitted changes, sync status)
2. Queries `worktree_list_active` MCP tool for database-tracked story worktrees
3. Cross-references DB records against git worktrees to detect orphaned and untracked entries
4. Renders a unified view of both sources

## Section 1: Git Worktrees

### Information Displayed

- **Current worktree location** — Where you are now
- **All worktrees and their states** — Overview of all worktrees
- **Uncommitted changes** — Files modified, staged, untracked
- **Branches ahead/behind origin** — Sync status with remote

### How to Collect

Use Bash tool to run git status commands:

```bash
git worktree list
git status
git log --oneline -5
```

## Section 2: Story Associations

### How to Collect

Call the `worktree_list_active` MCP tool:

```
worktree_list_active({})
```

### Null-Check Resilience

The `worktree_list_active` call must handle null/error responses gracefully:

```
result = worktree_list_active({})

if result is null or tool call throws an error:
  Print: "Story Associations unavailable (MCP error). Git worktree list above is still accurate."
  Return (show git section only, do NOT fail the whole command)

if result is [] (empty array):
  Print: "No active story associations found."

if result is [records...]:
  → perform path cross-reference (see below)
  → render tabular output
```

### Path Normalization

Before comparing DB `worktreePath` values against git worktree paths:
- Resolve trailing slashes (remove them)
- Compare absolute paths (resolve relative paths against repo root)

### Cross-Reference Mechanism

After collecting both DB records and git worktree paths:

1. Collect the set of normalized `worktreePath` values from all DB records (`db_paths`)
2. Collect the set of normalized git worktree paths from `git worktree list` (`git_paths`)
3. For each DB record: check if `worktreePath` exists in `git_paths`
   - If NOT in `git_paths`: the path no longer exists on disk — flag as `(orphaned)`
4. For each git worktree path that is NOT in `db_paths`:
   - Flag that git worktree as `(untracked)` in the story_id column

An `(untracked)` label means: a git worktree exists on disk but has no corresponding active DB record (potential orphan from pre-WINT-1130 sessions or `--skip-worktree` runs).

### Output Format

Section header (visually separated from git section):

```
--- Story Associations ---
```

Tabular output (consistent column widths, no emoji):

```
story_id      branch_name               worktree_path                 age
WINT-1140     story/WINT-1140           tree/story/WINT-1140          3d 2h
WINT-1130     story/WINT-1130           tree/story/WINT-1130          5d 10h (orphaned)
(untracked)   story/WINT-1050           tree/story/WINT-1050          —
```

The `age` column is calculated from the `createdAt` timestamp relative to now. Display as `Nd Nh` (days and hours).

Empty state:

```
--- Story Associations ---
No active story associations found.
```

Degraded state (MCP tool error):

```
Story Associations unavailable (MCP error). Git worktree list above is still accurate.
```

### Graceful Degradation Summary

| Condition | Behavior |
|-----------|----------|
| `worktree_list_active` returns `[]` | Show "No active story associations found." |
| `worktree_list_active` returns error/null | Show "Story Associations unavailable (MCP error). Git worktree list above is still accurate." Do NOT fail the whole command. |
| `git worktree list` returns empty | Show only DB records (no cross-reference possible) |

## Full Execution Flow

```
1. Run git worktree commands → collect git_paths and worktree status
2. Display git section
3. Call worktree_list_active({})
   a. If null/error → show degradation warning, stop
   b. If [] → print "No active story associations found."
   c. If [records...]:
      - Normalize all paths (trailing slashes, absolute)
      - Cross-reference: match DB worktreePath against git_paths
      - Flag DB records with no git match as (orphaned)
      - Flag git worktrees with no DB match as (untracked)
      - Render tabular Story Associations section
```

## Benefits

- **Complete Overview** — See everything at a glance (git + DB)
- **Sync Awareness** — Know what needs pushing/pulling
- **Change Tracking** — See all uncommitted work
- **Multi-Worktree View** — Status of all git worktrees
- **Conflict Detection** — Identify stories with active DB-tracked worktrees to prevent parallel work collisions
- **Orphaned Record Detection** — Flag DB records where path no longer exists on disk
- **Untracked Git Worktree Detection** — Flag git worktrees with no DB record (possible abandoned sessions)

## Schema References

The `worktree_list_active` result follows `WorktreeListActiveOutputSchema` — an array of `WorktreeRecord`:

```typescript
WorktreeRecord {
  id: string (UUID)           // worktree database ID — use for worktree_mark_complete
  storyId: string             // human-readable story ID (e.g., "WINT-1130")
  worktreePath: string        // filesystem path (e.g., "tree/story/WINT-1130")
  branchName: string          // git branch (e.g., "story/WINT-1130")
  status: "active"            // always "active" from worktree_list_active
  createdAt: Date             // registration timestamp
  updatedAt: Date
  mergedAt: Date | null
  abandonedAt: Date | null
  metadata: Record<unknown>
}
```

## Related Skills

- `/wt:new` — Create a new story worktree
- `/wt:switch` — Switch to an existing worktree
- `/wt:finish` — Complete and clean up a worktree
