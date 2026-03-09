---
name: react-nextjs
description: Next.js 14+ App Router best practices including Server Components, data fetching, caching, and Vercel optimization patterns. Use for Next.js development with waterfall prevention, bundle optimization, and server actions.
---

# Next.js App Router Best Practices

> Next.js 14+ with Vercel optimization patterns.

## Instructions

### 1. App Router Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page
├── loading.tsx         # Loading UI
├── error.tsx           # Error UI
├── not-found.tsx       # 404 page
├── (auth)/             # Route group
│   ├── login/
│   └── register/
└── api/
    └── users/
        └── route.ts    # API route
```

### 2. Server vs Client Components

```tsx
// ✅ Server Component (default) - no directive
async function UserList() {
  const users = await getUsers(); // Direct DB access
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// ✅ Client Component - needs interactivity
'use client';
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### 3. Prevent Request Waterfall

```tsx
// ❌ Bad - sequential (waterfall)
async function Page() {
  const user = await getUser();
  const posts = await getPosts(user.id);
  const comments = await getComments(posts[0].id);
  return ...;
}

// ✅ Good - parallel with Promise.all
async function Page() {
  const [user, posts] = await Promise.all([
    getUser(),
    getPosts()
  ]);
  return ...;
}

// ✅ Good - defer non-critical
async function Page() {
  const user = await getUser();
  const postsPromise = getPosts(user.id); // Don't await yet
  
  return (
    <div>
      <UserProfile user={user} />
      <Suspense fallback={<PostsSkeleton />}>
        <Posts promise={postsPromise} />
      </Suspense>
    </div>
  );
}
```

### 4. No Barrel Files (Bundle Optimization)

```tsx
// ❌ Bad - barrel file imports entire module
import { Button, Card } from '@/components';

// ✅ Good - direct imports
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
```

### 5. Dynamic Imports

```tsx
// ✅ Lazy load heavy components
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false
});
```

### 6. Server Actions

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  
  await db.post.create({ data: { title } });
  
  revalidatePath('/posts');
}

// Usage in component
<form action={createPost}>
  <input name="title" />
  <button type="submit">Create</button>
</form>
```

### 7. Caching Strategies

```tsx
// ✅ React.cache for request deduplication
import { cache } from 'react';

export const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } });
});

// ✅ Next.js fetch cache
const data = await fetch(url, {
  next: { revalidate: 3600 } // Revalidate hourly
});

// ✅ Static generation
export const dynamic = 'force-static';
```

### 8. Metadata

```tsx
// Static metadata
export const metadata: Metadata = {
  title: 'My App',
  description: 'Description...'
};

// Dynamic metadata
export async function generateMetadata({ params }): Promise<Metadata> {
  const product = await getProduct(params.id);
  return { title: product.name };
}
```

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Blog](https://vercel.com/blog)
