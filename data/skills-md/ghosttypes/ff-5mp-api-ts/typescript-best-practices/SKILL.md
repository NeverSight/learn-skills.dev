---
name: typescript-best-practices
description: TypeScript best practices and patterns for writing type-safe, maintainable code. Use when working with TypeScript files, configuring tsconfig, defining interfaces/types, implementing error handling, writing generics, or setting up type-safe communication patterns. Includes patterns for discriminated unions, type guards, utility types, and more.
---

# TypeScript Best Practices

## Quick Start

Always enable strict mode and use explicit types for public APIs. Prefer type-only imports (`import type`) and named exports over default exports. Use discriminated unions for state management and type guards for runtime validation.

## Type Safety Fundamentals

### Strict Mode Configuration

Enable all strict flags in `tsconfig.json`:
```json
{
  "strict": true,
  "noImplicitAny": true,
  "noImplicitReturns": true,
  "strictNullChecks": true,
  "strictFunctionTypes": true
}
```

### Null Safety

```typescript
// Explicit null handling
export function findById<T>(items: Map<string, T>, id: string): T | null {
  return items.get(id) ?? null;
}

// Optional chaining and nullish coalescing
export function getName(item?: Item): string {
  return item?.name ?? 'Unknown';
}
```

### Explicit Return Types

Use explicit return types for public APIs:
```typescript
// Good
export function validateConfig(data: unknown): ValidatedConfig | null {
  const result = ConfigSchema.safeParse(data);
  return result.success ? result.data : null;
}

// Bad - implicit return type
export function validateConfig(data) {
  return data;
}
```

## Core Patterns

### Discriminated Unions for State

```typescript
export type ConnectionState =
  | { status: 'disconnected' }
  | { status: 'connecting'; progress: number }
  | { status: 'connected'; connectionId: string }
  | { status: 'error'; message: string };

// TypeScript knows which properties are available in each branch
```

### Result Type for Error Handling

```typescript
export type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

const result = await connectToService(options);
if (result.success) {
  console.log('Connected:', result.data.id);
} else {
  console.error('Failed:', result.error.message);
}
```

### Readonly Properties

Use `readonly` for immutable data:
```typescript
export interface Config {
  readonly enableFeature: boolean;
  readonly port: number;
}
```

## Type Guards and Assertions

```typescript
// Type guard
export function isUserData(data: unknown): data is UserData {
  return typeof data === 'object' && data !== null && 'name' in data;
}

// Assertion function
export function assertIsDefined<T>(value: T): asserts value is NonNullable<T> {
  if (value === undefined || value === null) throw new Error('Value is undefined or null');
}
```

## Import/Export Conventions

```typescript
// Type-only imports (preferred)
import type { Config } from '../types/config';

// Named exports (avoid default exports)
export class DataService {}
export const getService = () => DataService.getInstance();

// Grouped imports
import { External } from 'external';           // External deps
import { internalUtil } from './utils';         // Internal utils
import type { MyType } from './types';          // Types
```

## When to Use References

| Reference File | When to Load |
|----------------|--------------|
| `tsconfig.md` | Setting up TypeScript configuration |
| `interfaces-types.md` | Defining interfaces, generic types, extending external types |
| `unions-discriminated.md` | Working with discriminated unions, result types, exhaustive checks |
| `type-guards-assertions.md` | Runtime validation, branded types, assertion functions |
| `utility-types.md` | Using built-in utilities, const assertions, template literal types |
| `error-handling.md` | Implementing structured errors, error factories, retry logic |
| `generics.md` | Building generic services, repositories, factories, event emitters |
| `import-export.md` | Organizing imports/exports, avoiding circular dependencies |

## Common Anti-Patterns to Avoid

1. **Using `any`** - Use `unknown` with type guards instead
2. **Default exports** - Harder to refactor and tree-shake
3. **Implicit return types** on public APIs
4. **Non-readonly interfaces** for immutable data
5. **Nested optionals** (`{ a?: { b?: string } }`) - use discriminated unions instead
