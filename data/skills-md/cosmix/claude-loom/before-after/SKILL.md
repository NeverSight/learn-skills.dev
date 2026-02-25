---
name: before-after
description: Generates before/after verification pairs for loom plans. Proves a stage actually changed system behavior by capturing state before and after implementation. Use for delta-proof verification — proving new commands, endpoints, modules, or bug fixes work by comparing system state.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
trigger-keywords: before after, before-after, delta proof, prove change, prove new, verify delta, state transition, before implementation, after implementation
---

# Before/After Verification Skill

## Overview

Before/after verification is a technique for proving that a stage **actually changed** system behavior. Instead of just checking that the final state is valid, you capture what was true BEFORE implementation and what should be true AFTER implementation. The pair proves your stage caused the change.

This matters because without before/after thinking, you can't distinguish:

- "The feature already worked" from "My stage made it work"
- "The bug was already fixed" from "My fix resolved it"
- "The endpoint existed" from "I created the endpoint"

## The Delta-Proof Concept

A **delta-proof** is verification that proves a state transition occurred.

### The Pattern

1. **Before State**: Capture system behavior BEFORE implementation
   - For new features: Expected to FAIL (feature doesn't exist yet)
   - For bug fixes: Expected to SUCCEED (bug reproducer demonstrates the problem)

2. **After State**: Capture system behavior AFTER implementation
   - For new features: Expected to SUCCEED (feature now exists)
   - For bug fixes: Expected to FAIL (bug reproducer no longer triggers the bug)

3. **The Pair**: Together, before + after prove the implementation caused the change

### Why This Matters

Without delta-proof thinking, verification can be misleading:

**Bad Example:**

```yaml
# Stage: Add user authentication
truths:
  - "cargo test"  # All tests pass
```

Problem: Tests might have passed before this stage. This doesn't prove authentication was added.

**Good Example:**

```yaml
# Stage: Add user authentication
description: |
  Implement JWT-based user authentication.

  BEFORE: curl -f localhost:8080/api/protected returns 200 (no auth required)
  AFTER: curl -f localhost:8080/api/protected returns 401 (auth now required)
  AFTER: curl -f -H "Authorization: Bearer <token>" localhost:8080/api/protected returns 200

truths:
  - "curl -sf localhost:8080/api/protected | grep -q 401"
  - "curl -sf -H 'Authorization: Bearer fake' localhost:8080/api/protected && exit 1 || exit 0"

wiring:
  - source: "src/middleware/auth.rs"
    pattern: "pub fn require_auth"
    description: "Authentication middleware registered"
```

This proves authentication was ADDED by this stage (not already present).

## When to Use Before/After Thinking

Use delta-proof verification when:

1. **Adding new features** — Prove the feature didn't exist before
2. **Fixing bugs** — Prove the bug existed before and is gone after
3. **Changing behavior** — Prove old behavior is replaced by new behavior
4. **Creating endpoints/commands** — Prove they're newly available
5. **Refactoring with behavior change** — Prove the behavior actually changed

Do NOT use when:

- Verification is straightforward (just checking files exist)
- The stage is knowledge-only (no implementation)
- You're just checking code quality (linting, formatting)

## Templates for Common Scenarios

### Scenario 1: New CLI Command

When adding a new CLI command, prove it didn't exist before.

**Before State:** Command doesn't exist (help fails or command not found)
**After State:** Command exists (help succeeds, basic invocation works)

```yaml
- id: add-verify-command
  name: "Add loom verify command"
  stage_type: standard
  working_dir: "loom"
  description: |
    Implement the `loom verify <stage-id>` CLI command.

    DELTA PROOF:
    - BEFORE: `loom verify --help` fails (command not registered)
    - AFTER: `loom verify --help` succeeds
    - AFTER: `loom verify test-stage` runs verification logic

  truths:
    - "loom verify --help"
    - "loom verify nonexistent-stage 2>&1 | grep -q 'Stage not found'"

  wiring:
    - source: "src/main.rs"
      pattern: "verify"
      description: "Verify command registered in CLI"
    - source: "src/commands/verify.rs"
      pattern: "pub fn execute"
      description: "Verify command implementation exists"

  artifacts:
    - "src/commands/verify.rs"
```

### Scenario 2: New API Endpoint

When adding an API endpoint, prove it returns 404 before and data after.

**Before State:** Endpoint returns 404 (not registered)
**After State:** Endpoint returns expected status/data

```yaml
- id: add-status-endpoint
  name: "Add /api/status endpoint"
  stage_type: standard
  working_dir: "."
  description: |
    Implement GET /api/status endpoint returning system health.

    DELTA PROOF:
    - BEFORE: curl localhost:8080/api/status returns 404
    - AFTER: curl localhost:8080/api/status returns 200 with JSON health data

  truths:
    - "curl -sf localhost:8080/api/status | jq -e '.healthy'"
    - "curl -sf -o /dev/null -w '%{http_code}' localhost:8080/api/status | grep -q 200"

  wiring:
    - source: "src/routes/mod.rs"
      pattern: "/api/status"
      description: "Status endpoint registered in router"
    - source: "src/handlers/status.rs"
      pattern: "pub async fn status_handler"
      description: "Status handler implementation"

  artifacts:
    - "src/handlers/status.rs"
```

### Scenario 3: New Module/Library

When adding a new module, prove imports fail before and succeed after.

**Before State:** Import/use fails (module doesn't exist)
**After State:** Import/use succeeds

```yaml
- id: add-retry-module
  name: "Add retry module"
  stage_type: standard
  working_dir: "loom"
  description: |
    Create retry module with exponential backoff.

    DELTA PROOF:
    - BEFORE: `use crate::retry::RetryPolicy;` would fail (module doesn't exist)
    - AFTER: Module compiles, exports are available

  truths:
    - "cargo check"
    - "cargo test --lib retry"

  wiring:
    - source: "src/lib.rs"
      pattern: "pub mod retry"
      description: "Retry module exported from lib.rs"
    - source: "src/orchestrator/core/orchestrator.rs"
      pattern: "use crate::retry"
      description: "Retry module imported in orchestrator"

  artifacts:
    - "src/retry.rs"
    - "tests/retry_tests.rs"
```

### Scenario 4: Bug Fix (COUNTERINTUITIVE)

When fixing a bug, prove the bug reproducer SUCCEEDS before (bug exists) and FAILS after (bug fixed).

**Before State:** Bug reproducer succeeds (demonstrates the bug)
**After State:** Bug reproducer fails (bug no longer triggers)

This is counterintuitive but correct: the reproducer "working" means the bug is present.

```yaml
- id: fix-crash-on-empty-plan
  name: "Fix crash when plan has no stages"
  stage_type: standard
  working_dir: "loom"
  description: |
    Fix crash when initializing empty plan.

    DELTA PROOF (NOTE: Before/after are inverted for bugs):
    - BEFORE: Empty plan causes panic (bug reproducer succeeds at finding the bug)
    - AFTER: Empty plan returns error gracefully (bug reproducer fails to find the bug)

    Verification approach:
    1. Create test case that reproduces the crash
    2. Test should PASS after fix (catches the crash gracefully)
    3. The bug is proven fixed when the panic no longer occurs

  truths:
    - "cargo test test_empty_plan_no_crash"
    - "cargo test --lib plan::parser"

  wiring:
    - source: "src/plan/parser.rs"
      pattern: "if stages.is_empty()"
      description: "Empty stage list check added"
    - source: "src/plan/parser.rs"
      pattern: 'Err.*"Plan must contain at least one stage"'
      description: "Error returned instead of panic"

  artifacts:
    - "tests/empty_plan_tests.rs"
```

**Important:** For bug fixes, the test SHOULD FAIL before the fix (reproducing the bug) and PASS after the fix. The wiring verification proves the defensive code was added.

## Common Pitfalls

### 1. Testing the Wrong Thing

**Bad:**

```yaml
# Adding a new user registration endpoint
truths:
  - "cargo test"  # Too broad - doesn't prove endpoint exists
```

**Good:**

```yaml
truths:
  - "curl -sf -X POST localhost:8080/api/register -d '{\"email\":\"test@example.com\"}' | jq -e '.user_id'"
```

### 2. Not Capturing Enough State

**Bad:**

```yaml
# Adding command output
truths:
  - "loom status"  # Just checks it runs
```

**Good:**

```yaml
truths:
  - "loom status | grep -q 'Active Plan:'"
  - "loom status | grep -q 'Executing:'"
```

### 3. Forgetting This Is About Implementation

Before/after is about what YOUR STAGE changes, not about test setup.

**Bad thinking:** "Before the test runs, I need to set up data. After the test runs, I clean up."
**Good thinking:** "Before my stage, feature X doesn't exist. After my stage, feature X works."

### 4. Using Before/After When Simple Truths Suffice

Overkill:

```yaml
# Just adding a config file
description: |
  BEFORE: config.toml doesn't exist
  AFTER: config.toml exists

truths:
  - "test -f config.toml"
```

Better:

```yaml
artifacts:
  - "config.toml"
```

Reserve before/after thinking for behavioral changes, not simple file additions.

### 5. Bug Fix Direction Confusion

**Wrong:**

```yaml
# Fix infinite loop bug
description: |
  BEFORE: Test passes
  AFTER: Test fails demonstrating the bug
```

**Correct:**

```yaml
# Fix infinite loop bug
description: |
  BEFORE: Code enters infinite loop (bug exists)
  AFTER: Code completes successfully (bug fixed)

truths:
  - "timeout 5s cargo test test_no_infinite_loop"
```

## YAML Structure Reference

Loom has explicit `before_stage` and `after_stage` fields that accept TruthCheck definitions. These run at specific points in the stage lifecycle:

- `before_stage`: Runs BEFORE the agent starts working (verifies pre-conditions in a fresh worktree)
- `after_stage`: Runs when the agent calls `loom stage complete` (verifies post-conditions)

### 1. Before/After Stage Fields (Explicit Delta Proof)

```yaml
before_stage:
  - command: "cargo test test_feature"
    exit_code: 1
    description: "Feature test fails before implementation"

after_stage:
  - command: "cargo test test_feature"
    exit_code: 0
    description: "Feature test passes after implementation"
```

Each entry is a TruthCheck with fields: `command` (required), `exit_code` (default 0), `description`, `stdout_contains`, `stdout_not_contains`, `stderr_empty`.

### 2. Truths (Capture the After State)

```yaml
truths:
  - "command that proves feature works"
  - "test that validates behavior"
```

Truths run AFTER implementation and should succeed.

### 3. Wiring (Prove Integration Points)

```yaml
wiring:
  - source: "src/main.rs"
    pattern: "register_feature"
    description: "Feature registered in main entry point"
```

### 4. Artifacts (Prove Files Exist)

```yaml
artifacts:
  - "src/feature/implementation.rs"
  - "tests/feature_tests.rs"
```

### 5. Stage Description (Document the Delta)

Also document delta-proof thinking in the stage description for human readers:

```yaml
description: |
  Implement feature X.

  DELTA PROOF:
  - BEFORE: <what's true before this stage>
  - AFTER: <what should be true after this stage>

  [Implementation details...]
```

### Complete Example

```yaml
- id: add-metrics-endpoint
  name: "Add /metrics endpoint"
  stage_type: standard
  working_dir: "."
  description: |
    Add Prometheus-compatible /metrics endpoint.

    DELTA PROOF:
    - BEFORE: curl localhost:8080/metrics returns 404
    - AFTER: curl localhost:8080/metrics returns Prometheus format
    - AFTER: Metrics include request_count, response_time

    Implementation:
    - Create metrics middleware
    - Register /metrics endpoint
    - Export request_count and response_time gauges

  dependencies: ["add-middleware-support"]

  before_stage:
    - command: "curl -sf localhost:8080/metrics"
      exit_code: 1
      description: "Metrics endpoint does not exist yet"

  after_stage:
    - command: "curl -sf localhost:8080/metrics | grep -q 'request_count'"
      exit_code: 0
      description: "Metrics endpoint returns request_count"
    - command: "curl -sf localhost:8080/metrics | grep -q 'response_time'"
      exit_code: 0
      description: "Metrics endpoint returns response_time"

  truths:
    - "curl -sf localhost:8080/metrics | grep -q 'request_count'"
    - "curl -sf localhost:8080/metrics | grep -q 'response_time'"
    - "curl -sf localhost:8080/metrics | grep -q 'TYPE request_count counter'"

  wiring:
    - source: "src/routes/mod.rs"
      pattern: "Router.*metrics"
      description: "Metrics endpoint registered"
    - source: "src/middleware/metrics.rs"
      pattern: "pub fn track_metrics"
      description: "Metrics middleware implemented"

  artifacts:
    - "src/middleware/metrics.rs"
    - "src/routes/metrics.rs"

  acceptance:
    - "cargo test"
    - "cargo clippy -- -D warnings"
```

## Integration with Loom Plans

### Planning Phase

When writing stage descriptions:

1. Think: "What can the system do NOW?"
2. Think: "What should the system do AFTER this stage?"
3. Document the delta explicitly
4. Write verification that captures the after state

### Stage Description Template

```yaml
description: |
  [One-line summary of what this stage does]

  DELTA PROOF:
  - BEFORE: [State before this stage - expected to fail/pass]
  - AFTER: [State after this stage - expected to pass/fail]

  [Detailed implementation guidance]

  EXECUTION PLAN:
  [If using subagents, describe parallel work]
```

### Verification Strategy

For each stage, choose verification mechanisms:

| Verification Type | Use When | Proves |
|------------------|----------|--------|
| `truths` | Behavior is observable via shell commands | Feature works at runtime |
| `wiring` | Feature must integrate with existing code | Code is connected/registered |
| `artifacts` | New files must exist | Files were created |
| `acceptance` | Standard checks (build, test, lint) | Code compiles and tests pass |

Use `truths` and `wiring` together for strong delta-proofs.

### Example: Full Stage with Delta Proof

```yaml
- id: add-stage-complete-command
  name: "Add loom stage complete command"
  stage_type: standard
  working_dir: "loom"

  description: |
    Implement `loom stage complete <stage-id>` command to mark stages as complete.

    DELTA PROOF:
    - BEFORE: `loom stage complete --help` fails (command doesn't exist)
    - AFTER: `loom stage complete --help` shows usage
    - AFTER: `loom stage complete test-stage` transitions stage to Completed state

    Implementation:
    - Add StageComplete command to CLI
    - Implement state transition logic
    - Add validation for stage existence
    - Update stage file with completion timestamp

  dependencies: ["knowledge-bootstrap"]

  truths:
    - "loom stage complete --help"
    - "loom stage list | grep -q complete"

  wiring:
    - source: "src/main.rs"
      pattern: "Commands::StageComplete"
      description: "StageComplete command registered in CLI"
    - source: "src/commands/stage.rs"
      pattern: "pub fn complete"
      description: "Stage complete implementation exists"
    - source: "src/models/stage/transitions.rs"
      pattern: "fn transition_to_completed"
      description: "State transition logic implemented"

  artifacts:
    - "src/commands/stage.rs"

  acceptance:
    - "cargo test"
    - "cargo test stage_complete"
    - "cargo clippy -- -D warnings"
```

## Working Directory and Paths

All verification paths are relative to `working_dir`:

```yaml
working_dir: "loom"  # Commands execute from loom/ directory

truths:
  - "cargo test"  # Runs in loom/ (where Cargo.toml lives)

artifacts:
  - "src/commands/verify.rs"  # Resolves to loom/src/commands/verify.rs

wiring:
  - source: "src/main.rs"  # Resolves to loom/src/main.rs
```

If `working_dir: "."`, paths are relative to worktree root.

## Best Practices

1. **Document the delta** in stage descriptions - make before/after explicit
2. **Use truths for runtime behavior** - prove the feature works when invoked
3. **Use wiring for integration** - prove the feature is connected
4. **Use artifacts sparingly** - prefer truths/wiring over file existence
5. **Test the delta** - run truths against the actual implementation
6. **Think from user perspective** - what would a user try to prove it works?

## Summary

Before/after verification proves your stage changed the system:

- **New features**: Before fails → After succeeds
- **Bug fixes**: Before succeeds (bug exists) → After fails (bug gone)
- **Behavior changes**: Before shows old behavior → After shows new behavior

Use `before_stage`/`after_stage` for explicit automated delta-proof, `truths` to capture the after state, `wiring` to prove integration, and `artifacts` to prove files exist.

Always think: "What can I measure that PROVES this stage made a difference?"
