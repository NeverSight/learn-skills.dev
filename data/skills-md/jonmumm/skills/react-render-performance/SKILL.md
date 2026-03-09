---
name: react-render-performance
description: >
  Minimize unnecessary React re-renders when consuming external state (XState, @xstate/store,
  Zustand, Redux, Nanostores, context). Prefer selector-based subscriptions over useState(wholeObject).
  Use when dealing with external state in React, optimizing re-renders, choosing state patterns,
  or integrating with these libraries.
---

# React Render Performance

Patterns for minimizing unnecessary React re-renders when consuming external
state. **Prefer selector-based subscriptions over `useState(wholeObject)`** —
subscribe only to the slice each component needs.

## Core idea

Storing a full state object in React state (e.g. `useState(snapshot)` and
subscribing to every change) forces re-renders on **any** update. A component
that only needs `phase` will still re-render when `quiz.selectedWrong` changes
if both live in the same object.

**Avoid:** subscribe → `setState(fullObject)` → read a field in render.  
**Prefer:** subscribe to a **selector** or **slice** so the component re-renders
only when that value changes. Every library below supports this; use it.

**Tree position matters.** The higher a component is in the tree, the more
expensive a re-render becomes, because React re-renders it and all descendants.
Subscribing to the whole store in `App.tsx` is especially bad — every store
change re-renders the entire app. Push subscriptions down to the leaf or
route-level components that actually need the data, or use selectors so
high-level components only re-render when their slice changes.

---

## Library patterns

### XState (actors) — `@xstate/react`

Use `useSelector(actor, selector)` so the component re-renders only when the
selected value changes.

```tsx
// GOOD: stable selector — re-renders only when phase changes
import { useSelector } from "@xstate/react";
import { selectPhase } from "./selectors";

function PhaseIndicator({ actor }) {
  const phase = useSelector(actor, selectPhase);
  return <Text>{phase}</Text>;
}
```

```tsx
// BAD: full snapshot in React state — re-renders on every actor change
const [snapshot, setSnapshot] = useState(null);
useEffect(() => {
  const sub = actor.subscribe((snap) => setSnapshot(snap));
  return () => sub.unsubscribe();
}, [actor]);
const phase = snapshot?.value?.sessionFlow; // unnecessary re-renders
```

**Actor + ref for callbacks:** Keep the actor in `useState` (so `useSelector`
re-subscribes if the actor is replaced) and in a `useRef` for synchronous
access in event handlers:

```tsx
const [actor, setActor] = useState(() => {
  const a = createActor(machine);
  a.start();
  return a;
});
const actorRef = useRef(actor);
actorRef.current = actor;

function send(event) {
  actorRef.current.send(event);
}
```

---

### @xstate/store — `@xstate/store-react`

Use `useSelector(store, selector)` to subscribe to a slice of store context.
Re-renders only when the selected value changes (strict equality by default;
optional custom `compare`).

```tsx
// GOOD: select one field — re-renders only when count changes
import { createStore, useSelector } from "@xstate/store-react";

const store = createStore({
  context: { count: 0, name: "" },
  on: { inc: (ctx) => ({ ...ctx, count: ctx.count + 1 }) },
});

function CountDisplay() {
  const count = useSelector(store, (state) => state.context.count);
  return <span>{count}</span>;
}
```

```tsx
// BAD: selecting whole context — re-renders on any context change
const context = useSelector(store, (state) => state.context);
return <span>{context.count}</span>;
```

Custom comparison when the selector returns an object:

```tsx
const user = useSelector(
  store,
  (state) => state.context.user,
  (prev, next) => prev.id === next.id
);
```

---

### Zustand

Use the store with a **selector** as the first argument. The component
re-renders only when the selected value changes (referential equality).

```tsx
// GOOD: selector — re-renders only when count changes
const count = useStore((state) => state.count);

// GOOD: primitive or stable ref — minimal re-renders
const phase = useStore((state) => state.session.phase);
```

```tsx
// BAD: no selector — re-renders on every store change
const state = useStore();
return <span>{state.count}</span>;
```

```tsx
// BAD: selecting a new object every time — re-renders every time
const { count, name } = useStore((state) => ({ count: state.count, name: state.name }));
// Use two selectors or useShallow instead
```

Use a **module-level selector** so the function reference is stable (see
Selector rules below). For multiple fields, use `useShallow` or pick
primitives:

```tsx
import { useShallow } from "zustand/react/shallow";
const { count, name } = useStore(useShallow((state) => ({ count: state.count, name: state.name })));
```

---

### Redux — `react-redux`

Use `useSelector(selector)` and select the smallest slice needed. Redux uses
referential equality; selecting a new object every time forces re-renders.

```tsx
// GOOD: select a primitive or stable reference
const phase = useSelector((state) => state.session.phase);
const count = useSelector((state) => state.counter);
```

