---
name: cleanup-useeffect
description: Use when writing new React components that involve state derived from props, event-driven side effects, or external subscriptions. Also use when auditing existing code for unnecessary useEffect calls, reviewing useEffect-heavy components, or refactoring to eliminate cascading renders. Applies to React 18+ codebases.
license: CC-BY-NC 4.0
---

# Avoiding and Removing Redundant useEffect

## Overview

Most `useEffect` calls can be replaced with render-time computation, `useMemo`, event handlers, `key` props, or `useSyncExternalStore`. This skill helps you avoid writing unnecessary Effects in the first place and identify them in existing code.

**Core principle:** Effects synchronize with external systems (DOM, network, browser APIs). If there's no external system, you don't need an Effect.

## When to Use

- Writing a new component and considering `useEffect`
- About to add state that mirrors or derives from existing props/state
- Auditing a codebase for Effect overuse
- Reviewing a component with multiple `useEffect` calls
- Performance profiling reveals cascading renders

## Writing New Components: Think Before You Effect

Before reaching for `useEffect`, ask:

1. **Can I compute this during render?** → Derived value, no state needed
2. **Am I caching an expensive computation?** → `useMemo`
3. **Am I reacting to a user event?** → Put it in the event handler
4. **Am I resetting state when a prop changes?** → `key` prop on the component
5. **Am I subscribing to something outside React?** → `useSyncExternalStore` or legitimate Effect with cleanup

If none of these apply, you probably need an Effect. If #1–#4 apply, you definitely don't.

### State Design Checklist

When adding state to a component, verify each variable:

- **Can it be computed from other state or props?** → Don't store it. Compute it.
- **Does it reset when a prop changes?** → Use `key` on the component, not an Effect to reset.
- **Does it only change in response to user events?** → Update it in the event handler, not via Effect watching a flag.
- **Is it tracking an external value (DOM, localStorage, media query)?** → Use `useSyncExternalStore` if the value can change reactively. Use a mount Effect only for one-time reads.

## Quick Reference: The 11 Anti-Patterns

| # | Anti-Pattern | Symptom | Fix |
|---|---|---|---|
| 1 | Deriving state from props/state | `useEffect(() => setFullName(a+b), [a,b])` | Compute during render: `const fullName = a + b` |
| 2 | Caching calculations | `useEffect(() => setFiltered(filter(items)), [items])` | `useMemo(() => filter(items), [items])` |
| 3 | Resetting all state on prop change | `useEffect(() => setComment(''), [userId])` | Pass `key={userId}` to parent component |
| 4 | Adjusting state on prop change | `useEffect(() => setSelection(null), [items])` | Compute from ID: `items.find(id => id === selectedId)` or use prev-items pattern during render |
| 5 | Event-specific logic in Effects | `useEffect(() => { if (x) notify() }, [x])` | Call from event handler that changed `x` |
| 6 | Chains of computations | Multiple Effects each calling `setState` to trigger next | Compute all next state in one event handler |
| 7 | App init in Effects | `useEffect(() => loadCache(), [])` | Lazy state initializer: `useState(() => loadCache())` or module-level `if (typeof window !== 'undefined')` |
| 8 | Notifying parent from Effect | `useEffect(() => onChange(value), [value])` | Call `onChange` in the same event handler that sets `value` |
| 9 | Passing data to parent via Effect | `useEffect(() => onFetched(data), [data])` | Fetch in parent, pass down; or move Effect to parent |
| 10 | Subscribing to external store in Effect | Manual `addEventListener`/`removeEventListener` to sync store → state | `useSyncExternalStore(subscribe, getSnapshot)` |
| 11 | Fetching data without cleanup | `useEffect(() => { fetch(...).then(setData) }, [query])` | Add AbortController or `let ignore = false` flag with cleanup |

## Legitimate Effects (NOT Anti-Patterns)

These SHOULD use `useEffect` — in both new and existing code:

- **DOM subscriptions with cleanup**: scroll, resize, `mousemove`, `keydown`, click-outside, IntersectionObserver, ResizeObserver, MutationObserver
- **Browser API subscriptions**: `matchMedia`, `navigator.onLine`, geolocation
- **Imperative library lifecycles**: CodeMirror, Three.js renderers, video players — setup/teardown
- **Animation loops**: `requestAnimationFrame` with cleanup
- **Timers with cleanup**: `setInterval`, `setTimeout` (but prefer event handlers for one-time delays)
- **Focus management**: Auto-focusing inputs after mount
- **Data fetching WITH cleanup**: AbortController or `ignore` flag for race-condition prevention
- **External store reads (transitional)**: localStorage/sessionStorage reads on mount (but prefer `useSyncExternalStore` for reactivity)

## Decision Rules for Borderline Cases

### 1. Auto-Save Effects

