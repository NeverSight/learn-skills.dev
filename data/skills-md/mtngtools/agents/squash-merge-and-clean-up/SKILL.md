---
name: squash-merge-and-clean-up
description: Squash-merge this session's PR, then remove the branches and worktree it created.
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [prs, github, branching, git, worktrees]
---

# squash-merge-and-clean-up

> **human-only.** Start this only when a human asks for it by name. If you arrived here from another skill, stop and get explicit confirmation before running any step.

Land the PR this session opened and clear what this session created: leave the worktree, squash-merge, delete both branches, remove the worktree.

**Session-scoped throughout.** Other agent sessions run concurrently in the same repo and their worktrees and branches sit in the same listings. Touch only what **this** session made — the worktree it entered, the branch it pushed, the PR it opened. Everything else is someone's work in progress.

**Two gates, split on ownership.** Gate one covers everything this session owns: the merge and the removal of its own worktree and branches. Gate two covers the one step that touches **shared** state — bringing the primary checkout current, which every other session reads.

## 1. Survey

Gather, and hold for the plan:

- `gh pr view <n> --json number,title,body,state,mergeable,mergeStateStatus,headRefName,baseRefName,closingIssuesReferences`
- `gh pr checks <n>` — a docs-only PR may report no checks, which is a pass, not a failure
- `git worktree list` — note which entries this session created; `locked` marks another session's
- `git branch -vv` — the `+` prefix marks a branch checked out in some worktree

**Amend the PR body before you plan, not after.** The merge is what closes the linked issues, so a missing keyword means they outlive it and someone closes them by hand later. If this PR is meant to close issues and `closingIssuesReferences` is empty — or misses one — add `Closes #{issue}`, one line per issue, with `gh pr edit <n> --body`, keeping the body that is already there and appending. Take the issue numbers from the branch name, the commits, or the body's own prose; **do not guess a number**, and do not link an issue this branch does not actually close. If nothing here closes an issue, that is a normal PR — change nothing. Re-read the body after editing and say in the plan which issues the merge will close.

## 2. Gate one: print the plan, then ask

**The plan travels by two routes, because each alone fails.** Text printed just before a tool call may never render — the harness can swallow it, so the question arrives with no plan above it. And the question field itself renders as one plain paragraph with no list formatting, so a plan inlined there arrives unreadable — exactly when the human most needs to read it carefully. So: print the plan as ordinary output, where it lands in the transcript, **and** carry the same plan as each option's `preview`, which the question UI renders beside the choices. Whichever route the harness honors, the plan is on screen when the question is.

Output the plan for steps 3 to 5 as a numbered list under a `PLAN:` heading, naming the **actual** PR number, branch name, and worktree path — never a placeholder:

```markdown
PLAN:
1. Exit the worktree at `<path>`, returning to the primary checkout
2. Squash-merge <PR title> (#<n>) into `<base>` as `<commit subject>`, closing #<issue>
3. Confirm from the API that it merged, and that the branch's content landed
4. Remove the worktree at `<path>`
5. Delete `<branch>` locally and on origin
```

The closing clause on line 2 names every issue the body links, and is dropped entirely when it links none.

Then ask with `AskUserQuestion`, one question, this wording:

> Execute the squash merge plan shown in the preview?

Options are **Yes, run it**, **No, stop here**, and **Don't see the plan. Output it again.** Give **every** option the full `PLAN:` list as its `preview`, **copied verbatim from the output above — never retyped, shortened, or summarized**: one text, two routes, so the copies cannot disagree. Beyond the previews, nothing from the plan goes in the question text, the option labels, or the option descriptions — a second, shorter copy is what makes the two disagree.

On **Don't see the plan**, neither route rendered: print the full `PLAN:` list again and **end the turn there**, with the plan as the final message and no tool call after it — the one spot the harness always renders. Ask the same question again only after the human responds. Proceed only on yes.

## 3. Leave the worktree first

Exit the worktree **before** merging, and return the session to the primary checkout.

