---
name: kv
description: Eventually-consistent key-value storage distributed globally. Load when implementing session storage, authentication tokens, caching API responses, feature flags, A/B testing, rate limiting, or storing user preferences at the edge.
---

# Workers KV

Fast, eventually-consistent key-value storage distributed globally across Cloudflare's edge network.

## FIRST: Create KV Namespace

```bash
# Create namespace
wrangler kv namespace create MY_KV

# Create preview namespace for dev
wrangler kv namespace create MY_KV --preview

# Add to wrangler.jsonc (use IDs from commands above)
```

## When to Use

| Use Case | Why KV |
|----------|---------|
| Session storage | Fast token/session lookups at the edge |
| Caching | Cache API responses, rendered HTML, or computed results |
| Configuration data | Feature flags, app settings, rate limit counters |
| User profiles | Store user preferences, settings, metadata |
| A/B testing | Store experiment assignments and feature toggles |
| Rate limiting | Track request counts per user/IP with TTL |

**Don't use KV for:**
- Strongly consistent data (use Durable Objects)
- Relational queries (use D1)
- Large files >25MB (use R2)
- Transactional operations

## Quick Reference

| Operation | API | Example |
|-----------|-----|---------|
| Read value | `get(key)` | `await env.KV.get("user:123")` |
| Read with metadata | `getWithMetadata(key)` | `await env.KV.getWithMetadata("key", "json")` |
| Write value | `put(key, value, options)` | `await env.KV.put("key", "value", { expirationTtl: 3600 })` |
| Delete value | `delete(key)` | `await env.KV.delete("key")` |
| List keys | `list(options)` | `await env.KV.list({ prefix: "user:" })` |

### Value Types

```typescript
// String (default)
await env.KV.get("key")

// JSON (auto-parse)
await env.KV.get("user:123", "json")

// Binary
await env.KV.get("image", "arrayBuffer")

// Stream
await env.KV.get("large-file", "stream")
```

## wrangler.jsonc Configuration

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01",
  
  "kv_namespaces": [
    {
      "binding": "AUTH_TOKENS",
      "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "preview_id": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    },
    {
      "binding": "CACHE",
      "id": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    }
  ]
}
```

**After adding bindings, generate types:**
```bash
wrangler types
```

## Session Authentication Pattern

Complete session management using KV for token storage with Hono router:

```typescript
// src/index.ts
import { Hono } from 'hono'
import { cors } from 'hono/cors'

interface Env {
  AUTH_TOKENS: KVNamespace;
}

const app = new Hono<{ Bindings: Env }>()

// Add CORS middleware
app.use('*', cors())

app.get('/', async (c) => {
  try {
    // Get token from header or cookie
    const token = c.req.header('Authorization')?.slice(7) ||
      c.req.header('Cookie')?.match(/auth_token=([^;]+)/)?.[1];
    
    if (!token) {
      return c.json({
        authenticated: false,
        message: 'No authentication token provided'
      }, 403)
    }

    // Check token in KV
    const userData = await c.env.AUTH_TOKENS.get(token)

    if (!userData) {
      return c.json({
        authenticated: false,
        message: 'Invalid or expired token'
      }, 403)
    }

    return c.json({
      authenticated: true,
      message: 'Authentication successful',
      data: JSON.parse(userData)
    })

  } catch (error) {
    console.error('Authentication error:', error)
    return c.json({
      authenticated: false,
      message: 'Internal server error'
    }, 500)
  }
})

export default app
```

**Store a session token:**
```typescript
// Create token (e.g., on login)
const token = crypto.randomUUID()
const userData = { userId: 123, email: "user@example.com" }

// Store with 24-hour expiration
await env.AUTH_TOKENS.put(
  token, 
  JSON.stringify(userData),
  { expirationTtl: 86400 }
)
```

## Key Design Patterns

### TTL (Time-to-Live)

```typescript
// Expire after 1 hour
await env.KV.put("cache:api-response", data, {
  expirationTtl: 3600
})

