---
name: cloudflare-opennext
description: Deploy Next.js to Cloudflare Workers with full App Router, Pages Router, ISR, and SSG support. Load when creating Next.js projects for Workers, migrating from Vercel/next-on-pages, configuring caching (R2/KV/D1), accessing Cloudflare bindings via getCloudflareContext, or fixing bundle size issues.
---

# Cloudflare OpenNext

Deploy Next.js applications to Cloudflare Workers using the `@opennextjs/cloudflare` adapter with full support for App Router, Pages Router, ISR, SSG, and Cloudflare bindings.

## When to Use

- Creating new Next.js apps for Cloudflare Workers
- Migrating existing Next.js apps to Cloudflare
- Configuring ISR/SSG caching with R2, KV, or D1
- Accessing Cloudflare bindings (KV, R2, D1, Durable Objects, AI)
- Using databases and ORMs (Drizzle, Prisma) in Next.js
- Troubleshooting deployment issues or bundle size problems

## Getting Started

### New App

```bash
npm create cloudflare@latest -- my-next-app --framework=next --platform=workers
cd my-next-app
npm run dev      # Local development with Next.js
npm run preview  # Preview in Workers runtime
npm run deploy   # Deploy to Cloudflare
```

### Existing App Migration

```bash
# 1. Install dependencies
npm install @opennextjs/cloudflare@latest
npm install --save-dev wrangler@latest

# 2. Create wrangler.jsonc (see Configuration section)
# 3. Create open-next.config.ts
# 4. Update next.config.ts
# 5. Add scripts to package.json
# 6. Deploy
npm run deploy
```

## Core Concepts

### How OpenNext Works

The `@opennextjs/cloudflare` adapter:
1. Runs `next build` to generate the Next.js build output
2. Transforms the build output to work in Cloudflare Workers runtime
3. Outputs to `.open-next/` directory with `worker.js` entry point
4. Uses Workers Static Assets for static files (`_next/static`, `public`)

### Node.js Runtime (Not Edge)

**Critical**: OpenNext uses Next.js **Node.js runtime**, NOT the Edge runtime:

```typescript
// ❌ Remove this - Edge runtime not supported
export const runtime = "edge";

// ✅ Default Node.js runtime - fully supported
// No export needed, this is the default
```

The Node.js runtime provides:
- Full Node.js API compatibility via `nodejs_compat` flag
- More Next.js features than Edge runtime
- Access to all Cloudflare bindings

## Configuration Files

### wrangler.jsonc

Minimal configuration for OpenNext:

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-nextjs-app",
  "main": ".open-next/worker.js",
  "compatibility_date": "2024-12-30",
  "compatibility_flags": [
    "nodejs_compat",                    // Required for Node.js APIs
    "global_fetch_strictly_public"      // Security: prevent local IP fetches
  ],
  "assets": {
    "directory": ".open-next/assets",   // Static files
    "binding": "ASSETS"
  },
  "services": [
    {
      "binding": "WORKER_SELF_REFERENCE",
      "service": "my-nextjs-app"        // Must match "name" above
    }
  ],
  "images": {
    "binding": "IMAGES"                 // Optional: Enable image optimization
  }
}
```

**Required settings**:
- `nodejs_compat` compatibility flag
- `compatibility_date` >= `2024-09-23`
- `WORKER_SELF_REFERENCE` service binding (must match worker name)
- `main` and `assets` paths should not be changed

See [references/configuration.md](references/configuration.md) for complete configuration with R2, KV, D1 bindings.

### open-next.config.ts

Configure caching and OpenNext behavior:

```typescript
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";

export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
});
```

This file is auto-generated if not present. See [references/caching.md](references/caching.md) for cache options.

### next.config.ts

Initialize OpenNext for local development:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Your Next.js configuration
};

export default nextConfig;

// Enable bindings access during `next dev`
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
initOpenNextCloudflareForDev();
```

### .dev.vars

Environment variables for local development:

```bash
# .dev.vars
NEXTJS_ENV=development
```

The `NEXTJS_ENV` variable selects which Next.js `.env` file to load:
- `development` → `.env.development`
- `production` → `.env.production` (default)

## Accessing Cloudflare Bindings

Use `getCloudflareContext()` to access bindings in any route:

```typescript
import { getCloudflareContext } from "@opennextjs/cloudflare";

// Route Handler (App Router)
export async function GET(request: Request) {
  const { env, cf, ctx } = getCloudflareContext();
  
  // Access KV
  const value = await env.MY_KV.get("key");
  
  // Access R2
  const object = await env.MY_BUCKET.get("file.txt");
  
  // Access D1
  const result = await env.DB.prepare("SELECT * FROM users").all();
  
  // Access Durable Objects
  const stub = env.MY_DO.idFromName("instance-1");
  const doResponse = await stub.fetch(request);
  
  // Access request info
  const country = cf?.country;
  
  // Background tasks
  ctx.waitUntil(logAnalytics());
  
  return Response.json({ value });
}

// API Route (Pages Router)
export default async function handler(req, res) {
  const { env } = getCloudflareContext();
  const data = await env.MY_KV.get("key");
  res.json({ data });
}

// Server Component
export default async function Page() {
  const { env } = getCloudflareContext();
  const data = await env.MY_KV.get("key");
  return <div>{data}</div>;
}
```

