---
name: resolve-git-conflicts
description: Use when resolving Git conflicts from merge, rebase, cherry-pick, or stash apply/pop via CLI, especially with unmerged paths, standard Git conflict marker lines, or messages like "both modified" or "needs merge".
---

# Resolve Git Conflicts

## Overview

Resolve Git conflicts end-to-end in the CLI. Analyze base/ours/theirs, decide which changes to keep or combine, verify the code works, then stop for human review before any commit or continue.

## Quick Start

1. `git status -sb`
2. `git diff --name-only --diff-filter=U`
3. For each file, inspect base/ours/theirs: `git show :1:PATH`, `git show :2:PATH`, `git show :3:PATH`
4. Edit files to a clean, marker-free result and run `git add PATH`
5. Run the repo build/tests if available
6. Stop for review. Do not run `git commit`, `git merge --continue`, `git rebase --continue`, or `git cherry-pick --continue`

## Workflow

1. Understand why the conflict happened.
Use `git status -sb` and `git log --oneline --decorate -n 20` to identify the operation and the competing commits.
2. Analyze all versions.
Use `git show :1:PATH` (base), `:2:` (ours), `:3:` (theirs). Use `git diff --ours PATH` and `git diff --theirs PATH` to see intent.
3. Resolve conflicts with explicit choices.
Remove markers, choose `ours`, `theirs`, or a combined result based on the decision framework. Prefer minimal, intention-preserving edits. Do not ask the user to edit; apply the changes directly and record the rationale in your response.
4. Verify the code works.
Run the project's build/test/lint commands if defined. If none exist, run the smallest available smoke check.
5. Handoff for review.
Stop after changes are staged and verified. Do not `git commit`, `git merge --continue`, `git rebase --continue`, or `git cherry-pick --continue`. Provide a short summary of decisions and files touched for review.

## Decision Framework

Do not default to `ours` or `theirs`. Decide per file using evidence.
Questions to answer before choosing:
- Which version matches the current API and usage sites?
- Which version aligns with the most recent refactor or commit intent?
- Which version is covered by or fixes failing tests?
- Which version removes deprecated code or references?
- Would combining both introduce duplication or inconsistent behavior?

Interpretation notes:
- In a merge, `ours` is the current branch and `theirs` is the merged-in branch.
- In a rebase or cherry-pick, `ours` is the branch you are applying onto and `theirs` is the commit being applied.
- If still ambiguous, choose the least risky change and state the assumption.

## Commands

| Goal | Command |
| --- | --- |
| List conflicted files | `git diff --name-only --diff-filter=U` |
| See conflict markers | `rg -n "<<<<<<<|======|>>>>>>>"` |
| Show base/ours/theirs | `git show :1:PATH`, `git show :2:PATH`, `git show :3:PATH` |
| Diff ours vs file | `git diff --ours PATH` |
| Diff theirs vs file | `git diff --theirs PATH` |
| Accept ours/theirs quickly | `git checkout --ours PATH`, `git checkout --theirs PATH` |
| Stage resolution | `git add PATH` |

If `rg` is unavailable, use `grep -n "<<<<<<<\\|======\\|>>>>>>>" PATH`.

## Example

Conflict:
```javascript
function formatUser(user) {
<<<<<<< HEAD
  return `${user.name} <${user.email}>`;
=======
  return `${user.displayName} <${user.email}>`;
>>>>>>> feature/use-display-name
}
```

Resolved (use new field, keep fallback):
```javascript
function formatUser(user) {
  const name = user.displayName ?? user.name;
  return `${name} <${user.email}>`;
}
```

Rationale: the feature branch introduced `displayName`, but existing callers may still populate `name`.

## Common Mistakes

- Continuing a merge/rebase/cherry-pick before the review handoff.
- Treating `ours` and `theirs` as fixed to "my branch" and "their branch" in all operations.
- Leaving conflict markers or partially resolved blocks in files.
- Auto-accepting one side without inspecting base and usage context.
