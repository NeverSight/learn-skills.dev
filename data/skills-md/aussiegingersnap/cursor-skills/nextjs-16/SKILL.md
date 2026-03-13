---
name: nextjs-16
description: Next.js 16 specific patterns including proxy.ts (replaces middleware), cache components, and App Router conventions. This skill should be used when setting up a new Next.js 16 project or migrating from earlier versions.
---

# Next.js 16 Skill

Patterns and conventions specific to Next.js 16, including the new proxy.ts system, caching strategies, and modern App Router patterns.

## When to Use This Skill

- Setting up a new Next.js 16 project
- Migrating from Next.js 16 or earlier
- Implementing route protection with proxy.ts
- Configuring caching and PPR
- Understanding Next.js 16 breaking changes

## Breaking Changes in Next.js 16

### proxy.ts Replaces middleware.ts

**This is the biggest change.** The Edge-based `middleware.ts` is replaced by Node.js-based `proxy.ts`.

| Feature | middleware.ts (15) | proxy.ts (16) |
|---------|-------------------|---------------|
| Runtime | Edge | Node.js |
| Export | `middleware` | `proxy` |
| Async | Limited | Full async/await |
| Node APIs | Not available | Available |

## proxy.ts Setup

### Basic Structure

Create `proxy.ts` at project root (same level as `app/`):

```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function proxy(request: NextRequest): Promise<NextResponse> {
  // Your logic here
  return NextResponse.next();
}

export const config = {
  matcher: [
    // Match all paths except static files and API routes
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

### Authentication Proxy

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

const protectedRoutes = ['/dashboard', '/settings', '/profile'];
const authRoutes = ['/login', '/signup', '/forgot-password'];

export async function proxy(request: NextRequest): Promise<NextResponse> {
  const { pathname } = request.nextUrl;
  
  const isProtectedRoute = protectedRoutes.some((route) => 
    pathname.startsWith(route)
  );
  const isAuthRoute = authRoutes.some((route) => 
    pathname.startsWith(route)
  );
  
  // Skip for non-protected, non-auth routes
  if (!isProtectedRoute && !isAuthRoute) {
    return NextResponse.next();
  }
  
  // Get session (full async now works!)
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  
  // Redirect unauthenticated users from protected routes
  if (isProtectedRoute && !session) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }
  
  // Redirect authenticated users from auth routes
  if (isAuthRoute && session) {
    const redirect = request.nextUrl.searchParams.get('redirect') || '/dashboard';
    return NextResponse.redirect(new URL(redirect, request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Adding Headers

```typescript
export async function proxy(request: NextRequest): Promise<NextResponse> {
  const response = NextResponse.next();
  
  // Add security headers
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  return response;
}
```

### Geolocation / Feature Flags

```typescript
export async function proxy(request: NextRequest): Promise<NextResponse> {
  const response = NextResponse.next();
  
  // Access geo data (if available from your provider)
  const country = request.geo?.country || 'US';
  response.headers.set('x-user-country', country);
  
  return response;
}
```

## Project Structure

### Recommended Layout

```
project-root/
├── proxy.ts              # Route protection (NEW in 16)
├── next.config.ts        # Next.js configuration
├── drizzle.config.ts     # Database configuration
├── package.json
├── tsconfig.json
├── .env.local            # Environment variables
├── src/
│   ├── app/
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Home page
│   │   ├── (auth)/       # Auth route group
│   │   │   ├── login/
│   │   │   └── signup/
│   │   ├── (dashboard)/  # Dashboard route group
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── settings/
│   │   └── api/
│   │       ├── _lib/     # API utilities
│   │       ├── auth/     # Auth endpoints
│   │       └── [resources]/
│   ├── components/
│   │   ├── ui/           # Base UI components
│   │   └── [features]/   # Feature components
│   ├── lib/
│   │   ├── db/           # Database
│   │   ├── auth.ts       # Auth config
│   │   └── auth-client.ts
│   ├── hooks/            # React hooks
│   ├── stores/           # Zustand stores
│   └── providers/        # React providers
├── drizzle/
│   └── migrations/       # Database migrations
└── public/               # Static assets
```

### Route Groups

Use route groups `(folder)` for organization without affecting URLs:

```
app/
├── (marketing)/          # Marketing pages
│   ├── page.tsx          # → /
│   ├── about/            # → /about
│   └── pricing/          # → /pricing
├── (auth)/               # Auth pages (shared layout optional)
│   ├── login/            # → /login
│   └── signup/           # → /signup
└── (dashboard)/          # Dashboard (separate layout)
    ├── layout.tsx        # Dashboard layout with sidebar
    ├── page.tsx          # → /dashboard
    └── settings/         # → /dashboard/settings
