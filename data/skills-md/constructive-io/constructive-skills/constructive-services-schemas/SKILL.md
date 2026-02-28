---
name: constructive-services-schemas
description: >
  Create and configure Constructive services (APIs), attach database schemas to them,
  set up domains, API modules, and schema grants using the @constructive-io/sdk TypeScript SDK.
  Use when: "create an API", "set up a service", "attach schema to API", "configure domains",
  "add API module", "grant schema access", "set up service routing".
compatibility: Node.js 18+, @constructive-io/sdk
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Constructive Services & Schemas

Configure Constructive services (APIs), attach database schemas, set up domain routing, and manage access — all via the `@constructive-io/sdk` TypeScript SDK with zero SQL.

## When to Apply

Use this skill when:
- Creating a new API service for a Constructive database
- Attaching database schemas to an API to expose them via GraphQL
- Setting up domain/subdomain routing for APIs and sites
- Adding configuration modules to an API
- Granting role-based access to schemas
- Querying existing APIs with their attached schemas and domains

## Core Concepts

### Entity Hierarchy

```
Database (top-level container)
├── Schema (database schema, e.g. "public" — auto-created with database)
│   ├── Table, View, SchemaGrant, ...
│   └── ApiSchema (join: links Schema ↔ Api)
├── Api (service endpoint with role-based access)
│   ├── ApiSchema (which schemas this API exposes)
│   ├── ApiModule (named JSON config blobs)
│   └── Domain (routing: subdomain.domain → this API)
├── Site (website metadata: title, logo, favicon, etc.)
│   └── Domain (routing: subdomain.domain → this site)
└── Domain (maps subdomain + domain to an Api and/or Site)
```

### Key Relationships

| Entity | Purpose | Key Fields |
|--------|---------|------------|
| **Api** | A service endpoint | `databaseId`, `name`, `roleName`, `anonRole`, `isPublic` |
| **ApiSchema** | Links an Api to a Schema | `databaseId`, `apiId`, `schemaId` |
| **ApiModule** | Named JSON config for an Api | `databaseId`, `apiId`, `name`, `data` |
| **Domain** | Routes subdomain.domain → Api/Site | `databaseId`, `apiId`, `siteId`, `subdomain`, `domain` |
| **Schema** | Database schema container | `databaseId`, `name`, `schemaName` |
| **SchemaGrant** | Grants a role access to a schema | `databaseId`, `schemaId`, `granteeName` |

Every entity requires a `databaseId` — the UUID of the parent Database.

## SDK Setup

```typescript
import { createClient } from '@constructive-io/sdk';

const sdk = createClient({
  endpoint: 'https://your-constructive-api.example.com/graphql',
  headers: { Authorization: 'Bearer <token>' },
});
```

## Creating an API

An API defines a service endpoint with role-based access control.

```typescript
const result = await sdk.api
  .create({
    data: {
      databaseId,            // required: parent database UUID
      name: 'public',        // required: API name
      roleName: 'authenticated', // role for authenticated users
      anonRole: 'anonymous',    // role for anonymous access
      isPublic: true,           // whether the API is publicly accessible
    },
    select: { id: true, name: true, databaseId: true },
  })
  .execute();

if (!result.ok) {
  throw new Error(`createApi failed: ${JSON.stringify(result.errors)}`);
}

const api = result.data.createApi.api;
```

### Required fields for `api.create`:
- `databaseId` (string) — parent database UUID
- `name` (string) — API name (e.g., `"public"`, `"admin"`, `"meta"`)

### Optional fields:
- `dbname` (string) — database name override
- `roleName` (string) — role for authenticated users (e.g., `"authenticated"`, `"administrator"`)
- `anonRole` (string) — role for anonymous access (e.g., `"anonymous"`, `"administrator"`)
- `isPublic` (boolean) — whether the API is publicly accessible

## Attaching Schemas to an API

Use `apiSchema` to link a Schema to an Api. This is a many-to-many join — one API can expose multiple schemas, and one schema can be exposed by multiple APIs.

```typescript
const linkResult = await sdk.apiSchema
  .create({
    data: {
      databaseId,   // required: parent database UUID
      apiId: api.id, // required: the API to attach to
      schemaId: publicSchema.id, // required: the schema to expose
    },
    select: { id: true },
  })
  .execute();

if (!linkResult.ok) {
  throw new Error(`createApiSchema failed: ${JSON.stringify(linkResult.errors)}`);
}
```

### Required fields for `apiSchema.create`:
- `databaseId` (string)
- `apiId` (string) — the API to attach the schema to
- `schemaId` (string) — the schema to expose through this API

