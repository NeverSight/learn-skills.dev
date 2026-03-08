---
name: tanstack-start
displayName: TanStack Start
description: Build full-stack React apps with TanStack Start — server functions, type-safe routing, loaders, middleware, SSR/streaming, and deployment patterns. Use when working on TanStack Start apps, server functions, TanStack Router, or any gremlin-cms development.
version: 0.1.0
author: joel
tags:
  - framework
  - tanstack
  - react
  - fullstack
  - gremlin
disable-model-invocation: true
---

# TanStack Start

Full-stack React framework built on TanStack Router + Vite. Client-first with opt-in server capabilities. Type-safe from routes to server functions.

## When to Use

Triggers: `tanstack start`, `tanstack router`, `server function`, `createServerFn`, `createFileRoute`, `gremlin-cms`, `tanstack app`, or any work in a TanStack Start project.

## Core Concepts

### Execution Model — Critical

**Route loaders are ISOMORPHIC** — they run on BOTH server and client. This is the #1 gotcha.

```ts
// ❌ WRONG — loader runs on client too, exposes secrets
export const Route = createFileRoute('/users')({
  loader: () => {
    const secret = process.env.SECRET // Exposed to client!
    return fetch(`/api/users?key=${secret}`)
  },
})

// ✅ CORRECT — server function wraps server-only logic
const getUsers = createServerFn().handler(() => {
  const secret = process.env.SECRET // Server-only
  return fetch(`/api/users?key=${secret}`)
})

export const Route = createFileRoute('/users')({
  loader: () => getUsers(), // Isomorphic call to server function
})
```

### Server Functions

Type-safe RPC that replaces REST/tRPC/GraphQL for internal data access. Build process replaces server implementations with RPC stubs in client bundles.

```ts
import { createServerFn } from '@tanstack/react-start'

// GET (default)
export const getPosts = createServerFn().handler(async () => {
  return db.posts.findMany()
})

// POST with input validation
export const createPost = createServerFn({ method: 'POST' })
  .inputValidator((data: { title: string; body: string }) => data)
  .handler(async ({ data }) => {
    return db.posts.create(data)
  })
```

**Where to call server functions:**
- Route loaders — data fetching
- Components — via `useServerFn()` hook
- Other server functions — compose server logic
- Event handlers — form submissions, clicks

### Server-Only Functions

For utilities that must NEVER reach the client bundle:

```ts
import { createServerOnlyFn } from '@tanstack/react-start'

const getDbUrl = createServerOnlyFn(() => process.env.DATABASE_URL)
// Calling from client THROWS — crashes intentionally
```

### File-Based Routing

```
app/
├── routes/
│   ├── __root.tsx          # Root layout
│   ├── index.tsx           # /
│   ├── about.tsx           # /about
│   ├── posts/
│   │   ├── index.tsx       # /posts
│   │   └── $postId.tsx     # /posts/:postId
│   └── _authed/
│       └── dashboard.tsx   # /dashboard (with auth layout)
├── client.tsx              # Client entry
├── router.tsx              # Router config
└── ssr.tsx                 # SSR entry
```

- `$param` = dynamic segment
- `_prefix` = pathless layout route (groups routes without adding URL segments)
- `__root.tsx` = root layout (wraps everything)

### Route Definition

```ts
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/posts/$postId')({
  // Loader runs before render (isomorphic!)
  loader: ({ params }) => getPost({ data: params.postId }),

  // Component receives loader data
  component: PostPage,

  // Error boundary
  errorComponent: ({ error }) => <div>Error: {error.message}</div>,

  // Pending component (while loader runs)
  pendingComponent: () => <div>Loading...</div>,
})

function PostPage() {
  const post = Route.useLoaderData()
  return <h1>{post.title}</h1>
}
```

### Middleware

Compose reusable server function middleware:

```ts
import { createMiddleware } from '@tanstack/react-start'

const authMiddleware = createMiddleware({ type: 'function' }).server(
  async ({ next }) => {
    const session = await getSessionFn()
    if (!session?.user) throw new Error('Unauthorized')
    return next({ context: { session } })
  }
)

// Use in server functions
export const listPosts = createServerFn({ method: 'GET' })
  .middleware([authMiddleware])
  .handler(async ({ context }) => {
    return db.posts.where({ userId: context.session.user.id })
  })
```

