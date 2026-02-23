---
name: cloudflare-workers
description: Rapid development with Cloudflare Workers - build and deploy serverless applications on Cloudflare's global network. Use when building APIs, full-stack web apps, edge functions, background jobs, or real-time applications. Triggers on phrases like "cloudflare workers", "wrangler", "edge computing", "serverless cloudflare", "workers bindings", or files like wrangler.toml, worker.ts, worker.js.
---

# Cloudflare Workers

## Overview

Cloudflare Workers is a serverless execution environment that runs JavaScript, TypeScript, Python, and Rust code on Cloudflare's global network. Workers execute in milliseconds, scale automatically, and integrate with Cloudflare's storage and compute products through bindings.

**Key Benefits:**
- **Zero cold starts** - Workers run in V8 isolates, not containers
- **Global deployment** - Code runs in 300+ cities worldwide
- **Rich ecosystem** - Bindings to D1, KV, R2, Durable Objects, Queues, Containers, Workflows, and more
- **Full-stack capable** - Build APIs and serve static assets in one project
- **Standards-based** - Uses Web APIs (fetch, crypto, streams, WebSockets)

## When to Use This Skill

Use Cloudflare Workers for:

- **APIs and backends** - RESTful APIs, GraphQL, tRPC, WebSocket servers
- **Full-stack applications** - React, Next.js, Remix, Astro, Vue, Svelte with static assets
- **Edge middleware** - Authentication, rate limiting, A/B testing, routing
- **Background processing** - Scheduled jobs (cron), queue consumers, webhooks
- **Data transformation** - ETL pipelines, real-time data processing
- **AI applications** - RAG systems, chatbots, image generation with Workers AI
- **Durable workflows** - Multi-step long-running tasks with automatic retries (Workflows)
- **Container workloads** - Run Docker containers alongside Workers (Containers)
- **MCP servers** - Host remote Model Context Protocol servers
- **Proxy and gateway** - API gateways, content transformation, protocol translation

## Quick Start Workflow

### 1. Install Wrangler CLI

```bash
npm install -g wrangler

# Login to Cloudflare
wrangler login
```

### 2. Create a New Worker

```bash
# Using C3 (create-cloudflare) - recommended
npm create cloudflare@latest my-worker

# Or create manually
wrangler init my-worker
cd my-worker
```

### 3. Write Your Worker

**Basic HTTP API (TypeScript):**

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/api/hello") {
      return Response.json({ message: "Hello from Workers!" });
    }

    return new Response("Not found", { status: 404 });
  },
};
```

**With environment variables and KV:**

```typescript
interface Env {
  MY_VAR: string;
  MY_KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Access environment variable
    const greeting = env.MY_VAR;

    // Read from KV
    const value = await env.MY_KV.get("my-key");

    return Response.json({ greeting, value });
  },
};
```

### 4. Develop Locally

```bash
# Start local development server with hot reload
wrangler dev

# Access at http://localhost:8787
```

### 5. Deploy to Production

```bash
# Deploy to workers.dev subdomain
wrangler deploy

# Deploy to custom domain (configure in wrangler.toml)
wrangler deploy
```

## Core Concepts

### Workers Runtime

Workers use the V8 JavaScript engine with Web Standard APIs:

- **Execution model**: Isolates (not containers) - instant cold starts
- **CPU time limit**: 10ms (Free), 30s (Paid) per request
- **Memory limit**: 128 MB per isolate
- **Languages**: JavaScript, TypeScript, Python, Rust
- **APIs**: fetch, crypto, streams, WebSockets, WebAssembly

**Supported APIs:**
- Fetch API (HTTP requests)
- URL API (URL parsing)
- Web Crypto (encryption, hashing)
- Streams API (data streaming)
- WebSockets (real-time communication)
- Cache API (edge caching)
- HTML Rewriter (HTML transformation)

### Handlers

Workers respond to events through handlers:

**Fetch Handler** (HTTP requests):
```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    return new Response("Hello!");
  },
};
```

**Scheduled Handler** (cron jobs):
```typescript
export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    // Runs on schedule defined in wrangler.toml
    await env.MY_KV.put("last-run", new Date().toISOString());
  },
};
```

**Queue Handler** (message processing):
```typescript
export default {
  async queue(batch: MessageBatch<any>, env: Env, ctx: ExecutionContext) {
    for (const message of batch.messages) {
      await processMessage(message.body);
      message.ack();
    }
  },
};
```

### Bindings

Bindings connect your Worker to Cloudflare resources. Configure in `wrangler.toml`:

**KV (Key-Value Storage):**
```toml
[[kv_namespaces]]
binding = "MY_KV"
id = "your-kv-namespace-id"
```

```typescript
// Usage
await env.MY_KV.put("key", "value");
const value = await env.MY_KV.get("key");
```

**D1 (SQL Database):**
```toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-database-id"
```

```typescript
// Usage
const result = await env.DB.prepare(
  "SELECT * FROM users WHERE id = ?"
).bind(userId).all();
```

**R2 (Object Storage):**
```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

