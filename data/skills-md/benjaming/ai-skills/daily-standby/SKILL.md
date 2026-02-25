---
name: daily-standby
description: Put a task on standby when it's blocked or waiting on someone. This skill should be used when Benjamin says "standby", "waiting on", "put on hold", "blocked", "can't proceed", or needs to park a task that requires external input.
argument-hint: "[task-id or JIRA-KEY] \"reason\""
disable-model-invocation: true
---

# Standby — Park a Blocked Task

Put a task on standby with a required reason describing what it's waiting on.

## Configuration

```yaml
persistence:
  tasksDir: "~/.claude/daily-tasks"
```

## Execution Steps

### 1. Parse Arguments

Split `$ARGUMENTS` into an identifier and a reason:

- **Identifier:** first token — either a numeric task ID or a Jira key pattern (e.g., `RGI-265`, `MITB-123`).
- **Reason:** everything after the identifier (strip surrounding quotes if present).

**If no reason provided:**

```
⛔ A reason is required. What are you waiting on?
   Example: /daily-standby 3 "waiting on Claire's design review"
   Example: /daily-standby RGI-265 "needs data pipeline rerun"
```

**Stop here.**

**If no identifier provided:** check for a single `in_progress` task and use that automatically. If zero or multiple `in_progress` tasks, ask for an explicit task ID. **Stop here** if ambiguous.

### 2. Load Task File

Read today's task file:

```bash
cat ~/.claude/daily-tasks/$(date +%Y-%m-%d).json 2>/dev/null
```

If no file exists: "No task file for today. Run `/daily-standup` first." **Stop.**

Parse the JSON. Find the target task by numeric ID or `jira_key`.

If not found: "Task #N not found. Today has tasks 1-M." **Stop.**

### 3. Validate Transition

| Current status | Action |
|----------------|--------|
| `done` | Reject: "Task #N is already done. Can't put a completed task on standby." Stop. |
| `skipped` | Reject: "Task #N was skipped. Use `/daily-next N` to pick it up first." Stop. |
| `standby` (no new reason) | Show current reason: "Task #N is already on standby. Waiting on: {waiting_on}. Use `/daily-unblock N` to activate it, or re-run `/daily-standby N \"new reason\"` to update the reason." Stop. |
| `standby` (with new reason) | Update `waiting_on` and `paused_at` in place. Proceed. |
| `pending` or `in_progress` | Proceed. |

### 4. Update Task

Read the current task file (fresh read), update the target task:
- Set `status` to `"standby"`
- Set `waiting_on` to the parsed reason string
- Set `paused_at` to current ISO timestamp (`date -u +%Y-%m-%dT%H:%M:%SZ`)
- Preserve `started_at` as-is (do not clear — needed for unblock logic)
- Update `updated_at` on the root object

Write the updated JSON back using the **Write tool**.

### 5. Confirm

Display:

```
⏸️  Task #N on standby: $JIRA_KEY — $SUMMARY
   └─ Waiting on: $REASON
```

Show compact remaining actionable tasks (status `pending` or `in_progress` only — exclude `standby` tasks):

```
Remaining:
  #N. [TIER] $JIRA_KEY — $SUMMARY
  #N. [TIER] $JIRA_KEY — $SUMMARY
```

If any standby tasks exist (including the one just parked), add a line:

```
⏸ N task(s) on standby — run /daily-unblock to activate when ready
```

Suggest next actionable task:

```
👉 Next up: Task #N ($JIRA_KEY) — $SUMMARY
   Run /daily-next to pick it up.
```

If no actionable tasks remain:

```
📭 No actionable tasks remaining.
   ⏸ N task(s) on standby — run /daily-unblock when unblocked, or /daily-standup to refresh.
```

## Edge Cases

- **`/daily-standby` with no identifier and no `in_progress` task:** Ask for explicit ID. Stop.
- **`/daily-standby` on already-standby task with new reason:** Update `waiting_on` and `paused_at`. Confirm update.
- **`/daily-standby` on already-standby task without new reason:** Show current reason, suggest `/daily-unblock`. Stop.
- **Task ID doesn't exist:** "Task #N not found. Today has tasks 1-M."
- **File write fails:** Report error, do not silently lose the update.
