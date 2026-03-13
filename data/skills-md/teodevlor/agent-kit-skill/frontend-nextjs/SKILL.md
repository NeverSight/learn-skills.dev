---
name: frontend-nextjs
description: Next.js frontend development conventions. Use when working on Next.js/React projects with App Router.
---

# Frontend Next.js Conventions

This skill provides specific conventions for Next.js frontend development.

## When to Use
- Use this skill when working on Next.js projects
- Use this skill when creating new pages, components, or API routes
- This skill builds upon `project-standards` skill

## Instructions

### 1. App Router Strategy

#### Default to Server Components
All components in `app/` are Server Components by default. Only add `"use client"` when interactivity is strictly needed.

```tsx
// Server Component (default) - No directive needed
async function UserProfile({ userId }: { userId: string }) {
  const user = await getUser(userId); // Direct data fetching
  return <div>{user.name}</div>;
}

// Client Component - Only when needed
"use client";

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

#### Data Fetching
Fetch data directly in Server Components using `async/await`. Avoid `useEffect` for data fetching.

### 2. File Structure & Naming

```
app/
├── (auth)/                    # Route group (no URL impact)
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── (dashboard)/
│   ├── layout.tsx             # Shared layout
│   ├── page.tsx               # /dashboard
│   └── settings/
│       └── page.tsx           # /dashboard/settings
├── api/
│   └── users/
│       └── route.ts           # API route
├── _components/               # Private folder (excluded from routing)
│   ├── Header.tsx
│   └── Footer.tsx
└── globals.css
```

#### Filenames
- `page.tsx`: Route UI
- `layout.tsx`: Shared UI (wrappers)
- `loading.tsx`: Loading states (Suspense)
- `error.tsx`: Error boundary
- `not-found.tsx`: 404 page

### 3. Performance & Optimization

#### Images
**STRICTLY** use `next/image` with defined dimensions.

```tsx
import Image from 'next/image';

// Good
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // For above-the-fold images
/>

// With fill
<div className="relative h-64 w-full">
  <Image src="/bg.jpg" alt="Background" fill className="object-cover" />
</div>
```

#### Fonts
Use `next/font` to optimize loading.

```tsx
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

### 4. Server Actions

Use Server Actions for form submissions instead of API routes.

```tsx
// app/actions.ts
"use server";

export async function createUser(formData: FormData) {
  const email = formData.get('email');
  // Server-side logic
  await db.user.create({ data: { email } });
  revalidatePath('/users');
}

// app/users/new/page.tsx
import { createUser } from '../actions';

export default function NewUserPage() {
  return (
    <form action={createUser}>
      <input name="email" type="email" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

### 5. State Management

#### URL as State
Prioritize storing search parameters in the URL.

```tsx
"use client";

import { useSearchParams, useRouter } from 'next/navigation';

function ProductFilters() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const setFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams);
    params.set(key, value);
    router.push(`?${params.toString()}`);
  };

  return (
    <select onChange={(e) => setFilter('category', e.target.value)}>
      {/* options */}
    </select>
  );
}
```

### 6. Component Patterns

```tsx
// Component with Props interface
interface CardProps {
  title: string;
  children: React.ReactNode;
  variant?: 'default' | 'outlined';
}

export function Card({ title, children, variant = 'default' }: CardProps) {
  return (
    <div className={cn('rounded-lg p-4', variants[variant])}>
      <h3 className="font-bold">{title}</h3>
      {children}
    </div>
  );
}
```

### 7. Dependencies

- **Styling:** Tailwind CSS
- **State:** TanStack Query + Zustand
- **Forms:** React Hook Form + Zod
- **UI:** shadcn/ui (recommended)
