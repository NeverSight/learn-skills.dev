---
name: data-fair-ws
description: >
  How to implement real-time websocket communication in data-fair services.
  Covers the full stack: server-side setup with @data-fair/lib-express/ws-server,
  emitting events with @data-fair/lib-node/ws-emitter, subscribing from
  Vue components with @data-fair/lib-vue/ws, and using
  @data-fair/lib-node/ws-client for Node.js programmatic WS clients and
  integration tests. Use this skill whenever the user wants to add websocket
  support, emit real-time events, subscribe to channels, implement live updates,
  push notifications, any pub/sub pattern in a data-fair service, or write
  integration tests that verify websocket behavior — even if they just say
  "real-time", "live updates", or "test websockets".
---

# WebSocket Integration in data-fair Services

The data-fair stack provides a turnkey pub/sub websocket system built on three
coordinated packages. Messages flow through a MongoDB capped collection that
acts as a durable bus, so the system scales across multiple server processes
without an external broker.

## Architecture Overview

```
Vue UI (browser)                 Express API server              Worker / background process
─────────────────                ──────────────────               ──────────────────────────
useWS('/my-svc/api/')            wsServer.start(server, db,      wsEmitter.init(db)
  .subscribe(channel, cb)  ◄──    canSubscribe)                  wsEmitter.emit(channel, data)
                                       │  ▲                             │
Node.js client (tests)                 │  │ ws connection               │
──────────────────────                 │  │                             │
WsClient / DataFairWsClient       ─────┘  │                             │
  .subscribe(channel)            ◄────────┘                             │
  .waitFor(channel, filter)            │  tailable cursor               │  insert
                                       ▼                                ▼
                                 ┌──────────────────────────────────────────┐
                                 │  MongoDB capped collection "ws-messages" │
                                 └──────────────────────────────────────────┘
```

1. **`@data-fair/lib-node/ws-emitter`** — writes messages to the capped collection.
2. **`@data-fair/lib-express/ws-server`** — runs a `WebSocketServer` attached to
   the HTTP server. Uses a MongoDB tailable cursor to watch for new messages and
   forwards them to subscribed browser clients. Handles subscribe/unsubscribe
   protocol and authorization.
3. **`@data-fair/lib-vue/ws`** (`useWS`) — Vue composable that manages a
   `ReconnectingWebSocket` connection, tracks subscriptions reactively, and
   auto-cleans up via `onScopeDispose`.
4. **`@data-fair/lib-node/ws-client`** (`WsClient` / `DataFairWsClient`) — Node.js
   WebSocket client with auto-reconnect, JSON parsing, and channel subscriptions.
   Designed for programmatic use in workers and **integration tests**.

## Step-by-step Integration Guide

### 1. Server-side: start the WS server

In your Express API entry point (typically `server.ts`):

```ts
import * as wsServer from '@data-fair/lib-express/ws-server.js'
import * as wsEmitter from '@data-fair/lib-node/ws-emitter.js'

// Inside your start() function, after creating the HTTP server:
await wsServer.start(server, mongo.db, async (channel, sessionState) => {
  // Authorization callback — return true if the user may subscribe to `channel`.
  // Parse the channel string to extract the resource and check permissions.
  // sessionState is the user's session from @data-fair/lib-express session middleware.
  // Admin mode users bypass this check automatically in ws-server.
  return myAuthCheck(channel, sessionState)
})
await wsEmitter.init(mongo.db)
```

On shutdown:
```ts
await wsServer.stop()
```

The `canSubscribe` callback receives `(channel: string, sessionState: SessionState, message: any)`.
It is the place to enforce per-channel authorization. Common patterns:

- **User-scoped channels** (`user:{userId}:notifications`): check `sessionState.user.id === ownerId`
- **Resource-scoped channels** (`things/{thingId}/updates`): load the resource, check the user's permission profile

Read `references/server-examples.md` for full examples from events and processings.

### 2. Server-side: emit events

Anywhere you need to push data (API routes, workers, background tasks):

