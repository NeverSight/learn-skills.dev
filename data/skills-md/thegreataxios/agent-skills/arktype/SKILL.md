---
name: arktype
description: TypeScript type validation with ArkType, ArkEnv, and ArkRegex. Use for schemas, environment variables, and type-safe regex.
license: MIT
metadata:
  author: thegreataxios
  version: "1.0.0"
---

# ArkType Development

ArkType is a TypeScript-first validation library with powerful runtime type checking, scopes, generics, and pattern matching. Use this skill when defining schemas, validating data, or working with type-safe APIs.

## When to Apply

Reference this skill when:
- Defining type schemas for validation
- Creating reusable type scopes and modules
- Working with generics and constrained types
- Pattern matching with `match`
- Validating environment variables with ArkEnv
- Type-safe regular expressions with ArkRegex
- Converting to/from JSON Schema
- Testing with Attest

## Quick Reference

### Type Definition Syntax

| Syntax | Use Case | Example |
|--------|-----------|---------|
| String | Concise definitions | `type({ name: "string", age: "number >= 18" })` |
| Fluent | Chaining methods | `type.string.atLeastLength(8).email()` |
| Tuple | Complex/nested | `type(["string", ["number", "number"]])` |
| Args | Operators | `type("string", "|", "boolean")` |

### Validation Results

| Method | Returns |
|--------|---------|
| `.validate(data)` | `{ data: T } | { errors: ArkErrors }` |
| `.assert(data)` | Validated data or throws |
| Type as function | Validated data or `type.errors` instance |

### Key Operators

| Operator | Meaning |
|----------|---------|
| `|` | Union |
| `&` | Intersection |
| `>` / `>=` | Greater than (exclusive/inclusive) |
| `<` / `<=` | Less than (exclusive/inclusive) |
| `%` | Divisible by |
| `?` suffix | Optional property |
| `=` suffix | Default value |

## Core Concepts

### 1. Type Definition

**String Syntax (Most Concise)**
```typescript
const User = type({
  name: "string",
  age: "number.integer >= 0",
  email: "string.email",
  "role?": "'admin' | 'user' = 'user'"
})
```

**Fluent API (Best for chaining)**
```typescript
const Password = type.string
  .atLeastLength(8)
  .describe("a valid password")
```

### 2. Scopes & Modules

**Define a Scope**
```typescript
const types = scope({
  Id: "string",
  User: { id: "Id", name: "string" },
  "User[]": "User[]"
}).export()
```

### 3. Generics

**Basic Generic**
```typescript
const boxOf = type("<t>", { value: "t" })
const StringBox = boxOf({ type: "string" })
```

**Constrained Generic**
```typescript
const nonEmpty = type("<arr extends unknown[]>", "arr > 0")
```

### 4. Pattern Matching

```typescript
import { match } from "arktype"

const sizeOf = match({
  string: v => v.length,
  number: v => v,
  default: "assert"
})

// Discriminated union matching
const getValue = match
  .in<{ id: 1 } | { id: 2 }>()
  .at("id")
  .match({
    1: o => o.value,
    2: o => o.other,
    default: "assert"
  })
```

## ArkType Ecosystem

### ArkEnv (Environment Variables)

```typescript
import { arkenv } from "arkenv"

const env = arkenv({
  HOST: "string.host",
  PORT: "number.port",
  NODE_ENV: "'development' | 'production' | 'test' = 'development'"
})

// Fully typed - TypeScript knows exact types!
console.log(env.HOST)     // string
console.log(env.PORT)     // number
console.log(env.NODE_ENV) // "development" | "production" | "test"
```

**ArkEnv Keywords**
| Keyword | Validates |
|---------|----------|
| `string.host` | Hostname |
| `string.url` | URL |
| `number.port` | Port (1-65535) |
| `string.email` | Email format |
| `string.uuid.v4` | UUID v4 |

### ArkRegex (Type-safe RegExp)

```typescript
import { regex } from "arkregex"

const ok = regex("^ok$", "i")
// Regex<"ok" | "oK" | "Ok" | "OK", { flags: "i" }>

const semver = regex("^(\\d*)\\.(\\d*)\\.(\\d*)$")
// Regex<`${bigint}.${bigint}.${bigint}`, { captures: [bigint, bigint, bigint] }

const email = regex("^(?<name>\\w+)@(?<domain>\\w+\\.\\w+)$")
// Regex with typed groups: { name: string; domain: `${string}.${string}` }
```

**Features**
| Feature | Description |
|---------|-------------|
| Type inference | Infers capture types from pattern |
| Named groups | `.groups` object is fully typed |
| Zero runtime | Uses native RegExp at runtime |
| TS 5.9+ | Required for best experience |

### Attest (Testing)

```typescript
import { attest, setup } from "@ark/attest"

setup()

it("type tests", () => {
  attest<string>(myType.infer)
  attest(myType.json).snap({ /* ... */ })
})
```

### JSON Schema

```typescript
// Type to JSON Schema
const schema = User.toJsonSchema()

// JSON Schema to Type
import { jsonSchemaToType } from "@ark/json-schema"
const T = jsonSchemaToType({ type: "string", minLength: 5 })
```

## Common Patterns

### Recursive Types

```typescript
const Node = scope({
  Node: {
    value: "string",
    "children?": "Node[]"
  }
}).export().Node
```

### Discriminated Unions

```typescript
const Event = type({
  type: "'click'",
  x: "number",
  y: "number"
}).or({
  type: "'keydown'",
  key: "string"
})
```

### Branded Types

```typescript
const Even = type("number % 2").brand("even")
type Even = typeof Even.infer
```

## How to Work

1. **Choose syntax**: String for conciseness, fluent for chaining
2. **Define schema**: Use `type()` for one-off, `scope()` for reusable
3. **Validate**: Call type as function or use `.assert()`
4. **Handle errors**: Check `instanceof type.errors`
5. **Export modules**: Use `.export()` for public APIs

## Related Resources

- **arktype**: `github.com/arktypeio/arktype`
- **arkregex**: Type-safe RegExp replacement
- **arkenv**: Environment variables with ArkType
- **@ark/attest**: Testing utilities
- **@ark/json-schema**: JSON Schema conversion

## Related Skills

- `typescript` - TypeScript best practices
