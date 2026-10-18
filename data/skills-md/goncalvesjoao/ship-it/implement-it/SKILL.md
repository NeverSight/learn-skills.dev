---
name: implement-it
description: "Implement a spec with a draft PR, repeating fixes and code-review until both axes and required checks pass, then mark it ready for review."
disable-model-invocation: true
metadata:
  dependency: "implement-spec, code-review, pr"
  credits-author: Matt Pocock
  credits-url: https://github.com/mattpocock/skills
---

# Implement it

## Repository identity

Before GitHub access, Git writes/network operations, delegation, or scheduling, read and follow [the shared identity instructions](references/github-identity.md). Apply them to invoked upstream skills and every worker.

## User questions

Before asking or relaying any user question, read and follow [the user question rules](references/user-questions.md).

Requires Matt Pocock's `implement-spec`, `code-review`, and `pr` skills, their prerequisites, subagent support, and authenticated `gh`. This skill adds integration isolation, implementation reports, and a repeated review gate.

Invocation authorizes implementation, scoped commits, normal pushes, and draft PR creation and finalization. It does not authorize merging. Editing this skill does not start implementation.

## Implement

1. Locate and read the three installed skills. Invoke through the Skill tool when available; otherwise read and follow their `SKILL.md` files. If any skill or a required capability is unavailable, report the missing prerequisite and leave the work incomplete.
2. Read the spec, tickets, repository instructions, and issue-tracker workflow. Resolve the target repository, head remote and base branch, and check `gh auth status`. Before creating a branch on resumed work, follow the recovery procedure below. Acquire integration ownership and prepare the dedicated worktree below before issue-status writes or implementation. Pin the starting integration base to a commit SHA before implementation. Preserve that SHA and the authoritative spec pointers for every review round. For resumed work, recover the original base covering the entire spec implementation rather than using the current integration tip.
3. Complete the implementation preflight below, then apply the issue status step below to the GitHub spec issue. Apply it to each GitHub ticket when work on that ticket begins, including resumed work. For local specs or tickets without a GitHub issue, skip labeling.
4. Run `implement-spec` with these overrides: use the prepared integration worktree, apply issue status before each ticket, replace its review-and-fix step with the loop below, and defer finalization until that gate passes. Keep the PR draft until the readiness procedure succeeds.

Require implementation and fix workers to report material decisions, tradeoffs, approved deviations, limitations, and evidence pointers alongside their results. Retain these findings for the caller and recovery. Record missing before evidence honestly.

## Implementation preflight

Verify that required prerequisite implementations are present in the integration history, using their verified commits and behavior rather than issue closure alone. Integrate completed prerequisites through the normal merge workflow before dependent implementation; preserve the original pinned review base. An unfinished prerequisite keeps dependent work pending while independent authorized work can continue.

Inspect active worktrees and implementation reports for overlapping changes to shared modules. Agree on the shared interface and integration order before dispatching dependent writers; separate worktrees provide isolation but do not resolve semantic dependencies. Pass the prerequisite commits and shared-file coordination to workers.

Read the repository's check commands and CI/hook configuration. Report missing guardrails when existing checks have neither a CI job nor a configured hook. Continue running required checks locally; adding repository infrastructure requires authorization within the task scope.

## Integration worktree and ownership

Each spec has one dedicated integration worktree and branch, separate from the repository's primary checkout and other specs. Inspect `git worktree list --porcelain` and any attached managed worktrees before creating one. Reuse a worktree only when its repository, spec identity, branch, and exclusive availability are verified. Prefer the host's managed worktree tools when available; otherwise use `git worktree add -b <integration-branch> <absolute-path> <pinned-base-sha>`. Preserve the primary checkout's branch, index, and files. Never switch the primary checkout to an integration branch or force a branch into a second worktree.

