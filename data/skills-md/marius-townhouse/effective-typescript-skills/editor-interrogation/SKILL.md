---
name: editor-interrogation
description: Use when debugging type inference. Use when types behave unexpectedly. Use when learning unfamiliar code.
---

# Use Your Editor to Interrogate and Explore the Type System

## Overview

**Your editor is your best TypeScript learning tool.**

TypeScript's language services provide autocomplete, inspection, navigation, and refactoring. These aren't just conveniences - they're the primary way to understand what TypeScript thinks about your code.

## When to Use This Skill

- Debugging unexpected type inference
- Understanding widening and narrowing behavior
- Exploring unfamiliar codebases
- Learning how libraries model their types
- Verifying that inferred return types match expectations

## The Iron Rule

```
ALWAYS hover to verify types when behavior is unexpected.
```

**Remember:**
- Inferred types can differ from your expectations
- The editor shows what TypeScript ACTUALLY thinks
- "Go to Definition" reveals library type implementations
- Refactoring tools understand scope and imports

## Detection: When to Interrogate

Check types when:

```typescript
// 1. Type inference seems wrong
const num = 10;        // Hover: what's the type?
const str = "hello";   // Is it string or literal "hello"?

// 2. Function returns don't match expectations
function add(a: number, b: number) {
  return a + b;
}
// Hover over `add` - is return type number?

// 3. Narrowing isn't working as expected
function process(x: string | null) {
  if (x) {
    x  // Hover here - should be string, not string | null
  }
}
```

## Editor Inspection Techniques

### Hover for Inferred Types

```typescript
const list = [1, 2, 3];
//    ^? const list: number[]

const tuple = [1, 2, 3] as const;
//    ^? const tuple: readonly [1, 2, 3]
```

### Inspect Generics in Chains

```typescript
const result = "a,b,c"
  .split(",")   // Hover: Array<string>
  .map(Number)  // Hover: number[]
  .filter(n => n > 0);  // Hover: number[]
```

### Watch Narrowing in Branches

```typescript
function example(x: string | number | null) {
  if (typeof x === "string") {
    x  // Hover: string
  } else if (x) {
    x  // Hover: number
  } else {
    x  // Hover: number | null
  }
}
```

## "Go to Definition" for Library Types

Explore external types:

```typescript
// Click "Go to Definition" on fetch
const response = await fetch('/api');
// Takes you to lib.dom.d.ts:
// declare function fetch(
//   input: RequestInfo | URL, init?: RequestInit
// ): Promise<Response>;

// Click through RequestInit to see all options:
// interface RequestInit {
//   body?: BodyInit | null;
//   cache?: RequestCache;
//   headers?: HeadersInit;
//   ...
// }
```

## Refactoring Tools

### Rename Symbol (F2)

Rename understands scope:

```typescript
let i = 0;
for (let i = 0; i < 10; i++) {  // Rename this i
  console.log(i);               // This updates
  {
    let i = 12;                 // This stays unchanged
    console.log(i);
  }
}
console.log(i);                 // This stays unchanged
```

### Move Symbol to New File

- Automatically updates imports
- Works across the entire project

### Extract Method/Variable

- Creates typed functions from selected code
- Preserves type information

## Common Gotchas to Check

### typeof null

```typescript
function getElement(x: string | HTMLElement | null) {
  if (typeof x === 'object') {
    x  // Hover: HTMLElement | null (not just HTMLElement!)
    // typeof null === 'object' in JavaScript
  }
}
```

### Optional Properties vs Undefined

```typescript
interface Config {
  name?: string;
}

const config: Config = {};
config.name  // Hover: string | undefined
```

### Array Index Access

```typescript
const arr = [1, 2, 3];
arr[10]  // Hover: number (not number | undefined!)
// Unless noUncheckedIndexedAccess is enabled
```

## Pressure Resistance Protocol

### 1. "I Know What the Type Is"

**Pressure:** "I don't need to hover, I know it's a string"

**Response:** Assumptions cause bugs. The editor shows truth.

**Action:** Hover anyway. 2 seconds to verify.

### 2. "Library Types Are Too Complex"

**Pressure:** "I can't understand these generic types"

**Response:** Click through one piece at a time. Follow the breadcrumbs.

**Action:** Use "Go to Definition" iteratively.

## Red Flags - STOP and Check

- Type errors you don't understand
- Runtime errors that "shouldn't happen"
- Generic types that look wrong
- Narrowing that doesn't seem to work

## Quick Reference

| Action | VS Code Shortcut |
|--------|------------------|
| Hover for type | Mouse over symbol |
| Go to Definition | F12 or Cmd/Ctrl+Click |
| Find All References | Shift+F12 |
| Rename Symbol | F2 |
| Quick Fix | Cmd/Ctrl+. |

## The Bottom Line

**Your editor knows more about your types than you do.**

When types behave unexpectedly, don't guess - inspect. Hover over symbols, follow definitions, and watch how types narrow. This builds intuition faster than any documentation.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 6: Use Your Editor to Interrogate and Explore the Type System.
