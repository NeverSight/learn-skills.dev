---
name: react
description: This skill should be used when working with React 19, including hooks, components, server components, concurrent features, and React DOM APIs. Provides comprehensive knowledge of React patterns, best practices, and modern React architecture.
---

# React 19 Skill

This skill provides comprehensive knowledge and patterns for working with React 19 effectively in modern applications.

## When to Use This Skill

Use this skill when:
- Building React applications with React 19 features
- Working with React hooks and component patterns
- Implementing server components and server functions
- Using concurrent features and transitions
- Optimizing React application performance
- Troubleshooting React-specific issues
- Working with React DOM APIs and client/server rendering
- Using React Compiler features

## Core Concepts

### React 19 Overview

React 19 introduces significant improvements:
- **Server Components** - Components that render on the server
- **Server Functions** - Functions that run on the server from client code
- **Concurrent Features** - Better performance with concurrent rendering
- **React Compiler** - Automatic memoization and optimization
- **Form Actions** - Built-in form handling with useActionState
- **Improved Hooks** - New hooks like useOptimistic, useActionState
- **Better Hydration** - Improved SSR and hydration performance

### Component Fundamentals

Use functional components with hooks:

```typescript
// Functional component with props interface
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary'
}

const Button = ({ label, onClick, variant = 'primary' }: ButtonProps) => {
  return (
    <button
      onClick={onClick}
      className={`btn btn-${variant}`}
    >
      {label}
    </button>
  )
}
```

**Key Principles:**
- Use functional components over class components
- Define prop interfaces in TypeScript
- Use destructuring for props
- Provide default values for optional props
- Keep components focused and composable

## React Hooks Reference

### State Hooks

#### useState
Manage local component state:

```typescript
const [count, setCount] = useState<number>(0)
const [user, setUser] = useState<User | null>(null)

// Named return variables pattern
const handleIncrement = () => {
  setCount(prev => prev + 1)  // Functional update
}

// Update object state immutably
setUser(prev => prev ? { ...prev, name: 'New Name' } : null)
```

#### useReducer
Manage complex state with reducer pattern:

```typescript
type State = { count: number; status: 'idle' | 'loading' }
type Action = 
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'setStatus'; status: State['status'] }

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + 1 }
    case 'decrement':
      return { ...state, count: state.count - 1 }
    case 'setStatus':
      return { ...state, status: action.status }
    default:
      return state
  }
}

const [state, dispatch] = useReducer(reducer, { count: 0, status: 'idle' })
```

#### useActionState
Handle form actions with pending states (React 19):

```typescript
const [state, formAction, isPending] = useActionState(
  async (previousState: FormState, formData: FormData) => {
    const name = formData.get('name') as string
    
    // Server action or async operation
    const result = await saveUser({ name })
    
    return { success: true, data: result }
  },
  { success: false, data: null }
)

return (
  <form action={formAction}>
    <input name="name" />
    <button disabled={isPending}>
      {isPending ? 'Saving...' : 'Save'}
    </button>
  </form>
)
```

### Effect Hooks

#### useEffect
Run side effects after render:

```typescript
// Named return variables preferred
useEffect(() => {
  const controller = new AbortController()
  
  const fetchData = async () => {
    const response = await fetch('/api/data', {
      signal: controller.signal
    })
    const data = await response.json()
    setData(data)
  }
  
  fetchData()
  
  // Cleanup function
  return () => {
    controller.abort()
  }
}, [dependencies])  // Dependencies array
```

**Key Points:**
- Always return cleanup function for subscriptions
- Use dependency array correctly to avoid infinite loops
- Don't forget to handle race conditions with AbortController
- Effects run after paint, not during render

#### useLayoutEffect
Run effects synchronously after DOM mutations but before paint:

```typescript
useLayoutEffect(() => {
  // Measure DOM nodes
  const height = ref.current?.getBoundingClientRect().height
  setHeight(height)
}, [])
```

