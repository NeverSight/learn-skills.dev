---
name: perf-benchmark
description: >
  Use when profiling Linux Python or C workloads for algorithmic scaling,
  cache, branch, memory, or ASM bottlenecks, or when comparing a new benchmark
  run against a saved performance baseline.
---

# Performance Benchmark Pipeline

## Overview

Use this skill to systematically profile and score performance of Python + C
projects on Linux. It orchestrates industry-standard tools across 4 tiers of
increasing depth, scores a 7-dimension rubric, and outputs priority-ordered
prescriptions.

This skill is intentionally repo-agnostic when you provide the benchmark
entrypoint explicitly. Pytest benchmark autodiscovery is a convenience for Python repos.

## Use This Skill When

1. You need to profile CPU, cache, branch, or memory behavior of hot code.
2. You want to detect algorithmic scaling issues (O(n) vs O(n^2)) before micro-optimizing.
3. You need a baseline benchmark for regression comparison.
4. You want to identify whether a bottleneck is algorithmic, data-layout, or hardware-level.
5. You need ASM-level analysis of compiled code (C extensions, Numba JIT).

## Outputs

1. `benchmark_report.md` — unified human-readable report with rubric scorecard, findings, prescriptions.
2. `benchmark_summary.json` — machine-readable scores and raw metrics for baseline/regression.
3. `tier1/` — pytest-benchmark JSON, tracemalloc JSON, GNU time output.
4. `tier2/` — cachegrind + callgrind annotated outputs.
5. `tier3/` — massif heap profile, perf stat counters, and opt-in native `perf record/report` artifacts.
6. `tier4/` — objdump disassembly, Numba ASM (if `--asm-audit`).

## Workflow

### 1. Check Prerequisites

The script auto-checks at startup:
- Python >= 3.10
- `valgrind` (required for Tier 2+)
- `perf_event_paranoid` (perf stat requires <= 1)
- CPU governor (warns if not `performance`)
- Cache topology (auto-detected from sysfs for accurate Valgrind simulation)
- Available RAM (warns if insufficient for parallel Valgrind)

### 2. Discover or Specify Targets

Auto-discovers `pytest.mark.benchmark` tests and `tests/benchmarks/` directories.
Override with `--target "cmd {SIZE}"` or `--binary ./path/to/program`.
Use `--target` or `--binary` for non-pytest repos.
Multi-size explicit targets must include `{SIZE}`.
Single-size explicit targets must also include `{SIZE}` when `--sizes` is present; otherwise omit `--sizes`.

### 3. Run Pipeline

```bash
python /path/to/perf-benchmark/scripts/perf_benchmark_pipeline.py \
  --root /path/to/repo \
  --target "python -m benchmark_entrypoint {SIZE}" \
  --source-prefix path/to/source/ \
  --tier medium \
  --sizes 10000,100000 \
  --out-dir /tmp/perf-bench
```

Tier options:
- `fast`: Tier 1 only (pytest-benchmark + tracemalloc + GNU time). Seconds.
- `medium`: Tiers 1-2 (+ cachegrind + callgrind). Minutes.
- `deep`: Tiers 1-3 (+ massif + perf stat). Minutes.
- `asm`: All tiers including Tier 4 ASM audit.

Native sampled hotspots are opt-in via `--perf-record`. When enabled and `perf`
is available, Tier 3 also runs `perf record` + `perf report --stdio` and writes
raw artifacts plus a compact hotspot summary.

### 4. Review Rubric Scores

7 dimensions scored 0-4 each (max 28), in priority order:

| Priority | Dimension | Impact | Tool |
|---|---|---|---|
| 1 (highest) | Algorithmic Scaling | 100-1000x | pytest-benchmark + callgrind |
| 2 | L1 Cache Efficiency | 5-20x | cachegrind |
| 2 | Last-Level Cache | 5-20x | cachegrind |
| 2 | Memory Profile | 5-20x | massif + tracemalloc |
| 3 | Wall-Time Stability | quality gate | pytest-benchmark / time |
| 3 | CPU Efficiency | 2-5x | callgrind + perf stat |
| 3 | Branch Prediction | 2-5x | cachegrind / perf stat |

If Dimension 0 (Algorithmic Scaling) is FAIL, the report prints a STOP warning:
fix algorithmic issues before pursuing hardware optimizations.
If Dimension 0 is `N/A`, the report lists the missing sub-check evidence.
Full Algorithmic Scaling scoring requires `deep` or `asm` because allocation churn comes from massif.

### 5. Apply Prescriptions

Each FAIL/WARN dimension maps to concrete optimization patterns.
See `references/rubric.md` for thresholds and `references/tool-guide.md` for
tool selection guidance.

