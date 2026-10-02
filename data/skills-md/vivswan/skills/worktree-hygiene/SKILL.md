---
name: worktree-hygiene
description: Use when creating, removing, or handing over git worktrees, retiring a branch after it landed, or when several actors share one repository through worktrees.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Worktree Hygiene

> A worktree is shared mutable state. Removal is destructive, a handover is an ownership transfer, and every worktree shares the main repository's `.git`. Each rule below guards against a destructive failure seen in production.

"An actor" below is anything that writes into a worktree: an agent, a subagent, a human session, a process one of them spawned.

## When to Apply

- Removing a git worktree, or retiring a branch after it landed (its worktree, its local ref, optionally its remote ref)
- Handing a worktree or branch from one actor to another, or resuming an actor that owns one
- Several actors (agents, sessions, scripts) share one repository or one worktree
- Checking out branches or writing `git config` while other worktrees exist

## Removing a Worktree

Verify all three before `git worktree remove`, freshly, in this order:

1. **Clean, by fresh status codes.** Run a fresh `git -C <tree> status --porcelain -uall` and read the STATUS CODES. Never trust a prior report's dirty count: counts cannot distinguish new files from removal-in-progress deletions, and codes can. `-uall` overrides a `status.showUntrackedFiles=no` config that would silently hide untracked files.

   Every entry blocks the removal unless its exact path is positively identified as disposable. A removal-in-progress shows its own deletions as `D`, and a coordinating actor's keepalive marker (below) is a lone `??`. A `??`, `M`, or `D` entry not identified that way is real work.
   - A clean tree loses nothing TRACKED on removal. Its commits survive on their ref.
   - IGNORED files are invisible to plain status yet die with the tree. When a worktree may hold valuable ignored artifacts (a local database, captured data), list them first with `git -C <tree> status --porcelain -uall --ignored`. Keep `-uall` here too, since `--ignored` alone does not override a `status.showUntrackedFiles=no` config.
2. **On a durable ref.** A DETACHED worktree's unique commits can be reachable only through its private HEAD, which removal deletes, reflog included. `git -C <tree> symbolic-ref -q HEAD` exiting non-zero means detached. Put a branch or tag on `git -C <tree> rev-parse HEAD` before removing, or prove that commit reachable from a durable ref.
3. **No live writer.** Check for processes whose cwd is inside the worktree (`lsof -a -p <pid> -d cwd`, or `lsof +D <tree>`). An actor absent from the running list is not itself writing, but processes it spawned (test chains, installs) can still be. Kill them or wait them out first.

   Never remove a LOCKED tree (`git worktree list --porcelain` shows `locked` with its reason), or a tree another actor may be using, without knowing whose it is and why.

After removing:

- **Remove with `git worktree remove`, never a bare `rm -rf`.** Manual deletion leaves the worktree's administrative entry in the shared git dir. Git then keeps treating its branch as checked out, and blocks deleting it, until the entry is pruned.
  - `git worktree prune --expire now` clears stale entries immediately. A bare `prune` honors `gc.worktreePruneExpire` (three months by default), so it can leave a just-deleted tree's entry in place, its branch still blocked. Git eventually expires entries on its own too, but never count on that timing.
  - Anchor BEFORE pruning. A prune deletes each swept entry's private HEAD and reflog, and it sweeps EVERY missing unlocked tree in one pass, not just yours. `git worktree list --porcelain` marks each prunable entry and prints its recorded `HEAD` sha, so put a branch or tag on any detached one (rule 2) first.
- **Removal does not kill survivors.** A finished actor's wedged test chain can outlive its deleted directory for hours. Re-check and kill any process whose cwd names the deleted path.

### Deleting the branch too

Removing a tree that sits on a branch keeps that branch. Delete it only once its work is proven preserved on the mainline. `scripts/retire-branch.mts` (Retiring a Landed Branch, below) proves that and deletes in one gated run. Two rules bind regardless:

