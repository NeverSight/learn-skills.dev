---
name: react-usecallback
description: Use when writing or reviewing useCallback usage in React components. Covers React Compiler impact, when useCallback is justified, and the most common mistake (useCallback without memo).
metadata:
  author: b4r7x
  version: "1.0.0"
---

# React useCallback

## Overview

useCallback memoizes function references between renders. In 2026 with React Compiler, **manual useCallback is rarely needed** — the compiler auto-memoizes. Without the compiler, useCallback only helps when paired with `memo()` on the child component.

## With React Compiler (2025+)

React Compiler 1.0 (Oct 2025) auto-applies memoization at build time. **Don't add new useCallback** — the compiler handles it better. If memoization is unnecessary, the compiler omits it from output.

**Exceptions where manual useCallback is still needed:**
- External libraries not compiled by React Compiler (older react-hook-form, animation libs)
- Functions used as `useEffect` dependencies that can't be moved inside the effect
- Custom hooks exporting functions — wrap in useCallback for stable references
- Measured performance issues the compiler doesn't fix

## Without React Compiler

useCallback only makes sense **together with `memo()` on the child component**.

```jsx
// ❌ useCallback without memo = dead code
function Parent() {
  const handleClick = useCallback(() => {
    console.log('click');
  }, []);
  return <Child onClick={handleClick} />;
  // Child re-renders anyway because Parent re-renders
}

// ✅ useCallback + memo = Child skips re-render
const Child = memo(function Child({ onClick }) {
  return <button onClick={onClick}>Click</button>;
});

function Parent() {
  const handleClick = useCallback(() => {
    console.log('click');
  }, []);
  return <Child onClick={handleClick} />;
  // Child does NOT re-render — handleClick has stable reference
}
```

## Valid Use Cases

### 1. useEffect dependency
```jsx
const fetchData = useCallback(async () => {
  const data = await fetch('/api/users');
}, []);

useEffect(() => {
  fetchData();
}, [fetchData]); // stable reference = runs once
```

### 2. Custom hook exports
```jsx
function useCart() {
  const [items, setItems] = useState([]);
  // ✅ Stable references for hook consumers
  const addItem = useCallback((item) => {
    setItems(prev => [...prev, item]);
  }, []);
  return { items, addItem };
}
```

### 3. Context provider functions
```jsx
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const logout = useCallback(() => setUser(null), []);
  const value = useMemo(() => ({ user, logout }), [user, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
```

## Decision

| Question | Answer |
|----------|--------|
| Using React Compiler? | Don't add useCallback manually |
| Passing fn to `memo()`'d child? | ✅ useCallback |
| Function in useEffect deps? | ✅ useCallback (or move fn inside effect) |
| Exporting fn from custom hook? | ✅ useCallback |
| Event handler without memo on child? | ❌ Skip — it's dead code |

## Common Mistake

The most over-used pattern: wrapping every event handler in useCallback "for performance" without memo on the child. The React docs say explicitly: **use useCallback only for performance optimization, not as a default way to declare functions**.

## References
- [useCallback — React docs](https://react.dev/reference/react/useCallback) — official API reference with usage examples and caveats
- [Understanding useMemo and useCallback](https://www.joshwcomeau.com/react/usememo-and-usecallback/) — Josh Comeau's deep dive on when memoization actually helps
- [React Compiler](https://react.dev/learn/react-compiler) — official guide on how React Compiler replaces manual useCallback
