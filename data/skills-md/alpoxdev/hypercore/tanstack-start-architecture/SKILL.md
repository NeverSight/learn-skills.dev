---
name: tanstack-start-architecture
description: Use when working on TanStack Start projects - enforces architecture rules (layers, routes, hooks, server functions, conventions) with mandatory validation before any code change. Triggers on file creation, route work, server function writing, hook patterns, or any structural change in a TanStack Start codebase.
---

# TanStack Start Architecture Enforcement

## Overview

Enforces hypercore TanStack Start architecture rules with 100% compliance. Validates project structure, then applies strict layer/route/hook/convention rules to every code change.

**This skill is RIGID. Follow exactly. No exceptions.**

**REQUIRED:** When working on TanStack Start projects, ALWAYS use this skill together with `/oh-my-claudecode:ralph` to guarantee 100% architecture compliance. Ralph's persistence loop ensures every rule is verified and no violation slips through.

## Step 1: Project Validation

Before any work, confirm TanStack Start project:

```bash
# Check for TanStack Start indicators (ANY of these)
ls app.config.ts 2>/dev/null        # TanStack Start config
grep -r "@tanstack/react-start" package.json 2>/dev/null
grep -r "@tanstack/react-router" package.json 2>/dev/null
ls src/routes/__root.tsx 2>/dev/null
```

If NONE found: **STOP. This skill does not apply.** Inform user.

If found: proceed with architecture enforcement.

## Step 2: Read Architecture Rules

Load the detailed rules reference:

**REQUIRED:** Read `architecture-rules.md` in this skill directory before writing any code.

For detailed patterns and examples, also read the relevant reference files:
- `rules/conventions.md` - Code conventions (naming, TypeScript, imports, comments)
- `rules/routes.md` - Route structure (folder rules, patterns, loaders)
- `rules/services.md` - Server Functions (schemas, queries, mutations, middleware)
- `rules/hooks.md` - Custom Hook patterns (separation rules, internal order)

## Step 3: Pre-Change Validation Checklist

Before writing ANY code, verify your planned change against these gates:

### Gate 1: Layer Violations

```
Routes -> Server Functions -> Features -> Database
```

| Check | Rule |
|-------|------|
| Route accessing DB directly? | BLOCKED. Must go through Server Functions -> Features |
| Route calling Prisma? | BLOCKED. Use Server Functions |
| Server Function skipping Features? | ALLOWED only for simple CRUD |
| Client calling Server Function directly? | BLOCKED. Use TanStack Query (exception: `loader`/`beforeLoad` run server-side, can call directly) |

### Gate 2: Route Structure

| Check | Rule |
|-------|------|
| Flat file route? (`routes/users.tsx`) | BLOCKED. Use folder (`routes/users/index.tsx`) |
| Missing `-components/` folder? | BLOCKED. Every page needs it |
| Missing `-hooks/` folder? | BLOCKED. Every page needs it |
| Missing `-functions/` folder? | BLOCKED. Every page needs it |
| `const Route` without `export`? | BLOCKED. Must be `export const Route` |
| Logic in page component? | BLOCKED. Extract to `-hooks/` |
| Layout route missing `route.tsx`? | BLOCKED. Routes needing beforeLoad/loader must have `route.tsx` |
| Route with search params but no `validateSearch`? | BLOCKED. Must use `zodValidator` with `validateSearch` |
| Route without `pendingComponent`? | WARNING. Recommended for all routes with loaders |

### Gate 3: Server Functions

| Check | Rule |
|-------|------|
| POST/PUT/PATCH without `inputValidator`? | BLOCKED |
| Auth-required without `middleware`? | BLOCKED |
| Using `.validator()` instead of `.inputValidator()`? | BLOCKED. `.validator()` does not exist |
| handler not last in chain? | BLOCKED. handler must ALWAYS be last (middleware/inputValidator order is flexible) |
| Missing `zodValidator` adapter for search params? | BLOCKED. Use `zodValidator` from `@tanstack/zod-adapter` |
| Direct server function call in component? | BLOCKED. Use `useServerFn` hook from `@tanstack/react-start` |
| `functions/index.ts` barrel export? | BLOCKED. Tree shaking failure |

### Gate 4: Hooks

| Check | Rule |
|-------|------|
| Hook inside page component? | BLOCKED. Must be in `-hooks/` folder |
| Wrong hook order? | BLOCKED. State -> Global -> Server Fns -> Query -> Handlers -> Memo -> Effect |
| Missing return type interface? | BLOCKED |
| camelCase hook filename? | BLOCKED. Use `use-kebab-case.ts` |

