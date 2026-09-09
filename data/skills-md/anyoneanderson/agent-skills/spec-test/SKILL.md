---
name: spec-test
description: |
  Create and run tests for a spec task implementation.

  Reads task completion criteria from tasks.md, detects existing test patterns,
  creates test cases, runs them, and outputs a structured test result file.
  Works standalone or as part of the spec-implement pipeline.

  English triggers: "Test this task", "Run spec-test", "Create tests for task"
  日本語トリガー: 「このタスクをテスト」「spec-testを実行」「タスクのテストを作成」
license: MIT
---

# spec-test — Create and Run Tests for a Spec Task

Create tests based on task completion criteria, run them, and output structured results.

## Language Rules

1. **Auto-detect input language** → output in the same language
2. Japanese input → Japanese output, use `references/test-guide.ja.md`
3. English input → English output, use `references/test-guide.md`
4. Explicit override takes priority

## Options

| Option | Description |
|--------|-------------|
| `--task {task-id}` | Task ID to test (reads completion criteria from tasks.md) |
| `--spec {path}` | Path to .specs/ directory |
| `--files {paths}` | Target files to test (auto-detect from task if omitted) |
| `--output {path}` | Output path for test result (default: `.specs/{feature}/test-{task-id}.md`) |

## Execution Flow

### Step 0: Context Loading (Phase A / Phase B)

Same as spec-code §Step 0, but identify your role as **tester**.

Phase B applies when re-testing after a fix: focus on the specific test failures and changed code.

### Step 1: Extract Test Requirements

From `tasks.md`, find the task matching `--task {task-id}` and extract:
- Completion criteria (checkboxes)
- Target files (implementation files to test)
- Requirements ID (for traceability)

From `design.md` (if available):
- Expected interfaces and behaviors
- Edge cases mentioned in design

### Step 2: Detect Test Patterns

Scan the project for existing test conventions:

1. **Find test files**: look for `*.test.*`, `*.spec.*`, `__tests__/`, `test/`, `tests/` directories
2. **Detect framework**: Jest, Vitest, Mocha, pytest, Go test, Rust test, etc.
3. **Detect patterns**: AAA (Arrange-Act-Assert), describe/it blocks, test helpers, fixtures
4. **Detect test commands**: from `package.json` scripts, `Makefile`, `CLAUDE.md`, etc.

If no existing tests found, use framework defaults appropriate to the language.

### Step 3: Design Test Cases

Based on completion criteria and design:

1. **Happy path tests**: Each completion criterion → at least one test
2. **Edge cases**: Empty inputs, boundary values, error conditions
3. **Negative tests**: Invalid inputs, unauthorized access, missing data

### Step 4: Create Tests

Write test files following detected patterns:
- Place in the conventional test location
- Import test helpers/fixtures if they exist
- Follow naming conventions of existing tests
- Apply AAA pattern (Arrange-Act-Assert)

### Step 5: Run Tests

Execute the detected test command:
```
# Auto-detect and run
npm test / npx jest / npx vitest / pytest / go test / cargo test
```

If a specific test file can be targeted, run only the new tests first, then the full suite.

### Step 6: Collect Results and Write Output

Output to `--output` path (default: `.specs/{feature}/test-{task-id}.md`):

```markdown
# Test: {task-id}
type: test

## Meta
- Tester: spec-test
- Date: {ISO 8601}
- Command: {test command used}
- Framework: {detected framework}

## Results
- Tests: {passed}/{total} passed
- Coverage: {percentage}% (if available)
- Duration: {time}

## Test Cases
- [x] {test name} — {what it verifies}
- [x] {test name} — {what it verifies}
- [ ] {test name} — FAILED: {error message}

## Completion Criteria Coverage
| Criterion | Test | Status |
|---|---|---|
| {criterion from tasks.md} | {test name} | PASS / FAIL |

## Gate: PASS / FAIL
```

**Gate logic:**
- All tests pass → PASS
- Any test fails → FAIL

### Step 7: Commit Tests

Commit test files following project conventions:
- Default format: `test(scope): {task-id} — {brief description}`
- Stage only test files

## Error Handling

| Situation | Response |
|---|---|
| `--task` ID not found in tasks.md | Error: task ID not found |
| No test framework detected | Warning: suggest installing one, create basic tests |
| Test command fails to run | Error: report command and error output |
| Some tests fail | Write results with FAIL gate, do not fix (spec-code handles fixes) |
| Coverage tool not available | Warning: skip coverage, note in results |

## Usage Examples

```
# Test a specific task
/spec-test --task T-007 --spec .specs/did-deactivation/

# Test with explicit file targets
/spec-test --task T-003 --spec .specs/auth-feature/ --files src/auth/service.ts

# Standalone (no spec context)
/spec-test --task T-001 --files src/utils/parser.ts
```
