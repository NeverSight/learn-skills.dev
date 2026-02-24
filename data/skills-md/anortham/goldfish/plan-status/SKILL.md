---
name: plan-status
description: Assess progress against the active Goldfish plan using checkpoints and plan data
allowed-tools: mcp__goldfish__recall, mcp__goldfish__plan
---

# Plan Status — Progress Assessment

## What This Does

Pulls plans from multiple sources and recent checkpoints, then assesses how actual work aligns with planned goals. Reports what's done, what's next, and whether the project is drifting from the plan.

## How to Assess Plan Status

### Step 1: Gather plans from ALL sources

**Source 1: Goldfish plans**
```
mcp__goldfish__recall({ limit: 0 })
```

This returns the active Goldfish plan for the current workspace.

If you need a specific plan by ID (not just the active one):

```
mcp__goldfish__plan({ action: "get", id: "plan-id" })
```

If no active plan exists, note it but continue — there may still be plans in `docs/plans/`.

**Source 2: Project plan docs**

Scan `docs/plans/*.md` in the current project directory. Read each file and check:
- The `**Status:**` field in the header (typically "Approved", "Complete", "In Progress")
- The date in the filename (format: `YYYY-MM-DD-<name>.md`)
- Skip files with Status "Complete" unless they were completed very recently (last 3 days)

### Step 2: Recall recent checkpoints

```
mcp__goldfish__recall({ days: 7, limit: 20, full: true })
```

Use `full: true` to get file lists and git metadata — this helps match checkpoints to plan items. Use a wider window (7 days) to capture the full arc of plan execution.

If the plans are older, extend the range:
```
mcp__goldfish__recall({ days: 14, limit: 30, full: true })
```

### Step 3: Cross-reference and assess

Map each checkpoint to a plan goal. Identify:
- Which plan items have checkpoint evidence of completion
- Which plan items have WIP checkpoints but aren't done
- Which plan items have zero checkpoint activity
- Which checkpoints don't map to any plan item (scope drift)

**For docs/plans files:** Do NOT blindly trust the Status header. Verify against checkpoints:
- Status "Approved" + all tasks have checkpoint evidence → effectively complete
- Status "Approved" + partial checkpoint coverage → in progress
- Status "Approved" + no checkpoints → not started

**For Goldfish plans:** Use the plan's status field directly.

## Report Format

Start with a header that identifies the plan and assessment date, then structure as four sections followed by an overall health assessment.

### Header

```
## Plan Status — "Auth System Overhaul" — Feb 14, 2026
Source: Goldfish active plan
3/5 items complete (60%)
```

When reporting on docs/plans:
```
## Plan Status — "v5.1 Skills Refresh" — Feb 14, 2026
Source: docs/plans/2026-02-16-v5.1-implementation.md
2/8 tasks complete (25%)
```

Always include the source location and completion fraction for instant comprehension.

### Completed
Plan items with clear checkpoint evidence of completion. Include the approximate date completed and any notable details.

- [x] JWT refresh token rotation — completed Feb 12, shipped with full test coverage
- [x] Rate limiter Redis support — completed Feb 13, integration tests passing

### In Progress
Plan items with recent checkpoints showing active work but not yet complete.

- [ ] Session management API — 3 checkpoints this week, endpoints implemented but missing error handling
- [ ] Admin dashboard auth — started Feb 13, basic scaffold in place

### Not Started
Plan items with no checkpoint activity at all. Flag these — they might be blocked, deprioritized, or forgotten.

- [ ] API documentation — no activity found
- [ ] Load testing — no activity found (may be blocked by staging environment)

### Drift Assessment
Work captured in checkpoints that doesn't map to any plan item. This isn't automatically bad — emergent work happens — but it should be called out.

**Unplanned work detected:**
- Bug fix: file corruption on concurrent writes (2 checkpoints, Feb 11)
- Dependency upgrade: fuse.js v7 migration (1 checkpoint, Feb 12)

These consumed ~1 day of effort outside the plan scope.

### Overall: Minor Drift

Render the health assessment as a `### Overall:` header with the verdict, followed by a direct, honest summary.

Health levels:
- **On track** — Most plan items progressing, minimal drift, no blockers
- **Minor drift** — Some unplanned work but plan items still advancing
- **Significant drift** — More unplanned work than planned work, or key items stalled
- **Stalled** — Little to no progress on plan items, or major blockers

Be direct. "The plan called for 5 deliverables this sprint. Two are done, one is in progress, and two haven't been touched. You're behind, and the unplanned auth bug ate a day." That's more useful than "progress is being made."

## Multiple Plans

When both a Goldfish active plan AND docs/plans files exist, report on each separately with clear source attribution. Present the Goldfish plan first (it's the "active" strategic direction), then docs/plans (implementation plans).

If plans overlap or conflict, flag it: "The Goldfish active plan focuses on auth, but docs/plans shows active work on a performance benchmark suite. These may be competing priorities."

## Critical Rules

- **Do NOT sugarcoat.** If the plan is behind, say so. The user needs accurate information, not comfort.
- **Do NOT fabricate progress.** Only claim completion for items with actual checkpoint evidence.
- **DO flag scope drift.** Unplanned work is a leading indicator of timeline slip.
- **DO suggest plan updates.** If a plan is clearly outdated, recommend updating it — via `mcp__goldfish__plan({ action: "update" })` for Goldfish plans, or by editing the file directly for docs/plans.
- **Match checkpoints to plan items carefully.** A checkpoint about "auth" doesn't automatically satisfy a plan item about "auth" — read the descriptions and match on actual content.
- **Include time estimates when possible.** "3 checkpoints over 2 days" gives the user a sense of effort invested.
- **Check BOTH plan sources.** Missing a source means an incomplete assessment.
- **Attribute sources clearly.** The user should always know whether a plan came from `.memories/plans/` or `docs/plans/`.
