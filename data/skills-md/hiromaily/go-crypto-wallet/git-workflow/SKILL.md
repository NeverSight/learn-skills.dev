---
name: git-workflow
description: Git branch management, commit conventions, and PR creation workflow. Use for all tasks that require code changes, regardless of language or scope.
---

# Git Workflow

Standard Git workflow for all tasks in this repository.

## ⚠️ MANDATORY: Check Branch Before Starting ANY Task

**This is the FIRST step for ANY task that involves code changes.**

Before writing any code or making any changes, you MUST check the current branch:

```bash
git branch --show-current
```

### Decision Flow

```
Current Branch?
    │
    ├─ main → ❌ DO NOT work here
    │         → Create a new branch first (see "Creating a New Branch")
    │
    ├─ Feature branch for this task → ✅ Continue working
    │
    └─ Different feature branch → ⚠️ Ask user which branch to use
```

### If on `main` Branch

**NEVER make changes directly on `main`.** Always create a new branch first:

```bash
# 1. Ensure main is up to date
git fetch origin
git reset --hard origin/main

# 2. Create new branch
git checkout -b {type}/{brief-description}-{issue-number}
```

### If on Wrong Feature Branch

Ask the user:

> "You are currently on branch `{current-branch}`. Should I:
>
> 1. Continue working on this branch?
> 2. Switch to `main` and create a new branch for this task?"

### Example Check Output

```bash
$ git branch --show-current
main
# → Must create new branch before any work!

$ git branch --show-current
feature/add-taproot-support-123
# → OK to continue if this is the correct branch for the task
```

---

## Branch Management

### Creating a New Branch

Always create from latest `main`:

```bash
git fetch origin
git checkout main
git reset --hard origin/main
git checkout -b {type}/{brief-description}-{issue-number}
```

### Branch Naming Convention

**Format**: `{type}/{brief-description}-{issue-number}`

- Description should be short and meaningful (use kebab-case)
- Issue number at the end (just the number, no "issue-" prefix)

| Type          | Prefix      | Example                           |
| ------------- | ----------- | --------------------------------- |
| Feature       | `feature/`  | `feature/add-taproot-support-123` |
| Bug fix       | `fix/`      | `fix/db-connection-error-456`     |
| Refactoring   | `refactor/` | `refactor/clean-arch-layer-789`   |
| Documentation | `docs/`     | `docs/update-readme-311`          |
| DevOps/CI     | `ci/`       | `ci/add-lint-workflow-100`        |
| Chore         | `chore/`    | `chore/update-deps-200`           |

### Branch Rules

- **Always from `main`**: Never branch from feature branches
- **One issue = One branch**: Create only one branch per issue
- **Short-lived**: Merge within days, not weeks
- **Delete after merge**: Keep repository clean

### ⚠️ Important: No Multiple Branches Per Issue

**Do NOT create multiple branches for the same issue.**

```
❌ Prohibited Pattern:
  issue-123 → fix/first-attempt-123
            → fix/second-attempt-123  ← Do NOT create this
            → fix/another-fix-123     ← Do NOT create this either

✅ Correct Pattern:
  issue-123 → fix/description-123
            → Create PR → Review → Merge
            → (If needed) Create new issue with new branch
```

### Pre-Work Verification

**Before creating a new branch, always check the following:**

```bash
# 1. Check for existing branches
git branch -a | grep "{issue-number}"

# 2. Check for existing PRs
gh pr list --search "{issue-number}"
```

- **If existing branch exists**: Continue working on that branch
- **If existing PR exists**: Merge the PR before starting new work
- **If nothing exists**: OK to create a new branch

## Commit Conventions

