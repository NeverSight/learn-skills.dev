---
name: hyperdrive
description: Connection pooling and caching for PostgreSQL and MySQL databases. Load when connecting Workers to existing Postgres/MySQL, reducing connection overhead, using Drizzle/Prisma with external databases, or migrating traditional database apps to the edge.
---

# Hyperdrive

Accelerate access to existing PostgreSQL and MySQL databases with connection pooling and caching.

## FIRST: Create Hyperdrive Configuration

```bash
# Create a Hyperdrive configuration for your database
npx wrangler hyperdrive create <YOUR_CONFIG_NAME> --connection-string="postgres://user:password@HOSTNAME_OR_IP_ADDRESS:PORT/database_name"

# Copy the ID from the output for your wrangler.jsonc
```

Add the binding to `wrangler.jsonc`:

```jsonc
{
  "hyperdrive": [
    {
      "binding": "HYPERDRIVE",
      "id": "<YOUR_DATABASE_ID>"
    }
  ]
}
```

## When to Use

Use Hyperdrive when:

- **Connecting to existing databases** - PostgreSQL or MySQL hosted anywhere
- **Reducing connection latency** - Connection pooling eliminates per-request connection overhead
- **Geographic distribution** - Cache query results at the edge for read-heavy workloads
- **Database migration** - Connect Workers to traditional databases without rewriting apps
- **Connection limits** - Share connections across many Workers efficiently

## Quick Reference

| Operation | API |
|-----------|-----|
| Get connection string | `env.HYPERDRIVE.connectionString` |
| Connect with Postgres.js | `postgres(env.HYPERDRIVE.connectionString)` |
| Query with Postgres.js | `` await sql`SELECT * FROM users` `` |
| No cleanup needed | Hyperdrive handles connection pooling—don't call `sql.end()` |
| List configs | `npx wrangler hyperdrive list` |
| Get config details | `npx wrangler hyperdrive get <ID>` |
| Update config | `npx wrangler hyperdrive update <ID> --origin-password=<NEW_PASSWORD>` |
| Delete config | `npx wrangler hyperdrive delete <ID>` |

## Connect with Postgres.js

**Install dependencies first:**
```bash
npm install postgres
```

**Code:**

```typescript
import postgres from "postgres";

export interface Env {
  // If you set another name in the Wrangler config file as the value for 'binding',
  // replace "HYPERDRIVE" with the variable name you defined.
  HYPERDRIVE: Hyperdrive;
}

export default {
  async fetch(request, env, ctx): Promise<Response> {
    // Create a database client that connects to your database via Hyperdrive.
    //
    // Hyperdrive generates a unique connection string you can pass to
    // supported drivers, including node-postgres, Postgres.js, and the many
    // ORMs and query builders that use these drivers.
    const sql = postgres(env.HYPERDRIVE.connectionString);

    try {
      // Test query
      const results = await sql`SELECT * FROM pg_tables`;

      // Return result rows as JSON
      return Response.json(results);
    } catch (e) {
      console.error(e);
      return Response.json(
        { error: e instanceof Error ? e.message : e },
        { status: 500 },
      );
    }
  },
} satisfies ExportedHandler<Env>;
```

## Connection Management

**Important:** Do NOT call `sql.end()` or close connections manually.

- Hyperdrive manages connection pooling automatically
- Connections are reused across requests efficiently
- Closing connections can cause errors and reduce performance
- The connection pool persists between Worker invocations

```typescript
// ❌ DON'T DO THIS
const sql = postgres(env.HYPERDRIVE.connectionString);
await sql`SELECT * FROM users`;
await sql.end(); // DON'T close the connection

// ✅ DO THIS INSTEAD
const sql = postgres(env.HYPERDRIVE.connectionString);
await sql`SELECT * FROM users`;
// Let Hyperdrive manage the connection
```

## Supported Drivers

