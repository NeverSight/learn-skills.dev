---
name: test-standards
description: Test quality validation detecting mesa-optimization, happy-path bias, vacuous assertions, and error-swallowing anti-patterns. Use when reviewing test files for quality issues, evaluating test meaningfulness, or ensuring tests validate behavior rather than passing trivially. Supports JavaScript, TypeScript, and Python test frameworks.
---

# Test Standards

Validates test quality through automated scanning and LLM-guided heuristics to detect:
- Mesa-optimization (tests that pass trivially)
- No assertions (tests execute but verify nothing)
- Tautological assertions (always true regardless of implementation)
- Vacuous property checks (only existence, not values)
- Mock-only validation (only verify mocks called, not behavior)
- Happy-path bias (only success tests, no error handling)
- Error-swallowing patterns (catch blocks without assertions)
- Missing async test protection (`expect.assertions(n)`)
- Low assertion density (superficial testing)

## When to Use

Execute test-standards during QA validation:
1. After reviewing test file changes
2. When tests were modified by Action Agent
3. Before approving changes for merge
4. When evaluating test meaningfulness
5. During test creation/maintenance

## Validation Workflow

### 1. Automated Scanning (Script)

Run script first for deterministic, fast detection:

**Scan specific test files:**
```bash
python scripts/test_quality_scanner.py tests/auth.test.ts tests/api.test.ts --format json
```

**Scan test directory:**
```bash
python scripts/test_quality_scanner.py ./tests --format json
```

**Save report:**
```bash
python scripts/test_quality_scanner.py ./tests --output test-quality-report.json
```

**Exclude patterns:**
```bash
python scripts/test_quality_scanner.py ./tests --exclude node_modules .snapshots --format json
```

### 2. Interpret Scan Results

Parse JSON output and evaluate findings:

**Finding Structure:**
```json
{
  "category": "no_assertions|tautological_assertion|vacuous_check|mock_only_validation|...",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "file": "tests/auth.test.ts",
  "test_name": "validates user login",
  "line": 42,
  "pattern": "regex pattern or description",
  "context": "relevant code snippet",
  "message": "human-readable description"
}
```

**Report Structure:**
```json
{
  "files_scanned": 15,
  "total_tests": 128,
  "total_findings": 12,
  "findings_by_severity": {
    "CRITICAL": 2,
    "HIGH": 5,
    "MEDIUM": 4,
    "LOW": 1
  },
  "findings": [...],
  "test_stats": [
    {
      "file": "tests/auth.test.ts",
      "total_tests": 25,
      "tests_with_assertions": 23,
      "tests_without_assertions": 2,
      "async_tests_without_protection": 3,
      "error_tests": 5,
      "success_tests": 18,
      "avg_assertions_per_test": 3.2
    }
  ],
  "summary": {
    "no_assertions": 2,
    "tautological_assertions": 1,
    "vacuous_checks": 3,
    "mock_only_validation": 2,
    "missing_assertion_count": 3,
    "error_swallowing": 1,
    "low_assertion_density": 0,
    "happy_path_bias": 1
  }
}
```

**Severity Guidelines:**
- **CRITICAL**: No assertions, tautological assertions - BLOCK merge immediately
- **HIGH**: Vacuous checks, mock-only validation, error swallowing - Require fixes
- **MEDIUM**: Happy-path bias, missing assertion count, low density - Review and justify
- **LOW**: Minor quality issues - Optional fixes

### 3. LLM Heuristic Review (Context-Dependent)

After automated scanning, apply judgment for patterns the script cannot detect:

#### Test Assertion Weakening

Compare test changes in git diff to detect semantic weakening:

**Indicators of Weakening:**
- Reduced assertion count without clear reason
- Replaced specific assertions with generic checks
- Removed edge case validations
- Changed from behavior validation to mock validation only

**Example - Weakened Test:**
```typescript
// Before (git diff -)
expect(response.data).toMatchObject({
  id: expect.any(String),
  status: 'active',
  count: expect.any(Number)
});

// After (git diff +)
expect(response.data).toBeDefined(); // ❌ Lost specificity
```

**Action**: Flag as HIGH severity, request Action Agent restore specific assertions.

#### Scope Alignment