### Attaching multiple schemas to one API:

```typescript
const schemaIds = [publicSchemaId, usersSchemaId, authSchemaId];

for (const schemaId of schemaIds) {
  await sdk.apiSchema
    .create({
      data: { databaseId, apiId: api.id, schemaId },
      select: { id: true },
    })
    .execute();
}
```

## Setting Up Domains

Domains route `subdomain.domain` to an API and/or Site. Create the domain first, then link it to an API.

### Step 1: Create domains

```typescript
const domainResult = await sdk.domain
  .create({
    data: {
      databaseId,
      subdomain: 'api',       // the subdomain part
      domain: 'example.com',  // the domain part
    },
    select: { id: true, subdomain: true, domain: true },
  })
  .execute();

if (!domainResult.ok) {
  throw new Error(`createDomain failed: ${JSON.stringify(domainResult.errors)}`);
}

const domain = domainResult.data.createDomain.domain;
```

### Step 2: Link domain to an API

```typescript
const updateResult = await sdk.domain
  .update({
    where: { id: domain.id },
    data: { apiId: api.id },
    select: { id: true, apiId: true },
  })
  .execute();
```

### Required fields for `domain.create`:
- `databaseId` (string)

### Optional fields:
- `apiId` (string) — link to an API at creation time
- `siteId` (string) — link to a Site
- `subdomain` (string) — e.g., `"api"`, `"app"`, `"admin"`
- `domain` (string) — e.g., `"example.com"`, `"localhost"`

## Adding API Modules

API modules attach named JSON configuration to an API.

```typescript
const moduleResult = await sdk.apiModule
  .create({
    data: {
      databaseId,
      apiId: api.id,
      name: 'cors_config',       // required: module name
      data: {                     // required: JSON config data
        allowedOrigins: ['https://app.example.com'],
        allowedMethods: ['GET', 'POST'],
        maxAge: 86400,
      },
    },
    select: { id: true, name: true },
  })
  .execute();
```

### Required fields for `apiModule.create`:
- `databaseId` (string)
- `apiId` (string) — the API this module belongs to
- `name` (string) — module name
- `data` (JSON object) — module configuration

## Granting Schema Access

Schema grants control which roles can access a schema.

```typescript
const grantResult = await sdk.schemaGrant
  .create({
    data: {
      schemaId: publicSchema.id,
      granteeName: 'authenticated',  // role name to grant access to
    },
    select: { id: true },
  })
  .execute();
```

### Required fields for `schemaGrant.create`:
- `schemaId` (string) — the schema to grant access to
- `granteeName` (string) — the role name (e.g., `"authenticated"`, `"anonymous"`)

### Optional fields:
- `databaseId` (string)

## Querying APIs with Relations

### List all APIs with their schemas and domains

```typescript
const apis = await sdk.api
  .findMany({
    select: {
      id: true,
      name: true,
      roleName: true,
      anonRole: true,
      isPublic: true,
      apiSchemas: {
        select: {
          id: true,
          schema: {
            select: { id: true, name: true, schemaName: true },
          },
        },
      },
      domains: {
        select: { id: true, subdomain: true, domain: true },
      },
      apiModules: {
        select: { id: true, name: true, data: true },
      },
    },
  })
  .execute();
```

### Find a specific API by name

```typescript
const result = await sdk.api
  .findFirst({
    where: { name: { equalTo: 'public' } },
    select: {
      id: true,
      name: true,
      apiSchemas: {
        select: {
          schema: { select: { id: true, name: true } },
        },
      },
    },
  })
  .execute();
```

### Query a schema with its API links

```typescript
const schemaResult = await sdk.schema
  .findFirst({
    where: { name: { equalTo: 'public' } },
    select: {
      id: true,
      name: true,
      schemaName: true,
      apiSchemas: {
        select: {
          api: { select: { id: true, name: true } },
        },
      },
      schemaGrants: {
        select: { id: true, granteeName: true },
      },
    },
  })
  .execute();
```

## Complete End-to-End Example

This example shows a full service setup workflow: create a database, set up multiple APIs with different roles, attach schemas, configure domains, and add site metadata.

