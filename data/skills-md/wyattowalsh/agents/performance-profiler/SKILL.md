---
name: performance-profiler
description: >-
  Performance analysis: complexity estimation, profiler output parsing, caching
  design, regression risk. Use for optimization guidance. NOT for running
  profilers, load tests, or monitoring.
argument-hint: "<mode> [target]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Performance Profiler

Analysis-based performance review. Every recommendation grounded in evidence.
6-mode pipeline: Analyze, Profile, Cache, Benchmark, Regression, Leak-Patterns.

**Scope:** Performance analysis and recommendations only. NOT for running profilers, executing load tests, infrastructure monitoring, or actual memory leak detection. This skill provides analysis-based guidance, not measurements.

## Canonical Vocabulary

Use these terms exactly throughout all modes:

| Term | Definition |
|------|-----------|
| **complexity** | Big-O algorithmic classification of a function or code path |
| **hotspot** | Code region with disproportionate resource consumption (time or memory) |
| **bottleneck** | System constraint limiting overall throughput |
| **profiler output** | Textual data from cProfile, py-spy, perf, or similar tools pasted by user |
| **cache strategy** | Eviction policy + write policy + invalidation approach for a caching layer |
| **benchmark skeleton** | Template code for measuring function performance with proper methodology |
| **regression risk** | Likelihood that a code change degrades performance, scored LOW/MEDIUM/HIGH/CRITICAL |
| **anti-pattern** | Known performance-harmful code pattern (N+1, unbounded allocation, etc.) |
| **evidence** | Concrete proof: AST analysis, profiler data, code pattern match, or external reference |
| **recommendation** | Actionable optimization suggestion with expected impact and trade-offs |
| **flame graph** | Hierarchical visualization of call stack sampling data |
| **wall time** | Elapsed real time (includes I/O waits) vs CPU time (compute only) |

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `analyze <file/function>` | Algorithmic complexity analysis, Big-O review |
| `profile <data>` | Interpret textual profiler output (cProfile, py-spy, perf) |
| `cache <system>` | Caching strategy design (LRU/LFU/TTL/write-through/write-back) |
| `benchmark <code>` | Benchmark design and methodology review |
| `regression <diff>` | Performance regression risk assessment from code diff |
| `leak-patterns` | Common memory leak pattern scan (NOT actual detection) |
| Empty | Show mode menu with examples for each mode |

## Mode 1: Analyze

Algorithmic complexity analysis for files or functions.

### Analyze Step 1: Scan

Run the complexity estimator script:

```
uv run python skills/performance-profiler/scripts/complexity-estimator.py <path>
```

Parse JSON output. If script fails, perform manual AST-level analysis.

### Analyze Step 2: Classify

For each function in scope:

1. Identify loop nesting depth, recursion patterns, data structure operations
2. Map to Big-O classification using `references/complexity-patterns.md`
3. Score hotspot risk: nesting depth * call frequency * data size sensitivity
4. Flag functions with O(n^2) or worse in hot paths

### Analyze Step 3: Report

Present findings as a table:

| Function | Estimated Complexity | Evidence | Hotspot Risk | Recommendation |
|----------|---------------------|----------|-------------|----------------|

Include trade-off analysis for each recommendation.

## Mode 2: Profile

Interpret textual profiler output pasted by the user.

### Profile Step 1: Parse

Run the profile parser script on user-provided data:

```
uv run python skills/performance-profiler/scripts/profile-parser.py --input <file>
```

If data is inline, save to temp file first. Parse JSON output.

### Profile Step 2: Identify Hotspots

From parsed data:

1. Rank functions by cumulative time (top 10)
2. Identify functions with high call count but low per-call time (overhead candidates)
3. Identify functions with low call count but high per-call time (optimization candidates)
4. Check for I/O-bound vs CPU-bound patterns (wall time vs CPU time ratio)

### Profile Step 3: Recommend

For each hotspot, provide:

- Root cause hypothesis with evidence from the profiler data
- Optimization approach with expected impact range
- Trade-offs and risks of the optimization
- Reference to relevant anti-patterns from `references/anti-patterns.md`

## Mode 3: Cache

Design caching strategies for a described system.

### Cache Step 1: Understand Access Patterns

Ask about or infer from code:

1. Read/write ratio
2. Data freshness requirements (TTL tolerance)
3. Cache size constraints
4. Consistency requirements (eventual vs strong)
5. Eviction pressure (working set vs cache capacity)

### Cache Step 2: Design Strategy

Use `references/caching-strategies.md` decision tree:

| Factor | LRU | LFU | TTL | Write-Through | Write-Back |
|--------|-----|-----|-----|---------------|------------|
| Read-heavy, stable working set | Good | Best | OK | -- | -- |
| Write-heavy | -- | -- | -- | Safe | Fast |
| Strict freshness | -- | -- | Best | Best | Risky |
| Memory-constrained | Best | Good | OK | -- | -- |

### Cache Step 3: Specify

Deliver: eviction policy, write policy, invalidation strategy, warm-up approach, monitoring recommendations. Include capacity planning formula.

## Mode 4: Benchmark

Design benchmarks and review methodology.

### Benchmark Step 1: Generate Skeleton

Run the benchmark designer script:

