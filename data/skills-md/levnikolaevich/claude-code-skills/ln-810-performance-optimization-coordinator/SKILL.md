---
name: ln-810-performance-optimization-coordinator
description: "Coordinates performance optimization: algorithm, query, and runtime workers in parallel"
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-810-performance-optimization-coordinator

**Type:** L2 Domain Coordinator
**Category:** 8XX Optimization

Coordinates performance optimization by delegating to L3 workers: ln-811 (algorithm), ln-812 (query), ln-813 (runtime). Workers run in parallel when inputs are independent.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Target file/module OR audit report (ln-650 output) |
| **Output** | Optimized code with verification proof |
| **Workers** | ln-811 (algorithm), ln-812 (query), ln-813 (runtime) |

---

## Workflow

**Phases:** Pre-flight → Analyze Input → Delegate → Collect → Verify → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Target file OR audit report | Yes | Block optimization |
| Git clean state | Yes | Block (need clean baseline for revert) |
| Test infrastructure | Yes | Block (workers need tests for keep/discard) |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` for test/build detection.

---

## Phase 1: Analyze Input

### Input Sources

| Source | Detection | Workers Activated |
|--------|-----------|-------------------|
| `docs/project/persistence_audit.md` | ln-650 output exists | ln-812 (query) + ln-813 (runtime) |
| Target file + function | User-specified | ln-811 (algorithm) |
| Full audit report | All ln-65X sections present | All three workers |

### Worker Selection

| Condition | ln-811 | ln-812 | ln-813 |
|-----------|--------|--------|--------|
| Target function specified | Yes | No | No |
| ln-651 findings present | No | Yes | No |
| ln-653 findings present | No | No | Yes |
| All audit findings | Conditional* | Yes | Yes |

*ln-811 activated only if specific algorithmic inefficiency identified in audit.

---

## Phase 2: Delegate to Workers

> **CRITICAL:** All delegations use Task tool with `subagent_type: "general-purpose"` and `isolation: "worktree"` — each worker creates its own branch per `shared/references/git_worktree_fallback.md`.

### Delegation Protocol

```
FOR each selected worker:
  Task(description: "Optimize via ln-81X",
       prompt: "Execute ln-81X-{worker}. Read skill from ln-81X-{worker}/SKILL.md. Context: {delegationContext}",
       subagent_type: "general-purpose",
       isolation: "worktree")
```

### Delegation Context

| Field | Type | Description |
|-------|------|-------------|
| projectPath | string | Absolute path to project |
| auditReport | string | Path to persistence_audit.md (if applicable) |
| targetFile | string | Target file path (if applicable) |
| targetFunction | string | Target function name (if applicable) |
| options.runTests | bool | Run tests after optimization |
| options.runLint | bool | Run lint after optimization |

### Parallelism

| Workers | Can Parallel | Reason |
|---------|-------------|--------|
| ln-812 + ln-813 | Yes | Different files, different fix types |
| ln-811 + ln-812 | Depends | Only if targeting different files |
| ln-811 + ln-813 | Depends | Only if targeting different files |

**Rules:**
- If workers target the SAME file, run sequentially (ln-811 first, then ln-812/813).
- **Dependent workers share branch:** If worker B depends on worker A's output (e.g., ln-813 needs ln-812's query changes), launch worker B in worker A's branch — so B sees A's changes.

---

## Phase 3: Collect Results

Each worker produces an isolated branch. Coordinator aggregates branch reports.

### Worker Branches

| Worker | Branch Pattern | Contents |
|--------|---------------|----------|
| ln-811 | `optimize/ln-811-{function}-{ts}` | Algorithm optimizations with benchmarks |
| ln-812 | `optimize/ln-812-{ts}` | Query optimizations |
| ln-813 | `optimize/ln-813-{ts}` | Runtime optimizations |

### Result Schema

| Field | Type | Description |
|-------|------|-------------|
| worker | string | ln-811, ln-812, or ln-813 |
| status | enum | success, partial, failed |
| branch | string | Worker's result branch name |
| fixes_applied | int | Number of kept optimizations |
| fixes_discarded | int | Number of discarded attempts |
| details | object | Worker-specific report |

---

## Phase 4: Aggregate Reports

Each worker verified independently in its branch (tests, build, lint run by worker itself). Coordinator does NOT rerun verification or revert worker changes.

### On Failure

1. Branch with failing tests logged as "failed" in report
2. User reviews failed branch independently

---

## Phase 5: Report Summary

### Report Schema

| Field | Description |
|-------|-------------|
| input_source | Audit report or target file |
| workers_activated | Which workers ran |
| total_fixes_applied | Sum across all workers |
| total_fixes_discarded | Sum across all workers |
| build_verified | PASSED or FAILED |
| per_worker[] | Individual worker reports |
| algorithm_improvement | Benchmark improvement % (ln-811 only) |

---

## Configuration

```yaml
Options:
  # Input
  audit_report: "docs/project/persistence_audit.md"
  target_file: ""
  target_function: ""

  # Workers
  enable_algorithm: true
  enable_query: true
  enable_runtime: true

  # Verification
  run_tests: true
  run_build: true
  run_lint: true

  # Safety
  revert_on_build_failure: true
```

---

## Error Handling

### Recoverable Errors

| Error | Recovery |
|-------|----------|
| Worker timeout | Log timeout, continue with other workers |
| Single worker failure | Revert worker changes, report partial success |
| Build failure | Revert last worker, re-verify |

### Fatal Errors

| Error | Action |
|-------|--------|
| No workers activated | Report "no optimization targets found" |
| All workers failed | Report failures, suggest manual review |
| Dirty git state | Block with "commit or stash changes first" |

---

## References

- `../ln-811-algorithm-optimizer/SKILL.md`
- `../ln-812-query-optimizer/SKILL.md`
- `../ln-813-runtime-optimizer/SKILL.md`
- `shared/references/ci_tool_detection.md`

---

## Definition of Done

- Input analyzed (audit report or target file/function)
- Appropriate workers selected based on input type
- Workers delegated with worktree isolation (`isolation: "worktree"`)
- Each worker produces isolated branch, pushed to remote
- Coordinator report aggregates per-worker results (branch, fixes, status)

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
