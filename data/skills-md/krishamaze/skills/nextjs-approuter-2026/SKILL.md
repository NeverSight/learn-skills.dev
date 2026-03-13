---
name: nextjs-approuter-2026
description: >
  Next.js App Router patterns for 2026 (Next.js 15+/16+). Use this skill when building
  the web dashboard frontend — layouts, server components, client components, route handlers,
  server actions, and data fetching. NEVER use Pages Router, getServerSideProps, or
  getStaticProps. ALWAYS default to Server Components unless interactivity is needed.
  Covers the 'use client'/'use server' boundary, fetch caching, and Tailwind v4.
---

# Next.js App Router 2026

## Version (2026)
- Next.js: `15.x` (stable) / `16.x` (latest with Cache Components, PPR)
- React: `19.x` — Server Components stable
- Tailwind: `v4`
- TypeScript: required

```bash
npx create-next-app@latest dashboard --typescript --tailwind --app --src-dir
```

## App Router — Core Mental Model
```
app/
├── layout.tsx          # Root layout (required — wraps all pages)
├── page.tsx            # Home page
├── (auth)/             # Route group — no URL segment
│   └── login/
│       └── page.tsx
├── dashboard/
│   ├── layout.tsx      # Nested layout (dashboard shell)
│   ├── page.tsx        # /dashboard
│   └── feed/
│       └── page.tsx    # /dashboard/feed
└── api/
    └── browser/
        └── route.ts    # Route handler (replaces pages/api/)
```

**Rule: Folders = routes. Files = behavior.**
- `page.tsx` — renders the route
- `layout.tsx` — persistent wrapper, doesn't re-render on child navigation
- `loading.tsx` — Suspense fallback while data loads
- `error.tsx` — error boundary
- `route.ts` — API endpoint (GET, POST, etc.)

## Server vs Client Components

### Server Components (default in 2026)
- Run on server. Zero JS sent to client.
- Can `async/await` directly — no useEffect, no useState
- Can access secrets, DB, filesystem
- Cannot: use hooks, event handlers, browser APIs

```tsx
// app/dashboard/feed/page.tsx — Server Component by default
export default async function FeedPage() {
    // Direct async data fetch — no useEffect needed
    const feed = await fetch("http://api:8000/browser/feed", {
        cache: "no-store",  // always fresh (dynamic route)
    }).then(r => r.json())

    return (
        <div>
            {feed.map((post: any) => (
                <PostCard key={post.id} post={post} />
            ))}
        </div>
    )
}
```

### Client Components
```tsx
// 'use client' MUST be first line
"use client"

import { useState } from "react"

export function ApproveButton({ draftId }: { draftId: string }) {
    const [loading, setLoading] = useState(false)

    async function approve() {
        setLoading(true)
        await fetch(`/api/browser/approve/${draftId}`, { method: "POST" })
        setLoading(false)
    }

    return (
        <button onClick={approve} disabled={loading}>
            {loading ? "Posting..." : "Approve"}
        </button>
    )
}
```

**Pattern: Server component renders the page, imports client components for interactive islands.**

## Fetch Caching (2026 — Explicit)
```tsx
// Always fresh — for live data
const data = await fetch(url, { cache: "no-store" })

// Cached with revalidation every 60s — for semi-static
const data = await fetch(url, { next: { revalidate: 60 } })

// Fully static — for config/reference data
const data = await fetch(url)  // default: cached
```

## Route Handlers (API endpoints)
```ts
// app/api/browser/approve/[id]/route.ts
import { NextRequest, NextResponse } from "next/server"

export async function POST(
    req: NextRequest,
    { params }: { params: { id: string } }
) {
    const res = await fetch(`http://api:8000/browser/approve/${params.id}`, {
        method: "POST",
    })
    const data = await res.json()
    return NextResponse.json(data)
}
```

## Server Actions (form + mutation without API route)
```tsx
// app/dashboard/compose/page.tsx
export default function ComposePage() {
    async function createDraft(formData: FormData) {
        "use server"   // marks this function as server action
        const content = formData.get("content") as string
        await fetch("http://api:8000/drafts", {
            method: "POST",
            body: JSON.stringify({ content }),
            headers: { "Content-Type": "application/json" },
        })
    }

    return (
        <form action={createDraft}>
            <textarea name="content" placeholder="What's on your mind?" />
            <button type="submit">Save Draft</button>
        </form>
    )
}
```

## Layouts (Persistent Shell)
```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex h-screen">
            <nav className="w-64 bg-gray-900">
                {/* Sidebar — never re-renders between dashboard pages */}
            </nav>
            <main className="flex-1 overflow-auto">
                {children}
            </main>
        </div>
    )
}
```

## Tailwind v4 (2026)
```bash
# v4 is CSS-first — no tailwind.config.js needed for basic use
uv add --dev @tailwindcss/vite  # or use Next.js built-in support
```

Key v4 changes vs v3:
- Config in CSS `@theme` block, not `tailwind.config.js`
- Automatic content detection (no `content: []` array needed)
- `@import "tailwindcss"` replaces `@tailwind base/components/utilities`

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
    --color-brand: #6366f1;
    --font-sans: "Inter", sans-serif;
}
```

## Environment Variables
```bash
# .env.local (server-only, never sent to client)
API_URL=http://api:8000

# .env.local (accessible in client — must prefix NEXT_PUBLIC_)
NEXT_PUBLIC_WS_URL=ws://your-vps:8000/ws/feed
```

```tsx
// Server component — can use server-only env
const apiUrl = process.env.API_URL

// Client component — must use NEXT_PUBLIC_
const wsUrl = process.env.NEXT_PUBLIC_WS_URL
```

## Anti-Patterns
```tsx
// ❌ Pages Router — dead in 2026 for new projects
// pages/index.tsx
export async function getServerSideProps() { ... }  // NEVER

// ❌ useEffect for data fetching in 2026
useEffect(() => {
    fetch("/api/feed").then(...)  // use Server Component async fetch instead
}, [])

// ❌ 'use client' everywhere — kills perf
// Only add 'use client' when you actually need hooks/events

// ❌ API routes in pages/api/
// pages/api/browser.ts  — use app/api/ route handlers instead
```

## WebSocket in Client Component
```tsx
"use client"
import { useEffect, useState } from "react"

export function LiveFeed() {
    const [posts, setPosts] = useState<any[]>([])

    useEffect(() => {
        const ws = new WebSocket(process.env.NEXT_PUBLIC_WS_URL!)
        ws.onmessage = (e) => {
            const post = JSON.parse(e.data)
            setPosts(prev => [post, ...prev])
        }
        return () => ws.close()
    }, [])

    return <div>{posts.map(p => <div key={p.id}>{p.content}</div>)}</div>
}
```

## References
- Next.js App Router docs: https://nextjs.org/docs/app
- Server/Client Components: https://nextjs.org/docs/app/getting-started/server-and-client-components
- Production checklist: https://nextjs.org/docs/app/guides/production-checklist
- Tailwind v4: https://tailwindcss.com/docs/v4-beta
