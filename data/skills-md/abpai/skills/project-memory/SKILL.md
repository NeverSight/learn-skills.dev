---
name: project-memory
description: Always-on project memory workflow. At the start of every task, read `.agents/LEARNINGS.md`; while working, update it with mistakes, corrections, successful and failed patterns, and project-specific preferences.
---

# Project Memory

Maintain a per-project markdown memory file so future work improves over time.

This skill is always active. No trigger phrase is required.

## Session Start

1. Read `.agents/LEARNINGS.md` before doing any task work.
1. Apply its guidance silently during execution.
1. If it does not exist, create it with this template:

```markdown
# LEARNINGS

## Corrections

| Date | Source | What Went Wrong | What To Do Instead |
| ---- | ------ | --------------- | ------------------ |

## User Preferences

- (accumulate here as you learn them)

## Patterns That Work

- (approaches that succeeded)

## Patterns That Don't Work

- (approaches that failed and why)

## Domain Notes

- (project/domain context that matters)
```

Adapt sections to fit the repo, but keep entries easy to scan.

## Continuous Updates

Update `.agents/LEARNINGS.md` continuously while working, not only at session boundaries.

Add an entry immediately when:

- You identify the cause of an error.
- The user corrects your behavior or preferred approach.
- You catch your own mistake.
- An attempted approach fails.
- A non-obvious approach works reliably.
- You re-check project memory before a risky or previously error-prone step.

## What To Log

Log anything that should change behavior in future sessions:

- Self mistakes: wrong assumptions, misread code, failed commands, incorrect fixes.
- User corrections: what was requested instead.
- Tool or environment surprises.
- User preferences: style, workflow, structure.
- Reliable patterns: what worked and when.

Write entries that are specific and actionable.

Bad: `Made an error`
Good: `Assumed API returned a list; it returns a paginated object with .items`

## Maintenance

Every 5 to 10 sessions, or when file length exceeds about 150 lines:

1. Merge redundant entries.
1. Promote repeated corrections into `User Preferences`.
1. Remove notes already captured by stable rules.
1. Archive outdated or resolved items.
1. Keep the file under 200 high-signal lines.

## Examples

Self-caught mistake:

```markdown
| 2026-02-06 | self | Passed (name, id) to createUser but signature is (id, name) | Check function signatures before calling; this repo does not use conventional arg ordering |
```

User correction:

```markdown
| 2026-02-06 | user | Used relative imports | Use absolute imports from `src/` in this repo |
```
