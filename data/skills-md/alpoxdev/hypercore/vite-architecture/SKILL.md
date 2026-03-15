---
name: vite-architecture
description: Use when working on Vite + TanStack Router projects - enforces architecture rules (layers, routes, hooks, services, conventions) with mandatory validation before any code change. Triggers on file creation, route work, hook patterns, or any structural change in a Vite + TanStack Router codebase.
---

# Vite + TanStack Router Architecture Enforcement

## Overview

Enforces hypercore Vite architecture rules with 100% compliance. Validates project structure, then applies strict layer/route/hook/convention rules to every code change.

**This skill is RIGID. Follow exactly. No exceptions.**

**REQUIRED:** When working on Vite + TanStack Router projects, ALWAYS use this skill together with `/oh-my-claudecode:ralph` to guarantee 100% architecture compliance.

## Step 1: Project Validation

Before any work, confirm Vite + TanStack Router project:

```bash
# Check for Vite + TanStack Router indicators (ANY of these)
grep -r "@tanstack/react-router" package.json 2>/dev/null
grep -r "vite" package.json 2>/dev/null
ls vite.config.ts 2>/dev/null
ls src/routes/__root.tsx 2>/dev/null
```

If NONE found: **STOP. This skill does not apply.** Inform user.

If found: proceed with architecture enforcement.

> **Note:** If `@tanstack/react-start` is present, use `tanstack-start-architecture` instead.

## Step 2: Read Architecture Rules

Load the detailed rules reference:

**REQUIRED:** Read `architecture-rules.md` in this skill directory before writing any code.

For detailed patterns and examples, also read the relevant reference files:
- `rules/conventions.md` - Code conventions (naming, TypeScript, imports, comments)
- `rules/routes.md` - Route structure (folder rules, patterns, loaders)
- `rules/services.md` - API Services (schemas, queries, mutations)
- `rules/hooks.md` - Custom Hook patterns (separation rules, internal order)

## Step 3: Pre-Change Validation Checklist

Before writing ANY code, verify your planned change against these gates:

### Gate 1: Layer Violations

```
Routes -> Services -> External API
```

| Check | Rule |
|-------|------|
| Route calling fetch/axios directly? | BLOCKED. Must go through Services |
| Hook calling fetch/axios directly? | BLOCKED. Must go through Services |
| Service returning raw Response? | BLOCKED. Must return typed data |
| `createServerFn` anywhere? | BLOCKED. This is a Vite project, no server functions |

### Gate 2: Route Structure

| Check | Rule |
|-------|------|
| Flat file route? (`routes/users.tsx`) | BLOCKED. Use folder (`routes/users/index.tsx`) |
| Missing `-components/` folder? | BLOCKED. Every page needs it |
| Missing `-hooks/` folder? | BLOCKED. Every page needs it |
| `-functions/` folder present? | BLOCKED. No server functions in Vite |
| `const Route` without `export`? | BLOCKED. Must be `export const Route` |
| Logic in page component? | BLOCKED. Extract to `-hooks/` |
| Layout route missing `route.tsx`? | BLOCKED. Routes needing beforeLoad/loader must have `route.tsx` |
| Route with search params but no `validateSearch`? | BLOCKED. Must use `zodValidator` with `validateSearch` |
| Route without `pendingComponent`? | WARNING. Recommended for all routes with loaders |

### Gate 3: Services

| Check | Rule |
|-------|------|
| POST/PUT/PATCH without schema validation? | BLOCKED. Validate with Zod before calling |
| Direct `fetch`/`axios` in route or hook? | BLOCKED. Use service functions |
| `services/index.ts` barrel export? | BLOCKED. Import directly from individual files |
| Missing return type on service function? | BLOCKED. Always explicit typed return |

### Gate 4: Hooks

| Check | Rule |
|-------|------|
| Hook inside page component? | BLOCKED. Must be in `-hooks/` folder |
| Wrong hook order? | BLOCKED. State -> Global -> Query -> Handlers -> Memo -> Effect |
| Missing return type interface? | BLOCKED |
| camelCase hook filename? | BLOCKED. Use `use-kebab-case.ts` |
| `useServerFn` in hook? | BLOCKED. No server functions in Vite |

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
- [ ] Layer architecture respected (Routes -> Services -> External API)
- [ ] Route uses folder structure with -components/, -hooks/
- [ ] export const Route = createFileRoute(...) used
- [ ] No server functions (createServerFn, useServerFn) anywhere
- [ ] Search params use zodValidator from @tanstack/zod-adapter
- [ ] Custom Hooks in -hooks/ with correct internal order
- [ ] All filenames kebab-case
- [ ] Korean block comments present
- [ ] const arrow functions with explicit return types
```

## Step 5: Post-Change Verification

After writing code, verify:

1. **Structure check**: `ls` the route folder - confirm `-components/`, `-hooks/` exist (no `-functions/`)
2. **Export check**: grep for `export const Route` in route files
3. **Layer check**: no direct fetch/axios in route or hook files
4. **Convention check**: no camelCase filenames, no `function` keyword declarations
5. **Hook order check**: read hook files, verify State -> Global -> Query -> Handlers -> Memo -> Effect

## Quick Reference: Folder Structure

```
src/
├── routes/                    # File-based routing
│   └── <page>/
│       ├── index.tsx          # Page (UI only)
│       ├── route.tsx          # Layout (beforeLoad, loader)
│       ├── -components/       # REQUIRED: page components
│       ├── -hooks/            # REQUIRED: page hooks (ALL logic here)
│       └── -sections/         # Optional: 200+ line pages
├── services/<domain>/         # API service wrappers
│   ├── schemas.ts
│   ├── queries.ts
│   └── mutations.ts
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
| `createServerFn(...)` | Use service function + React Query |
| `useServerFn(...)` | Use `useQuery` / `useMutation` directly |
| Direct `fetch()` in hook | Extract to `services/<domain>/queries.ts` |
| Logic in page component | Extract to `-hooks/use-*.ts` |
| `-functions/` folder in route | Remove; no server functions in Vite |
| `lib/store` folder | Use `stores/` |
| Hook with mixed order | Follow: State -> Global -> Query -> Handlers -> Memo -> Effect |
| `getUserById.ts` filename | `get-user-by-id.ts` |
| `function doThing() {}` | `const doThing = (): ReturnType => {}` |
| Direct Zod schema in `validateSearch` | Use `zodValidator(schema)` from `@tanstack/zod-adapter` |

## Red Flags - STOP and Fix

- Route or hook importing `fetch`/`axios` directly
- Missing `export` on `const Route`
- Page component with `useState`, `useQuery` etc. inline (not in hook)
- `createServerFn` or `useServerFn` anywhere in the codebase
- `any` type anywhere
- camelCase filenames
- `-functions/` folder inside route
- Route using search params without `validateSearch`
