---
name: task-tracking
description: Task management and tracking for agents. Use this skill whenever you need to create, update, claim, or retrieve tasks for agent workflows. This skill is triggered for any request involving task lists, task assignment, or status updates.
---

This skill enables agents to manage tasks using the bundled bash script `task_tracking.sh`, located in the skill's `scripts` folder.

## Prerequisites

Requires `jq` for JSON processing. Install via your system package manager if not already available.

## How It Works

The script stores task data in a `.tasks` directory. It automatically finds the correct location by:

1. Walking up from your current directory to find an existing `.tasks` directory
2. If not found, creates `.tasks` in your current directory

**This means:**

- ✅ Works from any subdirectory once `.tasks` exists
- ✅ No need to remember or navigate to workspace root
- ⚠️ Initial setup: be in your desired workspace root when creating the first task list

> **Discovery:** Run `bash <path-to-skill>/scripts/task_tracking.sh --help` to see all available commands.

## Quick Start

**Note:** In all examples below, replace `<path-to-skill>` with the absolute path to where this skill is loaded from (the directory containing this SKILL.md file).

- **Create a task list:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh create-list <list-name>
  ```
- **List available task lists:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh list-lists
  ```
- **Add a task:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh add-task <list-name> "<description>" [--file <path>]... [--doc <path>]... [--skill <name>]... [--ac "<criterion>"]... [--verify-command "<cmd>"] [--verify-instruction "<text>"] [--depends-on <task-id>]...
  ```
- **Claim or get next task:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh next <list-name> [--skip-failed] [--claim <AGENT_ID>]
  ```
- **Update task status:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh update-status <list-name> <task-id> <status> "<note>"
  ```
- **Update task metadata:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh update-task <list-name> <task-id> [--description "<text>"] [--file <path>]... [--doc <path>]... [--skill <name>]... [--ac "<criterion>"]... [--verify-command "<cmd>"] [--verify-instruction "<text>"] [--depends-on <task-id>]...
  ```
- **Add a dependency:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh add-dependency <list-name> <task-id> <depends-on-task-id>
  ```
- **Remove a dependency:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh remove-dependency <list-name> <task-id> <depends-on-task-id>
  ```
- **List all tasks in a list:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh list-tasks <list-name> [--format summary|full|json]
  ```
- **Query/filter tasks:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh query <list-name> [--status <status>] [--search <term>] [--depends-on <task-id>] [--blocked] [--claimed-by <agent-id>] [--limit <n>]
  ```
- **Count tasks:**
  ```bash
  bash <path-to-skill>/scripts/task_tracking.sh count <list-name> [--status <status>] [--exclude-status <status>]...
  ```

## Script Reference

Run `bash <path-to-skill>/scripts/task_tracking.sh --help` for complete CLI documentation.

**Key concepts:**

- **The script automatically finds or creates the `.tasks` directory** by walking up from your current location. All operations are performed via the CLI interface.

- Task statuses: `todo`, `in_progress`, `completed`, `failed`, `skipped`
  - `completed` and `skipped` are **terminal** — `next` will not pick them up, and they satisfy dependency requirements for downstream tasks
  - `skipped` means "won't implement" — use `update-status <list> <id> skipped "<reason>"` to mark a task as deliberately bypassed
- **`update-status`** changes status and writes a log entry. Both `<status>` and `<note>` are positional and always required.
- **`update-task`** edits metadata only — description, context, acceptance criteria, verification, dependencies. It never changes status or writes a log entry. Use it to fix typos, add context, or clarify scope at any time.
- Each task has a `context` object with `files`, `docs`, and `skills` arrays (via repeatable `--file`, `--doc`, `--skill` flags). All are optional and default to empty arrays.
- Tasks may include `acceptance_criteria` (list of strings, via repeatable `--ac`) and a `verification` object (via `--verify-command` or `--verify-instruction`). All are optional.
- `--verify-command` stores `{"type":"command","value":"..."}` — a shell command the agent can execute.
- `--verify-instruction` stores `{"type":"instruction","value":"..."}` — a free-text instruction for manual verification.
- Only one of `--verify-command` or `--verify-instruction` may be specified per task.
- Metadata arrays (`--file`, `--doc`, `--skill`, `--ac`) are **replaced**, not appended, when passed to `update-task`.

### Listing, Querying, and Counting Tasks

