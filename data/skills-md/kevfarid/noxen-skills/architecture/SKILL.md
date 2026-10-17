---
name: architecture
description: >
  Use when deciding where new code should live in a React + TypeScript codebase —
  folder structure, feature modules, routing, service/adapter layers, import
  conventions, or file naming. Trigger on tasks like "where should this file go",
  "set up a new feature", "add a route", "create a service for this API call",
  or any question about project structure and organization. Do NOT trigger for
  visual/UI component styling or TypeScript typing questions specifically.
metadata:
  version: 1.0
  collection: noxen
---

# Noxen — Architecture

Part of the **Noxen** skill set (a personal engineering standard for React +
TypeScript + Tailwind). This skill covers project structure only — for
component patterns see `react-patterns`, for typing see `typescript`.

## Folder Structure

```
src/
├── core/               # App-level utilities (not feature-specific)
│   ├── config/         # Env vars, endpoints
│   ├── cx/             # clsx + tailwind-merge → import { cx } from '@/core/cx'
│   ├── http/           # Axios instance (VITE_API_URL base, Bearer token)
│   └── components/     # App-specific shared components (AppLogo, AppSearch…)
├── features/           # Self-contained feature modules
│   └── <feature>/
│       ├── pages/          # Route targets (one per route)
│       ├── components/     # Feature-scoped UI
│       ├── hooks/          # use-*.ts
│       ├── services/       # *.service.ts — pure async functions
│       ├── adapters/       # *.adapter.ts — API → UI type mapping
│       ├── types/          # *.types.ts
│       ├── router.ts       # Optional: feature-level routes
│       └── index.ts        # Public API — export only what others need
├── plugins/            # Registry-based extensibility
├── libs/               # Cross-feature logic (no feature imports)
├── ui/                 # Design system
└── resources/          # Images, icons, SVGs
```

Sub-features allowed: `src/features/patients/{list,create,detail}/`
Shared types across sub-features: `src/features/patients/shared/`

## Alternative Layering — Layered + Vertical-Slice

An equally valid variant, more common in larger apps or frameworks with a
server runtime (see `nextjs/app-router`): rename `features/` to `libs/`, add
a `provider/` slot per feature for feature-scoped React Context, and route
cross-cutting infra through `libs/core/` instead of `core/`. Pick one
variant per project and stay consistent — this is a naming difference, not
a different principle. This section is enough on its own; `ui-architecture`
is an optional complement, not a requirement — install it only if the repo
doesn't match either variant above and you need the full decision tree
(monorepo, Feature-Sliced Design, shadcn-vendored, …).

## Feature Module Rules

- **Self-contained**: pages, components, hooks, services live together
- **No cross-feature imports** — use `libs/` for shared logic
- **Public API** via `index.ts` — never import internal paths from outside

```ts
// ✅ Good
import { useEmailAuth } from "@/features/auth";

// ❌ Bad
import { useEmailAuth } from "@/features/auth/hooks/use-email-auth";
```

## Routing (React Router v7)

```tsx
// src/router.tsx
const callRoutes: RouteObject = {
  path: "/calls",
  children: [
    { index: true, element: <CallsPage /> },
    { path: ":id/summary", element: <CallSummaryPage /> },
  ],
};
```

- Routes defined per feature, composed in `src/router.tsx`
- Lazy-load all pages for code splitting
- Guard private routes with `<ProtectedRoute>` (uses Clerk `useUser`)

## Service Layer

Services = pure async functions. No hooks, no state.

```ts
// features/calls/services/call.service.ts
export const CallService = {
  getCalls: async (): Promise<ApiCallListItem[]> => {
    const { data } = await http.get("/api/calls", { params: { limit: 20 } });
    return data;
  },
};
```

## Adapter Layer

```ts
// features/calls/adapters/call.adapter.ts
export function adaptCallListItem(item: ApiCallListItem): CallListItem {
  return {
    id: item.correlation_id,
    patientName: item.patient_name,
    procedure: item.procedure,
  };
}
```

## Adapters vs. HTTP-Boundary Conversion — Pick One

The adapter layer above maps API shape to UI shape per-feature. An
alternative is to centralize *shape* conversion (e.g. snake_case →
camelCase) in the HTTP client's interceptors instead — see `http-layer`.
Use `adapters/` for feature-specific remapping (renaming/dropping/deriving
fields); use the HTTP boundary for conversions that are the same for every
response in the app. Don't do both for the same field — if the interceptor
already normalizes case, an adapter that also does it is dead code waiting
to drift.

## Import Convention — Always `@/`

```ts
import { cx } from "@/core/cx";
import { http } from "@/core/http";
import { Button } from "@/ui";
import { useCalls } from "@/features/calls";

// Relative only within the same feature
import { CallRow } from "./call-row";
```

## Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Files | kebab-case | `call-row.tsx` |
| Components | PascalCase | `CallRow` |
| Hooks | use-feature-name | `use-calls.ts` → `useCalls` |
| Services | feature.service.ts | `call.service.ts` |
| Adapters | feature.adapter.ts | `call.adapter.ts` |
| Types | feature.types.ts | `call.types.ts` |
| Pages | name-page.tsx | `calls-page.tsx` |
| Constants | SCREAMING_SNAKE | `MAX_RETRY_COUNT` |

## Hard Rules

- Never create cross-feature imports — route shared logic through `libs/`
- Every feature exposes its API through `index.ts` only
- Always use the `@/` import alias, never deep relative paths across folders
- On Next.js App Router, load `nextjs/app-router` first — routing and where pages live changes (see that skill's delta table)
