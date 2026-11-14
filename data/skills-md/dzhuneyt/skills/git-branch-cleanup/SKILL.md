---
name: git-branch-cleanup
description: Use when stale git branches pile up after pull requests merge — local branches marked [gone], squash-merged branches that `git branch --merged` does not list, or leftover remote branches in a repo without auto-delete. Also use when the user names branches to purge, or asks to clean up, prune, or purge branches.
allowed-tools: [Bash, AskUserQuestion]
---

# Purge stale git branches

Delete branches that are already merged. Protect every branch that still holds work.

A squash merge rewrites the commits. After a squash merge, `git branch --merged` does not
list the branch, and `git branch -d` refuses to delete it. Both tools are therefore unsafe
signals here. This skill asks GitHub what the pull request merged, then compares that commit
to the local branch tip.

## When to use

Use this skill when any of these are true:

- Merged pull requests left local branches behind.
- `git branch -vv` marks branches with `[gone]`.
- The repository has no auto-delete setting, and merged remote branches remain.
- The user names one or more branches to purge.

Do not use this skill to delete a branch with work that is not merged. Do not use it to
abandon an open pull request.

## Arguments

`$ARGUMENTS` holds an optional list of branch names.

- If the list is empty, scan the whole repository and propose candidates.
- If the list has names, evaluate only those names. Run every safety check without change. A
  named branch gets no softer treatment than a discovered one.

## Step 1: preflight

Run these commands first. Stop if the first command fails.

```bash
git rev-parse --git-dir                                   # not a repo -> stop
git symbolic-ref --quiet --short refs/remotes/origin/HEAD  # -> origin/main
git fetch --prune                                          # every later check needs this
git worktree list --porcelain                              # branches checked out elsewhere
git remote get-url origin
gh auth status
```

Find the default branch. Never assume the name `main` or `master`. If `git symbolic-ref`
gives no answer, run `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`. If
both fail, ask the user.

The `gh` result and the origin host together set the mode. GitHub origin plus valid `gh`
authentication gives full mode. Anything else gives degraded mode (see Degraded mode).

## Step 2: list the branches

```bash
git for-each-ref refs/heads \
  --format='%(refname:short)%09%(upstream:short)%09%(upstream:track)%09%(objectname:short)%09%(committerdate:relative)'
git for-each-ref refs/remotes/origin \
  --format='%(refname:short)%09%(objectname:short)%09%(committerdate:relative)'
```

`%(upstream:track)` prints `[gone]` when the remote branch no longer exists. This is the
cheapest signal for a merged-and-deleted pull request. It costs no API call.

## Step 3: find the merge state of each branch

Apply these tests in order. Stop at the first one that answers.

1. `git merge-base --is-ancestor <branch> origin/<default>` — exit 0 means a true merge or a
   fast-forward. No network needed.
2. `gh pr list --head <branch> --state all --limit 5 --json number,state,url,mergedAt,headRefOid`
   - state `MERGED` — the branch is merged. This is the squash case.
   - state `OPEN` — protect the branch. Never delete it.
   - state `CLOSED` with no `mergedAt` — the work is abandoned. See the `abandoned` bucket.
   - no pull request — go to test 3.
3. Compare the merge result to the default branch. Run this test in degraded mode, and also
   in full mode when test 2 finds no pull request.

   ```bash
   git merge-tree --write-tree origin/<default> <branch>   # prints a tree sha
   git rev-parse origin/<default>^{tree}
   ```

   Equal trees mean the branch adds nothing. The branch is merged. A non-zero exit means a
   conflict, so the branch is not merged.

   This test reads content, not history. A branch whose changes reached the default branch by
   another route also gives equal trees. The result is still safe: equal trees mean the branch
   holds no content that the default branch lacks.

Never use `git cherry` or `git branch --merged` for this test. Both compare commits, and a
squash merge rewrites the commits. Both report a fully merged branch as unmerged.
`git merge-tree` compares content, so the squash does not hide the merge.

`git merge-tree --write-tree` needs git 2.38 or later. On an older git, ask the user before
you delete anything.

## Step 4: find the commits that arrive after the merge

A squash merge makes every branch commit look absent from the default branch. Therefore
`git log origin/<default>..<branch>` cannot separate merged work from new work. Ask GitHub
for the commit that the pull request actually merged, then compare:

