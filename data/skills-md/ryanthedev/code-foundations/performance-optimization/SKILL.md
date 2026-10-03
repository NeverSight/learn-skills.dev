---
name: performance-optimization
description: "Applies measure-first performance optimization: profiles to find hot spots, applies algorithm and data-structure improvements before micro-optimizations, and validates each change prevents regression. For single-process code tuning; not for correctness bugs (use cc-debugging) or concurrency, distributed, and real-time tuning (explicitly out of scope)."
user-invocable: false
---

# Skill: performance-optimization

## Measure First — the gate every optimization passes through

Profile before optimizing — intuition about hot spots is measurably wrong more often than right:

- **Correctness before speed** -- make it work, then make it fast
- **<4% of code causes >50% of runtime** (Knuth 1971) -- find the hot spot before touching anything
- **>50% of optimizations produce negligible or negative results** -- measurement prevents wasted effort

Optimization proceeds only from a measurement — unmeasured "optimizations" are edits with a coin-flip chance of helping.

---

## Scope Limitations

This skill covers single-threaded, single-process code tuning for general-purpose computing.

**Not covered (need specialized guidance):**
- **Concurrency:** Lock contention often dominates; profile thread states, not just CPU
- **Distributed systems:** Network latency ~10,000x memory; optimize RPC/serialization first
- **Real-time systems:** Need worst-case latency, not average; caching adds variance
- **Embedded/constrained:** Memory/power budgets require different tradeoffs

---

## The Simplicity-Performance Relationship

Simpler code usually runs faster. Fewer special cases = less code to check; deep modules = more work per call with fewer layer crossings; complicated code does extraneous or redundant work.

---

## Primary Workflow: 7-Step Decision Tree

Each step is a gate — skipping one forfeits the evidence the next step depends on.

```
1. Is the program correct and complete?
   NO  -> Make it correct first. STOP optimization.
   YES -> Continue

2. Have you measured to find the actual bottleneck?
   NO  -> Profile/measure first. Do NOT guess.
   YES -> Continue

3. Can requirements be relaxed?
   YES -> Relax requirements. Done.
   NO  -> Continue

4. Can design/architecture solve it? (Stage 2: Fundamental Fixes)
   YES -> Fix design. Done.
   NO  -> Continue

5. Can algorithm/data structure solve it?
   YES -> Change algorithm. Done.
   NO  -> Continue

6. Can compiler flags help? (40-59% improvement possible)
   YES -> Enable optimizations. Measure.
   NO  -> Continue

7. Is it in the <4% that causes >50% of runtime?
   NO  -> Do NOT optimize this code. Find actual hot spot.
   YES -> PROCEED with code tuning (see below)
```

### Step 2 Detail: Measurement

**What counts as valid measurement:**
- Actual profiling data (timing, call counts, memory usage)
- Multiple runs to account for variance
- Specific hotspot identification, not just "it's slow"

**Identify WHICH dimension:** throughput, latency, memory, or CPU. Different problems need different solutions.

### Step 4 Detail: Fundamental Fixes (APOSD Stage 2)

Before code-level changes, check for architectural fixes:

- **Add a cache?** Eliminate repeated expensive computation
- **Better algorithm?** e.g., balanced tree vs. list, hash map vs. linear search
- **Bypass layers?** e.g., kernel bypass for networking, direct buffer access

If a fundamental fix exists, implement it with standard design techniques. If not, continue down the tree.

### Step 4 Extended: Critical Path Redesign (APOSD Stage 3)

When no fundamental fix is available, redesign the critical path:

1. **Ask:** What is the smallest amount of code for the common case?
2. **Disregard** existing code structure entirely
3. **Ignore** special cases in current code -- consider only data needed for critical path
4. **Define "the ideal"** -- simplest and fastest code assuming complete redesign freedom
5. **Design** the rest of the class around these critical paths

**Consolidation techniques:**

| Technique | Example |
|-----------|---------|
| Encode multiple conditions in single value | Variable that is 0 when any special case applies |
| Single test for multiple cases | Replace 6 individual checks with 1 combined check |
| Combine layers into single method | Critical path handled in one method, not three |
| Merge variables | Combine multiple values into single structure |

---

## Code Tuning Procedure (ordered — each step's evidence feeds the next)

Only reached after completing the 7-step decision tree.

```
1. Save working version (cannot revert without backup)
2. Make ONE change (multiple changes = unmeasurable)
3. Measure improvement (same workload, before/after)
4. Keep if faster, revert if not (no "close enough")
5. Repeat
```

### Technique Priority by Category

**Logic:**
1. Stop testing when answer known (break, short-circuit)
2. Order tests by frequency (most common first)
3. Substitute table lookups for complex logic
4. Use lazy evaluation

**Loops:**
1. Unswitch (move invariant tests outside)
2. Jam/fuse loops operating on same range
3. Put busiest loop on inside
4. Minimize work inside loops
5. Use sentinel values for search loops
6. Unroll ONLY if measured (can be -27% in Python!)

**Data:**
1. Use integers instead of floating-point when possible
2. Use fewest array dimensions
3. Cache frequently computed values
4. Precompute results where practical

**Expressions:**
1. Initialize at compile time
2. Exploit algebraic identities
3. Use strength reduction (multiplication -> addition)
4. Eliminate common subexpressions

---

## After Making Changes

Checklist and code examples: `Read(${CLAUDE_SKILL_DIR}/checklists.md)`

Re-measure before keeping any change. Keep only if: significant speedup (with data), OR simpler AND at least as fast. Otherwise back it out.

---

## Red Flags

| Red Flag | Symptom |
|----------|---------|
| Premature Optimization | Optimizing without measurement |
| Death by Thousand Cuts | Many small inefficiencies, no single fix helps (5-10x slower) |
| Pass-Through Methods | Identical signature to caller, unnecessary layer crossing |
| Shallow Layers | Multiple layers providing same abstraction |
| Repeated Special Cases | Same conditions checked multiple times |
| Trading maintainability for <10% gain | Complex optimization for minor speedup |

---

## Quick Reference

| Threshold/Rule | Value | Source |
|----------------|-------|--------|
| Hot spot concentration | <4% causes >50% runtime | Knuth 1971 |
| Failed optimization rate | >50% negligible or negative | CC p.607 |
| Compiler optimization gains | 40-59% improvement possible | CC p.596 |
| I/O vs memory | ~1000x difference | CC p.591 |

---

## Checker

Checklist: `Read(${CLAUDE_SKILL_DIR}/checklists.md)`

Output Format:
  | Item | Status | Evidence | Location |
  |------|--------|----------|----------|
  | Measured before tuning? | VIOLATION | No profiler/measurement found | N/A |
  | Loop unswitching opportunity | WARNING | Invariant `if (debug)` inside loop | app.py:142 |

Severity: VIOLATION (clear anti-pattern), WARNING (needs measurement), PASS (no issues)

---

## Chain

| After | Next |
|-------|------|
| Optimization complete | Verify design not degraded |
| Structure degraded | cc-refactoring-guidance |
