---
name: optimizing-performance
description: Measure-first performance optimization that balances gains against complexity. Use when addressing slow code, profiling issues, or evaluating optimization trade-offs.
argument-hint: "[file-path-or-area]"
---

# Optimizing Performance

**Core principle:** Readable code that's "fast enough" beats complex code that's "optimal". Measure first.

**Focus area:** If `$ARGUMENTS` is provided, use it as the optimization target. Otherwise, run `git diff` and focus on unstaged changes. If no unstaged changes exist, ask the user what to optimize.

## The Golden Rule

```
IF optimization reduces complexity AND improves performance → ALWAYS DO IT
IF optimization increases complexity → Only if 10x faster OR fixes critical UX (>16ms UI, >100ms input)
```

## Four-Phase Process

```
- [ ] Phase 1: Measure baseline (time/renders/memory/KB)
- [ ] Phase 2: Identify root cause (algorithm/I/O/payload)
- [ ] Phase 3: Evaluate cost vs benefit
- [ ] Phase 4: Implement & verify improvement
```

### Phase 1: Measure First (REQUIRED)

**Never optimize without data.**

| Metric | What to Count | Tools |
|--------|--------------|-------|
| Time | ms per operation | `performance.now()`, profilers |
| Re-renders | Component render count | React DevTools Profiler |
| Memory | MB allocated | DevTools Memory tab |
| Network | Request count, KB | Network tab, bundle analyzer |
| Database | Query count, rows scanned | EXPLAIN plans |

### Phase 2: Identify Root Cause

| Issue | Indicators | Fix Direction |
|-------|------------|---------------|
| O(n²) complexity | Nested loops, `.includes()` in loop | Use Set/Map |
| Unnecessary work | Re-computing same result | Cache/memoize |
| I/O bottleneck | N+1 queries, sequential APIs | Batch, use joins |
| Large datasets | Rendering 1000+ items | Virtualization |
| Payload size | >500KB bundles | Tree-shake, lazy load |

### Phase 3: Evaluate Cost vs Benefit

1. Reduces complexity? → Always do it
2. Increases complexity? → Only if 10x faster OR fixes critical UX
3. Otherwise → Don't do it

### Phase 4: Implement & Verify

1. Make minimal changes targeting bottleneck
2. Re-run benchmark
3. Verify tests pass

## Win-Win Optimizations (Always Do)

**Multiple loops → Single loop:**
```javascript
// ❌ Three passes
const ids = users.map(u => u.id);
const active = users.filter(u => u.active);

// ✅ One pass
const { ids, active } = users.reduce((acc, u) => {
  acc.ids.push(u.id);
  if (u.active) acc.active.push(u);
  return acc;
}, { ids: [], active: [] });
```

**Nested loops → Hash map (O(n²) → O(n)):**
```javascript
// ❌ O(n²)
const matched = orders.filter(o => users.some(u => u.id === o.userId));

// ✅ O(n)
const userIds = new Set(users.map(u => u.id));
const matched = orders.filter(o => userIds.has(o.userId));
```

## High-Value Optimizations

| Pattern | When | Fix |
|---------|------|-----|
| Virtualization | Lists >1000 items | react-window, tanstack-virtual |
| Memoization | >5ms calc OR unnecessary re-renders | `useMemo`, `React.memo` |
| Batching | Multiple state updates | Single setState, bulk INSERT |
| Lazy loading | Large dependencies | `import('./heavy-lib')` |

## Red Flags

- Optimizing without benchmark data
- Micro-optimizing <16ms code
- Adding complexity for minimal gain
- Optimizing infrequently-run code
