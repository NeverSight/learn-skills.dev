---
name: git-fix-pr
description: Use when an active PR needs a deliberate fix pass to identify the right PR, triage CI, review, and body blockers, agree on actions with the user, make and commit the fixes, update reviewer threads or PR text, then push once.
---

# Git Fix PR

Use this skill to turn an active PR with blockers into a clean follow-up push. Optimize for good triage, explicit user decisions, short reviewer replies, and one final push after all local commits and PR housekeeping are ready.

This is a companion to `git-commit-pr`: use that skill's staging, commit, validation, and push discipline when it is available. Local repo rules still win.

## Core Invariant

Do not push fix commits while still discovering or working through blockers. A push can retrigger CI, review bots, or reviewer notifications. Gather the full PR state, agree on a plan, finish local fixes, commit, prepare or post all necessary replies/body updates, then push once.

If the host requires new commits to exist remotely before a reply can link to them, queue the exact replies, push once, then post the queued replies immediately after that push without making more commits.

## Identify The Target PR

Resolve the target PR before collecting blockers.

Use the PR the user specified by reference when invoking this skill:

- PR number, such as `#123` or `PR 123`
- Full or partial PR URL
- Head branch name
- Exact or near-exact PR title

If the user does not specify a PR, use the latest PR that was created or clearly discussed in the current session. If that PR is far back in the context window, was created a long time ago relative to the current task, or could plausibly be stale, use the PR associated with the current branch instead.

If neither path is certain, ask the user immediately which PR to fix. Do not inspect CI, comments, or body TODOs for a guessed PR.

Once the target is resolved, state it briefly:

```text
Target PR: #123 <title> (<head-branch> -> <base-branch>)
Reason selected: user provided #123 / current branch / latest created PR in this session
```

## Study The PR State

Start by identifying the current branch, PR, base branch, local changes, and repo rules:

```bash
git status --short
git branch --show-current
git remote -v
git log --format='%h %s' -n 20
```

Prefer the best available GitHub or forge integration. Command examples describe the evidence to gather, not a required tool choice.

Collect:

- PR title, URL, state, draft status, base/head branch, body, labels, review decision, requested reviewers, latest commits, changed files, and merge state.
- CI/check status, including failed job names, links, and failed logs when available.
- PR-level comments, review submissions, and inline review threads. `gh pr view --comments` is not enough because it misses inline review comments.
- Unresolved review threads only when the platform exposes resolution state; otherwise label the resolution status as unknown.
- TODOs in the PR body: unchecked task-list items, `TODO`, `FIXME`, placeholders, unresolved template comments, or verification text that says work remains.
- Local uncommitted changes or staged work that could be user-owned.

Use API or GraphQL when normal PR commands hide important state:

```bash
gh pr view <PR> --json title,url,body,state,isDraft,baseRefName,headRefName,mergeStateStatus,reviewDecision,statusCheckRollup,comments,reviews,latestReviews,files,commits
gh pr checks <PR>
gh api repos/OWNER/REPO/pulls/<PR>/comments
gh api repos/OWNER/REPO/issues/<PR>/comments
gh api repos/OWNER/REPO/pulls/<PR>/reviews
```

Use GraphQL or a GitHub connector for review-thread resolution state when it matters. Do not treat dismissed reviews, resolved threads, collapsed spam/off-topic comments, or stale bot comments as blockers without evidence that they still apply.

## Triage Blockers

Classify each item before proposing changes:

- `CI`: failed, cancelled, missing, or flaky checks that block merge or reviewer confidence.
- `REVIEW`: unresolved review comments, requested changes, reviewer questions, or maintainers asking for evidence.
- `TODO`: PR body tasks, placeholders, required manual tests, screenshots, migration notes, or verification gaps.
- `PR-BODY`: contradictions between the body and current diff, stale scope claims, obsolete screenshots, or missing reviewer-critical context.
- `MERGE`: merge conflicts, stale base, branch protection, missing approvals, or a required rebase.

For every item, record the evidence: comment URL or thread id, check name/log link, body line or copied TODO text, changed file, and why it is or is not blocking.

Prefer root-cause fixes over superficial replies. For CI failures, inspect failed logs before editing. For review comments, read the surrounding code and PR diff before accepting or pushing back. For TODOs, either close them with real work/evidence or keep the body honest.

## Present Review State

Before asking planning questions, output a compact review-state snapshot with the action-item ledger. This snapshot must put the problem, location, and evidence for each item directly in the chat so the user can decide without hunting through earlier tool output.

Keep this snapshot factual. Do not include recommendations, decision options, or proposed fixes here; those belong in the item-by-item planning questions.

Use this shape:

```text
PR state
- Target: #123 <title> (<head-branch> -> <base-branch>)
- CI: <passing/failing/pending, with failed checks named>
- Review: <approved/changes requested/commented, with unresolved count>
- Body TODOs: <count and summary>
- Merge state: <clean/conflicted/stale/unknown>

Action items
REVIEW-1: <reviewer, file/line or PR thread>
PROBLEM: <brief summary of the problem, location, and evidence>

CI-1: <failed check name>
PROBLEM: <brief summary of the failure, location, and evidence>
```

After this snapshot, wait for user input unless the user explicitly authorized fixing the PR's blockers when invoking the skill. If that authorization clearly covers an item, treat its action as approved; still ask about any item where the intended fix or tradeoff is ambiguous.

