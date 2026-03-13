---
name: nextjs-fullstack
description: Opinionated Next.js fullstack patterns — App Router, Tailwind CSS v4, shadcn/ui, Better Auth, Drizzle ORM, Server Actions, and Vercel deployment. Use when scaffolding a new project or enforcing consistent architecture across client projects.
---

This skill codifies an opinionated fullstack Next.js stack for building production web applications. It defines architecture patterns, file conventions, and best practices to ensure consistency across projects.

Use when: starting a new project, onboarding a developer to the stack, or reviewing code for pattern compliance.

## The Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Framework** | Next.js | 16+ | App Router, RSC, Server Actions |
| **Language** | TypeScript | 5.x | Strict mode enabled |
| **Styling** | Tailwind CSS | v4 | Utility-first, CSS variables |
| **Components** | shadcn/ui | latest | Copy-paste primitives, Radix-based |
| **Auth** | Better Auth | latest | Email/password, OAuth, sessions |
| **Database** | Drizzle ORM | latest | Type-safe SQL, migrations |
| **DB Provider** | PostgreSQL | (via Neon/Supabase/local) | Production database |
| **Animations** | Framer Motion | latest | LazyMotion + m for tree-shaking |
| **Forms** | React Hook Form + Zod | latest | Validation, Server Actions |
| **Email** | Nodemailer | latest | Transactional emails |
| **Hosting** | Vercel | — | Auto-deploy, edge functions |

## Project Structure

```
src/
├── app/
│   ├── (auth)/              # Auth route group
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── layout.tsx       # Auth layout (centered, minimal)
│   ├── (dashboard)/         # Protected route group
│   │   ├── dashboard/page.tsx
│   │   └── layout.tsx       # Dashboard layout (sidebar)
│   ├── (marketing)/         # Public route group
│   │   ├── page.tsx         # Homepage
│   │   ├── about/page.tsx
│   │   └── layout.tsx       # Marketing layout (header + footer)
│   ├── api/
│   │   ├── auth/[...all]/route.ts  # Better Auth handler
│   │   └── webhooks/               # External webhooks
│   ├── layout.tsx           # Root layout (providers, fonts, metadata)
│   ├── globals.css          # Tailwind imports, CSS variables
│   ├── sitemap.ts           # Dynamic sitemap
│   └── robots.ts            # Robots config
├── components/
│   ├── ui/                  # shadcn/ui components (don't edit)
│   ├── layout/              # Header, footer, sidebar, nav
│   ├── forms/               # Form components with validation
│   └── sections/            # Page section components
├── data/                    # Static content data (TypeScript)
├── lib/
│   ├── auth.ts              # Better Auth client instance
│   ├── auth-server.ts       # Better Auth server instance
│   ├── db/
│   │   ├── index.ts         # Drizzle client
│   │   ├── schema.ts        # Database schema
│   │   └── migrations/      # SQL migrations
│   ├── utils.ts             # cn() and shared utilities
│   └── validations/         # Zod schemas (shared client + server)
├── hooks/                   # Custom React hooks
├── types/                   # TypeScript type definitions
└── actions/                 # Server Actions
    ├── auth.ts
    └── {resource}.ts
```

## Architecture Patterns

### Server Components by Default

Every component is a Server Component unless it needs interactivity:

```typescript
// src/app/page.tsx — Server Component (default)
import { db } from "@/lib/db";

export default async function HomePage() {
  const posts = await db.query.posts.findMany();
  return <PostList posts={posts} />;
}
```

Add `"use client"` only for:
- Event handlers (onClick, onChange, onSubmit)
- useState, useEffect, useRef
- Browser APIs (window, document)
- Third-party client libraries

### Server Actions for Mutations

Use Server Actions instead of API routes for data mutations:

```typescript
// src/actions/contact.ts
"use server";

import { z } from "zod";
import { contactSchema } from "@/lib/validations/contact";

export async function submitContact(formData: FormData) {
  const parsed = contactSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
    message: formData.get("message"),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  // Send email, save to DB, etc.
  return { success: true };
}
```

### API Routes Only For

- Webhooks from external services
- Auth handlers (Better Auth)
- Public APIs consumed by third parties
- File uploads

### Route Groups for Layout Separation

```
(marketing)/  → public pages with header/footer
(auth)/       → login/register with minimal centered layout
(dashboard)/  → protected pages with sidebar, requires auth
```

