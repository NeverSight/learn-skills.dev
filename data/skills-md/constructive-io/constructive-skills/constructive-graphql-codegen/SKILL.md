---
name: constructive-graphql-codegen
description: Generate type-safe React Query hooks, Prisma-like ORM client, or inquirerer-based CLI from GraphQL endpoints, schema files/directories, databases, or PGPM modules using @constructive-io/graphql-codegen. Also generates documentation (README, AGENTS.md, skills/, mcp.json). Use when asked to "generate GraphQL hooks", "generate ORM", "generate CLI", "set up codegen", "generate docs", "generate skills", "export schema", or when implementing data fetching for a PostGraphile backend.
compatibility: Node.js 22+, PostgreSQL 14+, PostGraphile v5+ (optional)
metadata:
  author: constructive-io
  version: "4.5.x"
---

# Constructive GraphQL Codegen

Generate type-safe React Query hooks, Prisma-like ORM client, or inquirerer-based CLI from GraphQL schema files, endpoints, databases, or PGPM modules. Also generates documentation in multiple formats.

## When to Apply

Use this skill when:
- Setting up GraphQL code generation for a PostGraphile backend
- User asks to generate hooks, ORM, CLI, or type-safe GraphQL client
- Exporting a GraphQL schema from a database or endpoint
- Generating documentation (README, AGENTS.md, skill files, MCP tool definitions)
- Implementing features that need to fetch or mutate data
- Using previously generated hooks, ORM, or CLI code
- Regenerating code after schema changes

**Important**: Always prefer generated code over raw GraphQL queries or SQL.

## Recommended Workflow: Schema Export + Schema Directory

The **recommended approach** is a two-step workflow using schema export followed by `schemaDir`. This is the most deterministic and portable way to use codegen:

### Step 1: Export schema(s) to `.graphql` files

Export your schema from any source (database, PGPM module, endpoint) into a directory of `.graphql` files:

```bash
# Export from database
npx @constructive-io/graphql-codegen --schema-only --schemas public --schema-only-output ./schemas --schema-only-filename public.graphql

# Export from PGPM module (via config)
npx @constructive-io/graphql-codegen --schema-only -c graphql-codegen.config.ts

# Export from endpoint
npx @constructive-io/graphql-codegen --schema-only -e https://api.example.com/graphql --schema-only-output ./schemas
```

Or programmatically:

```typescript
import { generate } from '@constructive-io/graphql-codegen';

// Export from database
await generate({
  db: { schemas: ['public'] },
  schemaOnly: true,
  schemaOnlyOutput: './schemas',
  schemaOnlyFilename: 'public.graphql',
});

// Export from PGPM module
await generate({
  db: {
    pgpm: { modulePath: './packages/my-module' },
    schemas: ['app_public'],
  },
  schemaOnly: true,
  schemaOnlyOutput: './schemas',
  schemaOnlyFilename: 'app_public.graphql',
});
```

### Step 2: Generate code from the schema directory

Point `schemaDir` at the directory containing your `.graphql` files. Each file automatically becomes a separate target:

```typescript
// graphql-codegen.config.ts
import { defineConfig } from '@constructive-io/graphql-codegen';

export default defineConfig({
  schemaDir: './schemas',   // Directory of .graphql files
  output: './generated',    // Each file becomes ./generated/{name}/
  reactQuery: true,
  orm: true,
});
```

```bash
npx @constructive-io/graphql-codegen -c graphql-codegen.config.ts
```

Given `schemas/public.graphql` and `schemas/admin.graphql`, this produces:

```
generated/
  public/          # Generated from public.graphql
    hooks/
    orm/
  admin/           # Generated from admin.graphql
    hooks/
    orm/
```

**Why this approach is best:**
- **Deterministic** — `.graphql` files are static, version-controllable artifacts
- **Portable** — no live database or endpoint needed at code generation time
- **Fast** — no network requests or ephemeral database creation during codegen
- **Reviewable** — schema changes show up as clear diffs in version control

## Quick Start

### Installation

