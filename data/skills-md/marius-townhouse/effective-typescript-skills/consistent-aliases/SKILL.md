---
name: consistent-aliases
description: Use when narrowing doesn't work as expected. Use when using variables for object properties. Use when refinements are lost.
---

# Be Consistent in Your Use of Aliases

## Overview

**If you create an alias, use it consistently.**

When you assign an object property to a variable, you create an alias. TypeScript tracks them separately, so narrowing one doesn't narrow the other. Choose one and stick with it.

## When to Use This Skill

- Type narrowing isn't working as expected
- Using both a variable and its source property
- Property checks not affecting aliased variables
- Refinements being "lost" after function calls

## The Iron Rule

```
One alias OR the original - never mix them in the same scope.
Prefer destructuring for consistent naming.
```

**Remember:**
- Aliases and originals are tracked separately
- Narrowing one doesn't narrow the other
- Function calls can invalidate property refinements
- Local variables are safer than object properties

## Detection: Alias Breaks Narrowing

```typescript
interface Polygon {
  exterior: Coordinate[];
  bbox?: BoundingBox;
}

function isPointInPolygon(polygon: Polygon, pt: Coordinate) {
  const box = polygon.bbox;  // Created an alias
  
  if (polygon.bbox) {  // Narrows polygon.bbox
    if (pt.x < box.x[0]) {  // box is still possibly undefined!
      //       ~~~
      // 'box' is possibly 'undefined'
    }
  }
}
```

The check on `polygon.bbox` doesn't narrow `box`.

## The Golden Rule: Use Aliases Consistently

```typescript
function isPointInPolygon(polygon: Polygon, pt: Coordinate) {
  const box = polygon.bbox;
  
  if (box) {  // Check the alias
    if (pt.x < box.x[0]) {  // Use the alias
      // OK - box is narrowed here
    }
  }
}
```

Now both the check and usage refer to the same variable.

## Best Practice: Use Destructuring

```typescript
function isPointInPolygon(polygon: Polygon, pt: Coordinate) {
  const { bbox } = polygon;  // Same name as property
  
  if (bbox) {
    const { x, y } = bbox;  // Continue destructuring
    if (pt.x < x[0] || pt.x > x[1] || pt.y < y[0] || pt.y > y[1]) {
      return false;
    }
  }
  return true;
}
```

Benefits:
- Consistent naming (no `box` vs `bbox` confusion)
- More concise
- Works well with TypeScript's control flow

## Aliases at Runtime Too

Aliasing affects runtime behavior:

```typescript
const { bbox } = polygon;

if (!bbox) {
  calculatePolygonBbox(polygon);  // Fills in polygon.bbox
  // Now polygon.bbox exists, but bbox is still undefined!
}
```

The alias and original can diverge at runtime.

## Function Calls and Refinements

TypeScript makes a pragmatic choice about function calls:

```typescript
function expandPolygon(p: Polygon) { /* ... */ }

if (polygon.bbox) {
  polygon.bbox  // BoundingBox (narrowed)
  
  expandPolygon(polygon);
  
  polygon.bbox  // Still BoundingBox (TypeScript trusts you)
  // But the function might have set it to undefined!
}
```

TypeScript assumes functions don't invalidate refinements. This is usually fine but can be wrong.

## Safer: Local Variables

```typescript
if (polygon.bbox) {
  const bbox = polygon.bbox;  // Capture it locally
  
  expandPolygon(polygon);
  
  bbox  // Still BoundingBox - local variable is safe
}
```

Local variables can't be changed by function calls.

## Readonly for Extra Safety

```typescript
function safeExpand(p: Readonly<Polygon>) {
  // Can't modify p.bbox
}

if (polygon.bbox) {
  safeExpand(polygon);
  polygon.bbox  // Guaranteed still BoundingBox
}
```

Readonly parameters prevent mutation concerns.

## Common Patterns

### Nullish Coalescing Instead of Alias

```typescript
// Instead of:
const name = person.nickname;
const displayName = name ? name : person.fullName;

// Use:
const displayName = person.nickname ?? person.fullName;
```

### Map.get Pattern

```typescript
// TypeScript doesn't connect has() and get():
if (map.has(key)) {
  const value = map.get(key);  // Still T | undefined
}

// Better pattern:
const value = map.get(key);
if (value !== undefined) {
  value  // T (narrowed)
}

// Or with nullish coalescing:
const value = map.get(key) ?? defaultValue;
```

## Pressure Resistance Protocol

### 1. "I Need Both Names"

**Pressure:** "Sometimes I use the property, sometimes the variable"

**Response:** Pick one. Mixing them breaks narrowing.

**Action:** Use destructuring for consistent naming.

### 2. "The Function Won't Modify It"

**Pressure:** "I know expandPolygon doesn't touch bbox"

**Response:** TypeScript can't know that. Document with `Readonly`.

**Action:** Use local variables or readonly parameters for safety.

## Red Flags - STOP and Reconsider

- Variable created from property, then property used in condition
- Type errors about "possibly undefined" after an `if` check
- Mixing property access and variable use in the same block
- Relying on refinements after function calls

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "The alias is the same thing" | TypeScript tracks them separately |
| "I already checked the property" | Check doesn't narrow the alias |
| "Functions won't mutate it" | TypeScript can't verify that |

## Quick Reference

```typescript
// DON'T: Mix alias and original
const box = polygon.bbox;
if (polygon.bbox) {  // Checks original
  box.x;  // Uses alias - still possibly undefined!
}

// DO: Use alias consistently
const box = polygon.bbox;
if (box) {  // Checks alias
  box.x;  // Uses alias - narrowed correctly
}

// DO: Use destructuring
const { bbox } = polygon;
if (bbox) {
  const { x, y } = bbox;
}
```

## The Bottom Line

**Choose one name and use it consistently.**

When you alias a property, TypeScript tracks the alias and original separately. Narrowing one doesn't narrow the other. Use destructuring for consistent naming, and prefer local variables when function calls might invalidate refinements.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 23: Be Consistent in Your Use of Aliases.
