---
name: ahooks
description: |
  Utility hooks for React state management - grouped state and localStorage persistence.
  
  Use when: managing grouped state that changes together, persisting state to localStorage, or coordinating state between URL and storage.
---

# Skill: ahooks

## Scope

- Applies to: ahooks v3+ utility hooks for React state management, grouped state updates, localStorage persistence
- Does NOT cover: Data fetching (use TanStack Query), URL state management (use nuqs), complex state machines, async operations

## Assumptions

- ahooks v3+
- React 18+ with hooks support
- TypeScript v5+ (for type inference)
- Client-side only (hooks require browser APIs for localStorage)

## Principles

- Use `useSetState` for grouped state that changes together (not URL-shareable)
- Use `useLocalStorageState` for persistent state across browser sessions
- Prefer nuqs for URL-shareable state over localStorage
- Prefer TanStack Query for async operations and loading states
- Use `useState` only for simple independent state (rare)

## Constraints

### MUST

- Use `useSetState` for grouped state not in URL (form state, game engine state, ephemeral UI state)
- Use `useLocalStorageState` for localStorage persistence

### SHOULD

- Prefer nuqs for URL-shareable state over localStorage
- Prefer TanStack Query for async operations and loading states
- Use TypeScript generics for type-safe state: `useLocalStorageState<boolean>('key', { defaultValue: false })`

### AVOID

- Using for URL state (use nuqs instead)
- Using for loading/error states (use TanStack Query instead)
- Using for complex async operations (use TanStack Query instead)
- Mixing URL state with localStorage without explicit sync logic

## Interactions

- Complements nuqs for URL state management (can sync bidirectionally)
- Complements TanStack Query for async operations (use TanStack Query for data fetching)
- Part of state management decision tree (see React rules)
- Works with React 18+ hooks architecture

## Patterns

### useSetState Pattern

Use for grouped state that updates together:

```typescript
import { useSetState } from 'ahooks'

const [state, setState] = useSetState({
  name: '',
  email: '',
  age: 0,
})

// Partial updates (shallow merge)
setState({ name: 'John' })
setState(prev => ({ ...prev, email: 'john@example.com' }))
```

**When to use**: Form state, game engine state, UI state that changes together (if not URL-shareable)

**When NOT to use**: URL-shareable state (use nuqs), loading states (use TanStack Query)

### useLocalStorageState Pattern

Use for state that persists across browser sessions:

```typescript
import { useLocalStorageState } from 'ahooks'

const [value, setValue] = useLocalStorageState<boolean>('key', {
  defaultValue: false,
})

// Type-safe with generics
const [settings, setSettings] = useLocalStorageState<Settings>('settings', {
  defaultValue: { theme: 'light', fontSize: 14 },
})
```

**When to use**: User preferences, debug flags, settings that should persist across sessions

**When NOT to use**: URL-shareable state (use nuqs), sensitive data (use secure storage)

### Integration with nuqs

Bidirectional sync between URL and localStorage:

```typescript
import { useLocalStorageState } from 'ahooks'
import { useQueryState } from 'nuqs'
import { useEffect, useRef } from 'react'

const [queryState, setQueryState] = useQueryState('debug')
const [storageState, setStorageState] = useLocalStorageState<boolean>('debug', {
  defaultValue: false,
})
const isFirstMount = useRef(true)

// Sync on mount: localStorage → URL
useEffect(() => {
  if (isFirstMount.current) {
    isFirstMount.current = false
    if (storageState && queryState !== 'true') {
      setQueryState('true')
      return
    }
  }
  // Sync changes: URL → localStorage
  if (queryState === 'true' && !storageState) {
    setStorageState(true)
  } else if (queryState === 'false' && storageState) {
    setStorageState(false)
  }
}, [queryState, storageState, setQueryState, setStorageState])
```

**Use case**: Debug flags, feature toggles that should be both URL-shareable and persistent

### State Management Decision Tree

1. **URL-shareable state** → Use `nuqs` (filters, search, tabs, pagination)
2. **Grouped state not in URL** → Use `useSetState` (form state, game engine, ephemeral UI)
3. **Async operations** → Use TanStack Query (data fetching, mutations, caching)
4. **localStorage persistence** → Use `useLocalStorageState` (preferences, settings)
5. **Simple independent state** → Use `useState` (rare, prefer other options)

## References

- [ahooks documentation](https://ahooks.js.org/) - Official documentation
- React rules - State management decision tree and patterns
- TanStack Query - Async operations and data fetching patterns
