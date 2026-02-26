---
name: avoid-numeric-index
description: Use when defining array-like types. Use when tempted to use number as index type. Use when understanding array keys.
---

# Avoid Numeric Index Signatures

## Overview

**JavaScript object keys are always strings, even for arrays.**

TypeScript's numeric index signatures are a helpful fiction for catching mistakes, but they don't reflect JavaScript's runtime behavior. Use Array, tuple, or ArrayLike types instead.

## When to Use This Skill

- Defining array-like types
- Understanding JavaScript's array behavior
- Choosing between arrays and objects
- Working with Object.keys on arrays

## The Iron Rule

```
NEVER use number as an index signature type.
Use Array<T>, tuple, or ArrayLike<T> instead.
```

**Remember:**
- JavaScript converts all object keys to strings
- Array indices are strings at runtime
- `Object.keys` always returns strings
- TypeScript's number index is compile-time only

## Detection: The JavaScript Reality

```typescript
// JavaScript converts numeric keys to strings
const obj = { 1: 'one', 2: 'two' };
console.log(Object.keys(obj));  // ['1', '2'] - strings!

// Arrays work the same way
const arr = ['a', 'b', 'c'];
console.log(Object.keys(arr));  // ['0', '1', '2'] - strings!

// String access works on arrays
console.log(arr['1']);  // 'b' - same as arr[1]
```

## TypeScript's Helpful Fiction

TypeScript pretends arrays have numeric indices:

```typescript
interface Array<T> {
  [n: number]: T;  // Fiction: indices are actually strings
}

const xs = [1, 2, 3];
const x0 = xs[0];      // OK: number index
const x1 = xs['1'];    // OK: TypeScript allows stringified numbers

// TypeScript catches non-numeric string indices
const inputEl = document.querySelector('input')!;
const bad = xs[inputEl.value];
//          ~~~~~~~~~~~~~~~~~
// Index expression is not of type 'number'.
```

This is useful for catching mistakes, even though it's not technically accurate.

## Why Avoid Numeric Index Signatures

### Reality Leaks Through

```typescript
const xs = [1, 2, 3];
const keys = Object.keys(xs);
//    ^? const keys: string[]  (not number[]!)

for (const key of Object.keys(xs)) {
  console.log(typeof key);  // 'string', always
}
```

### Creates False Mental Model

```typescript
// This might make you think numeric keys are "real"
type NumericDict = { [key: number]: string };

// But at runtime:
const dict: NumericDict = { 0: 'zero', 1: 'one' };
console.log(Object.keys(dict));  // ['0', '1'] - strings!
```

## Better Alternatives

### Use Array<T> for Sequences

```typescript
// Instead of
type Bad = { [index: number]: string };

// Use
type Good = string[];  // or Array<string>
```

### Use Tuple for Fixed Length

```typescript
// Fixed-length numeric "index"
type Point = [number, number];        // 2 elements
type RGB = [number, number, number];  // 3 elements

const origin: Point = [0, 0];
```

### Use ArrayLike<T> for Array-like Structures

```typescript
// ArrayLike has length and numeric index signature
// Good for accepting any indexable collection
function sum(items: ArrayLike<number>): number {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i];
  }
  return total;
}

// Works with arrays
sum([1, 2, 3]);

// Works with array-like objects
sum({ 0: 1, 1: 2, 2: 3, length: 3 });

// Works with NodeList, arguments, etc.
```

### Use Iterable<T> for Iteration Only

```typescript
// If you only need to iterate, not index
function sumIterable(items: Iterable<number>): number {
  let total = 0;
  for (const item of items) {
    total += item;
  }
  return total;
}

// Works with arrays
sumIterable([1, 2, 3]);

// Works with Sets
sumIterable(new Set([1, 2, 3]));

// Works with generators
function* nums() { yield 1; yield 2; yield 3; }
sumIterable(nums());
```

## The String/Number Index Relationship

```typescript
// When you use a number index, you get T
// When you use Object.keys, you get string[]
// This inconsistency is intentional

const arr = [1, 2, 3];

// TypeScript: number index gives number
const first: number = arr[0];  // OK

// JavaScript reality: keys are strings
const keys = Object.keys(arr);  // string[]

// You can use string indices (TypeScript allows numeric strings)
const second = arr['1'];  // OK, TypeScript permits this
```

## Safe Array Access

```typescript
// Without noUncheckedIndexedAccess:
const arr = [1, 2, 3];
const x = arr[10];
//    ^? const x: number  (but actually undefined!)

// With noUncheckedIndexedAccess:
const y = arr[10];
//    ^? const y: number | undefined  (safer)

// Or use a wrapper function:
function checkedAccess<T>(xs: ArrayLike<T>, i: number): T {
  if (i >= 0 && i < xs.length) {
    return xs[i];
  }
  throw new Error(`Index ${i} out of bounds`);
}
```

## Pressure Resistance Protocol

### 1. "I Want a Sparse Array Type"

**Pressure:** "I need `{ [n: number]: T }` for a sparse array"

**Response:** Use `Map<number, T>` for sparse data, or regular arrays with optional access.

**Action:** `new Map<number, string>()` for sparse numeric keys.

### 2. "I Need Numeric Keys for My Object"

**Pressure:** "My object uses IDs as keys: `{ 1: user1, 2: user2 }`"

**Response:** Use `Map<number, User>` or `Record<string, User>` and convert.

**Action:** Embrace that keys are strings, or use Map.

## Red Flags - STOP and Reconsider

- `{ [key: number]: T }` in your own types
- Assuming `Object.keys(array)` returns numbers
- Using numeric strings as array indices
- Confusion about why `typeof key` is 'string'

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Arrays have numeric indices" | At runtime, they're strings |
| "TypeScript uses number in Array<T>" | It's a convenient fiction for type safety |
| "I need sparse numeric keys" | Use Map<number, T> instead |

## Quick Reference

```typescript
// DON'T: Numeric index signature
type Bad = { [n: number]: string };

// DO: Use Array for sequences
type Good = string[];

// DO: Use tuple for fixed length
type Point = [number, number];

// DO: Use ArrayLike for indexable collections
function process(items: ArrayLike<string>) { ... }

// DO: Use Iterable for anything you can loop over
function process(items: Iterable<string>) { ... }

// DO: Use Map for sparse numeric keys
const sparse = new Map<number, string>();
```

## The Bottom Line

**Numeric index signatures are a TypeScript convenience, not JavaScript reality.**

JavaScript object keys are always strings. TypeScript's numeric indices help catch mistakes but create a false mental model. Use Array, tuple, ArrayLike, or Map instead of defining your own numeric index signatures.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 17: Avoid Numeric Index Signatures.
