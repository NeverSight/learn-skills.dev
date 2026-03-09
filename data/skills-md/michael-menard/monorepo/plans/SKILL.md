---
name: plans
description: List all plans from the KB database with key metadata. Use to get a quick overview of plan statuses, priorities, and story counts.
---

# /plans - List All Plans

## Usage

```
/plans                    # All non-archived plans (excludes implemented + superseded)
/plans all                # All plans regardless of status
/plans --status=draft     # Filter by status
/plans --type=migration   # Filter by plan type
```

## Execution

### Step 1 — Parse Arguments

Parse the user's input for optional filters:

| Argument | Maps To | Values |
|----------|---------|--------|
| `all` | no filter | show everything |
| `--status=X` | `status` filter | draft, accepted, stories-created, in-progress, implemented, superseded, archived |
| `--type=X` | `plan_type` filter | feature, refactor, migration, infra, tooling, workflow, audit, spike |
| `--prefix=X` | `story_prefix` filter | e.g., APIP, SKCR, DASH |
| *(no args)* | default | exclude `implemented` and `superseded` |

### Step 2 — Query KB

Call `kb_list_plans` with the appropriate filters and `limit: 100`.

If the default filter (no args), make TWO calls and combine:
1. `kb_list_plans({ status: 'draft', limit: 100 })`
2. `kb_list_plans({ status: 'in-progress', limit: 100 })`
3. Also include `stories-created` and `accepted` if any exist

**Simpler approach:** Call `kb_list_plans({ limit: 100 })` once, then filter client-side to exclude `implemented` and `superseded` when no explicit filter is given.

### Step 3 — Format Output

Display results as a markdown table with these columns:

```
| Plan Slug | Title | Status | Type | Prefix | Priority | Stories | Tags | Updated |
```

**Column formatting:**
- **Plan Slug**: backtick-wrapped slug
- **Title**: truncate to 50 chars if needed
- **Status**: as-is
- **Type**: as-is
- **Prefix**: story_prefix or `—`
- **Priority**: P1-P5
- **Stories**: estimated_stories or `—`
- **Tags**: first 3 tags comma-separated, `+N` if more
- **Updated**: relative date (e.g., "2h ago", "3d ago")

Sort order: status (draft/in-progress first), then priority (P1 first), then slug.

### Step 4 — Summary Line

After the table, output a one-line summary:

```
N plans total: X draft, Y in-progress, Z implemented, W superseded
```
