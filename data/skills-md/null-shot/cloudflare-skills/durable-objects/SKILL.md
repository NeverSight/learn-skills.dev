---
name: durable-objects
description: Create and review SQLite-backed Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing RPC methods, SQLite storage API, PITR recovery, alarms, WebSocket hibernation, service bindings, or reviewing DO code for best practices. Comprehensive coverage of SQL queries, transactions, namespace API, and testing.
---

# Durable Objects

Build stateful, coordinated applications on Cloudflare's edge using Durable Objects.

> **Important**: This guide focuses on **SQLite-backed Durable Objects** (recommended for all new projects). Configure with `new_sqlite_classes` in migrations. Legacy KV-backed Durable Objects exist for backwards compatibility but are not covered in detail here to avoid confusion.

## When to Use

- Creating new Durable Object classes for stateful coordination
- Implementing RPC methods, alarms, or WebSocket handlers
- Reviewing existing DO code for best practices
- Configuring wrangler.jsonc/toml for DO bindings and migrations
- Writing tests with `@cloudflare/vitest-pool-workers`
- Designing sharding strategies and parent-child relationships

## Reference Documentation

### Durable Objects Core
- `./references/sqlite-storage.md` - Complete SQLite API, PITR, KV methods, transactions, limits
- `./references/service-bindings.md` - Namespace API, stub creation, RPC methods, service bindings
- `./references/rules.md` - Core rules, storage patterns, concurrency, WebSockets
- `./references/testing.md` - Vitest setup, unit/integration tests, alarm testing
- `./references/workers.md` - Workers handlers, types, wrangler config, observability

### SQLite SQL Features
- `./references/json-functions.md` - Complete JSON API: extract, modify, arrays, objects, generated columns
- `./references/foreign-keys.md` - Foreign key constraints, CASCADE, RESTRICT, SET NULL, deferring constraints
- `./references/sql-statements.md` - SQLite extensions (FTS5, Math), PRAGMA statements, schema introspection

Search: `sql.exec`, `getByName`, `transactionSync`, `ctx.storage.sql`, `blockConcurrencyWhile`

## Core Principles

### Use Durable Objects For

| Need | Example |
|------|---------|
| Coordination | Chat rooms, multiplayer games, collaborative docs |
| Strong consistency | Inventory, booking systems, turn-based games |
| Per-entity storage | Multi-tenant SaaS, per-user data |
| Persistent connections | WebSockets, real-time notifications |
| Scheduled work per entity | Subscription renewals, game timeouts |

### Do NOT Use For

- Stateless request handling (use plain Workers)
- Maximum global distribution needs
- High fan-out independent requests

## Quick Reference

### Wrangler Configuration

```jsonc
// wrangler.jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "MY_DO", "class_name": "MyDurableObject" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyDurableObject"] }]
}
```

### Basic Durable Object Pattern

```typescript
import { DurableObject } from "cloudflare:workers";

export interface Env {
  MY_DO: DurableObjectNamespace<MyDurableObject>;
}

export class MyDurableObject extends DurableObject<Env> {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    ctx.blockConcurrencyWhile(async () => {
      this.ctx.storage.sql.exec(`
        CREATE TABLE IF NOT EXISTS items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          data TEXT NOT NULL
        )
      `);
    });
  }

  async addItem(data: string): Promise<number> {
    const result = this.ctx.storage.sql.exec<{ id: number }>(
      "INSERT INTO items (data) VALUES (?) RETURNING id",
      data
    );
    return result.one().id;
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const stub = env.MY_DO.getByName("my-instance");
    const id = await stub.addItem("hello");
    return Response.json({ id });
  },
};
```

## Concurrency Model: Request Queuing

### Single-Threaded Execution

Each Durable Object instance is **single-threaded** and processes requests **one at a time**:

- JavaScript execution is strictly serialized within a DO instance
- No two pieces of code run in parallel on the same DO
- Requests are automatically queued when the DO is busy
- **Soft limit: ~1,000 requests/second per DO instance**

