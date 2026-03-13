---
name: nextjs-performance-architecture
description: A comprehensive guide to Next.js performance patterns, combining Data Fetching Colocation, the Donut Pattern, and the 'use cache' directive for optimal application architecture.
---

This document aggregates three core architectural patterns for modern Next.js 16+ development: **Data Fetching Colocation**, **The Donut Pattern**, and **Cache Components with `use cache`**. These patterns are designed to improve performance, maintainability, and code composition.

> **Prerequisites**: Next.js 16+ with `cacheComponents: true` enabled in `next.config.ts`.

---

## Quick Decision Guide

Use this flowchart to choose the right pattern:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Component Rendering Decision                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                ┌─────────────────────────────┐
                │ Does it need user state,    │
                │ event handlers, or hooks?   │
                └─────────────────────────────┘
                     │              │
                   Yes              No
                     │              │
                     ▼              ▼
            ┌────────────┐   ┌─────────────────────┐
            │ "use       │   │ Keep as Server      │
            │ client"    │   │ Component           │
            └────────────┘   └─────────────────────┘
                                    │
                                    ▼
                      ┌─────────────────────────────┐
                      │ Does it fetch data or do    │
                      │ expensive computation?      │
                      └─────────────────────────────┘
                           │              │
                         Yes              No
                           │              │
                           ▼              ▼
            ┌──────────────────────┐   Static in shell
            │ Is data user/request │   (automatic)
            │ specific?            │
            └──────────────────────┘
                  │         │
                Yes         No
                  │         │
                  ▼         ▼
         ┌─────────────┐  ┌─────────────┐
         │ Wrap in     │  │ Add         │
         │ <Suspense>  │  │ "use cache" │
         └─────────────┘  └─────────────┘
```

---

## 1. Data Fetching Colocation

### When to Use

- Data is passed through multiple layers of components (prop drilling)
- Root layout/page is blocked by a large initial data fetch
- Components are not reusable because they depend on props from a specific parent

### Implementation

Move `async` fetch calls directly into the Server Component that consumes the data:

```tsx
// ❌ Before: Prop drilling blocks parallelism
export default async function Page() {
  const data = await getData();
  return <Child data={data} />;
}

// ✅ After: Collocated fetching enables parallel loading
export default async function Child() {
  const data = await getData();
  return <div>{data.title}</div>;
}
```

### Resolving Promises with `use()`

Pass promises directly to Client Components and unwrap with `React.use()`:

```tsx
// Server Component
export default function Page() {
  const userPromise = getUser(); // Don't await!
  return (
    <Suspense fallback={<UserSkeleton />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}

// Client Component
"use client";
import { use } from "react";

export function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspends until resolved
  return <div>{user.name}</div>;
}
```

### ❌ Anti-Patterns

- Fetching all data at page level and threading through props
- Using `useEffect` + `useState` for data that could be fetched server-side
- Duplicating fetch logic across components instead of colocating

---

## 2. The Donut Pattern

### When to Use

- Adding interactivity to a page section while keeping nested content server-rendered
- Avoiding `"use client"` on a large component tree for a small interactive element
- Preserving `async` capability in deeply nested Server Components

### Implementation

1. **Isolate Interactive Logic** → Extract into a Client Component
2. **Create the "Hole"** → Accept `children` as a prop
3. **Compose on Server** → Pass Server Components as children

```tsx
// AnimatedContainer.tsx (Client Component - the "donut")
"use client";
import { motion } from "framer-motion";

export function AnimatedContainer({ children }: { children: React.ReactNode }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {children}
    </motion.div>
  );
}

// Page.tsx (Server Component)
import { AnimatedContainer } from "./AnimatedContainer";
import { ProductList } from "./ProductList"; // Server Component

export default function Page() {
  return (
    <AnimatedContainer>
      {/* ProductList runs on server, not included in client bundle */}
      <ProductList />
    </AnimatedContainer>
  );
}
```

### Benefits

- **Reduced Bundle Size**: Server Component code stays on server
- **Async Support**: Inner components can still be `async` and fetch data
- **Animation/Interactivity**: Outer wrapper handles client-side concerns

### ❌ Anti-Patterns

- Marking entire page as `"use client"` to add one click handler
- Putting data fetching in Client Components when it could be server-side
- Nesting Client Components unnecessarily deep

---

## 3. Cache Components with `use cache`

Cache Components let you mix static, cached, and dynamic content in a single route—the speed of static sites with the flexibility of dynamic rendering.

### Setup

Enable in `next.config.ts`:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  cacheComponents: true,
};

export default nextConfig;
```

