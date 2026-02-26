---
name: understand-type-widening
description: Use when confused why TypeScript infers general types. Use when const vs let gives different types. Use when literals become string or number.
---

# Understand Type Widening

## Overview

**When TypeScript infers a type from a value, it often widens it.**

A variable initialized with `"x"` could be intended to hold any string, or just the literal `"x"`. TypeScript guesses using heuristics, and understanding these helps you write predictable code.

## When to Use This Skill

- Confused why a type is `string` instead of `"specific-value"`
- `const` and `let` give different types for the same value
- Array literals get unexpected element types
- Object properties are wider than expected
- Type errors about literals not being assignable

## The Iron Rule

```
ALWAYS understand how your declaration style affects inferred types.
```

**Remember:**
- `let` variables widen literals to their base type
- `const` variables keep literal types (for primitives)
- Object/array contents widen even with `const`
- Use `as const` for full literal inference

## Detection: The Widening Surprise

If TypeScript infers a broader type than you expected, you're seeing widening.

```typescript
// Primitive widening with let
let x = 'x';
//  ^? let x: string  (not "x")

// No widening with const (for primitives)
const y = 'y';
//    ^? const y: "y"

// But object properties still widen
const obj = { x: 1, y: 2 };
//    ^? const obj: { x: number; y: number }  (not { x: 1, y: 2 })
```

## Why Widening Exists

TypeScript must balance two goals:
1. **Specificity** - Catch real bugs with narrow types
2. **Flexibility** - Allow reasonable mutations

```typescript
// Without widening, this would fail:
let x = 'x';  // If inferred as "x", then...
x = 'y';      // Error! "y" is not assignable to "x"

// With widening:
let x = 'x';  // Inferred as string
x = 'y';      // OK
```

## The Widening Rules

### Rule 1: `let` Widens, `const` Preserves (Primitives)

```typescript
// let → widened
let a = 'hello';
//  ^? let a: string

let b = 42;
//  ^? let b: number

let c = true;
//  ^? let c: boolean

// const → literal
const d = 'hello';
//    ^? const d: "hello"

const e = 42;
//    ^? const e: 42

const f = true;
//    ^? const f: true
```

### Rule 2: Object Properties Always Widen

```typescript
const point = { x: 3, y: 4 };
//    ^? const point: { x: number; y: number }

// Not { x: 3, y: 4 } - because you might do:
point.x = 10;  // This must be valid
```

### Rule 3: Array Elements Widen

```typescript
const arr = [1, 2, 3];
//    ^? const arr: number[]

// Not [1, 2, 3] or readonly [1, 2, 3]
```

### Rule 4: Mixed Arrays Get Union Types

```typescript
const mixed = [1, 'x'];
//    ^? const mixed: (string | number)[]

// TypeScript picks the "best common type"
```

## Controlling Widening

### Use `as const` for Full Literal Inference

```typescript
// Regular object - properties widen
const obj1 = { x: 1, y: 2 };
//    ^? const obj1: { x: number; y: number }

// With as const - properties are literal and readonly
const obj2 = { x: 1, y: 2 } as const;
//    ^? const obj2: { readonly x: 1; readonly y: 2 }

// Arrays too
const arr = [1, 2, 3] as const;
//    ^? const arr: readonly [1, 2, 3]
```

### Use Type Annotations to Be Explicit

```typescript
// Annotate to get the type you want
const x: 'x' | 'y' = 'x';
//    ^? const x: "x" | "y"

// Can be reassigned to 'y', but nothing else
```

### Use Satisfies for Checked Inference

```typescript
type Point = { x: number; y: number };

// Type annotation: loses literal types
const p1: Point = { x: 1, y: 2 };
//    ^? const p1: Point

// satisfies: keeps literals while checking structure
const p2 = { x: 1, y: 2 } satisfies Point;
//    ^? const p2: { x: number; y: number }

p2.x;  // number (not 1, but still good for inference)
```

## Common Widening Problems

### Problem: Literal Expected, Got String

```typescript
type HTTPMethod = 'GET' | 'POST' | 'PUT';

function makeRequest(method: HTTPMethod) { /* ... */ }

let method = 'GET';
makeRequest(method);
//          ~~~~~~ Argument of type 'string' is not assignable
```

**Solutions:**

```typescript
// Solution 1: Use const
const method = 'GET';
makeRequest(method);  // OK

// Solution 2: Type annotation
let method: HTTPMethod = 'GET';
makeRequest(method);  // OK

// Solution 3: as const
let method = 'GET' as const;
makeRequest(method);  // OK
```

### Problem: Object Property Too Wide

```typescript
type Config = {
  mode: 'development' | 'production';
  debug: boolean;
};

function configure(config: Config) { /* ... */ }

const config = { mode: 'development', debug: true };
configure(config);
//        ~~~~~~ Type 'string' is not assignable to type '"development" | "production"'
```

**Solutions:**

```typescript
// Solution 1: Type annotation
const config: Config = { mode: 'development', debug: true };

// Solution 2: as const on the whole object
const config = { mode: 'development', debug: true } as const;

// Solution 3: as const on just the property
const config = { mode: 'development' as const, debug: true };
```

### Problem: Tuple Becomes Array

```typescript
function setPoint(point: [number, number]) { /* ... */ }

const coords = [10, 20];
setPoint(coords);
//       ~~~~~~ Type 'number[]' is not assignable to type '[number, number]'
```

**Solutions:**

```typescript
// Solution 1: Type annotation
const coords: [number, number] = [10, 20];

// Solution 2: as const (makes it readonly)
const coords = [10, 20] as const;
// Note: readonly [10, 20] may not be assignable to [number, number]
// depending on the function's type
```

## Pressure Resistance Protocol

### 1. "Just Use `any`"

**Pressure:** "Type is wrong, just cast it to `any`"

**Response:** The type is right, just wider than you want.

**Action:** Use `const`, type annotations, or `as const`.

### 2. "TypeScript Is Being Dumb"

**Pressure:** "It's obviously 'GET', why infer string?"

**Response:** TypeScript assumes `let` variables will change.

**Action:** Use `const` for values that won't change.

## Red Flags - STOP and Reconsider

- Casting to fix literal type errors
- Surprised that object properties are `string` not `"specific"`
- Tuple types becoming arrays
- Union literals widening unexpectedly

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "const should make it literal" | Only for primitives, not object contents |
| "The value is clearly X" | `let` means it could change |
| "as any fixes it" | Use proper narrowing controls |

## Quick Reference

| Declaration | Value | Inferred Type |
|-------------|-------|---------------|
| `let x = "hello"` | string literal | `string` |
| `const x = "hello"` | string literal | `"hello"` |
| `const x = { a: 1 }` | object | `{ a: number }` |
| `const x = { a: 1 } as const` | object | `{ readonly a: 1 }` |
| `const x = [1, 2]` | array | `number[]` |
| `const x = [1, 2] as const` | array | `readonly [1, 2]` |

## The Bottom Line

**TypeScript widens types to allow reasonable mutations.**

Use `const` for primitives, type annotations for explicit types, and `as const` when you need full literal inference. Understanding widening prevents surprising type errors and helps you write more precise types.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 20: Understand How Variables Get Their Types.
