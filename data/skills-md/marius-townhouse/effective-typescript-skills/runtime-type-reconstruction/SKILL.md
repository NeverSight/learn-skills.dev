---
name: runtime-type-reconstruction
description: Use when validating data at runtime. Use when parsing JSON. Use when types need runtime checks. Use when using io-ts or zod. Use when building validation schemas.
---

# Know How to Reconstruct Types at Runtime

## Overview

TypeScript types are erased at runtime, but sometimes you need to validate that runtime data matches your types. Use libraries like io-ts, zod, or runtypes to define schemas that provide both runtime validation and static types. This ensures your types match reality.

## When to Use This Skill

- Validating data at runtime
- Parsing JSON with type safety
- Types need runtime checks
- Using io-ts, zod, or runtypes
- Building validation schemas

## The Iron Rule

**Use validation libraries like zod or io-ts to get both runtime validation and TypeScript types from a single source of truth.**

## Example with Zod

```typescript
import { z } from 'zod';

// Define schema once
const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  age: z.number().optional(),
});

// Get TypeScript type from schema
type User = z.infer<typeof UserSchema>;

// Runtime validation
const result = UserSchema.safeParse(unknownData);
if (result.success) {
  // result.data is typed as User
  console.log(result.data.name);
} else {
  console.error(result.error);
}
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 74: Know How to Reconstruct Types at Runtime
