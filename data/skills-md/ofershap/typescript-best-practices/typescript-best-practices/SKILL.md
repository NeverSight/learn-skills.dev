---
name: typescript-best-practices
description:
  Modern TypeScript patterns your AI agent should use. Strict mode, discriminated unions, satisfies
  operator, const assertions, and type-safe patterns for TypeScript 5.x.
metadata:
  tags: typescript, type-safety, best-practices
---

## When to use

Use this skill when working with TypeScript code. AI agents frequently generate outdated patterns -
using `any` instead of `unknown`, type assertions instead of `satisfies`, optional fields instead of
discriminated unions, and missing strict mode options. This skill enforces modern TypeScript 5.x
patterns.

## Critical Rules

### 1. Enable Strict Mode with All Checks

**Wrong (agents do this):**

```json
{
  "compilerOptions": {
    "strict": false,
    "target": "ES2020"
  }
}
```

**Correct:**

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "target": "ES2022"
  }
}
```

**Why:** Strict mode catches entire categories of bugs. `noUncheckedIndexedAccess` prevents unsafe
array/object access. Agents often skip these for "convenience."

### 2. Use satisfies Instead of Type Assertions

**Wrong (agents do this):**

```typescript
const config = {
  port: 3000,
  host: "localhost",
} as Config;

config.port.toFixed(); // No error even if port could be string
```

**Correct:**

```typescript
const config = {
  port: 3000,
  host: "localhost",
} satisfies Config;

config.port.toFixed(); // TypeScript knows port is number
```

**Why:** `satisfies` validates the type without widening it. `as` silences the compiler and can hide
bugs. Use `satisfies` for validation, `as` only when you genuinely know more than the compiler.

### 3. Use Discriminated Unions Over Optional Fields

**Wrong (agents do this):**

```typescript
interface ApiResponse {
  data?: User;
  error?: string;
  loading?: boolean;
}
```

**Correct:**

```typescript
type ApiResponse =
  | { status: "loading" }
  | { status: "success"; data: User }
  | { status: "error"; error: string };
```

**Why:** Optional fields allow impossible states (data AND error both present). Discriminated unions
make each state explicit and exhaustively checkable.

### 4. Use const Assertions for Literal Types

**Wrong (agents do this):**

```typescript
const ROUTES = {
  home: "/",
  about: "/about",
  contact: "/contact",
};
// Type: { home: string; about: string; contact: string }
```

**Correct:**

```typescript
const ROUTES = {
  home: "/",
  about: "/about",
  contact: "/contact",
} as const;
// Type: { readonly home: "/"; readonly about: "/about"; readonly contact: "/contact" }
```

**Why:** Without `as const`, TypeScript widens literal types to `string`. With it, you get exact
literal types and readonly properties.

### 5. Use unknown Instead of any

**Wrong (agents do this):**

```typescript
function parseJson(text: string): any {
  return JSON.parse(text);
}

const data = parseJson('{"name": "test"}');
data.nonExistent.method(); // No error - runtime crash
```

**Correct:**

```typescript
function parseJson(text: string): unknown {
  return JSON.parse(text);
}

const data = parseJson('{"name": "test"}');
if (isUser(data)) {
  data.name; // Safe - type narrowed
}
```

**Why:** `any` disables all type checking. `unknown` forces you to narrow the type before using it,
catching bugs at compile time.

### 6. Use Template Literal Types for String Patterns

**Wrong (agents do this):**

```typescript
function getLocaleMessage(id: string): string { ... }
```

**Correct:**

```typescript
type Locale = 'en' | 'ja' | 'pt';
type MessageKey = 'welcome' | 'goodbye';
type LocaleMessageId = `${Locale}_${MessageKey}`;

function getLocaleMessage(id: LocaleMessageId): string { ... }
```

**Why:** Template literal types create precise string patterns from unions. The compiler catches
typos and invalid combinations at build time.

### 7. Use NoInfer to Prevent Unwanted Inference

**Wrong (agents do this):**

```typescript
function createLight<C extends string>(colors: C[], defaultColor?: C) { ... }
createLight(['red', 'green', 'blue'], 'purple'); // No error - purple widens C
```

**Correct:**

```typescript
function createLight<C extends string>(colors: C[], defaultColor?: NoInfer<C>) { ... }
createLight(['red', 'green', 'blue'], 'purple'); // Error - 'purple' not in C
```

**Why:** `NoInfer<T>` (TypeScript 5.4+) prevents a parameter from influencing type inference,
ensuring stricter checks.

### 8. Use Branded Types for Type-Safe IDs

**Wrong (agents do this):**

```typescript
function getUser(id: string): User { ... }
function getOrder(id: string): Order { ... }

