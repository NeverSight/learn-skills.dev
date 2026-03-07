---
name: next-cache-components
description: Next.js 16 caching model expertise covering the 'use cache' directive, cacheLife() API, cacheTag() for invalidation, cacheComponents configuration, and Partial Prerendering (PPR). Use when implementing caching strategies in Next.js 16+ applications, migrating from unstable_cache, or optimizing server component rendering.
license: MIT
metadata:
  author: vercel-labs
  version: '1.0.0'
  source: vercel-labs/next-skills
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
version: 1.1.0
tools: []
---

# Next.js Cache Components

Deep expertise on the Next.js 16 caching model. Covers the `'use cache'` directive, `cacheLife()` profiles, `cacheTag()` invalidation, `cacheComponents` configuration, and Partial Prerendering (PPR) integration.

## When to Apply

Use this skill when:

- Implementing caching in a Next.js 16+ application
- Migrating from `unstable_cache` or `revalidate` patterns to the new caching API
- Configuring component-level caching with `cacheComponents`
- Setting up cache invalidation with tags
- Integrating Partial Prerendering (PPR) with cached components
- Choosing between static generation, ISR, and dynamic rendering

## Core Concepts

### The Caching Paradigm Shift (Next.js 15 to 16)

Next.js 16 introduces a fundamentally new caching model:

| Feature           | Next.js 14          | Next.js 15            | Next.js 16                       |
| ----------------- | ------------------- | --------------------- | -------------------------------- |
| fetch() caching   | Cached by default   | Not cached by default | Not cached by default            |
| Route caching     | Automatic           | Opt-in                | `'use cache'` directive          |
| Data caching      | `revalidate` option | `revalidate` option   | `cacheLife()` API                |
| Invalidation      | `revalidateTag()`   | `revalidateTag()`     | `cacheTag()` + `revalidateTag()` |
| Component caching | Not available       | Experimental          | `cacheComponents: true`          |

### Key Principle

In Next.js 16, caching is **explicit and opt-in**. Nothing is cached unless you explicitly use the `'use cache'` directive.

## The 'use cache' Directive

### Basic Usage

Add `'use cache'` at the top of a file or function to enable caching:

```typescript
// app/page.tsx -- cache the entire page
'use cache';

export default async function Page() {
  const data = await fetch('https://api.example.com/data');
  const posts = await data.json();

  return (
    <main>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.body}</p>
        </article>
      ))}
    </main>
  );
}
```

### Function-Level Caching

Cache individual async functions instead of entire pages:

```typescript
// lib/data.ts
import { cacheLife, cacheTag } from 'next/cache';

export async function getUser(id: string) {
  'use cache';
  cacheLife('hours');
  cacheTag(`user-${id}`);

  const res = await fetch(`https://api.example.com/users/${id}`);
  return res.json();
}

export async function getPosts() {
  'use cache';
  cacheLife('minutes');
  cacheTag('posts');

  const res = await fetch('https://api.example.com/posts');
  return res.json();
}
```

### Component-Level Caching

With `cacheComponents: true` in `next.config.ts`, individual Server Components can be cached:

```typescript
// next.config.ts
const nextConfig = {
  cacheComponents: true,
};

export default nextConfig;
```

```tsx
// components/user-profile.tsx
import { cacheLife, cacheTag } from 'next/cache';

export async function UserProfile({ userId }: { userId: string }) {
  'use cache';
  cacheLife('hours');
  cacheTag(`user-profile-${userId}`);

  const user = await fetch(`/api/users/${userId}`).then(r => r.json());

  return (
    <div className="profile-card">
      <img src={user.avatar} alt={user.name} />
      <h2>{user.name}</h2>
      <p>{user.bio}</p>
    </div>
  );
}
```

**Key benefit**: The page can re-render while the cached component serves from cache, avoiding redundant data fetches for unchanged components.

## Cache Profiles with cacheLife()

### Built-in Profiles

```typescript
import { cacheLife } from 'next/cache';

