---
name: tail-recursive-generics
description: Use when getting "Type instantiation is excessively deep" errors. Use when writing recursive generic types. Use when processing large or deep type structures. Use when building type-level loops.
---

# Prefer Tail-Recursive Generic Types

## Overview

TypeScript limits the depth of type instantiation to prevent infinite loops. When you hit "Type instantiation is excessively deep and possibly infinite," you need to refactor your recursive types to be tail-recursive. Using an accumulator pattern, you can write types that TypeScript can optimize, avoiding depth limits.

This skill is essential for type-level programming that processes large or deeply nested structures.

## When to Use This Skill

- Getting "Type instantiation is excessively deep" errors
- Writing recursive generic types
- Processing large type structures
- Building type-level loops or iterations
- Deeply nested object transformations

## The Iron Rule

**Use accumulator patterns to make generic types tail-recursive. Pass accumulated results as type parameters rather than building up nested type structures.**

## Detection

Watch for these symptoms:

```typescript
// ERROR: Type instantiation is excessively deep
type DeepTransform<T> = T extends object
  ? { [K in keyof T]: DeepTransform<T[K]> }
  : T;

// Works for shallow objects, fails for deeply nested ones
type Test = DeepTransform<{ a: { b: { c: { d: { e: string } } } } }>;
```

## The Problem: Non-Tail Recursion

```typescript
// BAD: Non-tail-recursive - builds nested type structure
type NTuple<T, N extends number> = 
  N extends 0 
    ? []
    : [T, ...NTuple<T, Subtract<N, 1>>];
//          ^^^^^^^^^^^^^^^^^^^^^^^^^^
//          Recursive call not in tail position
//          TypeScript can't optimize this

// Each recursive call adds a layer:
// NTuple<T, 3> = [T, ...NTuple<T, 2>]
//              = [T, ...[T, ...NTuple<T, 1>]]
//              = [T, ...[T, ...[T, ...[]]]]
// Depth grows with N
```

## The Solution: Tail Recursion with Accumulator

```typescript
// GOOD: Tail-recursive with accumulator
type NTuple<T, N extends number> = NTupleHelp<T, N, []>;

type NTupleHelp<T, N extends number, Acc extends T[]> =
  Acc['length'] extends N
    ? Acc
    : NTupleHelp<T, N, [T, ...Acc]>;
//    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
//    Recursive call is in tail position
//    TypeScript can optimize this

// Accumulator builds result iteratively:
// NTupleHelp<T, 3, []>
// → NTupleHelp<T, 3, [T]>
// → NTupleHelp<T, 3, [T, T]>  
// → NTupleHelp<T, 3, [T, T, T]>
// → [T, T, T] (Acc['length'] extends 3)
```

## Real-World Example: Deep Readonly

```typescript
// BAD: Non-tail-recursive, hits depth limit
type DeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

// GOOD: Tail-recursive with accumulator
type DeepReadonly<T> = DeepReadonlyHelp<T, []>;

type DeepReadonlyHelp<T, Seen extends unknown[]> = 
  T extends object
    ? T extends Seen[number]  // Check for circular reference
      ? T
      : { 
          readonly [K in keyof T]: DeepReadonlyHelp<
            T[K], 
            [T, ...Seen]  // Accumulate seen types
          > 
        }
    : T;

// Usage
type Deep = DeepReadonly<{
  a: { b: { c: { d: { e: { f: string } } } } }
}>;
// Works without hitting depth limit!
```

## String Transformation Example

```typescript
// BAD: Non-tail-recursive string replacement
type ReplaceAll<S extends string, From extends string, To extends string> =
  S extends `${infer Before}${From}${infer After}`
    ? `${Before}${To}${ReplaceAll<After, From, To>}`  // Not tail-recursive
    : S;

// GOOD: Tail-recursive with accumulator
type ReplaceAll<S extends string, From extends string, To extends string> =
  ReplaceAllHelp<S, From, To, ''>;

type ReplaceAllHelp<
  S extends string,
  From extends string,
  To extends string,
  Acc extends string
> = S extends `${infer Before}${From}${infer After}`
  ? ReplaceAllHelp<After, From, To, `${Acc}${Before}${To}`>
  : `${Acc}${S}`;

// Usage
type Result = ReplaceAll<'foo-bar-baz', '-', '_'>;
// 'foo_bar_baz' - works for long strings!
```

## Key Principles

```typescript
// 1. Pass accumulator as type parameter
type Transform<T, Acc = []> = /* ... */;

// 2. Recursive call must be in tail position
// BAD:  [T, ...Recursive<...]  // Spread is not tail position
// GOOD: Recursive<..., [...Acc, T]>  // Accumulator updated

// 3. Base case checks accumulator
type Helper<T, Acc> = Condition<Acc> extends true
  ? Acc  // Return accumulated result
  : Helper<T, Update<Acc>>;  // Continue with updated accumulator
```

## When Tail Recursion Doesn't Help

Some types are inherently deep:

```typescript
// Pathological case: deeply nested object
type Deep = {
  a: { b: { c: { d: { e: { f: { g: string } } } } } }
};

// Even tail-recursive types may struggle with
// objects nested 50+ levels deep
```

## Pressure Resistance Protocol

When hitting depth limit errors:

1. **Identify recursion**: Find the recursive type causing issues
2. **Add accumulator**: Create helper type with accumulator parameter
3. **Move to tail position**: Ensure recursive call is last operation
4. **Test with deep cases**: Verify it handles deeply nested types
5. **Consider alternatives**: Sometimes runtime validation is better

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `...Recursive<...>` in tuple | Not tail-recursive | Use accumulator |
| Deep nesting without accumulator | Hits depth limit | Add accumulator param |
| Recursive call in conditional | May not be optimized | Restructure |

## Common Rationalizations

### "I'll just increase TypeScript's depth limit"

**Reality**: There's no configuration for this. The limit protects against infinite loops.

### "My types aren't that deep"

**Reality**: Generated types (from GraphQL, etc.) can be deeper than expected. Tail recursion makes them robust.

### "This is too complex"

**Reality**: The pattern is simple: helper type + accumulator. Learn it once, apply everywhere.

## Quick Reference

| Pattern | Non-Tail | Tail-Recursive |
|---------|----------|----------------|
| Tuple building | `[T, ...Rec<N-1>]` | `Rec<N, [T, ...Acc]>` |
| String building | `` `${X}${Rec<Y>}` `` | `` `Rec<Y, `${Acc}${X}`>` `` |
| Object traversal | `{ [K]: Rec<T[K]> }` | `Rec<T[K], [T, ...Acc]>` |

## The Bottom Line

Use accumulator patterns to make recursive generic types tail-recursive. This avoids "excessively deep" errors and makes your types work with arbitrarily large inputs.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 57: Prefer Tail-Recursive Generic Types
