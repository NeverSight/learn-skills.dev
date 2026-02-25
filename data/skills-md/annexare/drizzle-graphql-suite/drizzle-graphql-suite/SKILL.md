---
name: drizzle-graphql-suite
description: Build GraphQL APIs from Drizzle PostgreSQL schemas with auto-generated CRUD, type-safe clients, and React Query hooks. Use when creating GraphQL servers from Drizzle ORM tables, building type-safe GraphQL clients, adding React data-fetching hooks with TanStack Query, or generating GraphQL SDL/types from Drizzle schemas.
---

# drizzle-graphql-suite

Three-layer toolkit that turns Drizzle ORM PostgreSQL schemas into fully working GraphQL APIs with end-to-end type safety.

## Packages

| Import | Package | Purpose |
|--------|---------|---------|
| `drizzle-graphql-suite/schema` | `@drizzle-graphql-suite/schema` | Server-side GraphQL schema builder with CRUD, filtering, hooks, and codegen |
| `drizzle-graphql-suite/client` | `@drizzle-graphql-suite/client` | Type-safe GraphQL client with entity-based API |
| `drizzle-graphql-suite/query` | `@drizzle-graphql-suite/query` | TanStack React Query hooks wrapping the client |

**Data flow:** Drizzle schema -> `buildSchema()` -> GraphQL server -> `createDrizzleClient()` -> `<GraphQLProvider>` + hooks

**Peer dependencies:**
- `./schema`: `drizzle-orm` >=0.44.0, `graphql` >=16.3.0
- `./client`: `drizzle-orm` >=0.44.0
- `./query`: `react` >=18.0.0, `@tanstack/react-query` >=5.0.0

## When to Use

Use this skill when the user is:
- Creating a GraphQL server from Drizzle ORM table definitions
- Building type-safe GraphQL clients for a drizzle-graphql-suite server
- Adding React data-fetching with TanStack Query for GraphQL
- Generating GraphQL SDL or static TypeScript types when client and server are in separate repos
- Configuring hooks, table exclusion, relation depth, or operation filtering
- Setting up runtime permissions or role-based schema variants
- Implementing row-level security with WHERE clause injection
- Working with relation-level filtering (some/every/none quantifiers)
- Debugging GraphQL schema generation or client type inference

## Quick Start

### 1. Define Drizzle Schema

```ts
// db/schema.ts
import { relations } from 'drizzle-orm'
import { pgTable, text, uuid } from 'drizzle-orm/pg-core'

export const user = pgTable('user', {
  id: uuid().primaryKey().defaultRandom(),
  name: text().notNull(),
  email: text().notNull(),
})

export const post = pgTable('post', {
  id: uuid().primaryKey().defaultRandom(),
  title: text().notNull(),
  body: text().notNull(),
  userId: uuid().notNull(),
})

export const userRelations = relations(user, ({ many }) => ({
  posts: many(post),
}))

export const postRelations = relations(post, ({ one }) => ({
  author: one(user, { fields: [post.userId], references: [user.id] }),
}))
```

### 2. Build GraphQL Server

```ts
import { buildSchema } from 'drizzle-graphql-suite/schema'
import { createYoga } from 'graphql-yoga'
import { createServer } from 'node:http'
import { db } from './db'

const { schema } = buildSchema(db, {
  tables: { exclude: ['session'] },
  hooks: {
    user: {
      query: {
        before: async ({ context }) => {
          if (!context.user) throw new Error('Unauthorized')
        },
      },
    },
  },
})

const yoga = createYoga({ schema })
createServer(yoga).listen(4000)
```

### 3. Create Type-Safe Client

```ts
import { createDrizzleClient } from 'drizzle-graphql-suite/client'
import * as schema from './db/schema'

const client = createDrizzleClient({
  schema,
  config: { suffixes: { list: 's' } },
  url: '/api/graphql',
  headers: () => ({ Authorization: `Bearer ${getToken()}` }),
})

const users = await client.entity('user').query({
  select: { id: true, name: true, posts: { id: true, title: true } },
  where: { name: { ilike: '%john%' } },
  limit: 10,
})
```

### 4. Add React Hooks

