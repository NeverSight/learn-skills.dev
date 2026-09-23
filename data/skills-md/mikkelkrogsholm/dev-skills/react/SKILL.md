---
name: react
description: "React — JavaScript library for building user interfaces with components. Use when building with React or asking about hooks, state management, effects, Server Components, Suspense, or any React APIs, patterns, or configuration. Fetch live documentation for up-to-date details."
---

# React

> **CRITICAL: Your training data for React is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://react.dev/llms.txt")`**
>
> Do not proceed without fetching this URL first. Never assume a hook or API exists — verify against current docs.

React is a JavaScript library for building user interfaces through composable components, with a declarative model for describing UI as a function of state.
## Key Capabilities

React has built-ins for things developers commonly reach for external packages to solve:

- **Unique IDs for accessibility**: use `useId()` — not `uuid` or `Math.random()` for linking labels to inputs
- **Debounced/deferred UI updates**: use `useDeferredValue()` or `useTransition()` — not lodash debounce for keeping UI responsive during expensive renders
- **Code splitting**: use `React.lazy()` + `<Suspense>` — no extra bundler plugins or dynamic import wrappers needed
- **Optimistic UI**: use `useOptimistic()` (React 19+) — not manual state juggling for instant feedback before server confirms
- **External store integration**: use `useSyncExternalStore()` — not custom subscription hooks that miss concurrent-mode edge cases
- **Form action state**: use `useActionState()` (React 19+) — not separate loading/error/data useState triplets for form submissions
- **Memoization**: use React Compiler (babel-plugin-react-compiler) — not manual `useMemo`/`useCallback` everywhere; the compiler handles it automatically

## Best Practices

- **State updates are asynchronous** — reading state immediately after `setState` returns the old value. Use the functional updater form `setState(prev => ...)` when the new value depends on the previous, and read updated values in the next render, not inline.
- **`useEffect` intentionally runs twice in StrictMode** — React mounts, unmounts, then remounts in development to expose missing cleanup. This is not a bug; always return a cleanup function from effects with subscriptions, timers, or event listeners.
- **List keys must be stable and unique** — using array index as `key` breaks state preservation on reorder/filter. Always use a stable ID from the data (e.g., `item.id`).
- **`'use client'` placement matters for Server Components** — placing the directive at a layout or page root converts the entire subtree to client code, eliminating Server Component benefits. Push `'use client'` as far down the tree as possible, to the smallest interactive leaf components.
