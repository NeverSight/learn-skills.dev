---
name: testing-implementation
description: Evaluates test implementation and coverage, identifying gaps, weak assertions, and untested paths. Use when auditing test quality, coverage, or testing strategy.
license: CC0-1.0
metadata:
  category: code-quality
allowed-tools: Read Grep Glob Write
disable-model-invocation: true
argument-hint: "[path or scope]"
---

**Target:** $ARGUMENTS

If no target path is given above, review the entire codebase.

---

Evaluate testing implementation for this software project

Analyze:

1. TEST COVERAGE
   - Unit test coverage percentage
   - Integration test presence
   - E2E test coverage
   - Uncovered critical paths

2. TEST QUALITY
   - Test naming clarity
   - Arrange-Act-Assert pattern
   - Test independence
   - Mock usage appropriateness
   - Test data management

3. TEST PATTERNS
   - Test pyramid adherence (unit > integration > E2E)
   - Testing anti-patterns (testing implementation vs behavior)
   - Brittle tests identification
   - Test speed issues

4. MISSING TESTS
   - Error scenarios
   - Edge cases
   - Security tests
   - Performance tests

Provide a test improvement plan with examples.

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is

Remediation: precise code-level fix or config change (snippets welcome) if possible

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
