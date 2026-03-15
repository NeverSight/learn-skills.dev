---
name: react-development
description: React 19+ with TypeScript — hooks, custom hooks, state management (useState/useReducer/useContext), React Query/SWR, Tailwind CSS, performance. Use when building React components, apps, or optimizing renders.
license: Complete terms in LICENSE.txt
---

# React Development

Expert guidance for building high-quality React applications with React 19+, modern hooks, TypeScript, and best practices following official React documentation at https://react.dev.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

**Core React Development:**
- Building React components with hooks and TypeScript
- Setting up React applications (Vite, Next.js, CRA)
- Working with React Router for navigation
- Implementing forms and user input handling
- Creating responsive layouts and component architecture

**State Management & Data:**
- Managing state (useState, useReducer, useContext)
- Implementing React Query or SWR for data fetching
- Building custom hooks for reusable stateful logic
- Creating Context providers for global state
- Implementing React 19 Server Components (if using Next.js)

**Component Patterns:**
- Creating reusable UI components with proper composition
- Building forms with React Hook Form and Zod validation
- Implementing modal dialogs and overlays
- Creating custom React hooks (useDebounce, useLocalStorage)
- Designing responsive variants for different screen sizes

**Performance & Quality:**
- Optimizing React app performance
- Implementing memoization (useMemo, useCallback)
- Code splitting and lazy loading
- Writing tests with React Testing Library
- Ensuring accessibility compliance (ARIA, keyboard nav)

## Part 1: React Fundamentals

### Project Structure

**Recommended Structure:**
```
src/
├── components/          # Reusable UI components
│   ├── ui/            # Primitives (Button, Input, Modal)
│   ├── forms/          # Form components
│   └── layout/         # Layout components
├── hooks/              # Custom hooks
├── contexts/            # Context providers
├── pages/              # Page components
├── lib/                # Utilities, API clients
├── types/              # TypeScript types
├── styles/              # Global styles
└── main.jsx            # App entry point
```

### Component Architecture

#### Functional Components (React 19 Standard)

```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
  children: React.ReactNode;
  disabled?: boolean;
  isLoading?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  onClick,
  children,
  disabled = false,
  isLoading = false,
}: ButtonProps) {
  const baseClasses = 'rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variantClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500',
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-900 focus:ring-gray-500',
    danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500',
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-5 py-2.5 text-lg',
  };

  return (
    <button
      disabled={disabled || isLoading}
      onClick={onClick}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
    >
      {isLoading ? 'Loading...' : children}
    </button>
  );
}
```

#### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

function List<T>({ items, renderItem, keyExtractor, emptyMessage = 'No items' }: ListProps<T>) {
  return (
    <ul>
      {items.length === 0 ? (
        <li>{emptyMessage}</li>
      ) : (
        items.map((item, index) => (
          <li key={keyExtractor(item)}>
            {renderItem(item, index)}
          </li>
        ))
      )}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={(user) => `${user.firstName} ${user.lastName}`}
  keyExtractor={(user) => user.id}
/>
```

### Component Patterns

**Composition over Inheritance:**

```typescript
// ✅ GOOD - Component composition
function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="border rounded-lg p-4 shadow-sm">
      {children}
    </div>
  );
}

function CardHeader({ children }: { children: React.ReactNode }) {
  return (
    <div className="font-bold text-lg mb-2 border-b pb-2">
      {children}
    </div>
  );
}

function CardBody({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>;
}

// Usage
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content here</CardBody>
</Card>

// ❌ BAD - Inheritance or complex props
function Card({ renderHeader, renderBody, renderFooter }: { ... }) { ... }
```

**Presentational vs Container Components:**

```typescript
// Presentational - UI only, doesn't fetch data
interface UserCardProps {
  user: User;
  onStatusChange: (status: string) => void;
}

function UserCard({ user, onStatusChange }: UserCardProps) {
  return (
    <div>
      <h3>{user.name}</h3>
      <select value={user.status} onChange={(e) => onStatusChange(e.target.value)}>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>
  );
}

// Container - Fetches data, passes to presentational
function UserContainer() {
  const { data: user, mutate: updateStatus } = useUser(userId);

  return user ? (
    <UserCard user={user} onStatusChange={(status) => updateStatus({ status })} />
  ) : (
    <LoadingSpinner />
  );
}
```

---

## Part 2: Hooks Patterns

### Built-in Hooks Mastery

#### useState - For Local State

```typescript
// Simple state
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <span>{count}</span>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}

