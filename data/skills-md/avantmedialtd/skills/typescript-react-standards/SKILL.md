---
name: typescript-react-standards
description: Opinionated TypeScript and React development standards from Avant Media. Use when scaffolding new components, reviewing code, writing TypeScript interfaces or types, setting up project structure, creating React hooks, or working on any TypeScript/React codebase. Also use when the user asks about best practices, patterns, or conventions for TypeScript or React projects, even if they don't explicitly mention "standards."
---

# TypeScript & React Standards

Opinionated standards for building TypeScript and React applications. These are the patterns we use at Avant Media across client projects and internal products. They prioritize readability, maintainability, and developer experience over cleverness.

## TypeScript Conventions

### Strict mode, always

Every project uses `strict: true` in `tsconfig.json`. No exceptions. This catches entire categories of bugs at compile time. If the types are hard to write, the code is probably too complex.

```json
{
    "compilerOptions": {
        "strict": true,
        "noUncheckedIndexedAccess": true,
        "exactOptionalPropertyTypes": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true
    }
}
```

### Interfaces over types for object shapes

Use `interface` for anything that describes an object shape. Use `type` for unions, intersections, mapped types, and utility types. The distinction matters because interfaces are extensible and produce better error messages.

```typescript
// Object shapes → interface
interface User {
    id: string;
    email: string;
    role: UserRole;
}

// Unions, utilities → type
type UserRole = 'admin' | 'editor' | 'viewer';
type PartialUser = Partial<User>;
```

### Name things for what they are, not what they do

```typescript
// Good
interface CreateUserRequest { ... }
interface UserListResponse { ... }

// Bad
interface IUserData { ... }      // Hungarian notation
interface UserPayload { ... }    // vague
```

No `I` prefix on interfaces. No `T` prefix on types. No `E` prefix on enums. These are Java/C# conventions that add noise without information.

### Enums: use `as const` objects instead

TypeScript enums have well-documented quirks (numeric enums reverse-map, `const enum` has build tool issues). Use `as const` objects — they're type-safe, tree-shakeable, and have no runtime surprises.

```typescript
// Prefer this
const UserRole = {
    Admin: 'admin',
    Editor: 'editor',
    Viewer: 'viewer',
} as const;

type UserRole = (typeof UserRole)[keyof typeof UserRole];

// Over this
enum UserRole {
    Admin = 'admin',
    Editor = 'editor',
    Viewer = 'viewer',
}
```

### Explicit return types on exported functions

Internal helpers can rely on inference. Anything exported gets an explicit return type. This catches accidental API changes and makes the contract clear.

```typescript
// Exported → explicit return type
export function formatCurrency(amount: number, currency: string): string {
    return new Intl.NumberFormat('en-GB', { style: 'currency', currency }).format(amount);
}

// Internal → inference is fine
const double = (n: number) => n * 2;
```

### Avoid `any` — use `unknown` and narrow

`any` disables the type system. `unknown` forces you to narrow before use. If you genuinely don't know the type, use `unknown` and add a type guard.

```typescript
function processInput(input: unknown): string {
    if (typeof input === 'string') return input;
    if (typeof input === 'number') return String(input);
    throw new Error(`Unexpected input type: ${typeof input}`);
}
```

If you're wrapping a third-party library with bad types, isolate the `any` in a thin adapter layer and type the boundary.

### Barrel exports: use sparingly

`index.ts` re-exports are fine for public API surfaces (a component library, a shared package). Don't use them inside application code — they create circular dependency traps and make tree-shaking harder.

```
// Fine: package public API
src/components/index.ts → re-exports Button, Input, Modal

// Avoid: deep application barrel files
src/features/auth/index.ts → re-exports everything in auth
```

## React Conventions

### Functional components only

No class components. No `React.FC` (it implicitly includes `children` in older versions and adds no value). Just typed props and a function.

```typescript
interface ButtonProps {
  label: string;
  variant?: 'primary' | 'secondary';
  onClick: () => void;
}

export function Button({ label, variant = 'primary', onClick }: ButtonProps) {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {label}
    </button>
  );
}
```

