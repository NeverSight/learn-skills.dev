---
name: zustand-state
description: State management with Zustand for Remix/React applications. Covers store creation, TypeScript patterns, persistence, and Shopify-specific state patterns.
---

# Zustand State Management

Zustand is a lightweight, fast state management solution perfect for Shopify Remix apps. It's simpler than Redux, more flexible than Context, and works seamlessly with TypeScript.

## Why Zustand for Shopify Apps?

- **Minimal boilerplate**: No providers, no reducers, no actions
- **TypeScript-first**: Full type inference out of the box
- **Small bundle**: ~1KB gzipped
- **Remix-friendly**: Works with SSR without hydration issues
- **Selective re-renders**: Components only re-render when their selected state changes

## Installation

```bash
npm install zustand
```

## 1. Basic Store Pattern

### Simple Store

```typescript
// app/stores/app-store.ts
import { create } from 'zustand';

interface AppState {
  // State
  isLoading: boolean;
  selectedProductIds: string[];

  // Actions
  setLoading: (loading: boolean) => void;
  selectProduct: (id: string) => void;
  deselectProduct: (id: string) => void;
  clearSelection: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  isLoading: false,
  selectedProductIds: [],

  // Actions
  setLoading: (loading) => set({ isLoading: loading }),

  selectProduct: (id) => set((state) => ({
    selectedProductIds: [...state.selectedProductIds, id]
  })),

  deselectProduct: (id) => set((state) => ({
    selectedProductIds: state.selectedProductIds.filter(pid => pid !== id)
  })),

  clearSelection: () => set({ selectedProductIds: [] }),
}));
```

### Usage in Components

```typescript
// app/components/ProductList.tsx
import { useAppStore } from '~/stores/app-store';

export function ProductList() {
  // Select only what you need (prevents unnecessary re-renders)
  const selectedIds = useAppStore((state) => state.selectedProductIds);
  const selectProduct = useAppStore((state) => state.selectProduct);

  return (
    <ResourceList
      items={products}
      renderItem={(product) => (
        <ResourceItem
          id={product.id}
          selected={selectedIds.includes(product.id)}
          onClick={() => selectProduct(product.id)}
        />
      )}
    />
  );
}
```

## 2. TypeScript Patterns

### Slice Pattern (Recommended for Large Apps)

```typescript
// app/stores/slices/product-slice.ts
import { StateCreator } from 'zustand';

export interface ProductSlice {
  products: Product[];
  selectedProductId: string | null;
  setProducts: (products: Product[]) => void;
  selectProduct: (id: string | null) => void;
}

export const createProductSlice: StateCreator<ProductSlice> = (set) => ({
  products: [],
  selectedProductId: null,
  setProducts: (products) => set({ products }),
  selectProduct: (id) => set({ selectedProductId: id }),
});
```

```typescript
// app/stores/slices/ui-slice.ts
import { StateCreator } from 'zustand';

export interface UISlice {
  isSidebarOpen: boolean;
  activeModal: string | null;
  toggleSidebar: () => void;
  openModal: (modalId: string) => void;
  closeModal: () => void;
}

export const createUISlice: StateCreator<UISlice> = (set) => ({
  isSidebarOpen: true,
  activeModal: null,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  openModal: (modalId) => set({ activeModal: modalId }),
  closeModal: () => set({ activeModal: null }),
});
```

```typescript
// app/stores/index.ts
import { create } from 'zustand';
import { ProductSlice, createProductSlice } from './slices/product-slice';
import { UISlice, createUISlice } from './slices/ui-slice';

type StoreState = ProductSlice & UISlice;

export const useStore = create<StoreState>()((...args) => ({
  ...createProductSlice(...args),
  ...createUISlice(...args),
}));
```

### Typed Selectors (Performance Optimization)

```typescript
// app/stores/selectors.ts
import { useStore } from './index';
import { useShallow } from 'zustand/react/shallow';

// Single value selector
export const useSelectedProductId = () =>
  useStore((state) => state.selectedProductId);

// Multiple values with shallow compare (prevents unnecessary re-renders)
export const useProductState = () =>
  useStore(
    useShallow((state) => ({
      products: state.products,
      selectedId: state.selectedProductId,
    }))
  );

// Derived state
export const useSelectedProduct = () =>
  useStore((state) =>
    state.products.find(p => p.id === state.selectedProductId)
  );
```

## 3. Persistence (LocalStorage/SessionStorage)