### Input Gates (Automatic Protection)

**Input gates prevent race conditions** by blocking new events during storage operations:

```typescript
async getUniqueNumber(): Promise<number> {
  // ✅ Safe from race conditions even without explicit locking
  // Input gate blocks other requests during these storage operations
  const val = this.ctx.storage.kv.get("counter") ?? 0;
  this.ctx.storage.kv.put("counter", val + 1);
  return val;
}
```

**While storage operations execute:**
- New incoming requests are queued (blocked from starting)
- No other events delivered except storage completion
- Prevents interleaving of concurrent requests

**Input gates do NOT block:**
- External I/O like `fetch()` (allows event delivery while waiting)
- Multiple storage ops initiated in same call without awaits

### Output Gates (Durability Guarantee)

**Output gates ensure data durability** by holding responses until writes complete:

```typescript
async addUser(name: string): Promise<void> {
  // Write without awaiting (fast!)
  this.ctx.storage.sql.exec("INSERT INTO users (name) VALUES (?)", name);
  
  // Response held until write confirms
  // If write fails, response is discarded and DO restarts
}
```

**While storage writes are in progress:**
- Outgoing responses are held back
- External `fetch()` calls are delayed
- Guarantees writes complete before confirmation sent
- On write failure: DO restarts, messages discarded

### Automatic Write Coalescing

Multiple writes without `await` between them execute atomically:

```typescript
// ✅ All three writes commit together atomically
this.ctx.storage.sql.exec("DELETE FROM temp");
this.ctx.storage.sql.exec("INSERT INTO logs VALUES (?)");
this.ctx.storage.sql.exec("UPDATE counts SET value = value + 1");
// Output gate waits for all writes to confirm
```

### Request Queue Limits

When too many requests arrive at one DO:

- Requests queue internally (bounded queue)
- **Overload errors** returned if queue exceeds limits:
  - Too many requests queued (count)
  - Too much data queued (bytes)
  - Requests queued too long (time)

**Error example:**
```typescript
try {
  await stub.doSomething();
} catch (error) {
  if (error.overloaded) {
    // DO is overloaded - back off and retry
    return new Response("Service busy", { status: 429 });
  }
}
```

### Automatic In-Memory Caching

Storage API includes automatic caching (several MB per DO):

- `get()` returns instantly if key is cached
- `put()` writes to cache immediately (persists asynchronously)
- Output gates ensure durability before responses sent
- Write coalescing minimizes network round trips

### Best Practices

1. **Don't create global singleton DOs** - Bottleneck at ~1k req/s
2. **Shard by natural keys** - One DO per user/room/game
3. **Minimize per-request work** - Keep operations fast
4. **Don't await between related writes** - Use write coalescing
5. **Avoid `blockConcurrencyWhile()` on every request** - Kills throughput
6. **Handle overload errors gracefully** - Return 429, exponential backoff

See `./references/rules.md` for detailed concurrency patterns.

## Critical Rules

1. **Model around coordination atoms** - One DO per chat room/game/user, not one global DO
2. **Use `getByName()` for deterministic routing** - Same input = same DO instance
3. **Use SQLite storage** - Configure `new_sqlite_classes` in migrations
4. **Initialize in constructor** - Use `blockConcurrencyWhile()` for schema setup only
5. **Use RPC methods** - Not fetch() handler (compatibility date >= 2024-04-03)
6. **Trust input/output gates** - Write naturally, gates prevent race conditions
7. **One alarm per DO** - `setAlarm()` replaces any existing alarm

## Anti-Patterns (NEVER)

- Single global DO handling all requests (bottleneck)
- Using `blockConcurrencyWhile()` on every request (kills throughput)
- Storing critical state only in memory (lost on eviction/crash)
- Using `await` between related storage writes (breaks atomicity)
- Holding `blockConcurrencyWhile()` across `fetch()` or external I/O

