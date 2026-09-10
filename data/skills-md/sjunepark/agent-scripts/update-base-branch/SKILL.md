---
name: update-base-branch
description: "Switch the current Git worktree from a feature branch to its intended base or integration branch and fast-forward that local branch to its configured remote tip. Use when the user asks to leave current feature work and update, refresh, or move to the latest dev, main, trunk, or worktree-specific primary branch. Do not use to merge or rebase a base branch into a feature branch, rewrite divergent history, or update a different worktree."
---

# Update Base Branch

Move the current worktree onto its intended base branch and update it without discarding work or guessing across ambiguous branches, remotes, or worktrees.

## Protect the current worktree

Inspect the branch, status, and worktrees. If dirty, assess the target and
upstream read-only, then report any ambiguity with the request to commit or
stash local work. Fetch or switch only after verifying a clean worktree;
never stash automatically.

## Resolve the target

1. Inspect local and remote branches and upstream configuration.
2. Use a branch the user named. Otherwise select the current worktree's established base or integration branch when repository evidence makes it unambiguous. Treat an available `dev` branch as the usual default candidate, not as permission to ignore conflicting evidence.
3. Ask the user which branch to use when the target remains ambiguous. Include the likely candidates and their upstreams.
4. Keep the operation inside the current worktree. If the desired branch is checked out in another worktree, ask for a different worktree-specific base branch or tell the user to run the operation in the owning worktree. Do not update the other worktree implicitly.

## Resolve the upstream

1. Resolve the selected local branch's configured upstream. Do not assume a remote named `origin`.
2. If the branch has no upstream, or the same branch name exists on multiple remotes without a clear choice, ask which remote branch should be authoritative.
3. Never reset, force-switch, delete, or rewrite commits to reach the remote tip.

## Update the branch

1. Fetch only after the target branch and authoritative remote are resolved.
2. Before switching, verify that the selected local branch is an ancestor of the fetched upstream. If it contains commits absent from the upstream, whether ahead or diverged, stop and report both sides instead of choosing a reconciliation strategy.
3. Switch the current worktree to the selected local branch. If the user selected a remote-only branch, create its local tracking branch without overwriting an existing ref.
4. Fast-forward the local branch to the fetched upstream. Require a fast-forward-only update.
5. Verify that:
   - the current worktree is on the selected branch;
   - its upstream is the resolved remote branch;
   - local `HEAD` equals the fetched upstream tip; and
   - the worktree remains clean.

Report the branch, upstream, and resulting commit. If any assertion fails, report the exact state and do not claim completion.
