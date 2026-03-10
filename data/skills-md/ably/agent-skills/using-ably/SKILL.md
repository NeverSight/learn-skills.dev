---
name: using-ably
description: >
  ALWAYS use when building realtime features with Ably — messaging, chat,
  collaboration, presence, or AI token streaming. Covers product and SDK selection
  (Pub/Sub vs Chat vs Spaces vs LiveObjects), authentication (JWT, token auth,
  authUrl), channel design, React integration, and critical mistakes like
  missing Chat attach(), client-side API key exposure, and creating Ably clients
  inside components. Fetches current docs from ably.com/llms.txt before generating
  code. Not for general WebSocket or non-Ably realtime libraries.
license: Apache-2.0
metadata:
  tags: ably, realtime, pubsub, websocket, messaging, chat, spaces, ai-transport, liveobjects, livesync
---

# Using Ably

Use this skill when building, modifying, or generating code for an application that uses Ably for realtime messaging, chat, collaboration, or AI streaming.

## What Ably Is

Ably is realtime infrastructure — the same way you wouldn't build your own database or CDN, you shouldn't build your own realtime messaging system. Ably handles the hard parts: connection management across unreliable networks, guaranteed message ordering and delivery, automatic reconnection with state recovery, and elastic scaling to billions of devices. It works across platforms (25+ SDKs) and protocols (WebSocket, MQTT, SSE, HTTP), so you can focus on your application logic rather than transport reliability.

## Documentation

