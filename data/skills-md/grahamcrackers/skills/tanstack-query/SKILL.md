---
name: tanstack-query
description: TanStack Query v5 patterns for server state management, caching, mutations, optimistic updates, and query organization. Use when working with TanStack Query, React Query, server state, data fetching hooks, or when the user asks about caching strategies, query invalidation, or mutation patterns.
---

# TanStack Query v5 Best Practices

## Core Principles

- TanStack Query manages **server state** — async data from APIs, databases, etc. Don't use it for client-only state (forms, UI toggles, modals).
- All hooks use a **single object signature** (v5 breaking change):

```tsx
useQuery({ queryKey, queryFn, ...options });
useMutation({ mutationFn, ...options });
```

## Query Keys

Design query keys as hierarchical arrays for granular invalidation:

```typescript
const queryKeys = {
    users: {
        all: ["users"] as const,
        lists: () => [...queryKeys.users.all, "list"] as const,
        list: (filters: UserFilters) => [...queryKeys.users.lists(), filters] as const,
        details: () => [...queryKeys.users.all, "detail"] as const,
        detail: (id: string) => [...queryKeys.users.details(), id] as const,
    },
} as const;
```

Use a query key factory per domain entity. This enables:

- `queryClient.invalidateQueries({ queryKey: queryKeys.users.all })` — invalidate everything user-related.
- `queryClient.invalidateQueries({ queryKey: queryKeys.users.lists() })` — invalidate only lists.

## Custom Query Hooks

Wrap `useQuery` in custom hooks — never call `useQuery` directly in components:

```typescript
function useUser(id: string) {
    return useQuery({
        queryKey: queryKeys.users.detail(id),
        queryFn: () => api.users.getById(id),
        staleTime: 5 * 60 * 1000,
    });
}

function useUsers(filters: UserFilters) {
    return useQuery({
        queryKey: queryKeys.users.list(filters),
        queryFn: () => api.users.list(filters),
    });
}
```

This collocates query configuration, makes queries reusable, and provides a single place to update options.

## Important Defaults

Understand the defaults before overriding them:

| Default                | Value  | Notes                                                         |
| ---------------------- | ------ | ------------------------------------------------------------- |
| `staleTime`            | `0`    | Data is immediately stale; refetches on mount/focus/reconnect |
| `gcTime`               | 5 min  | Inactive cache entries garbage collected after 5 minutes      |
| `retry`                | `3`    | Failed queries retry 3 times with exponential backoff         |
| `refetchOnWindowFocus` | `true` | Stale queries refetch when window regains focus               |
| `structuralSharing`    | `true` | Results are referentially stable if data hasn't changed       |

Set `staleTime` appropriately for your data — data that rarely changes can have `staleTime: Infinity`.

## Mutations

### Basic Mutation Hook

```typescript
function useCreateUser() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: CreateUserInput) => api.users.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.users.lists() });
        },
    });
}
```

### Direct Cache Updates

When the mutation response contains the updated data, update the cache directly instead of refetching:

```typescript
function useUpdateUser() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: UpdateUserInput }) => api.users.update(id, data),
        onSuccess: (updatedUser) => {
            queryClient.setQueryData(queryKeys.users.detail(updatedUser.id), updatedUser);
            queryClient.invalidateQueries({ queryKey: queryKeys.users.lists() });
        },
    });
}
```

Always use **immutable updates** with `setQueryData` — spread or structuredClone, never mutate in place.

### Optimistic Updates

```typescript
function useToggleTodo() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => api.todos.toggle(id),
        onMutate: async (id) => {
            await queryClient.cancelQueries({ queryKey: queryKeys.todos.detail(id) });
            const previous = queryClient.getQueryData(queryKeys.todos.detail(id));

            queryClient.setQueryData(queryKeys.todos.detail(id), (old: Todo) => ({
                ...old,
                completed: !old.completed,
            }));

            return { previous };
        },
        onError: (_err, id, context) => {
            queryClient.setQueryData(queryKeys.todos.detail(id), context?.previous);
        },
        onSettled: (_data, _err, id) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.todos.detail(id) });
        },
    });
}
```

## Dependent Queries

Use `enabled` to defer queries until prerequisites are available:

```typescript
function useUserPosts(userId: string | undefined) {
    return useQuery({
        queryKey: queryKeys.posts.byUser(userId!),
        queryFn: () => api.posts.getByUser(userId!),
        enabled: !!userId,
    });
}
```

## Infinite Queries

```typescript
function useInfiniteUsers() {
    return useInfiniteQuery({
        queryKey: queryKeys.users.lists(),
        queryFn: ({ pageParam }) => api.users.list({ cursor: pageParam }),
        initialPageParam: undefined as string | undefined,
        getNextPageParam: (lastPage) => lastPage.nextCursor,
    });
}
```

## Suspense Integration

```typescript
function useUserSuspense(id: string) {
    return useSuspenseQuery({
        queryKey: queryKeys.users.detail(id),
        queryFn: () => api.users.getById(id),
    });
}
```

`useSuspenseQuery` guarantees `data` is never `undefined` — no need for loading/error checks in the component. Wrap the parent in `<Suspense>` and `<ErrorBoundary>`.

## Query Organization

```
src/
├── api/              # API client functions (no TanStack Query here)
│   └── users.ts
├── queries/          # query hooks and key factories
│   ├── keys.ts       # all query key factories
│   ├── users.ts      # useUser, useUsers, useCreateUser, etc.
│   └── posts.ts
```

Keep API functions pure (return promises), and keep TanStack Query hooks in a separate layer. This makes the API layer testable without TanStack Query and keeps query hooks thin.

## Anti-Patterns to Avoid

- **Don't use `useEffect` to sync query data into local state** — use the query result directly.
- **Don't duplicate server state in `useState`** — TanStack Query is your cache.
- **Don't invalidate everything** — use specific query keys to invalidate only what changed.
- **Don't forget `enabled: false`** when a query depends on runtime data that might be `undefined`.