const userId = getUserId();
getOrder(userId); // No error - but wrong!
```

**Correct:**

```typescript
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };

function getUser(id: UserId): User { ... }
function getOrder(id: OrderId): Order { ... }

const userId = getUserId();
getOrder(userId); // Error - UserId is not OrderId
```

**Why:** Branded types prevent accidentally passing one ID type where another is expected. The brand
exists only at compile time - zero runtime cost.

### 9. Use Exhaustive Switch with never

**Wrong (agents do this):**

```typescript
function handleStatus(status: "active" | "inactive" | "pending") {
  switch (status) {
    case "active":
      return "Active";
    case "inactive":
      return "Inactive";
    // 'pending' silently falls through
  }
}
```

**Correct:**

```typescript
function handleStatus(status: "active" | "inactive" | "pending") {
  switch (status) {
    case "active":
      return "Active";
    case "inactive":
      return "Inactive";
    case "pending":
      return "Pending";
    default: {
      const _exhaustive: never = status;
      throw new Error(`Unhandled status: ${_exhaustive}`);
    }
  }
}
```

**Why:** The `never` check ensures every union member is handled. When a new status is added, the
compiler flags the missing case.

### 10. Use Type Predicates Over Type Assertions

**Wrong (agents do this):**

```typescript
function processItem(item: unknown) {
  const user = item as User;
  console.log(user.name);
}
```

**Correct:**

```typescript
function isUser(item: unknown): item is User {
  return typeof item === "object" && item !== null && "name" in item && "email" in item;
}

function processItem(item: unknown) {
  if (isUser(item)) {
    console.log(item.name); // Safe - narrowed to User
  }
}
```

**Why:** Type predicates (`item is User`) narrow types safely with runtime checks. Type assertions
(`as User`) bypass the compiler and can hide bugs.

### 11. Use import type for Type-Only Imports

**Wrong (agents do this):**

```typescript
import { User, UserService } from "./user";
// User is only used as a type, but gets included in the bundle
```

**Correct:**

```typescript
import type { User } from "./user";
import { UserService } from "./user";
```

**Why:** `import type` is erased at compile time, reducing bundle size. It also makes the intent
clear - this import is for types only.

### 12. Use Record Over Index Signatures

**Wrong (agents do this):**

```typescript
interface Config {
  [key: string]: string;
}
```

**Correct:**

```typescript
type Config = Record<string, string>;

// Or better - use a specific union for keys:
type Config = Record<"host" | "port" | "env", string>;
```

**Why:** `Record<K, V>` is more readable and composable than index signatures. When possible, use a
union for keys to get exhaustive checking.

### 13. Use using for Resource Management

**Wrong (agents do this):**

```typescript
const file = openFile("data.txt");
try {
  processFile(file);
} finally {
  file.close();
}
```

**Correct:**

```typescript
using file = openFile("data.txt");
processFile(file);
// file.close() called automatically via Symbol.dispose
```

**Why:** The `using` keyword (TypeScript 5.2+) provides deterministic resource cleanup via the
Disposable protocol, similar to Python's `with` or C#'s `using`.

## Patterns

- Enable `strict: true` and `noUncheckedIndexedAccess: true` in every project
- Use `satisfies` for type validation without widening
- Use discriminated unions with a `type` or `kind` field for state modeling
- Use `as const` for configuration objects and route maps
- Use branded types for domain-specific IDs
- Use `import type` for all type-only imports
- Use exhaustive `switch` with `never` default for union handling

## Anti-Patterns

- NEVER use `any` - use `unknown` and narrow with type guards
- NEVER use `as` for type assertions unless you genuinely know more than the compiler
- NEVER use optional fields to model mutually exclusive states - use discriminated unions
- NEVER use `// @ts-ignore` or `// @ts-expect-error` without a comment explaining why
- NEVER use `enum` - use `as const` objects or union types instead
- NEVER use `Function` type - use specific function signatures
- NEVER disable strict mode for convenience
