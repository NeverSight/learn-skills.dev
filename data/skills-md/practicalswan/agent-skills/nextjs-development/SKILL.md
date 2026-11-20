---
name: nextjs-development
version: "2.0"
last_updated: 2026-09-08
tags: [nextjs, development, testing, quality, automation]
description: "Next.js 16.2.4 with TypeScript — App Router, Server Components, use cache directive, Turbopack dev, Server Actions, ISR, SSR, SSG, MCP devtools, metadata API, route handlers, instrumentation."
---
# Next.js Development

> Optimized for Next.js 16+, React 19+, TypeScript 5.5+, Turbopack, and App Router-first architectures.

Comprehensive reference for [Next.js](https://nextjs.org/docs) (latest: **16.2.4**) with the App Router, TypeScript, and modern patterns. Covers project structure, Server/Client Components, data fetching, caching with the `use cache` directive, Server Actions, MCP devtools integration, and performance optimization.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Component Review Rubric Reference

Apply the shared [Component Review Rubric](../frontend-design/SKILL.md#component-review-rubric) before approving Next.js components, then run the Next.js-specific checks below.

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/nextjs-development` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Next.js MCP

- Fallback prompt: "Use the Next.js Development skill without MCP. Follow the documented local or manual fallback, show the selected tool surface, and report the verification evidence."
- Use `next dev`, `next build`, `next lint`, browser console output, and local server logs when live MCP diagnostics are unavailable.
- Verify routing, rendering mode, and data-fetching behavior with the bundled examples and a running dev server.
- Do not claim an MCP operation was used when the active host does not expose it.

<!-- MCP:END -->

## Anti-Patterns

- Mixing server and client responsibilities: Bundle size, caching, and auth decisions become harder to reason about.
- Using legacy synchronous request APIs: Modern Next.js expects async request surfaces such as `params`, `headers()`, and `cookies()`.
- Skipping route-level loading and error states: Streaming apps feel broken when only the happy path is implemented.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Nextjs Development guidance is tied to a concrete route, component, screen, or design artifact.
2. Pass/fail: Component states cover loading, empty, error, success, and responsive breakpoints where applicable.
3. Pass/fail: Accessibility, visual hierarchy, and interaction behavior are reviewed against the shared component rubric.
4. Pressure-test scenario: Review the component on a narrow mobile viewport, keyboard-only path, and slow-loading state.
5. Success metric: Zero generic UI approval; every approval cites rendered behavior or source evidence.

## Before and After Example

```typescript
// Before
export default function ProductPage({ params }: { params: { id: string } }) {
  const [product, setProduct] = useState<Product | null>(null);
  useEffect(() => {
    fetch(`/api/products/${params.id}`).then((r) => r.json()).then(setProduct);
  }, [params.id]);
  return product ? <ProductView product={product} /> : <Spinner />;
}

// After
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  const product = await getProduct(id);
  return <ProductView product={product} />;
}
```

Moves data fetching into the server component and follows the async request API used in current Next.js releases.

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

### App Router & Routing
- Creating or modifying `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`
- Working with dynamic routes `[slug]`, catch-all `[...slug]`, optional catch-all `[[...slug]]`
- Parallel routes `@slot`, intercepting routes, route groups `(group)`
- New v15/v16 file conventions: `forbidden.tsx`, `proxy.ts`, `template.tsx`, `unauthorized.tsx`

### Server & Client Components
- Deciding when to use `"use client"` or `"use server"` directives
- Component boundary questions, RSC + RCC composition patterns
- Passing Server Components as children/props to Client Components
- `taint` API for data security

### Data Fetching & Caching
- Using `use cache` directive (replaces `cache: 'force-cache'`)
- `cacheTag()`, `cacheLife()`, `revalidateTag()`, `revalidatePath()`
- Async Request APIs: `await cookies()`, `await headers()`, `await params`, `await searchParams`
- `after()` for post-response work, `connection()` for dynamic rendering

### Server Actions & Forms
- `"use server"` in functions or module scope
- `<Form>` component with client-side navigation
- Form validation, optimistic updates, error handling
- `after()` for side-effects after action completes

### Performance & Turbopack
- `next dev` with Turbopack (default in v15+, stable)
- Image optimization with `next/image`
- Font subsetting with `next/font`
- Lazy loading, bundle optimization, `serverComponentsHmrCache`

### Next.js MCP Dev Tools
- Querying live errors, logs, routes from the running dev server
- Using `next-devtools-mcp` with coding agents (requires Next.js 16+)
- Upgrading to Next.js 16 with codemods
- Enabling Cache Components feature

---

## Part 1: Project Setup & Config

### Creating a New Project

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
```

### TypeScript Config (`next.config.ts`)

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactCompiler: true,          // stable in v16
  reactStrictMode: true,
  serverExternalPackages: ['sharp'],  // renamed from serverComponentsExternalPackages in v15
  experimental: {
    turbopackFileSystemCache: true,   // persist Turbopack cache across restarts
    serverComponentsHmrCache: true,   // cache fetch responses during HMR
  },
  cacheLife: {                        // custom cache profiles
    frequent: { stale: 60, revalidate: 60, expire: 3600 },
    daily: { stale: 3600, revalidate: 3600, expire: 86400 },
  },
}

