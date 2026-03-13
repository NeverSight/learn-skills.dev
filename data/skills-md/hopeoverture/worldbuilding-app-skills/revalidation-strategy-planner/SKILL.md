---
name: revalidation-strategy-planner
description: Evaluates Next.js routes and outputs optimal revalidate settings, cache tags for ISR, SSR configurations, or streaming patterns. This skill should be used when optimizing Next.js caching strategies, configuring Incremental Static Regeneration, planning cache invalidation, or choosing between SSR/ISR/SSG. Use for Next.js caching, revalidation, ISR, cache tags, on-demand revalidation, or rendering strategies.
---

# Revalidation Strategy Planner

Analyze Next.js application routes and recommend optimal caching and revalidation strategies for performance and data freshness.

## Overview

To optimize Next.js caching strategies:

1. Analyze route characteristics (data freshness requirements, update frequency)
2. Determine appropriate rendering strategy (SSG, ISR, SSR, streaming)
3. Configure revalidation intervals for ISR routes
4. Implement cache tags for on-demand revalidation
5. Set up streaming for progressive page loading

## Rendering Strategies

### Static Site Generation (SSG)

To use SSG for rarely changing content:

```typescript
// app/about/page.tsx
export default async function AboutPage() {
  // Generated at build time, no revalidation
  return <div>About Us</div>;
}
```

**Best for:**
- Marketing pages
- Documentation
- Static content that rarely changes

### Incremental Static Regeneration (ISR)

To use ISR for periodically updated content:

```typescript
// app/entities/[id]/page.tsx
export const revalidate = 3600; // Revalidate every hour

export default async function EntityPage({ params }: { params: { id: string } }) {
  const entity = await fetchEntity(params.id);
  return <EntityDetail entity={entity} />;
}
```

**Best for:**
- Entity detail pages
- Blog posts
- Product listings
- Content with predictable update patterns

### Server-Side Rendering (SSR)

To use SSR for real-time data:

```typescript
// app/dashboard/page.tsx
export const dynamic = 'force-dynamic';

export default async function Dashboard() {
  const data = await fetchUserData();
  return <DashboardView data={data} />;
}
```

**Best for:**
- User dashboards
- Personalized content
- Real-time data displays
- Authentication-dependent pages

### Streaming

To use streaming for progressive loading:

```typescript
// app/timeline/page.tsx
import { Suspense } from 'react';

export default function TimelinePage() {
  return (
    <div>
      <TimelineHeader />
      <Suspense fallback={<TimelineLoader />}>
        <TimelineEvents />
      </Suspense>
    </div>
  );
}
```

**Best for:**
- Pages with slow data fetching
- Complex pages with multiple data sources
- Improving perceived performance

Consult `references/rendering-strategies.md` for detailed strategy comparison.

## Revalidation Configuration

### Time-Based Revalidation

To set revalidation intervals:

```typescript
// Revalidate every 60 seconds
export const revalidate = 60;

// Revalidate every hour
export const revalidate = 3600;

// Revalidate every day
export const revalidate = 86400;
```

### On-Demand Revalidation

To implement on-demand cache invalidation:

```typescript
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  const { path, tag } = await request.json();

  if (path) {
    revalidatePath(path);
  }

  if (tag) {
    revalidateTag(tag);
  }

  return Response.json({ revalidated: true, now: Date.now() });
}
```

Use from Server Actions:

```typescript
'use server';

import { revalidatePath } from 'next/cache';

export async function updateEntity(id: string, data: EntityData) {
  await saveEntity(id, data);
  revalidatePath(`/entities/${id}`);
  revalidatePath('/entities');
}
```

### Cache Tags

To implement cache tag-based revalidation:

```typescript
// app/entities/[id]/page.tsx
export default async function EntityPage({ params }: { params: { id: string } }) {
  const entity = await fetch(`/api/entities/${params.id}`, {
    next: {
      tags: [`entity-${params.id}`, 'entities'],
    },
  });

  return <EntityDetail entity={entity} />;
}
```

Revalidate by tag:

```typescript
import { revalidateTag } from 'next/cache';

// Revalidate all pages with 'entities' tag
revalidateTag('entities');

// Revalidate specific entity
revalidateTag(`entity-${entityId}`);
```

Reference `assets/cache-tag-patterns.ts` for cache tagging patterns.

## Route Analysis

Use `scripts/analyze_routes.py` to analyze application routes and recommend strategies:

```bash
python scripts/analyze_routes.py ./app
```

Output includes:

- Route path
- Recommended rendering strategy
- Suggested revalidation interval
- Appropriate cache tags
- Reasoning for recommendations

### Analysis Criteria

Consider these factors:

1. **Data Freshness Requirements**
   - Real-time: SSR or very short revalidation (1-60s)
   - Near real-time: ISR with short interval (60-300s)
   - Periodic updates: ISR with medium interval (300-3600s)
   - Rarely changes: SSG or long interval (3600s+)

2. **Update Frequency**
   - Continuous: SSR
   - Multiple times per hour: ISR (60-300s)
   - Hourly: ISR (3600s)
   - Daily: ISR (86400s)
   - Weekly+: SSG

3. **Personalization**
   - User-specific: SSR
   - Role-based: SSR or ISR with user context
   - Public: SSG or ISR

4. **Data Source Performance**
   - Fast (<100ms): Any strategy
   - Medium (100-500ms): Consider streaming
   - Slow (>500ms): Use streaming or aggressive caching

Consult `references/decision-matrix.md` for the complete decision matrix.

## Implementation Patterns

### Entity Detail Pages

To optimize entity pages:

