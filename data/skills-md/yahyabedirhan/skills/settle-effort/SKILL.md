---
name: settle-effort
description: Settle an effort once its pull request is approved - merge it, run the post-merge follow-ups, carry unfinished work into next-effort tickets, close the spec and tickets, then settle the session. Use when the user says to settle the effort, or when another skill says to.
argument-hint: "The pull request (optional: defaults to the current branch's)"
---

# Settle Effort

Approving the pull request is the user's last step. Everything after it is yours.

## Flow

1. **Find the effort:** the pull request, its branch, spec, tickets and handoff, and every worktree and branch the build left behind, delegates' leftovers included.
   - **From a checkout that isn't on the effort's branch:** list pull requests by head branch with `gh pr list --head` and `--state all`, since without `--state all` a merged pull request doesn't show.
2. **Merge** the pull request once its checks pass, and check that the default branch's CI passes after the merge. Merge with `gh pr merge` and the project's usual method, and leave out `--delete-branch`: it deletes branches before they are proven merged, and switches the current checkout to the default branch.
   - **When the pull request is stacked,** with another pull request's branch as its base: merge it after its base pull request, and retarget it to the default branch with `gh pr edit --base` before the base branch is deleted, since deleting the base branch closes it for good.
   - **When the session has the session-status tool:** before merging, raise its open `before_settling` and `blocked` decisions as `/settle-session`'s "Nothing undecided" step says, since an answer can change the merge.
   - **When the spec says "QA: blocking":** merge only once every QA ticket is closed. Until then, tell the user which ones are still open and stop the settle there; it resumes once they're closed.
   - **When the default branch's CI fails after the merge:** stop before step 5, tell the user what failed, and file or fix it as they decide.
   - **After a squash or a rebase:** check that anything pinned to one of the branch's commits, such as an image URL with a commit SHA, still resolves, since the default branch doesn't hold those commits.
   - **When the pull request is already merged:** skip the merge, and still check the default branch's CI and, after a squash or a rebase, the pinned commits.
3. **Read the pull request's description and the handoff** for what the delivery left open: follow-ups, checks it skipped and decisions for the user.
4. **Run every follow-up and skipped check from step 3,** such as installing what changed or trying what could only be tried after the merge, and note each result for the report.
5. **Carry unfinished work over** as tickets in the next effort, labelled for it and linked back to where each came from. `gh issue create --label` fails when the label doesn't exist yet, so create a missing `effort:` label first with `gh label create`. Then close the spec and every ticket the merge finished, by hand for any a "closes" keyword missed.
   - **When it isn't clear which effort is next:** ask the user.
   - **For QA tickets:** leave them open for the user, with a comment on how to reach the build.
6. **Settle the session** with `/settle-session`, naming every worktree and branch from step 1 for cleanup assessment. Keep the caller and terminal topology open; release only the proven-merged, unoccupied worktrees that qualify under `/settle-session`. Have its report also say what merged, what closed, what carried over and what each follow-up from step 4 showed.
