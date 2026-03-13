---
name: python-profiling
description: >
  Structured workflow for profiling and optimizing Python code — CPU hotspots,
  memory usage, and benchmark-driven validation. Use this skill whenever the user
  asks to make Python code faster, reduce memory usage, profile performance, find
  bottlenecks, optimize hot paths, reduce allocations, or investigate why something
  is slow. Also trigger when the user mentions profiling tools (cProfile, line_profiler,
  py-spy, memray, tracemalloc) or asks to set up benchmarks. Even casual requests
  like "this is slow" or "can we speed this up" should trigger this skill.
license: MIT
---

# Python Profiling & Optimization

A structured, measurement-driven workflow for making Python code faster and leaner.
The core principle: **never optimize without measuring first, and never trust an
optimization without measuring after.**

## Before you start

Read `references/tools-cheatsheet.md` for detailed command syntax for each profiling
tool. It covers installation, usage patterns, and output interpretation.

## Phase 1: Understand the project

Before profiling anything, gather context:

1. **Python version** — Check `pyproject.toml` for `requires-python` and
   `target-version`. This determines which tools and stdlib features are available.
2. **Package manager** — Look for `uv.lock`, `poetry.lock`, `Pipfile.lock`,
   or `requirements.txt` to determine how dependencies are managed.
3. **Existing benchmarks** — Search for `pytest-benchmark`, `benchmark` directories,
   or profiling scripts already in the project.
4. **Test suite** — Understand how tests run so you can validate correctness after
   each optimization.

## Phase 2: Establish a baseline

You cannot improve what you haven't measured. Before any optimization:

### If the project has pytest-benchmark

Save a named baseline snapshot:
```bash
uv run pytest <benchmark_file> -m slow \
    --benchmark-only --benchmark-disable-gc \
    --benchmark-save=baseline
```

### If the project lacks benchmarks

Create a minimal benchmark file targeting the code to optimize. Use `pytest-benchmark`
with `pedantic()` for stable, reproducible results:

```python
@pytest.mark.slow()
class TestPerformance:
    def test_hot_path(self, benchmark):
        # Setup outside the measured region
        obj = create_object()
        benchmark.pedantic(obj.hot_method, rounds=10, iterations=1000)
```

Use `pedantic()` over the simple `benchmark()` call — it gives explicit control over
rounds and iterations, producing more stable measurements with lower variance.

### Quick ad-hoc baseline (no benchmark framework)

For quick exploration before setting up proper benchmarks:
```python
import cProfile
cProfile.run('function_to_profile()', sort='cumulative')
```

## Phase 3: Identify bottlenecks

Use the right tool for the job. Start broad, then narrow down.

### Decision tree

```
Is the problem CPU-bound or memory-bound?

CPU-bound:
  Need a quick overview? .............. cProfile (stdlib, zero install)
  Need per-line granularity? .......... line_profiler (uv pip install)
  Can't modify code / need sampling? .. py-spy (uv pip install)
  Want CPU + memory together? ......... scalene (uv pip install)

Memory-bound:
  Quick stdlib check? ................. tracemalloc (stdlib, zero install)
  Need detailed allocations/flamegraph? memray (uv pip install)
  Want CPU + memory together? ......... scalene (uv pip install)
```

### Tool installation

For tools not in the project's dependencies, install them as standalone tools
that won't pollute the project. Always ask the user before installing:

```bash
# Temporary install (lost if venv is recreated)
uv pip install line-profiler
uv pip install py-spy
uv pip install memray
uv pip install scalene

# Or add as dev dependency (persists across venv recreations)
uv add --group dev line-profiler
```

Recommend `uv pip install` by default — profiling tools are typically used
temporarily during optimization work, not as permanent project dependencies.

### Profiling workflow

1. **Start broad with cProfile** — Identify which functions consume the most time.
   Look at cumulative time (`cumtime`) to find the call trees that matter.

2. **Narrow down with line_profiler** — Once you know which function is hot,
   profile it line-by-line to find the exact bottleneck.

3. **For production or running processes** — Use py-spy to attach to a running
   process without modifying code or restarting.

4. **For memory issues** — Start with tracemalloc snapshots, graduate to memray
   for flamegraphs and detailed allocation tracking.

## Phase 4: Optimize (one change at a time)

Each optimization must be:
- **A single, focused change** — Don't bundle multiple optimizations together.
  If one of them causes a regression, you won't know which.
- **Measured immediately** — Run benchmarks right after the change.
- **Validated for correctness** — Run the full test suite. A faster wrong answer
  is worse than a slow correct one.

### Common Python optimization patterns

Listed roughly by impact and safety (safest first):

1. **Algorithm/data structure** — The highest-impact changes. `O(n)` lookup → `O(1)`
   with a dict/set. Sorting when you only need min/max. Quadratic nested loops.