```tsx
import { GraphQLProvider, useEntity, useEntityList } from 'drizzle-graphql-suite/query'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <GraphQLProvider client={graphqlClient}>
        <UserList />
      </GraphQLProvider>
    </QueryClientProvider>
  )
}

function UserList() {
  const user = useEntity('user')
  const { data, isLoading } = useEntityList(user, {
    select: { id: true, name: true, email: true },
    limit: 20,
  })

  if (isLoading) return <div>Loading...</div>
  return <ul>{data?.map((u) => <li key={u.id}>{u.name}</li>)}</ul>
}
```

## Core API

### Schema Package (`drizzle-graphql-suite/schema`)

```ts
// Build complete GraphQL schema from Drizzle db instance
buildSchema(db, config?): { schema: GraphQLSchema; entities: GeneratedEntities; withPermissions: (p: PermissionConfig) => GraphQLSchema }

// Build entities only (queries, mutations, inputs, types) without full schema
buildEntities(db, config?): GeneratedEntities

// Build schema from Drizzle exports without a db connection (for codegen only)
buildSchemaFromDrizzle(drizzleSchema, config?): { schema: GraphQLSchema; entities: GeneratedEntities; withPermissions: (p: PermissionConfig) => GraphQLSchema }

// Permission helpers — build PermissionConfig objects for withPermissions()
permissive(id, tables?): PermissionConfig             // All tables allowed by default; overrides deny
restricted(id, tables?): PermissionConfig             // Nothing allowed by default; overrides grant
readOnly(): TableAccess                               // Shorthand: queries only, no mutations

// Row-level security and hook composition
withRowSecurity(rules): HooksConfig                   // Generate WHERE-injecting hooks from rules
mergeHooks(...configs): HooksConfig                   // Deep-merge multiple HooksConfig objects

// Code generation (for separate-repo setups where client can't import Drizzle schema)
generateSDL(schema): string                          // GraphQL SDL string
generateTypes(schema, options?): string               // TypeScript types (wire, filters, inputs, orderBy)
generateEntityDefs(schema, options?): string           // Runtime entity descriptors + EntityDefs type

// Custom scalar
GraphQLJSON  // JSON scalar type for json/jsonb columns
```

### Client Package (`drizzle-graphql-suite/client`)

```ts
// Recommended: create client from Drizzle schema (full type inference)
createDrizzleClient(options): GraphQLClient

// Alternative: create client from pre-generated schema descriptor
createClient(config): GraphQLClient

// Build schema descriptor from Drizzle schema (for codegen workflows)
buildSchemaDescriptor(schema, config?): SchemaDescriptor

// Error classes
GraphQLClientError  // GraphQL response errors (has .errors, .status)
NetworkError        // HTTP/network failures (has .status)
```

**Entity operations** (via `client.entity('name')`):

| Method | Description |
|--------|-------------|
| `query({ select, where?, limit?, offset?, orderBy? })` | List query returning `T[]` |
| `querySingle({ select, where?, offset?, orderBy? })` | Single query returning `T \| null` |
| `count({ where? })` | Count matching rows |
| `insert({ values, returning? })` | Insert array, returns `T[]` |
| `insertSingle({ values, returning? })` | Insert one, returns `T \| null` |
| `update({ set, where?, returning? })` | Update matching rows |
| `delete({ where?, returning? })` | Delete matching rows |

### Query Package (`drizzle-graphql-suite/query`)

```tsx
// Provider (wrap app)
<GraphQLProvider client={graphqlClient}>

// Access hooks
useGraphQLClient()                                    // Get client from context
useEntity(entityName)                                 // Get typed EntityClient

// Query hooks
useEntityQuery(entity, params, options?)              // Single entity (T | null)
useEntityList(entity, params, options?)               // List query (T[])
useEntityInfiniteQuery(entity, params, options?)      // Paginated infinite query

// Mutation hooks
useEntityInsert(entity, returning?, options?)         // Insert mutation
useEntityUpdate(entity, returning?, options?)         // Update mutation
useEntityDelete(entity, returning?, options?)         // Delete mutation
```

## Configuration

### `BuildSchemaConfig` (Server)

