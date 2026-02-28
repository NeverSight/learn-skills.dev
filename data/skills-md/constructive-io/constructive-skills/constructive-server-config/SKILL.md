---
name: constructive-server-config
description: Configure and run the Constructive GraphQL server (cnc server), GraphiQL explorer (cnc explorer), and code generation (cnc codegen). Use when asked to "start the server", "run cnc server", "start GraphQL API", "run GraphiQL", "configure API routing", "generate types", or when working with the Constructive CLI and PostGraphile.
compatibility: Node.js 22+, PostgreSQL 17+, PostGraphile v5+, @constructive-io/cli 7.1.3+
metadata:
  author: constructive-io
---

# Constructive Server Configuration

How to run and configure the Constructive GraphQL API server, explorer, and codegen tools. The server exposes a multi-target GraphQL API with subdomain-based routing.

## When to Apply

Use this skill when:
- Starting the Constructive GraphQL server (`cnc server`)
- Opening the GraphiQL explorer (`cnc explorer`)
- Running code generation (`cnc codegen`)
- Configuring API routing (header-based vs domain-based)
- Running the server in CI for integration tests
- Understanding the schema → PostGraphile → GraphQL pipeline

## Prerequisites

- PostgreSQL 17+ running with a deployed Constructive database (see `pgpm-docker` and `pgpm-env` skills)
- `@constructive-io/cli` installed (`npm install -g @constructive-io/cli` or available from the monorepo)
- Database users bootstrapped via `pgpm admin-users bootstrap --yes`

## The Constructive CLI (`cnc`)

The Constructive CLI (`cnc` or `constructive`) is the main entry point for running the platform.

### Core Commands

| Command | Purpose |
|---------|---------|
| `cnc server` | Start the GraphQL API server |
| `cnc explorer` | Start the GraphiQL explorer UI |
| `cnc codegen` | Generate TypeScript types and SDK from the running API |

## Starting the Server

### Quick Start

```bash
# Start with defaults
cnc server

# Start on a specific port with a specific database
PGDATABASE=constructive cnc server --port 5555

# Start with CORS wildcard (required for non-interactive / CI)
cnc server --origin '*'

# Start with explicit host, port, and origin
cnc server --host 0.0.0.0 --port 3000 --origin "*"
```

**Important:** The `--origin` option has **no default**. If omitted, the server will prompt interactively. Always pass `--origin` explicitly for non-interactive use (CI, Docker, scripts).

### Server Options

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Bind address | `localhost` |
| `--port` | Listen port | `5555` |
| `--origin` | CORS allowed origin | (interactive prompt) |
| `--database` | Database name (or set `PGDATABASE`) | (interactive prompt) |
| `--simpleInflection` | Use simple inflection | `true` |
| `--oppositeBaseNames` | Use opposite base names | `false` |
| `--postgis` | Enable PostGIS extension | `true` |
| `--servicesApi` | Enable Services API routing | `true` |
| `--cwd` | Working directory | current directory |

### Environment Variables

The server reads its configuration from environment variables. Set these before starting:

> **Prerequisite:** Ensure PG env vars are loaded (see `pgpm-env` skill) before starting the server.

```bash
# Required
export PGDATABASE=constructive

# API configuration
export API_IS_PUBLIC=true          # or false for admin mode
export API_EXPOSED_SCHEMAS=metaschema_public,services_public
export API_ANON_ROLE=anonymous     # Role for unauthenticated requests
export API_ROLE_NAME=authenticated # Role for authenticated requests
```

| Variable | Default | Description |
|----------|---------|-------------|
| `PGHOST` | `localhost` | PostgreSQL host |
| `PGPORT` | `5432` | PostgreSQL port |
| `PGUSER` | `postgres` | PostgreSQL user |
| `PGPASSWORD` | (none) | PostgreSQL password |
| `PGDATABASE` | (prompt) | Database name |
| `API_IS_PUBLIC` | — | `true` for public API, `false` for admin |
| `API_EXPOSED_SCHEMAS` | — | Comma-separated schemas to expose |
| `API_ANON_ROLE` | — | Role for unauthenticated requests |
| `API_ROLE_NAME` | — | Role for authenticated requests |
| `API_ENABLE_SERVICES` | — | Enable services schema (admin only) |
| `API_META_SCHEMAS` | — | Meta schemas for routing |
| `NODE_ENV` | `development` | Environment (affects CORS warnings) |

