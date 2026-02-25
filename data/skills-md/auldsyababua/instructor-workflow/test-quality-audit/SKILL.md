---
name: Test Quality Audit
description: Scan test files for anti-patterns including mesa-optimization, disabled tests, trivial assertions, and error swallowing
category: validation
usage: qa, action, backend
version: 1.0
created: 2025-11-05
converted_from: docs/agents/shared-ref-docs/test-quality-red-flags.md
---

# Test Quality Audit

## When to Use

Use this skill when you need to:

- **Test review** (QA Agent): Validate test quality during code review
- **Test audit** (QA Agent): Systematic audit of test files for anti-patterns
- **Code review** (Any Agent): Check for mesa-optimization or happy-path testing
- **Pre-merge validation** (QA Agent): Ensure tests are meaningful before PR approval

**Triggers**:
- During QA review when test files are modified
- When code review shows test changes unrelated to feature
- Before approving PR with test modifications
- When tests are failing and you suspect quality issues
- Systematic test audit for entire codebase or feature area

**Red Flags to Watch For**:
- Tests weakened (fewer assertions, replaced checks, removed edge cases)
- Assertions removed or weakened
- Error handling bypassed
- Tests disabled without explanation

## Workflow

### Step 1: Identify Test Files to Audit

**For code review (PR-specific)**:
- Scan only test files modified in the PR
- Focus on changes to existing tests (not new test creation)
- Look for test weakening patterns in diff

**For systematic audit (codebase-wide)**:
- Scan all test files in specified directories
- Common test file patterns: `*.test.js`, `*.spec.ts`, `*_test.py`, `test_*.py`
- Organize findings by severity

### Step 2: Scan for Anti-Patterns

Run the following checks on test files:

#### Check 1: Disabled Tests

**Purpose**: Detect tests that are skipped or disabled in committed code

**Patterns to detect**:
```javascript
// JavaScript/TypeScript:
describe.skip("...", ...)
it.skip("...", ...)
test.skip("...", ...)
it.only("...", ...)  // CRITICAL: Means other tests are ignored
test.only("...", ...)

// Python:
@unittest.skip("...")
@pytest.mark.skip
pytest.skip()
# TODO: fix this test
```

**Scan command**:
```bash
# JavaScript/TypeScript:
grep -rn -E "\.(skip|only)\(" tests/ spec/ __tests__/

# Python:
grep -rn -E "(@unittest\.skip|@pytest\.mark\.skip|pytest\.skip\(|# TODO.*test)" tests/
```

**Severity**:
- **CRITICAL**: `.only()` in committed code (all other tests ignored)
- **HIGH**: `.skip()` without issue reference or justification
- **MEDIUM**: `.skip()` with TODO comment but no timeline

**Pass Criteria**: No disabled tests, OR all disabled tests have:
- Linear issue reference (`# LAW-123: Re-enable when feature X ships`)
- Clear justification for why test is disabled
- Timeline for re-enabling

#### Check 2: Trivial Assertions

**Purpose**: Detect assertions that don't validate meaningful behavior

**Patterns to detect**:
```javascript
// JavaScript/TypeScript:
expect(true).toBe(true)
expect(result).toBeDefined()
expect(response).toBeTruthy()
expect(error).toBeFalsy()  // Error swallowing!

// Python:
assert True
assert result is not None
assert response  # Vague assertion
```

**Scan command**:
```bash
# JavaScript/TypeScript:
grep -rn -E "(expect\(true\)|expect\(false\)|\.toBeTruthy\(\)|\.toBeFalsy\(\)|\.toBeDefined\(\))" tests/ spec/

# Python:
grep -rn -E "(assert True|assert False|assert [a-zA-Z_]+ is not None)" tests/
```

**Severity**:
- **HIGH**: Assertion on boolean literals (`expect(true).toBe(true)`)
- **MEDIUM**: Vague assertions without specific value checks
- **MEDIUM**: `toBeDefined()` without validating actual value

**Pass Criteria**: All assertions validate specific expected values or behaviors

#### Check 3: Error Swallowing

**Purpose**: Detect try/catch blocks that suppress errors without assertions

**Patterns to detect**:
```javascript
// JavaScript/TypeScript:
try {
  // ... test code ...
} catch (error) {
  // No assertion on error - swallowed!
}

// Broad catch without validation:
try {
  await riskyOperation()
} catch (e) {
  console.log(e)  // Logged but not asserted
}
```

```python
# Python:
try:
    # ... test code ...
except Exception:
    pass  # Error swallowed!

# Broad except without assertion:
try:
    risky_operation()
except Exception as e:
    print(e)  # Logged but not asserted
```

**Manual Review Required**: This pattern requires reading test code context

**Check for**:
- Try/catch blocks in tests
- Verify each catch block has assertion on error (or explicitly expects no error)
- Verify catch is not overly broad (`catch (Exception)` is suspicious)