```bash
pnpm add @constructive-io/graphql-codegen
```

### Generate React Query Hooks

```bash
npx @constructive-io/graphql-codegen --react-query -s ./schemas/public.graphql -o ./generated
```

### Generate ORM Client

```bash
npx @constructive-io/graphql-codegen --orm -s ./schemas/public.graphql -o ./generated
```

### Generate CLI

```bash
npx @constructive-io/graphql-codegen --cli -s ./schemas/public.graphql -o ./generated
```

### Generate from Endpoint

```bash
npx @constructive-io/graphql-codegen --react-query -e https://api.example.com/graphql -o ./generated
```

### Generate from Database

```bash
npx @constructive-io/graphql-codegen --react-query --schemas public,app_public -o ./generated
```

## Programmatic API

Use the `generate()` function to integrate codegen into your build scripts or tools.

### Import and Basic Usage

```typescript
import { generate } from '@constructive-io/graphql-codegen';

// Generate from endpoint
await generate({
  endpoint: 'https://api.example.com/graphql',
  output: './generated',
  reactQuery: true,
  orm: true,
});

// Node.js with undici dispatcher (fixes localhost DNS issues)
await generate({
  endpoint: 'http://api.localhost:3000/graphql',
  output: './generated',
  reactQuery: true,
  browserCompatible: false,  // Use undici with custom dispatcher
});
```

### Schema Sources

```typescript
// From GraphQL endpoint
await generate({
  endpoint: 'https://api.example.com/graphql',
  headers: { Authorization: 'Bearer token' },
  reactQuery: true,
});

// From schema file
await generate({
  schemaFile: './schema.graphql',
  output: './generated',
  orm: true,
});

// From database (explicit schemas)
await generate({
  db: { schemas: ['public', 'app_public'] },
  reactQuery: true,
});

// From database (auto-discover via API names)
await generate({
  db: { apiNames: ['my_api'] },
  orm: true,
});

// From PGPM module
await generate({
  db: {
    pgpm: { modulePath: './packages/my-module' },
    schemas: ['public'],
  },
  reactQuery: true,
});
```

### Generate Options

```typescript
interface GenerateOptions {
  // Schema source (choose one)
  endpoint?: string;
  schemaFile?: string;
  schemaDir?: string;       // Directory of .graphql files — auto-expands to multi-target
  db?: {
    config?: { host, port, database, user, password };
    schemas?: string[];
    apiNames?: string[];    // Auto-discover schemas from services_public.api_schemas
    pgpm?: { modulePath, workspacePath, moduleName };
    keepDb?: boolean;       // Keep ephemeral DB after introspection (debugging)
  };
  
  // Output
  output?: string;  // Default: './generated/graphql'
  
  // Generators
  reactQuery?: boolean;  // Default: false
  orm?: boolean;         // Default: false
  cli?: CliConfig | boolean; // Default: false — generate inquirerer CLI
  
  // Schema export (instead of code generation)
  schemaOnly?: boolean;          // Export schema to .graphql file, skip codegen
  schemaOnlyOutput?: string;     // Output directory for exported schema
  schemaOnlyFilename?: string;   // Filename (default: 'schema.graphql')
  
  // Documentation (generated alongside code)
  docs?: DocsConfig | boolean; // Default: { readme: true, agents: true, mcp: false, skills: false }
  
  // Node.js HTTP adapter (auto-enabled when cli is true)
  nodeHttpAdapter?: boolean; // Default: false
  
  // Filtering
  tables?: { include?, exclude?, systemExclude? };
  queries?: { include?, exclude?, systemExclude? };
  mutations?: { include?, exclude?, systemExclude? };
  excludeFields?: string[];
  
  // Authentication
  headers?: Record<string, string>;
  authorization?: string;  // Convenience for Authorization header
  
  // Options
  verbose?: boolean;
  dryRun?: boolean;
  skipCustomOperations?: boolean;
}
```

### Build Script Example

