---
name: react-useeffect-avoid
description:
  Guides when NOT to use useEffect and suggests better alternatives. Use when reviewing React code, troubleshooting performance, or considering useEffect for derived state or form resets.
---

# React: When Not to Use useEffect

## Core Principle

**`useEffect` is an escape hatch for synchronizing with external systems, not a general-purpose tool for state management or event handling.**

Modern React patterns prioritize **one-way data flow** and **event-driven updates** over effect-based synchronization to avoid performance penalties and complex synchronization bugs.

---

## When NOT to Use useEffect

### 1. ❌ Calculating Derived State

**Problem:** Computing one state value from another using `useEffect` causes unnecessary double-renders and complexity.

```jsx
// ❌ BAD: Double render cycle
function FilteredList({ items }) {
  const [query, setQuery] = useState('');
  const [filtered, setFiltered] = useState([]);

  useEffect(() => {
    setFiltered(items.filter(item => item.name.includes(query)));
  }, [items, query]); // Renders twice on every input

  return <ul>{filtered.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

**✅ Solution:** Calculate derived state directly during render.

```jsx
// ✅ GOOD: Single render, no effect needed
function FilteredList({ items }) {
  const [query, setQuery] = useState('');

  // Calculated every render - no state, no effect
  const filtered = items.filter(item => item.name.includes(query));

  return <ul>{filtered.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

**Why it's better:**
- Immediate feedback UI updates (no double render pause)
- Simpler mental model: what you see is what you get
- No dependency array to manage
- React can optimize calculations via memoization when needed

---

### 2. ❌ Resetting State When a Prop Changes

**Problem:** Watching a prop change and manually resetting state causes stale data display and extra renders.

```jsx
// ❌ BAD: Shows old state briefly, then new
function UserForm({ userId }) {
  const [userName, setUserName] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    setUserName('');  // First render shows old userName
    setEmail('');    // Then this effect runs to reset
  }, [userId]);      // Double render every userId change

  return (
    <form>
      <input value={userName} onChange={e => setUserName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
    </form>
  );
}
```

**✅ Solution A: Key Prop (Preferred)**
```jsx
// ✅ GOOD: React tears down and rebuilds component
function App() {
  const [userId, setUserId] = useState(1);

  return (
    <div>
      <button onClick={() => setUserId(prev => prev + 1)}>Next User</button>
      {/* Different key = different component instance */}
      <UserForm key={userId} userId={userId} />
    </div>
  );
}
```

**✅ Solution B: Derived State (When you only need partial reset)**
```jsx
// ✅ GOOD: Only reset specific values, keep others
function UserForm({ userId }) {
  const [userName, setUserName] = useSyncExternalStore(
    () => ({ onSet: setUserName }), // Reset when userId changes
    { value: '' }
  );
  const [email, setEmail] = useState('');

  // Email persists, userName resets
  return <form>...</form>;
}
```

**⚠️ Caveat:** The `key` prop approach remounts the entire component. Use when you need a complete state reset. For partial resets, consider derived state patterns.

---

### 3. ❌ Waterfall of State Updates

**Problem:** Multiple effects triggering each other create cascading renders that are hard to debug.

```jsx
// ❌ BAD: Effects trigger effects
function OrderForm() {
  const [formData, setFormData] = useState({});
  const [validated, setValidated] = useState(false);
  const [error, setError] = useState(null);

  // Effect 1: Validate when formData changes
  useEffect(() => {
    setValidated(validateData(formData));
  }, [formData]);

  // Effect 2: Set error when validation changes
  useEffect(() => {
    setError(validated ? null : 'Invalid');
  }, [validated]);

  // Effect 3: Submit when no error
  useEffect(() => {
    if (!error && validated) submitOrder(formData);
  }, [error, validated, formData]);
}
```

**✅ Solution:** Handle all logic in event handler.

```jsx
// ✅ GOOD: One handler, one render, clear flow
function OrderForm() {
  const [formData, setFormData] = useState({});

  const handleSubmit = () => {
    // All logic happens atomically
    if (validateData(formData)) {
      submitOrder(formData);  // No intermediate states
    } else {
      setError('Invalid form');  // Set directly, no cascade
    }
  };

  return <button onClick={handleSubmit}>Submit</button>;
}
```

---

### 4. ❌ Fetching Data on User Action

**Problem:** Using a flag to trigger effects loses user intent and creates fragile code.

```jsx
// ❌ BAD: Intent is lost, hard to follow
function LoginForm() {
  const [username, setUsername] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    setSubmitted(true);  // Just a flag, no actual logic
  };

  useEffect(() => {
    if (submitted) {
      login(username);  // What triggered this? Which submit was it?
    }
  }, [submitted, username]);
}
```

**✅ Solution:** Perform action directly in handler.

```jsx
// ✅ GOOD: Clear intent, direct action
function LoginForm() {
  const [username, setUsername] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();  // User action context preserved

    // Actual logic here, not delayed
    try {
      await login(username);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

---

### 5. ❌ Filtering/Transforming Lists

**Problem:** Creating filtered lists via effects is a common mistake that causes extra renders.

```jsx
// ❌ BAD: Unnecessary effect
function ProductList({ products }) {
  const [visibleProducts, setVisibleProducts] = useState([]);

  useEffect(() => {
    setVisibleProducts(products.filter(p => p.inStock));
  }, [products]); // Runs twice whenever products change
}
```

**✅ Solution:** Filter directly during render.

```jsx
// ✅ GOOD: Immediate, single render
function ProductList({ products }) {
  const visibleProducts = products.filter(p => p.inStock);
}
```

---

### 6. ❌ Subscribing to Browser APIs (Without useSyncExternalStore)

**Problem:** Using `useState` + `useEffect` for external subscriptions causes "tearing" in concurrent rendering.

```jsx
// ❌ BAD: UI can show inconsistent state during concurrent updates
function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
}
```

**✅ Solution:** Use `useSyncExternalStore` for external state.

```jsx
// ✅ GOOD: Prevents tearing, single source of truth
function WindowSize() {
  const width = useSyncExternalStore(
    // Subscribe - return cleanup function
    (callback) => {
      window.addEventListener('resize', callback);
      return () => window.removeEventListener('resize', callback);
    },
    // Get snapshot
    () => window.innerWidth,
    // Server fallback
    () => 1200
  );
}
```

**Why it's better:**
- React can guarantee UI consistency even during concurrent rendering
- Single source of truth
- Built-in optimization - subscription fires only when needed

---

### 7. ❌ Initial Data Fetch Without Dependencies (Stale Data)

**Problem:** Empty dependency array with state inside effect causes stale bugs.

```jsx
// ❌ BAD: Id never updates, always fetches user 1
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch(`/user/1`).then(res => res.json()).then(setUser);
  }, [ ]); // Missing userId dependency!
}
```

**✅ Solution:** Include all dependencies or use proper patterns.

```jsx
// ✅ GOOD: Correct dependencies
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch(`/user/${userId}`).then(res => res.json()).then(setUser);
  }, [userId]); // Properly tracks changes
}
```

**Better:** Move to event-driven fetching or data libraries.

```jsx
// ✅ EVEN BETTER: No effect, just loader
function UserProfile({ userId }) {
  const user = use(userId); // React 19's use API
  // Or use React Query, SWR, etc.
}
```

---

## Decision Tree: useEffect vs Alternatives

```
Need to sync with external system?
├─ Yes (browser APIs, websockets, timers)
│  └─ Use useEffect
│
└─ No (pure React application logic)
   ├─ Derived state calculation?
   │  ├─ Yes → Calculate during render
   │  └─ No → Continue...
   │
   ├─ User action triggered?
   │  ├─ Yes → Use event handler
   │  └─ No → Continue...
   │
   ├─ State reset needed?
   │  ├─ Yes → Use key prop
   │  └─ No → Continue...
   │
   └─ Really need effect after re-think?
      └─ Yes → Use useState/useReducer/setState pattern