### SSG Routes with Async Context

For Static Site Generation routes, use async mode:

```typescript
// In SSG route (generateStaticParams, etc.)
const { env } = await getCloudflareContext({ async: true });
const products = await env.DB.prepare("SELECT * FROM products").all();
```

**Warning**: During SSG, secrets from `.dev.vars` and local binding values are included in the static build. Be careful with sensitive data.

### TypeScript Types

Generate types for your bindings:

```bash
npx wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts
```

Add to `package.json`:

```json
{
  "scripts": {
    "cf-typegen": "wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts"
  }
}
```

Run after any binding changes in `wrangler.jsonc`.

## CLI Commands

The `opennextjs-cloudflare` CLI wraps Wrangler with OpenNext-specific behavior:

```bash
# Build the Next.js app and transform for Workers
npx opennextjs-cloudflare build

# Build and preview locally with Wrangler
npm run preview
# or
npx opennextjs-cloudflare preview

# Build and deploy to Cloudflare
npm run deploy
# or
npx opennextjs-cloudflare deploy

# Build and upload as a version (doesn't deploy)
npm run upload
# or
npx opennextjs-cloudflare upload

# Populate cache (called automatically by preview/deploy/upload)
npx opennextjs-cloudflare populateCache local   # Local bindings
npx opennextjs-cloudflare populateCache remote  # Remote bindings
```

**Recommended package.json scripts**:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "preview": "opennextjs-cloudflare build && opennextjs-cloudflare preview",
    "deploy": "opennextjs-cloudflare build && opennextjs-cloudflare deploy",
    "upload": "opennextjs-cloudflare build && opennextjs-cloudflare upload",
    "cf-typegen": "wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts"
  }
}
```

## Caching Strategies

OpenNext supports Next.js caching with Cloudflare storage:

| Cache Type | Use Case | Storage Options |
|------------|----------|-----------------|
| **Incremental Cache** | ISR/SSG page data | R2, KV, Static Assets |
| **Queue** | Time-based revalidation | Durable Objects, Memory |
| **Tag Cache** | On-demand revalidation | D1, Durable Objects |

**Quick setup examples:**

```typescript
// Static Site (SSG only)
import staticAssetsCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";
export default defineCloudflareConfig({
  incrementalCache: staticAssetsCache,
  enableCacheInterception: true,
});

// Small Site with ISR
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";
export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
  queue: doQueue,
  tagCache: d1NextTagCache,
});
```

See [references/caching.md](references/caching.md) for complete caching patterns including regional cache and sharded tag cache

## Image Optimization

Enable Cloudflare Images for automatic image optimization:

```jsonc
// wrangler.jsonc
{
  "images": {
    "binding": "IMAGES"
  }
}
```

Next.js `<Image>` components will automatically use Cloudflare Images. Additional costs apply.

**Compatibility notes**:
- Supports: PNG, JPEG, WEBP, AVIF, GIF, SVG
- `minimumCacheTTL` not supported
- `dangerouslyAllowLocalIP` not supported

## Database and ORM Patterns

**Critical Rule**: Never create global database clients in Workers. Create per-request:

```typescript
// ❌ WRONG - Global client causes I/O errors
import { Pool } from "pg";
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// ✅ CORRECT - Per-request client
import { cache } from "react";
import { Pool } from "pg";

export const getDb = cache(() => {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    maxUses: 1,  // Don't reuse connections across requests
  });
  return drizzle({ client: pool, schema });
});

