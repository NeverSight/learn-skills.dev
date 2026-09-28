---
name: flow-git-fix
description: "Git repair that preserves unrelated work. Use for merge or rebase conflicts, interrupted operations, broken stacks, lost commits or authorized branch cleanup. Hands back to `flow-work` or `flow-ship`."
metadata:
  stage: deliver
---

# Repair Git state

Understand the operation and ownership before changing history. Fix the requested problem
without making unrelated user work disappear.

## Phase 1: Inspect and preserve

- Read status, branch/upstream, remotes, worktrees, staged/unstaged/untracked changes, and any
  active merge, rebase, cherry-pick or revert. Check history/reflog as needed.
- Preserve valuable local work before a destructive recovery. Never reset, clean or delete an
  unfamiliar file or branch just to make a command succeed.

## Phase 2: Resolve the actual operation

- Read conflict markers, index stages, the common base and both intended changes. Ours/theirs
  flips between merge and rebase/cherry-pick; never apply one side blindly.
- Resolve behavior and affected callers, run relevant checks, stage only resolved paths, and
  continue with the operation-specific command. Confirm no conflict markers remain.
- Abort is not a universal undo: Git may be unable to restore pre-existing uncommitted changes.
  Inspect what it preserves first, then verify the resulting state instead of promising no harm.

## Phase 3: Handle stacks and publication deliberately

- Check the installed stack tool, version and help before assuming semantics.
- Stack tools differ: some restack locally, others sync by pulling, pushing and deleting
  branches. Read the dry run and scope first, use a local-only mode for local repairs, and
  account for branches skipped because another worktree owns them. Syncing a stack is not a
  local whole-stack rebase.
- Rewrite published history only when authorized and necessary. Record the remote tip being
  replaced and use an explicit lease: `--force-with-lease=refs/heads/<branch>:<reviewed-remote-oid>`.
  A bare lease can be weakened by background fetches. A rejected lease means reinspect, never
  retry the force-push. Prefer a simpler valid repair when one meets the request.

## Phase 4: Clean up only requested obsolete work

Match repository, branch identity and current tip to the merged work. Check later commits,
upstream, all worktrees and unpushed changes. A reused branch name or old merged change request is not proof
of obsolescence, and `git branch -d` may compare against upstream instead of the default
branch. Use dry-run discovery and paginated results; keep uncertain items.

## Anti-patterns

- Blind ours/theirs, `reset --hard` or `clean -fd` as routine troubleshooting.
- Replaying an interrupted external action before checking its outcome.
- Overstating what abort, branch deletion or a bare force-with-lease guarantees.
- Pushing when the user asked only for local conflict resolution.

## Done when

- The Git operation is resolved and the resulting graph and index are inspected.
- Intended behavior and unrelated local work are preserved, with relevant checks run.
- Any authorized remote change is confirmed against the actual remote ref.

Resume `flow-work` or `flow-ship` at the stage the user originally requested.
