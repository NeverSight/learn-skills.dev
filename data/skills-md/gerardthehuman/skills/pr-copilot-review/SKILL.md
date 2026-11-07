---
name: pr-copilot-review
description: "Drive one PR through CI and Copilot review until feedback is resolved."
disable-model-invocation: true
---

# PR Feedback Loop

Run one pull request through a bounded Copilot cycle. Keep `OWNER/REPO`,
`PR_NUMBER`, and the current head SHA in view.

## 1. Establish the PR state

Resolve `OWNER/REPO` and `PR_NUMBER`, verify GitHub authentication, and inspect
the working tree. Continue only for an open PR and keep unrelated changes
separate. Make a draft PR ready before proceeding.

**Complete when:** the PR is open and ready for review, the repository and PR
number are known, and the working-tree state is recorded.

## 2. `ci_pending` — wait for checks

Run:

```bash
gh pr checks PR_NUMBER --repo OWNER/REPO --watch
```

Inspect failed or cancelled checks and their logs. Fix branch-owned failures,
validate, push, and return to this step. Report failures owned by external
services, permissions, quotas, or infrastructure.

**Complete when:** every check is green, or each non-branch-owned failure is
recorded and reported.

## 3. `review_pending` — inspect current feedback

Check the current Copilot status once:

```bash
node <skill-dir>/scripts/await_review_status.mjs --repo OWNER/REPO --pr PR_NUMBER --timeout-seconds 0
```

Read the latest Copilot review, all unresolved threads, the review body’s
`<details><summary>Suppressed comments</summary>` section, and Copilot’s
overview comment in the PR conversation (the poller does not fetch the overview).
Copilot labels each comment `High`, `Medium`, or `Low`; use the label to
prioritize, not to skip. Record the review effort level and approval assessment
from the overview comment. An approval assessment is not merge readiness, and a
later push dismisses a Copilot approval. Compare findings with the current head
SHA. Mark `review_complete` when the review matches the current head and has no
actionable findings or unresolved threads. Mark `unresolved_comments` for every
thread or suppressed finding that still needs a response or fix.

**Complete when:** every current-head Copilot finding is classified as
`review_complete` or listed as `unresolved_comments`, including suppressed
comments.

## 4. `unresolved_comments` — fix and resolve existing threads

For each `unresolved_comments` item, verify it against the current branch. Make
the smallest complete fix for a valid finding, validate it, and fold it into the
introducing branch commit with `/pr-apply-changes` or a `--fixup` commit. Push
rewritten history with `git push --force-with-lease`.

Treat files under `docs/worklog/*` as dated historical records. For a comment
about an outdated command or inventory, reply with evidence pointing to the
current workflow or documentation source of truth, then resolve the thread.

Copilot does not see replies and does not respond in threads; replies are for
human reviewers. Copilot can repeat a finding you dismissed or resolved on
re-review. Re-check the repeat against the current head, and if it is still
invalid, resolve it with evidence rather than fixing it again.

Resolve every fixed or answered thread beside the feedback handling:

```bash
gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{id isResolved}}}' -f id='THREAD_ID'
```

**Complete when:** every existing finding has been fixed or answered, every
corresponding thread is resolved, and any resulting push has completed.

## 5. `review_complete` or stale — request Copilot when needed

When the current review is not `review_complete`, request Copilot. Copilot needs
a new request after each push unless automatic review of new pushes is enabled:

```bash
gh pr edit PR_NUMBER --repo OWNER/REPO --add-reviewer @copilot
```

The REST API also accepts the Copilot reviewer bot as a request target:

```bash
gh api -X POST repos/OWNER/REPO/pulls/PR_NUMBER/requested_reviewers -f 'reviewers[]=copilot-pull-request-reviewer[bot]'
```

Review effort (Lite or Balanced) is set in the PR's Reviewers menu, not by these
commands. Skip the request only when the one-shot check confirmed
`review_complete` for the current head.

**Complete when:** Copilot accepted the request, or the current-head review is
already `review_complete`.

## 6. `review_pending` — wait for Copilot

Wait for the requested review:

```bash
node <skill-dir>/scripts/await_review_status.mjs --repo OWNER/REPO --pr PR_NUMBER --timeout-seconds 1800 --interval-seconds 30
```

**Complete when:** the poller returns a review result for the current head, or
the state is `timeout` and the timeout is reported.

## 7. `head_changed` — repeat the loop

After every push or a poller result showing `head_changed`, return to step 2.
Re-run CI, inspect the new Copilot review, overview comment, and suppressed
comments, and handle all new `unresolved_comments` before requesting another
review. Repeated findings follow the step 4 rule: report a repeat that stays
invalid after re-checking rather than looping on it.

Finish when CI is green or an external failure is reported, the current-head
review is `review_complete`, and no unresolved Copilot threads remain. Report
`timeout`, an unchanged failing check or thread, failed validation, or an
unavailable Copilot request with the relevant evidence.

**Complete when:** the PR satisfies all finish conditions, or a named blocking
state and its evidence have been reported.
