---
name: execution-report
description: Use when generating an implementation report after feature completion documenting what was done, divergences from plan, and test results
---

# Execution Report

Review and deeply analyze the implementation you just completed.

## Context

You have just finished implementing a feature. Before moving on, reflect on:

- What you implemented
- How it aligns with the plan
- What challenges you encountered
- What diverged and why

## Step 1: Read PROGRESS.md

**MANDATORY FIRST STEP:**

1. Read `PROGRESS.md` to find the execution phase notes for this feature
2. Review what was accomplished and what's left to do
3. Use this context to inform your execution report

## Generate Report

**CRITICAL: Create report in `.agents/execution-reports/` folder**

### Step 1: Determine Feature Name

Extract the feature/module name from PROGRESS.md or the plan file path.
Example: "module-5-multi-format-enhancement" from plan path `.agents/plans/module-5-multi-format-enhancement.md`

### Step 2: Summarize Test Coverage

Before writing the report, inspect the test files that were added or modified during this implementation:

1. Use `git diff --name-only HEAD` (or diff against the base branch) to identify changed files
2. Filter for test files (files under `tests/`, named `test_*.py`, `*.test.ts`, `*.spec.*`, etc.)
3. For each changed test file, read it and identify:
   - What functions/endpoints/behaviors are tested
   - What scenarios are covered (happy path, error cases, edge cases)
4. Produce a concise bulleted list — one sentence per item — capturing what each test validates

You will include this list in the report under `## What was tested`.

### Step 3: Create Detailed Execution Report

**Create file:** `.agents/execution-reports/{feature-name}.md`

**Use Write tool to create this file with the following structure:**

```markdown
# Execution Report: [Feature Name]

**Date:** [Current date]
**Plan:** [path to plan file]
**Executor:** [team-based/sequential/etc]
**Outcome:** ✅ Success / ⚠️ Partial / ❌ Failed

---

## Executive Summary

[2-3 sentence summary of what was implemented and outcome]

**Key Metrics:**
- **Tasks Completed:** X/Y (Z%)
- **Tests Added:** X
- **Test Pass Rate:** X/Y (Z%)
- **Files Modified:** X
- **Lines Changed:** +X/-Y
- **Execution Time:** ~X minutes
- **Alignment Score:** X/10

---

## Implementation Summary

[Detailed breakdown of what was implemented, organized by phase/wave/category]

---

## Divergences from Plan

### Divergence #1: [Title]

**Classification:** ✅ GOOD / ❌ BAD / ⚠️ ENVIRONMENTAL

**Planned:** [what plan specified]
**Actual:** [what was implemented]
**Reason:** [why divergence occurred]
**Root Cause:** [plan gap, environmental, framework behavior, etc]
**Impact:** [positive/negative/neutral - describe]
**Justified:** Yes/No

[Repeat for each divergence]

---

## Test Results

**Tests Added:** [list with descriptions]
**Test Execution:** [show test output summary]
**Pass Rate:** X/Y (Z%)

---

## What was tested

[Bulleted list — one sentence each — describing what each test validates. Derived from inspecting changed test files (Step 2 above). Focus on the scenario/behavior, not the file name.]

- [e.g., `POST /ingest` returns 422 when the payload is missing required fields]
- [e.g., Semantic search returns ranked results ordered by cosine similarity]
- [e.g., KB entry creation is atomic — partial writes are rolled back on failure]

---

## Validation Results

| Level | Command | Status | Notes |
|-------|---------|--------|-------|
| 1 | [command] | ✅/❌ | [notes] |
| 2 | [command] | ✅/❌ | [notes] |

---

## Challenges & Resolutions

**Challenge 1:** [description]
- **Issue:** [what went wrong]
- **Root Cause:** [why it happened]
- **Resolution:** [how it was fixed]
- **Time Lost:** [estimate]
- **Prevention:** [how to avoid in future]

[Repeat for each challenge]

---

## Files Modified

**[Category] (X files):**
- `path/to/file1` - [description] (+X/-Y)
- `path/to/file2` - [description] (+X/-Y)

**Total:** X insertions(+), Y deletions(-)

---

## Success Criteria Met

- [x] Criterion 1
- [x] Criterion 2
- [ ] Criterion 3 (deferred/skipped)

---

## Recommendations for Future

**Plan Improvements:**
- [specific suggestions]

**Process Improvements:**
- [specific suggestions]

**CLAUDE.md Updates:**
- [specific patterns to document]

---

## Conclusion

**Overall Assessment:** [summary paragraph]
**Alignment Score:** X/10 - [rationale]
**Ready for Production:** Yes/No - [reasoning]
```

### Step 4: Update PROGRESS.md

**Use Edit tool to add/update in PROGRESS.md under the current feature:**

```markdown
### Reports Generated

**Execution Report:** `.agents/execution-reports/{feature-name}.md`
- Detailed implementation summary
- Divergences and resolutions
- Test results and metrics
- Team performance analysis (if applicable)
```

**Do NOT include the full report content in PROGRESS.md - only the reference.**