---
name: implement-pr
description: Deliver a change as a green, merge-ready pull request. Use when the user says "implement" about an issue URL, a file path, or a change discussed earlier in the conversation, or asks for a change to be "merge ready".
---

# Implement PR

Own the change through a green, review-ready PR. Completion is the merge-ready PR, not the finished code.

## 1. Take ownership of linked work

Read each linked GitHub issue with `gh issue view <number> --json title,body,labels,state,comments`.

For every linked ticket or work item, record ownership before implementation: Use the tracker's assignee field to assign the item to the currently authenticated user. If assignment is unavailable, use the tracker's explicit ownership or in-progress mechanism.

## 2. Establish the contract

Run `git fetch origin <base-branch>` so planning starts from the current base. Read the request, linked tickets or spec, repository instructions, and relevant code before editing. Write a short working contract and a task checklist to a git-ignored file (`.claude/tasks.md` when `git check-ignore -q .claude/tasks.md`, run as its own command, exits 0). Tick items off and add new ones as you find them; after compaction, re-read the file instead of the summary. When the code already exists (invoked after an iteration loop), write the contract from the existing diff. The contract has five parts:

- **Outcome:** observable behavior that must exist.
- **Preserve:** behavior and interfaces that must stay unchanged. For performance-motivated work, include performance.
- **Scope:** files, packages, and systems the request permits changing.
- **Evidence:** focused checks that prove the outcome and preserved behavior, including a benchmark for performance-motivated work.
- **Stop:** the PR, required CI, and requested review state that define completion.

Resolve repository and external facts by inspection or a cheap experiment. Choose defaults that follow existing patterns.

## 3. Implement the smallest complete change

Follow repository conventions and reuse established seams. Add only behavior required by the contract. Keep types precise from the lowest changed boundary to the highest consumer.

Read what the contract's open questions need, then edit. Once a read stops changing the plan, the reading is done: start implementing.

Add focused tests at the stable behavioral seam. Skip tests that only memorialize deleted behavior, duplicate type checks, or restate implementation details.

For visual or interactive work, use the browser, Android emulator or iOS simulator to check the affected states and responsive behavior. Capture evidence needed by the PR.

## 4. Verify

Before review, run the affected package's complete test, typecheck, lint, and build commands that the repository documents, including the test suites its aggregate `check` script leaves out. Record commands and results for the PR. After review or CI fixes, re-run only the checks the fix touches; CI runs the full matrix.

## 5. Review cold

Review spend scales with the diff. Every reviewer is a fresh background subagent that gets the diff command, the contract file path, and only what its axis needs; `$spec-review` also gets the linked tickets. Each subagent's completion notification is your wake signal.

**Base.** Run `git fetch origin <base-branch>` again and diff against `origin/<base-branch>`. A worktree's local base branch lags the remote and pulls unrelated commits into the diff. The review diff is `git diff origin/<base-branch>...HEAD`.

**Depth.** Size the diff with `git diff --shortstat origin/<base-branch>...HEAD`:

- **Light:** under about 50 changed lines that delete, rename, or adjust config, copy or docs without adding behavior. Run `$bug-review` alone.
- **Full:** everything else, and any diff touching auth, permissions, money, persisted data or migrations, concurrency, or a public interface, whatever its size. Run `$bug-review`, `$spec-review` and `$simplicity-review`.

Treat findings as hypotheses:

1. Verify each finding against the contract and current code.
2. Fix every valid, in-scope finding. Out of scope applies only to code the diff leaves untouched; a defect in lines the diff adds is in scope.
3. Record false positives and out-of-scope findings, leaving the change as it stands.
4. Re-run the checks your fixes touched.
5. Re-dispatch only the reviewers whose findings drove a fix, handing each the fix hunks (`git diff <reviewed-sha>..HEAD`) and its prior findings with your verdicts. Repeat until a round raises nothing new, within each reviewer's round cap.

**Round caps.** `$bug-review` and `$spec-review`: 3 rounds, or 5 while a security finding (auth, permissions, data exposure, injection) drives the fix. `$simplicity-review`: 1 round.

Completion: every finding has a recorded verdict (fixed, false positive, or out of scope) in the contract file.

## 6. File and babysit the PR

Commit the complete change, push it, and use the `$file-pr` skill to open the PR.

Use the `$babysit-pr` skill until required CI and review automation are green. It addresses review feedback; re-run the evidence each fix affects.

Finish only when the PR is merge-ready or an external blocker remains, and print the PR URL.
