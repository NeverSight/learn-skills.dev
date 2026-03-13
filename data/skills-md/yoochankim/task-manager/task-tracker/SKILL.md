---
name: task-tracker
description: >
  Manage an ongoing todo list in todos.md. Supports listing open tasks,
  marking items complete, querying by owner, and scheduled alerts for
  overdue or upcoming deadlines.
allowed-tools:
  - Read
  - Write
---

# Task Tracker

Manages `todos.md` — the central task list maintained by the `action-item-extractor` skill.
Use this skill to view, update, and monitor tasks after they've been added.

## Configuration

Default path (edit to match your environment):

```
TODOS_FILE: ~/todos.md
```

---

## Operations

### 1. List Items

Show open todos, optionally filtered by owner.

**Steps:**
1. Read `todos.md`
2. Extract all lines under `## Open` matching `- [ ]`
3. If an owner filter is provided, return only lines containing `**{Owner}**`
4. Format output:
   ```
   Open todos [for {Owner}]:
   1. [{Owner}] {Task} — due: {deadline} (source: {source})
   ...
   ```
5. If no items match: "No open todos [for {Owner}]."

**Usage examples:**
- "Show all open todos"
- "What does Alice need to do?"
- "List tasks for Bob"

---

### 2. Complete Item

Mark a todo as done.

**Steps:**
1. Read `todos.md`
2. Identify the matching item — by number (from List output), owner + keyword, or exact task text
3. If ambiguous (multiple matches), show options and ask the user to confirm
4. Change `- [ ]` to `- [x]` and append `_(completed: {today's date})_`
5. Move the line from `## Open` to `## Done`
6. Write the updated file
7. Confirm: "Marked as done: {task}"

**Usage examples:**
- "Mark Alice's design task as done"
- "Complete item 2"
- "Done: project proposal"

---

### 3. Query by Owner

Show all todos (open and done) for a specific person.

**Steps:**
1. Read `todos.md`
2. Extract all lines (both `## Open` and `## Done`) matching `**{Owner}**`
3. Format output:
   ```
   Todos for {Owner}:

   Open:
   - {Task} (due: {deadline})

   Done:
   - {Task} (completed: {date})
   ```
4. If none found: "No todos found for {Owner}."

---

## Scheduled Alerting

On each scheduled run, check for overdue or upcoming tasks.

**Steps:**
1. Read `todos.md`
2. For each open item with a concrete deadline (not TBD):
   - If `due date < today`: flag as **overdue**
   - If `due date <= today + 2 days`: flag as **due soon**
3. If flagged items exist, send an alert:
   ```
   ⚠️ Task Alert:
   Overdue ({N}):
   - [{Owner}] {Task} — was due {date}
   Due soon ({N}):
   - [{Owner}] {Task} — due {date}
   ```
4. If nothing flagged: no alert needed, exit silently

**Tip:** Configure your agent to run this skill periodically
so overdue alerts fire automatically without manual prompting.

---

## Error Handling

- **File not found:** Notify the user — `todos.md` doesn't exist yet. Direct them to run `action-item-extractor` or add a task manually
- **Ambiguous match on Complete:** Show matching items, ask user to confirm which one
- **No deadlines set (all TBD):** Scheduled check skips alerting silently
- **Malformed todos.md:** Notify the user and ask whether to overwrite with a clean template or attempt repair
