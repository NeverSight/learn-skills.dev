---
name: tanstack-store
description: 'TanStack Store for framework-agnostic reactive state management with derived state and batching. Use when managing shared state, creating derived computations, or building framework-agnostic state logic. Use for tanstack-store, store, state, derived, batch, subscribe, reactive-state.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://tanstack.com/store/latest'
---

# TanStack Store

## Overview

TanStack Store is a lightweight, framework-agnostic reactive state management library with type-safe updates, derived computations, batched mutations, and effect management. It powers the core of TanStack libraries internally and can be used as a standalone state solution. Framework adapters are available for React, Vue, Solid, Angular, and Svelte.

**Core primitives:**

- **Store** — reactive container with `setState`, subscriptions, and lifecycle hooks
- **Derived** — lazily computed values that track Store/Derived dependencies
- **Effect** — side-effect runner triggered by dependency changes
- **batch** — groups multiple updates so subscribers fire once

**When to use:** Shared reactive state across components, derived/computed values from multiple stores, batched state updates, framework-agnostic state logic reusable across React/Vue/Solid/Angular/Svelte, lightweight alternative to Redux/Zustand/MobX.

**When NOT to use:** Server state and caching (TanStack Query), complex normalized state with middleware (Redux Toolkit), form state management (TanStack Form), simple component-local state (useState/useSignal).

**Key characteristics:**

- Tiny bundle size with zero dependencies
- Immutable update model (always return new references from `setState`)
- Lazy evaluation for Derived values (recompute only when accessed after change)
- Explicit mount/unmount lifecycle for Derived and Effect (no automatic cleanup)

## Installation

| Package                   | Use Case                        |
| ------------------------- | ------------------------------- |
| `@tanstack/store`         | Framework-agnostic core         |
| `@tanstack/react-store`   | React adapter (re-exports core) |
| `@tanstack/vue-store`     | Vue adapter                     |
| `@tanstack/solid-store`   | Solid adapter                   |
| `@tanstack/angular-store` | Angular adapter                 |
| `@tanstack/svelte-store`  | Svelte adapter                  |

Framework packages re-export the core `Store`, `Derived`, `Effect`, and `batch` — install only the framework package, not both.

## Quick Reference

| Pattern              | API                                  | Key Points                                         |
| -------------------- | ------------------------------------ | -------------------------------------------------- |
| Create store         | `new Store(initialState, options?)`  | Generic over `TState` and `TUpdater`               |
| Read state           | `store.state`                        | Synchronous property access                        |
| Previous state       | `store.prevState`                    | Value before last `setState` call                  |
| Update state         | `store.setState((prev) => newState)` | Accepts updater function or direct value           |
| Subscribe            | `store.subscribe(listener)`          | Returns unsubscribe function                       |
| Derived value        | `new Derived({ deps, fn })`          | Lazily recomputes when dependencies change         |
| Mount derived        | `derived.mount()`                    | Required to activate dependency tracking           |
| Derived from derived | Nest `Derived` in another `deps`     | Forms a computation graph                          |
| Batch updates        | `batch(() => { ... })`               | Subscribers notified once after all updates        |
| Side effects         | `new Effect({ deps, fn, eager? })`   | Runs fn when dependencies change                   |
| Mount effect         | `effect.mount()`                     | Required to start listening                        |
| React binding        | `useStore(store, selector?)`         | Re-renders only when selected value changes        |
| Shallow compare      | `useStore(store, selector, shallow)` | Prevents re-renders for structurally equal objects |
| Lifecycle: subscribe | `onSubscribe` option                 | Fires on first subscriber, cleanup on last         |
| Lifecycle: update    | `onUpdate` option                    | Fires after every state change                     |
| Custom updater       | `updateFn` option                    | Replace default setState behavior                  |
| Previous deps        | `fn: ({ prevDepVals })`              | Compare current vs previous dependency values      |
| Dep vals access      | `fn: ({ currDepVals })`              | Array ordered by `deps` declaration order          |

## Common Mistakes

| Mistake                                           | Correct Pattern                                                       |
| ------------------------------------------------- | --------------------------------------------------------------------- |
| Reading `derived.state` without mounting          | Call `derived.mount()` before accessing state                         |
| Forgetting to unmount derived/effect              | Store the cleanup function and call it on teardown                    |
| Multiple `setState` calls without batching        | Wrap related updates in `batch()` to avoid intermediate recomputation |
| Selecting objects in `useStore` without `shallow` | Pass `shallow` as third argument to prevent unnecessary re-renders    |
| Mutating state object directly                    | Always return a new object from `setState` updater                    |
| Subscribing inside render without cleanup         | Use `useStore` hook in React instead of manual `subscribe`            |
| Creating stores inside React components           | Instantiate stores outside components or in a ref/useState            |
| Not including all deps in Derived                 | List every Store/Derived dependency in the `deps` array               |
| Mounting Derived deps after the parent            | Mount leaf dependencies before parent Derived values                  |
| Using `@tanstack/store` with React directly       | Install `@tanstack/react-store` which re-exports core                 |

## Delegation

- **Server state and caching**: Delegate to the `tanstack-query` skill if available. Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-query`
- **React component patterns**: Delegate to framework-specific skills for component architecture
- **Form state management**: Delegate to the `tanstack-form` skill if available. Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-form`
- **Query pattern discovery**: Use `Explore` agent to find examples in the codebase
- **Code review**: Delegate to `code-reviewer` agent for store architecture review

## References

- [Core concepts: Store, setState, subscriptions, and lifecycle hooks](references/core-concepts.md)
- [Derived state: computed values, dependency tracking, and batching](references/derived-state.md)
- [React integration: useStore hook, selectors, and performance](references/react-integration.md)
