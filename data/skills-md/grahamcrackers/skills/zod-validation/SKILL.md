---
name: zod-validation
description: Zod schema validation patterns for TypeScript, including API response parsing, form validation, environment variables, and type inference. Use when validating data, parsing API responses, defining schemas, integrating with forms, or when the user asks about Zod, runtime validation, or schema design.
---

# Zod Validation Patterns

## Core Concepts

Zod provides runtime validation with automatic TypeScript type inference — define the schema once, get the type for free:

```typescript
import { z } from "zod";

const UserSchema = z.object({
    id: z.string().uuid(),
    name: z.string().min(1),
    email: z.string().email(),
    role: z.enum(["admin", "member", "viewer"]),
    createdAt: z.coerce.date(),
});

type User = z.infer<typeof UserSchema>;
```

## Schema Design

### Primitives

```typescript
z.string().min(1).max(255);
z.number().int().positive();
z.boolean();
z.date();
z.literal("active");
z.enum(["small", "medium", "large"]);
z.nativeEnum(HttpStatus); // TypeScript enum
```

### Objects

```typescript
const CreateUserSchema = z.object({
    name: z.string().min(1, "Name is required"),
    email: z.string().email("Invalid email"),
    age: z.number().int().min(18).optional(),
});

// Derive variants from a base schema
const UpdateUserSchema = CreateUserSchema.partial();
const UserResponseSchema = CreateUserSchema.extend({
    id: z.string().uuid(),
    createdAt: z.coerce.date(),
});
```

### Arrays and Records

```typescript
z.array(UserSchema).min(1).max(100);
z.record(z.string(), z.number()); // Record<string, number>
z.tuple([z.string(), z.number()]); // [string, number]
```

### Unions and Discriminated Unions

```typescript
const ResultSchema = z.discriminatedUnion("status", [
    z.object({ status: z.literal("success"), data: UserSchema }),
    z.object({ status: z.literal("error"), message: z.string() }),
]);
```

Prefer `discriminatedUnion` over `union` — it's faster and produces better error messages.

### Transforms and Coercion

```typescript
const SlugSchema = z.string().transform((s) => s.toLowerCase().replace(/\s+/g, "-"));

// Coerce strings to numbers/dates (useful for form data and query params)
z.coerce.number(); // "42" → 42
z.coerce.date(); // "2025-01-01" → Date
z.coerce.boolean(); // "true" → true
```

### Refinements

Custom validation logic:

```typescript
const PasswordSchema = z
    .string()
    .min(8)
    .refine((val) => /[A-Z]/.test(val), "Must contain an uppercase letter")
    .refine((val) => /[0-9]/.test(val), "Must contain a number");

const DateRangeSchema = z
    .object({
        start: z.coerce.date(),
        end: z.coerce.date(),
    })
    .refine((data) => data.end > data.start, {
        message: "End date must be after start date",
        path: ["end"],
    });
```

### Defaults and Preprocessing

```typescript
const SettingsSchema = z.object({
    theme: z.enum(["light", "dark"]).default("light"),
    pageSize: z.number().default(20),
    notifications: z.boolean().default(true),
});

// Preprocess handles raw input before validation
const NumberFromString = z.preprocess((val) => (typeof val === "string" ? parseInt(val, 10) : val), z.number());
```

## Parsing Patterns

### Safe Parsing

```typescript
const result = UserSchema.safeParse(unknownData);
if (result.success) {
    console.log(result.data); // typed as User
} else {
    console.error(result.error.flatten());
}
```

Use `safeParse` when you want to handle errors yourself. Use `parse` when invalid data should throw.

### API Response Validation

```typescript
async function fetchUser(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    const json = await response.json();
    return UserSchema.parse(json);
}
```

Parse API responses at the boundary — everything downstream gets guaranteed types.

### Paginated Response

```typescript
function paginatedSchema<T extends z.ZodType>(itemSchema: T) {
    return z.object({
        items: z.array(itemSchema),
        total: z.number(),
        page: z.number(),
        pageSize: z.number(),
    });
}

const UsersResponseSchema = paginatedSchema(UserSchema);
type UsersResponse = z.infer<typeof UsersResponseSchema>;
```

## Environment Variables

```typescript
const EnvSchema = z.object({
    NODE_ENV: z.enum(["development", "production", "test"]),
    DATABASE_URL: z.string().url(),
    API_KEY: z.string().min(1),
    PORT: z.coerce.number().default(3000),
    DEBUG: z.coerce.boolean().default(false),
});

export const env = EnvSchema.parse(process.env);
```

Parse `process.env` at startup — fail fast if required variables are missing.

## Form Integration

Zod integrates with React Hook Form via `@hookform/resolvers`:

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

const FormSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Minimum 8 characters"),
});

type FormData = z.infer<typeof FormSchema>;

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(FormSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
      <input type="password" {...register("password")} />
      {errors.password && <span>{errors.password.message}</span>}
      <button type="submit">Login</button>
    </form>
  );
}
```

## Error Formatting

```typescript
const result = schema.safeParse(data);
if (!result.success) {
    // Flat structure: { formErrors: string[], fieldErrors: Record<string, string[]> }
    const flat = result.error.flatten();

    // Formatted (nested): matches schema shape
    const formatted = result.error.format();
}
```

## Schema Organization

```
src/
├── schemas/
│   ├── user.ts          # UserSchema, CreateUserSchema, UpdateUserSchema
│   ├── post.ts          # PostSchema, etc.
│   ├── common.ts        # PaginatedSchema, IdSchema, DateRangeSchema
│   └── env.ts           # EnvSchema
```

- Co-locate schemas with their domain.
- Export the schema and its inferred type together.
- Build complex schemas by composing smaller ones with `.extend()`, `.merge()`, `.pick()`, and `.omit()`.

## Guidelines

- Parse at boundaries (API responses, form submissions, env vars, URL params) — trust the types internally.
- Use `.safeParse()` for user input. Use `.parse()` for data that should never be invalid (programmer errors).
- Keep custom error messages user-friendly: `"Email is required"`, not `"Expected string, received undefined"`.
- Prefer `z.coerce.*` over manual `preprocess` for simple type coercions.
- Use `discriminatedUnion` over `union` for tagged types — better performance and error messages.
