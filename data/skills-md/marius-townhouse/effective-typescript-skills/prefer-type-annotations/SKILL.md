---
name: prefer-type-annotations
description: Use when assigning values to variables with types. Use when tempted to use type assertions. Use when TypeScript flags type errors you want to silence.
---

# Prefer Type Annotations to Type Assertions

## Overview

**Type annotations (: Type) verify that values conform to types. Type assertions (as Type) tell TypeScript to trust you.**

Annotations check your work. Assertions bypass checks. When you have a choice, prefer annotations.

## When to Use This Skill

- Assigning values to variables
- Defining function return types
- Working with object literals
- Tempted to use `as Type` to fix errors
- Getting "not assignable" errors

## The Iron Rule

```
NEVER use type assertions when type annotations would work.
```

**No exceptions:**
- Not for "it's obviously correct"
- Not for "I know better than TypeScript"
- Not for "the assertion is simpler"

## Detection: The "as" Smell

See `as SomeType`? Ask: "Could I use a type annotation instead?"

```typescript
// ❌ VIOLATION: Type assertion bypasses checking
const alice = {} as Person;  // No error! But alice has no properties

// ✅ CORRECT: Type annotation verifies the value
const alice: Person = {};
// ~~~~~ Property 'name' is missing in type '{}' but required in type 'Person'
```

## The Critical Difference

### Type Annotation (Safe)

```typescript
interface Person { name: string }

// TypeScript CHECKS that the value matches the type
const bob: Person = { name: 'Bob' };  // OK
const bad: Person = {};                // Error: missing 'name'
const extra: Person = { 
  name: 'Carol', 
  age: 30           // Error: 'age' does not exist on type 'Person'
};
```

### Type Assertion (Unsafe)

```typescript
// TypeScript TRUSTS you that the value matches the type
const bob = {} as Person;       // No error, but wrong!
const bad = { foo: 1 } as Person;  // No error, but wrong!
```

## Arrow Functions: Annotate Returns

```typescript
// ❌ VIOLATION: Assertion hides errors
const people = ['alice', 'bob'].map(name => ({name} as Person));

// Even worse: completely wrong values slip through
const people = ['alice', 'bob'].map(name => ({} as Person));  // No error!

// ✅ CORRECT: Annotate the return type
const people = ['alice', 'bob'].map((name): Person => ({name}));  // OK
const people = ['alice', 'bob'].map((name): Person => ({}));
//                                                     ~~ Error: missing 'name'
```

## When Assertions ARE Appropriate

Type assertions make sense when **you truly know more than TypeScript**:

### 1. DOM Elements

```typescript
// You know #myButton exists and is a button
const button = document.querySelector('#myButton') as HTMLButtonElement;

// Better: include a comment explaining why
const button = document.querySelector('#myButton') as HTMLButtonElement;
// This button is created in index.html and always exists
```

### 2. After Runtime Checks

```typescript
const el = document.getElementById('foo');
if (el) {
  el.innerHTML = 'Hello';  // TypeScript knows el is not null
}

// Or with non-null assertion (use sparingly!)
const el = document.getElementById('foo')!;
```

## Pressure Resistance Protocol

### 1. "The Error Is Wrong"

**Pressure:** "TypeScript is complaining but my code is correct"

**Response:** TypeScript is usually right. Read the error message carefully.

**Action:** 
1. Check if your type definition matches your intention
2. Check if your value actually matches the type
3. Only use assertion if you can explain WHY TypeScript is wrong

### 2. "The Assertion Is Simpler"

**Pressure:** "Adding annotations everywhere is verbose"

**Response:** Annotations catch bugs. Assertions hide them. Safety > brevity.

**Action:** Add the annotation. Your future self will thank you.

### 3. "I Know The Type At Runtime"

**Pressure:** "I checked the type at runtime, so assertion is safe"

**Response:** If you checked at runtime, TypeScript should be able to narrow the type.

**Action:** Use a type guard or conditional to narrow, not an assertion.

## Red Flags - STOP and Reconsider

- `as any` anywhere in your code
- `as Type` immediately after creating an object
- Multiple assertions in a chain (`x as A as B`)
- Assertions to fix "not assignable" errors
- `!` (non-null assertion) without good reason

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "I know it's a Person" | Then prove it with an annotation, not an assertion. |
| "TypeScript is wrong" | TypeScript found a real inconsistency. Investigate. |
| "It's just one assertion" | Assertions spread. One leads to many. |
| "The types are too strict" | Strict types catch bugs. Embrace them. |

## Quick Reference

| Situation | Use Annotation | Use Assertion |
|-----------|----------------|---------------|
| Variable declaration | `:Type` | Never |
| Function parameter | `:Type` | Never |
| Function return | `:Type` | Rarely |
| Object literal | `:Type` | Never |
| DOM element you know | - | `as HTMLElement` with comment |
| After null check | - | `!` if certain |
| Unknown value from API | - | After validation with `unknown` |

## The Non-Null Assertion (`!`)

```typescript
// Tells TypeScript: "Trust me, this isn't null"
const el = document.getElementById('foo')!;

// Prefer a runtime check:
const el = document.getElementById('foo');
if (!el) throw new Error('No element #foo');
// Now TypeScript knows el is not null
```

## The Bottom Line

**Type annotations are a contract. Type assertions are a lie you tell TypeScript.**

Use annotations to declare your intentions. Use assertions only when you have information TypeScript cannot have. Always include a comment explaining why an assertion is valid.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 9: Prefer Type Annotations to Type Assertions.