| Driver | Package | Notes |
|--------|---------|-------|
| Postgres.js | `postgres` | **Recommended** - 3.4.5 or later |
| node-postgres | `pg` | Widely used, works well |
| Drizzle ORM | `drizzle-orm` | Use with postgres driver |
| Prisma | `@prisma/client` | Add `?connection_limit=1` to connection string |

See [references/drivers.md](references/drivers.md) for detailed driver integration examples.

## ORM Integration

### Drizzle ORM

```typescript
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

export default {
  async fetch(request, env, ctx): Promise<Response> {
    const client = postgres(env.HYPERDRIVE.connectionString);
    const db = drizzle(client);
    
    const results = await db.select().from(users);
    return Response.json(results);
  }
};
```

### Prisma

**Important:** Add `?connection_limit=1` to prevent connection pool exhaustion:

```typescript
import { PrismaClient } from '@prisma/client';

export default {
  async fetch(request, env, ctx): Promise<Response> {
    // Append connection_limit=1 for Prisma
    const prisma = new PrismaClient({
      datasourceUrl: env.HYPERDRIVE.connectionString + '?connection_limit=1'
    });
    
    const users = await prisma.user.findMany();
    return Response.json(users);
  }
};
```

## MySQL Support

Hyperdrive also supports MySQL databases:

```bash
# Create MySQL Hyperdrive config
npx wrangler hyperdrive create my-mysql \
  --connection-string="mysql://user:password@host:3306/database"
```

```typescript
import { connect } from '@planetscale/database';

export default {
  async fetch(request, env, ctx): Promise<Response> {
    const conn = connect({ url: env.HYPERDRIVE.connectionString });
    const results = await conn.execute('SELECT * FROM users');
    return Response.json(results.rows);
  }
};
```

## Caching Configuration

Hyperdrive automatically caches query results. Configure caching behavior when creating the config:

```bash
# Default: cache enabled with 60s TTL
npx wrangler hyperdrive create my-db \
  --connection-string="postgres://..." \
  --caching-disabled=false \
  --max-age=60
```

**Caching behavior:**
- Only **read queries** (SELECT) are cached
- Write queries (INSERT, UPDATE, DELETE) are never cached
- Cache is automatically invalidated when writes occur to the same table

## Detailed References

- **[references/setup.md](references/setup.md)** - Creating configs, connection strings, security
- **[references/drivers.md](references/drivers.md)** - Driver-specific patterns, ORMs, troubleshooting
- **[references/testing.md](references/testing.md)** - Local PostgreSQL setup, Vitest integration, testing with real databases

## Best Practices

1. **Use Postgres.js 3.4.5+** - Best compatibility and performance with Hyperdrive
2. **Never call sql.end()** - Hyperdrive manages connection lifecycle
3. **One config per database** - Reuse the same Hyperdrive binding across Workers
4. **Use Prisma carefully** - Always add `?connection_limit=1` to the connection string
5. **Test locally with wrangler dev** - Use `--remote` flag to connect through Hyperdrive
6. **Store credentials securely** - Never commit connection strings; use environment variables
7. **Monitor with observability** - Enable in `wrangler.jsonc` to track query performance
8. **Connection string format** - Use standard Postgres/MySQL connection string format

## Troubleshooting

**Connection errors:**
- Verify your database allows connections from Cloudflare IPs
- Check firewall rules and security groups
- Test connection string format (must be valid Postgres/MySQL URL)

**Prisma connection pool errors:**
- Add `?connection_limit=1` to the connection string
- Ensure Prisma client is initialized once per request, not globally

**"Too many connections" errors:**
- Your origin database may have reached its connection limit
- Increase max connections on your database server
- Hyperdrive already pools connections efficiently

**Local development:**
```bash
# Use --remote to test with actual Hyperdrive
npx wrangler dev --remote

# Or use local connection string for development
# (add to .dev.vars)
HYPERDRIVE_CONNECTION_STRING=postgres://localhost:5432/mydb
```
