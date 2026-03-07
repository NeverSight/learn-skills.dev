---
name: performance-profiler
description: Profile and optimize application performance including load times, memory usage, and rendering. Use when debugging slow performance, memory leaks, or optimizing app speed.
---

# Performance Profiler

## Instructions

When profiling performance:

1. **Identify the bottleneck type**: Network, rendering, memory, or compute
2. **Measure baseline** before optimizing
3. **Profile with appropriate tools**
4. **Apply optimizations**
5. **Measure improvement**

## Web Performance

### Core Web Vitals

```bash
# Lighthouse CLI
npx lighthouse https://yoursite.com --view

# With specific metrics
npx lighthouse https://yoursite.com --only-categories=performance
```

**Target Metrics**:
| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |

### Bundle Analysis

```bash
# Next.js
ANALYZE=true npm run build

# Webpack
npx webpack-bundle-analyzer stats.json

# Vite
npx vite-bundle-visualizer
```

## React Performance

### React DevTools Profiler

1. Install React DevTools browser extension
2. Open DevTools → Profiler tab
3. Click Record, interact with app, stop recording
4. Analyze flame graph for slow components

### Common React Optimizations

```tsx
// 1. Memoize expensive components
const MemoizedList = React.memo(function List({ items }) {
  return items.map(item => <Item key={item.id} {...item} />);
});

// 2. Use useMemo for expensive calculations
const sortedItems = useMemo(() => {
  return [...items].sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// 3. Use useCallback for stable function references
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

// 4. Virtualize long lists
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  return (
    <FixedSizeList
      height={400}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </FixedSizeList>
  );
}

// 5. Lazy load components
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

## Node.js Performance

### Profiling

```bash
# CPU profile
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Heap snapshot
node --inspect app.js
# Then use Chrome DevTools Memory tab

# Clinic.js (comprehensive)
npx clinic doctor -- node app.js
npx clinic flame -- node app.js
npx clinic bubbleprof -- node app.js
```

### Memory Leak Detection

```javascript
// Add to app for debugging
const used = process.memoryUsage();
console.log({
  heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)} MB`,
  heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)} MB`,
  external: `${Math.round(used.external / 1024 / 1024)} MB`,
});
```

## Database Performance

```sql
-- PostgreSQL: Analyze slow queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Find missing indexes
SELECT relname, seq_scan, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan;
```

### Query Optimization

```typescript
// Bad: N+1 query
const users = await db.user.findMany();
for (const user of users) {
  const posts = await db.post.findMany({ where: { userId: user.id } });
}

// Good: Single query with include
const users = await db.user.findMany({
  include: { posts: true }
});

// Good: Select only needed fields
const users = await db.user.findMany({
  select: { id: true, name: true, email: true }
});
```

## Quick Wins Checklist

- [ ] Enable gzip/brotli compression
- [ ] Add caching headers
- [ ] Lazy load images (`loading="lazy"`)
- [ ] Preconnect to external domains
- [ ] Use CDN for static assets
- [ ] Minimize JavaScript bundle
- [ ] Defer non-critical JS
- [ ] Optimize images (WebP, proper sizing)
- [ ] Add database indexes
- [ ] Use connection pooling
