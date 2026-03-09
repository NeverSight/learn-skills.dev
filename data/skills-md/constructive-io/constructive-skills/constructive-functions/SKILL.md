---
name: constructive-functions
description: Build and deploy Knative-style HTTP cloud functions for the Constructive platform. Use when creating serverless functions for Constructive (email, webhooks, background jobs), building functions that interact with the Constructive GraphQL API, or running PGPM commands programmatically.
---

Build and deploy Knative-style HTTP cloud functions for the Constructive platform.

## When to Apply

Use this skill when:
- Creating serverless functions for Constructive (email, webhooks, background jobs)
- Building functions that interact with the Constructive GraphQL API
- Running PGPM commands programmatically in cloud functions
- Executing SQL scripts or database operations as cloud functions

## Architecture Overview

Constructive functions are TypeScript HTTP handlers deployed as Knative services on Kubernetes. Each function:
- Exports a default async handler receiving `(params, context)`
- Runs on port 8080 (Knative default)
- Gets a GraphQL client via `context.client` for database access
- Builds to `dist/` and runs via a shared Node.js runner

## Project Structure

```
constructive-functions/
  functions/
    my-function/
      src/
        index.ts          # Handler implementation
      __tests__/
        index.test.ts     # Tests
      package.json
      tsconfig.json
      Dockerfile          # Optional, for custom images
  _runtimes/
    node/
      runner.js           # Shared HTTP server wrapper
  k8s/
    base/                 # Base K8s manifests
    overlays/
      local/              # Local development overlay
      dev/                # Dev cluster overlay
  pnpm-workspace.yaml
  Makefile
```

## Function Handler Pattern

Every function exports a default async handler:

```typescript
import { createClient } from './generated/orm';

export default async (params: any, context: any) => {
  const db = createClient({
    endpoint: process.env.GRAPHQL_ENDPOINT || 'http://constructive-server:3000/graphql',
    headers: context.headers,
  });

  // Type-safe query using generated ORM client
  const result = await db.user
    .findMany({
      select: { id: true, username: true },
      first: 10,
    })
    .execute();

  if (!result.ok) {
    return { error: 'Query failed', details: result.errors };
  }

  return { success: true, users: result.data.users.nodes };
};
```

The `context` object provides:
- `client` — Legacy GraphQL client (prefer using generated ORM client instead)
- `headers` — Request headers from the incoming HTTP request

**Important:** Use the typed SDK from `@constructive-io/graphql-codegen` instead of raw gql strings. See the `graphql-codegen` skill for setup.

## Creating a New Function

1. Create the function directory:

```bash
mkdir -p functions/my-function/src
mkdir -p functions/my-function/__tests__
```

2. Create `functions/my-function/package.json`:

```json
{
  "name": "@constructive-io/my-function-fn",
  "version": "0.1.0",
  "description": "My Knative function",
  "author": "Constructive <developers@constructive.io>",
  "private": false,
  "main": "index.js",
  "module": "esm/index.js",
  "types": "index.d.ts",
  "publishConfig": {
    "access": "public",
    "directory": "dist"
  },
  "files": ["dist"],
  "scripts": {
    "copy": "makage assets",
    "clean": "makage clean",
    "prepublishOnly": "npm run build",
    "build": "makage build",
    "test": "jest --forceExit __tests__/index.test.ts",
    "start": "node ../../_runtimes/node/runner.js dist/index.js"
  },
  "dependencies": {
    "@constructive-io/knative-job-fn": "latest",
    "@pgpmjs/env": "latest",
    "graphql-tag": "^2.12.6",
    "cross-fetch": "^4.0.0",
    "graphql-request": "^6.1.0"
  },
  "devDependencies": {
    "@types/node": "latest",
    "@types/jest": "latest",
    "jest": "latest",
    "makage": "0.1.10",
    "ts-jest": "latest",
    "typescript": "latest",
    "pgsql-test": "latest"
  }
}
```

**Critical fields for publishing:**
- `publishConfig.directory: "dist"` — Publish from dist folder (prevents tree-shaking into weird paths)
- `main: "index.js"` — Points to CJS build (in dist)
- `module: "esm/index.js"` — Points to ESM build (in dist)
- `types: "index.d.ts"` — Points to type declarations (in dist)