```typescript
// app/entities/[id]/page.tsx
export const revalidate = 1800; // 30 minutes

export async function generateStaticParams() {
  const entities = await fetchAllEntityIds();
  return entities.map((id) => ({ id: id.toString() }));
}

export default async function EntityPage({ params }: { params: { id: string } }) {
  const entity = await fetchEntity(params.id, {
    next: { tags: [`entity-${params.id}`, 'entities'] },
  });

  return <EntityDetail entity={entity} />;
}
```

### List Pages

To optimize listing pages:

```typescript
// app/entities/page.tsx
export const revalidate = 300; // 5 minutes

export default async function EntitiesPage({
  searchParams,
}: {
  searchParams: { page?: string };
}) {
  const page = parseInt(searchParams.page || '1');
  const entities = await fetchEntities(page, {
    next: { tags: ['entities'] },
  });

  return <EntityList entities={entities} />;
}
```

### Timeline Pages

To optimize timeline with streaming:

```typescript
// app/timeline/page.tsx
import { Suspense } from 'react';

export default function TimelinePage() {
  return (
    <div>
      <Suspense fallback={<TimelineHeaderSkeleton />}>
        <TimelineHeader />
      </Suspense>
      <Suspense fallback={<EventsSkeleton />}>
        <TimelineEvents />
      </Suspense>
    </div>
  );
}

async function TimelineEvents() {
  const events = await fetchTimelineEvents({
    next: { tags: ['timeline'], revalidate: 600 },
  });
  return <EventsList events={events} />;
}
```

### Dashboard Pages

To implement personalized dashboard:

```typescript
// app/dashboard/page.tsx
export const dynamic = 'force-dynamic';

export default async function DashboardPage() {
  const session = await getSession();
  const data = await fetchUserDashboard(session.userId);

  return (
    <div>
      <Suspense fallback={<StatsSkeleton />}>
        <DashboardStats userId={session.userId} />
      </Suspense>
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity userId={session.userId} />
      </Suspense>
    </div>
  );
}
```

## Cache Invalidation Strategies

### Granular Invalidation

To invalidate specific resources:

```typescript
// After entity update
revalidateTag(`entity-${entityId}`);

// After relationship change
revalidateTag(`entity-${sourceId}`);
revalidateTag(`entity-${targetId}`);
revalidateTag('relationships');
```

### Cascade Invalidation

To invalidate related resources:

```typescript
async function updateEntity(id: string, data: EntityData) {
  await saveEntity(id, data);

  // Invalidate entity page
  revalidateTag(`entity-${id}`);

  // Invalidate list pages
  revalidateTag('entities');

  // Invalidate related pages
  const relationships = await getEntityRelationships(id);
  for (const rel of relationships) {
    revalidateTag(`entity-${rel.targetId}`);
  }
}
```

### Batch Invalidation

To invalidate multiple resources efficiently:

```typescript
async function bulkUpdateEntities(updates: EntityUpdate[]) {
  await saveBulkUpdates(updates);

  // Collect unique tags
  const tags = new Set<string>(['entities']);
  for (const update of updates) {
    tags.add(`entity-${update.id}`);
  }

  // Revalidate all at once
  for (const tag of tags) {
    revalidateTag(tag);
  }
}
```

## Performance Optimization

### Stale-While-Revalidate

To implement SWR pattern:

```typescript
export const revalidate = 60; // Revalidate every minute
export const dynamic = 'force-static'; // Serve stale while revalidating
```

### Parallel Data Fetching

To fetch data in parallel:

```typescript
export default async function EntityPage({ params }: { params: { id: string } }) {
  const [entity, relationships, timeline] = await Promise.all([
    fetchEntity(params.id),
    fetchRelationships(params.id),
    fetchTimeline(params.id),
  ]);

  return <EntityDetailView entity={entity} relationships={relationships} timeline={timeline} />;
}
```

### Selective Streaming

To stream only slow components:

```typescript
export default function EntityPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <EntityHeader id={params.id} /> {/* Fast, no streaming */}
      <Suspense fallback={<RelationshipsSkeleton />}>
        <EntityRelationships id={params.id} /> {/* Slow, stream it */}
      </Suspense>
    </div>
  );
}
```

## Monitoring and Testing

To monitor cache performance:

1. **Cache Hit Rates**: Track ISR cache hits vs. regenerations
2. **Revalidation Frequency**: Monitor how often pages regenerate
3. **Response Times**: Measure time to first byte (TTFB)
4. **Stale Serving**: Track stale-while-revalidate occurrences

Use Next.js analytics or custom logging:

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const start = Date.now();

  return NextResponse.next({
    headers: {
      'x-response-time': `${Date.now() - start}ms`,
    },
  });
}
```

## Best Practices

1. **Start Conservative**: Begin with shorter revalidation intervals, increase gradually
2. **Use Cache Tags**: Prefer tag-based invalidation over path-based
3. **Monitor Performance**: Track cache hit rates and response times
4. **Plan Invalidation**: Design invalidation strategy with data mutations
5. **Test Edge Cases**: Verify behavior with stale data and revalidation
6. **Document Decisions**: Record why specific intervals were chosen
7. **Consider Users**: Balance freshness with performance

## Troubleshooting

Common issues:

- **Stale Data Persisting**: Check cache tag implementation and invalidation logic
- **Excessive Regeneration**: Increase revalidation interval or fix trigger-happy invalidation
- **Slow Page Loads**: Add streaming for slow components
- **Cache Not Working**: Verify fetch options and dynamic/static configuration
- **Development vs Production**: Remember ISR only works in production builds
