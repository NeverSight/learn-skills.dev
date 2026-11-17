---
name: submit-pull-request-work
description: Submit completed work on an existing OneDev pull request by pushing code and applying discussion, review, or merge actions.
---

# Submit work on a OneDev pull request

Use configured `tod` in a checkout of the source or target project. Use the
PR reference supplied by the prompt or session, or run `tod pr current-reference`.
If the reference cannot be resolved, report the error and stop.

Take PR actions from the prompt or `<saved-pr-actions>` in the session.
Preserve their order, exact text, and parameters. Omit blank text-only
actions and optional notes. For discussion-only, review-only, merge-only, or
no-code work, or a detached HEAD, go straight to **Apply PR actions** and
leave the checkout as it is.

## Verify the source branch

Read `tod pr get <pr>` for status, source and target projects and branches,
and PR reference and URL. Check `tod project current`, `tod remote`, and
`git symbolic-ref --short HEAD`. Require an open PR, its source project and
branch, and upstream `<remote>/<source-branch>` (check with
`git rev-parse --abbrev-ref @{upstream}`). Stop on a mismatch. Fetch with
`git fetch --no-recurse-submodules <remote> <source-branch>`.

## Commit and push

Inspect the worktree and commit retrieved, changed submodules deepest first.
For each submodule, inspect its diff, verify its default branch and upstream,
and use `tod get-commit-message-requirement` to write the commit message.
Commit its changes, check that it is clean, and push outstanding commits
before committing its gitlink in the parent. On non-fast-forward only, use
`git pull --no-rebase --no-recurse-submodules <upstream-remote> <upstream-branch>`,
resolve conflicts, complete the merge commit, verify a clean worktree, and
retry the push once. Stop on other failures and avoid force-pushing.

Inspect the final source diff. For a commit, satisfy every non-empty
requirement from `tod get-commit-message-requirement` and
`tod pr get-commit-message-requirement --target-project <project> --target-branch <branch>`.
Write the message here. Stage and commit the completed changes, including
any resolved merge in progress. Verify `git status --porcelain` is empty
and push with `git push <remote> <source-branch>`. Stop on failure.

## Apply PR actions

Apply saved actions in order after any code submission succeeds. If code
submission fails, stop before applying the saved actions. With no code or
actions, report that there is nothing to submit.

| Action | Command |
| --- | --- |
| General PR feedback | `tod pr add-comment <pr> --file <file>` |
| Line-anchored finding | `tod pr add-code-comment <pr> --file <file> --on-file <path> --from-line <line> [--to-line <line>]` |
| Code-thread reply | `tod code-comment add-reply <id> --file <file>` |
| Resolve or reopen a code thread | `tod code-comment resolve <id>` or `tod code-comment unresolve <id>`, with `--note-file <file>` when there is a note |
| Formal review outcome | `tod pr approve <pr>` or `tod pr request-changes <pr>`, with `--summary-file <file>` when there is a summary. Use the outcome for your pending review. |

OneDev posts a resolve or unresolve note as a reply. If saved actions repeat
the same explanation in a reply and a status change note for the same thread,
apply the status change with its note once. If you already posted the reply,
apply the status change without a note.

OneDev posts an approval or change-request summary as a PR comment. If saved
actions repeat the same feedback in a general comment and a review summary
for the same PR, submit the review with its summary once. If you already posted
the comment, submit the review without a summary.

Pass exact Markdown via temporary files outside the checkout. For stdin,
use a quoted heredoc with `--file -`, `--note-file -`, or `--summary-file -`.
Use OneDev references such as `PR #42`,
`issue team/app#7`, and `build APP-9`. Shell-quote commit messages so the
shell preserves them literally.

### Merge

Read `tod pr get <pr>` immediately before a merge. For an automatic merge,
require `status` to be `OPEN (ready to merge)`, confirm you are still an
assignee, and check that `headCommitHash` matches the reviewed head. Skip the
merge and report why if a check fails.

Use `tod pr merge <pr>`. For `SQUASH_SOURCE_BRANCH_COMMITS`, first read:

```bash
tod pr get-commit-message-requirement --target-project <project> --target-branch <branch>
tod issue list --query 'fixed in pull request "<pr>"'
```

Compose a compliant message from the PR and its fixed issues, then pass it
with `tod pr merge <pr> --commit-message '<message>'`.

## Restore the checkout after code submission

If `git rev-parse --abbrev-ref @{-1}` identifies a previous branch different
from the submitted branch, check it out and delete the local submitted branch
with `git branch -d`. Run `git submodule update --recursive` to restore
retrieved submodules, without initializing others. Verify a clean worktree.
If no previous branch can be identified, leave the current checkout in place.

## If blocked

Report the reason and any failing command or error. If the prompt identifies
you as an AI user and the PR reference is known, post a concise PR comment
explaining the blocker or needed decision, then stop without asking for
direction. For a human user, ask when a decision is needed.