### How It Works

At build time, Next.js renders your route. Components that don't access network resources or request data are **automatically static**. For others, you choose:

| Scenario | Solution |
|----------|----------|
| Needs request data (cookies, headers, user-specific) | Wrap in `<Suspense>` |
| Expensive but static/shared | Add `"use cache"` |
| Mix of both | Combine patterns (Donut + Cache) |

### Basic Usage

```tsx
// File-level caching (all exports cached)
"use cache";

export async function getProducts() {
  return await db.product.findMany();
}

export async function getCategories() {
  return await db.category.findMany();
}
```

```tsx
// Function-level caching
export async function getFeaturedSkills() {
  "use cache";
  return await db.skill.findMany({ where: { featured: true } });
}
```

### Cache Lifetime with `cacheLife()`

Control how long cached content lives using preset profiles:

| Profile | Use Case | Stale | Revalidate | Expire |
|---------|----------|-------|------------|--------|
| `"seconds"` | Real-time data (stock prices) | 0s | 1s | 60s |
| `"minutes"` | Frequently updated (feeds) | 5min | 1min | 1h |
| `"hours"` | Moderately static (blog posts) | 5min | 1h | 1d |
| `"days"` | Rarely changing (product catalog) | 5min | 1d | 1w |
| `"weeks"` | Very stable (landing pages) | 5min | 1w | 1mo |
| `"max"` | Immutable (versioned assets) | 5min | 1y | indefinite |

```tsx
import { cacheLife } from "next/cache";

export async function ProductCatalog() {
  "use cache";
  cacheLife("days"); // Cache for ~1 day

  const products = await db.product.findMany();
  return <ProductGrid products={products} />;
}
```

#### Conditional Cache Lifetimes

```tsx
import { cacheLife, cacheTag } from "next/cache";

async function getPostContent(slug: string) {
  "use cache";
  cacheTag(`post-${slug}`);

  const post = await fetchPost(slug);

  if (!post) {
    cacheLife("minutes"); // Missing content, check again soon
    return null;
  }

  cacheLife("days"); // Published content, cache longer
  return post.data;
}
```

### Cache Invalidation with `cacheTag()`

Tag cached entries for on-demand invalidation:

```tsx
import { cacheTag } from "next/cache";

export async function getSkillById(id: string) {
  "use cache";
  cacheTag("skills", `skill-${id}`);

  return await db.skill.findUnique({ where: { id } });
}
```

Invalidate with `updateTag()` in Server Actions (preferred for immediate invalidation):

```tsx
"use server";
import { updateTag } from "next/cache";

export async function updateSkill(id: string, data: SkillData) {
  await db.skill.update({ where: { id }, data });
  updateTag(`skill-${id}`); // Invalidate specific skill immediately
  updateTag("skills");       // Invalidate all skills
}
```

> **`updateTag` vs `revalidateTag`**:
>
> - **`updateTag`** — Use in Server Actions for **read-your-own-writes** (user sees changes immediately)
> - **`revalidateTag`** — Use in Route Handlers, webhooks, or when stale-while-revalidate is acceptable

### ❌ Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| `export const revalidate = 3600` | `cacheLife("hours")` inside `"use cache"` |
| `export const dynamic = "force-static"` | Add `"use cache"` to component |
| `export const fetchCache = "force-cache"` | Use `"use cache"` to control caching |
| Reading cookies/headers inside cached scope | Read outside, pass as arguments |

---

## 4. Combined Patterns

The real power comes from combining all three patterns:

### Example: E-commerce Product Page

```tsx
// app/products/[id]/page.tsx (Server Component)
import { Suspense } from "react";
import { ProductDetails } from "@/components/ProductDetails";
import { AddToCartButton } from "@/components/AddToCartButton";
import { RecommendedProducts } from "@/components/RecommendedProducts";
import { ProductSkeleton, RecommendedSkeleton } from "@/components/skeletons";

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return (
    <div className="grid grid-cols-3 gap-6">
      {/* Cached: Product details rarely change */}
      <div className="col-span-2">
        <Suspense fallback={<ProductSkeleton />}>
          <ProductDetails id={id} />
        </Suspense>
      </div>

      {/* Dynamic: User-specific cart state (Donut Pattern) */}
      <aside>
        <AddToCartButton productId={id} />
      </aside>

      {/* Cached with Suspense: Recommendations can stream in */}
      <div className="col-span-3">
        <Suspense fallback={<RecommendedSkeleton />}>
          <RecommendedProducts productId={id} />
        </Suspense>
      </div>
    </div>
  );
}
```

