---
name: neo-code-review
description: >
  Use this skill when the user asks to review or audit source code, a PR, diff, commit,
  or recent changes for bugs, security, performance, tests, compatibility, or
  maintainability, duplicated code or logic across files, or hard-coded values. Also use
  it after an AI agent finishes modifying code to inspect the current uncommitted working
  tree before handoff and report actionable findings with file and line evidence.
compatibility: Requires Python 3.11+ and uv for the Git change helper.
---

# Code Review

Follow this read-only workflow. Report only actionable findings supported by evidence.

## Trigger On

- The user requests a code, PR, diff, commit, security, performance, test, or maintainability review.
- The user asks whether code or logic is duplicated across files, or whether hard-coded values should be centralized.
- An AI Agent finishes modifying code, tests, configuration, or scripts before handoff.

## Workflow

1. **Define the review scope**
   - Use the files or snippets supplied by the user as the primary scope.
   - If the user provides no scope and the current directory is a Git repository, run:
     ```bash
     uv run skills/neo-code-review/scripts/git-diff-reviewer.py --working-tree
     ```
   - Use `--staged` for staged-only changes and `--commit <range>` for a commit range.
   - Read surrounding code, related tests, and existing contracts. If no reviewable input exists, report it and stop.
   - For a working-tree review, include the helper's tracked diff and each non-ignored untracked file as separate inputs.

2. **Load the review rules**
   - Read [review-checklist.md](references/review-checklist.md) before evaluating code.
   - Identify the actual language, framework, and affected behavior from the change. Do not infer unverified rules from filenames.

3. **Run the cross-file consistency scan**
   - Build the comparison set from the review targets and relevant repository source and configuration files. Use `rg --files` and the repository's ignore rules. Exclude dependency, vendor, cache, generated, minified, build, and coverage output unless a file is explicitly in scope.
   - Inventory changed or reviewed functions, classes, validation and authorization rules, state transitions, request or query construction, error handling, and distinctive literals such as URLs, routes, timeouts, retry counts, thresholds, regexes, feature flags, and error messages.
   - Search the comparison set for exact and near-exact matches, then read each match in context. Ignore name and formatting differences when the behavior matches. Treat renamed or slightly rearranged copies as duplicates when their business rules, inputs, side effects, and failure behavior are materially the same.
   - Report only meaningful duplication: copied implementation, duplicated business or validation logic, divergent security or state logic, or repeated non-trivial hard-coded configuration. Do not report a match based only on a common keyword, normal one-time literal, test fixture, snapshot, generated file, or vendor code.
   - For every cross-file finding, cite both file paths and line numbers. Explain the concrete maintenance, divergence, security, or behavior risk and recommend a specific shared helper, constant, configuration source, or other single source of truth.
   - If the user supplied only a snippet or specific files without repository context, state in `## Validation` that cross-file verification was unavailable. Never invent repository matches or line evidence.

4. **Analyze risk**
   - Prioritize correctness, regressions, security, data consistency, resource lifetime, concurrency, and high-risk test gaps.
   - `🔴 Critical Issues` contain only security vulnerabilities, data loss, incorrect behavior, authorization bypasses, or major regressions.
   - `🟡 Suggestions` contain only actionable, non-blocking issues with a clear impact and remediation direction.
   - Classify ordinary duplicated logic or hard-coded configuration as `🟡 Suggestions`. Classify hard-coded secrets or duplication that creates a demonstrable security or behavior defect as `🔴 Critical Issues`.
   - Do not report preferences, unsupported speculation, or checklist items that were not triggered by evidence.

5. **Produce a concise report**
   - Write in English and preserve file paths and line numbers, such as `src/user.ts:42`.
   - Use this structure. Keep all severity sections and write `None` when a section has no findings:

     ```markdown
     ## 🔍 Review Summary
     - **Status**: `🟢 Ready to deliver`, `🟡 Fix recommended`, `🔴 Delivery blocked`, or `⚪ No reviewable changes`
     - **Scope**: Files or changes that were inspected.

     ## 🔴 Critical Issues
     - **Location**: `path:line`
       - **Problem**: Specific behavioral defect.
       - **Impact**: Verifiable consequence.
       - **Fix**: Concrete remediation direction; include code only when it clarifies the fix.

     ## 🟡 Suggestions
     - **Location**: `path:line`
       - **Type**: Duplicated logic, duplicated hard-coded value, or another applicable category.
       - **Evidence**: The matching location and the relevant behavior or value in each file.
       - **Recommendation**: Specific, non-blocking improvement.

     ## 🟢 Strengths
     - List only strengths directly supported by the change.

     ## Validation
     - State the cross-file comparison scope and any unavailable repository context.
     - List executed tests, builds, and checks. Name any that were not run.
     ```

6. **Apply the delivery gate**
   - If an automatic review finds `🔴 Critical Issues`, cannot establish the review scope, or cannot load the skill, do not declare completion or hand off.
   - After fixing findings, rerun the required checks and review the changes again.
