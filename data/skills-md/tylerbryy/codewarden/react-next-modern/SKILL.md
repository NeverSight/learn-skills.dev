---
name: react-next-modern
description: Enforce modern React 19 and Next.js App Router patterns - server-first data fetching, minimal useEffect, Server Components, Server Actions, and form hooks. Use when reviewing React/Next.js code, migrating legacy patterns, or building new features with App Router.
allowed-tools: Read, Grep, Glob, Edit
---

# React and Next.js Modern Best Practices (2025)

## Purpose

This skill enforces the architectural shift from client-side synchronization to **async-native** patterns using React 19 and Next.js App Router. The goal is to eliminate unnecessary `useEffect` usage, move data fetching to the server, and leverage modern primitives like Server Components and Server Actions.

## Core Philosophy: The Paradigm Shift

**Legacy Era (Pre-2024)**: Client components mount, then sync with server via `useEffect`
**Modern Era (2025)**: Server components execute async logic, stream results to client

This shift eliminates:
- Waterfall network requests
- Race conditions in effects
- Layout shifts from loading states
- Manual state management for async operations
- Prop drilling for data

## When to Use This Skill

Activate when:
- Writing new React/Next.js code
- Migrating from Pages Router to App Router
- Refactoring `useEffect`-heavy components
- Implementing forms and mutations
- Reviewing data fetching patterns
- Setting up authentication or authorization
- Optimizing React performance

## How to Use This Skill

When reviewing React/Next.js code:

1. **Identify the stack**
   - Check `package.json` for Next.js version
   - Detect if `app/` directory exists (App Router)
   - Note if React 19 is being used

2. **Scan for code smells**
   - Search for: `useEffect`, `useState`, `useCallback`, `useMemo`
   - Look for: `fetch` in Client Components, API routes used for internal data
   - Find: `getServerSideProps`, `getStaticProps` (legacy patterns)

3. **Apply the checklists below**
   - For each issue, propose a modern alternative
   - Show before/after code examples

4. **Prioritize fixes**
   - First: Correctness and side effect bugs
   - Second: Architecture and data fetching
   - Third: Performance and ergonomics

---

## Checklist 1: useEffect - The "Escape Hatch" Rule

### The Modern Definition

**useEffect is ONLY for synchronizing with external systems outside React's control.**

It is NOT for:
- ❌ Data fetching on component mount
- ❌ Deriving state from props or other state
- ❌ Mirroring props into state
- ❌ Business logic that could be pure functions
- ❌ Generic "on mount" initialization

It IS for:
- ✅ WebSocket subscriptions
- ✅ Browser APIs (localStorage, IntersectionObserver, ResizeObserver)
- ✅ DOM event listeners (window.resize, scroll)
- ✅ Third-party widgets (maps, chat, analytics)
- ✅ Timers tied to React state (setTimeout, setInterval)

### Anti-Pattern #1: Deriving State

**❌ Bad - Effect for derived state:**

```tsx
const [firstName, setFirstName] = useState("John")
const [lastName, setLastName] = useState("Doe")
const [fullName, setFullName] = useState("")

useEffect(() => {
  setFullName(`${firstName} ${lastName}`)
}, [firstName, lastName])
```

**✅ Good - Calculate during render:**

```tsx
const [firstName, setFirstName] = useState("John")
const [lastName, setLastName] = useState("Doe")

const fullName = `${firstName} ${lastName}` // Just compute it!
```

**Why**: Eliminates an entire render cycle and guarantees consistency.

### Anti-Pattern #2: Event Logic in Effects

**❌ Bad - Using effect for user actions:**

```tsx
const [submitted, setSubmitted] = useState(false)

useEffect(() => {
  if (submitted) {
    submitForm(formData)
  }
}, [submitted, formData])

// Later:
<button onClick={() => setSubmitted(true)}>Submit</button>
```

**✅ Good - Direct event handler:**

```tsx
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  await submitForm(formData)
}

// Later:
<form onSubmit={handleSubmit}>
  <button type="submit">Submit</button>
</form>
```

**Why**: User actions should trigger in event handlers, not via state flags.

### Anti-Pattern #3: Data Fetching on Mount

**❌ Bad - Client-side fetch in effect:**

```tsx
"use client"

function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/products')
      .then(res => res.json())
      .then(data => {
        setProducts(data)
        setLoading(false)
      })
  }, [])

  if (loading) return <Spinner />
  return <ProductsList products={products} />
}
```

**✅ Good - Server Component with async/await:**

