---
name: project-log
description: Ensures a .docs folder exists, creates project-log.md, and records current project status for handoff. Use when ending a session, before context switches, when handing off to another person or agent, or when the user asks to save project status or create a project log.
metadata:
  author: switch-dimension
  version: "1.0.0"
---

# Project Log Skill

Creates or updates a project handoff log so anyone picking up the project understands its current state.

## Instructions

### 1. Ensure `.docs` folder exists

- List the project root directory.
- If `.docs` does not exist, create it.
- Use the workspace root path for all operations.

### 2. Create or update `project-log.md`

- Path: `.docs/project-log.md`
- If the file exists, append a new entry rather than overwriting.
- If it does not exist, create it with the structure below.

### 3. Record current project status

Populate the log entry with information that helps the next person (or agent) understand:

- **What was done**: Summary of recent work, changes made, or decisions.
- **Current state**: Working / broken / in progress / blocked.
- **Next steps**: Explicit recommendations for what to do next.
- **Context**: Relevant tech stack, important files, environment notes, blockers.
- **Timestamp**: Date and brief context (e.g. "After implementing auth", "End of session").

## Template

```markdown
## [YYYY-MM-DD] — [Brief title, e.g. "End of auth implementation"]

### Summary
[1–2 sentences: what was accomplished in this session or phase]

### Current State
[ ] Working
[ ] In progress
[ ] Blocked — [reason]
[ ] Broken — [what’s wrong]

### Next Steps
1. [First concrete action]
2. [Second action]
3. [Third action]

### Context
- **Stack**: [e.g. Next.js 14, PostgreSQL]
- **Key files**: [e.g. `src/auth/`, `lib/db.ts`]
- **Notes**: [Environment setup, credentials location, known gotchas]

---
```

## When to Use

- User says: "Save the project status", "Create a project log", "Log what we did", "Hand off"
- Before ending a long session or switching to unrelated work
- When explicitly handing off to another person or agent
- When user asks to "document current state" or "note next steps"