Always check the official docs at [ably.com/docs](https://ably.com/docs?source=using-ably) for current API references. For LLM-optimized documentation, use [ably.com/llms.txt](https://ably.com/llms.txt?source=using-ably). The guidance below covers architectural decisions and common mistakes that documentation alone doesn't prevent.

---

## Before Writing Code

**Always verify against current documentation before generating Ably code.** Training data goes stale — methods get renamed, parameters change, new products launch. These three checks prevent the most common LLM code generation failures.

### 1. Fetch Current Docs First

Before generating code for any Ably feature:

1. Fetch `https://ably.com/llms.txt?source=using-ably` to get the documentation URL index
2. Fetch the relevant product and platform documentation pages
3. Verify method names, parameters, return types, and package versions against the fetched docs
4. If a feature or method doesn't appear in the docs, it probably doesn't exist — don't fabricate it

Never guess or construct doc URLs. Only use URLs from llms.txt or web search results. If a URL 404s, go back to llms.txt. Web search is also allowed as a complementary approach. If llms.txt is unreachable, fall back to web search or browse `https://ably.com/docs?source=using-ably` directly.

### 2. Confirm SDK Availability

Not all products are available on all platforms. Before generating code, confirm from the fetched docs that the product has an SDK for the user's platform.

If no SDK exists:
- State clearly: "[Product] does not currently have an SDK for [platform]"
- Don't fabricate an API
- Offer alternatives: REST API directly, a different product that IS available, or MQTT/SSE protocol adapters for constrained devices

### 3. Post-Generation Check

After generating code, verify these common-mistake patterns:

- [ ] **API key in client code?** Must use `authUrl`/`authCallback` with JWT or token auth (see Section 3)
- [ ] **Chat SDK: `attach()` before subscribing?** Subscribe first to avoid messages being silently lost (see Section 7)
- [ ] **React: Ably client created inside a component without cleanup?** Create once outside and pass via provider, or use useEffect with proper cleanup (see Section 8)
- [ ] **Server-side: Realtime SDK used when REST would suffice?** Default to `Ably.Rest` for publishing, token generation, history (see Section 2)
- [ ] **Connection cleanup on unmount/exit?** Call `realtime.close()` (see Section 5)
- [ ] **Reimplementing built-in behavior?** Don't add custom debounce for typing indicators, custom throttling for cursors, or custom conflict resolution for LiveObjects (see Section 9)

---

## 1. Understand the Product and SDK Landscape

Ably is a multi-product platform, not a single SDK. Choosing the wrong product or SDK is the most common integration mistake.

### Product Layer: What Are You Building?

| Product | Use Case | SDK |
|---------|----------|-----|
| **Pub/Sub** | Core messaging: live dashboards, notifications, IoT, event streaming | `ably` (Realtime or REST) |
| **AI Transport** | Streaming LLM tokens, multi-agent coordination, resumable AI sessions | `ably` (Realtime) |
| **LiveObjects** | Shared mutable state: counters, key-value maps, collaborative data | `ably` + LiveObjects plugin |
| **LiveSync** | Database-to-frontend sync (PostgreSQL change streams) | `@ably-labs/models` + ADBC connector |
| **Chat** | Chat rooms, typing indicators, reactions, message history, moderation | `@ably/chat` |
| **Spaces** | Collaborative cursors, avatar stacks, member locations, component locking | `@ably/spaces` |

### SDK Architecture: Two Layers

**Layer 1 — Core SDKs** (used directly for Pub/Sub, AI Transport, LiveObjects, LiveSync):

| SDK | Use When | Connection |
|-----|----------|------------|
| **`Ably.Realtime`** | Client needs to **subscribe** to messages, presence, or state changes | Persistent WebSocket |
| **`Ably.Rest`** | Server-side **publish only**, token generation, history queries | Stateless HTTP |

These are the foundation. AI Transport, LiveObjects, and LiveSync all use the core Realtime SDK directly — they are patterns and plugins on top of Pub/Sub, not separate SDKs.

**Layer 2 — Product SDKs** (higher-level abstractions for specific use cases):

| SDK | Purpose |
|-----|---------|
| **`@ably/chat`** | Rooms, typing indicators, reactions, message history, moderation |
| **`@ably/spaces`** | Cursors, avatar stacks, member locations, component locking |

These product SDKs depend on the core Realtime SDK. You pass an `Ably.Realtime` instance when creating them. The underlying Realtime knowledge (auth, channels, presence) still applies.

### Decision Rules

```
Q: Is this server-side or client-side?
├── Server-side:
│   ├── Publishing, token generation, history → Use Ably.Rest (stateless HTTP)
│   └── Need persistent connection (AI token streaming, subscribing) → Use Ably.Realtime
└── Client-side → Use Ably.Realtime, then:
    ├── Building chat? → Use @ably/chat (pass Realtime instance)
    ├── Building collaboration? → Use @ably/spaces (pass Realtime instance)
    ├── Need shared state? → Use LiveObjects plugin with Realtime
    ├── Syncing database? → Use @ably-labs/models with ADBC connector
    └── Otherwise → Use Ably.Realtime directly (Pub/Sub, AI Transport)
```

**Server-side rule of thumb:** Default to `Ably.Rest` for server operations. Only use `Ably.Realtime` on the server when you genuinely need a persistent connection — for example, an AI agent streaming tokens to clients, or a backend service that subscribes to events.

### Common Mistakes

```javascript
// WRONG: Using REST SDK then polling for messages
const rest = new Ably.Rest({ key: '...' });
setInterval(async () => {
  const history = await rest.channels.get('updates').history();
}, 1000);

// RIGHT: Using Realtime SDK to subscribe
const realtime = new Ably.Realtime({ key: '...' });
realtime.channels.get('updates').subscribe((msg) => {
  console.log('Received:', msg.data);
});

// WRONG: Using raw Pub/Sub for chat when Chat SDK exists
const channel = realtime.channels.get('chat-room');
channel.subscribe((msg) => { /* manually handling typing, reactions, history... */ });

// RIGHT: Using Chat SDK which handles all chat patterns
import { ChatClient } from '@ably/chat';
const chat = new ChatClient(realtime);
const room = await chat.rooms.get('my-room');
room.messages.subscribe((msg) => console.log(msg.text));
await room.typing.keystroke(); // built-in typing indicators
```

---

## 2. Use Modern SDK Patterns (v2.x)

Ably's JavaScript SDK v2.x uses async/await. **Never generate callback-style 1.x patterns.**

```javascript
// WRONG: Old 1.x callback pattern (deprecated)
const channel = realtime.channels.get('updates');
channel.subscribe('event', function(message) {
  console.log(message.data);
});
channel.publish('event', { text: 'hello' }, function(err) {
  if (err) console.error(err);
});

// RIGHT: Modern 2.x async/await pattern
const channel = realtime.channels.get('updates');
channel.subscribe('event', (message) => {
  console.log(message.data);
});
await channel.publish('event', { text: 'hello' });
```

**Imports and initialization — keep it simple:**

```javascript
// RIGHT: Standard ESM import
import Ably from 'ably';
const realtime = new Ably.Realtime({ key: 'your-key' });
const rest = new Ably.Rest({ key: 'your-key' });

// RIGHT: Chat SDK import
import { ChatClient } from '@ably/chat';

// WRONG: Don't invent type-based initialization
const options: Ably.Types.ClientOptions = { ... }; // unnecessary
```

If you hit ESM/CommonJS import errors, check that your `tsconfig.json` has `"moduleResolution": "bundler"` or `"node16"`, and that you're importing from `'ably'` (not subpaths). Don't try multiple import strategies — check the [SDK README](https://github.com/ably/ably-js) for your environment.

**Server-side: Default to REST SDK.** Only use `Ably.Realtime` on the server when you need a persistent connection.

```javascript
// WRONG: Realtime SDK on server just to publish
const realtime = new Ably.Realtime({ key: '...' }); // opens WebSocket unnecessarily
await realtime.channels.get('events').publish('update', data);

// RIGHT: REST SDK for server-side publish
const rest = new Ably.Rest({ key: '...' }); // stateless HTTP
await rest.channels.get('events').publish('update', data);

// RIGHT: Realtime on server for AI streaming (message-per-response pattern)
// See ably.com/docs/ai-transport/token-streaming/message-per-response?source=using-ably
const channel = realtime.channels.get('conversation:123');
const { serials: [msgSerial] } = await channel.publish({ name: 'response', data: '' });
for await (const event of llmStream) {
  if (event.type === 'token') {
    channel.appendMessage({ serial: msgSerial, data: event.text });
  }
}
```

---

## 3. Authentication

**API keys are for server-side only. Never expose them to clients.**

API keys don't expire. If leaked, attackers have indefinite access until you regenerate the key.

### Recommended: JWT Authentication

JWT is the recommended authentication method for client-side applications.

**Why JWT over Ably tokens:**
- No round-trip to Ably servers — your backend creates and signs the JWT directly
- Integrates with existing auth systems — uses standard JWT libraries you already have
- Capabilities defined per-token — not limited to what's configured on the API key
- Works everywhere — including environments without an Ably SDK (MQTT, embedded devices)

**JWT Claims:**
- `kid` (header): Your Ably API key name (e.g., `xVLyHw.abcdef`)
- `iat`: Issued-at timestamp (seconds)
- `exp`: Expiration timestamp (seconds)
- `x-ably-capability`: JSON string of channel permissions
- `x-ably-clientId` (optional): Client identity for presence

```javascript
// Server-side: Create JWT for client
import jwt from 'jsonwebtoken';

app.post('/api/ably-auth', (req, res) => {
  const apiKey = process.env.ABLY_API_KEY; // 'appId.keyId:keySecret'
  const [keyName, keySecret] = apiKey.split(':');

  const token = jwt.sign(
    {
      'x-ably-capability': JSON.stringify({
        'room:*': ['subscribe', 'publish', 'presence'],
        [`notifications:${req.user.id}`]: ['subscribe'],
      }),
      'x-ably-clientId': req.user.id,
    },
    keySecret,
    {
      expiresIn: '1h',
      keyid: keyName,
    }
  );

  res.json(token);
});

// Client-side: Use JWT with Ably
const realtime = new Ably.Realtime({
  authUrl: '/api/ably-auth',
  authMethod: 'POST',
});
```

### Alternative: Ably Token Requests

JWT is recommended for most use cases, but Ably tokens may be preferred when your capability list is too large for JWT size limits (JWTs must fit within HTTP headers, ~8KB), or when you need to keep capabilities confidential since JWTs can be decoded by clients. The trade-off is that Ably token integration is more involved and doesn't support all JWT functionality like channel-scoped claims and per-connection rate limits.

```javascript
// Ably's native token system (requires round-trip to Ably servers from backend)
app.post('/api/ably-token', (req, res) => {
  const client = new Ably.Rest({ key: process.env.ABLY_API_KEY });
  client.auth.createTokenRequest({
    clientId: req.user.id,
    capability: { 'room:*': ['subscribe', 'publish'] },
  }).then(tokenRequest => res.json(tokenRequest));
});
```

### Rules
- Server-side: API key is fine (`{ key: 'appId.keyId:keySecret' }`)
- Client-side: Always use `authUrl` or `authCallback` — never embed the API key or pass a static `token` directly (it won't auto-refresh on expiry)
- Set `clientId` if you need presence features — it's required for presence
- Use capabilities to restrict what channels and operations each client can access

---

## 4. Channel Design

Channels separate messages into topics. Get the naming right early — it's hard to change later.

**Rules:**
- Use `:` as a hierarchy separator: `chat:room-123`, `orders:user-456`
- Channel names are case-sensitive
- Don't create one channel per message — channels are long-lived topics
- Use [rules](https://ably.com/docs/channels#rules?source=using-ably) in the dashboard to apply settings (e.g., persistence, push notifications) to groups of channels

**Common patterns:**
```
chat:room-{roomId}           # Chat rooms
notifications:user-{userId}  # Per-user notifications
cursors:doc-{docId}          # Collaborative editing
events:{eventType}           # Event streaming
conversation:{sessionId}     # AI Transport sessions
```

---

## 5. Connection Management

The Realtime SDK manages reconnection automatically. Don't fight it.

**Rules:**
- Don't manually reconnect — the SDK handles transient failures with exponential backoff
- Listen to connection state changes to update UI:

```javascript
realtime.connection.on('connected', () => { /* online */ });
realtime.connection.on('disconnected', () => { /* temporarily offline */ });
realtime.connection.on('suspended', () => { /* offline for extended period */ });
```

- Call `realtime.close()` when done (component unmount, page unload, etc.)
- Messages published while disconnected are received on reconnection (within the 2-minute recovery window)
- For AI Transport (client-side): use channel `rewind` to hydrate returning clients with recent messages:

```javascript
const channel = realtime.channels.get('conversation:123', {
  params: { rewind: '2m' }  // Replay last 2 minutes on attach
});
```

---

## 6. Presence

Presence tracks which clients are on a channel. Use it for "who's online" features.

**Rules:**
- Set `clientId` during auth — it's required for presence
- Call `channel.presence.enter()` to join, `channel.presence.update()` to update data, `channel.presence.leave()` to depart
- Use `channel.presence.get()` for current members, `channel.presence.subscribe()` for changes
- If a client disconnects ungracefully, Ably removes them after ~15 seconds (not instantly)
- Don't use presence for high-frequency data (cursor positions, typing coordinates) — use channels instead. Presence is for low-frequency state (online/offline, user status)
- For Chat: use `room.presence` instead of raw channel presence
- For Spaces: use `space.enter()` / `useMembers()` hook. Spaces has dedicated `cursors` API for cursor positions

---

## 7. Chat SDK: Critical Lifecycle

If using `@ably/chat`, these are the most common mistakes:

**Always subscribe before calling `attach()`.** Attaching without subscribing first causes silent message loss — the worst kind of bug.

```javascript
const room = await chat.rooms.get('my-room');

// WRONG: Attach without subscribing first — messages silently lost
await room.attach();
room.messages.subscribe((msg) => console.log(msg.text)); // may miss messages during attach

// RIGHT: Subscribe first, then attach
room.messages.subscribe((msg) => console.log(msg.text));
await room.attach();
```

**Use the actual API.** The Chat SDK does NOT have: threading, read receipts, file attachments, or `room.messages.broadcast()`. Use `room.messages.send()` to send messages.

**Don't mix Chat and Pub/Sub patterns.** If you're using `@ably/chat`, use `room.messages`, `room.typing`, `room.reactions` — not raw `channel.subscribe()` / `channel.publish()`.

**Built-in behavior you don't need to reimplement:**
- Typing indicator frequency control is handled by the SDK automatically
- Room reactions delivery is handled by the SDK
- Message ordering and history pagination are built-in

---

## 8. React Integration

Ably provides React hooks for each product:

| Product | Package | Key Hooks |
|---------|---------|-----------|
| Pub/Sub | `ably/react` | `useChannel`, `usePresence`, `useConnectionStateListener` |
| Chat | `@ably/chat/react` | `useMessages`, `useTyping`, `usePresence`, `useRoomReactions` |
| Spaces | `@ably/spaces/react` | `useMembers`, `useCursors`, `useLocations`, `useLocks` |

**Critical rule: Don't create a new Ably client on every render.** This creates a new WebSocket connection each time — a memory leak.

```javascript
// WRONG: Creates new connection every render — memory leak
function Chat() {
  const ably = new Ably.Realtime({ authUrl: '/api/ably-auth' });
  // ...
}

// RIGHT: Create client once, pass via provider
const ably = new Ably.Realtime({ authUrl: '/api/ably-auth' });

function App() {
  return (
    <AblyProvider client={ably}>
      <ChannelProvider channelName="chat:room-1">
        <Chat />
      </ChannelProvider>
    </AblyProvider>
  );
}

// ALSO RIGHT: Create in useEffect with proper cleanup
function App() {
  const [client, setClient] = useState(null);
  useEffect(() => {
    const ably = new Ably.Realtime({ authUrl: '/api/ably-auth' });
    setClient(ably);
    return () => ably.close();
  }, []);
  // ...
}
```

---

## 9. Spaces and LiveObjects: Built-in Behavior

When using **Spaces** (`@ably/spaces`):
- Cursor position batching is built-in — don't implement custom throttling
- Member location tracking is built-in via `space.locations`
- Component locking handles contention automatically via `space.locks`

When using **LiveObjects**:
- Available data structures are Maps and Counters only (no custom object types)
- Conflict resolution is built-in — don't implement your own
- State recovery after reconnection is automatic
- Prefer the path-based API over the instance API for simplicity

---

## 10. LiveSync: Database-to-Frontend

LiveSync connects your database to frontends: Database → ADBC Connector → Ably Channels → Models SDK → Frontend.

**Key constraints:** PostgreSQL requires logical replication (14+, WAL level change needs restart). MongoDB requires a replica set (no standalone). The Database Connector handles channel mapping automatically once you configure an ingress rule.

**Always fetch current LiveSync docs** from [ably.com/docs/livesync](https://ably.com/docs/livesync?source=using-ably) — database permissions and connector configuration change across versions.

---

## 11. Production Checklist

Before going to production, verify:

- [ ] **No API keys in client code** — use JWT or token auth via `authUrl`/`authCallback`
- [ ] **Capabilities are scoped** — don't grant `{"*":["*"]}` to clients; restrict to specific channels and operations
- [ ] **Connection cleanup** — call `realtime.close()` on unmount/unload to avoid connection leaks
- [ ] **Error handling** — listen to `connection.on('failed')` and handle auth failures gracefully
- [ ] **Channel detach** — detach from channels you no longer need (`channel.detach()`)
- [ ] **Message size** — messages are limited to 64KB by default; if you're hitting this, split payloads or reconsider message design
- [ ] **Idempotent publishing** — set unique message IDs when exactly-once delivery matters
- [ ] **`echoMessages: false`** — set this if publishers don't need to receive their own messages (saves bandwidth and cost)
- [ ] **Rate limits** — Ably enforces rate limits (e.g., 50 messages/second per channel, 200 channels per connection). If you're hitting them, check your publish frequency and channel fan-out. Read the [limits documentation](https://ably.com/docs/general/limits?source=using-ably)

### Error Handling

Ably error codes can be broad (e.g., 40000, 50000) — always read the error **message text**, not just the code. Every error code has a help page at `https://help.ably.io/error/{code}`.

---

## 12. Quick Reference

**Product docs:** [Pub/Sub](https://ably.com/docs/pubsub?source=using-ably) | [Chat](https://ably.com/docs/chat?source=using-ably) | [Spaces](https://ably.com/docs/spaces?source=using-ably) | [LiveObjects](https://ably.com/docs/liveobjects?source=using-ably) | [LiveSync](https://ably.com/docs/livesync?source=using-ably) | [AI Transport](https://ably.com/docs/ai-transport?source=using-ably)

**Platform SDKs:** JavaScript, React, Python, Ruby, Java, Kotlin, Swift, .NET, Go, PHP, Flutter — [ably.com/docs/sdks](https://ably.com/docs/sdks?source=using-ably)

**Ably CLI:** Install with `npm install -g @ably/cli` to publish test messages, subscribe to channels, and verify setup. Run `ably --help` to discover commands.

For API references, start at [ably.com/docs](https://ably.com/docs?source=using-ably).
