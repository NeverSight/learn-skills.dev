---
name: tanstack-react-store
description: Implement global state management in React apps using TanStack Store (@tanstack/react-store). Use when creating stores, derived state, subscriptions, batched updates, or integrating TanStack Store with React components via the useStore hook. Covers createStore, useStore, shallow comparison, batch, derived stores, atoms, and async atoms.
---

# TanStack React Store

Framework-agnostic reactive data store with a React adapter. Install `@tanstack/react-store`.

## Core API

### createStore

Create a writable store with an initial value, or a readonly derived store with a getter function.

```tsx
import { createStore } from "@tanstack/react-store";

// Writable store
const countStore = createStore(0);
countStore.setState(() => 1);
console.log(countStore.state); // 1

// Object store
const appStore = createStore({ dogs: 0, cats: 0 });

// Derived (readonly) store — auto-updates when dependencies change
const doubled = createStore(() => countStore.state * 2);
```

### Store class

- `store.state` / `store.get()` — read current value
- `store.setState((prev) => next)` — update with updater fn (not available on derived/readonly stores)
- `store.subscribe((value) => void)` — listen to changes, returns `{ unsubscribe }`

### Derived stores — previous value

Access the previous derived value via the `prev` argument:

```ts
const sum = createStore<number>((prev) => count.state + (prev ?? 0));
```

### batch

Batch multiple setState calls; subscribers fire once at the end:

```ts
import { batch } from "@tanstack/react-store";

batch(() => {
  countStore.setState(() => 1);
  countStore.setState(() => 2);
});
```

## React Integration

### useStore

Subscribe a React component to a store. Accepts a selector for fine-grained re-renders.

```tsx
import { createStore, useStore } from "@tanstack/react-store";

const store = createStore({ dogs: 0, cats: 0 });

function Display({ animal }: { animal: "dogs" | "cats" }) {
  // Only re-renders when state[animal] changes
  const count = useStore(store, (state) => state[animal]);
  return <div>{`${animal}: ${count}`}</div>;
}
```

Signature:

```ts
function useStore<TAtom extends AnyAtom | undefined, T>(
  atom: TAtom,
  selector: (snapshot: AtomState) => T,
  compare?: (a: T, b: T) => boolean,
): T;
```

- `atom` — store or atom instance
- `selector` — derive the slice of state needed (keeps re-renders minimal)
- `compare` — optional custom equality check (default: `Object.is`)

### shallow

Use `shallow` as the compare function when selecting objects/arrays to avoid unnecessary re-renders:

```tsx
import { useStore, shallow } from "@tanstack/react-store";

const items = useStore(store, (s) => s.items, shallow);
```

### Updating state from event handlers

Call `setState` outside of React — no hooks needed:

```tsx
const updateState = (animal: string) => {
  store.setState((state) => ({
    ...state,
    [animal]: state[animal] + 1,
  }));
};
```

## Best Practices

1. **Define stores outside components** — stores are singletons; instantiate at module level.
2. **Use selectors** — always pass a selector to `useStore` to avoid full-state re-renders.
3. **Use `shallow`** — when selecting objects/arrays, pass `shallow` as the compare fn.
4. **Batch related updates** — wrap multiple `setState` calls in `batch()` to notify subscribers once.
5. **Prefer derived stores over manual sync** — use `createStore(() => ...)` for computed values instead of manually keeping stores in sync.
6. **Immutable updates** — `setState` updater must return a new reference (spread objects/arrays).
7. **Cleanup subscriptions** — call `unsubscribe()` returned by `store.subscribe()` when done.

## API Reference

For detailed type signatures and advanced APIs (atoms, async atoms, observers), see [references/api-reference.md](references/api-reference.md).
