---
name: react-anti-patterns
description: Use when reviewing React code — especially AI-generated code — to catch common anti-patterns. Covers 18 anti-patterns with detection difficulty, including stale closures, state mutation, useEffect abuse, and boolean explosion.
metadata:
  author: b4r7x
  version: "1.0.0"
---

# React Anti-patterns

## Overview

18 anti-patterns commonly found in AI-generated and junior React code. Organized by detection difficulty — **hard-to-detect bugs first**.

## Hard to Detect

### 1. Stale Closure
```jsx
// ❌ count is always 0 in the timeout — closure captured old value
const handleDelayedAlert = () => {
  setTimeout(() => alert(`Count: ${count}`), 3000);
};

// ✅ useRef for current value in async/timeout
const countRef = useRef(count);
useEffect(() => { countRef.current = count; });
const handleDelayedAlert = () => {
  setTimeout(() => alert(`Count: ${countRef.current}`), 3000);
};
```

### 2. Component Inside Component
```jsx
// ❌ New component reference every render = unmount/remount cycle
function List({ items }) {
  const ListItem = ({ item }) => <div>{item.name}</div>; // INSIDE!
  return items.map(item => <ListItem key={item.id} item={item} />);
}

// ✅ Define outside
const ListItem = ({ item }) => <div>{item.name}</div>;
function List({ items }) {
  return items.map(item => <ListItem key={item.id} item={item} />);
}
```

### 3. State Duplication (out of sync)
```jsx
// ❌ selectedUser is a copy — gets stale when users updates
const [users, setUsers] = useState([]);
const [selectedUser, setSelectedUser] = useState(null); // full object!

// ✅ Store only ID — derive the object
const [selectedUserId, setSelectedUserId] = useState(null);
const selectedUser = users.find(u => u.id === selectedUserId) ?? null;
```

## Medium to Detect

### 4. State Mutation
```jsx
// ❌ Mutating — React doesn't see the change
const todo = todos.find(t => t.id === id);
todo.done = !todo.done; // mutation!
setTodos(todos); // same reference — no re-render

// ✅ New reference
setTodos(prev => prev.map(t => t.id === id ? { ...t, done: !t.done } : t));
```

### 5. Boolean Explosion
```jsx
// ❌ 2^4 = 16 combinations, most impossible
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
const [isRetrying, setIsRetrying] = useState(false);

// ✅ Finite state machine
type Status = 'idle' | 'loading' | 'success' | 'error' | 'retrying';
const [status, setStatus] = useState<Status>('idle');
```

### 6. useCallback Without memo
```jsx
// ❌ useCallback alone = dead code (Child re-renders anyway)
const handleClick = useCallback(() => {}, []);
return <Child onClick={handleClick} />;

// ✅ Only useful WITH memo on the child
const Child = memo(function Child({ onClick }) { /* ... */ });
```

### 7. Props Mirroring in State
```jsx
// ❌ Syncing props to state via useEffect
const [title, setTitle] = useState(initialTitle);
useEffect(() => { setTitle(initialTitle); }, [initialTitle]);

// ✅ Fully controlled
<input value={title} onChange={e => onChange(e.target.value)} />

// ✅ Or fully uncontrolled with key reset
<EditableTitle key={userId} initialTitle={title} />
```

### 8. Mega-Context
```jsx
// ❌ One context — any change re-renders ALL consumers
<AppContext.Provider value={{ user, cart, theme, notifications }}>

// ✅ Separate, isolated contexts
<ThemeProvider><AuthProvider><CartProvider>{children}</CartProvider></AuthProvider></ThemeProvider>
```

### 9. Granular useState Instead of useReducer
```jsx
// ❌ 6 related useState calls — hard to reset, easy to desync
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
// ... 4 more

// ✅ One state object or useReducer
const [form, setForm] = useState({ firstName: '', lastName: '', /* ... */ });
const updateField = (field) => (e) => setForm(prev => ({ ...prev, [field]: e.target.value }));
```

