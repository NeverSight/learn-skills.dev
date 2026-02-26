---
name: type-value-space
description: Use when symbols are ambiguous. Use when class or typeof behaves unexpectedly. Use when destructuring fails.
---

# Know How to Tell Whether a Symbol Is in Type Space or Value Space

## Overview

**Every symbol in TypeScript exists in type space, value space, or both.**

The same name can refer to completely different things depending on context. Understanding this distinction is essential for reading TypeScript code correctly.

## When to Use This Skill

- Debugging confusing type errors
- Understanding class vs interface behavior
- Using typeof correctly
- Destructuring with type annotations
- Understanding enum behavior

## The Iron Rule

```
ALWAYS determine whether you're in type space or value space before interpreting a symbol.
```

**Remember:**
- Types are erased at runtime (use TypeScript Playground to verify)
- Classes introduce BOTH a type AND a value
- typeof means different things in each space
- Destructuring syntax differs from type annotation syntax

## Detection: Same Name, Different Meaning

```typescript
// Same name, different entities!
interface Cylinder {
  radius: number;
  height: number;
}
const Cylinder = (radius: number, height: number) => ({ radius, height });

// This refers to the VALUE (function), not the TYPE (interface)
if (shape instanceof Cylinder) {
  // instanceof is a runtime operator - uses value space
}
```

## The Two Spaces

### Type Space (Erased at Runtime)

```typescript
type StringAlias = string;     // Type alias
interface Person { name: string; }  // Interface
type T = typeof myVar;         // Type-level typeof
```

### Value Space (Exists at Runtime)

```typescript
const x = 123;                 // Variable
function add(a, b) { return a + b; }  // Function
const t = typeof myVar;        // Runtime typeof (returns string)
```

### Both Spaces (class and enum)

```typescript
class MyClass {
  value: number = 0;
}

// As a type: describes the shape of instances
const instance: MyClass = new MyClass();

// As a value: the constructor function
const ctor = MyClass;  // typeof ctor is typeof MyClass
```

## Context Determines Space

### After `:` or `as` = Type Space

```typescript
const alice: Person = { name: 'Alice' };
//           ^^^^^^ Type space

const bob = someValue as Person;
//                       ^^^^^^ Type space
```

### After `=` = Value Space

```typescript
const x = Person;  // Value space (error if Person is only a type)
```

### Function Signatures Alternate

```typescript
function email(to: Person, subject: string, body: string): Response {
//             ^^          ^^^^^^^          ^^^^           ^^^^^^^^ Types
//       ^^^^^^^ ^^        ^^^^^^^ ^^^^^^   ^^^^ ^^^^              Values
}
```

## typeof: Different in Each Space

### Type Space typeof

```typescript
const person = { name: 'Alice', age: 30 };

type PersonType = typeof person;
//   ^? type PersonType = { name: string; age: number }

// Gets the TypeScript type of a value
```

### Value Space typeof

```typescript
const person = { name: 'Alice', age: 30 };

const t = typeof person;  // "object"
// JavaScript's runtime typeof - only 8 possible values:
// "string", "number", "boolean", "undefined", 
// "object", "function", "symbol", "bigint"
```

## Other Dual-Meaning Constructs

| Construct | Type Space | Value Space |
|-----------|------------|-------------|
| `typeof` | TypeScript type of value | JS runtime type (8 options) |
| `this` | Type of `this` | JS `this` keyword |
| `&`, `\|` | Intersection, union | Bitwise AND, OR |
| `const` | `as const` context | Variable declaration |
| `extends` | Subtype/constraint | Subclass |
| `in` | Mapped types | `for...in` loops |
| `!` | Non-null assertion | Logical NOT |

## Property Access: `[]` vs `.`

```typescript
interface Person {
  first: string;
  last: string;
}

// Value space: both work
const name1 = person['first'];
const name2 = person.first;

// Type space: ONLY brackets work
type First = Person['first'];     // OK: string
type First2 = Person.first;       // Error!
```

## Common Mistake: Destructuring with Types

### Wrong: Type Names in Value Position

```typescript
function email({
  to: Person,      // Error! 'Person' implicitly has 'any' type
  subject: string, // Error! 'string' implicitly has 'any' type
}) { }
// This creates variables named Person and string!
```

### Right: Separate Types from Destructuring

```typescript
function email(
  { to, subject, body }: { to: Person; subject: string; body: string }
) { }
// Destructures values, then annotates the whole parameter
```

## Using the TypeScript Playground

The Playground shows what's erased:

```typescript
interface Person { name: string; }  // Disappears in JS
type StringType = string;           // Disappears in JS

class MyClass { }                   // Stays (has runtime value)
const x = 42;                       // Stays (has runtime value)
```

If a symbol disappears in the JS output, it was in type space only.

## Pressure Resistance Protocol

### 1. "instanceof Should Work with Interfaces"

**Pressure:** "Why doesn't `x instanceof MyInterface` work?"

**Response:** `instanceof` is a runtime operator. Interfaces don't exist at runtime.

**Action:** Use type guards or discriminated unions instead.

### 2. "typeof Should Give Me the Full Type"

**Pressure:** "Why is `typeof x` just 'object'?"

**Response:** You're using value-space typeof. For the TypeScript type, use it in a type annotation.

**Action:** `type T = typeof x` for the full TypeScript type.

## Red Flags - STOP and Reconsider

- `instanceof` with an interface or type alias
- Expecting runtime typeof to distinguish object shapes
- Destructuring that creates unexpected variable names
- Type errors mentioning "cannot be used as a value"

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Class and interface are the same" | Classes have runtime values; interfaces don't |
| "typeof works the same everywhere" | Completely different meaning in type vs value space |
| "I can destructure with type names" | Destructuring uses value space; annotations use type space |

## Quick Reference

```typescript
// Type space indicators:
type X = ...       // After 'type'
interface X { }    // After 'interface'
x: Type            // After ':'
as Type            // After 'as'

// Value space indicators:
const x = ...      // After '='
x instanceof Y     // instanceof operand
typeof x           // Without type annotation

// Both spaces:
class X { }        // Introduces type and value
enum X { }         // Introduces type and value
```

## The Bottom Line

**Context determines whether a symbol refers to a type or a value.**

The same name can mean completely different things. When code is confusing, first determine which space you're in. Use the TypeScript Playground to see what gets erased - that's your type space.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 8: Know How to Tell Whether a Symbol Is in the Type Space or Value Space.
