---
name: git-workflow
description: Enforce structured git workflow with conventional commits, feature branches, semver versioning, and work logging. Use for all code changes to prevent work loss and maintain history.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Git Workflow Skill

Structured development workflow using git, conventional commits, and work logging.

## Core Principles

| Principle | Description |
|-----------|-------------|
| Issue-First | All work starts with an issue (bd or GitHub) |
| Feature Branches | One branch per issue/feature |
| Conventional Commits | Structured commit messages |
| Semver Versioning | Semantic version numbers |
| Work Logging | Document all changes in `.worklog/` |
| UAT Workflow | Human acceptance testing before merge |

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  1. Create/claim issue (bd create or bd update --status)    │
│                     ↓                                       │
│  2. Create feature branch (git checkout -b type/issue-id)   │
│                     ↓                                       │
│  3. Make changes, commit with conventional format           │
│                     ↓                                       │
│  4. Create worklog entry documenting changes                │
│                     ↓                                       │
│  5. Request UAT (/uat request <feature>)                    │
│                     ↓                                       │
│  6. Human tests and approves (/uat approve) or denies       │
│                     ↓                                       │
│  7. Merge to main, close issue, tag if release              │
└─────────────────────────────────────────────────────────────┘
```

## Branch Naming Convention

```
<type>/<issue-id>-<short-description>
```

| Type | Use Case | Example |
|------|----------|---------|
| `feature/` | New functionality | `feature/proj-123-dark-mode` |
| `fix/` | Bug fixes | `fix/proj-456-form-validation` |
| `chore/` | Maintenance, deps | `chore/proj-789-update-deps` |
| `docs/` | Documentation only | `docs/proj-101-api-reference` |
| `refactor/` | Code restructuring | `refactor/proj-202-simplify-auth` |

## Conventional Commits

Format: `<type>(<scope>): <description>`

### Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature for the user |
| `fix` | Bug fix for the user |
| `docs` | Documentation changes |
| `style` | Formatting, missing semicolons (no code change) |
| `refactor` | Refactoring production code |
| `test` | Adding tests (no production code change) |
| `chore` | Build tasks, package manager configs |

### Examples

```bash
# Feature
git commit -m "feat(auth): add OAuth2 login support"

# Bug fix
git commit -m "fix(forms): correct email validation regex"

# Documentation
git commit -m "docs(readme): add installation instructions"

# Breaking change (add ! after type)
git commit -m "feat(api)!: change response format to JSON:API"
```

### Commit Body for Complex Changes

```bash
git commit -m "$(cat <<'EOF'
feat(validation): add incremental file validation

- Add git-aware file detection
- Implement MD5-based result caching
- Support staged-only mode for pre-commit hooks

Closes: proj-59l
EOF
)"
```

## Semantic Versioning (Semver)

Format: `MAJOR.MINOR.PATCH`

| Version Part | When to Bump | Example |
|--------------|--------------|---------|
| MAJOR | Breaking changes | 1.0.0 → 2.0.0 |
| MINOR | New features (backward compatible) | 1.0.0 → 1.1.0 |
| PATCH | Bug fixes (backward compatible) | 1.0.0 → 1.0.1 |

### Tagging Releases

```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release v1.2.0: Add dark mode support"

# Push tags
git push origin --tags
```

## Work Logging

Every significant change creates a worklog entry in `.worklog/`.

### Worklog File Format

File: `.worklog/YYYY-MM-DD-issue-id-description.md`

```markdown
# Worklog: [Issue ID] - Short Description

**Date**: YYYY-MM-DD HH:MM
**Issue**: {issue-id}
**Branch**: feature/{issue-id}-description
**Status**: in_progress | complete | blocked

## Summary
Brief description of what was done.

## Changes Made
- List of files modified
- Key decisions made
- Problems solved

## Files Modified
- `path/to/file1.js` - Description of change
- `path/to/file2.css` - Description of change

## Testing Done
- [ ] Unit tests pass
- [ ] Manual testing complete
- [ ] UAT requested

## Notes
Any additional context for future reference.

## Recovery Instructions
If this work needs to be recovered:
1. Checkout branch: `git checkout feature/{issue-id}`
2. Key commits: `abc1234`, `def5678`
```

## Git Commands Reference

### Starting Work

```bash
# Sync with remote
git fetch origin
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/{issue-id}-description

# Claim the issue
bd update {issue-id} --status in_progress
```

### During Work

```bash
# Stage changes
git add <files>

# Commit with conventional format
git commit -m "feat(scope): description"

# Push to remote (first time)
git push -u origin feature/{issue-id}-description

# Push subsequent changes
git push
```

### Completing Work

```bash
# Ensure all tests pass
npm test

# Update worklog
# Create/update .worklog/YYYY-MM-DD-xxx.md

# Request UAT
# /uat request <feature-name>

# After UAT approval, merge to main
git checkout main
git pull origin main
git merge --no-ff feature/{issue-id}-description
git push origin main

# Close the issue
bd close {issue-id} --reason "Implemented and merged"

# Delete feature branch
git branch -d feature/{issue-id}-description
git push origin --delete feature/{issue-id}-description
```

## UAT (User Acceptance Testing)

### Requesting UAT

After completing work, request human testing:

```
/uat request <feature-name>
```

This creates a `uat-<feature-name>.md` file with testing instructions.

### UAT Response

Human reviews and responds:

```
/uat approve <feature-name>    # Feature accepted
/uat deny <feature-name>       # Feature needs work
```

### Handling Denied UAT

If UAT is denied:
1. Review feedback in the UAT file
2. Make necessary changes
3. Update worklog
4. Request UAT again

## Pre-Session Checklist

When starting an AI assistant session:

1. **Check git status**: Any uncommitted changes?
2. **Review open issues**: `bd ready` or `bd list --status open`
3. **Check current branch**: On main or a feature branch?
4. **Review recent worklogs**: `.worklog/` for context

## Red Flags

| Situation | Action |
|-----------|--------|
| Working without an issue | Create issue first with `bd create` |
| Commits directly to main | Use feature branch |
| No worklog entry | Create before requesting UAT |
| Large uncommitted changes | Commit incrementally |
| Merge conflicts | Resolve carefully, test after |

## Quick Reference

```bash
# Start work on issue
bd update <id> --status in_progress
git checkout -b feature/<id>-description

# Commit change
git add . && git commit -m "feat(scope): description"

# Complete work
git push -u origin HEAD
# Create worklog entry
# /uat request <feature>
# After approval: merge, close issue, cleanup
```

## Related Skills

- **pre-flight-check** - "INVOKE FIRST before any code work
- **ci-cd** - Configure GitHub Actions for automated testing, building,...