- **`list-tasks <list> [--format summary|full|json]`** — Lists all tasks in a list.
  - `summary` (default): returns `[{id, description, status}]` from the index — fast, no file reads
  - `full`: returns full task objects in order, reading each per-task file
  - `json`: returns the raw `_task-list.json` index

- **`count <list> [options]`** — Returns a single integer: the number of tasks matching the filters. Reads only the index file (fast). Supports `--status <status>` and `--exclude-status <status>` (repeatable; excludes each listed status).

- **`query <list> [options]`** — Filters tasks matching ALL provided criteria. Returns `[{id, description, status, claimed_by, depends_on}]`.
  - `--status <status>` — match exact status (`todo`, `in_progress`, `completed`, `failed`)
  - `--search <term>` — case-insensitive substring match in description, acceptance criteria, or notes
  - `--depends-on <task-id>` — tasks that list the given ID in their `depends_on`
  - `--blocked` — non-completed tasks with at least one non-completed dependency
  - `--claimed-by <agent-id>` — tasks claimed by the specified agent
  - `--limit <n>` — cap results at N (default: 0 = unlimited)

  Examples:

  ```bash
  # All todo tasks
  bash <path-to-skill>/scripts/task_tracking.sh query my-list --status todo

  # Search for auth-related tasks
  bash <path-to-skill>/scripts/task_tracking.sh query my-list --search "auth"

  # Tasks blocked by task-01 being incomplete
  bash <path-to-skill>/scripts/task_tracking.sh query my-list --depends-on task-01

  # All blocked tasks
  bash <path-to-skill>/scripts/task_tracking.sh query my-list --blocked

  # Tasks claimed by a specific agent
  bash <path-to-skill>/scripts/task_tracking.sh query my-list --claimed-by agent-123

  # Combine filters: in-progress tasks claimed by agent-123
  bash <path-to-skill>/scripts/task_tracking.sh query my-list --status in_progress --claimed-by agent-123
  ```

## Dependency Tracking

Tasks can declare dependencies on other tasks via `depends_on` (a list of task IDs).

- **`next --claim`** rejects a task if any of its `depends_on` tasks are not `completed`. Complete blocking tasks first.
- **`update-status ... completed`** prints a warning listing any pending tasks that depend on the one being completed, so you know what is now unblocked.
- Use `--depends-on <task-id>` (repeatable) with `add-task` or `update-task` to set/replace the full dependency list.
- Use `add-dependency` / `remove-dependency` for surgical edits to an existing task's dependencies.
- Circular dependencies are not auto-detected; avoid them when designing task lists.

## Error Handling

**CRITICAL:** If the task tracking script returns an error or fails to execute:

1. **IMMEDIATELY notify the user** about the error and include the full error message
2. **DO NOT attempt to modify task files manually** (e.g., editing `.tasks/` directory JSON files directly)
3. **DO NOT work around the script** by using jq, cat, or other tools to manipulate task data
4. **WAIT for explicit user instruction** before taking any alternative action

The task tracking system is designed to maintain data integrity through the script interface only. Manual modifications can corrupt the task list, status logs, or task metadata.

**Data location:** The script automatically finds the `.tasks` directory by walking up from your current location, or creates it in the current directory if not found.

## Best Practices

**Initial Setup**

- Create your first task list from your intended workspace root directory
- The `.tasks` directory will be created there
- Subsequent commands work from any subdirectory

**Task management**

- Always provide meaningful context for each task
- Use agent IDs to claim tasks for specific agents
- Log progress and errors using the `update-task` command with notes
- If the script fails, stop and notify the user - do not attempt manual workarounds

**After completing a task**

- Provide a git commit message summarizing the work done for the user to use when committing changes

## Writing Self-Sufficient Tasks

When creating a task, populate enough context for a zero-context agent to succeed without follow-up questions:

**Description**: State the current state and desired outcome, not just the task name.

- Poor: `"Fix free book button"`
- Good: `"Free products show 'Add to Cart' — change button label to 'Get Free' for products with price = 0"`

**Before running `add-task`**, search the codebase to identify relevant files, then include them via `--file`.

**Acceptance criteria** (`--ac`) should describe observable outcomes, not restate the description.

**Verification**: Use `--verify-command` for automated checks, `--verify-instruction` when human judgment is needed.
