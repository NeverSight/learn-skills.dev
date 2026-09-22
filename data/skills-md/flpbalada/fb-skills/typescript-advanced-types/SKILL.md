---
name: typescript-advanced-types
description: Design readable advanced TypeScript types. Use when creating reusable type utilities, generics, conditional types, mapped types, template literal types, infer helpers, branded types, type guards, assertion functions, typed libraries, API clients, configs, or state helpers. Prefer simple types until complexity pays off. For broad code-quality typing guidance use typescript-best-practices.
---

# TypeScript Advanced Types

## Goal

Use advanced types to improve safety without making code unreadable.
Prefer simple types until complexity pays for itself.

## Rules

- Use `unknown` instead of `any` when input is not trusted.
- Let TypeScript infer simple types.
- Add generics only when a type must connect multiple positions.
- Prefer unions and discriminated unions for variants.
- Prefer `interface` for object shapes.
- Use `type` for unions, conditionals, mapped types, and aliases.
- Avoid deeply nested conditional or recursive types.
- Add type tests for reusable utilities when the project supports them.

## Core Tools

- Generics: reuse logic across related types.
- Conditional types: choose a type from a type condition.
- Mapped types: transform object properties.
- Template literal types: constrain string patterns.
- Utility types: use `Pick`, `Omit`, `Partial`, `Required`, `Readonly`, `Record`.
- `infer`: extract inner types from arrays, promises, functions, or objects.
- Type guards: narrow `unknown` at runtime.
- Assertion functions: throw when runtime validation fails.
- Branded types: distinguish validated strings or IDs.

## Generic Rule

If a type parameter appears only once, it is probably unnecessary.

## Useful Patterns

```ts
type StrictOmit<T, K extends keyof T> = Omit<T, K>;
```

```ts
type ElementType<T> = T extends (infer U)[] ? U : never;
```

```ts
type UserId = string & { readonly __brand: "UserId" };
```

```ts
type User = z.infer<typeof userSchema>;
```

## Avoid

- `any` as a shortcut.
- Type assertions when a guard is possible.
- Overly clever types that hide intent.
- Unbounded generic parameters.
- Duplicating types already available from schema or API definitions.
- Recursive types that slow the compiler.

## Progressive Disclosure

This skill provides detailed examples through context files. Load them when needed:

| Context File                      | When to Load                                    |
| --------------------------------- | ----------------------------------------------- |
| `context/core-examples.md`       | Need generics, conditionals, mapped types examples |
| `context/patterns.md`            | Implementing real-world patterns like EventEmitter, API client, or Builder |
| `context/techniques.md`          | Type inference, guards, assertions, and testing |

## References

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [Type Challenges](https://github.com/type-challenges/type-challenges)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Effective TypeScript](https://effectivetypescript.com/2020/08/12/generics-golden-rule/)

## Output

- Type approach.
- Simplest type shape.
- Generic constraints if needed.
- Runtime validation boundary when input is unknown.
