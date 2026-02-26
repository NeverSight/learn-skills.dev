---
name: zod
description: TypeScript-first schema validation with Zod v4. Use for schemas, type inference, validation, transformations, and JSON Schema generation.
license: MIT
metadata:
  author: thegreataxios
  version: "1.0.0"
  zod_version: "4.x"
---

# Zod Development

Zod is a TypeScript-first schema declaration and validation library. Use this skill when defining schemas, validating data, transforming inputs, or working with type-safe APIs.

## When to Apply

Reference this skill when:
- Defining schemas for runtime validation
- Creating type-safe API boundaries
- Transforming and coercing data
- Generating JSON Schema from TypeScript types
- Validating form inputs, environment variables, or API responses
- Working with Zod v4's new features (Mini, Core, Codecs)

## Quick Reference

### Primitive Types

| Type | Description | Example |
|------|-------------|---------|
| `z.string()` | String validation | `z.string().min(1).max(100)` |
| `z.number()` | Number validation | `z.number().int().positive()` |
| `z.bigint()` | BigInt validation | `z.bigint().min(0n)` |
| `z.boolean()` | Boolean values | `z.boolean()` |
| `z.date()` | Date objects | `z.date().min(new Date())` |
| `z.symbol()` | Symbol values | `z.symbol()` |
| `z.undefined()` | Undefined only | `z.undefined()` |
| `z.null()` | Null only | `z.null()` |
| `z.void()` | Void type | `z.void()` |
| `z.any()` | Any type (escape hatch) | `z.any()` |
| `z.unknown()` | Unknown type (safer) | `z.unknown()` |
| `z.never()` | Never type | `z.never()` |
| `z.nan()` | NaN value | `z.nan()` |

### String Formats

| Method | Validates | Example |
|--------|-----------|---------|
| `.email()` | Email format | `z.string().email()` |
| `.url()` | URL format | `z.string().url()` |
| `.uuid()` | UUID format | `z.string().uuid()` |
| `.ip()` | IP address | `z.string().ip({ version: "v4" })` |
| `.cidr()` | CIDR notation | `z.string().cidr()` |
| `.mac()` | MAC address | `z.string().mac()` |
| `.jwt()` | JWT format | `z.string().jwt()` |
| `.hash()` | Hash string | `z.string().hash("sha256")` |
| `.regex()` | Custom pattern | `z.string().regex(/^[a-z]+$/)` |
| `.emoji()` | Emoji only | `z.string().emoji()` |
| `.cuid()` / `.cuid2()` | CUID identifiers | `z.string().cuid2()` |
| `.ulid()` | ULID identifiers | `z.string().ulid()` |
| `.datetime()` | ISO datetime | `z.string().datetime()` |
| `.date()` | ISO date | `z.string().date()` |
| `.time()` | ISO time | `z.string().time()` |
| `.duration()` | ISO duration | `z.string().duration()` |

### String Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `.min(n)` | Minimum length | `.min(1)` |
| `.max(n)` | Maximum length | `.max(100)` |
| `.length(n)` | Exact length | `.length(10)` |
| `.startsWith(s)` | Prefix check | `.startsWith("https://")` |
| `.endsWith(s)` | Suffix check | `.endsWith(".com")` |
| `.includes(s)` | Contains substring | `.includes("@")` |
| `.trim()` | Trim whitespace | `.trim()` |
| `.toLowerCase()` | Lowercase transform | `.toLowerCase()` |
| `.toUpperCase()` | Uppercase transform | `.toUpperCase()` |
| `.normalize()` | Unicode normalize | `.normalize("NFC")` |
| `.nonempty()` | Min length 1 | `.nonempty()` |

### Number Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `.min(n)` | Minimum value | `.min(0)` |
| `.max(n)` | Maximum value | `.max(100)` |
| `.int()` | Integer only | `.int()` |
| `.positive()` | > 0 | `.positive()` |
| `.negative()` | < 0 | `.negative()` |
| `.nonnegative()` | >= 0 | `.nonnegative()` |
| `.nonpositive()` | <= 0 | `.nonpositive()` |
| `.multipleOf(n)` | Divisible by n | `.multipleOf(5)` |
| `.finite()` | Not Infinity | `.finite()` |
| `.safe()` | Safe integer | `.safe()` |
| `.step(n)` | Stepped values | `.step(0.01)` |

### Coercion