```typescript
// Usage
await env.MY_BUCKET.put("file.txt", "contents");
const object = await env.MY_BUCKET.get("file.txt");
const text = await object?.text();
```

**Environment Variables:**
```toml
[vars]
API_KEY = "development-key"  # pragma: allowlist secret
```

**Secrets** (sensitive data):
```bash
# Set via CLI (not in wrangler.toml)
wrangler secret put API_KEY
```

### Context (ctx)

The `ctx` parameter provides control over request lifecycle:

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    // Run tasks after response is sent
    ctx.waitUntil(
      env.MY_KV.put("request-count", String(Date.now()))
    );

    // Pass through to origin on exception
    ctx.passThroughOnException();

    return new Response("OK");
  },
};
```

### Top-level Environment Access

Since March 2025, you can import `env` at the module level instead of passing it through handlers:

```typescript
import { env } from "cloudflare:workers";

// Access bindings outside of handlers
const apiClient = new ApiClient({ apiKey: env.API_KEY });

export default {
  async fetch(request: Request): Promise<Response> {
    // env is also available here without the parameter
    const data = await env.MY_KV.get("config");
    return Response.json({ data });
  },
};
```

This eliminates prop-drilling `env` through function signatures and enables module-level initialization.

## Rapid Development Patterns

### Wrangler Configuration

**Essential `wrangler.toml`:**

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2025-09-01"

# Custom domain
routes = [
  { pattern = "api.example.com/*", zone_name = "example.com" }
]

# Or workers.dev subdomain
workers_dev = true

# Environment variables
[vars]
ENVIRONMENT = "production"

# Bindings
[[kv_namespaces]]
binding = "CACHE"
id = "your-kv-id"

[[d1_databases]]
binding = "DB"
database_name = "production-db"
database_id = "your-db-id"

[[r2_buckets]]
binding = "ASSETS"
bucket_name = "my-assets"

# Cron triggers
[triggers]
crons = ["0 0 * * *"]  # Daily at midnight
```

### Environment Management

Use environments for staging/production:

```toml
[env.staging]
vars = { ENVIRONMENT = "staging" }

[env.staging.d1_databases]
binding = "DB"
database_name = "staging-db"
database_id = "staging-db-id"

[env.production]
vars = { ENVIRONMENT = "production" }

[env.production.d1_databases]
binding = "DB"
database_name = "production-db"
database_id = "production-db-id"
```

```bash
# Deploy to staging
wrangler deploy --env staging

# Deploy to production
wrangler deploy --env production
```

### Common Patterns

**JSON API with Error Handling:**

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    try {
      const url = new URL(request.url);

      if (url.pathname === "/api/users" && request.method === "GET") {
        const users = await env.DB.prepare("SELECT * FROM users").all();
        return Response.json(users.results);
      }

      if (url.pathname === "/api/users" && request.method === "POST") {
        const body = await request.json();
        await env.DB.prepare(
          "INSERT INTO users (name, email) VALUES (?, ?)"
        ).bind(body.name, body.email).run();
        return Response.json({ success: true }, { status: 201 });
      }

      return Response.json({ error: "Not found" }, { status: 404 });
    } catch (error) {
      return Response.json(
        { error: error.message },
        { status: 500 }
      );
    }
  },
};
```

**Authentication Middleware:**

```typescript
async function authenticate(request: Request, env: Env): Promise<string | null> {
  const authHeader = request.headers.get("Authorization");
  if (!authHeader?.startsWith("Bearer ")) {
    return null;
  }

  const token = authHeader.substring(7);
  const userId = await env.SESSIONS.get(token);
  return userId;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const userId = await authenticate(request, env);

    if (!userId) {
      return Response.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Proceed with authenticated request
    return Response.json({ userId });
  },
};
```

**CORS Headers:**

```typescript
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