## Easy to Detect

### 10. useEffect for Derived State
```jsx
// ❌ Two unnecessary renders
useEffect(() => { setTotal(items.reduce((s, i) => s + i.price, 0)); }, [items]);

// ✅ Compute during render
const total = items.reduce((s, i) => s + i.price, 0);
```

### 11. Missing useEffect Cleanup
```jsx
// ❌ Memory leak
useEffect(() => { setInterval(() => setCount(c => c + 1), 1000); }, []);

// ✅ Always cleanup
useEffect(() => {
  const id = setInterval(() => setCount(c => c + 1), 1000);
  return () => clearInterval(id);
}, []);
```

### 12. key={index} on Dynamic Lists
```jsx
// ❌ Removing item from middle = broken re-renders, lost input state
{items.map((item, index) => <TodoItem key={index} item={item} />)}

// ✅ Stable unique ID
{items.map(item => <TodoItem key={item.id} item={item} />)}
```
`key={index}` is OK only for static, never-reordered lists.

### 13. Manual Fetch Instead of React Query
```jsx
// ❌ No cache, no retry, no dedup, race conditions
const [user, setUser] = useState(null);
const [loading, setLoading] = useState(true);
useEffect(() => { fetch(`/api/users/${id}`).then(/* ... */); }, [id]);

// ✅ React Query handles all edge cases
const { data: user, isLoading } = useQuery({
  queryKey: ['user', id],
  queryFn: () => fetch(`/api/users/${id}`).then(r => r.json()),
});
```

### 14. Missing Loading/Error/Empty States
```jsx
// ❌ Only happy path — crashes on undefined
return data.map(p => <ProductCard key={p.id} product={p} />);

// ✅ All states handled
if (isLoading) return <Skeleton />;
if (error) return <ErrorMessage error={error} />;
if (!data?.length) return <EmptyState />;
return data.map(p => <ProductCard key={p.id} product={p} />);
```

### 15. Conditional Hooks
```jsx
// ❌ Breaks Rules of Hooks — React loses track of hook order
if (isAdmin) { const data = useAdminData(); }

// ✅ All hooks at top, conditions in JSX or inside hooks
const adminData = useAdminData();
if (!userId) return null; // return AFTER all hooks
```

### 16. `&&` With Numbers Rendering "0"
```jsx
// ❌ When count === 0, renders "0" in UI
{count && <CartBadge count={count} />}

// ✅ Explicit boolean
{count > 0 && <CartBadge count={count} />}
```

### 17. God Components
AI generates one 300-line component mixing fetch + logic + UI + forms. **Split into focused components with their own state/hooks.**

### 18. Batching Surprise (React 18+)
React 18 auto-batches all state updates (even in async). If you need immediate render (e.g., to measure DOM), use `flushSync`:
```jsx
import { flushSync } from 'react-dom';
flushSync(() => setCount(1)); // renders immediately
console.log(ref.current.offsetHeight); // safe to measure
```

## Code Review Checklist

| Check | Question |
|-------|----------|
| `useEffect` | Is it truly needed, or is this derived state? |
| `useEffect` | Is there a cleanup `return`? |
| `fetch` in effect | AbortController or ignore flag? |
| Lists | key is stable ID, not index? |
| `useState` + props | Props mirroring? |
| `useCallback`/`useMemo` | Is there `memo()` on the receiving child? |
| Server data | Should this be React Query instead? |
| Component states | Loading, error, empty, success all handled? |
| State shape | Boolean explosion? Use union type. |
| Component definitions | Any components defined inside other components? |
| Closures | Stale state in setTimeout/setInterval/async? |

## References
- [You Might Not Need an Effect — React docs](https://react.dev/learn/you-might-not-need-an-effect) — official guide identifying the most common useEffect anti-patterns
- [React Anti-Patterns and Best Practices](https://www.perssondennis.com/articles/react-anti-patterns-and-best-practices-dos-and-donts) — comprehensive list of dos and don'ts with examples
