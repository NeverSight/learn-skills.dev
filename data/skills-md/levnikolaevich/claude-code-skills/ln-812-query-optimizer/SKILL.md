---
name: ln-812-query-optimizer
description: "Fixes N+1 queries, redundant fetches, over-fetching with keep/discard verification"
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-812-query-optimizer

**Type:** L3 Worker
**Category:** 8XX Optimization
**Parent:** ln-810-performance-optimization-coordinator

Fixes query efficiency issues found by ln-651-query-efficiency-auditor. Each fix verified via tests with keep/discard pattern. Metric: query count reduction (not runtime benchmark).

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Audit findings from `docs/project/persistence_audit.md` (ln-651 section) OR target file |
| **Output** | Optimized queries, verification report |
| **Companion** | ln-651-query-efficiency-auditor (finds issues) → ln-812 (fixes them) |

---

## Workflow

**Phases:** Pre-flight → Load Findings → Prioritize → Fix Loop → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Audit findings OR target file | Yes | Block optimization |
| Test infrastructure | Yes | Block (need tests for verification) |
| Git clean state | Yes | Block (need clean baseline for revert) |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` — use Test Frameworks section for test detection.

### Worktree & Branch Isolation

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md` — use ln-812 row.

---

## Phase 1: Load Findings

### From Audit Report

Read `docs/project/persistence_audit.md`, extract ln-651 findings:

| Finding Type | Optimization |
|--------------|-------------|
| N+1 query | Batch loading / eager loading / `.Include()` / `prefetch_related` |
| Redundant fetch | Pass object instead of ID, cache result |
| Over-fetching | Select specific fields / projection / `.Select()` |
| Missing index hint | Add index annotation / migration |
| Unbounded query | Add `.Take()` / `LIMIT` / pagination |

### From Target File

If no audit report: scan target file for query patterns matching the table above.

---

## Phase 2: Prioritize Fixes

| Priority | Criteria |
|----------|----------|
| 1 (highest) | N+1 in hot path (called per request) |
| 2 | Redundant fetches (same entity loaded multiple times) |
| 3 | Over-fetching (SELECT * where few columns needed) |
| 4 | Missing pagination on user-facing endpoints |

---

## Phase 3: Fix Loop (Keep/Discard)

### Per-Fix Cycle

```
FOR each finding (F1..FN):
  1. APPLY: Edit query code (surgical change)
  2. VERIFY: Run tests
     IF tests FAIL → DISCARD (revert) → next finding
  3. VERIFY: Tests PASS → KEEP
  4. LOG: Record fix for report
```

### Keep/Discard Decision

| Condition | Decision |
|-----------|----------|
| No tests cover affected file/function | SKIP finding — log as "uncovered, skipped" |
| Tests pass | KEEP |
| Tests fail | DISCARD + log failure reason |
| Fix introduces new N+1 | DISCARD |

**Note:** No benchmark needed — query optimization metric is correctness (tests pass) + structural improvement (fewer queries). The audit already identified the inefficiency.

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
  target_file: ""               # Alternative to audit report

  # Verification
  run_tests: true

  # Scope
  fix_types:                    # Filter which types to fix
    - n_plus_one
    - redundant_fetch
    - over_fetching
    - unbounded_query
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No audit findings | ln-651 not run or no issues | Report "no findings to optimize" |
| ORM-specific syntax | Unknown ORM | Query Context7/Ref for ORM docs |
| Migration needed | Index addition requires migration | Log as manual step, skip |

---

## References

- `../ln-651-query-efficiency-auditor/SKILL.md` (companion: finds issues)
- `shared/references/ci_tool_detection.md` (test detection)

---

## Definition of Done

- Findings loaded from audit report or target file scan
- Fixes prioritized (N+1 first, then redundant, over-fetch, unbounded)
- Each fix applied with keep/discard: tests pass → keep, tests fail → discard
- No new query inefficiencies introduced by fixes
- Report returned with findings total, fixes applied, fixes discarded

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
