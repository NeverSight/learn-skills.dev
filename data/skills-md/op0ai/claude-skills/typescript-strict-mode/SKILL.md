---
name: typescript-strict-mode
description: "Guide for strict TypeScript practices including avoiding any, using proper type annotations, and leveraging TypeScript's type system effectively. Use when working with TypeScript codebases that enforce strict type checking, when you need guidance on type safety patterns, or when encountering type errors. Activates for TypeScript type errors, strict mode violations, or general TypeScript best practices."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# TypeScript Strict Mode Best Practices

## Overview

This skill covers strict TypeScript practices applicable across all frameworks. It focuses on avoiding `any`, using proper type annotations, and leveraging TypeScript's type system for safer, more maintainable code.

## The Golden Rule: NEVER Use `any`

**CRITICAL RULE:** Many codebases have `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

**Why `any` is dangerous:**

- Defeats the purpose of TypeScript's type system
- Hides bugs that would be caught at compile time
- Propagates type unsafety through the codebase
- Makes refactoring difficult and error-prone

## Alternatives to `any`

### 1. Use Specific Types

**❌ WRONG:**

```typescript
function processData(data: any) { ... }
const items: any[] = [];
```

**✅ CORRECT:**

```typescript
function processData(data: { id: string; name: string }) { ... }
const items: string[] = [];
```

### 2. Use `unknown` When Type is Truly Unknown

`unknown` is the type-safe counterpart to `any`. It forces you to narrow the type before using it.

**❌ WRONG:**

```typescript
function handleResponse(response: any) {
  return response.data.name; // No type checking!
}
```

**✅ CORRECT:**

```typescript
function handleResponse(response: unknown) {
  if (
    typeof response === "object" &&
    response !== null &&
    "data" in response &&
    typeof (response as { data: unknown }).data === "object"
  ) {
    const data = (response as { data: { name: string } }).data;
    return data.name;
  }
  throw new Error("Invalid response format");
}
```

### 3. Use Generics for Reusable Components

**❌ WRONG:**

```typescript
function wrapValue(value: any): { wrapped: any } {
  return { wrapped: value };
}
```

**✅ CORRECT:**

```typescript
function wrapValue<T>(value: T): { wrapped: T } {
  return { wrapped: value };
}

// Usage
const wrappedString = wrapValue("hello"); // { wrapped: string }
const wrappedNumber = wrapValue(42); // { wrapped: number }
```

### 4. Use Union Types for Multiple Possibilities

**❌ WRONG:**

```typescript
function handleInput(input: any) {
  if (typeof input === 'string') { ... }
  if (typeof input === 'number') { ... }
}
```

**✅ CORRECT:**

```typescript
function handleInput(input: string | number) {
  if (typeof input === 'string') { ... }
  if (typeof input === 'number') { ... }
}
```

### 5. Use Type Guards for Runtime Checks

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    "email" in value &&
    typeof (value as User).id === "string" &&
    typeof (value as User).name === "string" &&
    typeof (value as User).email === "string"
  );
}

function processUser(data: unknown) {
  if (isUser(data)) {
    // data is now typed as User
    console.log(data.name);
  }
}
```

### 6. Use `Record<K, V>` for Dynamic Objects

**❌ WRONG:**

```typescript
const cache: any = {};
cache["key"] = "value";
```

**✅ CORRECT:**

```typescript
const cache: Record<string, string> = {};
cache["key"] = "value";

// Or with specific keys
const userSettings: Record<"theme" | "language", string> = {
  theme: "dark",
  language: "en",
};
```

### 7. Use Index Signatures for Flexible Objects

```typescript
interface Config {
  name: string;
  version: string;
  [key: string]: string | number | boolean; // Additional properties
}

const config: Config = {
  name: "my-app",
  version: "1.0.0",
  debug: true,
  port: 3000,
};
```

## Common Event Handler Types

### React Event Types

```typescript
// Form events
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  // ...
};

// Input events
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const value = e.target.value;
  // ...
};

// Click events
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  // ...
};

// Keyboard events
const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  if (e.key === 'Enter') { ... }
};

// Focus events
const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
  // ...
};
```

### DOM Event Types (Non-React)

```typescript
// Generic DOM events
document.addEventListener('click', (e: MouseEvent) => { ... });
document.addEventListener('keydown', (e: KeyboardEvent) => { ... });
document.addEventListener('submit', (e: SubmitEvent) => { ... });
```

## Promise and Async Types

### Typing Async Functions

```typescript
// Function returning a promise
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// Arrow function variant
const fetchUser = async (id: string): Promise<User> => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
};
```

### Promise Type Patterns

```typescript
// Promise with explicit type
const userPromise: Promise<User> = fetchUser("123");

// Awaiting with type inference
const user = await fetchUser("123"); // User

// Promise.all with multiple types
const [user, posts] = await Promise.all([fetchUser("123"), fetchPosts("123")]); // [User, Post[]]
```

## Function Types

### Callback Types

