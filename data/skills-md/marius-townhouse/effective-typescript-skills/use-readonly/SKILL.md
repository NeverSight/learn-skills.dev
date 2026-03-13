---
name: use-readonly
description: Use when passing arrays or objects to functions. Use when mutation bugs occur. Use when wanting to signal that data should not be modified.
---

# Use readonly to Avoid Errors Associated with Mutation

## Overview

**readonly signals intent and lets TypeScript catch accidental mutations.**

Mutation is a common source of bugs. readonly helps TypeScript catch them at compile time and documents your intent to other developers.

## When to Use This Skill

- Passing arrays or objects to functions
- Debugging unexpected data changes
- Designing function signatures
- Working with shared state
- Creating APIs that shouldn't mutate inputs

## The Iron Rule

```
NEVER mutate function parameters unless mutation is the explicit purpose.
```

**No exceptions:**
- Not for "it's more efficient"
- Not for "no one else uses this data"
- Not for "I'll remember not to mutate"

## Detection: The "Mutation Smell"

If a function receives an array or object and modifies it, consider if that's intended.

```typescript
// ❌ VIOLATION: Function mutates its input
function printTriangles(n: number[]) {
  n.sort((a, b) => a - b);  // Mutates the original array!
  console.log(n);
}

const nums = [5, 3, 8, 1];
printTriangles(nums);
console.log(nums);  // [1, 3, 5, 8] - Original changed!

// ✅ CORRECT: Use readonly to prevent mutation
function printTriangles(n: readonly number[]) {
  n.sort((a, b) => a - b);
  // ~~~~ Property 'sort' does not exist on 'readonly number[]'
}
```

## readonly for Arrays

```typescript
// readonly number[] - can read, cannot modify
function sum(arr: readonly number[]): number {
  arr.push(1);        // Error: Property 'push' does not exist
  arr[0] = 5;         // Error: Index signature only permits reading
  return arr.reduce((a, b) => a + b, 0);  // OK: reading is fine
}

// If you need to modify, copy first:
function sortedCopy(arr: readonly number[]): number[] {
  return [...arr].sort((a, b) => a - b);  // Copy, then sort
  // Or use toSorted() which doesn't mutate:
  return arr.toSorted((a, b) => a - b);
}
```

## readonly for Objects

```typescript
interface Point {
  x: number;
  y: number;
}

// Readonly<T> makes all properties readonly
function movePoint(p: Readonly<Point>, dx: number, dy: number): Point {
  p.x += dx;  // Error: Cannot assign to 'x' because it is a read-only property
  
  // Return a new object instead
  return { x: p.x + dx, y: p.y + dy };
}
```

## readonly Properties

```typescript
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

const config: Config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};

config.apiUrl = 'https://other.com';  // Error: Cannot assign to read-only property
```

## readonly is Shallow

```typescript
interface Outer {
  readonly inner: { value: number };
}

const obj: Outer = { inner: { value: 1 } };
obj.inner = { value: 2 };        // Error: readonly
obj.inner.value = 2;             // OK! Nested object is not readonly

// For deep readonly, use DeepReadonly utility or as const
const deepObj = {
  inner: { value: 1 }
} as const;
// ^? const deepObj: { readonly inner: { readonly value: 1 } }
```

## Pressure Resistance Protocol

### 1. "It's More Efficient"

**Pressure:** "Copying arrays is slow, mutation is faster"

**Response:** Correctness > micro-optimization. If perf matters, measure first.

**Action:** Use readonly by default. Only mutate after profiling shows a real need.

### 2. "I Control All the Callers"

**Pressure:** "No one else calls this function"

**Response:** Code evolves. You won't remember this in 6 months.

**Action:** Design for the future. readonly is documentation that lasts.

### 3. "readonly Is Too Verbose"

**Pressure:** "Adding readonly everywhere is tedious"

**Response:** It's a one-time cost. The bugs it prevents save time.

**Action:** Start with function parameters. Expand from there.

## readonly vs Immutable

```typescript
// readonly is a compile-time check, not a runtime guarantee
const arr: readonly number[] = [1, 2, 3];

// TypeScript prevents this:
arr.push(4);  // Error

// But at runtime, it's still a regular array:
(arr as number[]).push(4);  // Works at runtime!

// For true immutability, use Object.freeze():
const frozen = Object.freeze([1, 2, 3]);
// ^? const frozen: readonly number[]
```

## Red Flags - STOP and Reconsider

- Functions that `.push()`, `.sort()`, or `.splice()` on parameters
- Comments like "// Don't modify this array"
- Bugs where data changes unexpectedly
- Shared state modified by multiple functions
- Parameters reassigned within functions

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's just an internal function" | Internal code needs correctness too. |
| "Copying is expensive" | Prove it with benchmarks first. |
| "I'll document it" | Types are better documentation than comments. |
| "TypeScript is too strict" | TypeScript is protecting you from mutation bugs. |

## Quick Reference

| You Have | Use | Effect |
|----------|-----|--------|
| `number[]` parameter | `readonly number[]` | Prevents mutations |
| Object parameter | `Readonly<T>` | Shallow readonly |
| Deep nesting | `as const` | Deep readonly |
| Array return value | `readonly T[]` | Signals immutability |

## The Immutable Pattern

```typescript
// Instead of mutating, return new values:

// ❌ Mutating
function addItem(arr: string[], item: string) {
  arr.push(item);
}

// ✅ Immutable
function addItem(arr: readonly string[], item: string): string[] {
  return [...arr, item];
}

// ❌ Mutating object
function updateUser(user: User, name: string) {
  user.name = name;
}

// ✅ Immutable
function updateUser(user: Readonly<User>, name: string): User {
  return { ...user, name };
}
```

## The Bottom Line

**readonly is a contract that TypeScript enforces.**

Use it on function parameters to prevent accidental mutation. Use it on properties that shouldn't change. Let TypeScript catch mutation bugs at compile time instead of debugging them at runtime.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 14: Use readonly to Avoid Errors Associated with Mutation.
