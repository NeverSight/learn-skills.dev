---
name: ln-811-algorithm-optimizer
description: "Optimizes algorithms via autoresearch loop: benchmark, research, hypothesize, keep/discard"
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-811-algorithm-optimizer

**Type:** L3 Worker
**Category:** 8XX Optimization
**Parent:** ln-810-performance-optimization-coordinator

Optimizes target function performance via autoresearch loop: establish baseline benchmark, research best practices, generate 3-7 hypotheses, apply each with keep/discard verification.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | `target_file` + `target_function` (or audit findings from ln-650) |
| **Output** | Optimized function with benchmark proof, optimization report |
| **Pattern** | Autoresearch: modify → benchmark → keep (≥10%) / discard |

---

## Workflow

**Phases:** Pre-flight → Baseline → Research → Hypothesize → Optimize Loop → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Target file exists | Yes | Block optimization |
| Target function identifiable | Yes | Block optimization |
| Test infrastructure | Yes | Block optimization (see ci_tool_detection.md) |
| Test coverage for target function | Yes | Block — no coverage = no safety net |
| Git clean state | Yes | Block (need clean baseline for revert) |
| Benchmark infrastructure | No | Generate benchmark (see references) |

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` — use Benchmarks + Test Frameworks sections.

### Coverage Verification

Before starting optimization, verify target function has test coverage:

| Step | Action |
|------|--------|
| 1 | Grep test files for target function name / imports from target module |
| 2 | If ≥1 test references target → PROCEED |
| 3 | If 0 tests reference target → BLOCK with "no test coverage for {function}" |

> Without test coverage, benchmark improvements are meaningless — the optimized function may produce wrong results faster.

### Worktree & Branch Isolation

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md` — use ln-811 row.

All work (edits, benchmarks, KEEP commits) in worktree. Never modify main worktree.

---

## Phase 1: Establish Baseline

### Step 1.1: Detect or Generate Benchmark

| Situation | Action |
|-----------|--------|
| Existing benchmark found | Use as-is |
| No benchmark exists | Generate minimal benchmark (see [benchmark_generation.md](references/benchmark_generation.md)) |

### Step 1.2: Run Baseline

| Parameter | Value |
|-----------|-------|
| Runs | 5 |
| Metric | Median execution time |
| Warm-up | 1 discarded run |
| Output | `baseline_median`, `baseline_p95` |

Save baseline result — all improvements measured against this.

---

## Phase 2: Research Best Practices

**MANDATORY READ:** Load `shared/references/research_tool_fallback.md` for MCP tool chain.

### Research Strategy

| Priority | Tool | Query Template |
|----------|------|----------------|
| 1 | mcp__context7__query-docs | `"{language} {algorithm_type} optimization techniques"` |
| 2 | mcp__Ref__ref_search_documentation | `"{language} {function_name} performance best practices"` |
| 3 | WebSearch | `"{algorithm_type} optimization {language} benchmark {current_year}"` |

### Research Output

Collect optimization techniques applicable to the target function. For each technique note:
- Name and description
- Expected improvement category (algorithmic complexity, memory, cache, parallelism)
- Applicability conditions (data size, structure, language features)

---

## Phase 3: Generate Hypotheses (3-7)

### Hypothesis Sources

**MANDATORY READ:** Load [optimization_categories.md](references/optimization_categories.md) for category checklist.

| Source | Priority |
|--------|----------|
| Research findings (Phase 2) | 1 |
| Optimization categories checklist | 2 |
| Code analysis (anti-patterns in target) | 3 |

### Hypothesis Format

| Field | Description |
|-------|-------------|
| id | H1, H2, ... H7 |
| category | From optimization_categories.md |
| description | What to change |
| expected_impact | Estimated improvement % |
| risk | Low / Medium / High |
| dependencies | Other hypotheses this depends on |

### Ordering

Sort by: `expected_impact DESC, risk ASC`. Independent hypotheses first (no dependencies).

---

## Phase 4: Optimize Loop (Keep/Discard)

### Per-Hypothesis Cycle

```
FOR each hypothesis (H1..H7):
  1. APPLY: Edit target function (surgical change, function body only)
  2. VERIFY: Run tests
     IF tests FAIL (assertion) → DISCARD (revert) → next hypothesis
     IF tests CRASH (runtime error, OOM, import error):
       IF fixable (typo, missing import) → fix & re-run ONCE
       IF fundamental (design flaw, incompatible API) → DISCARD + log "crash: {reason}"
  3. BENCHMARK: Run 5 times, take median
  4. COMPARE: improvement = (baseline - new) / baseline * 100
     IF improvement >= 10% → KEEP:
       git add {target_file}
       git commit -m "perf(H{N}): {description} (+{improvement}%)"
       new baseline = new median
     IF improvement < 10%  → DISCARD (revert edit)
  5. LOG: Record result to experiment log + report
```

