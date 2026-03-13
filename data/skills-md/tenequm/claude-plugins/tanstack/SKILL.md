---
name: tanstack
description: Build type-safe React apps with TanStack Query (data fetching, caching, mutations), Router (file-based routing, search params, loaders), and Start (SSR, server functions, middleware). Use when working with react-query, data fetching, server state, routing, search params, loaders, SSR, server functions, or full-stack React. Triggers on tanstack, react query, query client, useQuery, useMutation, invalidateQueries, tanstack router, file-based routing, search params, route loader, tanstack start, createServerFn, server functions, SSR.
metadata:
  version: "0.1.0"
---

# TanStack (Query + Router + Start)

Type-safe libraries for React applications. **Query** manages server state (fetching, caching, mutations). **Router** provides file-based routing with validated search params and data loaders. **Start** extends Router with SSR, server functions, and middleware for full-stack apps.

## When to Use

**Query** - data fetching, caching, mutations, optimistic updates, infinite scroll, streaming AI/SSE responses, tRPC v11 integration
**Router** - file-based routing, type-safe navigation, validated search params, route loaders, code splitting, preloading
**Start** - SSR/SSG, server functions (type-safe RPCs), middleware, API routes, deployment to Cloudflare/Vercel/Node

**Decision tree:**
- Client-only SPA with API calls -> Router + Query
- Full-stack with SSR/server functions -> Start + Query (Start includes Router)

## TanStack Query v5

### Setup

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  )
}
```

### Queries

```tsx
import { useQuery, queryOptions } from '@tanstack/react-query'

// Reusable query definition (recommended pattern)
const todosQueryOptions = queryOptions({
  queryKey: ['todos'],
  queryFn: async () => {
    const res = await fetch('/api/todos')
    if (!res.ok) throw new Error('Failed to fetch')
    return res.json() as Promise<Todo[]>
  },
})

// In component - full type inference from queryOptions
function TodoList() {
  const { data, isLoading, error } = useQuery(todosQueryOptions)
  if (isLoading) return <Spinner />
  if (error) return <div>Error: {error.message}</div>
  return <ul>{data.map(t => <li key={t.id}>{t.title}</li>)}</ul>
}
```

### Mutations

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query'

function CreateTodo() {
  const queryClient = useQueryClient()
  const mutation = useMutation({
    mutationFn: (newTodo: { title: string }) =>
      fetch('/api/todos', { method: 'POST', body: JSON.stringify(newTodo) }).then(r => r.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  return (
    <button onClick={() => mutation.mutate({ title: 'New' })}>
      {mutation.isPending ? 'Creating...' : 'Create'}
    </button>
  )
}
```

### Key Patterns

**Query keys** - hierarchical arrays for cache management:
```tsx
['todos']                          // all todos
['todos', 'list', { page, sort }]  // filtered list
['todo', todoId]                   // single item
```

**Dependent queries** - chain with `enabled`:
```tsx
const { data: user } = useQuery({ queryKey: ['user', id], queryFn: () => fetchUser(id) })
const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => fetchProjects(user!.id),
  enabled: !!user?.id,
})
```

**Important defaults**: staleTime: 0, gcTime: 5min, retry: 3, refetchOnWindowFocus: true

**Suspense** - use `useSuspenseQuery` with `<Suspense>` boundaries

**Streamed queries** (experimental) - for AI chat/SSE:
```tsx
import { experimental_streamedQuery as streamedQuery } from '@tanstack/react-query'

const { data: chunks } = useQuery(queryOptions({
  queryKey: ['chat', sessionId],
  queryFn: streamedQuery({ streamFn: () => fetchChatStream(sessionId), refetchMode: 'reset' }),
}))
```

### DevTools

```bash
pnpm add @tanstack/react-query-devtools
```
```tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
// Add inside QueryClientProvider
<ReactQueryDevtools initialIsOpen={false} />
```

### Query Deep Dives

