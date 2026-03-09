---
name: roadmap
description: Show the active roadmap — current and future plans only (excludes implemented, superseded, archived). Quick view of what's in flight and coming next.
---

# /roadmap - Active Roadmap View

## Usage

```
/roadmap                   # All active plans sorted by priority
/roadmap --type=feature    # Filter by plan type
/roadmap --priority=P1     # Show only P1 items
/roadmap --prefix=APIP     # Filter by story prefix
```

Multiple filters can be combined: `/roadmap --priority=P1 --type=infra`

## Execution

### Step 1 — Parse Arguments

Parse the user's input for optional filters:

| Argument | Maps To | Values |
|----------|---------|--------|
| `--type=X` | `plan_type` filter | feature, refactor, migration, infra, tooling, workflow, audit, spike |
| `--priority=X` | `priority` filter | P1, P2, P3, P4, P5 |
| `--prefix=X` | `story_prefix` filter | e.g., APIP, SKCR, DASH |
| *(no args)* | no extra filters | all active plans |

### Step 2 — Query KB

Call `kb_list_plans` for each active status: `in-progress`, `stories-created`, `draft`. Make the three calls **in parallel**.

Pass any parsed filters (`plan_type`, `priority`, `story_prefix`) to each call. Use `limit: 50` for each.

Merge all results into a single list and sort by:
1. Priority (P1 first)
2. Status order: in-progress > stories-created > draft
3. Plan slug alphabetically

### Step 3 — Format Output

Display results as a markdown table:

```
| Priority | Type | Status | Plan Slug | Description | Prefix | Stories | Updated |
```

**Column formatting:**
- **Priority**: P1-P5
- **Type**: planType value (feature, infra, workflow, etc.)
- **Status**: as-is
- **Plan Slug**: backtick-wrapped slug
- **Description**: use `summary` field from KB response, truncate to 80 chars if needed (append "...")
- **Prefix**: story_prefix or `--`
- **Stories**: If the plan has stories (status is `stories-created` or `in-progress`), call `kb_list_stories` with the plan's `story_prefix` to get total and completed counts, then display as `completed/total` (e.g., `3/20`). Count a story as "completed" if its status is `UAT`, `done`, or `implemented`. If no stories exist yet, show `estimated_stories` or `--`.
- **Updated**: relative date (e.g., "2h ago", "3d ago")

### Step 4 — Summary Line

After the table, output a one-line summary:

```
Roadmap: N active plans — X draft, Y accepted, Z stories-created, W in-progress
```

Count each status from the returned results.