Use when you need to:
- Measure DOM layout
- Synchronously re-render before browser paints
- Prevent visual flicker

#### useInsertionEffect
Insert styles before any DOM reads (for CSS-in-JS libraries):

```typescript
useInsertionEffect(() => {
  const style = document.createElement('style')
  style.textContent = '.my-class { color: red; }'
  document.head.appendChild(style)
  
  return () => {
    document.head.removeChild(style)
  }
}, [])
```

### Performance Hooks

#### useMemo
Memoize expensive calculations:

```typescript
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b)
}, [a, b])
```

**When to use:**
- Expensive calculations that would slow down renders
- Creating stable object references for dependency arrays
- Optimizing child component re-renders

**When NOT to use:**
- Simple calculations (overhead not worth it)
- Values that change frequently

#### useCallback
Memoize callback functions:

```typescript
const handleClick = useCallback(() => {
  console.log('Clicked', value)
}, [value])

// Pass to child that uses memo
<ChildComponent onClick={handleClick} />
```

**Use when:**
- Passing callbacks to optimized child components
- Function is a dependency in another hook
- Function is used in effect cleanup

### Ref Hooks

#### useRef
Store mutable values that don't trigger re-renders:

```typescript
// DOM reference
const inputRef = useRef<HTMLInputElement>(null)

useEffect(() => {
  inputRef.current?.focus()
}, [])

// Mutable value storage
const countRef = useRef<number>(0)
countRef.current += 1  // Doesn't trigger re-render
```

#### useImperativeHandle
Customize ref handle for parent components:

```typescript
interface InputHandle {
  focus: () => void
  clear: () => void
}

const CustomInput = forwardRef<InputHandle, InputProps>((props, ref) => {
  const inputRef = useRef<HTMLInputElement>(null)
  
  useImperativeHandle(ref, () => ({
    focus: () => {
      inputRef.current?.focus()
    },
    clear: () => {
      if (inputRef.current) {
        inputRef.current.value = ''
      }
    }
  }))
  
  return <input ref={inputRef} {...props} />
})
```

### Context Hooks

#### useContext
Access context values:

```typescript
// Create context
interface ThemeContext {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContext | null>(null)

// Provider
const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  
  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }, [])
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// Consumer
const ThemedButton = () => {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  
  const { theme, toggleTheme } = context
  
  return (
    <button onClick={toggleTheme}>
      Current theme: {theme}
    </button>
  )
}
```

### Transition Hooks

#### useTransition
Mark state updates as non-urgent:

```typescript
const [isPending, startTransition] = useTransition()

const handleTabChange = (newTab: string) => {
  startTransition(() => {
    setTab(newTab)  // Non-urgent update
  })
}

return (
  <>
    <button onClick={() => handleTabChange('profile')}>
      Profile
    </button>
    {isPending && <Spinner />}
    <TabContent tab={tab} />
  </>
)
```

**Use for:**
- Marking expensive updates as non-urgent
- Keeping UI responsive during state transitions
- Preventing loading states for quick updates

#### useDeferredValue
Defer re-rendering for non-urgent updates:

```typescript
const [query, setQuery] = useState('')
const deferredQuery = useDeferredValue(query)

// Use deferred value for expensive rendering
const results = useMemo(() => {
  return searchResults(deferredQuery)
}, [deferredQuery])

return (
  <>
    <input value={query} onChange={e => setQuery(e.target.value)} />
    <Results data={results} />
  </>
)
```

### Optimistic Updates

#### useOptimistic
Show optimistic state while async operation completes (React 19):

