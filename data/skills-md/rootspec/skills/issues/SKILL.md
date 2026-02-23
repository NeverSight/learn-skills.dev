---
name: issues
description: Use when the user wants to view, add, update, or close issues. Manages ISSUES.md for this project.
argument-hint: "[add|close|list] [description]"
---

You are managing `ISSUES.md` for this project. This file tracks **incomplete or recently completed** issues (bugs, features, etc.).

## Rules

- **ISSUES.md** = active/incomplete issues only. Issues are removed when their work is committed.
- **CHANGELOG.md** = permanent record. When closing an issue, the commit hook already requires a CHANGELOG entry — remind the user of this if relevant.
- Keep issue descriptions concise but include: priority (P0–P3), relevant files, and approach if known.

## Commands

### `/issues` or `/issues list`
Read and display all open issues from `ISSUES.md` in a clear summary.

### `/issues add [description]`
Add a new issue to `ISSUES.md`. Ask the user for:
- Priority (P0 bug / P1 UX / P2 medium / P3 polish)
- Description and context
- Relevant files (if known)
- Approach (if known)

Then append it to the appropriate priority section in `ISSUES.md`.

### `/issues close [description]`
Remove the specified issue from `ISSUES.md` (match by name/description). Remind the user that CHANGELOG.md must also be updated as part of the commit.

## Format

Issues in `ISSUES.md` use this structure:

```markdown
## P[n] — Section Name

### Issue Title
Brief description of the problem or feature.

**Files:** `path/to/file.vue`

**Approach:** How to fix/implement it.

**Status:** (optional — e.g. "Needs scoping", "Parked")
```

Always read the current `ISSUES.md` before making any changes.
