---
name: syncore-react-realtime
description: React patterns for Syncore including SyncoreProvider, platform wrapper providers, useQuery, useMutation, useAction, useQueries, skip semantics, loading state handling, and inference-safe hook usage. Use when wiring Syncore into React apps or debugging hook inference and subscription lifecycle issues.
---

# Syncore React Realtime

Use this skill when wiring Syncore into React apps or debugging hook inference,
watch lifecycle, or result propagation.

## Documentation Sources

Read these first:

- `packages/react/src/index.tsx`
- `packages/react/AGENTS.md`
- `packages/platform-web/src/react.tsx`
- `packages/platform-node/src/ipc-react.tsx`
- `packages/platform-expo/src/react.tsx`
- `packages/next/src/index.tsx`
- `docs/quickstarts/react-web.md`
- `docs/quickstarts/expo.md`
- `docs/quickstarts/electron.md`
- `docs/quickstarts/next-pwa.md`
- `examples/electron/src/renderer/App.tsx`
- `examples/expo/App.tsx`
- `examples/next-pwa/app/bookmarks-screen.tsx`

## Instructions

### Provider First

Every hook depends on `SyncoreProvider` or a platform wrapper that mounts it
for you.

Raw provider:

```tsx
import { SyncoreProvider } from "syncorejs/react";

<SyncoreProvider client={client}>{children}</SyncoreProvider>;
```

Common wrapper providers in app code are:

- `SyncoreBrowserProvider` from `syncorejs/browser/react`
- `SyncoreElectronProvider` from `syncorejs/node/ipc/react`
- `SyncoreExpoProvider` from `syncorejs/expo/react`
- `SyncoreNextProvider` from `syncorejs/next`

If no provider is present, hooks will throw.

### useQuery

`useQuery` is the core reactive read API. It returns `undefined` while the
first result is still loading.

```tsx
import { useQuery } from "syncorejs/react";
import { api } from "../syncore/_generated/api";

function Tasks() {
  const tasks = useQuery(api.tasks.list) ?? [];
  return <pre>{JSON.stringify(tasks, null, 2)}</pre>;
}
```

Pass `"skip"` as the second argument to suppress the subscription entirely:

```tsx
import { skip, useQuery } from "syncorejs/react";

const results = useQuery(
  api.notes.search,
  searchText.trim() ? { query: searchText.trim() } : skip
);
```

### useMutation And useAction

Mutations and actions return callable functions with typed args and results
inferred from the reference.

```tsx
import { useAction, useMutation } from "syncorejs/react";
import { api } from "../syncore/_generated/api";

const createTask = useMutation(api.tasks.create);
const exportTasks = useAction(api.tasks.exportTasks);
```

### Prefer Inference Over Manual Generics

Preferred:

```tsx
const todos = useQuery(api.todos.list) ?? [];
const createTodo = useMutation(api.todos.create);
```

Fallbacks with manual generics should be treated as a signal to inspect shared
typing, not as the ideal pattern.

### Watch Lifecycle Matters

Syncore React hooks are thin wrappers over `SyncoreClient.watchQuery(...)`.
When changing React bindings:

- preserve stable args behavior
- dispose watches when refs or args change
- keep React types aligned with `SyncoreClient`

### useQueries

Use `useQueries` when a keyed batch of query subscriptions is the right shape
for the view:

```tsx
const data = useQueries([
  { key: "tasks", reference: api.tasks.list },
  { key: "notes", reference: api.notes.list }
]);
```

Represent the result as keyed query state, not as a substitute for ordinary
component composition.

`useQueries` is intentionally less strongly typed than `useQuery`,
`useMutation`, and `useAction`. Prefer the single-hook APIs when they fit the
component shape better.

## Examples

### Basic App Wiring

```tsx
import { SyncoreProvider, useMutation, useQuery } from "syncorejs/react";
import type { SyncoreClient } from "syncorejs";
import { api } from "../syncore/_generated/api";

export function App({ client }: { client: SyncoreClient }) {
  return (
    <SyncoreProvider client={client}>
      <Todos />
    </SyncoreProvider>
  );
}

function Todos() {
  const todos = useQuery(api.todos.list) ?? [];
  const createTodo = useMutation(api.todos.create);

  return (
    <div>
      <button onClick={() => void createTodo({ title: "Ship local-first DX" })}>
        Add
      </button>
      {todos.map((todo) => (
        <div key={todo._id}>{todo.title}</div>
      ))}
    </div>
  );
}
```

### Platform Wrapper Example

```tsx
import { SyncoreNextProvider } from "syncorejs/next";

const createWorker = () =>
  new Worker(new URL("./syncore.worker", import.meta.url), {
    type: "module"
  });

export function AppSyncoreProvider({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <SyncoreNextProvider createWorker={createWorker}>
      {children}
    </SyncoreNextProvider>
  );
}
```

### Loading State

```tsx
function Notes() {
  const notes = useQuery(api.notes.list);
  if (notes === undefined) {
    return <div>Loading...</div>;
  }
  return <pre>{JSON.stringify(notes, null, 2)}</pre>;
}
```

## Best Practices

- Always mount hooks under `SyncoreProvider` or a platform wrapper provider
- Prefer `useQuery(api.foo.bar)` without manual generics when typing supports it
- Handle `undefined` loading state explicitly
- Use `skip` instead of hand-rolled conditional subscriptions
- Keep hooks thin over `SyncoreClient` rather than duplicating runtime behavior
- Prefer platform wrapper providers in app shells and the raw provider in low-level tests or custom integrations
- When editing hook types, validate inference and watch cleanup together

## Common Pitfalls

1. Calling hooks outside a Syncore provider
2. Treating manual generics as the desired steady state for app code
3. Forgetting that query subscriptions must be cleaned up when args or refs change
4. Narrowing React-facing types more than the core client allows
5. Using `useQueries` where better-typed independent hooks would be clearer

## References

- `packages/react/src/index.tsx`
- `packages/react/AGENTS.md`
- `packages/platform-web/src/react.tsx`
- `packages/platform-node/src/ipc-react.tsx`
- `packages/platform-expo/src/react.tsx`
- `packages/next/src/index.tsx`
