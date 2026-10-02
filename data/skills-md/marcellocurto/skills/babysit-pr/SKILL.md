---
name: babysit-pr
description: Watch a pull request, settle review comments from people and Codex as they arrive, and stop once every thread is answered and Codex approves the latest commit, or when a problem needs the user.
disable-model-invocation: true
---

# Babysit PR

Keep a pull request moving until every reviewer, human or Codex, has been answered: no review thread or conversation comment is left unanswered, and Codex has reviewed the latest commit and reacted with 👍. Each round, wait for new feedback, let Codex finish if it is mid-review, settle the whole batch, push once, and wait again. Human reviewers get the same treatment as Codex: their comments are audited on the merits, fixed when justified, and answered in every case. Work without asking for approval and stop only for the reasons under **Stop**. Never force-push or merge.

## Start

1. **Find the PR.** Use the PR from the conversation, otherwise the current branch's PR. Ask only if neither is clear. Check every interval the user gave, otherwise every 5 minutes.
2. **Write down the PR's intent** before reading any comment: the problem it solves, the approach it chose, and what it deliberately leaves out. Take it from the user's instructions in this conversation, then the linked issue, the PR description, and the commits, in that order. Every comment is judged against this intent.

## Wait for feedback

Run:

```
python "<skill-path>/scripts/watch_pr.py" [--pr URL_OR_NUMBER] --interval <minutes> [--since <checked_at>]
```

Omit `--since` on the first run so that existing feedback counts. On later runs, pass the `checked_at` value from the previous result. The watcher checks the PR every interval and returns JSON whose `reason` says why it stopped waiting. While Codex is reviewing, it keeps waiting, so feedback that arrives mid-review is handled together with Codex's findings. It ignores comments from the authenticated account, which includes your own replies; if the user says they commented, run a round anyway.

Run the watcher as a background command if your host wakes you when it exits. Otherwise run it in the foreground with a shell timeout longer than `--timeout` (30 minutes by default), and lower `--timeout` if the shell limit requires it.

Act on `reason`:

- `new-activity`: someone commented, reviewed, or replied in a thread. Run a round.
- `codex-approved`: Codex reviewed the head commit and found nothing. If no unresolved threads remain, the PR is done. If the only unresolved threads are ones you left open for a decision, stop. Otherwise run a round for the remaining threads.
- `timeout` with Codex `pending`: Codex has not started on the head commit. Comment `@codex review` once for that commit and wait again. If it still has not started after another timeout, stop.
- `timeout` with Codex `running`: wait again. Stop once it has been running on the same commit for over two hours.
- `timeout` with Codex `findings`: Codex's findings on the head commit are already answered without a push, so Codex will not review again on its own. Comment `@codex review` once for that commit and wait again.
- `codex-failed` or `closed`: stop.

## Run a round

1. **Collect the open feedback.** Fetch it with `python "<skill-path>/scripts/fetch_review_context.py" [--pr URL_OR_NUMBER]`. Open feedback is every unresolved review thread, every conversation comment or review body you have not answered yet, and every review that requests changes, whoever wrote it. A human reply in a thread you already resolved reopens it.
2. **Triage the batch.** When five or more comments are open, or the same area draws comments for a second round, group them by root cause before fixing anything. Decide whether you have many independent small fixes or symptoms of one design problem (see **Small fixes or an architectural problem**).
3. **Audit each comment.** Check the code to decide whether the comment is correct and whether its suggestion is the right fix. Then check it against the PR's intent (see **Reject what works against the PR**). If the concern is real but the suggestion is poor, fix it a better way.
4. **Fix in one batch.** Make every justified fix, run the relevant checks, commit, and push once. Every push restarts Codex's review, so never push per comment.
5. **Reply and resolve.** In each thread, reply with what changed and the commit, or with why nothing changed, then resolve it. Answer conversation comments with one reply that addresses each point. Keep replies to one or two sentences.
6. Go back to waiting.

## Reject what works against the PR

Be strict. A reviewer's confidence, a severity label, or a ready-made patch is not evidence. Reply with the reason and resolve the thread when a comment:

- asks for work outside the PR's intent, such as a new feature, an unrelated refactor, or a follow-up
- reverses a decision the PR made on purpose, as stated in the conversation, the description, or the code
- adds speculative hardening: guards against inputs that the types or callers already rule out, fallbacks, configuration, or compatibility code for callers that do not exist
- asks for a style the repository's conventions and tooling do not require
- misreads the code

Point to the intent in the reply, for example: "This PR intentionally drops the legacy format, so a fallback for it would keep the code we are removing." When a rejected point comes back in a later round, reply once with a link to the earlier answer and resolve it without arguing the point again.

A real defect introduced by the PR is never out of scope. Fix it even when the suggested patch is poor.

## Small fixes or an architectural problem

A batch points to one design problem when:

- several comments are symptoms of the same cause, such as state owned in two places, an invariant the types should enforce, a lifecycle or concurrency model that does not fit, or a data model that does not match the domain
- fixing one comment would undo or conflict with another
- the fixes add special cases, flags, or guards around the same code
- the same area draws new findings after each push

If the cause can be fixed within the PR's intent as one contained change, fix the cause instead of the symptoms, and reply on each affected thread that the shared fix in that commit covers it. If fixing it would change the PR's approach or scope, do not patch the symptoms. Leave those threads open and stop.

Otherwise, treat the comments as independent small fixes and settle them all in this round's batch.

## Stop

- **Done:** no unresolved thread or unanswered comment remains, no review still requests changes, and Codex reacted with 👍 for the head commit.
- **Architectural problem:** fixing it would change the PR's approach or scope.
- **Decision needed:** a comment needs a product or design decision you cannot make. Leave the thread open and say in the reply what is needed.
- **Codex unavailable:** Codex failed, never started on the head commit, or ran on the same commit for over two hours.
- **Repeated rejection:** Codex re-raises points you already rejected after you requested a new review on the same commit.
- **No convergence:** ten rounds without approval, or twelve hours since the first check.
- **Closed:** the PR was merged or closed.

## Report

Say whether the PR is done or why you stopped, and name the head commit and the number of rounds. List each comment with its outcome: fixed (with the commit), rejected (with the reason), or left open (with the decision needed). For an architectural problem, name the root cause, the comments that point to it, and the change you recommend.