**Severity**:
- **CRITICAL**: Empty catch block or catch with only logging
- **HIGH**: Broad exception catch without specific error assertion
- **MEDIUM**: Catch block that doesn't validate error message/type

**Pass Criteria**: All try/catch blocks either:
- Assert on expected error type/message
- Document why error is ignored (with justification)
- Use specific exception types (not broad `Exception` catch)

#### Check 4: Commented-Out HTTP Calls

**Purpose**: Detect HTTP calls replaced with mocks/constants without rationale

**Patterns to detect**:
```javascript
// JavaScript/TypeScript:
// const response = await fetch('/api/endpoint')
const response = { status: 200, data: mockData }

// await api.createUser(userData)
// Commented out actual API call
```

**Scan command**:
```bash
# Look for commented HTTP calls:
grep -rn -E "// .*(fetch\(|axios\.|http\.|api\.)" tests/ spec/
```

**Severity**:
- **HIGH**: HTTP call commented out and replaced with mock, no explanation
- **MEDIUM**: Mock replaces real call without validating actual API integration

**Pass Criteria**: All mocked HTTP calls either:
- Have integration tests that validate real API calls
- Document why mock is used instead of real call
- Use proper mocking libraries (not inline constants)

#### Check 5: Mesa-Optimization Patterns

**Purpose**: Detect tests weakened to make them pass (instead of fixing code)

**Manual Review Required**: Compare test changes in PR diff

**Patterns to detect**:
- Assertions removed in test modification
- Edge case tests removed
- Expected values changed to match buggy output (instead of fixing bug)
- Validation logic weakened (e.g., regex made less strict)

**Check in PR diff**:
```diff
- expect(result.users).toHaveLength(5)
+ expect(result.users).toHaveLength(3)  // Why changed? Bug or feature?

- expect(response.status).toBe(200)
+ // Status check removed - why?

- expect(() => validateInput('')).toThrow('Input required')
+ expect(() => validateInput('')).not.toThrow()  // Validation removed?
```

**Severity**:
- **CRITICAL**: Assertions removed without explanation
- **CRITICAL**: Expected values changed to match buggy behavior
- **HIGH**: Edge case tests removed
- **MEDIUM**: Validation weakened without clear rationale

**Pass Criteria**: All test weakening changes are justified with:
- Linear issue documenting requirement change
- PR comment explaining why assertion/validation changed
- Confirmation that code behavior (not test) was updated to match new requirement

#### Check 6: Security Script Warnings Suppressed

**Purpose**: Detect security validation bypassed via ignore patterns

**Patterns to detect**:
```javascript
// eslint-disable security/detect-non-literal-fs-filename
// eslint-disable-next-line security/detect-unsafe-regex
// prettier-ignore
```

**Scan command**:
```bash
# Look for security-related linter disables:
grep -rn -E "(eslint-disable.*security|nosec|# noqa.*security)" tests/ src/
```

**Severity**:
- **HIGH**: Security linter disabled without justification
- **MEDIUM**: Broad disable (entire file) instead of line-specific

**Pass Criteria**: All security linter disables have:
- Comment explaining why security rule doesn't apply
- Verification that actual security risk doesn't exist
- Minimal scope (line-specific, not file-wide)

### Step 3: Categorize Findings by Severity

Organize all detected anti-patterns by severity:

**CRITICAL (blocks merge)**:
- `.only()` in committed tests (all other tests ignored)
- Empty catch blocks in tests
- Assertions removed without explanation

**HIGH (requires fix before approval)**:
- Disabled tests without issue reference
- Assertions on boolean literals
- Broad exception catches without assertions
- Security linter disabled without justification

**MEDIUM (request fix, but can approve with warning)**:
- Disabled tests with TODO but no timeline
- Vague assertions (toBeDefined, toBeTruthy)
- HTTP calls mocked without integration test coverage

**INFO (feedback for improvement)**:
- Minor style inconsistencies in tests
- Opportunities to improve test clarity

### Step 4: Report Findings

**If anti-patterns found**, generate a report:

```markdown
**Test Quality Audit Results**

⚠️ **ISSUES FOUND** - Test quality concerns detected

### Critical Issues (Must Fix Before Merge)

1. **Disabled Test with .only()** (tests/user.test.ts:45):
   - Pattern: `it.only("creates user", ...)`
   - Issue: All other tests in suite are ignored
   - Fix: Remove `.only()` or explain why only this test should run

2. **Empty Catch Block** (tests/api.test.ts:89):
   - Pattern: `catch (error) { /* empty */ }`
   - Issue: Errors swallowed without assertion
   - Fix: Assert on expected error or remove try/catch

### High Priority Issues (Fix Recommended)

3. **Disabled Test Without Justification** (tests/auth.test.ts:120):
   - Pattern: `it.skip("validates token expiry", ...)`
   - Issue: No Linear issue or explanation for skip
   - Fix: Add issue reference or re-enable test

4. **Trivial Assertion** (tests/validation.test.ts:67):
   - Pattern: `expect(true).toBe(true)`
   - Issue: Assertion doesn't validate actual behavior
   - Fix: Assert on specific validation result

### Medium Priority Issues (Warnings)

5. **Vague Assertion** (tests/response.test.ts:34):
   - Pattern: `expect(response).toBeDefined()`
   - Issue: Doesn't validate response contents
   - Fix: Assert on specific response fields (status, data, etc.)

**Recommendation**: [BLOCKED | REQUEST FIXES | APPROVED WITH WARNINGS]
```

