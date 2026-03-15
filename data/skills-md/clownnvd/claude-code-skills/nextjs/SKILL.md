---
name: nextjs
description: "Next.js 16 App Router patterns, proxy.ts, use cache, async APIs, 37 documented errors with fixes, ecosystem compatibility, postinstall patches."
---

# Next.js 16 — App Router

## When to Use

Trigger on: next.js, nextjs, app router, server components, client components, use cache, proxy.ts, middleware migration, RSC, streaming, PPR, cacheComponents, route handler, server action, params, searchParams, cookies, headers, Suspense, cacheLife, cacheTag, revalidatePath, revalidateTag, next.config, turbopack, webpack.

## Reference Files

| File | Description |
|------|-------------|
| `references/breaking-changes.md` | 12 v15→v16 breaking changes, codemods, route segment replacements, CVE-2025-66478 |
| `references/best-practices.md` | Server/Client components, data fetching, caching, proxy, forms, auth, async APIs, performance |
| `references/errors-critical-high.md` | ERR-001 to ERR-014 — CRITICAL and HIGH severity errors with code fixes |
| `references/errors-medium-low.md` | ERR-015 to ERR-037 — MEDIUM and LOW severity errors, CVE summary |
| `references/ecosystem.md` | Prisma 7, Better Auth, Polar, @react-pdf, Anthropic SDK, Tailwind v4 compatibility |
| `references/patches.md` | 6 postinstall patches + 3 config workarounds for Next.js 16.1.6 |
| `references/quick-cards.md` | 11 quick reference cards (A-K): data fetching, caching, forms, proxy, env vars, DO/DON'T |

## Error Quick Lookup

| ID | Error | Severity |
|----|-------|----------|
| ERR-001 | CVE-2025-66478 RCE (CVSS 10.0) | CRITICAL |
| ERR-002 | Async params/searchParams TypeError | CRITICAL |
| ERR-003 | middleware.ts silently ignored | CRITICAL |
| ERR-004 | htmlLimitedBots build crash | CRITICAL |
| ERR-005 | useContext null in global-error | CRITICAL |
| ERR-006 | Turbopack + webpack config conflict | HIGH |
| ERR-007 | Uncached data outside Suspense | HIGH |
| ERR-008 | SWC options undefined (16.1.6) | HIGH |
| ERR-009 | Missing NextRequest/Response stubs | HIGH |
| ERR-010 | Dynamic APIs inside cache scope | HIGH |
| ERR-011 | "use cache" prerender timeout | HIGH |
| ERR-012 | Route segment config + cacheComponents | HIGH |
| ERR-013 | Functions passed to Client Components | HIGH |
| ERR-014 | useState/useContext null in build | HIGH |

For ERR-015 to ERR-037, see `references/errors-medium-low.md`.

## Top 5 Breaking Changes

| # | Change | Fix |
|---|--------|-----|
| 1 | `middleware.ts` → `proxy.ts` | Rename file + function. Codemod: `npx @next/codemod@canary middleware-to-proxy .` |
| 2 | Async request APIs | `await params`, `await cookies()`. Codemod: `npx @next/codemod next-async-request-api .` |
| 3 | fetch not cached by default | Add `{ cache: 'force-cache' }` explicitly |
| 4 | Turbopack is default bundler | Use `--webpack` flag to revert |
| 5 | Route segment configs removed | Replace with `'use cache'` + `cacheLife()` |

## Key Patterns

### Async Request APIs (v16)
```tsx
// Server Component
const { slug } = await params
const { q } = await searchParams
const cookieStore = await cookies()

// Route Handler
export async function GET(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
}
```

### Caching
```tsx
async function getData(id: string) {
  'use cache'
  cacheTag(`item-${id}`)
  return db.item.findUnique({ where: { id } })
}

// Invalidate in Server Action
'use server'
async function updateItem(id: string) {
  await db.item.update(...)
  revalidatePath('/items')   // BEFORE redirect
  redirect('/items')
}
```

### Proxy (formerly Middleware)
```ts
// src/proxy.ts
export function proxy(request: NextRequest) {
  const token = request.cookies.get('session')?.value
  if (!token && request.nextUrl.pathname.startsWith('/dashboard'))
    return NextResponse.redirect(new URL('/login', request.url))
  return NextResponse.next()
}
export const config = { matcher: ['/dashboard/:path*'] }
```

## Security

**CVE-2025-66478 (CVSS 10.0 — RCE):** Unauthenticated RCE via `Next-Action` header deserialization. Fix: `pnpm add next@16.0.10+`.
