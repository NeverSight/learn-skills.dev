---
name: tanstack-query
description: |
  TanStack Query (React Query) for async operations, data fetching, caching, and state management.
  
  Use when: fetching server data, managing async operations, caching responses, handling mutations, or any operation that benefits from automatic state management and caching.
---

# Skill: tanstack-query

## Scope

- Applies to: TanStack Query v5+ for async operations, data fetching, caching, mutations, infinite queries, optimistic updates
- Does NOT cover: URL state management (use nuqs), grouped synchronous state (use ahooks.useSetState), localStorage persistence (use ahooks.useLocalStorageState)

## Assumptions

- TanStack Query v5+
- React 18+ with hooks support
- TypeScript v5+ (for type inference)
- `@lukemorales/query-key-factory` for query key management
- QueryClientProvider configured at app root

## Principles

- Use TanStack Query for ANY async operation that benefits from caching or state management
- Query key factory pattern for centralized, type-safe query keys
- Never manually manage `isLoading`, `error`, or `isError` states (provided by hooks)
- `queryFn` can be any Promise-returning function (not just HTTP calls)
- All TanStack features work identically regardless of data source: caching, deduping, background refetching, stale-while-revalidate

## Constraints

### MUST

- Use query key factory (`@lukemorales/query-key-factory`) for all query keys
- Use TanStack Query hooks for async operations (never manually manage loading/error states)
- Use namespace invalidation: `queryClient.invalidateQueries({ queryKey: users._def })`

### SHOULD

- Use TanStack Query for any async operation that benefits from caching (HTTP, localStorage reads, local computations, file operations)
- Extract query logic into custom hooks for reusability
- Combine multiple queries into cohesive hooks
- Use TypeScript generics for type-safe queries: `useQuery<ResponseType>(...)`
- Configure QueryClient defaults (retry, staleTime) at provider level

### AVOID

- Manually constructing query keys: `useQuery({ queryKey: ['users', id] })`
- Hardcoding query keys in invalidations: `queryClient.invalidateQueries({ queryKey: ['users'] })`
- Manually managing loading/error states (use hook-provided states)
- Using for URL-shareable state (use nuqs instead)
- Using for grouped synchronous state (use ahooks.useSetState instead)
- Using for one-off promises without caching needs (use plain async/await in event handlers)

## Interactions

- Complements nuqs for URL state management (queries can depend on URL params)
- Complements ahooks for synchronous state (useSetState for form state, useLocalStorageState for persistence)
- Works with generated API clients from OpenAPI specs (@repo/react)
- Part of state management decision tree (see React rules)

## Patterns

### Query Key Factory Pattern

Centralized, type-safe query keys:

```typescript
import { createQueryKeys } from '@lukemorales/query-key-factory'

export const users = createQueryKeys('users', {
  detail: (id: string) => ({
    queryKey: [id],
    queryFn: () => fetchUser(id),
  }),
  list: (filters?: Filters) => ({
    queryKey: [filters],
    queryFn: () => fetchUsers(filters),
  }),
})

// Usage
import { useQuery } from '@tanstack/react-query'
import { users } from '@/queries/users'

const { data, isLoading, error } = useQuery(users.detail(userId))
```

**File Organization**: `src/queries/users.ts` - Query key factory for users, `src/queries/articles.ts` - Query key factory for articles, `src/queries/index.ts` - Re-export all query keys

### Versatile queryFn Pattern

TanStack Query accepts ANY async `queryFn`—not just HTTP calls:

```typescript
// Server data fetching (traditional)
const { data } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => fetchUser(userId),
})

// Local computation (no network)
const { data } = useQuery({
  queryKey: ['fibonacci', n],
  queryFn: () => computeFibonacci(n),
})

// localStorage read
const { data: settings } = useQuery({
  queryKey: ['user-settings'],
  queryFn: () => Promise.resolve(
    JSON.parse(localStorage.getItem('settings') || '{}')
  ),
})

// File operation
const { data } = useQuery({
  queryKey: ['file-content', path],
  queryFn: () => readFile(path),
})
```

**When to use**: Any async operation that benefits from automatic caching, stale management, or repeated execution

**When NOT to use**: One-off promises without caching needs (use plain async/await in event handlers)

### Mutation Pattern

Mutations with automatic invalidation:

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { users } from '@/queries/users'

function useCreateUser() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (data: CreateUserInput) => {
      const response = await createUser(data)
      return response
    },
    onSuccess: () => {
      // Namespace invalidation (recommended)
      queryClient.invalidateQueries({ queryKey: users._def })
    },
  })
}

// Usage
const createUser = useCreateUser()
createUser.mutate({ name: 'John', email: 'john@example.com' })
```

### Infinite Query Pattern

Pagination with infinite scroll:

```typescript
import { useInfiniteQuery } from '@tanstack/react-query'
import { users } from '@/queries/users'

const {
  data,
  fetchNextPage,
  hasNextPage,
  isFetchingNextPage,
} = useInfiniteQuery({
  queryKey: ['users', 'infinite'],
  queryFn: ({ pageParam = 0 }) => fetchUsers({ page: pageParam }),
  getNextPageParam: (lastPage, pages) => lastPage.nextPage,
  initialPageParam: 0,
})
```

### QueryClient Configuration

Configure defaults at provider level:

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        retry: 1,
        refetchOnWindowFocus: false,
      },
    },
  }))

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

### Generated API Client Integration

Use generated hooks from OpenAPI specs:

```typescript
import { useHealthCheck } from '@repo/react'

function HealthStatus() {
  const { data, isLoading, error } = useHealthCheck()
  
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return <div>Status: {data.status}</div>
}
```

### Custom Hook Pattern

Extract query logic into reusable hooks:

```typescript
// hooks/useUser.ts
import { useQuery } from '@tanstack/react-query'
import { users } from '@/queries/users'

export function useUser(userId: string) {
  return useQuery(users.detail(userId))
}

// Component usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useUser(userId)
  // ...
}
```

### State Management Decision Tree

1. **URL-shareable state** → Use `nuqs` (filters, search, tabs, pagination)
2. **Grouped state not in URL** → Use `ahooks.useSetState` (form state, game engine, ephemeral UI)
3. **Async operations** → Use TanStack Query (data fetching, mutations, caching)
4. **localStorage persistence** → Use `ahooks.useLocalStorageState` (preferences, settings)
5. **Simple independent state** → Use `useState` (rare, prefer other options)

**Use TanStack Query for**: Server data fetching, mutations, optimistic updates, background refetching, caching, any async operation that benefits from state management

**Don't use TanStack Query for**: URL-shareable state (use nuqs), grouped synchronous state (use ahooks.useSetState), one-off promises without caching needs

## References

- [TanStack Query documentation](https://tanstack.com/query/latest) - Official documentation
- [Query Key Factory](https://github.com/lukemorales/query-key-factory) - Query key factory library
- React rules - State management decision tree and patterns
- [ahooks](@cursor/skills/ahooks-v3/SKILL.md) - Utility hooks for synchronous state
- [OpenAPI Integration](@cursor/skills/openapi-ts-v0/references/react-query-integration.md) - Generated client patterns
