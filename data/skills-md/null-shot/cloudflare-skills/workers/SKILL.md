---
name: workers
description: Core Workers fundamentals including handlers, configuration, and Service Bindings. Load when creating new Workers, configuring wrangler.jsonc, implementing fetch/scheduled/queue handlers, using Service Bindings for RPC, generating types with wrangler types, or building microservices.
---

# Cloudflare Workers

Essential patterns for building Cloudflare Workers applications with TypeScript, proper configuration, and Service Bindings for microservices.

## FIRST: Project Setup

Initialize a new Workers project:

```bash
npm create cloudflare@latest my-worker
# OR
wrangler init my-worker
```

**Minimal wrangler.jsonc:**

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "compatibility_flags": ["nodejs_compat"],
  "observability": {
    "enabled": true,
    "head_sampling_rate": 1
  }
}
```

## Code Standards

| Standard | Requirement | Notes |
|----------|-------------|-------|
| **Language** | TypeScript by default | JavaScript only if explicitly requested |
| **Module Format** | ES modules only | NEVER use Service Worker format |
| **Imports** | Always import types/classes | Must import all used methods |
| **File Structure** | Single file unless specified | Keep code in one file by default |
| **Dependencies** | Minimize external deps | Use official SDKs when available |
| **Native Bindings** | Not supported | Avoid FFI/C bindings |
| **Types** | Include TypeScript types | Define Env interface for bindings |

## Handler Patterns

### HTTP Request Handler (fetch)

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // Route handling
    if (url.pathname === "/api/data") {
      return handleAPI(request, env);
    }
    
    return new Response("Hello World!", {
      headers: { "Content-Type": "text/plain" }
    });
  }
};

async function handleAPI(request: Request, env: Env): Promise<Response> {
  // Validate request method
  if (request.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }
  
  try {
    const data = await request.json();
    // Process data...
    return Response.json({ success: true, data });
  } catch (error) {
    return Response.json(
      { error: "Invalid JSON" },
      { status: 400 }
    );
  }
}
```

### Scheduled Handler (cron)

```typescript
export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    // Run scheduled tasks
    console.log("Cron triggered:", new Date(event.scheduledTime).toISOString());
    
    // Use waitUntil for background work
    ctx.waitUntil(performCleanup(env));
  }
};

async function performCleanup(env: Env): Promise<void> {
  // Background cleanup logic
  console.log("Cleanup completed");
}
```

**wrangler.jsonc configuration:**

```jsonc
{
  "triggers": {
    "crons": ["0 */6 * * *"]  // Every 6 hours
  }
}
```

### Queue Consumer Handler

```typescript
export default {
  async queue(batch: MessageBatch<QueueMessage>, env: Env, ctx: ExecutionContext): Promise<void> {
    for (const message of batch.messages) {
      try {
        await processMessage(message.body, env);
        message.ack();
      } catch (error) {
        console.error("Message processing failed:", error);
        message.retry();
      }
    }
  }
};

type QueueMessage = {
  id: string;
  data: unknown;
};

async function processMessage(body: QueueMessage, env: Env): Promise<void> {
  // Process queue message
  console.log("Processing message:", body.id);
}
```

## Auto-Generate Environment Types

**RECOMMENDED:** Use `wrangler types` to automatically generate your `Env` interface from your `wrangler.jsonc`:

```bash
# Generate types from wrangler.jsonc
npx wrangler types

# Output to custom path
npx wrangler types ./types/env.d.ts

# Include runtime types (Wrangler >= 3.66.0)
npx wrangler types --experimental-include-runtime
```

This generates a `worker-configuration.d.ts` file with:
- **Env interface** matching all your bindings (KV, R2, D1, secrets, etc.)
- **Runtime types** matching your `compatibility_date` and `compatibility_flags`
- **Service binding types** with full RPC method signatures

**Add to tsconfig.json:**
```jsonc
{
  "compilerOptions": {
    "types": ["@cloudflare/workers-types", "./worker-configuration"]
  }
}
```

**When to regenerate:**
- After adding/removing bindings in wrangler.jsonc
- After changing compatibility_date or compatibility_flags
- After modifying .dev.vars (secrets)
- Before deploying (run in CI/CD)

**Example generated Env interface:**

