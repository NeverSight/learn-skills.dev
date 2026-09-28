---
name: jb-git-sync
description: Sync a configured personal Git repository by committing local changes, integrating upstream, and pushing.
disable-model-invocation: true
---

# JB Git sync

Run only when the user explicitly invokes `jb-git-sync`. The invocation authorizes the commit, pull, and push sequence for the selected repository.

## Repositories

| Name | Path | Purpose |
| --- | --- | --- |
| `jb-home` | `~/jb-home` | Back up symlinked settings and other tracked home configuration. |

Sync `jb-home` when the user names no repository. Add other repositories to this table when the user configures them; do not guess a path from a name.

## Sync

1. Expand the configured path and check that it exists, is a Git worktree, has a current branch, and has an upstream. If any check fails, report the reason and stop for that repository.
2. Inspect staged, unstaged, and untracked changes. Load and apply `jb-committer` to group and commit all coherent pending changes. Its push step belongs at step 4 of this workflow.
3. Fetch and integrate the current branch's upstream with a merge. Resolve straightforward conflicts using the repository context; if the correct resolution is unclear, stop with the conflicted files identified. Never discard local changes or rewrite published history to complete a sync.
4. Push the current branch to its configured upstream. Confirm the push succeeded and the worktree is clean. If there was nothing to commit or push, report that accurately.
5. Give a short summary of the local changes pushed, any upstream changes integrated, and the resulting branch status. Report failures with the point where the sync stopped.