```ts
buildSchema(db, {
  mutations: true,                  // Generate mutations (default: true)
  limitRelationDepth: 3,            // Max relation nesting depth (default: 3, 0 = no relations)
  limitSelfRelationDepth: 1,        // Self-relation depth (default: 1 = omitted)
  suffixes: { list: '', single: 'Single' },  // Query name suffixes
  tables: {
    exclude: ['session', 'migration'],        // Omit tables entirely
    config: {
      auditLog: { queries: true, mutations: false },  // Per-table operation control
    },
  },
  pruneRelations: {
    'user.sensitiveData': false,              // Omit relation entirely
    'post.comments': 'leaf',                  // Expand with scalars only
    'org.members': { only: ['profile'] },     // Expand with listed relations only
  },
  hooks: { /* see Hooks section */ },
  debug: true,                                // Log schema size diagnostics
})
```

### `ClientSchemaConfig` (Client)

The client config must align with the server config for correct query generation:

```ts
createDrizzleClient({
  schema,
  config: {
    mutations: true,                          // Must match server
    suffixes: { list: 's', single: 'Single' },  // Must match server
    tables: { exclude: ['session'] },         // Must match server
    pruneRelations: { 'user.secret': false }, // Must match server
  },
  url: '/api/graphql',
})
```

See [references/configuration.md](references/configuration.md) for full details.

## Hooks

Hooks intercept query/mutation execution on the server. Two patterns:

### Before/After Hooks

```ts
hooks: {
  user: {
    query: {
      before: async ({ args, context, info }) => {
        if (!context.user) throw new Error('Unauthorized')
        // Optionally return { args } to override resolver arguments
        // Optionally return { data } to pass data to after hook
      },
      after: async ({ result, beforeData, context }) => {
        // Transform or log result
        return result
      },
    },
  },
}
```

### Resolve Hooks (replace entire resolver)

```ts
hooks: {
  post: {
    insert: {
      resolve: async ({ args, context, info, defaultResolve }) => {
        args.values = args.values.map((v) => ({ ...v, authorId: context.user.id }))
        return defaultResolve(args)
      },
    },
  },
}
```

Hooks apply to all 7 operation types: `query`, `querySingle`, `count`, `insert`, `insertSingle`, `update`, `delete`.

See [patterns/hooks-patterns.md](patterns/hooks-patterns.md) for common recipes.

## Permissions

Build filtered `GraphQLSchema` variants per role or user — introspection fully reflects what each role can see and do.

```ts
import { buildSchema, permissive, restricted, readOnly } from 'drizzle-graphql-suite/schema'

const { schema, withPermissions } = buildSchema(db)

// Full schema (admin)
const adminSchema = schema

// Permissive: everything allowed except audit (excluded) and users (read-only)
const maintainerSchema = withPermissions(
  permissive('maintainer', { audit: false, users: readOnly() }),
)

// Restricted: nothing allowed except posts and comments (queries only)
const userSchema = withPermissions(
  restricted('user', { posts: { query: true }, comments: { query: true } }),
)

// Restricted with nothing granted — only Query { _empty: Boolean }
const anonSchema = withPermissions(restricted('anon'))
```

### Permission Helpers

| Helper | Description |
|--------|-------------|
| `permissive(id, tables?)` | All tables allowed by default; overrides deny |
| `restricted(id, tables?)` | Nothing allowed by default; overrides grant |
| `readOnly()` | Shorthand for `{ query: true, insert: false, update: false, delete: false }` |

### `TableAccess`

Each table can be set to `true` (all operations), `false` (excluded entirely), or a `TableAccess` object:

```ts
type TableAccess = {
  query?: boolean   // list + single + count
  insert?: boolean  // insert + insertSingle
  update?: boolean
  delete?: boolean
}
```

In **permissive** mode, omitted fields default to `true`. In **restricted** mode, omitted fields default to `false`.

### Caching

Schemas are cached by `id` — calling `withPermissions` with the same `id` returns the same `GraphQLSchema` instance.

See [references/permissions.md](references/permissions.md) for full API details and [examples/permissions.md](examples/permissions.md) for multi-role examples.

## Row-Level Security

Generate hooks that inject WHERE clauses for row-level filtering. Compose with other hooks using `mergeHooks`.

```ts
import { buildSchema, withRowSecurity, mergeHooks } from 'drizzle-graphql-suite/schema'

const { schema } = buildSchema(db, {
  hooks: mergeHooks(
    withRowSecurity({
      posts: (context) => ({ authorId: { eq: context.user.id } }),
    }),
    myOtherHooks,
  ),
})
```

