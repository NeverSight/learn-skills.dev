---
name: function-type-expressions
description: Use when writing multiple functions with same signature. Use when implementing callbacks. Use when matching existing function types.
---

# Apply Types to Entire Function Expressions When Possible

## Overview

**Type entire functions at once instead of individual parameters.**

When using function expressions (not statements), you can apply a type to the entire function. This reduces repetition, improves type safety, and makes code more readable.

## When to Use This Skill

- Writing multiple functions with the same signature
- Implementing callbacks for libraries
- Matching signatures of existing functions
- Wrapping or extending existing functions

## The Iron Rule

```
When functions share a signature, define the type ONCE and apply it to EACH function.
```

**Remember:**
- Function expressions can have types applied to them
- Parameter types are inferred from the function type
- Return types are checked against the function type
- Use `typeof fn` to match existing function signatures

## Detection: Repeated Signatures

```typescript
// Repetitive - same signature 4 times
function add(a: number, b: number) { return a + b; }
function sub(a: number, b: number) { return a - b; }
function mul(a: number, b: number) { return a * b; }
function div(a: number, b: number) { return a / b; }
```

## The Solution: Function Types

### Define Once, Use Many Times

```typescript
type BinaryFn = (a: number, b: number) => number;

const add: BinaryFn = (a, b) => a + b;  // Types inferred
const sub: BinaryFn = (a, b) => a - b;
const mul: BinaryFn = (a, b) => a * b;
const div: BinaryFn = (a, b) => a / b;
```

Benefits:
- No repeated type annotations
- Return type checked automatically
- Logic is more visible without type noise

### Match Existing Functions with typeof

```typescript
// Match fetch's signature exactly
const checkedFetch: typeof fetch = async (input, init) => {
  const response = await fetch(input, init);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response;
};
```

TypeScript infers:
- `input: RequestInfo | URL`
- `init?: RequestInit`
- Return: `Promise<Response>`

### Change Return Type with Parameters

```typescript
// Match parameters but change return type
async function fetchNumber(
  ...args: Parameters<typeof fetch>
): Promise<number> {
  const response = await checkedFetch(...args);
  return Number(await response.text());
}
```

## Function Statement vs Expression

```typescript
// Statement - must annotate each parameter
function rollDice1(sides: number): number { /* ... */ }

// Expression - can apply type to entire function
type DiceRollFn = (sides: number) => number;
const rollDice2: DiceRollFn = (sides) => { /* ... */ };
```

## Common Function Type Patterns

### Callback Types

```typescript
type EventHandler = (event: Event) => void;
type AsyncCallback<T> = () => Promise<T>;
type Comparator<T> = (a: T, b: T) => number;

const handleClick: EventHandler = (e) => {
  console.log(e.target);  // e is typed as Event
};
```

### Generic Function Types

```typescript
type Mapper<T, U> = (item: T, index: number) => U;

const double: Mapper<number, number> = (n) => n * 2;
const stringify: Mapper<number, string> = (n) => String(n);
```

### Interface Syntax (Alternative)

```typescript
// Function type as interface
interface StringTransform {
  (input: string): string;
}

const toUpper: StringTransform = s => s.toUpperCase();
```

## Return Type Safety

Function types catch return type errors:

```typescript
const checkedFetch: typeof fetch = async (input, init) => {
  const response = await fetch(input, init);
  if (!response.ok) {
    return new Error('Failed');  // Error!
    // Type 'Error' is not assignable to type 'Response'
  }
  return response;
};
```

Without the function type, this would only error at call sites.

## Library Callback Types

Libraries often provide callback types:

```typescript
// React provides these
import { MouseEventHandler, ChangeEventHandler } from 'react';

const handleClick: MouseEventHandler<HTMLButtonElement> = (e) => {
  console.log(e.currentTarget.disabled);  // Fully typed
};

const handleChange: ChangeEventHandler<HTMLInputElement> = (e) => {
  console.log(e.target.value);  // Fully typed
};
```

## When NOT to Use Function Types

Don't over-engineer for single functions:

```typescript
// Overkill for a single standalone function
type GreetFn = (name: string) => string;
const greet: GreetFn = (name) => `Hello, ${name}`;

// Just use a normal function statement
function greet(name: string): string {
  return `Hello, ${name}`;
}
```

## Pressure Resistance Protocol

### 1. "Function Statements Are Clearer"

**Pressure:** "I prefer seeing types inline with parameters"

**Response:** With shared signatures, centralizing the type removes noise.

**Action:** Use function types when 2+ functions share a signature.

### 2. "I Don't Know the Library's Type"

**Pressure:** "I can't find the callback type in the library"

**Response:** Use `typeof existingFunction` or `Parameters<typeof fn>`.

**Action:** Match existing signatures with typeof.

## Red Flags - STOP and Reconsider

- Same parameter types repeated across multiple functions
- Wrapper functions that should match the wrapped function's signature
- Callbacks without proper typing

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Types on parameters are clearer" | Not when repeated 4 times |
| "Function statements are simpler" | Function expressions with types are just as clear |
| "I'll just use `any`" | Loses all type safety benefits |

## Quick Reference

```typescript
// Define function type
type Transform<T> = (value: T) => T;

// Apply to function expression
const double: Transform<number> = v => v * 2;

// Match existing function
const myFetch: typeof fetch = async (input, init) => { ... };

// Match parameters, change return
function wrapper(...args: Parameters<typeof original>): NewReturn { ... }
```

## The Bottom Line

**Apply types to entire function expressions when you have shared signatures.**

This reduces repetition, centralizes type definitions, and catches return type errors at the source. Use `typeof` to match existing function signatures exactly.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 12: Apply Types to Entire Function Expressions When Possible.
