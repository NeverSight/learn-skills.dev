---
name: react-router-loader-performance
description: React Router v7 loader performance optimization techniques. Use when optimizing TTFB, eliminating waterfalls, consolidating database queries, or streaming secondary data in loaders. Triggers on "slow loaders", "optimize TTFB", "speed up React Router", "loader performance", or when loaders exceed 500ms response time.
---

# React Router Loader Performance

Critical optimization techniques for React Router v7 loaders. Contains 4 rules focused on eliminating waterfalls and maximizing parallel execution.

**Impact: CRITICAL** - Poor loader performance directly impacts Time To First Byte (TTFB) and perceived page speed.

## When to Apply

Use these techniques when:

- Loader TTFB exceeds 500ms
- Multiple database queries execute sequentially
- Secondary data (recommendations, analytics) blocks critical path
- Database latency is high (>50ms per query)
- Optimizing React Router v7 data loading patterns

## Rules Summary

### Database Optimization (CRITICAL)

#### loader-consolidate-queries - @rules/loader-consolidate-queries.md

Use ORM includes/relations for single-query data fetching.

```tsx
// Bad: 3 DB calls (~450ms on 150ms latency)
const product = await db.product.findUnique({ where: { id } });
const reviews = await db.review.findMany({ where: { productId: id } });
const variations = await db.variation.findMany({ where: { productId: id } });

// Good: 1 DB call (~200ms)
const product = await db.product.findUnique({
  where: { id },
  include: { reviews: true, variations: true },
});
```

**Impact:** Often the single biggest loader performance win, especially on high-latency DB connections.

### Streaming Optimization (HIGH)

#### loader-defer-slow-secondary - @rules/loader-defer-slow-secondary.md

Stream non-critical data without awaiting.

```tsx
// Bad: blocks on slow operation (~3500ms TTFB)
const product = await getProduct(id); // 500ms
const recommendations = await getRecommendations(product); // 3000ms
return data({ product, recommendations }); // TTFB: 3500ms

// Good: streams secondary data (~500ms TTFB)
const product = await getProduct(id); // 500ms
const recommendations = getRecommendations(product); // Don't await
return data({ product, recommendations }); // TTFB: 500ms
```

**Impact:** Keeps slow operations off critical path. Recommendations stream while user views product.

### Infrastructure Optimization (HIGH)

#### infrastructure-colocation

Minimize geographic distance between servers and databases.

**Key metrics:**
- Same region: <10ms latency
- Cross-region: 50-200ms latency
- Cross-continent: >100ms latency

**Actions:**
1. Host DB and servers in same cloud region
2. Use read replicas near application servers for read-heavy routes
3. Analyze ORM query logs for consistent >30ms latency
4. When DB latency is high, infrastructure changes provide greater gains than code optimization

### Parallel Execution (CRITICAL)

#### promise-all-independent

Use Promise.all for independent async operations (covered in frontend-async-best-practices).

```tsx
// Bad: sequential (~900ms)
const product = await fetchProduct(); // 400ms
const reviews = await fetchReviews(); // 300ms
const variations = await fetchVariations(); // 200ms

// Good: parallel (~400ms)
const [product, reviews, variations] = await Promise.all([
  fetchProduct(),
  fetchReviews(),
  fetchVariations(),
]);
```

**Impact:** Total time equals slowest operation, not sum of all operations.

## Performance Targets

- **TTFB**: <500ms for critical path
- **DB latency**: <30ms per query (measure with ORM logs)
- **Secondary data**: Stream anything >1000ms that's non-critical

## Measurement

Use Server-Timing headers to identify bottlenecks:

```tsx
import { time } from "~/utils/timing.server";

export async function loader({ params }: Route.LoaderArgs) {
  const product = await time("product", () => getProduct(params.id));
  const recommendations = time("recommendations", () =>
    getRecommendations(product)
  );
  return data({ product, recommendations });
}
```

Analyze Chrome DevTools Network tab for Server-Timing breakdown.
