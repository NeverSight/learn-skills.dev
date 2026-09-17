---
name: using-git-worktrees
description: Use when a change needs workspace isolation or when determining whether an existing workspace is already isolated.
---

# Work Safely in the Right Workspace

Inspect the current directory, branch, working tree, remotes, and worktree state
before creating or switching anything. Preserve user changes. A linked worktree or
a dedicated clone may already provide the isolation needed.

Use an existing suitable workspace. If new isolation is needed, follow the user's
preference and repository policy. Prefer host-managed workspace tools when they
own the task's checkout; otherwise use Git worktrees. Do not create extra worktrees
merely because implementation has a plan.

For manual worktrees, choose a clear task-specific location and branch. Verify a
project-local worktree directory is ignored, or use a location outside the repo.
Do not commit unrelated ignore-file changes automatically. A directory's name
does not prove who owns it.

Use the repository's package manager and setup instructions. Install dependencies
only when needed. Run relevant baseline checks when they help distinguish existing
failures from regressions; do not force a full environment rebuild for a docs edit.

If isolation is required but unavailable, report the limitation instead of silently
editing a checkout that was meant to remain untouched. Detached HEAD alone does
not prove branch creation is forbidden; follow actual host capabilities and rules.

Keep the workspace for iteration and handoff. Cleanup requires known ownership,
inspection for uncommitted work, and authorization appropriate to the deletion.
Never reset or remove a user's workspace to tidy up.