## Endpoints

The server uses subdomain-based routing via the `Host` header. For local development, `*.localhost` resolves to `127.0.0.1` automatically.

| Target | Endpoint | Description |
|--------|----------|-------------|
| Public | `http://api.localhost:<port>/graphql` | Public API (databases, tables, fields, schemas) |
| Auth | `http://auth.localhost:<port>/graphql` | Authentication (sign-up, sign-in, tokens) |
| Objects | `http://objects.localhost:<port>/graphql` | Object store (blobs, trees, commits) |
| Admin | `http://admin.localhost:<port>/graphql` | Admin operations |

Health check: `GET /healthz`

## API Routing Modes

### Public Mode (`API_IS_PUBLIC=true`)

Uses **domain-based routing**. Each site/app gets its own subdomain:

```
https://myapp.example.com/graphql → routes to myapp's schemas
```

- Used for external-facing APIs
- `API_ANON_ROLE=anonymous` — unauthenticated users get minimal access
- `API_ROLE_NAME=authenticated` — authenticated users get full access per RLS

### Admin Mode (`API_IS_PUBLIC=false`)

Uses **header-based routing**. The client sends headers to select the target:

```
X-Api-Name: my_api
X-Database-Id: <uuid>
X-Meta-Schema: metaschema_public
```

- Used for the Constructive admin UI
- `API_ANON_ROLE=administrator` — admin users get full schema access
- `API_ENABLE_SERVICES=true` — exposes the services schema for site/API management

### Services API mode

When `--servicesApi` is `true` (default), the server enables the Constructive services routing layer, which routes requests based on the `Host` header subdomain to the correct schema/role combination. When `false`, it falls back to exposing raw PostgreSQL schemas.

## GraphiQL Explorer

```bash
cnc explorer
```

Opens an interactive GraphiQL interface in the browser for testing queries against the running server. Useful for:
- Exploring the generated schema
- Testing queries and mutations
- Debugging authentication and RLS policies

## Code Generation

### Using cnc codegen

```bash
cnc codegen
```

Generates TypeScript types and SDK code from the running GraphQL server. This is a convenience wrapper around `@constructive-io/graphql-codegen`.

### Using graphql-codegen directly

For more control, use the codegen package directly:

```bash
npx @constructive-io/graphql-codegen --react-query --orm -e http://localhost:5555/graphql -o ./generated
```

See the `constructive-graphql-codegen` skill for full codegen documentation.

## The Schema → GraphQL Pipeline

Understanding how database schemas become a GraphQL API:

```
PostgreSQL schemas (app_public, etc.)
        ↓
    PostGraphile v5 introspection
        ↓
    GraphQL schema (auto-generated)
        ↓
    cnc server (serves the API)
        ↓
    graphql-codegen (generates typed client)
        ↓
    React Query hooks / ORM / CLI
```

### Key Concepts

1. **Schemas are the source of truth** — tables, functions, views, and RLS policies in PostgreSQL define the API surface
2. **PostGraphile introspects automatically** — no manual schema writing needed
3. **Smart naming** — PostGraphile converts `snake_case` SQL to `camelCase` GraphQL automatically
4. **RLS is the auth layer** — Row-Level Security policies in Postgres control what each user can access via GraphQL

## Exposed Schemas

The `API_EXPOSED_SCHEMAS` variable controls which PostgreSQL schemas are exposed via GraphQL:

| Schema | Purpose |
|--------|---------|
| `metaschema_public` | Database metadata (tables, fields, constraints, etc.) |
| `services_public` | Service management (sites, APIs, domains, etc.) |
| `constructive_auth_public` | Authentication (login, register, tokens) |
| `app_public` (custom) | Application-specific tables and functions |

### Meta Schemas

`API_META_SCHEMAS` lists schemas used for schema validation and X-Meta-Schema routing:

```
API_META_SCHEMAS=metaschema_public,services_public,metaschema_modules_public,constructive_auth_public
```

