---
name: frontend-patterns
description: Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices.
origin: ECC
---

# Frontend Development Patterns

Modern frontend patterns for React, Next.js, and performant user interfaces.

## When to Activate

- Building React components (composition, props, rendering)
- Managing state (useState, useReducer, Zustand, Context)
- Implementing data fetching (Suspense-first, SWR, React Query, server components)
- Optimizing performance (memoization, virtualization, code splitting)
- Working with forms (validation, controlled inputs, Zod schemas)
- Building with the Next.js App Router (Server vs Client Components, caching, server actions)
- Handling client-side routing and navigation
- Building accessible, responsive UI patterns

## Pattern Index

| Area | Patterns | Reference |
|------|----------|-----------|
| Components | Composition, compound components, render props | `reference/components.md` |
| Custom hooks | `useToggle`, `useQuery`, `useDebounce` | `reference/hooks.md` |
| State management | Context + Reducer | `reference/state-management.md` |
| Data fetching | Suspense-first, isolated API layer | `reference/data-fetching.md` |
| Next.js App Router | Server/Client split, caching, server actions | `reference/nextjs-app-router.md` |
| Performance | Memoization, code splitting, virtualization | `reference/performance.md` |
| Forms | Controlled forms, validation, error boundaries | `reference/forms.md` |
| Animation | Framer Motion lists and modals | `reference/animation.md` |
| Accessibility | Keyboard navigation, focus management | `reference/accessibility.md` |

## Core Conventions

- **Composition over inheritance** — build UIs from small composable pieces (`Card` + `CardHeader` + `CardBody`), not deep class hierarchies.
- **Compound components** share state via Context (e.g. `Tabs` / `TabList` / `Tab`); throw if a child is used outside its provider.
- **Custom hooks** encapsulate reusable stateful logic (`use` prefix); always memoize callbacks with `useCallback` and clean up effects (clear timeouts, cancel subscriptions).
- **Context + Reducer** for non-trivial shared state; reducers return new state objects immutably (`{ ...state, ... }`), never mutate.
- **Memoize deliberately** — `useMemo` for expensive computations, `useCallback` for functions passed to children, `React.memo` for pure components. Don't memoize everything.
- **Code-split heavy components** with `lazy` + `Suspense`; virtualize long lists with `@tanstack/react-virtual`.
- **Controlled forms** with explicit validation; show field-level errors; immutable `setFormData(prev => ({ ...prev, field }))` updates.
- **Error boundaries** wrap app/feature roots to catch render errors and show fallbacks.
- **Accessibility first** — keyboard handlers (Arrow/Enter/Escape), ARIA roles (`combobox`, `dialog`, `aria-modal`), and focus save/restore on modal open/close.

## Quick Reference

```typescript
// Memoization
const sorted = useMemo(() => items.sort(...), [items])
const onClick = useCallback(() => {...}, [])
export const Pure = React.memo<Props>(({ x }) => <div>{x}</div>)

// Lazy load
const Heavy = lazy(() => import('./Heavy'))
<Suspense fallback={<Spinner />}><Heavy /></Suspense>

// Immutable state update
setFormData(prev => ({ ...prev, name: e.target.value }))
```

## Reference Files

- `reference/components.md` — read when building component APIs (composition, compound components, render props).
- `reference/hooks.md` — read when writing custom hooks (`useToggle`, `useQuery`, `useDebounce`).
- `reference/state-management.md` — read when wiring shared state with Context + Reducer.
- `reference/data-fetching.md` — read when fetching client data (Suspense-first pattern, isolated API layer, loading/error handling).
- `reference/nextjs-app-router.md` — read when building with the Next.js App Router (Server vs Client Components, fetch caching/revalidation, route conventions, server actions).
- `reference/performance.md` — read when optimizing render performance (memoization, lazy loading, virtualization, debounce/cleanup defaults).
- `reference/forms.md` — read when building forms with validation or error boundaries.
- `reference/animation.md` — read when adding Framer Motion list/modal animations.
- `reference/accessibility.md` — read when implementing keyboard navigation or focus management.

**Remember**: Modern frontend patterns enable maintainable, performant user interfaces. Choose patterns that fit your project complexity.