This project uses [Conventional Commits](https://www.conventionalcommits.org/) format.
**Commit messages are validated by `lefthook` commit-msg hook.**

### Format

```
{type}({scope}): {brief description}

- {detail 1}
- {detail 2}

Closes #{issue_number}
```

### Types (Required)

| Type       | Description                       | Release Impact |
| ---------- | --------------------------------- | -------------- |
| `feat`     | New feature                       | MINOR          |
| `fix`      | Bug fix                           | PATCH          |
| `docs`     | Documentation only                | -              |
| `refactor` | Code refactoring (no feature/fix) | -              |
| `test`     | Adding or updating tests          | -              |
| `ci`       | CI/CD changes                     | -              |
| `chore`    | Maintenance tasks                 | -              |
| `build`    | Build system changes              | -              |
| `perf`     | Performance improvements          | PATCH          |
| `style`    | Code style (formatting, etc.)     | -              |
| `revert`   | Revert a previous commit          | -              |

### Breaking Changes

Add `!` after type/scope to indicate breaking changes:

```bash
feat(btc)!: change address format to bech32m only
fix!: remove deprecated API endpoint
```

### Scope (Optional)

The following are suggested scopes, but other alphanumeric scopes are also permitted.

| Scope | Description          |
| ----- | -------------------- |
| `btc` | Bitcoin-related      |
| `bch` | Bitcoin Cash-related |
| `eth` | Ethereum-related     |
| `xrp` | XRP-related          |
| `db`  | Database             |
| `api` | API changes          |
| `cli` | CLI changes          |
| `pr`  | PR review fixes      |

### Examples

```bash
# Feature with scope
git commit -m "feat(btc): add taproot address support

- Add bech32m encoding
- Update address validation

Closes #123"

# Bug fix without scope
git commit -m "fix: resolve database connection timeout

- Increase pool timeout
- Add retry logic

Closes #456"

# Documentation
git commit -m "docs: update architecture guide

- Add layer diagram
- Clarify dependency rules

Closes #789"

# Breaking change
git commit -m "feat(btc)!: require bech32m for all taproot addresses

BREAKING CHANGE: Legacy address format no longer supported

Closes #999"
```

### Validation Error

If commit message validation fails:

```
ERROR: Commit message does not follow Conventional Commits format.

Expected format: <type>(<scope>): <description>

Types: feat, fix, docs, refactor, test, ci, chore, build, perf, style, revert

Examples:
  feat(btc): add taproot address support
  fix: resolve database connection timeout
  docs: update architecture guide
  refactor(api): reorganize endpoint handlers

Your commit message: <your-invalid-commit-message>
```

## Pull Request Creation

### ⚠️ MANDATORY: Ask Before Creating PR

**Always ask the user before creating a PR.**

Multi-phase tasks create multiple commits on a single branch.
Do not create a PR until all commits are complete.

```
After commits are pushed, ALWAYS ask:
> "Would you like me to create a PR? Or is there additional work to do?"
```

### When to Ask

| Situation                   | Action                            |
| --------------------------- | --------------------------------- |
| Single commit task          | Ask before creating PR            |
| Multi-phase task            | Ask after ALL phases are complete |
| User explicitly requests PR | Create PR without asking          |

### Create PR

```bash
git push -u origin {branch-name}

# Ask user: "Would you like me to create a PR?"
# Only proceed if user confirms

gh pr create --title "{type}: {description}" --body "$(cat <<'EOF'
## Summary
- {change 1}
- {change 2}

## Test plan
- [ ] Verification commands pass
- [ ] Manual testing completed

Closes #{issue_number}
EOF
)"
```

### PR Title Format

```
{type}: {description} (Closes #{issue_number})
```

Examples:

- `feat: add taproot address support (Closes #123)`
- `fix: resolve database connection timeout (Closes #456)`
- `docs: update architecture guide (Closes #789)`

### PR Description Template

```markdown
## Summary

- Brief description of changes

## Changes

- Change 1
- Change 2

## Test plan

- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing completed

## Related

- Closes #{issue_number}
- Related to #{other_issue}
```

## Pre-Commit Self-Review (Required)

**Before EVERY commit, you MUST complete self-review:**

### Step 1: Run Verification Commands

Execute verification commands for the modified file types:

| File Type           | Required Commands                                                                  |
| ------------------- | ---------------------------------------------------------------------------------- |
| Go (`*.go`)         | `make go-lint && make tidy && make check-build && make go-test`                    |
| TypeScript (`*.ts`) | See `typescript-development` skill (Bun for xrpl-grpc-server, npm for eth-contracts) |
| Shell (`*.sh`)      | `make shfmt`                                                                       |
| Makefile            | `make mk-lint`                                                                     |
| SQL/HCL             | `make atlas-fmt && make atlas-lint`                                                |

### Step 2: Complete Self-Review Checklist

Read the applicable language skill and verify ALL checklist items:

| File Type      | Skill                    | Section to Check       |
| -------------- | ------------------------ | ---------------------- |
| Go (`*.go`)    | `go-development`         | Self-Review Checklist  |
| TypeScript/JS  | `typescript-development` | Self-Review Checklist  |
| Shell (`*.sh`) | `shell-scripts`          | Verification Checklist |
| Makefile       | `makefile-update`        | Verification Checklist |
| SQL/HCL        | `db-migration`           | Verification Checklist |

### Step 3: Confirm Before Commit

Only proceed to commit after:

- [ ] All verification commands pass
- [ ] Self-review checklist is complete
- [ ] No unresolved linter errors

⚠️ **DO NOT commit until all steps are verified.**

## Safety Rules

### Allowed Operations

- `git add` - Stage changes
- `git commit` - Create commits
- `git push` - Push to remote
- `git checkout -b` - Create branches

### NOT Allowed Operations

- `git push --force` - Never force push
- `git merge` - Don't merge locally
- `git rebase` on shared branches - Avoid rebasing
- Direct commits to `main` - Always use PRs

## Quick Reference

### New Issue Workflow

```bash
# 0. Check for existing branches/PRs (Required)
git branch -a | grep "{issue-number}"
gh pr list --search "{issue-number}"
# → If exists, continue working on that branch

# 1. Update main
git fetch origin && git checkout main && git reset --hard origin/main

# 2. Create branch (only if none exists)
git checkout -b {type}/{brief-description}-{issue-number}

# 3. Make changes...

# 4. Self-Review (REQUIRED - see "Pre-Commit Self-Review" section)
#    - Run verification commands for modified file types
#    - Complete self-review checklist from language skill
#    - Confirm no linter errors

# 5. Commit (only after self-review is complete)
git add <files>
git commit -m "{type}: {description}

Closes #{number}"

# 6. Push
git push -u origin {branch-name}

# 7. Ask user before creating PR (REQUIRED)
#    "Would you like me to create a PR? Or is there additional work?"
#    Only create PR if user confirms
gh pr create --title "{type}: {description}"
```

### PR Review Fixes

```bash
# Already on PR branch

# 1. Make fixes...

# 2. Self-Review (REQUIRED)
#    Run verification commands & complete checklist

# 3. Commit and push
git add <files>
git commit -m "fix(pr): address review comments"
git push
```
