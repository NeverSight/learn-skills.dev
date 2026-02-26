---
name: exhaustiveness-checking
description: Use when handling tagged unions. Use when adding new cases to discriminated unions. Use when switch statements must cover all cases.
---

# Use Never Types for Exhaustiveness Checking

## Overview

**Use `never` to ensure all cases in a union are handled.**

When you add a new variant to a union type, TypeScript can automatically flag every switch statement that needs updating. This catches errors of omission at compile time.

## When to Use This Skill

- Handling all cases of a tagged union
- Adding new variants to discriminated unions
- Writing switch statements that must be complete
- Want compile-time errors when cases are missed

## The Iron Rule

```
ALWAYS add exhaustiveness checking to switch statements on union types.
```

**Remember:**
- After exhaustive cases, the type is `never`
- Nothing is assignable to `never` except `never`
- Missing cases turn into type errors
- This catches errors of omission

## Detection: The Missing Case Problem

Without exhaustiveness checking, new union variants are silently ignored:

```typescript
type Shape = Box | Circle | Line;

function drawShape(shape: Shape, ctx: CanvasRenderingContext2D) {
  switch (shape.type) {
    case 'box':
      ctx.rect(...shape.topLeft, ...shape.size);
      break;
    case 'circle':
      ctx.arc(...shape.center, shape.radius, 0, 2 * Math.PI);
      break;
    // Forgot 'line' - NO ERROR! Lines silently don't draw.
  }
}
```

## The Exhaustiveness Pattern

### The `assertUnreachable` Helper

```typescript
function assertUnreachable(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}
```

### Using It in Switch Statements

```typescript
function drawShape(shape: Shape, ctx: CanvasRenderingContext2D) {
  switch (shape.type) {
    case 'box':
      ctx.rect(...shape.topLeft, ...shape.size);
      break;
    case 'circle':
      ctx.arc(...shape.center, shape.radius, 0, 2 * Math.PI);
      break;
    default:
      assertUnreachable(shape);
      // If we missed a case, shape won't be 'never' and we get a type error!
  }
}
```

### When You Add a New Type

```typescript
// Add a new shape type
interface Line {
  type: 'line';
  start: Coord;
  end: Coord;
}
type Shape = Box | Circle | Line;  // Added Line

// Now drawShape shows an error:
function drawShape(shape: Shape, ctx: CanvasRenderingContext2D) {
  switch (shape.type) {
    case 'box': /* ... */ break;
    case 'circle': /* ... */ break;
    default:
      assertUnreachable(shape);
      //                ~~~~~ 
      // Argument of type 'Line' is not assignable to parameter of type 'never'
  }
}
```

Fix by handling the new case:

```typescript
function drawShape(shape: Shape, ctx: CanvasRenderingContext2D) {
  switch (shape.type) {
    case 'box':
      ctx.rect(...shape.topLeft, ...shape.size);
      break;
    case 'circle':
      ctx.arc(...shape.center, shape.radius, 0, 2 * Math.PI);
      break;
    case 'line':
      ctx.moveTo(...shape.start);
      ctx.lineTo(...shape.end);
      break;
    default:
      assertUnreachable(shape);  // Now shape is 'never', no error!
  }
}
```

## How It Works

After handling all cases, the remaining type is `never`:

```typescript
function processShape(shape: Shape) {
  switch (shape.type) {
    case 'box': break;
    case 'circle': break;
    case 'line': break;
    default:
      shape
      // ^? (parameter) shape: never
  }
}
```

If you miss a case, the type isn't `never`:

```typescript
function processShape(shape: Shape) {
  switch (shape.type) {
    case 'box': break;
    case 'circle': break;
    // (forgot 'line')
    default:
      shape
      // ^? (parameter) shape: Line
  }
}
```

Since `Line` is not assignable to `never`, you get a type error.

## Alternative: Return Type Enforcement

You can also use return types to enforce exhaustiveness:

```typescript
function getShapeName(shape: Shape): string {
  switch (shape.type) {
    case 'box':
      return 'Box';
    case 'circle':
      return 'Circle';
    // Missing 'line' - TypeScript error!
    // Function lacks ending return statement and return type does not include 'undefined'
  }
}
```

This only works if:
- The function has an explicit return type
- All cases must return
- `strictNullChecks` is enabled

## Complete Example

```typescript
// Types
type Coord = [x: number, y: number];

interface Box {
  type: 'box';
  topLeft: Coord;
  size: Coord;
}

interface Circle {
  type: 'circle';
  center: Coord;
  radius: number;
}

interface Line {
  type: 'line';
  start: Coord;
  end: Coord;
}

type Shape = Box | Circle | Line;

// Helper
function assertUnreachable(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}

// Usage - guaranteed to handle all shapes
function getArea(shape: Shape): number {
  switch (shape.type) {
    case 'box':
      return shape.size[0] * shape.size[1];
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'line':
      return 0;  // Lines have no area
    default:
      return assertUnreachable(shape);
  }
}
```

## When NOT to Use

Sometimes you intentionally want to ignore some cases:

```typescript
function handleCommonShapes(shape: Shape) {
  switch (shape.type) {
    case 'box':
    case 'circle':
      // Handle common cases
      break;
    // Intentionally ignore 'line' - don't add assertUnreachable here
  }
}
```

## Pressure Resistance Protocol

### 1. "The Default Case Handles It"

**Pressure:** "We have a default case, so it's fine"

**Response:** A silent default hides bugs when new variants are added.

**Action:** Use `assertUnreachable` in default to make missing cases explicit.

### 2. "We'll Remember to Update"

**Pressure:** "We know where to add new cases"

**Response:** Human memory fails. Compiler checking doesn't.

**Action:** Let TypeScript track it for you.

## Red Flags - STOP and Reconsider

- Switch on union type without exhaustiveness check
- Default cases that silently do nothing
- Adding variants to unions without checking all usages
- "TODO: handle new case" comments

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "We'll remember to update" | You won't, or your teammates won't |
| "Default handles unknowns" | It hides bugs from new variants |
| "It's just one switch" | Union types often have many switches |

## Quick Reference

```typescript
// The pattern
function assertUnreachable(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}

// In switch statements
switch (union.type) {
  case 'a': /* ... */ break;
  case 'b': /* ... */ break;
  default:
    assertUnreachable(union);  // Type error if cases missing
}
```

## The Bottom Line

**Turn missing cases into compile-time errors with `never`.**

When handling tagged unions, add `assertUnreachable(value)` to your default case. This ensures that adding new variants to the union produces type errors everywhere the union is handled, catching errors of omission at compile time rather than runtime.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 59: Use Never Types to Perform Exhaustiveness Checking.