```typescript
// scripts/codegen.ts
import { generate } from '@constructive-io/graphql-codegen';

async function main() {
  console.log('Generating GraphQL code...');
  
  const result = await generate({
    endpoint: process.env.GRAPHQL_ENDPOINT!,
    headers: {
      Authorization: `Bearer ${process.env.API_TOKEN}`,
    },
    output: './src/generated',
    reactQuery: true,
    orm: true,
    tables: {
      include: ['User', 'Post', 'Comment'],
    },
  });
  
  if (!result.success) {
    console.error('Codegen failed:', result.error);
    process.exit(1);
  }
  
  console.log('✓ Code generated successfully');
}

main();
```

## CLI Commands

**Note**: The CLI does not use subcommands. All options are passed directly to `graphql-codegen`.

| Command | Purpose |
|---------|---------|
| `npx @constructive-io/graphql-codegen` | Generate code (use `--react-query`, `--orm`, and/or `--cli` flags) |
| `npx @constructive-io/graphql-codegen --react-query` | Generate React Query hooks |
| `npx @constructive-io/graphql-codegen --orm` | Generate ORM client |
| `npx @constructive-io/graphql-codegen --cli` | Generate inquirerer-based CLI |
| `npx @constructive-io/graphql-codegen --react-query --orm --cli` | Generate all three |

### Common Options

| Option | Description |
|--------|-------------|
| `-e, --endpoint <url>` | GraphQL endpoint URL |
| `-s, --schema-file <path>` | Path to GraphQL schema file |
| `--schema-dir <path>` | Directory of `.graphql` files (auto multi-target) |
| `--schemas <list>` | PostgreSQL schemas (comma-separated) |
| `--api-names <list>` | API names for auto schema discovery |
| `-o, --output <dir>` | Output directory (default: `./generated/graphql`) |
| `-c, --config <path>` | Config file path |
| `--react-query` | Generate React Query hooks |
| `--orm` | Generate ORM client |
| `--cli` | Generate inquirerer-based CLI |
| `--schema-only` | Export schema to `.graphql` file (no code generation) |
| `--schema-only-output <dir>` | Output directory for schema export |
| `--schema-only-filename <name>` | Filename for exported schema (default: `schema.graphql`) |
| `-a, --authorization <token>` | Authorization header |
| `-t, --target <name>` | Target name in multi-target config |
| `--dry-run` | Preview without writing |
| `-v, --verbose` | Show detailed output |

## Configuration File

Create a configuration file manually:

**File: `graphql-codegen.config.ts`**

```typescript
import { defineConfig } from '@constructive-io/graphql-codegen';

// RECOMMENDED: From a directory of .graphql schema files
export default defineConfig({
  schemaDir: './schemas',
  output: './generated',
  reactQuery: true,
  orm: true,
});

// From a single schema file
export default defineConfig({
  schemaFile: './schemas/public.graphql',
  output: './generated',
  reactQuery: true,
  orm: true,
});

// From GraphQL endpoint
export default defineConfig({
  endpoint: 'https://api.example.com/graphql',
  output: './generated',
  reactQuery: true,
  orm: true,
  headers: {
    Authorization: `Bearer ${process.env.API_TOKEN}`,
  },
});

// From database
export default defineConfig({
  db: {
    schemas: ['public', 'app_public'],  // Explicit schemas
    // OR
    apiNames: ['my_api'],  // Auto-discover schemas from API
  },
  output: './generated',
  reactQuery: true,
});

// From PGPM module
export default defineConfig({
  db: {
    pgpm: { modulePath: './packages/my-module' },
    schemas: ['public'],
  },
  output: './generated',
  orm: true,
});
```

### CLI Generation

```typescript
export default defineConfig({
  endpoint: 'https://api.example.com/graphql',
  output: './generated',
  cli: true,  // Generate CLI with default tool name
  // OR with options:
  cli: {
    toolName: 'myapp',      // Config stored at ~/.myapp/
    entryPoint: true,        // Generate runnable index.ts
    builtinNames: {          // Override infra command names
      auth: 'credentials',
      context: 'env',
    },
  },
});
```

