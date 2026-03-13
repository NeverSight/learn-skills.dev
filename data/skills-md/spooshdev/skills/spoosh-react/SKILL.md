---
name: spoosh-react
description: Use this skill when the user asks about "Spoosh", "useRead", "useWrite", "usePages", "useQueue", "useSSE", "createClient", "Spoosh React", "Spoosh hooks", "Spoosh plugins", "cache plugin", "retry plugin", "polling plugin", "optimistic updates", "invalidation", "devtool", "Next.js SSR", "initialData", "HonoToSpoosh", "ElysiaToSpoosh", "OpenAPI", "data fetching component", "mutation component", "infinite scroll", "Spoosh patterns", or needs to build React components with type-safe API calls. Provides comprehensive API knowledge and component patterns for @spoosh/react.
---

# Spoosh React

Spoosh is a type-safe API toolkit with a composable plugin architecture for TypeScript. This skill covers the React integration including hooks API, plugins, and component patterns.

## Setup

```bash
pnpm add @spoosh/core @spoosh/react
```

```typescript
import { Spoosh } from "@spoosh/core";
import { create } from "@spoosh/react";

type ApiSchema = {
  "users": {
    GET: { data: User[] };
    POST: { data: User; body: CreateUserBody };
  };
  "users/:id": {
    GET: { data: User };
    DELETE: { data: void };
  };
};

const spoosh = new Spoosh<ApiSchema, Error>("/api")
  .use([cachePlugin(), retryPlugin()]);

export const { useRead, useWrite, usePages, useQueue, useSSE } = create(spoosh);
```

## createClient (Lightweight)

For simple use cases without hooks or plugins:

```typescript
import { createClient } from "@spoosh/core";

const api = createClient<ApiSchema, Error>("/api");

const { data, error } = await api("users").GET();
const { data: user } = await api("users/:id").GET({ params: { id: "123" } });
await api("users").POST({ body: { name: "John" } });
```

## Hooks API

### useRead

Fetch data with automatic caching and state management.

```typescript
const { data, loading, error, trigger } = useRead(
  (api) => api("users").GET(),
  { staleTime: 30000, enabled: true }
);
```

**Returns:** `data`, `loading`, `fetching`, `error`, `trigger()`, `abort()`, `meta`

**Options:** `enabled`, `tags`, `staleTime`, `retry`, `pollingInterval`, `refetch`, `debounce`, `transform`, `initialData`

### useWrite

Perform mutations (POST, PUT, DELETE).

```typescript
const { trigger, loading, error } = useWrite((api) => api("users").POST());

await trigger({
  body: { name, email },
  invalidate: "all"
});
```

**Returns:** `trigger()`, `loading`, `error`, `data`, `meta`, `abort()`

**Trigger options:** `body`, `params`, `query`, `headers`, `invalidate`, `clearCache`, `optimistic`

### usePages

Bidirectional pagination with infinite scroll.

```typescript
const { data, fetchNext, canFetchNext, loading } = usePages(
  (api) => api("posts").GET({ query: { page: 1 } }),
  {
    canFetchNext: ({ lastPage }) => lastPage?.data?.hasMore ?? false,
    nextPageRequest: ({ lastPage, request }) => ({
      query: { ...request.query, page: (lastPage?.data?.page ?? 0) + 1 }
    }),
    merger: (pages) => pages.flatMap(p => p.data?.items ?? [])
  }
);
```

**Returns:** `data`, `pages`, `loading`, `fetchingNext`, `canFetchNext`, `fetchNext()`, `fetchPrev()`, `trigger()`

### useQueue

Queue management for batch operations with concurrency control.

```typescript
const { tasks, stats, trigger, retry } = useQueue(
  (api) => api("files").POST(),
  { concurrency: 3 }
);

files.forEach(file => trigger({ body: form({ file }) }));
```

**Returns:** `tasks`, `stats`, `trigger()`, `abort()`, `retry()`, `remove()`, `removeSettled()`, `clear()`, `setConcurrency()`

