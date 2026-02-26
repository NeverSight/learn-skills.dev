---
name: codegen-over-complex-types
description: Use when types become extremely complex. Use when types mirror external schemas. Use when maintaining type-to-schema mappings. Use when types require extensive type-level logic. Use when types drift from data sources.
---

# Consider Codegen as an Alternative to Complex Types

## Overview

Sometimes the best type-level code is no type-level code at all. When types become extremely complex, when they mirror external schemas (APIs, databases, protocols), or when they need to stay synchronized with changing external sources, code generation is often a better solution than sophisticated type-level programming.

Code generation trades compile-time complexity for build-time generation, often resulting in simpler, more maintainable code that stays in sync with its source of truth.

## When to Use This Skill

- Types mirror external schemas (OpenAPI, GraphQL, database)
- Type-level logic becomes extremely complex
- Types need to stay synchronized with external sources
- Type maintenance cost exceeds value
- Team struggles with complex type-level code

## The Iron Rule

**When types become too complex or must stay synchronized with external sources, generate them from schemas rather than writing sophisticated type-level code.**

## Detection

Watch for these signals:

```typescript
// RED FLAGS - Complex types that might be generated
// 50+ lines of conditional types to parse a URL
type ParseURL<T> = /* extremely complex type-level parser */;

// Types manually maintained to match API
type APIResponse = {
  // 100+ fields that must match backend
  // Every API change requires manual updates
};

// Types derived from JSON Schema via complex mappings
type FromSchema<T> = /* recursive conditional mapped type */;
```

## The Complexity Trade-off

```typescript
// OPTION 1: Complex type-level code (maintainability cost)
type ParseOpenAPI<Schema> = Schema extends {
  paths: infer Paths
} ? {
  [Path in keyof Paths]: Paths[Path] extends {
    [Method in 'get' | 'post' | 'put' | 'delete']: {
      responses: infer Responses
    }
  } ? {
    [Method in keyof Paths[Path]]: Responses extends {
      200: { content: { 'application/json': infer Body } }
    } ? Body : never
  } : never
} : never;
// 50+ more lines of type-level logic...

// OPTION 2: Generated types (build-time cost)
// Generated from OpenAPI schema:
interface GetUserResponse { /* ... */ }
interface CreateUserRequest { /* ... */ }
// Clear, debuggable, always in sync
```

## Generating from OpenAPI

```bash
# Generate TypeScript from OpenAPI schema
npm install -D openapi-typescript
npx openapi-typescript schema.yaml -o src/api-types.ts
```

```typescript
// Generated types - always in sync with API
export interface paths {
  "/users": {
    get: {
      responses: {
        200: {
          content: {
            "application/json": components["schemas"]["UserList"];
          };
        };
      };
    };
    post: {
      requestBody: {
        content: {
          "application/json": components["schemas"]["CreateUserRequest"];
        };
      };
    };
  };
}

export interface components {
  schemas: {
    User: {
      id: string;
      name: string;
      email: string;
    };
    UserList: {
      users: components["schemas"]["User"][];
      total: number;
    };
  };
}
```

## Generating from GraphQL

```bash
# Generate TypeScript from GraphQL schema
npm install -D @graphql-codegen/cli @graphql-codegen/typescript
```

```yaml
# codegen.yml
schema: schema.graphql
generates:
  src/generated/graphql.ts:
    plugins:
      - typescript
      - typescript-operations
```

```typescript
// Generated types from GraphQL schema
export type User = {
  __typename?: 'User';
  id: Scalars['ID']['output'];
  name: Scalars['String']['output'];
  email: Scalars['String']['output'];
  posts?: Maybe<Array<Maybe<Post>>>;
};

export type GetUserQueryVariables = {
  id: Scalars['ID']['input'];
};

export type GetUserQuery = {
  __typename?: 'Query';
  user?: {
    __typename?: 'User';
    id: string;
    name: string;
  } | null;
};
```

