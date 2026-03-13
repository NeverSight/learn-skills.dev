---
name: limit-any-type
description: Use when tempted to use any type. Use when getting type errors that seem hard to fix. Use when migrating JavaScript to TypeScript.
---

# Limit Use of the any Type

## Overview

**The any type effectively disables TypeScript's type checker for the code that uses it.**

While any can be useful as an escape hatch, it eliminates the benefits of TypeScript: type safety, developer experience, refactoring confidence, and bug prevention.

## When to Use This Skill

- Reaching for any to silence a type error
- Migrating JavaScript code to TypeScript
- Working with third-party libraries without types
- Feeling frustrated with complex type errors
- Adding type annotations to existing code

## The Iron Rule

```
NEVER use any without a specific, documented reason.
```

**No exceptions:**
- Not for "it's just a quick fix"
- Not for "the type is too complicated"
- Not for "I'll fix it later"
- Not for "it works at runtime"

## Detection: The "any Smell"

If you're typing `any`, stop and ask: "Is there a better way?"

```typescript
// ❌ VIOLATION: Using any because it's "easy"
function processData(data: any) {
  return data.items.map((item: any) => item.name);
}

// ✅ CORRECT: Define proper types
interface DataItem {
  name: string;
}
interface Data {
  items: DataItem[];
}
function processData(data: Data) {
  return data.items.map(item => item.name);
}
```

## The Five Dangers of any

### 1. No Type Safety

```typescript
let age: number;
age = '12' as any;  // No error, but wrong!
age += 1;           // "121" at runtime
```

### 2. Breaks Contracts

```typescript
function calculateAge(birthDate: Date): number { /* ... */ }

let birthDate: any = '1990-01-19';  // string, not Date!
calculateAge(birthDate);  // No error, but will fail
```

### 3. No Language Services

```typescript
// With proper types: autocomplete, refactoring, documentation
person.  // Shows: name, age, email...

// With any: nothing
(person as any).  // No autocomplete
```

### 4. Masks Refactoring Bugs

```typescript
interface Props {
  onSelectItem: (id: number) => void;  // Changed from (item: any)
}

function handleSelectItem(item: any) {
  selectedId = item.id;  // Bug! Should be just `item` now
}
```

### 5. Hides Type Design

```typescript
// ❌ BAD: What is this state?
const appState: any = { /* ... */ };

// ✅ GOOD: Clear, documented design
interface AppState {
  user: User | null;
  preferences: UserPreferences;
  isLoading: boolean;
}
```

## Pressure Resistance Protocol

### 1. "It's Too Complicated"

**Pressure:** "The type is so complex, any is easier"

**Response:** Complex types often indicate complex data. Defining the type forces you to understand and document your data model.

**Action:** Break down the type. Use interfaces and type aliases. Ask: "What does this data actually look like?"

### 2. "I'll Fix It Later"

**Pressure:** "I'll come back and add proper types"

**Response:** You won't. Technical debt accumulates. any spreads through your codebase.

**Action:** Fix it now. If you truly can't, add a // TODO with a ticket number.

### 3. "The Library Doesn't Have Types"

**Pressure:** "This npm package has no @types"

**Response:** You have options: write minimal types, use unknown, or create a .d.ts file.

**Action:** Use unknown for values you don't control. Create focused interface for what you actually use.

## Better Alternatives to any

| Instead of | Use |
|------------|-----|
| `any` for unknown values | `unknown` (forces you to narrow) |
| `any[]` | `unknown[]` or specific type |
| `(x: any) => any` | Proper function signature |
| `Record<string, any>` | `Record<string, unknown>` |
| `any` for JSON | Parse and validate with unknown |

## Red Flags - STOP and Reconsider

- Multiple `any` types in a single function
- `as any` to silence errors
- `// @ts-ignore` or `@ts-expect-error` to bypass checking
- any in public API signatures
- any in function return types

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It works at runtime" | Types exist to catch bugs BEFORE runtime. |
| "TypeScript is too strict" | TypeScript is protecting you. Learn what it's saying. |
| "I don't know the type" | Use `unknown` and narrow it. |
| "Third-party library" | Write minimal types for what you use. |
| "It's just internal code" | Internal code is still code. You'll debug it later. |

## Quick Reference

| Symptom | Action |
|---------|--------|
| Type error you don't understand | Read the error carefully, use `unknown` |
| Complex nested type | Break into smaller interfaces |
| Dynamic data from API | Define response type, validate at boundary |
| Migrating from JS | Start with `unknown`, gradually add types |

## The Bottom Line

**Every any is a bug waiting to happen.**

Use `unknown` for values you don't know. Use proper types for values you do. When you must use any, scope it narrowly, document why, and plan to eliminate it.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 5: Limit Use of the any Type.
