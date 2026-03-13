---
name: toggl-cli
description: >
  Manage Toggl Track time entries, projects, tags, clients, tasks, workspaces, and organizations via the `toggl` CLI.
  Features HTTP response caching for improved performance and reduced API calls.
  Use for time-tracking requests like start/stop/continue/list/edit/delete, profile/preferences, and resource management,
  even when the user does not explicitly mention Toggl.
---

# Toggl CLI Skill

- Install: `npm install -g @correctroadh/toggl-cli`
- Auth: `toggl auth <TOKEN>`

## Command Shapes

Time entries:
- `toggl start [description] [-p PROJECT] [--task TASK] [-t TAG...] [-b] [--start DATETIME] [--end DATETIME]`
- `toggl stop`
- `toggl continue [-i]`
- `toggl running` or `toggl current`
- `toggl show <id> [-j]`
- `toggl edit time-entry [id] [-d DESCRIPTION] [--billable true|false] [-p PROJECT] [--task TASK] [-t TAG...] [--start DATETIME] [--end DATETIME|""]`
- `toggl delete <time_entry_id>`
- `toggl bulk-edit-time-entries <id...> --json '<json-patch-array>'`

Resources:
- `toggl list [--since DATETIME] [--until DATETIME] [project|tag|client|workspace|task|organization] [-j]`
- `toggl organization list [-j]`
- `toggl organization show <id> [-j]`
- `toggl create project <name> [--color HEX]`
- `toggl create tag <name>`
- `toggl create client <name>`
- `toggl create workspace <organization_id> <name>`
- `toggl create task -p PROJECT <name> [--active true|false] [--estimated-seconds N] [--user-id ID]`
- `toggl rename project <old_name> <new_name>`
- `toggl rename tag <old_name> <new_name>`
- `toggl rename client <old_name> <new_name>`
- `toggl rename workspace <old_name> <new_name>`
- `toggl delete project <name>`
- `toggl delete tag <name>`
- `toggl delete client <name>`
- `toggl delete task -p PROJECT <name>`
- `toggl edit task -p PROJECT <name> [--new-name NAME] [--active true|false] [--estimated-seconds N] [--user-id ID]`
- `toggl preferences`
- `toggl edit preferences '<json>'`
- `toggl me`
- `toggl config init|active|-e|-p|-d`

## Know-How

- Multiple tags: pass multiple values to `-t`, for example `-t dev review`, not one quoted string like `-t "dev review"` if you want two separate tags.
- Clear tags on edit: use `toggl edit time-entry [id] -t ""`.
- Remove project or task on edit: use `-p ""` or `--task ""`.
- If `start` gets both `--start` and `--end`, it creates a closed historical entry and does not stop the currently running entry.
- If `start` omits `--end`, it stops any currently running entry first.
- `--end` requires `--start`, and end time must be later than start time.
- `edit time-entry` without `[id]` edits the currently running entry.
- If you change a time entry's project during edit and do not explicitly provide `--task`, the existing task is cleared.
- If you provide a task name and it resolves successfully, that task's project becomes the time entry's project.
- `start` uses config defaults when flags are omitted, including default project, task, tags, and billable state.
- `delete` is overloaded: `toggl delete <id>` deletes a time entry, while `toggl delete project "name"` deletes a project.
- `current` and `running` are aliases.
- `list` and `show` support `-j` for JSON output.
- `list --since/--until` accepts RFC3339, local datetime, or date-only values.
- For `toggl list`, a date-only `--since YYYY-MM-DD` means local `00:00:00` at the start of that day.
- For `toggl list`, a date-only `--until YYYY-MM-DD` includes the whole local day by using the next day's `00:00:00` as the exclusive upper bound.
- To fetch exactly one local day, use the same date for both flags, for example `toggl list --since 2026-03-06 --until 2026-03-06`.
- **Bulk editing**: Use JSON Patch format for `bulk-edit-time-entries`. Common operations: `{"op":"replace","path":"/description","value":"new desc"}`, `{"op":"replace","path":"/billable","value":true}`, `{"op":"replace","path":"/tags","value":["tag1","tag2"]}`. All time entries must be in the same workspace.
- **Performance**: Read-only API responses are cached for 30 seconds by default. Cache can be disabled with `TOGGL_HTTP_CACHE_DISABLED=1` or TTL customized with `TOGGL_HTTP_CACHE_TTL_SECONDS`.
- **Organizations**: Use `toggl organization list` to see available organizations, and `toggl organization show <id>` for detailed info.

## Minimal Examples

```bash
toggl start "Feature work" -p "App" -t dev review -b
toggl start "Backfill" --start "2026-03-05 09:00" --end "2026-03-05 10:30"
toggl edit time-entry 123 -d "Updated" --billable false -p "" -t ""
toggl list --since "2026-03-06 09:00" --until "2026-03-06 18:30"
toggl list --since 2026-03-06 --until 2026-03-06
toggl list project -j
toggl organization list -j
toggl organization show 12345
toggl create project "App" --color "#06aaf5"
toggl delete task -p "App" "Code Review"
toggl edit task -p "App" "Code Review" --new-name "CR"
toggl edit preferences '{"time_format":"H:mm"}'

# Bulk edit examples
toggl bulk-edit-time-entries 123 456 789 --json '[{"op":"replace","path":"/description","value":"Meeting"}]'
toggl bulk-edit-time-entries 123 456 --json '[{"op":"replace","path":"/billable","value":true}]'
toggl bulk-edit-time-entries 123 456 --json '[{"op":"replace","path":"/tags","value":["urgent","client-work"]}]'
```

## Output And Time

- Time-entry display format: `[$] [HH:MM:SS]* - description @Project #[tag1, tag2]`
- `$` means billable; `*` means currently running.
- Accepted datetime input for `--start`, `--end`, `--since`, `--until`:
- RFC3339: `2026-03-05T09:00:00+08:00`
- Local datetime: `2026-03-05 09:00` or `2026-03-05T09:00:00`
- Date only for `--start`/`--end`: `2026-03-05` meaning local `00:00:00`
- Date only for `toggl list --since`: local `00:00:00` at the start of that day
- Date only for `toggl list --until`: includes the full local day
