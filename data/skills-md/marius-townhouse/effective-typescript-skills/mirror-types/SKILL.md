---
name: mirror-types
description: Use when depending on external types. Use when avoiding tight coupling. Use when external types might change. Use when building adapters. Use when types are only used internally.
---

# Mirror Types to Sever Dependencies

## Overview

When you depend on types from external packages, changes to those types can break your code. Mirroring types - creating your own local copies of external types - severs this dependency. This is useful when you only need a subset of external types or when you want to insulate yourself from external changes.

## When to Use This Skill

- Depending on external types
- Avoiding tight coupling to external packages
- External types might change frequently
- Building adapters or wrappers
- Types are only used internally

## The Iron Rule

**Mirror external types when you want to sever dependencies. Define only the subset you need, insulated from external changes.**

## Example

```typescript
// BAD: Direct dependency on external type
import { ExternalUser } from 'external-library';

interface MyService {
  processUser(user: ExternalUser): void;
}

// If ExternalUser changes, your code breaks

// GOOD: Mirror the type
interface User {
  id: string;
  name: string;
  email: string;
}

interface MyService {
  processUser(user: User): void;
}

// Adapter converts external to internal type
function adaptExternalUser(external: ExternalUser): User {
  return {
    id: external.id,
    name: external.name,
    email: external.email,
  };
}
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 70: Mirror Types to Sever Dependencies