Verify test changes align with issue scope:

**Legitimate Changes:**
- Tests added for new feature functionality
- Tests updated to match changed implementation
- Error handling tests added for new edge cases

**Suspicious Changes:**
- Unrelated tests modified without explanation
- Tests removed without justification
- Test patterns changed across multiple files beyond issue scope

**Action**: Request clarification or justification in scratch notes.

#### Test Coverage Gaps

Identify functions/features lacking tests:

**Review Approach:**
1. Read implementation changes from git diff
2. Identify new functions, branches, error paths
3. Check if corresponding tests exist
4. Flag missing coverage for critical paths

**Action**: Request additional tests for uncovered critical functionality.

### 4. Generate Validation Report

Combine automated findings with heuristic review:

```markdown
## Test Standards Validation for [ISSUE-ID]

### Automated Scan Summary
- Test Files Scanned: X
- Total Tests: Y
- Total Findings: Z
- CRITICAL: A findings
- HIGH: B findings
- MEDIUM: C findings

### Critical Findings (BLOCK)
1. [test_name in file:line] - No assertions found
2. [test_name in file:line] - Tautological assertion: expect(true).toBe(true)

### High Priority Findings (FIX REQUIRED)
1. [test_name in file:line] - Only validates mocks, not behavior
2. [test_name in file:line] - Catch block swallows errors without assertions

### Medium Priority Findings (REVIEW)
1. [file:0] - Happy-path bias: 15 success tests, 0 error tests
2. [test_name in file:line] - Async try/catch missing expect.assertions(n)

### Heuristic Review
- **Assertion Quality**: PASS/WARN/FAIL with examples
- **Coverage Completeness**: PASS/WARN/FAIL with gaps identified
- **Scope Alignment**: PASS/WARN with details

### Test Statistics
- Average assertions per test: 3.2
- Tests without assertions: 2 (8%)
- Async tests without protection: 3 (12%)
- Error test coverage: 20%

### Recommendation
[APPROVED | CHANGES REQUIRED | BLOCKED]

### Action Items
[Specific fixes needed with file:line references]
```

## Finding Categories Reference

### no_assertions (CRITICAL)
Test executes code but makes no assertions. Always indicates a problem.

### tautological_assertion (CRITICAL)
Assertion always true regardless of implementation (e.g., `expect(true).toBe(true)`).

### vacuous_check (HIGH)
Only checks property exists without validating value (e.g., only `.toBeDefined()`).

### mock_only_validation (HIGH)
Test only verifies mocks were called, doesn't validate actual behavior.

### missing_assertion_count (MEDIUM)
Async test with try/catch missing `expect.assertions(n)` protection.

### error_swallowing (HIGH)
Catch block swallows errors without assertions (test always passes).

### low_assertion_density (LOW)
Test has suspiciously few assertions for its length (may be superficial).

### happy_path_bias (MEDIUM)
File has only success-path tests, no error handling tests.

## Integration with QA Protocol

Execute test-standards at **Step 3: Change Review (Diff)** or **Step 7: Tests (Right-Sized)** in QA workflow:

1. Action Agent completes implementation with test changes
2. **Run test-standards script on changed test files**
3. **Interpret automated findings**
4. **Apply LLM heuristics for semantic review**
5. Generate validation report
6. If CRITICAL or multiple HIGH findings:
   - BLOCK validation
   - Report to Traycer with specific file:line references
   - Delegate to Action Agent for fixes
   - Re-run validation after fixes
7. Continue with remaining QA steps

## Quick Reference

**For detailed examples and patterns**, read `references/test-quality-patterns.md`:
- Mesa-optimization anti-patterns with code examples
- Good vs bad test structures by language
- Async test protection patterns
- Happy-path bias examples
- Error-swallowing anti-patterns

## Resources

- **Scripts**:
  - `scripts/test_quality_scanner.py` - Automated test quality detection

- **References**:
  - `references/test-quality-patterns.md` - Detailed patterns and examples

## Notes

- Run script first for deterministic checks (fast, reliable)
- Use LLM heuristics for semantic/contextual evaluation
- Always provide file:line references in reports
- CRITICAL findings must block merge
- Document justified exceptions in test comments