**This ordering is the whole point of the step.** `gh pr merge` run from inside a worktree merges server-side and *then* fails locally with `fatal: '<base>' is already used by worktree at …`, because its local step tries to check out the base branch that the primary checkout holds. It exits non-zero on a merge that succeeded, and `--delete-branch` never runs. Retrying reads as the obvious fix and is wrong — the PR is already merged.

Leave by moving your working directory back to the primary checkout — by whatever mechanism your harness provides — and **keep the worktree on disk**: it is removed in step 5, once its content is confirmed landed, and not a moment before. If your harness has no way to move, run the merge with an explicit path (`git -C <primary-checkout> …`, and `gh -R <owner/name>`) rather than from inside the worktree. **If you are Claude Code**, that is `ExitWorktree` with `action: "keep"`.

## 4. Squash-merge, then verify

```
gh pr merge <n> --squash --subject "<type>(<scope>): <subject> (#<issue>) (#<pr>)"
```

The subject follows the repo's convention: the conventional-commit subject, the issue number, then the PR number.

**Confirm from the API, not the exit code:**

```
gh pr view <n> --json state,mergedAt,mergeCommit
```

`state: MERGED` with a `mergeCommit.oid` is the completion criterion. When it says merged, the merge is done however the command exited.

## 5. Remove what this session created

Explicit, in order, each with its precondition:

1. **Confirm nothing is lost** — `git fetch origin --prune`, then `git diff --stat <worktree-HEAD> origin/<base>`. An empty diff proves the squash carried the content. The local commit is discarded by removal, so check before removing, not after.
2. **Remove the worktree** — `git worktree remove <path>`, then `git worktree prune`. Skip any entry marked `locked` or that this session did not create. A worktree with populated submodules refuses a plain remove even when clean: confirm `git -C <path> status` shows nothing modified inside the submodules, then remove with `--force`.
3. **Delete the local branch** — `git branch -D <branch>`. Step 2 is what frees it: a branch checked out in a worktree cannot be deleted.
4. **Delete the remote branch** — `git push origin --delete <branch>`. By hand, because `--delete-branch` on the merge often will not have run.

## 6. Gate two: bring the primary checkout current

Everything above touched only this session's own state. This step moves the checkout **every concurrent session shares**, so it is asked separately even after a yes at gate one.

Same shape as gate one, including both routes: the plan printed as ordinary output **and** carried verbatim as every option's `preview`. Print what the checkout looks like right now — the branch it is on, whether it is clean, how far behind `origin/<base>`, and anything uncommitted that the move would have to work around.

**Submodules: stale is not dirty.** In a repo with submodules, an ` M <submodule>` in `git status` carries two different meanings, and the plan must say which. `git submodule status` splits them: a `+` prefix means the checkout sits at a different commit than the branch records — a **stale pointer**, left behind because moving a branch never moves the submodule checkouts — while modified or untracked files inside (`git -C <submodule> status`) mean real work. A stale pointer is the checkout being behind, so syncing it belongs in this step's plan. Real work inside a submodule belongs to another session or the human: name it, leave it, and leave that submodule out of the sync.

```markdown
PLAN:
- Primary checkout is on `<branch>`, <clean | N uncommitted files>, <N> behind `origin/<base>`
- Fast-forward it to `origin/<base>` (`<sha>`) with `git merge --ff-only`
- Sync stale submodule checkouts to the recorded pointers with `git submodule update --init`
```

The sync line appears only when the repo has submodules, and it is what makes the step complete there: a fast-forward updates the pointers the branch records and leaves every submodule checkout where it was, so a checkout is current only once both have run. Sync per-path (`git submodule update --init -- <path>`) when one submodule must be left alone.

Then ask, one question:

> Bring the primary checkout current as shown in the preview?

Options are **Yes, run it** and **No, leave it**, each carrying the full `PLAN:` list as its `preview`. On yes, `git merge --ff-only origin/<base>` — only when the checkout is clean (stale submodule pointers count as clean) and `0` ahead — then the submodule sync from the plan. A **no** is a clean finish, not a failure.

Close by reporting what was removed and anything left standing. An untracked file you did not write, or a `locked` worktree, belongs to another session or the human: name it and leave it.
