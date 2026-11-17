---
name: submit-issue-work
description: Submit completed OneDev issue work by pushing code, updating or opening its pull request, and posting issue comments.
---

# Submit work on a OneDev issue

Use configured `tod` in a checkout of the issue's project. Use the reference
supplied by the prompt or session, or run `tod issue current-reference`. If
the reference cannot be resolved, report the error and stop.

Take issue comments from the prompt or `<saved-issue-comments>` in the session.
Keep their exact text and order. Omit blank drafts. For comments-only work,
an explicit no-code handoff, or a detached HEAD, go straight to **Post
comments** and leave the checkout as it is.

## Verify the branch and choose the PR

Read `tod issue get <issue>` to find the server issue branch. Check
`tod project current`, `tod remote`, and `git symbolic-ref --short HEAD`.
Require the issue project, its issue branch, and upstream
`<remote>/<issue-branch>` (check with
`git rev-parse --abbrev-ref @{upstream}`). Stop if the branch is absent or
anything differs. Fetch with
`git fetch --no-recurse-submodules <remote> <issue-branch>`.

Find open PRs with `tod pr list --query 'includes issue "<issue>" and open'`.

- For one result, read `tod pr get <pr>` and verify its source project and
  branch match the checkout. Record its reference, URL, and target.
- For no results, plan a PR unless the prompt opts out. Use target project and
  branch from the prompt, then `defaultPullRequestTargetProject` and
  `defaultPullRequestTargetBranch` from the issue. Stop if either is missing.
- For multiple results, use the blocker procedure below to request a choice.

## Commit and push

Inspect the worktree and commit retrieved, changed submodules deepest first.
For each submodule, inspect its diff, verify its default branch and upstream,
and use `tod get-commit-message-requirement` to write the commit message.
Commit its changes, check that it is clean, and push outstanding commits
before committing its gitlink in the parent. On non-fast-forward only, use
`git pull --no-rebase --no-recurse-submodules <upstream-remote> <upstream-branch>`,
resolve conflicts, complete the merge commit, verify a clean worktree, and
retry the push once. Stop on other failures and avoid force-pushing.

Inspect the final parent diff. For a commit, satisfy every non-empty
requirement from `tod get-commit-message-requirement` and, if using a PR,
`tod pr get-commit-message-requirement --target-project <project> --target-branch <branch>`.
Write the message here. Stage and commit the completed changes and verify
`git status --porcelain` is empty. If there are outstanding commits and a
new PR is planned, read
`tod pr get-title-and-description-requirement --target-project <project> --target-branch <branch>`.
Before pushing, summarize the outstanding commits in the PR title and
description, following those requirements.

Push outstanding commits with `git push <remote> <issue-branch>`.
If the push updates an existing PR, use its recorded reference and URL.
After a successful push, create the planned PR with:

```bash
tod pr create '<title>' --description-file <description-file> --target-project <project> --target-branch <branch>
```

For an AI user, add a PR reference to the issue comments. Combine it with the
draft if there is exactly one, otherwise append it as a separate comment.
For a human user, report the PR reference and URL.

## Post comments

Post every saved comment in order after any code submission succeeds. If
code submission fails, stop before posting the saved comments. With no code
or comments, report that there is nothing to submit.

Use `tod issue add-comment <issue> --file <comment-file>` for each comment,
with the exact Markdown in a temporary file outside the checkout. For stdin,
use `--file -` with a quoted heredoc. Use OneDev references such as `PR #42`,
`issue team/app#7`, and `build APP-9`. Shell-quote titles and commit messages
so the shell preserves them literally.

## Restore the checkout after code submission

If `git rev-parse --abbrev-ref @{-1}` identifies a previous branch different
from the submitted branch, check it out and delete the local submitted branch
with `git branch -d`. Run `git submodule update --recursive` to restore
retrieved submodules, without initializing others. Verify a clean worktree.
If no previous branch can be identified, leave the current checkout in place.

## If blocked

Report the reason and any failing command or error. If the prompt identifies
you as an AI user and the issue reference is known, post a concise issue
comment explaining the blocker or needed decision, then stop without asking
for direction. For a human user, ask when a decision is needed.