```tsx
// app/products/page.tsx - Server Component (no "use client")
import { db } from '@/lib/db'

export default async function ProductsPage() {
  // This runs on the server, directly queries DB
  const products = await db.select().from(productsTable)

  return <ProductsList products={products} />
}
```

**Why**:
- Eliminates loading states
- Runs closer to data source (low latency)
- No client bundle size increase
- Content is server-rendered (better SEO)

### Legitimate useEffect Patterns

**✅ Good - External system subscription:**

```tsx
"use client"

function ChatRoom({ roomId }: { roomId: string }) {
  useEffect(() => {
    const connection = createConnection(roomId)
    connection.connect()

    return () => {
      connection.disconnect() // Cleanup
    }
  }, [roomId])

  return <div>Connected to {roomId}</div>
}
```

**✅ Good - Browser API sync:**

```tsx
"use client"

function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(true)

  useEffect(() => {
    const handleOnline = () => setIsOnline(true)
    const handleOffline = () => setIsOnline(false)

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  return isOnline
}
```

### Custom Hooks for Repeated Effects

When the same effect pattern appears multiple times:

**✅ Extract to custom hook:**

```tsx
// hooks/useMediaQuery.ts
"use client"

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const media = window.matchMedia(query)
    setMatches(media.matches)

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches)
    media.addEventListener('change', listener)

    return () => media.removeEventListener('change', listener)
  }, [query])

  return matches
}

// Usage:
const isMobile = useMediaQuery('(max-width: 768px)')
```

---

## Checklist 2: Server Components and Data Fetching

### Server Components by Default

In Next.js App Router (`app/` directory):

**✅ Default: Server Component (no directive)**

```tsx
// app/dashboard/page.tsx
import { db } from '@/lib/db'

export default async function DashboardPage() {
  // Direct database access - runs on server
  const stats = await db.query.stats.findFirst()

  return <div>Revenue: ${stats.revenue}</div>
}
```

**✅ Opt-in: Client Component (with directive)**

```tsx
"use client" // Only add when you need interactivity

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### Rules for Server vs Client Components

| Feature | Server Component | Client Component |
|---------|------------------|------------------|
| **Directive** | None (default) | `"use client"` |
| **Data fetching** | `async/await` DB queries | `use()` or data libraries |
| **Interactivity** | ❌ No event handlers | ✅ onClick, onChange, etc. |
| **React hooks** | ❌ No useState, useEffect | ✅ All hooks available |
| **Bundle size** | ✅ Zero JS shipped | ❌ Increases bundle |
| **Browser APIs** | ❌ No window, localStorage | ✅ Full access |
| **Environment vars** | ✅ Private vars safe | ⚠️ Only NEXT_PUBLIC_* |

### Request Memoization: End of Prop Drilling

**Problem**: Multiple components need the same data. Legacy solution: prop drilling or Context.

**Solution**: Request memoization with `React.cache`.

**✅ Modern pattern - No prop drilling:**

```tsx
// lib/data.ts
import { cache } from 'react'
import { db } from './db'

// Wrap in cache() for automatic request memoization
export const getCurrentUser = cache(async () => {
  return await db.query.users.findFirst({ where: ... })
})
```

```tsx
// app/layout.tsx
import { getCurrentUser } from '@/lib/data'

export default async function RootLayout({ children }) {
  const user = await getCurrentUser() // Call #1

  return (
    <html>
      <Header user={user} />
      {children}
    </html>
  )
}
```

```tsx
// app/profile/page.tsx
import { getCurrentUser } from '@/lib/data'

export default async function ProfilePage() {
  const user = await getCurrentUser() // Call #2 - Same request, cached!

  return <div>Email: {user.email}</div>
}
```

**Why**: Both components call `getCurrentUser()`, but the DB query executes only once per request. No props, no Context, no drilling.

### The use() API: Streaming Promises to Client

**Pattern**: Server Component starts a query, Client Component displays it.

**✅ Server Component (initiates fetch):**

```tsx
// app/search/page.tsx
import { db } from '@/lib/db'
import { SearchResults } from './search-results'

export default async function SearchPage() {
  // Don't await - pass the promise directly
  const resultsPromise = db.query.products.findMany()

  return (
    <Suspense fallback={<ResultsSkeleton />}>
      <SearchResults promise={resultsPromise} />
    </Suspense>
  )
}
```

**✅ Client Component (unwraps promise):**

```tsx
// app/search/search-results.tsx
"use client"

import { use } from 'react'
import type { Product } from '@/lib/db'

