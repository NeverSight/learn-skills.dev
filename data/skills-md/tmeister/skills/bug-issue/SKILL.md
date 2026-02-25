---
name: bug-issue
description: Diagnose and fix a GitHub issue with a reproduction-first workflow.
---

# Bug Issue

Use this skill to fix bugs or regressions reported in a GitHub issue.

## How this differs from feature-issue

- Focuses on reproducing and diagnosing a problem, not building new functionality.
- Requires a root-cause analysis and regression tests.

## Workflow

1. **Issue analysis**
   - Require an issue number argument. If missing, ask for it.
   - `gh issue view <issue-number>`
   - Summarize expected vs actual behavior.
   - If anything is unclear, interview the user for clarification and reproduction details.

2. **Reproduce**
   - Follow the steps from the issue.
   - If you cannot reproduce, ask for logs, environment details, or a minimal repro.

3. **Root cause**
   - Identify the smallest code path that triggers the issue.
   - Explain the cause in one paragraph before coding the fix.

4. **Fix**
   - Implement the minimal change that addresses the root cause.
   - Keep changes tightly scoped.

5. **Tests and validation**
   - Add or update tests to prevent regression.
   - Run relevant checks and fix diagnostics before proceeding.

6. **Review-first checkpoint**
   - Summarize changes, root cause, and test results.
   - Do not start a commit. The user initiates the commit process when ready.
