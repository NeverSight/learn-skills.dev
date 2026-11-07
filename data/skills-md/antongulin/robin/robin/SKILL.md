---
name: robin
description: Use whenever an agent creates, updates, reviews, or completes a GitHub pull request. Detect whether Robin is installed in the repository; when it is, automatically drive the PR through a bounded review, verified-fix, reply, thread-resolution, re-review, authorized-merge, and cleanup loop without requiring the user to mention Robin. Also use for explicit Robin requests, PR feedback triage, unresolved review threads, or waiting for PR checks.
metadata:
  version: 2.13.1 # x-release-please-version
---

# Robin PR Completion Protocol

Robin is an AI reviewer that runs as a GitHub Action. Use this skill as the owner-side
protocol for completing a PR; do not blindly obey Robin. Robin may see only the diff and
may use a weak rotating model, while the working agent has repository and conversation
context. Fix verified bugs and reject noise with a factual reply.

## Non-negotiable behavior

- Activate for ordinary PR work without requiring the user to say “Robin.”
- Detect Robin on the PR base branch before entering the loop. Do not install it unless
  the user asks.
- Continue through waits and review rounds autonomously. A running check, a pushed fix,
  or a requested re-review is not a terminal state.
- Count completed Robin review results. Start with a budget of 5. Above 5, obtain approval
  for each additional review unless the user explicitly pre-authorized continuous review.
- Reply separately to every Robin inline comment, including rejected findings, and
  resolve every review thread after replying.
- Fix only verified defects. Severity and confidence prioritize investigation; they do
  not prove correctness.
- Never merge without explicit authorization. “Create a PR” does not authorize merge.
- Preserve unrelated local changes and branches. Never stash, discard, commit, or delete
  them merely to complete this protocol.
- Never prepare or publish a release automatically.

## Terminal states

Do not hand control back merely because Robin or another check is still running. Continue
polling, triaging, fixing, replying, resolving, and re-reviewing until exactly one of these
states is reached:

1. **READY:** all gates pass, but merge authorization is absent.
2. **COMPLETE:** an authorized merge is confirmed and cleanup is verified.
3. **CAP:** the currently approved review budget was used and another review requires
   authorization.
4. **BLOCKED:** repeated infrastructure failure, unsafe cleanup conflict, missing access,
   or another condition that cannot be resolved without the user.

Provide brief progress updates during long waits, but keep ownership of the task until a
terminal state is reached.

## 1. Establish policy and safety

When planning to create a PR, record two independent policies before creation.

**Merge policy:**

- Explicit instructions such as “merge when green” or “create, review, and merge it”
  authorize automatic merge for this PR.
- Otherwise ask once whether the user wants automatic merge when green. Until the user
  says yes, record the policy as **manual**.
- A standing preference applies only when the user clearly made it standing. Never infer
  one from an earlier merge.

**Review-extension policy:**

- Default to **one-at-a-time**: reviews 1–5 are pre-approved; every review above 5 needs
  a new explicit approval.
- `One more Robin review` increases the budget by exactly one. It does not authorize all
  later reviews. If review 6 leads to a need for review 7, ask again.
- Explicit instructions such as “full auto,” “keep running Robin until green,” “do not
  ask between extra Robin rounds,” or an equivalent goal authorize **continuous** extra
  reviews for this PR. Continue without per-review questions, but still stop early when
  green and stop on BLOCKED infrastructure or safety conditions.
- `Auto-merge` alone authorizes only merge; it does not authorize reviews above 5.
- `Full auto` or “auto mode through Robin and merge” authorizes both continuous reviews
  and merge for this PR. Do not infer a standing cross-PR policy unless stated explicitly.

For an existing PR with no recorded authorization, use manual mode and continue through
the review loop; stop at READY.

Capture the initial repository state so unrelated changes can be preserved and reported:

```bash
git status --short --branch
gh repo view --json nameWithOwner -q .nameWithOwner
```

Once the PR exists, record its identity and branches:

```bash
gh pr view --json number,url,baseRefName,headRefName,state,reviewDecision,mergeStateStatus,statusCheckRollup
```

Stage only task or verified-review-fix files. Never use broad staging when unrelated files
exist.

## 2. Detect Robin

Robin must exist on the PR’s base branch for an opened PR to trigger it. Fetch the base
and inspect that tree, not only the feature branch:

```bash
git fetch origin <base-branch>
git grep -n 'antongulin/robin' origin/<base-branch> -- .github/workflows
```

Also recognize an equivalent workflow discovered through `gh api` when the base is not
available locally. Confirm that it listens to `pull_request` or accepts `/robin` through
`issue_comment`.

- Robin present: run this entire protocol automatically.
- Robin absent: continue the user’s normal PR task without the Robin loop and mention the
  absence. Do not add Robin unless asked.
