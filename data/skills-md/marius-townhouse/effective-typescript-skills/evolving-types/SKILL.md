---
name: evolving-types
description: Use when types change as code executes. Use when arrays are built incrementally. Use when working with any[] that narrows.
---

# Understand Evolving Types

## Overview

**Some variables start with broad types and narrow as TypeScript sees values added.**

This is an exception to the rule that types don't change. Variables initialized without a value, or as empty arrays, can have "evolving" types that narrow based on what you assign to them.

## When to Use This Skill

- Variables initialized to `null` or `undefined`
- Arrays that start empty and get values pushed
- Variables that start as `any` and narrow
- Understanding when explicit annotations are better

## The Iron Rule

```
Evolving types work but are fragile.
Prefer explicit annotations for clarity.
```

**Remember:**
- Only applies to variables without initial typed values
- Type evolves based on assignments
- Final type is only valid after all assignments
- Explicit annotation is often clearer

## Detection: The Evolving any

```typescript
const result = [];  // any[]
result.push('a');   // string[]
result.push(1);     // (string | number)[]

result
// ^? (string | number)[]
```

The type evolves with each `push`.

## How Evolving Types Work

### Uninitialized Variables

```typescript
let val;  // any (evolving)
val
// ^? let val: any

if (Math.random() < 0.5) {
  val = /hello/;
  val
  // ^? let val: RegExp
} else {
  val = 12;
  val
  // ^? let val: number
}
val
// ^? let val: number | RegExp
```

TypeScript tracks assignments and computes the union.

### Empty Arrays

```typescript
const arr = [];  // any[] (evolving)
arr.push(1);
arr
// ^? number[]

arr.push('hello');
arr
// ^? (string | number)[]
```

### null or undefined Initial Value

```typescript
let x = null;  // any (evolving)
x
// ^? null

x = 12;
x
// ^? number
```

## When Types Stop Evolving

Once a variable leaves its scope or is used in a function, its type is fixed:

```typescript
function buildArray() {
  const arr = [];
  arr.push(1);
  arr.push(2);
  return arr;  // Type fixed as number[]
}

const myArray = buildArray();
myArray.push('hello');  // Error if return type is number[]
```

## Problems with Evolving Types

### Order Matters

```typescript
const arr = [];
arr.push(1);
// arr is number[] here

// If this line is later:
arr.push('hello');
// arr is (string | number)[] but earlier uses assumed number[]
```

### Implicit any

With `noImplicitAny`, empty arrays without annotation get `any[]`:

```typescript
const values = [];  // Implicit any[] - may cause lint warnings
```

### Fragile Inference

```typescript
let x = null;
x = 'hello';
x = 42;  // Now it's string | number

// Later, someone adds:
x = true;  // Now it's string | number | boolean

// All code using x must handle all possibilities
```

## Better: Explicit Annotations

```typescript
// Clear intent, stable type
const result: number[] = [];
result.push(1);
result.push(2);
// result is always number[]

// Prevents accidents
result.push('hello');
//          ~~~~~~~
// Argument of type 'string' is not assignable to 'number'
```

## When Evolving Types Are OK

### Short, Simple Loops

```typescript
const squares = [];
for (let i = 0; i < 5; i++) {
  squares.push(i * i);
}
// squares: number[] is clear from context
```

### Accumulating Known Types

```typescript
let result = null;
for (const item of items) {
  if (condition(item)) {
    result = item;
    break;
  }
}
// result evolves to ItemType | null
```

## Functional Alternatives

Instead of evolving arrays, prefer functional constructs:

```typescript
// Don't:
const doubled = [];
for (const n of numbers) {
  doubled.push(n * 2);
}

// Do:
const doubled = numbers.map(n => n * 2);
// ^? number[]
```

Type is inferred directly, no evolution needed.

## Real-World Example

```typescript
// Evolving (works but fragile)
async function fetchData() {
  let data;
  try {
    const response = await fetch('/api');
    data = await response.json();
  } catch (e) {
    data = null;
  }
  return data;  // any
}

// Better: explicit
async function fetchData(): Promise<Data | null> {
  try {
    const response = await fetch('/api');
    return await response.json();
  } catch (e) {
    return null;
  }
}
```

## Pressure Resistance Protocol

### 1. "Evolving Types Work"

**Pressure:** "TypeScript figures it out automatically"

**Response:** It's fragile and can change unexpectedly with new code.

**Action:** Add explicit annotation for stability.

### 2. "I Don't Know the Type Yet"

**Pressure:** "The type depends on runtime conditions"

**Response:** You know the possible types; declare them.

**Action:** Use union type: `let x: string | number | null = null;`

## Red Flags - STOP and Reconsider

- `const arr = []` without annotation
- `let x = null` or `let x` without annotation
- Types that change based on assignment order
- `any[]` warnings in lint

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "TypeScript infers it" | It infers something, not necessarily what you want |
| "I'll add types later" | Later never comes; add them now |
| "It's just temporary" | Temporary code becomes permanent |

## Quick Reference

```typescript
// EVOLVING (works but fragile)
const arr = [];       // any[]
arr.push(1);          // number[]
arr.push('a');        // (string | number)[]

// BETTER (stable and clear)
const arr: number[] = [];
arr.push(1);
arr.push('a');  // Error!

// BEST (functional)
const arr = items.map(item => item.value);
// Type inferred correctly
```

## The Bottom Line

**Evolving types are a convenience, not a best practice.**

While TypeScript can track types through assignments, explicit annotations are clearer and more robust. Use evolving types only for simple, localized code. For anything else, declare your intent with annotations.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 25: Understand Evolving Types.
