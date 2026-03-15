---
name: nextjs-frontend
description: >
  Expert Next.js, React.js, and Vue.js frontend development skill. ALWAYS trigger for ANY task
  involving Next.js (App Router, Pages Router), React.js, Vue.js, TypeScript frontend,
  server components, client components, SSR, SSG, ISR, SEO optimization, metadata API,
  Zustand/Redux/Pinia state management, React Query/SWR data fetching, form handling
  (React Hook Form + Zod), routing, middleware, image optimization, performance (Core Web Vitals),
  internationalization (i18n), or deploying to Vercel/Netlify.
  Also triggers for: "build a website", "create a web app", "Next.js project", "React page",
  "Vue component", "frontend architecture", "landing page", "dashboard UI".
---

# Next.js / React / Vue Frontend Expert

You are a senior frontend engineer specializing in Next.js 14+ (App Router), React 18+, Vue 3,
TypeScript, and Tailwind CSS. You build performant, accessible, SEO-friendly web applications.

## Next.js App Router Architecture

```
app/
├── (marketing)/           # Route group (no URL segment)
│   ├── page.tsx           # /
│   ├── about/page.tsx     # /about
│   └── layout.tsx
├── (dashboard)/
│   ├── layout.tsx         # Protected layout
│   ├── dashboard/page.tsx
│   └── settings/page.tsx
├── api/
│   ├── auth/[...nextauth]/route.ts
│   └── products/route.ts
├── globals.css
├── layout.tsx             # Root layout
└── not-found.tsx

components/
├── ui/                    # shadcn/ui components
├── layout/                # Header, Footer, Sidebar
└── features/              # Feature-specific

lib/
├── db.ts                  # Prisma client singleton
├── auth.ts                # NextAuth config
└── utils.ts               # cn() and helpers

hooks/
├── use-debounce.ts
└── use-media-query.ts
```

## Server vs Client Components

```typescript
// ✅ Server Component (default) - fetch data directly
// app/products/page.tsx
import { db } from '@/lib/db';

export default async function ProductsPage() {
  const products = await db.product.findMany({ orderBy: { createdAt: 'desc' } });
  return (
    <div>
      {products.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  );
}

// ✅ Client Component - only when needed (interactivity, hooks, browser APIs)
'use client';
import { useState } from 'react';

export function SearchBar({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('');
  return (
    <input
      value={query}
      onChange={e => { setQuery(e.target.value); onSearch(e.target.value); }}
    />
  );
}
```

## Data Fetching Patterns

```typescript
// ✅ Server Component with fetch (automatic deduplication)
async function getData(id: string) {
  const res = await fetch(`${process.env.API_URL}/posts/${id}`, {
    next: { revalidate: 60 }, // ISR: revalidate every 60s
  });
  if (!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

// ✅ React Query for client-side (hooks/useProducts.ts)
import { useQuery } from '@tanstack/react-query';

export function useProducts(filters: Filters) {
  return useQuery({
    queryKey: ['products', filters],
    queryFn: () => fetch(`/api/products?${new URLSearchParams(filters as any)}`).then(r => r.json()),
    staleTime: 1000 * 60 * 5,
  });
}
```

## Route Handlers (API)

```typescript
// app/api/products/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { db } from '@/lib/db';
import { auth } from '@/lib/auth';

const CreateProductSchema = z.object({
  name: z.string().min(1).max(100),
  price: z.number().positive(),
});

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const page = Number(searchParams.get('page') ?? 1);

  const products = await db.product.findMany({
    skip: (page - 1) * 20,
    take: 20,
    orderBy: { createdAt: 'desc' },
  });

  return NextResponse.json({ products, page });
}

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const body = await req.json();
  const parsed = CreateProductSchema.safeParse(body);
  if (!parsed.success) return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });

  const product = await db.product.create({ data: { ...parsed.data, userId: session.user.id } });
  return NextResponse.json(product, { status: 201 });
}
```

## Forms with React Hook Form + Zod

```typescript
'use client';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8, 'Min 8 characters'),
});

type FormData = z.infer<typeof schema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await signIn('credentials', data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} type="email" />
      {errors.email && <span>{errors.email.message}</span>}
      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  );
}
```

## Metadata API (SEO)

```typescript
// app/products/[id]/page.tsx
import { Metadata } from 'next';

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const product = await fetchProduct(params.id);
  return {
    title: `${product.name} | MyStore`,
    description: product.description,
    openGraph: {
      title: product.name,
      images: [{ url: product.imageUrl, width: 1200, height: 630 }],
    },
  };
}
```

## Next.js Performance

```typescript
// ✅ Image optimization
import Image from 'next/image';
<Image src="/hero.jpg" alt="Hero" width={1200} height={630} priority sizes="100vw" />

// ✅ Font optimization
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'], display: 'swap' });

// ✅ Dynamic imports
const HeavyChart = dynamic(() => import('@/components/Chart'), {
  loading: () => <Skeleton />,
  ssr: false,
});

// ✅ Parallel data fetching
const [user, posts, comments] = await Promise.all([
  fetchUser(id),
  fetchPosts(id),
  fetchComments(id),
]);
```

## Middleware (Auth Protection)

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';

export default auth(function middleware(req) {
  if (!req.auth && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## Tailwind + shadcn/ui Setup

```bash
# New project
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir
cd my-app

# shadcn/ui
npx shadcn@latest init
npx shadcn@latest add button card input form table dialog

# React Query
npm i @tanstack/react-query @tanstack/react-query-devtools

# Forms
npm i react-hook-form @hookform/resolvers zod

# Auth
npm i next-auth@beta
```

## Vercel Deployment

```json
// next.config.ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  images: {
    remotePatterns: [{ hostname: 'res.cloudinary.com' }],
  },
  experimental: {
    ppr: true, // Partial prerendering
  },
};

export default config;
```

## Core Web Vitals Checklist

- [ ] LCP < 2.5s (optimize images, use `priority` on above-fold images)
- [ ] FID/INP < 100ms (minimize JS, defer non-critical)
- [ ] CLS < 0.1 (set image dimensions, avoid layout shifts)
- [ ] Server components for data-heavy pages
- [ ] Dynamic import for heavy client components
- [ ] `next/image` for all images
- [ ] `next/font` for web fonts (no FOUT)
- [ ] Streaming with `<Suspense>` for slow data
