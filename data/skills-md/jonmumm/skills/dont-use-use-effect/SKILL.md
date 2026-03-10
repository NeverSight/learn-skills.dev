---
name: dont-use-use-effect
description: >
  Avoid unnecessary useEffect in React components. Most uses of useEffect are
  anti-patterns — derived state, event-driven logic, data fetching, and external
  store subscriptions all have better, more idiomatic alternatives. Apply this
  skill when writing or reviewing React components that use useEffect.
---

# Don't Use useEffect

`useEffect` is one of the most misused hooks in React. In the vast majority of cases where developers reach for it, there is a simpler, more performant, and more correct alternative. Every unnecessary `useEffect` introduces an extra render cycle, increases the risk of bugs (stale closures, race conditions, infinite loops), and makes components harder to reason about.

**The golden rule:** Effects are for **synchronizing with external systems** (DOM APIs, timers, websockets, third-party widgets). If the work you're doing is a response to a user event, or can be calculated from existing state/props, you don't need an Effect.

---

## 1. Derived State — Just Calculate It

The most common `useEffect` anti-pattern: storing a value in state that can be computed from other state or props.

```tsx
// 🔴 BAD: Redundant state + unnecessary Effect
function Form() {
  const [firstName, setFirstName] = useState('Taylor');
  const [lastName, setLastName] = useState('Swift');
  const [fullName, setFullName] = useState('');

  useEffect(() => {
    setFullName(firstName + ' ' + lastName);
  }, [firstName, lastName]);

  return <span>{fullName}</span>;
}
```

This causes **two renders** every time `firstName` or `lastName` changes: one with the stale `fullName`, and another after the Effect updates it.

```tsx
// ✅ GOOD: Calculate during render
function Form() {
  const [firstName, setFirstName] = useState('Taylor');
  const [lastName, setLastName] = useState('Swift');

  // Derived — no state, no Effect, one render
  const fullName = firstName + ' ' + lastName;

  return <span>{fullName}</span>;
}
```

For **expensive calculations**, wrap in `useMemo` instead of storing in state:

```tsx
// ✅ GOOD: Memoize expensive derivations
function TodoList({ todos, filter }) {
  const [newTodo, setNewTodo] = useState('');

  // Only recomputes when todos or filter change, not when newTodo changes
  const visibleTodos = useMemo(
    () => getFilteredTodos(todos, filter),
    [todos, filter]
  );

  return <ul>{visibleTodos.map(todo => <li key={todo.id}>{todo.text}</li>)}</ul>;
}
```

---

## 2. Event-Driven Logic — Use Event Handlers

If code should run **because the user did something** (clicked, submitted, typed), it belongs in an event handler — not an Effect. Effects run because a component **rendered**, not because the user took an action.

```tsx
// 🔴 BAD: Event-specific logic triggered by state change in an Effect
function ProductPage({ product, addToCart }) {
  useEffect(() => {
    if (product.isInCart) {
      showNotification(`Added ${product.name} to the cart!`);
    }
  }, [product]);

  function handleBuyClick() {
    addToCart(product);
  }
  // ...
}
```

This is buggy: the notification fires on page reload if the product is already in the cart.

```tsx
// ✅ GOOD: Side effects belong in the event handler that caused them
function ProductPage({ product, addToCart }) {
  function buyProduct() {
    addToCart(product);
    showNotification(`Added ${product.name} to the cart!`);
  }

  function handleBuyClick() {
    buyProduct();
  }

  function handleCheckoutClick() {
    buyProduct();
    navigateTo('/checkout');
  }
  // ...
}
```

**Rule of thumb:** If you can point to the exact user interaction that should trigger the code, put it in that interaction's event handler.

---

## 3. Effect Chains — Consolidate Into Event Handlers

Chaining Effects that each set state based on other state creates a cascade of unnecessary re-renders and rigid, fragile code.

```tsx
// 🔴 BAD: Chain of Effects triggering each other (4 render passes!)
function Game() {
  const [card, setCard] = useState(null);
  const [goldCardCount, setGoldCardCount] = useState(0);
  const [round, setRound] = useState(1);
  const [isGameOver, setIsGameOver] = useState(false);

  useEffect(() => {
    if (card !== null && card.gold) {
      setGoldCardCount(c => c + 1);
    }
  }, [card]);

  useEffect(() => {
    if (goldCardCount > 3) {
      setRound(r => r + 1);
      setGoldCardCount(0);
    }
  }, [goldCardCount]);

  useEffect(() => {
    if (round > 5) setIsGameOver(true);
  }, [round]);
  // ...
}
```

```tsx
// ✅ GOOD: Derive what you can, compute the rest in the event handler
function Game() {
  const [card, setCard] = useState(null);
  const [goldCardCount, setGoldCardCount] = useState(0);
  const [round, setRound] = useState(1);

  // Derived — no state needed
  const isGameOver = round > 5;

  function handlePlaceCard(nextCard) {
    if (isGameOver) throw Error('Game already ended.');

    setCard(nextCard);
    if (nextCard.gold) {
      if (goldCardCount < 3) {
        setGoldCardCount(goldCardCount + 1);
      } else {
        setGoldCardCount(0);
        setRound(round + 1);
        if (round === 5) alert('Good game!');
      }
    }
  }
  // ...
}
```

---

## 4. Data Fetching — Use a Data-Fetching Library

Fetching data in `useEffect` is fragile. You must manually handle race conditions, loading states, caching, error handling, and cleanup. Raw `useEffect` fetching has **no caching, no deduplication, and no SSR support**.