export default {
  async fetch(request: Request): Promise<Response> {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const response = await handleRequest(request);

    // Add CORS headers to response
    Object.entries(corsHeaders).forEach(([key, value]) => {
      response.headers.set(key, value);
    });

    return response;
  },
};
```

### Static Assets (Full-Stack Apps)

Serve static files alongside your Worker code:

```toml
[assets]
directory = "./public"
binding = "ASSETS"
```

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // API routes
    if (url.pathname.startsWith("/api/")) {
      return handleAPI(request, env);
    }

    // Serve static assets via the ASSETS binding
    return env.ASSETS.fetch(request);
  },
};
```

### Testing

**Using Vitest:**

```typescript
import { env, createExecutionContext } from "cloudflare:test";
import { describe, it, expect } from "vitest";
import worker from "./index";

describe("Worker", () => {
  it("responds with JSON", async () => {
    const request = new Request("http://example.com/api/hello");
    const ctx = createExecutionContext();
    const response = await worker.fetch(request, env, ctx);

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ message: "Hello!" });
  });
});
```

## Framework Integration

Workers supports major frameworks with adapters:

- **Next.js** - Full App Router and Pages Router support
- **Remix / React Router** - Native Cloudflare adapter
- **Astro** - Server-side rendering on Workers
- **SvelteKit** - Cloudflare adapter available
- **Hono** - Lightweight web framework built for Workers
- **tRPC** - Type-safe APIs with full Workers support

**Example with Hono:**

```typescript
import { Hono } from "hono";

const app = new Hono();

app.get("/", (c) => c.text("Hello!"));
app.get("/api/users/:id", async (c) => {
  const id = c.req.param("id");
  const user = await c.env.DB.prepare(
    "SELECT * FROM users WHERE id = ?"
  ).bind(id).first();
  return c.json(user);
});

export default app;
```

## Advanced Topics

For detailed information on advanced features, see the reference files:

- **Complete Bindings Guide**: `references/bindings-complete-guide.md` - All binding types (D1, KV, R2, Durable Objects, Queues, Workers AI, Vectorize, Workflows, Containers, Secrets Store, Pipelines, AutoRAG)
- **Deployment & CI/CD**: `references/wrangler-and-deployment.md` - Wrangler v4 migration, commands, GitHub Actions, GitLab CI/CD, gradual rollouts, remote bindings
- **Development Best Practices**: `references/development-patterns.md` - Testing, debugging, error handling, performance, top-level env access patterns
- **Advanced Features**: `references/advanced-features.md` - Containers, Workflows, MCP servers, Workers for Platforms, WebSockets, Node.js compat, streaming
- **Observability**: `references/observability.md` - Logging (tail, Logpush, Workers Logs), metrics, traces, debugging

## Resources

**Official Documentation:**
- Workers: https://developers.cloudflare.com/workers/
- Wrangler CLI: https://developers.cloudflare.com/workers/wrangler/
- Runtime APIs: https://developers.cloudflare.com/workers/runtime-apis/
- Examples: https://developers.cloudflare.com/workers/examples/

- Workflows: https://developers.cloudflare.com/workflows/
- Containers: https://developers.cloudflare.com/containers/

**Templates & Quick Starts:**
- Templates: https://developers.cloudflare.com/workers/get-started/quickstarts/
- Framework guides: https://developers.cloudflare.com/workers/framework-guides/

**Community:**
- Discord: https://discord.cloudflare.com
- GitHub: https://github.com/cloudflare/workers-sdk