- Robin is added only on the current PR branch: it cannot review that PR automatically
  because the workflow is absent from the base. Explain this limitation rather than
  pretending a review will arrive.

At the start, a best-effort version check is allowed but must never delay PR work:

```bash
gh release view --repo antongulin/robin --json tagName -q .tagName 2>/dev/null
```

Report an outdated installed skill, but update it only with prior authorization.

## 3. Observe a completed review

The PR-open review is normally automatic. Do not immediately post `/robin`; first inspect
PR comments, reviews, checks, and Actions runs. Poll about every 30 seconds.

```bash
gh pr view <number> --json comments,reviews,statusCheckRollup
gh run list --limit 20 --json databaseId,event,status,conclusion,workflowName,createdAt,url,displayTitle,headBranch
```

- If a Robin run is active, watch it and keep polling.
- If a run fails, classify it as infrastructure failure, inspect it, and retry the failed
  run once before considering a slash command.
- If no Robin signal appears after about 3 minutes, confirm the workflow trigger. Only
  then post `/robin`.
- Cap a single wait around 8–10 minutes. Report a persistent provider or Actions failure
  as BLOCKED with the run URL; never treat silence or an empty result as a clean review.

Increment the review counter only when a completed, usable Robin result arrives. For an
existing PR, the latest usable result on the current head starts this completion run as
review 1; do not count obsolete historical results. Each completed re-review increments
the counter once. Track both `reviews_used` and `reviews_approved`; initialize the latter
to 5.

## 4. Fetch and classify every finding

Fetch top-level review data, REST inline comments, and GraphQL review-thread state. Read
[references/github-pr-api-reference.md](references/github-pr-api-reference.md) for the
exact queries, reply endpoint, and resolution mutation.

Classify every finding against the actual repository:

- **FIX:** confirmed correctness, security, reliability, data-loss, test, or materially
  misleading documentation defect. Fix it, regardless of Robin’s stated severity.
- **REJECT:** false positive, duplicate, already handled, subjective churn, conflict with
  repository conventions, or a claim disproved by broader context. Do not change code.
- **INFRA:** reviewer timeout, failed workflow, empty response, or superseded/cancelled
  run. Handle the run; do not change code.

Suggestions are off by default. Apply one only when it prevents a concrete problem or is
clearly necessary for the requested change. Never invent a change merely to satisfy the
reviewer.

## 5. Close the current review before starting another

For each completed Robin result, perform this sequence in order:

1. Implement only FIX items in the repository’s existing style.
2. Run proportionate local verification and `git diff --check`.
3. Stage only intended files and create a local commit when code changed.
4. Reply individually to every Robin inline comment from this review:
   - FIX: name the correction and local commit.
   - REJECT: state the concrete repository evidence for not changing it.
5. For findings present only in the review body, post one itemized disposition comment
   because GitHub provides no inline reply target.
6. Resolve every handled review thread, including outdated threads.
7. Re-query GraphQL and verify zero unresolved handled threads and zero unanswered Robin
   inline comments.
8. Only now decide whether to push and re-review under step 6.

Example replies:

- `Fixed in abc123: abort and timeout failures now return distinct errors.`
- `Not changing: the value is passed as a bound query parameter at db.ts:84, so the
  reported interpolation path does not exist.`

Do not use a single top-level summary as a substitute for inline replies. Do not start
the next review while replies or threads from the current review remain open.

## 6. Decide whether to re-review

- No code changed because all findings were REJECT: do not spend another Robin review.
  Proceed to the green-light gate.
- Code changed and `reviews_used < reviews_approved`: push it and obtain another Robin
  result.
- The approved budget is exhausted and another result would materially improve confidence:
  follow the budget-extension rules below.

Robin’s default workflow reviews on PR open and on `/robin`, not on every push
(`synchronize` is opt-in), but some installs and customized workflows do trigger on
`synchronize`. After pushing a fix:

1. Inspect the workflow trigger and Actions runs for `synchronize`.
2. If the push started Robin, watch that run and do not post a duplicate command.
3. Otherwise request the normal manual re-review with `/robin`, including the fix commit
   and verification summary.

```bash
gh pr comment <number> --body '/robin

Fixed in <commit>:
- <verified issue>

Verification:
- <command and result>'
```

Then return to step 3 without asking the user to prompt the next round.

When the approved budget is exhausted, fix verified defects, reply, and resolve as usual.
Then decide whether another review is actually useful:

- If the PR is green, or only rejected noise remains, stop without another review.
- If verified issues remain, code changed and needs validation, or material uncertainty
  remains, another review is useful.
- In continuous mode, increase `reviews_approved` by one and proceed automatically.
- In one-at-a-time mode, enter CAP and ask: `Used <N> approved Robin reviews. Do you want
  me to run review <N+1>?` A yes increases the budget by exactly one. After that review,
  repeat this decision and ask again if yet another review is useful.

