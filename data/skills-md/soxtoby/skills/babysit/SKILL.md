---
name: babysit
description: Babysit a pull request when asked to watch its checks, merge conflicts, or review comments.
---

# Babysit a PR

Invoking this skill authorizes fixing build/test failures, resolving merge conflicts, and handling PR comments under the rules below, including commits, pushes, and comment replies. Merging the PR requires separate authorization.

## 1. Establish current state

Identify the target PR, repository, base, head branch, and head commit. Infer from the current branch when unambiguous; otherwise ask for the PR. Read repository instructions and inspect local changes before editing. Preserve unrelated work.

Fetch current checks and failure logs, mergeability, reviews, inline threads, and general PR comments, including paginated results. Read the surrounding code and discussion before acting. Account for every outstanding failure, conflict, and comment; distinguish resolved or superseded feedback from actionable work. If available, register the PR with `link_pull_request`.

## 2. Address outstanding work

### Failed checks and merge conflicts

Diagnose and fix build/test failures, preserving intended behavior and meaningful checks. Resolve conflicts against the current base using repository conventions. If resolution requires an undecided product or design choice, ask about that choice while completing independent work.

For an infrastructure failure, retry when evidence supports a transient cause; report persistent access or infrastructure blockers. A retry is complete only when its result is known.

### Comments

Prefix every response to a PR comment with `🤖 `, including acknowledgments, explanations, and justifications for declining changes.

Evaluate human and automated comments against the code, PR intent, and repository conventions. Choose one disposition per concern:

- **Not worthwhile:** reply with a brief, concrete justification. Leave the code unchanged.
- **Meaningful behavior change:** explain the proposed before/after behavior and recommendation; ask whether to make the change before implementing it. This gate applies even to a one-line edit.
- **Large code change:** explain scope and recommendation; ask whether to make the change before implementing it.
- **Purely mechanical or small and worthwhile:** implement it, then publish under step 3 and tell the user briefly.

Judge size by conceptual scope and review burden, not line or file count. A consistent internal rename across many files can be mechanical; a public API rename can meaningfully change behavior. Treat uncertain behavior or scope as a decision to investigate, then ask if it remains unresolved. When both approval gates apply, ask once with both reasons.

Track each concern as addressed, declined with justification, or awaiting the user's decision. Revisit it only when new evidence or feedback changes the disposition. Continue independent authorized work while a decision is pending.

## 3. Validate and publish

Run checks appropriate to the change, including the failing build/test when applicable. Inspect the final diff for unintended changes. Refresh the remote head and relevant discussion before publishing; reconcile concurrent updates first.

- **Small or mechanical changes:** commit only the relevant changes and push to the PR branch. After a successful push, reply to each triggering comment briefly: "🤖 Fixed", "🤖 Done", "🤖 Renamed as requested", or a short explanation when needed. Report the change to the user concisely.
- **Large changes, including failure or conflict fixes:** finish the implementation and validation locally, then present the diff and results for user review before pushing. Approval to implement a comment is distinct from approval to publish the resulting large change; honor explicit authorization already given for either stage.

Keep changes awaiting review separate from changes authorized for push. A local fix or failed push is not a published fix; report its actual state. Check CI for the pushed commit, since results from an earlier head do not validate it.

Once all comments are addressed or declined with justification and all resulting fixes are pushed, refresh reviews and request re-review from every reviewer still requesting changes (`CHANGES_REQUESTED`). Confirm each request succeeded or is already pending; retain reviewer and review IDs across wakes to avoid duplicate requests for the same review.

## 4. Keep watching

After each batch, refresh PR state and repeat for new failures, conflicts, and comments. Retain the last inspected head, handled comment IDs, pending decisions, and validation results across wakes to avoid duplicate work or replies.

When T3 Code provides `watch_pull_request`, handle existing feedback first, call it, and end the turn. Let its events wake the thread; use this watcher instead of polling or starting another watcher. On each wake, inspect fresh state and resume this workflow. Green checks alone do not end babysitting while the PR remains open.

When handing control back for a decision, review, blocker, or stop request, call `unwatch_pull_request` first if watching. Resume watching after the user responds and the resulting work is handled. Before handing back, use `list_thread_pull_requests` when available and link the target PR if missing.

Without a persistent watcher, use available bounded monitoring during the active session and state its limits. Report whether monitoring is active, awaiting input, or stopped; claim future monitoring only after it is actually registered.

Finish when the PR merges or closes, or the user stops babysitting. Give a brief status covering published fixes, comment dispositions, checks for the current head, and anything awaiting the user.
