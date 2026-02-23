---
name: cloudflare-worker
description: Build edge-first TypeScript applications on Cloudflare Workers. Covers Workers API, Hono framework, KV/D1/R2 storage, Durable Objects, Queues, and testing patterns. Use when creating serverless workers, edge functions, or Cloudflare-deployed services.
allowed-tools: Read Write Edit MultiEdit Grep Glob Bash WebSearch WebFetch
---

# Cloudflare Workers

**Development patterns for TypeScript Workers.**

**Related skills (majestic-devops):**
- `wrangler-coder`: CLI deployment, secrets, testing, multi-environment
- `cloudflare-coder`: Infrastructure provisioning with Terraform/OpenTofu

## Core Principles

### Edge-First Thinking

- **Stateless by default**: Workers don't persist state between requests
- **Global distribution**: Code runs in 300+ data centers worldwide
- **Cold start optimized**: V8 isolates start in milliseconds
- **Request/response model**: Each invocation handles one request

### Storage Selection

| Storage | Use Case | Consistency | Latency |
|---------|----------|-------------|---------|
| **KV** | Config, flags, cached data | Eventually consistent | ~10ms |
| **D1** | Relational data, transactions | Strong (single region) | ~30-50ms |
| **R2** | Files, images, large objects | Strong | ~50-100ms |
| **Durable Objects** | Real-time state, WebSockets | Strong (per-object) | ~50ms |
| **Queues** | Async processing, batching | At-least-once | Async |

## Project Structure

```
my-worker/
├── src/
│   ├── index.ts          # Entry point
│   ├── routes/           # Route handlers
│   ├── services/         # Business logic
│   └── types.ts          # Type definitions
├── test/
├── wrangler.toml         # Cloudflare config
├── package.json
└── tsconfig.json
```

## Quick Start

### Minimal wrangler.toml

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-01"
compatibility_flags = ["nodejs_compat"]
```

See [references/setup.md](references/setup.md) for full configuration with all bindings.

### Basic Hono App

```typescript
import { Hono } from 'hono';
import { Env } from './types';

const app = new Hono<{ Bindings: Env }>();

app.get('/', (c) => c.json({ status: 'ok' }));
app.onError((err, c) => c.json({ error: 'Internal Error' }, 500));
app.notFound((c) => c.json({ error: 'Not Found' }, 404));

export default app;
```

See [references/hono.md](references/hono.md) for route organization and middleware patterns.

## Storage Quick Reference

### KV (Key-Value)

```typescript
await env.CACHE.get('key', 'json');
await env.CACHE.put('key', value, { expirationTtl: 3600 });
await env.CACHE.delete('key');
```

### D1 (SQLite)

```typescript
const user = await env.DB.prepare('SELECT * FROM users WHERE id = ?')
  .bind(id).first();
```

### R2 (Object Storage)

```typescript
await env.STORAGE.put('path/file.json', JSON.stringify(data));
const object = await env.STORAGE.get('path/file.json');
```

See [references/storage.md](references/storage.md) for caching patterns, migrations, and queries.

## Durable Objects

Use for: real-time coordination, WebSockets, rate limiting, distributed locks.

```typescript
// Get DO stub
const id = c.env.COUNTER.idFromName('my-counter');
const stub = c.env.COUNTER.get(id);
const response = await stub.fetch(new Request('http://do/increment'));
```

See [references/durable-objects.md](references/durable-objects.md) for full patterns including WebSocket Hibernation.

## Queues

```typescript
// Producer
await env.QUEUE.send({ type: 'email', payload: { to: 'user@example.com' } });

// Consumer (add to default export)
async queue(batch: MessageBatch, env: Env) {
  for (const msg of batch.messages) {
    try { await process(msg.body); msg.ack(); }
    catch { msg.retry(); }
  }
}
```

See [references/queues-testing.md](references/queues-testing.md) for consumer patterns and testing setup.

## CLI Commands

```bash
# Development
wrangler dev                    # Start local server
wrangler dev --remote           # Dev with remote bindings

# Deploy
wrangler deploy

# D1
wrangler d1 migrations apply my-database

# Secrets
wrangler secret put API_KEY

# Logs
wrangler tail
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Service Worker format | ES modules |
| `await` cache writes | `waitUntil` for non-blocking |
| Large KV values (>25MB) | R2 for files |
| `server.accept()` for WebSockets | `ctx.acceptWebSocket()` (Hibernation API) |
| Block on analytics/logging | `waitUntil` for background tasks |
| Assume KV immediate consistency | D1 or DOs for consistency-critical |

## Resources

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Hono Documentation](https://hono.dev/docs/getting-started/cloudflare-workers)
- [D1 Documentation](https://developers.cloudflare.com/d1/)
- [Durable Objects Guide](https://developers.cloudflare.com/durable-objects/)
