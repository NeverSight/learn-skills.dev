---
name: typescript
description: "Strict typing and type-safe development. Trigger: When implementing TypeScript in .ts/.tsx files, adding types, or enforcing safety."
license: "Apache 2.0"
metadata:
  version: "1.0"
  type: language
  dependencies:
    typescript: ">=5.0.0 <6.0.0"
---

# TypeScript

Strict typing with compile-time correctness. Avoid `any`, leverage generics/utility types.

## When to Use

**Use when:**

- Writing or refactoring `.ts`/`.tsx` files
- Adding type definitions, interfaces, or type aliases
- Working with generics, utility types, or advanced type features
- Configuring `tsconfig.json`
- Resolving type errors or improving type inference

**Don't use for:**

- Runtime validation ([form-validation](../form-validation/SKILL.md))
- JS-only patterns (javascript skill)
- Framework typing (react, mui skills)

---

## Critical Patterns

### ❌ NEVER: use `any`

```typescript
// BAD: Disables type checking
function process(data: any) {
  return data.value;
}

// GOOD: unknown with type guards
function process(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    return (data as { value: string }).value;
  }
  throw new Error("Invalid data");
}
```

### ✅ REQUIRED: Enable strict mode

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true
  }
}
```

### ✅ REQUIRED: Use proper types for object shapes

```typescript
// Interface for extensible objects
interface User {
  id: number;
  name: string;
}

// Type alias for unions/intersections
type Status = "pending" | "approved" | "rejected";
type UserWithStatus = User & { status: Status };

// BAD: Empty object (too permissive)
const user: {} = { anything: "allowed" };
```

### ✅ REQUIRED: Constrain generics

```typescript
// GOOD: Constrained generic
function getProperty<T extends object, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// BAD: Unconstrained
function getProperty<T>(obj: T, key: string): any {
  return obj[key];
}
```

### ✅ REQUIRED: Use `import type` for type-only imports

```typescript
// GOOD: Separate type imports
import type { User, Product } from "./types";
import { fetchUser } from "./api";

// GOOD: Inline type keyword when mixing values and types
import { Installer, type Model } from "../core/installer";

// BAD: Types as values (emits unnecessary JS)
import { User, Product } from "./types";
```

### ✅ REQUIRED: Named imports over namespace imports

```typescript
// GOOD: Explicit, tree-shakeable
import { readFileSync, existsSync } from "fs";
import { join, resolve } from "path";

// BAD: Namespace import when using few exports
import * as fs from "fs";
import * as path from "path";

// EXCEPTION: OK when using 6+ exports from one module
import * as p from "@clack/prompts";
```

### ✅ REQUIRED: No unused code

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}

// BAD: Unused import and variable
import { something } from "./lib"; // never used
const unused = 42;

// GOOD: Prefix intentionally unused params with _
function handler(_event: Event, data: string) {
  return data;
}
```

### ✅ REQUIRED: Use `satisfies` for type validation without widening

```typescript
const config = {
  endpoint: "/api/users",
  timeout: 5000,
} satisfies Config;
// Inferred type + validated against Config
```

### ✅ REQUIRED: Use `as const` for literal types

```typescript
const ROUTES = {
  HOME: "/",
  ABOUT: "/about",
} as const;

type Route = (typeof ROUTES)[keyof typeof ROUTES]; // '/' | '/about'
```

---

## Decision Tree

- **Runtime validation needed?** -> Use [form-validation](../form-validation/SKILL.md) (Zod/Yup). TypeScript is compile-time only.
- **Transforming types?** -> See [references/utility-types.md](references/utility-types.md) for Partial, Pick, Omit, Record, and 20+ more.
- **Unknown data?** -> Use `unknown`, never `any`. See [references/type-guards.md](references/type-guards.md).
- **Missing third-party types?** -> Install `@types/*` or declare custom types in `types/`.
- **Importing types only?** -> Use `import type { ... }` or inline `type` keyword.
- **Using <6 exports from a module?** -> Named imports: `import { x, y } from 'mod'`.
- **Unused import/variable?** -> Delete it. Enable `noUnusedLocals`/`noUnusedParameters` in tsconfig.
- **Complex object shape?** -> `interface` for extensibility, `type` for unions/intersections/computed.
- **Reusable logic across types?** -> See [references/generics-advanced.md](references/generics-advanced.md).
- **External API response?** -> Define interface from actual response shape. Use quicktype for generation.
- **New project setup?** -> See [references/config-patterns.md](references/config-patterns.md).
- **Type-safe error handling?** -> See [references/error-handling.md](references/error-handling.md).

---

## Example

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

type UserUpdate = Partial<Pick<User, "name" | "email">>;

function updateUser<T extends User>(user: T, updates: UserUpdate): T {
  return { ...user, ...updates };
}

const result: User = updateUser(
  { id: 1, name: "John", email: "john@example.com" },
  { name: "Jane" },
);
```

---

## Edge Cases

**Discriminated unions for type narrowing:**

```typescript
type Result =
  | { success: true; data: string }
  | { success: false; error: Error };

function handle(result: Result) {
  if (result.success) {
    console.log(result.data); // TypeScript knows data exists
  }
}
```

**Custom type guards:**

```typescript
function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null && "id" in value;
}
```

- **Circular types:** Extract shared interfaces or use type parameters.
- **Index signatures:** `Record<string, Type>` for dynamic keys; mapped types for known keys.
- **Const assertions:** `as const` creates readonly literal types.

---

## Checklist

- [ ] `strict: true` in `tsconfig.json`
- [ ] No `any` usage -- use `unknown` with type guards
- [ ] `import type` for type-only imports (or inline `type` keyword)
- [ ] Named imports over namespace imports (`import { x }` not `import * as`)
- [ ] No unused imports, variables, or parameters (`noUnusedLocals`, `noUnusedParameters`)
- [ ] Interfaces for object shapes, type aliases for unions/intersections
- [ ] Generics constrained with `extends`
- [ ] `satisfies` for validation without type widening
- [ ] `as const` for literal inference

---

## Resources

- [references/](references/README.md) -- utility types, generics, type guards, config patterns, error handling
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig)
