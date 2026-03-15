---
name: state-management
description: Expert guide for React state management with Zustand, Context, and modern patterns. Use when managing global state, forms, complex UI state, or optimizing re-renders.
---

# State Management Skill

## Overview

This skill helps you choose and implement the right state management solution for your React/Next.js application. From local state to global stores, this covers all the patterns you need.

## State Management Hierarchy

### 1. Local State (useState)
Use for component-specific state that doesn't need to be shared.

```typescript
'use client'
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

### 2. URL State (useSearchParams)
Use for state that should be shareable via URL.

```typescript
'use client'
import { useSearchParams, useRouter } from 'next/navigation'

export function SearchFilter() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const category = searchParams.get('category') || 'all'

  const setCategory = (cat: string) => {
    const params = new URLSearchParams(searchParams)
    params.set('category', cat)
    router.push(`?${params.toString()}`)
  }

  return (
    <select value={category} onChange={(e) => setCategory(e.target.value)}>
      <option value="all">All</option>
      <option value="tech">Tech</option>
      <option value="design">Design</option>
    </select>
  )
}
```

### 3. Server State (Server Components)
Use for data from your database/API that doesn't change client-side.

```typescript
// Server Component (no 'use client')
export default async function UserProfile({ userId }: { userId: string }) {
  const user = await db.users.findUnique({ where: { id: userId } })

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

### 4. Context (React Context)
Use for simple global state (theme, user, settings) within a component tree.

```typescript
'use client'
import { createContext, useContext, useState, ReactNode } from 'react'

type Theme = 'light' | 'dark'

const ThemeContext = createContext<{
  theme: Theme
  setTheme: (theme: Theme) => void
}>({ theme: 'light', setTheme: () => {} })

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  return useContext(ThemeContext)
}

// Usage in component
function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Current: {theme}
    </button>
  )
}
```

### 5. Zustand (Global Store)
Use for complex global state that needs to be accessed across many components.

**Basic Store:**
```typescript
// stores/user-store.ts
import { create } from 'zustand'

interface UserState {
  user: User | null
  isLoading: boolean
  setUser: (user: User | null) => void
  fetchUser: (id: string) => Promise<void>
  logout: () => void
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  isLoading: false,

  setUser: (user) => set({ user }),

  fetchUser: async (id) => {
    set({ isLoading: true })
    try {
      const response = await fetch(`/api/users/${id}`)
      const user = await response.json()
      set({ user, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
    }
  },

  logout: () => set({ user: null })
}))

// Usage in component
'use client'
import { useUserStore } from '@/stores/user-store'

export function UserProfile() {
  const { user, isLoading, fetchUser } = useUserStore()

  return (
    <div>
      {isLoading ? <p>Loading...</p> : <p>{user?.name}</p>}
    </div>
  )
}
```

**Persisted Store (localStorage):**
```typescript
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

interface PreferencesState {
  theme: 'light' | 'dark'
  language: string
  setTheme: (theme: 'light' | 'dark') => void
  setLanguage: (lang: string) => void
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set) => ({
      theme: 'light',
      language: 'en',
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language })
    }),
    {
      name: 'preferences-storage',
      storage: createJSONStorage(() => localStorage)
    }
  )
)
```

**Sliced Stores (Organized):**
```typescript
// stores/slices/auth-slice.ts
export const createAuthSlice = (set, get) => ({
  token: null,
  isAuthenticated: false,
  login: async (credentials) => {
    const token = await loginAPI(credentials)
    set({ token, isAuthenticated: true })
  },
  logout: () => set({ token: null, isAuthenticated: false })
})

// stores/slices/cart-slice.ts
export const createCartSlice = (set, get) => ({
  items: [],
  addItem: (item) => set((state) => ({
    items: [...state.items, item]
  })),
  removeItem: (id) => set((state) => ({
    items: state.items.filter(item => item.id !== id)
  })),
  total: () => {
    const items = get().items
    return items.reduce((sum, item) => sum + item.price, 0)
  }
})

// stores/app-store.ts
import { create } from 'zustand'
import { createAuthSlice } from './slices/auth-slice'
import { createCartSlice } from './slices/cart-slice'

export const useAppStore = create((...a) => ({
  ...createAuthSlice(...a),
  ...createCartSlice(...a)
}))
```

**Immer Middleware (Immutable Updates):**
```typescript
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface TodoState {
  todos: Todo[]
  addTodo: (text: string) => void
  toggleTodo: (id: string) => void
  updateTodo: (id: string, text: string) => void
}

export const useTodoStore = create<TodoState>()(
  immer((set) => ({
    todos: [],

    addTodo: (text) =>
      set((state) => {
        state.todos.push({ id: crypto.randomUUID(), text, done: false })
      }),

    toggleTodo: (id) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id)
        if (todo) todo.done = !todo.done
      }),

    updateTodo: (id, text) =>
      set((state) => {
        const todo = state.todos.find((t) => t.id === id)
        if (todo) todo.text = text
      })
  }))
)
```

## Form State Management

### React Hook Form (Recommended)
```typescript
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  age: z.number().min(18)
})

type FormData = z.infer<typeof schema>

export function UserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<FormData>({
    resolver: zodResolver(schema)
  })

  const onSubmit = async (data: FormData) => {
    await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      {errors.name && <p>{errors.name.message}</p>}

      <input {...register('email')} type="email" />
      {errors.email && <p>{errors.email.message}</p>}

      <input {...register('age', { valueAsNumber: true })} type="number" />
      {errors.age && <p>{errors.age.message}</p>}

      <button type="submit" disabled={isSubmitting}>
        Submit
      </button>
    </form>
  )
}
```

## Performance Optimization

### Selective Store Subscription
```typescript
// ❌ Bad - Component re-renders for any store change
function BadExample() {
  const store = useUserStore()
  return <div>{store.user?.name}</div>
}

// ✅ Good - Only re-renders when user.name changes
function GoodExample() {
  const userName = useUserStore((state) => state.user?.name)
  return <div>{userName}</div>
}

// ✅ Better - Use shallow comparison for multiple values
import { shallow } from 'zustand/shallow'

function BetterExample() {
  const { user, isLoading } = useUserStore(
    (state) => ({ user: state.user, isLoading: state.isLoading }),
    shallow
  )
  return <div>{isLoading ? 'Loading...' : user?.name}</div>
}
```

### React.memo for Components
```typescript
import { memo } from 'react'

const ExpensiveComponent = memo(function ExpensiveComponent({
  data
}: {
  data: Data
}) {
  // This only re-renders when data changes
  return <div>{/* Expensive rendering */}</div>
})
```

### useCallback for Functions
```typescript
'use client'
import { useCallback } from 'react'

export function Parent() {
  const [count, setCount] = useState(0)

  // ❌ Bad - New function on every render
  const handleClick = () => {
    console.log('clicked')
  }

  // ✅ Good - Stable function reference
  const handleClickMemoized = useCallback(() => {
    console.log('clicked')
  }, [])

  return <Child onClick={handleClickMemoized} />
}
```

## Advanced Patterns

### Computed Values
```typescript
import { create } from 'zustand'

interface CartState {
  items: CartItem[]
  // Computed value - always fresh
  total: () => number
  subtotal: () => number
  tax: () => number
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],

  total: () => {
    const items = get().items
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  },

  subtotal: () => {
    return get().total()
  },

  tax: () => {
    return get().subtotal() * 0.1
  }
}))

// Usage - recalculates on every call
function Cart() {
  const total = useCartStore((state) => state.total())
  return <div>Total: ${total}</div>
}
```

### Async Actions
```typescript
interface DataState {
  data: Data[]
  isLoading: boolean
  error: string | null
  fetchData: () => Promise<void>
  refetch: () => Promise<void>
}

export const useDataStore = create<DataState>((set, get) => ({
  data: [],
  isLoading: false,
  error: null,

  fetchData: async () => {
    set({ isLoading: true, error: null })
    try {
      const response = await fetch('/api/data')
      const data = await response.json()
      set({ data, isLoading: false })
    } catch (error) {
      set({ error: error.message, isLoading: false })
    }
  },

  refetch: async () => {
    await get().fetchData()
  }
}))
```

### Middleware Composition
```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'
import { devtools } from 'zustand/middleware'

export const useStore = create<State>()(
  devtools(
    persist(
      immer((set) => ({
        // Your store
      })),
      { name: 'my-store' }
    )
  )
)
```

## Decision Tree

```
Do you need state?
  ├─ Only in this component? → useState
  ├─ Pass to 2-3 child components? → props
  ├─ Shareable URL? → useSearchParams
  ├─ From database/API?
  │   ├─ Static/rarely changes? → Server Component
  │   └─ Dynamic/frequent updates? → React Query/SWR
  ├─ Simple global (theme, user)? → Context
  └─ Complex global/many subscribers? → Zustand
```

## Best Practices Checklist

- [ ] Start with local state (useState)
- [ ] Use URL state for shareable filters/tabs
- [ ] Prefer Server Components for DB data
- [ ] Use Context for simple global state
- [ ] Use Zustand for complex global state
- [ ] Select only needed store values
- [ ] Use shallow comparison for multiple values
- [ ] Persist user preferences to localStorage
- [ ] Handle loading and error states
- [ ] Use React Hook Form for complex forms
- [ ] Memoize expensive computations
- [ ] Use TypeScript for type safety

## Common Mistakes to Avoid

1. **Over-using global state** - Start local, move to global when needed
2. **Not selecting store values** - Always use selectors to prevent unnecessary re-renders
3. **Storing derived values** - Compute on-the-fly instead
4. **Not handling loading states** - Always show feedback to users
5. **Putting everything in Zustand** - Use the right tool for the job

## When to Use This Skill

Invoke this skill when:
- Choosing a state management solution
- Setting up Zustand stores
- Optimizing component re-renders
- Managing form state
- Implementing global user settings
- Debugging state-related issues
- Migrating from Redux to Zustand
- Setting up persisted state