```typescript
// app/stores/settings-store.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface SettingsState {
  theme: 'light' | 'dark';
  itemsPerPage: number;
  setTheme: (theme: 'light' | 'dark') => void;
  setItemsPerPage: (count: number) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      theme: 'light',
      itemsPerPage: 25,
      setTheme: (theme) => set({ theme }),
      setItemsPerPage: (count) => set({ itemsPerPage: count }),
    }),
    {
      name: 'app-settings', // localStorage key
      storage: createJSONStorage(() => localStorage),
      // Only persist specific fields
      partialize: (state) => ({
        theme: state.theme,
        itemsPerPage: state.itemsPerPage
      }),
    }
  )
);
```

### SSR-Safe Persistence (Important for Remix)

```typescript
// app/stores/persisted-store.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

// Prevent hydration mismatch
const storage = createJSONStorage(() => {
  if (typeof window === 'undefined') {
    return {
      getItem: () => null,
      setItem: () => {},
      removeItem: () => {},
    };
  }
  return localStorage;
});

export const usePersistedStore = create<State>()(
  persist(
    (set) => ({
      // ... state and actions
    }),
    {
      name: 'my-store',
      storage,
      skipHydration: true, // Manual hydration control
    }
  )
);

// In root.tsx or layout
useEffect(() => {
  usePersistedStore.persist.rehydrate();
}, []);
```

## 4. Shopify-Specific Patterns

### Shop Context Store

```typescript
// app/stores/shop-store.ts
import { create } from 'zustand';

interface ShopInfo {
  id: string;
  name: string;
  domain: string;
  plan: string;
  currency: string;
}

interface ShopState {
  shop: ShopInfo | null;
  isAuthenticated: boolean;
  setShop: (shop: ShopInfo) => void;
  clearShop: () => void;
}

export const useShopStore = create<ShopState>((set) => ({
  shop: null,
  isAuthenticated: false,
  setShop: (shop) => set({ shop, isAuthenticated: true }),
  clearShop: () => set({ shop: null, isAuthenticated: false }),
}));
```

### Bulk Operations Store

```typescript
// app/stores/bulk-operations-store.ts
import { create } from 'zustand';

type OperationStatus = 'idle' | 'running' | 'completed' | 'failed';

interface BulkOperation {
  id: string;
  type: 'product-update' | 'inventory-sync' | 'price-change';
  status: OperationStatus;
  progress: number;
  totalItems: number;
  processedItems: number;
  errors: string[];
}

interface BulkOperationsState {
  operations: Map<string, BulkOperation>;
  activeOperationId: string | null;

  startOperation: (id: string, type: BulkOperation['type'], totalItems: number) => void;
  updateProgress: (id: string, processedItems: number) => void;
  completeOperation: (id: string) => void;
  failOperation: (id: string, error: string) => void;
  clearOperation: (id: string) => void;
}

export const useBulkOperationsStore = create<BulkOperationsState>((set, get) => ({
  operations: new Map(),
  activeOperationId: null,

  startOperation: (id, type, totalItems) => set((state) => {
    const operations = new Map(state.operations);
    operations.set(id, {
      id,
      type,
      status: 'running',
      progress: 0,
      totalItems,
      processedItems: 0,
      errors: [],
    });
    return { operations, activeOperationId: id };
  }),

  updateProgress: (id, processedItems) => set((state) => {
    const operations = new Map(state.operations);
    const op = operations.get(id);
    if (op) {
      operations.set(id, {
        ...op,
        processedItems,
        progress: Math.round((processedItems / op.totalItems) * 100),
      });
    }
    return { operations };
  }),

  completeOperation: (id) => set((state) => {
    const operations = new Map(state.operations);
    const op = operations.get(id);
    if (op) {
      operations.set(id, { ...op, status: 'completed', progress: 100 });
    }
    return {
      operations,
      activeOperationId: state.activeOperationId === id ? null : state.activeOperationId
    };
  }),

  failOperation: (id, error) => set((state) => {
    const operations = new Map(state.operations);
    const op = operations.get(id);
    if (op) {
      operations.set(id, {
        ...op,
        status: 'failed',
        errors: [...op.errors, error]
      });
    }
    return { operations };
  }),

  clearOperation: (id) => set((state) => {
    const operations = new Map(state.operations);
    operations.delete(id);
    return { operations };
  }),
}));
```

### Resource Picker State