```typescript
const [optimisticMessages, addOptimisticMessage] = useOptimistic(
  messages,
  (state, newMessage: string) => [
    ...state,
    { id: 'temp', text: newMessage, pending: true }
  ]
)

const handleSend = async (formData: FormData) => {
  const message = formData.get('message') as string
  
  // Show optimistic update immediately
  addOptimisticMessage(message)
  
  // Send to server
  await sendMessage(message)
}

return (
  <>
    {optimisticMessages.map(msg => (
      <div key={msg.id} className={msg.pending ? 'opacity-50' : ''}>
        {msg.text}
      </div>
    ))}
    <form action={handleSend}>
      <input name="message" />
      <button>Send</button>
    </form>
  </>
)
```

### Other Hooks

#### useId
Generate unique IDs for accessibility:

```typescript
const id = useId()

return (
  <>
    <label htmlFor={id}>Name:</label>
    <input id={id} type="text" />
  </>
)
```

#### useSyncExternalStore
Subscribe to external stores:

```typescript
const subscribe = (callback: () => void) => {
  store.subscribe(callback)
  return () => store.unsubscribe(callback)
}

const getSnapshot = () => store.getState()
const getServerSnapshot = () => store.getInitialState()

const state = useSyncExternalStore(
  subscribe,
  getSnapshot,
  getServerSnapshot
)
```

#### useDebugValue
Display custom label in React DevTools:

```typescript
const useCustomHook = (value: string) => {
  useDebugValue(value ? `Active: ${value}` : 'Inactive')
  return value
}
```

## React Components

### Fragment
Group elements without extra DOM nodes:

```typescript
// Short syntax
<>
  <ChildA />
  <ChildB />
</>

// Full syntax (when you need key prop)
<Fragment key={item.id}>
  <dt>{item.term}</dt>
  <dd>{item.description}</dd>
</Fragment>
```

### Suspense
Show fallback while loading:

```typescript
<Suspense fallback={<Loading />}>
  <AsyncComponent />
</Suspense>

// With error boundary
<ErrorBoundary fallback={<Error />}>
  <Suspense fallback={<Loading />}>
    <AsyncComponent />
  </Suspense>
</ErrorBoundary>
```

### StrictMode
Enable additional checks in development:

```typescript
<StrictMode>
  <App />
</StrictMode>
```

**StrictMode checks:**
- Warns about deprecated APIs
- Detects unexpected side effects
- Highlights potential problems
- Double-invokes functions to catch bugs

### Profiler
Measure rendering performance:

```typescript
<Profiler id="App" onRender={onRender}>
  <App />
</Profiler>

const onRender = (
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) => {
  console.log(`${id} took ${actualDuration}ms`)
}
```

## React APIs

### memo
Prevent unnecessary re-renders:

```typescript
const ExpensiveComponent = memo(({ data }: Props) => {
  return <div>{data}</div>
}, (prevProps, nextProps) => {
  // Return true if props are equal (skip render)
  return prevProps.data === nextProps.data
})
```

### lazy
Code-split components:

```typescript
const Dashboard = lazy(() => import('./Dashboard'))

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

### startTransition
Mark updates as transitions imperatively:

```typescript
startTransition(() => {
  setTab('profile')
})
```

### cache (React Server Components)
Cache function results per request:

```typescript
const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } })
})
```

### use (React 19)
Read context or promises in render:

```typescript
// Read context
const theme = use(ThemeContext)

// Read promise (must be wrapped in Suspense)
const data = use(fetchDataPromise)
```

## Server Components & Server Functions

### Server Components

Components that run only on the server:

```typescript
// app/page.tsx (Server Component by default)
const Page = async () => {
  // Can fetch data directly
  const posts = await db.post.findMany()
  
  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  )
}

export default Page
```

**Benefits:**
- Direct database access
- Zero bundle size for server-only code
- Automatic code splitting
- Better performance

### Server Functions

Functions that run on server, callable from client:

```typescript
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string
  
  const post = await db.post.create({
    data: { title, content }
  })
  
  revalidatePath('/posts')
  return post
}
```

**Usage from client:**

```typescript
'use client'

import { createPost } from './actions'

