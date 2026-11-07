---
name: finish-pr
description: >-
  Finish a PR by repeatedly requesting a Kelos review, waiting for its check,
  addressing valid review findings, squashing commits, and updating the PR
  until a review approves and that iteration is finalized. Use when the user
  says "finish-pr" or asks for this review-and-fix loop. Defaults to the PR for
  the current branch.
---

# Finish PR

Repeat the following loop until a Kelos review approves, then complete that
iteration before breaking. An approving verdict must still go through findings,
squashing, pushing, and PR updates. Use `gh` for GitHub operations. This workflow
updates the PR; it does not merge it.

## Establish the target

Resolve the requested PR, or the current branch's PR when none is specified.
Identify its repository, number, base branch, head branch, and head SHA. Work
on that head branch and preserve unrelated local changes. Publish any intended
pending changes before requesting a review so the reviewer sees them.

## Review loop

1. **Request a review.** Record the current remote head SHA, existing review
   check IDs, and review comment timestamps. Post exactly `/kelos review` with
   `gh pr comment <number> --repo <owner/repo> --body '/kelos review'`.
2. **Wait for this review.** Discover the Kelos review check created for this
   request on the recorded SHA, and poll that check until it completes. Wait
   for it to appear even if older checks have already passed; do not post
   duplicate requests while waiting. Keep the user informed during the wait.
   If the head changes during the review, reconcile it before starting another
   iteration; that result cannot approve a different head.
3. **Read and address the findings.** Read the fresh Kelos result and all PR
   reviews, inline threads, and review comments. Kelos may publish an `APPROVE`
   verdict in an updated sticky comment rather than a GitHub `APPROVED` review.
   A successful check means the review task completed, not that it approved
   the PR. Require a result attributable to this request and recorded head.
   Use `address-pr-review` to verify findings and fix only those that are
   valid, current, and required. Check each finding's author, timestamp, head,
   and thread resolution; explicitly triage findings that do not warrant a
   change. Run the project's appropriate validation for any fixes.
4. **Squash and update the PR.** Squash the PR branch's commits into one commit
   above its merge base with the PR base, including any fixes. If it is already
   one commit and there are no changes, leave the commit intact. Preserve the
   complete intended diff and push to the PR's head branch, using an explicit
   `--force-with-lease=<head-ref>:<expected-remote-sha>` when rewriting history.
   If the lease fails, reconcile the remote changes before retrying. Update
   the PR title and description to describe the final implementation and
   validation, following the repository's PR template when present.
5. **Decide whether to repeat.** Break only if this iteration's Kelos verdict
   approves the recorded review head, steps 3 and 4 are complete, and no valid
   required findings remain. Break even if addressing findings or squashing in
   this iteration changed the pushed SHA; do not request another review solely
   to approve the resulting commit. Otherwise continue the loop.

Stop and report the blocker if the review check fails, is cancelled, cannot
run, or completes without a usable verdict, or if repeated iterations cannot
make progress on the same unresolved finding. Do not spin on failed tooling
or silently treat a blocked review as approval.

On success, report the PR link, final commit, approval result, and validation.
If finalization changed the SHA, identify the reviewed commit separately from
the final pushed commit.
