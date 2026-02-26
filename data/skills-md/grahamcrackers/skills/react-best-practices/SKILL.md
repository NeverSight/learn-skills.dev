---
name: react-best-practices
description: Modern React 19 patterns for components, hooks, state management, performance, and project structure. Use when writing React components, reviewing React code, designing component APIs, or when the user asks about React conventions, architecture, or best practices.
---

# React Best Practices

## Component Design

- One component per file. Name the file the same as the component.
- Prefer function components — never write class components.
- Keep components small and focused. If a component exceeds ~150 lines, split it.
- Define components at module scope — never define components inside other components (breaks state preservation and identity).
- Colocate related files (component, hook, types, styles, tests) in the same directory.

## Props

- Destructure props in the function signature:

```tsx
function UserCard({ name, email, avatar }: UserCardProps) { ... }
```

- Use `children` via `React.PropsWithChildren` or explicit `children: React.ReactNode`.
- Prefer specific prop types over `Record<string, unknown>` or `any`.
- Avoid prop drilling beyond 2-3 levels — use composition, context, or a state management solution.

## Hooks

- Follow the Rules of Hooks: only call at the top level, only in React components or custom hooks.
- Extract reusable logic into custom hooks (`use*` prefix).
- Keep hooks focused — a hook that does too many things should be split.

### State Management

- Keep state as local as possible. Lift only when sibling components need it.
- Use `useReducer` for complex state with multiple related transitions.
- Reserve context for truly global concerns (theme, auth, locale) — not frequently changing data.
- For server state, use TanStack Query or a similar library instead of `useState` + `useEffect`.

### React 19 Hooks

- **`use()`**: Read context or unwrap promises inside components. Replaces some `useContext` patterns.
- **`useActionState()`**: Manage form submission state (pending, error, result) without manual boilerplate.
- **`useOptimistic()`**: Show optimistic UI immediately during async operations.
- **`useTransition()`**: Wrap non-urgent state updates to keep the UI responsive.

## React 19 Patterns

### Automatic Memoization (React Compiler)

When using the React Compiler:

- Remove manual `React.memo()`, `useMemo()`, and `useCallback()` — the compiler handles memoization automatically.
- If not using the compiler, still be intentional — only memoize when profiling reveals a real performance issue.

### Actions and Forms

Use React 19 Actions for form handling:

```tsx
function CreatePost() {
    const [state, action, isPending] = useActionState(createPostAction, null);

    return (
        <form action={action}>
            <input name="title" required />
            <button type="submit" disabled={isPending}>
                Create
            </button>
            {state?.error && <p>{state.error}</p>}
        </form>
    );
}
```

### Server Components

- Default to server components for non-interactive content (data display, lists, static layouts).
- Add `"use client"` only when the component needs interactivity (event handlers, hooks, browser APIs).
- Push `"use client"` boundaries as far down the tree as possible.

## Performance

- Use `React.lazy()` + `Suspense` for code-splitting large routes and heavy components.
- Use `startTransition` for expensive state updates that don't need immediate rendering.
- Wrap `Suspense` boundaries around async data fetching to avoid waterfall loading.
- Avoid creating new objects/arrays in JSX props on every render — extract to constants or memoize.

## Patterns

### Composition over Configuration

Prefer composable children over giant config props:

```tsx
// Prefer
<Dialog>
  <Dialog.Header>Title</Dialog.Header>
  <Dialog.Body>Content</Dialog.Body>
  <Dialog.Footer>
    <Button>Close</Button>
  </Dialog.Footer>
</Dialog>

// Avoid
<Dialog
  header="Title"
  body="Content"
  footer={<Button>Close</Button>}
/>
```

### Render Props & Children as Function

Use when a component needs to share render-time data without prescribing UI:

```tsx
<DataLoader query={userQuery}>{(data) => <UserProfile user={data} />}</DataLoader>
```

### Custom Hook + Component Pairs

Separate logic from presentation:

```tsx
function useUserSearch(query: string) {
    // filtering, debouncing, API calls
    return { results, isLoading, error };
}

function UserSearch() {
    const [query, setQuery] = useState("");
    const { results, isLoading } = useUserSearch(query);
    // render
}
```

## Error Handling

- Use Error Boundaries to catch render errors and show fallback UI.
- Don't use Error Boundaries for event handler errors — use try/catch in the handler.
- Provide meaningful fallback UI, not blank screens.

## Testing

- Test behavior, not implementation. Query by role, label, or text — not by test IDs or CSS classes.
- Use `@testing-library/react` for component tests.
- Mock at the network boundary (e.g., MSW) rather than mocking hooks or internal state.
- Test custom hooks with `renderHook` from `@testing-library/react`.

## Project Structure

```
src/
├── components/       # shared/reusable components
│   └── button/
│       ├── button.tsx
│       ├── button.test.tsx
│       └── index.ts
├── features/         # feature-specific code (components, hooks, utils)
│   └── auth/
├── hooks/            # shared custom hooks
├── lib/              # utilities, API clients, helpers
├── types/            # shared TypeScript types
└── app/              # routes / pages
```

Colocate feature-specific code in `features/` and only promote to `components/` or `hooks/` when reused across features.
