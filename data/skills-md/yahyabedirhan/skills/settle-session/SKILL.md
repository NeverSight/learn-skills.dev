---
name: settle-session
description: Settle a session by saving its work, recording what remains and freeing proven-merged, unoccupied worktrees while leaving the caller and terminal layout open. Use when the user says "settle" or "end the session" about this session, or when another skill says to settle. When the user says to settle an effort, use /settle-effort instead.
argument-hint: "Other branches and worktrees to consider for cleanup (optional)"
---

# Settle Session

A settled session saves its work and everything another agent needs in the issue tracker or the project's files. Leave the calling session available and its occupied worktree leased, even when its branch has merged.

Do every step yourself. Leave all terminal workspaces, tabs and panes open. An explicit request to close named topology can authorize that separate cleanup; settlement never implies closing linked or grouped topology.

## Parameters

- `<worktree-tool>`: the tool that makes and frees worktrees, e.g. `treehouse`, or plain git worktrees.
- `<session-host>`: where agent sessions run, e.g. `herdr`, Claude Code Desktop, Codex Desktop.

## Flow

Run each commit, push and deletion as its own call, so a refused one stops only itself.

1. **Take stock** of what this session touched: the checkouts and worktrees it worked in and their branches, the pull requests and issues it opened, the processes and agents it started, and the threads still open. Add any branches and worktrees the calling skill or the user names. Through `<session-host>`, resolve the live caller and its current hierarchy before identifying cleanup targets; report any mismatch with the handoff or inherited context. Use actual pane and process locations, since workspace checkout metadata alone does not establish them.
2. **Nothing running.** Stop the task processes this session started, such as dev servers, watchers, background commands and preview or browser tabs, unless the user wants one kept; name each one kept in the report. Immediately before stopping or interrupting work, verify the live caller, target identity, actual location, hierarchy and task ownership; keep and report an uncertain target. Wait for or interrupt unfinished work by agents this session started, leaving their sessions and terminal topology open. Preserve unrelated agents, shells and services.
3. **Nothing unsaid.** Write down what this session learned that lives only in its context: decisions and their reasons, surprises, checks it skipped, what comes next. Put each where an agent that never saw this session will look for it: the issue it belongs to, the pull request's description, or a handoff written with `/handoff`.
4. **Nothing undecided.** Give each leftover thread an outcome: finish it, file it as a ticket, or raise it with the user and record what they decide. Ask while the user is here, and settle only once each question has its answer.
   - **When the user can't be reached,** such as when a handoff says to decide alone: decide it yourself, and record the decision and its reason where step 3 puts what the session knows.
   - **When the session has the session-status tool:** call its `list` action with `filter: { kind: ["decision"], state: "open" }`, and raise each open `before_settling` and `blocked` decision here. Read the decisions only through the tool, since the mod owns its store file and may change its format.
5. **Nothing unsaved.** In each checkout this session worked in, commit and push everything, including the files steps 3 and 4 wrote, until `git status` is clean and the branch matches its remote. Set aside on purpose anything that doesn't belong in a commit, and name it in the report.
   - **In each worktree considered for release:** list the ignored and untracked files with `git status --ignored` and copy out what's worth keeping, where `/orchestrating`'s `folder-standard.md` puts each kind, since removing a worktree deletes them. Copy editor settings like `.vscode/` to the main checkout, keeping the main checkout's own copy of any file already there.
   - **After an interrupted or rejected commit or push:** check the log before retrying, because it may have landed anyway.
   - **When the changes sit on the default branch or in the user's main checkout:** commit only this session's own changes, on a new branch, and open its pull request with `/to-pr`. Leave the user's other changes where they are, and push nothing to the default branch.
   - **When the work's branch has already merged,** and settling changes tracked files, such as status changes or files copied out of a worktree: put the changes on a small follow-up branch and open its pull request with `/to-pr`. Leave the user's main checkout on its branch, since they may be working there, and pull in it only when it is clean and already on the default branch. Make the follow-up worktree with `<worktree-tool>` from the remote default branch, and keep it until it qualifies for release below.
