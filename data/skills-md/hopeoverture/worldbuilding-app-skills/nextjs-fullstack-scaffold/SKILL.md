---
name: nextjs-fullstack-scaffold
description: This skill should be used when the user requests to scaffold, create, or initialize a full-stack Next.js application with a modern tech stack including Next.js 16, React 19, TypeScript, Tailwind CSS v4, shadcn/ui, Supabase auth, Prisma ORM, and comprehensive testing setup. Use it for creating production-ready starter templates with authentication, protected routes, forms, and example features. Trigger terms scaffold, create nextjs app, initialize fullstack, starter template, boilerplate, setup nextjs, production template, full-stack setup, nextjs supabase, nextjs prisma.
---

# Next.js Full-Stack Scaffold

To scaffold a production-grade Next.js 16 full-stack application with modern tooling and best practices, follow these steps systematically.

## Prerequisites Check

Before scaffolding, verify the target directory:
1. Confirm the current working directory is where files should be generated
2. Check if directory is empty or if user wants to override existing files
3. Confirm user wants to proceed with scaffold generation

## Step 1: Gather Project Information

Prompt the user for the following details using the AskUserQuestion tool:
- Project name (for package.json)
- Project description
- Author name

Use sensible defaults if user prefers to skip.

## Step 2: Create Folder Structure

Create the complete folder structure as defined in `assets/folder-structure.txt`. Generate all necessary directories by writing files to them (directories are created automatically).

## Step 3: Generate Configuration Files

Create all configuration files in the project root. Consult `references/stack-architecture.md` for architectural guidance.

### Essential Config Files

Generate these files using Write tool:
- **package.json** - Use template from `assets/templates/package.template.json`, replacing placeholders
- **tsconfig.json** - TypeScript config with strict mode and path aliases
- **next.config.ts** - Next.js configuration with server actions
- **tailwind.config.ts** - Tailwind v4 with dark mode and shadcn/ui colors
- **postcss.config.mjs** - PostCSS with Tailwind plugin
- **eslint.config.mjs** - ESLint v9 flat config
- **prettier.config.js** - Prettier with Tailwind plugin
- **.gitignore** - Standard Next.js ignore patterns
- **.env.example** - Environment variable template
- **vitest.config.ts** - Vitest test configuration
- **playwright.config.ts** - Playwright E2E configuration

## Step 4: Generate App Router Files

Create all Next.js app router files following RSC conventions.

### Root Files
- `app/layout.tsx` - Root layout with metadata and providers
- `app/page.tsx` - Landing page
- `app/globals.css` - Tailwind directives and CSS variables

### Authentication Routes
- `app/(auth)/layout.tsx` - Auth layout (centered)
- `app/(auth)/login/page.tsx` - Login page with form

### Protected Routes
- `app/(protected)/layout.tsx` - Protected layout with auth check
- `app/(protected)/dashboard/page.tsx` - Dashboard with stats
- `app/(protected)/profile/page.tsx` - User profile page
- `app/(protected)/data/page.tsx` - Data table page

### API Routes
- `app/api/data/route.ts` - Example API endpoint

### Middleware
- `middleware.ts` - Supabase auth middleware

## Step 5: Generate UI Components

Create shadcn/ui components in `components/ui/`:
- `button.tsx`, `card.tsx`, `input.tsx`, `label.tsx`, `form.tsx`, `table.tsx`, `dropdown-menu.tsx`, `avatar.tsx`

Create custom components:
- `components/providers.tsx` - App providers with Toaster
- `components/layout/header.tsx` - Header with navigation
- `components/layout/sidebar.tsx` - Sidebar navigation
- `components/layout/nav.tsx` - Navigation links
- `components/auth/login-form.tsx` - Login form with RHF + Zod
- `components/auth/auth-button.tsx` - Sign in/out button
- `components/dashboard/stats-card.tsx` - Stats display card
- `components/dashboard/data-table.tsx` - Interactive data table

All components must be TypeScript and accessible.

## Step 6: Generate Lib Files

Create utility and action files:

### Utilities
- `lib/utils.ts` - cn() function and utilities
- `lib/prisma.ts` - Prisma client singleton

### Supabase Clients
- `lib/supabase/client.ts` - Client-side Supabase client
- `lib/supabase/server.ts` - Server-side Supabase client
- `lib/supabase/middleware.ts` - Middleware helper

### Server Actions (all must start with `'use server'`)
- `lib/actions/auth.ts` - signIn(), signOut()
- `lib/actions/user.ts` - updateProfile()
- `lib/actions/data.ts` - CRUD operations

### Validation Schemas (Zod)
- `lib/validations/auth.ts` - Login/signup schemas
- `lib/validations/user.ts` - Profile update schema
- `lib/validations/data.ts` - Data CRUD schemas

## Step 7: Generate Prisma Schema

Create `prisma/schema.prisma`:
- PostgreSQL datasource with connection pooling
- User model (id, email, name, timestamps)
- Item model (example data model with relations)
- Proper indexes and constraints

Create `prisma/seed.ts`:
- TypeScript seed script
- Sample users and items

## Step 8: Generate Tests

Create test files:
- `tests/unit/utils.test.ts` - Unit test for utilities
- `tests/integration/auth.test.tsx` - Integration test for auth
- `tests/e2e/login.spec.ts` - E2E test for login flow

## Step 9: Generate CI Workflow

Create `.github/workflows/ci.yml`:
- Lint, type check, test, build jobs
- Run on push and PR

## Step 10: Generate README

Create comprehensive `README.md` with:
- Project overview and tech stack
- Prerequisites and installation steps
- Environment setup instructions
- Database setup (Prisma commands)
- Development and testing commands
- Deployment guide
- Folder structure explanation

## Step 11: Final Verification

After generating all files:
1. Confirm all files were created successfully
2. List the folder structure for user review
3. Provide next steps for installation and setup

## Implementation Notes

### TypeScript
- All files must use TypeScript
- Proper type annotations
- No `any` types unless necessary

### Server Components
- Use Server Components by default
- Only add `"use client"` when required for interactivity

### Accessibility
- Use shadcn/ui accessible components
- Include ARIA labels
- Ensure keyboard navigation

### Security
- Validate inputs with Zod
- Use Server Actions for mutations
- Never expose secrets to client

## Consulting References

Throughout scaffolding:
- Consult `references/stack-architecture.md` for patterns
- Consult `references/implementation-checklist.md` to track progress

## Completion

When finished:
1. Summarize what was created
2. List all major files and directories
3. Provide next steps
4. Offer to answer questions
