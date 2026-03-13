---
name: control-union-distribution
description: Use when conditional types behave unexpectedly with unions. Use when boolean or never types cause surprises. Use when needing to prevent distribution over unions. Use when recursive generic types don't distribute.
---

# Control the Distribution of Unions over Conditional Types

## Overview

Conditional types in TypeScript distribute over unions by default. This is usually what you want, but sometimes it causes surprising behavior. Understanding how to control distribution - both preventing it when unwanted and enabling it when needed - is essential for advanced type-level programming.

Key surprises include: `boolean` being treated as `true | false`, `never` distributing to `never`, and recursive types that fail to distribute. This skill shows you how to handle these cases.

## When to Use This Skill

- Conditional type behaves unexpectedly with union inputs
- `boolean` type produces surprising results
- `never` type evaluates unexpectedly
- Need to prevent distribution over unions
- Recursive generic types not distributing correctly

## The Iron Rule

**Wrap conditions in one-tuples `[T]` to prevent distribution; add bare conditions `N extends...` to force distribution. Understand how `boolean` and `never` behave with distributive conditionals.**

## Detection

Watch for these surprising behaviors:

```typescript
// Surprising: boolean distributes
type Celebrate<V> = V extends true ? 'Huzzah!' : never;
type Surprise = Celebrate<boolean>;  // "Huzzah!" not never

// Surprising: never distributes to never
type AllowIn<T> = T extends { password: string } ? 'Yes' : 'No';
type N = AllowIn<never>;  // never, not 'Yes' | 'No'

// Problem: recursive type doesn't distribute
type NTuple<T, N> = /* ... */;  // NTuple<string, 2 | 3> gives wrong result
```

## Preventing Distribution

Wrap the condition in a one-tuple `[T]`:

```typescript
// Problem: distributes over unions
type Comparable<T> =
  T extends Date ? Date | number :
  T extends number ? number :
  T extends string ? string :
  never;

// Date | string becomes (Date | number) | string - wrong!
let dateOrStr: Date | string;
const result: Comparable<typeof dateOrStr>;  // Should be never

// Solution: wrap in one-tuple
type Comparable<T> =
  [T] extends [Date] ? Date | number :
  [T] extends [number] ? number :
  [T] extends [string] ? string :
  never;

// Now Date | string correctly evaluates to never
```

## The Boolean Surprise

TypeScript treats `boolean` as `true | false`:

```typescript
type CelebrateIfTrue<V> = V extends true ? 'Huzzah!' : never;

// Surprising result
type Party = CelebrateIfTrue<true>;      // "Huzzah!"
type NoParty = CelebrateIfTrue<false>;   // never
type Surprise = CelebrateIfTrue<boolean>; // "Huzzah!" (!)

// Why? boolean distributes:
// CelebrateIfTrue<true | false>
// = CelebrateIfTrue<true> | CelebrateIfTrue<false>
// = "Huzzah!" | never
// = "Huzzah!"

// Fix: prevent distribution
type CelebrateIfTrue<V> = [V] extends [true] ? 'Huzzah!' : never;
type SurpriseFixed = CelebrateIfTrue<boolean>;  // never - correct!
```

## The Never Surprise

`never` is treated as an empty union:

```typescript
type AllowIn<T> = T extends { password: string } ? 'Yes' : 'No';

// Surprising: never evaluates to never
type N = AllowIn<never>;  // never (not 'Yes' or 'No')

// Why? never is empty union:
// AllowIn<never> = AllowIn<> = empty union = never

// Fix: wrap in one-tuple
type AllowIn<T> = [T] extends [{ password: string }] ? 'Yes' : 'No';
type NFixed = AllowIn<never>;  // 'No' - correct!
```

## Enabling Distribution

Sometimes you need to force distribution. Add a bare condition:

```typescript
// Problem: recursive type doesn't distribute
type NTuple<T, N extends number> = NTupleHelp<T, N, []>;
type NTupleHelp<T, N, Acc extends T[]> =
  Acc['length'] extends N
    ? Acc
    : NTupleHelp<T, N, [T, ...Acc]>;

type PairOrTriple = NTuple<string, 2 | 3>;
// Got: [string, string] (wrong!)
// Want: [string, string] | [string, string, string]

// Solution: add distributive wrapper
type NTuple<T, N extends number> =
  N extends number  // Forces distribution
    ? NTupleHelp<T, N, []>
    : never;

type PairOrTripleFixed = NTuple<string, 2 | 3>;
// Now: [string, string] | [string, string, string] - correct!
```

## Complete Example

```typescript
// Type-safe comparison function
type Comparable<T> =
  [T] extends [Date] ? Date | number :  // Prevent distribution
  [T] extends [number] ? number :
  [T] extends [string] ? string :
  never;

declare function isLessThan<T>(a: T, b: Comparable<T>): boolean;

// Valid comparisons
isLessThan(new Date(), new Date());      // OK
isLessThan(new Date(), Date.now());      // OK (Date/number)
isLessThan(12, 23);                      // OK
isLessThan('A', 'B');                    // OK

// Invalid comparison - correctly rejected
isLessThan(12, 'B');  // Error: string not assignable to number

// Union case - correctly rejected
let dateOrStr: Date | string;
isLessThan(dateOrStr, 'B');  // Error: string not assignable to never
```

## Pressure Resistance Protocol

When conditional types behave unexpectedly:

1. **Check for distribution**: Is the type distributing over unions when it shouldn't?
2. **Test with boolean/never**: These often reveal distribution issues
3. **Wrap in one-tuple**: `[T] extends [X]` prevents distribution
4. **Add bare condition**: `N extends any` forces distribution
5. **Verify with unions**: Test your type with union inputs

## Red Flags

| Symptom | Cause | Fix |
|---------|-------|-----|
| `boolean` gives unexpected result | Distribution | Wrap in `[T]` |
| `never` gives `never` | Empty union | Wrap in `[T]` |
| Union doesn't split correctly | No distribution | Add bare `N extends` |
| Intersection wanted, union got | Distribution | Wrap in `[T]` |

## Common Rationalizations

### "I'll just use `any` for complex cases"

**Reality**: Understanding distribution gives you precise control. `any` sacrifices all type safety.

### "This is too complex for my use case"

**Reality**: The one-tuple trick is simple: `[T] extends [X]` vs `T extends X`. Learn it once, use it forever.

### "The type system shouldn't work this way"

**Reality**: Distribution is a powerful feature. Understanding it lets you harness that power rather than fight it.

## Quick Reference

| Goal | Syntax | Example |
|------|--------|---------|
| Allow distribution | `T extends X` | Default behavior |
| Prevent distribution | `[T] extends [X]` | For unions, boolean, never |
| Force distribution | `N extends any ? ... : never` | For recursive types |

## The Bottom Line

Distribution over unions is usually what you want, but not always. Use `[T] extends [X]` to prevent it and bare conditions to force it. Understand how `boolean` and `never` behave to avoid surprises.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 53: Know How to Control the Distribution of Unions over Conditional Types
