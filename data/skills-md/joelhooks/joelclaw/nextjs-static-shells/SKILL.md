---
name: nextjs-static-shells
displayName: Next.js Static Shells
description: "Static-first Next.js 16 architecture patterns: cached shells with dynamic slots, provider islands, 'use cache' boundaries, and link preloading strategy. Use when building or refactoring Next.js routes to maximize static rendering, implementing 'use cache' with dynamic personalization, splitting entry vs static renderers, scoping client providers, or tuning prefetch behavior. Triggers on 'static shell', 'use cache pattern', 'dynamic slots', 'provider island', 'prefetch strategy', 'static first', 'cache boundary', 'route goes dynamic unexpectedly', or any Next.js architecture work involving mixed static/dynamic rendering."
version: 1.0.0
author: Joel Hooks
tags: [nextjs, architecture, caching, performance, rsc, static]
---

# Static-First Next.js 16 Patterns

Build a **static shell first**, then cut **small dynamic holes** where personalization or request-specific behavior is required.

- Static shell = deterministic, cacheable, fast first paint
- Dynamic holes = isolated request/user behavior streamed with Suspense
- Client interactivity = provider islands, not global client sprawl

---

## Route Architecture: Entry + Static + Slots

### Pattern

1. **Entry component (server, request-aware)**
   - Reads params/search/auth/session/cookies
   - Validates access, resolves IDs, prepares dynamic props
2. **Static renderer (server, `'use cache'`)**
   - Renders deterministic layout/content
   - Accepts dynamic UI as slot props (`ReactNode`)
3. **Dynamic slots**
   - Injected from entry component
   - Suspense-wrapped where rendered in static shell

### Why This Works

- Static shell stays cacheable
- Dynamic behavior is explicit and narrow
- Streaming keeps UI responsive
- No accidental full-route dynamic bailout

```tsx
import { Suspense, type ReactNode } from 'react';

type PageProps = { params: Promise<{ slug: string }> };

/** Request-aware server entry. */
export default async function PageEntry({ params }: PageProps) {
  const { slug } = await params;

  const staticData = await getStaticData(slug); // deterministic
  const userData = await getUserData(); // request-dependent

  const dynamicPanel = <PersonalizedPanel userData={userData} />;

  return <PageStatic data={staticData} panel={dynamicPanel} />;
}

type PageStaticProps = {
  data: StaticData;
  panel?: ReactNode;
};

/** Cached static shell. Keep request-volatile reads out. */
async function PageStatic({ data, panel }: PageStaticProps) {
  'use cache';

  return (
    <main>
      <Hero data={data.hero} />
      <Content data={data.content} />
      <Suspense fallback={<PanelSkeleton />}>{panel}</Suspense>
    </main>
  );
}
```

---

## Cache Components Setup & Mechanics

### Enable

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

Replaces the old `experimental.ppr` flag.

### Three Content Types

| Type | Characteristic | Example |
|------|---------------|---------|
| **Static** | Synchronous, pure computation | `<header><h1>Our Blog</h1></header>` |
| **Cached** (`'use cache'`) | Async but deterministic for given inputs | `db.posts.findMany()` with `cacheLife('hours')` |
| **Dynamic** (Suspense) | Runtime/request-specific, must be fresh | `cookies()`, user session, notifications |

### `'use cache'` Scope Levels

```tsx
// File level — entire module cached
'use cache'
export default async function Page() { /* ... */ }

// Component level
export async function CachedComponent() {
  'use cache'
  const data = await fetchData()
  return <div>{data}</div>
}

// Function level
export async function getData() {
  'use cache'
  return db.query('SELECT * FROM posts')
}
```

### Cache Profiles with `cacheLife()`

```tsx
import { cacheLife } from 'next/cache'

async function getData() {
  'use cache'
  cacheLife('hours')  // Built-in: 'default' | 'minutes' | 'hours' | 'days' | 'weeks' | 'max'
  return fetch('/api/data')
}

// Or inline config:
async function getDataCustom() {
  'use cache'
  cacheLife({
    stale: 3600,      // 1h — serve stale while revalidating
    revalidate: 7200, // 2h — background revalidation interval
    expire: 86400,    // 1d — hard expiration
  })
  return fetch('/api/data')
}
```

