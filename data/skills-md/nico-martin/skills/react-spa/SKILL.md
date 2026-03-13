---
name: react-spa
description: Build React Single Page Applications with TypeScript, Vite, Tailwind CSS v4+, and lucide-react. Follows a structured architecture with theme components, utilities, and strict TypeScript patterns. Optimized for small demo applications with best practices for performance, code organization, and maintainability.
license: Apache-2.0
metadata:
  category: frontend-framework
  tags: [react, typescript, vite, tailwindcss, spa]
compatibility: Requires Node.js 18+ for Vite. Uses Tailwind CSS v4+ with CSS-first configuration. Modern browser support (ES2020+).
---

# React SPA Development Pattern

This skill provides guidelines for developing React Single Page Applications following a specific architecture pattern, primarily used for small demo applications.

## When to Use This Skill

Use this skill when:
- Building a new React SPA from scratch
- Working on an existing React SPA project
- The user mentions they want a React app following their standard pattern

## Project Setup

When scaffolding a new React SPA project, refer to **[PROJECT_SETUP.md](./PROJECT_SETUP.md)** for:
- Gathering project information (name, description, version)
- Complete dependency list with latest versions
- Full project structure
- All configuration files (vite, TypeScript, ESLint, Prettier, git)
- Initial source files

## Project Structure

```
src/
├── components/           # App-specific components with logic
├── theme/
│   └── index.ts         # Central export for all theme components
├── utils/
│   └── classnames.ts    # CN utility for conditional classes
├── App.tsx              # Root component
├── index.css            # Tailwind v4 theme + animations
├── main.tsx             # React entry point
└── vite-env.d.ts        # Vite type declarations
```

## Component Organization

### Components (`src/components/`)

App-specific components with business logic:
- Contains components tied to the application's functionality
- Should be grouped in folders where it makes sense (e.g., `components/auth/`, `components/dashboard/`)
- One default export per component file
- Can use state, side effects, and complex logic

**Example structure:**
```
components/
├── auth/
│   ├── LoginForm.tsx
│   └── RegisterForm.tsx
├── dashboard/
│   └── MetricCard.tsx
└── LanguageSelector.tsx
```

### Theme Components (`src/theme/`)

Reusable UI components with minimal logic:
- Generic, reusable UI elements (buttons, inputs, cards, etc.)
- Rarely contain business logic (but can if needed)
- **Must always be imported/exported through `src/theme/index.ts`**
- Organized in subfolders by component type

**Example theme component:**

```tsx
// src/theme/button/Button.tsx
import type { ButtonHTMLAttributes } from "react";
import cn from "../../utils/classnames";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
  className?: string;
}

export default function Button({
  variant = "primary",
  className = "",
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        "px-4 py-2 rounded",
        {
          "bg-blue-500 text-white": variant === "primary",
          "bg-gray-200 text-black": variant === "secondary",
        },
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

**Central theme export:**

```ts
// src/theme/index.ts

export { default as Button } from "./button/Button";
export { default as InputText } from "./form/InputText";
```

**Usage in components:**

```tsx
import { Button, InputText } from "./theme";

export default function MyComponent() {
  return (
    <div>
      <InputText placeholder="Enter name" />
      <Button variant="primary">Submit</Button>
    </div>
  );
}
```

### Utilities (`src/utils/`)

Utility files export multiple helper functions:
- Pure functions without side effects
- Group related utilities in the same file
- Use named exports for utilities

**Examples:**
- `utils/classnames.ts` - CN utility for conditional classes (required)
- `utils/format.ts` - `formatDate()`, `formatNumber()`, `formatCurrency()`
- `utils/validation.ts` - `isEmail()`, `isValidUrl()`, `validateForm()`

## React Component Pattern

Standard structure for all React components:

```tsx
import { useState } from "react";
import cn from "./utils/classnames";
import { Button } from "./theme";

interface MyComponentProps {
  title: string;
  count?: number;
  className?: string;
  onSubmit?: (value: string) => void;
}

