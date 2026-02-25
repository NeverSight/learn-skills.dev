---
name: trekker
description: |
  Trekker CLI task tracking for AI coding agents. Covers epics, tasks, subtasks, dependencies, comments, full-text search, history audit log, and kanban-style workflow with local SQLite storage.

  Use when creating task trackers, managing agent work sessions, tracking epics and dependencies, or implementing local-first issue tracking with Trekker CLI.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  runtime: bun
  storage: .trekker/trekker.db
user-invocable: false
---

# Trekker

## Overview

Trekker is a CLI-based issue tracker designed for AI coding agents. It stores data locally in SQLite (`.trekker/trekker.db`) and supports epics, tasks, subtasks, dependencies, comments, full-text search, and an audit history log. Use `--toon` on any command for token-efficient output.

**When to use:** Agent work session tracking, local task management, kanban-style workflows, dependency-aware task ordering, checkpoint comments for context persistence across sessions.

**When NOT to use:** Team-wide project management (use GitHub Issues/Linear), real-time collaboration, remote-first workflows, CI/CD-integrated issue tracking.

## Essential Commands

```bash
trekker init
trekker --toon ready
trekker --toon task list --status in_progress
trekker --toon task list --status todo
trekker --toon task list --epic EPIC-1
trekker --toon task show TREK-1
trekker --toon epic list
trekker --toon epic show EPIC-1
trekker --toon comment list TREK-1
trekker --toon search "query" --type task
trekker --toon list --status in_progress
trekker --toon history --entity TREK-1
trekker epic create -t "Title" -d "description" -p 2
trekker task create -t "Title" -d "description" -e EPIC-1 -p 2 --tags "a,b"
trekker subtask create TREK-1 -t "Title" -d "description" -p 2
trekker task update TREK-1 -s in_progress
trekker task update TREK-1 -s completed
trekker epic complete EPIC-1
trekker dep add TREK-2 TREK-1
trekker comment add TREK-1 -a "agent" -c "Summary: what was done and which files changed"
```

**Statuses** — Tasks/Subtasks: `todo`, `in_progress`, `completed`, `wont_fix`, `archived` | Epics: `todo`, `in_progress`, `completed`, `archived`

**Priority** — `0` critical, `1` high, `2` medium (default), `3` low, `4` backlog, `5` someday

## Valid Flags by Command

Only use flags listed here. Do NOT guess or invent flags.

| Command                     | Valid flags                                                                      |
| --------------------------- | -------------------------------------------------------------------------------- |
| `epic create`               | `-t` `-d` `-p` `-s`                                                              |
| `epic list`                 | `--status`                                                                       |
| `epic update`               | `-t` `-d` `-p` `-s`                                                              |
| `epic show/complete/delete` | (no flags, just ID)                                                              |
| `task create`               | `-t` `-d` `-p` `-s` `-e` `--tags`                                                |
| `task list`                 | `--status` `--epic`                                                              |
| `task update`               | `-t` `-d` `-p` `-s` `-e` `--tags` `--no-epic`                                    |
| `task show/delete`          | (no flags, just ID)                                                              |
| `subtask create`            | `-t` `-d` `-p` `-s`                                                              |
| `subtask update`            | `-t` `-d` `-p` `-s`                                                              |
| `subtask list/delete`       | (no flags, just ID)                                                              |
| `comment add`               | `-a` `-c` (both required)                                                        |
| `comment update`            | `-c`                                                                             |
| `comment list/delete`       | (no flags, just ID)                                                              |
| `dep add/remove`            | (no flags, two IDs)                                                              |
| `dep list`                  | (no flags, just ID)                                                              |
| `search`                    | `--type` `--status` `--limit` `--page` `--rebuild-index`                         |
| `history`                   | `--entity` `--type` `--action` `--since` `--until` `--limit` `--page`            |
| `list`                      | `--type` `--status` `--priority` `--since` `--until` `--sort` `--limit` `--page` |
| `ready`                     | (no flags)                                                                       |
| `wipe`                      | `-y`                                                                             |

**Flags that do NOT exist** (agents commonly hallucinate these):

- `--offset` — use `--page` and `--limit` instead
- `--assignee` — trekker has no assignee field
- `--label` — use `--tags` on task create/update instead
- `--verbose` / `--json` / `--quiet` — use `--toon` for compact output, default is verbose
- `--filter` — use `--status`, `--type`, `--priority` as separate flags
- `--sort` on `task list` — only available on `trekker list`
- `--all` — not a flag on any command
- `--force` / `-f` — only `wipe` accepts `-y`
- `--name` / `-n` — use `-t` / `--title` instead

**When unsure about flags**, run `--help` on any command:

```bash
trekker --help
trekker task --help
trekker task create --help
```

## Common Mistakes

| Mistake                                             | Correct Pattern                                                               |
| --------------------------------------------------- | ----------------------------------------------------------------------------- |
| Creating task without searching first               | Always `trekker search "keyword"` before creating to avoid duplicates         |
| Completing task without summary comment             | Add `Summary:` comment with what was done and which files changed             |
| Not using `--toon` flag                             | Always use `--toon` to reduce token usage in agent contexts                   |
| Forgetting to set `in_progress` before working      | Set status before starting so other agents know the task is claimed           |
| Using `epic delete` instead of `epic complete`      | `epic delete` silently orphans tasks; use `epic complete` to archive them     |
| Dependency direction reversed                       | `dep add TREK-2 TREK-1` means TREK-2 depends on TREK-1 (TREK-1 blocks TREK-2) |
| Not adding checkpoint comments before context reset | Add `Checkpoint:` comment with done items, next steps, and affected files     |
| Coding before planning                              | Create epic and break into tasks with dependencies before writing code        |
| Vague task descriptions                             | Include implementation steps, files to modify, and acceptance criteria        |
| Searching without type filter                       | Use `--type task` or `--status in_progress` to narrow results                 |
| Empty search query `trekker search ""`              | FTS5 rejects empty strings; always provide a search term                      |
| Using `wont_fix` when task is just deferred         | `wont_fix` = will never do; use `archived` for deferred or superseded work    |
| `comment add` missing `-a` or `-c`                  | Both `-a` (author) and `-c` (content) are required                            |
| Running `trekker init` twice                        | Not idempotent; errors if `.trekker/` already exists                          |
| Forgetting to gitignore `.trekker/`                 | Add `.trekker/` to `.gitignore` after init unless sharing task state          |

## Delegation

- **Task discovery and prioritization**: Use `Explore` agent to scan codebase and identify work
- **Multi-task execution**: Use `Task` agent for parallel subtask completion

## References

- [Agent workflow and session management](references/agent-workflow.md)
- [Commands and CLI usage](references/commands.md)