// Predefined profiles
cacheLife('seconds'); // stale: 0, revalidate: 1s, expire: 60s
cacheLife('minutes'); // stale: 5min, revalidate: 1min, expire: 1h
cacheLife('hours'); // stale: 5min, revalidate: 1h, expire: 1d
cacheLife('days'); // stale: 5min, revalidate: 1d, expire: 1w
cacheLife('weeks'); // stale: 5min, revalidate: 1w, expire: 30d
cacheLife('max'); // stale: 5min, revalidate: 30d, expire: 365d
```

### Custom Profiles

Define custom cache profiles in `next.config.ts`:

```typescript
// next.config.ts
const nextConfig = {
  cacheLife: {
    'blog-post': {
      stale: 300, // 5 minutes -- serve stale while revalidating
      revalidate: 3600, // 1 hour -- revalidate in background
      expire: 86400, // 1 day -- maximum cache lifetime
    },
    'user-session': {
      stale: 0, // Never serve stale
      revalidate: 60, // Revalidate every minute
      expire: 300, // Expire after 5 minutes
    },
    'static-content': {
      stale: 3600, // 1 hour stale tolerance
      revalidate: 86400, // Revalidate daily
      expire: 604800, // Expire after 1 week
    },
  },
};
```

Usage:

```typescript
async function getBlogPost(slug: string) {
  'use cache';
  cacheLife('blog-post');
  cacheTag(`blog-${slug}`);

  return fetch(`/api/posts/${slug}`).then(r => r.json());
}
```

### Profile Selection Guide

| Content Type     | Profile                 | Rationale                        |
| ---------------- | ----------------------- | -------------------------------- |
| Static pages     | `'max'` or `'weeks'`    | Content rarely changes           |
| Blog posts       | `'days'` or custom      | Updated occasionally             |
| Product listings | `'hours'`               | Prices/stock change moderately   |
| User dashboards  | `'minutes'`             | Data updates frequently          |
| Real-time feeds  | `'seconds'` or no cache | Data changes constantly          |
| Auth-dependent   | custom (stale: 0)       | Must never serve stale auth data |

## Cache Invalidation with cacheTag()

### Tagging Cached Data

```typescript
import { cacheTag } from 'next/cache';

async function getProduct(id: string) {
  'use cache';
  cacheLife('hours');
  cacheTag('products', `product-${id}`);

  return fetch(`/api/products/${id}`).then(r => r.json());
}
```

### Invalidating Cache

Use `revalidateTag()` in Server Actions or Route Handlers:

```typescript
// app/actions.ts
'use server';

import { revalidateTag } from 'next/cache';

export async function updateProduct(id: string, data: ProductData) {
  await db.products.update(id, data);

  // Invalidate specific product cache
  revalidateTag(`product-${id}`);

  // Invalidate all products listing
  revalidateTag('products');
}
```

### Tag Naming Conventions

```
entity-type                  -> 'products', 'users', 'posts'
entity-type-id               -> 'product-123', 'user-456'
entity-type-relation         -> 'product-reviews', 'user-orders'
entity-type-relation-id      -> 'product-123-reviews'
```

### Hierarchical Invalidation

```typescript
// Tag hierarchy for a blog
cacheTag('blog'); // All blog content
cacheTag('blog', `blog-${slug}`); // Specific post
cacheTag('blog', 'blog-comments'); // All comments
cacheTag('blog', `blog-comments-${postId}`); // Post comments

// Invalidate all blog content
revalidateTag('blog');

// Invalidate just one post
revalidateTag(`blog-${slug}`);
```

## Partial Prerendering (PPR) Integration

PPR combines static shells with dynamic holes, and `'use cache'` works with it.

### How PPR + Cache Works

```tsx
// app/product/[id]/page.tsx
import { Suspense } from 'react';
import { ProductDetails } from './product-details';
import { RecommendedProducts } from './recommended';
import { UserReviews } from './reviews';

// Static shell (prerendered at build time)
export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <main>
      {/* Cached component -- serves from cache */}
      <ProductDetails productId={id} />

      {/* Dynamic holes -- rendered on request */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <UserReviews productId={id} />
      </Suspense>

      <Suspense fallback={<RecommendedSkeleton />}>
        <RecommendedProducts productId={id} />
      </Suspense>
    </main>
  );
}
```

```tsx
// components/product-details.tsx
import { cacheLife, cacheTag } from 'next/cache';

export async function ProductDetails({ productId }: { productId: string }) {
  'use cache';
  cacheLife('hours');
  cacheTag(`product-${productId}`);

  const product = await fetch(`/api/products/${productId}`).then(r => r.json());

  return (
    <section>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <span>${product.price}</span>
    </section>
  );
}
```

### Enable PPR

```typescript
// next.config.ts
const nextConfig = {
  ppr: true, // Enable Partial Prerendering
  cacheComponents: true, // Enable component-level caching
};
```

## Migration from Previous Caching APIs

### From unstable_cache (Next.js 14/15)

```typescript
// Before (Next.js 14/15)
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (id: string) => {
    return db.users.findUnique({ where: { id } });
  },
  ['user'],
  { revalidate: 3600, tags: ['users'] }
);

