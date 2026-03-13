---
name: react-typescript
description: Build React 19 applications with TypeScript. Covers Actions, Activity, use() hook, React Compiler, ref-as-prop, useEffectEvent, and strict TypeScript patterns. Use when creating components, managing state, typing props, handling events, using hooks, or working with React 19 features. Triggers on react, typescript, tsx, component types, hook types, react 19, react compiler, actions, use hook, useEffectEvent, activity, import defer.
metadata:
  version: "0.1.0"
---

# React TypeScript

Patterns for building type-safe React 19.2 applications with TypeScript 5.9. React Compiler handles memoization automatically - write plain components, let the tooling optimize.

## Critical Rules

### No forwardRef - ref Is a Prop Now

```tsx
// WRONG - deprecated pattern
const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <input ref={ref} {...props} />
))

// CORRECT - React 19: ref is a regular prop
function Input({ ref, ...props }: React.ComponentProps<"input">) {
  return <input ref={ref} {...props} />
}
```

### No Manual Memoization with React Compiler

```tsx
// WRONG - unnecessary with React Compiler
const MemoizedList = memo(function List({ items }: { items: Item[] }) {
  const sorted = useMemo(() => items.toSorted(compare), [items])
  const handleClick = useCallback((id: string) => onSelect(id), [onSelect])
  return sorted.map(item => <Row key={item.id} onClick={() => handleClick(item.id)} />)
})

// CORRECT - React Compiler auto-memoizes all of this
function List({ items, onSelect }: { items: Item[]; onSelect: (id: string) => void }) {
  const sorted = items.toSorted(compare)
  return sorted.map(item => <Row key={item.id} onClick={() => onSelect(item.id)} />)
}
```

### Use `React.ComponentProps<>` for Element Props

```tsx
// WRONG - manual HTML attribute typing
interface ButtonProps {
  onClick?: (e: MouseEvent<HTMLButtonElement>) => void
  disabled?: boolean
  children: React.ReactNode
  className?: string
}

// CORRECT - extend native element props
type ButtonProps = React.ComponentProps<"button"> & {
  variant?: "primary" | "ghost"
}
```

### Type State Discriminated Unions, Not Booleans

```tsx
// WRONG - impossible states possible
interface RequestState { isLoading: boolean; error: string | null; data: User | null }

// CORRECT - discriminated union prevents impossible states
type RequestState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; error: string }
  | { status: "success"; data: User }
```

### Use `satisfies` for Type-Safe Literals

```tsx
// WRONG - widens to Record<string, Route>
const routes: Record<string, Route> = { home: { path: "/" }, about: { path: "/about" } }

// CORRECT - preserves literal keys while checking shape
const routes = {
  home: { path: "/" },
  about: { path: "/about" },
} satisfies Record<string, Route>

routes.home // typed, autocomplete works
```

### Context Must Have Strict Defaults or Throw

```tsx
// WRONG - null default with no guard
const AuthContext = createContext<AuthState | null>(null)
// consumers must null-check every time

// CORRECT - factory hook that throws on missing provider
const AuthContext = createContext<AuthState | null>(null)

function useAuth(): AuthState {
  const ctx = use(AuthContext)
  if (ctx === null) throw new Error("useAuth must be used within AuthProvider")
  return ctx
}
```

### Prefer `use()` over `useContext()`

```tsx
// OLD pattern
function Header() {
  const theme = useContext(ThemeContext) // cannot use after early return
  if (!isVisible) return null
  return <h1 style={{ color: theme.color }}>Title</h1>
}

// CORRECT - React 19: use() works after early returns
function Header({ isVisible }: { isVisible: boolean }) {
  if (!isVisible) return null
  const theme = use(ThemeContext) // works here - use() is not bound by hook rules
  return <h1 style={{ color: theme.color }}>Title</h1>
}
```

## React 19 Patterns

### Component Authoring

Plain functions with `data-slot` for styling hooks. No `forwardRef`, no `FC`:

```tsx
type CardProps = React.ComponentProps<"div"> & {
  variant?: "elevated" | "outlined"
}

function Card({ variant = "outlined", className, ...props }: CardProps) {
  return (
    <div
      data-slot="card"
      data-variant={variant}
      className={cn("rounded-xl border bg-card", className)}
      {...props}
    />
  )
}

function CardTitle({ className, ...props }: React.ComponentProps<"h3">) {
  return <h3 data-slot="card-title" className={cn("font-semibold", className)} {...props} />
}
```

