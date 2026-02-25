---
name: quality-verify-implementation-complete
description: |
  Verifies that implemented code is actually integrated into the system and executes at runtime,
  preventing "done but not integrated" failures. Use when marking features complete, before moving
  ADRs to completed status, after implementing new modules/nodes/services, or when claiming "feature
  works". Triggers on "verify implementation", "is this integrated", "check if code is wired",
  "prove it runs", or before declaring work complete. Works with Python modules, LangGraph nodes,
  CLI commands, API endpoints, and service classes. Enforces Creation-Connection-Verification (CCV)
  principle.

---

# Verify Implementation Complete

## Quick Start

Before claiming any implementation is "done", run this verification:

```bash
# 1. Check if your new module is imported
grep -r "from.*your_module import\|import.*your_module" src/

# 2. Check if your functions are called
grep -r "your_function_name" src/ --include="*.py" | grep -v test | grep -v "def "

# 3. Run integration verification
./scripts/verify_integration.sh  # If available

# 4. Answer the Four Questions (see below)
```

If any check fails or you cannot answer all four questions, **the implementation is NOT complete**.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. The CCV Principle
4. The Four Questions Test
5. Step-by-Step Verification Process
6. Verification by Artifact Type
7. Common Failure Patterns
8. Supporting Files
9. Expected Outcomes
10. Requirements
11. Red Flags to Avoid

## When to Use This Skill

### Explicit Triggers
- "Verify this implementation is complete"
- "Is this code integrated?"
- "Check if my code is wired into the system"
- "Prove this feature runs"
- "Verify integration for [feature/module]"
- "Run implementation completeness check"

### Implicit Triggers
- Before marking any task as "done" or "complete"
- Before moving an ADR from `in_progress/` to `completed/`
- After creating new Python modules, classes, or functions
- After implementing LangGraph nodes, CLI commands, or API endpoints
- Before claiming "feature works" or "implementation successful"
- When self-reviewing code changes