// After (Next.js 16)
import { cacheLife, cacheTag } from 'next/cache';

async function getUser(id: string) {
  'use cache';
  cacheLife('hours');
  cacheTag('users', `user-${id}`);

  return db.users.findUnique({ where: { id } });
}
```

### From fetch revalidate Option

```typescript
// Before (Next.js 14)
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600, tags: ['data'] },
});

// After (Next.js 16)
async function getData() {
  'use cache';
  cacheLife('hours');
  cacheTag('data');

  return fetch('https://api.example.com/data').then(r => r.json());
}
```

### From generateStaticParams + revalidate

```typescript
// Before (Next.js 14/15)
export const revalidate = 3600;

export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({ slug: post.slug }));
}

// After (Next.js 16) -- use 'use cache' at page level
('use cache');

import { cacheLife } from 'next/cache';

cacheLife('hours');

export default async function Page({ params }) {
  const { slug } = await params;
  // ...
}
```

## Common Patterns

### Cached Data Layer

Create a centralized data access layer with caching:

```typescript
// lib/data/products.ts
import { cacheLife, cacheTag } from 'next/cache';

export async function getProduct(id: string) {
  'use cache';
  cacheLife('hours');
  cacheTag('products', `product-${id}`);

  return prisma.product.findUnique({ where: { id } });
}

export async function getProducts(category?: string) {
  'use cache';
  cacheLife('minutes');
  cacheTag('products', category ? `category-${category}` : 'all-products');

  return prisma.product.findMany({
    where: category ? { category } : undefined,
    orderBy: { createdAt: 'desc' },
  });
}
```

### Auth-Aware Caching

Cache public data but keep auth-dependent data dynamic:

```tsx
// Cached: product data (same for all users)
async function ProductInfo({ id }: { id: string }) {
  'use cache';
  cacheLife('hours');
  cacheTag(`product-${id}`);

  const product = await getProduct(id);
  return <ProductCard product={product} />;
}

// NOT cached: user-specific data
async function UserCartStatus({ userId }: { userId: string }) {
  // No 'use cache' -- always dynamic
  const cart = await getCart(userId);
  return <CartBadge count={cart.items.length} />;
}
```

## Iron Laws

1. **ALWAYS** use `'use cache'` explicitly on every component or function you intend to cache — in Next.js 16, nothing is cached unless you opt in; implicit caching assumptions from Next.js 14 are gone.
2. **NEVER** use `'use cache'` on components that render user-specific or auth-dependent data — the cache key does not include session context; different users will receive each other's cached content.
3. **ALWAYS** call `cacheTag()` on every cached function that reads mutable data — without tags, there is no way to invalidate stale data after a mutation; the only recourse is waiting for expiry.
4. **NEVER** cache Server Actions that perform mutations — `'use cache'` returns a cached response instead of executing the mutation; data changes are silently discarded.
5. **ALWAYS** call `revalidateTag()` in Server Actions or Route Handlers immediately after a mutation — forgetting invalidation means stale data persists for the full cache lifetime after every write.

## Anti-Patterns

| Anti-Pattern                                     | Why It Fails                                                                            | Correct Approach                                                                  |
| ------------------------------------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Using `'use cache'` on auth-dependent components | Cache key excludes session context; different users receive each other's cached data    | Keep auth-dependent components dynamic; cache only public, user-agnostic data     |
| Caching Server Actions that mutate data          | Returns cached response instead of executing mutation; writes are silently discarded    | Never put `'use cache'` on mutation actions; only cache read operations           |
| Missing `cacheTag()` on mutable data             | No invalidation path; stale data persists until expiry with no way to purge on mutation | Always tag cached data: `cacheTag('entity', 'entity-id')`                         |
| Forgetting `revalidateTag()` after mutations     | Stale data persists for full cache lifetime after every write                           | Call `revalidateTag()` in every Server Action or Route Handler that modifies data |
| Overly broad cache tag names                     | `revalidateTag('all')` invalidates the entire cache on every mutation — defeats purpose | Use granular hierarchical tags: `'products'`, `'product-{id}'`                    |

## References

- [Next.js Caching Documentation](https://nextjs.org/docs/app/building-your-application/caching)
- [use cache Directive](https://nextjs.org/docs/app/api-reference/directives/use-cache)
- [cacheLife API](https://nextjs.org/docs/app/api-reference/functions/cacheLife)
- [cacheTag API](https://nextjs.org/docs/app/api-reference/functions/cacheTag)
- [Partial Prerendering](https://nextjs.org/docs/app/building-your-application/rendering/partial-prerendering)
