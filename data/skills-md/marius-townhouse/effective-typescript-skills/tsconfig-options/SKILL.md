---
name: tsconfig-options
description: Use when setting up a TypeScript project. Use when confused by type checking behavior. Use when strict mode causes unexpected errors.
---

# Know Which TypeScript Options You're Using

## Overview

**TypeScript's behavior depends heavily on configuration.**

The same code can pass or fail type checking depending on options like `noImplicitAny` and `strictNullChecks`. Know your options to use TypeScript effectively.

## When to Use This Skill

- Setting up a new TypeScript project
- Code behaves differently than expected
- Debugging type errors that others don't see
- Deciding on strictness level

## The Iron Rule

```
ALWAYS use a tsconfig.json and enable strict mode for new projects.
```

**Key Settings:**
- `noImplicitAny`: Require explicit types when TypeScript can't infer
- `strictNullChecks`: Make null/undefined explicit in types
- `strict`: Enable all strict checks (recommended)

## The Most Important Options

### noImplicitAny

Controls whether TypeScript allows implicit `any` types:

```typescript
// With noImplicitAny: false (OFF) - No error
function add(a, b) {
  return a + b;
}
// a and b are implicitly 'any' - dangerous!

// With noImplicitAny: true (ON) - Error
function add(a, b) {
  //         ~  Parameter 'a' implicitly has an 'any' type
  //            ~  Parameter 'b' implicitly has an 'any' type
  return a + b;
}

// Fixed:
function add(a: number, b: number) {
  return a + b;
}
```

### strictNullChecks

Controls whether null/undefined are allowed in all types:

```typescript
// With strictNullChecks: false (OFF)
const x: number = null;  // OK, but dangerous

// With strictNullChecks: true (ON)
const x: number = null;
//    ~ Type 'null' is not assignable to type 'number'

// Fixed - be explicit:
const x: number | null = null;  // OK
```

### Handling Nullable Values

```typescript
// strictNullChecks forces you to handle null:
const statusEl = document.getElementById('status');

statusEl.textContent = 'Ready';
// ~~~~~~ 'statusEl' is possibly 'null'.

// Option 1: Check for null
if (statusEl) {
  statusEl.textContent = 'Ready';  // OK
}

// Option 2: Assert non-null (use carefully!)
statusEl!.textContent = 'Ready';  // OK
```

## Recommended Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,  // Enables all strict checks
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}
```

Create with: `tsc --init`

## Strict Mode Includes

The `strict` flag enables:
- `noImplicitAny`
- `strictNullChecks`
- `strictFunctionTypes`
- `strictBindCallApply`
- `strictPropertyInitialization`
- `noImplicitThis`
- `alwaysStrict`

## Stricter Than Strict

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true  // Extra safety for array/object access
  }
}
```

With `noUncheckedIndexedAccess`:

```typescript
const arr = ['a', 'b', 'c'];
arr[0].toUpperCase();  // Error: Object is possibly 'undefined'

// Must check:
const first = arr[0];
if (first) {
  first.toUpperCase();  // OK
}
```

## Migration Path

For existing JavaScript projects:

1. Start with minimal settings
2. Enable `noImplicitAny`
3. Fix all implicit any errors
4. Enable `strictNullChecks`
5. Eventually reach full `strict` mode

## Pressure Resistance Protocol

### 1. "Strict Mode Is Too Hard"

**Pressure:** "There are too many errors with strict mode"

**Response:** Each error is a potential bug. Fix incrementally.

**Action:** Enable strict, fix errors one file at a time.

### 2. "We Don't Need Types on Everything"

**Pressure:** "Implicit any is fine, we know what the types are"

**Response:** You know. TypeScript doesn't. Future maintainers won't.

**Action:** Enable `noImplicitAny` - types are documentation.

## Red Flags - STOP and Reconsider

- No tsconfig.json in project
- Using command-line flags instead of config file
- `strict: false` without a migration plan
- Different team members using different settings

## Quick Reference

| Option | Effect | Recommendation |
|--------|--------|----------------|
| `strict` | Enable all strict checks | Always for new projects |
| `noImplicitAny` | Require explicit types | Essential |
| `strictNullChecks` | null/undefined must be explicit | Essential |
| `noUncheckedIndexedAccess` | Array access might be undefined | Consider enabling |

## The Bottom Line

**Know your options. Enable strict mode.**

TypeScript's behavior depends on configuration. Use tsconfig.json, enable strict mode for new projects, and understand what `noImplicitAny` and `strictNullChecks` do. Consistent configuration across your team is essential.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 2: Know Which TypeScript Options You're Using.