```

---

## Patterns to Always Avoid

### ❌ 1. useEffect for DOM Manipulation (without refs)

```jsx
// BAD
function Modal() {
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = ''; };
  }, []);
}
```

**✅ Better:** Use refs or layout effects when needed.

---

### ❌ 2. useEffect for Logging

```jsx
// BAD
function App({ data }) {
  useEffect(() => {
    console.log('Data changed:', data);
  }, [data]);
}
```

**✅ Better:** Log in event handler or use `React DevTools` profiling.

---

### ❌ 3. useEffect for Component Initialization

```jsx
// BAD
function Widget() {
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    someLibrary.init();
    setInitialized(true);
  }, []);
}
```

**✅ Better:** Initialize outside component effect:

```jsx
// GOOD
let initialized = false;

function Widget() {
  if (!initialized) {
    someLibrary.init();
    initialized = true;
  }
}
```

Or use library-specific initialization patterns.

---

## Quick Reference

### ❌ Don't use useEffect for:

| Scenario | Problem | Alternative |
|----------|---------|-------------|
| **Derived state** | Double render | Calculate during render |
| **State resets** | Stale data | Use `key` prop |
| **User actions** | Lost intent | Event handlers |
| **List filtering** | Extra renders | Filter in render |
| **Browser APIs** | Tearing bugs (concurrent) | `useSyncExternalStore` |
| **Form submission** | Fragile flag pattern | Direct async handler |
| **Data fetching** | Manual cache management | React Query, SWR, Suspense |

### ✅ DO use useEffect for:

- Subscribing to external systems (websockets, browser APIs, etc.)
- Setting up timers with cleanup
- Managing third-party library integration
- Document title changes
- Analytics/telemetry when rendering completes

---

## React 19: New Alternatives

React 19 introduces the `use` API for reading resources in render:

```jsx
// React 19+ - Direct resource reading
function UserProfile({ userId }) {
  const user = use(fetchUser(userId)); // Reads promise directly

  return <div>{user.name}</div>;
}
```

This eliminates many data-fetching useEffect patterns entirely.

---

## References and Further Reading

### Official Documentation
- [React Docs: You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [React Docs: Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)
- [React Docs: useSyncExternalStore](https://react.dev/reference/react/useSyncExternalStore)

### Articles from Senior Engineers
- [LogRocket: 15 Common useEffect Mistakes](https://blog.logrocket.com/15-common-useeffect-mistakes-react/) - Comprehensive anti-pattern catalog
- [Epic React: Myths About useEffect](https://www.epicreact.dev/myths-about-useeffect) - Kent Dodds on mental models
- [Kent Dodds: useSyncExternalStore Demystified](https://www.epicreact.dev/use-sync-external-store-demystified-for-practical-react-development-w5ac0)

### Key Principles
1. **Effects are escape hatches** - use only when stepping outside React
2. **Event-driven > Effect-driven** - prefer handlers for user actions
3. **Render-time > Effect-time** - calculate values during render
4. **Single source of truth** - avoid duplicating state in effects
5. **Concurrent-safe** - use specialized hooks for external subscriptions