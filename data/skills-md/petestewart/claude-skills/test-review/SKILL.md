---
name: test-review
description: Review unit tests for quality, coverage, consistency, and adherence to existing codebase patterns. Use when the user says "/test-review", "review my tests", "check my test coverage", "are my tests good", or needs feedback on test quality and patterns.
version: 1.0.0
---

# Test Review - Unit Test Quality Review Skill

Review unit tests for quality, coverage, consistency, and adherence to established codebase patterns.

## Usage

```
/test-review [path]
```

Where:
- `[path]` - Optional. Directory or file to review. Defaults to the entire test suite.

## Examples

```
/test-review                           # Review all tests
/test-review spec/                     # Review Ruby specs
/test-review tests/unit/               # Review specific directory
/test-review src/__tests__/auth.test.ts  # Review specific file
```

## Review Criteria

This skill evaluates tests against five key areas:

### 1. Test Volume - No Overabundance

**Flags:**
- Multiple tests covering identical behavior with trivial variations
- Excessive permutation testing (e.g., testing every input combination when a few representative cases suffice)
- Tests for trivial getters/setters with no logic
- Redundant assertions that test the same thing multiple ways
- Tests that duplicate integration test coverage unnecessarily

**Guidance:**
- Each test should earn its place by covering distinct behavior
- Prefer fewer, more meaningful tests over many superficial ones
- "One assertion per test" is a guideline, not a rule—test logical units of behavior

### 2. Test Coverage - No Critical Gaps

**Flags:**
- Missing tests for public API methods
- Untested error handling and edge cases
- No tests for critical business logic
- Missing boundary condition tests
- Untested state transitions
- No tests for recently modified code

**Guidance:**
- Focus coverage on code with high complexity or business impact
- Ensure error paths are tested, not just happy paths
- Test boundaries: empty inputs, nulls, max values, off-by-one scenarios

### 3. Uniformity - Consistent Test Structure

**Flags:**
- Inconsistent test naming patterns within the same project
- Mixed describe/context/it nesting styles
- Varying setup patterns (beforeEach vs inline setup)
- Inconsistent assertion styles
- Mixed approaches to test data creation

**Guidance:**
- Tests in the same project should feel like they were written by one person
- Follow the dominant pattern, even if you prefer something else
- Consistency aids readability and maintenance

### 4. Pattern Adherence - Respect Existing Conventions

**This is the most critical review criteria.**

Before suggesting any change, first discover what patterns exist in the codebase:

**Discovery Steps:**
1. Identify the test framework and version in use
2. Find existing test files (minimum 3-5 representative files)
3. Document observed patterns for:
   - File naming (`*.test.ts`, `*_spec.rb`, `*Test.java`, etc.)
   - Directory structure (`__tests__/`, `spec/`, `test/`, etc.)
   - Describe/context/it block organization
   - Setup and teardown approaches
   - Mocking/stubbing libraries and patterns
   - Factory/fixture usage
   - Assertion style
   - Test data patterns

**Flags:**
- Introducing new mocking libraries when one is already established
- Using different factory patterns than existing tests
- Changing describe block organization style
- Introducing new assertion matchers without justification
- Adding test utilities that duplicate existing helpers

**Guidance:**
- New patterns require extraordinary justification
- "I prefer it this way" is not justification
- If the existing pattern is genuinely problematic, flag it for discussion rather than silently changing it

### 5. Runnability - Tests Must Pass

**Verification Steps:**
1. Identify the test command from package.json, Makefile, or project docs
2. Run the test suite (or relevant subset)
3. Capture any failures, errors, or warnings

**Flags:**
- Tests that fail
- Tests that are skipped without explanation
- Missing dependencies that prevent test execution
- Environment setup issues
- Flaky tests (pass/fail inconsistently)

**Guidance:**
- All tests should pass before review is complete
- Skipped tests should have comments explaining why
- Tests should run in isolation without external dependencies

## Review Process

### Phase 1: Discovery - Understand Existing Patterns

Before reviewing any new or changed tests:

1. **Locate test configuration:**
   ```bash
   # Find test config files
   ls -la jest.config* vitest.config* .rspec* pytest.ini* phpunit.xml*
   ```

2. **Sample existing tests:**
   - Read 3-5 established test files
   - Document the patterns observed
   - Note any helper files, factories, or shared setup

3. **Identify test command:**
   - Check package.json scripts
   - Check Makefile targets
   - Check CI configuration

### Phase 2: Analysis - Review Against Criteria

For each test file under review:

1. **Check Volume:**
   - Count tests vs. lines of source code being tested
   - Identify any obvious redundancy
   - Flag tests that don't add coverage value

2. **Check Coverage:**
   - Compare public methods to test coverage
   - Identify untested branches
   - Note missing edge cases

3. **Check Uniformity:**
   - Compare structure to other test files
   - Note style inconsistencies
   - Check naming conventions match

4. **Check Pattern Adherence:**
   - Compare mocking approach to established pattern
   - Check factory/fixture usage matches existing
   - Verify describe block organization follows convention

### Phase 3: Execution - Verify Tests Run

```bash
# Run the tests
npm test           # or
yarn test          # or
bundle exec rspec  # or
pytest             # or
go test ./...      # etc.
```

Capture and report:
- Pass/fail status
- Any skipped tests
- Coverage metrics if available
- Runtime warnings

### Phase 4: Report - Structured Output

Output a review in this format:

```markdown
## Test Review Report

### Summary
[1-2 sentence overall assessment]

### Existing Patterns Observed
| Pattern | Observed Convention |
|---------|---------------------|
| Test Framework | [e.g., Jest 29, RSpec 3.12] |
| File Naming | [e.g., `*.test.ts`] |
| Directory Structure | [e.g., `__tests__/` alongside source] |
| Mocking | [e.g., jest.mock with manual mocks in `__mocks__/`] |
| Factories | [e.g., Factory Bot with factories in `spec/factories/`] |
| Assertion Style | [e.g., expect().toEqual()] |

### Test Execution Results
- **Status:** [PASS/FAIL]
- **Total Tests:** [N]
- **Passed:** [N]
- **Failed:** [N]
- **Skipped:** [N]
- **Coverage:** [X% if available]

### Issues Found

#### Volume Concerns
[List any redundant or excessive tests]

#### Coverage Gaps
[List missing tests with severity]

#### Uniformity Issues
[List inconsistencies with file:line references]

#### Pattern Violations
[List deviations from established patterns - MOST IMPORTANT]

#### Runnability Issues
[List any test failures or execution problems]

### Recommendations
[Prioritized list of suggested changes]

### Approved Patterns
[Note tests that exemplify good practices]
```

## Quick Reference

**Trigger Phrases:**
- "/test-review"
- "review my tests"
- "check my test coverage"
- "are my tests good"
- "review the test file"
- "analyze my unit tests"

**Key Principles:**
1. **Pattern adherence is paramount** - Never introduce new patterns without extraordinary justification
2. **Discover before prescribing** - Always understand existing conventions first
3. **Quality over quantity** - Fewer meaningful tests beats many trivial ones
4. **Tests must run** - A failing test suite is the top priority to fix

**Review Priority Order:**
1. Runnability (tests must pass)
2. Pattern adherence (respect existing conventions)
3. Coverage gaps (critical paths must be tested)
4. Uniformity (consistency matters)
5. Volume concerns (remove redundancy)
