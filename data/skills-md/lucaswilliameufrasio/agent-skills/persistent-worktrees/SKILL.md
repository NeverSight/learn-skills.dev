---
name: persistent-worktrees
description: >-
  Choose and manage persistent locations for Git worktrees, alternate checkouts,
  build/test workspaces, and agent-managed workspaces. Use before creating or
  selecting any separate workspace, including during parallel coding, testing,
  or Git delivery. Default to `~/git-worktrees`; never put a repository checkout
  or persistent workspace under `/tmp`, `/var/tmp`, `$TMPDIR`, `/dev/shm`, or
  another temporary or RAM-backed filesystem.
---

# Persistent worktrees and workspaces

Keep full checkouts and long-lived task workspaces on persistent storage. On
many systems `/tmp` is RAM-backed or routinely cleared; repositories,
dependencies, and build outputs there can consume memory or disappear on
cleanup/reboot.

## Before creating a workspace

1. Prefer the current checkout when isolation is not needed. Do not create a
   second checkout just because a tool offers one.
2. If isolation is needed, use `~/git-worktrees/<repo>/<purpose>` by default,
   for example `~/git-worktrees/payments-api/review-webhook`.
3. Apply this rule to Git worktrees, cloned checkouts, agent/subagent workspaces,
   and build/test directories that hold a checkout or large artifacts. Do not
   place them under `/tmp`, `/var/tmp`, `$TMPDIR`, `/dev/shm`, `/run`, tmpfs,
   ramfs, or another ephemeral/RAM-backed location. Do not use `mktemp` for a
   repository checkout or persistent workspace.
4. Verify the destination resolves to persistent storage before creating it.
   Check for symlinks into temporary paths and, when the mount is not known,
   inspect filesystem type and available space with read-only tools. A path
   named `~/git-worktrees` is only a default, not proof that its backing mount
   is persistent or has enough capacity.
5. If that location is unavailable, on tmpfs, or low on space, do not silently
   fall back to `/tmp`. Reuse an existing safe checkout or ask the user which
   persistent location to use.

## Tool-managed worktrees

Before calling a tool that creates a worktree or workspace, determine its actual
destination **before creation** and whether it can be set to the persistent
path. Never invoke a creator whose destination is hidden, unknown, or
unconfigurable: checking the returned path afterward is too late, because the
checkout may already have consumed temporary or RAM-backed storage. If the tool
does not expose and honor an explicit safe destination, use an explicit-path
mechanism such as `git worktree add` or ask the user. Do not move an
accidentally-created temporary worktree and consider that compliant.

For a shell example, replace these example values with the actual repo, purpose,
and existing branch after checking the destination and following the current
host's shell preflight:

```sh
repo="payments-api"
purpose="review-webhook"
branch="feature/review-webhook"
mkdir -p "$HOME/git-worktrees/$repo"
git worktree add "$HOME/git-worktrees/$repo/$purpose" "$branch"
```

Avoid multiplying large dependency and build directories across worktrees.
Reuse package-manager caches or existing dependencies only when safe for the
project and branch; do not symlink mutable project state blindly.

## Cleanup and reporting

- Reuse existing worktrees where appropriate; never overwrite or remove a
  worktree you did not create.
- Before removing one you created, verify its exact path, Git worktree
  registration, and status. Preserve modified or untracked work; never use a
  forced removal or broad recursive delete as routine cleanup.
- Report the chosen persistent path and any space/tooling limitation. Small,
  disposable files may use an approved scratch directory; this exception does
  not apply to checkouts, worktrees, dependency trees, or build workspaces.
