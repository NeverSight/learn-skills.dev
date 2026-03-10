---
name: parallel-planner
description: Analyze multi-step tasks to identify which steps can run in parallel, build dependency graphs, detect conflicts (write-write, read-write, resource contention), and produce optimized execution plans. Triggers on 3+ independent steps, "speed up", "run simultaneously", "parallelize", "optimize" or any task where sequential execution wastes time.
---

# Parallel Planner Protocol

Analyze task steps — which ones must wait for each other, which ones can run simultaneously? Build a dependency graph, form parallel groups, and prevent conflicts.

**Core principle:** Sequential is safe but slow. Parallel is fast but requires care. Making the right distinction is this skill's job.

---

## Parallelization Criteria

A step can run in parallel only if **all** conditions are met:
- Not dependent on another step's output
- Does not write to a resource another step reads (no write conflict)
- Does not modify shared state (global variable, same file)
- If it fails, it does not block other parallel steps

A step must run sequentially if **any** of these apply:
- Its input is another step's output
- It writes to the same file / DB table / API resource
- Order matters for correctness (e.g., schema before data)
- Must be atomic (inside a transaction)

---

## Parallelizable Work Types

| Type | Parallel When | Sequential When |
|------|--------------|-----------------|
| Web search | Different topics/sources | Result of search A needed for search B |
| Code generation | Writing to different files | File B imports from file A |
| API calls | Reading from same or different resources | Auth token needed first |
| Data processing | Different data slices | Normalization before analysis |
| Independent subtasks | No shared output/resource | Test depends on module |

---

## Conflict Detection

After identifying parallel candidates, check for conflicts:

### Write-Write Conflict
Two steps write to the same resource → cannot be parallel.
Solution: Run sequentially OR write to separate files, then merge.

### Read-Write Conflict
One step reads while another writes to the same resource → cannot be parallel.
Solution: Read first, then write (sequential).

### Resource Contention
Shared rate limits or connection pools → limit parallel count.
Solution: Cap at 3 parallel, run in batches.

---

## Output Format

```
PARALLEL PLANNER
Total steps: N | Parallel groups: N | Sequential steps: N
Estimated speedup: ~X% faster

## Dependency Graph
[mermaid or text visualization]

## Execution Plan

### Group 1 — Parallel (N steps)
- [ ] #A: [step]
- [ ] #B: [step]
- [ ] #C: [step]
-> All complete, then proceed to Group 2

### Group 2 — Sequential
- [ ] #D: [step]  (requires: #A, #B)
- [ ] #E: [step]  (requires: #D)

## Conflict Warnings
[If any — blocked parallel candidates and reason]

## Steps Kept Sequential
| Step | Reason | Depends On |
|------|--------|------------|
| #D | Uses #A output | #A |
```

---

## Speed Estimate

```
Sequential total = Sum(all step durations)
Parallel total   = Sum(longest step per group)
Speedup          = (Sequential - Parallel) / Sequential * 100
```

Complexity-based estimates when duration is unknown:
- Simple (file read, short code): ~1 unit
- Medium (API call, analysis): ~3 units
- Heavy (web research, large code): ~5 units

---

## When to Skip

- 2 or fewer steps — parallelization is meaningless
- All steps are sequentially dependent
- User said "do it step by step"
- Transaction-bound operations (must be atomic)

---

## Guardrails

- **Never parallelize write operations to the same resource** — even if it seems safe.
- **Always show the dependency graph** — the user must see why steps are ordered this way.
- **Cross-skill**: works with `task-decomposer` (provides the step list) and `tool-selector` (optimizes tool usage within groups).