export default nextConfig
```

### Project Structure

```
my-app/
├── app/
│   ├── layout.tsx          # Root layout (required)
│   ├── page.tsx            # Home page
│   ├── loading.tsx         # Streaming skeleton
│   ├── error.tsx           # Error boundary
│   ├── not-found.tsx       # 404 page
│   ├── forbidden.tsx       # 403 page (v16)
│   ├── unauthorized.tsx    # 401 page (v16)
│   ├── (marketing)/        # Route group (no URL segment)
│   │   └── about/page.tsx
│   ├── blog/
│   │   └── [slug]/page.tsx # Dynamic route
│   └── api/
│       └── route.ts        # Route Handler
├── components/             # Shared RSC/RCC components
├── lib/                    # Server utilities
├── public/                 # Static assets
├── next.config.ts          # TypeScript config (v15+)
├── .mcp.json               # MCP server config (v16)
└── instrumentation.ts      # Server lifecycle hooks (stable v15)
```

---

## Part 2: App Router Routing

### File Conventions

| File | Purpose |
|------|---------|
| `page.tsx` | UI for the route segment, makes it publicly accessible |
| `layout.tsx` | Shared UI that persists across navigations |
| `template.tsx` | Like layout, but remounts on navigation |
| `loading.tsx` | Suspense skeleton; shown while page loads |
| `error.tsx` | Isolate errors; `"use client"` required |
| `not-found.tsx` | Rendered by `notFound()` or 404 |
| `forbidden.tsx` | Rendered by `forbidden()` (v16) |
| `unauthorized.tsx` | Rendered by `unauthorized()` (v16) |
| `route.ts` | API endpoint (cannot coexist with page.tsx at same level) |
| `proxy.ts` | Lightweight HTTP proxy (v16) |
| `middleware.ts` | Runs before request completes (project root) |
| `instrumentation.ts` | Server lifecycle, OpenTelemetry (stable v15) |
| `instrumentation-client.ts` | Client-side performance monitoring (v16) |

### Dynamic Routes

```typescript
// app/blog/[slug]/page.tsx
// IMPORTANT: params is now async in Next.js 15+
export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params  // must await in v15+
  return <h1>{slug}</h1>
}

