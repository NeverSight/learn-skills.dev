---
name: daily-done
description: Mark the current or specified task as done in today's daily task list and show progress. This skill should be used when Benjamin says "done", "task complete", "finished", "mark done", or wants to mark a task as completed.
argument-hint: "[task-id or JIRA-KEY]"
disable-model-invocation: true
---

# Done — Complete Current Task

Mark a task as completed in today's task file and show remaining work.

## Configuration

```yaml
persistence:
  tasksDir: "~/.claude/daily-tasks"
```

## Execution Steps

### 1. Load Task File

Read today's task file:

```bash
cat ~/.claude/daily-tasks/$(date +%Y-%m-%d).json 2>/dev/null
```

If no file exists: "No task file for today. Nothing to mark as done." **Stop here.**

Parse the JSON.

### 2. Identify Task to Complete

**If `$ARGUMENTS` is a number:** target that task ID.

**If `$ARGUMENTS` matches a Jira key pattern** (e.g., `RGI-265`): find the task with matching `jira_key`.

**If `$ARGUMENTS` is empty:** find the task with `status: "in_progress"`.
- If multiple tasks are `in_progress`, list them and ask which one to complete.
- If no task is `in_progress`: "No task currently in progress. Specify a task ID: `/daily-done 3`"
- **Stop here** if unable to identify a single task.

**Validation:**
- If the selected task has `status: "done"`: "Task #N is already done."
- If the selected task ID doesn't exist: "Task #N not found. Today has tasks 1-M."
- If the selected task has `status: "pending"` (never started): Mark as done anyway, but note: "Task #N was never started — marking as done directly."
- If the selected task has `status: "standby"`: Warn but proceed: "⚠️ Task #N is on standby (waiting on: {waiting_on}). Marking as done anyway."

### 3. Mark as Done

Read the current task file, update the target task:
- Set `status` to `"done"`
- Set `completed_at` to current ISO timestamp (use `date -u +%Y-%m-%dT%H:%M:%SZ`)
- Set `waiting_on` to `null` and `paused_at` to `null` (clean up any standby fields)
- Update `updated_at` on the root object

Write the updated JSON back using the **Write tool**.

### 4. Show Completion Summary

Display:

```
✅ Task #N done: $JIRA_KEY — $SUMMARY
```

If `started_at` exists, calculate and show duration:

```
   ⏱️  Duration: Xh Ym
```

Show overall progress:

```
📋 Progress: N/M tasks done today
```

### 5. Show Next Task

List remaining actionable tasks (`pending` or `in_progress` only — exclude `standby`):

```
Remaining:
  #N. [TIER] $JIRA_KEY — $SUMMARY
  #N. [TIER] $JIRA_KEY — $SUMMARY
```

If any standby tasks exist, add a note:

```
⏸ N task(s) on standby — run /daily-unblock to activate when ready
```

Suggest the next task:

```
👉 Next up: Task #N ($JIRA_KEY) — $SUMMARY
   Run /daily-next to pick it up, or /daily-next M for a different task.
```

### 6. All Done State

If no pending or in-progress tasks remain (standby tasks don't count):

```
🎉 All tasks for today are done!

📋 Final: M/M complete
⏱️  Total tracked time: Xh Ym (sum of all tasks with started_at and completed_at)

Consider:
  - Running /daily-standup to refresh and check for new items
  - Checking Jira backlog for new work
```

## Edge Cases

- **Multiple `in_progress` tasks, no argument**: List all in-progress tasks with IDs and ask which to complete. Do not guess.
- **Task is `skipped`**: Allow marking as `done` — change status from `skipped` to `done`.
- **Task is `standby`**: Warn about standby state but allow marking as `done`. Clear `waiting_on` and `paused_at`.
- **File write fails**: Report error, do not silently lose the update.
- **Concurrent modification**: Read-then-write is sufficient for single-user workflow. If the file was modified between read and write, the latest write wins.