### Actions and useTransition

Async functions in transitions handle pending state, errors, and form resets automatically:

```tsx
function UpdateProfile({ userId }: { userId: string }) {
  const [error, submitAction, isPending] = useActionState(
    async (_prev: string | null, formData: FormData) => {
      const result = await updateProfile(userId, formData)
      if (result.error) return result.error
      redirect("/profile")
      return null
    },
    null
  )

  return (
    <form action={submitAction}>
      <input type="text" name="displayName" required />
      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Save"}
      </button>
      {error && <p className="text-destructive">{error}</p>}
    </form>
  )
}
```

**useTransition for non-form Actions:**

```tsx
function DeleteButton({ onDelete }: { onDelete: () => Promise<void> }) {
  const [isPending, startTransition] = useTransition()

  return (
    <button
      disabled={isPending}
      onClick={() => startTransition(async () => { await onDelete() })}
    >
      {isPending ? "Deleting..." : "Delete"}
    </button>
  )
}
```

**useOptimistic for instant feedback:**

```tsx
function LikeButton({ likes, onLike }: { likes: number; onLike: () => Promise<void> }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(likes, (prev) => prev + 1)

  const handleLike = async () => {
    addOptimisticLike(null)
    await onLike()
  }

  return (
    <form action={handleLike}>
      <button type="submit">{optimisticLikes} Likes</button>
    </form>
  )
}
```

### use() Hook

Read promises and context in render. Works conditionally, after early returns:

```tsx
// Reading a promise - suspends until resolved
function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  const comments = use(commentsPromise)
  return (
    <ul>
      {comments.map(c => <li key={c.id}>{c.text}</li>)}
    </ul>
  )
}

// Parent gets promise from loader/cache, NOT created during render
function PostPage({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  return (
    <Suspense fallback={<Skeleton />}>
      <Comments commentsPromise={commentsPromise} />
    </Suspense>
  )
}

// Reading context conditionally
function AdminPanel({ user }: { user: User | null }) {
  if (!user) return <LoginPrompt />
  const permissions = use(PermissionsContext) // legal - use() works after early return
  if (!permissions.isAdmin) return <Forbidden />
  return <Dashboard user={user} permissions={permissions} />
}
```

**Important:** `use()` does not support promises created during render. Pass promises from loaders, server functions, or cached sources.

### Activity Component (React 19.2)

Preserve state of hidden UI. Hidden children keep their state and DOM but unmount effects:

```tsx
import { Activity, useState } from "react"

function TabLayout({ tabs }: { tabs: TabConfig[] }) {
  const [activeTab, setActiveTab] = useState(tabs[0].id)

  return (
    <div>
      <nav>
        {tabs.map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}>
            {tab.label}
          </button>
        ))}
      </nav>

      {tabs.map(tab => (
        <Activity key={tab.id} mode={activeTab === tab.id ? "visible" : "hidden"}>
          <tab.component />
        </Activity>
      ))}
    </div>
  )
}
```

**Key behaviors:**
- `visible` - renders normally, effects mounted
- `hidden` - hides via `display: none`, effects cleaned up, state preserved, updates deferred
- Pre-rendering: `<Activity mode="hidden">` renders children at low priority for faster future reveals
- DOM side effects (video, audio) persist when hidden - add `useLayoutEffect` cleanup

### useEffectEvent (React 19.2)

Extract non-reactive logic from effects. The event function always sees latest props/state without triggering effect re-runs:

```tsx
function ChatRoom({ roomId, theme }: { roomId: string; theme: string }) {
  const onConnected = useEffectEvent(() => {
    showNotification("Connected!", theme) // always reads latest theme
  })

  useEffect(() => {
    const connection = createConnection(roomId)
    connection.on("connected", () => onConnected())
    connection.connect()
    return () => connection.disconnect()
  }, [roomId]) // theme NOT in deps - onConnected is an Effect Event
}
```

**Rules:**
- Only call from inside effects or other effect events
- Never pass to child components or include in dependency arrays
- Never call during render
- Use for logic that is conceptually an "event" fired from an effect

**Custom hook pattern:**

```tsx
function useInterval(callback: () => void, delay: number | null) {
  const onTick = useEffectEvent(callback)

  useEffect(() => {
    if (delay === null) return
    const id = setInterval(() => onTick(), delay)
    return () => clearInterval(id)
  }, [delay])
}
```