// Generate static paths
export async function generateStaticParams() {
  const posts = await fetchPosts()
  return posts.map((post) => ({ slug: post.slug }))
}
```

### Route Groups & Parallel Routes

```
app/
├── (auth)/                 # Route group: no URL impact
│   ├── login/page.tsx      # /login
│   └── register/page.tsx   # /register
├── @modal/                 # Parallel route (slot)
│   └── photo/[id]/page.tsx
├── layout.tsx              # Receives { children, modal } props
└── page.tsx
```

### Intercepting Routes

```
app/
├── photos/[id]/page.tsx    # Full page: /photos/123
└── @modal/
    └── (.)photos/[id]/     # Intercept same-level route
        └── page.tsx        # Renders as modal without full navigation
```

### searchParams (async in v15+)

```typescript
// app/search/page.tsx
export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q: string; page: string }>
}) {
  const { q, page } = await searchParams  // must await in v15+
  return <Results query={q} page={Number(page)} />
}
```

---

## Part 3: Server & Client Components

### Decision Tree

```
Does the component need:
  - onClick, onChange, event handlers?    → "use client"
  - useState, useEffect, useReducer?      → "use client"
  - Browser-only APIs (window, localStorage)?  → "use client"
  - useRouter, useParams, useSearchParams?     → "use client"
  
Otherwise:
  - Direct DB/API access without extra fetch?  → Server Component (default)
  - Large dependencies (marked-js, date-fns)?  → Server Component (not in JS bundle)
  - Access cookies(), headers(), auth tokens?  → Server Component
```

### Component Composition Pattern

```typescript
// ✅ Pass Server Components as children to Client Components
// app/page.tsx (Server Component)
import { ClientWrapper } from '@/components/ClientWrapper'
import { ServerData } from '@/components/ServerData'

export default function Page() {
  return (
    <ClientWrapper>
      <ServerData /> {/* Server Component as child — no "use client" boundary issue */}
    </ClientWrapper>
  )
}

// components/ClientWrapper.tsx
"use client"
import { useState } from 'react'

export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false)
  return <div onClick={() => setOpen(!open)}>{children}</div>
}
```

### Directives Reference

| Directive | Where | Effect |
|-----------|-------|--------|
| `"use client"` | Top of file | All exports are Client Components |
| `"use server"` | Top of file or function | Marks Server Actions; top-of-file applies to all exports |
| `"use cache"` | Top of file or function | Marks a component/function as a Cache Component |
| `"use cache: private"` | Top of file or function | Cache Component, private (user-specific) data |
| `"use cache: remote"` | Top of file or function | Cache Component, persisted remotely |

### Data Security with `taint`

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  experimental: { taint: true }
}

// lib/user.ts (Server)
import { experimental_taintUniqueValue } from 'react'

export async function getUser(id: string) {
  const user = await db.user.findUnique({ where: { id } })
  // Prevent accidental serialization of sensitive fields
  experimental_taintUniqueValue(
    'Do not pass user.passwordHash to Client',
    user,
    user.passwordHash
  )
  return user
}
```

---

## Part 4: Data Fetching & Caching

### The `use cache` Directive (Next.js 15+)

`use cache` replaces the old `cache: 'force-cache'` approach and works at the **file**, **component**, or **function** level.

```typescript
// Cache an entire async function
async function getProducts() {
  'use cache'
  const data = await fetch('https://api.example.com/products')
  return data.json()
}

// Cache a Server Component
async function ProductList() {
  'use cache'
  cacheLife('daily')          // use named profile from next.config.ts
  cacheTag('products')        // tag for targeted revalidation

  const products = await getProducts()
  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>
}
```

### `cacheLife` Profiles

```typescript
// Built-in profiles
cacheLife('seconds')   // stale: 0,  revalidate: 1,    expire: 60
cacheLife('minutes')   // stale: 60, revalidate: 60,   expire: 3600
cacheLife('hours')     // stale: 3600, revalidate: 3600, expire: 86400
cacheLife('days')      // stale: 86400, revalidate: 86400, expire: 604800
cacheLife('weeks')     // stale: 604800, revalidate: 604800, expire: 2592000
cacheLife('max')       // stale: 2592000, revalidate: 2592000, expire: Infinity

// Custom profile (defined in next.config.ts)
cacheLife('frequent')  // stale: 60, revalidate: 60, expire: 3600
```

