---
name: avoid-repeated-params
description: Use when functions have multiple parameters of same type. Use when parameter order is easy to confuse. Use when designing function signatures.
---

# Avoid Repeated Parameters of the Same Type

## Overview

**Multiple parameters of the same type invite mix-ups.**

When a function takes `(string, string, string)`, it's easy to pass arguments in the wrong order. Use named parameters (objects) to make calls self-documenting.

## When to Use This Skill

- Functions with 2+ parameters of the same type
- Parameters that are easy to confuse
- APIs that users will call frequently
- Refactoring confusing function signatures

## The Iron Rule

```
If parameter order is confusing, use an object.
Names prevent mix-ups better than positions.
```

**Remember:**
- TypeScript can't detect swapped same-type arguments
- Position-based APIs require documentation study
- Object parameters are self-documenting
- IDE autocomplete works better with named params

## Detection: Easy to Confuse

```typescript
function sendEmail(
  to: string,
  subject: string,
  body: string
) { /* ... */ }

// Which is which?
sendEmail(
  'Hello!',
  'bob@example.com',
  'Welcome to our service'
);
// Whoops! Subject and recipient are swapped
```

TypeScript sees `(string, string, string)` - all valid, no error.

## Solution: Object Parameter

```typescript
function sendEmail(params: {
  to: string;
  subject: string;
  body: string;
}) { /* ... */ }

// Now it's clear:
sendEmail({
  to: 'bob@example.com',
  subject: 'Hello!',
  body: 'Welcome to our service'
});

// Wrong order is obvious:
sendEmail({
  to: 'Hello!',  // Clearly wrong
  subject: 'bob@example.com',  // Obviously an email
  body: 'Welcome'
});
```

## When Position-Based is OK

### Different Types

```typescript
// Clear: types are different
function setProperty(obj: object, key: string, value: unknown) { }

// Clear: number vs string
function pad(str: string, length: number) { }
```

### Single Parameter

```typescript
// Nothing to confuse
function greet(name: string) { }
```

### Well-Known Conventions

```typescript
// Math functions are universally position-based
function max(a: number, b: number) { }

// Array methods follow established patterns
function slice(arr: any[], start: number, end: number) { }
```

## Destructuring for Clean Implementation

```typescript
// Clean function signature and implementation
function sendEmail({
  to,
  subject,
  body
}: {
  to: string;
  subject: string;
  body: string;
}) {
  console.log(`Sending to ${to}: ${subject}`);
  // Use to, subject, body directly
}
```

## Optional Parameters with Defaults

```typescript
interface SendEmailOptions {
  to: string;
  subject: string;
  body: string;
  cc?: string[];
  priority?: 'high' | 'normal' | 'low';
}

function sendEmail({
  to,
  subject,
  body,
  cc = [],
  priority = 'normal'
}: SendEmailOptions) {
  // ...
}

// Call with just required params
sendEmail({ to: 'bob@example.com', subject: 'Hi', body: 'Hello!' });

// Or with optional params
sendEmail({
  to: 'bob@example.com',
  subject: 'Urgent',
  body: 'Please respond',
  priority: 'high'
});
```

## Mixing Required and Optional

```typescript
// Required first parameter, options object second
function createElement(
  tagName: string,
  options?: {
    className?: string;
    id?: string;
    children?: Element[];
  }
) { /* ... */ }

createElement('div');
createElement('div', { className: 'container', id: 'main' });
```

## Real-World Example: Date Formatting

```typescript
// Bad: which is format, which is locale?
function formatDate(date: Date, format: string, locale: string): string { }

formatDate(new Date(), 'en-US', 'YYYY-MM-DD');  // Wrong order!

// Good: named parameters
function formatDate(
  date: Date,
  options: { format: string; locale: string }
): string { }

formatDate(new Date(), { format: 'YYYY-MM-DD', locale: 'en-US' });
```

## Rectangle Example

```typescript
// Bad: easy to confuse width/height, x/y
function drawRect(x: number, y: number, width: number, height: number) { }

// Better: grouped semantically
function drawRect(
  position: { x: number; y: number },
  size: { width: number; height: number }
) { }

// Best: named everything
interface DrawRectOptions {
  x: number;
  y: number;
  width: number;
  height: number;
}
function drawRect(options: DrawRectOptions) { }
```

## Pressure Resistance Protocol

### 1. "Too Verbose"

**Pressure:** "Object syntax is longer"

**Response:** One-time verbosity prevents ongoing confusion.

**Action:** Use named parameters for clarity; brevity isn't worth bugs.

### 2. "It's a Standard Pattern"

**Pressure:** "Other libraries use positional params"

**Response:** You're not other libraries. Make your API clear.

**Action:** Design for your users, not convention.

## Red Flags - STOP and Reconsider

- Functions with 2+ parameters of the same type
- Documentation needed to explain parameter order
- Tests that verify parameter order
- Bugs from swapped arguments

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's only two parameters" | Two strings are still confusable |
| "IDE shows parameter names" | Names shown, not enforced |
| "We have good documentation" | People don't read docs |

## Quick Reference

```typescript
// DON'T: Same-type positional parameters
function fn(a: string, b: string, c: string) { }
fn('x', 'y', 'z');  // What's what?

// DO: Named parameters
function fn(params: { a: string; b: string; c: string }) { }
fn({ a: 'x', b: 'y', c: 'z' });  // Clear!

// OK: Different types
function fn(name: string, count: number) { }

// OK: Single parameter
function fn(message: string) { }
```

## The Bottom Line

**Named parameters prevent argument mix-ups.**

When functions take multiple parameters of the same type, use an object parameter. The small verbosity cost is repaid many times over in prevented bugs and improved readability.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 38: Avoid Repeated Parameters of the Same Type.