// Complex state - use useReducer instead
function Form() {
  type FormState = {
    name: string;
    email: string;
    submitted: boolean;
  };

  const [form, setForm] = useState<FormState>({
    name: '',
    email: '',
    submitted: false,
  });

  const updateField = (field: keyof FormState) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => setForm(f => ({ ...f, [field]: e.target.value }));

  return (
    <form>
      <input value={form.name} onChange={updateField('name')} />
      <input value={form.email} onChange={updateField('email')} />
    </form>
  );
}
```

#### useReducer - For Complex State

```typescript
type Action =
  | { type: 'ADD_TODO'; payload: string }
  | { type: 'TOGGLE_TODO'; payload: number }
  | { type: 'DELETE_TODO'; payload: number };

type TodoState = {
  items: Array<{ id: number; text: string; completed: boolean }>;
};

function todosReducer(state: TodoState, action: Action): TodoState {
  switch (action.type) {
    case 'ADD_TODO':
      return {
        items: [
          ...state.items,
          { id: Date.now(), text: action.payload, completed: false },
        ],
      };
    case 'TOGGLE_TODO':
      return {
        items: state.items.map((item) =>
          item.id === action.payload ? { ...item, completed: !item.completed } : item
        ),
      };
    case 'DELETE_TODO':
      return {
        items: state.items.filter((item) => item.id !== action.payload),
      };
    default:
      return state;
  }
}

function TodoApp() {
  const [state, dispatch] = useReducer(todosReducer, { items: [] });

  return (
    <div>
      <ToDoList items={state.items} onToggle={(id) => dispatch({ type: 'TOGGLE_TODO', payload: id })} />
    </div>
  );
}
```

#### useEffect - For Side Effects

```typescript
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  // ✅ GOOD - Run on mount and when userId changes
  useEffect(() => {
    let cancelled = false;

    async function fetchUser() {
      const userData = await api.getUser(userId);
      if (!cancelled) {
        setUser(userData);
      }
    }

    fetchUser();

    return () => {
      cancelled = true; // Cleanup to prevent state updates after unmount
    };
  }, [userId]);

  // ✅ GOOD - Document title update
  useEffect(() => {
    if (user) {
      document.title = `${user.name} - Profile`;
    }
    return () => {
      document.title = 'App';
    };
  }, [user]);

  if (!user) return <LoadingSkeleton />;

  return (
    <div>
      <h1>{user.name}</h1>
      {/* ... */}
    </div>
  );
}
```

#### useContext - For Global State

```typescript
// Context creation
type ThemeContextType = {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextType | null>(null);

// Provider component
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => setTheme(t => t === 'light' ? 'dark' : 'light');

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Custom hook for using context
export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Usage in component
function ThemedButton() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className={theme === 'dark' ? 'bg-gray-800 text-white' : 'bg-white text-black'}
    >
      Toggle {theme} theme
    </button>
  );
}
```

### Performance Hooks

#### useMemo - Memoize Expensive Computations

```typescript
function ProductList({ products }: { products: Product[] }) {
  // ✅ GOOD - Memoize expensive calculation
  const sortedProducts = useMemo(() => {
    return [...products].sort((a, b) => a.price - b.price);
  }, [products]);

  const expensiveAnalysis = useMemo(() => {
    // Only recompute when prices change
    const avgPrice = products.reduce((sum, p) => sum + p.price, 0) / products.length;
    const maxPrice = Math.max(...products.map(p => p.price));
    return { avgPrice, maxPrice };
  }, [products]);

  return (
    <div>
      <StatsCard data={expensiveAnalysis} />
      <ProductCards products={sortedProducts} />
    </div>
  );
}
```

#### useCallback - Memoize Functions

```typescript
function ParentComponent() {
  const [items, setItems] = useState<Item[]>([]);

  // ✅ GOOD - Memoize callback to prevent child re-renders
  const handleItemAdd = useCallback((item: Item) => {
    setItems(prev => [...prev, item]);
  }, []);

  const handleItemRemove = useCallback((id: string) => {
    setItems(prev => prev.filter(item => item.id !== id));
  }, []);

  return (
    <div>
      <AddItemForm onAdd={handleItemAdd} />
      <ItemList items={items} onRemove={handleItemRemove} />
    </div>
  );
}

