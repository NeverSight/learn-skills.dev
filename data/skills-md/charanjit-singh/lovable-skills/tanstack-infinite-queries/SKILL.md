---
name: tanstack-infinite-queries
description: >-
  Use when implementing pagination, infinite scroll, or "load more" lists with
  TanStack Query: useInfiniteQuery, cursor-based or offset-based pagination,
  virtualization. Not for single-page lists where one query is enough.
---

# TanStack infinite queries (pagination / infinite scroll)

Use `useInfiniteQuery` for any list that can grow beyond ~50 rows. Pair with **cursor-based** pagination (Supabase `lt(created_at, lastCursor)`) — offset pagination breaks when rows are inserted.

Companion skills: [`tanstack-query-alternative`](../tanstack-query-alternative/), [`postgres-full-text-search`](../postgres-full-text-search/), [`error-states-and-empty-ui`](../error-states-and-empty-ui/).

## Cursor-based fetcher (Supabase)

```ts
// src/api/posts.ts
const PAGE_SIZE = 20;

export async function fetchPostsPage({
  orgId,
  cursor,
}: { orgId: string; cursor?: string }) {
  let q = supabase
    .from("posts")
    .select("*")
    .eq("organization_id", orgId)
    .is("deleted_at", null)
    .order("created_at", { ascending: false })
    .order("id", { ascending: false })  // tiebreaker, stable order
    .limit(PAGE_SIZE);

  if (cursor) q = q.lt("created_at", cursor);

  const { data, error } = await q;
  if (error) throw error;

  const nextCursor = data.length === PAGE_SIZE ? data[data.length - 1].created_at : undefined;
  return { rows: data, nextCursor };
}
```

`order("id")` as a tiebreaker prevents skipped rows when multiple records share a `created_at`.

## Hook

```ts
// src/hooks/queries/usePosts.ts
import { useInfiniteQuery } from "@tanstack/react-query";

export function usePosts(orgId: string) {
  return useInfiniteQuery({
    queryKey: postKeys.list({ orgId }),
    queryFn: ({ pageParam }) => fetchPostsPage({ orgId, cursor: pageParam }),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (last) => last.nextCursor,
    staleTime: 30_000,
  });
}
```

Flatten in the component:

```tsx
const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = usePosts(orgId);
const posts = data?.pages.flatMap((p) => p.rows) ?? [];
```

## Trigger next page

### Intersection observer (recommended)

```tsx
const ref = useIntersectionObserver(() => {
  if (hasNextPage && !isFetchingNextPage) fetchNextPage();
});

return (
  <>
    {posts.map((p) => <PostCard key={p.id} post={p} />)}
    <div ref={ref} />
    {isFetchingNextPage && <Skeleton />}
  </>
);
```

### Button fallback

A "Load more" button is more accessible than infinite scroll for long lists. Combine: button + observer triggers below it.

## Virtualization (large lists)

For ≥ 200 rendered rows, add **`@tanstack/react-virtual`** so the DOM only holds visible items:

```ts
const rowVirtualizer = useVirtualizer({
  count: posts.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 88,
  overscan: 8,
});
```

Required for chat, activity feeds, and ledger views — without it, scroll jank kills UX.

## Inserts and deletes — cache updates

```ts
// after creating a post, prepend to the first page
qc.setQueryData<InfiniteData<typeof first>>(postKeys.list({ orgId }), (old) => {
  if (!old) return old;
  const [first, ...rest] = old.pages;
  return { ...old, pages: [{ ...first, rows: [newPost, ...first.rows] }, ...rest] };
});
```

For deletes, filter rows across all pages.

After complex changes, invalidate to reconcile with the server:

```ts
qc.invalidateQueries({ queryKey: postKeys.list({ orgId }) });
```

## Avoid

- Offset pagination (`range(0, 19)` / `range(20, 39)`) on tables with frequent inserts — rows shift.
- Missing tiebreaker `order` — duplicate or missing rows at page boundaries.
- Rendering 1000 rows without virtualization.
- Loading the next page on a 1 px scroll trigger (causes thrash) — use observer with margin.
- Re-fetching every page on a single delete; surgical cache update instead.

## Checklist

- [ ] Cursor-based query with stable tiebreaker.
- [ ] `hasNextPage` + `isFetchingNextPage` UX.
- [ ] Virtualization on long lists.
- [ ] Surgical `setQueryData` on insert/delete; invalidate to reconcile.
- [ ] Empty / error states (`error-states-and-empty-ui`).