### Document Metadata

Render `<title>`, `<meta>`, and `<link>` directly in components - React hoists them to `<head>`:

```tsx
function BlogPost({ post }: { post: Post }) {
  return (
    <article>
      <title>{post.title}</title>
      <meta name="description" content={post.excerpt} />
      <meta name="author" content={post.author} />
      <link rel="canonical" href={`https://example.com/posts/${post.slug}`} />
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}
```

### Context as Provider

```tsx
const ThemeContext = createContext<Theme>("light")

// React 19 - use Context directly as provider (no .Provider)
function App({ children }: { children: React.ReactNode }) {
  return (
    <ThemeContext value="dark">
      {children}
    </ThemeContext>
  )
}
```

### Ref Cleanup Functions

```tsx
function MeasuredBox() {
  return (
    <div
      ref={(node) => {
        if (node) {
          const observer = new ResizeObserver(handleResize)
          observer.observe(node)
          return () => observer.disconnect() // cleanup on unmount
        }
      }}
    />
  )
}
```

## React Compiler

### What It Does

React Compiler (`babel-plugin-react-compiler`) analyzes your code at build time and automatically inserts memoization. It replaces manual `useMemo`, `useCallback`, and `React.memo` in most cases.

**Auto-memoizes:**
- Component return values (skip re-render if props unchanged)
- Expensive computations inside components
- Callback functions passed as props
- JSX element creation

### Setup (Vite)

```bash
pnpm add -D babel-plugin-react-compiler
```

```ts
// vite.config.ts
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: ["babel-plugin-react-compiler"], // must be first
      },
    }),
  ],
})
```

### What NOT to Do

```tsx
// DON'T - compiler handles this
const MemoComponent = memo(MyComponent)
const memoized = useMemo(() => expensive(data), [data])
const stableCallback = useCallback(() => handler(id), [id])

// DO - write plain code, compiler optimizes
function MyComponent({ data, onSelect }: Props) {
  const processed = expensive(data)
  return <Child onClick={() => onSelect(data.id)} />
}
```

### When Manual Memoization Still Applies

- `useMemo`/`useCallback` as effect dependencies when you need precise control over when effects fire
- Values shared across many components (compiler memoizes per-component, not globally)
- Opting out: `"use no memo"` directive skips compilation for a specific component

### Verification

Components optimized by the compiler show a "Memo" badge in React DevTools. Check build output for `react/compiler-runtime` imports.

## TypeScript Patterns

### Strict tsconfig for React

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "target": "esnext",
    "module": "nodenext",
    "moduleDetection": "force",
    "jsx": "react-jsx",
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedSideEffectImports": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "types": []
  }
}
```

### Component Props Patterns

```tsx
// Extending native element props
type ButtonProps = React.ComponentProps<"button"> & {
  variant?: "primary" | "secondary"
  isLoading?: boolean
}

function Button({ variant = "primary", isLoading, children, ...props }: ButtonProps) {
  return (
    <button data-slot="button" disabled={isLoading || props.disabled} {...props}>
      {isLoading ? <Spinner /> : children}
    </button>
  )
}

// Polymorphic "as" prop
type PolymorphicProps<E extends React.ElementType> = {
  as?: E
} & Omit<React.ComponentProps<E>, "as">

function Text<E extends React.ElementType = "span">({
  as,
  ...props
}: PolymorphicProps<E>) {
  const Component = as || "span"
  return <Component {...props} />
}

// Usage: <Text as="h1">Hello</Text>
```

### Event Handler Types

```tsx
function Form() {
  // Inferred from handler context - no explicit typing needed
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    // process formData
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value)
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") submit()
  }

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} onKeyDown={handleKeyDown} />
    </form>
  )
}
```

### Hook Types

```tsx
// useState - inferred when initial value provided
const [count, setCount] = useState(0) // number
const [user, setUser] = useState<User | null>(null) // explicit for null init

// useReducer - discriminated union actions
type CounterAction =
  | { type: "increment"; amount: number }
  | { type: "decrement"; amount: number }
  | { type: "reset" }

function counterReducer(state: number, action: CounterAction): number {
  switch (action.type) {
    case "increment": return state + action.amount
    case "decrement": return state - action.amount
    case "reset": return 0
  }
}

const [count, dispatch] = useReducer(counterReducer, 0)
dispatch({ type: "increment", amount: 5 })

// useRef - element refs (React 19: returns RefObject<T | null>, always nullable)
const inputRef = useRef<HTMLInputElement>(null)

// useRef - mutable value (no null)
const intervalRef = useRef<number | undefined>(undefined)
```

