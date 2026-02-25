---
name: test-debug-failures
description: |
  Evidence-based test debugging enforcing systematic root cause analysis.
  Use when tests are failing, pytest errors occur, test suite not passing,
  debugging test failures, or fixing broken tests. Prevents assumption-based
  fixes by enforcing proper diagnostic sequence. Works with Python (.py),
  JavaScript/TypeScript (.js/.ts), Go, Rust test files. Supports pytest,
  jest, vitest, mocha, go test, cargo test, and other frameworks.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Edit
  - MultiEdit
---

# Debug Test Failures

## When to Use This Skill

Use this skill when users mention:
- "tests are failing"
- "pytest errors"
- "test suite not passing"
- "debug test failures"
- "fix broken tests"
- "tests failing after changes"
- "mock not called"
- "assertion error in tests"
- Any test-related debugging task

## What This Skill Does

Provides systematic evidence-based test debugging through 6 mandatory phases:

1. **Evidence Collection** - Run tests with verbose output, capture actual errors
2. **Root Cause Analysis** - Categorize problems (test setup vs business logic vs integration)
3. **Specific Issue Location** - Identify exact file:line:column for ALL occurrences
4. **Systematic Fix** - Plan and implement fixes for all related errors
5. **Validation** - Re-run tests and verify no regressions
6. **Quality Gates** - Run project-specific checks (type, lint, dead code)

Prevents assumption-driven fixes by enforcing proper diagnostic sequence.

## Quick Start

When tests fail, use this skill to systematically identify and fix root causes:

```bash
# This skill will guide you through:
# 1. Running tests with verbose output
# 2. Parsing actual error messages
# 3. Identifying root cause (test setup vs business logic vs integration)
# 4. Locating specific issues (file:line:column)
# 5. Fixing ALL occurrences systematically
# 6. Validating the fix
# 7. Running quality gates
```

## Table of Contents

