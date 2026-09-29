---
name: using-git-worktrees
description: "Use when the user requests branch or workspace isolation, or current-workspace interference requires it; not merely because implementation has parallel subagents."
---

# Using Git worktrees

## Overview

Create a worktree only when isolation materially reduces interference or branch risk. Worktrees are optional setup, not a default precondition for implementation.

## When to Use

- Large features or refactors that should stay off the current workspace
- Work that needs a clean branch or separate dependency state
- Parallel efforts that would otherwise interfere with the current directory

## When Not to Use

- Tiny edits or single-file changes that do not benefit from isolation
- Repositories where the current workspace is already the correct branch and state
- Parallelizable work whose write scopes can remain isolated without changing branch state

## Minimal Workflow

1. Inspect the current branch, worktrees, dirty state, and untracked work. Use isolation when it solves a current interference or branch-state problem; otherwise stay in the existing workspace.
2. Use Worktrunk (`wt`) for agent-created workspaces. Its user configuration owns the destination; inspect `wt config show` and `wt list` before choosing a new branch. Reuse an already isolated host- or app-created task workspace instead of creating another inside it.
3. Infer routine branch and base choices from the task and repo conventions. Repo guidance or project `wt` hooks own setup; run a documented repo bootstrap in the new workspace rather than recreating it by hand. An authorized task permits needed reversible isolation. Preserve existing branches, dirty files, and untracked work; do not switch, reset, clean, or overwrite them without authority.
4. Run `wt switch --create <branch> --base <base> --no-cd --format json` for noninteractive creation. Use the returned absolute `path` as the working directory in subsequent tool calls; a subprocess cannot change later tool calls' directories. For interactive shells, `wt switch --create <branch> --base <base>` switches directories through shell integration. Noninteractive runs stop on unapproved project hooks: review them (`wt config approvals list --format json`), then rerun with `--yes`, which approves that run only. Persistent `wt config approvals add` needs authority.
5. Pre-start hooks finish before `wt switch` returns; if setup runs in post-start, confirm it finished (`wt config state logs`) before relying on it. Verify selected env files are ignored and present without printing their contents. Keep mutable dependency trees and generated clients independent; check symlinks before copying them. Use the repo's dependency reconciliation command for the new branch's manifests/lockfile. Copying env files does not isolate databases or ports; configure those before running services or database writes.
6. Verify the relevant baseline and report branch, absolute location, and setup result. If setup or a baseline fails, retain the workspace and report the exact failure; do not claim the source also fails unless verified. Preserve current work and do not commit or publish setup changes without authorization.

## Authorized cleanup

Follow `finishing-a-development-branch` for the integration/cleanup decision. Before removal, check dirty and untracked work, ignored evidence/local data, unique commits, saved tasks, processes, and mounts. A merged PR or clean status alone does not prove disposability. Preserve required evidence first.

For an agent-owned workspace whose removal is authorized, run `wt remove <branch-or-path> --no-delete-branch --foreground` from a retained workspace, then verify the exact path and registration are gone. Keep branch deletion separate. Stop on dirty/locked state or active references; resolve ownership rather than forcing removal. Stop only processes known to belong to the task within existing authority; Worktrunk's experimental `--reap` is not a blanket cleanup default.

Host- or app-created workspaces retain their creator's cleanup ownership. Keep active existing paths stable.

## Reference Routing

- Read [references/worktrunk.md](references/worktrunk.md) when Worktrunk is missing, remote env/dependency setup is needed, or host or app workspace ownership is unclear.
- Use `engineering` as the next primary skill once the isolated workspace is ready and the real task becomes implementation.
- Use `finishing-a-development-branch` when the isolated branch is complete and needs an integration decision.

## Failure modes

- Treating worktrees as mandatory for trivial work
- Bypassing configured setup hooks or creating nested isolation
- Ignoring a repo bootstrap script and recreating setup by hand
- Assuming Worktrunk relocates existing trees or intercepts host or app workspace creation
- Overwriting existing work or committing setup changes without authority
- Using broken path expansion or stale runtime-specific paths