```ts
import * as wsEmitter from '@data-fair/lib-node/ws-emitter.js'

// wsEmitter.init(db) must have been called first in the same process.
await wsEmitter.emit('things/abc123/updated', { status: 'done', progress: 100 })
```

The emitter writes a document `{ type: 'message', channel, data, date }` into the
`ws-messages` capped collection. The ws-server's tailable cursor picks it up and
forwards it to all clients subscribed to that channel.

Because the bus is MongoDB, **any process connected to the same database can emit**.
This is how workers/background tasks push updates to the API server's WS clients.

### 3. Channel naming conventions

Use colon or slash-separated hierarchical names that encode the authorization scope:

| Pattern | Use case |
|---------|----------|
| `user:{userId}:notifications` | Per-user channels (events service) |
| `things/{thingId}/updates` | Per-resource channels (general) |
| `things/{thingId}/run-log` | Sub-resource event streams (processings) |

The first segment(s) should let `canSubscribe` extract the resource identifier
and look up permissions efficiently.

### 4. Client-side: subscribe in Vue components

```ts
import { useWS } from '@data-fair/lib-vue/ws.js'
// or rely on auto-import if configured

const ws = useWS('/my-service/api/')

// Subscribe to a channel. The callback fires for each incoming message.
// Subscription is auto-cleaned when the Vue scope is disposed.
ws?.subscribe<MyDataType>('things/abc123/updates', (data) => {
  // data is the payload passed to wsEmitter.emit()
  applyUpdate(data)
})
```

Key behaviors of `useWS`:
- Converts the path to `ws://` / `wss://` based on `window.location.origin`
- Uses `ReconnectingWebSocket` — auto-reconnects and re-subscribes on reconnect
- One singleton connection per path (multiple `useWS('/same/')` calls share it)
- `onScopeDispose` auto-unsubscribes — no manual cleanup needed in most cases
- Manual unsubscribe: `ws?.unsubscribe(channel, listener)` when needed outside of scope disposal

### 5. Wire protocol

The WS connection uses a simple JSON protocol:

**Client to server:**
```json
{"type": "subscribe", "channel": "my_channel"}
{"type": "unsubscribe", "channel": "my_channel"}
```

**Server to client:**
```json
{"type": "subscribe-confirm", "channel": "my_channel"}
{"type": "unsubscribe-confirm", "channel": "my_channel"}
{"type": "message", "channel": "my_channel", "data": {...}, "date": "2025-01-01T00:00:00.000Z"}
{"type": "error", "status": 400, "data": "error message", "channel": "my_channel"}
```

The `Message` type is defined in `@data-fair/lib-common-types/ws`:
```ts
interface Message { type: string; channel: string; data?: any; status?: number }
```

### 6. Nginx / proxy configuration

WebSocket upgrade headers must be set in your reverse proxy:

```nginx
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "Upgrade";
```

### 7. Node.js client: `@data-fair/lib-node/ws-client`

The `ws-client` module provides two classes for consuming websockets from Node.js
(not from the browser). This is essential for **integration tests** and for
programmatic use in workers or CLI tools.

#### `WsClient` — generic WS client

```ts
import { WsClient } from '@data-fair/lib-node/ws-client.js'

const client = new WsClient({
  url: 'http://localhost:8080',   // HTTP URL — auto-converted to ws://
  headers: { Cookie: '...' },     // optional: forward auth cookies
  apiKey: 'my-api-key',           // optional: sent in subscribe messages
  adminMode: true,                // optional: enables admin mode
  account: { type: 'organization', id: 'org1', name: 'Org 1' },  // optional
  log: console                    // optional: defaults to console
})
```

**Key methods:**

- **`subscribe(channel, force?, timeout?)`** — Subscribes to a channel. Opens the
  WS connection on first call. Sends a subscribe message including `apiKey` and
  `account` if configured. Waits for `subscribe-confirm` or throws on `error`.
  ```ts
  await client.subscribe('things/abc123/updates')
  ```

