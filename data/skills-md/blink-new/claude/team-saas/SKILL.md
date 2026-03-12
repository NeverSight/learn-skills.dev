---
name: team-saas
description: Build production-grade multi-tenant SaaS applications with team workspaces, member invitation, authentication, and modern UI
---

# Team SaaS Architecture Skill

Build production-grade multi-tenant SaaS applications with team workspaces, member invitation, authentication, and modern UI. Based on a proven architecture powering real production applications.

## When to Use This Skill

Use when:
- Building a new SaaS product with team/workspace functionality
- Setting up multi-tenant authentication and authorization
- Implementing team member invitation flows
- Creating Linear/Vercel-style modern UI with light/dark mode
- Setting up background job processing for SaaS
- Deploying full-stack Next.js apps to Railway

## Tech Stack Overview

| Layer | Technology | Version |
|-------|------------|---------|
| **Framework** | Next.js (App Router) | 16.x |
| **React** | React | 19.x |
| **Runtime** | Bun | Latest |
| **Database** | PostgreSQL (Railway) | - |
| **ORM** | Prisma | 7.x |
| **Auth** | NextAuth v5 (Auth.js) | 5.0.0-beta |
| **UI** | shadcn/ui (new-york) | Latest |
| **Styling** | Tailwind CSS | v4 |
| **Theming** | next-themes | Latest |
| **Icons** | Lucide React | Latest |
| **State** | TanStack React Query | 5.x |
| **Validation** | Zod | 4.x |
| **Email** | Resend | 6.x |
| **Storage** | Railway S3-compatible | - |
| **Jobs** | pg-boss | 12.x |
| **Hosting** | Railway | - |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Next.js Application                          │
├─────────────────────────────────────────────────────────────────────┤
│  Landing Page     │    Auth Pages    │     Dashboard (Protected)    │
│  /                │    /login        │     /teams/[teamId]/*        │
│  /pricing         │    /register     │     /dashboard               │
│                   │    /invite/[t]   │     /settings                │
├─────────────────────────────────────────────────────────────────────┤
│                          API Routes                                 │
│  /api/auth/*      │  /api/teams/*    │  /api/uploads/*              │
│  /api/cron/*      │  /api/webhooks/* │  /api/invitations/*          │
├─────────────────────────────────────────────────────────────────────┤
│  proxy.ts (Security Headers)  │  layout.tsx (Auth Protection)       │
├─────────────────────────────────────────────────────────────────────┤
│                         Services Layer                              │
│  Prisma (DB)  │  Resend (Email)  │  S3 (Storage)  │  pg-boss (Jobs) │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Railway Infrastructure                         │
│   PostgreSQL   │   S3 Bucket   │   Redis (optional)                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Core Patterns

### 1. Multi-Tenant Team Structure

Every data entity belongs to a team. Users can be members of multiple teams with roles.

```
User ─┬─> TeamMember ─> Team ─┬─> Creator
      │                       ├─> Campaign
      └─> TeamMember ─> Team  ├─> Content
                              └─> ... (all team resources)
```

### 2. Route Groups

```
src/app/
├── (auth)/              # Public auth pages (login, register)
│   └── layout.tsx       # Client component, styling only
├── (dashboard)/         # Protected authenticated routes
│   ├── layout.tsx       # Server component with auth() check + redirect
│   └── teams/[teamId]/  # Team-scoped pages
├── (marketing)/         # Public marketing pages
├── invite/[token]/      # Team invitation acceptance
└── api/                 # API routes
```

### 3. Route Protection Pattern (Layout-based, NOT middleware)

**IMPORTANT:** Auth protection is done via Server Component layout checks, NOT Edge middleware.

```typescript
// src/app/(dashboard)/layout.tsx
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function DashboardLayout({ children }) {
  const session = await auth();
  
  if (!session?.user) {
    redirect("/login");
  }
  
  return <DashboardShell session={session}>{children}</DashboardShell>;
}
```

### 4. API Route Permission Pattern

```typescript
// Use api-helpers for clean, consistent patterns
import { requireTeamMember, parseJsonBody, withErrorHandler, ApiError } from "@/lib/api-helpers";

type RouteParams = {
  params: Promise<{ teamId: string }>;  // Next.js 15+ async params
};

export const POST = withErrorHandler(async (req: NextRequest, { params }: RouteParams) => {
  const { teamId } = await params;  // MUST await params
  
  const { userId, role } = await requireTeamMember(teamId);  // Throws 401/403
  
  if (role !== "ADMIN") {
    throw new ApiError("Admin access required", 403);
  }
  
  const data = await parseJsonBody(req, mySchema);  // Validates with Zod
  
  // ... business logic
  
  return NextResponse.json(result);
});
```

## File Structure

```
src/
├── app/
│   ├── (auth)/                    # Auth pages (public)
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── layout.tsx             # Client component, no auth
│   ├── (dashboard)/               # Protected pages
│   │   ├── layout.tsx             # Server component, auth check
│   │   ├── dashboard-shell.tsx    # Sidebar + nav
│   │   └── teams/[teamId]/
│   ├── invite/[token]/page.tsx    # Invitation acceptance
│   ├── api/
│   │   ├── auth/[...nextauth]/route.ts
│   │   ├── teams/
│   │   │   ├── route.ts           # List/create teams
│   │   │   └── [teamId]/
│   │   │       ├── route.ts       # Team CRUD
│   │   │       ├── members/
│   │   │       └── invitations/
│   │   ├── invitations/
│   │   │   └── [token]/accept/route.ts
│   │   └── uploads/[...path]/route.ts  # S3 proxy
│   ├── globals.css                # Design system
│   ├── layout.tsx                 # Root layout with Providers
│   └── page.tsx                   # Landing page
├── components/
│   ├── ui/                        # shadcn components
│   ├── teams/                     # Team management
│   ├── invitations/               # Invitation UI
│   ├── shared/                    # Reusable patterns
│   ├── providers.tsx              # App providers
│   └── theme-toggle.tsx           # Theme switcher
├── hooks/
│   ├── use-teams.ts               # Team hooks
│   └── ...
├── lib/
│   ├── auth.ts                    # NextAuth config (Node.js runtime)
│   ├── auth.config.ts             # Auth config (callbacks, pages)
│   ├── api-helpers.ts             # withErrorHandler, requireTeamMember, etc.
│   ├── prisma.ts                  # Prisma client (lazy proxy)
│   ├── s3.ts                      # S3 utilities
│   ├── resend.ts                  # Email client
│   ├── query-client.ts            # React Query
│   ├── utils.ts                   # cn(), getInitials(), etc.
│   └── jobs/                      # pg-boss setup
├── proxy.ts                       # Security headers (NOT auth)
├── types/
│   └── next-auth.d.ts             # Auth type extensions
└── generated/
    └── prisma/                    # Prisma client output
```

## Related Asset Files

This skill includes ready-to-use templates:

| Asset | Description |
|-------|-------------|
| `assets/lib/auth.ts` | NextAuth v5 with Credentials provider |
| `assets/lib/auth.config.ts` | Auth config (callbacks, custom pages) |
| `assets/lib/api-helpers.ts` | withErrorHandler, requireTeamMember, ApiError |
| `assets/lib/prisma.ts` | Lazy-loaded Prisma client with pg adapter |
| `assets/lib/s3.ts` | S3 utilities with presigned URLs |
| `assets/lib/resend.ts` | Resend email client + templates |
| `assets/lib/query-client.ts` | React Query setup |
| `assets/lib/boss.ts` | pg-boss job queue |
| `assets/lib/utils.ts` | Utility functions |
| `assets/components/providers.tsx` | App providers |
| `assets/components/theme-toggle.tsx` | Light/dark/system toggle |
| `assets/components/team-switcher.tsx` | Team dropdown |
| `assets/config/globals.css` | Linear-style design system |
| `assets/config/Dockerfile` | Production Docker build |
| `assets/config/railway.toml` | Railway deployment |
| `assets/config/next.config.ts` | Next.js configuration |
| `assets/config/proxy.ts` | Security headers |
| `assets/config/.env.example` | Environment variables |
| `assets/config/components.json` | shadcn configuration |
| `assets/prisma/schema.prisma` | Base team schema |
| `assets/api/teams-route.ts` | Team API template |
| `assets/api/invitations-route.ts` | Invitations API template |
| `assets/hooks/use-teams.ts` | React Query hooks |
| `assets/types/next-auth.d.ts` | Type extensions |

## Setup Instructions

### 1. Initialize Project

```bash
bunx create-next-app@latest my-saas --typescript --tailwind --eslint --app --src-dir
cd my-saas
```

### 2. Install Dependencies

```bash
# Core
bun add next-auth@beta @auth/prisma-adapter bcryptjs
bun add @prisma/client @prisma/adapter-pg pg
bun add -D prisma @types/bcryptjs

# UI
bun add lucide-react
bun add next-themes class-variance-authority clsx tailwind-merge
bun add @tanstack/react-query

# Validation
bun add zod

# Email
bun add resend

# Storage
bun add @aws-sdk/client-s3 @aws-sdk/s3-request-presigner

# Jobs
bun add pg-boss

# shadcn
bunx shadcn@latest init
bunx shadcn@latest add button card dialog input label sonner tooltip dropdown-menu avatar badge form command popover
```

### 3. Configure Environment

Copy `.env.example` and fill in values:

```bash
# Required
DATABASE_URL="postgresql://..."
AUTH_SECRET="openssl rand -base64 32"
NEXTAUTH_URL="http://localhost:3000"
RESEND_API_KEY="re_..."
EMAIL_FROM="onboarding@resend.dev"

# S3 Storage (Railway)
AWS_ENDPOINT_URL="https://..."
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_S3_BUCKET_NAME="..."
AWS_DEFAULT_REGION="auto"
```

### 4. Setup Prisma

```bash
# Initialize
bunx prisma init

# Copy the schema from assets/prisma/schema.prisma
# Ensure generator uses "prisma-client" (not "prisma-client-js")
# Ensure output is "../src/generated/prisma"

# Push to database
bunx prisma db push
bunx prisma generate
```

### 5. Copy Asset Files

Copy the template files from `assets/` to your project, adjusting imports as needed.

## Design System

### Brand Colors

Primary purple: `#8b5cf6` (HSL: 262 83% 58%)

### Light Mode
- Background: `#ffffff`
- Foreground: `hsl(240 10% 10%)`
- Border: `hsl(240 6% 90%)`

### Dark Mode (Linear-style)
- Background: `#0A0A0B` (hsl 240 5% 4%)
- Foreground: `hsl(0 0% 95%)`
- Border: `rgba(255,255,255,0.06)`

### Theme Toggle

Three-option segmented control with icons only:
- Sun icon → Light
- Moon icon → Dark
- Monitor icon → System

Located in sidebar footer or header. Uses `next-themes` with `attribute="class"`.

### Typography

- Font: Geist Sans / Geist Mono
- Tight letter-spacing: -0.011em body, -0.02em headings
- Font smoothing: antialiased

## API Route Patterns

### Route Handler Signature (Next.js 15+)

**CRITICAL:** In Next.js 15+, `params` is a `Promise` and MUST be awaited:

```typescript
type RouteParams = {
  params: Promise<{ teamId: string }>;
};

export async function GET(req: NextRequest, { params }: RouteParams) {
  const { teamId } = await params;  // MUST await!
  // ...
}
```

### Using withErrorHandler (Recommended)

```typescript
import { NextRequest, NextResponse } from "next/server";
import { requireTeamMember, parseJsonBody, withErrorHandler, ApiError } from "@/lib/api-helpers";
import { prisma } from "@/lib/prisma";
import { z } from "zod";

const createSchema = z.object({
  name: z.string().min(1),
});

type RouteParams = {
  params: Promise<{ teamId: string }>;
};

export const POST = withErrorHandler(async (req: NextRequest, { params }: RouteParams) => {
  const { teamId } = await params;
  
  // Auth check - throws 401/403
  await requireTeamMember(teamId);
  
  // Parse and validate body - throws 400
  const { name } = await parseJsonBody(req, createSchema);
  
  // Business logic
  const result = await prisma.someModel.create({
    data: { name, teamId },
  });
  
  return NextResponse.json(result, { status: 201 });
});
```

### React Query Keys

```typescript
// Factory pattern for query keys
export const teamKeys = {
  all: ["teams"] as const,
  lists: () => [...teamKeys.all, "list"] as const,
  details: () => [...teamKeys.all, "detail"] as const,
  detail: (id: string) => [...teamKeys.details(), id] as const,
  members: (id: string) => [...teamKeys.detail(id), "members"] as const,
};
```

### Mutation Pattern (Simple Invalidation)

```typescript
export function useCreateTeam() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createTeam,
    onSuccess: (newTeam) => {
      queryClient.invalidateQueries({ queryKey: teamKeys.lists() });
      queryClient.setQueryData(teamKeys.detail(newTeam.id), newTeam);
    },
  });
}
```

## Background Jobs

### pg-boss Setup

Jobs run alongside Next.js in the same container via startup script.

Queue pattern:
```typescript
// Create job
await boss.send(QUEUES.SEND_EMAIL, payload, DEFAULT_JOB_OPTIONS);

// Worker handles job
boss.work(QUEUES.SEND_EMAIL, { batchSize: 1 }, async (job) => {
  await handleSendEmail(job.data);
});
```

### Scheduled Jobs

```typescript
// Schedule recurring jobs on worker startup
await boss.schedule(QUEUES.CLEANUP, "0 6 * * *", {}); // Daily at 6 AM UTC
```

## Deployment

### Dockerfile

Single container running both Next.js server and pg-boss worker:

```dockerfile
FROM node:22-alpine
RUN npm install -g bun
# ... build steps ...
CMD ["/app/start.sh"]  # Runs both processes
```

### Railway Config

```toml
[build]
builder = "dockerfile"

[deploy]
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
```

### next.config.ts Rewrites

```typescript
async rewrites() {
  return [
    {
      source: "/uploads/:path*",
      destination: "/api/uploads/:path*",
    },
  ];
}
```

## Checklist

- [ ] Project initialized with Next.js + TypeScript
- [ ] Dependencies installed (see list above)
- [ ] Environment variables configured
- [ ] Prisma schema with User, Team, TeamMember, Invitation
- [ ] NextAuth v5 with Credentials provider
- [ ] Dashboard layout with server-side auth check
- [ ] API helpers (withErrorHandler, requireTeamMember, etc.)
- [ ] proxy.ts for security headers
- [ ] Team creation and switching
- [ ] Member invitation flow
- [ ] Light/dark mode toggle
- [ ] React Query configured
- [ ] Resend email service
- [ ] S3 storage with /uploads proxy
- [ ] pg-boss for background jobs
- [ ] Dockerfile for Railway deployment
