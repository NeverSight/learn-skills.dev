---
name: type-display-attention
description: Use when complex types display poorly in IDE. Use when users see ugly type expansions. Use when debugging type issues. Use when building public APIs. Use when types become deeply nested.
---

# Pay Attention to How Types Display

## Overview

The types you write are not just for the compiler - they're also for developers reading code in their IDE. Complex types can display as unwieldy expansions that obscure meaning and hurt developer experience. Understanding how to control type display helps you create types that are both correct and readable.

Type display matters for debugging, API usability, and overall developer productivity. A type that works correctly but displays poorly creates friction.

## When to Use This Skill

- Complex types display poorly in hover tooltips
- Users see expanded instead of named types
- Debugging confusing type errors
- Building public APIs with generic types
- Types become deeply nested or recursive

## The Iron Rule

**Control how types display using type aliases and identity mapped types. Ensure your types are readable in IDE tooltips and error messages.**

## Detection

Watch for these display issues:

```typescript
// UGLY DISPLAY - Users see this expansion:
// { [K in keyof T as ToCamel<K & string>]: T[K] }
// Instead of a clean name

// CONFUSING ERROR - Type displays as:
// { a: { b: { c: { d: string } } } }
// Instead of: DeepNested<string>
```

## The Identity Mapped Type Trick

Force TypeScript to preserve a type alias:

```typescript
// Without trick - displays as expansion
type ObjectToCamel<T> = {
  [K in keyof T as ToCamel<K & string>]: T[K]
};

const result = objectToCamel({ foo_bar: 1 });
// Hover shows: { [K in keyof T as ToCamel<... 

// With identity mapped type - displays as name
type ObjectToCamel<T> = {
  [K in keyof T as ToCamel<K & string>]: T[K]
} extends infer O 
  ? { [K in keyof O]: O[K] } 
  : never;

const result = objectToCamel({ foo_bar: 1 });
// Hover shows: ObjectToCamel<{ foo_bar: number }>
```

## Creating Clean Type Aliases

```typescript
// BAD: Complex inline type
function processData(
  input: { [K in keyof User as `set${Capitalize<K & string>}`]: User[K] }
): void;

// GOOD: Named type alias
type SetterMethods<T> = {
  [K in keyof T as `set${Capitalize<K & string>}`]: T[K]
};

function processData(input: SetterMethods<User>): void;
// Displays as: SetterMethods<User>
```

## Simplifying Complex Return Types

```typescript
// Complex generic return type
type QueryResult<T> = T extends { data: infer D }
  ? D extends Array<infer Item>
    ? PaginatedResult<Item>
    : SingleResult<D>
  : ErrorResult;

// Simplify display with intermediate type
type QueryResult<T> = T extends { data: infer D }
  ? QueryResultHelper<D>
  : ErrorResult;

type QueryResultHelper<D> = D extends Array<infer Item>
  ? PaginatedResult<Item>
  : SingleResult<D>;
```

## Hiding Implementation Details

```typescript
// Internal complex type
type InternalTransform<T> = /* complex 10-line type */;

// Public clean type
type PublicType<T> = InternalTransform<T> extends infer R
  ? { [K in keyof R]: R[K] }
  : never;

// Users see: PublicType<T>
// Not the messy InternalTransform expansion
```

## Preserving Type Names in Unions

```typescript
// Each branch keeps its name
type Result<T> = 
  | { type: 'success'; data: T }
  | { type: 'error'; error: Error }
  | { type: 'loading' };

// Displays cleanly as:
// Result<User> = 
//   | { type: 'success'; data: User }
//   | { type: 'error'; error: Error }
//   | { type: 'loading' }
```

## Testing Type Display

Check how your types appear in practice:

```typescript
// Create test cases to see how types display
type TestCase1 = YourComplexType<{ a: string }>;
// Hover over TestCase1 to see display

type TestCase2 = YourComplexType<{ nested: { deep: number } }>;
// Check nested case

// Check error messages
const x: TestCase1 = {} as any;
// Trigger an error to see how type appears in message
```

## IDE-Specific Considerations

Different IDEs display types differently:

```typescript
// VS Code: Hover to see type
type Example = /* your type */;

// Check in:
// - Hover tooltips
// - IntelliSense autocomplete
// - Error message panels
// - Quick fix suggestions
```

## Pressure Resistance Protocol

When types display poorly:

1. **Check hover tooltips**: See what users actually see
2. **Introduce aliases**: Break complex types into named pieces
3. **Use identity mapped type**: Force preservation of type names
4. **Test error messages**: Ensure errors reference clean type names
5. **Consider simplification**: Maybe the type is too complex

## Red Flags

| Symptom | Problem | Solution |
|---------|---------|----------|
| Type shows as expansion | Not preserving alias | Identity mapped type |
| Deeply nested display | Too many levels | Intermediate type aliases |
| Generic noise | Too many type params | Simplify or use defaults |
| Unreadable in errors | Complex conditional | Named result types |

## Common Rationalizations

### "Users can read the expansion"

**Reality**: Complex expansions are hard to read. Clean names convey intent immediately.

### "It's just for internal use"

**Reality**: Internal types are read by colleagues (and future you). Clean display helps everyone.

### "The type is inherently complex"

**Reality**: You can hide complexity behind clean interfaces. Users don't need to see all the machinery.

## Quick Reference

| Technique | Syntax | Use When |
|-----------|--------|----------|
| Type alias | `type Name = ...` | Any complex type |
| Identity mapped | `extends infer O ? { [K in keyof O]: O[K] } : never` | Force name preservation |
| Intermediate types | Break into steps | Multi-step transformations |
| Union branches | Named object types | Discriminated unions |

## The Bottom Line

Types are user interface. Control how they display using aliases and identity mapped types. Readable types in hover tooltips and error messages improve developer experience.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 56: Pay Attention to How Types Display