- **`waitFor(channel, filter?, timeout?, skipSubscribe?, fullMessage?)`** — Subscribes
  (unless `skipSubscribe`) then returns a promise that resolves when a matching
  message arrives on the channel, or rejects on timeout (default 5 minutes).
  ```ts
  // Wait for a specific event type
  const event = await client.waitFor(
    'things/abc123/updates',
    (data) => data.status === 'done',
    10000  // 10s timeout
  )
  ```

- **`close()`** — Terminates the underlying WebSocket connection.

Auto-reconnect: if the connection drops, `WsClient` automatically reconnects
and re-subscribes to all previously subscribed channels.

#### `DataFairWsClient` — specialized for Data Fair datasets

Extends `WsClient` with a convenience method for waiting on dataset journal events:

```ts
import { DataFairWsClient } from '@data-fair/lib-node/ws-client.js'

const ws = new DataFairWsClient({
  url: 'http://localhost:8080',
  apiKey: 'my-api-key',
  log: console
})

// Wait for a dataset to finish indexing
const event = await ws.waitForJournal(datasetId, 'finalize-end', 60000)
// Throws if an 'error' event arrives before the expected event
```

#### Integration testing with `WsClient`

The `WsClient` is the primary tool for writing integration tests that verify
websocket behavior end-to-end. Typical pattern:

```ts
import { WsClient } from '@data-fair/lib-node/ws-client.js'
import * as wsEmitter from '@data-fair/lib-node/ws-emitter.js'

describe('websocket integration', () => {
  let client: WsClient

  beforeAll(async () => {
    // Point at the test server
    client = new WsClient({
      url: 'http://localhost:' + testPort,
      headers: { Cookie: testSessionCookie }  // or use apiKey
    })
  })

  afterAll(() => {
    client.close()
  })

  it('should receive emitted events', async () => {
    // Subscribe and set up a waiter BEFORE emitting
    const eventPromise = client.waitFor(
      'things/abc123/updates',
      (data) => data.status === 'done'
    )

    // Trigger the action that emits
    await wsEmitter.emit('things/abc123/updates', { status: 'done', result: 42 })

    // Assert the received event
    const event = await eventPromise
    expect(event.status).toBe('done')
    expect(event.result).toBe(42)
  })

  it('should reject unauthorized subscriptions', async () => {
    const unauthorizedClient = new WsClient({
      url: 'http://localhost:' + testPort
      // no auth headers
    })
    try {
      await unauthorizedClient.subscribe('private/channel')
      throw new Error('should have thrown')
    } catch (err) {
      expect(err.message).toMatch(/Permission/)
    } finally {
      unauthorizedClient.close()
    }
  })
})
```

**Testing tips:**
- Always call `waitFor()` or `subscribe()` **before** the action that emits —
  otherwise the event may fire before the subscription is active.
- Use short timeouts in tests (e.g. 5000ms) to fail fast instead of the default 5min.
- Call `client.close()` in `afterAll` / `afterEach` to avoid hanging connections.
- The `WsClient` sends `apiKey` and `account` in the subscribe message payload,
  which the server's `canSubscribe` callback receives as `message.apiKey` and
  `message.account`. This allows tests to authenticate without cookies.

## Common Pitfalls

- **Forgetting `wsEmitter.init(db)` in workers**: each process that emits must
  call `init()` with its own MongoDB `db` handle. The API server AND the worker
  both need it.
- **canSubscribe not parsing the channel**: the channel string is the *only* input
  for authorization. Design channels so the auth callback can extract the resource
  ID without extra lookups when possible.
- **SSR guard**: `useWS` checks `import.meta.env?.SSR` and bails out during
  server-side rendering. No action needed, but be aware it returns `undefined`
  in SSR — always use optional chaining (`ws?.subscribe`).

## Reference Files

- `references/server-examples.md` — Full canSubscribe and emit examples from
  the events and processings services, plus integration test patterns using
  `WsClient`. Read this when implementing a new service's WS layer or writing
  tests.
- `references/source-api.md` — Abridged source of the four library modules
  (ws-server, ws-emitter, useWS, ws-client). Read this only if you need to
  understand internal behavior or debug an issue.
