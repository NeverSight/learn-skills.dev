---
name: export-public-types
description: Use when publishing libraries. Use when types appear in public APIs. Use when users need to reference types. Use when building reusable components. Use when designing library interfaces.
---

# Export All Types That Appear in Public APIs

## Overview

When you publish a library, users need access to all types that appear in your public API. If a function returns `User` but `User` isn't exported, users can't type their own variables to match. Export all types that appear in public function signatures, return types, or interfaces.

This is essential for good developer experience in libraries.

## When to Use This Skill

- Publishing TypeScript libraries
- Types appear in public function signatures
- Users need to reference your types
- Building reusable components
- Designing library interfaces

## The Iron Rule

**Export every type that appears in your public API. Users need these types to work with your library effectively.**

## Example

```typescript
// BAD: Internal type not exported
interface User {
  id: string;
  name: string;
}

export function getUser(id: string): User {
  // ...
}

// User can't do:
// import { getUser, User } from 'library'; // Error: User not exported
// const user: User = getUser('123');

// GOOD: Export the type
export interface User {
  id: string;
  name: string;
}

export function getUser(id: string): User {
  // ...
}

// User can now:
// import { getUser, User } from 'library';
// const user: User = getUser('123');
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 67: Export All Types That Appear in Public APIs
