---
name: generics-as-functions
description: Use when defining generic types or functions. Use when constraining type parameters. Use when writing type-level code. Use when documenting generic types.
---

# Think of Generics as Functions Between Types

## Overview

Generic types are the type-level equivalent of functions in value space. Just as a function takes parameters and returns a value, a generic type takes type parameters and produces a concrete type. This mental model helps you write better generic types by applying the same principles you use for writing functions: constraining inputs, choosing good names, and documenting behavior.

Understanding generics as functions between types clarifies when to use constraints, how to name type parameters, and why some generic patterns work while others don't. This perspective is essential for effective type-level programming in TypeScript.

## When to Use This Skill

- Defining generic types that transform other types
- Writing generic functions with type parameters
- Constraining what types can be passed to generics
- Documenting generic types with TSDoc
- Creating reusable type utilities

## The Iron Rule

**Think of generic types as functions between types: use extends to constrain inputs like type annotations, choose descriptive names, and document with @template TSDoc.**

## Detection

Watch for these patterns:

```typescript
// RED FLAGS - Poor generic design
type MyPick<T, K> = { [P in K]: T[P] };  // No constraints, errors in implementation
type BadGeneric<X, Y, Z> = ...;  // Single-letter names without context
function parse<T>(input: string): T;  // Return-only generic, no better than any
```

## Generic Types as Functions

A generic type takes type parameters and produces a concrete type:

```typescript
// Generic type "function"
type MyPartial<T> = { [K in keyof T]?: T[K] };

// "Calling" the function with Person
type PartPerson = MyPartial<Person>;
// Equivalent to: { name?: string; age?: number; }
```

Just like functions, generic types can have multiple parameters:

```typescript
// Two type parameters
type MyPick<T, K extends keyof T> = { [P in K]: T[P] };

// Usage
type NameOnly = MyPick<Person, 'name'>;
// Equivalent to: { name: string }
```

## Constraining Type Parameters

Use `extends` to constrain type parameters, just as you'd use type annotations for function parameters:

```typescript
// GOOD: Constrained type parameters
type MyPick<T extends object, K extends keyof T> = {
  [P in K]: T[P]
};

// Without constraints - allows invalid instantiations
type BadPick<T, K> = { [P in K]: T[P] };  // Errors in implementation

// Invalid uses caught by constraints:
type Bad1 = MyPick<Person, 'firstName'>;  // Error: 'firstName' not in Person
type Bad2 = MyPick<'age', Person>;  // Error: string doesn't satisfy object
```

## Naming Type Parameters

Choose descriptive names, especially for complex generics:

```typescript
// Short names OK for simple, local generics
type Partial<T> = { [K in keyof T]?: T[K] };

// Longer names for complex or exported generics
type MapValues<
  ObjectType extends object,
  ValueTransformer extends (value: any) => any
> = {
  [Key in keyof ObjectType]: ValueTransformer<ObjectType[Key]>
};
```

## Documenting Generics

Use `@template` TSDoc tag to document type parameters:

```typescript
/**
 * Construct a new object type using a subset of properties from another.
 * @template T - The original object type
 * @template K - The keys to pick, typically a union of string literal types
 */
type MyPick<T extends object, K extends keyof T> = {
  [P in K]: T[P]
};
```

## Generic Functions

Generic functions define associated generic types and enable type inference:

```typescript
function pick<T extends object, K extends keyof T>(
  obj: T,
  ...keys: K[]
): Pick<T, K> {
  const result: Partial<Pick<T, K>> = {};
  for (const k of keys) {
    result[k] = obj[k];
  }
  return result as Pick<T, K>;
}

// TypeScript infers types from arguments
const person = { name: 'Alice', age: 30 };
const nameOnly = pick(person, 'name');
// Type: Pick<{ name: string; age: number }, 'name'>
```

## Generic Classes

Generic classes capture types that don't need to be passed to methods:

```typescript
class Box<T> {
  value: T;
  constructor(value: T) {
    this.value = value;
  }
  getValue(): T {
    return this.value;
  }
}

// Type inferred from constructor
const dateBox = new Box(new Date());
// Type: Box<Date>
```

## Pressure Resistance Protocol

When pressured to use unconstrained generics:

1. **Add constraints**: Use `extends` to limit valid type arguments
2. **Consider defaults**: Provide sensible defaults for type parameters
3. **Document requirements**: Use TSDoc to explain constraints
4. **Test edge cases**: Verify generics work with unions and edge cases

## Red Flags

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| Unconstrained type parameters | Allows invalid instantiations, implementation errors |
| Single-letter names in complex generics | Reduces readability |
| Return-only generics | Equivalent to type assertions, no type safety |
| Missing TSDoc on public generics | Poor developer experience |

## Common Rationalizations

### "Constraints limit flexibility"

**Reality**: Constraints catch errors at the type level rather than producing confusing type errors or wrong types. They document valid usage.

### "T, K, V are standard names"

**Reality**: They are conventional for simple cases, but descriptive names improve readability in complex generics. Match name length to scope.

### "Users can figure out the types"

**Reality**: Documentation helps users understand generics without reading implementation. @template tags appear in IDE tooltips.

## Quick Reference

| Concept | Value-Level | Type-Level |
|---------|-------------|------------|
| Definition | `function` | `type` |
| Parameters | `(x: T)` | `<T extends Constraint>` |
| Return | `: ReturnType` | `= ResultType` |
| Documentation | `@param` | `@template` |
| Constraints | Type annotations | `extends` keyword |

## The Bottom Line

Generic types are functions between types. Apply the same principles you use for writing functions: constrain inputs, choose meaningful names, and document thoroughly. This mental model makes complex type-level code more approachable and maintainable.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 50: Think of Generics as Functions Between Types
