---
name: performance-optimization
description: Optimizes application performance. Use when performance requirements exist, when you suspect performance regressions, or when Core Web Vitals or load times need improvement. Use when profiling reveals bottlenecks that need fixing.
---

# Performance Optimization

## Overview

Measure before optimizing. Performance work without measurement is guessing — and guessing leads to premature optimization that adds complexity without improving what matters. Profile first, identify the actual bottleneck, fix it, measure again.

## When to Use

- Performance requirements exist in the spec (load time budgets, response time SLAs)
- Users or monitoring report slow behavior
- Core Web Vitals scores are below thresholds
- You suspect a change introduced a regression
- Building features that handle large datasets or high traffic

**When NOT to use:** Don't optimize before you have evidence of a problem.

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

## The Optimization Workflow

```
1. MEASURE  → Establish baseline with real data
2. IDENTIFY → Find the actual bottleneck (not assumed)
3. FIX      → Address the specific bottleneck
4. VERIFY   → Measure again, confirm improvement
5. GUARD    → Add monitoring or tests to prevent regression
```

### Where to Start

```
What is slow?
├── First page load
│   ├── Large bundle? → Measure bundle size, check code splitting
│   ├── Slow server response? → Measure TTFB in Network waterfall
│   └── Render-blocking resources? → Check CSS/JS blocking in waterfall
├── Interaction feels sluggish
│   ├── UI freezes on click? → Profile main thread, look for long tasks (>50ms)
│   ├── Form input lag? → Check re-renders, controlled component overhead
│   └── Animation jank? → Check layout thrashing, forced reflows
├── Page after navigation
│   ├── Data loading? → Measure API response times, check for waterfalls
│   └── Client rendering? → Profile component render time
└── Backend / API
    ├── Single endpoint slow? → Profile DaaS queries, check indexes (on an Engine project, index a field by creating it with `schema.add_index: true` through `POST /api/fields/:collection`)
    ├── All endpoints slow? → Check connection pool, memory, CPU
    └── Intermittent slowness? → Check for lock contention, GC pauses
```

## Fix Common Anti-Patterns

### N+1 Queries (DaaS)

```typescript
// BAD: Separate fetch per related item
for (const task of tasks) {
  task.owner = await fetch(`/api/users/${task.ownerId}`);
}

// GOOD: Use DaaS deep query with fields parameter
const tasks = await fetch('/api/items/tasks?fields=*,owner.*');
```

On an Engine project the `fields` parameter expands the relation as shown; the Engine ignores the `deep` parameter.

### Unnecessary Re-renders (React)

```tsx
// BAD: Creates new object on every render
function TaskList() {
  return <TaskFilters options={{ sortBy: 'date', order: 'desc' }} />;
}

// GOOD: Stable reference
const DEFAULT_OPTIONS = { sortBy: 'date', order: 'desc' } as const;
function TaskList() {
  return <TaskFilters options={DEFAULT_OPTIONS} />;
}
```

### Large Bundle Size (Next.js)

```typescript
// GOOD: Dynamic import for heavy features
const ChartLibrary = lazy(() => import('./ChartLibrary'));

// GOOD: Route-level code splitting (Next.js does this automatically)
// Each page in app/ is automatically code-split
```

### Unbounded Data Fetching

```typescript
// BAD: Fetching all records
const all = await fetch('/api/items/tasks');

// GOOD: Paginated with DaaS
const page = await fetch('/api/items/tasks?limit=20&offset=0&sort=-date_created');
```

On an Engine project `limit` is capped at 1000: a request for more returns at most 1000 items, so page through larger sets.

## Performance Budget

```
JavaScript bundle: < 200KB gzipped (initial load)
CSS: < 50KB gzipped
Images: < 200KB per image (above the fold)
API response time: < 200ms (p95)
Lighthouse Performance score: ≥ 90
```

## Next.js / DaaS Specific Tips

- Use Server Components by default (reduces client JS)
- Use `'use client'` only when needed (event handlers, hooks, browser APIs)
- Use `next/image` for automatic image optimization
- Use `next/font` for font optimization
- Leverage DaaS aggregate API for counts/sums instead of fetching all records
- Use DaaS `fields` parameter to fetch only needed fields
- Use DaaS `filter` parameter server-side instead of client-side filtering
- On an Engine project the Engine serves the same `aggregate`, `fields` and `filter` parameters, and caps `limit` at 1000

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We'll optimize later" | Performance debt compounds. Fix obvious anti-patterns now. |
| "It's fast on my machine" | Your machine isn't the user's. Profile on representative hardware. |
| "This optimization is obvious" | If you didn't measure, you don't know. Profile first. |
| "Users won't notice 100ms" | Research shows 100ms delays impact conversion rates. |
| "The framework handles performance" | Frameworks can't fix N+1 queries or oversized bundles. |

## Red Flags

- Optimization without profiling data to justify it
- N+1 query patterns in data fetching
- List endpoints without pagination
- Images without dimensions, lazy loading, or responsive sizes
- Bundle size growing without review
- No performance monitoring in production
- `React.memo` and `useMemo` everywhere (overusing is as bad as underusing)

## Verification

After any performance-related change:

- [ ] Before and after measurements exist (specific numbers)
- [ ] The specific bottleneck is identified and addressed
- [ ] Core Web Vitals are within "Good" thresholds
- [ ] Bundle size hasn't increased significantly
- [ ] No N+1 queries in new data fetching code
- [ ] Existing tests still pass (optimization didn't break behavior)

## See Also

For detailed checklists, see `references/performance-checklist.md`.
