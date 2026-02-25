---
name: feature-sliced-design
description: Use when the user asks to implement FSD, use Feature-Sliced Design, organize architecture, structure project folders, set up FSD layers, create feature slices, refactor to FSD, or mentions feature slices, layered architecture, FSD methodology, views layer, entities layer, shared layer, Next.js with FSD. Provides comprehensive guidance for implementing Feature-Sliced Design (FSD v2.1) in Next.js applications. Optional monorepo (Turborepo) support - see references/monorepo.md.
license: MIT
metadata:
  version: 0.4.0
---

# Feature-Sliced Design Architecture

## Overview

Provides guidance for implementing Feature-Sliced Design (FSD v2.1) in Next.js applications. FSD organizes code into a layered hierarchy that prevents circular dependencies and promotes maintainability.

### Next.js Customization (Only Difference from Official FSD)

This skill adapts FSD for **Next.js App Router** with one structural choice:

| Official FSD | This Skill (Next.js) |
|--------------|----------------------|
| `app/` (routing, providers) + `pages/` (page logic) | **`src/app/`** = Next.js routing + FSD App merged |
| `pages/` layer | **`src/views/`** — page business logic |
| Separate routing layer | Next.js file-based routing (`page.tsx`, `layout.tsx`) |

**`src/app/`** holds both Next.js routing files (`layout.tsx`, `page.tsx`, route groups) and FSD App layer concerns (providers, styles). `page.tsx` imports from `@/views` and renders. All other FSD rules (layers, slices, segments, public API, import rules) align with [FSD v2.1](https://feature-sliced.design/).

**Reference files** (load as needed):

- [layers-and-segments.md](./references/layers-and-segments.md) — Layer definitions, slices (zero coupling, slice groups), segment patterns, migration
- [public-api.md](./references/public-api.md) — Public API rules, @x cross-imports, shared/ui structure, circular imports
- [code-smells.md](./references/code-smells.md) — Desegmentation, generic folders anti-patterns
- [examples.md](./references/examples.md) — Full examples: layers, auth patterns, types, API requests
- [react-query.md](./references/react-query.md) — React Query + FSD: Query Factory, pagination, QueryProvider
- [monorepo.md](./references/monorepo.md) — *(Optional)* Turborepo + FSD structure

---

## Purpose

Feature-Sliced Design (FSD) is an architectural methodology for organizing frontend applications into a standardized, scalable structure. It provides clear separation of concerns through a layered hierarchy that prevents circular dependencies and promotes maintainability.

### Why use FSD

- **Scalability**: Grows naturally as your application expands
- **Maintainability**: Clear boundaries make refactoring safer
- **Team collaboration**: Consistent structure enables parallel development
- **Onboarding**: New developers understand architecture quickly

### Unified `src/app/` structure

Both Next.js App Router and FSD App layer live in **`src/app/`**. Next.js recognizes `layout.tsx`, `page.tsx`, etc. inside `src/app/`, so all code stays under `src/` without a root-level `app/` folder, aligning with [FSD v2.1](https://feature-sliced.design/docs/reference/layers).

### Custom 'views' layer

This skill uses 'views' instead of the standard FSD 'pages' layer. Page business logic goes in `/src/views`; routing structure stays in `/src/app/`.

## When to Use

Apply Feature-Sliced Design when:

- Starting new Next.js projects that require clear architectural boundaries
- Refactoring growing codebases that lack consistent structure
- Working with multi-developer teams needing standardized organization
- Building applications with complex business logic requiring separation of concerns
- Scaling applications where circular dependencies become problematic
- Creating enterprise applications with long-term maintenance requirements
- *(Optional)* Developing monorepo applications (Turborepo, etc.) — see [monorepo.md](./references/monorepo.md)

## Core Principles (FSD v2.1)

### Layer Hierarchy

FSD v2.1 organizes code into **7 layers** (from most to least responsibility/dependency):

1. **app** - App-wide matters (entrypoint, providers, global styles, router config)
2. **processes** - **Deprecated**; move contents to `features` and `app`
3. **views** - Page-level business logic (custom naming; standard FSD uses 'pages')
4. **widgets** - Large self-sufficient UI blocks
5. **features** - Main user interactions and business value
6. **entities** - Business domain objects and models
7. **shared** - Foundation (UI kit, API client, libs, config)

You don't have to use every layer — add only what brings value. Most projects use at least Shared, Pages (or views), and App.

**FSD v2.1 pages-first:** Start with pages/views; keep most logic there. Extract to features/entities only when code is reused across several pages.

**Import rule:** A module can only import from layers **strictly below** it.

```
┌─────────────────┐
│      app        │  ← Can import from all layers below
├─────────────────┤
│     views       │  ← Can import: widgets, features, entities, shared
├─────────────────┤
│    widgets      │  ← Can import: features, entities, shared
├─────────────────┤
│    features     │  ← Can import: entities, shared
├─────────────────┤
│    entities     │  ← Can import: shared only
├─────────────────┤
│     shared      │  ← Cannot import from any FSD layer
└─────────────────┘
```

### 'Views' vs 'Pages' Layer

- **`src/app/`**: Next.js routing + FSD App layer — `layout.tsx`, `page.tsx`, route groups, providers, styles. `page.tsx` imports from `@/views` and renders.
- **`src/views/`**: Page business logic, component composition — View components, models, API calls. Composes widgets, features, entities.

### Slices and Public API

**Slices** are domain-based partitions within layers (except app and shared). Examples: `views/dashboard`, `widgets/header`, `features/auth`, `entities/user`.

- **Zero coupling, high cohesion** — Slices should be independent (no same-layer imports) and contain related code.
- **Slice groups** — Related slices can live in a folder, but **no code sharing** between them inside that folder.
- Each slice exports through `index.ts`. Use explicit exports — avoid `export * from`. Consumers import from public API only.

See [public-api.md](./references/public-api.md) for circular import rules, shared/ui structure, and @x cross-imports.

### Segments

Segments group code by **purpose (why)**, not essence (what). Avoid `components`, `hooks`, `types`, `utils` — use purpose-based names.

- **ui/** - React components, visual elements
- **model/** - Business logic, state management, TypeScript types
- **api/** - API clients, data fetching, external integrations
- **lib/** - One area of focus per library; document in README
- **config/** - Configuration constants, feature flags

**Shared layer segments:** `api`, `ui`, `lib`, `config`, `i18n`, `routes`

### Naming Conventions

| Target | Convention | Example |
|--------|------------|---------|
| Folders, slices | kebab-case | `user-profile/`, `theme-toggle/` |
| Component files | kebab-case | `login-form.tsx`, `user-card.tsx` |
| Hook files | camelCase | `useAuth.ts`, `useDashboard.ts` |
| Store files | camelCase | `authStore.ts` |
| Function/API collections | camelCase | `userApi.ts`, `formatDate.ts` |

## FSD with Next.js App Router

Next.js recognizes routing files inside `src/app/`. All FSD layers live under `src/`; **no root-level `app/` folder**.

**File organization:**

```
my-nextjs-app/
├── src/
│   ├── app/                    # Next.js routing + FSD App layer
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── dashboard/page.tsx
│   │   ├── providers/
│   │   └── styles/
│   ├── views/
│   ├── widgets/
│   ├── features/
│   ├── entities/
│   └── shared/
│       ├── ui/
│       ├── lib/
│       └── api/
└── package.json
```

**Routing pages import from views:**

```typescript
// src/app/dashboard/page.tsx
import { DashboardView } from '@/views/dashboard';
export default function DashboardPage() {
  return <DashboardView />;
}
```

*(Optional)* **Monorepo:** See [monorepo.md](./references/monorepo.md)

For full directory structure and layer examples, see [references](./references/).

## Workflow

### Step 1: Set Up Layer Directories

```bash
mkdir -p src/{app,views,widgets,features,entities,shared}
mkdir -p src/app/{providers,styles,config}
mkdir -p src/shared/{ui,lib,api,config}
```

### Step 2: Create First Entity

Start with entities (bottom layer). Define core business models in `entities/{name}/model/` and API in `entities/{name}/api/`. Export via `index.ts`.

### Step 3: Build Features Using Entities

Create features in `features/{name}/`. Features import from entities and shared only.

### Step 4: Compose Widgets from Features

Build composite widgets in `widgets/{name}/`. Widgets can import from features, entities, shared.

### Step 5: Assemble Views

Create page-level views in `views/{name}/`. Views compose widgets, features, entities.

### Step 6: Connect to App Router

Wire views to Next.js routing. `page.tsx` imports from `@/views/{slice}`.

## Import Rules

### Allowed

- Layer importing from layer below
- Any layer importing from shared
- Slice importing different slice in lower layer

### Forbidden

- Layer importing from same or higher layer
- Cross-slice imports within same layer
- Shared importing from FSD layers

### Fixing Circular Dependencies

1. Extract shared logic to lower layer (entities or shared)
2. Create higher layer (widget) that imports both
3. Review if slice should be split

## Public API Enforcement

Always use `index.ts` to control exports. Import from public API only:

```typescript
// ✅ Correct
import { LoginForm } from '@/features/auth';

// ❌ Wrong (deep import)
import { LoginForm } from '@/features/auth/ui/LoginForm';
```

## Migration Strategy (Bottom-up)

1. Start with shared layer — extract UI, lib, API client
2. Define entities — business domain objects
3. Extract features — user interactions
4. Build widgets — composite UI blocks
5. Organize views — move page logic from page files
6. Configure app layer — providers, styles

Migrate incrementally; run tests after each layer.

## Best Practices

- No cross-slice imports within same layer
- Export through `index.ts`; avoid `export * from`; use explicit exports
- shared/ui: per-component index for tree-shaking (see [public-api.md](./references/public-api.md))
- Avoid generic folders/files: `types.ts`, `utils.ts`, `components/` — use domain names (see [code-smells.md](./references/code-smells.md))
- Colocate tests next to implementation
- Keep slices focused; avoid "god slices"
- Name by domain: `features/product-search` not `features/search-bar-component`
- Use TypeScript strict mode

## Troubleshooting

**Import path issues:** Configure path aliases in `tsconfig.json` — see Configuration below.

**Build errors:** Clear `.next`, run `npm install`, restart dev server.

## Configuration

### TypeScript Path Aliases

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/app/*": ["src/app/*"],
      "@/views/*": ["src/views/*"],
      "@/widgets/*": ["src/widgets/*"],
      "@/features/*": ["src/features/*"],
      "@/entities/*": ["src/entities/*"],
      "@/shared/*": ["src/shared/*"]
    }
  },
  "include": ["src"]
}
```

### ESLint (Optional)

```javascript
'no-restricted-imports': ['error', {
  patterns: [{
    group: ['@/views/*', '@/widgets/*'],
    message: 'Features cannot import from views or widgets',
  }],
}]
```

## Reference Files

### Documentation Library

Load these resources as needed during development:

**Core FSD Reference**

- [layers-and-segments.md](./references/layers-and-segments.md) — Layers, slices (zero coupling, slice groups), segments, @x cross-reference, migration (including v2.0→v2.1)
- [public-api.md](./references/public-api.md) — Public API rules, @x cross-imports, circular imports, shared/ui tree-shaking, Steiger
- [code-smells.md](./references/code-smells.md) — Desegmentation, generic folder/file anti-patterns

**Implementation Examples**

- [examples.md](./references/examples.md) — Full examples: each layer, page layouts, auth, types/DTOs, API requests, domain-based files

**Optional**

- [react-query.md](./references/react-query.md) — React Query + FSD: Query Factory, pagination, QueryProvider
- [monorepo.md](./references/monorepo.md) — Turborepo + FSD structure

**External**

- [FSD Documentation](https://feature-sliced.design/) | [Layers v2.1](https://feature-sliced.design/docs/reference/layers) | [Public API](https://feature-sliced.design/docs/reference/public-api) | [Next.js Guide](https://feature-sliced.design/docs/guides/tech/with-nextjs) | [Migration v2.0→v2.1](https://feature-sliced.design/docs/guides/migration/from-v2-0) | [React Query Guide](https://feature-sliced.design/docs/guides/tech/with-react-query) | [FSD Examples](https://github.com/feature-sliced/examples)