2. **Reduce allocations** — Reuse objects instead of creating new ones in hot loops.
   Use `__slots__` on frequently instantiated classes. Prefer tuples over lists for
   fixed-size sequences.

3. **Cache repeated work** — `functools.lru_cache` or `functools.cache` (3.9+) for
   pure functions. Manual caching with `dict` for methods. `__hash__` caching for
   objects used as dict keys.

4. **Avoid unnecessary copies** — `str.join()` instead of `+=` in loops.
   Generator expressions instead of list comprehensions when you only iterate once.

5. **Move work out of hot loops** — Attribute lookups (`self.x` → local variable),
   method resolution, import-time computation.

6. **Use stdlib accelerators** — `collections.deque` for queue operations,
   `bisect` for sorted insertion, `itertools` for iterator patterns.

7. **Leverage C extensions** — `re.compile()` for repeated regex, `struct.pack()`
   for binary data, `array.array` for homogeneous numeric data.

### After each optimization

```bash
# Measure
uv run pytest <benchmark_file> -m slow \
    --benchmark-only --benchmark-disable-gc \
    --benchmark-save=<optimization-label> \
    --benchmark-compare=<baseline-number>

# Validate correctness
uv run pytest  # full test suite
```

### Log results

Keep a progress log documenting each optimization:

```markdown
### Optimization N: <title>

| Benchmark | Before | After | Delta |
|-----------|--------|-------|-------|
| ... | ... | ... | ...% |

**Commit:** `<hash>`
**Description:** ...
**Tests pass:** yes/no
```

## Phase 5: Deep investigation

When the broad tools aren't enough, go deeper.

### pytest-benchmark + cProfile integration

Get per-function breakdown within a specific benchmark:
```bash
uv run pytest <benchmark_file>::<TestClass>::<test_name> \
    -m slow --benchmark-only --benchmark-disable-gc \
    --benchmark-cprofile=cumtime --benchmark-cprofile-top=30
```

**IMPORTANT:** By default, `--benchmark-cprofile` profiles a **single iteration**
of the benchmark function, which produces near-zero times for fast code (everything
shows `0.0000`). Use `--benchmark-cprofile-loops=N` to run the profiled code N times,
giving cProfile enough samples to produce meaningful cumulative times:

```bash
uv run pytest <benchmark_file>::<TestClass>::<test_name> \
    -m slow --benchmark-only --benchmark-disable-gc \
    --benchmark-cprofile=cumtime --benchmark-cprofile-top=30 \
    --benchmark-cprofile-loops=1000
```

Choose N so the total profiled time is at least 0.5–1s — this gives enough
resolution to distinguish real hotspots from noise. For very fast functions
(~100µs), use `--benchmark-cprofile-loops=5000` or more.

### Visual profiling

Generate `.prof` files and visualize with snakeviz or speedscope:
```bash
uv run pytest <benchmark_file>::<test_name> \
    -m slow --benchmark-only --benchmark-disable-gc \
    --benchmark-cprofile=cumtime --benchmark-cprofile-loops=1000 \
    --benchmark-cprofile-dump=/tmp/bench

# Interactive flamegraph in browser
uv pip install snakeviz
uv run snakeviz /tmp/bench-<test_name>.prof
```

### Memory flamegraphs with memray

```bash
uv pip install memray
uv run memray run -o /tmp/mem.bin script.py
uv run memray flamegraph /tmp/mem.bin -o /tmp/mem.html
open /tmp/mem.html  # or xdg-open on Linux
```

## Anti-patterns to avoid

- **Premature optimization** — Profile first. The bottleneck is almost never where
  you think it is.
- **Micro-benchmarking in isolation** — A function that's fast in isolation may be
  slow in context due to cache effects, GC pressure, or contention.
- **Optimizing cold paths** — Focus on code that runs frequently. A 10x speedup on
  code that runs once at startup is worth less than a 2x speedup on a hot loop.
- **Breaking the API for speed** — Prefer internal optimizations that don't change
  the public interface.
- **Trusting a single measurement** — Use `pedantic()` with multiple rounds.
  Compare means AND standard deviations. A 5% improvement with 20% stddev is noise.
- **Bundling multiple changes** — One optimization per commit. If you combine three
  changes and get a 15% speedup, you don't know which change helped (or if one
  actually regressed and the others compensated).

## Checklist

Before declaring an optimization complete:

- [ ] Baseline benchmark saved before any changes
- [ ] Each optimization is a separate, focused change
- [ ] Benchmark comparison shows measurable improvement (beyond noise/stddev)
- [ ] Full test suite passes
- [ ] Progress log updated with before/after numbers
- [ ] No public API changes (or changes are documented)
