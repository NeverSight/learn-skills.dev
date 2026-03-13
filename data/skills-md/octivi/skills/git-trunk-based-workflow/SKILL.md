---
name: git-trunk-based-workflow
description: Plan and execute Git Trunk-Based Development workflows on a repository with main as trunk. Use whenever the user asks about branch strategy, branch naming, rebasing on main, merge conflicts during rebase, PR flow, merge strategy, safe history rewrite, or branch cleanup, even if they do not mention "trunk-based" explicitly. For commit message formatting and Conventional Commits wording, delegate to git-commits.
---

# Git Trunk-Based Workflow

Guide contributors through a safe trunk-based Git workflow.

## Goal

Keep `main` releasable while integrating small changes frequently and predictably.

## Canonical rules table

Use this table as the single source of truth for workflow decisions.

| ID      | Scope             | Requirement                                                                                 |
| ------- | ----------------- | ------------------------------------------------------------------------------------------- |
| `WF-1`  | Trunk policy      | Never commit directly to `main`; use short-lived feature branches and pull requests.        |
| `WF-2`  | Branch lifecycle  | Feature branches SHOULD stay focused and short-lived; delete branches after merge.          |
| `WF-3`  | Integration       | Rebase feature branch on top of `main` frequently to minimize integration drift.            |
| `WF-4`  | History rewrite   | If branch history was rewritten (rebase/squash), push with `--force-with-lease` only.       |
| `WF-5`  | PR quality        | Open PR to `main`, keep CI green, and address review feedback before merge.                 |
| `WF-6`  | Merge mode        | Prefer standard repository merge path (typically GitHub UI) unless local merge is required. |
| `WF-7`  | Cleanup           | After merge, clean up local/remote branch references.                                       |
| `WF-8`  | Safety            | Commands provided to users MUST be copy-paste ready and scoped to their current step.       |
| `WF-9`  | Preflight         | Before branch operations, verify current branch and working tree state.                     |
| `WF-10` | Conflict recovery | Rebase guidance MUST include safe conflict resolution (`--continue` / `--abort`).           |

## Branch state preflight

Run before creating/rebasing/merging branches:

```bash
git branch --show-current
git status --short
```

If working tree is not clean, pause and either commit, stash, or discard changes before proceeding.

## Rebase conflict handling

When `git rebase` stops on conflict:

```bash
git status
# resolve conflicts in files
git add <resolved-file>...
git rebase --continue
```

If you need to cancel the rebase:

```bash
git rebase --abort
```

## Authoring workflow

1. Run `Branch state preflight` and confirm current goal.
2. Create or switch to a short-lived feature branch from up-to-date `main`.
3. Commit and push incremental progress to the feature branch.
4. Rebase feature branch onto `main` frequently (use `--rebase-merges` only when needed).
5. If rebase conflicts occur, execute `Rebase conflict handling`.
6. Optionally clean branch history before opening PR.
7. Open and land PR to `main` with green CI and addressed feedback.
8. Clean up merged branches locally and remotely.

For full command sequences and edge-case notes, use `references/git-workflow.md`.

## Out of scope

- Commit message wording/formatting and Conventional Commits phrasing belong to `git-commits`.

## Quality checklist

- Guidance conforms to all applicable `WF-*` rules.
- Commands are copy-paste ready and ordered by execution flow.
- No recommendation conflicts with repository branch policy (`main` as trunk).
- Preflight and rebase conflict recovery commands are included when relevant.
- If user asks about commit message style, explicitly route to `git-commits`.

## Prompt templates

- `Propose a trunk-based git workflow for implementing this task from branch creation to merge.`
- `Review my current git commands and rewrite them to follow a safe rebase + PR flow on main.`
- `Give me a step-by-step checklist to clean up history and merge this feature branch into main.`

## References

- `references/git-workflow.md` (canonical detailed workflow and commands)
- https://trunkbaseddevelopment.com/