When `cli: true`, `nodeHttpAdapter` is auto-enabled (Node.js HTTP adapter for localhost subdomain resolution).

### Documentation Generation

```typescript
export default defineConfig({
  endpoint: 'https://api.example.com/graphql',
  output: './generated',
  orm: true,
  docs: true,  // Enable all doc formats
  // OR configure individually:
  docs: {
    readme: true,   // README.md — human-readable overview
    agents: true,   // AGENTS.md — structured for LLM consumption
    mcp: false,     // mcp.json — MCP tool definitions
    skills: true,   // skills/ — per-command .md skill files (Devin-compatible)
  },
});
```

**`docs.skills`**: Generates a `skills/` directory with individual `.md` files for each command. Compatible with Devin and similar agent skill systems. Each skill file contains description, usage, and examples.

**`docs.agents`**: Generates an `AGENTS.md` with tool definitions, exact signatures, input/output schemas, workflow recipes, and machine-parseable sections.

**`docs.mcp`**: Generates an `mcp.json` with MCP (Model Context Protocol) tool definitions. Each CLI command becomes a tool with typed JSON Schema `inputSchema`.

### Node.js HTTP Adapter

```typescript
export default defineConfig({
  endpoint: 'http://api.localhost:3000/graphql',
  output: './generated',
  orm: true,
  nodeHttpAdapter: true,  // Generates node-fetch.ts with NodeHttpAdapter
});
```

The `NodeHttpAdapter` uses `node:http`/`node:https` for requests, enabling local development with subdomain-based routing (e.g., `auth.localhost:3000`). No global patching required.

```typescript
import { NodeHttpAdapter } from './orm/node-fetch';
import { createClient } from './orm';

const db = createClient({
  adapter: new NodeHttpAdapter(endpoint, headers),
});
```

### Multi-Target Configuration

There are three ways to get multi-target generation:

#### 1. Schema directory (recommended)

`schemaDir` automatically creates one target per `.graphql` file in the directory:

```typescript
export default defineConfig({
  schemaDir: './schemas',   // Contains public.graphql, admin.graphql, etc.
  output: './generated',    // Produces ./generated/public/, ./generated/admin/, etc.
  reactQuery: true,
  orm: true,
});
```

#### 2. Explicit multi-target

Define each target explicitly when they have different sources or options:

```typescript
export default defineConfig({
  public: {
    schemaFile: './schemas/public.graphql',
    output: './generated/public',
    reactQuery: true,
  },
  admin: {
    schemaFile: './schemas/admin.graphql',
    output: './generated/admin',
    orm: true,
    cli: true,
  },
});
```

#### 3. Auto-expand from multiple API names

When `db.apiNames` contains multiple entries, each API name automatically becomes a separate target:

```typescript
export default defineConfig({
  db: { apiNames: ['public', 'admin'] },
  output: './generated',  // Produces ./generated/public/, ./generated/admin/
  orm: true,
});
```

This queries `services_public.api_schemas` for each API name to resolve the corresponding PostgreSQL schemas, then generates each target independently.

#### Shared PGPM sources in multi-target

When multiple targets share the same PGPM module, the codegen automatically deduplicates ephemeral database creation. One ephemeral database is created and reused across all targets that reference the same module, avoiding redundant deploys.

## Using Generated Hooks

### Configure Client (once at app startup)

```typescript
import { configure } from '@/generated/hooks';

configure({
  endpoint: process.env.NEXT_PUBLIC_GRAPHQL_URL!,
  headers: { Authorization: `Bearer ${getToken()}` },
});
```

### Query Data

```typescript
import { useUsersQuery } from '@/generated/hooks';

function UserList() {
  const { data, isLoading } = useUsersQuery({
    first: 10,
    filter: { role: { eq: 'ADMIN' } },
  });

  if (isLoading) return <Spinner />;
  return <ul>{data?.users?.nodes.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

### Mutate Data

```typescript
import { useCreateUserMutation } from '@/generated/hooks';

