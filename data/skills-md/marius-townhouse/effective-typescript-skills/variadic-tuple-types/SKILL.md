---
name: variadic-tuple-types
description: Use when functions accept variable arguments. Use when typing rest parameters with specific constraints. Use when building generic function compositions. Use when preserving tuple length through transformations. Use when working with typed function pipelines.
---

# Use Rest Parameters and Tuple Types to Model Variadic Functions

## Overview

Variadic functions - functions that accept a variable number of arguments - are common in JavaScript. TypeScript's tuple types and rest parameters let you type these precisely, preserving the number and types of arguments. This enables powerful patterns like typed function composition and generic pipelines.

Understanding how to combine rest parameters with tuple types unlocks precise typing for flexible APIs.

## When to Use This Skill

- Functions accept variable number of typed arguments
- Need to preserve tuple length through transformations
- Building generic function composition utilities
- Typing rest parameters with specific constraints
- Creating typed function pipelines

## The Iron Rule

**Use rest parameters with tuple types to precisely type variadic functions. Combine with generics to preserve argument types through transformations.**

## Detection

Watch for these untyped patterns:

```typescript
// RED FLAGS - Untyped variadic functions
function logAll(...args: any[]): void;  // Lost type information
function compose(...fns: Function[]): Function;  // No type safety
function curry(fn: Function): Function;  // Arguments not tracked
```

## Basic Rest Parameters with Tuples

```typescript
// Preserve exact argument types
function logAll<T extends any[]>(...args: T): void {
  console.log(args);
}

logAll(1, 'hello', true);
// T is inferred as [number, string, boolean]

// Constrain the tuple
type StringNumberPair = [string, number];
function formatPair(...pair: StringNumberPair): string {
  return `${pair[0]}: ${pair[1]}`;
}

formatPair('score', 100);  // OK
formatPair('score');       // Error: missing number
formatPair('score', 100, 'extra');  // Error: too many arguments
```

## Generic Variadic Functions

```typescript
// Preserve types through transformation
function tail<T extends any[]>(
  head: T[0],
  ...rest: T extends [any, ...infer R] ? R : never
): T {
  return [head, ...rest] as T;
}

const result = tail(1, 'a', true);
// result: [number, string, boolean]
```

## Function Composition

```typescript
// Compose functions with preserved types
type Fn = (...args: any[]) => any;

function compose<T extends Fn[]>(
  ...fns: T
): (...args: Parameters<T[0]>) => ReturnType<T[number]> {
  return (arg) => fns.reduceRight((acc, fn) => fn(acc), arg);
}

const add1 = (x: number) => x + 1;
const double = (x: number) => x * 2;
const toString = (x: number) => String(x);

const composed = compose(toString, double, add1);
// (x: number) => string

const result = composed(5);  // "12"
```

## Curry with Tuple Types

```typescript
// Type-safe currying
type Curry<T extends any[], R> = T extends [infer First, ...infer Rest]
  ? (arg: First) => Rest extends [] ? R : Curry<Rest, R>
  : () => R;

function curry<T extends any[], R>(
  fn: (...args: T) => R
): Curry<T, R> {
  return ((arg: any) => {
    if (arguments.length >= fn.length) {
      return fn(...arguments);
    }
    return curry(fn.bind(null, arg));
  }) as Curry<T, R>;
}

const sum3 = (a: number, b: number, c: number) => a + b + c;
const curried = curry(sum3);

const result = curried(1)(2)(3);  // 6
// Each step is correctly typed!
```

## Real-World Example: Event Emitter

```typescript
type EventMap = {
  click: [x: number, y: number];
  keypress: [key: string];
  load: [];
};

class TypedEmitter<Events extends Record<string, any[]>> {
  emit<K extends keyof Events>(
    event: K,
    ...args: Events[K]
  ): void {
    // Implementation
  }
  
  on<K extends keyof Events>(
    event: K,
    handler: (...args: Events[K]) => void
  ): void {
    // Implementation
  }
}

const emitter = new TypedEmitter<EventMap>();

emitter.emit('click', 100, 200);  // OK
emitter.emit('click', 100);       // Error: missing y
emitter.on('keypress', (key) => {
  console.log(key);  // key is string
});
```

## Pressure Resistance Protocol

When typing variadic functions:

1. **Use tuple constraints**: `[string, number]` not `string | number`
2. **Preserve with generics**: `T extends any[]` captures exact types
3. **Consider length**: Use tuple length for conditional types
4. **Test edge cases**: Empty tuples, single elements, many elements

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `...args: any[]` | Lost type information | `T extends any[]` |
| `Function` type | No parameter/return types | Generic function types |
| Array instead of tuple | Loses length information | Tuple types |

## Common Rationalizations

### "It's too complex for my use case"

**Reality**: Start with `T extends any[]` and add complexity only when needed.

### "Users can pass arguments as an array"

**Reality**: Rest parameters are more ergonomic. Type them correctly for best DX.

### "I'll just use overloads"

**Reality**: Tuples handle the general case. Overloads require manual enumeration.

## Quick Reference

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| Capture args | `T extends any[]` | Preserve argument types |
| Constrain length | `[A, B, C]` | Fixed number of args |
| Minimum length | `[A, B, ...C[]]` | At least 2 args |
| Transform | `Parameters<T[0]>` | Extract parameter types |

## The Bottom Line

Rest parameters with tuple types enable precise typing of variadic functions. Use generics to preserve argument types through transformations, enabling powerful patterns like typed composition.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 62: Use Rest Parameters and Tuple Types to Model Variadic Functions
