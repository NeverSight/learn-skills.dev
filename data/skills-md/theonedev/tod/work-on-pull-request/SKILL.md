---
name: work-on-pull-request
description: Work on a OneDev pull request. Follow a specific request or infer review, feedback, maintenance, and merge work from the current PR and your roles.
---

# Work on a OneDev pull request

Use configured `tod` in a checkout of the source or target project. Use the
PR reference supplied by the prompt or session, or run `tod pr current-reference`.
If it cannot be resolved, report the error and stop.

## Inspect and choose work

| Context | Command |
| --- | --- |
| Status, head, branches, merge strategy, roles, reviews | `tod pr get <pr>` |
| Login and prior contributions | `tod get-login-name` |
| Discussion | `tod pr get-comments <pr>` and `tod pr get-code-comments <pr>` |
| Issues the PR fixes | `tod issue list --project <target-project> --query 'fixed in pull request "<pr>"'`, then `tod issue get` and `tod issue get-comments` for relevant results |

A code comment with a `commit` refers to that commit's lines. Use
`tod download <original-url> <output-file>` to inspect linked attachments
from the PR and its fixed issues. Save downloads outside the working tree.

Follow any specific request. If the request just names the PR, use its
current state, your roles, and outstanding discussion to choose work.
When the prompt supplies an event timestamp, check activity around and since it.

| Situation | Work |
| --- | --- |
| Your review on an open PR is `PENDING` | Review the current head and draft your formal outcome. |
| You submitted the open PR | Address outstanding review feedback. Use `statusDate`, summaries just before the status change, code threads, and later commits or replies to identify what still needs attention. Plan resolve/unresolve actions for code comments as appropriate. |
| PR discussion | Reply only when it concerns you and needs a response. |
| PR maintenance | As submitter or assignee of an open PR, use supplied `RESOLVE_MERGE_CONFLICTS` and `FIX_FAILED_BUILDS` responsibilities to select work. In manual work without supplied responsibilities, check `hasMergeConflicts` and current build failures. Resolve conflicts first when both apply. |
| `MERGE_IF_ACCEPTABLE` | As assignee, review a mergeable PR. Save a merge action if acceptable, or draft actionable feedback in a PR comment mentioning the submitter if changes are needed. |

Base conflict work on a calculated merge preview. For a closed PR, infer only
relevant discussion work.

## Review and discussion

Review with `tod pr get-patch <pr> --for-code-review`. Inspect relevant files at
the PR head when the patch needs context, using `git show <head>:<path>` and
fetching the head if needed. Use the fixed issues as the specification unless
the prompt provides one. Check correctness, edge cases, security, style, and
test coverage.

Save each line-specific finding as a code comment when the affected added
or context line is visible on the right side of the patch. Put findings
outside the patch in overall feedback with paths and line numbers where
possible.

For existing code threads you started as a reviewer, first assess whether
their resolution status should change. If so, save a resolve/unresolve action
with an explanatory note. If the status should stay the same, save a standalone
reply only when you have new information.

As a reviewer, do not reply to or modify code threads started by other users
unless asked to do so.

Draft approval or changes requested for your pending review, with overall
feedback in the review summary. OneDev posts the summary as a PR comment.
Use a standalone PR comment for informal reviews or separate discussion.
Save explicit merge requests and attach the reviewed `headCommitHash` to any
automatic merge action. If you edit the source in this run, defer review and
merge decisions until the updated head can be assessed.

## Code changes

Keep the current checkout for read-only work. Use
`tod pr checkout --for-write <pr>` when edits require the PR source branch.
Respect an explicit request to keep the current checkout.

### Conflicts

1. Fetch the target head with
   `git fetch --no-recurse-submodules <target-remote-or-url> <target-branch>`
   and record `git rev-parse FETCH_HEAD`.
2. For merge-commit strategies, run `git merge --no-commit <target-head>`.
   For `SQUASH_SOURCE_BRANCH_COMMITS`, use `git merge --squash <target-head>`.
   For `REBASE_SOURCE_BRANCH_COMMITS`, stop and seek direction before
   rewriting commits, following the blocker instructions below.
3. Resolve conflicts and confirm `git status --porcelain` has no unmerged
   entries. Run `git submodule update --recursive` to follow updated gitlinks.

### Failed builds

Handle PR build repairs within this workflow. Use the PR checkout guidance
above and include the fix and any feedback in the PR handoff below.

Use a specified build if given. Otherwise run `tod pr get-builds <pr>` and
inspect every current `FAILED` build. If none failed, continue with other work.
For each selected build, read `tod build get <build>` and
`tod build get-log <build>`. Compare its `commitHash` with the checkout before
applying a fix. One change can fix several builds once you confirm their cause.

- Follow required dependency failures recursively when they failed on the
  same commit. Report a cancelled dependency as a blocker. If the dependency
  ran on a different commit, report it as the cause of the current failure.
- Take the exact report name inside brackets on the failure line, preserving
  spaces and casing. Quote it as one argument and read the report before editing.
  - `[<report>]: found problems with severity <severity> or higher` →
    `tod build get-code-problems <build> "<report>" <severity>`.
  - `[<report>]: <count> not passed test cases` →
    `tod build get-unit-test-report <build> "<report>"`. Use
    `--artifact <path> > <output-file>` to retrieve a referenced test artifact.
- Inspect `.onedev-buildspec.yml` for job configuration issues. Run
  `tod build get-spec-schema` before editing it. Use
  `tod build get-changes-since-success <build>` when useful.
- Verify the fix against the current source checkout after resolving any
  conflicts. Draft feedback if a build needs an explanation or cannot be fixed.

## Leave work ready to submit

Leave completed edits uncommitted and changed submodules on default branches
with upstreams. Record whether code is ready to submit, including when there
is no work. Keep planned OneDev actions in an ordered `<saved-pr-actions>`
list in the session. Preserve exact Markdown and action parameters.

- PR comment, or code comment with file and line range.
- Code-thread reply, resolve, or unresolve with comment ID and any note.
- Approve or request changes with any review summary.
- Merge, with the reviewed head for an automatic merge.

Base code-comment resolution changes on the current code and discussion:
save a resolve action for an addressed finding, or an unresolve action for a
resolved concern that remains unaddressed or has resurfaced.

When resolving or reopening a thread, put the explanation in the status change
note. OneDev posts that note as a reply. Use a standalone reply when the thread
status stays the same.

Omit blank text-only actions and optional notes. Use OneDev references such
as `PR #42`, `issue team/app#7`, and `build APP-9`. For automated feedback
accompanying a push or formal review, omit mentions. In PR discussion comments,
mention someone when you need a response.

A request such as “work on PR 123” ends after reporting the prepared work.
Commit, push, or apply saved OneDev actions only when the user or automated
prompt explicitly requests submission.

If blocked, report the reason and any failing command or error. Record that
no code is ready to submit. If the prompt identifies you as an AI user, save a
PR comment explaining the blocker or needed decision and stop without asking
for direction. Otherwise, ask the user when a decision is required.
