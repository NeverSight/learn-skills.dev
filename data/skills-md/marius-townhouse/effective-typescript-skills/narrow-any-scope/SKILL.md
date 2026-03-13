---
name: narrow-any-scope
description: Use when any is unavoidable. Use when working with untyped libraries. Use when silencing specific type errors.
---

# Use the Narrowest Possible Scope for any Types

## Overview

**If you must use any, contain the damage.**

any is contagious - it spreads through your code. Keep it as narrowly scoped as possible to limit its impact on type safety.

## When to Use This Skill

- Forced to use any for some reason
- Working with untyped third-party code
- Dealing with complex type errors
- Migrating JavaScript to TypeScript
- Reviewing code that uses any

## The Iron Rule

```
NEVER let any escape its minimal necessary scope.
```

**No exceptions:**
- Not for "it's just one variable"
- Not for "I'll fix it later"
- Not for "the function is short"

## Detection: The "Escaping any" Smell

If any could be more narrowly scoped, scope it.

```typescript
// ❌ VIOLATION: any on parameter escapes to return value
function processExpression(expression: any) {
  const result = expression.evaluate();  // result is any
  return result;                          // Returns any - spreads everywhere
}

// ✅ BETTER: any only where needed
function processExpression(expression: any) {
  const result: number = expression.evaluate();  // Constrain immediately
  return result;                                  // Returns number
}
```

## Technique 1: Narrow in Assignments

```typescript
// ❌ BAD: any spreads
const config = getConfig() as any;
config.debug = true;      // config stays any
const debug = config.debug;  // debug is any

// ✅ GOOD: Constrain immediately
const config = getConfig() as any;
const debug: boolean = config.debug;  // debug is boolean
```

## Technique 2: Inline any Assertions

```typescript
// ❌ BAD: any on the whole object
function processObject(obj: any) {
  obj.x = 1;
  obj.y = 2;
  return obj;  // Returns any
}

// ✅ GOOD: any only on the problematic line
function processObject(obj: Foo) {
  // @ts-expect-error - The library typings are wrong here
  (obj as any).secretMethod();
  return obj;  // Returns Foo
}
```

## Technique 3: Return Type Annotations

```typescript
// ❌ BAD: Return type infected by any
function parse(input: string) {
  const parsed = JSON.parse(input);  // parsed is any
  return parsed;                      // Return type is any
}

// ✅ GOOD: Explicit return type blocks the any
function parse(input: string): ParsedData {
  const parsed = JSON.parse(input);  // Still any internally
  return parsed;                      // But return type is ParsedData
}
```

## Technique 4: Intermediate Variables

```typescript
// ❌ BAD: any infects the whole expression
function calculate(a: number, b: any, c: number) {
  return a + b + c;  // Result is any because b is any
}

// ✅ BETTER: Convert any before use
function calculate(a: number, b: any, c: number) {
  const bNum: number = b;  // Constrain b to number
  return a + bNum + c;     // Result is number
}
```

## Technique 5: Type Assertions Over any Parameters

```typescript
// ❌ BAD: Changing parameter type to any
function processUser(user: any) {
  return user.name.toUpperCase();
}

// ✅ GOOD: Keep the type, assert where needed
function processUser(user: User) {
  // Only use any assertion if absolutely necessary
  return (user as any).secretField;  // any is inline only
}
```

## The any[] Trap

```typescript
// ❌ DANGEROUS: any[] elements are any
function getFirst(arr: any[]) {
  return arr[0];  // Returns any
}

// ✅ SAFER: Use generics or unknown
function getFirst<T>(arr: T[]): T {
  return arr[0];  // Returns T
}

function getFirst(arr: unknown[]): unknown {
  return arr[0];  // Returns unknown - forces checking
}
```

## Function Signatures: More Precise any

```typescript
// ❌ BAD: Maximally broad any
type Callback = any;

// ✅ BETTER: Precise function types
type Callback0 = () => any;           // No params
type Callback1 = (arg: any) => any;   // One param
type CallbackN = (...args: any[]) => any;  // Any params
```

## Pressure Resistance Protocol

### 1. "It's Just This One Place"

**Pressure:** "The any is isolated anyway"

**Response:** any spreads through return types, assignments, and function calls.

**Action:** Scope it narrower. Add type constraints immediately.

### 2. "The Type Is Too Complex"

**Pressure:** "I can't figure out the right type"

**Response:** Use any temporarily, but constrain the output.

**Action:** Add explicit return type. Add intermediate type annotations.

### 3. "It's Internal Code"

**Pressure:** "No external code uses this"

**Response:** Your future self is external code.

**Action:** Scope the any narrow. Document why it exists.

## Red Flags - STOP and Reconsider

- any on function parameters
- Functions returning any (especially without explicit return type)
- any assigned to a variable used multiple times
- any spreading through expressions
- Multiple functions passing any between them

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's contained" | any spreads through returns and assignments. |
| "Only used once" | That's one bug waiting to happen. |
| "I'll fix it later" | Later never comes. Scope it now. |
| "The function is short" | Short functions can still spread any. |

## Quick Reference

| any Situation | Narrowing Technique |
|---------------|---------------------|
| any parameter | Add return type annotation |
| any return value | Add explicit return type |
| any in expression | Assign to typed variable |
| any from JSON.parse | Add return type or validate |
| any from library | Assert to specific type |

## Auditing any Usage

```typescript
// Before: any everywhere
function process(data: any): any {
  const x = data.foo;        // any
  const y = data.bar;        // any
  return { x, y };           // any
}

// After: any contained
function process(data: any): Result {
  const x: number = data.foo;   // number
  const y: string = data.bar;   // string
  return { x, y };              // Result
}
```

## The Bottom Line

**Treat any like a hazardous material. Contain the spill.**

If you must use any, use it on the smallest possible piece of code. Add type annotations to stop it from spreading. Your goal is type safety everywhere except the one line that needs any.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 43: Use the Narrowest Possible Scope for any Types.
