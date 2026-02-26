---
name: handoff
description: Transfer context to a new focused session. Use when starting a new phase of work, handing off to a new session, or when context needs to be summarized for continuation. Triggers on "handoff", "transfer context", "start new session with context", or when the user wants to continue work in a fresh session.
---

# Handoff

Generate a session summary and write it to `handoff.md` so a new session can pick up where this one left off.

## Workflow

1. **Analyze the current session** — gather goals, progress, decisions, file changes, blockers, and next steps.
2. **Write `handoff.md`** — save the summary to `handoff.md` in the project root (overwrite if exists).
3. **Guide the user** — tell the user to start a new session with: `read handoff.md and continue the work`.

## Handoff File Template

Write `handoff.md` using this structure:

```markdown
# Handoff

## Goal

[Original objective of this session]

## Progress

- [What was completed]
- [What was partially done]

## Key Decisions

- [Decision 1 and why]
- [Decision 2 and why]

## Files Changed

- `path/to/file1` — [what changed]
- `path/to/file2` — [what changed]

## Current State

[Where things stand right now — what works, what doesn't]

## Blockers / Gotchas

- [Any issues, edge cases, or warnings for the next session]

## Next Steps

1. [Concrete next action]
2. [Follow-up action]
```

## Guidelines

- **Be self-contained** — the new session must understand the full picture without the old conversation.
- **Be concise** — include only what's relevant; skip empty sections.
- **Focus on decisions and rationale** — what was decided and why, not the full discussion.
- **List concrete files with context** — path + what changed, not just paths.
- **State next steps as actionable tasks** — clear enough to execute immediately.

## After Writing

Confirm the file was written and instruct the user:

> `handoff.md` has been saved. To continue in a new session, start with:
>
> ```
> read handoff.md and continue the work
> ```
