---
name: typescript
description: WHEN writing TypeScript, defining types/schemas, or building type-safe apps; outputs strict, schema-first, production-ready code.
---

# TypeScript Best Practices

Production-grade TypeScript development with schema-first design, strict type safety, and immutable patterns.

## Core Principles

1. **Type Safety at All Boundaries** - Runtime validation (schemas) + compile-time safety (TypeScript)
2. **Schema-First Development** - Define schemas before types, derive types from schemas
3. **Immutability** - No data mutation, always create new values
4. **Explicit Types** - No implicit any, strict mode enabled
5. **Behavior over implementation** - Focus on contracts and outcomes

## Quick Reference

| Topic                                                                  | Guide                                                 |
| ---------------------------------------------------------------------- | ----------------------------------------------------- |
| Schema-first development, when to use schemas vs types, test factories | [schemas.md](references/schemas.md)                   |
| Type vs interface, any vs unknown, assertions, strict mode             | [types-interfaces.md](references/types-interfaces.md) |
| Immutability patterns, readonly, forbidden methods, error handling     | [immutability.md](references/immutability.md)         |
| Branded types, utility types, code smells reference                    | [utilities.md](references/utilities.md)               |
| Common TypeScript patterns with examples                               | [patterns.md](references/patterns.md)                 |

## When to Use Each Guide

### Schemas

Use [schemas.md](references/schemas.md) when you need:

- Schema-first development patterns
- Decision framework: when schema is required vs optional
- Trust boundary identification
- Test data factory patterns with schema validation
- Examples of schema usage (API responses, business validation)

### Types and Interfaces

Use [types-interfaces.md](references/types-interfaces.md) when you need:

- Type vs interface guidance
- The any vs unknown decision
- Type assertion best practices
- Strict mode configuration
- tsconfig.json settings

### Immutability

Use [immutability.md](references/immutability.md) when you need:

- Immutability patterns (spread operators)
- Readonly modifiers
- Forbidden array methods reference
- Options objects vs positional parameters
- Boolean parameter anti-patterns
- Result types for error handling
- Early return patterns

### Utilities

Use [utilities.md](references/utilities.md) when you need:

- Branded types for domain concepts
- Built-in utility types (Pick, Omit, Partial, etc.)
- Custom utility types
- Code smell reference tables

### Patterns

Use [patterns.md](references/patterns.md) when you need:

- Schema-first examples at trust boundaries
- Internal type examples without schemas
- Schema with test factory patterns
- Result type for error handling
- Branded types for domain safety
- Immutable array operations
- Options object pattern

## Quick Reference: Decision Trees

### Should I use a schema?

```
Does data come from outside the application?
├── Yes → Schema required
└── No → Does it have validation rules (format, range, enum)?
    ├── Yes → Schema required
    └── No → Is it shared between systems?
        ├── Yes → Schema required
        └── No → Type is fine
```

### Should I use `type` or `interface`?

```
Am I defining a behavior contract for dependency injection?
├── Yes → interface
└── No → type
```

### Should I use `any` or `unknown`?

```
Never use any.
Always use unknown for truly unknown types.
```

### Options object or positional parameters?

```
How many parameters?
├── 1-2 → Positional is fine
└── 3+ → Use options object
```

## Summary Checklist

Before committing TypeScript code, verify:

- [ ] Strict mode enabled in tsconfig.json
- [ ] No `any` types (use `unknown` instead)
- [ ] Schemas at all trust boundaries (API, user input, files)
- [ ] Types derived from schemas using `z.infer`
- [ ] Using `type` for data, `interface` only for behavior contracts
- [ ] All data structures use `readonly` where appropriate
- [ ] No array mutations (push, pop, splice, etc.)
- [ ] Functions with 3+ params use options objects
- [ ] No boolean positional parameters
- [ ] Result types for operations that can fail
- [ ] Early returns instead of nested conditionals
- [ ] Test factories validate with schemas
- [ ] Branded types for domain concepts that shouldn't mix
- [ ] Explicit return types on functions