Built-in profile shortcuts: `'use cache'` alone → 5m stale / 15m revalidate. `'use cache: remote'` → platform KV. `'use cache: private'` → allows runtime APIs (compliance escape hatch).

### Cache Invalidation

```tsx
import { cacheTag } from 'next/cache'

async function getProduct(id: string) {
  'use cache'
  cacheTag('products', `product-${id}`)
  return db.products.findUnique({ where: { id } })
}
```

**`updateTag()`** — immediate, same-request invalidation:
```tsx
'use server'
import { updateTag } from 'next/cache'

export async function updateProduct(id: string, data: FormData) {
  await db.products.update({ where: { id }, data })
  updateTag(`product-${id}`)  // caller sees fresh data
}
```

**`revalidateTag()`** — background stale-while-revalidate:
```tsx
'use server'
import { revalidateTag } from 'next/cache'

export async function createPost(data: FormData) {
  await db.posts.create({ data })
  revalidateTag('posts')  // next request sees fresh data
}
```

### Cache Key Generation (Automatic)

Keys derived from: build ID + function location hash + serializable arguments + closure variables. No manual `keyParts` like `unstable_cache`.

```tsx
async function Component({ userId }: { userId: string }) {
  const getData = async (filter: string) => {
    'use cache'
    // cache key = userId (closure) + filter (argument)
    return fetch(`/api/users/${userId}?filter=${filter}`)
  }
  return getData('active')
}
```

---

## What Cannot Live Inside `'use cache'`

**Hard rule:** No per-request volatility inside cached boundaries.

| Banned inside `'use cache'` | Why |
|---|---|
| `cookies()`, `headers()` | Request-specific |
| `searchParams` | Request-specific |
| Session/auth reads | User-specific |
| Hidden user logic in helper calls | Invisible request dependency |
| Side effects tied to request lifecycle | Non-deterministic |
| `Math.random()`, `Date.now()` | Execute once at build time inside cache |

### Fix: Extract Outside, Pass as Arguments

```tsx
// Wrong — runtime API inside 'use cache'
async function CachedProfile() {
  'use cache'
  const session = (await cookies()).get('session')?.value  // Error!
  return <div>{session}</div>
}

// Correct — extract in entry, pass as prop
async function ProfilePage() {
  const session = (await cookies()).get('session')?.value
  return <CachedProfile sessionId={session} />
}

async function CachedProfile({ sessionId }: { sessionId: string }) {
  'use cache'
  // sessionId becomes part of cache key automatically
  const data = await fetchUserData(sessionId)
  return <div>{data.name}</div>
}
```

Exception: `'use cache: private'` allows `cookies()` / `headers()` for compliance cases where refactoring is impractical.

---

## RSC Boundary Rules

These interact directly with the static shell pattern.

### Async Client Components Are Invalid

Client components **cannot** be async. Only Server Components can be async.

```tsx
// Bad
'use client'
export default async function UserProfile() {
  const user = await getUser()  // Cannot await in client
  return <div>{user.name}</div>
}

// Good — fetch in server entry, pass data down
// page.tsx (server)
export default async function Page() {
  const user = await getUser()
  return <UserProfile user={user} />
}

// UserProfile.tsx (client)
'use client'
export function UserProfile({ user }: { user: User }) {
  return <div>{user.name}</div>
}
```

### Non-Serializable Props Kill the Boundary

Props from Server → Client must be JSON-serializable.

| Cannot pass | Fix |
|---|---|
| Functions (except Server Actions) | Define inside client component |
| `Date` objects | `.toISOString()` on server |
| `Map`, `Set` | `Object.fromEntries()` / `Array.from()` |
| Class instances | Pass plain object |

Server Actions (`'use server'`) **can** be passed to client components — they're the exception.

---

## Async Patterns (Next.js 15+)

`params`, `searchParams`, `cookies()`, `headers()` are all async. Type them as `Promise<...>` and `await` in the entry component.

