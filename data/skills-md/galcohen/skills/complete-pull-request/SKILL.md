---
name: complete-pull-request
description: Take an existing pull request from proposed change to verified, merge-ready completion. Use whenever the user asks to finish, finalize, rescue, revive, update, unblock, babysit, shepherd, or take a PR to completion—even if they only provide a PR URL. First independently verify that the underlying problem is still real and important and that the proposed solution is directionally correct; stop before changing anything when it is not. Then update the PR with its base branch, resolve conflicts and valid review feedback, repair relevant CI failures, run the project’s full validation, and report whether it is truly merge-ready.
disable-model-invocation: true
---

# Complete Pull Request

Take ownership of an existing pull request. The PR may have been opened by a bot or another agent and may have gone stale. Do not assume that its description, implementation, review state, or earlier CI results are still correct.

The goal is a reviewed, current, verified, merge-ready PR—not merely a green check or a conflict-free branch.

## Operating contract

- Treat the PR URL or number as the source of scope. Read repository instructions before acting.
- Start with independent read-only review. The user's request to complete a PR authorizes ordinary in-scope edits, commits, and pushes to that PR after the verdict gate below.
- Do not merge, close, convert to draft, retarget, or rewrite published history unless the user explicitly asks or repository instructions clearly make that part of the requested workflow.
- Do not hide failures by weakening tests, skipping checks, dismissing review threads, or changing CI requirements.
- Preserve unrelated user changes. If the available worktree is dirty, use an existing clean PR worktree or create a separate worktree when safe; otherwise stop and explain the collision.
- Prefer the repository's existing tooling and conventions. Do not introduce new dependencies or broad refactors just to finish the PR.
- Use related installed skills for GitHub review comments, failing GitHub Actions checks, and implementation-complete validation when available, while retaining the verdict and mutation boundaries in this skill.

## Phase 1: Establish reality before changing anything

Gather enough evidence to explain the PR without trusting its summary:

1. Read the PR title, description, author, draft state, head/base branches, commit list, changed files, complete diff, linked issues, labels, reviews, unresolved conversations, and current checks.
2. Read repository guidance such as `AGENTS.md`, contributor docs, CI workflows, build manifests, and test commands relevant to the changed area.
3. Trace the affected production code and tests beyond the diff. Understand the current behavior, the claimed failure, and the architectural conventions the patch should follow.
4. Check how the base branch has evolved since the PR opened. Determine whether later work already fixed, replaced, or invalidated the problem or solution.
5. Reproduce the reported bug or establish it from strong code/test evidence when practical. Distinguish a real current defect from a hypothetical concern or stale report.
6. Review the patch like an independent maintainer: correctness, edge cases, concurrency, security/privacy, compatibility, data migration, user experience/accessibility, tests, and unnecessary scope.

Evidence gathering may use read-only host queries and repository inspection. Do not edit files, switch the shared worktree, commit, push, resolve conversations, or otherwise update the PR before the verdict.

## Verdict gate

State one of these verdicts in the working notes before mutation:

- **PROCEED** — The problem is still real and worth solving; the proposed direction is sound. Implementation defects that can be repaired without changing the fundamental approach are compatible with this verdict.
- **STOP: invalid problem** — The behavior is no longer present, is intended, is already fixed, or lacks credible evidence. Stop without modifying the PR.
- **STOP: wrong solution** — The approach is fundamentally unsafe, architecturally wrong, or solves a different problem. Stop without modifying the PR.
- **PAUSE: decision required** — Correctness depends on a product, security, migration, compatibility, or scope choice the user has not authorized. Do not guess.

For STOP or PAUSE, return a concise assessment with supporting file/line, check, issue, or discussion evidence; explain what would need to change before work could continue. Do not “salvage” the PR by silently replacing its premise.

## Phase 2: Make a valid PR current

Only continue after **PROCEED**.

1. Refresh PR and base-branch state because it may have changed during analysis.
2. Confirm the exact remote head branch, push permissions, current worktree/branch, and whether the repository requires merge or rebase updates.
3. Bring the base into the PR branch:
   - Prefer merging the current base into the head when no convention is stated; it avoids rewriting a published branch.
   - Rebase only when requested or clearly required by repository convention. Push rebased history with `--force-with-lease`, never plain `--force`.
   - Never push the base branch or an ambiguously resolved branch name.
