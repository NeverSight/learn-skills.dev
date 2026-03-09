---
name: do-task
description: Look up a task by ID or name and start working on it. Use when the user wants to pick up and execute a task.
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, Task, EnterPlanMode
---

# Do Task

Look up a task and start working on it.

## Instructions

The user's query is in `$ARGUMENTS` (a task ID like `077` or a task name/keyword).

1. **Look up the task**: Run `taskmd get $ARGUMENTS` to find the task
   - If not found, run `taskmd list` to show available tasks and ask the user which one they meant
2. **Read the task file** with the `Read` tool to get the full description, subtasks, and acceptance criteria
3. **Mark the task as in-progress**: Run `taskmd set <ID> --status in-progress`
4. **Start a worklog entry** (if worklogs are enabled):
   - Check `.taskmd.yaml` for `worklogs: true` -- only create worklogs if explicitly enabled
   - If enabled, find or create the worklog file at `tasks/<group>/.worklogs/<ID>.md` (or `tasks/.worklogs/<ID>.md` for root tasks)
   - Append a timestamped entry noting your approach and initial findings
5. **Do the task**: Follow the task description and complete the work described
   - Use `EnterPlanMode` for non-trivial implementation tasks
   - Check off subtasks (`- [x]`) in the task file as you complete them
   - Append worklog entries when you make key decisions, hit blockers, or complete significant subtasks
   - In the Plan, include a reference to the original task ID, and task file path.
6. **Write a final worklog entry** summarizing what was done, decisions made, and any open items
7. **Mark the task as done**: Use the `/complete-task` skill (invoke it with the task ID) to complete the task. It handles verification and status changes automatically.

## Worklog Format

Each worklog entry uses a timestamp heading followed by free-form notes:

```markdown
## 2026-02-15T10:30:00Z

Started implementation of the search feature.

**Approach:** Using full-text search with the existing SQLite database
rather than adding Elasticsearch -- simpler and sufficient for our scale.

**Completed:**

- [x] Added search query parser
- [x] Created search index

**Next:** Add result ranking and write tests.
```