## Stub Creation and RPC Methods

### Get Stub by Name (Recommended)

```typescript
// Direct stub creation - single call, deterministic
const stub = env.MY_DO.getByName("room-123");

// Call RPC methods directly (type-safe)
const message = await stub.sendMessage("user-456", "Hello!");
const messages = await stub.getMessages(20);
```

### Other Stub Creation Methods

```typescript
// From existing ID string
const id = env.MY_DO.idFromString(storedIdString);
const stub = env.MY_DO.get(id);

// New unique ID - store mapping externally
const id = env.MY_DO.newUniqueId();
const stub = env.MY_DO.get(id);
const idString = id.toString(); // Store this

// With location hint (influence placement)
const id = env.GAME.idFromName(gameId, { locationHint: "wnam" });
const stub = env.GAME.get(id);

// Jurisdiction (GDPR compliance)
const euNamespace = env.MY_DO.jurisdiction("eu");
const stub = euNamespace.getByName("user-123");
```

### RPC vs fetch()

```typescript
// ✅ Preferred: RPC methods (clean, type-safe)
export class ChatRoom extends DurableObject<Env> {
  async sendMessage(userId: string, content: string): Promise<Message> {
    // Implementation
    return { id: 1, userId, content };
  }
}

// Caller
const stub = env.CHAT_ROOM.getByName("room-1");
const msg = await stub.sendMessage("user-1", "Hi"); // Type-safe!

// ❌ Legacy: fetch() method (HTTP overhead)
const response = await stub.fetch(request);
```

See `./references/service-bindings.md` for complete namespace and RPC documentation.

## Storage Operations

### SQLite API (Recommended)

Use `ctx.storage.sql` for structured data with tables, indexes, and SQL queries.

**SQLite Features Available:**
- **JSON Functions** - Query and manipulate JSON data. See [references/json-functions.md](references/json-functions.md)
- **Foreign Keys** - Enforce referential integrity. See [references/foreign-keys.md](references/foreign-keys.md)
- **Full-Text Search (FTS5)** - Fast text search with stemming. See [references/sql-statements.md](references/sql-statements.md)
- **Math Functions** - sqrt(), pow(), sin(), cos(), and more
- **PRAGMA Statements** - Schema introspection, optimization, constraint checking

**Basic Usage:**

```typescript
// Create table (in constructor with blockConcurrencyWhile)
this.ctx.storage.sql.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL
  );
  CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
`);

// Insert with parameter binding
const result = this.ctx.storage.sql.exec<{ id: number }>(
  "INSERT INTO users (username, email) VALUES (?, ?) RETURNING id",
  "alice", "alice@example.com"
);
const userId = result.one().id;

// Query
const users = this.ctx.storage.sql.exec<User>(
  "SELECT * FROM users WHERE email = ?",
  email
).toArray();

// Database size
const size = this.ctx.storage.sql.databaseSize; // bytes
```

### Synchronous KV API (Fast Key-Value)

Use `ctx.storage.kv` for simple key-value storage:

```typescript
// Get (returns immediately, no Promise)
const count = this.ctx.storage.kv.get("counter") ?? 0;

// Put (synchronous write to buffer)
this.ctx.storage.kv.put("counter", count + 1);
this.ctx.storage.kv.put("user", { id: 123, name: "Alice" });

// Delete
const existed = this.ctx.storage.kv.delete("temp-key");

// List
for (const [key, value] of this.ctx.storage.kv.list({ prefix: "user:" })) {
  console.log(key, value);
}
```

### Async KV API (Legacy)

Still supported for compatibility:

```typescript
// Get (async)
const value = await this.ctx.storage.get("key");
const values = await this.ctx.storage.get(["key1", "key2"]); // Map<string, any>

// Put (async)
await this.ctx.storage.put("key", value);
await this.ctx.storage.put({ key1: "value1", key2: "value2" });