```tsx
type PageProps = {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ query?: string }>
}

export default async function Page({ params, searchParams }: PageProps) {
  const { slug } = await params
  const { query } = await searchParams
  // ...
}
```

For synchronous client components that need params, use `React.use()`:

```tsx
import { use } from 'react'

export default function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params)
}
```

---

## Suspense Boundary Requirements

### `useSearchParams` Always Needs Suspense

Without Suspense, the entire page becomes CSR:

```tsx
// Bad — entire page CSR bailout
'use client'
import { useSearchParams } from 'next/navigation'
export default function SearchBar() {
  const searchParams = useSearchParams()
  return <div>Query: {searchParams.get('q')}</div>
}

// Good — isolated in Suspense
import { Suspense } from 'react'
export default function Page() {
  return (
    <Suspense fallback={<SearchSkeleton />}>
      <SearchBar />
    </Suspense>
  )
}
```

### Quick Reference

| Hook | Suspense Required |
|------|-------------------|
| `useSearchParams()` | Always |
| `usePathname()` | Yes in dynamic routes |
| `useParams()` | No |
| `useRouter()` | No |

---

## Provider Islands (Client Providers Done Cleanly)

### Rule

Mount client providers **as low as possible** and only where interactivity is needed.

- Good: feature-level provider island
- Bad: global root provider for local feature state

### Pattern

Server entry passes typed initial state. Client provider resolves inside `'use client'` boundary. Hooks stay inside island.

```tsx
'use client';

import { createContext, useContext, useMemo } from 'react';

type FeatureState = { enabled: boolean };
type FeatureContextValue = { state: FeatureState };

const FeatureContext = createContext<FeatureContextValue | null>(null);

export function FeatureProvider({
  children,
  initialState,
}: {
  children: React.ReactNode;
  initialState: FeatureState;
}) {
  const value = useMemo(() => ({ state: initialState }), [initialState]);
  return <FeatureContext.Provider value={value}>{children}</FeatureContext.Provider>;
}

export function useFeature() {
  const ctx = useContext(FeatureContext);
  if (!ctx) throw new Error('useFeature must be used within FeatureProvider');
  return ctx;
}
```

---

## Data Fetching in the Static Shell Model

### Decision Tree

| Need | Pattern |
|------|---------|
| Read data in server component | Fetch directly — no API layer |
| Mutation from UI | Server Action (`'use server'`) |
| External API / webhook / mobile client | Route Handler |
| Client component needs data | Pass from server parent (preferred) or Route Handler |

### Avoiding Waterfalls

```tsx
// Bad — sequential
const user = await getUser();
const posts = await getPosts();

// Good — parallel
const [user, posts] = await Promise.all([getUser(), getPosts()]);

// Better — streaming with Suspense (each section independent)
<Suspense fallback={<UserSkeleton />}><UserSection /></Suspense>
<Suspense fallback={<PostsSkeleton />}><PostsSection /></Suspense>
```

### Preload Pattern

```tsx
import { cache } from 'react';

export const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } });
});

export const preloadUser = (id: string) => {
  void getUser(id);  // fire-and-forget, deduped by cache()
};
```

---

## Link Preloading Strategy

### Rules

- **Preload static/common routes** aggressively
- **Disable prefetch** for personalized/query-heavy/volatile URLs
- Preload shell, defer user-specific data behind dynamic boundaries
- `generateStaticParams` boosts prefetch hit quality for common paths

```tsx
import Link from 'next/link';

/** Static/common route: keep default prefetch. */
<Link href={`/docs/${slug}`}>Read next</Link>

/** Personalized or volatile route: disable speculative prefetch. */
<Link href={`/certificate/${userId}?name=${encodeURIComponent(name)}`} prefetch={false}>
  View certificate
</Link>
```

### Preload Decision Checklist

- Is route static and frequently visited? → preload
- Is route personalized or volatile? → don't preload
- Is user data deferred behind Suspense/dynamic island? → preload shell only
- Is there measured nav improvement? → keep prefetch; otherwise cut it

---

## Decision Matrix

