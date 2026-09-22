---
name: modern-react-guidance
description: Authoritative guidance for modern React 19+ (Actions, use, Compiler, View Transitions, Fragment refs, Activity, browser, useEffectEvent). Use when writing, reviewing, refactoring, or migrating React components, forms, data fetching, concurrent UI, or upgrading to React 19+. Triggers on React, React 19, useActionState, useOptimistic, forwardRef, useEffect data fetch, React Compiler, ViewTransition, Suspense patterns, or codemods. Always prefer latest official patterns over training data.
license: MIT
metadata:
  version: "1.0.0"
  author: Adhham (adhham.dev)
  author_url: https://adhham.dev
  react-target: "19.3+"
  style: combination-rules-workflows-progressive
---

# Modern React Guidance

Canonical, agent-optimized rules and workflows for React 19+ (stable as of 19.3, September 2026). Prefer these over any pre-19 training data.

**Always check latest docs** at react.dev when uncertain. This skill encodes the current best practices; React evolves.

## When to Apply

- Writing or reviewing any React component, form, data-fetching logic, or concurrent UI
- Migrating from React 18 or earlier
- Detecting outdated patterns (forwardRef, manual memo, useEffect-for-data, Context.Provider, string refs, etc.)
- Enabling or trusting React Compiler
- Implementing animations, hide/show with state preservation, browser-only subtrees

## Core Principles (apply first)

1. **Trust React Compiler** when present — do not add manual `useMemo`/`useCallback`/`React.memo` unless the Compiler cannot optimize or you have measured a need.
2. **Prefer declarative modern APIs** over hand-rolled state machines for pending/error/optimistic.
3. **Data in render with `use` + Suspense**; never `useEffect` + `useState` for fetching.
4. **Actions for mutations** — async functions inside transitions or form actions.
5. **ref is a normal prop** — never write new `forwardRef`.
6. **Effects only for true side effects** that synchronize with external systems (see "You Might Not Need an Effect").
7. **Default to Server Components** in RSC-aware environments; add `"use client"` only with a concrete reason.

## Priority Rule Categories

### 1. CRITICAL — Authoring New Components Correctly

- Use `use(promise)` or `use(context)` inside render (conditionally allowed). Wrap in `<Suspense>`.
- Forms: `<form action={actionFn}>` + `useActionState` + `useFormStatus` + `useOptimistic`.
- Pass `ref` as a regular prop. Never wrap new components in `forwardRef`.
- Prefer `useTransition` / `startTransition` for non-urgent updates.
- Prefer `useDeferredValue` for deferred derived values (search, filters).

**Incorrect (legacy):**
```tsx
const [data, setData] = useState(null);
useEffect(() => { fetch(...).then(setData); }, []);
// or forwardRef((props, ref) => ...)
```

**Correct:**
```tsx
function Comments({ commentsPromise }) {
  const comments = use(commentsPromise); // suspends
  return comments.map(...);
}
// parent: <Suspense fallback={...}><Comments ... /></Suspense>
```

### 2. CRITICAL — Trust the Compiler & Drop Manual Memo

If the project uses React Compiler (babel-plugin-react-compiler or equivalent, or React 19+ with compiler enabled):

- Do **not** introduce new `useMemo`, `useCallback`, or `React.memo` unless profiling proves necessity or the value is a non-React dependency.
- Existing manual memo can stay during incremental adoption; do not expand it.
- Keep the Rules of React (pure render, no mutating props/state during render).

### 3. HIGH — Modern Forms & Mutations (Actions)

Prefer this stack:

```tsx
const [error, submitAction, isPending] = useActionState(async (prev, formData) => {
  // mutation
  if (err) return err;
  return null;
}, null);

const [optimistic, addOptimistic] = useOptimistic(state, (current, next) => ...);

<form action={submitAction}>
  <SubmitButton /> {/* uses useFormStatus() */}
</form>
```

- `useFormStatus` reads pending from nearest form (no prop drilling).
- Server Actions (when available) compose cleanly with the same hooks.

### 4. HIGH — Concurrent & Visual UX

