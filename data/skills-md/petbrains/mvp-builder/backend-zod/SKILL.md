---
name: backend-zod
description: TypeScript-first schema validation library. Use for ALL input validation in TypeScript projects — API inputs, form data, environment variables, config files. Essential companion for tRPC (required), React Hook Form, and any data boundary. Choose Zod when you need runtime validation with automatic TypeScript type inference.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Zod (Schema Validation)

## Overview

Zod is a TypeScript-first schema declaration and validation library. Define a schema once, get both runtime validation AND TypeScript types automatically via `z.infer<>`.

**Version**: Zod 4 (2025) / Zod 3.x widely used  
**Requirements**: TypeScript ≥5.5, strict mode

**Key Benefit**: Single source of truth for validation and types — no drift between runtime checks and TypeScript.

## When to Use This Skill

✅ **Use Zod when:**
- Validating API inputs (required for tRPC)
- Building forms with react-hook-form
- Parsing environment variables
- Validating config files or JSON
- Creating DTOs between layers
- Any data crossing trust boundaries

❌ **Zod is NOT for:**
- Complex business rule validation (use domain logic)
- Database schema definition (use Prisma schema)
- Static type-only definitions (use interfaces)

---

## Quick Start

### Installation

```bash
npm install zod
```

### Basic Usage

```typescript
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

// Infer TypeScript type
type User = z.infer<typeof UserSchema>;

// Validate
const result = UserSchema.safeParse(data);
if (result.success) {
  console.log(result.data); // typed as User
} else {
  console.log(result.error.issues);
}
```

---

## Core Schema Patterns

### Primitives with Validation

```typescript
const EmailSchema = z.string().email('Invalid email format');
const PasswordSchema = z.string().min(8, 'Min 8 characters');
const AgeSchema = z.number().int().positive().max(150);
const UrlSchema = z.string().url();
const UuidSchema = z.string().uuid();
```

### Object Schemas

```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(2).max(100),
  role: z.enum(['user', 'admin', 'moderator']),
  createdAt: z.date(),
});

type User = z.infer<typeof UserSchema>;
```

### Derive Variations

```typescript
// For create (omit auto-generated fields)
const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true });

// For update (all optional)
const UpdateUserSchema = CreateUserSchema.partial();

// For public response (only safe fields)
const PublicUserSchema = UserSchema.pick({ id: true, name: true });
```

---

## Advanced Patterns

### Discriminated Unions

**Use for type-safe API responses:**

```typescript
const ApiResponse = z.discriminatedUnion('status', [
  z.object({ status: z.literal('success'), data: UserSchema }),
  z.object({ status: z.literal('error'), code: z.string(), message: z.string() }),
]);

type ApiResponse = z.infer<typeof ApiResponse>;
// TypeScript knows: if status === 'success', data exists
```

### Custom Validation with Refine

```typescript
const PasswordSchema = z.string()
  .min(8)
  .refine(val => /[A-Z]/.test(val), 'Must contain uppercase')
  .refine(val => /[0-9]/.test(val), 'Must contain number');
```

### Cross-Field Validation with SuperRefine

```typescript
const FormSchema = z.object({
  password: z.string(),
  confirmPassword: z.string(),
}).superRefine((data, ctx) => {
  if (data.password !== data.confirmPassword) {
    ctx.addIssue({
      code: 'custom',
      message: 'Passwords must match',
      path: ['confirmPassword'],
    });
  }
});
```

### Transforms (Data Normalization)

```typescript
// Normalize email
const NormalizedEmail = z.string()
  .email()
  .transform(s => s.toLowerCase().trim());

// Parse string to number
const StringToNumber = z.string()
  .transform(s => parseInt(s, 10))
  .pipe(z.number());
```

### Coercion (API Query Parameters)

```typescript
// GET requests receive strings — use coercion
const PaginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  active: z.coerce.boolean().optional(),
});
```

---

## Common Schema Recipes

### Pagination Input

```typescript
export const PaginationSchema = z.object({
  limit: z.number().min(1).max(100).default(10),
  cursor: z.string().uuid().optional(),
});
```

### Date Range Filter

```typescript
export const DateRangeSchema = z.object({
  from: z.coerce.date(),
  to: z.coerce.date(),
}).refine(d => d.from <= d.to, 'From must be before To');
```

### Environment Variables

```typescript
const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  PORT: z.coerce.number().default(3000),
});

export const env = EnvSchema.parse(process.env);
```

### File Upload Metadata

```typescript
const FileSchema = z.object({
  name: z.string(),
  size: z.number().max(10 * 1024 * 1024), // 10MB
  type: z.enum(['image/png', 'image/jpeg', 'application/pdf']),
});
```

---

## Integration with tRPC

```typescript
import { z } from 'zod';
import { publicProcedure } from '../trpc';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

export const userRouter = router({
  create: publicProcedure
    .input(CreateUserSchema)  // ← Zod validates automatically
    .mutation(({ input }) => {
      // input is typed as { email: string; name: string }
    }),
});
```

---

## Rules

### Do ✅

- Use `z.infer<typeof Schema>` to derive types
- Use discriminated unions over regular unions for objects
- Use `.safeParse()` when handling errors gracefully
- Add descriptive error messages
- Use `.default()` for optional fields with defaults
- Keep schemas in dedicated files (`/schemas/*.schema.ts`)

### Avoid ❌

- Async transforms in tRPC input (not supported)
- Using `.catchall()` with output schemas (inference issues)
- Multiple Zod installations (causes type inference failures)
- Overly complex nested refinements (hard to debug)

---

## Parse Methods

| Method | Throws | Returns |
|--------|--------|---------|
| `.parse(data)` | Yes | `T` |
| `.safeParse(data)` | No | `{ success, data?, error? }` |
| `.parseAsync(data)` | Yes | `Promise<T>` |
| `.safeParseAsync(data)` | No | `Promise<{ success, data?, error? }>` |

**Use `.safeParse()` in application code, `.parse()` in trusted contexts.**

---

## Troubleshooting

```yaml
"Type inference not working":
  → Check single Zod installation: npm ls zod
  → Ensure TypeScript strict mode enabled
  → Restart TypeScript server

"Coercion not working":
  → Use z.coerce.number() not z.number() for query params
  → Check input is string before coercion

"Transform output type wrong":
  → Use .pipe() after transform for additional validation
  → Check transform return type

"Refinement errors unclear":
  → Add path parameter to ctx.addIssue()
  → Use descriptive error messages
```

---

## File Structure

```
src/schemas/
├── user.schema.ts       # User-related schemas
├── post.schema.ts       # Post-related schemas
├── common.schema.ts     # Pagination, date ranges, etc.
└── env.schema.ts        # Environment validation
```

## References

- https://zod.dev — Official documentation
- https://zod.dev/?id=basic-usage — Quick reference
- https://github.com/colinhacks/zod — GitHub
