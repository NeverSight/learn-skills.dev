---
name: no-type-in-docs
description: Use when writing comments about types. Use when documenting function parameters. Use when naming variables.
---

# Don't Repeat Type Information in Documentation

## Overview

**Type annotations are your documentation. Don't duplicate them in comments.**

Comments describing types get out of sync with code. TypeScript's type system is designed to be compact and readable - use it as your primary source of type documentation.

## When to Use This Skill

- Writing JSDoc or comments for functions
- Documenting parameter types
- Naming variables
- Describing return values

## The Iron Rule

```
Never put type information in comments.
Let the type annotations speak for themselves.
```

**Remember:**
- Comments drift out of sync; types are checked
- Type annotations are designed to be readable
- Comments should explain WHY, not WHAT type
- Variable names shouldn't include type info

## Detection: Type Info in Comments

```typescript
/**
 * Returns a string with the foreground color.
 * Takes zero or one arguments. With no arguments, returns the
 * standard foreground color. With one argument, returns the foreground color
 * for a particular page.
 */
function getForegroundColor(page?: string) {
  return page === 'login' ? {r: 127, g: 127, b: 127} : {r: 0, g: 0, b: 0};
}
```

Problems:
- Comment says "returns a string" but function returns an object
- Comment describes parameter count (visible in signature)
- Comment is longer than the implementation!

## Better Documentation

```typescript
/** Get the foreground color for the application or a specific page. */
function getForegroundColor(page?: string): Color {
  // ...
}
```

The type signature tells you:
- Parameter is optional string
- Return type is Color
- No need to repeat this in comments

## Don't Document Non-Mutation

```typescript
// Bad: comment lies (sort() mutates in place)
/** Sort the strings by numeric value. Does not modify nums. */
function sortNumerically(nums: string[]): string[] {
  return nums.sort((a, b) => Number(a) - Number(b));
}

// Good: type enforces non-mutation
/** Sort the strings by numeric value. */
function sortNumerically(nums: readonly string[]): string[] {
  return nums.toSorted((a, b) => Number(a) - Number(b));
}
```

The `readonly` modifier is enforced by TypeScript. Comments are not.

## Variable Names

Don't include types in variable names:

```typescript
// Bad: redundant type in name
const ageNum = 30;
const nameString = 'Alice';
const usersArray = [];

// Good: descriptive names, types inferred
const age = 30;
const name = 'Alice';
const users = [];
```

### Exception: Units

Include units when not obvious from type:

```typescript
// Good: units aren't captured by type
const timeMs = 1000;
const temperatureC = 20;
const distanceKm = 5.5;

// Better: use branded types (Item 64)
type Milliseconds = number & { _brand: 'ms' };
const time: Milliseconds = 1000 as Milliseconds;
```

## JSDoc Best Practices

Use @param for parameter documentation, not type info:

```typescript
/**
 * Formats a user's display name.
 * @param user - The user to format
 * @param options - Formatting options
 * @returns The formatted display name
 */
function formatDisplayName(
  user: User,
  options?: FormatOptions
): string {
  // ...
}
```

Don't duplicate type information:

```typescript
// Bad: duplicates types
/**
 * @param user {User} - The user object
 * @param options {FormatOptions | undefined} - Optional formatting options
 * @returns {string} The formatted name
 */
```

## What Comments SHOULD Include

- Purpose and intent
- Business logic explanations
- Algorithm descriptions
- Non-obvious behavior
- Links to relevant documentation

```typescript
/**
 * Calculates compound interest using the standard formula.
 * See: https://en.wikipedia.org/wiki/Compound_interest
 */
function compoundInterest(
  principal: number,
  rate: number,
  periods: number
): number {
  // P(1 + r)^n
  return principal * Math.pow(1 + rate, periods);
}
```

## Pressure Resistance Protocol

### 1. "Comments Make Code More Readable"

**Pressure:** "I want to document types for clarity"

**Response:** Types ARE documentation. They're checked, always accurate.

**Action:** Remove type info from comments. Improve type names if unclear.

### 2. "I Need to Document Complex Types"

**Pressure:** "The type is complicated, I need to explain it"

**Response:** Use TSDoc on the type definition itself.

**Action:** Add documentation to the type, not the usage.

## Red Flags - STOP and Reconsider

- Comments mentioning "returns a string" or similar
- Parameter count mentioned in comments
- "Does not modify" claims (use readonly instead)
- Variable names like `numUsers` or `strName`

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's more readable" | Types are designed to be readable |
| "Not everyone knows TypeScript" | They can hover/click to see types |
| "Documentation is always good" | Outdated documentation is harmful |

## Quick Reference

```typescript
// DON'T: Type info in comments
/** Returns string, takes number */ 
function f(n: number): string { ... }

// DON'T: Claim non-mutation in comments
/** Does not modify array */
function sort(arr: number[]): number[] { ... }

// DON'T: Types in variable names
const ageNum = 30;

// DO: Describe purpose, not types
/** Get display name for UI header */
function getName(user: User): string { ... }

// DO: Use readonly for non-mutation
function sort(arr: readonly number[]): number[] { ... }

// DO: Units in names when helpful
const timeMs = 1000;
```

## The Bottom Line

**Type annotations are your documentation.**

TypeScript's type system is expressive and always accurate. Comments about types will drift out of sync and mislead readers. Use comments to explain purpose, intent, and business logic - not types.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 31: Don't Repeat Type Information in Documentation.
