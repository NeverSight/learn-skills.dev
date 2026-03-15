---
name: zustand
description: Implement global state management for React/TypeScript applications. Use when creating, modifying, or debugging Zustand stores, implementing state management patterns (slices, persist, devtools, immer), setting up Zustand with Next.js/SSR, writing tests for Zustand stores, or working with TypeScript typing for Zustand (curried create, StateCreator, middleware mutators).
---

# Zustand

Lightweight state management for React. No providers, no boilerplate. Stores are hooks.

## Quick start

```ts
import { create } from "zustand"

interface BearState {
  bears: number
  increase: (by: number) => void
}

const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
}))

// In components — select only what you need
const bears = useBearStore((state) => state.bears)
```

## Critical rules

1. **TypeScript:** Use curried form `create<T>()(...)` — required for type inference
2. **Immutability:** Treat state as immutable. `set` shallow-merges at one level only
3. **Selectors:** Always select specific fields, not the whole store. Use `useShallow` for multi-field selectors returning new references
4. **Middleware order:** `devtools` must be outermost: `devtools(persist(immer(...)))`
5. **Next.js:** Create stores per-request via `createStore` + Context, NOT global `create`
6. **Nested updates:** Use Immer for deep nesting, spread operator for shallow

## When to use what

| Need | Solution |
|------|----------|
| Basic React store | `create<T>()(...)` |
| Vanilla (non-React) store | `createStore` from `zustand/vanilla` |
| Use vanilla store in React | `useStore(store, selector)` |
| Auto-infer types (no interface) | `combine` middleware |
| Persist to localStorage | `persist` middleware |
| Redux DevTools | `devtools` middleware |
| Mutable-style updates | `immer` middleware |
| Subscribe to slices externally | `subscribeWithSelector` middleware |
| Multiple fields without rerender | `useShallow` wrapper |
| Large store modularization | Slices pattern with `StateCreator` |
| Next.js App Router | `createStore` + Context + Provider |
| Reset store | `set(initialState)` or `store.getInitialState()` |

## References

- **API reference** (create, createStore, hooks, shallow): See [references/apis.md](references/apis.md)
- **TypeScript patterns** (curried create, slices, middleware typing, custom middleware): See [references/typescript.md](references/typescript.md)
- **Middlewares** (persist, devtools, immer, redux, combine, subscribeWithSelector): See [references/middlewares.md](references/middlewares.md)
- **Patterns & best practices** (Next.js, testing, reset, auto-selectors, SSR, deep updates): See [references/patterns.md](references/patterns.md)