```

## Server Components vs Client Components

### Default: Server Components

```typescript
// This is a Server Component by default
// Can directly fetch data, access DB, etc.
export default async function ProjectsPage() {
  const projects = await db.query.project.findMany();
  
  return (
    <div>
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
}
```

### Client Components

Add `'use client'` directive when you need:
- Event handlers (onClick, onChange)
- State (useState, useReducer)
- Effects (useEffect)
- Browser APIs
- Custom hooks that use above

```typescript
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### Composition Pattern

Server Component with Client Component children:

```typescript
// Server Component (page.tsx)
export default async function DashboardPage() {
  const data = await fetchData();
  
  return (
    <div>
      <h1>Dashboard</h1>
      {/* Pass server data to client component */}
      <InteractiveChart data={data} />
    </div>
  );
}

// Client Component (interactive-chart.tsx)
'use client';

export function InteractiveChart({ data }: { data: ChartData }) {
  const [filter, setFilter] = useState('all');
  // Interactive logic
}
```

## Data Fetching

### In Server Components

```typescript
async function getData() {
  // This runs on the server
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }, // Cache for 1 hour
  });
  return res.json();
}

export default async function Page() {
  const data = await getData();
  return <div>{/* Use data */}</div>;
}
```

### Caching Options

```typescript
// No cache (dynamic)
fetch(url, { cache: 'no-store' });

// Cache forever (static)
fetch(url, { cache: 'force-cache' });

// Revalidate after N seconds
fetch(url, { next: { revalidate: 60 } });

// Revalidate on-demand with tags
fetch(url, { next: { tags: ['projects'] } });

// Then invalidate:
import { revalidateTag } from 'next/cache';
revalidateTag('projects');
```

## Server Actions

### Basic Server Action

```typescript
// actions.ts
'use server';

import { db, project } from '@/lib/db';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const createSchema = z.object({
  name: z.string().min(1).max(255),
});

export async function createProject(formData: FormData) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) throw new Error('Unauthorized');
  
  const parsed = createSchema.safeParse({
    name: formData.get('name'),
  });
  
  if (!parsed.success) {
    return { error: 'Invalid input' };
  }
  
  await db.insert(project).values({
    name: parsed.data.name,
    userId: session.user.id,
  });
  
  revalidatePath('/dashboard/projects');
  return { success: true };
}
```

### Using in Forms

```typescript
// Client Component
'use client';

import { createProject } from './actions';
import { useActionState } from 'react';

export function CreateProjectForm() {
  const [state, formAction, isPending] = useActionState(createProject, null);
  
  return (
    <form action={formAction}>
      <input name="name" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Project'}
      </button>
      {state?.error && <p className="text-red-500">{state.error}</p>}
    </form>
  );
}
```

## Loading and Error States

### Loading UI

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />;
}
```

### Error Handling

```typescript
// app/dashboard/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Not Found

```typescript
// app/dashboard/[id]/page.tsx
import { notFound } from 'next/navigation';

export default async function ProjectPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const project = await getProject(id);
  
  if (!project) {
    notFound();
  }
  
  return <div>{project.name}</div>;
}

// app/dashboard/[id]/not-found.tsx
export default function NotFound() {
  return <div>Project not found</div>;
}
```

## next.config.ts

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Recommended settings
  reactStrictMode: true,
  poweredByHeader: false,
  
  // Image domains
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.googleusercontent.com',
      },
    ],
  },
  
  // Experimental features
  experimental: {
    // Enable if using Partial Pre-rendering
    // ppr: true,
  },
};

export default nextConfig;
```

## Environment Variables

### Naming Convention

```bash
# Server-only (default)
DATABASE_URL=postgres://...
BETTER_AUTH_SECRET=...

# Client-accessible (NEXT_PUBLIC_ prefix)
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_POSTHOG_KEY=...
```

### Accessing

```typescript
// Server-side (any variable)
const dbUrl = process.env.DATABASE_URL;

// Client-side (only NEXT_PUBLIC_ variables)
const appUrl = process.env.NEXT_PUBLIC_APP_URL;
```

## TypeScript Configuration

Ensure `tsconfig.json` includes:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "incremental": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "plugins": [
      { "name": "next" }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## Migration from Next.js 16

### Checklist

- [ ] Rename `middleware.ts` to `proxy.ts`
- [ ] Change export from `middleware` to `proxy`
- [ ] Update any Edge-specific code (now runs on Node.js)
- [ ] Review and update `next.config.js` → `next.config.ts`
- [ ] Test all protected routes
- [ ] Verify async operations in proxy work correctly
