---
name: treehouse
description: Lease, list, return and destroy git worktrees with `treehouse`'s pre-warmed pool. Use when the project's worktree tool is `treehouse`, or when another skill says to make or remove a worktree with it.
---

# Treehouse

`treehouse` keeps a pool of pre-warmed git worktrees, with dependencies already installed. Lease worktrees autonomously for an authorized task. Return an empty worktree to the pool rather than destroying it, so the next effort finds one ready; destroy only one the pool shouldn't keep. Settlement keeps the calling session's occupied worktree leased and leaves its session host's topology open.

1. Check the installed version and help for the operation. For a new effort, use `get --lease --json --lease-holder <effort> -b <branch>` and save the returned `path`, `lease_id` and `lease_holder`. Resolve the path physically and verify its repository and branch before using it. Use the returned identity for later release; a holder label alone can be reused.
2. Before releasing a worktree, verify its exact canonical path, repository, branch and current lease against that recorded acquisition. Confirm the worktree is clean, preserve any needed ignored files, and prove the branch merged using the invoking workflow's merge proofs. If the original acquisition has no recorded identity, verify ownership before recording the current lease; a current pool listing alone does not authorize adopting someone else's lease.
3. Check occupants immediately before release, using `treehouse status --json` together with live caller, pane and OS process inspection. Verify actual current directories for agents, idle sessions, shells, services and their children, including descendants of the worktree path. Workspace checkout metadata, titles and conversation context do not prove process location. Resolve symlinks and compare path components, so a similarly prefixed sibling does not match. Independently check the caller and its ancestors: Treehouse filters them from its reported process list. A service or session known to use the worktree also counts as an occupant even if its current directory is elsewhere.
   - **When occupied or uncertain:** Preserve the lease and branch, and report the occupants or missing evidence. This includes the calling session, a missing lease ID, unreadable relevant process locations, recovered or damaged entries, and changed identities. `status` silently omits processes whose directories it cannot read; an empty process list alone is not proof that the worktree is empty. Keep topology open and do not schedule delayed cleanup or terminate occupants to make settlement possible.
4. From outside the target worktree, return only the verified empty target with `treehouse return <exact-path> --if-lease-id <recorded-id> --if-lease-holder <recorded-holder>`. Recheck identity and occupancy after any intervening work. The flags atomically guard the lease before detach, process termination and reset; they do not guard occupancy or terminal topology. Use a single explicit target, since `return --all` can reclaim occupied slots.
5. Check the command's exit status and inspect the resulting pool and Git state. Delete its branch only after confirmed successful release and the invoking workflow's merge proofs bound to the verified branch tip, and after verifying no worktree still checks out that branch. Recheck the tip before deletion and repeat the merge proofs if it changed. A failed, interrupted or uncertain return may have changed state: preserve the branch, inspect live state before any retry, and use the original lease identity again only if it still matches. An already available or reassigned slot is not a reason to retry return.

| Need | Command | Notes |
|---|---|---|
| A durable worktree for an effort | `treehouse get --lease --json --lease-holder <effort> -b <branch>` | Returns the path and lease identity. A leased worktree is never handed out again or pruned until returned. |
| See the pool | `treehouse status --json` | Reports leases and processes it would terminate; independently verify caller and relevant unreadable process locations. |
| Give an empty worktree back | `treehouse return <path> --if-lease-id <id> --if-lease-holder <holder>` | Terminates processes with a current directory in the worktree, excluding the return process and its ancestors. An external shell can therefore terminate the calling agent. Dirty cleanup declined or unanswered exits 3 and preserves the lease; other failures can occur after detach or termination. |
| Preview removal for good | `treehouse destroy <exact-path>` | Dry run. `--yes` executes removal; `--include-leased` permits a named leased target. Destroy has no lease-identity guard: preserve a leased target unless exclusive ownership can be established through execution. Reapply the release checks before removal. |

## A worktree on a new branch

A leased worktree starts on a detached HEAD unless `get` makes its branch. `get --lease` fetches origin first and cuts the worktree from the remote default branch, and `-b <branch>` creates the effort's branch there with no upstream, so a bare `git push` can't push to the default branch before the first `git push -u`. `-b` fails if the branch already exists.

## Gotchas

- `return` keeps ignored files, even with `--force`, and the next effort that leases the worktree finds them, such as an old `.scratch/` or build output. Copy out what's worth keeping before returning. Use ordinary guarded return for settlement; `--force` discards changes without confirmation and does not make an occupied worktree safe.
- `destroy` removes everything in the worktree, ignored files included, without warning. Copy out anything worth keeping first.
- `destroy --include-in-use` terminates processes and `--include-unlanded` permits discarding work. Settlement preserves those targets; these flags do not establish permission to terminate a session or service.
- These facts were checked against `treehouse` v3.1.0 help and [kunchenguid/treehouse at c099281010efda0bf82bbaf8d882528fcbed6acc](https://github.com/kunchenguid/treehouse/tree/c099281010efda0bf82bbaf8d882528fcbed6acc), including its isolated release and process fixtures. Check them again after an update. Lease guards do not make the separate occupancy check atomic; if safe ownership through execution cannot be established, preserve the target.
