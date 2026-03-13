---
name: frontend-architecture
description: Recommends and scaffolds frontend technology stack for new projects. Use when starting a new frontend project, selecting a framework, setting up a web app from scratch, or when the user asks about frontend tech stack, scaffolding, or architecture selection. Covers React/Next.js/Astro/Vue, TypeScript, Tailwind CSS, state management, data fetching, UI components, testing, and monorepo setup.
---

# Frontend Architecture Selection

Guides frontend technology stack selection and project scaffolding for new or empty projects.

## Step 1: Clarify Requirements

Before recommending a stack, MUST ask (or infer from context):

| Question | Options | Impact |
|----------|---------|--------|
| Rendering mode | SPA / SSR / SSG / Hybrid | Determines framework |
| Content type | Dashboard / Landing / Docs / App | Determines UI library |
| SEO required? | Yes / No | SSR vs SPA decision |
| Backend API | REST / GraphQL / gRPC-Web | Data layer strategy |
| Team size | Solo / Small / Large | Monorepo strategy |
| Backend stack | Go / Node / Other | Type-safe client gen |

## Step 2: Recommended Default Stack

When requirements are general-purpose (no strong constraints), recommend this stack:

```
Framework:      Next.js 15 (App Router)     # SSR + SPA hybrid, SEO-friendly
Language:       TypeScript 5.x (strict)     # Non-negotiable
Build:          Turbopack (built-in Next.js) / Vite (standalone SPA)
Styling:        Tailwind CSS v4
UI Components:  Ant Design v5
Global State:   Zustand
Server State:   TanStack Query v5
Forms:          React Hook Form + Zod
Package Mgr:    pnpm (preferred)
Testing:        Vitest + Testing Library + Playwright (E2E)
Linting:        ESLint v9 (flat config) + Prettier
```

## Step 3: Scenario-Based Selection

Use the decision tree below, then see [stacks.md](stacks.md) for full matrices.

```
New Frontend Project
        │
        ├─ SEO / SSR required? ──────▶ Next.js 15 (App Router)
        │
        ├─ Content / Docs / Blog? ───▶ Astro 5
        │
        ├─ Vue team? ────────────────▶ Nuxt 3 (mirrors Next.js)
        │
        └─ General SPA ──────────────▶ React 19 + Vite + Ant Design v5
```

## Step 4: Confirm Stack & Update README.md

After the user confirms the tech stack, **MUST** update (or create) the project's `README.md` with a Tech Stack section.

Template to insert/append:

```markdown
## Tech Stack

| Layer | Choice |
|-------|--------|
| Framework | <!-- e.g. Next.js 15 (App Router) --> |
| Language | TypeScript 5.x (strict) |
| Build | <!-- e.g. Turbopack / Vite --> |
| Styling | <!-- e.g. Tailwind CSS v4 --> |
| UI Components | <!-- e.g. Ant Design v5 --> |
| Global State | <!-- e.g. Zustand --> |
| Server State | <!-- e.g. TanStack Query v5 --> |
| Forms | <!-- e.g. React Hook Form + Zod --> |
| Package Manager | pnpm |
| Testing | Vitest + Testing Library + Playwright |
| Linting | ESLint v9 + Prettier |
```

Rules:
- If `README.md` already exists: append the Tech Stack section; **do NOT overwrite** existing content.
- If `README.md` does not exist: create it with project name as heading and the Tech Stack section.
- Fill in each row with the actual confirmed choices, removing placeholder comments.

## Step 5: Go Backend Integration

When the backend is Go (common in this workspace):

- **Type-safe API client**: Use [Orval](https://orval.dev/) or [Hey API](https://heyapi.dev/) to auto-generate TypeScript client from OpenAPI/Swagger spec — eliminates manual type definitions
- **Auth (JWT)**: Handle token refresh in TanStack Query's `defaultOptions` or axios interceptor
- **CORS**: Confirm Go handler sets correct headers for the frontend origin

## Step 6: Scaffold the Project

After README.md is updated, run the appropriate init commands.  
See [templates/nextjs.md](templates/nextjs.md), [templates/vite-spa.md](templates/vite-spa.md), or [templates/astro.md](templates/astro.md) for exact commands.

## Project Structure Convention

Follow Feature-Sliced Design (aligned with Go Clean Architecture on the backend):

```
src/
├── app/          # App-level setup: providers, router, global styles
├── pages/        # Route-level components (or Next.js app/ dir)
├── features/     # Feature modules: each has ui/, model/, api/
├── shared/       # Reusable: ui components, lib, types, hooks
└── entities/     # Domain models (aligned with backend domain layer)
```

## Code Quality Checklist

- [ ] TypeScript `strict: true` enabled in tsconfig
- [ ] ESLint + Prettier configured with pre-commit hook (Husky + lint-staged)
- [ ] Path aliases (`@/`) configured in tsconfig and build tool
- [ ] Environment variables typed (e.g. `env.d.ts` or `t3-env`)
- [ ] Zod schemas colocated with forms / API boundaries
- [ ] TanStack Query keys in a central `queryKeys.ts` file
- [ ] Tests: unit (Vitest), component (Testing Library), E2E (Playwright)

## Reference

- Full technology stack matrices → [stacks.md](stacks.md)
- Next.js scaffold commands → [templates/nextjs.md](templates/nextjs.md)
- Vite SPA scaffold commands → [templates/vite-spa.md](templates/vite-spa.md)
- Astro scaffold commands → [templates/astro.md](templates/astro.md)