### Safety Rules

| Rule | Description |
|------|-------------|
| Scope | Only target function body; no signature changes |
| Dependencies | No new package installations |
| Revert | `git checkout -- {target_file}` on discard |
| Time budget | 30 minutes total for all hypotheses |
| Compound | Each KEEP becomes new baseline for next hypothesis |
| Traceability | Each KEEP = separate git commit with hypothesis ID in message |
| Isolation | All work in isolated worktree; never modify main worktree |

### Keep/Discard Decision

| Condition | Decision | Action |
|-----------|----------|--------|
| Tests fail | DISCARD | Revert, log reason |
| Improvement ≥ 10% | KEEP | Update baseline |
| Improvement 10-20% BUT complexity increase | REVIEW | Log as "marginal + complex", prefer DISCARD |
| Improvement < 10% | DISCARD | Revert, log as "insufficient gain" |
| Regression (slower) | DISCARD | Revert, log regression amount |

> **Simplicity criterion (per autoresearch):** If improvement is marginal (10-20%) and change significantly increases code complexity (>50% more lines, deeply nested logic, hard-to-read constructs), prefer DISCARD. Simpler code at near-equal performance wins.

---

## Phase 5: Report Results

### Report Schema

| Field | Description |
|-------|-------------|
| target | File path + function name |
| baseline | Original median benchmark |
| final | Final median after all kept optimizations |
| total_improvement | Percentage improvement |
| hypotheses_tested | Total count |
| hypotheses_kept | Count of kept optimizations |
| hypotheses_discarded | Count + reasons |
| optimizations[] | Per-kept: id, category, description, improvement% |

### Experiment Log

Write to `{project_root}/.optimization/ln-811-log.tsv`:

| Column | Description |
|--------|-------------|
| timestamp | ISO 8601 |
| hypothesis_id | H1..H7 |
| category | From optimization_categories.md |
| description | What changed |
| baseline_ms | Baseline median before this hypothesis |
| result_ms | New median after change |
| improvement_pct | Percentage change |
| status | keep / discard / crash |
| commit | Git commit hash (if kept) |

Append to existing file if present (enables tracking across multiple runs).

### Cleanup

| Action | When |
|--------|------|
| Remove generated benchmark | If benchmark was auto-generated AND no kept optimizations |
| Keep generated benchmark | If any optimization was kept (proof of improvement) |

---

## Configuration

```yaml
Options:
  # Target
  target_file: ""
  target_function: ""

  # Benchmark
  benchmark_runs: 5
  improvement_threshold: 10    # percent
  warmup_runs: 1

  # Hypotheses
  max_hypotheses: 7
  min_hypotheses: 3

  # Safety
  time_budget_minutes: 30
  allow_new_deps: false
  scope: "function_body"       # function_body | module

  # Verification
  run_tests: true
  run_lint: false
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No benchmark framework | Stack not in ci_tool_detection.md | Generate inline benchmark |
| All hypotheses discarded | No effective optimization found | Report "no improvements found" |
| Benchmark noise too high | Inconsistent timing | Increase runs to 10, use p50 |
| Test flake | Non-deterministic test | Re-run once; if flakes again, skip hypothesis |

---

## References

- [benchmark_generation.md](references/benchmark_generation.md)
- [optimization_categories.md](references/optimization_categories.md)
- `shared/references/ci_tool_detection.md` (Benchmarks section)
- `shared/references/research_tool_fallback.md`

---

## Definition of Done

- Test coverage for target function verified before optimization
- Target function identified and baseline benchmark established (5 runs, median)
- Research completed via MCP tool chain (Context7/Ref/WebSearch)
- 3-7 hypotheses generated, ordered by expected impact
- Each hypothesis tested: apply → tests → benchmark → keep/discard
- Each kept optimization = separate git commit with hypothesis ID
- Kept optimizations compound (each becomes new baseline)
- Marginal gains (10-20%) with complexity increase reviewed via simplicity criterion
- Tests pass after all kept optimizations
- Experiment log written to `.optimization/ln-811-log.tsv`
- Report returned with baseline, final, improvement%, per-hypothesis results
- Generated benchmark cleaned up if no optimizations kept
- All changes on isolated branch, pushed to remote

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