// Child component wrapped in React.memo
const ItemList = React.memo(function ItemList({
  items,
  onRemove,
}: {
  items: Item[];
  onRemove: (id: string) => void;
}) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>
          {item.name}
          <button onClick={() => onRemove(item.id)}>Remove</button>
        </li>
      ))}
    </ul>
  );
});
```

---

## Part 3: Custom Hooks

### useDebounce

Debounce rapid value changes, useful for search inputs:

```typescript
import { useState, useEffect } from 'react';

function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchBar() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    // This only runs 300ms after user stops typing
    if (debouncedQuery) {
      performSearch(debouncedQuery);
    }
  }, [debouncedQuery]);

  return (
    <input
      type="text"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

### useLocalStorage

Persist state to localStorage:

```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  };

  return [storedValue, setValue] as const;
}

// Usage
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Current theme: {theme}
    </button>
  );
}
```

### useToggle

Toggle boolean state with useful utilities:

```typescript
function useToggle(initialValue: boolean = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue(v => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse, setValue } as const;
}

// Usage
function ModalExample() {
  const { value: isOpen, toggle, setFalse: close } = useToggle(false);

  return (
    <>
      <button onClick={toggle}>Open Modal</button>
      <Modal isOpen={isOpen} onClose={close}>
        <p>Modal content</p>
      </Modal>
    </>
  );
}
```

### useFetch

Data fetching with loading and error states:

```typescript
type UseFetchResult<T> = {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
};

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      const jsonData = await response.json();
      setData(jsonData);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, loading, error } = useFetch<User>(`/api/users/${userId}`);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error.message} />;

  return (
    <div>
      <h1>{user?.name}</h1>
      <p>{user?.email}</p>
    </div>
  );
}
```

---

## Part 4: Forms & Validation

### React Hook Form with Zod

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Zod schema for validation
const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  age: z.number().min(18, 'Must be at least 18'),
  subscribe: z.boolean().default(false),
});

type FormData = z.infer<typeof formSchema>;

function UserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = async (data: FormData) => {
    try {
      await api.createUser(data);
      alert('User created successfully!');
    } catch (error) {
      alert('Error creating user');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="mb-4">
        <label>Name</label>
        <input {...register('name')} />
        {errors.name && <span className="error">{errors.name.message}</span>}
      </div>

      <div className="mb-4">
        <label>Email</label>
        <input type="email" {...register('email')} />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </div>

      <div className="mb-4">
        <label>Age</label>
        <input type="number" {...register('age', { valueAsNumber: true })} />
        {errors.age && <span className="error">{errors.age.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

### Form Components

```typescript
interface FormFieldProps {
  label: string;
  error?: string;
  children: React.ReactNode;
}

function FormField({ label, error, children }: FormFieldProps) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium mb-1">{label}</label>
      {children}
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
}

// Usage
<FormField label="Email" error={errors.email?.message}>
  <input
    type="email"
    {...register('email')}
    className="w-full px-3 py-2 border rounded"
  />
</FormField>
```

---

## Part 5: Tailwind CSS Integration

### Utility Classes for React Components

```typescript
// Button component with variants
const buttonVariants = {
  primary: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500',
  secondary: 'bg-gray-200 hover:bg-gray-300 focus:ring-gray-500',
  danger: 'bg-red-600 hover:bg-red-700 focus:ring-red-500',
  ghost: 'bg-transparent hover:bg-gray-100 focus:ring-gray-500',
};

const buttonSizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-5 py-2.5 text-lg',
};

export function Button({
  variant = 'primary',
  size = 'md',
  className = '',
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-lg font-medium transition-colors focus:outline-none focus:ring-2',
        buttonVariants[variant],
        buttonSizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

### Responsive Variants

```typescript
interface CardProps {
  isFeatured?: boolean;
  children: React.ReactNode;
}

export function Card({ isFeatured = false, children }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-lg shadow-md p-6 transition-all',
        'bg-white hover:shadow-lg',
        // Responsive padding
        'sm:p-4 md:p-6 lg:p-8',
        // Featured highlight
        isFeatured && 'ring-2 ring-blue-500 border-2 border-blue-500'
      )}
    >
      {children}
    </div>
  );
}
```

---

## Part 6: State Management Patterns

### Context API for Global State

```typescript
// AppContext.tsx
interface AppState {
  user: User | null;
  loading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

const AppContext = createContext<AppState | null>(null);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);

  const login = async (credentials: LoginCredentials) => {
    setLoading(true);
    try {
      const userData = await api.login(credentials);
      setUser(userData);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    api.logout();
    setUser(null);
  };

  return (
    <AppContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) throw new Error('useApp must be used within AppProvider');
  return context;
}
```

### Using React Query (TanStack Query)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetch data
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => api.getUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error.message} />;

  return (
    <div>
      <h1>{user?.name}</h1>
      <p>{user?.email}</p>
    </div>
  );
}

// Mutate data
function UpdateUserForm({ user: initialUser }: { user: User }) {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: api.updateUser,
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['user', initialUser.id] });
    },
  });

  const handleSubmit = (data: Partial<User>) => {
    mutation.mutate({ ...initialUser, ...data });
  };

  return (
    <form onSubmit={(e) => { e.preventDefault(); handleSubmit(/* data */); }}>
      {/* Form fields */}
    </form>
  );
}
```

---

## Part 7: Performance Optimization

### Code Splitting with React.lazy

```typescript
import { lazy, Suspense } from 'react';

// Lazy load components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Reports = lazy(() => import('./pages/Reports'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Virtual Scrolling

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated item height
    overscan: 5, // Render extra items beyond viewport
  });

  return (
    <div ref={parentRef} className="h-96 overflow-auto">
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => {
          const item = items[virtualItem.index];
          return (
            <div
              key={virtualItem.key}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualItem.size}px`,
                transform: `translateY(${virtualItem.start}px)`,
              }}
            >
              {/*
...existing code...
*/}
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

