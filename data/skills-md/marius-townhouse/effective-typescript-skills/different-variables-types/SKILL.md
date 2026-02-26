---
name: different-variables-types
description: Use when tempted to reuse variables. Use when variable changes type. Use when using union types for multiple purposes.
---

# Use Different Variables for Different Types

## Overview

**Don't reuse variables for different purposes.**

In JavaScript, you can assign any value to any variable. But in TypeScript, a variable's type is generally fixed. Using different variables for different concepts improves type safety and code clarity.

## When to Use This Skill

- Reusing a variable name for a different purpose
- Variables assigned values of different types
- Union types used just to accommodate reassignment
- Debugging type errors from variable reuse

## The Iron Rule

```
One variable, one type, one purpose.
Different concepts deserve different names.
```

**Remember:**
- Variable values can change; types generally don't
- Union types are harder to work with than simple types
- const is better than let
- Different names communicate different intentions

## Detection: Type Errors from Reuse

```typescript
let productId = "12-34-56";
fetchProduct(productId);  // Expects string

productId = 123456;
// ~~~~~~~ Type 'number' is not assignable to type 'string'

fetchProductBySerialNumber(productId);
// Expects number
```

TypeScript infers `productId` as `string` from the first assignment.

## The Union Type "Fix" (Problematic)

```typescript
// Works, but creates problems
let productId: string | number = "12-34-56";
fetchProduct(productId);

productId = 123456;  // OK
fetchProductBySerialNumber(productId);  // OK

// But now everywhere you use productId, you need type guards:
if (typeof productId === 'string') {
  // ...
}
```

Union types are harder to work with and obscure the code's intent.

## The Better Solution: Different Variables

```typescript
const productId = "12-34-56";
fetchProduct(productId);

const serial = 123456;
fetchProductBySerialNumber(serial);
```

Benefits:
- Disentangles unrelated concepts
- More specific variable names
- Better type inference (no annotations needed)
- Simpler types (not unions)
- Variables can be `const`

## Why const is Better

```typescript
// let: type can be reassigned
let x = 'hello';
x = 'goodbye';  // OK
x = 42;         // Error: different type

// const: value cannot change
const y = 'hello';
y = 'goodbye';  // Error: cannot reassign const
// No type ambiguity ever
```

`const` makes code easier for both humans and TypeScript to understand.

## Shadowing: A Different Issue

```typescript
const productId = "12-34-56";
fetchProduct(productId);

{
  const productId = 123456;  // Different variable, same name
  fetchProductBySerialNumber(productId);
}
```

This works because they're different variables in different scopes. But it's confusing for humans - prefer different names instead.

## Type Narrowing vs Variable Reuse

TypeScript allows type narrowing (getting more specific):

```typescript
let x: string | number = getValue();

if (typeof x === 'string') {
  x  // Type: string (narrowed)
  x.toUpperCase();  // OK
}
```

This is different from trying to widen a type (getting less specific), which doesn't work:

```typescript
let x = 'hello';  // Type: string
x = 42;  // Error: can't widen to string | number
```

## Real-World Example

```typescript
// Bad: reusing 'result' for different things
let result = await fetchUser(id);
processUser(result);

result = await fetchPosts(id);  // Error: different type!
processPosts(result);

// Good: descriptive names for each
const user = await fetchUser(id);
processUser(user);

const posts = await fetchPosts(id);
processPosts(posts);
```

## Pressure Resistance Protocol

### 1. "I Want to Reuse the Variable"

**Pressure:** "It's just temporary, I'll reassign it"

**Response:** Use a new variable. It's clearer and type-safe.

**Action:** Create a new `const` with a descriptive name.

### 2. "Union Types Work"

**Pressure:** "I'll just use `string | number`"

**Response:** Union types add complexity everywhere you use the variable.

**Action:** Separate variables with simple types are easier to work with.

## Red Flags - STOP and Reconsider

- `let x: A | B` where A and B serve different purposes
- Variables that get reassigned to completely different values
- Type errors from reassignment
- Generic variable names like `temp` or `result` being reused

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It saves a variable" | Variables are cheap; bugs are expensive |
| "Same data, different format" | Different formats = different variables |
| "Less code" | More clarity > less code |

## Quick Reference

```typescript
// DON'T: Reuse variable for different purposes
let id = "abc";
fetchByString(id);
id = 123;  // Error

// DON'T: Use union just to allow reassignment
let id: string | number = "abc";

// DO: Different variables for different concepts
const stringId = "abc";
const numericId = 123;
```

## The Bottom Line

**Different concepts deserve different variables.**

TypeScript types don't change (except narrowing). Embrace this by using separate variables for separate purposes. Your code becomes clearer, types simpler, and bugs rarer.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 19: Use Different Variables for Different Types.