- **Never trust `git branch -d`.** It only tests merge into the branch's configured upstream (or into HEAD when none is set), and the usual upstream is the branch's own `origin/<topic>`, not your mainline. It can succeed on unlanded work and refuse on landed work, so neither verdict proves anything.
- **Delete a server-side ref only under a lease** pinned to the sha you verified, so a push landing between your verification and the delete is refused instead of destroyed:

  ```bash
  git push <remote> --force-with-lease=refs/heads/<topic>:<verified-sha> :refs/heads/<topic>
  ```

### Auto-removal can destroy a live workspace

Harnesses that auto-clean isolation worktrees remove them when their actor completes with a clean tree. An actor that stops "to wait" before anything is written, while others still work in its tree, leaves them working in a deleted directory.

- **Dirty the tree IMMEDIATELY on start** when an actor coordinates others inside its own isolation worktree. One untracked marker file at the worktree root is enough (e.g. `.orchestrator-keepalive`).

  Verify the marker actually shows as `??` in `git status --porcelain -uall`. Keep `-uall` here too, or a `status.showUntrackedFiles=no` config hides the very evidence this check needs. An ignore rule can hide it, and a hidden marker protects nothing, so pick another name when it does.

  The marker is never staged or committed (removal rule 1 names it the one disposable `??`), and it is deleted before the final signal or handoff.
- **Verify the worktree still exists** before resuming any actor that stopped clean in an isolation worktree. Respawn fresh when it does not.

## Retiring a Landed Branch

`scripts/retire-branch.mts` runs the retirement as one program, so the destructive step is unreachable from a failed gate. It fetches the mainline into a ref the run owns, proves the branch landed, enforces the removal rules above on the branch's worktree, removes it, and deletes the local ref pinned to the verified sha.

CI verdict first: `/watch-ci-after-push`. Then rehearse. Without `--execute` every gate runs and nothing is destroyed:

```bash
bun "<skill-dir>/scripts/retire-branch.mts" --branch feature/thing
```

```text
[fetch] origin/main -> 4f2a9c... (the remote-tracking ref was already current)
[branch] refs/heads/feature/thing is at 91bd0e...
[landed] by content equivalence at 7c31f0...: feature/thing matches 4f2a9c on all 3 path(s) it changed
[worktree] /repo/.worktrees/thing is clean and idle
[worktree] would remove /repo/.worktrees/thing (add --execute)
[delete] would delete refs/heads/feature/thing at 91bd0e... (add --execute)
REHEARSED: every gate passed for feature/thing; nothing was destroyed
```

Then for real:

```bash
bun "<skill-dir>/scripts/retire-branch.mts" --branch feature/thing --execute
```

| Exit | Meaning | What to do |
| --- | --- | --- |
| 0 | every gate passed (and every step ran, under `--execute`) | done |
| 1 | a gate REFUSED on the evidence: not landed, worktree holds work, the ref moved | read the refusal; it names what blocked |
| 2 | usage error | fix the invocation |
| 3 | BROKEN measurement: a ref that does not resolve, a git failure, a probe that could not run, a shallow clone | the question was never answered; never retry with the gate removed |

Flags:

```bash
--mainline develop --remote upstream --repo-root /path/to/repo
--original-tip 7c31f0e   # a branch rebased before landing: prove the OLD tip landed too
--no-writer-check        # a host where lsof cannot answer; the run says so out loud
```

A squash or rebase merge leaves the branch's shas off the mainline, so ancestry refuses. The script then settles the landing by content equivalence automatically and prints which gate cleared it: `[landed] by ancestry` or `[landed] by content equivalence at <base>`. Why each gate exists: `references/retire-branch.md`.

## Handing Over a Worktree

Ownership transfers explicitly, never by inference. At any moment a worktree has exactly one owner: a single actor, or a coordinating actor that has granted disjoint per-file territories inside it (File Ownership, below). A handover is a named event (a stop plus a grant), not a guess from silence.

