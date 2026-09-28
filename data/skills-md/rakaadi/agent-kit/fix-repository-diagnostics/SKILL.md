---
name: fix-repository-diagnostics
description: Close repository diagnostic findings from TypeScript, ESLint, and React Doctor. Use when asked to verify or fix project-wide tsc errors, ESLint violations, React Doctor findings, or a scoped batch from any of those tools.
---

# Fix Repository Diagnostics

Run a closed diagnostic loop: establish the baseline, verify each finding, fix its root cause, rerun the finding's source, and report the remaining state.

Follow explicit user instructions when they override this skill's defaults. For fix requests, carry the selected batch through verification and reporting without pausing for routine allocation or implementation choices. Continue independent authorized work when a finding is blocked or requires approval.

## 1. Establish Scope

1. Work from the repository root and read the applicable repository instructions.
2. Inspect the worktree before editing. Preserve user-owned changes and identify files already modified by others.
3. Use the requested tools, files, rules, or findings as the scope. When the request gives no narrower scope, run all three project-wide diagnostics:

   ```bash
   nub run lint
   nubx tsc --noEmit
   nubx react-doctor@latest
   ```

4. Run diagnostics separately so each exit status and output remains attributable to one tool.
5. Record findings in stable tool-output order with their tool, rule or error code, file, location, and message. Record a command failure as a blocker, not as a clean result.

Complete this phase only when every requested diagnostic has either produced a baseline or has an exact recorded blocker.

## 2. Verify and Build a File-Complete 15-Issue Batch

Treat one distinct diagnostic record as one issue. Exact duplicate records from the same tool count once.

1. Use 15 issues as the base selection cap. File closure may extend the final batch beyond 15.
2. Aim for an even distribution across the requested diagnostic types, starting with five issues per type when all three are in scope. Redistribute unused capacity as evenly as practical among types with more verified findings. Choose the allocation using judgment; file closure and root-cause grouping take precedence over balance.
3. Within each type, consider findings in their original output order unless the request explicitly prioritizes particular findings.
4. For each candidate considered:
   - Open the referenced code and confirm the finding still applies to the current worktree.
   - Trace enough surrounding code, types, configuration, and dependency versions to identify the root cause.
   - Treat React Doctor findings as hypotheses until the referenced implementation and installed package versions confirm them.
   - Treat dependency findings as report-only unless the user explicitly authorizes the specific manifest or dependency change. Classify unapproved findings as approval-required, and check package-manager and peer-dependency relationships; absence from application imports is not evidence that a dependency is unused.
   - Classify the finding as reproducible, stale, duplicate, false positive, approval-required, already owned by another change, or blocked, and keep the supporting evidence.
5. Count only reproducible findings toward the batch. Continue selecting until the batch reaches 15 issues or no eligible findings remain.
6. Make each selected file a closure group across the requested diagnostics:
   - When any finding selects a file, verify every TypeScript, ESLint, and React Doctor finding for that file that is in the run's scope.
   - Include every reproducible finding for that file in the same batch, even when the findings have different types or root causes.
   - Count closure findings toward the base cap until it is reached. Include every remaining finding in an already-selected file as an additional issue beyond the cap; never defer part of a selected file.
   - Stop selecting new files after the batch reaches or exceeds 15 issues.
7. Keep findings that one root-cause change is expected to resolve in the same batch. Count every affected diagnostic record, and defer an oversized group only before any of its files is selected; file closure takes precedence after selection.
8. Freeze the selected batch before editing. Record the per-type counts, additional issues beyond 15, and the reason for any batch below 15. Defer all unselected findings to a later run.

Complete this phase when the batch includes every reproducible, authorized in-scope finding in each selected file, only file closure extends it beyond 15, and excluded findings have recorded classifications and evidence. Keep approval-required dependency findings outside the batch.

## 3. Fix the Root Cause

1. Make the smallest in-scope change that resolves the verified cause while preserving behavior.
2. Follow the repository's current React Native, Expo, React, TypeScript, and lint conventions.
3. Prefer a real type, control-flow, or component correction. Use a suppression, unsafe cast, rule change, or generated-file edit only when evidence shows it is the correct fix and the task authorizes its scope.
4. Keep dependency findings report-only unless the user explicitly approves the specific change. Do not edit dependency manifests or lockfiles, or add, remove, install, uninstall, or update packages, without that approval.
5. Avoid unrelated refactors, formatting churn, and opportunistic cleanup.
6. After each coherent fix, inspect the diff and check that every changed line serves an accounted-for finding.

Complete this phase when every selected issue is fixed or has an exact unresolved blocker and all edits stay within the selected root-cause groups. A selected file with unresolved findings remains incomplete; report that state explicitly.

## 4. Close the Loop

1. For modified JavaScript or TypeScript files, run the repository's changed-file ESLint command with auto-fix and inspect any resulting edits:

   ```bash
   bunx eslint <changed files> --fix
   ```

2. After the final edits, rerun the exact project-wide commands for the requested diagnostics to verify the selected findings and file closure.
3. Run the narrowest relevant tests when a fix changes runtime behavior. Repeat or broaden checks only when subsequent edits, failures, or unresolved concerns justify them.
4. Inspect the final diff for scope, correctness, accidental edits, and conflicts with pre-existing work.
5. Compare the final diagnostics with the baseline. A nonzero project-wide command may remain when deferred or out-of-scope debt exists; prove that the selected findings disappeared and that modified files gained no new findings.

Complete this phase when fresh output accounts for every selected issue and confirms file closure, or exact blockers explain what remains unresolved or unverified. Claim a modified file is complete only when it has no remaining in-scope finding from any requested diagnostic type.

## 5. Report

Use this summary:

- TypeScript: `<fixed>` fixed, `<remaining>` remaining
- ESLint: `<fixed>` fixed, `<remaining>` remaining
- React Doctor: `<fixed>` fixed, `<remaining>` remaining
- Verification: each final diagnostic command and exit status
- Blockers: exact blockers, or `none`
- Dependency findings awaiting approval: each finding and the evidence needed for a human decision, or `none`

### Additional Fixes

- Total: `<count>` issues fixed beyond the 15-issue base cap
- By file: `<path>: <count>`, or `none`

Count `fixed` from selected baseline issues that disappeared in fresh output, including additional fixes. Count an additional fix when a reproducible baseline issue beyond the first 15 was included to complete a selected file and disappeared in fresh output. Count `remaining` from all distinct findings in the final full diagnostic output, including deferred and out-of-scope findings. Report `unknown` instead of zero when a diagnostic cannot complete. Omit root causes and per-finding narratives.

State that a tool passes only when its fresh full command exits successfully. Otherwise report the narrower verified result without describing the repository as clean.