// Usage in route
export async function GET() {
  const db = getDb();
  const users = await db.select().from(usersTable);
  return Response.json(users);
}
```

See [references/database-orm.md](references/database-orm.md) for Drizzle and Prisma patterns.

## Critical Rules

### ✅ DO

1. **Use Node.js runtime** - Default runtime, remove any `export const runtime = "edge"`
2. **Create DB clients per-request** - Use React's `cache()` for request-scoped instances
3. **Enable nodejs_compat** - Required compatibility flag with date >= 2024-09-23
4. **Use getCloudflareContext()** - Access bindings, not getRequestContext from next-on-pages
5. **Add .open-next to .gitignore** - Build output should not be committed
6. **Use wrangler.jsonc** - Not wrangler.toml (JSONC supports comments and validation)
7. **Set WORKER_SELF_REFERENCE** - Service binding must match worker name
8. **Add public/_headers** - Configure static asset caching headers

### ❌ DON'T

1. **Don't use Edge runtime** - Remove `export const runtime = "edge"` from all routes
2. **Don't use Turbopack** - Use `next build`, not `next build --turbo`
3. **Don't create global DB clients** - Causes "Cannot perform I/O" errors
4. **Don't exceed 10 MiB** - Worker size limit (3 MiB on free plan)
5. **Don't use next-on-pages** - Different adapter, use @opennextjs/cloudflare instead
6. **Don't commit .open-next/** - Build output directory
7. **Don't use Node Middleware** - Not supported (Next.js 15.2+ feature)

## Supported Features

| Feature | Support | Notes |
|---------|---------|-------|
| **App Router** | ✅ Full | All features supported |
| **Pages Router** | ✅ Full | Including API routes |
| **Route Handlers** | ✅ Full | GET, POST, etc. |
| **Dynamic Routes** | ✅ Full | `[slug]`, `[...slug]` |
| **SSG** | ✅ Full | Static Site Generation |
| **SSR** | ✅ Full | Server-Side Rendering |
| **ISR** | ✅ Full | Incremental Static Regeneration |
| **PPR** | ✅ Full | Partial Prerendering |
| **Middleware** | ✅ Partial | Standard middleware works, Node Middleware (15.2+) not supported |
| **Image Optimization** | ✅ Full | Via Cloudflare Images binding |
| **Composable Caching** | ✅ Full | `'use cache'` directive |
| **next/font** | ✅ Full | Font optimization |
| **after()** | ✅ Full | Background tasks |
| **Turbopack** | ❌ No | Use standard build |

**Supported Next.js versions**:
- Next.js 15: All minor and patch versions
- Next.js 14: Latest minor version only

## Development Workflow

```bash
# Local development with Next.js dev server
npm run dev

# Preview in Workers runtime (faster than deploy)
npm run preview

# Deploy to production
npm run deploy

# Update TypeScript types after binding changes
npm run cf-typegen
```

**Local Development Notes**:
- `next dev` - Uses Node.js runtime, bindings available via `initOpenNextCloudflareForDev()`
- `npm run preview` - Uses Workers runtime with Wrangler, closer to production
- Both support hot reloading

## Detailed References

- **[references/configuration.md](references/configuration.md)** - Complete wrangler.jsonc, environment variables, TypeScript types
- **[references/caching.md](references/caching.md)** - ISR, SSG, R2/KV/D1 caches, tag cache, queues, cache purge
- **[references/database-orm.md](references/database-orm.md)** - Drizzle, Prisma setup with D1, PostgreSQL, Hyperdrive
- **[references/troubleshooting.md](references/troubleshooting.md)** - Size limits, bundle analysis, common errors

## Migration from @cloudflare/next-on-pages

If migrating from `@cloudflare/next-on-pages`:

1. Uninstall `@cloudflare/next-on-pages` and `eslint-plugin-next-on-pages`
2. Install `@opennextjs/cloudflare`
3. Update `next.config.ts`:
   - Remove `setupDevPlatform()` calls
   - Replace with `initOpenNextCloudflareForDev()`
4. Update imports:
   - Replace `getRequestContext` from `@cloudflare/next-on-pages`
   - Use `getCloudflareContext` from `@opennextjs/cloudflare`
5. Remove Edge runtime exports (`export const runtime = "edge"`)
6. Update wrangler.jsonc with required OpenNext settings
7. Remove next-on-pages eslint rules

## Examples

Official examples in the [@opennextjs/cloudflare repository](https://github.com/opennextjs/opennextjs-cloudflare/tree/main/examples):

- `create-next-app` - Basic Next.js starter
- `middleware` - Middleware usage
- `vercel-blog-starter` - SSG blog example

## Best Practices

1. **Start simple** - Use Static Assets cache for SSG-only sites
2. **Add caching gradually** - Enable R2 cache when you need ISR
3. **Monitor bundle size** - Stay under 10 MiB compressed (use ESBuild Bundle Analyzer)
4. **Use TypeScript** - Run `cf-typegen` to get binding types
5. **Test with preview** - Use `npm run preview` before deploying
6. **Cache database clients** - Use React's `cache()` for per-request instances
7. **Enable observability** - Add `observability` to wrangler.jsonc for logging
8. **Use remote bindings for build** - Enable for ISR with real data

## Common Patterns

See [references/configuration.md](references/configuration.md) for complete examples including:
- Custom Worker with multiple handlers (fetch, scheduled, queue)
- Environment-specific configuration (staging, production)
- Remote bindings for build-time data access

## Resources

- [OpenNext Cloudflare Documentation](https://opennext.js.org/cloudflare)
- [Next.js Documentation](https://nextjs.org/docs)
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers)
- [GitHub Repository](https://github.com/opennextjs/opennextjs-cloudflare)
