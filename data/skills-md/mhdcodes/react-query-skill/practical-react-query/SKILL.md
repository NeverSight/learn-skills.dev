---
name: practical-react-query
description: Comprehensive guide to React Query (TanStack Query) covering data fetching, caching, mutations, error handling, TypeScript, testing, and advanced patterns. Use when working with React Query, TanStack Query, or async state management in React applications.
license: MIT
metadata:
  author: tkdodo
---

# React Query Guide

This skill provides comprehensive guidance on React Query (TanStack Query) for building modern React applications with async state management.

## When to Use This Skill

Use this skill when you need help with:

- Setting up and configuring React Query
- Data fetching, caching, and synchronization
- Mutations and optimistic updates
- Error handling and retry strategies
- TypeScript integration
- Testing React Query code
- Performance optimization
- Advanced patterns and best practices

## Topics

Read the relevant reference file based on what you need:

### Getting Started

| Topic                 | Description                                       | File                                                              |
| --------------------- | ------------------------------------------------- | ----------------------------------------------------------------- |
| Practical React Query | Core concepts, defaults, query keys, custom hooks | [01-practical-react-query.md](references/01-practical-react-query.md) |
| Why Use React Query   | Benefits and reasons to adopt React Query         | [23-why-use.md](references/23-why-use.md)                             |
| When Not Needed       | Simpler alternatives when React Query is overkill | [21-when-not-needed.md](references/21-when-not-needed.md)             |

### Core Concepts

| Topic                  | Description                                            | File                                                                |
| ---------------------- | ------------------------------------------------------ | ------------------------------------------------------------------- |
| Query Keys             | Structuring keys for caching, refetching, invalidation | [08-query-keys.md](references/08-query-keys.md)                         |
| Query Function Context | Extract params from query keys                         | [09-query-function-context.md](references/09-query-function-context.md) |
| Query Options API      | Code organization and type inference                   | [24-query-options-api.md](references/24-query-options-api.md)           |
| State Manager          | React Query as an async state manager                  | [11-state-manager.md](references/11-state-manager.md)                   |

### Data Handling

| Topic                      | Description                                          | File                                                                    |
| -------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------- |
| Data Transformations       | Transform data in queryFn, render, or select         | [02-data-transformations.md](references/02-data-transformations.md)         |
| Placeholder & Initial Data | Pre-fill cache, improve UX                           | [10-placeholder-initial-data.md](references/10-placeholder-initial-data.md) |
| Seeding Cache              | Pre-populate query cache                             | [18-seeding-cache.md](references/18-seeding-cache.md)                       |
| Selectors                  | Advanced selector patterns for partial subscriptions | [28-selectors.md](references/28-selectors.md)                               |

### Mutations & Updates

| Topic                         | Description                                   | File                                                              |
| ----------------------------- | --------------------------------------------- | ----------------------------------------------------------------- |
| Mutations                     | useMutation, optimistic updates, invalidation | [13-mutations.md](references/13-mutations.md)                         |
| Auto Invalidation             | Automatic query invalidation patterns         | [25-auto-invalidation.md](references/25-auto-invalidation.md)         |
| Concurrent Optimistic Updates | Handle concurrent optimistic updates          | [27-concurrent-optimistic.md](references/27-concurrent-optimistic.md) |

### State & Error Handling

| Topic          | Description                        | File                                                |
| -------------- | ---------------------------------- | --------------------------------------------------- |
| Status Checks  | Loading states, background errors  | [04-status-checks.md](references/04-status-checks.md)   |
| Error Handling | Error boundaries, retry strategies | [12-error-handling.md](references/12-error-handling.md) |

### Performance

| Topic                | Description                                              | File                                                            |
| -------------------- | -------------------------------------------------------- | --------------------------------------------------------------- |
| Render Optimizations | notifyOnChangeProps, tracked queries, structural sharing | [03-render-optimizations.md](references/03-render-optimizations.md) |
| Infinite Queries     | Pagination, infinite scroll                              | [26-infinite-queries.md](references/26-infinite-queries.md)         |

### Integration

| Topic         | Description                                     | File                                            |
| ------------- | ----------------------------------------------- | ----------------------------------------------- |
| TypeScript    | Generics, type narrowing, enabled option typing | [06-typescript.md](references/06-typescript.md)     |
| Type Safety   | Advanced TypeScript patterns                    | [20-type-safe.md](references/20-type-safe.md)       |
| React Router  | Data loading, navigation integration            | [17-react-router.md](references/17-react-router.md) |
| React Context | Combining with React Context                    | [22-context.md](references/22-context.md)           |
| WebSockets    | Real-time data sync                             | [07-websockets.md](references/07-websockets.md)     |
| Forms         | Form integration, handling form state           | [15-forms.md](references/15-forms.md)               |

### Advanced

| Topic           | Description                               | File                                      |
| --------------- | ----------------------------------------- | ----------------------------------------- |
| Internals       | QueryClient, QueryCache, QueryObserver    | [19-internals.md](references/19-internals.md) |
| Offline Support | Persistence, offline mutations            | [14-offline.md](references/14-offline.md)     |
| Testing         | Mocking network requests, MSW integration | [05-testing.md](references/05-testing.md)     |
| FAQs            | Frequently asked questions                | [16-faqs.md](references/16-faqs.md)           |

## Quick Reference

### Basic Query

```tsx
import { useQuery } from "@tanstack/react-query";

function Component() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["todos"],
    queryFn: fetchTodos,
  });
}
```

### Basic Mutation

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function Component() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: addTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });
}
```

### Query Client Setup

```tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  );
}
```
