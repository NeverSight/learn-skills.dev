---
name: tdd-workflow
description: Test-driven development execution workflow with red-green-refactor cycle, increment decomposition, and pause/continue rules. Use when building features or fixing bugs using TDD. Framework-agnostic with language-specific configs for Python, TypeScript, Go, and Ruby delegation.
---

# TDD Workflow

## Core Principle

**Never write implementation code before a failing test exists for that behavior.**

## Execution Flow

### 1. Setup

```
LANG = /majestic:config tech_stack "unknown"
If LANG == "unknown": detect from project files (package.json → TypeScript, Gemfile → Ruby, go.mod → Go, pyproject.toml → Python)
If LANG == "unknown": AskUserQuestion("What language/framework?")

RUNNER = lookup LANG in [references/language-configs.md]
If LANG in [ruby]: delegate to `rspec-coder` or `minitest-coder` skill for runner details

INCREMENTS = decompose feature using patterns from [references/increments.md]
  - Read requirements/plan
  - Identify pattern (Data Transformation, CRUD, State Machine, Calculation, Integration)
  - Break into ordered increments: degenerate → happy path → variations → edge cases → errors

For each INCREMENT in INCREMENTS:
  TaskCreate(subject: INCREMENT.name, description: INCREMENT.test_description)

AskUserQuestion("Review increments. Adjust ordering or scope?", options: ["Looks good", "Modify"])
```

### 2. TDD Loop (per increment)

```
For each INCREMENT in INCREMENTS:
  TaskUpdate(INCREMENT.task_id, status: "in_progress")

  # RED
  Write failing test to real file (not code block)
  RUN = Bash(RUNNER.test_command)
  If RUN.status == PASS: STOP — investigate unexpected pass
  If RUN.status == FAIL (wrong reason): fix test, rerun
  PAUSE → show test + failure output, wait for user

  # GREEN
  Write minimal implementation code
  RUN = Bash(RUNNER.full_suite_command)
  If RUN.status == FAIL: show output, PAUSE → ask user to fix or hand off
  If RUN.status == PASS: auto-continue (no pause)

  # REFACTOR
  If improvement opportunities exist:
    Refactor implementation and/or test code
    RUN = Bash(RUNNER.full_suite_command)
    If RUN.status == FAIL: revert refactor, PAUSE → discuss
    If RUN.status == PASS: auto-continue (no pause)

  TaskUpdate(INCREMENT.task_id, status: "completed")
  Brief summary of what was implemented
  → immediately begin next increment (no pause between increments)
```

### 3. Wrap-up

```
RUN = Bash(RUNNER.full_suite_command)
Report: increments completed, total tests, pass/fail status
Suggest: remaining work, missed edge cases, integration tests needed
```

## Pause/Continue Rules

| Situation | Action |
|-----------|--------|
| RED: test fails (expected) | **Pause** — show test + failure, wait for user |
| RED: test passes unexpectedly | **Stop** — investigate, don't proceed |
| GREEN: all tests pass | **Auto-continue** to REFACTOR |
| GREEN: tests fail | **Pause** — show output, ask user |
| REFACTOR: tests pass | **Auto-continue** to next increment |
| REFACTOR: tests fail | **Revert + Pause** — discuss approach |
| Between increments | **Auto-continue** — no pause |

## Task Tracking Integration

```
TASK_TRACKING = /majestic:config task_tracking.enabled false
WORKFLOW_ID = "tdd-{timestamp}"

If TASK_TRACKING:
  For each TaskCreate: add metadata {workflow: WORKFLOW_ID, phase: "tdd-loop"}
  For each TaskUpdate: wrap with If TASK_TRACKING: TaskUpdate(...)
  On Wrap-up: update ledger if LEDGER_ENABLED
    LEDGER_ENABLED = /majestic:config task_tracking.ledger false
    LEDGER_PATH = /majestic:config task_tracking.ledger_path .agents/workflow-ledger.yml
```

## Red-Green-Refactor Cycle

### 1. Red Phase: Write a Failing Test

- Select one small, specific behavior from the increment
- Write a descriptive test that expresses the expected behavior
- Run the test to confirm it **fails** (red)
- The failure should be for the right reason (not syntax error or missing dependency)

### 2. Green Phase: Minimal Implementation

- Implement only the minimal code necessary to pass the failing test
- Resist adding extra features or handling edge cases not yet covered by tests
- Run the test to confirm it **passes** (green)

### 3. Refactor Phase: Improve Quality

- Review both implementation and test code for improvements
- Remove duplication, improve naming, extract methods
- Apply language-specific idioms and patterns
- Run tests after each refactoring step to ensure they still **pass**

## Test Sequencing Strategy

**Order tests from simple to complex:**

1. **Happy path** — The core behavior with valid inputs
2. **Validation tests** — Required fields, format constraints
3. **Edge cases** — Boundary conditions, empty values, unusual inputs
4. **Error handling** — Invalid inputs, failure scenarios
5. **Integration points** — Interactions with other components

## Test Quality Guidelines

**Each test should:**
- Cover exactly one behavior
- Be isolated — no shared state between tests
- Have a clear, descriptive name
- Fail for only one reason

**Avoid:**
- Testing implementation details instead of behavior
- Writing tests after the code
- Sharing test setup that creates hidden dependencies
- Skipping the refactor phase

## Framework-Specific Implementation

For language-specific test runner commands, see [references/language-configs.md](references/language-configs.md).

For Ruby projects:
- **RSpec:** Apply `rspec-coder` skill
- **Minitest:** Apply `minitest-coder` skill

A Rails example is available in [references/rails-tdd-workflow.md](references/rails-tdd-workflow.md).