```typescript
// worker-configuration.d.ts (auto-generated)
interface Env {
  // From wrangler.jsonc bindings
  MY_KV: KVNamespace;
  MY_BUCKET: R2Bucket;
  DB: D1Database;
  COUNTER: DurableObjectNamespace;
  AUTH_SERVICE: Service<typeof AuthService>;
  AI: Ai;
  MY_QUEUE: Queue;
  
  // From .dev.vars (secrets)
  DATABASE_URL: string;
  API_KEY: string;
  
  // From wrangler.jsonc vars
  ENVIRONMENT: "development" | "staging" | "production";
  API_VERSION: string;
}
```

## Secrets Management

**CRITICAL: Never put secrets in wrangler.jsonc!** Secrets must be encrypted and hidden.

### Secrets vs Environment Variables

| Type | Storage | Use For | Visibility |
|------|---------|---------|------------|
| **vars** (wrangler.jsonc) | Plaintext | Non-sensitive config (URLs, flags) | ✅ Visible |
| **secrets** | Encrypted | API keys, passwords, tokens | ❌ Hidden |

### Local Development with .dev.vars

Create a `.dev.vars` file for local secrets (NEVER commit this file):

```bash
# .dev.vars (add to .gitignore)
DATABASE_URL="postgresql://localhost:5432/dev"
API_KEY="dev-key-12345"
STRIPE_SECRET="sk_test_..."
```

### CI/CD Best Practice: Empty .dev.vars

For CI/CD and type generation, commit a `.dev.vars` with **empty values**:

```bash
# .dev.vars (committed to git)
# Real values set via: wrangler secret put
DATABASE_URL=""
API_KEY=""
STRIPE_SECRET=""
```

**Why this works:**
- `wrangler types` reads `.dev.vars` to generate `Env` types
- Empty values create correct TypeScript types
- CI/CD can run type checking without real secrets
- Production secrets are set via `wrangler secret put` or dashboard

### Setting Production Secrets

**Via Wrangler:**
```bash
# Add/update secret (deploys immediately)
npx wrangler secret put API_KEY
# You'll be prompted for value

# List secrets (values never shown)
npx wrangler secret list

# Delete secret
npx wrangler secret delete API_KEY
```

**Via Dashboard:**
Workers & Pages → Your Worker → Settings → Variables and Secrets → Add → Secret

**Accessing secrets in code:**
```typescript
interface Env {
  DATABASE_URL: string;
  API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Access secrets from env (same as regular env vars)
    const db = new Database(env.DATABASE_URL);
    
    // Validate API key
    const key = request.headers.get("x-api-key");
    if (key !== env.API_KEY) {
      return new Response("Unauthorized", { status: 401 });
    }
    
    return Response.json({ success: true });
  }
};
```

### Secret Store (Account-Level Secrets)

For secrets shared across multiple Workers:

```jsonc
{
  "secrets_store_secrets": [
    {
      "binding": "SHARED_API_KEY",
      "store_id": "abc123def456",
      "secret_name": "GLOBAL_API_KEY"
    }
  ]
}
```

**Accessing Secret Store:**
```typescript
interface Env {
  SHARED_API_KEY: {
    get(): Promise<string>;
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Secret Store requires .get() call
    const apiKey = await env.SHARED_API_KEY.get();
    return Response.json({ success: true });
  }
};
```

See [references/secrets.md](references/secrets.md) for complete secrets management guide.

## wrangler.jsonc Configuration

Complete example with common bindings:

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "compatibility_flags": ["nodejs_compat"],
  
  "observability": {
    "enabled": true,
    "head_sampling_rate": 1
  },
  
  "vars": {
    "ENVIRONMENT": "production"
  },
  
  "kv_namespaces": [
    { "binding": "MY_KV", "id": "your-kv-id" }
  ],
  
  "r2_buckets": [
    { "binding": "MY_BUCKET", "bucket_name": "my-bucket" }
  ],
  
  "d1_databases": [
    { "binding": "DB", "database_name": "my-db", "database_id": "your-db-id" }
  ],
  
  "durable_objects": {
    "bindings": [
      { "name": "COUNTER", "class_name": "Counter" }
    ]
  },
  
  "queues": {
    "producers": [
      { "binding": "MY_QUEUE", "queue": "my-queue" }
    ]
  }
}
```

**Key Configuration Rules:**

- Use `wrangler.jsonc`, NOT `wrangler.toml`
- Set `compatibility_date` to current date (format: `YYYY-MM-DD`)
- Always include `compatibility_flags: ["nodejs_compat"]`
- Enable observability with `head_sampling_rate: 1` for full logging
- Only include bindings that are actually used in your code
- Never include npm dependencies in wrangler.jsonc

See [references/configuration.md](references/configuration.md) for complete configuration options.

## Background Tasks with waitUntil

Offload non-critical work to run after the response is sent:

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // Return fast response
    const response = Response.json({ status: "accepted" });
    
    // Process in background (doesn't block response)
    ctx.waitUntil(performAsyncWork(request, env));
    
    return response;
  }
};

async function performAsyncWork(request: Request, env: Env): Promise<void> {
  // This runs after the response is sent
  const data = await request.json();
  await env.MY_KV.put("processed", JSON.stringify(data));
}
```

