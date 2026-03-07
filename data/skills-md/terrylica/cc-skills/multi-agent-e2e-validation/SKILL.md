---
name: multi-agent-e2e-validation
description: Multi-agent parallel E2E validation for database refactors. TRIGGERS - E2E validation, schema migration testing, database refactor validation.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Multi-Agent E2E Validation

## Overview

Prescriptive workflow for spawning parallel validation agents to comprehensively test database refactors. Successfully identified 5 critical bugs (100% system failure rate) in QuestDB migration that would have shipped in production.

## When to Use This Skill

Use this skill when:

- Database refactors (e.g., v3.x file-based → v4.x QuestDB)
- Schema migrations requiring validation
- Bulk data ingestion pipeline testing
- System migrations with multiple validation layers
- Pre-release validation for database-centric systems

**Key outcomes:**

- Parallel agent execution for comprehensive coverage
- Structured validation reporting (VALIDATION_FINDINGS.md)
- Bug discovery with severity classification (Critical/Medium/Low)
- Release readiness assessment

## Core Methodology

### 1. Validation Architecture (3-Layer Model)

**Layer 1: Environment Setup**

- Container orchestration (Colima/Docker)
- Database deployment and schema application
- Connectivity validation (ILP, PostgreSQL, HTTP ports)
- Configuration file creation and validation

**Layer 2: Data Flow Validation**

- Bulk ingestion testing (CloudFront → QuestDB)
- Performance benchmarking against SLOs
- Multi-month data ingestion
- Deduplication testing (re-ingestion scenarios)
- Type conversion validation (FLOAT→LONG casts)

**Layer 3: Query Interface Validation**

- High-level query methods (get_latest, get_range, execute_sql)
- Edge cases (limit=1, cross-month boundaries)
- Error handling (invalid symbols, dates, parameters)
- Gap detection SQL compatibility

### 2. Agent Orchestration Pattern

**Sequential vs Parallel Execution:**

```
Agent 1 (Environment) → [SEQUENTIAL - prerequisite]
  ↓
Agent 2 (Bulk Loader) → [PARALLEL with Agent 3]
Agent 3 (Query Interface) → [PARALLEL with Agent 2]
```

**Dependency Rule**: Environment validation must pass before data flow/query validation

**Dynamic Todo Management:**