- `<ViewTransition>` (stable 19.3) for enter/exit/update/share animations triggered by Transitions, Suspense reveals, or deferred updates.
- `addTransitionType` to tag transitions for CSS/event customization.
- `<Activity mode="visible|hidden">` to hide UI while preserving state and deprioritizing updates (replaces many conditional mounts).
- `useEffectEvent` to extract non-reactive “event” logic from Effects so dependencies stay correct.
- `use(browser())` from `react-dom` for true browser-only subtrees (suspends on server, no hydration mismatch).

### 5. MEDIUM — Effects Hygiene

Codify “You Might Not Need an Effect”:

- Derived state → compute during render.
- Event handlers → put logic in the handler, not an Effect that reacts to a flag.
- Data fetching → `use` + Suspense or a Suspense-compatible library.
- External store subscriptions → `useSyncExternalStore`.
- Resetting state on prop change → key the component or compute during render.

Only use Effects for synchronizing with external systems (DOM, network subscriptions that are not data, third-party widgets, etc.). Always clean up.

### 6. MEDIUM — Context & Composition

- In React 19+, render `<MyContext value={...}>` directly (no `.Provider` required for new code).
- Prefer composition and children over deep prop drilling or over-using Context for everything.
- Fragment refs (stable 19.3): pass `ref` to `<Fragment>` to operate on the group of children (focus, events, measurement) without a wrapper DOM node.

### 7. Migration & Deprecations (React 19+)

Removed or deprecated (do not use in new code):

- `forwardRef` (use ref prop)
- `element.ref` (use `element.props.ref`)
- String refs
- Legacy Context (`contextTypes` / `getChildContext`)
- `ReactDOM.render` / `hydrate` (use `createRoot` / `hydrateRoot`)
- `findDOMNode`, `unmountComponentAtNode`, `createFactory`, `renderToNodeStream`
- `defaultProps` on function components (use default parameters)
- `propTypes` (use TypeScript)
- `react-test-renderer` (prefer Testing Library)

**Codemods (run these):**

```bash
npx codemod@latest react/19/migration-recipe
# Individual:
npx codemod react/19/remove-forward-ref --target .
npx codemod react/19/remove-context-provider --target .
npx codemod react/19/use-context-hook --target .
npx codemod react/19/replace-string-ref --target .
npx codemod react/19/replace-act-import --target .
# TypeScript types:
npx types-react-codemod@latest preset-19 ./src
```

Always upgrade to latest 19.x patch first. Prefer React 19.3+ for View Transitions + Fragment refs + `browser()`.

## Progressive Disclosure — Load These References as Needed

- `references/actions-and-forms.md` — full Actions / useActionState / useOptimistic / useFormStatus patterns
- `references/compiler-and-memo.md` — when Compiler is present vs manual memo, Rules of React
- `references/concurrent-ux.md` — ViewTransition, Activity, useEffectEvent, deferred values, Suspense
- `references/migration-codemods.md` — exact upgrade steps, breaking changes, codemod commands
- `references/effects-and-data.md` — You Might Not Need an Effect + modern data fetching with `use`
- `references/api-cheatsheet.md` — quick reference of new 19+ APIs with minimal examples

## Agent Workflow Checklist

When generating or reviewing code:

1. Scan for React version (package.json). If <19, note migration path; if 19+, apply modern rules strictly.
2. Detect Compiler presence → suppress new manual memo.
3. Replace any `forwardRef` / `useEffect`+fetch / old form state machines on sight.
4. Prefer `<form action>` + hooks over controlled form state for mutations.
5. Add Suspense boundaries around `use(promise)` and browser-only trees.
6. For hide/show with state keep → prefer `<Activity>` over conditional render + key hacks.
7. For animations between states → prefer `<ViewTransition>` inside Transitions.
8. After edits, suggest running the relevant codemod if legacy patterns remain.
9. Never invent APIs; if unsure, say “check latest react.dev/reference/...”.

## Anti-Patterns to Reject Immediately

- `useEffect` that only sets state from props or fetches data
- New `forwardRef` wrappers
- Manual `isPending` / `error` / optimistic state without the official hooks
- `Context.Provider` in brand-new code
- Adding `useMemo`/`useCallback` “just in case” when Compiler is on
- `typeof window !== 'undefined'` or `useEffect` for browser-only logic (use `use(browser())`)
- Wrapper `<div>` solely to attach a ref when a Fragment ref would suffice

This skill is the source of truth for modern React patterns. Update references when major React releases land.