| Scenario | Pattern |
|---|---|
| Static content + personalized controls | Entry (dynamic) + cached static renderer + slot injection |
| Cacheable deterministic server work | `'use cache'` boundary |
| Pure client interactivity | Local `'use client'` provider island |
| Faster navigation | Targeted prefetch + static params coverage |

---

## Common Failure Modes + Fixes

1. **Whole route goes dynamic unexpectedly**
   - Cause: request-bound reads (`cookies()`, `headers()`) leak into static shell
   - Fix: move those reads to entry component, pass slot props

2. **Client hydration is too heavy**
   - Cause: global provider mounted at root for feature-local state
   - Fix: push provider down to feature/layout segment

3. **Prefetch waste and noisy network**
   - Cause: prefetching personalized/query-heavy links
   - Fix: `prefetch={false}` for volatile URLs

4. **Static shell blocked by dynamic work**
   - Cause: dynamic components rendered without Suspense seams
   - Fix: wrap dynamic slots in Suspense with small fallbacks

5. **Unclear ownership of data flow**
   - Cause: mixed static/dynamic logic in one component
   - Fix: enforce Entry vs Static renderer split with strict prop contracts

6. **`useSearchParams` causes full-page CSR bailout**
   - Cause: missing Suspense boundary around search-param-reading component
   - Fix: always wrap `useSearchParams` consumers in Suspense

7. **Date/Map/class props silently break client components**
   - Cause: non-serializable props passed across RSC→client boundary
   - Fix: serialize on server (`.toISOString()`, `Object.fromEntries()`, plain objects)

8. **`unstable_cache` still in codebase**
   - Cause: pre-v16 caching pattern not migrated
   - Fix: replace with `'use cache'` + `cacheTag()` + `cacheLife()` — no manual key arrays needed

---

## Migration from Previous Versions

| Old Config | Replacement |
|---|---|
| `experimental.ppr` | `cacheComponents: true` |
| `dynamic = 'force-dynamic'` | Remove (default behavior) |
| `dynamic = 'force-static'` | `'use cache'` + `cacheLife('max')` |
| `revalidate = N` | `cacheLife({ revalidate: N })` |
| `unstable_cache()` | `'use cache'` directive |

### `unstable_cache` → `'use cache'`

```tsx
// Before
const getCachedUser = unstable_cache(
  async (id) => getUser(id),
  ['my-app-user'],
  { tags: ['users'], revalidate: 60 }
)

// After
async function getCachedUser(id: string) {
  'use cache'
  cacheTag('users')
  cacheLife({ revalidate: 60 })
  return getUser(id)
}
```

Key differences: no manual cache keys (auto from args + closures), tags via `cacheTag()`, revalidation via `cacheLife()`.

---

## Limitations

- **Edge runtime not supported** — requires Node.js
- **Static export not supported** — needs server
- **Non-deterministic values** (`Math.random()`, `Date.now()`) execute once at build time inside `'use cache'`

For request-time randomness outside cache:

```tsx
import { connection } from 'next/server'

async function DynamicContent() {
  await connection()  // defer to request time
  const id = crypto.randomUUID()
  return <div>{id}</div>
}
```

---

## Implementation Sequence

1. Identify static vs dynamic inputs per route
2. Split pages into Entry + cached Static renderer
3. Convert personalized bits into typed slots
4. Add Suspense around slot render points
5. Refactor providers into client islands
6. Apply prefetch rules to navigation links
7. Add static params for high-traffic static routes
8. Measure before/after (TTFB, shell paint, nav latency, prefetch traffic)

---

## PR Acceptance Criteria

- [ ] Static shell renders without waiting on user-specific data
- [ ] Cached boundaries contain no request-volatile reads
- [ ] Dynamic UI only appears via explicit slot boundaries
- [ ] Client providers are feature-scoped unless globally justified
- [ ] Personalized/volatile links have prefetch explicitly disabled
- [ ] Navigation to common static routes is preloaded and measurably faster
- [ ] `useSearchParams` consumers wrapped in Suspense
- [ ] No non-serializable props crossing RSC→client boundary
- [ ] No `unstable_cache` — migrated to `'use cache'` directive