| Method | Coerces From | Example |
|--------|--------------|---------|
| `z.coerce.string()` | Any to string | `z.coerce.string()` |
| `z.coerce.number()` | String/Boolean to number | `z.coerce.number()` |
| `z.coerce.boolean()` | String/Number to boolean | `z.coerce.boolean()` |
| `z.coerce.bigint()` | To BigInt | `z.coerce.bigint()` |
| `z.coerce.date()` | String/Number to Date | `z.coerce.date()` |

### Object Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `.pick(keys)` | Select keys | `.pick({ name: true })` |
| `.omit(keys)` | Remove keys | `.omit({ password: true })` |
| `.partial()` | All optional | `.partial()` |
| `.required()` | All required | `.required()` |
| `.extend(obj)` | Add keys | `.extend({ age: z.number() })` |
| `.merge(schema)` | Merge schemas | `.merge(OtherSchema)` |
| `.keyof()` | Keys schema | `.keyof()` |
| `.strict()` | No extra keys | `.strict()` |
| `.passthrough()` | Allow extra | `.passthrough()` |
| `.strip()` | Remove extra | `.strip()` |
| `.catchall(schema)` | Validate extra | `.catchall(z.string())` |

### Array Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `.min(n)` | Min items | `.min(1)` |
| `.max(n)` | Max items | `.max(10)` |
| `.length(n)` | Exact length | `.length(5)` |
| `.nonempty()` | Min 1 item | `.nonempty()` |

### Set Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `.min(n)` | Min size | `.min(1)` |
| `.max(n)` | Max size | `.max(10)` |
| `.size(n)` | Exact size | `.size(5)` |
| `.nonempty()` | Min 1 item | `.nonempty()` |

### Union Types

| Type | Purpose | Example |
|------|---------|---------|
| `z.union()` | Any of types | `z.union([z.string(), z.number()])` |
| `z.discriminatedUnion()` | Tagged union | `z.discriminatedUnion("type", [...])` |
| `z.xor()` | Exclusive or | `z.xor(SchemaA, SchemaB)` |
| `z.intersection()` | All of types | `z.intersection(A, B)` |

### Optionality

| Method | Effect | Example |
|--------|--------|---------|
| `.optional()` | T \| undefined | `z.string().optional()` |
| `.nullable()` | T \| null | `z.string().nullable()` |
| `.nullish()` | T \| null \| undefined | `z.string().nullish()` |
| `.unwrap()` | Remove wrapper | `schema.unwrap()` |

### Validation & Transforms

| Method | Purpose | Example |
|--------|---------|---------|
| `.refine(fn)` | Custom validation | `.refine(v => v > 0)` |
| `.superRefine(fn)` | Multiple issues | `.superRefine(addIssue)` |
| `.check()` | New v4 validation | `.check(ctx => ...)` |
| `.transform(fn)` | Transform value | `.transform(v => v.trim())` |
| `.pipe(schema)` | Chain schemas | `.pipe(z.string().uuid())` |
| `.default(val)` | Default value | `.default("unknown")` |
| `.prefault(fn)` | Lazy default | `.prefault(() => Date.now())` |
| `.catch(val)` | Fallback on error | `.catch("fallback")` |

### Parsing Methods

| Method | Returns | Throws? |
|--------|---------|---------|
| `.parse(data)` | T | Yes |
| `.parseAsync(data)` | Promise\<T\> | Yes |
| `.safeParse(data)` | SafeReturnType\<T\> | No |
| `.safeParseAsync(data)` | Promise\<SafeReturnType\<T\>\> | No |
| `.spa` | Alias for safeParseAsync | No |

### Error Handling

| Function | Purpose |
|----------|---------|
| `z.prettifyError(error)` | Human-readable error |
| `z.treeifyError(error)` | Tree structure |
| `z.formatError(error)` | Formatted object |
| `z.flattenError(error)` | Flattened errors |

### Metadata

| Method | Purpose | Example |
|--------|---------|---------|
| `.describe(text)` | Add description | `.describe("User name")` |
| `.meta(obj)` | Custom metadata | `.meta({ id: "User" })` |
| `.register(registry)` | Register schema | `.register(registry)` |

### JSON Schema

| Method | Purpose |
|--------|---------|
| `z.toJSONSchema(schema)` | Convert to JSON Schema |
| `z.toJSONSchema(schema, config)` | With configuration |

### Codecs (v4)