function CreateUser() {
  const createUser = useCreateUserMutation();

  return (
    <button onClick={() => createUser.mutate({ input: { name: 'John' } })}>
      Create
    </button>
  );
}
```

## Using Generated CLI

When `cli: true` is set, codegen generates inquirerer-based CLI commands to `{output}/cli/`.

### Generated Structure

```
generated/cli/
  commands/           # One file per table + custom operations
    users.ts          # CRUD commands for users table
    posts.ts          # CRUD commands for posts table
    my-query.ts       # Custom query command
  command-map.ts      # Maps command names to handlers
  executor.ts         # Command executor with auth context
  utils.ts            # Shared utilities
  node-fetch.ts       # NodeHttpAdapter for localhost
  index.ts            # Entry point (if entryPoint: true)
```

### Running the CLI

If `entryPoint: true` is set:

```bash
npx ts-node generated/cli/index.ts
```

Or integrate the command map into your own CLI:

```typescript
import { commands } from './generated/cli/command-map';
import { Inquirerer } from 'inquirerer';

const prompter = new Inquirerer();
await commands.users.list(argv, prompter);
```

### Built-in Infrastructure Commands

The CLI includes infrastructure commands:
- **auth** (or `credentials` if name collides) — manage API credentials stored via appstash
- **context** (or `env` if name collides) — manage endpoint and auth context

## Using Generated ORM

### Create Client

```typescript
import { createClient } from '@/generated/orm';

export const db = createClient({
  endpoint: process.env.GRAPHQL_URL!,
  headers: { Authorization: `Bearer ${process.env.API_TOKEN}` },
});
```

### Query Data

```typescript
const users = await db.user.findMany({
  select: { id: true, name: true, email: true },
  filter: { role: { eq: 'ADMIN' } },
  first: 10,
}).execute().unwrap();
```

### Relations

```typescript
const posts = await db.post.findMany({
  select: {
    id: true,
    title: true,
    author: { select: { id: true, name: true } },
  },
}).execute().unwrap();

// posts[0].author.name is fully typed
```

### Error Handling

```typescript
const result = await db.user.findOne({ id: '123' }).execute();

if (result.ok) {
  console.log(result.value.name);
} else {
  console.error(result.error.message);
}

// Or use helpers
const user = await db.user.findOne({ id }).execute().unwrap(); // throws on error
const user = await db.user.findOne({ id }).execute().unwrapOr(defaultUser);
```

## Schema Sources

The codegen supports 6 schema source modes. The **recommended** approach is schema export + `schemaDir` (see top of this document).

| Priority | Source | Config Key | Best For |
|----------|--------|-----------|----------|
| **1 (recommended)** | Schema directory | `schemaDir: './schemas'` | Deterministic, portable, multi-target |
| 2 | Schema file | `schemaFile: './schema.graphql'` | Single schema, simple projects |
| 3 | PGPM module (path) | `db.pgpm.modulePath` | Schema export from a pgpm module |
| 4 | PGPM workspace | `db.pgpm.workspacePath + moduleName` | Schema export from a pgpm workspace |
| 5 | Database | `db.schemas` or `db.apiNames` | Schema export from a live database |
| 6 | Endpoint | `endpoint` | Schema export from a running server |

### From Schema Directory (recommended)

```bash
npx @constructive-io/graphql-codegen --react-query --orm --schema-dir ./schemas -o ./generated
```

### From Schema File

```bash
npx @constructive-io/graphql-codegen --react-query -s ./schemas/public.graphql -o ./generated
```

### From GraphQL Endpoint

```bash
npx @constructive-io/graphql-codegen --react-query -e https://api.example.com/graphql
```

### From Database

```bash
# Explicit schemas
npx @constructive-io/graphql-codegen --orm --schemas public,app_public

# Auto-discover from API names
npx @constructive-io/graphql-codegen --react-query --api-names my_api
```

### From PGPM Module

```typescript
// In config file — direct path
export default defineConfig({
  db: {
    pgpm: { modulePath: './packages/my-module' },
    schemas: ['public'],
  },
  reactQuery: true,
});