### Debugging Triggers
- "Why isn't my feature working?" (often it's not integrated)
- "Tests pass but feature doesn't run" (classic integration gap)
- "Code exists but nothing happens" (orphaned code)
- "Feature used to work" (regression - connection removed)

## What This Skill Does

This skill enforces the **Creation-Connection-Verification (CCV) Principle** by:

1. **Verifying Creation** - Confirms artifacts exist (files, tests, types)
2. **Verifying Connection** - Confirms artifacts are wired into the system
3. **Verifying Execution** - Confirms artifacts execute at runtime
4. **Providing Evidence** - Generates proof that all three phases are complete

**This skill prevents the ADR-013 failure mode** where code was created and tested but never integrated into `builder.py`, causing the feature to never execute despite passing all quality gates.

## The CCV Principle

### The Formula

```
COMPLETE = CREATION + CONNECTION + VERIFICATION
```

### The Three Phases

| Phase | Proves | Evidence Required |
|-------|--------|-------------------|
| **CREATION** | Artifact exists | File written, tests pass, types check, linting clean |
| **CONNECTION** | Artifact is wired in | Import statement, registration call, configuration entry |
| **VERIFICATION** | Artifact executes | Logs showing execution, output observed, state changes confirmed |

**Missing any phase = Implementation is INCOMPLETE**

### Why All Three Are Required

- **Creation without Connection** → Dead code that never runs
- **Connection without Verification** → Unknown if it actually works
- **Creation + Connection without Verification** → Might work, might not, no proof

## The Four Questions Test

Before claiming "done", you MUST answer ALL FOUR questions:

### Question 1: How do I trigger this?
**What it means:** What user action, CLI command, API call, or system event causes this code to execute?

**Examples:**
- `uv run temet-run -a talky -p "analyze code"`
- `curl -X POST /api/endpoint`
- `from myapp.service import MyService; MyService().method()`

**If you cannot answer:** Feature has no entry point → NOT COMPLETE

### Question 2: What connects it to the system?
**What it means:** Where is the import, registration, or wiring that makes this code reachable?

**Examples:**
- `builder.py line 45: from .architecture_nodes import create_review_node`
- `main.py line 12: app.add_command(my_command)`
- `container.py line 67: container.register(MyService)`

**If you cannot answer:** Code is orphaned → NOT COMPLETE

### Question 3: What evidence proves it runs?
**What it means:** What logs, traces, or observable output demonstrates execution?

**Examples:**
- `[2025-12-07 10:30:45] INFO architecture_review_triggered`
- `✓ Task completed successfully (in CLI output)`
- `HTTP 200 OK (in curl response)`

**If you cannot answer:** No execution proof → NOT COMPLETE

### Question 4: What shows it works correctly?
**What it means:** What output, state change, or behavior proves correct function?

**Examples:**
- `state.architecture_review = ArchitectureReviewResult(status=APPROVED)`
- `Database row inserted with expected values`
- `File created with correct contents`

**If you cannot answer:** No outcome proof → NOT COMPLETE

## Step-by-Step Verification Process

### Phase 1: Verify Creation (Artifacts Exist)

Run standard quality gates:

```bash
# Type checking
uv run mypy src/

# Linting
uv run ruff check .

# Unit tests
uv run pytest tests/unit/ --no-cov -v
```

**Checklist:**
- [ ] Files exist with complete implementations (no stubs/TODOs)
- [ ] Unit tests pass (isolated behavior verified)
- [ ] Type checking passes (no type errors)
- [ ] Linting passes (code style clean)

**If any fail:** Fix before proceeding to Phase 2

### Phase 2: Verify Connection (Wiring Exists)

#### 2.1 Check Import Statements

For a new module `your_module.py`:

```bash
# Find all imports of your module
grep -r "from.*your_module import\|import.*your_module" src/ --include="*.py" | grep -v test
```

**Expected:** At least one import in production code (not just tests)

**If empty:** Module is NOT imported → NOT CONNECTED

#### 2.2 Check Call-Sites

For a new function `your_function`:

```bash
# Find all call-sites
grep -r "your_function" src/ --include="*.py" | grep -v test | grep -v "def your_function"
```

**Expected:** At least one call-site in production code

**If empty:** Function is never called → NOT CONNECTED

#### 2.3 Check Registration (if applicable)

For components that require registration:

```bash
# LangGraph nodes
grep -E "add_node.*your_node|from.*your_module" src/coordination/graph/builder.py

# CLI commands
grep -r "add_command\|@.*\.command\|@click\.command" src/ | grep your_command

# DI container
grep -r "container\.register\|container\.provide" src/ | grep YourService

# API routes
grep -r "router\.add\|@.*\.route\|@app\." src/ | grep your_endpoint
```

**Expected:** Registration code exists

**If empty:** Component is NOT registered → NOT CONNECTED

**Checklist:**
- [ ] Module imported in at least one production file
- [ ] Functions/classes called in at least one production path
- [ ] (If applicable) Component registered in system
- [ ] Can trace path from entry point to your code

**If any fail:** Wire the code before proceeding to Phase 3

### Phase 3: Verify Execution (Runtime Proof)

#### 3.1 Trigger the Feature

Execute the actual entry point:

```bash
# Example: CLI command
uv run temet-run -a talky -p "test command"

# Example: API endpoint
curl -X POST http://localhost:8000/api/endpoint -d '{"test": "data"}'

# Example: Direct invocation
uv run python -c "from myapp.service import MyService; MyService().method()"
```

**Observe:** Command completes without errors

#### 3.2 Capture Execution Evidence

Look for evidence that YOUR code executed:

```bash
# Check logs for your module
grep "your_module\|your_function" logs/daemon.log

# Check structured logs
grep "your_module" logs/*.jsonl | jq .

# Check database for expected changes
sqlite3 app.db "SELECT * FROM your_table WHERE created_at > datetime('now', '-1 minute')"
```

**Expected:** Evidence that your code path was executed

**If no evidence:** Code path was not reached → NOT VERIFIED

#### 3.3 Confirm Correct Behavior

Verify the outcome matches expectations:

```bash
# Check state changes
# Example: LangGraph state field populated
assert result.your_field is not None

# Example: File created
ls -la expected_output_file.txt

# Example: Database row inserted
# (query from 3.2)
```

**Expected:** Behavior matches specification

**If incorrect:** Implementation has bugs → NOT VERIFIED

**Checklist:**
- [ ] Feature can be triggered via documented entry point
- [ ] Logs/traces show code execution
- [ ] Expected outcome observed (state change, output, etc.)
- [ ] Can answer all Four Questions

**If any fail:** Debug and fix before claiming "done"

## Verification by Artifact Type

### LangGraph Nodes

**Creation:**
- [ ] Node file exists (e.g., `architecture_nodes.py`)
- [ ] Factory function implemented (e.g., `create_architecture_review_node()`)
- [ ] Routing function implemented (e.g., `should_review_architecture()`)
- [ ] Unit tests pass

**Connection:**
```bash
# Verify import
grep "architecture_nodes" src/temet_run/coordination/graph/builder.py

# Expected output:
# from .architecture_nodes import create_architecture_review_node, should_review_architecture
```

- [ ] Imported in `builder.py`
- [ ] Node added to graph: `graph.add_node("your_node", node)`
- [ ] Edges wired: `graph.add_conditional_edges(...)` or `graph.add_edge(...)`

**Verification:**
```bash
# Add to test_graph_completeness.py
EXPECTED_NODES = [
    "your_node_name",  # Add this
    # ... other nodes
]
```

- [ ] Node in `EXPECTED_NODES` list
- [ ] Integration test passes
- [ ] Coordinator execution shows node in logs
- [ ] State field populated after execution

### CLI Commands

**Creation:**
- [ ] Command function exists
- [ ] Decorated with `@click.command()` or `@app.command()`
- [ ] Tests pass

**Connection:**
```bash
# Verify registration
grep -r "add_command\|@.*\.command" src/your_app/cli/ | grep your_command_name
```

- [ ] Command registered in CLI group
- [ ] Shows in `--help` output

**Verification:**
```bash
# Test command
uv run your-app your-command --help
uv run your-app your-command [args]
```

- [ ] Command appears in `--help`
- [ ] Command executes without errors
- [ ] Expected output observed

### Service Classes (with DI)

**Creation:**
- [ ] Service class exists
- [ ] Methods implemented
- [ ] Unit tests pass

**Connection:**
```bash
# Verify DI registration
grep -r "container\.register\|register_singleton\|provide" src/ | grep YourServiceName
```

- [ ] Service registered in container
- [ ] Dependencies injected correctly

**Verification:**
```bash
# Test injection
uv run python -c "
from your_app.container import container
service = container.resolve('YourService')
service.method()
"
```

- [ ] Service can be resolved from container
- [ ] Method executes correctly
- [ ] Dependencies are provided

### API Endpoints

**Creation:**
- [ ] Endpoint function exists
- [ ] Route handler implemented
- [ ] Tests pass

**Connection:**
```bash
# Verify route registration
grep -r "router\.add\|@.*\.route\|@app\." src/ | grep your_endpoint
```

- [ ] Route added to router
- [ ] Endpoint shows in OpenAPI docs (if applicable)

**Verification:**
```bash
# Test endpoint
curl -X POST http://localhost:8000/api/your-endpoint -d '{"test": "data"}'
```

- [ ] Endpoint responds (not 404)
- [ ] Expected status code (200, 201, etc.)
- [ ] Response body correct

## Common Failure Patterns

### Pattern 1: Created But Never Imported

**Symptom:** File exists, tests pass, but nothing uses it

**Detection:**
```bash
grep -r "from.*your_module import" src/ --include="*.py" | grep -v test
# Returns: (empty)
```

**Fix:** Add import where the module should be used

### Pattern 2: Imported But Never Called

**Symptom:** Import exists, but functions never invoked

**Detection:**
```bash
grep -r "your_function_name" src/ --include="*.py" | grep -v test | grep -v "def "
# Returns: (empty - only the definition exists)
```

**Fix:** Add call-site where the function should be used

### Pattern 3: Registered But Wrong Configuration

**Symptom:** Component registered, but with wrong parameters/order

**Detection:** Integration tests fail, runtime errors

**Fix:** Review registration code, compare with working examples

### Pattern 4: Unit Tests Pass, Integration Fails

**Symptom:** Isolated tests work, but feature fails in real system

**Detection:** Integration tests fail, or manual testing shows errors

**Fix:** Add integration tests that exercise real dependencies

### Pattern 5: Code Reachable But Conditional Never Triggers

**Symptom:** Code is wired, but conditional logic prevents execution

**Detection:** Code never appears in logs despite feature being triggered

**Fix:** Review conditional logic, adjust trigger conditions

## Supporting Files

### References
- `references/ccv-principle.md` - Deep dive into Creation-Connection-Verification
- `references/four-questions-framework.md` - Detailed explanation of the Four Questions
- `references/adr-013-case-study.md` - Real-world failure that motivated this skill

### Examples
- `examples/langgraph-node-verification.md` - Complete LangGraph node verification example
- `examples/cli-command-verification.md` - CLI command verification walkthrough
- `examples/service-di-verification.md` - Service with DI verification example

### Scripts
- `scripts/verify_integration.sh` - Automated orphan detection script
- `scripts/check_imports.sh` - Check if module is imported
- `scripts/check_callsites.sh` - Check if functions are called

### Templates
- `templates/verification-checklist.md` - Copy-paste checklist for feature verification
- `templates/integration-test-template.py` - Template for integration tests

## Expected Outcomes

### Successful Verification

```
✅ Implementation Verification Complete

Feature: ArchitectureReview Node
Location: src/temet_run/coordination/graph/architecture_nodes.py

Phase 1: CREATION ✅
  - File exists (175 lines)
  - Unit tests pass (24/24)
  - Type checking clean
  - Linting clean

Phase 2: CONNECTION ✅
  - Imported in: builder.py line 12
  - Registered: graph.add_node("architecture_review", node)
  - Edges: Conditional edge from "query_claude"
  - Evidence:
    $ grep "architecture_nodes" src/coordination/graph/builder.py
    from .architecture_nodes import create_architecture_review_node

Phase 3: VERIFICATION ✅
  - Integration test: EXPECTED_NODES includes "architecture_review"
  - Execution proof:
    [2025-12-07 10:30:45] INFO architecture_review_triggered
    [2025-12-07 10:30:46] INFO architecture_review_complete status=approved
  - Outcome proof: state.architecture_review = ArchitectureReviewResult(...)

Four Questions Test ✅
  1. Trigger: uv run temet-run -a talky -p "Write code"
  2. Connection: builder.py line 12 (import), line 146 (add_node)
  3. Execution: Logs above show node executed
  4. Outcome: state.architecture_review contains approval data

✅ IMPLEMENTATION IS COMPLETE
```

### Verification Failure

```
❌ Implementation Verification Failed

Feature: ArchitectureReview Node
Location: src/temet_run/coordination/graph/architecture_nodes.py

Phase 1: CREATION ✅
  - File exists (175 lines)
  - Unit tests pass (24/24)
  - Type checking clean
  - Linting clean

Phase 2: CONNECTION ❌
  - Imported in: NOT FOUND
  - Evidence:
    $ grep "architecture_nodes" src/coordination/graph/builder.py
    (empty - no imports found)

CRITICAL FAILURE: Module is not imported in builder.py

❌ IMPLEMENTATION IS INCOMPLETE

Required Actions:
1. Add import in builder.py: from .architecture_nodes import create_architecture_review_node
2. Register node: graph.add_node("architecture_review", review_node)
3. Add edges to wire into workflow
4. Re-run verification after fixes

DO NOT claim this feature is "done" until verification passes.
```

## Requirements

### Tools Required
- Read (to examine source files)
- Grep (to search for imports/calls)
- Bash (to run verification commands)

### Knowledge Required
- Understanding of the project's architecture
- Knowledge of where entry points are (main.py, builder.py, etc.)
- Familiarity with import paths and module structure

### Environment Required
- Working directory is project root
- Source code in `src/` directory
- Tests in `tests/` directory

## Red Flags to Avoid

### Do Not
- ❌ Claim "feature complete" without running this verification
- ❌ Skip Phase 2 (connection) verification
- ❌ Skip Phase 3 (runtime) verification
- ❌ Accept "tests pass" as proof of integration
- ❌ Move ADRs to `completed/` without this verification
- ❌ Self-approve without answering Four Questions
- ❌ Assume code is integrated just because it compiles
- ❌ Trust unit tests alone (they can hide orphaned code)

### Do
- ✅ Run all three phases of verification
- ✅ Paste actual command output as evidence
- ✅ Answer all Four Questions before claiming "done"
- ✅ Add integration tests for new components
- ✅ Update `EXPECTED_NODES` or equivalent tracking lists
- ✅ Show execution logs as proof
- ✅ Verify correct behavior, not just "no errors"
- ✅ Document evidence in task/ADR completion notes

## Notes

- This skill was created in response to ADR-013 failure (2025-12-07)
- The failure: 313 lines of code, 46 passing tests, but code never integrated
- This skill prevents that exact failure mode from recurring
- Integrate this skill with `util-manage-todo` (three-phase pattern)
- Integrate with `create-adr-spike` (Phase 6: Integration Verification)
- Integrate with `quality-run-quality-gates` (add as Gate 6)

**Remember:** Code is not "done" when it compiles and tests pass. Code is "done" when it executes at runtime and produces correct outcomes.
