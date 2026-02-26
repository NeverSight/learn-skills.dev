---
name: structural-typing
description: Use when surprised by TypeScript accepting unexpected values. Use when designing function parameters. Use when testing with mock objects.
---

# Get Comfortable with Structural Typing

## Overview

**TypeScript uses structural typing: if it has the right shape, it fits.**

Unlike nominal typing (where types must be explicitly declared), TypeScript checks structure. Understanding this prevents surprises and unlocks powerful patterns.

## When to Use This Skill

- Surprised that TypeScript accepts "wrong" values
- Designing interfaces and function parameters
- Writing unit tests with mock objects
- Debugging "impossible" type errors
- Understanding why extra properties are allowed

## The Iron Rule

```
NEVER assume types are "sealed" - they always allow extra properties.
```

**Accept that:**
- If it has the required properties, it's assignable
- Extra properties don't make a value invalid
- Classes are compared by structure, not identity

## Detection: The "Sealed Type" Assumption

If you're surprised that TypeScript accepts a value, you're probably assuming nominal typing.

```typescript
interface Vector2D {
  x: number;
  y: number;
}

function calculateLength(v: Vector2D) {
  return Math.sqrt(v.x ** 2 + v.y ** 2);
}

// ✅ Works as expected
calculateLength({ x: 3, y: 4 });  // 5

// ✅ Also works! Has x and y, so it's a valid Vector2D
const namedVector = { x: 3, y: 4, name: 'Pythagoras' };
calculateLength(namedVector);  // 5

// ✅ Even 3D vectors work (but give wrong results!)
const vector3D = { x: 3, y: 4, z: 5 };
calculateLength(vector3D);  // 5 (ignores z!)
```

## The Structural Typing Principle

A value is assignable to a type if it has at least the required properties with compatible types.

```typescript
interface Point {
  x: number;
  y: number;
}

// All of these are valid Points:
const p1: Point = { x: 1, y: 2 };                    // Exact match
const p2: Point = { x: 1, y: 2, z: 3 };             // Extra property (via variable)
const p3: Point = { x: 1, y: 2, name: 'origin' };   // Different extra property

// But not this:
const p4: Point = { x: 1 };  // Error: missing 'y'
```

## Why This Matters for Functions

```typescript
interface Vector2D { x: number; y: number; }
interface Vector3D { x: number; y: number; z: number; }

function normalize(v: Vector3D) {
  const length = Math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2);
  return {
    x: v.x / length,
    y: v.y / length,
    z: v.z / length,
  };
}

// This is a bug, but TypeScript doesn't catch it:
function calculateLength2D(v: Vector2D) {
  return Math.sqrt(v.x ** 2 + v.y ** 2);
}

// normalize calls calculateLength2D internally
function normalize(v: Vector3D) {
  const length = calculateLength2D(v);  // Bug: ignores z!
  // Vector3D is assignable to Vector2D
}
```

## Structural Typing with Classes

```typescript
class SmallContainer {
  num: number;
  constructor(num: number) {
    if (num < 0 || num >= 10) {
      throw new Error('Must be 0-9');
    }
    this.num = num;
  }
}

const a = new SmallContainer(5);  // OK

// This also type-checks, but bypasses validation!
const b: SmallContainer = { num: 2024 };  // No error!

// Because SmallContainer structurally is just { num: number }
```

## Benefits: Easy Testing

Structural typing makes testing simpler - no mocking libraries needed:

```typescript
interface Database {
  runQuery(sql: string): any[];
}

function getUsers(db: Database) {
  return db.runQuery('SELECT * FROM users');
}

// In tests, just create an object with the right shape:
test('getUsers', () => {
  const mockDb = {
    runQuery(sql: string) {
      return [{ name: 'Alice' }, { name: 'Bob' }];
    }
  };
  
  const users = getUsers(mockDb);  // Works! No type error
  expect(users).toHaveLength(2);
});
```

## The "Excess Property Checking" Exception

Object literals get special treatment - TypeScript flags extra properties:

```typescript
interface Point { x: number; y: number; }

// Extra property in object literal: Error!
const p: Point = { x: 1, y: 2, z: 3 };
//                            ~ Object literal may only specify known properties

// But via intermediate variable: No error
const temp = { x: 1, y: 2, z: 3 };
const p: Point = temp;  // OK
```

This is a usability feature, not a change in structural typing rules. See the excess-property-checking skill for details.

## When Structural Typing Causes Problems

### Problem: Wrong Vector Dimension

```typescript
// Solution 1: Use optional never to forbid property
interface Vector2D {
  x: number;
  y: number;
  z?: never;  // Explicitly disallows z
}

// Solution 2: Use branded types (see branded-types skill)
type Vector2D = { x: number; y: number } & { _brand: 'Vector2D' };
```

### Problem: Class Validation Bypassed

```typescript
// Solution: Make the class have unique properties
class SmallContainer {
  private readonly _brand = 'SmallContainer';  // Can't be faked
  num: number;
  // ...
}
```

## Pressure Resistance Protocol

### 1. "This Shouldn't Be Allowed"

**Pressure:** "TypeScript should reject values with extra properties"

**Response:** That's nominal typing. TypeScript uses structural typing.

**Action:** Use techniques like branded types if you need stricter checking.

### 2. "My Class Should Be Special"

**Pressure:** "Only real instances of my class should be valid"

**Response:** Classes are structurally typed. Add private fields to differentiate.

**Action:** Use private fields or brands for nominal-like behavior.

## Red Flags - STOP and Reconsider

- Assuming extra properties make a value invalid
- Expecting class identity to matter
- Surprised when TypeScript accepts "wrong" values
- Thinking types are "sealed"
- Validation logic that TypeScript doesn't see

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's not the right type" | If it has the right shape, it is. |
| "My class validates" | Structural objects bypass the constructor. |
| "Extra props shouldn't work" | In TypeScript, they do. |

## Quick Reference

| Scenario | Structural Typing Behavior |
|----------|---------------------------|
| Extra properties on values | Allowed (except object literals) |
| Class instances | Compared by structure, not class identity |
| Function parameters | Any structurally compatible value works |
| Object literal assignment | Excess properties flagged (special case) |

## The Bottom Line

**TypeScript checks shape, not identity.**

If a value has all the required properties with compatible types, it's assignable. This enables easy testing and flexible APIs, but can cause surprises. Use techniques like branded types when you need stricter checking.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 4: Get Comfortable with Structural Typing.
