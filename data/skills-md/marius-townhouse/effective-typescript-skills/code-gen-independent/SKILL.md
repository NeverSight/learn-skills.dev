---
name: code-gen-independent
description: Use when confused about types at runtime. Use when trying to use instanceof with interfaces. Use when type errors don't prevent JavaScript output.
---

# Understand That Code Generation Is Independent of Types

## Overview

**TypeScript compilation and type checking are separate processes.**

The TypeScript compiler does two things: (1) transpile TypeScript to JavaScript, and (2) check types. These are independent - type errors don't prevent code generation, and types don't exist at runtime.

## When to Use This Skill

- Confused why code runs despite type errors
- Trying to check types at runtime
- Using instanceof with interfaces
- Expecting types to affect runtime behavior

## The Iron Rule

```
NEVER expect TypeScript types to exist at runtime. They are erased.
```

**Key Facts:**
- Code with type errors can still produce JavaScript output
- Types are erased during compilation
- You can't use instanceof on TypeScript interfaces
- Runtime checks require JavaScript constructs

## Type Errors Don't Prevent Output

```bash
$ cat test.ts
let x = 'hello';
x = 1234;  // Type error!

$ tsc test.ts
test.ts:2:1 - error TS2322: Type 'number' is not assignable to type 'string'

$ cat test.js
var x = 'hello';
x = 1234;  // JavaScript was still generated!
```

Type errors are like warnings - they don't stop compilation.

## You Can't Check Types at Runtime

```typescript
interface Square {
  width: number;
}
interface Rectangle extends Square {
  height: number;
}
type Shape = Square | Rectangle;

function calculateArea(shape: Shape) {
  if (shape instanceof Rectangle) {
      //            ~~~~~~~~~ 'Rectangle' only refers to a type,
      //                      but is being used as a value here
    return shape.width * shape.height;
  }
  return shape.width * shape.width;
}
```

**Why?** `interface` and `type` are erased. They don't exist in JavaScript.

## Solutions for Runtime Type Checking

### Option 1: Property Checking

```typescript
function calculateArea(shape: Shape) {
  if ('height' in shape) {
    // TypeScript knows shape is Rectangle here
    return shape.width * shape.height;
  }
  return shape.width * shape.width;
}
```

### Option 2: Tagged Union (Recommended)

```typescript
interface Square {
  kind: 'square';
  width: number;
}
interface Rectangle {
  kind: 'rectangle';
  width: number;
  height: number;
}
type Shape = Square | Rectangle;

function calculateArea(shape: Shape) {
  if (shape.kind === 'rectangle') {
    return shape.width * shape.height;
  }
  return shape.width * shape.width;
}
```

### Option 3: Use Classes

```typescript
class Square {
  constructor(public width: number) {}
}
class Rectangle extends Square {
  constructor(width: number, public height: number) {
    super(width);
  }
}

function calculateArea(shape: Square | Rectangle) {
  if (shape instanceof Rectangle) {
    // This works! Classes exist at runtime
    return shape.width * shape.height;
  }
  return shape.width * shape.width;
}
```

## Type Operations Don't Affect Runtime

```typescript
function asNumber(val: number | string): number {
  return val as number;  // Type assertion
}

// Generated JavaScript:
function asNumber(val) {
  return val;  // No conversion! Just returns val as-is
}
```

Type assertions don't convert values. Use runtime code:

```typescript
function asNumber(val: number | string): number {
  return typeof val === 'string' ? Number(val) : val;
}
```

## Runtime Types May Differ from Declared Types

```typescript
function setLightSwitch(value: boolean) {
  switch (value) {
    case true: turnLightOn(); break;
    case false: turnLightOff(); break;
    default:
      console.log("I'm afraid I can't do that.");
      // TypeScript thinks this is unreachable, but...
  }
}

// At runtime, someone could call:
setLightSwitch("ON" as any);  // Hits the default case!
```

API responses, external data, and `any` types can cause runtime type mismatches.

## You Can't Overload Based on Types

```typescript
// ❌ This doesn't work - types are erased
function add(a: number, b: number) { return a + b; }
function add(a: string, b: string) { return a + b; }
// ~~~ Duplicate function implementation

// ✅ Use a single implementation with union type
function add(a: number | string, b: number | string) {
  if (typeof a === 'number' && typeof b === 'number') {
    return a + b;
  }
  return String(a) + String(b);
}
```

## Pressure Resistance Protocol

### 1. "Just Use `as Type`"

**Pressure:** "Type assertion will convert the value"

**Response:** Assertions don't convert. They're compile-time only.

**Action:** Write actual runtime conversion code.

### 2. "Use instanceof"

**Pressure:** "instanceof should work on my interface"

**Response:** Interfaces don't exist at runtime. Use tagged unions or classes.

**Action:** Add a discriminant property or use classes.

## Red Flags - STOP and Reconsider

- Using instanceof with interface/type
- Expecting type assertions to convert values
- Assuming type errors prevent JavaScript output
- Relying on TypeScript types for runtime validation

## Quick Reference

| TypeScript Construct | Exists at Runtime? |
|---------------------|-------------------|
| `interface` | No |
| `type` | No |
| Type annotation (`: T`) | No |
| Type assertion (`as T`) | No |
| `class` | Yes |
| `enum` (non-const) | Yes |
| Tagged union property | Yes |

## The Bottom Line

**Types are erased. Code generation is independent of type checking.**

TypeScript types exist only at compile time. For runtime type checking, use JavaScript constructs: property checks, tagged unions, classes, or typeof/instanceof (for values, not types).

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 3: Understand That Code Generation Is Independent of Types.