```typescript
// app/stores/resource-picker-store.ts
import { create } from 'zustand';

interface SelectedResource {
  id: string;
  title: string;
  handle?: string;
  images?: { originalSrc: string }[];
}

interface ResourcePickerState {
  isOpen: boolean;
  resourceType: 'Product' | 'Collection' | 'Customer' | null;
  selectedResources: SelectedResource[];
  maxSelectable: number;

  openPicker: (type: ResourcePickerState['resourceType'], max?: number) => void;
  closePicker: () => void;
  setSelectedResources: (resources: SelectedResource[]) => void;
  clearSelection: () => void;
}

export const useResourcePickerStore = create<ResourcePickerState>((set) => ({
  isOpen: false,
  resourceType: null,
  selectedResources: [],
  maxSelectable: 1,

  openPicker: (type, max = 1) => set({
    isOpen: true,
    resourceType: type,
    maxSelectable: max
  }),

  closePicker: () => set({ isOpen: false }),

  setSelectedResources: (resources) => set({
    selectedResources: resources,
    isOpen: false,
  }),

  clearSelection: () => set({ selectedResources: [] }),
}));
```

## 5. Middleware & DevTools

### DevTools Integration

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export const useStore = create<State>()(
  devtools(
    (set) => ({
      // ... state and actions
    }),
    {
      name: 'ShopifyAppStore',
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);
```

### Immer Middleware (Immutable Updates)

```typescript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface State {
  products: Product[];
  updateProduct: (id: string, updates: Partial<Product>) => void;
}

export const useStore = create<State>()(
  immer((set) => ({
    products: [],
    updateProduct: (id, updates) => set((state) => {
      const product = state.products.find(p => p.id === id);
      if (product) {
        Object.assign(product, updates); // Direct mutation is OK with immer
      }
    }),
  }))
);
```

### Combined Middleware

```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

export const useStore = create<State>()(
  devtools(
    persist(
      immer((set) => ({
        // ... state and actions
      })),
      { name: 'app-store' }
    ),
    { name: 'ShopifyAppStore' }
  )
);
```

## 6. Testing Zustand Stores

```typescript
// app/stores/__tests__/app-store.test.ts
import { act, renderHook } from '@testing-library/react';
import { useAppStore } from '../app-store';

describe('useAppStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useAppStore.setState({
      isLoading: false,
      selectedProductIds: [],
    });
  });

  it('should select a product', () => {
    const { result } = renderHook(() => useAppStore());

    act(() => {
      result.current.selectProduct('gid://shopify/Product/123');
    });

    expect(result.current.selectedProductIds).toContain('gid://shopify/Product/123');
  });

  it('should clear selection', () => {
    useAppStore.setState({ selectedProductIds: ['1', '2', '3'] });

    const { result } = renderHook(() => useAppStore());

    act(() => {
      result.current.clearSelection();
    });

    expect(result.current.selectedProductIds).toHaveLength(0);
  });
});
```

## Anti-Patterns to Avoid

### DON'T: Store server data in Zustand

```typescript
// BAD - Server data should come from loaders
const useStore = create((set) => ({
  products: [], // Server data
  fetchProducts: async () => {
    const res = await fetch('/api/products');
    set({ products: await res.json() });
  },
}));

// GOOD - Use Remix loaders for server data
// Use Zustand only for UI state
export async function loader() {
  return json({ products: await getProducts() });
}
```

### DON'T: Create stores inside components

```typescript
// BAD - Creates new store on every render
function MyComponent() {
  const useLocalStore = create((set) => ({ count: 0 }));
  // ...
}

// GOOD - Define stores outside components
const useLocalStore = create((set) => ({ count: 0 }));

function MyComponent() {
  const count = useLocalStore((s) => s.count);
  // ...
}
```

### DON'T: Select entire state object

```typescript
// BAD - Re-renders on ANY state change
const state = useStore();

// GOOD - Select only what you need
const count = useStore((s) => s.count);
const { count, increment } = useStore(useShallow((s) => ({
  count: s.count,
  increment: s.increment
})));
```

## Best Practices Summary

1. **Keep stores small and focused** - One store per domain/feature
2. **Use selectors** - Always select minimal state needed
3. **Server data in loaders** - Zustand for UI state only
4. **TypeScript everything** - Full type safety for stores
5. **Test stores in isolation** - Use `setState` for setup
6. **DevTools in development** - Easier debugging
7. **SSR-safe persistence** - Handle hydration properly