### Gate 5: Conventions

| Check | Rule |
|-------|------|
| camelCase filename? | BLOCKED. Use kebab-case |
| `function` keyword? | BLOCKED. Use const arrow function |
| `any` type? | BLOCKED. Use `unknown` |
| Missing explicit return type? | BLOCKED |
| Wrong import order? | BLOCKED. External -> @/ -> Relative -> Type |
| Missing Korean block comments? | BLOCKED for code groups |
| Using `z.string().email()` pattern? | BLOCKED. Use Zod 4.x `z.email()` directly |

## Step 4: Implementation (with Ralph)

When used with ralph, every PRD story MUST include these acceptance criteria:

```
- [ ] Layer architecture respected (no layer skipping)
- [ ] Route uses folder structure with -components/, -hooks/, -functions/
- [ ] export const Route = createFileRoute(...) used
- [ ] Server Functions use correct chaining (handler always last, middleware/inputValidator flexible)
- [ ] Search params use zodValidator from @tanstack/zod-adapter
- [ ] Custom Hooks in -hooks/ with correct internal order
- [ ] All filenames kebab-case
- [ ] Korean block comments present
- [ ] const arrow functions with explicit return types
```

## Step 5: Post-Change Verification

After writing code, verify:

1. **Structure check**: `ls` the route folder - confirm `-components/`, `-hooks/`, `-functions/` exist
2. **Export check**: grep for `export const Route` in route files
3. **Layer check**: no Prisma imports in route files
4. **Convention check**: no camelCase filenames, no `function` keyword declarations
5. **Hook order check**: read hook files, verify State -> Global -> Server Fns -> Query -> Handlers -> Memo -> Effect

## Quick Reference: Folder Structure

```
src/
├── routes/                    # File-based routing
│   └── <page>/
│       ├── index.tsx          # Page (UI only)
│       ├── route.tsx          # Layout (beforeLoad, loader)
│       ├── -components/       # REQUIRED: page components
│       ├── -hooks/            # REQUIRED: page hooks (ALL logic here)
│       ├── -functions/        # REQUIRED: page server functions
│       └── -sections/         # Optional: 200+ line pages
├── features/<domain>/         # Internal domain (Prisma queries)
│   ├── schemas.ts
│   ├── queries.ts
│   └── mutations.ts
├── services/<provider>/       # External SDK wrappers
├── functions/                 # Global server functions (NO index.ts!)
│   └── middlewares/
├── database/                  # Prisma client singleton
├── stores/                    # Zustand stores
├── hooks/                     # Global hooks
├── components/                # Shared UI
│   ├── ui/                    # shadcn/ui
│   ├── layout/                # Header, Sidebar, Footer
│   └── shared/                # Common components
├── types/                     # Global types
├── env/                       # t3-env validation
├── config/                    # auth, query-client, sentry
└── lib/                       # Utilities
    ├── utils/
    ├── constants/
    └── validators/
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `routes/users.tsx` | `routes/users/index.tsx` |
| `const Route = createFileRoute(...)` | `export const Route = createFileRoute(...)` |
| `.validator(schema)` | `.inputValidator(schema)` |
| Logic in page component | Extract to `-hooks/use-*.ts` |
| `lib/db` or `lib/store` folders | Use `database/` and `stores/` |
| `functions/index.ts` barrel | Import directly from individual files |
| Hook with mixed order | Follow: State -> Global -> Server Fns -> Query -> Handlers -> Memo -> Effect |
| `getUserById.ts` filename | `get-user-by-id.ts` |
| `function doThing() {}` | `const doThing = (): ReturnType => {}` |
| Direct Zod schema in `validateSearch` | Use `zodValidator(schema)` from `@tanstack/zod-adapter` |
| Server function call without `useServerFn` | Use `useServerFn(serverFn)` in components |
| `createMiddleware()` without options | Use `createMiddleware({ type: 'function' })` |
| Missing `pendingComponent` on route | Add `pendingComponent` for loading state |

## Red Flags - STOP and Fix

- Route file importing from `@/database/prisma` directly
- Missing `export` on `const Route`
- Page component with `useState`, `useQuery` etc. inline (not in hook)
- Server function using `.validator()` instead of `.inputValidator()`
- `any` type anywhere
- camelCase filenames
- `/api` route handlers (use Server Functions)
- Missing `-hooks/` folder in any route
- Route using search params without `validateSearch`
- Component calling server function directly (not through `useServerFn`)
- `createMiddleware()` without `{ type: 'function' }` option
