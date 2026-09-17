---
name: typescript-v6
description: Advanced TypeScript patterns for type-safe, maintainable code using sophisticated type system features. Use when building type-safe APIs, implementing complex domain models, or leveraging TypeScript's advanced type capabilities.
---

# Skill: typescript

## Scope

- Applies to: TypeScript 6.0+ type system features, type-safe APIs, complex domain models, inference, compile-time guarantees
- Does NOT cover: Basic syntax, framework-specific patterns, runtime validation (use Zod separately)

## Assumptions

- Folder major tracks `package.json` `typescript` (this repo: `@typescript/typescript6` ^6), not `npm view typescript` (may already be 7)
- 6.0 is the last JavaScript-based compiler; 7.0 is native (Go). `@typescript/native` may sit beside `tsc`; it is not this skill’s major
- Strict mode (`"strict": true`)
- Target ES2020+ (6.0 defaults trend toward `esnext` / `es2025`)
- Options deprecated in 6.0 can be ignored with `"ignoreDeprecations": "6.0"` until 7.0 removes them. Prefer fixing deprecations: https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/

## Principles

- Use conditional types for type selection based on conditions
- Use mapped types for systematic object type transformations
- Use type guards (`value is Type`) for runtime checking with type narrowing
- Use discriminated unions for type-safe state machines with exhaustiveness checking
- Use branded types to prevent primitive mixing
- Prefer `unknown` over `any` for type safety
- Use type guards over type assertions (`as Type`)
- Keep types composable and shallow (avoid deep nesting)
- Mark immutable data structures as `readonly`

## Constraints

### MUST

- Enable strict mode (`"strict": true` in `tsconfig.json`)
- Use `unknown` instead of `any` for untyped values
- Use type guards (`value is Type`) instead of type assertions when possible

### SHOULD

- Use `type` for unions/utilities, `interface` for object shapes
- Keep types composable and shallow
- Mark immutable data structures as `readonly`
- Use branded types to prevent primitive mixing
- Address 6.0 deprecations before adopting TypeScript 7 native

### AVOID

- Using `any` (use `unknown` with type guards)
- Type assertions without validation
- Overusing generics (only when types truly vary)
- Deep type nesting (slow compilation, hard to debug)
- Import assertions (`assert { type: ... }`); use `with` import attributes

## Interactions

- Works with [zod](https://zod.dev) for runtime validation with type inference
- Complements [next](../next-v16/SKILL.md) for type-safe API routes
- Complements [fastify](../fastify-v5/SKILL.md) for type-safe route schemas

## Patterns

### Mapped Types

Transform object types systematically:

```typescript
type Partial<T> = { [P in keyof T]?: T[P] }
type Readonly<T> = { readonly [P in keyof T]: T[P] }
type Pick<T, K extends keyof T> = { [P in K]: T[P] }
```

### Type Guards

Runtime type checking with type narrowing:

```typescript
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

function isSuccess(result: Result): result is Success {
  return result.status === 'success'
}
```

### Branded Types

Create nominal types for type safety:

```typescript
type UserId = string & { readonly __brand: 'UserId' }
type PostId = string & { readonly __brand: 'PostId' }

function createUserId(id: string): UserId {
  return id as UserId
}
```

### Discriminated Unions

Type-safe state machines with exhaustiveness checking:

```typescript
type LoadingState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: string[] }
  | { status: 'error'; error: Error }
```

## References

- [Conditional Types](references/conditional-types.md) - Type selection based on conditions
- [Advanced Generics](references/advanced-generics.md) - Generic constraints and inference patterns
- [Discriminated Unions](references/discriminated-unions.md) - Type-safe state machines

## Resources

- [Announcing TypeScript 6.0](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [Type Challenges](https://github.com/type-challenges/type-challenges)