Before creating or mutating integration state, acquire `<absolute-git-common-dir>/implement-it/<spec-key>.lock` by atomic directory creation. Derive the common directory from Git, resolving it to an absolute path; use the lowercase SHA-256 hex digest of the authoritative spec URL, or the canonical absolute local spec path, as the spec key. Hash the UTF-8 identity without a trailing newline so sessions and worktrees derive the same key. Record the owning session/worker identifier and spec identity inside the lock, then the absolute checkout path, integration branch, and original pinned base as soon as established, so interruption before the first report remains recoverable. An existing lock blocks another session from writes. Reclaim it only after verifying the recorded owner and its nested writers are inactive; an old timestamp or unavailable owner status is insufficient. An interrupted or partially initialized lock with unverifiable ownership is a blocker.

Keep ownership through implementation, merges, report edits, checks, and PR finalization. Nested workers operate under the same owner; serialize writes to the integration checkout. Fix implementers also use separate worktrees based on the integration branch. Supply every implementer, merger, reviewer, and PR worker the absolute integration checkout path and branch plus its own checkout path when different. Run integration edits, merges, commits, checks, and PR operations explicitly in the integration checkout, using command working directories or `git -C`; verify its repository and branch before mutations rather than relying on inherited shell state.

On completion, blocked handoff, or user pause, stop or await all nested writers before releasing only your own lock. Preserve the integration worktree, branch, report, and uncommitted task work for recovery and monitoring. If writers cannot be confirmed inactive, retain the lock and report the ownership blocker.

## Recovery

For a resumed spec, find `docs/implementations/<spec-gh-issue-id>.md` and verify its authoritative spec URL and repository before using its integration branch and original pinned base. If absent locally, inspect existing worktrees and local branch contents, then relevant remote branches after fetching if needed. Read branch contents without modifying unrelated checkouts. Reconcile the retained checkout and ownership record with the report and `git worktree list --porcelain`; reuse the verified dedicated integration worktree. If the branch is checked out in the primary checkout or an unrelated active worktree, report the conflict and preserve it until safe relocation is possible. Do not switch, reset, stash, or remove someone else's checkout to release the branch. If the recorded dedicated worktree is gone but the branch survives and is not checked out elsewhere, recreate a worktree on that branch without resetting it. Use the recorded branch; a missing or conflicting report or branch identity blocks a known prior run rather than authorizing a replacement branch. Preserve unrelated local work. Recover the associated PR using the lifecycle below before repeating publication operations.

## PR lifecycle

For GitHub specs, prefix every created or updated PR title with `[ISSUE #<gh issue id>] ` using the authoritative spec issue number, not a child ticket number. For example, `[ISSUE #42] Add location search`. Keep exactly one issue prefix, replacing any stale prefix on resumed PRs, and verify it with the title on readback. For local specs without a GitHub issue, keep the title unprefixed.

Before PR creation or updates, inspect the complete diff against the intended base and find any existing open PR for the actual head repository/branch and base in the target repository. Fetch and verify its URL, repository and head-repository identity, base, head branch/SHA, title, body, draft state, and labels. Reuse a matching PR. An ambiguous or conflicting target blocks publication until resolved. Reconcile uncertain writes by fetching current state before retrying, especially after an uncertain creation result.

Use explicit repository, base, and head arguments, including `<owner>:<head>` for forks. Push normally to the intended remote; resolve rejections without force-pushing. Verify the created PR is open and draft, with the intended repository, base, actual head repository/branch, and pushed SHA, and attach it in Codex when supported. If a resumed PR is already ready but the implementation gate is unmet, convert it to draft and remove stale readiness status labels before continuing. Preserve unrelated metadata and non-status labels.

### Readiness

After the review gate passes, recover the validation record described below and reuse validation only when verified evidence covers the exact current `HEAD`, both zero-finding review axes against the original pinned base, and every required check, with no uncommitted task changes. Honor requests for fresh checks and changes to required checks or validation environment. Missing or invalid evidence, or implementation changes during PR preparation, requires the full gate on the current SHA.

