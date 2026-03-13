---
name: valid-state-types
description: Use when designing types that represent state. Use when types allow invalid combinations. Use when state has implicit dependencies between fields.
---

# Prefer Types That Always Represent Valid States

## Overview

**Design types so that only valid states are representable.**

If your types allow invalid combinations of values, you'll end up with code that's harder to write, harder to read, and more prone to bugs.

## When to Use This Skill

- Designing state types for applications
- Creating types with related fields
- Modeling states that have dependencies
- Debugging impossible state errors
- Refactoring confusing type definitions

## The Iron Rule

```
NEVER design types that can represent invalid states.
```

**No exceptions:**
- Not for "it's simpler this way"
- Not for "we'll validate at runtime"
- Not for "the extra types are too much work"

## Detection: The "Invalid State" Smell

If your type allows combinations that should never happen, redesign it.

```typescript
// ❌ VIOLATION: Allows invalid states
interface RequestState {
  status: 'loading' | 'success' | 'error';
  data?: string;
  error?: string;
}

// These are all valid according to the type, but nonsensical:
const bad1: RequestState = { status: 'success' };           // Where's the data?
const bad2: RequestState = { status: 'error' };             // Where's the error?
const bad3: RequestState = { status: 'loading', data: 'x' }; // Loading but has data?
const bad4: RequestState = { status: 'success', error: 'x' }; // Success with error?
```

## The Solution: Discriminated Unions

```typescript
// ✅ CORRECT: Only valid states are representable
interface RequestPending {
  status: 'pending';
}
interface RequestLoading {
  status: 'loading';
}
interface RequestSuccess {
  status: 'success';
  data: string;
}
interface RequestError {
  status: 'error';
  error: string;
}

type RequestState = RequestPending | RequestLoading | RequestSuccess | RequestError;

// Now invalid states are impossible:
const bad: RequestState = { status: 'success' };
//    ~~~ Property 'data' is missing in type '{ status: "success"; }'
```

## Real-World Example: Page State

```typescript
// ❌ BAD: Implicit relationships, invalid states possible
interface PageState {
  isLoading: boolean;
  error?: string;
  currentPage: string;
  data?: PageData;
}

// What does this mean?
const confusing: PageState = {
  isLoading: true,
  error: 'Network error',
  currentPage: '/home',
  data: someData,  // Loading but has data? Has error but also data?
};

// ✅ GOOD: Explicit states, no invalid combinations
interface PagePending { state: 'pending' }
interface PageLoading { state: 'loading'; currentPage: string }
interface PageLoaded { state: 'loaded'; currentPage: string; data: PageData }
interface PageError { state: 'error'; currentPage: string; error: string }

type PageState = PagePending | PageLoading | PageLoaded | PageError;

// Now the render function is clear:
function renderPage(state: PageState) {
  switch (state.state) {
    case 'pending':
      return renderPending();
    case 'loading':
      return renderSpinner(state.currentPage);
    case 'loaded':
      return renderData(state.data);
    case 'error':
      return renderError(state.error);
  }
}
```

## Related Fields Should Travel Together

```typescript
// ❌ BAD: Related fields can be independently undefined
interface Person {
  name: string;
  placeOfBirth?: string;  // These should either both
  dateOfBirth?: Date;     // be present or both absent
}

// This is valid but probably wrong:
const person: Person = { name: 'Alice', placeOfBirth: 'NYC' };  // No date?

// ✅ GOOD: Group related fields
interface Person {
  name: string;
  birth?: {
    place: string;
    date: Date;
  };
}

// Now they travel together:
function printBirth(person: Person) {
  if (person.birth) {
    // Both place AND date are guaranteed to exist
    console.log(`Born in ${person.birth.place} on ${person.birth.date}`);
  }
}
```

## The Air France 447 Anti-Pattern

A tragic example of bad state design:

```typescript
// ❌ DANGEROUS: Independent controls with conflicting states
interface CockpitControls {
  leftSideStick: number;   // Pilot's stick position
  rightSideStick: number;  // Copilot's stick position
}

// What if they conflict? The code has to decide somehow.
function getStickSetting(controls: CockpitControls): number {
  // Average them? Return left? Return right? No good answer!
  return (controls.leftSideStick + controls.rightSideStick) / 2;
}

// ✅ SAFE: Single source of truth
interface CockpitControls {
  stickAngle: number;  // One stick, one truth
}
```

## Pressure Resistance Protocol

### 1. "More Types Is More Work"

**Pressure:** "Creating all these interfaces is tedious"

**Response:** Invalid states cause bugs. The types are the easy part.

**Action:** Invest the time upfront. You'll save debugging time later.

### 2. "We Validate At Runtime"

**Pressure:** "We check for invalid combinations in the code"

**Response:** Every consumer has to remember to validate. They won't.

**Action:** Make invalid states unrepresentable. Eliminate the need to validate.

### 3. "It's Just Internal State"

**Pressure:** "No external code uses this type"

**Response:** Internal code is still code. You'll still have bugs.

**Action:** Design good types everywhere.

## Red Flags - STOP and Reconsider

- Multiple boolean flags that have dependencies
- Optional fields that should appear together
- Status enum with optional data fields
- Comments explaining "if X then Y must be set"
- Validation code checking for impossible combinations
- Switch statements with "should never happen" default cases

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's simpler" | It's simpler until you have bugs. |
| "We're careful" | Carelessness happens. Types don't forget. |
| "We document it" | Documentation gets stale. Types don't. |
| "Too many interfaces" | Better than too many bugs. |

## Quick Reference

| Bad Pattern | Good Pattern |
|-------------|--------------|
| Multiple related optional fields | Nested object that's optional |
| Status string + optional data/error | Discriminated union |
| Boolean flags with dependencies | Discriminated union |
| Multiple independent sources of truth | Single source of truth |

## Designing Valid State Types

1. **List all possible states** your system can be in
2. **For each state**, determine what data is required
3. **Create an interface** for each state
4. **Use a discriminated union** to combine them
5. **Verify**: Can you construct any invalid states?

```typescript
// Example: Shopping Cart
interface EmptyCart { state: 'empty' }
interface ActiveCart { state: 'active'; items: CartItem[] }
interface CheckoutCart { state: 'checkout'; items: CartItem[]; payment: PaymentInfo }
interface CompletedCart { state: 'completed'; orderId: string }

type ShoppingCart = EmptyCart | ActiveCart | CheckoutCart | CompletedCart;
```

## The Bottom Line

**If invalid states are representable, invalid states will occur.**

Design types that can only represent valid states. Use discriminated unions. Group related fields. Your code will be easier to write, easier to understand, and harder to break.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 29: Prefer Types That Always Represent Valid States.