export function SearchResults({ promise }: { promise: Promise<Product[]> }) {
  // use() unwraps the promise - suspends until resolved
  const results = use(promise)

  return (
    <ul>
      {results.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  )
}
```

**Why**:
- Initial HTML ships immediately (with fallback)
- Data streams in as server resolves the query
- Improves First Contentful Paint (FCP)

### Client/Server Component Composition

**❌ Bad - Can't import Server Component in Client:**

```tsx
"use client"

import { ServerDetails } from './server-details' // ERROR!

export function ClientCard() {
  return (
    <div onClick={...}>
      <ServerDetails /> {/* This won't work */}
    </div>
  )
}
```

**✅ Good - Pass Server Component as children:**

```tsx
// app/page.tsx (Server Component)
import { ClientCard } from './client-card'
import { ServerDetails } from './server-details'

export default function Page() {
  return (
    <ClientCard>
      <ServerDetails /> {/* Composed in Server Component */}
    </ClientCard>
  )
}
```

```tsx
// client-card.tsx
"use client"

export function ClientCard({ children }: { children: React.ReactNode }) {
  return (
    <div onClick={...}>
      {children} {/* Server Component renders here */}
    </div>
  )
}
```

---

## Checklist 3: Server Actions and Mutations

### Server Actions vs Route Handlers

| Use Case | Tool | Why |
|----------|------|-----|
| **Form submission** | Server Action | Integrated with React, auto cache revalidation |
| **UI mutation (like, delete)** | Server Action | Type-safe, works without JS (progressive) |
| **Public API endpoint** | Route Handler | Mobile app, webhooks, third-party access |
| **Webhook receiver** | Route Handler | External system, not tied to UI |

### The React 19 Form Hooks Trinity

#### 1. useActionState - Form State Management

Replaces manual `useState` for form errors and submission.

**✅ Server Action:**

```tsx
// actions/auth.ts
"use server"

import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
})

export async function loginAction(prevState: any, formData: FormData) {
  // Validate input
  const parsed = loginSchema.safeParse({
    email: formData.get('email'),
    password: formData.get('password')
  })

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors }
  }

  // Perform login
  const result = await login(parsed.data)

  if (!result.success) {
    return { errors: { _form: ['Invalid credentials'] } }
  }

  redirect('/dashboard')
}
```

**✅ Client Component (form):**

```tsx
"use client"

import { useActionState } from 'react'
import { loginAction } from '@/actions/auth'

export function LoginForm() {
  const [state, formAction, isPending] = useActionState(loginAction, null)

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      {state?.errors?.email && <span>{state.errors.email}</span>}

      <input name="password" type="password" />
      {state?.errors?.password && <span>{state.errors.password}</span>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Logging in...' : 'Log in'}
      </button>

      {state?.errors?._form && <span>{state.errors._form}</span>}
    </form>
  )
}
```

**Key Points**:
- Server Action signature: `(prevState, formData) => newState`
- `isPending` tracks submission automatically
- Form works without JavaScript (progressive enhancement)

#### 2. useFormStatus - Child Component UI

Allows any child of a `<form>` to access the form's pending state.

**✅ Extract submit button:**

```tsx
"use client"

import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  )
}
```

**✅ Use in form:**

```tsx
<form action={formAction}>
  <input name="title" />
  <SubmitButton /> {/* Automatically knows form state */}
</form>
```

**Constraint**: Must be used in a *child* component, not the same component that renders `<form>`.

#### 3. useOptimistic - Instant UI Updates

Updates UI immediately while Server Action processes.

**✅ Optimistic like button:**

```tsx
"use client"

import { useOptimistic } from 'react'
import { likePost } from '@/actions/posts'

export function LikeButton({ postId, initialLikes }: Props) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    initialLikes,
    (state, amount: number) => state + amount
  )

  return (
    <form
      action={async () => {
        // Update UI instantly
        addOptimisticLike(1)

        // Server Action runs in background
        await likePost(postId)
      }}
    >
      <button type="submit">❤️ {optimisticLikes}</button>
    </form>
  )
}
```

**Behavior**:
- UI updates immediately when button clicked
- Server Action processes in background
- If success: parent re-renders with real data, optimistic state discarded
- If failure: optimistic update automatically rolls back

---

## Checklist 4: Security Standards for Server Actions

### Rule 1: Always Validate Input

**❌ Bad - Trusting FormData:**

```tsx
"use server"