**Stats:** `pending`, `loading`, `settled`, `success`, `failed`, `total`, `percentage`

### useSSE

Server-Sent Events for real-time streaming.

```typescript
const { data, isConnected, trigger, disconnect } = useSSE(
  (api) => api("stream").GET(),
  { parse: "json", accumulate: "replace" }
);
```

**Returns:** `data`, `error`, `isConnected`, `loading`, `trigger()`, `disconnect()`, `reset()`

**Options:** `enabled`, `parse` (auto|json|text|json-done), `accumulate` (replace|merge), `maxRetries`, `retryDelay`

## Plugins

| Plugin | Purpose | Key Options |
|--------|---------|-------------|
| `cachePlugin` | Response caching | `staleTime` |
| `retryPlugin` | Automatic retries | `retry: { retries, delay }` |
| `pollingPlugin` | Auto-refresh | `pollingInterval` |
| `invalidationPlugin` | Cache invalidation | `invalidate` |
| `optimisticPlugin` | Instant UI updates | `optimistic` |
| `debouncePlugin` | Debounce requests | `debounce` |
| `refetchPlugin` | Refetch on focus | `refetch: { onFocus, onReconnect }` |
| `initialDataPlugin` | Preloaded data | `initialData` |
| `devtool` | Visual debugging panel | `enabled`, `showFloatingIcon` |

## Devtool

```typescript
import { devtool } from "@spoosh/devtool";

const spoosh = new Spoosh<ApiSchema, Error>("/api")
  .use([cachePlugin(), devtool({ enabled: process.env.NODE_ENV === "development" })]);
```

Features: request tracing, plugin visualization, cache inspector, timeline view.

## Cache Invalidation

```typescript
// After mutation
await trigger({ body: data, invalidate: "all" });    // Invalidate hierarchy
await trigger({ body: data, invalidate: "self" });   // Exact path only
await trigger({ body: data, invalidate: ["users"] }); // Specific tags
```

## Component Patterns

### Data Fetching

```typescript
export function UserList() {
  const { data, loading, error, trigger } = useRead(
    (api) => api("users").GET(),
    { staleTime: 30000 }
  );

  if (loading) return <UserListSkeleton />;
  if (error) return <ErrorMessage error={error} onRetry={trigger} />;
  if (!data?.length) return <EmptyState message="No users found" />;

  return (
    <ul>
      {data.map((user) => <UserCard key={user.id} user={user} />)}
    </ul>
  );
}
```

### Mutation Form

```typescript
export function CreateUserForm() {
  const [name, setName] = useState("");
  const { trigger, loading, error } = useWrite((api) => api("users").POST());

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await trigger({ body: { name }, invalidate: "all" });
    if (result.data) setName("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} disabled={loading} />
      {error && <p className="error">{error.message}</p>}
      <button disabled={loading}>{loading ? "Creating..." : "Create"}</button>
    </form>
  );
}
```

### Infinite Scroll

```typescript
export function InfinitePostList() {
  const { ref, inView } = useInView();
  const { data, loading, fetchingNext, canFetchNext, fetchNext } = usePages(
    (api) => api("posts").GET({ query: { page: 1, limit: 20 } }),
    {
      canFetchNext: ({ lastPage }) => lastPage?.data?.hasMore ?? false,
      nextPageRequest: ({ lastPage, request }) => ({
        query: { ...request.query, page: (lastPage?.data?.page ?? 0) + 1 }
      }),
      merger: (pages) => pages.flatMap((p) => p.data?.items ?? [])
    }
  );

  useEffect(() => {
    if (inView && canFetchNext && !fetchingNext) fetchNext();
  }, [inView, canFetchNext, fetchingNext]);

  if (loading) return <PostListSkeleton />;

  return (
    <div>
      {data?.map((post) => <PostCard key={post.id} post={post} />)}
      <div ref={ref}>{fetchingNext && <LoadingSpinner />}</div>
    </div>
  );
}
```

### Optimistic Updates