Inspect the final description against the complete diff, spec, user constraints, report, actual validation evidence, and `pr` guidance. Reuse a correct description; otherwise invoke `pr` with the spec, tickets, complete diff, decisions, report, and actual validation evidence to prepare the final body. Preserve closing references and disclose missing before evidence. Save the body verbatim to a temporary Markdown file and update only changed title/body values using `gh pr edit <pr-number> --repo <owner/repo> --title <title> --body-file <body-file>`. Push any remaining reviewed commits normally. Verify the remote head SHA equals the final reviewed SHA before marking the draft ready with `gh pr ready <pr-number> --repo <owner/repo>`.

Ensure `status/ready-for-review` exists, creating it if missing while preserving existing label settings. Remove every other `status/` label and add `status/ready-for-review`, preserving non-status labels. Verify the open PR's URL, repository/head-repository identity, base, head branch/SHA, intended title/body and closing references, ready state, and labels with `gh pr view`, including `url,state,isDraft,baseRefName,headRefName,headRefOid,headRepository,headRepositoryOwner,title,body,labels`. The head SHA must equal the final reviewed SHA and the review-ready label must be the only status label. Defer human review requests until merge readiness or a blocked handoff under the shared identity instructions.

If a resumed PR already satisfies all these conditions with verified current validation, attach and return it without regenerating the description, rerunning checks, pushing, or editing GitHub. Otherwise repair only pending work. Attach the verified PR when supported. Delete temporary body files after success; preserve the prepared body and report the exact blocker on failure. Do not add PR entries to the implementation report or commit report changes after publication merely to record its URL.

## Implementation report

For a GitHub spec, fetch its authoritative issue number and URL. Create `docs/implementations/<spec-gh-issue-id>.md` in the integration checkout, using the spec issue number, not a child ticket or issue title. Reuse that report on resumed runs; verify its recorded spec URL before editing and preserve unrelated content. For a local spec, use its established filesystem-safe identifier instead of a GitHub issue number.

Maintain one concise report containing:

- Spec and ticket pointers, repository identity, absolute integration checkout path, integration branch, and original pinned base SHA for recovery.
- A brief implementation summary, material decisions and tradeoffs, approved deviations with their approval source and scope, and limitations. State when there are no approved deviations; omit other empty categories.
- Validation and review evidence pointers, unresolved failures and acceptance gaps, and unavailable before evidence. Existing results may be summarized with the commit they cover; final results belong in the validation record below.
- Pointers to relevant tests, commits, CI runs, or existing stable evidence URLs.

Replace superseded check and review summaries rather than accumulating a round-by-round narrative or intermediate commit catalogue. Retain decisions, approvals, limitations, and unresolved findings. Create additional evidence files only when required by the spec or repository instructions, or needed to substantiate a finding that existing references cannot establish. Keep routine raw logs and intermediate captures outside the committed report; retained evidence must exclude secrets and unrelated private material.

Create the report during implementation and update decisions, limitations and evidence pointers before each review round's commit and checks so they are included in review. Keep final check and review outcomes in `<absolute-git-common-dir>/implement-it/<spec-key>/validation.json`, outside tracked files. Record repository, checkout, original base, exact checked HEAD, commands and exit statuses, evidence paths, both review outcomes and reviewed SHA, and relevant environment/check configuration. Replace the record atomically under integration ownership; preserve it for recovery and return its absolute path with the report and final reviewed SHA. Verify referenced evidence before reuse. Inaccessible, incomplete or stale evidence requires fresh validation.

After checks or reviews finish, update that record and the PR description or final response rather than committing a report-only results update. Any committed change, including a necessary report correction, requires the gate on the new SHA. Record blocked progress before its review when possible; final blocked outcomes also belong in the validation record.

## Issue status

