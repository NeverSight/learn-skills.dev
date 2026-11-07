---
name: maintainable-react
description: Principles for writing, refactoring, and reviewing React code so it stays maintainable — resisting premature abstraction (the "demon component"), keeping data flow obvious, and putting state and effects in the right place. Use when writing or refactoring a React component or hook, deciding whether to extract or reuse one, reviewing React for maintainability, reaching for useEffect, choosing where state lives, or untangling prop drilling and over-abstraction.
---

Maintainable React comes from **resisting premature abstraction and keeping data flow obvious** — not from DRY, not from "clean code" for its own sake. The most common way a React codebase rots is the opposite of messiness: a well-meaning shared component or hook that grows a new prop, a new `if`, a new variant for every edge case until no one can safely touch it. Optimize for the next developer reading one file, not for eliminating every repeated line.

These are principles to apply and to check against, not an ordered procedure. Each names a **leading word** — carry it while you work.

## Avoid hasty abstractions (AHA) — beware the demon component

**Duplication is cheaper than the wrong abstraction.** Do not build a shared component, hook, or util until you have **two or three real call sites** that demonstrably share a shape. Abstract from concrete examples, never from anticipation.

The failure mode to fear is the **demon component**: one component that absorbs every new use case through more boolean props (`isCompact`, `hideHeader`, `variant="settings"`) and conditional branches until it is unreadable and unsafe to change. When an abstraction starts fighting you — you're adding a prop just to make one caller behave differently — that is the signal to **back it out**: let the call sites diverge back into separate components and re-abstract later only if a genuine common shape emerges.

- Two similar-but-separate components are healthier than one component with a `variant` prop and five conditionals.
- Prefer more lines of straightforward code over one clever generic that needs a mental model to use.
- Extract a hook or component when it is **hard to read in one pass** or **genuinely reused** — not "for the fun of it." A long function with clearly-named chunks beats a hook extracted purely for tidiness (premature hook extraction usually complicates effect/dependency timing rather than simplifying it).

## Derive, don't sync

If a value can be computed from existing props or state, **compute it during render** — do not store it in `useState` and keep it in sync with an Effect.

```tsx
// ❌ redundant state + effect
const [fullName, setFullName] = useState("")
useEffect(() => { setFullName(`${first} ${last}`) }, [first, last])

// ✅ derived in render
const fullName = `${first} ${last}`
```

- Expensive derivation → `useMemo`, still not state.
- Filtering/mapping a list for display → derive in render, never mirror into state.
- "Computed values should not be state" is the rule. Reach for `useState` only for values a user or external system *changes*, not values you can *calculate*.

## Effects are an escape hatch, not a reaction system

An Effect exists to **synchronize with something outside React** (network, subscriptions, the DOM, a non-React widget). If no external system is involved, you almost certainly don't need one. Golden test: *"Code that runs because the component was displayed goes in an Effect; code that runs because of a specific interaction goes in an event handler."*

| Instead of an Effect that… | Do this |
| --- | --- |
| derives one state from another | compute in render (see above) |
| caches an expensive value | `useMemo` |
| resets all state when a prop changes | give the component `key={id}` so React remounts it |
| adjusts some state on a prop change | derive it in render; adjust-during-render only as last resort |
| reacts to a click/submit (toast, POST, navigate) | put it in the event handler |
| chains: setState → effect → setState → effect | collapse into one event handler, compute the cascade synchronously |
| notifies the parent of a change (`onChange`) | call the parent's handler in the same event handler |
| initializes the app once | module-level code, or a controlled entry point — not `useEffect(…, [])` |

Legitimate Effect uses: real data fetching (with a cleanup/`ignore` flag for race conditions — though prefer a query library) and subscribing to external stores (`useSyncExternalStore`).

## Colocate state, lift only on a real second consumer

Put state as close to where it's used as possible. Decision path:

1. `useState` in the component that needs it.
2. A child needs it → push it **down** into the child.
3. Siblings/parent need it → lift to the **closest common ancestor**, no higher.
4. Only reach for Context once colocation is exhausted and prop drilling is a real, felt pain.

Revisit placement during every refactor — colocation is a habit. The same promotion rule governs *code* location: logic starts inside the feature that uses it (`app/<domain>/_components`, `_hooks`); promote it to a shared module (`modules/`) or the design system (`packages/ui`) **the moment a second feature actually consumes it** — not before. Don't reach across features directly; don't pre-emptively hoist to shared.

## Composition over context over prop drilling

When data is threaded through intermediate components that don't use it, fix it in this order:

1. **Composition / slots first** — pass rendered components as `children` or props to a layout, so the data-owner and data-consumer sit adjacent and the middle layers hold nothing.
2. **Context second**, as a fallback, only when composition genuinely can't express it. Context is not the default; it's the escape valve.

Never define a component inside another component's render body — it gets a new identity every render, defeating memoization and silently resetting the child's state.

## Server state and client state are different problems

Data that comes from a server, chain, or subgraph is **server state** — it belongs in the query cache (TanStack Query), never copied into `useState`/Zustand/Context. A second copy of server data is a second source of truth and *will* drift. Configure `staleTime` per query rather than disabling refetch flags piecemeal; stale data beats a spinner. Use Zustand/local state only for genuine **client state** (UI toggles, form drafts, cross-reload persistence). (See `tanstack-best-practices` for query-layer specifics.)

## Split the loader from the view

If a component needs data loaded before it can render correctly, split it:

- an **outer** component that gathers the data (params, queries) and shows the loading/error state, and
- an **inner** presentational component that accepts **fully-resolved props — no nulls, no undefineds**.

The inner component becomes pure (props in, JSX out, no fetching), trivial to read and test as a black box. If there are different data paths (endpoint A vs B), split further so each resolved shape has its own component. This is the surviving core of container/presentational: keep the "container" work in a hook or outer component, keep the view pure.

## Make the types scream

Push correctness into the type system so a wrong change fails to compile rather than at runtime.

- Known set of options → a **union** (`"idle" | "loading" | "error"`) or discriminated union, never a bare `string`.
- Mapping a key to a value → `Record<EnumType, ValueType>` instead of a `switch` with a `default`. When you add a case, TypeScript forces you to handle it everywhere; a `default` silently swallows it.
- Model mutually-exclusive states as a **discriminated union**, not a bag of optional booleans (`{ status: "success"; data: T } | { status: "error"; error: E }`, not `{ isLoading?, data?, error? }`).
- Derive types from their source rather than re-declaring them: `Pick<ApiType, "name" | "id">`, not a fresh `{ name: string; id: string }`. When the source changes, your code breaks at compile time where it matters.

## Keep module boundaries one-directional

Dependencies flow one way: shared packages → shared modules → feature/domain → app shell. Features must **not import from each other**, so any feature folder stays deletable without cascading breakage. Each boundary exposes an explicit public surface (a barrel `index.ts` with named exports); never reach into another module's internals. A behavior change that forces edits across many unrelated files (**shotgun surgery**) is a smell — the logic wants to live behind one interface, not scattered as conditionals.

## When refactoring an existing messy component

1. **Cover it first** — write black-box tests asserting what it renders and which callbacks it fires, so you can refactor without fear.
2. **Delete dead code** — commented-out logic, unused state, unused imports. Version control remembers.
3. **Replace hand-rolled logic with proven libraries** — data fetching and forms are the usual complexity sinks.
4. Then apply the principles above: derive instead of sync, move effect logic into handlers, split loader from view, and let over-eager abstractions diverge back into focused pieces.

Prefer tests that resemble real usage (interaction over implementation detail); lean on integration-level tests. (See `testing-best-practices` for this repo's conventions.)
