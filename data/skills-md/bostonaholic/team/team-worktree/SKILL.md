---
name: team-worktree
description: 'Use for isolated worktrees only on explicit request. Never infer from work needing isolation. Applies project conventions.'
effort: low
argument-hint: "[docs/plans/<id>/]"
---

# Team Worktree

Before finalizing prose you author, read the [writing standards](../team/references/writing.md).

Create one isolated git worktree per involved repo, all on branch `<id>`, without touching any main working tree: the home repo in single-repo mode (default), or every repo in `docs/plans/<id>/4-repos.md` when it exists.

## Core contracts

- Detect a linked checkout with `git rev-parse --git-dir` and `git rev-parse --git-common-dir`.
- **Non-default branch** in an existing linked checkout → skip worktree creation for this repo.
- **Default branch** → report and stop.
- Single-repo: `git worktree add .claude/worktrees/<branch>`. Each `4-repos.md` entry: `git -C <repo> worktree add .claude/worktrees/<branch>`.
- Record every created path under `## Worktrees` in `4-repos.md`.

## Procedure references

Read each reference completely when reaching it, in order; later stages depend on earlier state and gates.

1. [Input](references/01-input.md)
2. [Detect mode](references/02-detect-mode.md)
3. [Detect existing worktree](references/03-detect-existing-worktree.md)
4. [Execution](references/04-execution.md)