### Algorithm Diagnosis Playbook

Use this advisory checklist before dropping into cache, branch, or ASM work:

- Confirm measured growth matches the expected complexity class before tuning constants.
- Prefer a lower asymptotic class or smaller search space before hardware-level work.
- Replace full recomputation with incremental maintenance when updates are local.
- Process the delta, not the full retained history; bound per-update work to changed inputs.
- Remove redundant passes, rereads, and copies of unchanged data.
- Add indexes, partitions, caches, or summaries so queries touch only required state.
- For streaming workloads, check whether per-update work scales with delta size or total state size.

Use `references/question-bank.md` for the fuller advisory diagnosis prompts.

### 6. Regression Comparison (Optional)

```bash
python scripts/perf_benchmark_pipeline.py \
  --root . \
  --out-dir /tmp/bench \
  --target "./path/to/benchmark {SIZE}" \
  --baseline /path/to/previous/benchmark_summary.json
```

Any scored dimension dropping >= 1 tier from baseline is surfaced in the
report and summary as a regression blocker.

## Agent Parallelism Opportunities

After the script completes, analysis can be parallelized across sub-agents:

Tier 1 stays isolated because timing and tracemalloc measurements are noise-sensitive.
Preferred subagent split: per-artifact or per-rubric-dimension after the pipeline finishes.

**Phase 1** (before script): prerequisites check || target discovery

**Phase 2** (after script): each tool output parsed by independent sub-agent:
- parse tier1/pytest_benchmark.json
- parse tier2/cachegrind_annotated.txt
- parse tier2/callgrind_annotated.txt
- parse tier3/massif.out
- parse tier3/perf_stat.txt
- parse tier4/objdump_*.txt

**Phase 3**: rubric dimensions scored independently in parallel.

**Phase 4**: prescriptions written independently per dimension.

Sub-agents return structured findings matching `references/finding-schema.json`.

## Framework-Specific Notes

- **Numba**: Pass `--env NUMBA_DISABLE_JIT=1` for coverage; omit for actual JIT benchmarks.
- **ctypes/CFFI**: C extensions loaded via Python — use `--source-prefix` to filter Valgrind noise.
- **Standalone C**: Use `--binary ./path/to/program` to skip Python entirely.
- **Hybrid CPUs** (Intel Alder/Raptor Lake): cachegrind simulates P-core cache hierarchy.

## Quick Reference

```bash
# Fast check (seconds)
python scripts/perf_benchmark_pipeline.py --root . --out-dir /tmp/b --tier fast --target "python -m benchmark_entrypoint {SIZE}" --sizes 10000,100000

# Medium with source filtering
python scripts/perf_benchmark_pipeline.py --root . --out-dir /tmp/b --tier medium --target "./path/to/benchmark {SIZE}" --source-prefix path/to/source/ --sizes 10000,100000

# Deep with regression baseline
python scripts/perf_benchmark_pipeline.py --root . --out-dir /tmp/b --tier deep --target "./path/to/benchmark {SIZE}" --baseline /path/to/previous/benchmark_summary.json --sizes 10000,100000

# Deep with opt-in native hotspot sampling
python scripts/perf_benchmark_pipeline.py --root . --out-dir /tmp/b --tier deep --target "./path/to/benchmark {SIZE}" --sizes 10000,100000 --perf-record

# ASM audit for C binary
python scripts/perf_benchmark_pipeline.py --root . --out-dir /tmp/b --tier asm --binary ./path/to/program --asm-audit
```

## References

1. [`references/rubric.md`](references/rubric.md): 7-dimension scoring rubric.
2. [`references/tool-guide.md`](references/tool-guide.md): tool selection decision tree.
3. [`references/asm-checklist.md`](references/asm-checklist.md): 6-pattern ASM reading guide.
4. [`references/question-bank.md`](references/question-bank.md): performance audit questions.
5. [`references/finding-schema.json`](references/finding-schema.json): sub-agent return format.
6. [`references/sample-report.md`](references/sample-report.md): annotated example output.

## Known Limitations

- Valgrind cachegrind simulates 2-level cache (L1 -> LL). No separate L2.
- Valgrind adds 20-50x slowdown. Use `--valgrind-size` for large inputs.
- `perf stat` requires `perf_event_paranoid <= 1`.
- `--perf-record` is opt-in and also requires `perf_event_paranoid <= 1`.
- `tracemalloc` is Python-only. C memory uses massif exclusively.
- Dimension 0 requires benchmarks at >= 2 input sizes.
- callgrind heuristics cannot determine argument identity (memoization needs manual check).
