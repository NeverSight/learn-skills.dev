---
name: daily-unblock
description: Unblock a task on standby and bring it back to active status. This skill should be used when Benjamin says "unblock", "resume", "unpause", "pick back up", or when a blocked task's dependency has been resolved.
argument-hint: "[task-id or JIRA-KEY]"
disable-model-invocation: true
---

# Unblock — Activate a Standby Task

Bring a standby task back to active status, restoring it to `in_progress` or `pending` depending on whether work had started.

## Configuration

```yaml
persistence:
  tasksDir: "~/.claude/daily-tasks"
```

## Execution Steps

### 1. Parse Arguments

**If `$ARGUMENTS` is a number:** target that task ID.

**If `$ARGUMENTS` matches a Jira key pattern** (e.g., `RGI-265`): find the task with matching `jira_key`.

**If `$ARGUMENTS` is empty:** find all tasks with `status: "standby"`.
- If exactly one standby task: use it automatically.
- If multiple standby tasks: list them all and ask which to unblock:

```
⏸ Multiple standby tasks — which to unblock?

  #3. RGI-265 — Evr Insights migration
     └─ Waiting on: Claire's QA review · standby 2h ago
  #7. MITB-99 — Gong push config regression
     └─ Waiting on: data pipeline rerun · standby 1d ago

Run /daily-unblock 3 or /daily-unblock RGI-265 to pick one.
```

**Stop here.**

- If zero standby tasks: "No tasks on standby. Nothing to unblock." **Stop.**

### 2. Load Task File

Read today's task file:

```bash
cat ~/.claude/daily-tasks/$(date +%Y-%m-%d).json 2>/dev/null
```

If no file exists: "No task file for today. Run `/daily-standup` first." **Stop.**

Parse the JSON. Find the target task by numeric ID or `jira_key`.

If not found: "Task #N not found. Today has tasks 1-M." **Stop.**

### 3. Validate

If `status !== "standby"`: "Task #N is not on standby (current status: {status}). Nothing to unblock." **Stop.**

### 4. Determine Target Status

- If `started_at` is not null → restore to `"in_progress"` (task was in progress when parked)
- If `started_at` is null → restore to `"pending"` (task was never started)

### 5. Update Task

Read the current task file (fresh read), update the target task:
- Set `status` to the determined value (`in_progress` or `pending`)
- Set `waiting_on` to `null`
- Set `paused_at` to `null`
- Update `updated_at` on the root object

Write the updated JSON back using the **Write tool**.

### 6. Confirm

Display:

```
▶️  Task #N unblocked: $JIRA_KEY — $SUMMARY
   Status: $NEW_STATUS
```

**If restored to `pending`:**

```
👉 Run /daily-next $N to pick it up and get full context.
```

**If restored to `in_progress`:**

```
👉 Task is back in progress. Run /daily-next $N to get a briefing and continue.
```

Show compact remaining standby tasks if any still exist:

```
⏸ N task(s) still on standby — run /daily-unblock N when ready.
```

## Edge Cases

- **Task not on standby:** "Task #N is not on standby (status: X)." Stop.
- **Multiple standby tasks, no argument:** List all with reasons and ask. Stop.
- **Zero standby tasks, no argument:** "No tasks on standby." Stop.
- **Task ID doesn't exist:** "Task #N not found. Today has tasks 1-M."
- **File write fails:** Report error, do not silently lose the update.