// In config file — workspace + module name
export default defineConfig({
  db: {
    pgpm: {
      workspacePath: '.',
      moduleName: 'my-module',
    },
    schemas: ['app_public'],
  },
  orm: true,
});
```

PGPM module sources create an ephemeral database, deploy the module, introspect the schema via PostGraphile, then tear down the database (unless `keepDb: true` for debugging).

## Schema Export

Schema export (`schemaOnly: true`) fetches a schema from any source and writes it as a `.graphql` SDL file without generating any code. This is the recommended first step in the two-step workflow.

### CLI

```bash
# Export from database
npx @constructive-io/graphql-codegen --schema-only --schemas public --schema-only-output ./schemas --schema-only-filename public.graphql

# Export from endpoint
npx @constructive-io/graphql-codegen --schema-only -e https://api.example.com/graphql --schema-only-output ./schemas

# Export from PGPM module (via config)
npx @constructive-io/graphql-codegen --schema-only -c codegen.config.ts
```

### Programmatic

```typescript
import { generate } from '@constructive-io/graphql-codegen';

const result = await generate({
  db: { schemas: ['public'] },
  schemaOnly: true,
  schemaOnlyOutput: './schemas',
  schemaOnlyFilename: 'public.graphql',
});

console.log(result.message); // "Schema exported to ./schemas/public.graphql"
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `schemaOnly` | Enable schema export mode (no code generation) | `false` |
| `schemaOnlyOutput` | Output directory for the exported schema | Same as `output` |
| `schemaOnlyFilename` | Filename for the exported schema | `schema.graphql` |

## Query Key Factory (React Query)

Generated hooks include a centralized query key factory for type-safe cache management:

```typescript
import { userKeys, invalidate, remove } from '@/generated/hooks';
import { useQueryClient } from '@tanstack/react-query';

const queryClient = useQueryClient();

// Invalidate queries (triggers refetch)
invalidate.user.all(queryClient);        // All user queries
invalidate.user.lists(queryClient);      // All list queries
invalidate.user.detail(queryClient, id); // Specific user

// Remove from cache (for delete operations)
remove.user(queryClient, userId);

// Track in-flight mutations
import { userMutationKeys } from '@/generated/hooks';
import { useIsMutating } from '@tanstack/react-query';

const isMutating = useIsMutating({ mutationKey: userMutationKeys.all });
```

See `references/query-keys.md` for details.

## Filter Syntax

```typescript
// Comparison
filter: { age: { eq: 25 } }
filter: { age: { gte: 18, lt: 65 } }
filter: { status: { in: ['ACTIVE', 'PENDING'] } }

// String
filter: { name: { contains: 'john' } }
filter: { email: { endsWith: '.com' } }

// Logical
filter: {
  OR: [
    { role: { eq: 'ADMIN' } },
    { role: { eq: 'MODERATOR' } },
  ],
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No hooks generated | Add `reactQuery: true` to config  |
| No CLI generated | Add `cli: true` to config |
| Schema not accessible | Verify endpoint URL and auth headers |
| Missing `_meta` query | Ensure PostGraphile v5+ with Meta plugin |
| Type errors after regeneration | Delete output directory and regenerate |
| Import errors | Verify generated code exists and paths match |
| Auth errors at runtime | Check `configure()` headers are set |
| Localhost fetch errors (Node.js) | Enable `nodeHttpAdapter: true` for localhost subdomain resolution |
| No skill files generated | Set `docs: { skills: true }` in config |
| Schema export produces empty file | Verify database/endpoint has tables in the specified schemas |
| `schemaDir` generates nothing | Ensure directory contains `.graphql` files (not `.gql` or other extensions) |

## References

For detailed documentation on specific topics only when needed, see [references/](references/):

- CLI options and configuration: `cli-reference.md`, `config-reference.md`
- Advanced usage patterns: `hooks-patterns.md`, `orm-patterns.md`
- Error handling and relations: `error-handling.md`, `relations.md`
- Query key factory and cache management: `query-keys.md`
- Generated output structure: `hooks-output.md`, `orm-output.md`