4. Resolve conflicts semantically. Compare both sides and preserve their intended behavior; do not mechanically choose “ours” or “theirs.”
5. Inspect the resulting aggregate diff against the current base. Base updates can make code redundant or subtly change the solution, so repeat the correctness verdict if the effective behavior changed materially.
6. Run a fast build or focused tests after conflict resolution before stacking more changes on top.

If the PR comes from a fork or the head branch is not writable, do not push to a substitute branch without permission. Prepare the smallest safe patch or exact handoff instructions and report the access blocker.

## Phase 3: Resolve implementation and review issues

Build a single action list from your independent review, unresolved human threads, requested changes, bot findings, and current CI failures.

For each item:

1. Verify it against the latest code; stale feedback may no longer apply after the base update.
2. Classify it as **address**, **already resolved/stale**, **defer**, or **needs decision**.
3. Address every valid in-scope correctness, security, regression, test, or maintainability issue necessary for this PR to merge safely.
4. Add or update tests that demonstrate the bug and protect the corrected behavior. Prefer a regression test that fails for the original behavior and passes for the repaired implementation.
5. Keep fixes cohesive and within the PR's purpose. Surface valid out-of-scope work rather than expanding indefinitely.
6. Reply to or resolve a review conversation only after the fix is present and verified. Never dismiss a requested change merely to make the UI appear clean.

When feedback conflicts with the PR's goal or another reviewer, explain the conflict and pause for the smallest necessary decision.

## Phase 4: Validate like CI

Discover the project's actual commands rather than assuming a toolchain. Map local validation to repository instructions and required CI workflows.

Run, in a useful fail-fast order:

1. Formatting and lint checks.
2. Type checking or compilation.
3. Focused tests for rapid feedback.
4. The full unit, integration, and end-to-end suite required by the repository.
5. Coverage, generated-file checks, migrations, or platform builds when configured.

Then push the focused commits to the PR branch and monitor required checks to a terminal result. For failures:

- Reproduce and fix failures caused by the PR.
- Re-run a suspected flaky job only after collecting evidence that the failure is nondeterministic; do not call a red job flaky by intuition.
- Identify infrastructure failures and pre-existing base-branch failures with links or comparative evidence. Do not claim “all tests pass” when a required check remains red or was not run.
- If local validation is impossible, say exactly why and rely on CI only to the extent the checks cover the gap.

After every pushed fix, confirm that the PR head SHA shown by the host matches the commit you validated. Re-read the aggregate diff, unresolved threads, approvals, mergeability, and required checks; earlier green results may belong to an obsolete SHA.

Before declaring the PR complete, if `code-review-changes` was not run against the final diff, apply the `code-comments` skill's self-check to every comment the diff added or stranded.

## Completion standard

A PR is **merge-ready** only when all of the following are true:

- The original problem remains valid and the final solution is correct against the current base.
- The branch contains the current base and the host reports no merge conflicts.
- All necessary in-scope feedback is addressed, with no unresolved requested changes that require action.
- Required local validation and required remote checks pass for the current head SHA, or any exception is explicitly documented and acceptable under repository policy.
- The final diff is focused, contains no accidental files or secrets, and has adequate regression coverage.
- Required approvals and policy gates are satisfied.

Do not equate “code changes complete” with “PR merge-ready.” Missing permission, unavailable infrastructure, pending human approval, or a required external check is a blocker to report, not a reason to overclaim.

## Final report

Lead with one status: **Stopped**, **Needs decision**, **Blocked**, or **Merge-ready**.

Include:

- **Verdict:** why the problem and final approach are valid, or why work stopped.
- **Changes:** base update strategy, conflicts resolved, implementation changes, and feedback disposition.
- **Validation:** exact local commands and outcomes; remote checks and the verified head SHA.
- **Remaining:** pending approvals, external failures, deferred follow-ups, or “none.”
- **PR:** link and whether it was updated. State explicitly that it was not merged unless the user asked for and received a merge.

Keep intermediate updates brief, especially while builds or checks run, but persist until checks reach a meaningful terminal state or a genuine external blocker remains.