- **Stop the predecessor first.** A message sent to a completed or idle agent RESUMES it. An acknowledgment or thank-you sent after a handover wakes the predecessor, which resumes writing into the worktree its successor now owns (a live-writer clobber). The order is always: stop the actor first (TaskStop in Claude Code), and any farewell after that is unnecessary.
- **A successor checks for a live writer** before editing. Check for processes with cwd inside the tree first (the same lsof check as removal rule 3), then hash a hot file, wait, hash again (`shasum <file>; sleep 5; shasum <file>`). These checks gather evidence, never proof: a writer can be idle between edits or writing a different file. The ownership invariant stays the explicit stop-and-grant above.
- **A removed tree's branch goes to whoever collects it.** Stopping an actor and removing its worktree transfers its branch to the collector, and only to the collector. Follow-up fixes on that branch go to a FRESH actor in a NEW worktree.
- **Never resurrect a released actor.** A message to a stopped actor resumes it into a directory that no longer exists. Once its worktree is removed, that actor is never messaged again.

## File Ownership Across Parallel Actors

When several actors write into ONE worktree, or several rounds of actors work the same file set:

- **Every file has exactly one owner across ALL rounds.** Give each actor an explicit file whitelist.
- **A later round's list is computed by SUBTRACTING** everything any earlier round covered, by file list, not by "looks done".
- **No round starts while a prior round's actor may still be writing.**

Re-assigning files a prior round still owns produces racing-writer collisions and duplicated work even when exact-match edit semantics prevent outright corruption.

## One Branch, One Worktree

Git refuses, by default, to check out a branch that is already checked out in ANY worktree ("already used by worktree"). So a branch is held by at most one tree, and the holder must release it before anyone else can take it:

```bash
git -C <holding-tree> checkout --detach   # or check out another branch there,
                                          # or remove the worktree (rules above)
git checkout <branch>                     # only now succeeds elsewhere
```

The refusal is a guard, not a lock: `git worktree add --force` and `git checkout --ignore-other-worktrees` override it. Never use them to take a branch a live tree holds. Two checkouts of one branch means two writers of one ref.

Plan around the guard rather than fighting it. Operations that need a branch checked out (rebase, merge, stack tooling) run only after the tree holding that branch is released or removed, never while its owner is live.

## Worktrees Share the Main Repository's .git

Every linked worktree keeps a small private git dir (HEAD, index, in-progress rebase or bisect state, `refs/worktree/*`). It shares everything else through the main repository's git dir (`$GIT_COMMON_DIR`): one config, one remote list, one hook set, one store for branches and tags. Consequences for concurrent actors:

- **`git config` writes are repository-wide.** An actor enabling `rerere`, setting `remote.pushDefault`, or rewriting `branch.<name>.*` sections changes behavior in every sibling worktree at once, mid-run. Per-worktree config exists only when `extensions.worktreeConfig` is enabled and the write targets `config.worktree`. Without that, every write is shared.
- **Identity is shared.** A `user.email` or `user.name` write in one tree stamps every sibling's next commit. Set identity per command (`git -c user.email=...`) or in environment variables scoped to the actor, never in the shared config while others run.
- **Branches and tags are shared.** A branch update or deletion or a tag move performed in one tree is instantly visible in all. A sibling about to start a rebase or merge onto a ref you just deleted errors in ways it cannot diagnose, so coordinate ref surgery, or schedule it when no sibling is live.

  The per-tree refs are the exception: HEAD, `FETCH_HEAD` and the other pseudo-refs, `refs/worktree/*`, `refs/bisect/*`, `refs/rewritten/*`.
- **Hooks are shared by default.** Installing or editing a hook from one worktree changes what every sibling's next commit runs. A per-worktree `core.hooksPath`, or a relative hooks path resolving per tree, is the exception. Absent that, assume shared.