// Delete
const existed = await this.ctx.storage.delete("key");
const count = await this.ctx.storage.delete(["key1", "key2"]);
```

> **Note**: For new projects, use **SQLite** (`ctx.storage.sql`) for structured data or **synchronous KV** (`ctx.storage.kv`) for simple key-value storage. Legacy KV-backed Durable Objects (without SQLite) are not recommended.

See `./references/sqlite-storage.md` for complete API documentation.

## Transactions

### Synchronous Transactions (Recommended for SQL)

```typescript
// All operations commit atomically or rollback on exception
this.ctx.storage.transactionSync(() => {
  this.ctx.storage.sql.exec(
    "UPDATE accounts SET balance = balance - ? WHERE id = ?",
    100, fromAccount
  );
  this.ctx.storage.sql.exec(
    "UPDATE accounts SET balance = balance + ? WHERE id = ?",
    100, toAccount
  );
  this.ctx.storage.sql.exec(
    "INSERT INTO transfers (from_id, to_id, amount) VALUES (?, ?, ?)",
    fromAccount, toAccount, 100
  );
});
```

### Automatic Write Coalescing

Multiple writes without `await` between them are batched atomically:

```typescript
// ✅ All three writes commit together (atomic)
this.ctx.storage.sql.exec("UPDATE ...");
this.ctx.storage.sql.exec("INSERT ...");
this.ctx.storage.sql.exec("DELETE ...");

// ❌ await breaks atomicity
await this.ctx.storage.put("key1", val1);
await this.ctx.storage.put("key2", val2); // Separate transaction!
```

> **Important**: Do NOT use `BEGIN TRANSACTION`, `COMMIT`, or `ROLLBACK` in SQL queries. Use `transactionSync()` or write coalescing instead.

## Point-in-Time Recovery (PITR)

Restore Durable Object to any point in last 30 days:

```typescript
// Get bookmark for 2 days ago
const twoDaysAgo = Date.now() - (2 * 24 * 60 * 60 * 1000);
const bookmark = await this.ctx.storage.getBookmarkForTime(twoDaysAgo);

// Schedule recovery on next restart
const undoBookmark = await this.ctx.storage.onNextSessionRestoreBookmark(bookmark);

// Restart to perform recovery
this.ctx.abort();
```

Recovers both SQL data and KV data. See `./references/sqlite-storage.md` for details.

## Alarms

```typescript
// Schedule (replaces existing)
await this.ctx.storage.setAlarm(Date.now() + 60_000);

// Handler
async alarm(): Promise<void> {
  // Process scheduled work
  const tasks = this.ctx.storage.sql.exec<Task>(
    "SELECT * FROM tasks WHERE due_at <= ?",
    Date.now()
  ).toArray();
  
  for (const task of tasks) {
    await this.processTask(task);
  }
  
  // Reschedule if more work
  const next = this.ctx.storage.sql.exec<{ due_at: number }>(
    "SELECT MIN(due_at) as due_at FROM tasks WHERE due_at > ?",
    Date.now()
  ).one();
  
  if (next?.due_at) {
    await this.ctx.storage.setAlarm(next.due_at);
  }
}

// Check/cancel
const alarmTime = await this.ctx.storage.getAlarm(); // number | null
await this.ctx.storage.deleteAlarm();
```

Alarms execute within milliseconds of scheduled time, automatically retry on failure (use idempotent handlers).

## WebSocket Hibernation API

Durable Objects support hibernatable WebSocket connections that can be evicted from memory during inactivity while keeping connections open.

### When to Use WebSockets

- Real-time chat applications
- Multiplayer games requiring persistent connections
- Live notifications and updates
- Collaborative editing tools

### Basic WebSocket Pattern

```typescript
import { DurableObject } from "cloudflare:workers";

export interface Env {
  WEBSOCKET_SERVER: DurableObjectNamespace<WebSocketServer>;
}