```typescript
import { createClient } from '@constructive-io/sdk';

const sdk = createClient({
  endpoint: 'https://your-api.example.com/graphql',
  headers: { Authorization: 'Bearer <token>' },
});

// 1. Create a database (schemas like "public" are auto-created)
const dbResult = await sdk.database
  .create({
    data: { name: 'my-project', ownerId: userId },
    select: {
      id: true,
      schemas: { select: { id: true, name: true }, first: 10 },
    },
  })
  .execute();

const database = dbResult.data.createDatabase.database;
const databaseId = database.id;
const publicSchema = database.schemas?.nodes?.find(
  (s) => s.name === 'public'
);

// 2. Create domains for routing
const subdomains = ['api', 'app', 'meta'];
const domains: Record<string, string> = {};

for (const subdomain of subdomains) {
  const domainResult = await sdk.domain
    .create({
      data: { databaseId, subdomain, domain: 'localhost' },
      select: { id: true },
    })
    .execute();
  domains[subdomain] = domainResult.data.createDomain.domain.id;
}

// 3. Helper: create an API, attach schemas, and link a domain
async function setupApi(opts: {
  name: string;
  roleName: string;
  anonRole: string;
  schemaIds?: string[];
  domainId: string;
}) {
  // Create the API
  const apiResult = await sdk.api
    .create({
      data: {
        databaseId,
        name: opts.name,
        roleName: opts.roleName,
        anonRole: opts.anonRole,
        isPublic: true,
      },
      select: { id: true, name: true },
    })
    .execute();

  const api = apiResult.data.createApi.api;

  // Attach schemas
  for (const schemaId of opts.schemaIds ?? []) {
    await sdk.apiSchema
      .create({
        data: { databaseId, apiId: api.id, schemaId },
        select: { id: true },
      })
      .execute();
  }

  // Link domain to this API
  await sdk.domain
    .update({
      where: { id: opts.domainId },
      data: { apiId: api.id },
      select: { id: true },
    })
    .execute();

  return api;
}

// 4. Set up services
await setupApi({
  name: 'public',
  roleName: 'authenticated',
  anonRole: 'anonymous',
  schemaIds: [publicSchema.id],
  domainId: domains['api'],
});

await setupApi({
  name: 'meta',
  roleName: 'authenticated',
  anonRole: 'anonymous',
  domainId: domains['meta'],
});

// 5. Create a site and link it to the app domain
const siteResult = await sdk.site
  .create({
    data: {
      databaseId,
      title: 'My App',
      description: 'My Constructive application',
    },
    select: { id: true },
  })
  .execute();

await sdk.domain
  .update({
    where: { id: domains['app'] },
    data: { siteId: siteResult.data.createSite.site.id },
    select: { id: true },
  })
  .execute();
```

## Updating and Deleting

### Update an API

```typescript
await sdk.api
  .update({
    where: { id: apiId },
    data: { isPublic: false, anonRole: 'authenticated' },
    select: { id: true, isPublic: true },
  })
  .execute();
```

### Remove a schema from an API

```typescript
await sdk.apiSchema
  .delete({
    where: { id: apiSchemaId },
    select: { id: true },
  })
  .execute();
```

### Delete a domain

```typescript
await sdk.domain
  .delete({
    where: { id: domainId },
    select: { id: true },
  })
  .execute();
```

## Common Patterns

### Multiple APIs, same database

A single database typically has several APIs with different access levels:

| API Name | `roleName` | `anonRole` | Purpose |
|----------|-----------|-----------|---------|
| `public` | `authenticated` | `anonymous` | Public-facing API |
| `meta` | `authenticated` | `anonymous` | Metadata/schema introspection |

> **DANGEROUS — Development/Testing Only!**
>
> APIs with `administrator` as both `roleName` and `anonRole` (e.g., `admin`, `super`)
> should **never** exist in production. These grant full administrator access to
> anonymous users. They are only used in local development and test environments.
> If you see administrator APIs in a production setup, treat it as a critical
> security misconfiguration.

### Domain routing pattern

Each API gets its own subdomain:

| Subdomain | Domain | Linked To |
|-----------|--------|-----------|
| `api` | `example.com` | `public` API |
| `app` | `example.com` | Site (frontend) |
| `meta` | `example.com` | `meta` API |

## Error Handling

All SDK operations return a discriminated union. Always check `.ok`:

```typescript
const result = await sdk.api.create({ ... }).execute();

if (!result.ok) {
  console.error('Failed:', result.errors);
  // result.errors is GraphQLError[]
  return;
}

// Safe to access result.data
const api = result.data.createApi.api;
```

Or use `.unwrap()` to throw on error:

```typescript
const data = await sdk.api.create({ ... }).unwrap();
const api = data.createApi.api;
```

## References

- For detailed ORM field reference, see `references/entity-fields.md`
- Related skill: `constructive-graphql-codegen` — generate the typed SDK
- Related skill: `constructive-functions` — build cloud functions using the SDK
