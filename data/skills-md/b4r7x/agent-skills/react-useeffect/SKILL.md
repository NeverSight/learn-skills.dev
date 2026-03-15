---
name: react-useeffect
description: Use when writing, reviewing, or debugging useEffect in React. Covers the 6 valid use cases, 6 anti-patterns, dependency pitfalls, and the decision tree for whether you actually need an effect.
metadata:
  author: b4r7x
  version: "1.0.0"
---

# React useEffect

## Overview

useEffect is an **escape hatch** — it synchronizes a component with an external system. If there's no external system involved, you probably don't need an effect.

> "Code that runs because a component was displayed should be in Effects. The rest should be in events." — React docs

## Decision Tree

```
Code you want to run...
  ├─ User clicked / submitted / performed action?
  │         → Event handler
  ├─ Derivable from existing state/props?
  │         → Compute during render (or useMemo)
  ├─ Need to reset state when a prop changes?
  │         → key on the component
  ├─ Need to notify parent about state change?
  │         → Call callback in the same event handler
  └─ Component is visible and must sync with something
     OUTSIDE React (DOM, network, timer, library)?
              → useEffect ✅
```

## Valid Use Cases

### 1. External system connection
```jsx
useEffect(() => {
  const conn = createConnection(serverUrl, roomId);
  conn.connect();
  return () => conn.disconnect(); // always cleanup
}, [serverUrl, roomId]);
```

### 2. Browser event subscription
```jsx
useEffect(() => {
  const handler = () => setIsOnline(navigator.onLine);
  window.addEventListener('online', handler);
  window.addEventListener('offline', handler);
  return () => {
    window.removeEventListener('online', handler);
    window.removeEventListener('offline', handler);
  };
}, []);
```
Consider `useSyncExternalStore` as a less error-prone alternative.

### 3. Data fetch (without framework)
```jsx
// Option A: ignore flag
useEffect(() => {
  let ignore = false;
  fetchUser(userId).then(data => {
    if (!ignore) setUser(data);
  });
  return () => { ignore = true; };
}, [userId]);

// Option B: AbortController (preferred — actually cancels the request)
useEffect(() => {
  const controller = new AbortController();
  fetch(`/api/users/${userId}`, { signal: controller.signal })
    .then(r => r.json())
    .then(setUser)
    .catch(err => {
      if (err.name !== 'AbortError') setError(err);
    });
  return () => controller.abort();
}, [userId]);
```
If using a framework (Next.js, Remix) — use its data fetching mechanism instead.

### 4. Non-React library integration (D3, maps, video)
### 5. Analytics (logging page views)

### 6. Server/client rendering differences
```jsx
function ClientOnlyComponent() {
  const [isClient, setIsClient] = useState(false);
  useEffect(() => { setIsClient(true); }, []);
  if (!isClient) return <ServerFallback />;
  return <div>{localStorage.getItem('theme')}</div>;
}
```

## Anti-patterns

### 1. Derived state (most common mistake)
```jsx
// ❌ Two unnecessary renders
const [total, setTotal] = useState(0);
useEffect(() => {
  setTotal(items.reduce((sum, i) => sum + i.price, 0));
}, [items]);

// ✅ Compute during render
const total = items.reduce((sum, i) => sum + i.price, 0);
```

### 2. Event-specific logic
```jsx
// ❌ Notification fires on every page refresh
useEffect(() => {
  if (product.isInCart) showNotification(`Added ${product.name}!`);
}, [product]);

// ✅ Logic in event handler — only when user clicks
function handleBuyClick() {
  addToCart(product);
  showNotification(`Added ${product.name}!`);
}
```

### 3. Chains of effects
```jsx
// ❌ 3 effects, each triggering the next = 3 unnecessary renders
useEffect(() => { if (card?.gold) setGoldCount(c => c + 1); }, [card]);
useEffect(() => { if (goldCount > 3) { setRound(r => r + 1); setGoldCount(0); } }, [goldCount]);
useEffect(() => { if (round > 5) setIsGameOver(true); }, [round]);

// ✅ All logic in one event handler — single render
function handlePlaceCard(nextCard) {
  setCard(nextCard);
  if (nextCard.gold) {
    if (goldCount < 3) setGoldCount(goldCount + 1);
    else { setGoldCount(0); setRound(round + 1); }
  }
}
const isGameOver = round > 5; // derived, not state
```

### 4. Notifying parent via effect
```jsx
// ❌ Double render
useEffect(() => { onChange(isOn); }, [isOn, onChange]);

// ✅ Both states in one interaction
function handleClick() {
  const next = !isOn;
  setIsOn(next);
  onChange(next); // immediately, in same event
}
```

### 5. Resetting state via effect
```jsx
// ❌ Renders with stale state first, then resets
useEffect(() => { setComment(''); }, [userId]);

// ✅ key forces React to reset all state
<Profile key={userId} userId={userId} />
```

### 6. App initialization
```jsx
// ❌ Runs twice in Strict Mode
useEffect(() => { checkAuthToken(); }, []);

// ✅ Module-level (runs once on import)
if (typeof window !== 'undefined') { checkAuthToken(); }
```

## Dependency Pitfalls

### Object as dependency
```jsx
// ❌ New object every render = effect runs every render
const options = { serverUrl, roomId };
useEffect(() => { /* ... */ }, [options]);

// ✅ Create object inside effect
useEffect(() => {
  const options = { serverUrl, roomId };
  // ...
}, [roomId]); // only primitive deps
```

### Functional updater to avoid deps
```jsx
// ❌ count in deps = reset interval on every change
useEffect(() => {
  const id = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(id);
}, [count]);

// ✅ Functional update — no count in deps
useEffect(() => {
  const id = setInterval(() => setCount(c => c + 1), 1000);
  return () => clearInterval(id);
}, []);
```

## Cleanup Checklist

Every effect that subscribes, connects, or sets a timer **must return a cleanup function**:
- `setInterval` → `clearInterval`
- `addEventListener` → `removeEventListener`
- WebSocket connect → disconnect
- `fetch` → `AbortController.abort()` or ignore flag

## References
- [Synchronizing with Effects — React docs](https://react.dev/learn/synchronizing-with-effects) — official guide on when useEffect is needed
- [You Might Not Need an Effect — React docs](https://react.dev/learn/you-might-not-need-an-effect) — official decision tree for avoiding unnecessary effects