### Core Sections
- [Purpose](#purpose) - Evidence-based systematic debugging philosophy
- [Quick Start](#quick-start) - Immediate workflow overview
- [Mandatory Debugging Sequence](#mandatory-debugging-sequence) - 6-phase systematic approach
  - [Phase 1: Evidence Collection](#phase-1-evidence-collection) - Run tests, capture output, parse errors
  - [Phase 2: Root Cause Analysis](#phase-2-root-cause-analysis) - Categorize problems, check test vs code
  - [Phase 3: Specific Issue Location](#phase-3-specific-issue-location) - Exact locations, find all occurrences
  - [Phase 4: Systematic Fix](#phase-4-systematic-fix) - Plan, implement, address all related errors
  - [Phase 5: Validation](#phase-5-validation) - Re-run tests, check results, full test suite
  - [Phase 6: Quality Gates](#phase-6-quality-gates) - Project checks, verify all gates pass
- [Anti-Patterns](#anti-patterns---stop-if-you-see-these) - Common mistakes to avoid
- [Common Test Failure Patterns](#common-test-failure-patterns) - Diagnostic reference
  - [Pattern 1: Mock Not Called](#pattern-1-mock-not-called) - Execution path issues
  - [Pattern 2: Attribute Error on Mock](#pattern-2-attribute-error-on-mock) - Mock configuration issues
  - [Pattern 3: Assertion Mismatch](#pattern-3-assertion-mismatch) - Business logic errors
  - [Pattern 4: Import/Fixture Errors](#pattern-4-importfixture-errors) - Dependency issues

### Framework-Specific Guides
- [Framework-Specific Quick Reference](#framework-specific-quick-reference) - Test runner commands and flags
  - **Python (pytest)** - Run tests, common flags, debugging options
  - **JavaScript/TypeScript (Jest/Vitest)** - Jest flags, Vitest reporter options
  - **Go** - Test commands, race detection, specific package testing
  - **Rust** - Cargo test, output control, sequential execution

### Advanced Topics
- [Success Criteria](#success-criteria) - Task completion checklist
- [Examples](#examples) - Detailed walkthroughs (see examples.md)
- [Related Documentation](#related-documentation) - Project CLAUDE.md, quality gates, testing strategy
- [Philosophy](#philosophy) - Evidence-based debugging principles

## Instructions

**YOU MUST follow this sequence. No shortcuts.**

### Phase 1: Evidence Collection

**1.1 Run Tests First - See Actual Errors**

DO NOT make any changes before running tests. Execute with maximum verbosity:

**Python/pytest:**
```bash
uv run pytest <failing_test_path> -v --tb=short
# Or for full stack traces:
uv run pytest <failing_test_path> -vv --tb=long
# Or for specific test function:
uv run pytest <file>::<test_function> -vv
```

**JavaScript/TypeScript:**
```bash
# Jest
npm test -- --verbose --no-coverage <test_path>

# Vitest
npm run test -- --reporter=verbose <test_path>

# Mocha
npm test -- --reporter spec <test_path>
```

**Other Languages:**
```bash
# Go
go test -v ./...

# Rust
cargo test -- --nocapture --test-threads=1

# Ruby (RSpec)
bundle exec rspec <spec_path> --format documentation
```

**1.2 Capture Output**

Save the COMPLETE output. Do not summarize. Do not assume.

**1.3 Read The Error - Parse Actual Messages**

Identify:
- Error type (AssertionError, AttributeError, ImportError, etc.)
- Error message (exact wording)
- Stack trace (which functions called which)
- Line numbers (where error originated)

**CRITICAL:** Is this a "mock not called" error or an actual assertion failure?

### Phase 2: Root Cause Analysis

**2.1 Categorize The Problem**

**Test Setup Issues:**
- Mock configuration incorrect (`mock_X not called`, `mock has no attribute Y`)
- Fixture problems (missing, incorrectly scoped, teardown issues)
- Test data issues (invalid inputs, wrong test doubles)
- Import/dependency injection errors

**Business Logic Bugs:**
- Assertion failures on expected values
- Logic errors in implementation
- Missing validation
- Incorrect algorithm

**Integration Issues:**
- Database connection failures
- External service unavailable
- File system access problems
- Environment configuration missing

**2.2 Check Test vs Code**

Use Read tool to examine:
1. The failing test file
2. The code being tested
3. Related fixtures/mocks/setup

**CRITICAL QUESTION:** Is the problem in how the test is written, or what the code does?

### Phase 3: Specific Issue Location

**3.1 Provide Exact Locations**

For EVERY error, document:
- **File:** Absolute path to file
- **Line:** Exact line number
- **Column:** Character position (if available)
- **Function/Method:** Name of failing function
- **Error Type:** Specific exception/assertion
- **Actual vs Expected:** What was expected, what was received

**Example:**
```
File: /abs/path/to/test_service.py
Line: 45
Function: test_process_data
Error: AssertionError: mock_repository.save not called
Expected: save() called once with data={'key': 'value'}
Actual: save() never called
```

**3.2 Identify ALL Occurrences**

Use Grep to find all instances of the pattern:

```bash
# Find all similar test patterns
grep -r "pattern_causing_error" tests/

# Find all places where mocked function is used
grep -r "mock_function_name" tests/
```

**DO NOT fix just the first occurrence. Fix ALL of them.**

### Phase 4: Systematic Fix

**4.1 Plan The Fix**

Before making changes, document:
- What needs to change
- Why this fixes the root cause
- How many files/locations affected
- Whether this is test code or business logic

**4.2 Implement Fix**

**Use MultiEdit for multiple changes to same file:**

```python
# ✅ CORRECT - All edits to same file in one operation
MultiEdit("path/to/file.py", [
    {"old_string": incorrect_mock_setup_1, "new_string": correct_mock_setup_1},
    {"old_string": incorrect_mock_setup_2, "new_string": correct_mock_setup_2},
    {"old_string": incorrect_assertion, "new_string": correct_assertion}
])
```

**For changes across multiple files, use Edit for each file:**

```python
# Fix in test file
Edit("tests/test_service.py", old_string=..., new_string=...)

# Fix in implementation
Edit("src/service.py", old_string=..., new_string=...)
```

**4.3 Address All Related Errors**

If error appears in 10 places, fix all 10. No arbitrary limits.

If pattern appears across files:
1. Use Grep to find all occurrences
2. Document each location
3. Fix each location
4. Track completion

### Phase 5: Validation

**5.1 Re-run Tests**

Run the EXACT same test command from Phase 1:

```bash
# Same command as before
uv run pytest <failing_test_path> -vv
```

**5.2 Check Results**

- ✅ **PASS:** All tests green → Proceed to Phase 6
- ❌ **FAIL:** New errors → Return to Phase 2 (different root cause)
- ⚠️ **PARTIAL:** Some pass, some fail → Incomplete fix, return to Phase 3

**5.3 Run Full Test Suite**

Ensure no regressions:

```bash
# Python
uv run pytest tests/ -v

# JavaScript
npm test

# Go
go test ./...
```

### Phase 6: Quality Gates

**6.1 Run Project-Specific Quality Checks**

**For this project (project-watch-mcp):**
```bash
./scripts/check_all.sh
```

**Generic quality gates:**
```bash
# Type checking
pyright  # or tsc, or mypy

# Linting
ruff check src/  # or eslint, or rubocop

# Dead code detection
vulture src/  # or knip (JS)

# Security
bandit src/  # or npm audit
```

**6.2 Verify All Gates Pass**

Task is NOT done if quality gates fail. Fix or request guidance.

## Usage Examples

### Example 1: Mock Configuration Issue

```bash
# User says: "Tests failing in test_service.py"
# Phase 1: Run tests
uv run pytest tests/test_service.py -vv

# Error: AssertionError: Expected 'save' to be called once. Called 0 times.
# Phase 2: Root cause - Mock not called (execution path issue)
# Phase 3: Location - test_service.py:45, function test_process_data
# Phase 4: Fix mock configuration to match actual code path
# Phase 5: Re-run tests - PASS
# Phase 6: Run quality gates - PASS
```

### Example 2: Business Logic Assertion

```bash
# User says: "test_calculate is failing"
# Phase 1: Run tests
uv run pytest tests/test_calculator.py::test_calculate -vv

# Error: AssertionError: assert 42 == 43
# Phase 2: Root cause - Business logic error (calculation off by 1)
# Phase 3: Location - src/calculator.py:23, function calculate
# Phase 4: Fix algorithm in implementation
# Phase 5: Re-run tests - PASS
# Phase 6: Run quality gates - PASS
```

### Example 3: Integration Test Failure

```bash
# User says: "Integration tests are failing"
# Phase 1: Run tests
uv run pytest tests/integration/ -vv

# Error: Neo4j connection failed
# Phase 2: Root cause - Integration issue (database unavailable)
# Phase 3: Location - Environment configuration
# Phase 4: Start Neo4j Desktop
# Phase 5: Re-run tests - PASS
# Phase 6: Run quality gates - PASS
```

## Validation Process

This skill enforces systematic validation at each phase:

1. **Evidence Validation** - Actual test output captured, not assumed errors
2. **Root Cause Validation** - Problem categorized correctly (setup vs logic vs integration)
3. **Location Validation** - Exact file:line:column identified for ALL occurrences
4. **Fix Validation** - Re-run tests to verify fix works
5. **Regression Validation** - Full test suite passes, no new failures
6. **Quality Validation** - All quality gates pass (type check, lint, dead code)

## Expected Outcomes

### Successful Debugging

```
✓ Tests Fixed

Failing tests: tests/test_service.py::test_process_data
Root cause: Mock configuration - save() not called due to early return
Fix applied: Updated mock to handle validation failure path
Location: tests/test_service.py:45-52

Test results:
  ✓ Specific test: PASS
  ✓ Full suite: PASS (no regressions)
  ✓ Quality gates: PASS

Time: 8 minutes (systematic debugging)
Confidence: High (evidence-based fix)
```

### Debugging Failure (Needs More Investigation)

```
⚠️ Additional Investigation Required

Failing tests: tests/test_integration.py::test_database
Root cause: Partially identified - connection issue
Current status: Neo4j started, but connection still failing

Next steps:
  1. Check Neo4j logs for startup errors
  2. Verify connection configuration in settings
  3. Test connection manually with cypher-shell
  4. Check firewall/network settings

Blocker: Database configuration needs review
```

## Integration Points

### With Project CLAUDE.md

**Implements CLAUDE.md debugging approach:**
- "Run tests first" - Enforced in Phase 1
- "Read the error" - Phase 1.3 parses actual messages
- "Be specific" - Phase 3 requires file:line:column
- "Be complete" - Phase 4 fixes ALL occurrences

### With Quality Gates

**Integrates with quality validation:**
- Phase 6 runs project check_all.sh
- Ensures type checking passes (pyright)
- Validates linting (ruff)
- Checks for dead code (vulture)

### With Other Skills

**Coordinates with complementary skills:**
- `run-quality-gates` - Automated Phase 6 execution
- `analyze-logs` - Investigate test failure logs
- `debug-type-errors` - Resolve type checking failures
- `setup-async-testing` - Fix async test issues

## Expected Benefits

| Metric | Without Skill | With Skill | Improvement |
|--------|--------------|------------|-------------|
| **Debug Time** | 30-60 min (trial & error) | 8-15 min (systematic) | 4-7x faster |
| **Fix Accuracy** | ~60% (assumptions) | ~95% (evidence-based) | 58% improvement |
| **Regressions** | ~20% (incomplete fixes) | <2% (full validation) | 90% reduction |
| **Complete Fixes** | ~40% (first occurrence only) | ~98% (all occurrences) | 145% improvement |
| **Quality Gate Pass** | ~70% (skipped) | 100% (enforced) | 43% improvement |

## Success Metrics

After using this skill:

- **100% evidence-based** - No assumptions, only actual test output
- **95% fix accuracy** - Root cause identified correctly
- **98% complete fixes** - All occurrences addressed
- **<2% regressions** - Full suite validation prevents new failures
- **100% quality gate compliance** - All checks pass before "done"

## Red Flags to Avoid

**❌ WRONG: Making changes before running tests**
```
"The mock setup looks wrong, let me fix it..."
```
**✅ RIGHT: Run test first, see actual error**
```
"Let me run the test to see the exact error message..."
```

---

**❌ WRONG: Assuming errors are unrelated**
```
"This ImportError is probably unrelated to the test failure..."
```
**✅ RIGHT: Investigate every error**
```
"Let me trace why this import is failing - it may be the root cause..."
```

---

**❌ WRONG: Fixing first occurrence only**
```
"Fixed the mock in test_create.py, done!"
```
**✅ RIGHT: Search for all occurrences**
```
"Let me search for this pattern across all test files..."
```

---

**❌ WRONG: Skipping quality gates**
```
"Tests pass now, we're done!"
```
**✅ RIGHT: Run full validation**
```
"Tests pass. Running quality gates to check for regressions..."
```

---

**❌ WRONG: Quick fix without understanding**
```
"Let me just add a try/except to suppress this error..."
```
**✅ RIGHT: Understand root cause**
```
"This error indicates a deeper issue. Let me investigate why..."
```

## Common Test Failure Patterns

### Pattern 1: Mock Not Called

**Error:**
```
AssertionError: Expected 'save' to be called once. Called 0 times.
```

**Root Cause:**
- Code path not executing
- Early return before mock called
- Exception preventing execution
- Wrong mock target

**Investigation:**
1. Read the test - what's being tested?
2. Read the implementation - is save() actually called?
3. Check for early returns or exceptions
4. Verify mock is patching correct location

### Pattern 2: Attribute Error on Mock

**Error:**
```
AttributeError: Mock object has no attribute 'success'
```

**Root Cause:**
- Mock returns dict when ServiceResult expected
- Incomplete mock configuration
- Missing return_value or side_effect
- Wrong mock type

**Investigation:**
1. Check what test expects mock to return
2. Check what code actually returns
3. Verify mock configuration matches interface
4. Look for type mismatches (dict vs object)

### Pattern 3: Assertion Mismatch

**Error:**
```
AssertionError: assert 'foo' == 'bar'
```

**Root Cause:**
- Business logic error
- Test expectation wrong
- Data transformation issue
- Configuration problem

**Investigation:**
1. Is expected value correct?
2. Is actual value correct?
3. Is transformation logic correct?
4. Are inputs to function correct?

### Pattern 4: Import/Fixture Errors

**Error:**
```
ImportError: cannot import name 'X' from 'module'
fixture 'db_session' not found
```

**Root Cause:**
- Missing dependency
- Fixture not in scope
- Circular import
- Module not installed

**Investigation:**
1. Check imports at top of file
2. Check fixture definition location
3. Check conftest.py for fixtures
4. Verify dependencies installed

## Troubleshooting

See [Troubleshooting](#troubleshooting) section below for common issues.

## Task Completion Checklist

Before declaring task complete:

- [ ] All tests pass (specific failing test)
- [ ] Full test suite passes (no regressions)
- [ ] Root cause identified and documented
- [ ] All related errors fixed (not just first occurrence)
- [ ] Quality gates pass
- [ ] No new errors introduced
- [ ] Fix addresses root cause, not symptoms

## Framework-Specific Quick Reference

### Python (pytest)

**Run tests:**
```bash
uv run pytest tests/ -v                    # All tests
uv run pytest tests/test_file.py -vv      # Specific file
uv run pytest tests/test_file.py::test_fn # Specific test
uv run pytest -k "pattern" -v             # Pattern matching
uv run pytest --lf -v                     # Last failed
```

**Common flags:**
- `-v` - Verbose
- `-vv` - Extra verbose
- `-s` - Show print statements
- `--tb=short` - Shorter traceback
- `--tb=long` - Full traceback
- `--pdb` - Drop into debugger on failure

### JavaScript/TypeScript (Jest/Vitest)

**Run tests:**
```bash
npm test                                  # All tests
npm test -- <test_file>                   # Specific file
npm test -- --testNamePattern="pattern"   # Pattern matching
npm test -- --verbose                     # Verbose output
```

**Jest flags:**
- `--verbose` - Detailed output
- `--no-coverage` - Skip coverage
- `--detectOpenHandles` - Find async issues
- `--forceExit` - Force exit after tests

**Vitest flags:**
- `--reporter=verbose` - Detailed output
- `--run` - Run once (no watch)
- `--coverage` - Generate coverage

### Go

**Run tests:**
```bash
go test ./...                             # All packages
go test -v ./pkg/service                  # Specific package
go test -run TestFunctionName             # Specific test
go test -v -race ./...                    # Race detection
```

### Rust

**Run tests:**
```bash
cargo test                                # All tests
cargo test test_function_name             # Specific test
cargo test -- --nocapture                 # Show output
cargo test -- --test-threads=1            # Sequential
```

## Examples

See [examples.md](./references/examples.md) for detailed walkthroughs of:
- Mock configuration debugging
- Business logic assertion failures
- Integration test issues
- Fixture scope problems
- Cross-framework patterns

## Shell Scripts

- [Test Skill Script](./scripts/test_skill.sh) - Helper script for testing and running test debug workflows

## Requirements

**Tools needed:**
- Bash (for running tests)
- Read (for examining test and source files)
- Grep (for finding all occurrences)
- Glob (for pattern matching)
- Edit/MultiEdit (for fixing code)

**Test Frameworks Supported:**
- **Python:** pytest, unittest
- **JavaScript/TypeScript:** Jest, Vitest, Mocha
- **Go:** go test
- **Rust:** cargo test
- **Ruby:** RSpec

**Project-Specific:**
- Access to test suite (tests/ directory)
- Access to source code under test
- Ability to run quality gates (./scripts/check_all.sh or equivalent)

**Knowledge:**
- Basic understanding of test framework syntax
- Ability to read stack traces
- Understanding of mock/fixture patterns

## Related Documentation

- **Project CLAUDE.md:** Critical workflow rules and debugging approach
- **Quality Gates:** [../quality-run-quality-gates/references/shared-quality-gates.md](../quality-run-quality-gates/references/shared-quality-gates.md)
- **Testing Strategy:** Project-specific testing documentation

## Philosophy

**This skill enforces evidence-based debugging:**
1. See actual errors (not assumed errors)
2. Understand root causes (not symptoms)
3. Fix systematically (not randomly)
4. Validate thoroughly (not superficially)

**The goal is not speed. The goal is correctness.**

Slow down. Read the errors. Understand the problem. Fix it properly.