export default function MyComponent({
  title,
  count = 0,
  className = "",
  onSubmit,
}: MyComponentProps) {
  const [value, setValue] = useState<string>("");

  const handleSubmit = () => {
    if (onSubmit) {
      onSubmit(value);
    }
  };

  return (
    <div className={cn("container", className)}>
      <h2>{title}</h2>
      <p>Count: {count}</p>
      <Button onClick={handleSubmit}>Submit</Button>
    </div>
  );
}
```

**Key patterns:**
- One default export per component
- TypeScript interface for props (suffix with `Props`)
- Always include `className?: string` in props for styling flexibility
- Destructure props with default values in function signature
- Use `cn()` utility for combining classnames
- Import theme components from `"./theme"`
- Early returns for conditional rendering

## TypeScript Guidelines

### Type Safety Rules

- **Strict mode enabled** - Use strict compiler options
- **Explicit types** - Define interfaces for all component props and function parameters
- **No `any`** - Use proper types or `unknown` with type guards
- **Type imports** - Import types separately: `import type { MyType } from './types'`
- **Const assertions** - Use `as const` for literal types instead of enums
- **Interface over type** - Prefer `interface` for object shapes

### Common Patterns

**IMPORTANT:** Never use `React.` prefix for types. Always import types directly from React.

```tsx
import type { 
  ButtonHTMLAttributes, 
  InputHTMLAttributes,
  MouseEvent,
  ReactNode 
} from "react";

// ✓ Correct: Import types and extend without React. prefix
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
}

// ✗ Wrong: Don't use React. prefix
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
}

// ✓ Event handlers
const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
  // ...
};

// ✓ Refs
const inputRef = useRef<HTMLInputElement>(null);

// ✓ Children prop
interface ContainerProps {
  children: ReactNode;
}

// ✓ Generic components
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => ReactNode;
}
```

## React Patterns

### Component Guidelines

- **Functional components only** - No class components
- **React hooks** - Use `useState`, `useEffect`, `useRef`, `useMemo`, `useCallback`
- **Props destructuring** - Destructure props in function signature with defaults
- **Default exports** - Components use default export, utilities use named exports
- **Single responsibility** - Keep components focused on one task
- **Composition over inheritance** - Build complex UIs from simple components

### State Management

- **Local state first** - Use `useState` for component-specific state
- **Props drilling** - Pass state down explicitly, avoid global state unless needed
- **Lift state up** - Move state to common ancestor when multiple components need it
- **Form libraries** - Use `react-hook-form` for complex forms
- **URL state** - Use URL hash/query params for shareable state

### Common Hooks Patterns

```tsx
// State with derived values
const [items, setItems] = useState<Item[]>([]);
const activeItems = items.filter((item) => item.active);

// Effect with cleanup
useEffect(() => {
  const subscription = api.subscribe();
  return () => subscription.unsubscribe();
}, []);

// Memoized expensive computation
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// Memoized callback
const handleClick = useCallback(() => {
  console.log(value);
}, [value]);

// Refs for DOM access
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => {
  inputRef.current?.focus();
}, []);
```

## File Naming Conventions

- **Components**: PascalCase (e.g., `LanguageSelector.tsx`, `MetricCard.tsx`)
- **Utilities**: camelCase (e.g., `classnames.ts`, `format.ts`, `validation.ts`)
- **Types**: `types.ts` or `index.ts` in dedicated folders
- **Constants**: `constants.ts` with SCREAMING_SNAKE_CASE exports

**Examples:**
```
src/
├── components/
│   ├── UserProfile.tsx          ✓ PascalCase
│   └── DashboardMetrics.tsx     ✓ PascalCase
├── theme/
│   └── button/
│       └── Button.tsx           ✓ PascalCase
├── utils/
│   ├── classnames.ts            ✓ camelCase
│   ├── format.ts                ✓ camelCase
│   └── validation.ts            ✓ camelCase
└── constants.ts                 ✓ camelCase
```

## Code Style

### General Formatting

- **Prettier formatting** - Auto-format on save, follow `.prettierrc` rules
- **ESLint** - Use TypeScript + React hooks + React Refresh plugins
- **Functional programming** - Prefer immutable operations, `map`/`filter` over loops
- **Early returns** - Use guard clauses to reduce nesting
- **Descriptive names** - Clear variable/function names over comments

### Import Order

Imports are automatically sorted using `@trivago/prettier-plugin-sort-imports`:

**Configuration in `.prettierrc`:**
```json
{
  "importOrder": ["<THIRD_PARTY_MODULES>", "^[./]"],
  "plugins": ["@trivago/prettier-plugin-sort-imports"]
}
```

**Result: Two groups separated by blank line:**

```tsx
// Group 1: Third-party modules (alphabetically sorted)
import { useState, useEffect } from "react";
import type { ButtonHTMLAttributes, ReactNode } from "react";
import { User, Settings } from "lucide-react";