- `query-guide.md` - Complete Query reference with all patterns
- `infinite-queries.md` - useInfiniteQuery, pagination, virtual scroll
- `optimistic-updates.md` - Optimistic UI, rollback, undo
- `query-performance.md` - staleTime tuning, deduplication, prefetching
- `query-invalidation.md` - Cache invalidation strategies, filters, predicates
- `query-typescript.md` - Type inference, generics, custom hooks

---

## TanStack Router v1

### Setup (Vite)

```bash
pnpm add @tanstack/react-router @tanstack/router-plugin
```

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { tanstackRouter } from '@tanstack/router-plugin/vite'

export default defineConfig({
  plugins: [
    tanstackRouter({ autoCodeSplitting: true }),
    react(),
  ],
})
```

```tsx
// src/router.ts
import { createRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

export const router = createRouter({ routeTree, defaultPreload: 'intent' })

declare module '@tanstack/react-router' {
  interface Register { router: typeof router }
}
```

### File-Based Routing

Files in `src/routes/` auto-generate route config:

| Convention | Purpose | Example |
|---|---|---|
| `__root.tsx` | Root route (always rendered) | `src/routes/__root.tsx` |
| `index.tsx` | Index route | `src/routes/index.tsx` -> `/` |
| `$param` | Dynamic segment | `posts.$postId.tsx` -> `/posts/:id` |
| `_prefix` | Pathless layout | `_layout.tsx` wraps children |
| `(folder)` | Route group (no URL) | `(auth)/login.tsx` -> `/login` |

### Type-Safe Navigation

```tsx
<Link to="/posts/$postId" params={{ postId: '123' }}>View Post</Link>

// Active styling
<Link to="/posts" activeProps={{ className: 'font-bold' }}>Posts</Link>

// Imperative
const navigate = useNavigate({ from: '/posts' })
navigate({ to: '/posts/$postId', params: { postId: post.id } })
```

Always provide `from` on Link and hooks - narrows types and improves TS performance.

### Search Params

```tsx
import { zodValidator, fallback } from '@tanstack/zod-adapter'
import { z } from 'zod'

const searchSchema = z.object({
  page: fallback(z.number(), 1).default(1),
  sort: fallback(z.enum(['newest', 'oldest']), 'newest').default('newest'),
})

export const Route = createFileRoute('/products')({
  validateSearch: zodValidator(searchSchema),
  component: () => {
    const { page, sort } = Route.useSearch()
    // Writing
    return <Link from={Route.fullPath} search={prev => ({ ...prev, page: prev.page + 1 })}>Next</Link>
  },
})
```

Use `fallback(...).default(...)` from the Zod adapter. Plain `.catch()` causes type loss.

### Data Loading

```tsx
export const Route = createFileRoute('/posts')({
  // loaderDeps: only extract what loader needs (not full search)
  loaderDeps: ({ search: { page } }) => ({ page }),
  loader: ({ deps: { page } }) => fetchPosts({ page }),
  pendingComponent: () => <Spinner />,
  component: () => {
    const posts = Route.useLoaderData()
    return <PostList posts={posts} />
  },
})
```

### Route Context (Dependency Injection)

```tsx
// __root.tsx
interface RouterContext { queryClient: QueryClient }
export const Route = createRootRouteWithContext<RouterContext>()({ component: Root })

// router.ts
const router = createRouter({ routeTree, context: { queryClient } })

// Child route - queryClient available in loader
export const Route = createFileRoute('/posts')({
  loader: ({ context: { queryClient } }) =>
    queryClient.ensureQueryData(postsQueryOptions()),
})
```

### Router Deep Dives

- `router-guide.md` - Complete Router reference with all patterns
- `search-params.md` - Custom serialization, Standard Schema, sharing params
- `data-loading.md` - Deferred loading, streaming SSR, shouldReload
- `routing-patterns.md` - Virtual routes, route masking, navigation blocking
- `code-splitting.md` - Automatic/manual splitting strategies
- `router-ssr.md` - SSR setup, streaming, hydration

---

## TanStack Start (RC)

Full-stack framework extending Router with SSR, server functions, middleware. API stable, feature-complete. No RSC yet.

### Setup

```bash
pnpm create @tanstack/start@latest
```

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import viteReact from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    tanstackStart(),
    viteReact(), // MUST come after tanstackStart()
  ],
})
```

### Server Functions

Type-safe RPCs. Server code extracted from client bundles at build time.

```tsx
import { createServerFn } from '@tanstack/react-start'
import { z } from 'zod'

// GET - no input
export const getUsers = createServerFn({ method: 'GET' })
  .handler(async () => db.users.findMany())

// POST - validated input
export const createUser = createServerFn({ method: 'POST' })
  .inputValidator(z.object({ name: z.string(), email: z.string().email() }))
  .handler(async ({ data }) => db.users.create(data))

// Call from loader
export const Route = createFileRoute('/users')({
  loader: () => getUsers(),
  component: () => {
    const users = Route.useLoaderData()
    return <UserList users={users} />
  },
})
```

**Critical**: Loaders are isomorphic (run on server AND client). Never put secrets in loaders - use `createServerFn()` instead.

### Middleware

```tsx
import { createMiddleware } from '@tanstack/react-start'

const authMiddleware = createMiddleware({ type: 'function' })
  .server(async ({ next }) => {
    const user = await getCurrentUser()
    if (!user) throw redirect({ to: '/login' })
    return next({ context: { user } })
  })

const getProfile = createServerFn()
  .middleware([authMiddleware])
  .handler(async ({ context }) => context.user) // typed
```

Global middleware via `src/start.ts`:
```tsx
export const startInstance = createStart(() => ({
  requestMiddleware: [logger],    // all requests
  functionMiddleware: [auth],     // all server functions
}))
```

### SSR Modes

| Mode | Use Case |
|------|----------|
| `true` (default) | SEO, performance |
| `false` | Browser-only features |
| `'data-only'` | Dashboards (data on server, render on client) |

SPA mode: `tanstackStart({ spa: { enabled: true } })` in vite.config.ts

### Deployment

- **Cloudflare Workers**: `@cloudflare/vite-plugin` (official partner)
- **Netlify**: `@netlify/vite-plugin-tanstack-start`
- **Node/Vercel/Bun/Docker**: via Nitro
- **Static**: `tanstackStart({ prerender: { enabled: true, crawlLinks: true } })`

### Start Deep Dives

- `start-guide.md` - Complete Start reference with all patterns
- `server-functions.md` - Streaming, FormData, progressive enhancement
- `middleware.md` - sendContext, custom fetch, global config
- `ssr-modes.md` - Selective SSR, shellComponent, fallback rendering
- `server-routes.md` - Dynamic params, wildcards, pathless layouts

---

## Best Practices

1. **Use `queryOptions()` factory** for reusable, type-safe query definitions
2. **Structure query keys hierarchically** - `['entity', 'action', { filters }]`
3. **Set staleTime per data type** - static: `Infinity`, dynamic: `0`, moderate: `5min`
4. **Always validate search params** with Zod via `zodValidator` + `fallback().default()`
5. **Provide `from` on navigation** - narrows types, catches route mismatches
6. **Use route context for DI** - pass QueryClient, auth via `createRootRouteWithContext`
7. **Set `defaultPreload: 'intent'`** globally for perceived performance
8. **Never put secrets in loaders** - use `createServerFn()` for server-only code
9. **Compose middleware hierarchically** - global -> route -> function
10. **Use `head()` on every content route** for SEO (title, description, OG tags)

## Resources

- **Query Docs**: https://tanstack.com/query/latest/docs/framework/react/overview
- **Router Docs**: https://tanstack.com/router/latest/docs/framework/react/overview
- **Start Docs**: https://tanstack.com/start/latest/docs/framework/react/overview
- **GitHub**: https://github.com/TanStack/query | https://github.com/TanStack/router
- **Discord**: https://discord.gg/tanstack