**If audit passes**, confirm quality:

```markdown
**Test Quality Audit Results**

✅ **PASSED** - No test quality issues found

All checks passed:
- [x] No disabled tests without justification
- [x] All assertions validate specific behaviors
- [x] Error handling includes assertions
- [x] No HTTP calls replaced with inline mocks
- [x] No test weakening detected
- [x] Security linter rules properly applied

**Recommendation**: APPROVED for merge
```

## Reference

### Common Anti-Patterns Examples

#### ❌ Wrong: Disabled Test Without Justification
```javascript
// Bad example:
it.skip("validates email format", () => {
  // Test disabled, no explanation why
})
```

#### ✅ Correct: Disabled Test With Issue Reference
```javascript
// Good example:
// LAW-456: Re-enable when email validation RFC compliance added
it.skip("validates email format per RFC 5322", () => {
  // Test disabled with clear reference to tracking issue
})
```

#### ❌ Wrong: Trivial Assertion
```javascript
// Bad example:
it("creates user", async () => {
  const result = await createUser(userData)
  expect(result).toBeDefined()  // Vague - what about result?
})
```

#### ✅ Correct: Specific Assertion
```javascript
// Good example:
it("creates user", async () => {
  const result = await createUser(userData)
  expect(result.id).toBeDefined()
  expect(result.email).toBe(userData.email)
  expect(result.status).toBe("active")
})
```

#### ❌ Wrong: Error Swallowing
```javascript
// Bad example:
it("handles invalid input", async () => {
  try {
    await processInput(null)
  } catch (error) {
    console.log(error)  // Logged but not asserted
  }
})
```

#### ✅ Correct: Error Assertion
```javascript
// Good example:
it("handles invalid input", async () => {
  await expect(processInput(null)).rejects.toThrow("Input cannot be null")
})
```

#### ❌ Wrong: HTTP Call Replaced With Mock
```javascript
// Bad example:
it("fetches user data", async () => {
  // const response = await fetch('/api/users/123')
  const response = { id: 123, name: "Test User" }  // Inline mock
  expect(response.name).toBe("Test User")
})
```

#### ✅ Correct: Proper Mocking
```javascript
// Good example:
it("fetches user data", async () => {
  // Mock at framework level, not inline
  jest.spyOn(api, "getUser").mockResolvedValue({ id: 123, name: "Test User" })

  const response = await fetchUserData(123)
  expect(response.name).toBe("Test User")
  expect(api.getUser).toHaveBeenCalledWith(123)
})
```

### Related Tools

- `grep`: Pattern matching for anti-pattern detection
- Test frameworks: Jest, Mocha, Pytest (for understanding test syntax)
- AST parsers (advanced): For more sophisticated pattern detection

### Related Documentation

- **Original Reference**: [test-quality-red-flags.md](/srv/projects/traycer-enforcement-framework-dev/docs/agents/shared-ref-docs/test-quality-red-flags.md) (deprecated - use this skill instead)
- **Agent Prompts**:
  - QA Agent: `docs/agents/qa/qa-agent.md` (Test Quality Standards section)
- **Related Skills**:
  - `/security-validate` - Security validation patterns
  - `/test-standards` - Comprehensive test quality validation (if available)
- **Related Ref-Docs**:
  - `test-audit-protocol.md` - Comprehensive test audit procedures

### Quick Reference: Test Audit Commands

**Scan for disabled tests**:
```bash
# JavaScript/TypeScript:
grep -rn -E "\.(skip|only)\(" tests/ spec/ __tests__/

# Python:
grep -rn -E "(@unittest\.skip|@pytest\.mark\.skip|pytest\.skip\()" tests/
```

**Scan for trivial assertions**:
```bash
# JavaScript/TypeScript:
grep -rn -E "(expect\(true\)|expect\(false\)|\.toBeTruthy\(\)|\.toBeFalsy\(\)|\.toBeDefined\(\))" tests/

# Python:
grep -rn -E "(assert True|assert False)" tests/
```

**Scan for commented HTTP calls**:
```bash
grep -rn -E "// .*(fetch\(|axios\.|http\.|api\.)" tests/
```

**Scan for security linter suppression**:
```bash
grep -rn -E "(eslint-disable.*security|nosec|# noqa.*security)" tests/ src/
```

### Version History

- v1.0 (2025-11-05): Converted from test-quality-red-flags.md to skill format
  - Expanded from quick reference to full audit workflow
  - Added scan commands and severity classifications
  - Included examples of correct vs. incorrect patterns
  - Created decision matrix for audit findings