// Expire at specific time
await env.KV.put("promo:summer", data, {
  expiration: Math.floor(Date.now() / 1000) + 86400
})
```

### Key Naming Conventions

```typescript
// Use prefixes for organization and listing
"user:123"           // User data
"session:abc123"     // Session tokens
"cache:api:/users"   // API cache
"config:feature:new" // Feature flags
"rate:ip:1.2.3.4"    // Rate limiting

// List all user keys
const { keys } = await env.KV.list({ prefix: "user:" })
```

### Metadata

```typescript
// Store metadata with value
await env.KV.put("user:123", userData, {
  metadata: { 
    created: Date.now(),
    version: "v1",
    tags: ["premium", "verified"]
  }
})

// Read with metadata
const { value, metadata } = await env.KV.getWithMetadata("user:123", "json")
console.log(metadata.tags) // ["premium", "verified"]
```

### Caching Pattern

```typescript
async function getCachedData(env: Env, key: string) {
  // Try cache first
  const cached = await env.CACHE.get(key, "json")
  if (cached) return cached

  // Fetch from origin
  const data = await fetchFromAPI()

  // Cache for 5 minutes
  await env.CACHE.put(key, JSON.stringify(data), {
    expirationTtl: 300
  })

  return data
}
```

### Rate Limiting

```typescript
async function checkRateLimit(env: Env, ip: string): Promise<boolean> {
  const key = `rate:${ip}`
  const count = await env.KV.get(key)

  if (!count) {
    // First request
    await env.KV.put(key, "1", { expirationTtl: 60 })
    return true
  }

  const current = parseInt(count)
  if (current >= 100) {
    return false // Rate limit exceeded
  }

  // Increment counter
  await env.KV.put(key, String(current + 1), { expirationTtl: 60 })
  return true
}
```

## Edge Cases

### Handling 404s (Key Not Found)

```typescript
const value = await env.KV.get("key")

if (value === null) {
  // Key doesn't exist or has expired
  console.log("Key not found")
}

// For JSON, check before parsing
const userData = await env.KV.get("user:123")
if (userData) {
  const user = JSON.parse(userData)
}

// Or use "json" type (returns null if not found)
const user = await env.KV.get("user:123", "json")
```

### Eventual Consistency

```typescript
// Write may take seconds to propagate globally
await env.KV.put("counter", "1")

// Immediate read might return old value or null
const value = await env.KV.get("counter") // Could be null or "1"

// For strong consistency, use Durable Objects instead
```

### Size Limits

```typescript
// Keys: max 512 bytes
// Values: max 25 MB
// Metadata: max 1024 bytes

// For larger data, use R2:
if (data.length > 25 * 1024 * 1024) {
  await env.BUCKET.put("large-file", data)
} else {
  await env.KV.put("small-file", data)
}
```

### List Pagination

```typescript
// List returns max 1000 keys per call
let cursor: string | undefined
const allKeys: string[] = []

do {
  const result = await env.KV.list({ 
    prefix: "user:",
    cursor 
  })
  
  allKeys.push(...result.keys.map(k => k.name))
  cursor = result.list_complete ? undefined : result.cursor
} while (cursor)
```

## Detailed References

- **[references/patterns.md](references/patterns.md)** - Advanced patterns: cache invalidation, distributed locks, A/B testing
- **[references/limits.md](references/limits.md)** - Size limits, rate limits, consistency model
- **[references/testing.md](references/testing.md)** - Vitest integration, mocking KV, test isolation

## Best Practices

1. **Use TTL for temporary data**: Always set expiration for sessions, caches, rate limits
2. **Prefix your keys**: Makes listing and management easier (`user:`, `session:`, `cache:`)
3. **Don't rely on immediate consistency**: KV is eventually consistent (usually <60s)
4. **Handle null values**: Keys not found or expired return `null`
5. **Use metadata for filtering**: Store timestamps, versions, tags without reading values
6. **Batch operations**: Use `list()` with prefix instead of individual gets
7. **Cache at the edge**: KV is fastest when accessed from same region as user
8. **Monitor costs**: Writes are more expensive than reads, optimize write patterns
9. **Use Durable Objects for coordination**: Don't use KV for locks or transactions
10. **Generate types**: Run `wrangler types` after config changes for type safety
