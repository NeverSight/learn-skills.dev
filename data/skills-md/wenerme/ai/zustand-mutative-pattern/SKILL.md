---
name: zustand-mutative-pattern
description: 'Use when implementing React state management with Zustand, including context-scoped stores, mutative updates, or actions namespace patterns'
---

# Zustand Context-Mutative Architecture

You are strictly required to follow this custom Zustand architecture pattern. Do NOT use plain global Zustand stores unless explicitly told otherwise. This project uses a **Bounded Context + Mutative Store** approach.

## 1. Core Architectural Rules (MUST FOLLOW)

1. **Actions Namespace:** All state modification functions MUST be grouped under an `actions` object. NEVER put actions at the root level of state.
2. **State Grouping:** Related UI states MUST be nested (e.g., `sidebar: { open: boolean }`, NOT `sidebarOpen: boolean`).
3. **Mutative Updates:** State updates MUST use `mutative` from `zustand-mutative`. Do NOT use plain spread operators for deep updates.
4. **Context Isolation:** Stores MUST be provided via React Context for scope isolation and SSR safety. NEVER use global singleton stores.
5. **Shallow Equality:** When selecting multiple properties, you MUST wrap the selector with `useShallow`.
6. **Event-Driven Side-Effects:** Store MUST only manage state and emit events. Side-effects (Toast, dialogs, network) MUST be handled by Sidecar components.

## 2. Store Definition & Factory

```typescript
import { mutative } from 'zustand-mutative';
import { createStore } from 'zustand/vanilla';
import type Emittery from 'emittery';

export type XxxStoreState = {
  // Data State
  loading: boolean;
  items: Item[];

  // UI State — MUST be grouped
  sidebar: { open: boolean };

  // Actions — MUST be namespaced
  actions: {
    refresh: () => void;
    select: (item: Item) => void;
  };

  // Event Emitter (optional, for side-effect decoupling)
  events?: Emittery<EventData>;
};

type CreateXxxStoreOptions = Partial<Omit<XxxStoreState, 'actions'>> & {
  actions?: Partial<XxxStoreState['actions']>;
};

export type XxxStore = ReturnType<typeof createXxxStore>;

export function createXxxStore(partial: CreateXxxStoreOptions = {}) {
  return createStore(
    // MUST use mutative
    mutative<XxxStoreState>((setState, getState) => ({
      loading: false,
      items: [],
      sidebar: { open: false },
      ...partial,

      actions: {
        refresh: () => { /* impl */ },
        select: (item) => {
          // Direct mutation via zustand-mutative
          setState((s) => { s.selected = item; });
        },
        ...partial.actions, // Support overriding defaults
      },
    })),
  );
}
```

## 3. Provider & Context

```tsx
import { createReactContext } from '@wener/reaction';
import { maybeFunction, type MaybeFunction } from '@wener/utils';

const XxxContext = createReactContext<XxxStore | undefined>('XxxContext', undefined);

export const XxxProvider = ({
  children,
  store,
  initialState,
}: {
  children: ReactNode;
  store?: XxxStore;
  initialState?: MaybeFunction<CreateXxxStoreOptions>;
}) => {
  // Support inheriting from parent context
  const parentStore = use(XxxContext);
  const [value] = useState(() => {
    if (store) return store;
    const initial = maybeFunction(initialState);
    return createXxxStore({ ...initial });
  });
  return <XxxContext value={value}>{children}</XxxContext>;
};
```

## 4. Hooks (Bounded Store)

```typescript
import { createBoundedUseStore } from '@wener/reaction/zustand';
import type { ExtractState } from 'zustand';
import { useShallow } from 'zustand/react/shallow';

// Get Store instance
export function useXxxStoreContext(): XxxStore {
  const store = use(XxxContext);
  if (!store) throw new Error('XxxStore not found, wrap with XxxProvider');
  return store;
}

type UseStore = {
  (): ExtractState<XxxStore>;
  <T = any>(selector: (state: ExtractState<XxxStore>) => T): T;
};

// Bounded store hook: useXxxStore(s => s.loading)
export const useXxxStore: UseStore = createBoundedUseStore(useXxxStoreContext);

// Action shortcut
export function useXxxActions() {
  return useXxxStore((s) => s.actions);
}

// MUST use useShallow when selecting multiple properties
export function useXxxSelection() {
  return useXxxStore(
    useShallow((s) => ({ path: s.path, items: s.items }))
  );
}
```

**Naming Convention:**
- `useXxxStoreContext()` — returns store instance (for direct store operations)
- `useXxxStore(selector)` — bounded store hook (for selecting state)

## 5. Advanced Patterns

For complete implementation examples including event-driven Sidecar pattern, Store inheritance, actions override, and performance optimization details, read: [references/zustand-pattern.md](references/zustand-pattern.md)