If in Plan mode, begin the item-by-item interview immediately. If not in Plan mode but the runtime provides a structured user-question tool, use it to conduct the same interview without requiring a mode change. Examples include Codex `request_user_input`, Claude Code `AskUserQuestion`, Cursor `cursor/ask_question`, and OpenCode `question`. If neither Plan mode nor a structured question tool is available, stop after the snapshot and wait for the user to respond.

## Agree On A Plan

Do not implement fixes until the user chooses an action for each blocking item, except where the permission given when invoking the skill already authorizes a clear action.

Ask one question per blocker or per independent actionable fix. Never ask one broad question such as "how should we fix all 5 items?" If two comments share the same root cause and will be fixed by the same code change, group them as one actionable fix, but list every triggering comment under that item.

If `grill-me` is available and the session is in Plan mode, use it for unresolved choices: ask one question at a time, recommend an answer, and inspect the repo instead of asking whenever code or PR state can answer the question. The question must name the specific item being decided and repeat a short problem summary, such as `For REVIEW-2, comments about tests in file X, should we fix this by ...?`

Otherwise, give a concise structured plan and ask the user to choose an action for each item. Use this shape:

```text
PR blocker plan

CI-1: <failed check name>
PROBLEM: <short location/problem summary>
SOLUTION: <user choice>

REVIEW-1: <reviewer/comment>
PROBLEM: <short location/problem summary>
SOLUTION: <user choice>

TODO-1: <body task>
PROBLEM: <short location/problem summary>
SOLUTION: <user choice>
```

When the plan includes commit, PR-body, tracker, reply, and push work, include an execution timeline that shows the final push last. Do not output a plan where `push` appears before reviewer replies or PR comments. Use this shape:

```text
Execution timeline
- Commit focused fixes locally.
- Update PR body, tracker tickets, and any top-level PR comment.
- Post reviewer replies, or queue exact reply text if the forge requires remote commits first.
- Final push after local fixes, validation, PR housekeeping, and replies or queued replies are ready.
```

If the forge cannot accept the final reply text until commits are remote, say that exact replies will be drafted or queued before the final push, then posted immediately after the push as the only exception.

A plan is accepted only when every blocking item has its own recorded decision. If the user answers with a broad instruction like "fix them all," map that answer onto each listed item, then ask follow-up questions only for items whose action is still ambiguous. Non-blocking observations can be listed separately with a recommendation, but do not let them blur the blockers.

## Implement After Plan Approval

After the user approves the plan, execute in this order.

1. **Implement local changes.** Keep edits scoped to the approved items. Preserve user changes and unrelated local work. If a new blocker appears, stop and amend the plan with the user.
2. **Validate.** Run the local equivalent of failed CI first, then package or repo checks justified by the blast radius. Capture the commands and outcomes for the final handoff.
3. **Commit locally.** Follow `git-commit-pr` conventions: exact-path staging, focused commits, repo commitlint rules, and no broad `git add .`. Capture final short SHAs.
4. **Rebase before posting SHA-bearing replies.** If a rebase or conflict fix is required, do it before publishing replies that mention commit IDs. If a rebase rewrites SHAs after replies were drafted, update the drafts.
5. **Post or queue replies before the final push.** For each review or PR comment that caused an action, post the reply before pushing when the forge allows it. If the reply must wait for remote commits, draft the exact reply text now and treat it as queued work that must happen immediately after the final push:
   - Fixed: `Fixed in <sha>: <one-line summary>.`
   - Pushback: `Leaving this unchanged: <reason>. <evidence or tradeoff>.`
   - Deferred by user choice: `Leaving this open for now per plan: <reason/owner>.`
6. **Update PR body or top-level thread when needed.** If the approved work changed direction, added meaningful scope, closed TODOs, or made the body contradictory, edit the PR body. For major direction changes or new features, add one main-thread comment summarizing what changed and why.
7. **Push once.** Push only after local commits, validation, comment replies or queued replies, and PR body updates are complete. If the user has not already authorized the final push in this session, show the branch, commits, validation, PR updates, and queued replies, then ask for confirmation.

If the platform cannot accept replies before the final push because the new commits are not remote yet, push once after step 6, then immediately post the queued replies. Do not create or push more commits after that without returning to planning.

## Reply And Body Guidelines

- Reply only to comments that triggered action, disagreement, or a user-approved deferral. Avoid noisy blanket updates.
- Keep replies factual and compact. Mention the commit id for code changes, not an essay.
- Do not include validation summaries, command lists, or `Validation:` sentences in review or PR comment replies. If the fix is test coverage, say the test was added, not which commands passed.
- When pushing back, explain the technical reason or product tradeoff. Do not frame it as preference.
- Do not mark a thread resolved unless the issue is actually fixed, intentionally rejected, or explicitly deferred with the user's approval.
- Remove stale TODOs or template hints from the PR body only after the underlying task is done or confirmed obsolete.
- Never claim a manual test, screenshot, migration, or deployment was completed unless it actually was.

## Final Handoff

End with:

- PR URL and branch.
- Blocking items handled, grouped as fixed, pushed back, deferred, or still blocked.
- Commit list and what each commit addressed.
- Validation run and results.
- Whether comments/body updates were posted before or after the final push.
- Any remaining reviewer, CI, or manual-test risk.
