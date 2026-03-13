---
name: action-item-extractor
description: >
  Extract action items from a meeting summary and append them to todos.md.
  Called as a downstream step by meeting-transcript-notes, or run manually
  to add tasks from any source.
allowed-tools:
  - Read
  - Write
---

# Action Item Extractor

Extracts action items and writes them to `todos.md` in a structured format.
Works as a downstream step from `meeting-transcript-notes`, or standalone
when a user provides tasks manually.

## Configuration

Default path (edit to match your environment):

```
TODOS_FILE: ~/todos.md
```

If `todos.md` does not exist, create it on first write using the format below.

---

## todos.md Format

`todos.md` uses a flat checklist with structured inline metadata:

```markdown
# Todo List

## Open

- [ ] **{Owner}** — {Task description} _(due: {YYYY-MM-DD or TBD})_ [source: {Meeting Title, YYYY-MM-DD}]

## Done

- [x] **{Owner}** — {Task description} _(completed: {YYYY-MM-DD})_ [source: {Meeting Title, YYYY-MM-DD}]
```

**Rules:**
- All open items live under `## Open`
- All completed items live under `## Done`
- Owner is the full name as it appears in the source
- `source` tag identifies origin (meeting title + date, or `manual`)
- If no deadline is known, use `TBD`

---

## Operations

### When called from meeting-transcript-notes

Input: the Action Items table from the meeting summary.

**Steps:**
1. Read current `todos.md` (or create if missing with the header structure above)
2. For each row in the Action Items table, append under `## Open`:
   ```
   - [ ] **{Owner}** — {Task} _(due: {Deadline or TBD})_ [source: {Meeting Title, YYYY-MM-DD}]
   ```
3. Write the updated file
4. Confirm: "Added {N} action item(s) to todos.md from {Meeting Title}"

### When called manually

**Steps:**
1. Ask the user: owner, task description, deadline (optional), source label (optional)
2. Append to `todos.md` under `## Open`:
   ```
   - [ ] **{Owner}** — {Task} _(due: {Deadline or TBD})_ [source: manual]
   ```
3. Write the updated file
4. Confirm: "Added 1 item to todos.md"

---

## Error Handling

- **File not found:** Create `todos.md` with the standard header, then write
- **Empty action items table:** Notify the user, do not write anything
- **Missing owner or task:** Ask the user to provide the missing field before proceeding