### Targeted Revalidation with `cacheTag`

```typescript
// app/actions.ts
'use server'
import { revalidateTag } from 'next/cache'

export async function updateProduct(id: string, data: FormData) {
  await db.products.update({ where: { id }, data: Object.fromEntries(data) })
  revalidateTag('products')      // invalidates all cached items with this tag
  revalidateTag(`product-${id}`) // fine-grained invalidation
}

// app/products/[id]/page.tsx
async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  'use cache'
  const { id } = await params
  cacheTag('products', `product-${id}`)
  const product = await db.products.findUnique({ where: { id } })
  return <Product data={product} />
}
```

### `fetch` Cache Behavior (v15+ defaults changed)

```typescript
// GET route handlers are NO LONGER cached by default in v15+
// Explicitly opt-in to caching:
const res = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600, tags: ['products'] }
})

// Force dynamic (never cache):
const res = await fetch('https://api.example.com/data', {
  cache: 'no-store'
})

// ISR — revalidate every N seconds:
export const revalidate = 3600  // segment-level option
```

### Async Request APIs (v15 Breaking Change)

```typescript
import { cookies, headers } from 'next/headers'

// BEFORE (v14): synchronous
const cookieStore = cookies()

// AFTER (v15+): must await
const cookieStore = await cookies()
const headersList = await headers()

// params and searchParams also async in page/layout props
const { slug } = await params
const { q } = await searchParams
```

### `after()` — Post-Response Side Effects

```typescript
import { after } from 'next/server'

export async function GET(request: Request) {
  const data = await fetchData()

  // Fires AFTER response is sent to client
  after(async () => {
    await logAnalyticsEvent('data-fetched', { timestamp: Date.now() })
  })

  return Response.json(data)
}
```

### `connection()` — Force Dynamic Rendering

```typescript
import { connection } from 'next/server'

export default async function Page() {
  // Signals this component requires a live request (opts out of static rendering)
  await connection()
  const realTimeData = await fetchLiveData()
  return <Dashboard data={realTimeData} />
}
```

---

## Part 5: Server Actions & Forms

### Server Actions

```typescript
// app/actions.ts
'use server'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { z } from 'zod'

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
})

export async function createPost(formData: FormData) {
  const parsed = CreatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  })

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors }
  }

  const post = await db.posts.create({ data: parsed.data })
  revalidatePath('/blog')
  redirect(`/blog/${post.id}`)
}
```

### `<Form>` Component (Next.js 15+)

```typescript
import Form from 'next/form'

export default function SearchForm() {
  // <Form> replaces <form> for client-side navigation + prefetching
  return (
    <Form action="/search">
      <input name="q" placeholder="Search..." />
      <button type="submit">Search</button>
    </Form>
  )
}
```

### Optimistic Updates with `useOptimistic`

```typescript
'use client'
import { useOptimistic, useTransition } from 'react'
import { toggleLike } from '@/app/actions'

export function LikeButton({ postId, initialLikes }: Props) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    initialLikes,
    (state, delta: number) => state + delta
  )
  const [isPending, startTransition] = useTransition()

  return (
    <button
      onClick={() => startTransition(async () => {
        addOptimisticLike(1)
        await toggleLike(postId)
      })}
      disabled={isPending}
    >
      {optimisticLikes} Likes
    </button>
  )
}
```

---

## Part 6: Next.js MCP Dev Tools

The `next-devtools-mcp` package enables coding agents to connect to the live Next.js development server. Requires **Next.js 16+**.

### Setup

