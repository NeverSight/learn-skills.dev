---
name: tagged-unions
description: Use when modeling states or variants. Use when interface has union properties. Use when different states have different data requirements.
---

# Prefer Unions of Interfaces to Interfaces with Unions

## Overview

**When an interface has union-typed properties, often a union of interfaces is better.**

Tagged unions (discriminated unions) make relationships between properties explicit and enable exhaustive type checking.

## When to Use This Skill

- Interface properties that only make sense together
- State types with different data per state
- Multiple boolean flags that have dependencies
- Union-typed properties with implicit relationships
- Switch statements on string/enum status fields

## The Iron Rule

```
NEVER create interfaces where property combinations can be invalid.
```

**No exceptions:**
- Not for "it's simpler"
- Not for "we document the relationship"
- Not for "we validate at runtime"

## Detection: The "Interface with Unions" Smell

If properties depend on each other, split into a union of interfaces.

```typescript
// ❌ VIOLATION: Allows invalid combinations
interface Layer {
  type: 'fill' | 'line' | 'point';
  layout: FillLayout | LineLayout | PointLayout;
  paint: FillPaint | LinePaint | PointPaint;
}

// These are technically valid but make no sense:
const badLayer: Layer = {
  type: 'fill',
  layout: new LineLayout(),   // Wrong layout for fill!
  paint: new PointPaint(),    // Wrong paint for fill!
};
```

## Solution: Tagged Union

```typescript
// ✅ CORRECT: Each variant is explicit
interface FillLayer {
  type: 'fill';
  layout: FillLayout;
  paint: FillPaint;
}

interface LineLayer {
  type: 'line';
  layout: LineLayout;
  paint: LinePaint;
}

interface PointLayer {
  type: 'point';
  layout: PointLayout;
  paint: PointPaint;
}

type Layer = FillLayer | LineLayer | PointLayer;

// Now invalid combinations are impossible:
const badLayer: Layer = {
  type: 'fill',
  layout: new LineLayout(),   // Error! Not assignable to FillLayout
  paint: new PointPaint(),
};
```

## The Magic: Narrowing Works Automatically

```typescript
function drawLayer(layer: Layer) {
  switch (layer.type) {
    case 'fill':
      // TypeScript knows: layer is FillLayer
      console.log(layer.paint);  // FillPaint
      console.log(layer.layout); // FillLayout
      break;
    case 'line':
      // TypeScript knows: layer is LineLayer
      console.log(layer.paint);  // LinePaint
      break;
    case 'point':
      // TypeScript knows: layer is PointLayer
      console.log(layer.paint);  // PointPaint
      break;
  }
}
```

## Example: Request State

```typescript
// ❌ BAD: Allows invalid states
interface RequestState {
  status: 'pending' | 'loading' | 'success' | 'error';
  data?: ResponseData;
  error?: Error;
}

// What does this mean?
const weird: RequestState = {
  status: 'error',
  data: someData,  // Has data but errored?
};

// ✅ GOOD: Tagged union
interface RequestPending { status: 'pending' }
interface RequestLoading { status: 'loading' }
interface RequestSuccess { status: 'success'; data: ResponseData }
interface RequestError { status: 'error'; error: Error }

type RequestState = RequestPending | RequestLoading | RequestSuccess | RequestError;

// Each state has exactly the data it needs
function handleRequest(state: RequestState) {
  switch (state.status) {
    case 'pending':
      return <Spinner />;
    case 'loading':
      return <LoadingBar />;
    case 'success':
      return <DataView data={state.data} />;  // data is guaranteed
    case 'error':
      return <ErrorView error={state.error} />;  // error is guaranteed
  }
}
```

## Optional Properties: Group Them

```typescript
// ❌ BAD: Related optional fields
interface Person {
  name: string;
  placeOfBirth?: string;  // These should be
  dateOfBirth?: Date;     // together or absent
}

// Valid but inconsistent:
const person: Person = {
  name: 'Alice',
  placeOfBirth: 'NYC',  // Has place but no date?
};

// ✅ GOOD: Group related optional fields
interface Person {
  name: string;
  birth?: {
    place: string;
    date: Date;
  };
}

// Now they're always together:
function printBirth(person: Person) {
  if (person.birth) {
    // Both place AND date are guaranteed
    console.log(`${person.birth.place} on ${person.birth.date}`);
  }
}
```

## The Tag Must Be a Literal Type

```typescript
// ❌ BAD: Tag is too broad
interface Shape {
  type: string;  // Any string - can't narrow!
}

// ✅ GOOD: Tag is a literal union
interface Circle { type: 'circle'; radius: number }
interface Square { type: 'square'; side: number }
type Shape = Circle | Square;

// Now narrowing works:
function area(shape: Shape) {
  if (shape.type === 'circle') {
    return Math.PI * shape.radius ** 2;  // TypeScript knows it's Circle
  }
  return shape.side ** 2;  // TypeScript knows it's Square
}
```

## Exhaustiveness Checking

Tagged unions enable exhaustiveness checking:

```typescript
function assertNever(x: never): never {
  throw new Error(`Unexpected: ${x}`);
}

function area(shape: Shape): number {
  switch (shape.type) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'square':
      return shape.side ** 2;
    default:
      return assertNever(shape);  // Error if we miss a case!
  }
}

// Later, if we add Triangle:
type Shape = Circle | Square | Triangle;

// TypeScript errors in assertNever:
// Argument of type 'Triangle' is not assignable to parameter of type 'never'
```

## When You Can't Change the Type

If the data comes from an API you don't control:

```typescript
// External API returns this shape
interface APIResponse {
  type: 'user' | 'admin';
  name: string;
  permissions?: string[];  // Only for admin
}

// Create a better internal type:
interface User { type: 'user'; name: string }
interface Admin { type: 'admin'; name: string; permissions: string[] }
type Person = User | Admin;

// Transform at the boundary:
function transformResponse(response: APIResponse): Person {
  if (response.type === 'admin') {
    return {
      type: 'admin',
      name: response.name,
      permissions: response.permissions ?? [],
    };
  }
  return { type: 'user', name: response.name };
}
```

## Pressure Resistance Protocol

### 1. "It's More Interfaces"

**Pressure:** "One interface is simpler than four"

**Response:** Invalid states are not simple to debug.

**Action:** Write the interfaces. They're documentation too.

### 2. "We Document the Dependencies"

**Pressure:** "Comments explain when fields apply"

**Response:** Types are better documentation. They're checked.

**Action:** Make the types express the relationships.

## Red Flags - STOP and Reconsider

- Interface with multiple optional fields that relate
- Status enum with optional data fields
- Switch statements checking type then accessing data
- Comments explaining "if X then Y is set"
- Runtime validation for field combinations

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's simpler" | Invalid states aren't simple to debug. |
| "We validate" | Types catch errors at compile time. |
| "Too many interfaces" | Better than too many bugs. |

## Quick Reference

| Pattern | Solution |
|---------|----------|
| Status + optional data/error | Tagged union per status |
| Type discriminator + union fields | Tagged union per type |
| Related optional fields | Nested object that's optional |
| Boolean flags with dependencies | Tagged union per state |

## The Bottom Line

**If properties depend on each other, express that in the type system.**

Use tagged unions (discriminated unions) to make relationships explicit. You get exhaustive checking, better narrowing, and types that can only represent valid states.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 34: Prefer Unions of Interfaces to Interfaces with Unions.
