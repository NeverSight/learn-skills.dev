---
name: typescript-conventions
description: "TypeScript coding conventions for strict, type-safe projects. Use when: (1) writing or reviewing TypeScript code, (2) choosing between `any` and `unknown`, (3) structuring imports with verbatimModuleSyntax, (4) naming functions, booleans, queries, and commands, (5) handling errors with guard clauses and early returns, or (6) avoiding common anti-patterns like primitive obsession, magic strings, and premature abstraction."
---

# TypeScript Conventions

Project-wide TypeScript standards that complement agent-specific instructions.

## Type Safety

- **No `any`**: Use `unknown` if the type is truly dynamic, then narrow.
- **Strict config**: `strict: true`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`.
- Use `Readonly<T>`, `Pick`, `Omit`, and `Record` for precise types.
- Use branded types for entity IDs (e.g., `UserId`, `OrderId`) to prevent mixing.
- Prefer `z.infer<typeof schema>` over hand-written types when a Zod schema exists.

## Imports

```typescript
// Type-only imports (required by verbatimModuleSyntax)
import type { FastifyInstance } from "fastify";

// Mixed imports: separate values and types
import { z } from "zod/v4";
import type { ZodType } from "zod/v4";

// ioredis: always named import
import { Redis } from "ioredis";
```

## Error Handling

- Handle errors at the beginning of functions with early returns / guard clauses.
- Avoid deep nesting -- use if-return pattern instead of else chains.
- In Fastify routes, throw `httpErrors` or use `reply.status().send()` -- the centralized `setErrorHandler` formats the response.
- Custom error classes for domain-specific errors (e.g., `NotFoundError`, `ConflictError`).

## Naming

- **Functions**: `getUserById`, `createReport`, `isActive`, `hasPermission`
- **Booleans**: `is/has/can/should` prefix
- **Query** (returns data): `get`, `find`, `list`, `fetch`
- **Command** (changes state): `create`, `update`, `delete`, `add`, `remove`

## Anti-Patterns

- **Primitive obsession**: Use branded types or Zod enums, not raw strings for IDs and statuses.
- **Magic numbers/strings**: Use constants from a shared package (e.g., `RATE_LIMITS`, `PAGINATION`, `CACHE`).
- **Long parameter lists**: Use an options object or a Zod schema.
- **Premature abstraction**: Three similar lines > one premature helper. Abstract on the third repetition.
