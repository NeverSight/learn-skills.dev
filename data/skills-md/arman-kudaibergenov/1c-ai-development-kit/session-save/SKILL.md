---
name: session-save
description: >
  Save current session state to session-notes.md in project root.
  Use when context is getting high (70%+) or before ending a work session.
---

# session-save

Save current session state to `session-notes.md` in project root.
Use when context is getting high (70%+) or before ending a work session.

## Trigger
User says: "session-save", "сохрани сессию", "save session"

## Steps
1. Create/overwrite `session-notes.md` in project root with:
   ```
   # Session Notes — <date> <time>

   ## Current Task
   <what you were working on>

   ## Completed
   - <bullet list of what was done this session>

   ## Pending
   - <what still needs to be done>

   ## Next Action
   <specific next step to take when resuming>

   ## Key Decisions
   - <important decisions made, with reasoning>

   ## Modified Files
   - <list of files changed this session>
   ```
2. Confirm to user: "Session saved to session-notes.md. You can /clear or run scripts/rotate-session.ps1"

## Rules
- Be specific in "Next Action" — it should be executable without additional context
- List ALL modified files, not just the important ones
- Keep "Completed" factual, not aspirational