## Generating from Database Schemas

```bash
# Generate TypeScript from database
npm install -D prisma
npx prisma generate
```

```typescript
// Generated from database schema
export type User = {
  id: string
  email: string
  name: string | null
  posts: Post[]
}

export type Post = {
  id: string
  title: string
  content: string | null
  published: boolean
  author: User
  authorId: string
}
```

## When to Choose Codegen

Choose code generation when:

```typescript
// 1. Source of truth is external
// API schema, database, protocol buffer definition
// → Generate types, don't write them

// 2. Types would be extremely complex
// Type-level URL parser, complex state machines
// → Generate simple types instead

// 3. Synchronization is critical
// API changes must be reflected in types
// → CI generates types from schema

// 4. Team type-level expertise is limited
// Complex type code is hard to maintain
// → Generated code is easier to understand
```

## When to Choose Type-Level Code

Choose type-level programming when:

```typescript
// 1. Deriving from existing TypeScript types
// Deriving variants, transformations of your own types
// → Type-level code is appropriate

// 2. Simple transformations
// Pick, Omit, Partial - standard utilities
// → Type-level is simpler than codegen

// 3. No external source of truth
// Internal domain models
// → Write types directly

// 4. Need runtime flexibility
// Types depend on runtime values
// → Type-level code can handle this
```

## Keeping Generated Types in Sync

```json
// package.json
{
  "scripts": {
    "generate:api": "openapi-typescript api.yaml -o src/api-types.ts",
    "generate:db": "prisma generate",
    "build": "npm run generate:api && npm run generate:db && tsc",
    "predev": "npm run generate:api && npm run generate:db"
  }
}
```

```yaml
# .github/workflows/ci.yml
- name: Check generated types are up to date
  run: |
    npm run generate:api
    git diff --exit-code src/api-types.ts
```

## Hybrid Approach

```typescript
// Generate base types from external source
import type { User as GeneratedUser } from './generated/api';

// Extend with application-specific types
interface User extends GeneratedUser {
  // Add computed properties
  displayName: string;
}

// Derive using type-level code
type UserInput = Omit<User, 'id' | 'createdAt'>;
type UserUpdate = Partial<UserInput>;
```

## Pressure Resistance Protocol

When deciding between type-level code and codegen:

1. **Assess complexity**: Will the type-level code be maintainable?
2. **Check source of truth**: Is there an external schema?
3. **Consider team**: Can the team maintain complex type code?
4. **Evaluate drift risk**: How often will types need updating?
5. **Prototype both**: Try both approaches, compare maintainability

## Red Flags

| Symptom | Problem | Solution |
|---------|---------|----------|
| 100+ line type definitions | Too complex | Generate from schema |
| Manual updates for API changes | Drift risk | Auto-generate from API |
| Team avoids touching type files | Too complex | Simplify or generate |
| Types out of sync with backend | No single source | Generate from schema |

## Common Rationalizations

### "I don't want a build step"

**Reality**: Modern development already has build steps. Type generation is fast and integrates into existing workflows.

### "Generated code is ugly"

**Reality**: You don't read generated code, you use it. The types it produces are clean and well-typed.

### "I can write better types by hand"

**Reality**: You might write nicer types initially, but generated types stay in sync automatically.

## Quick Reference

| Source | Tool | Command |
|--------|------|---------|
| OpenAPI | openapi-typescript | `npx openapi-typescript schema.yaml -o types.ts` |
| GraphQL | @graphql-codegen | `npx graphql-codegen` |
| Database | Prisma | `npx prisma generate` |
| JSON Schema | json-schema-to-typescript | `npx json2ts schema.json -o types.ts` |
| Protobuf | protobuf-ts | `npx protoc --ts_out` |

## The Bottom Line

When types become too complex or must stay synchronized with external sources, generate them. Code generation trades build complexity for maintainability and correctness.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 58: Consider Codegen as an Alternative to Complex Types
