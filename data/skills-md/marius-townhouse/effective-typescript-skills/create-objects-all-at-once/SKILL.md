---
name: create-objects-all-at-once
description: Use when building objects incrementally. Use when adding properties after creation. Use when TypeScript errors on dynamic object construction.
---

# Create Objects All at Once

## Overview

**Build objects in a single statement, not piece by piece.**

TypeScript infers an object's type when it's created. Adding properties later causes type errors. Build complete objects in one go using object literals and spread syntax.

## When to Use This Skill

- Creating objects step by step
- Adding properties after object creation
- Getting "property does not exist" errors
- Merging multiple objects

## The Iron Rule

```
Define all properties in a single object literal.
Use spread syntax (...) to combine objects.
```

**Remember:**
- Object types are fixed at creation
- Type assertions are not the answer
- Object spread preserves type safety
- Each spread creates a new variable

## Detection: Incremental Construction Fails

```typescript
const pt = {};
pt.x = 3;
// ~ Property 'x' does not exist on type '{}'
pt.y = 4;
// ~ Property 'y' does not exist on type '{}'
```

TypeScript infers `pt` as `{}`, and you can't add properties to it.

## The Type Assertion "Fix" (Problematic)

```typescript
interface Point { x: number; y: number; }

const pt = {} as Point;  // Assertion silences errors
pt.x = 3;
pt.y = 4;

// But: TypeScript won't check you assigned all properties!
const pt2 = {} as Point;  // No error, but x and y are undefined
```

Type assertions bypass safety checks.

## The Solution: Build All at Once

```typescript
interface Point { x: number; y: number; }

const pt: Point = {
  x: 3,
  y: 4,
};
// TypeScript verifies all required properties are present
```

## Combining Objects with Spread

Don't use Object.assign:

```typescript
const pt = { x: 3, y: 4 };
const id = { name: 'Origin' };

const namedPoint = {};
Object.assign(namedPoint, pt, id);
namedPoint.name;
// ~~~~~ Property 'name' does not exist on type '{}'
```

Use spread syntax instead:

```typescript
const pt = { x: 3, y: 4 };
const id = { name: 'Origin' };

const namedPoint = { ...pt, ...id };
//    ^? { name: string; x: number; y: number }
namedPoint.name;  // OK
```

## Building Up Objects Safely

Use a new variable for each step:

```typescript
const pt0 = {};
const pt1 = { ...pt0, x: 3 };
const pt: Point = { ...pt1, y: 4 };  // OK

// Each variable has a new, complete type
```

## Conditional Properties

Add properties conditionally with spread:

```typescript
declare let hasMiddle: boolean;

const firstLast = { first: 'Harry', last: 'Truman' };
const president = {
  ...firstLast,
  ...(hasMiddle ? { middle: 'S' } : {}),
};
//    ^? { middle?: string; first: string; last: string }
```

The conditional property becomes optional in the result type.

## Multiple Conditional Properties

```typescript
declare let hasDates: boolean;

const nameTitle = { name: 'Khufu', title: 'Pharaoh' };
const pharaoh = {
  ...nameTitle,
  ...(hasDates && { start: -2589, end: -2566 }),
};
//    ^? { start?: number; end?: number; name: string; title: string }
```

Both `start` and `end` are optional because they're conditionally added together.

## Transforming Objects

When transforming data, use functional constructs:

```typescript
// Don't build incrementally
const result: Record<string, number> = {};
for (const item of items) {
  result[item.name] = item.value;  // Works but less type-safe
}

// Do use Array methods
const result = Object.fromEntries(
  items.map(item => [item.name, item.value])
);
```

## Real-World Example: Configuration Objects

```typescript
interface Config {
  host: string;
  port: number;
  ssl?: boolean;
}

// Bad: incremental
const config = {} as Config;
config.host = 'localhost';  // Might forget port!

// Good: all at once
const config: Config = {
  host: 'localhost',
  port: 8080,
};

// Good: with conditional
const config: Config = {
  host: 'localhost',
  port: 8080,
  ...(useSSL && { ssl: true }),
};
```

## Pressure Resistance Protocol

### 1. "I Need to Build It Dynamically"

**Pressure:** "Properties come from different sources"

**Response:** Collect all data first, then build the object.

**Action:** Use spread to combine: `{ ...source1, ...source2 }`

### 2. "Type Assertion Works"

**Pressure:** "`as Type` fixes the error"

**Response:** It bypasses type checking. Missing properties won't be caught.

**Action:** Build complete objects; let TypeScript verify them.

## Red Flags - STOP and Reconsider

- `const obj = {}` followed by property assignments
- `Object.assign` for building objects
- Type assertions (`as`) to silence "property does not exist" errors
- Adding properties to objects in loops

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "I don't know all properties yet" | Gather data first, build object second |
| "It's more readable step by step" | Object literals are clear and type-safe |
| "Type assertion fixes it" | Assertions bypass type checking |

## Quick Reference

```typescript
// DON'T: Build incrementally
const obj = {};
obj.a = 1;  // Error

// DON'T: Use type assertion
const obj = {} as MyType;

// DO: Build all at once
const obj: MyType = { a: 1, b: 2 };

// DO: Combine with spread
const obj = { ...base, ...extra };

// DO: Conditional properties
const obj = { ...base, ...(cond && { opt: val }) };
```

## The Bottom Line

**Build objects completely in a single statement.**

TypeScript types are fixed at creation. Use object literals to define all properties at once. Use spread syntax to combine objects and add conditional properties. Avoid type assertions.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 21: Create Objects All at Once.