const PostForm = () => {
  const [state, formAction] = useActionState(createPost, null)
  
  return (
    <form action={formAction}>
      <input name="title" />
      <textarea name="content" />
      <button>Create</button>
    </form>
  )
}
```

### Directives

#### 'use client'
Mark file as client component:

```typescript
'use client'

import { useState } from 'react'

// This component runs on client
export const Counter = () => {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

#### 'use server'
Mark functions as server functions:

```typescript
'use server'

export async function updateUser(userId: string, data: UserData) {
  return await db.user.update({ where: { id: userId }, data })
}
```

## React DOM

### Client APIs

#### createRoot
Create root for client rendering (React 19):

```typescript
import { createRoot } from 'react-dom/client'

const root = createRoot(document.getElementById('root')!)
root.render(<App />)

// Update root
root.render(<App newProp="value" />)

// Unmount
root.unmount()
```

#### hydrateRoot
Hydrate server-rendered HTML:

```typescript
import { hydrateRoot } from 'react-dom/client'

hydrateRoot(document.getElementById('root')!, <App />)
```

### Component APIs

#### createPortal
Render children outside parent DOM hierarchy:

```typescript
import { createPortal } from 'react-dom'

const Modal = ({ children }: { children: React.ReactNode }) => {
  return createPortal(
    <div className="modal">{children}</div>,
    document.body
  )
}
```

#### flushSync
Force synchronous update:

```typescript
import { flushSync } from 'react-dom'

flushSync(() => {
  setCount(1)
})
// DOM is updated synchronously
```

### Form Components

#### <form> with actions

```typescript
const handleSubmit = async (formData: FormData) => {
  'use server'
  const email = formData.get('email')
  await saveEmail(email)
}

<form action={handleSubmit}>
  <input name="email" type="email" />
  <button>Subscribe</button>
</form>
```

#### useFormStatus

```typescript
import { useFormStatus } from 'react-dom'

const SubmitButton = () => {
  const { pending } = useFormStatus()
  
  return (
    <button disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  )
}
```

## React Compiler

### Configuration

Configure React Compiler in babel or bundler config:

```javascript
// babel.config.js
module.exports = {
  plugins: [
    ['react-compiler', {
      compilationMode: 'annotation',  // or 'all'
      panicThreshold: 'all_errors',
    }]
  ]
}
```

### Directives

#### "use memo"
Force memoization of component:

```typescript
'use memo'

const ExpensiveComponent = ({ data }: Props) => {
  const processed = expensiveComputation(data)
  return <div>{processed}</div>
}
```

#### "use no memo"
Prevent automatic memoization:

```typescript
'use no memo'

const SimpleComponent = ({ text }: Props) => {
  return <div>{text}</div>
}
```

## Best Practices

### Component Design

1. **Keep components focused** - Single responsibility principle
2. **Prefer composition** - Build complex UIs from simple components
3. **Extract custom hooks** - Reusable logic in hooks
4. **Named return variables** - Use named returns in functions
5. **Type everything** - Proper TypeScript interfaces for all props

### Performance

1. **Use React.memo sparingly** - Only for expensive components
2. **Optimize context** - Split contexts to avoid unnecessary re-renders
3. **Lazy load routes** - Code-split at route boundaries
4. **Use transitions** - Mark non-urgent updates with useTransition
5. **Virtualize lists** - Use libraries like react-window for long lists

### State Management

1. **Local state first** - useState for component-specific state
2. **Lift state up** - Only when multiple components need it
3. **Use reducers for complex state** - useReducer for complex logic
4. **Context for global state** - Theme, auth, etc.
5. **External stores** - TanStack Query, Zustand for complex apps

### Error Handling

1. **Error boundaries** - Catch rendering errors
2. **Guard clauses** - Early returns for invalid states
3. **Null checks** - Always check for null/undefined
4. **Try-catch in effects** - Handle async errors
5. **User-friendly errors** - Show helpful error messages

### Testing Considerations

1. **Testable components** - Pure, predictable components
2. **Test user behavior** - Not implementation details
3. **Mock external dependencies** - APIs, context, etc.
4. **Test error states** - Verify error handling works
5. **Accessibility tests** - Test keyboard navigation, screen readers

## Common Patterns

### Compound Components

```typescript
interface TabsProps {
  children: React.ReactNode
  defaultValue: string
}

const TabsContext = createContext<{
  value: string
  setValue: (v: string) => void
} | null>(null)

const Tabs = ({ children, defaultValue }: TabsProps) => {
  const [value, setValue] = useState(defaultValue)
  
  return (
    <TabsContext.Provider value={{ value, setValue }}>
      {children}
    </TabsContext.Provider>
  )
}

const TabsList = ({ children }: { children: React.ReactNode }) => (
  <div role="tablist">{children}</div>
)

const TabsTrigger = ({ value, children }: { value: string, children: React.ReactNode }) => {
  const context = useContext(TabsContext)
  if (!context) throw new Error('TabsTrigger must be used within Tabs')
  
  return (
    <button
      role="tab"
      aria-selected={context.value === value}
      onClick={() => context.setValue(value)}
    >
      {children}
    </button>
  )
}

const TabsContent = ({ value, children }: { value: string, children: React.ReactNode }) => {
  const context = useContext(TabsContext)
  if (!context) throw new Error('TabsContent must be used within Tabs')
  
  if (context.value !== value) return null
  
  return <div role="tabpanel">{children}</div>
}

// Usage
<Tabs defaultValue="profile">
  <TabsList>
    <TabsTrigger value="profile">Profile</TabsTrigger>
    <TabsTrigger value="settings">Settings</TabsTrigger>
  </TabsList>
  <TabsContent value="profile">Profile content</TabsContent>
  <TabsContent value="settings">Settings content</TabsContent>
</Tabs>
```

### Render Props

```typescript
interface DataFetcherProps<T> {
  url: string
  children: (data: T | null, loading: boolean, error: Error | null) => React.ReactNode
}

const DataFetcher = <T,>({ url, children }: DataFetcherProps<T>) => {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  
  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [url])
  
  return <>{children(data, loading, error)}</>
}

// Usage
<DataFetcher<User> url="/api/user">
  {(user, loading, error) => {
    if (loading) return <Spinner />
    if (error) return <Error error={error} />
    if (!user) return null
    return <UserProfile user={user} />
  }}
</DataFetcher>
```

### Custom Hooks Pattern

```typescript
const useLocalStorage = <T,>(key: string, initialValue: T) => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(error)
      return initialValue
    }
  })
  
  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }, [key, storedValue])
  
  return [storedValue, setValue] as const
}
```

## Troubleshooting

### Common Issues

#### Infinite Loops
- Check useEffect dependencies
- Ensure state updates don't trigger themselves
- Use functional setState updates

#### Stale Closures
- Add all used variables to dependency arrays
- Use useCallback for functions in dependencies
- Consider using refs for values that shouldn't trigger re-renders

#### Performance Issues
- Use React DevTools Profiler
- Check for unnecessary re-renders
- Optimize with memo, useMemo, useCallback
- Consider code splitting

#### Hydration Mismatches
- Ensure server and client render same HTML
- Avoid using Date.now() or random values during render
- Use useEffect for browser-only code
- Check for conditional rendering based on browser APIs

## References

- **React Documentation**: https://react.dev
- **React API Reference**: https://react.dev/reference/react
- **React DOM Reference**: https://react.dev/reference/react-dom
- **React Compiler**: https://react.dev/reference/react-compiler
- **Rules of React**: https://react.dev/reference/rules
- **GitHub**: https://github.com/facebook/react

## Related Skills

- **typescript** - TypeScript patterns and types for React
- **ndk** - Nostr integration with React hooks
- **skill-creator** - Creating reusable component libraries