```tsx
// components/ProductDetails.tsx (Cached Server Component)
import { cacheLife, cacheTag } from "next/cache";

export async function ProductDetails({ id }: { id: string }) {
  "use cache";
  cacheLife("hours");
  cacheTag("products", `product-${id}`);

  const product = await db.product.findUnique({ where: { id } });
  return (
    <article>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <span className="text-2xl font-bold">${product.price}</span>
    </article>
  );
}
```

```tsx
// components/AddToCartButton.tsx (Client Component - Donut wrapper)
"use client";
import { useState, useTransition } from "react";
import { addToCart } from "@/actions/cart";

export function AddToCartButton({ productId }: { productId: string }) {
  const [isPending, startTransition] = useTransition();
  const [quantity, setQuantity] = useState(1);

  return (
    <form
      action={() => startTransition(() => addToCart(productId, quantity))}
    >
      <input
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(Number(e.target.value))}
        min={1}
      />
      <button disabled={isPending}>
        {isPending ? "Adding..." : "Add to Cart"}
      </button>
    </form>
  );
}
```

---

## 5. Suspense Boundaries Best Practices

### When to Use Suspense

| Scenario | Suspense Needed? |
|----------|------------------|
| Cached component (`"use cache"`) | Usually not needed (part of static shell) |
| Dynamic data (user-specific) | **Yes** - shows fallback while loading |
| Streaming async Server Component | **Yes** - prevents blocking |
| Client Component with `use()` | **Yes** - parent must provide boundary |

### Granular vs. Coarse Boundaries

```tsx
// ❌ Coarse: Entire page waits for all data
<Suspense fallback={<FullPageSkeleton />}>
  <Header />
  <MainContent />
  <Sidebar />
</Suspense>

// ✅ Granular: Components load independently
<Header /> {/* Static, no Suspense */}
<Suspense fallback={<ContentSkeleton />}>
  <MainContent /> {/* Async */}
</Suspense>
<Suspense fallback={<SidebarSkeleton />}>
  <Sidebar /> {/* Async, loads parallel to MainContent */}
</Suspense>
```

---

## 6. Debugging Tips

### Check Cache Status

In development, Next.js logs cache hits/misses. Look for:

- `CACHE HIT` - Served from cache
- `CACHE MISS` - Generated fresh and cached
- `CACHE SKIP` - Not cacheable (dynamic data accessed)

### Common Issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Component not caching | Accessing request-specific data | Move cookies/headers read outside cached scope |
| Stale data after mutation | Missing `revalidateTag` call | Add proper cache tags and revalidate |
| Hydration mismatch | Date/time in cached component | Use `cacheLife("seconds")` or move to client |
| Build error with `use cache` | Edge runtime not supported | Use Node.js runtime only |

### Verify Static Shell

Run `next build` and check the output:

- `○` = Static (rendered at build time)
- `●` = SSG with dynamic params
- `ƒ` = Dynamic (rendered at request time)
- `◐` = Partial Prerendering (static shell + dynamic holes)

---

## Quick Reference

| Pattern | Purpose | Key Directive |
|---------|---------|---------------|
| **Data Colocation** | Fetch where data is used | None (architectural) |
| **Donut Pattern** | Server content in Client wrapper | `"use client"` on wrapper only |
| **Cache Components** | Cache expensive computations | `"use cache"` |

| Function | Purpose |
|----------|---------|
| `cacheLife(profile)` | Set cache duration |
| `cacheTag(...tags)` | Tag for targeted invalidation |
| `updateTag(tag)` | Invalidate immediately (Server Actions only) |
| `revalidateTag(tag)` | Invalidate with stale-while-revalidate (Route Handlers, webhooks) |

---

## Related Documentation

- [Cache Components Guide](https://nextjs.org/docs/app/getting-started/cache-components)
- [use cache Directive](https://nextjs.org/docs/app/api-reference/directives/use-cache)
- [cacheLife Function](https://nextjs.org/docs/app/api-reference/functions/cacheLife)
- [cacheTag Function](https://nextjs.org/docs/app/api-reference/functions/cacheTag)