3. Create `functions/my-function/tsconfig.json`:

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "__tests__"]
}
```

4. Create `functions/my-function/src/index.ts`:

```typescript
import { parseEnvBoolean } from '@pgpmjs/env';

const isDryRun = parseEnvBoolean(process.env.MY_FUNCTION_DRY_RUN) ?? false;

export default async (params: any, context: any) => {
  const { client } = context;
  console.log('[my-function] processing request');

  if (isDryRun) {
    console.log('[my-function] DRY RUN', params);
    return { dryRun: true, params };
  }

  // Your function logic here
  return { success: true };
};
```

## Using PGPM in Functions

Functions can use the `pgpm` library to run PGPM commands programmatically:

```typescript
import { dump } from 'pgpm';

export default async (params: any, context: any) => {
  const argv = {
    _: [],
    database: params.database,
    out: params.out,
    'database-id': params.database_id
  };

  const prompter = {
    prompt: () => { throw new Error('Interactive prompt not supported'); }
  };

  await dump(argv, prompter, {});
  
  return { message: 'PGPM dump completed', args: argv };
};
```

## Direct Database Access

For SQL execution, use `pg-cache` for connection pool management. It provides automatic caching, cleanup callbacks, and graceful shutdown handling:

```typescript
import { getPgPool, close } from 'pg-cache';

export default async (params: any, context: any) => {
  const { query } = params;
  
  if (!query) {
    return { error: 'Missing "query" in payload' };
  }

  // Get or create a cached pool (automatically reused across requests)
  const pool = getPgPool({
    host: process.env.PGHOST,
    port: Number(process.env.PGPORT || 5432),
    database: process.env.PGDATABASE || 'launchql',
    user: process.env.PGUSER,
    password: process.env.PGPASSWORD,
  });

  const result = await pool.query(query);
  return { rowCount: result.rowCount, rows: result.rows };
  
  // Note: No manual cleanup needed - pg-cache handles pool lifecycle
};
```

**Why pg-cache?**
- **Automatic pool caching** — Pools are reused across function invocations
- **Graceful shutdown** — Handles idle connection errors during cleanup
- **LRU eviction** — Automatically disposes unused pools
- **Cleanup callbacks** — Register callbacks for resource cleanup when pools are disposed

For graceful shutdown in long-running processes:

```typescript
import { close } from 'pg-cache';

process.on('SIGTERM', async () => {
  await close();  // Gracefully close all cached pools
  process.exit(0);
});
```

## Build Workflow

Functions use makage for builds, which handles TypeScript compilation and asset copying:

```bash
# Install dependencies
pnpm install

# Build all functions (from workspace root)
pnpm -r run build

# Build a specific function
cd functions/my-function
pnpm build

# Clean build artifacts
pnpm clean
```

### Build Output Structure

After `makage build`:

```text
my-function/
├── src/
│   └── index.ts
├── dist/
│   ├── index.js          # CJS build
│   ├── index.d.ts        # Type declarations
│   ├── esm/
│   │   └── index.js      # ESM build
│   ├── package.json      # Copied from root
│   ├── README.md         # Copied from root
│   └── LICENSE           # Copied from root
└── package.json
```

## Local Development

Run functions locally:

```bash
# Run a specific function locally
cd functions/my-function
pnpm start
# Function listens on http://localhost:8080

# Test with curl
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

## Publishing Functions to npm

Functions follow the same publishing workflow as other PNPM packages. See the `pnpm-publishing` skill for full details.

### Quick Publishing Workflow

```bash
# 1. Build all functions
pnpm -r run build

# 2. Run tests
pnpm -r run test

# 3. Version (interactive)
pnpm lerna version

# 4. Publish to npm
pnpm lerna publish from-package
```

### Dry Run

Test publishing without making changes:

```bash
# Test versioning
pnpm lerna version --no-git-tag-version --no-push

# Test publishing
pnpm lerna publish from-package --dry-run
```

## Docker Build

Build Docker images for deployment:

```bash
# Build all function images
make docker-build

# Build a specific function
docker build -t ghcr.io/constructive-io/constructive-functions/my-function:latest functions/my-function

# Push to registry
docker push ghcr.io/constructive-io/constructive-functions/my-function:latest
```