```tsx
// BAD: selecting whole slice — new object ref when any part of session updates
const session = useSelector((state) => state.session);
return <span>{session.phase}</span>;
```

For object slices use `shallowEqual` or a memoized selector:

```tsx
import { shallowEqual, useSelector } from "react-redux";

const { phase, step } = useSelector(
  (state) => ({ phase: state.session.phase, step: state.session.step }),
  shallowEqual
);
```

---

### Nanostores — `@nanostores/react`

Nanostores doesn’t take a selector in the hook; **shape your stores so each
consumer subscribes to a small store**. Use **computed** stores to derive
slices, or split state into multiple atoms.

```tsx
// GOOD: one atom per logical slice, or computed for a derived slice
import { atom, computed } from "nanostores";
import { useStore } from "@nanostores/react";

const $session = atom({ phase: "idle", step: 0 });
const $phase = computed($session, (s) => s.phase);

function PhaseIndicator() {
  const phase = useStore($phase); // re-renders only when phase changes
  return <Text>{phase}</Text>;
}
```

```tsx
// BAD: one big store, useStore on the whole thing — re-renders on any change
const $app = atom({ session: {...}, quiz: {...}, ui: {...} });
function PhaseIndicator() {
  const app = useStore($app);
  return <Text>{app.session.phase}</Text>;
}
```

Use **map** or **atoms** for granular updates and **computed** for derived
values; then each component `useStore`s only the store it needs.

---

### React context

Context re-renders all consumers when the value reference changes. Prefer
**splitting by update frequency** or **exposing a subscribable store** and
selecting in the consumer.

```tsx
// GOOD: split by update frequency
<FrequentContext.Provider value={frequentData}>
  <RareContext.Provider value={rareData}>
    {children}
  </RareContext.Provider>
</RareContext.Provider>
```

```tsx
// GOOD: store in context, select in consumer (e.g. Zustand store, XState actor)
function useSessionPhase() {
  const store = useContext(StoreContext);
  return useSelector(store, (s) => s.phase);
}
```

```tsx
// BAD: one context with everything — any change re-renders all consumers
<AppContext.Provider value={{ user, session, theme, settings, ... }}>
```

---

### useSyncExternalStore (custom stores)

For stores that aren’t one of the above, use React’s `useSyncExternalStore` and
subscribe to a **slice** in `getSnapshot` so the component only re-renders
when that slice changes.

```tsx
// GOOD: getSnapshot returns only the slice this component needs
const phase = useSyncExternalStore(
  store.subscribe,
  () => store.getSnapshot().session.phase,
  () => store.getSnapshot().session.phase
);
```

```tsx
// BAD: getSnapshot returns full state — re-renders on every store change
const state = useSyncExternalStore(store.subscribe, store.getSnapshot, store.getSnapshot);
return <span>{state.session.phase}</span>;
```

---

## Selector rules

1. **Keep selectors at module level** — not inline in the component. Inline
   arrow functions create new references each render and can defeat equality
   checks.

```tsx
// GOOD
const selectPhase = (snap) => snap.value?.sessionFlow;
function MyComponent({ actor }) {
  const phase = useSelector(actor, selectPhase);
}

// BAD — new function ref every render
function MyComponent({ actor }) {
  const phase = useSelector(actor, (snap) => snap.value?.sessionFlow);
}
```

2. **Return primitives or stable references.** If the selector returns a new
   object/array every time, the component will re-render on every update. Prefer
   primitives or use a custom comparison when you must return an object.

3. **Don’t put expensive derivation in selectors.** Heavy work belongs in
   `useMemo` in the component, not in the selector (selectors run often).

---

## Anti-patterns

| Anti-pattern | Why it's bad | Fix |
|--------------|--------------|-----|
| `setState(fullSnapshot)` in subscribe | Every store/actor change re-renders | Use selector / slice (useSelector, selector arg, computed store) |
| No selector / whole store in hook | Same as above | Pass selector to useStore/useSelector; or use computed/small stores |
| Inline selector function | New reference each render | Module-level selector |
| Selector returns new object every time | Always re-renders | Return primitive or use shallowEqual/custom compare |
| Mega-context with everything | Any update re-renders all consumers | Split context or put a store in context and select in consumer |

---

## When to use selectors

**Use a selector / slice when:**
- The component needs 1–2 fields from a larger state
- Different fields update at different rates (e.g. phase rarely, quiz state often)
- Several components each need different parts of the same store
- The component is **high in the tree** (e.g. `App.tsx`, layout, root route) — re-renders there cascade down the whole tree, so avoid subscribing to the whole store at that level

**A single subscription is OK when:**
- The component needs most or all of the state
- Updates are rare (e.g. user profile)
- There’s only one consumer or it’s a leaf with no children

**Rule of thumb:** If a component re-renders more often than its visible output
changes, add a selector (or a computed/small store). Use React DevTools
Profiler to confirm.
