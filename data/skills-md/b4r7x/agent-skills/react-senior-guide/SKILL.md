---
name: react-senior-guide
description: Use when writing or reviewing any React code as a comprehensive reference. Routes to 7 specialized React skills covering hooks, patterns, and anti-patterns. Includes cross-cutting principles and an AI code review checklist.
metadata:
  author: b4r7x
  version: "1.0.0"
---

# React Senior Guide

## Overview

Comprehensive React reference that routes to specialized skills. Use this as an entry point — it tells you which skill to read for your specific situation.

## Skill Router

| I need to... | Read |
|--------------|------|
| Decide if useCallback is needed | `react-usecallback` |
| Decide if useMemo is needed | `react-usememo` |
| Use Context / optimize re-renders / compound components | `react-usecontext` |
| Choose between useRef and useState | `react-useref` |
| Know if useEffect is the right tool | `react-useeffect` |
| Choose a component pattern (hooks, compound, headless...) | `react-design-patterns` |
| Review code for bugs and anti-patterns | `react-anti-patterns` |
| Optimize render performance | `react-usememo` + `react-usecallback` |
| Decide between useState vs useReducer vs useRef | `react-useref` + `react-anti-patterns` |
| Integrate external library (D3, maps, charts) | `react-useref` + `react-useeffect` |

## Cross-Cutting Principles

### 1. Derive, Don't Sync
If a value can be computed from existing state/props — compute it during render. Never sync derived values via useEffect + setState.

```jsx
// ❌ useEffect to "sync" derived state
useEffect(() => { setFullName(`${first} ${last}`); }, [first, last]);

// ✅ Compute during render
const fullName = `${first} ${last}`;
```

### 2. Events for Actions, Effects for Visibility
- User did something → **event handler**
- Component appeared on screen → **useEffect**

### 3. Measure Before Optimizing
Never add useMemo/useCallback/memo "just in case". Profile with React DevTools first. The only exception: useMemo on Context Provider value (well-understood, predictable benefit).

### 4. Reference Stability Matters for Objects, Not Primitives
React compares primitives (string, number, boolean) by value. Memoizing them is pointless. Objects and arrays are compared by reference — that's where useMemo/useCallback matter.

### 5. State Should Be Minimal
- Store IDs, not copies of objects (derive from source of truth)
- Use union types for status, not multiple booleans
- Related fields → one useState object or useReducer
- If it doesn't affect UI → useRef, not useState

### 6. React Compiler (2025+)
React Compiler auto-memoizes. If you're using it, don't add manual useCallback/useMemo unless you hit a measured issue or work with uncompiled external libraries.

## AI Code Review Checklist

Run this checklist on any AI-generated React code:

| # | Check | Anti-pattern |
|---|-------|-------------|
| 1 | Is `useEffect` doing derived state computation? | Compute during render |
| 2 | Is `useEffect` missing a cleanup return? | Add cleanup |
| 3 | Is `fetch` in useEffect without AbortController/ignore? | Add race condition protection |
| 4 | Are list keys using `index`? | Use stable IDs |
| 5 | Is state initialized from props and synced via effect? | Use controlled/uncontrolled + key |
| 6 | Is `useCallback` used without `memo()` on child? | Remove useCallback or add memo |
| 7 | Is server data fetched manually instead of React Query? | Use React Query |
| 8 | Are loading/error/empty states handled? | Add all states |
| 9 | Are multiple boolean flags used for status? | Use union type |
| 10 | Are components defined inside other components? | Move outside |
| 11 | Is state mutated directly? | Create new references |
| 12 | Are full objects stored in state (duplicated)? | Store IDs, derive objects |
| 13 | Is `&&` used with numbers that could be 0? | Use `> 0 &&` or ternary |
| 14 | Are hooks called conditionally or after early returns? | All hooks at top |
| 15 | Is one mega-context holding all app state? | Split into separate contexts |
| 16 | Is a closure capturing stale state in setTimeout/setInterval/async? | Use ref for current value |
| 17 | Are 5+ related useState calls used instead of useReducer? | Use useReducer or combined state |
| 18 | Is one component >200 lines mixing fetch + logic + UI? | Split into focused components |

## Pattern Decision Flowchart

```
Need reusable logic?
  ├─ Yes → Custom Hook
  │         ├─ Components always used together?
  │         │    └─ Yes → Compound Components
  │         └─ Need logic without imposed HTML/styling?
  │              └─ Yes → Headless Component
  └─ No
      ├─ Need crash isolation? → Error Boundary
      ├─ Need to escape DOM parent? → Portal
      ├─ Need to share stable global state? → Context Provider
      └─ Need full render control from parent? → Render Props
```

## References
- [React Compiler](https://react.dev/learn/react-compiler) — official guide on auto-memoization
- [Understanding useMemo and useCallback](https://www.joshwcomeau.com/react/usememo-and-usecallback/) — Josh Comeau's definitive memoization guide
- [You Might Not Need an Effect — React docs](https://react.dev/learn/you-might-not-need-an-effect) — the most impactful page for AI code review
