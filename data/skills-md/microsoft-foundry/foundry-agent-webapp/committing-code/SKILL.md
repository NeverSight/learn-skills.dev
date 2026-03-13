---
name: committing-code
description: >
  Provides commit message format and workflow for this repository.
  Use when creating git commits, reviewing staged changes, or
  generating conventional commit messages.
---

# Commit Message Format

```text
<type>(<scope>): <short description>

## Summary
Brief description of what was done. Fixes #<issue-number>.

## New Components

### ComponentName (path/to/file.ts)
- Bullet points describing the component

## Enhanced Components

### ExistingComponent.ts
- What was changed and why

## Files Changed
- path/to/file1.ts
- path/to/file2.ts

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

## Type Prefixes

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `chore` | Dependencies, config, tooling |
| `docs` | Documentation only |

Scope is optional — use when the change targets a specific area (e.g., `feat(citations):`, `fix(auth):`).

## Commit Workflow

1. Run `git diff --staged` to review all staged changes
2. Read files for context if needed; look for related issue numbers
3. Write the commit message to `COMMIT_MESSAGE.md`
4. Run `git commit -F COMMIT_MESSAGE.md`
5. Delete `COMMIT_MESSAGE.md`

## Rules

- Subject line: max 72 chars, imperative mood ("Add" not "Added")
- Include `Fixes #N` or `Closes #N` in Summary when applicable
- Always list all changed files in the Files Changed section
- Omit "Testing" and "Breaking Changes" sections — not used in this repo
- New components: document with bullet points describing key features
- Enhanced components: explain what changed and why
- Always include the Co-authored-by trailer as the last line of the commit body:
  `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`

## Constraints

- ❌ Don't stage files (`git add`) — that's the caller's job
- ❌ Don't push (`git push`) — user decides when to push
- ❌ Don't modify code — only create commits during the commit workflow