export class WebSocketServer extends DurableObject<Env> {
  async fetch(request: Request): Promise<Response> {
    // Create WebSocket pair
    const webSocketPair = new WebSocketPair();
    const [client, server] = Object.values(webSocketPair);

    // IMPORTANT: Use this.ctx.acceptWebSocket(), NOT server.accept()
    // This enables hibernation - the DO can be evicted from memory during
    // inactivity while the WebSocket connection remains open
    this.ctx.acceptWebSocket(server);

    return new Response(null, {
      status: 101,
      webSocket: client,
    });
  }

  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer): Promise<void> {
    // Handle incoming messages
    const connections = this.ctx.getWebSockets().length;
    ws.send(`[Durable Object] message: ${message}, connections: ${connections}`);
  }

  async webSocketClose(ws: WebSocket, code: number, reason: string, wasClean: boolean): Promise<void> {
    // Handle connection closure
    ws.close(code, "Durable Object is closing WebSocket");
  }

  async webSocketError(ws: WebSocket, error: unknown): Promise<void> {
    // Handle errors
    console.error("WebSocket error:", error);
    ws.close(1011, "WebSocket error");
  }
}
```

### Critical WebSocket Rules

1. **Use `this.ctx.acceptWebSocket(server)`** - NOT `server.accept()`
2. **Do NOT use `addEventListener` pattern** - Use the handler methods above
3. **Hibernation is automatic** - Don't reference "hibernation" in bindings or code
4. **Use `this.ctx.getWebSockets()`** - To get all active connections for broadcasting

### Broadcasting to All Connections

```typescript
async broadcast(message: string): Promise<void> {
  const sockets = this.ctx.getWebSockets();
  sockets.forEach(ws => ws.send(message));
}
```

### Wrangler Configuration

```jsonc
{
  "durable_objects": {
    "bindings": [
      {
        "name": "WEBSOCKET_SERVER",
        "class_name": "WebSocketServer"
      }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_classes": ["WebSocketServer"]
    }
  ]
}
```

## SQLite Features and Extensions

SQLite-backed Durable Objects support:

### Core SQL Features
- Tables, indexes, views, triggers
- Full SQL query support (SELECT, INSERT, UPDATE, DELETE, JOIN, etc.)
- Parameter binding with `?` placeholders
- Transactions (via `transactionSync()` or write coalescing)
- `PRAGMA` statements (e.g., `PRAGMA user_version` for migrations)

### Supported Extensions

| Extension | Use Case | Example |
|-----------|----------|---------|
| **FTS5** | Full-text search | `CREATE VIRTUAL TABLE docs_fts USING fts5(content)` |
| **JSON** | JSON functions | `SELECT json_extract(data, '$.user.name')` |
| **Math** | Math functions | `SELECT sqrt(value), log(value)` |

### NOT Supported
- Custom SQLite extensions
- Virtual tables (except FTS5)
- `ATTACH DATABASE` (each DO has one database)
- `BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK` in SQL (use `transactionSync()`)

### Numeric Precision

JavaScript's 52-bit precision affects large integers:

```typescript
// ⚠️ Very large int64 values may lose precision
this.ctx.storage.sql.exec("INSERT INTO big_numbers (value) VALUES (?)", 9007199254740993);
const result = this.ctx.storage.sql.exec("SELECT value FROM big_numbers").one();
// Result may not match exactly for very large numbers
```

For exact large integer handling, store as TEXT and parse with BigInt.

## Testing Quick Start

```typescript
import { env } from "cloudflare:test";
import { describe, it, expect } from "vitest";

describe("MyDO", () => {
  it("should work with SQLite", async () => {
    const stub = env.MY_DO.getByName("test");
    const result = await stub.addItem("test");
    expect(result).toBe(1);
  });
  
  it("should query data", async () => {
    const stub = env.MY_DO.getByName("test-2");
    await stub.addItem("item1");
    await stub.addItem("item2");
    const items = await stub.getAllItems();
    expect(items).toHaveLength(2);
  });
});
```

See `./references/testing.md` for comprehensive testing patterns.