### Metadata Pattern

Every page exports metadata. For `"use client"` pages, use a sibling layout:

```typescript
// src/app/about/page.tsx (Server Component)
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About",
  description: "About our company",
};

export default function AboutPage() { ... }
```

```typescript
// src/app/contact/layout.tsx (for client pages)
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contact",
  description: "Get in touch",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
```

### Authentication Pattern (Better Auth)

```typescript
// src/lib/auth-server.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/lib/db";

export const auth = betterAuth({
  database: drizzleAdapter(db),
  emailAndPassword: { enabled: true },
  // ... providers
});

// src/lib/auth.ts (client)
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient();
```

### Database Pattern (Drizzle ORM)

```typescript
// src/lib/db/schema.ts
import { pgTable, text, timestamp, uuid } from "drizzle-orm/pg-core";

export const posts = pgTable("posts", {
  id: uuid("id").primaryKey().defaultRandom(),
  title: text("title").notNull(),
  content: text("content"),
  createdAt: timestamp("created_at").defaultNow(),
});

// src/lib/db/index.ts
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import * as schema from "./schema";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

### Validation Pattern (Zod — Shared Client + Server)

```typescript
// src/lib/validations/contact.ts
import { z } from "zod";

export const contactSchema = z.object({
  name: z.string().min(2, "Name is required"),
  email: z.string().email("Invalid email"),
  message: z.string().min(10, "Message too short"),
});

export type ContactInput = z.infer<typeof contactSchema>;
```

Used in both Server Actions (server-side validation) and React Hook Form (client-side validation).

### Animation Pattern (Framer Motion — Tree-Shakeable)

```typescript
// src/components/sections/animated-section.tsx
"use client";

import { LazyMotion, domAnimation, m } from "framer-motion";

export function AnimatedSection({ children }: { children: React.ReactNode }) {
  return (
    <LazyMotion features={domAnimation}>
      <m.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.5 }}
      >
        {children}
      </m.div>
    </LazyMotion>
  );
}
```

Always use `LazyMotion` + `m` (not `motion`) for smaller bundles.

## Tailwind CSS v4 Setup

```css
/* src/app/globals.css */
@import "tailwindcss";

@theme {
  --color-primary: #8e375c;
  --color-primary-dark: #6d2847;
  --font-heading: "Playfair Display", serif;
  --font-body: "Inter", sans-serif;
}
```

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Files | kebab-case | `page-hero.tsx` |
| Components | PascalCase | `PageHero` |
| Hooks | camelCase with `use` prefix | `useAuth` |
| Server Actions | camelCase verb | `submitContact` |
| Zod schemas | camelCase + `Schema` suffix | `contactSchema` |
| DB tables | snake_case (plural) | `blog_posts` |
| DB columns | snake_case | `created_at` |
| CSS variables | kebab-case with `--` prefix | `--color-primary` |
| Env vars | SCREAMING_SNAKE_CASE | `DATABASE_URL` |

## Common Commands

```bash
# Development
npm run dev              # Start dev server
npm run build            # Production build
npm run lint             # ESLint

# Database
npx drizzle-kit generate   # Generate migration from schema changes
npx drizzle-kit migrate    # Apply migrations
npx drizzle-kit studio     # Open Drizzle Studio (DB browser)

# shadcn/ui
npx shadcn@latest add button   # Add a component

# Deployment
npx vercel                 # Deploy preview
npx vercel --prod          # Deploy production
```

## Environment Variables Template

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Auth
BETTER_AUTH_SECRET=generate-a-random-string
BETTER_AUTH_URL=http://localhost:3000

# Email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASS=your-password
SMTP_FROM=noreply@example.com

# Optional
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

## Agent Team Integration

This skill is used by the `designer` teammate in the `website-refactor` workflow to ensure consistent architecture. It can also be loaded by any teammate that needs to understand the project's patterns.

## Anti-Patterns (Don't Do This)

- **API routes for internal mutations** — Use Server Actions instead
- **`"use client"` on pages** — Keep pages as Server Components; extract client parts into child components
- **Importing `motion` directly** — Always use `LazyMotion` + `m` for tree-shaking
- **Raw SQL** — Use Drizzle ORM for type-safe queries
- **`any` types** — TypeScript strict mode is enabled; type everything
- **Inline styles** — Use Tailwind classes
- **`.env` in git** — Only `.env.example` is committed