// Group 2: Local imports (alphabetically sorted)
import { Button, InputText } from "./theme";
import UserCard from "./components/UserCard";
import type { UserData } from "./types";
import cn from "./utils/classnames";
import { formatDate } from "./utils/format";
```

**Do not manually organize imports** - let Prettier handle it automatically.

### Conditional Rendering

```tsx
// Early return for loading/error states
if (isLoading) return <LoadingSpinner />;
if (error) return <ErrorMessage error={error} />;

// Ternary for simple conditions
{isActive ? <ActiveIcon /> : <InactiveIcon />}

// Logical AND for conditional display
{showTitle && <h1>{title}</h1>}

// Complex conditions - extract to variable
const canSubmit = isValid && !isSubmitting && hasChanges;
return <Button disabled={!canSubmit}>Submit</Button>;
```

## Tailwind CSS Usage

### CSS-First Configuration (v4+)

All Tailwind configuration uses the new CSS-first approach in `src/index.css`:

```css
@import "tailwindcss";

@theme {
  /* Custom theme variables */
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  
  /* Custom breakpoints, spacing, etc. */
}
```

### Utility Classes

```tsx
// Use cn() for conditional classes
<div className={cn(
  "px-4 py-2 rounded",
  { "bg-blue-500": isPrimary },
  { "bg-gray-200": !isPrimary },
  className
)} />

// Responsive design
<div className="text-sm md:text-base lg:text-lg" />

// State variants
<button className="hover:bg-blue-600 focus:ring-2 active:scale-95" />
```

## Performance Patterns

### Optimization Strategies

- **Singleton pattern** - For expensive resources (API clients, model instances)
- **Lazy loading** - Load heavy resources only when needed
- **Debouncing** - For expensive operations (API calls, heavy computations)
- **Memoization** - Use `useMemo`/`useCallback` for expensive renders
- **Code splitting** - Use dynamic imports for large features

### Examples

```tsx
// Lazy loading components
const HeavyComponent = lazy(() => import("./HeavyComponent"));

<Suspense fallback={<Loading />}>
  <HeavyComponent />
</Suspense>

// Debouncing input
const [search, setSearch] = useState("");
const debouncedSearch = useMemo(
  () => debounce((value: string) => performSearch(value), 300),
  []
);

// Memoize expensive calculations
const filteredData = useMemo(
  () => data.filter((item) => item.category === category),
  [data, category]
);
```

## Best Practices

### Component Design

1. **Keep components small** - Aim for <200 lines per component
2. **Extract reusable logic** - Custom hooks for shared behavior
3. **Props over configuration** - Make components flexible through props
4. **Accessibility** - Use semantic HTML and ARIA attributes
5. **Error boundaries** - Wrap components that might fail

### Code Organization

1. **Group related files** - Keep related components together
2. **Consistent naming** - Follow naming conventions strictly
3. **Avoid deep nesting** - Flatten component hierarchies
4. **Clear separation** - Keep theme components separate from app logic
5. **Single source of truth** - Don't duplicate state

### Development Workflow

1. **Type first** - Define interfaces before implementation
2. **Test locally** - Use `npm run dev` for rapid iteration
3. **Lint and format** - Run `npm run lint` and `npm run format` before commits
4. **Build verification** - Run `npm run build` to catch build issues

## Tech Stack Summary

### Core Dependencies
- **React** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS v4+** - Styling with CSS-first configuration
- **lucide-react** - Icon components

### Dev Tools
- **@tailwindcss/vite** - Tailwind Vite plugin
- **@vitejs/plugin-react** - Fast Refresh support
- **ESLint** with TypeScript and React plugins
- **Prettier** - Code formatting

## Reference Documentation

- **[PROJECT_SETUP.md](./PROJECT_SETUP.md)** - Complete scaffolding guide with all configuration files
- **[about.md](./about.md)** - Original notes and context

---

This skill enables building maintainable, performant React SPAs with a consistent architecture pattern and best practices.