## Dockerfile Pattern

```dockerfile
FROM node:22-alpine

WORKDIR /usr/src/app

COPY package.json ./

RUN npm install -g pnpm@10.12.2 && pnpm install --prod

COPY dist ./dist

ENV NODE_ENV=production
ENV PORT=8080

USER node

CMD ["node", "dist/index.js"]
```

## Kubernetes Deployment

### Local Development with Kind/Minikube

```bash
cd k8s

# Install Knative Serving + Kourier
make operators-knative-only

# Apply local overlay (Postgres, MinIO, functions)
make kustomize-local

# Port-forward to services
make proxy-server   # GraphQL API -> localhost:8080
make proxy-web      # Dashboard UI -> localhost:3000
```

### Knative Service Manifest

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-function
  namespace: interweb
spec:
  template:
    spec:
      containers:
        - image: ghcr.io/constructive-io/constructive-functions/my-function:latest
          ports:
            - containerPort: 8080
          env:
            - name: MY_FUNCTION_DRY_RUN
              value: "false"
            - name: GRAPHQL_ENDPOINT
              value: "http://constructive-server:3000/graphql"
```

## Environment Variables

Common environment variables for functions:

| Variable | Description |
|----------|-------------|
| `PORT` | HTTP port (default: 8080) |
| `GRAPHQL_ENDPOINT` | GraphQL API URL |
| `PGHOST` | PostgreSQL host |
| `PGPORT` | PostgreSQL port |
| `PGUSER` | PostgreSQL user |
| `PGPASSWORD` | PostgreSQL password |
| `PGDATABASE` | PostgreSQL database |
| `*_DRY_RUN` | Enable dry-run mode (per function) |

## Testing Functions

```typescript
// __tests__/index.test.ts
import handler from '../src/index';

describe('my-function', () => {
  const mockClient = {
    request: jest.fn()
  };

  it('should process request', async () => {
    const params = { key: 'value' };
    const context = { client: mockClient };

    const result = await handler(params, context);

    expect(result.success).toBe(true);
  });
});
```

Run tests:

```bash
cd functions/my-function
pnpm test
```

## Error Handling

Return errors as JSON with appropriate status codes:

```typescript
export default async (params: any, context: any) => {
  const { requiredField } = params;

  // 400 Bad Request - missing required field
  if (!requiredField) {
    return { error: 'Missing required field' };
  }

  try {
    // Function logic
    return { success: true };
  } catch (e: any) {
    // 500 Internal Server Error
    console.error('Function failed:', e);
    return { error: e.message };
  }
};
```

The runner automatically maps certain error messages to 400 status codes:
- "Missing prompt"
- "Missing required field"
- "Missing \"query\" in payload"

All other errors return 500.

## Best Practices

1. **Use typed SDK** — Use `@constructive-io/graphql-codegen` ORM client instead of raw gql strings
2. **Use pg-cache** — Use `pg-cache` for database connections instead of manual Pool management
3. **Use makage for builds** — Consistent build tooling across all packages
4. **Publish from dist/** — Prevents tree-shaking into weird import paths
5. **Use dry-run mode** — Support `*_DRY_RUN` env var for testing without side effects
6. **Log context** — Log request details for debugging (but not sensitive data)
7. **Handle errors** — Use discriminated unions (`.execute()`) for explicit error handling
8. **Validate input** — Check required fields early and return clear error messages
9. **Use @pgpmjs/env** — Parse boolean env vars consistently with `parseEnvBoolean()`

## References

- Related skill: `graphql-codegen` for typed GraphQL SDK generation
- Related skill: `pnpm-publishing` for full npm publishing workflow
- Related skill: `pnpm-workspace` for workspace setup
- [constructive-functions repo](https://github.com/constructive-io/constructive-functions)
- [Knative Serving docs](https://knative.dev/docs/serving/)
- [@constructive-io/knative-job-fn](https://www.npmjs.com/package/@constructive-io/knative-job-fn)
- [pg-cache on npm](https://www.npmjs.com/package/pg-cache)
- [makage on npm](https://www.npmjs.com/package/makage)