### Generic Components

```tsx
type SelectProps<T> = {
  items: T[]
  value: T
  onChange: (item: T) => void
  getLabel: (item: T) => string
  getKey: (item: T) => string
}

function Select<T>({ items, value, onChange, getLabel, getKey }: SelectProps<T>) {
  return (
    <select
      value={getKey(value)}
      onChange={(e) => {
        const item = items.find(i => getKey(i) === e.target.value)
        if (item) onChange(item)
      }}
    >
      {items.map(item => (
        <option key={getKey(item)} value={getKey(item)}>
          {getLabel(item)}
        </option>
      ))}
    </select>
  )
}

// Usage - T inferred as User
<Select
  items={users}
  value={selectedUser}
  onChange={setSelectedUser}
  getLabel={u => u.name}
  getKey={u => u.id}
/>
```

### Discriminated Unions for Component State

```tsx
type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; error: Error }
  | { status: "success"; data: T }

function AsyncContent<T>({
  state,
  render,
}: {
  state: AsyncState<T>
  render: (data: T) => React.ReactNode
}) {
  switch (state.status) {
    case "idle": return null
    case "loading": return <Spinner />
    case "error": return <ErrorDisplay error={state.error} />
    case "success": return <>{render(state.data)}</>
  }
}
```

### Zod v4 Integration

```tsx
import { z } from "zod"

const UserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(["admin", "user", "viewer"]),
})

type User = z.infer<typeof UserSchema>

// Form validation with useActionState
type FieldErrors = { name?: string[]; email?: string[]; role?: string[] }

function CreateUser() {
  const [errors, submitAction, isPending] = useActionState(
    async (_prev: FieldErrors | null, formData: FormData) => {
      const result = UserSchema.safeParse(Object.fromEntries(formData))
      if (!result.success) {
        // Zod v4: use z.flattenError() to get field-level errors
        const flat = z.flattenError(result.error)
        return flat.fieldErrors as FieldErrors
      }
      await saveUser(result.data)
      return null
    },
    null
  )

  return (
    <form action={submitAction}>
      <input name="name" />
      {errors?.name && (
        <span className="text-destructive">{errors.name[0]}</span>
      )}
      <input name="email" type="email" />
      <select name="role">
        <option value="user">User</option>
        <option value="admin">Admin</option>
        <option value="viewer">Viewer</option>
      </select>
      <button type="submit" disabled={isPending}>Create</button>
    </form>
  )
}
```

## Best Practices

1. **Plain functions for components** - no `FC`, no `forwardRef`, no `memo`. `FC` implicitly typed `children` in older types and adds no value over plain function signatures. Let React Compiler optimize.
2. **`React.ComponentProps<"element">`** for extending native elements - catches all HTML attributes.
3. **Discriminated unions over booleans** for state - prevents impossible states at the type level.
4. **`use()` over `useContext()`** - works conditionally, cleaner for context with guards.
5. **`satisfies` for config objects** - preserves literal types while validating shape.
6. **`Activity` over conditional rendering** when state preservation matters (tabs, sidebars, wizards).
7. **`useEffectEvent` over suppressing deps** - extracts non-reactive logic cleanly from effects.
8. **Strict tsconfig** - enable `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `verbatimModuleSyntax`.
9. **`as const satisfies`** for route configs, theme tokens, and lookup objects.
10. **Type narrowing in switch** - exhaustive checks via `never` in default cases.
11. **`import defer`** (TS 5.9) - defer module evaluation until first property access for lazy-loaded heavy modules. See [typescript-patterns.md](references/typescript-patterns.md).

## Deep Dives

- [react-19-features.md](references/react-19-features.md) - Complete React 19/19.2 feature reference with detailed examples
- [typescript-patterns.md](references/typescript-patterns.md) - Advanced TypeScript patterns for React: generics, utility types, strict config, type-level programming

## Resources

- **React Docs**: https://react.dev
- **React 19.2 Blog Post**: https://react.dev/blog/2025/10/01/react-19-2
- **React Compiler**: https://react.dev/learn/react-compiler
- **TypeScript 5.9**: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-9.html
- **TypeScript 5.8**: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-8.html
- **React TypeScript Cheatsheet**: https://react-typescript-cheatsheet.netlify.app/