- Start with high-level plan (ADR-defined phases)
- Prune completed agents from todo list
- Grow todo list when bugs discovered (e.g., Bug #5 found by Agent 3)
- Update VALIDATION_FINDINGS.md incrementally

### 3. Validation Script Structure

Each agent produces:

1. **Test Script** (e.g., `test_bulk_loader.py`)
   - 5+ test functions with clear pass/fail criteria
   - Structured output (test name, result, details)
   - Summary report at end
2. **Artifacts** (logs, config files, evidence)
3. **Findings Report** (bugs, severity, fix proposals)

**Example Test Structure:**

```python
def test_feature(conn):
    """Test 1: Feature description"""
    print("=" * 80)
    print("TEST 1: Feature description")
    print("=" * 80)

    results = {}

    # Test 1a: Subtest name
    print("\n1a. Testing subtest:")
    result_1a = perform_test()
    print(f"   Result: {result_1a}")
    results["subtest_1a"] = result_1a == expected_1a

    # Summary
    print("\n" + "-" * 80)
    all_passed = all(results.values())
    print(f"Test 1 Results: {'✓ PASS' if all_passed else '✗ FAIL'}")
    for test_name, passed in results.items():
        print(f"  - {test_name}: {'✓' if passed else '✗'}")

    return {"success": all_passed, "details": results}
```

### 4. Bug Classification and Tracking

**Severity Levels:**

- 🔴 **Critical**: 100% system failure (e.g., API mismatch, timestamp corruption)
- 🟡 **Medium**: Degraded functionality (e.g., below SLO performance)
- 🟢 **Low**: Minor issues, edge cases

**Bug Report Format:**

```markdown
#### Bug N: Descriptive Name (**SEVERITY** - Status)

**Location**: `file/path.py:line`

**Issue**: One-sentence description

**Impact**: Quantified impact (e.g., "100% ingestion failure")

**Root Cause**: Technical explanation

**Fix Applied**: Code changes with before/after

**Verification**: Test results proving fix

**Status**: ✅ FIXED / ⚠️ PARTIAL / ❌ OPEN
```

### 5. Release Readiness Decision Framework

**Go/No-Go Criteria:**

```
BLOCKER = Any Critical bug unfixed
SHIP = All Critical bugs fixed + (Medium bugs acceptable OR fixed)
DEFER = >3 Medium bugs unfixed OR any High-severity bug
```

**Example Decision:**

- 5 Critical bugs found → all fixed ✅
- 1 Medium bug (performance 55% below SLO) → acceptable ✅
- Verdict: **RELEASE READY**

## Workflow: Step-by-Step

### Step 1: Create Validation Plan (ADR-Driven)

**Input**: ADR document (e.g., ADR-0002 QuestDB Refactor)
**Output**: Validation plan with 3-7 agents

**Plan Structure:**

```markdown
## Validation Agents

### Agent 1: Environment Setup

- Deploy QuestDB via Docker
- Apply schema.sql
- Validate connectivity (ILP, PG, HTTP)
- Create .env configuration

### Agent 2: Bulk Loader Validation

- Test CloudFront → QuestDB ingestion
- Benchmark performance (target: >100K rows/sec)
- Validate deduplication (re-ingestion test)
- Multi-month ingestion test

### Agent 3: Query Interface Validation

- Test get_latest() with various limits
- Test get_range() with date boundaries
- Test execute_sql() with parameterized queries
- Test detect_gaps() SQL compatibility
- Test error handling (invalid inputs)
```

### Step 2: Execute Agent 1 (Environment)

**Directory Structure:**

```
tmp/e2e-validation/
  agent-1-env/
    test_environment_setup.py
    questdb.log
    config.env
    schema-check.txt
```

**Validation Checklist:**

- ✅ Container running
- ✅ Ports accessible (9009 ILP, 8812 PG, 9000 HTTP)
- ✅ Schema applied without errors
- ✅ .env file created

### Step 3: Execute Agents 2-3 in Parallel

**Agent 2: Bulk Loader**

```
tmp/e2e-validation/
  agent-2-bulk/
    test_bulk_loader.py
    ingestion_benchmark.txt
    deduplication_test.txt
```

**Agent 3: Query Interface**

```
tmp/e2e-validation/
  agent-3-query/
    test_query_interface.py
    gap_detection_test.txt
```

**Execution:**

```bash
# Terminal 1
cd tmp/e2e-validation/agent-2-bulk
uv run python test_bulk_loader.py

# Terminal 2
cd tmp/e2e-validation/agent-3-query
uv run python test_query_interface.py
```

### Step 4: Document Findings in VALIDATION_FINDINGS.md

**Template:**

```markdown
# E2E Validation Findings Report

**Validation ID**: ADR-XXXX
**Branch**: feat/database-refactor
**Date**: YYYY-MM-DD
**Target Release**: vX.Y.Z
**Status**: [BLOCKED / READY / IN_PROGRESS]

## Executive Summary

E2E validation discovered **N critical bugs** that would have caused [impact]:

| Finding | Severity | Status | Impact       | Agent   |
| ------- | -------- | ------ | ------------ | ------- |
| Bug 1   | Critical | Fixed  | 100% failure | Agent 2 |

**Recommendation**: [RELEASE READY / BLOCKED / DEFER]

## Agent 1: Environment Setup - [STATUS]

...

## Agent 2: [Name] - [STATUS]

...
```

### Step 5: Iterate on Fixes

**For each bug:**

1. Document in VALIDATION_FINDINGS.md with 🔴/🟡/🟢 severity
2. Apply fix to source code
3. Re-run failing test
4. Update bug status to ✅ FIXED
5. Commit with semantic message (e.g., `fix: correct timestamp parsing in CSV ingestion`)

**Example Fix Commit:**

```bash
git add src/gapless_crypto_clickhouse/collectors/questdb_bulk_loader.py
git commit -m "fix: prevent pandas from treating first CSV column as index

BREAKING CHANGE: All timestamps were defaulting to epoch 0 (1970-01)
due to pandas read_csv() auto-indexing. Added index_col=False to
preserve first column as data.

Fixes #ABC-123"
```

### Step 6: Final Validation and Release Decision

**Run all tests:**

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
cd tmp/e2e-validation
for agent in agent-*; do
    echo "=== Running $agent ==="
    cd $agent
    uv run python test_*.py
    cd ..
done
SKILL_SCRIPT_EOF
```

**Update VALIDATION_FINDINGS.md status:**

- Count Critical bugs: X fixed, Y open
- Count Medium bugs: X fixed, Y open
- Apply decision framework
- Update **Status** field to ✅ RELEASE READY or ❌ BLOCKED

## Real-World Example: QuestDB Refactor Validation

**Context**: Migrating from file-based storage (v3.x) to QuestDB (v4.0.0)

**Bugs Found:**

1. 🔴 **Sender API mismatch** - Used non-existent `Sender.from_uri()` instead of `Sender.from_conf()`
2. 🔴 **Type conversion** - `number_of_trades` sent as FLOAT, schema expects LONG
3. 🔴 **Timestamp parsing** - pandas treating first column as index → epoch 0 timestamps
4. 🔴 **Deduplication** - WAL mode doesn't provide UPSERT semantics (needed `DEDUP ENABLE UPSERT KEYS`)
5. 🔴 **SQL incompatibility** - detect_gaps() used nested window functions (QuestDB unsupported)

**Impact**: Without this validation, v4.0.0 would ship with 100% data corruption and 100% ingestion failure

**Outcome**: All 5 bugs fixed, system validated, v4.0.0 released successfully

## Common Pitfalls

### 1. Skipping Environment Validation

❌ **Bad**: Assume Docker/database is working, jump to data ingestion tests
✅ **Good**: Agent 1 validates environment first, catches port conflicts, schema errors early

### 2. Serial Agent Execution

❌ **Bad**: Run Agent 2, wait for completion, then run Agent 3
✅ **Good**: Run Agent 2 & 3 in parallel (no dependency between them)

### 3. Manual Test Reporting

❌ **Bad**: Copy/paste test output into Slack/email
✅ **Good**: Structured VALIDATION_FINDINGS.md with severity, status, fix tracking

### 4. Ignoring Medium Bugs

❌ **Bad**: "Performance is 55% below SLO, but we'll fix it later"
✅ **Good**: Document in VALIDATION_FINDINGS.md, make explicit go/no-go decision

### 5. No Re-validation After Fixes

❌ **Bad**: Apply fix, assume it works, move on
✅ **Good**: Re-run failing test, update status in VALIDATION_FINDINGS.md

## Resources

### scripts/

Not applicable - validation scripts are project-specific (stored in `tmp/e2e-validation/`)

### references/

- `example_validation_findings.md` - Complete VALIDATION_FINDINGS.md template
- `agent_test_template.py` - Template for creating validation test scripts
- `bug_severity_classification.md` - Detailed severity criteria and examples

### assets/

Not applicable - validation artifacts are project-specific

---

## Troubleshooting

| Issue                          | Cause                          | Solution                                             |
| ------------------------------ | ------------------------------ | ---------------------------------------------------- |
| Container not starting         | Colima/Docker not running      | Run `colima start` before Agent 1                    |
| Port conflicts                 | Ports already in use           | Stop conflicting containers or use different ports   |
| Schema application fails       | Invalid SQL syntax             | Check schema.sql for database-specific compatibility |
| Agent 2/3 fail without Agent 1 | Environment not validated      | Ensure Agent 1 completes before starting Agent 2/3   |
| Test script import errors      | Missing dependencies           | Run `uv pip install` in agent directory              |
| Bug status not updating        | VALIDATION_FINDINGS.md stale   | Manually refresh status after each fix               |
| Parallel agents interference   | Shared resources conflict      | Ensure agents use isolated directories               |
| Decision unclear               | Severity mixed Critical/Medium | Apply Go/No-Go criteria strictly per documentation   |