Codecs are bi-directional transformations. You define them using `z.codec(inputSchema, outputSchema, { decode, encode })`:

```typescript
const stringToDate = z.codec(
  z.iso.datetime(),  // input: ISO date string
  z.date(),          // output: Date object
  {
    decode: (isoString) => new Date(isoString),
    encode: (date) => date.toISOString()
  }
)

// Forward: string → Date
stringToDate.decode("2024-01-15T10:30:00.000Z") // => Date

// Backward: Date → string  
stringToDate.encode(new Date()) // => "2024-01-15T10:30:00.000Z"
```

Use `.decode()` for forward processing and `.encode()` for backward processing.

### v4 Features

| Feature | Description |
|---------|-------------|
| **Performance** | 3-10x faster than v3 |
| **Bundle Size** | Up to 70% smaller |
| **zod/mini** | Functional API, tree-shakeable |
| **zod/v4/core** | Core utilities package |
| **Codecs** | Built-in encode/decode |
| **JSON Schema** | Improved generation |

## Core Concepts

### 1. Schema Definition

```typescript
import { z } from "zod"

const User = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().nonnegative().optional(),
  role: z.enum(["admin", "user", "guest"]).default("user"),
  createdAt: z.coerce.date()
})

type User = z.infer<typeof User>
```

### 2. Parsing & Validation

```typescript
// Parse (throws on error)
const user = User.parse(data)

// Safe parse (returns result)
const result = User.safeParse(data)
if (result.success) {
  console.log(result.data)
} else {
  console.log(result.error)
}

// Async parsing
const asyncUser = await User.parseAsync(data)
```

### 3. Transformations

```typescript
const TrimmedString = z.string().trim().toLowerCase()

const DateFromString = z.string().datetime().transform(val => new Date(val))

const FormattedUser = User.transform(user => ({
  ...user,
  displayName: `${user.name} <${user.email}>`
}))
```

### 4. Composition

```typescript
// Union
const StringOrNumber = z.union([z.string(), z.number()])

// Discriminated Union
const Event = z.discriminatedUnion("type", [
  z.object({ type: z.literal("click"), x: z.number(), y: z.number() }),
  z.object({ type: z.literal("keypress"), key: z.string() })
])

// Intersection
const Combined = z.intersection(BaseSchema, ExtraSchema)
```

### 5. Error Customization

```typescript
const Password = z.string()
  .min(8, "Password must be at least 8 characters")
  .max(100, "Password is too long")
  .regex(/[A-Z]/, "Must contain uppercase letter")

// Per-parse error handling
const result = schema.safeParse(data, {
  error: (issue) => `Custom: ${issue.message}`
})
```

## Common Patterns

### API Response Schema

```typescript
const ApiResponse = <T extends z.ZodTypeAny>(data: T) =>
  z.object({
    success: z.boolean(),
    data: data.optional(),
    error: z.string().optional()
  })
```

### Environment Variables

```typescript
const Env = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]),
  DATABASE_URL: z.string().url(),
  PORT: z.coerce.number().int().min(1).max(65535).default(3000)
})

const env = Env.parse(process.env)
```

### Recursive Schema

```typescript
const Node: z.ZodType<TreeNode> = z.lazy(() =>
  z.object({
    value: z.string(),
    children: z.array(Node).optional()
  })
)
```

### Form Validation

```typescript
const LoginForm = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password too short"),
  rememberMe: z.boolean().default(false)
})

type LoginInput = z.infer<typeof LoginForm>
```

## How to Work

1. **Import Zod**: `import { z } from "zod"`
2. **Define schema**: Use primitives, objects, and composition
3. **Add constraints**: Chain methods like `.min()`, `.max()`, `.email()`
4. **Parse data**: Use `.parse()` or `.safeParse()`
5. **Handle errors**: Check `.success` or use error formatting
6. **Transform if needed**: Use `.transform()` for data transformation

## v4 Migration Notes

- `z.custom()` now uses `z.custom<T>(fn)` syntax
- `.refine()` returns schema directly (no wrapping)
- Error messages use new formatting system
- Use `zod/mini` for optimal tree-shaking

## Related Resources

- **Official Docs**: https://zod.dev/
- **API Reference**: https://zod.dev/api
- **Ecosystem**: https://zod.dev/ecosystem
- **Migration Guide**: https://zod.dev/v4/changelog

## Related Skills

- `typescript` - TypeScript best practices
- `arktype` - Alternative validation library
