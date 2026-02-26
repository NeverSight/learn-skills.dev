---
name: zustand
description: Zustand state management patterns for React including store design, selectors, slices, middleware (immer, persist, devtools), and async actions. Use when managing client-side state, creating stores, working with Zustand, or when the user asks about global state management, store patterns, or state persistence.
---

# Zustand Patterns

## Basic Store

```typescript
import { create } from "zustand";

interface CounterStore {
    count: number;
    increment: () => void;
    decrement: () => void;
    reset: () => void;
}

const useCounterStore = create<CounterStore>((set) => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
    reset: () => set({ count: 0 }),
}));
```

## Selectors

Always select only the state you need — this prevents re-renders when unrelated state changes:

```tsx
// Select individual values
const count = useCounterStore((state) => state.count);
const increment = useCounterStore((state) => state.increment);

// Select multiple values with useShallow
import { useShallow } from "zustand/shallow";

const { count, increment } = useCounterStore(
    useShallow((state) => ({ count: state.count, increment: state.increment })),
);
```

Never destructure the entire store without a selector:

```typescript
// Bad — re-renders on every state change
const { count, increment } = useCounterStore();

// Good — re-renders only when count changes
const count = useCounterStore((state) => state.count);
```

## Async Actions

```typescript
interface UserStore {
    user: User | null;
    isLoading: boolean;
    error: string | null;
    fetchUser: (id: string) => Promise<void>;
}

const useUserStore = create<UserStore>((set) => ({
    user: null,
    isLoading: false,
    error: null,
    fetchUser: async (id) => {
        set({ isLoading: true, error: null });
        try {
            const user = await api.users.getById(id);
            set({ user, isLoading: false });
        } catch (error) {
            set({ error: "Failed to fetch user", isLoading: false });
        }
    },
}));
```

For server data, prefer TanStack Query over Zustand — Zustand is for client-only state.

## Middleware

### Immer

Write mutable-looking updates safely:

```typescript
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

const useTodoStore = create<TodoStore>()(
    immer((set) => ({
        todos: [],
        addTodo: (text) =>
            set((state) => {
                state.todos.push({ id: crypto.randomUUID(), text, completed: false });
            }),
        toggleTodo: (id) =>
            set((state) => {
                const todo = state.todos.find((t) => t.id === id);
                if (todo) todo.completed = !todo.completed;
            }),
    })),
);
```

### Persist

Sync state to storage:

```typescript
import { persist } from "zustand/middleware";

const useSettingsStore = create<SettingsStore>()(
    persist(
        (set) => ({
            theme: "light",
            language: "en",
            setTheme: (theme) => set({ theme }),
            setLanguage: (language) => set({ language }),
        }),
        {
            name: "settings",
            partialize: (state) => ({
                theme: state.theme,
                language: state.language,
            }),
        },
    ),
);
```

- `name` is the storage key.
- `partialize` controls which state is persisted — exclude functions and transient state.
- Default storage is `localStorage`. Use `storage: createJSONStorage(() => sessionStorage)` for session storage.

### Devtools

```typescript
import { devtools } from "zustand/middleware";

const useStore = create<Store>()(
    devtools(
        (set) => ({
            // ...
        }),
        { name: "MyStore" },
    ),
);
```

### Combining Middleware

Stack middleware from inside out — **immer → persist → devtools**:

```typescript
const useStore = create<Store>()(
    devtools(
        persist(
            immer((set) => ({
                // store definition
            })),
            { name: "store-key" },
        ),
        { name: "StoreName" },
    ),
);
```

## Slice Pattern

Split large stores into logical slices:

```typescript
interface AuthSlice {
    user: User | null;
    login: (credentials: Credentials) => Promise<void>;
    logout: () => void;
}

interface UISlice {
    sidebarOpen: boolean;
    toggleSidebar: () => void;
}

const createAuthSlice: StateCreator<AuthSlice & UISlice, [], [], AuthSlice> = (set) => ({
    user: null,
    login: async (credentials) => {
        const user = await api.auth.login(credentials);
        set({ user });
    },
    logout: () => set({ user: null }),
});

const createUISlice: StateCreator<AuthSlice & UISlice, [], [], UISlice> = (set) => ({
    sidebarOpen: true,
    toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
});

const useAppStore = create<AuthSlice & UISlice>()((...args) => ({
    ...createAuthSlice(...args),
    ...createUISlice(...args),
}));
```

## Computed / Derived State

Derive values in selectors, not in the store:

```typescript
// In the component or a custom hook
const completedCount = useTodoStore((state) => state.todos.filter((t) => t.completed).length);

// For expensive computations, memoize
const stats = useTodoStore(
    useShallow((state) => ({
        total: state.todos.length,
        completed: state.todos.filter((t) => t.completed).length,
    })),
);
```

## Accessing State Outside React

```typescript
// Get current state
const count = useCounterStore.getState().count;

// Subscribe to changes
const unsubscribe = useCounterStore.subscribe((state) => console.log("Count:", state.count));

// Set state from outside React
useCounterStore.getState().increment();
```

## Store Organization

```
src/
├── stores/
│   ├── auth-store.ts
│   ├── settings-store.ts
│   └── ui-store.ts
```

- One store per domain concern.
- Keep stores small and focused — don't create a single global "app store".
- Name stores with the `use*Store` convention.

## When to Use Zustand vs. Alternatives

| Use Case                                 | Solution              |
| ---------------------------------------- | --------------------- |
| Client UI state (theme, sidebar, modals) | Zustand               |
| Server data (API responses, caching)     | TanStack Query        |
| Form state                               | React Hook Form       |
| URL state (filters, pagination)          | URL search params     |
| Component-local state                    | useState / useReducer |
| Global shared state (auth, preferences)  | Zustand               |
