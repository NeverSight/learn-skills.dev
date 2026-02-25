---
name: stacked-diffs
description: >-
  Break large code changes into small, stacked pull requests using vanilla git
  and the gh CLI. Auto-trigger when implementing a feature or change that spans
  multiple logical steps, touches several files, or will exceed ~200 changed
  lines. Also trigger on "stack PRs", "break this into smaller PRs", "stacked
  diffs", or "create a PR stack". Do NOT trigger for single-file fixes, small
  bug fixes, or changes under ~200 lines that are a single logical unit.
---

# Stacked Diffs

Break large work into a chain of small, dependent PRs. Each PR is one logical unit — easy to review, test, and revert. The stack merges bottom-up into main.

## Core Rule

**Move to a new stacked branch whenever the current diff reaches a natural boundary.** Do not accumulate a large changeset on one branch. Commit, push, open a PR, then branch off and keep going.

A natural boundary is any of:
- A self-contained logical step is complete (new type, new endpoint, new test file)
- The diff is approaching ~200–400 changed lines
- The next change serves a different concern than the current one

## When to Stack

Stack when the work has **multiple logical steps that build on each other**:
- Scaffolding + core logic + edge cases
- Data model + API endpoint + UI integration
- Refactor + feature that depends on the refactor

Do NOT stack independent, unrelated changes — use separate PRs instead.

## Workflow

### 1. Plan the stack

Before writing code, sketch the stack — an ordered list of diffs, each one logical step:

```
Stack: <feature>
  01-<description> — <what and why>
  02-<description> — <what and why>
  03-<description> — <what and why>
```

The plan can evolve. If a diff grows too large or a new step emerges during implementation, split on the fly.

### 2. Execute each diff

Work through the stack sequentially. For each diff:

```bash
# First diff branches from main
git checkout main && git pull && git checkout -b <feature>/01-<description>

# Subsequent diffs branch from the previous
git checkout -b <feature>/02-<description>
```

When the diff is complete, commit, push, and open a PR:

```bash
git add <files> && git commit -m "<message>"
git push -u origin <branch>

# First PR targets main
gh pr create --base main --title "<title>" --body "$(cat <<'EOF'
...
EOF
)"

# Subsequent PRs target the previous branch
gh pr create --base <feature>/01-<description> --title "<title>" --body "$(cat <<'EOF'
...
EOF
)"
```

Then immediately check out a new branch for the next diff and keep working.

### 3. PR descriptions

Include a stack table so reviewers see the full chain:

```
## Stack

PR N/M for <feature>.

| # | PR | Description |
|---|-----|-------------|
| 1 | #<number> | <description> |
| 2 | **this PR** | <description> |

## Changes

<what this specific PR does>
```

Update earlier PRs with the table as new PRs are created.

### 4. Updating earlier diffs

If an earlier diff needs changes, rebase all downstream branches:

```bash
git checkout <feature>/01-<description>
# ... make changes, commit, push ...

git checkout <feature>/02-<description>
git rebase <feature>/01-<description>
git push --force-with-lease

git checkout <feature>/03-<description>
git rebase <feature>/02-<description>
git push --force-with-lease
```

Always `--force-with-lease`, never `--force`.

## Branch Naming

Pattern: `<feature>/<NN>-<short-description>`

```
auth/01-user-model
auth/02-login-endpoint
auth/03-session-middleware
```

## Notes

- Work one diff at a time — do not batch-create all branches upfront.
- If a diff grows beyond ~400 lines, split it before pushing.
- To extend an existing stack, branch from the current top.