```typescript
// Typed callback parameter
function processItems(
  items: string[],
  callback: (item: string, index: number) => void
) {
  items.forEach(callback);
}

// Alternative: Extract the type
type ItemCallback = (item: string, index: number) => void;

function processItems(items: string[], callback: ItemCallback) {
  items.forEach(callback);
}
```

### Overloaded Functions

```typescript
// Function overloads for different input/output types
function parse(input: string): object;
function parse(input: Buffer): object;
function parse(input: string | Buffer): object {
  if (typeof input === "string") {
    return JSON.parse(input);
  }
  return JSON.parse(input.toString());
}
```

## Type Assertions (Use Sparingly)

Use type assertions only when you know more than TypeScript:

```typescript
// DOM element assertion (when you know the element type)
const input = document.getElementById("email") as HTMLInputElement;

// Response data assertion (when you trust the API)
const data = (await response.json()) as ApiResponse;

// Non-null assertion (when you know it's not null)
const element = document.querySelector(".button")!;
```

**Warning:** Type assertions bypass TypeScript's checks. Prefer type guards when possible.

## Utility Types

### Built-in Utility Types

```typescript
// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Pick - select specific properties
type UserName = Pick<User, "name" | "email">;

// Omit - exclude specific properties
type UserWithoutId = Omit<User, "id">;

// Readonly - immutable properties
type ReadonlyUser = Readonly<User>;

// Record - create object type
type UserMap = Record<string, User>;

// ReturnType - extract function return type
type FetchUserReturn = ReturnType<typeof fetchUser>;

// Parameters - extract function parameters
type FetchUserParams = Parameters<typeof fetchUser>;
```

## Discriminated Unions

Pattern for handling multiple related types:

```typescript
type Result<T> = { success: true; data: T } | { success: false; error: string };

function handleResult<T>(result: Result<T>) {
  if (result.success) {
    // TypeScript knows result.data exists here
    console.log(result.data);
  } else {
    // TypeScript knows result.error exists here
    console.error(result.error);
  }
}
```

## Module Augmentation

Extend existing types without modifying original:

```typescript
// Extend Express Request
declare module "express" {
  interface Request {
    user?: User;
  }
}

// Extend environment variables
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      DATABASE_URL: string;
      API_KEY: string;
    }
  }
}
```

## Common Pitfalls

### Pitfall 1: Using `any` for JSON Data

**❌ WRONG:**

```typescript
const data: any = JSON.parse(jsonString);
```

**✅ CORRECT:**

```typescript
interface ExpectedData {
  id: string;
  name: string;
}

const data: unknown = JSON.parse(jsonString);
// Then validate with type guard or schema validation (zod, etc.)
```

### Pitfall 2: Implicit `any` in Callbacks

**❌ WRONG:**

```typescript
// 'item' has implicit 'any' type
items.map((item) => item.name);
```

**✅ CORRECT:**

```typescript
items.map((item: Item) => item.name);
// Or ensure 'items' has proper type: Item[]
```

### Pitfall 3: Object Property Access

**❌ WRONG:**

```typescript
function getValue(obj: any, key: string) {
  return obj[key];
}
```

**✅ CORRECT:**

```typescript
function getValue<T extends Record<string, unknown>, K extends keyof T>(
  obj: T,
  key: K
): T[K] {
  return obj[key];
}
```

### Pitfall 4: Empty Array Type

**❌ WRONG:**

```typescript
const items = []; // any[]
```

**✅ CORRECT:**

```typescript
const items: string[] = [];
// or
const items: Array<string> = [];
```

## ESLint Rules to Enable

For strict TypeScript, enable these rules:

```json
{
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/strict-boolean-expressions": "warn",
    "@typescript-eslint/no-unsafe-assignment": "error",
    "@typescript-eslint/no-unsafe-member-access": "error",
    "@typescript-eslint/no-unsafe-call": "error",
    "@typescript-eslint/no-unsafe-return": "error"
  }
}
```

> **Note**: Instead of the deprecated `@typescript-eslint/no-implicit-any-catch` rule, set `useUnknownInCatchVariables: true` in your `tsconfig.json` (TypeScript 4.4+). This ensures catch clause variables are typed as `unknown` instead of `any`.

## Quick Reference

| Instead of `any` | Use                      |
| ---------------- | ------------------------ | --- |
| Unknown data     | `unknown`                |
| Flexible type    | Generics `<T>`           |
| Multiple types   | Union `A                 | B`  |
| Dynamic keys     | `Record<K, V>`           |
| Nullable         | `T \| null`              |
| Optional         | `T \| undefined` or `T?` |
| Callback         | `(args) => ReturnType`   |
| Empty array      | `Type[]`                 |
| JSON data        | `unknown` + type guard   |

## Summary

- **Never use `any`** - it defeats TypeScript's purpose
- **Use `unknown`** for truly unknown types, then narrow with type guards
- **Use generics** for reusable, type-safe components
- **Use union types** for finite sets of possibilities
- **Use discriminated unions** for complex state machines
- **Enable strict ESLint rules** to catch violations automatically
