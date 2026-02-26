---
name: typescript-best-practices
description: Core TypeScript conventions for type safety, inference, and clean code. Use when writing TypeScript, reviewing TypeScript code, creating interfaces/types, or when the user asks about TypeScript patterns, conventions, or best practices.
---

# TypeScript Best Practices

## Type Safety

- Enable `strict: true` in `tsconfig.json` — never disable strict checks in production code.
- Prefer `unknown` over `any`. If `any` is unavoidable, add a comment explaining why and narrow it immediately.
- Use `satisfies` to validate a value matches a type while preserving its narrowed literal type:

```typescript
const config = {
    endpoint: "/api/users",
    timeout: 3000,
} satisfies Config;
```

- Prefer type narrowing (type guards, `in` operator, `instanceof`) over type assertions (`as`).

## Type Inference

- Let TypeScript infer when the type is obvious — don't annotate what the compiler already knows:

```typescript
// Redundant
const name: string = "Graham";

// Let it infer
const name = "Graham";
```

- Always annotate function return types for exported/public functions — it catches accidental return type changes and improves IDE performance:

```typescript
export function getUser(id: string): User | undefined {
    return users.get(id);
}
```

- Annotate function parameters — they cannot be inferred from implementation.

## Types vs Interfaces

- Use `type` for unions, intersections, mapped types, and utility types.
- Use `interface` for object shapes that may be extended or implemented.
- Be consistent within a codebase — pick one default and stick with it.

## Enums and Constants

- Prefer `as const` objects over `enum`:

```typescript
const Status = {
    Active: "active",
    Inactive: "inactive",
} as const;

type Status = (typeof Status)[keyof typeof Status];
```

- This gives you type safety, tree-shaking, and no runtime enum overhead.

## Null Handling

- Prefer explicit `| undefined` in types over optional properties when the distinction matters.
- Use optional chaining (`?.`) and nullish coalescing (`??`) over manual null checks.
- Avoid non-null assertions (`!`) — narrow the type instead.

## Generics

- Name generic parameters descriptively when there are multiple: `TInput`, `TOutput` instead of `T`, `U`.
- Constrain generics with `extends` to communicate intent:

```typescript
function merge<T extends Record<string, unknown>>(a: T, b: Partial<T>): T {
    return { ...a, ...b };
}
```

- Avoid over-genericizing — if a function only ever handles one type, don't make it generic.

## Utility Types

- Use built-in utility types (`Partial`, `Required`, `Pick`, `Omit`, `Record`, `Readonly`) instead of reimplementing them.
- `Readonly<T>` for data that should not be mutated.
- `Pick` and `Omit` to derive subsets from existing types rather than duplicating fields.

## Error Handling

- Type errors explicitly — don't rely on `catch (e)` being `any`:

```typescript
try {
    await fetchData();
} catch (error) {
    if (error instanceof ApiError) {
        handleApiError(error);
    }
    throw error;
}
```

- Create typed error classes for domain-specific errors.

## Module Organization

- One type/interface per concern — avoid monolithic `types.ts` files.
- Co-locate types with the code that uses them.
- Export types from barrel files only when they form part of the public API.
- Use `import type` / `export type` for type-only imports to enable proper tree-shaking.

## Naming Conventions

- PascalCase for types, interfaces, enums, and classes.
- camelCase for variables, functions, and methods.
- UPPER_SNAKE_CASE for true constants (compile-time values).
- Don't prefix interfaces with `I` or types with `T` — it's not C#.
