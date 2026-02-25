---
name: tsk
description: >
  Use this skill whenever the user wants to track tasks, manage a project backlog,
  create to-do lists, or organize work items using file-based YAML storage.
  Triggers include: "track this task", "add a task", "show my tasks", "what's the
  status", "move task to done", "project summary", "task list", "backlog",
  "create a task tracker", "initialize project tracking", mentions of .tsk directory,
  or any request to manage work items with priorities, statuses, tags, or activity logs.
  Also use when the user asks to set up lightweight project management without
  external services, or when working in a repo that already has a .tsk/ directory.
allowed-tools: Bash(tsk:*) Bash(node:*)
---

# tsk — File-Based Project Tracker

tsk is a CLI tool that stores tasks as YAML files in a `.tsk/` directory. It supports priorities (p0–p3), configurable statuses, tags, parent-child hierarchy, activity logs, and multiple output formats.

## Quick Start

```bash
# Initialize in current directory (creates .tsk/)
tsk init --defaults

# Create tasks
tsk add "Implement feature X" --priority p1 --tag backend
tsk add "Write tests for X" --parent 1 --tag testing

# View and manage
tsk ls                          # List all tasks grouped by status
tsk view 1                      # View task details + activity
tsk move 1 in_progress --by me  # Change status
tsk edit 1 --priority p0        # Update fields
tsk note 1 "Found edge case"    # Add activity note

# Review
tsk log                         # Activity timeline
tsk summary                     # Status breakdown with counts
tsk archive --done              # Archive completed tasks
```

## Core Workflow

1. **Check for existing project**: Look for a `.tsk/` directory in the working tree. If found, skip init.
2. **Initialize if needed**: `tsk init --defaults` creates `.tsk/` with config and task storage.
3. **Add tasks**: Use `tsk add "<title>"` with optional `--priority`, `--tag`, `--parent`, `--status`, `--by`.
4. **Track progress**: Use `tsk move <id> <status>` to transition tasks. Use `--by` to attribute actions.
5. **Communicate**: Use `tsk note <id> "<message>"` to record context and decisions.
6. **Review**: Use `tsk ls`, `tsk summary`, or `tsk log` to understand project state.

## Output Formats

tsk auto-detects the output format:
- **TTY** (interactive terminal): Pretty-printed with colors, emojis, and grouping
- **Non-TTY** (piped/programmatic): JSON output

Force a specific format with global flags:
```bash
tsk ls --json      # Always JSON
tsk ls --yaml      # Always YAML
tsk ls --quiet     # IDs only (for scripting)
```

**When using tsk programmatically (e.g., from an agent), output is JSON by default.** Parse it directly.

## Task IDs

Tasks get sequential numeric IDs (1, 2, 3...). Commands accept either:
- Bare number: `tsk view 1`
- Prefixed: `tsk view TSK-1`

## Statuses (default)

| Status        | Meaning          |
|---------------|------------------|
| `todo`        | Not started      |
| `in_progress` | Actively working |
| `review`      | Awaiting review  |
| `done`        | Completed        |

## Priorities

| Priority | Severity |
|----------|----------|
| `p0`     | Critical |
| `p1`     | High     |
| `p2`     | Medium (default) |
| `p3`     | Low      |

## Batch Operations

Move multiple tasks at once — the last argument is always the target status:
```bash
tsk move 1 2 3 done --by agent
```

## The `--by` Flag

Every mutation command (`add`, `move`, `edit`, `note`, `archive`) accepts `--by <name>` to record who performed the action. Defaults to `$USER`. Use this to attribute work when acting on behalf of a user or as an agent.

## Command Reference

For the complete list of commands with all options, read `references/commands.md`.
