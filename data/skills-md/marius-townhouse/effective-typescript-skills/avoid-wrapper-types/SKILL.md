---
name: avoid-wrapper-types
description: Use when typing primitives. Use when tempted to use String, Number, Boolean. Use when wrapper types appear in errors.
---

# Avoid Object Wrapper Types (String, Number, Boolean, Symbol, BigInt)

## Overview

**Use lowercase primitive types, never uppercase wrapper types.**

JavaScript has primitive types (`string`, `number`, `boolean`) and object wrapper types (`String`, `Number`, `Boolean`). TypeScript has types for both, but you should almost never use the wrapper types.

## When to Use This Skill

- Typing any primitive value
- Seeing errors about wrapper type mismatches
- Understanding why `String !== string`
- Working with methods on primitives

## The Iron Rule

```
ALWAYS use lowercase: string, number, boolean, symbol, bigint
NEVER use uppercase: String, Number, Boolean, Symbol, BigInt
```

**Remember:**
- Wrappers are objects, primitives are not
- TypeScript freely accepts primitives where wrappers expected
- TypeScript does NOT accept wrappers where primitives expected
- Methods work on primitives via auto-boxing

## Detection: The Wrapper Trap

```typescript
// These look similar but behave differently
const primitive: string = "hello";
const wrapper: String = new String("hello");

// Equality fails
primitive === wrapper;  // false (different types)
wrapper === wrapper;    // Wait, this is also comparing to itself...

const s1 = new String("hello");
const s2 = new String("hello");
s1 === s2;  // false! Each wrapper is a unique object
```

## How Primitive Methods Work

Primitives don't have methods, but this works:

```typescript
'primitive'.charAt(3);  // 'm' - how?
```

JavaScript auto-boxes:
1. Creates temporary `String` wrapper
2. Calls method on wrapper
3. Discards wrapper
4. Returns result

You get convenience without the wrapper's drawbacks.

## The Type Assignment Problem

```typescript
// Primitive assignable to wrapper (OK but don't do this)
const s: String = "primitive";  // Works

// Wrapper NOT assignable to primitive (Error)
function takesString(s: string) { }
takesString(new String("hello"));
//          ~~~~~~~~~~~~~~~~~~~
// Argument of type 'String' is not assignable to parameter of type 'string'.
// 'string' is a primitive, but 'String' is a wrapper object.
```

## All Primitive Types

| Primitive (USE) | Wrapper (AVOID) |
|-----------------|-----------------|
| `string` | `String` |
| `number` | `Number` |
| `boolean` | `Boolean` |
| `symbol` | `Symbol` |
| `bigint` | `BigInt` |

Note: `null` and `undefined` don't have wrapper types.

## Why Wrappers Are Problematic

### Identity Issues

```typescript
const s1 = new String("hello");
const s2 = new String("hello");

s1 == s2;   // false
s1 === s2;  // false
// Each is a distinct object
```

### typeof Confusion

```typescript
typeof "hello";              // "string"
typeof new String("hello");  // "object"
```

### Truthiness Gotchas

```typescript
const falsy = new Boolean(false);
if (falsy) {
  console.log("This runs!"); // Wrapper objects are always truthy
}
```

## Exception: Runtime Methods

You can use wrappers for their static methods:

```typescript
// These are fine - not creating wrapper objects
String.fromCharCode(65);  // "A"
Number.isNaN(x);
BigInt(123);              // Creates primitive, not wrapper
```

But never use them as types or create instances.

## Pressure Resistance Protocol

### 1. "I Need String Methods"

**Pressure:** "I want to use String methods, so I'll type it as String"

**Response:** Primitive `string` has all the same methods via auto-boxing.

**Action:** Use `string` type. Methods just work.

### 2. "TypeScript Inferred String (Uppercase)"

**Pressure:** "TypeScript gave me `String`, so it must be right"

**Response:** Check your code - you might be creating a wrapper accidentally.

**Action:** Find and fix the source. Use lowercase.

## Red Flags - STOP and Reconsider

- Uppercase `String`, `Number`, `Boolean` in type annotations
- `new String()`, `new Number()`, `new Boolean()` anywhere
- Errors about wrapper vs primitive assignment
- `typeof x === "object"` when expecting a primitive

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "String has more methods" | No, both have identical methods |
| "I need an object" | You rarely do; primitives are simpler |
| "It's the same thing" | No, wrappers have identity and truthiness issues |

## Quick Reference

```typescript
// ALWAYS use these
const s: string = "hello";
const n: number = 42;
const b: boolean = true;
const sym: symbol = Symbol();
const big: bigint = 9007199254740991n;

// NEVER use these
const s: String = "hello";   // Wrong
const n: Number = 42;        // Wrong
const b: Boolean = true;     // Wrong
```

## The Bottom Line

**Always use lowercase primitive types.**

There's never a good reason to use `String`, `Number`, or `Boolean` as types. The uppercase versions cause assignment errors, have identity issues, and provide no benefits over the lowercase primitives.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 10: Avoid Object Wrapper Types (String, Number, Boolean, Symbol, BigInt).
