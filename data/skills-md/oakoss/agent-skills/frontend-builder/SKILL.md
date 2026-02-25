---
name: frontend-builder
description: 'Builds modern React and Next.js frontends. Use when creating web applications, choosing frontend stack, structuring components, implementing UI/UX designs, or setting up project architecture. Use for React, Next.js, Tailwind CSS, shadcn/ui, server components, and component patterns.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://react.dev'
---

# Frontend Builder

## Overview

Builds maintainable, performant React and Next.js frontends using a server-first architecture. Covers component design, state management, data fetching, forms, styling, and performance optimization. Not for backend API design, database schema, or deployment infrastructure.

## Quick Reference

| Pattern          | Approach                                                    | Key Points                                                 |
| ---------------- | ----------------------------------------------------------- | ---------------------------------------------------------- |
| Framework        | Next.js App Router (default), React + Vite (SPAs)           | Server-first rendering, file-based routing                 |
| Components       | Page, Feature, UI, Layout types                             | Single responsibility, typed props, composition            |
| Server vs Client | Server Components default, `'use client'` at leaf nodes     | Push interactivity to edges of component tree              |
| State (local)    | `useState`, props, lift to parent                           | Keep state close to where it is consumed                   |
| State (global)   | Context API (theme, auth), Zustand (complex)                | Avoid Context for frequently changing values               |
| Data fetching    | Server Components (server), TanStack Query (client)         | Server Actions for mutations, `revalidatePath` for cache   |
| Forms            | React Hook Form + Zod, or Server Actions + `useActionState` | Schema validation, optimistic updates with `useOptimistic` |
| Styling          | Tailwind CSS v4 + shadcn/ui                                 | CSS-first config with `@theme`, OKLCH colors               |
| Performance      | Suspense streaming, code splitting, memoization             | `React.lazy()`, `next/dynamic`, selective `memo()`         |
| Error handling   | Error boundaries, `error.tsx` per route                     | Wrap feature sections, not individual components           |

## Common Mistakes

| Mistake                                                           | Correct Pattern                                                                                   |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Adding `'use client'` to every component                          | Default to Server Components; add `'use client'` only for interactivity                           |
| Giant multi-responsibility component                              | Break into focused sub-components with single purposes                                            |
| Placing all state at the top of the component tree                | Keep state as close to where it is consumed as possible                                           |
| Using `useEffect` to compute derived data                         | Use `useMemo` for derived values; reserve `useEffect` for side effects                            |
| Missing error boundaries around feature sections                  | Wrap feature areas with error boundaries to prevent full-page crashes                             |
| Creating API routes for simple mutations                          | Use Server Actions with `'use server'` for form submissions and mutations                         |
| Passing non-serializable props to Client Components               | Props crossing server/client boundary must be serializable (no functions, classes)                |
| Using `tailwind.config.js` with Tailwind v4                       | Use CSS-first configuration with `@theme` directive in CSS file                                   |
| Fetching data in Client Components when Server Components suffice | Fetch in Server Components by default; use TanStack Query only when client-side caching is needed |

## Delegation

When building frontends, delegate to specialized skills:

- `react-patterns` -- React hooks, rendering patterns, and performance optimization
- `nextjs` -- Next.js routing, middleware, and deployment configuration
- `tanstack-query` -- Client-side data fetching, caching, and mutations
- `tanstack-form` -- Complex form handling and field-level validation
- `tailwind` -- Tailwind CSS utility patterns and responsive design
- `design-system` -- Token hierarchy and component architecture
- `performance-optimizer` -- Profiling, bundle analysis, and Core Web Vitals

## References

- [Component Architecture](references/component-architecture.md) -- Component types, folder structure, TypeScript patterns, and composition
- [Server Components](references/server-components.md) -- Server/client boundary, Server Actions, Suspense streaming, and data flow
- [State Management](references/state-management.md) -- useState, Context API, Zustand, and URL state patterns
- [Data Fetching](references/data-fetching.md) -- TanStack Query, Server Components data, and cache revalidation
- [Forms and Validation](references/forms.md) -- React Hook Form, Zod schemas, Server Actions, and useActionState
- [Styling](references/styling.md) -- Tailwind CSS v4, shadcn/ui, CSS-first config, and responsive patterns
- [Performance and Errors](references/performance-and-errors.md) -- Memoization, code splitting, Suspense streaming, and error boundaries
