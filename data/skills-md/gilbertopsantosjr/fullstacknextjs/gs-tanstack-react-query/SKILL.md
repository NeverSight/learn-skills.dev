---
name: gs-tanstack-react-query
description: TanStack React Query for data fetching with Clean Architecture. Queries return DTOs, mutations call server actions. Use when working with useQuery, useMutation, cache invalidation, or integrating ZSA server actions.
---

# TanStack React Query (Clean Architecture)

## Data Flow with DTOs

```
useServerActionQuery → Server Action → Use Case → DTO
```

All query responses are **DTOs**, not Entities. TypeScript types should reflect this.

## Core Hooks

```typescript
import {
  useServerActionQuery,
  useServerActionMutation,
  useServerActionInfiniteQuery,
} from '@saas4dev/core'

import { useQueryClient } from '@tanstack/react-query'
```

## Query with DTO Types

```typescript
import type { CategoryDTO } from '@/features/category'
import { listCategoriesAction, getCategoryAction } from '@/features/category'

// List query - returns CategoryDTO[]
const { data, isLoading } = useServerActionQuery(listCategoriesAction, {
  input: { status: 'active' },
  queryKey: ['categories', 'list', { status: 'active' }],
})

// data.items is CategoryDTO[]

// Single item query
const { data: category } = useServerActionQuery(getCategoryAction, {
  input: { id },
  queryKey: ['categories', 'detail', id],
})

// category is CategoryDTO
```

## Mutation with Invalidation

```typescript
import { createCategoryAction } from '@/features/category'

const queryClient = useQueryClient()

const mutation = useServerActionMutation(createCategoryAction, {
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['categories'] })
    toast.success('Category created')
  },
  onError: (error) => toast.error(error.message),
})

// Usage
mutation.mutate({ name: 'New Category' })
```

## Query Key Pattern

```typescript
// Hierarchical keys for precise invalidation
['categories']                           // All categories
['categories', 'list']                   // All lists
['categories', 'list', { status }]       // Filtered list
['categories', 'detail', id]             // Single item
```

### Query Key Factory

```typescript
export const categoryKeys = {
  all: ['categories'] as const,
  lists: () => [...categoryKeys.all, 'list'] as const,
  list: (filters: { status?: string }) => [...categoryKeys.lists(), filters] as const,
  details: () => [...categoryKeys.all, 'detail'] as const,
  detail: (id: string) => [...categoryKeys.details(), id] as const,
}
```

## Optimistic Update

```typescript
const mutation = useServerActionMutation(updateCategoryAction, {
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: ['categories', 'detail', newData.id] })
    const previous = queryClient.getQueryData<CategoryDTO>(['categories', 'detail', newData.id])

    queryClient.setQueryData<CategoryDTO>(
      ['categories', 'detail', newData.id],
      (old) => old ? { ...old, ...newData } : old
    )

    return { previous }
  },
  onError: (err, newData, context) => {
    if (context?.previous) {
      queryClient.setQueryData(['categories', 'detail', newData.id], context.previous)
    }
  },
  onSettled: (_, __, variables) => {
    queryClient.invalidateQueries({ queryKey: ['categories', 'detail', variables.id] })
  },
})
```

## Pagination

```typescript
const { data, fetchNextPage, hasNextPage } = useServerActionInfiniteQuery(
  listCategoriesAction,
  {
    queryKey: ['categories', 'list'],
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: undefined,
    input: ({ pageParam }) => ({ cursor: pageParam, limit: 20 }),
  }
)

// data.pages[].items is CategoryDTO[]
```

## Best Practices

1. **Type with DTOs** - `useQueryData<CategoryDTO>()` not `Category`
2. **Actions only** - Never call Use Cases from components
3. **Hierarchical keys** - Invalidate broadly, fetch specifically
4. **Error handling** - Show domain exception messages
5. **Optimistic updates** - Always implement rollback

## References

- Web Client: `skills/nextjs-web-client/SKILL.md`
- Server Actions: `skills/nextjs-server-actions/SKILL.md`