**Use waitUntil for:**
- Analytics tracking
- Cache warming
- Logging
- Non-critical database writes
- Cleanup operations

## Error Handling

### HTTP Status Codes

```typescript
async function handleRequest(request: Request, env: Env): Promise<Response> {
  try {
    // 400 - Bad Request
    if (!request.headers.get("content-type")) {
      return Response.json({ error: "Content-Type required" }, { status: 400 });
    }
    
    // 401 - Unauthorized
    const apiKey = request.headers.get("x-api-key");
    if (apiKey !== env.API_KEY) {
      return Response.json({ error: "Invalid API key" }, { status: 401 });
    }
    
    // 404 - Not Found
    const resource = await env.MY_KV.get("resource");
    if (!resource) {
      return Response.json({ error: "Resource not found" }, { status: 404 });
    }
    
    // 200 - Success
    return Response.json({ success: true, data: resource });
    
  } catch (error) {
    // 500 - Internal Server Error
    console.error("Request failed:", error);
    return Response.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
```

### Error Boundaries

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    try {
      return await handleRequest(request, env, ctx);
    } catch (error) {
      console.error("Unhandled error:", error);
      return Response.json(
        { 
          error: "An unexpected error occurred",
          message: error instanceof Error ? error.message : "Unknown error"
        },
        { status: 500 }
      );
    }
  }
};
```

## Service Bindings (Microservices)

**Service Bindings are the recommended way to build multi-Worker architectures.** They enable Worker-to-Worker communication with zero latency, no HTTP overhead, and no additional costs.

### Why Service Bindings?

| Benefit | Description |
|---------|-------------|
| **Zero latency** | Both Workers run on same thread/server by default |
| **No HTTP overhead** | Direct RPC calls, not HTTP requests |
| **Zero additional cost** | Split functionality without increasing bills |
| **Type-safe RPC** | Call methods with full TypeScript support |
| **Internal-only Workers** | Build services not exposed to public internet |
| **Independent deployment** | Each Worker deploys on its own schedule |

### RPC Interface (Recommended)

Export an RPC class from your service Worker:

```typescript
// auth-service/src/index.ts
import { WorkerEntrypoint } from "cloudflare:workers";

export class AuthService extends WorkerEntrypoint<Env> {
  async validateToken(token: string): Promise<{ valid: boolean; userId?: string }> {
    const userId = await this.env.AUTH_TOKENS.get(token);
    return { valid: !!userId, userId: userId || undefined };
  }
  
  async createToken(userId: string): Promise<string> {
    const token = crypto.randomUUID();
    await this.env.AUTH_TOKENS.put(token, userId, { expirationTtl: 86400 });
    return token;
  }
}

// Must also export default handler for HTTP access (if needed)
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return new Response("Auth Service - use RPC interface");
  }
} satisfies ExportedHandler<Env>;
```

**auth-service/wrangler.jsonc:**
```jsonc
{
  "name": "auth-service",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "kv_namespaces": [
    { "binding": "AUTH_TOKENS", "id": "..." }
  ]
}
```

**Calling the service from another Worker:**

```typescript
// api-worker/src/index.ts
interface Env {
  AUTH: Service<import("auth-service").AuthService>;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const token = request.headers.get("Authorization")?.slice(7);
    
    if (!token) {
      return new Response("Unauthorized", { status: 401 });
    }
    
    // Call RPC method directly
    const result = await env.AUTH.validateToken(token);
    
    if (!result.valid) {
      return new Response("Invalid token", { status: 401 });
    }
    
