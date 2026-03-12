---
name: nextjs-16-proxy
description: Next.js 16 proxy convention (replacing middleware). Use when creating middleware, handling URL rewrites, or when the user mentions proxy.ts, middleware.ts, or route interception in Next.js 16+.
---

# Next.js 16 Proxy Convention

Next.js 16 renamed `middleware` to `proxy` to better reflect its network boundary purpose.

## Key Changes from Middleware

| Old (Next.js 15) | New (Next.js 16+) |
|------------------|-------------------|
| `middleware.ts` | `proxy.ts` |
| `export function middleware()` | `export function proxy()` |
| Same location | Same location |

## File Location

Place `proxy.ts` at the **same level as `app` or `pages`**:

```
src/
├── proxy.ts      ← Correct location
├── app/
│   └── ...
```

NOT inside `app/`:
```
src/
├── app/
│   ├── proxy.ts  ← Wrong location
│   └── ...
```

## Basic Template

```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Example: rewrite /uploads/* to /api/uploads/*
  if (pathname.startsWith("/uploads/")) {
    const newUrl = request.nextUrl.clone();
    newUrl.pathname = pathname.replace("/uploads/", "/api/uploads/");
    return NextResponse.rewrite(newUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/uploads/:path*"],
};
```

## Common Issue: Dynamic Routes Catching Paths

When you have a dynamic route like `[teamSlug]` at the root, it can catch paths before rewrites in `next.config.ts` are applied.

**Problem:**
- Request: `/uploads/image.png`
- Dynamic route `[teamSlug]` catches it as `teamSlug = "uploads"`
- Results in 404

**Solution:**
Use `proxy.ts` instead of `next.config.ts` rewrites. Proxy runs **before** routing.

## Migration Command

```bash
npx @next/codemod@canary middleware-to-proxy .
```

This automatically:
- Renames `middleware.ts` → `proxy.ts`
- Updates function name `middleware` → `proxy`