```
uv run python skills/performance-profiler/scripts/benchmark-designer.py --function <signature> --language <lang>
```

Parse JSON output for setup code, benchmark code, iterations, warmup.

### Benchmark Step 2: Review Methodology

Validate against benchmark best practices:

1. Warmup period sufficient to stabilize JIT/caches
2. Iteration count provides statistical significance
3. Measurement excludes setup/teardown overhead
4. Environment controlled (no interference from other processes)
5. Results include variance/percentiles, not just mean

### Benchmark Step 3: Deliver

Provide complete benchmark code with methodology notes, expected metrics, and interpretation guide.

## Mode 5: Regression

Assess performance regression risk from a code diff.

### Regression Step 1: Collect Diff

If path provided, read the diff. If git range provided, run `git diff`. Identify changed functions and their call sites.

### Regression Step 2: Assess Risk

For each changed function:

| Risk Factor | Weight | Check |
|-------------|--------|-------|
| Complexity increase | 3x | Loop nesting added, algorithm changed |
| Hot path change | 3x | Function called in request/render path |
| Data structure change | 2x | Collection type or size assumptions changed |
| I/O pattern change | 2x | New network/disk calls, removed batching |
| Memory allocation | 1x | New allocations in loops, larger buffers |

Risk score = sum of (weight * severity). Map to LOW/MEDIUM/HIGH/CRITICAL.

### Regression Step 3: Report

Present regression risk matrix with:

- Per-function risk assessment with evidence
- Aggregate risk score for the diff
- Recommended benchmark targets before merging
- Specific measurements to validate (what to profile and where)

## Mode 6: Leak-Patterns

Scan for common memory leak patterns. Static analysis only -- NOT actual leak detection.

### Leak Step 1: Scan

Read target files and check against patterns in `references/leak-patterns.md`:

- Event listener accumulation without cleanup
- Closure-captured references preventing GC
- Growing collections without bounds (unbounded caches, append-only lists)
- Circular references in reference-counted languages
- Resource handles not closed (files, connections, cursors)
- Global state accumulation

### Leak Step 2: Classify

For each potential leak pattern found:

| Pattern | Language | Severity | False Positive Risk |
|---------|----------|----------|-------------------|

### Leak Step 3: Report

Present findings with code citations, explain why each pattern risks leaking, and suggest fixes. Acknowledge that static analysis has high false positive rates -- recommend actual profiling tools for confirmation.

## Scaling Strategy

| Scope | Strategy |
|-------|----------|
| Single function | Direct analysis, inline report |
| Single file (< 500 LOC) | Script-assisted analysis, structured report |
| Multiple files / module | Parallel subagents per file, consolidated report |
| Full codebase | Prioritize entry points and hot paths, sample-based analysis |

## Reference Files

Load ONE reference at a time. Do not preload all references into context.

| File | Content | Read When |
|------|---------|-----------|
| `references/complexity-patterns.md` | Code pattern to Big-O mapping with examples | Mode 1 (Analyze) |
| `references/caching-strategies.md` | Caching decision tree, eviction policies, trade-offs | Mode 3 (Cache) |
| `references/anti-patterns.md` | Performance anti-patterns catalog (N+1, unbounded alloc, etc.) | Mode 2 (Profile), Mode 5 (Regression), Mode 6 (Leak) |
| `references/leak-patterns.md` | Memory leak patterns by language (Python, JS, Go, Java) | Mode 6 (Leak-Patterns) |
| `references/profiler-guide.md` | Profiler output interpretation, flame graph reading | Mode 2 (Profile) |
| `references/benchmark-methodology.md` | Benchmark design best practices, statistical methods | Mode 4 (Benchmark) |

| Script | When to Run |
|--------|-------------|
| `scripts/complexity-estimator.py` | Mode 1 — static complexity analysis via AST |
| `scripts/profile-parser.py` | Mode 2 — parse cProfile/pstats textual output to JSON |
| `scripts/benchmark-designer.py` | Mode 4 — generate benchmark skeleton from function signature |

| Template | When to Render |
|----------|----------------|
| `templates/dashboard.html` | After any mode — inject results JSON into data tag |

## Data Files

| File | Content |
|------|---------|
| `data/complexity-patterns.json` | Code pattern to Big-O mapping (machine-readable) |
| `data/caching-strategies.json` | Caching decision tree (machine-readable) |
| `data/anti-patterns.json` | Performance anti-patterns catalog (machine-readable) |

## Critical Rules

1. Never claim to measure performance — this skill provides analysis, not measurement
2. Every recommendation must include trade-offs — no "just do X" advice
3. Always acknowledge uncertainty in complexity estimates — static analysis has limits
4. Never recommend premature optimization — confirm the code is actually on a hot path first
5. Profiler output interpretation must cite specific data points, not general principles
6. Cache strategy recommendations must address invalidation — "cache invalidation is hard" is not a strategy
7. Benchmark designs must include warmup, statistical significance, and variance reporting
8. Regression risk assessment must trace to specific code changes, not general concerns
9. Leak pattern scanning is pattern-matching only — always recommend actual profiling for confirmation
10. Load ONE reference file at a time — do not preload all references into context
11. Present findings with evidence before suggesting fixes (approval gate)
12. Anti-pattern findings require code citation `[file:line]` — no generic warnings
