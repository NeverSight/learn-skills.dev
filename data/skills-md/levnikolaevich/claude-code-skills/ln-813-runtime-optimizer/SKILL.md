---
name: ln-813-runtime-optimizer
description: "Fixes blocking IO, unnecessary allocations, sync-in-async with keep/discard verification"
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-813-runtime-optimizer

**Type:** L3 Worker
**Category:** 8XX Optimization
**Parent:** ln-810-performance-optimization-coordinator

Fixes runtime performance issues found by ln-653-runtime-performance-auditor. Each fix verified via tests + lint with keep/discard pattern.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Audit findings from `docs/project/persistence_audit.md` (ln-653 section) OR target file |
| **Output** | Optimized code, verification report |
| **Companion** | ln-653-runtime-performance-auditor (finds issues) → ln-813 (fixes them) |

---

## Workflow

**Phases:** Pre-flight → Load Findings → Prioritize → Fix Loop → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Audit findings OR target file | Yes | Block optimization |
| Test infrastructure | Yes | Block (need tests for verification) |
| Linter available | No | Skip lint step in verification |
| Git clean state | Yes | Block (need clean baseline for revert) |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` — use Test Frameworks + Linters sections.

### Worktree & Branch Isolation

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md` — use ln-813 row.

---

## Phase 1: Load Findings

### From Audit Report

Read `docs/project/persistence_audit.md`, extract ln-653 findings:

| Finding Type | Optimization |
|--------------|-------------|
| Blocking IO in async | `asyncio.to_thread()`, `aiofiles`, async HTTP client |
| String concat in loop | `StringBuilder` (.NET), `"".join()` (Python), template literals (JS) |
| Unnecessary allocations | Pre-allocate collections, object pooling, `Span<T>` |
| Sync sleep in async | `asyncio.sleep()`, `Task.Delay()`, `setTimeout` |
| Redundant serialization | Cache serialized form, avoid round-trip JSON in memory |

### From Target File

If no audit report: scan target file for runtime patterns matching the table above.

---

## Phase 2: Prioritize Fixes

| Priority | Criteria |
|----------|----------|
| 1 (highest) | Blocking IO in async context (blocks event loop) |
| 2 | Sync sleep in async (starves thread pool) |
| 3 | Allocations in hot loop (GC pressure) |
| 4 | String concatenation patterns |
| 5 | Other micro-optimizations |

---

## Phase 3: Fix Loop (Keep/Discard)

### Per-Fix Cycle

```
FOR each finding (F1..FN):
  1. APPLY: Edit code (surgical change)
  2. VERIFY: Run tests
     IF tests FAIL → DISCARD (revert) → next finding
  3. VERIFY: Run lint (if available)
     IF lint FAIL → DISCARD (revert) → next finding
  4. BOTH PASS → KEEP
  5. LOG: Record fix for report
```

### Keep/Discard Decision

| Condition | Decision |
|-----------|----------|
| No tests cover affected file/function | SKIP finding — log as "uncovered, skipped" |
| Tests + lint pass | KEEP |
| Tests fail | DISCARD + log reason |
| Lint fail (new warnings) | DISCARD + log reason |
| Lint unavailable | KEEP (tests sufficient) |

---

## Phase 4: Report Results

### Report Schema

| Field | Description |
|-------|-------------|
| source | Audit report path or target file |
| findings_total | Total findings from audit |
| fixes_applied | Successfully kept fixes |
| fixes_discarded | Failed fixes with reasons |
| fix_details[] | Per-fix: finding type, file, before/after description |

---

## Configuration

```yaml
Options:
  # Source
  audit_report: "docs/project/persistence_audit.md"
  target_file: ""

  # Verification
  run_tests: true
  run_lint: true

  # Scope
  fix_types:
    - blocking_io
    - sync_sleep
    - unnecessary_alloc
    - string_concat
    - redundant_serialization
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No audit findings | ln-653 not run or no issues | Report "no findings to optimize" |
| Async rewrite complex | Deep call chain affected | Log as manual step, skip |
| Framework-specific pattern | Unknown async framework | Query Context7/Ref for docs |

---

## References

- `../ln-653-runtime-performance-auditor/SKILL.md` (companion: finds issues)
- `shared/references/ci_tool_detection.md` (test + lint detection)

---

## Definition of Done

- Findings loaded from audit report or target file scan
- Fixes prioritized (blocking IO first, then sync sleep, allocations, string concat)
- Each fix applied with keep/discard: tests + lint pass → keep, either fails → discard
- Report returned with findings total, fixes applied, fixes discarded

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
