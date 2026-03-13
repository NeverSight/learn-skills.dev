---
name: precise-any-variants
description: Use when forced to use any. Use when any is too broad. Use when function types need any.
---

# Prefer More Precise Variants of any to Plain any

## Overview

**If you must use any, make it as specific as possible.**

Plain `any` accepts everything. But `any[]`, `Record<string, any>`, or `() => any` are narrower and still provide some type checking.

## When to Use This Skill

- Forced to use any for some reason
- Writing functions that accept "anything"
- Dealing with truly dynamic data
- Migrating from JavaScript

## The Iron Rule

```
any is a last resort.
Specific variants of any preserve partial type safety.
```

**Remember:**
- `any[]` checks that it's an array
- `Record<string, any>` checks that it's an object
- `() => any` checks that it's a function
- `unknown` is even safer than any variant

## Detection: Over-broad any

```typescript
function getLength(x: any) {  // Too broad!
  return x.length;
}

getLength(123);     // No error, crashes at runtime
getLength(null);    // No error, crashes at runtime
getLength([1,2,3]); // OK
```

## Better: Specific any Variants

### any[] for Arrays

```typescript
function getLength(array: any[]) {
  return array.length;  // Type checked!
}

getLength([1, 2, 3]);  // OK
getLength(/regex/);
//        ~~~~~~~
// Argument of type 'RegExp' is not assignable to parameter of type 'any[]'
```

Benefits:
- `.length` access is type-checked
- Return type is `number`, not `any`
- Non-arrays are rejected

### Record<string, any> for Objects

```typescript
function hasKey(obj: Record<string, any>, key: string): boolean {
  return key in obj;
}

hasKey({ a: 1 }, 'a');  // OK
hasKey(null, 'a');
//     ~~~~
// Argument of type 'null' is not assignable to parameter of type 'Record<string, any>'
```

### () => any for Functions

```typescript
type Fn0 = () => any;           // No params
type Fn1 = (arg: any) => any;   // One param
type FnN = (...args: any[]) => any;  // Any params

function callTwice(fn: FnN) {
  fn();
  fn();
}

callTwice(() => console.log('hi'));  // OK
callTwice(123);
//        ~~~
// Argument of type 'number' is not assignable to parameter of type '(...args: any[]) => any'
```

## Use any[] for Rest Parameters

```typescript
// any rest parameter: return type is any
const numArgsBad = (...args: any) => args.length;
//    ^? (...args: any) => any

// any[] rest parameter: return type is number
const numArgsBetter = (...args: any[]) => args.length;
//    ^? (...args: any[]) => number
```

The return type matters for downstream code!

## Comparison of any Variants

| Type | Accepts | Rejects |
|------|---------|---------|
| `any` | Everything | Nothing |
| `any[]` | Arrays | Non-arrays |
| `Record<string, any>` | Objects | Primitives, null |
| `() => any` | Functions | Non-functions |
| `object` | Objects, arrays | Primitives, null |
| `unknown` | Everything | Everything (without check) |

## Consider unknown Instead

`unknown` is even safer:

```typescript
function process(data: unknown) {
  // Must narrow before using
  if (Array.isArray(data)) {
    data.length;  // OK, data is any[]
  }
  if (typeof data === 'object' && data !== null) {
    // data is object
  }
}
```

With `unknown`, you can't do anything without first checking the type.

## Real-World Example: JSON Parsing

```typescript
// Don't return any
function parseBad(json: string): any {
  return JSON.parse(json);
}

// Better: return unknown
function parseGood(json: string): unknown {
  return JSON.parse(json);
}

// Caller must narrow:
const data = parseGood('{"x": 1}');
if (typeof data === 'object' && data !== null && 'x' in data) {
  console.log(data.x);
}
```

## When any is Unavoidable

Sometimes you genuinely need any:

```typescript
// Wrapping a library that uses any internally
function wrapLibrary<T>(input: T): T {
  return (library as any).process(input);
}

// Type assertion in implementation
function merge<T>(a: Partial<T>, b: Partial<T>): T {
  return { ...a, ...b } as any as T;
}
```

Even then, hide it inside functions with good type signatures (Item 45).

## Pressure Resistance Protocol

### 1. "any Works"

**Pressure:** "Just use any and move on"

**Response:** any disables ALL type checking. Specific variants preserve some safety.

**Action:** Use the most specific variant that works.

### 2. "I Don't Know the Type"

**Pressure:** "The type is truly dynamic"

**Response:** unknown is safer for truly unknown types.

**Action:** Use unknown, then narrow before using.

## Red Flags - STOP and Reconsider

- `any` as function parameter (use specific variant)
- `any` as return type (prefer unknown)
- `any` for objects (use Record<string, any> or object)
- `any` for arrays (use any[])

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's too dynamic to type" | unknown handles truly dynamic data |
| "Specific variants are verbose" | A few characters save runtime errors |
| "any is fine for internal code" | Internal code still has bugs |

## Quick Reference

```typescript
// DON'T: Plain any
function f(x: any): any { ... }

// DO: Specific variants
function getLength(arr: any[]): number { ... }
function getKeys(obj: Record<string, any>): string[] { ... }
function call(fn: (...args: any[]) => any): void { ... }

// BEST: unknown when possible
function process(data: unknown): void {
  if (Array.isArray(data)) { ... }
}
```

## The Bottom Line

**If you must use any, make it specific.**

`any[]`, `Record<string, any>`, and `() => any` preserve some type checking while still allowing flexibility. But consider whether `unknown` is a safer choice.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 44: Prefer More Precise Variants of any to Plain any.