```json
// .mcp.json (project root)
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

Next.js 16+ includes a built-in MCP endpoint at `/_next/mcp` in the development server. `next-devtools-mcp` automatically discovers and connects to running instances — even across multiple ports.

### Available MCP Tools

| Tool | What It Does |
|------|-------------|
| `get_errors` | Retrieve current build, runtime, and type errors from the dev server |
| `get_logs` | Get the path to the dev log file (browser console + server output) |
| `get_page_metadata` | Get metadata about specific pages: routes, components, rendering type |
| `get_project_metadata` | Retrieve project structure, `next.config`, and dev server URL |
| `get_server_action_by_id` | Look up Server Actions by ID to find source file and function name |
| `nextjs_docs` | Query comprehensive Next.js documentation and best practices |
| `nextjs_runtime` | Interact with the running Next.js instance |
| `upgrade_nextjs_16` | Automated upgrade guide to Next.js 16 with codemods |
| `enable_cache_components` | Setup and configuration guide for Cache Components |

### Usage Patterns

```
# Ask the agent about runtime state
"What errors are currently in my application?"
→ Agent calls get_errors → analyzes build/type/runtime errors → suggests fixes

# Debug a specific route
"Why is /dashboard rendering statically instead of dynamically?"
→ Agent calls get_page_metadata with route=/dashboard → shows rendering config

# Navigate the codebase
"What Server Actions exist in this app?"
→ Agent calls get_project_metadata → then get_server_action_by_id for each action

# Upgrade workflow
"Help me upgrade to Next.js 16"
→ Agent calls upgrade_nextjs_16 → runs codemods → handles breaking changes

# Enable new features
"Set up Cache Components for this project"
→ Agent calls enable_cache_components → configures next.config.ts + shows patterns
```

---

## Part 7: Performance & Turbopack

### Turbopack (Default in v15+)

```bash
# Turbopack is now the default — no flag needed
npm run dev           # Uses Turbopack automatically

# Opt back to webpack if needed
npm run dev -- --webpack

# Enable Turbopack filesystem cache (persist across restarts)
# next.config.ts
experimental: { turbopackFileSystemCache: true }
```

**Benchmark vs webpack:** 76.7% faster cold starts, 96.3% faster HMR.

### Image Optimization

```typescript
import Image from 'next/image'

export function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      width={1200}
      height={600}
      priority          // LCP image: preloads synchronously
      sizes="(max-width: 768px) 100vw, 1200px"
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  )
}
```

### Font Optimization

```typescript
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',    // CSS variable for Tailwind
  display: 'swap',
})

// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  )
}
```

### React Compiler

```typescript
// next.config.ts — stable in v16
const nextConfig: NextConfig = {
  reactCompiler: true,  // eliminates manual useMemo/useCallback
}
```

### Bundle Optimization

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  // Avoid importing entire icon libraries
  // next/font handles subsetting automatically
  bundlePagesRouterDependencies: true,  // renamed from bundlePagesExternals in v15
  experimental: {
    optimizePackageImports: ['lucide-react', '@heroicons/react'],
  },
}
```

---

## Part 8: Metadata & SEO

### Static Metadata

```typescript
// app/layout.tsx or app/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: {
    template: '%s | My App',
    default: 'My App',
  },
  description: 'App description for SEO',
  openGraph: {
    type: 'website',
    url: 'https://example.com',
    images: [{ url: '/og-image.jpg', width: 1200, height: 630 }],
  },
  robots: { index: true, follow: true },
  metadataBase: new URL('https://example.com'),
}
```

### Dynamic Metadata

```typescript
// app/blog/[slug]/page.tsx
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params  // async in v15+
  const post = await getPost(slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      images: [{ url: post.cover, width: 1200, height: 630 }],
    },
  }
}
```

---

## Part 9: Route Handlers & Middleware

### Route Handlers (Uncached by Default in v15+)

```typescript
// app/api/products/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { after } from 'next/server'

// GET is NO LONGER cached by default in v15+
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const category = searchParams.get('category')

  const products = await db.products.findMany({
    where: category ? { category } : undefined,
  })

  // Side effect after response
  after(() => logRequest(request.url))

  return NextResponse.json(products)
}

// Opt-in to caching for a route segment
export const revalidate = 3600  // revalidate every hour
export const dynamic = 'force-static'  // always static
```

