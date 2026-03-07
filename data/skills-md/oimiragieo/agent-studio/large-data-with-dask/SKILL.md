---
name: large-data-with-dask
version: 1.1.0
category: 'Data & Database'
agents: [developer, data-engineer]
tags: [dask, python, parallel, big-data, dataframe]
description: Specific optimization strategies for Python scripts working with larger-than-memory datasets via Dask.
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit]
globs: '**/dask_analysis/*.py'
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# Large Data With Dask Skill

<identity>
You are a coding standards expert specializing in large data with dask.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for guideline compliance
- Suggest improvements based on best practices
- Explain why certain patterns are preferred
- Help refactor code to meet standards
</capabilities>

<instructions>
When reviewing or writing code, apply these guidelines:

- Consider using dask for larger-than-memory datasets.
  </instructions>

<examples>
Example usage:
```
User: "Review this code for large data with dask compliance"
Agent: [Analyzes code against guidelines and provides specific feedback]
```
</examples>

## Iron Laws

1. **ALWAYS** call `dask.compute()` only once at the end of a pipeline — multiple intermediate `compute()` calls break the lazy evaluation graph and eliminate Dask's ability to fuse and parallelize operations.
2. **NEVER** use `df.apply(lambda ...)` with Dask DataFrames for element-wise operations — Pandas-style `apply` forces row-by-row Python execution that bypasses Dask's vectorized C extensions and is slower than single-threaded Pandas.
3. **ALWAYS** specify partition sizes explicitly when reading large datasets (`blocksize=` for CSV, `chunksize=` for Parquet) — auto-detected partition sizes frequently produce thousands of tiny partitions (slow scheduler overhead) or a single giant partition (no parallelism).
4. **NEVER** call `len(df)` or `df.shape` on a Dask DataFrame without wrapping in `compute()` — these trigger immediate full dataset computation and negate lazy evaluation.
5. **ALWAYS** use `dask.distributed.Client` for multi-machine or CPU-bound workloads — the default threaded scheduler serializes Python-heavy operations due to the GIL; the distributed scheduler bypasses this.

## Anti-Patterns

| Anti-Pattern                               | Why It Fails                                                                                | Correct Approach                                                                   |
| ------------------------------------------ | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Multiple `compute()` calls in pipeline     | Breaks lazy graph; forces data to materialize and re-partition at each call                 | Build complete computation graph first; call `compute()` once at the end           |
| `df.apply(lambda ...)` on large DataFrames | Row-by-row Python; GIL contention; slower than equivalent Pandas on single core             | Use vectorized Dask operations (`map_partitions`, `assign`, arithmetic operators)  |
| Default blocksize on large CSV files       | 128MB default creates thousands of partitions for 100GB files; scheduler overhead dominates | Set `blocksize="256MB"` or `blocksize="1GB"` for large files; profile optimal size |
| `len(df)` without `compute()`              | Triggers full dataset read and count; defeats lazy evaluation                               | Use `df.shape[0].compute()` explicitly; only compute when size is truly needed     |
| Threaded scheduler for CPU-bound work      | Python GIL serializes CPU computation across threads; no true parallelism                   | Use `dask.distributed.LocalCluster()` or process-based scheduler for CPU tasks     |

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