Resolve each issue's repository and number from its authoritative pointer. Fetch its current labels with `gh issue view --repo <owner/repo> <number> --json labels`. Ensure `status/in-progress` exists in that repository; create it with `gh label create 'status/in-progress' --repo <owner/repo>` if absent, preserving existing label settings. Use `gh issue edit` to remove every current label starting with `status/` and add `status/in-progress`, preserving all other labels. Pass the exact label names through `--remove-label` and `--add-label`.

Fetch the labels again and verify that `status/in-progress` is the only label starting with `status/` and every previous non-status label remains. If the update or verification fails, report the blocker and leave implementation of that issue incomplete.

## Review and fix

Apply this check execution rule to all workers:

Run independent read-only checks concurrently when repository instructions permit and their outputs, ports, fixtures, and resources do not conflict. Preserve build-before-test dependencies, serialize suites sharing browser/server state, and avoid running a second build when a test command already builds. Await every command and retain its exit status and evidence; all required checks must pass before PR readiness or gate completion.

1. Wait for all implementation and merge work to finish. Update the implementation report, then commit only the task's changes on the integration branch so the review includes them, preserving unrelated user changes. Record the integration `HEAD` SHA and run the repository's required checks.
2. Invoke `code-review` against the original pinned base SHA, supplying the authoritative spec and tickets. For changes to asynchronous jobs or state machines, require the Spec reviewer to trace terminal outcomes through queued follow-ups, attached requests, retries/continuation and mixed-success execution where applicable. Evaluate observable state and side effects, including request counts, and require regression coverage for confirmed counterexamples. Review the entire integration diff each round, including previous fixes. Preserve its independent Standards and Spec subagents and their separate reports.
3. If either axis reports findings, dispatch a single **implementer subagent** with all findings, both reports, the spec pointers, the reviewed SHA, and any failed checks. It must fix every finding within the approved spec, use the upstream implementation and TDD workflow, and report its commits, validation results, and any unresolved findings. Integrate its work through the upstream merger workflow, then repeat from step 1. Failed checks also require an implementer fix round even when the review reports no findings.
4. The gate passes only when the latest complete review reports **zero findings on both axes**, all required checks pass, the integration `HEAD` still equals the reviewed SHA, and no task changes remain uncommitted. A skipped axis, failed or incomplete review, empty diff, or unresolved finding leaves the gate unmet. Any subsequent implementation change requires another review.

Keep the original spec and standards authoritative. Fix findings rather than hiding them, weakening checks, or changing requirements to obtain a clean report. If a finding appears mistaken, give the next review the concrete counterevidence; it remains unresolved until that review withdraws it.

There is no preset round limit. Continue while actionable work remains. Before a blocked handoff, investigate feasible alternatives within the existing authorization and requirements, such as a different reference or local acquisition instead of redistribution. Keep access, licensing and source-activation gates intact. Record the alternatives investigated, their evidence and why each is insufficient; distinguish an untried approach from an established external dependency. Hand off only when remaining progress requires a specific user decision, unavailable access, or an external change; report that dependency and outstanding findings, preserve the work, and leave the gate unmet. If the same findings recur after a fix, re-examine the cause and change the fix rather than repeating the same attempt.

## Finish

After the gate passes, complete PR readiness and resume issue-tracker finalization, then release integration ownership as described above. Retain the reviewed integration branch and usable checkout for the caller; clean up only temporary implementation worktrees that are no longer needed. Report the verified PR URL, repository, base, head repository/branch and SHA, readiness state, implementation report and validation record paths, checkout path, original pinned base SHA, integration branch, number of review rounds, final reviewed SHA, check results, material decisions and evidence pointers, and the zero-finding result for each axis. A blocked run must report its unresolved findings instead of claiming completion.

When changing this workflow, evaluate the publication, draft PR, and integration worktree scenarios in [the shared offline behavior checks](../address-it/references/behavior-checks.md) without GitHub writes.
