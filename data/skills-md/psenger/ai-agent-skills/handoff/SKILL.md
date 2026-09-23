---
name: handoff
description: >
  Make sure to use this skill whenever the user types /handoff (with or without a
  filename argument), says "handoff", "save state", "context rot", "save session",
  "create a handoff", "I need a clean start", wants to snapshot progress before
  clearing context or switching sessions, is approaching the context limit
  (300–400k tokens), or wants to delegate the current session state to another agent.
  Also invoke for RESUME mode: when the user says "load handoff", "resume from [file]",
  "continue where we left off", "pick up where I left off", "load the handoff at
  [path]", references a .claude/handoffs/ file path, or says there is a handoff file
  from a prior session. Creates or loads a structured JSON snapshot capturing goals,
  decisions, completed steps, pending work, constraints, and modified files so work
  can continue cleanly in a new session.
allowed-tools: Read, Write
---

# Handoff

Saves or loads a structured JSON snapshot of session state. Use the schema in `references/schema.md` for all fields.

---

## Mode Selection

- **User wants to save / pause / context is full** → CREATE workflow
- **User wants to resume / load / continue** → RESUME workflow
- **After 5+ file edits or a major decision** → suggest: *"We've made good progress — say 'create handoff' when you're ready to save state and start fresh."*

---

## CREATE Workflow

### Step 1 — Determine Output File

Use the user's argument if provided (e.g. `/handoff auth-work.json`). Otherwise default
to `.claude/handoffs/YYYY-MM-DD-HHMMSS-<slug>.json` in the project root, where `<slug>`
is 2–4 words from the task goal (e.g. `auth-refactor`, `payment-api`). Create
`.claude/handoffs/` if it doesn't exist.

### Step 2 — Analyse the Session

Review the full conversation and all modified files, then extract:

- The primary goal and what "done" looks like (acceptance criteria)
- All architectural and design decisions reached, with rationale
- What has been completed and can be verified
- What still needs to be done, in priority order
- Hard constraints and non-negotiables
- Known bugs, issues, or unresolved warnings
- Which files were changed and what was done to each

### Step 3 — Write the Handoff File

Write the JSON using the schema in `references/schema.md`. Do not omit any top-level
field — use `[]` if there is nothing to report.

### Step 4 — Confirm and Guide the User

```
Handoff written to: <filename>

Summary:
- Task: <goal>
- Completed: <N> steps
- Pending: <N> steps
- Constraints: <N>
- Open issues: <N>
- Modified files: <N>

Next steps:
1. Run /clear to wipe the context window
2. Start a new session
3. Paste this prompt to resume:

"<resume_prompt value>"
```

> Do **not** run `/clear` yourself — the user must do this manually.

---

## RESUME Workflow

### Step 1 — Locate the File

Use the user's argument if given. Otherwise read `.claude/handoffs/` and pick the most
recent file by filename timestamp. If the directory is empty or missing, tell the user.

### Step 2 — Load and Orient

Read the file fully. Then report:

```
Loaded handoff: <filename>

- Task: <goal>
- Completed: <N> steps
- Pending: <N> steps
- First step: <pending_steps[0]>
- Open issues: <N>
- Constraints: <N>
```

### Step 3 — Begin Work

Start immediately with `pending_steps[0]`. Keep `constraints`, `discovered_issues`, and
`decisions` visible as you work — don't re-litigate choices already made.

---

## Reference Files

- `references/schema.md` — full JSON schema, field rules, and a complete example