### Server Routes (API endpoints)

```ts
export const Route = createFileRoute('/api/health')({
  server: {
    handlers: ({ createHandlers }) => createHandlers({
      GET: async ({ request }) => {
        return new Response(JSON.stringify({ ok: true }), {
          headers: { 'Content-Type': 'application/json' },
        })
      },
    }),
  },
})
```

### Using with TanStack Query

```ts
import { useServerFn } from '@tanstack/react-start'
import { useQuery, useMutation } from '@tanstack/react-query'

function PostList() {
  const getPostsFn = useServerFn(getPosts)
  const createPostFn = useServerFn(createPost)

  const { data } = useQuery({
    queryKey: ['posts'],
    queryFn: () => getPostsFn(),
  })

  const mutation = useMutation({
    mutationFn: (data) => createPostFn({ data }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['posts'] }),
  })
}
```

## File Organization (Large Apps)

```
src/utils/
├── users.functions.ts    # createServerFn wrappers (safe to import anywhere)
├── users.server.ts       # Server-only helpers (DB queries, internal logic)
└── schemas.ts            # Shared validation schemas (client-safe)
```

- `.functions.ts` — server function wrappers, safe to import anywhere
- `.server.ts` — server-only helpers, NEVER import from client code

## App Config

```ts
// app.config.ts
import { defineConfig } from '@tanstack/react-start/config'
import tsConfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  vite: {
    plugins: [tsConfigPaths({ projects: ['./tsconfig.json'] })],
  },
})
```

## BetterAuth Integration

```ts
// Server function for session
import { createServerFn } from '@tanstack/react-start'
import { getRequestHeaders } from '@tanstack/react-start/server'
import { auth } from '@/lib/auth'

export const getSessionFn = createServerFn({ method: 'GET' }).handler(
  async () => {
    const headers = getRequestHeaders()
    return auth.api.getSession({ headers })
  }
)

// Protected layout route
export const Route = createFileRoute('/_authed')({
  beforeLoad: async () => {
    const session = await getSessionFn()
    if (!session?.user) throw redirect({ to: '/sign-in' })
  },
  component: () => <Outlet />,
})
```

## Deployment

TanStack Start deploys to any Node/Bun target, Vercel, Cloudflare Workers, Netlify.

### Vercel (Critical)

**You MUST add the `nitro()` Vite plugin** — without it, Vercel builds succeed but serve 404s.

```ts
// vite.config.ts
import { nitro } from 'nitro/vite'

export default defineConfig({
  plugins: [
    tanstackStart(),
    nitro(),        // ← REQUIRED for Vercel
    viteReact(),
  ],
})
```

Install: `pnpm add nitro`

**Monorepo (pnpm + Turborepo) quirks:**
- Set `rootDirectory` in Vercel project settings to the app dir (e.g., `apps/gremlin-cms`)
- Framework preset should be **TanStack Start** or auto-detect — never Next.js
- Do NOT manually set `outputDirectory` — Nitro generates `.vercel/output` automatically
- Build command from repo root: `turbo run build --filter=<app-name>` or let Vercel auto-detect
- If you get 404 after successful build, check: (1) nitro plugin present, (2) framework preset correct, (3) no stale `.vercel` config

**No CLI deploys** — push to git, let Vercel auto-deploy. Only use `vercel --prod` for emergency hotfixes.

## Rules

1. **Never access `process.env` in loaders directly** — use `createServerFn` or `createServerOnlyFn`
2. **Loaders are isomorphic** — they run on both server AND client during navigation
3. **Server functions are the boundary** — anything that touches DB, env vars, or secrets goes through `createServerFn`
4. **Prefer server functions over API routes** for internal data access — type-safe, no manual fetch
5. **Use `useServerFn()` hook** when calling server functions from components (not direct calls)
6. **Middleware composes** — stack auth, validation, logging as reusable middleware

## Living Document

This skill will grow as we build gremlin-cms. Update with patterns discovered during development.
