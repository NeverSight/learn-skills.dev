---
name: distinct-special-values
description: Use when tempted to use -1 or "" as special values. Use when indexOf returns -1. Use when special cases need representation.
---

# Use a Distinct Type for Special Values

## Overview

**Don't use -1, 0, or "" as special values. Use null or a distinct type.**

When a function can fail or have a special case, represent it with a type that TypeScript can distinguish, not an in-domain value like -1 that's just a regular number.

## When to Use This Skill

- Functions that can fail (not found, error, etc.)
- Values that have a "missing" or "unknown" state
- Wrapping APIs that use sentinel values like -1
- Designing your own return types

## The Iron Rule

```
Special cases deserve distinct types.
Use null, undefined, or tagged unions - not -1 or "".
```

**Remember:**
- -1 is just a number, indistinguishable from other numbers
- TypeScript can't protect you from special values
- null and undefined are trackable
- Explicit error states are clearer than magic numbers

## Detection: The -1 Trap

```typescript
function splitAround<T>(vals: readonly T[], val: T): [T[], T[]] {
  const index = vals.indexOf(val);
  return [vals.slice(0, index), vals.slice(index + 1)];
}

splitAround([1, 2, 3, 4, 5], 6);
// Expected: error or [[1,2,3,4,5], []]
// Actual: [[1,2,3,4], [1,2,3,4,5]] (!)
```

Why? `indexOf` returns -1 for "not found", but -1 is a valid array index (counts from end).

## Solution: Wrap with Distinct Type

```typescript
function safeIndexOf<T>(vals: readonly T[], val: T): number | null {
  const index = vals.indexOf(val);
  return index === -1 ? null : index;
}
```

Now TypeScript forces you to handle both cases:

```typescript
function splitAround<T>(vals: readonly T[], val: T): [T[], T[]] {
  const index = safeIndexOf(vals, val);
  return [vals.slice(0, index), vals.slice(index + 1)];
  //                   ~~~~~             ~~~~~ 
  // 'index' is possibly 'null'
}
```

Fixed version:

```typescript
function splitAround<T>(vals: readonly T[], val: T): [T[], T[]] {
  const index = safeIndexOf(vals, val);
  if (index === null) {
    return [[...vals], []];
  }
  return [vals.slice(0, index), vals.slice(index + 1)];
}
```

## Real-World Example: Product Price

```typescript
// Bad: -1 means "unknown price"
interface Product {
  title: string;
  /** Price in dollars, or -1 if price is unknown */
  priceDollars: number;
}

// Disaster waiting to happen:
function getTotal(products: Product[]) {
  return products.reduce((sum, p) => sum + p.priceDollars, 0);
  // Whoops: products with unknown price make total negative!
}
```

Better:

```typescript
interface Product {
  title: string;
  priceDollars: number | null;
}

function getTotal(products: Product[]) {
  return products.reduce((sum, p) => {
    if (p.priceDollars === null) {
      throw new Error(`Unknown price for ${p.title}`);
    }
    return sum + p.priceDollars;
  }, 0);
}
```

## Why strictNullChecks Matters

Using -1 as a special value is like disabling strictNullChecks:

```typescript
// @strictNullChecks: false
const truck: Product = {
  title: 'Tesla Cybertruck',
  priceDollars: null,  // ok with strictNullChecks off
};
```

When strictNullChecks is on, TypeScript distinguishes `number` from `number | null`. Using -1 as "unknown" bypasses this safety.

## When to Use Tagged Unions

If null/undefined isn't clear enough, use a tagged union:

```typescript
type RequestResult<T> = 
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
  | { status: 'pending' };

function fetchUser(id: string): RequestResult<User> {
  // ...
}

const result = fetchUser('123');
if (result.status === 'success') {
  console.log(result.data.name);  // TypeScript knows data exists
}
```

## Common Sentinel Values to Avoid

| Sentinel | Problem | Alternative |
|----------|---------|-------------|
| -1 (indexOf) | Valid array index | null |
| 0 | Valid number | null |
| "" | Valid string | null |
| [] | Valid array | null |
| {} | Valid object | null |
| NaN | number type | null or throw |

## Pressure Resistance Protocol

### 1. "JavaScript Uses -1"

**Pressure:** "indexOf returns -1, I should match that pattern"

**Response:** JavaScript's -1 is a historical mistake. Wrap it.

**Action:** Create wrapper returning `T | null`.

### 2. "It's Just a Placeholder"

**Pressure:** "We'll never actually use that value"

**Response:** Someone will forget. TypeScript won't protect you.

**Action:** Use a distinct type that TypeScript can track.

## Red Flags - STOP and Reconsider

- Magic numbers like -1, 0, or -999
- Empty strings meaning "no value"
- Comments explaining special values
- Bugs from forgetting to check for special values

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's a common pattern" | Common doesn't mean good |
| "Performance is better" | Marginal at best; safety matters more |
| "TypeScript can't track null" | Yes it can, that's the point! |

## Quick Reference

```typescript
// DON'T: Sentinel values
function indexOf(arr, val): number { ... }  // -1 means not found
function getPrice(): number { ... }  // -1 means unknown

// DO: Distinct types
function indexOf(arr, val): number | null { ... }
function getPrice(): number | null { ... }

// DO: Tagged unions for complex states
type Result<T> = { ok: true; value: T } | { ok: false; error: string };
```

## The Bottom Line

**Special cases deserve special types.**

Using -1 or "" as special values bypasses TypeScript's type system. Use null, undefined, or tagged unions to represent special cases. TypeScript will then force you to handle them correctly.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 36: Use a Distinct Type for Special Values.
