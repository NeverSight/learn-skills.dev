---
name: functional-constructs-types
description: Use when building arrays in loops. Use when types don't flow through code. Use when considering map/filter/reduce.
---

# Use Functional Constructs and Libraries to Help Types Flow

## Overview

**Functional programming constructs (map, filter, reduce) work better with TypeScript than imperative loops.**

TypeScript's type inference works particularly well with functional constructs. They produce intermediate types that flow naturally, whereas loops require you to manually track types.

## When to Use This Skill

- Building arrays with for loops
- Transforming data structures
- Types not flowing through imperative code
- Choosing between loops and functional methods

## The Iron Rule

```
Prefer map, filter, and reduce over for loops.
Types flow naturally through functional chains.
```

**Remember:**
- Functional methods return typed values
- Loops require manual type management
- Chaining preserves type context
- Libraries like Lodash have excellent type support

## Detection: Loop Type Problems

```typescript
// Loop: type must be declared or evolves
const result: string[] = [];
for (const item of items) {
  result.push(item.name);
}

// What if you forget the annotation?
const result = [];  // any[]
for (const item of items) {
  result.push(item.name);
}
result
// ^? any[] - type information lost
```

## The Functional Solution

```typescript
const result = items.map(item => item.name);
// ^? string[] - type inferred automatically
```

TypeScript infers the output type from the input type and the mapping function.

## Type Flow Through Chains

```typescript
const namesOfAdults = people
  .filter(p => p.age >= 18)
  // ^? Person[]
  .map(p => p.name)
  // ^? string[]
  .sort()
  // ^? string[]
  .join(', ');
  // ^? string
```

Each step has a well-defined type that TypeScript tracks.

## Common Transformations

### map: Transform Each Element

```typescript
const numbers = [1, 2, 3];
const doubled = numbers.map(n => n * 2);
// ^? number[]

const users = [{ name: 'Alice', age: 30 }];
const names = users.map(u => u.name);
// ^? string[]
```

### filter: Keep Elements Matching Condition

```typescript
const numbers = [1, 2, 3, 4, 5];
const evens = numbers.filter(n => n % 2 === 0);
// ^? number[]

// With type guard for narrowing
const mixed: (string | number)[] = [1, 'a', 2, 'b'];
const strings = mixed.filter((x): x is string => typeof x === 'string');
// ^? string[]
```

### reduce: Aggregate to Single Value

```typescript
const numbers = [1, 2, 3, 4, 5];
const sum = numbers.reduce((acc, n) => acc + n, 0);
// ^? number

const grouped = items.reduce((acc, item) => {
  const key = item.category;
  acc[key] = acc[key] || [];
  acc[key].push(item);
  return acc;
}, {} as Record<string, Item[]>);
// Note: reduce sometimes needs type hints
```

### flatMap: Map and Flatten

```typescript
const nested = [[1, 2], [3, 4], [5]];
const flat = nested.flatMap(arr => arr);
// ^? number[]

const sentences = ['Hello world', 'TypeScript rocks'];
const words = sentences.flatMap(s => s.split(' '));
// ^? string[]
```

## Object Transformations

### Object.entries / Object.fromEntries

```typescript
const obj = { a: 1, b: 2, c: 3 };

// Transform values
const doubled = Object.fromEntries(
  Object.entries(obj).map(([k, v]) => [k, v * 2])
);
// ^? { [k: string]: number }

// Filter entries
const filtered = Object.fromEntries(
  Object.entries(obj).filter(([k, v]) => v > 1)
);
```

### Record Transformations

```typescript
type Input = Record<string, number>;
type Output = Record<string, string>;

const input: Input = { a: 1, b: 2 };
const output: Output = Object.fromEntries(
  Object.entries(input).map(([k, v]) => [k, String(v)])
);
```

## Lodash and Type-Friendly Libraries

```typescript
import _ from 'lodash';

const grouped = _.groupBy(users, 'department');
// ^? Dictionary<User[]>

const sorted = _.sortBy(users, ['lastName', 'firstName']);
// ^? User[]

const unique = _.uniqBy(users, 'id');
// ^? User[]
```

Lodash has excellent TypeScript support.

## When Loops Are OK

### Performance-Critical Code

```typescript
// Loop might be faster for very large arrays
let sum = 0;
for (let i = 0; i < numbers.length; i++) {
  sum += numbers[i];
}
```

### Early Exit

```typescript
// find is functional, but loops can break early
function findFirst<T>(arr: T[], pred: (x: T) => boolean): T | undefined {
  for (const item of arr) {
    if (pred(item)) return item;
  }
  return undefined;
}
// Or just use: arr.find(pred)
```

### Complex Mutations

```typescript
// Some algorithms are clearer with loops
function quickSort<T>(arr: T[]): T[] {
  // ... loop-based implementation
}
```

## Converting Loops to Functional

```typescript
// Before: loop with accumulator
const result: ProcessedItem[] = [];
for (const item of items) {
  if (item.isValid) {
    result.push(processItem(item));
  }
}

// After: filter + map
const result = items
  .filter(item => item.isValid)
  .map(item => processItem(item));
```

## Pressure Resistance Protocol

### 1. "Loops Are More Readable"

**Pressure:** "I understand for loops better"

**Response:** Functional methods express intent clearly: map = transform, filter = select, reduce = aggregate.

**Action:** Learn the patterns. They become natural quickly.

### 2. "Performance Concerns"

**Pressure:** "Multiple passes are slower"

**Response:** For most data sizes, clarity beats micro-optimization.

**Action:** Profile before optimizing. Most code isn't performance-critical.

## Red Flags - STOP and Reconsider

- `const result = []` followed by loop pushing elements
- Type annotations needed only because of loops
- Complex state tracking in loops
- `any[]` that should be more specific

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Loops are simpler" | Functional methods have clearer intent |
| "I need the index" | `.map((item, i) => ...)` provides index |
| "Multiple passes are slow" | Usually doesn't matter; measure first |

## Quick Reference

```typescript
// DON'T: Loop with manual type
const result: string[] = [];
for (const x of items) {
  result.push(x.name);
}

// DO: Functional with inferred type
const result = items.map(x => x.name);

// Filter + Map
const processed = items
  .filter(x => x.isValid)
  .map(x => transform(x));

// Type guard in filter
const strings = mixed.filter((x): x is string => typeof x === 'string');

// Reduce (with type hint when needed)
const grouped = items.reduce((acc, x) => ..., {} as GroupedType);
```

## The Bottom Line

**Functional constructs make types flow naturally.**

`map`, `filter`, `reduce`, and similar methods produce well-typed results without manual annotation. They express transformations clearly and work excellently with TypeScript's inference. Use loops only when you have a specific reason to.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 26: Use Functional Constructs and Libraries to Help Types Flow.
