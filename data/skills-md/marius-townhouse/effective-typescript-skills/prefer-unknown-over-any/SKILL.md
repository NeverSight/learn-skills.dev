---
name: prefer-unknown-over-any
description: Use when receiving values of unknown type. Use when parsing JSON. Use when working with external data. Use instead of any.
---

# Use unknown Instead of any for Values with an Unknown Type

## Overview

**unknown is the type-safe cousin of any.**

When you don't know a value's type, use unknown. It forces you to narrow the type before using it, preventing bugs that any would allow.

## When to Use This Skill

- Parsing JSON or YAML
- Receiving data from external sources
- Working with user input
- Writing functions that accept anything
- Replacing any with something safer

## The Iron Rule

```
NEVER use any when unknown would work.
```

**No exceptions:**
- Not for "unknown is more verbose"
- Not for "I know it's safe"
- Not for "I'll check at runtime anyway"

## Detection: The "any for Unknown Data" Smell

If you're using any because you don't know the type, use unknown instead.

```typescript
// ❌ VIOLATION: any allows dangerous operations
function parseYAML(yaml: string): any {
  // ...
}

const data = parseYAML('...');
data.foo.bar.baz();        // No error! But will crash
data('call me maybe');     // No error! But will crash

// ✅ CORRECT: unknown forces you to check first
function safeParseYAML(yaml: string): unknown {
  // ...
}

const data = safeParseYAML('...');
data.foo.bar.baz();        // Error: 'data' is of type 'unknown'
data('call me maybe');     // Error: 'data' is of type 'unknown'
```

## any vs unknown: The Key Difference

| Property | any | unknown |
|----------|-----|---------|
| Anything assignable to it | Yes | Yes |
| Assignable to anything | Yes | **No** |
| Can call methods | Yes (danger!) | **No** (safe!) |
| Must narrow before use | No | **Yes** |

## Using unknown Safely

### With Type Assertion (when you're confident)

```typescript
interface Book {
  name: string;
  author: string;
}

const data = safeParseYAML(`
  name: Wuthering Heights
  author: Emily Bronte
`) as Book;  // You assert it's a Book

console.log(data.name);  // OK
```

### With instanceof (for classes)

```typescript
function processValue(value: unknown) {
  if (value instanceof Date) {
    value.toISOString();  // OK - value is Date
  }
}
```

### With typeof (for primitives)

```typescript
function processValue(value: unknown) {
  if (typeof value === 'string') {
    value.toUpperCase();  // OK - value is string
  }
  if (typeof value === 'number') {
    value.toFixed(2);     // OK - value is number
  }
}
```

### With Type Guards (for custom checks)

```typescript
interface Book {
  name: string;
  author: string;
}

function isBook(value: unknown): value is Book {
  return (
    typeof value === 'object' &&
    value !== null &&
    'name' in value &&
    'author' in value
  );
}

function processValue(value: unknown) {
  if (isBook(value)) {
    console.log(value.name, value.author);  // OK - value is Book
  }
}
```

## Common Use Cases

### JSON Parsing

```typescript
// ❌ BAD: JSON.parse returns any by default
const data = JSON.parse(response);
data.anything.goes();  // No error, but might crash

// ✅ GOOD: Parse as unknown, then validate
function parseJSON(text: string): unknown {
  return JSON.parse(text);
}

const data = parseJSON(response);
if (isValidResponse(data)) {
  // Now data is the validated type
}
```

### API Responses

```typescript
// ❌ BAD: Trusting the response
async function fetchUser(id: string): Promise<any> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// ✅ GOOD: Type unknown, validate before use
async function fetchUser(id: string): Promise<unknown> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

const user = await fetchUser('123');
if (isUser(user)) {
  console.log(user.name);  // Safe!
}
```

### Generic "Accept Anything" Functions

```typescript
// ❌ BAD: any loses all type info
function isSmallArray(arr: any[]): boolean {
  return arr.length < 10;
}

// ✅ GOOD: unknown[] is safer
function isSmallArray(arr: readonly unknown[]): boolean {
  return arr.length < 10;
}
```

## Narrowing unknown

TypeScript requires proof before it lets you use unknown:

```typescript
function process(value: unknown) {
  // Direct use: Error
  value.toString();  // Error: 'value' is of type 'unknown'
  
  // After null check
  if (value !== null && value !== undefined) {
    // Still unknown, but non-nullish
  }
  
  // After typeof check
  if (typeof value === 'string') {
    value.toUpperCase();  // OK: value is string
  }
  
  // After instanceof check
  if (value instanceof Date) {
    value.toISOString();  // OK: value is Date
  }
  
  // After type guard
  if (isBook(value)) {
    value.author;  // OK: value is Book
  }
}
```

## object, {}, and unknown

| Type | Includes | Does NOT include |
|------|----------|------------------|
| `unknown` | Everything | Nothing excluded |
| `{}` | Everything except null/undefined | null, undefined |
| `object` | Objects, arrays, functions | Primitives, null, undefined |

```typescript
// unknown is most broad - prefer it for "I don't know"
function acceptAnything(value: unknown) {}

// {} excludes null/undefined
function acceptNonNullish(value: {}) {}

// object excludes primitives
function acceptObject(value: object) {}
```

## Pressure Resistance Protocol

### 1. "unknown Is Too Verbose"

**Pressure:** "I have to add checks everywhere"

**Response:** Those checks catch bugs. any would let bugs through.

**Action:** Write the checks. They're documentation too.

### 2. "I Know The Type At Runtime"

**Pressure:** "I check the type before using it"

**Response:** With unknown, TypeScript verifies your checks are correct.

**Action:** Use unknown and let TypeScript track your narrowing.

### 3. "JSON.parse Returns any"

**Pressure:** "The built-in function returns any"

**Response:** Wrap it in a function that returns unknown.

**Action:** Create a safeParseJSON helper that returns unknown.

## Red Flags - STOP and Reconsider

- `any` for values from external sources
- `any` for parsed JSON/YAML
- `any` for API response bodies
- `any` just because "I don't know the type"
- Functions that accept `any` when they could accept `unknown`

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "I check at runtime" | unknown makes TypeScript verify your checks. |
| "It's too verbose" | Verbosity catches bugs. |
| "any is simpler" | Simpler to write, harder to debug. |
| "I trust the source" | External sources are never trustworthy. |

## Quick Reference

| Situation | Use |
|-----------|-----|
| Don't know the type | `unknown` |
| Parsing JSON/YAML | Return `unknown`, then validate |
| External API data | `unknown` until validated |
| Accept any value | `unknown` (not `any`) |
| Array of anything | `unknown[]` (not `any[]`) |

## The Bottom Line

**unknown says "I don't know this type." any says "I don't care about types."**

Use unknown when you genuinely don't know a value's type. It forces you to narrow before use, catching bugs that any would miss. Your code will be safer and more explicit about where type information comes from.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 46: Use unknown Instead of any for Values with an Unknown Type.