```tsx
// 🔴 BAD: Manual fetch in useEffect — race conditions, no caching, no SSR
function SearchResults({ query }) {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let ignore = false;
    setIsLoading(true);
    fetchResults(query).then(json => {
      if (!ignore) {
        setResults(json);
        setIsLoading(false);
      }
    });
    return () => { ignore = true; };
  }, [query]);
  // ...
}
```

```tsx
// ✅ GOOD: Use TanStack Query (or your framework's data primitive)
import { useQuery } from '@tanstack/react-query';

function SearchResults({ query }) {
  const { data: results = [], isLoading } = useQuery({
    queryKey: ['search', query],
    queryFn: () => fetchResults(query),
    enabled: !!query,
  });
  // Automatic caching, deduplication, race-condition handling,
  // background refetching, and SSR support — for free.
}
```

**Other good alternatives:**
- **Next.js / Remix:** `loader` functions, Server Components, `use()` + Suspense
- **SWR:** `useSWR(key, fetcher)` — similar to TanStack Query
- **tRPC:** End-to-end type-safe fetching with built-in React Query integration

If you **must** use `useEffect` for fetching (no framework, no library), at minimum:
1. Add the `ignore` cleanup flag to prevent race conditions
2. Extract the logic into a reusable custom hook (e.g. `useData(url)`)
3. Handle loading, error, and empty states explicitly

---

## 5. External Store Subscriptions — Use `useSyncExternalStore`

Subscribing to an external data source (browser API, third-party store, observable) using `useEffect` + `setState` is both boilerplate-heavy and can cause tearing in concurrent mode.

```tsx
// 🔴 BAD: Manual subscription with useEffect
function OnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return <span>{isOnline ? '✅ Online' : '❌ Offline'}</span>;
}
```

```tsx
// ✅ GOOD: useSyncExternalStore — concurrent-safe, less code
import { useSyncExternalStore } from 'react';

function subscribe(callback: () => void) {
  window.addEventListener('online', callback);
  window.addEventListener('offline', callback);
  return () => {
    window.removeEventListener('online', callback);
    window.removeEventListener('offline', callback);
  };
}

function getSnapshot() {
  return navigator.onLine;
}

function OnlineStatus() {
  const isOnline = useSyncExternalStore(subscribe, getSnapshot);
  return <span>{isOnline ? '✅ Online' : '❌ Offline'}</span>;
}
```

For state management libraries, use their built-in React hooks instead of manual subscriptions. See the [react-render-performance](../react-render-performance/SKILL.md) skill for selector-based patterns with XState, Zustand, Redux, and Nanostores.

---

## 6. Resetting State on Prop Changes — Use a `key`

Don't use `useEffect` to reset state when a prop changes. React has a built-in mechanism: the `key` prop.

```tsx
// 🔴 BAD: Resetting state in an Effect
function EditProfile({ userId }) {
  const [comment, setComment] = useState('');

  useEffect(() => {
    setComment('');
  }, [userId]);

  return <textarea value={comment} onChange={e => setComment(e.target.value)} />;
}
```

```tsx
// ✅ GOOD: Use key to reset component state
function ProfilePage({ userId }) {
  // When userId changes, React unmounts the old EditProfile and mounts a new one
  return <EditProfile userId={userId} key={userId} />;
}

function EditProfile({ userId }) {
  const [comment, setComment] = useState('');
  return <textarea value={comment} onChange={e => setComment(e.target.value)} />;
}
```

---

## When `useEffect` IS Correct

Effects are appropriate for synchronizing your component with something **outside of React**:

| Use Case | Why It's Correct |
|----------|-----------------|
| Integrating a non-React widget (map, chart, video player) | Syncing React state → imperative DOM API |
| Setting up a WebSocket or EventSource connection | External system lifecycle tied to component |
| Measuring DOM layout (`getBoundingClientRect`, `ResizeObserver`) | Reading post-render DOM information |
| Managing focus or scroll position imperatively | Imperative DOM interaction |
| Connecting to hardware APIs (camera, geolocation) | External system with subscribe/cleanup |
| `document.title` or other global side-effects | Syncing React state → browser API |

Even for these, consider whether a library already handles it (e.g., `react-intersection-observer`, `framer-motion`).

---

## Decision Flowchart

Ask yourself these questions before writing `useEffect`:

1. **Can I calculate this from existing props/state?** → Derive it during render (or `useMemo`).
2. **Is this a response to a user action?** → Put it in the event handler.
3. **Am I fetching data?** → Use TanStack Query, SWR, or your framework's data primitive.
4. **Am I subscribing to an external store?** → Use `useSyncExternalStore` or the library's hook.
5. **Am I resetting state when a prop changes?** → Use the `key` prop.
6. **Am I syncing with an external system that React doesn't control?** → ✅ This is a valid `useEffect`.

---

## Summary Checklist

- [ ] No `useEffect` that sets state derived from other state/props — calculate during render instead
- [ ] No `useEffect` that runs logic in response to user events — use event handlers instead
- [ ] No chains of `useEffect`s that trigger each other via state updates — consolidate into event handlers or derived values
- [ ] No raw `useEffect` for data fetching — use TanStack Query, SWR, or framework data primitives
- [ ] No `useEffect` + `setState` for external store subscriptions — use `useSyncExternalStore` or library hooks
- [ ] No `useEffect` to reset state when props change — use the `key` prop
- [ ] Every remaining `useEffect` is syncing with a genuine external system (DOM API, WebSocket, third-party widget)