export async function updateUser(formData: FormData) {
  const email = formData.get('email') // Could be anything!
  await db.update(users).set({ email })
}
```

**✅ Good - Zod validation:**

```tsx
"use server"

import { z } from 'zod'

const updateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100)
})

export async function updateUser(formData: FormData) {
  const parsed = updateUserSchema.safeParse({
    email: formData.get('email'),
    name: formData.get('name')
  })

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors }
  }

  await db.update(users).set(parsed.data)
  return { success: true }
}
```

### Rule 2: Always Authenticate

**❌ Bad - No auth check:**

```tsx
"use server"

export async function deletePost(postId: string) {
  await db.delete(posts).where(eq(posts.id, postId))
}
```

**✅ Good - Auth check first:**

```tsx
"use server"

import { auth } from '@/lib/auth'

export async function deletePost(postId: string) {
  const session = await auth()

  if (!session?.user) {
    throw new Error('Unauthorized')
  }

  // Verify ownership
  const post = await db.query.posts.findFirst({
    where: eq(posts.id, postId)
  })

  if (post.authorId !== session.user.id) {
    throw new Error('Forbidden')
  }

  await db.delete(posts).where(eq(posts.id, postId))
  revalidatePath('/posts')
}
```

### Rule 3: Module-Level Actions (Not Inline)

**❌ Bad - Inline action with closure:**

```tsx
export default async function Page() {
  const secretKey = process.env.SECRET_KEY // Sensitive!

  async function dangerousAction() {
    "use server"
    // This closure is encrypted but sent to client
    console.log(secretKey) // Risky!
  }

  return <form action={dangerousAction}>...</form>
}
```

**✅ Good - Module-level action:**

```tsx
// actions/posts.ts
"use server"

export async function createPost(formData: FormData) {
  const secretKey = process.env.SECRET_KEY // Stays on server
  // Safe - no closure, explicit arguments only
}
```

```tsx
// app/page.tsx
import { createPost } from '@/actions/posts'

export default function Page() {
  return <form action={createPost}>...</form>
}
```

### Rule 4: Rate Limiting

Add rate limiting to prevent abuse:

```tsx
"use server"

import { ratelimit } from '@/lib/rate-limit'

export async function sendEmail(formData: FormData) {
  const session = await auth()
  if (!session?.user) throw new Error('Unauthorized')

  const { success } = await ratelimit.limit(session.user.id)
  if (!success) {
    return { error: 'Too many requests. Try again later.' }
  }

  // Proceed with action...
}
```

---

## Checklist 5: Performance Optimization

### Eliminate Client-Side Waterfalls

**❌ Bad - Sequential client fetches:**

```tsx
"use client"

function Dashboard() {
  const [user, setUser] = useState(null)
  const [posts, setPosts] = useState([])

  useEffect(() => {
    fetch('/api/user').then(r => r.json()).then(setUser)
  }, [])

  useEffect(() => {
    if (user) {
      // Waits for user fetch!
      fetch(`/api/posts?userId=${user.id}`).then(r => r.json()).then(setPosts)
    }
  }, [user])

  return <div>...</div>
}
```

**✅ Good - Parallel server fetches:**

```tsx
// app/dashboard/page.tsx
import { db } from '@/lib/db'

export default async function Dashboard() {
  // Both queries run in parallel on server
  const [user, posts] = await Promise.all([
    db.query.users.findFirst(),
    db.query.posts.findMany()
  ])

  return <DashboardUI user={user} posts={posts} />
}
```

### Bundle Size Optimization

**✅ Lazy load heavy Client Components:**

```tsx
import dynamic from 'next/dynamic'

const RichTextEditor = dynamic(() => import('@/components/editor'), {
  loading: () => <p>Loading editor...</p>,
  ssr: false // Don't render on server
})

export default function Page() {
  return <RichTextEditor />
}
```

**✅ Keep heavy libraries in Server Components:**

```tsx
// Server Component - markdown lib stays on server
import { marked } from 'marked'

export default async function BlogPost({ slug }: Props) {
  const post = await getPost(slug)
  const html = marked(post.content) // Runs on server

  return <div dangerouslySetInnerHTML={{ __html: html }} />
}
```

### React Compiler (React 19)

With the React Compiler enabled:

- ✅ Automatically memoizes components and values
- ✅ Eliminates most `useMemo` and `useCallback`
- ✅ Focuses on business logic, not performance plumbing

**Before (manual memoization):**

```tsx
const sortedUsers = useMemo(() => {
  return users.sort((a, b) => a.name.localeCompare(b.name))
}, [users])