---

## Part 8: Testing with React Testing Library

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { expect } from 'vitest';
import userEvent from '@testing-library/user-event';

describe('Button Component', () => {
  it('renders children correctly', () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('calls onClick handler when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(<Button onClick={handleClick}>Click Me</Button>);

    await user.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Cannot Click</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});

describe('UseFetch Hook', () => {
  it('fetches data and returns it', async () => {
    const { result } = renderHook(() => useFetch('/api/test'));

    await waitFor(() => {
      expect(result.current.data).toBeDefined();
      expect(result.current.loading).toBe(false);
    });
  });
});
```

---

## React Development Best Practices

### Components
- [ ] Use functional components with hooks
- [ ] Keep components small and focused
- [ ] Use TypeScript for type safety
- [ ] Implement proper error boundaries
- [ ] Add loading and error states

### Hooks
- [ ] Follow rules of hooks (only call at top level)
- [ ] Use custom hooks for reusable stateful logic
- [ ] Memoize expensive computations and callbacks
- [ ] Clean up side effects properly

### Performance
- [ ] Implement code splitting for large bundles
- [ ] Use virtual scrolling for long lists
- [ ] Debounce/throttle user input
- [ ] Lazy load images and resources

### Accessibility
- [ ] Use semantic HTML elements
- [ ] Ensure keyboard navigation works
- [ ] Add ARIA labels where needed
- [ ] Support screen readers properly
- [ ] Test with accessibility tools

---

## References & Resources

### Documentation
- [Hooks Reference](./references/hooks-reference.md) — All 17 React hooks including React 19 new hooks (use, useFormStatus, useOptimistic)
- [Patterns Catalog](./references/patterns-catalog.md) — 12 React component patterns with TypeScript examples

### Scripts
- [Component Generator](./scripts/component-generator.ps1) — PowerShell component scaffolder with types: functional, page, layout, context

### Examples
- [Custom Hooks Gallery](./examples/custom-hooks-gallery.md) — 12 production-ready custom hooks with full implementations and tests

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [frontend-design](../frontend-design/SKILL.md) | UI/UX design principles for React apps |
| [vite-development](../vite-development/SKILL.md) | Build tooling for React projects |
| [javascript-development](../javascript-development/SKILL.md) | Core JS patterns underlying React |
| [stitch-design](../stitch-design/SKILL.md) | Convert Stitch screens to React components |
| [web-testing](../web-testing/SKILL.md) | Test React apps with Playwright |