### Component file structure

One component per file. The file name matches the component name exactly (PascalCase). Co-locate the component's types, hooks, and styles.

```
Button/
├── Button.tsx          # Component
├── Button.test.tsx     # Tests
├── Button.module.css   # Styles (if CSS modules)
├── useButton.ts        # Component-specific hook (if needed)
└── index.ts            # Re-export (optional)
```

### Hooks

Custom hooks extract reusable logic. Name them `use<Thing>`. They must call at least one React hook internally — otherwise it's just a function, not a hook.

```typescript
// This is a hook — it uses React state
function useToggle(initial = false) {
    const [value, setValue] = useState(initial);
    const toggle = useCallback(() => setValue((v) => !v), []);
    return [value, toggle] as const;
}

// This is NOT a hook — just call it formatDate()
function useDateFormat(date: Date) {
    return date.toLocaleDateString('en-GB');
}
```

### State management hierarchy

Use the simplest tool that works:

1. **Local state** (`useState`) — component-scoped, default choice
2. **Lifted state** — shared between siblings, lift to parent
3. **Context** — app-wide settings (theme, auth, locale), rarely-changing data
4. **External store** (Zustand, TanStack Query) — complex client state or server cache

Don't reach for global state managers for problems that `useState` and prop drilling solve cleanly. "Prop drilling" is only a problem at 4+ levels — and even then, composition (passing components as children) often fixes it better than context.

### Data fetching

Use TanStack Query (React Query) for server state. It handles caching, deduplication, background refetching, and error/loading states. Don't reinvent this with `useEffect` + `useState`.

```typescript
function useUsers() {
    return useQuery({
        queryKey: ['users'],
        queryFn: () => api.get<User[]>('/users'),
        staleTime: 5 * 60 * 1000, // 5 minutes
    });
}
```

For mutations, use `useMutation` with optimistic updates where the UX demands it.

### Error boundaries

Wrap major UI sections in error boundaries. A broken sidebar shouldn't crash the whole page. Use `react-error-boundary` — it's maintained, well-typed, and supports reset.

### Avoid premature abstraction

Don't create a `<GenericTable>` component before you have three concrete tables. Don't write a `useForm` hook before you have three forms. Let the pattern emerge from real usage, then extract.

The rule of three: duplicate first, abstract second.

## Project Structure

For application projects (not libraries), organize by feature, not by type:

```
src/
├── app/                 # Route definitions, layouts
├── features/            # Feature modules
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── types.ts
│   └── dashboard/
│       ├── components/
│       ├── hooks/
│       ├── api/
│       └── types.ts
├── shared/              # Cross-cutting concerns
│   ├── components/      # Generic UI components
│   ├── hooks/           # Generic hooks
│   ├── utils/           # Pure utility functions
│   └── types/           # Shared type definitions
├── lib/                 # Third-party adapters, API client setup
└── config/              # Environment, feature flags
```

The `features/` directory is the heart of the application. Each feature is self-contained. If deleting a feature folder breaks imports outside that folder, you have a coupling problem.

## Testing

See `references/testing-standards.md` for the full testing approach. The short version:

- **Unit tests**: Pure functions, hooks, utilities. Use Vitest.
- **Component tests**: Render, interact, assert on output. Use Testing Library.
- **Integration tests**: API routes, database queries. Test real integrations, not mocks.
- **E2E tests**: Critical user journeys only. Use Playwright.

Test behavior, not implementation. If refactoring the internals breaks your tests but not the user experience, your tests are wrong.

## Code Review Checklist

When reviewing TypeScript/React code, check for:

- Strict TypeScript with no `any` escapes
- Interfaces for object shapes, types for unions
- Explicit return types on exports
- No `React.FC`, no class components
- State at the right level (local first, escalate as needed)
- Error boundaries around major sections
- Feature-based file organization
- Tests that verify behavior, not implementation