const handleClick = useCallback(() => {
  console.log('clicked')
}, [])
```

**After (React Compiler handles it):**

```tsx
// Just write normal code - compiler optimizes
const sortedUsers = users.sort((a, b) => a.name.localeCompare(b.name))

const handleClick = () => {
  console.log('clicked')
}
```

---

## Checklist 6: Migration from Legacy Patterns

### Class Components → Function Components

**❌ Legacy class:**

```tsx
class UserProfile extends React.Component {
  state = { user: null }

  componentDidMount() {
    fetchUser().then(user => this.setState({ user }))
  }

  render() {
    return <div>{this.state.user?.name}</div>
  }
}
```

**✅ Modern function component:**

```tsx
// Server Component - no hooks needed!
export default async function UserProfile() {
  const user = await fetchUser()
  return <div>{user.name}</div>
}
```

### getServerSideProps → Server Component

**❌ Legacy Pages Router:**

```tsx
// pages/products.tsx
export async function getServerSideProps() {
  const products = await db.query.products.findMany()
  return { props: { products } }
}

export default function ProductsPage({ products }) {
  return <ProductsList products={products} />
}
```

**✅ Modern App Router:**

```tsx
// app/products/page.tsx
export default async function ProductsPage() {
  const products = await db.query.products.findMany()
  return <ProductsList products={products} />
}
```

**Benefits**: Simpler, fewer concepts, more composable.

### API Routes → Server Actions

**❌ Legacy API route:**

```tsx
// pages/api/users.ts
export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { name, email } = req.body
    const user = await createUser({ name, email })
    res.json({ user })
  }
}
```

**✅ Modern Server Action:**

```tsx
// actions/users.ts
"use server"

export async function createUserAction(formData: FormData) {
  const user = await createUser({
    name: formData.get('name'),
    email: formData.get('email')
  })

  revalidatePath('/users')
  return { success: true, user }
}
```

---

## Quick Reference: Decision Matrix

### When to use each pattern:

| Scenario | Solution | Key Tool |
|----------|----------|----------|
| **Initial page data** | Server Component async/await | `await db.query` |
| **Interactive list/form** | Client Component + Server Action | `useActionState` |
| **Real-time polling** | Client Component + TanStack Query | `useQuery({ refetchInterval })` |
| **Optimistic update** | Client Component | `useOptimistic` |
| **WebSocket/external sub** | Client Component | `useEffect` + cleanup |
| **Browser API sync** | Custom hook | `useSyncExternalStore` |
| **Public API endpoint** | Route Handler | `app/api/route.ts` |
| **Form with validation** | Server Action + Zod | `useActionState` |
| **Derived value** | Render calculation | `const x = a + b` |
| **User event logic** | Event handler | `onClick`, `onSubmit` |

---

## Response Format for Code Reviews

When using this skill for code review:

### 1. Summary
High-level assessment of how modern the codebase is and where the biggest wins are.

### 2. Structured Review

**A. useEffect and Side Effects**
- Issues found: List any unnecessary effects
- Suggested refactors: Show concrete alternatives
- Code examples: Before/after for at least one

**B. Data Fetching and Server Usage**
- Issues found: Client-side fetching, API routes for internal data
- Suggested refactors: Move to Server Components
- Code examples: Server Component implementation

**C. Hooks and State Management**
- Issues found: Unnecessary useState, missing memoization
- Suggested refactors: Derive state, use form hooks
- Code examples: useActionState implementation

**D. Component Structure**
- Issues found: Large components, improper Client/Server boundaries
- Suggested refactors: Split components, composition patterns
- Code examples: Proper component architecture

### 3. Next Steps
Prioritized list of actionable items:
- "Refactor user profile page data fetching to Server Component"
- "Replace useEffect-based form handling with useActionState"
- "Extract useMediaQuery custom hook for responsive logic"
- "Add Zod validation to all Server Actions"

---

## Common Mistakes to Avoid

### 1. "use client" at Top Level

**❌ Bad:**
```tsx
"use client" // Entire tree is client-side!

export default function Layout({ children }) {
  return <div>{children}</div>
}
```

**✅ Good:**
```tsx
// Layout is server component
export default function Layout({ children }) {
  return (
    <div>
      <InteractiveHeader /> {/* Only this is "use client" */}
      {children}
    </div>
  )
}
```

### 2. Mixing Server and Client Imports

**❌ Bad:**
```tsx
"use client"

import { db } from '@/lib/db' // ERROR: Can't import server code