### `withRowSecurity(rules)`

Generates a `HooksConfig` with `before` hooks on `query`, `querySingle`, `count`, `update`, and `delete` operations. Each rule is a function that receives the GraphQL context and returns a WHERE filter object.

### `mergeHooks(...configs)`

Deep-merges multiple `HooksConfig` objects:

- **`before` hooks** — chained sequentially; each receives the previous hook's modified args
- **`after` hooks** — chained sequentially; each receives the previous hook's result
- **`resolve` hooks** — last one wins (cannot be composed)

See [patterns/hooks-patterns.md](patterns/hooks-patterns.md) for composition recipes.

## Relation Filtering

Filter across relations using EXISTS subqueries:

```ts
// One-to-one: direct filter
where: { author: { name: { eq: 'Alice' } } }

// One-to-many: quantifier object
where: {
  comments: {
    some: { body: { ilike: '%bug%' } },    // At least one comment matches
    every: { approved: { eq: true } },      // All comments match
    none: { spam: { eq: true } },           // No comments match
  },
}

// Logical OR
where: {
  OR: [
    { title: { ilike: '%graphql%' } },
    { author: { name: { eq: 'Alice' } } },
  ],
}
```

## Error Handling

### Server (Schema Package)

Errors thrown in hooks or resolvers are caught and re-thrown as `GraphQLError`:
```ts
// Errors are prefixed: "Drizzle-GraphQL Error: ..."
// In custom hooks, throw standard Error — it will be wrapped in GraphQLError
```

### Client

```ts
import { GraphQLClientError, NetworkError } from 'drizzle-graphql-suite/client'

try {
  await client.entity('user').query({ select: { id: true } })
} catch (e) {
  if (e instanceof NetworkError) {
    console.error('HTTP error:', e.status, e.message)
  }
  if (e instanceof GraphQLClientError) {
    console.error('GraphQL errors:', e.errors)  // GraphQLErrorEntry[]
    console.error('HTTP status:', e.status)
  }
}
```

## Generated Operation Names

| Table `user` | Generated Name |
|-------------|----------------|
| List query | `user` (or `users` with `suffixes.list: 's'`) |
| Single query | `userSingle` (customizable via `suffixes.single`) |
| Count query | `userCount` |
| Insert | `insertIntoUser` |
| Insert single | `insertIntoUserSingle` |
| Update | `updateUser` |
| Delete | `deleteFromUser` |

## Resources

### Reference Documentation
- [Schema API](references/schema-api.md) — Full schema package API with all function signatures
- [Client API](references/client-api.md) — Client package API, EntityClient methods, error classes
- [Query API](references/query-api.md) — React hooks API, options, cache invalidation
- [Configuration](references/configuration.md) — BuildSchemaConfig and ClientSchemaConfig details
- [Permissions](references/permissions.md) — Permission helpers, withPermissions, TableAccess, RLS, mergeHooks
- [Type Mapping](references/type-mapping.md) — PostgreSQL column to GraphQL type mapping
- [Code Generation](references/codegen.md) — SDL/type generation for separate-repo setups

### Examples
- [Drizzle Schema](examples/drizzle-schema.md) — Shared example schema (users, posts, comments)
- [GraphQL Yoga Server](examples/server-yoga.md) — Server setup with hooks and table exclusion
- [Next.js Integration](examples/server-nextjs.md) — Next.js App Router route handler
- [ElysiaJS Integration](examples/server-elysia.md) — ElysiaJS with graphql-yoga plugin
- [Client Operations](examples/client-basic.md) — All 7 entity operations with createDrizzleClient
- [React CRUD](examples/react-crud.md) — Full CRUD component using all hooks
- [Auth Hooks](examples/hooks-auth.md) — Authentication and authorization hook patterns
- [Permissions](examples/permissions.md) — Multi-role permission setup with RLS
- [Codegen Script](examples/codegen-script.md) — Generate SDL/types for separate-repo setups

### Patterns
- [End-to-End Setup](patterns/end-to-end-setup.md) — Full stack setup guide with config alignment
- [Hook Recipes](patterns/hooks-patterns.md) — Auth guards, audit logging, hook composition, RLS