## Common Workflows

### Start local dev server

> Ensure PG env vars are loaded (see `pgpm-env` skill).

```bash
export PGDATABASE=constructive
cnc server --port 5555 --origin "*"
```

### Verify the server is running

```bash
curl -s http://api.localhost:5555/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{ __typename }"}' | jq
```

Expected response:
```json
{
  "data": {
    "__typename": "Query"
  }
}
```

### Explore the API

```bash
# In another terminal
cnc explorer
```

### Generate SDK from running server

```bash
npx @constructive-io/graphql-codegen \
  --react-query --orm \
  -e http://localhost:5555/graphql \
  -o ./src/generated
```

### Use with the generated CLI

```bash
cd sdk/constructive-cli

# Create context pointing to local server
npx tsx cli/index.ts context create local \
  --publicEndpoint http://api.localhost:5555/graphql \
  --authEndpoint http://auth.localhost:5555/graphql \
  --objectsEndpoint http://objects.localhost:5555/graphql \
  --adminEndpoint http://admin.localhost:5555/graphql

npx tsx cli/index.ts context use local
```

### Run admin and public servers together

```bash
# Terminal 1 — Admin server
API_IS_PUBLIC=false API_ENABLE_SERVICES=true \
  cnc server --port 3002 --origin "*"

# Terminal 2 — Public server
API_IS_PUBLIC=true \
  cnc server --port 3000 --origin "*"
```

### CI / GitHub Actions

> See `github-workflows-pgpm` for full CI patterns.

```yaml
- name: Start cnc server
  run: |
    PGDATABASE=constructive cnc server --port 5555 --origin '*' &
    # Wait for server readiness
    for i in $(seq 1 30); do
      if curl -sf http://api.localhost:5555/graphql \
        -H 'Content-Type: application/json' \
        -d '{"query":"{ __typename }"}' > /dev/null 2>&1; then
        echo "Server is ready!"
        break
      fi
      if [ "$i" -eq 30 ]; then
        echo "Server failed to start after 30 seconds"
        exit 1
      fi
      sleep 1
    done
```

## Server Architecture

The `cnc server` command:
1. Reads `PGDATABASE` or prompts for database selection
2. Collects configuration options (inflection, PostGIS, CORS, etc.)
3. Calls `GraphQLServer()` from `@constructive-io/graphql-server`
4. Starts an Express server with middleware for:
   - Subdomain-based API routing (`@constructive-io/url-domains`)
   - JWT authentication
   - PostGraphile GraphQL engine
   - CORS handling (per-API or fallback)
   - Health check endpoint at `/healthz`
5. Listens for PostgreSQL `schema:update` notifications to auto-flush caches

**Source code:**
- `constructive/packages/cli/src/commands/server.ts` — CLI command handler
- `constructive/graphql/server/src/server.ts` — `GraphQLServer` class and factory

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Server hangs on start | Missing `--origin` flag | Add `--origin "*"` for non-interactive mode |
| Port already in use | Another instance running | `lsof -ti:5555 \| xargs kill -9` |
| No schemas exposed | `API_EXPOSED_SCHEMAS` not set | Set the env var with comma-separated schema names |
| Auth errors | Wrong role configuration | Check `API_ANON_ROLE` and `API_ROLE_NAME` |
| Can't connect to DB | PG env vars not loaded | See `pgpm-env` skill for loading database connection variables |
| Endpoints return 404 | Database not deployed | Deploy with `pgpm deploy --createdb --workspace --all --yes` |
| GraphiQL shows empty schema | Server not running or wrong port | Verify server is up and explorer points to correct URL |
| Subdomain routing not working | DNS issue | `*.localhost` should resolve automatically; if not, add to `/etc/hosts` |
| CORS errors in browser | Wrong origin | Pass `--origin 'http://localhost:3000'` or `--origin '*'` |

## References

- Related skill: `pgpm-docker` for PostgreSQL container management
- Related skill: `pgpm-env` for environment variable setup
- Related skill: `constructive-graphql-codegen` for generating CLI from schema
- Related skill: `constructive-deployment` for Docker Compose and production deployment