export function ClientComponent() {
  // db is not available in browser!
}
```

**✅ Good:**
```tsx
// Pass data from Server Component as props
export function ClientComponent({ data }: { data: Data }) {
  // Use the data here
}
```

### 3. Not Handling Errors

**❌ Bad:**
```tsx
"use server"

export async function deleteUser(userId: string) {
  await db.delete(users).where(eq(users.id, userId))
  // No error handling!
}
```

**✅ Good:**
```tsx
"use server"

export async function deleteUser(userId: string) {
  try {
    const session = await auth()
    if (!session?.user) {
      return { error: 'Unauthorized' }
    }

    await db.delete(users).where(eq(users.id, userId))
    revalidatePath('/users')

    return { success: true }
  } catch (error) {
    console.error('Delete user failed:', error)
    return { error: 'Failed to delete user' }
  }
}
```

---

## Additional Resources

- [React 19 Docs - You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [React Server Components RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md)
- [Server Actions and Mutations](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)

---

## Examples

### Example 1: Complete Form with Server Action

**Server Action:**

```tsx
// actions/create-post.ts
"use server"

import { z } from 'zod'
import { auth } from '@/lib/auth'
import { db } from '@/lib/db'
import { revalidatePath } from 'next/cache'

const createPostSchema = z.object({
  title: z.string().min(3).max(100),
  content: z.string().min(10)
})

export async function createPostAction(prevState: any, formData: FormData) {
  const session = await auth()
  if (!session?.user) {
    return { errors: { _form: ['You must be logged in'] } }
  }

  const parsed = createPostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content')
  })

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors }
  }

  try {
    await db.insert(posts).values({
      ...parsed.data,
      authorId: session.user.id
    })

    revalidatePath('/posts')
    return { success: true }
  } catch (error) {
    return { errors: { _form: ['Failed to create post'] } }
  }
}
```

**Form Component:**

```tsx
// components/create-post-form.tsx
"use client"

import { useActionState } from 'react'
import { useFormStatus } from 'react-dom'
import { createPostAction } from '@/actions/create-post'

function SubmitButton() {
  const { pending } = useFormStatus()
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Post'}
    </button>
  )
}

export function CreatePostForm() {
  const [state, formAction] = useActionState(createPostAction, null)

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <label htmlFor="title">Title</label>
        <input id="title" name="title" type="text" required />
        {state?.errors?.title && (
          <p className="error">{state.errors.title}</p>
        )}
      </div>

      <div>
        <label htmlFor="content">Content</label>
        <textarea id="content" name="content" required />
        {state?.errors?.content && (
          <p className="error">{state.errors.content}</p>
        )}
      </div>

      {state?.errors?._form && (
        <p className="error">{state.errors._form}</p>
      )}

      {state?.success && <p className="success">Post created!</p>}

      <SubmitButton />
    </form>
  )
}
```

### Example 2: Optimistic Updates

```tsx
// components/like-button.tsx
"use client"

import { useOptimistic } from 'react'
import { likePost } from '@/actions/posts'

interface Props {
  postId: string
  initialLikes: number
  userHasLiked: boolean
}

export function LikeButton({ postId, initialLikes, userHasLiked }: Props) {
  const [optimisticLikes, addOptimistic] = useOptimistic(
    { likes: initialLikes, liked: userHasLiked },
    (state, newLiked: boolean) => ({
      likes: state.likes + (newLiked ? 1 : -1),
      liked: newLiked
    })
  )

  return (
    <form
      action={async () => {
        const newLiked = !optimisticLikes.liked
        addOptimistic(newLiked)
        await likePost(postId, newLiked)
      }}
    >
      <button type="submit">
        {optimisticLikes.liked ? '❤️' : '🤍'} {optimisticLikes.likes}
      </button>
    </form>
  )
}
```

---

## Summary: The 2025 React Mental Model

**Data flows from Server → Client**
- Server Components fetch and render
- Client Components add interactivity
- Never fetch in effects

**Mutations flow from Client → Server → Client**
- User triggers action in Client Component
- Server Action processes on server
- Results stream back to Client Component

**Effects are for external systems only**
- WebSockets, timers, browser APIs
- Not for data, not for business logic
- Use custom hooks for repeated patterns

**Forms are declarative**
- `<form action={serverAction}>` - no event handlers
- `useActionState` for state/errors
- `useFormStatus` for pending UI
- `useOptimistic` for instant feedback

This is the modern React architecture: **Async-Native, Server-First, Effect-Minimal.**
