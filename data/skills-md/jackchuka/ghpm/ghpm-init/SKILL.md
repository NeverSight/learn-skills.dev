---
name: ghpm-init
description: "Initialize GitHub Project Management config. Auto-discovers project schema (fields, views, repos) and generates .ghpm/config.json + .ghpm/cache.json."
argument-hint: "<project-url>"
allowed-tools: Bash(gh:*), Bash(mkdir:*), Read, Write, Grep
---

# ghpm-init

> **PREREQUISITE:** Read `../ghpm-shared/SKILL.md` for prerequisites and error handling.

Initialize a GitHub Projects v2 project for use with ghpm skills. Auto-discovers schema and generates config files.

## Arguments

- Project URL (e.g., `https://github.com/orgs/<org>/projects/<number>`)
- If no arguments, ask the user for the project URL or owner + number.

## Workflow

### Phase 1: Validate Access

1. Parse arguments to extract owner and project number from URL or positional args.
2. Run `gh auth status` to verify authentication. If this fails, tell the user to run `gh auth login` and stop.
3. Run `gh project view <number> --owner <owner> --format json` to verify access and get project metadata (id, title). If this fails with 403/404, tell the user to check token scopes (`read:project`, `project`) and project access.
4. Determine the owner type from the project view output. This matters for Phase 3: use `organization(login: "<owner>")` for org-owned projects or `user(login: "<owner>")` for user-owned projects.

### Phase 2: Discover Schema

5. Run `gh project field-list <number> --owner <owner> --format json` to get all fields with IDs, types, and options.
6. Identify the workflow field: find the `ProjectV2SingleSelectField` named "Status". If multiple candidates or none found, ask the user which field drives the kanban workflow.
7. Separate the workflow field from other fields.

### Phase 3: Discover Views

8. Run GraphQL query to fetch all views. Use the owner type determined in Phase 1 to choose the correct root field:

```bash
gh api graphql -f query='
{
  organization(login: "<owner>") {
    projectV2(number: <number>) {
      views(first: 50) {
        nodes {
          id
          name
          number
          layout
          filter
          groupByFields(first: 5) {
            nodes {
              ... on ProjectV2Field { name }
              ... on ProjectV2SingleSelectField { name }
              ... on ProjectV2IterationField { name }
            }
          }
          sortByFields(first: 5) {
            nodes {
              field {
                ... on ProjectV2Field { name }
                ... on ProjectV2SingleSelectField { name }
                ... on ProjectV2IterationField { name }
              }
              direction
            }
          }
        }
      }
    }
  }
}'
```

9. Transform view data into config format: lowercase layout names (TABLE_LAYOUT -> table, BOARD_LAYOUT -> board, ROADMAP_LAYOUT -> roadmap), preserve filter strings as-is.

### Phase 4: Discover Items and Repos

10. Run `gh project item-list <number> --owner <owner> --format json --limit 1000` to fetch all items. The `--limit` flag controls the total count returned (no cursor pagination available), so use a high value. **Note:** items beyond the limit are silently truncated — see cache reference for details.
11. Extract unique repository URLs from items to build the repos list.
12. Store all items in cache.

### Phase 5: Write Config Files

13. Assemble `.ghpm/config.json` with this structure:

```json
{
  "version": 1,
  "project": {
    "owner": "<owner>",
    "number": "<number>",
    "id": "<project_node_id>",
    "title": "<project_title>"
  },
  "workflow": {
    "field": "<status_field_name>",
    "field_id": "<status_field_id>",
    "columns": [{ "id": "<option_id>", "name": "<option_name>" }]
  },
  "fields": [
    {
      "name": "<field_name>",
      "id": "<field_id>",
      "type": "<field_type>",
      "options": [{ "id": "<option_id>", "name": "<option_name>" }]
    }
  ],
  "views": [
    {
      "name": "<view_name>",
      "number": "<view_number>",
      "id": "<view_id>",
      "layout": "<table|board|roadmap>",
      "filter": "<filter_string>",
      "sort": [{ "field": "<field_name>", "direction": "<ASC|DESC>" }],
      "group_by": ["<field_name>"]
    }
  ],
  "cache": {
    "ttl_minutes": 30
  },
  "conventions": {
    "branch": "{type}/{issue-number}/{slug}. Detect type from issue labels and title: bug→fix, enhancement/feature→feat, documentation→docs, test→test, refactor→refactor, default→chore",
    "status_sync": "On start, set to InProgress if currently Planned or ReadyForDev. On session end with merged PR, set to Done.",
    "decisions": "When a design decision is detected, nudge before recording. Post as issue comment."
  },
  "repos": ["<owner>/<repo>"]
}
```

- Only include `sort` key on views that have sort fields.
- Only include `group_by` key on views that have groupBy fields.
- Only include `options` on fields that are `single_select` or `iteration` type.
- Strip the full URL from repos, keep just `owner/repo`.

14. Write `.ghpm/cache.json` per `../ghpm-shared/references/cache.md`.

15. Run `mkdir -p .ghpm/sessions`. Check if `.gitignore` exists. If it does, check if `.ghpm/` is already listed. If not, ensure the file ends with a newline before appending `.ghpm/` on its own line. If `.gitignore` doesn't exist, create it with `.ghpm/\n`.

### Phase 6: Install Agent Integration (optional)

16. Detect the current agent environment and offer to install hooks/rules for enhanced `ghpm-work` sessions. See `../ghpm-shared/references/integrations.md` for available integrations.

    **Claude Code detection**: Check if `.claude/` directory exists or if the current process is running inside Claude Code.

    If detected, ask the user:
    ```
    Detected Claude Code. Install session hooks for ghpm-work? (y/n)
    Hooks add: auto session context injection, stale session detection.
    Without hooks, ghpm-work still works via explicit commands.
    ```

    If confirmed:
    - Add the hooks from `../ghpm-shared/references/integrations.md` into `.claude/settings.local.json` under the `"hooks"` key.
    - If `.claude/settings.local.json` already exists, merge the `"hooks"` key into the existing structure (preserve existing settings and hooks, add new ones).

    If declined or agent not detected, skip.

### Phase 7: Report

17. Print summary:

```
ghpm initialized for <title> (<owner>/projects/<number>)

  Fields:    <count> (<list of field names>)
  Views:     <count> (<list of view names>)
  Repos:     <count>
  Items:     <count> cached

Config:  .ghpm/config.json (gitignored)
Cache:   .ghpm/cache.json (gitignored)
Hooks:   <installed|skipped>

Run /ghpm-status for project overview.
```

## See Also

- [ghpm-shared](../ghpm-shared/SKILL.md) — Prerequisites and error handling
- [ghpm-status](../ghpm-status/SKILL.md) — Project health dashboard
