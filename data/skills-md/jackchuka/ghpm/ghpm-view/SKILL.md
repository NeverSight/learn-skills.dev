---
name: ghpm-view
description: "Query GitHub Project items by named view or ad-hoc filter. Shows items in board, table, or roadmap format."
argument-hint: "<view-name | filter> [--refresh]"
allowed-tools: Bash(gh:*), Read, Grep
---

# ghpm-view

> **PREREQUISITE:** Read `../ghpm-shared/SKILL.md` for prerequisites and error handling.

Drill into a specific named view or run an ad-hoc filter against project items.

## Arguments

- `/ghpm-view` — with no args, list available views (same as the Views section of `/ghpm-status`)
- `/ghpm-view <view name>` — fuzzy match against view names in config
- `/ghpm-view <free-form filter>` — natural language filter against field values
- `/ghpm-view --refresh` — force re-fetch cache before querying

## Workflow

### Phase 1: Load Config and Cache

Follow the startup sequence in `../ghpm-shared/SKILL.md` and load cache per `../ghpm-shared/references/cache.md`. If `--refresh` flag is present, skip cache and re-fetch.

### Phase 2: Resolve Query

4. If no arguments: list available views with item counts and stop.

5. If arguments provided, try to match against view names first:
   - Normalize input (lowercase, strip punctuation).
   - Compare against view names from config (also normalized).
   - Use substring matching: "standup" matches "daily standup", "triage" matches "Task Triage", "appshell" matches "AppShell".
   - If exactly one view matches: use that view's filter and layout.
   - If multiple views match: show matches and ask user to pick.

6. If no view matches, treat input as ad-hoc filter:
   - Match user's words against known field option names from `.ghpm/config.json`.
   - Match `@username` against assignee fields.
   - Match workflow column names (e.g., "in progress" -> InProgress).
   - Build a filter from matched fields.

### Phase 3: Apply Filter

7. Filter cached items based on the resolved query. Apply filter syntax per `../ghpm-shared/references/filter.md`.

8. Apply sort if the view has sort fields: sort items by the specified fields and directions.

### Phase 4: Format Output

9. Format based on layout type, following conventions in `../ghpm-shared/references/format.md`:

**Board layout** — group items by workflow column as vertical lists:

```
<View Name> (board) — <count> items

## <Col1> (N)
- #<num> <Title>
- #<num> <Title>

## <Col2> (N)
- #<num> <Title>
- #<num> <Title>
```

- Show item count per column in the heading.
- Only show non-empty columns.
- Include assignee if available: `- #<num> <Title> (@user)`.

**Table layout** — show as markdown table:

```
<View Name> (table) — <count> items

| # | Title | Assignee | <relevant fields...> | Status |
|---|-------|----------|----------------------|--------|
| 1 | ...   | ...      | ...                  | ...    |
```

- Include columns for: Title, Assignee, Status, and any fields referenced in the view's filter.
- If the view has no specific filter fields, show: Title, Assignee, Component (if exists), Status.

**Roadmap layout** — show as grouped table by iteration/quarter:

```
<View Name> (roadmap) — <count> items

## <Quarter/Iteration 1>
| Title | Status | Component | Assignee |
|-------|--------|-----------|----------|
| ...   | ...    | ...       | ...      |

## <Quarter/Iteration 2>
...
```

- Group by the sort field (typically Quarter or iteration).

**Ad-hoc filter** — always use table layout. Include a summary header showing total project items matched and what the filter resolved to:

```
Ad-hoc filter: <resolved filter> — <count> items (of <total> in project)

| # | Title | Assignee | Component | Status |
|---|-------|----------|-----------|--------|
| 1 | ...   | ...      | ...       | ...    |
```

If zero items match, explain why (e.g., the user doesn't exist, or no items match the status) and include helpful context: the total number of items in the project with that status, and a list of valid values for the field that didn't match. Suggest an alternative query using `/ghpm-view`.

10. If more than 30 items **total** (across all columns/groups), show only the first 30 items total and note: "Showing 30 of <total>. Narrow your filter to see more." For board layout, this means distributing the 30-item budget across columns proportionally — don't show all items in every column. For example, with 119 items across 4 columns, you might show ~8 per column rather than listing all 42 Planned items.

## Tips

- Read-only — never modifies the project or its items.

## See Also

- [ghpm-shared](../ghpm-shared/SKILL.md) — Prerequisites and error handling
- [ghpm-status](../ghpm-status/SKILL.md) — Project health dashboard
- [ghpm-suggest](../ghpm-suggest/SKILL.md) — Get work recommendations