Check synchronize behavior before pushing at a budget boundary. If a push itself would
start the unapproved next review, request approval before pushing. Otherwise push the
verified fix, do not post `/robin`, and enter CAP. Never use uncertainty as a reason for
an automatic extra review in one-at-a-time mode.

## 7. Green-light gate

Before declaring READY or merging, verify all of the following:

- Local verification appropriate to the change passed.
- Required GitHub checks are successful or intentionally neutral/skipped.
- No Robin or relevant required check is still running.
- Every reviewer finding has a recorded disposition.
- Every inline reviewer comment has a later owner reply.
- Every review thread, including outdated threads, is resolved.
- The PR is mergeable and has no unresolved conflict.
- The used and approved review counts are known and no unapproved review occurred.

Use GraphQL thread state as authoritative. `reviewDecision: CHANGES_REQUESTED` may be stale
after later clean results; treat it as stale only when the latest findings are addressed,
all threads are resolved, and all checks pass.

In manual mode, report the gate summary and enter READY. Ask for merge permission if it
has not already been requested. In automatic mode, proceed directly to merge.

## 8. Authorized merge and cleanup

Merge only after the gate passes and authorization exists. Inspect repository settings
and conventions before selecting squash, merge, or rebase. Honor an explicit method or
project instruction first. If exactly one method is allowed, use it. In repositories that
generate releases from conventional commits, prefer squash so one PR produces one release
entry. Otherwise follow recent repository history; ask before merging if the method remains
materially ambiguous. Do not change repository settings.

```bash
gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
gh pr merge <number> --squash --delete-branch # use the selected allowed method
gh pr view <number> --json state,mergedAt,mergedBy,mergeCommit,url
```

Do not assume `--delete-branch` completed every local operation. After confirming the PR
is merged:

1. Switch explicitly to the recorded PR base branch.
2. Fast-forward it from its upstream.
3. Fetch and prune stale remote-tracking refs.
4. Verify the task branch is absent remotely; delete that exact remote branch if the merge
   command left it behind.
5. Delete the local task branch if it remains. Force-delete only after confirming the
   squash/rebase/merge landed.
6. Verify the current branch, upstream alignment, remaining branches, and working tree.

```bash
git switch <base-branch>
git pull --ff-only origin <base-branch>
git fetch --prune origin
git status --short --branch
git branch --list <task-branch>
git ls-remote --heads origin refs/heads/<task-branch> # no output means deleted
task_branch="<task-branch>"
if git ls-remote --exit-code --heads origin "refs/heads/$task_branch" >/dev/null; then
  git push origin --delete "$task_branch"
fi
if git show-ref --verify --quiet "refs/heads/$task_branch"; then
  git branch -D "$task_branch" # only after confirmed merge and base-branch switch
fi
```

Delete only the branch created for this task. Never delete unrelated local or remote
branches. Preserve pre-existing uncommitted files; if they prevent a safe switch or pull,
enter BLOCKED and report exactly which cleanup postcondition remains incomplete.

## 9. Final report and optional release offer

Report:

- PR number, URL, and final state.
- Robin reviews used, including how many were within the default 5 and how many were
  additionally approved.
- FIX and REJECT counts with a concise explanation.
- Replied comments and resolved threads, expressed as verified totals.
- Local and GitHub check results.
- Merge authorization and merge result.
- Current base branch and upstream sync state.
- Local/remote task-branch deletion state.
- Unrelated uncommitted files preserved, or `none`.

After an authorized merge reaches COMPLETE, detect whether the repository already has an
established release mechanism. If it does and the merged change appears releasable, end
with one optional question: `Do you want me to prepare and publish a release?` Treat that
as a separate task requiring a new explicit yes. Do not edit changelogs, tags, versions,
or published release notes as part of this PR protocol.

## Common failure modes

- Waiting once and returning instead of owning the loop to a terminal state.
- Requiring the user to mention Robin even though the installed workflow is detectable.
- Treating severity as proof or fixing style noise.
- Pushing before replying and resolving the current review.
- Posting `/robin` while an automatic run is already active.
- Assuming every push auto-runs Robin without checking the workflow trigger; the default
  install omits `synchronize` and uses `/robin` for re-reviews.
- Counting fix rounds instead of completed review results.
- Treating approval for “one more” review as permission for every later review.
- Treating auto-merge permission as continuous review permission.
- Treating an empty or failed reviewer run as clean.
- Relying on REST data or `reviewDecision` instead of GraphQL thread state.
- Merging without explicit authorization.
- Assuming merge cleanup succeeded without checking the base and task branches.
- Touching unrelated dirty files, branches, releases, or release notes.

## References

- [references/github-pr-api-reference.md](references/github-pr-api-reference.md) — exact
  GitHub API queries and mutations.
- [references/lessons-learned.md](references/lessons-learned.md) — incidents behind the
  protocol’s safeguards.
