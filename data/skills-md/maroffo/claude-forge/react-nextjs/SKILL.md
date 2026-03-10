---
name: react-nextjs
description: "React 19 + Next.js 16 App Router development. Use when working with .tsx/.jsx files, next.config, or user asks about Server Components, data fetching, state management, forms, or React testing."
compatibility: "Requires Node.js and npm. Optional: Vitest, Playwright."
allowed-tools: [mcp__acp__Read, mcp__acp__Edit, mcp__acp__Write, mcp__acp__Bash]
---

# ABOUTME: React 19 + Next.js 16 development with App Router, Server Components, TypeScript
# ABOUTME: Modern patterns for data fetching, state management, forms, testing, and styling

# React 19 + Next.js 16

## What's New (2025-2026)

| React 19.2 | Next.js 16 | Tailwind v4 |
|------------|------------|-------------|
| useActionState | `use cache` directive | CSS-first config |
| useFormStatus | proxy.ts | Oxide engine (100x faster) |
| useOptimistic | Turbopack default | Container queries |
| React Compiler | DevTools MCP | |

## Commands

```bash
npm run dev && npm run build && npm run test && npm run typecheck
```

## Core Patterns

```tsx
// Server Component (default)
async function Page() {
  const data = await fetchData()
  return <Component data={data} />
}

// Client Component
'use client'
function Interactive() {
  const [state, setState] = useState()
  return <button onClick={() => setState(x => x + 1)} />
}

// Server Action
async function submit(formData: FormData) {
  'use server'
  await db.insert(formData)
}
```

---

## Project Structure

```
src/
├── app/                    # App Router
├── components/ui/          # Primitives
├── features/*/             # Feature modules
├── lib/                    # Utils
├── stores/                 # Zustand
└── types/
```

---

## Server vs Client Components

**Default to Server. Client only when needed.**

| Server | Client |
|--------|--------|
| Fetch data, DB access | onClick, onChange |
| Sensitive data | useState, useEffect |
| Large deps, SEO | Browser APIs |

---

## Data Fetching

```tsx
// Server
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', { next: { revalidate: 60 } })
  return res.json()
}

// Next.js 16 Caching
async function getData() {
  'use cache'
  cacheLife('minutes')
  return fetchData()
}

// Client: TanStack Query
'use client'
export function usePosts() {
  return useQuery({ queryKey: ['posts'], queryFn: api.posts.list })
}
```

---

## Key Patterns

**State:** TanStack Query (server state), Zustand (global client), nuqs (URL state).

**Forms:** Server Action + `useActionState` + Zod validation. `useFormStatus` for pending UI.

**Performance:** `next/image` with priority, `dynamic()` for lazy loading, React Compiler for auto-memoization.

**Testing:** Vitest + React Testing Library (unit), Playwright (E2E).

For detailed code examples (forms, Zustand, testing, performance), see `references/react-patterns.md`.

---

## Checklist

- [ ] No `any`, no unnecessary `'use client'`
- [ ] Server/Client correctly separated
- [ ] Forms: useActionState + useFormStatus
- [ ] useOptimistic for mutations
- [ ] Images: next/image + priority

**Libraries:** TanStack Query, Zustand, nuqs, Zod, Vitest + Playwright