```tsx
useEffect(() => {
  const timer = setTimeout(() => saveDraft(content), 500)
  return () => clearTimeout(timer)
}, [content])
```

**Classification:** **Legitimate** if debounced (setTimeout/clearTimeout), has proper cleanup, saves to external system.

**Why:** Debounced auto-save batches writes to an external system. The cleanup prevents stale saves.

**Improve it:** Extract into a custom `useAutoSave` hook.

### 2. localStorage/sessionStorage Hydration Calling Parent `onChange`

```tsx
useEffect(() => {
  const saved = localStorage.getItem(KEY)
  if (saved) onChange(JSON.parse(saved))
}, [onChange])
```

**Classification:** **Anti-pattern #7 + #9**

**Fix priority:**
1. **Best:** Lift state to parent — parent reads localStorage directly, passes value down
2. **Good:** `useSyncExternalStore` for reactive localStorage
3. **Acceptable:** Keep Effect but document why (SSR hydration mismatch avoidance)

**Why #1 wins:** Parent owns the state; child shouldn't initialize it via Effect. Violates unidirectional data flow.

### 3. Navigation-Triggered Effects

```tsx
const pathname = usePathname()
useEffect(() => {
  closeMobileNav()
}, [pathname])
```

**Classification:** **Anti-pattern #5**

**Fix:** Attach `onClick` to navigation links that calls `closeMobileNav()` directly.

**Why:** Navigation is a user event. Close the nav *during* the event, not after a re-render.

**Exception:** If your routing library doesn't expose navigation events, the Effect is acceptable but suboptimal.

### 4. DOM-Dependent State Adjustments

**Acceptable if:**
- Reads from DOM (`getBoundingClientRect`, `querySelector`, scroll position)
- State depends on *both* props AND DOM measurements
- Can't be computed from props alone

**Better approach:** Derive from props if possible — `items.find(item => item.id === activeId) ? activeId : items[0]?.id`. Only use Effect if DOM read is genuinely required.

### 5. Data Fetching in Effects

**Anti-pattern #11** (missing cleanup) **unless** it has AbortController cleanup or `let ignore = false` with cleanup return.

**Modern approach:** Use framework data-fetching (Next.js Server Components, Remix loaders, TanStack Query) or extract into a custom hook with proper cleanup.

## Before/After Example

### Before (3 Effects, 2 state variables):

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [displayName, setDisplayName] = useState('')

  // Anti-pattern #1: Deriving state from state
  useEffect(() => {
    if (user) setDisplayName(`${user.firstName} ${user.lastName}`)
  }, [user])

  // Anti-pattern #4: Adjusting state on prop change
  useEffect(() => {
    setUser(null)
    setDisplayName('')
  }, [userId])

  // Legitimate: Data fetching with cleanup
  useEffect(() => {
    let ignore = false
    fetchUser(userId).then(data => {
      if (!ignore) setUser(data)
    })
    return () => { ignore = true }
  }, [userId])

  return <div>{displayName || 'Loading...'}</div>
}
```

### After (1 Effect, 1 state variable, key prop):

```tsx
// Parent:
<UserProfile key={userId} userId={userId} />

// Component:
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  // ✅ Compute during render
  const displayName = user ? `${user.firstName} ${user.lastName}` : 'Loading...'

  // ✅ Data fetching with cleanup (key prop handles reset)
  useEffect(() => {
    let ignore = false
    fetchUser(userId).then(data => {
      if (!ignore) setUser(data)
    })
    return () => { ignore = true }
  }, [userId])

  return <div>{displayName}</div>
}
```

**Result:** 3 Effects → 1. 2 state variables → 1. Render count per `userId` change: 3 → 1.

## Common Mistakes

### Flagging Legitimate Effects as Anti-Patterns

**Mistake:** "This Effect subscribes to scroll events, that's anti-pattern #5."

**Reality:** Scroll listeners ARE external system subscriptions. Anti-pattern #5 is about *application logic* triggered by user events (button clicks, form submits), not browser events you're subscribing to.

**Rule:** `addEventListener` + cleanup `removeEventListener` = legitimate.

### Over-Applying `useSyncExternalStore`

`useSyncExternalStore` is for *reactive* external stores (cross-tab sync, detecting changes). One-time hydration on mount doesn't need it — use a lazy state initializer or a mount Effect.

### Confusing "Could be better" with "Anti-pattern"

- **Anti-pattern** = violates React's guidance, causes extra renders or bugs
- **Improvable** = works correctly but could be simpler/faster

Only flag clear anti-patterns during audits. Note improvements separately.

## Further Reading

If this skill doesn't cover your specific case, read the full React documentation article:

**[You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)**

The article provides additional examples, interactive sandboxes, and deeper explanations of each anti-pattern including edge cases around form submissions, chains of computations, and subscribing to external stores.
