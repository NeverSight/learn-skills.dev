---
name: test
description: Full TDD red-green-refactor cycle with automatic framework detection
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[task description]"
---

# /test -- Full TDD Red-Green-Refactor Cycle

Run a complete test-driven development cycle for the given task.
Four phases: Discovery, Red, Green, Refactor, then final Verification.

## Argument

A description of the feature or behavior to implement via TDD.

## Procedure

### Phase 0 -- Discovery

1. Detect the test framework by checking config files:
   - `pyproject.toml`, `setup.cfg`, `pytest.ini` for Python (pytest, unittest)
   - `package.json` for JS/TS (jest, vitest, mocha)
   - `Cargo.toml` for Rust
   - `go.mod` for Go
   - Fall back to asking the user if ambiguous

2. Identify the test command (e.g., `pytest`, `npm test`, `cargo test`)

3. Read 2-3 existing test files to learn project conventions:
   - File naming pattern (`test_*.py`, `*.test.ts`, etc.)
   - Import style, fixture usage, assertion style
   - Directory structure (`tests/`, `__tests__/`, co-located)

4. Confirm scope with the user before proceeding:
   - "I will write tests for [X] using [framework] in [directory]."
   - "Test cases planned: [list]"
   - Wait for user approval.

### Phase 1 -- RED (Write Failing Tests)

Write comprehensive tests covering:
- Happy path (expected inputs produce expected outputs)
- Edge cases (empty inputs, boundary values, type variations)
- Error cases (invalid inputs, expected exceptions)
- Integration points (if the feature interacts with other modules)

Conventions to follow:
- Add docstrings to every test function explaining what it validates
- Use descriptive test names (test_returns_empty_list_when_no_matches)
- No emojis anywhere
- Follow existing project test patterns discovered in Phase 0

Run the tests:
```bash
source venv/bin/activate && [test command] [test file]
```

All tests MUST fail. If any test passes, it is not testing new behavior --
fix or remove it. A passing test in the RED phase means the test is
not validating anything new.

### Phase 2 -- GREEN (Minimum Implementation)

Implement the minimum code to make each test pass:
- Add docstrings with the algorithm in plain English, args, and
  input/output documentation
- For functions taking loose objects (dict, pandas DataFrame, list, etc.),
  write the expected schema explicitly in the docstring
- Add `if __name__ == '__main__'` blocks with hardcoded example inputs
  (no argparse)
- Use `uv pip install` for any new packages (never bare pip)
- Always `source venv/bin/activate` before running anything

After each implementation change, run the tests:
```bash
source venv/bin/activate && [test command] [test file]
```

If tests still fail, iterate. Maximum 10 attempts before stopping and
reporting what is stuck. Do not loop infinitely.

### Phase 3 -- REFACTOR

With all tests passing, clean up:
- Remove duplication in implementation code
- Improve variable/function naming for clarity
- Extract helpers only where they reduce genuine complexity
  (not for one-time operations)
- Ensure docstrings are accurate after changes

After EACH refactor step, run the tests:
```bash
source venv/bin/activate && [test command] [test file]
```

If any test fails after a refactor, revert that specific change
immediately. Refactoring must not change behavior.

### Phase 4 -- Verification

1. Run the full test suite (not just new tests):
   ```bash
   source venv/bin/activate && [test command]
   ```

2. Run the project linter if one is configured:
   - Check `pyproject.toml` for ruff/flake8/black config
   - Check `package.json` for eslint/prettier scripts
   - Run it and fix any issues in new code only

3. Report final status:
   ```
   ## TDD Cycle Complete

   Tests written: [count]
   Tests passing: [count]
   Implementation files: [list]
   Linter status: [pass/fail/not configured]

   ### Test Coverage
   - Happy path: [covered/not covered]
   - Edge cases: [covered/not covered]
   - Error cases: [covered/not covered]
   - Integration: [covered/not covered]
   ```

## Important

- Never skip the RED phase. Tests must fail first to prove they test
  real behavior.
- Never skip running tests between changes. The cycle depends on
  continuous feedback.
- If the task is ambiguous, ask for clarification in Phase 0 before
  writing any tests.
- Keep test files focused. One test file per module/feature being tested.
- Do not refactor code outside the scope of this task.