```bash
git cat-file -e <headRefOid>^{commit}   # the sha must exist locally
git log --oneline <headRefOid>..<branch>
git diff --stat <headRefOid>..<branch>
```

No output means the branch adds nothing new. The branch is safe to delete.
Output means the branch holds work that the pull request never took. Block the branch.

If `git cat-file` fails, run `git fetch origin <headRefOid>`. If that also fails, use the
degraded check below.

In degraded mode there is no `headRefOid`. Use the merge result instead:

```bash
git diff --stat origin/<default> $(git merge-tree --write-tree origin/<default> <branch>)
```

This prints the content that the branch adds and the default branch does not have. Empty
output means the branch is safe to delete. Any output is unmerged work, so block the branch.
This test reports files, not commits, so name the files and not the shas in the report.

## Step 5: sort every branch into one bucket

| Bucket | Condition | Action |
| --- | --- | --- |
| `local-merged` | merged, tip equals `headRefOid`, not current, not default, not in a worktree | one batch confirm, then delete |
| `remote-merged` | `origin/<x>` merged, and no local branch holds work on top of it | one batch confirm, then delete |
| `orphan-work` | merged, but commits exist after `headRefOid` | blocked |
| `open-pr` | the pull request is still open | blocked |
| `worktree` | checked out in another worktree | blocked |
| `system` | the default branch, or the current branch | blocked |
| `abandoned` | the pull request closed without a merge | separate question |
| `stranded` | never pushed, no upstream, no pull request | report only, never delete |
| `unknown` | has an upstream, not merged, no pull request | report only |

Blocked branches get no delete prompt. Report them and continue.

## Step 6: report, then delete

Show the full report first, before any prompt. Expand each `orphan-work` row with the commit
sha, the subject, the age, and the diffstat. Give every other row one line.

Then run the prompts in this order.

1. One batch confirm for all `local-merged` branches.
2. One batch confirm for all `remote-merged` branches.
3. One separate question for the `abandoned` bucket. Show the pull request URL and the close
   date. Never merge this question into step 1 or step 2.

Read the sha of each branch before you delete it. Then delete:

```bash
git branch -D <branch>              # -d refuses squash-merged branches
git push origin --delete <branch>
```

`git branch -D` skips the merge check of git. The safety comes from Step 3 and Step 4
instead. Never call `-D` on a branch that those steps did not clear.

## Step 7: print the undo receipt

Print restore commands after each batch, before the next prompt:

```bash
git branch feat/login-fix a3f9c21
git push origin 8b1e044:refs/heads/feat/export
```

The reflog expires. A printed sha does not. A remote restore needs the object in the local
repository. Warn the user when the object is absent.

## Degraded mode

Degraded mode starts when `gh` is absent, the network is down, or the origin is not GitHub.
Report this once, at the top of the run. Then:

- Squash detection falls back to `git merge-tree`. The result is exact for content.
- The `orphan-work` report names files, not commits.
- The `abandoned` bucket is unavailable. A closed pull request looks the same as no pull
  request, so those branches land in `unknown` and stay.
- Every candidate needs its own confirm. No batch confirm.

One case stays invisible in degraded mode. If the merged work was later reverted on the
default branch, `git merge-tree` reports the branch as unmerged. Report the branch. Never
delete it.

## Failures

One branch that fails does not stop the run. Log the failure and continue. The summary lists
the branches that succeeded, failed, and were skipped.

## Red flags — stop

- `git branch --merged` used as the merge signal. It misses every squash merge.
- `git cherry` used as the merge signal. It misses every squash merge for the same reason.
- `git log <default>..<branch>` used as the orphan-work signal. It reports merged work as new.
- `git branch -D` on a branch that Step 3 did not clear.
- A delete before the report.
- A `stranded` branch offered for deletion.
- The default branch name assumed instead of detected.

## Common mistakes

| Mistake | Correction |
| --- | --- |
| Skip `git fetch --prune` | Every merge check reads stale refs. Run it first. |
| Treat a named branch as pre-approved | Names narrow the scan. They do not skip the checks. |
| Delete a remote branch with the local counterpart still ahead | The local branch holds the only copy of that work. |
| Fold `abandoned` into the merged batch | Closed work and merged work need separate decisions. |
| Print the receipt after the last batch only | Print it after each batch. A later failure must not hide it. |