### Middleware

```typescript
// middleware.ts (project root)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
}
```

---

## Part 10: Instrumentation

### Server-Side Lifecycle (`instrumentation.ts`)

```typescript
// instrumentation.ts (stable in v15)
export async function register() {
  // Runs once when the server starts (Node.js + Edge)
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    // Initialize OpenTelemetry, Sentry, etc.
    const { initTracing } = await import('./lib/tracing')
    await initTracing()
  }
}

export async function onRequestError(
  error: Error,
  request: { path: string; method: string },
  context: { routeType: string }
) {
  // Centralized error reporting
  await reportError(error, { path: request.path })
}
```

### Client-Side Instrumentation (`instrumentation-client.ts`)

```typescript
// instrumentation-client.ts (v16)
export function onRouteChange({ path }: { path: string }) {
  // Track route changes for analytics
  analytics.track('page_view', { path })
}

export function onCaughtError(error: Error) {
  // Capture client-side errors
  Sentry.captureException(error)
}
```

---

## Part 11: Auth Interrupts (v16)

```typescript
// middleware.ts or Server Component
import { forbidden, unauthorized } from 'next/navigation'

export default async function AdminPage() {
  const session = await getSession()

  if (!session) {
    unauthorized()  // renders unauthorized.tsx
  }

  if (!session.user.isAdmin) {
    forbidden()     // renders forbidden.tsx
  }

  return <AdminDashboard />
}
```

---

## Part 12: Upgrading to v15/v16

### Automated Codemods

```bash
# Upgrade to v15 (handles async Request APIs automatically)
npx @next/codemod@latest upgrade

# Or upgrade to v16 specifically
npx @next/codemod@latest upgrade next@16

# Available codemods
npx @next/codemod@latest next-async-request-api .
npx @next/codemod@latest next-og-import .
```

### Key v15 Breaking Changes

| Change | Before (v14) | After (v15+) |
|--------|-------------|-------------|
| `cookies()` | sync | `await cookies()` |
| `headers()` | sync | `await headers()` |
| `params` | sync | `await params` |
| `searchParams` | sync | `await searchParams` |
| GET Route Handlers | cached by default | **not cached** by default |
| Client Router Cache | cached segments | **not cached** by default |
| `serverComponentsExternalPackages` | old name | `serverExternalPackages` |
| `bundlePagesExternals` | old name | `bundlePagesRouterDependencies` |

---

## Modern Component and Testing Examples

### Server Components
```tsx
export default async function DashboardPage() {
  const metrics = await getDashboardMetrics();
  return <Dashboard metrics={metrics} />;
}
```

### Error Boundaries
```tsx
// app/dashboard/error.tsx
'use client';

export default function Error({ reset }: { reset: () => void }) {
  return <button onClick={reset}>Retry dashboard</button>;
}
```

### Accessibility Testing Tools
```ts
import AxeBuilder from '@axe-core/playwright';

test('dashboard has no critical accessibility issues', async ({ page }) => {
  await page.goto('/dashboard');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

## Common Pitfalls

- Mixing server and client responsibilities: It bloats bundles and makes caching or auth decisions harder to reason about.
- Using old synchronous request APIs: Current Next.js releases expect async `params`, `searchParams`, `cookies()`, and `headers()`.
- Skipping error and loading states: Streaming routes feel broken when only the happy path is modeled.

## Related Skills

- [react-development](../react-development/SKILL.md): Use it when the workflow also needs React component architecture and client or server boundaries.
- [javascript-development](../javascript-development/SKILL.md): Use it when the workflow also needs modern JavaScript and TypeScript application code.
- [web-testing](../web-testing/SKILL.md): Use it when the workflow also needs browser and end-to-end testing evidence.
- [devops-tooling](../devops-tooling/SKILL.md): Use it when the workflow also needs git, CI, and automation workflows.