6. **Nothing in the way.** Free only clean, proven-merged, unoccupied worktrees and their branches, and name each one kept with its reason and occupants. Keep the calling session's worktree and its local and remote branch, the main checkout and the default branch. Run `git fetch --prune` first, so the remote default branch is current. Three proofs count:
   - **Reachable:** `git merge-base --is-ancestor` with the branch and the remote default branch succeeds, as after a merge commit or a fast-forward. It is the cheapest, so try it first.
   - **Matched by patch:** `git cherry` with the remote default branch and the branch prints no `+` line, as after a rebase or an unchanged cherry-pick. A `+` proves nothing either way.
   - **In the merged pull request's head:** the hosting service shows the pull request merged, and the branch's tip is its head commit or an ancestor of it. A branch whose commit was integrated into the pull request's branch counts when the head contains that commit, or a commit carrying the same change as `git range-diff` or the diff shows, and the branch holds nothing else; when unsure, keep the branch. A squash merge, or a commit changed while it was integrated, fails the first two proofs; only this one proves it.

   Immediately before each release, refresh the live caller and target identities, repository, actual locations, hierarchy, branch tip and occupants through `<session-host>` and `<worktree-tool>`. Bind the merge proof to that tip; when it differs from the tip previously proven, prove the new tip or preserve the target. Check idle agents, shells and services as well as working agents; a tool's ability to terminate them does not make the worktree unoccupied. Preserve and report a target whose identity or occupancy is uncertain. For pooled worktrees, use the worktree tool's lease identity guards to prevent returning a reassigned lease.
   - **When `<worktree-tool>` is `treehouse`:** use `/treehouse` for its live occupancy checks, lease guards and release confirmation.

   Free worktrees with `<worktree-tool>`, without `--force`. Confirm that the intended worktree was released successfully before deleting either its local or remote branch; a failed, interrupted or uncertain release preserves both. Inspect current state before any retry, and never schedule delayed destructive cleanup. Immediately before branch deletion, compare its current tip with the recorded proven tip and re-prove any change; preserve it when the proof or exclusive ownership is uncertain. Delete a local branch with `git branch -d` after the reachable proof, and with `git branch -D` when only the other two prove it. Use `git branch -D` too when `-d` refuses a branch the reachable proof passed, since `-d` checks against the branch's upstream or `HEAD`, not the remote default branch. For a branch with no worktree, verify that it is not checked out or in use before applying the same merge proofs.
   - **When a freed branch has a remote branch:** delete it too once `git ls-remote --heads origin <branch>` shows it still exists and its tip is the local branch's tip or passes one of the proofs above; the repository may have deleted it on merge. Otherwise keep the remote branch and name it in the report. Before the deletion, retarget each open pull request whose base is that branch to the default branch on the hosting service, since deleting a base branch closes its stacked pull requests and a closed one can't be reopened against another base. When a retarget fails, keep the remote branch and name it in the report.
7. **Report** what was done, what was filed and where, what was kept and why, and what waits on the user. Include identity mismatches, preserved occupants and the caller's retained worktree and branch.
   - **When the session has the session-status tool:** put the decisions still open after step 4, such as the `after_settling` ones, in the report as one numbered list, each with its id, question, default and options. Then call the tool's `post_decide_list` action.
8. **End the report with a resume prompt:** one line the user pastes into a new session when they come back, so picking the work up needs no question to an agent. Name the worktree by its path, its branch, where the next session reads what remains (the handoff's path, or the issue or pull request that holds it), and the first thing to do; everything else stays there. Keep it to one line, because a pasted prompt of several lines arrives as pasted text and its skill never starts, and name skills in words rather than slash commands, so it works in every harness:

   ```text
   Continue in the worktree <path> on branch <branch>, from the handoff at <path>: <the first thing to do, in one sentence>.
   ```

   - **When nothing remains,** such as when every branch merged and nothing carried over: leave the prompt out, and say so in the report.
9. **Mark the session settled** through `<session-host>`, where the host labels sessions, after refreshing the current caller's live identity and hierarchy. The report, its resume prompt and the settled mark finish settlement; keep this session, its worktree and all terminal topology open.
