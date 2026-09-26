---
name: react
description: >
  Guide for writing and reviewing React code — hooks, effects, re-renders, and browser performance. Use this skill when:
  (1) writing or reviewing React components and custom hooks,
  (2) writing or debugging `useEffect` — deciding whether an Effect is needed at all,
  (3) using `useState` for derived values, or syncing state between components,
  (4) diagnosing unnecessary re-renders, stale closures, or memoization problems,
  (5) fixing data-fetching waterfalls, race conditions, or duplicate requests, or using `use()` with Suspense,
  (6) optimizing paint, hydration, resource loading, or hot-path JavaScript,
  (7) working with refs, composition, prop drilling, or controlled vs. uncontrolled components,
  (8) upgrading React 18 to 19 — removed APIs (`ReactDOM.render`, `findDOMNode`, string refs, legacy context), `forwardRef`, `defaultProps`, and tests (`test-utils`, `act`, StrictMode counts),
  (9) forms and mutations with Actions — `useActionState`, `useFormStatus`, `useOptimistic`.
license: MIT
compatibility: React 18+ (React 19 for `use`, Actions, `Activity`, ref-as-prop)
allowed-tools: Read Write Edit Glob Grep
---

# React Best Practices

Apply these guidelines when writing or reviewing React code.

## Reference Files

Read ALL relevant references in the same turn, in parallel. Cite them when giving feedback:

- [Effect patterns](references/effect-patterns.md): When you don't need an Effect, dependency rules, cleanup, subscriptions, `useSyncExternalStore`, one-time initialization
- [Re-render optimization](references/rerender-optimization.md): `memo`/`useMemo`/`useCallback`, derived state, functional updates, lazy init, `useDeferredValue`, `startTransition`, `useEffectEvent`
- [Component patterns](references/component-patterns.md): Refs, `useImperativeHandle`, custom hook rules, controlled vs. uncontrolled, composition over prop drilling, `flushSync`
- [Data fetching](references/data-fetching.md): Parallelizing requests, Suspense boundaries, `use()` and stable promise sources, request deduplication, passive listeners, `localStorage` versioning
- [Rendering performance](references/rendering-performance.md): `content-visibility`, hydration mismatches, resource hints, script loading, SVG animation, `Activity`, `useTransition`
- [JS performance](references/js-performance.md): Layout thrashing, `Set`/`Map` lookups, index maps, single-pass iteration, `toSorted`, `requestIdleCallback`
- [Actions](references/actions.md): `<form action>`, `useActionState`, `useFormStatus`, `useOptimistic` — pending, error, and optimistic state for mutations
- [React 19 migration](references/react19-migration.md): Upgrading from 18 — root API, `findDOMNode`, `forwardRef`, `defaultProps`, legacy context, string refs, propTypes, JSX transform, TypeScript types, `act`/`test-utils`, StrictMode test counts

## You Might Not Need an Effect

Effects are an **escape hatch** from React. They synchronize with external systems. If no external system is involved, you probably don't need one.

```
Need to respond to something?
├── User interaction (click, submit, drag)?
│   └── EVENT HANDLER
├── Props/state changed and need a derived value?
│   └── CALCULATE DURING RENDER
│       └── Measurably expensive? useMemo
├── Need to reset state when an identity prop changes?
│   └── key PROP on the component
└── Component appeared on screen, and there's an external system?
    └── EFFECT, with cleanup
```

**Do need an Effect:** non-React widgets and browser APIs, subscriptions (prefer `useSyncExternalStore`), analytics that fire because a component displayed, data fetching with cleanup (prefer a data library).

**Don't need an Effect:** transforming data for rendering, handling user events, deriving state, chaining state updates, notifying a parent, resetting state.

## Quick Reference

### Effects

| Situation | Don't | Do |
|---|---|---|
| Derived state from props/state | `useState` + `useEffect` | Calculate during render |
| Expensive calculation | `useEffect` to cache | `useMemo` |
| Reset state on prop change | `useEffect` + `setState` | `key` prop |
| Response to a user event | `useEffect` watching state | Event handler |
| Notify parent of a change | `useEffect` calling `onChange` | Call it in the event handler |
| Subscribe to an external store | Manual `useEffect` subscription | `useSyncExternalStore` |
| Fetch data | `useEffect` without cleanup | `ignore` flag, or a data library |
| Effect re-runs every render | Object/function in deps | Move creation inside the effect |
| Missing dependency | `eslint-disable exhaustive-deps` | Functional update or `useEffectEvent` |
| One-time app init | `useRef` guard | Module-level flag |

### Re-renders

- Never define a component inside another component — it remounts every render
- Use functional `setState` when the next state depends on the previous one
- `useState(() => expensive())` for expensive defaults; the plain form runs every render
- Don't wrap simple boolean/primitive expressions in `useMemo`
- Split combined `useMemo`/`useEffect` — one concern each
- Values that change often but aren't rendered (mouse position, flags) belong in refs
- If React Compiler is enabled, skip manual `memo`/`useMemo`/`useCallback`

### Data fetching

- `Promise.all()` for independent requests; chain per item for dependent ones
- Move `await` past early returns and behind cheap synchronous guards
- One shared request per endpoint (SWR / React Query), not one per component instance
- Every fetch effect needs an `ignore` flag or `AbortController`
- Promises passed to `use()` come from a loader, cache, library, or Server Component — never created in render

### Forms and mutations (React 19)

- `<form action={fn}>` over `onSubmit` + `preventDefault`; `useActionState` over a loading/error reducer
- Return expected errors from the action as state; thrown errors go to the error boundary
- `useFormStatus` is imported from `react-dom` and only reads a parent `<form>`
- Seed `useOptimistic` with confirmed state and call its setter inside an Action
- After `await` inside an Action, wrap state updates in another `startTransition`

### Upgrading to React 19

- Run `npx codemod@latest react/19/migration-recipe` first; the upgrade PR changes API surface only
- `forwardRef` still works — `ref` is a plain prop; convert opportunistically
- `defaultProps` are ignored on function components but still work on class components
- StrictMode still double-runs effects; what changed is `useMemo`/`useCallback` result reuse and double-invoked ref callbacks

### Performance

- Measure before optimizing — profile, don't guess
- Batch DOM writes, then read once; interleaving forces reflow
- `Set`/`Map` for repeated lookups; one pass instead of chained `.filter().map()`
- `.toSorted()` on props and state — `.sort()` mutates
- Defer analytics and prefetching with `requestIdleCallback`

## Review Checklist

1. Does every `useEffect` synchronize with an external system? If not, propose the alternative.
2. Are dependency arrays complete, with no lint suppressions?
3. Does every subscription, listener, timer, and fetch have cleanup?
4. Is any state redundant — derivable from other props or state?
5. Are components defined at module scope?
6. Are independent async calls parallelized?
7. Are mutating array methods used on props or state?
8. Is every promise passed to `use()` stable across renders?
9. On React 19: are forms using Actions with errors returned as state, and are removed APIs (`findDOMNode`, string refs, legacy context, `test-utils`) gone?