    return Response.json({ userId: result.userId });
  }
};
```

**api-worker/wrangler.jsonc:**
```jsonc
{
  "name": "api-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "services": [
    {
      "binding": "AUTH",
      "service": "auth-service"
    }
  ]
}
```

**Generate types for Service Bindings:**

```bash
# In api-worker directory
npx wrangler types
```

This auto-generates the `Env` interface with the correct `Service<AuthService>` type.

### Fetch-Based Service Binding

For simpler use cases or when you don't need RPC:

```typescript
// api-worker/src/index.ts
interface Env {
  AUTH: Fetcher;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Forward request to auth service
    const authResponse = await env.AUTH.fetch(new Request("https://internal/validate", {
      method: "POST",
      body: JSON.stringify({ token: "..." })
    }));
    
    const result = await authResponse.json();
    return Response.json(result);
  }
};
```

See [references/service-bindings.md](references/service-bindings.md) for advanced patterns including environment-specific bindings and testing.

## Detailed References

- **[references/handlers.md](references/handlers.md)** - Complete handler API reference, context objects, advanced routing
- **[references/configuration.md](references/configuration.md)** - Full wrangler.jsonc options, environment-specific config
- **[references/service-bindings.md](references/service-bindings.md)** - Advanced Service Bindings patterns, testing, environment routing
- **[references/secrets.md](references/secrets.md)** - Complete secrets management guide, .dev.vars, Secret Store, CI/CD best practices

## Best Practices

1. **Use TypeScript by default** - Better type safety and IDE support
2. **Generate types with wrangler types** - Auto-generate Env interface from config and .dev.vars
3. **NEVER put secrets in wrangler.jsonc** - Use `wrangler secret put` or .dev.vars for local dev
4. **Use .dev.vars with empty values for CI** - Enables type generation without exposing secrets
5. **Enable observability** - Set `observability.enabled: true` for logging
6. **Use Service Bindings for microservices** - Zero-cost, type-safe Worker-to-Worker calls
7. **Validate all inputs** - Never trust user data
8. **Handle errors gracefully** - Use try-catch and return appropriate status codes
9. **Use waitUntil for background tasks** - Don't block response on non-critical work
10. **Keep bundle size small** - Minimize dependencies for faster cold starts

## Common Patterns

### Complete API Worker

```typescript
interface Env {
  MY_KV: KVNamespace;
  API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    try {
      // CORS preflight
      if (request.method === "OPTIONS") {
        return new Response(null, {
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
          }
        });
      }
      
      // Route handling
      const url = new URL(request.url);
      
      if (url.pathname === "/api/data" && request.method === "GET") {
        const data = await env.MY_KV.get("data");
        return Response.json({ data: data || null });
      }
      
      if (url.pathname === "/api/data" && request.method === "POST") {
        const body = await request.json();
        await env.MY_KV.put("data", JSON.stringify(body));
        return Response.json({ success: true });
      }
      
      return new Response("Not found", { status: 404 });
      
    } catch (error) {
      console.error("Request failed:", error);
      return Response.json(
        { error: "Internal server error" },
        { status: 500 }
      );
    }
  }
};
```

### Middleware Pattern

```typescript
type Middleware = (
  request: Request,
  env: Env,
  ctx: ExecutionContext,
  next: () => Promise<Response>
) => Promise<Response>;

const authMiddleware: Middleware = async (request, env, ctx, next) => {
  const apiKey = request.headers.get("x-api-key");
  if (apiKey !== env.API_KEY) {
    return new Response("Unauthorized", { status: 401 });
  }
  return next();
};

const loggingMiddleware: Middleware = async (request, env, ctx, next) => {
  console.log(`${request.method} ${request.url}`);
  const response = await next();
  console.log(`Response: ${response.status}`);
  return response;
};

function compose(...middlewares: Middleware[]) {
  return async (request: Request, env: Env, ctx: ExecutionContext): Promise<Response> => {
    let index = 0;
    
    const next = async (): Promise<Response> => {
      if (index >= middlewares.length) {
        return handleRequest(request, env);
      }
      const middleware = middlewares[index++];
      return middleware(request, env, ctx, next);
    };
    
    return next();
  };
}

export default {
  fetch: compose(loggingMiddleware, authMiddleware)
};
```

## Resources

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers)
- [Workers Examples](https://developers.cloudflare.com/workers/examples)
- [Wrangler CLI Documentation](https://developers.cloudflare.com/workers/wrangler)
