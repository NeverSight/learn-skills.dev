---
name: no-null-in-aliases
description: Use when defining type aliases. Use when null/undefined appears in type definitions. Use when types are confusing.
---

# Avoid Including null or undefined in Type Aliases

## Overview

**Type aliases should represent something, not "something or nothing."**

When you read `User`, you expect a user - not maybe-a-user. Include null explicitly at usage sites instead of hiding it in type aliases.

## When to Use This Skill

- Defining type aliases
- Naming types that include null
- Understanding confusing nullability
- Designing function parameters

## The Iron Rule

```
Type aliases should represent valid values.
Use Type | null explicitly, not NullableType.
```

**Remember:**
- `User` should always be a user
- `User | null` is explicit about nullability
- Hidden nullability confuses readers
- Properties in objects can be optional/nullable

## Detection: Hidden Nullability

```typescript
// Is user nullable? Can't tell from usage
function getComments(comments: Comment[], user: User) {
  return comments.filter(c => c.userId === user?.id);
}
```

If the type is defined like this:

```typescript
type User = { id: string; name: string; } | null;
```

Then the optional chain `?.` is needed. But readers can't tell without checking the definition.

## Better: Explicit Nullability

```typescript
type User = { id: string; name: string; };

// Now nullability is visible at the usage site
function getComments(comments: Comment[], user: User | null) {
  return comments.filter(c => c.userId === user?.id);
}
```

Or if user is required:

```typescript
function getComments(comments: Comment[], user: User) {
  return comments.filter(c => c.userId === user.id);
}
```

## If You Must Include null

Use an explicit name:

```typescript
// Bad: hidden null
type User = { id: string } | null;

// Better: explicit in name
type NullableUser = { id: string } | null;

// Best: no alias, explicit at usage
type User = { id: string };
function fn(user: User | null) { ... }
```

## Nested Nullability is OK

This rule applies to the top level of type aliases. Nullable properties inside objects are fine:

```typescript
// OK: nullable property in object
interface BirthdayMap {
  [name: string]: Date | undefined;
}

// BAD: nullable at top level
type BirthdayMap = {
  [name: string]: Date | undefined;
} | null;
```

## Optional Properties

Optional properties are similar to nullable ones:

```typescript
interface User {
  id: string;
  name: string;
  email?: string;  // OK: optional property
}
```

But consider Items 33 and 37 for guidance on when optional properties are appropriate.

## Why This Matters

### Code Readability

```typescript
// What does this mean?
function processUser(user: User) { ... }

// If User includes null, you'd expect:
function processUser(user: User) {
  if (!user) return;  // But why? Isn't user required?
}

// Explicit is clearer:
function processUser(user: User | null) {
  if (!user) return;  // Ah, it might be null!
}
```

### Refactoring Safety

```typescript
// If User includes null, this might crash:
function processUser(user: User) {
  console.log(user.name);  // Runtime error if null
}

// With explicit typing, TypeScript catches it:
function processUser(user: User | null) {
  console.log(user.name);  // Error: 'user' is possibly 'null'
}
```

## Pressure Resistance Protocol

### 1. "It's More Concise"

**Pressure:** "NullableUser is shorter than User | null"

**Response:** Explicitness at usage is worth a few characters.

**Action:** Use `Type | null` at usage sites.

### 2. "It's Always Nullable"

**Pressure:** "Users from the API are always nullable"

**Response:** That's an API detail, not a property of users themselves.

**Action:** Handle nullability at the API boundary, not in the type.

## Red Flags - STOP and Reconsider

- Type alias ending with `| null` or `| undefined`
- Types named `NullableX` or `MaybeX`
- Optional chains on parameters you thought were required
- Confusion about whether a type includes null

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It documents that null is possible" | It hides it; explicit `\| null` documents it |
| "Less repetition" | Clarity > brevity |
| "It's how the data comes from API" | Transform at the boundary |

## Quick Reference

```typescript
// DON'T: null in type alias
type User = { id: string } | null;

// DON'T: Maybe/Nullable prefixes
type MaybeUser = User | null;

// DO: Clean type alias
type User = { id: string };

// DO: Explicit nullability at usage
function process(user: User | null) { ... }

// OK: Nullable properties inside objects
interface Config {
  timeout?: number;  // optional property
  data: Data | null; // nullable property
}
```

## The Bottom Line

**Type names should represent the thing, not maybe-the-thing.**

When you read `User`, you should expect a user. Include `| null` explicitly at usage sites where nullability matters. This makes code more readable and helps TypeScript catch null-related bugs.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 32: Avoid Including null or undefined in Type Aliases.
