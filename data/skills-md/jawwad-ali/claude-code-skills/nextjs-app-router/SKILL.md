---
name: nextjs-app-router
description: This skill MUST be loaded when ANY file in an app/ directory is being read, reviewed, edited, or created - including page.tsx, layout.tsx, loading.tsx, error.tsx, not-found.tsx, route.ts, template.tsx, default.tsx, or any .tsx/.ts file using App Router patterns. Also use when the user asks to "read a page.tsx", "review a Next.js file", "edit a layout", "create a Next.js page", "add a route", "create a layout", "implement server components", "add client components", "create API routes", "implement server actions", "add loading states", "handle errors in Next.js", "create dynamic routes", "implement parallel routes", "add intercepting routes", or mentions Next.js App Router, React Server Components (RSC), 'use client', 'use server', next/navigation, or app directory patterns.
---

# Next.js App Router Development Guide

This skill provides comprehensive guidance for building Next.js applications using the App Router (app directory).

## Core Concepts

### File-Based Routing

The App Router uses a file-system based router where:
- **Folders** define routes
- **Files** define UI for route segments

Special files:
| File | Purpose |
|------|---------|
| `page.tsx` | Unique UI for a route (makes route publicly accessible) |
| `layout.tsx` | Shared UI for a segment and its children |
| `loading.tsx` | Loading UI (uses React Suspense) |
| `error.tsx` | Error UI (uses React Error Boundary) |
| `not-found.tsx` | Not found UI |
| `route.ts` | API endpoint (Route Handler) |
| `template.tsx` | Re-rendered layout |
| `default.tsx` | Fallback for parallel routes |

### Server Components vs Client Components

**Server Components (Default)**
- All components in `app/` are Server Components by default
- Can directly access backend resources (database, file system)
- Can use `async/await` at component level
- Cannot use hooks, browser APIs, or event handlers

**Client Components**
- Add `'use client'` directive at the top of the file
- Required for interactivity, hooks, browser APIs
- Should be pushed down the component tree

```tsx
// Server Component (default)
export default async function Page() {
  const data = await fetchData() // Direct data fetching
  return <div>{data.title}</div>
}
```

```tsx
'use client'

// Client Component
import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### Data Fetching Patterns

**In Server Components (Recommended)**
```tsx
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'force-cache', // default - caches indefinitely
    // cache: 'no-store', // never cache
    // next: { revalidate: 3600 }, // revalidate every hour
  })
  return res.json()
}

export default async function Page() {
  const data = await getData()
  return <main>{data.content}</main>
}
```

**Server Actions (for mutations)**
```tsx
// app/actions.ts
'use server'

export async function createItem(formData: FormData) {
  const name = formData.get('name')
  await db.items.create({ data: { name } })
  revalidatePath('/items')
}
```

### Routing Hooks (Client Components Only)

Import from `next/navigation`:
```tsx
'use client'

import { useRouter, usePathname, useSearchParams, useParams } from 'next/navigation'

export function Navigation() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const params = useParams()

  // router.push('/dashboard')
  // router.replace('/login')
  // router.refresh()
  // router.back()
  // router.forward()
}
```

### Dynamic Routes

```
app/
├── blog/
│   └── [slug]/           # Dynamic segment
│       └── page.tsx
├── shop/
│   └── [...slug]/        # Catch-all segment
│       └── page.tsx
└── docs/
    └── [[...slug]]/      # Optional catch-all
        └── page.tsx
```

```tsx
// app/blog/[slug]/page.tsx
export default async function Page({
  params
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return <article>Post: {slug}</article>
}

// Generate static paths
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((post) => ({ slug: post.slug }))
}
```

### Layouts and Templates

**Root Layout (Required)**
```tsx
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

**Nested Layouts**
```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <section>
      <nav>Dashboard Nav</nav>
      {children}
    </section>
  )
}
```

### Loading and Error States

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <div>Loading...</div>
}

// app/dashboard/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

### Route Handlers (API Routes)

```tsx
// app/api/items/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('query')

  const items = await getItems(query)
  return NextResponse.json(items)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const item = await createItem(body)
  return NextResponse.json(item, { status: 201 })
}
```

### Metadata

```tsx
// Static metadata
export const metadata = {
  title: 'My Page',
  description: 'Page description',
}

// Dynamic metadata
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug)
  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

## Best Practices

1. **Keep Client Components small** - Push `'use client'` as far down the tree as possible
2. **Colocate data fetching** - Fetch data in Server Components close to where it's used
3. **Use Server Actions** for mutations instead of API routes when possible
4. **Leverage caching** - Use appropriate fetch cache options
5. **Handle loading/error states** - Always provide loading.tsx and error.tsx
6. **Use route groups** `(folder)` for organization without affecting URL
7. **Implement parallel routes** `@folder` for complex layouts
8. **Use intercepting routes** `(.)folder` for modals

## Common Patterns

See the `references/` directory for detailed patterns:
- `routing.md` - Advanced routing patterns
- `server-components.md` - Server component patterns
- `data-fetching.md` - Data fetching strategies

See the `examples/` directory for working code:
- `page-layout.tsx` - Page and layout examples
- `server-action.ts` - Server action examples
- `route-handler.ts` - API route examples