```typescript
export function ToggleLikeButton({ postId, liked, likeCount }: Props) {
  const { trigger } = useWrite((api) => api("posts/:id/like").POST());

  const handleToggle = () => {
    trigger({
      params: { id: postId },
      optimistic: (cache) => cache(`posts/${postId}`)
        .set((current) => ({
          ...current,
          liked: !liked,
          likeCount: liked ? likeCount - 1 : likeCount + 1
        }))
    });
  };

  return <button onClick={handleToggle}>{liked ? "Unlike" : "Like"} ({likeCount})</button>;
}
```

### Search with Debounce

```typescript
export function SearchUsers() {
  const [query, setQuery] = useState("");
  const { data, fetching } = useRead(
    (api) => api("users/search").GET({ query: { q: query } }),
    { enabled: query.length >= 2, debounce: 300 }
  );

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search..." />
      {fetching && <LoadingIndicator />}
      {data?.map((user) => <li key={user.id}>{user.name}</li>)}
    </div>
  );
}
```

### Polling

```typescript
export function JobStatus({ jobId }: { jobId: string }) {
  const { data } = useRead(
    (api) => api("jobs/:id").GET({ params: { id: jobId } }),
    {
      pollingInterval: ({ data }) => {
        if (data?.status === "completed" || data?.status === "failed") return false;
        return 2000;
      }
    }
  );

  return <p>Status: {data?.status}</p>;
}
```

## Next.js

### Server-side fetch with createClient

```typescript
// app/posts/page.tsx
import { createClient } from "@spoosh/core";

const api = createClient<ApiSchema, Error>(process.env.API_URL!);

export default async function PostsPage() {
  const { data: posts } = await api("posts").GET();
  return <PostList initialData={posts} />;
}
```

### Client with initialData

```typescript
// components/PostList.tsx
"use client";

export function PostList({ initialData }: { initialData: Post[] }) {
  const { data, loading } = useRead(
    (api) => api("posts").GET(),
    { initialData }  // No loading state on first render
  );

  return data?.map((post) => <PostCard key={post.id} post={post} />);
}
```

### Mutation with server revalidation

```typescript
// lib/spoosh.ts
import { nextjsPlugin } from "@spoosh/plugin-nextjs";

const spoosh = new Spoosh<ApiSchema, Error>("/api")
  .use([cachePlugin(), invalidationPlugin(), nextjsPlugin()]);
```

```typescript
// After mutation, Next.js cache tags are automatically revalidated
await trigger({ body: newPost, invalidate: "all" });
```

## Server Type Inference

### Hono

```typescript
import { Spoosh, StripPrefix } from "@spoosh/core";
import type { HonoToSpoosh } from "@spoosh/hono";

// Server: app.basePath("/api")
type FullSchema = HonoToSpoosh<typeof app>;
type ApiSchema = StripPrefix<FullSchema, "api">; // Avoid double /api/api

const spoosh = new Spoosh<ApiSchema, Error>("/api");
```

### Elysia

```typescript
import { Spoosh, StripPrefix } from "@spoosh/core";
import type { ElysiaToSpoosh } from "@spoosh/elysia";

// Server: new Elysia({ prefix: "/api" })
type FullSchema = ElysiaToSpoosh<typeof app>;
type ApiSchema = StripPrefix<FullSchema, "api">; // Avoid double /api/api

const spoosh = new Spoosh<ApiSchema, Error>("/api");
```

Use `StripPrefix` when your baseUrl includes the same prefix as the server's basePath to prevent double prefixing (e.g., `/api/api/users`).

## OpenAPI

```bash
# Export TypeScript → OpenAPI
npx spoosh-openapi export --schema ./schema.ts --output openapi.json

# Import OpenAPI → TypeScript
npx spoosh-openapi import openapi.json --output ./schema.ts
```

## References

For detailed API documentation:
- `references/hooks-api.md` - Complete hook signatures
- `references/plugins-api.md` - All plugin configurations
- `references/advanced-patterns.md` - Complex patterns and edge cases

If more detail needed, fetch https://spoosh.dev/docs/react/llms (or /llms-full for complete docs).
