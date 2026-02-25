---
name: watzup
description: '[Utilities] ⚡ Review recent changes and wrap up the work'
---

Review my current branch and the most recent commits.
Provide a detailed summary of all changes, including what was modified, added, or removed.
Analyze the overall impact and quality of the changes.

**IMPORTANT**: **Do not** start implementing.

## Doc Impact Review (MANDATORY)

After summarizing changes, you MUST check if related documentation needs updating.

### Step 1: Identify changed files

Run `git diff --name-only` (or check recent commits) to list all changed files.

### Step 2: Check each against the doc mapping

| Changed File Pattern            | Check These Docs                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `.claude/hooks/**`              | `docs/claude/claude-kit-setup.md`, `.claude/docs/hooks/README.md`, `.claude/docs/hooks/enforcement.md` |
| `.claude/skills/**`             | `docs/claude/claude-kit-setup.md`                                                                      |
| `.claude/workflows.json`        | `docs/claude/claude-kit-setup.md`                                                                      |
| `.claude/settings.json`         | `docs/claude/claude-kit-setup.md`, `.claude/docs/hooks/README.md`                                      |
| `src/Backend/**/*.cs`           | `docs/business-features/` (relevant module), `CHANGELOG.md`                                            |
| `src/Backend/**/*Command*`      | `docs/claude/backend-patterns.md` (if new pattern)                                                     |
| `src/Frontend/**/*.ts`          | `docs/business-features/` (relevant module), `CHANGELOG.md`                                            |
| `src/Frontend/**/*.component.*` | `docs/claude/frontend-patterns.md` (if new pattern)                                                    |
| `src/Platform/**`               | `docs/architecture-overview.md`, `CHANGELOG.md`                                                        |
| `docs/test-specs/**`            | `docs/TESTING.md`                                                                                      |
| `*.docker-compose*`             | `docs/claude/claude-kit-setup.md` (dev setup section)                                                  |

### Step 3: Report findings

For each stale or missing doc, report:

- **File**: path to the doc that needs updating
- **Reason**: what changed that affects it
- **Action**: what specifically needs to be added/updated

### Step 4: CHANGELOG check

Verify `CHANGELOG.md` `[Unreleased]` section is updated for non-trivial changes. If missing, flag it.

### Output format

Include a **Doc Review** section in your summary:

```
## Doc Review
- ✅ No stale docs found
OR
- ⚠️ `docs/claude/claude-kit-setup.md` — missing new hook X documentation
- ⚠️ `CHANGELOG.md` — [Unreleased] section not updated
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
