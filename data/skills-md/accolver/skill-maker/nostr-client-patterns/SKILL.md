---
name: nostr-client-patterns
description: Implement Nostr client architecture including relay pool management, subscription lifecycle with EOSE/CLOSED handling, event deduplication, optimistic UI for publishing, and reconnection strategies. Use when building Nostr clients, managing WebSocket relay connections, handling subscription state machines, implementing event caches, or debugging relay communication issues like missed events or broken reconnections.
---

# Nostr Client Patterns

## Overview

Implement robust Nostr client architecture. This skill covers the patterns
agents miss: relay pool connection management, subscription state machines that
correctly handle EOSE/CLOSED transitions, event deduplication across relays,
optimistic UI with OK message error recovery, and reconnection with gap-free
event delivery.

## When to Use

- Building a Nostr client that connects to multiple relays
- Implementing relay pool management (connection lifecycle, backoff)
- Managing subscription state (loading vs live, EOSE transitions)
- Deduplicating events received from multiple relays
- Implementing optimistic UI for event publishing
- Handling OK/EOSE/CLOSED/NOTICE relay messages correctly
- Building reconnection logic that doesn't lose events
- Caching events locally for offline or fast-load scenarios

**Do NOT use when:**

- Constructing event JSON structures (use nostr-event-builder)
- Building relay server software (this is client-side patterns)
- Working with NIP-19 encoding/decoding (bech32 concerns)
- Designing subscription filters (use nostr-filter-designer)

## Workflow

### 1. Design the Relay Pool

A relay pool manages WebSocket connections to multiple relays. Each relay
connection has a lifecycle that must be tracked independently.

**Connection states:**

```
disconnected → connecting → connected → disconnecting → disconnected
                    ↓                        ↑
                  failed ──(backoff)──→ connecting
```

**Key rules:**

- **One WebSocket per relay** (NIP-01). Never open parallel connections to the
  same relay URL.
- Normalize relay URLs before comparing: lowercase scheme/host, remove trailing
  slash, default port 443 for wss.
- Track state per relay:
  `{ url, ws, state, retryCount, lastConnected,
  activeSubscriptions, pendingPublishes }`.
- Implement connection limits (e.g., max 10 concurrent connections).
- Use NIP-65 relay lists (kind:10002) to determine which relays to connect to
  for each user. Write relays for fetching a user's events, read relays for
  fetching events that mention them.

```typescript
interface RelayConnection {
  url: string;
  ws: WebSocket | null;
  state: "disconnected" | "connecting" | "connected" | "disconnecting";
  retryCount: number;
  lastConnectedAt: number | null;
  lastEoseTimestamps: Map<string, number>; // subId → timestamp
  authChallenge: string | null;
}
```

See [references/relay-pool.md](references/relay-pool.md) for full implementation
patterns including backoff and NIP-42 auth.

### 2. Implement the Subscription Lifecycle

Subscriptions follow a state machine with distinct phases. Getting this wrong
causes either missing events or infinite loading states.

**Subscription states:**

```
idle → loading → live → closed
                  ↑       ↓
                  └─ replacing (new REQ with same sub-id)
```

**The lifecycle:**

1. **Open:** Send `["REQ", "<sub-id>", <filters...>]` to relay(s)
2. **Loading (stored events):** Receive `["EVENT", "<sub-id>", <event>]` for
   historical matches. UI shows loading indicator.
3. **EOSE received:** `["EOSE", "<sub-id>"]` — transition from "loading" to
   "live". Remove loading indicator, display stored events.
4. **Live events:** Continue receiving EVENTs. These are new, real-time events.
   Display immediately.
5. **Close:** Send `["CLOSE", "<sub-id>"]` when the view unmounts or the
   subscription is no longer needed.

**Critical transitions:**

- **EOSE is per-relay.** If subscribed to 5 relays, you get 5 EOSE messages.
  Track EOSE per relay per subscription. Transition to "live" when ALL relays
  have sent EOSE (or timed out).
- **Replacing:** Send a new REQ with the same sub-id to change filters without
  closing. The relay replaces the old subscription. Reset EOSE tracking.
- **CLOSED from relay:** `["CLOSED", "<sub-id>", "<reason>"]` means the relay
  terminated your subscription. Handle by reason prefix:
  - `auth-required:` → authenticate with NIP-42, then re-subscribe
  - `error:` → log error, maybe retry after backoff
  - `restricted:` → user lacks permission, don't retry
- **Timeout:** If a relay doesn't send EOSE within a reasonable time (e.g.,
  10s), treat it as EOSE for that relay to avoid infinite loading.

See [references/subscription-patterns.md](references/subscription-patterns.md)
for state machine implementation and multi-relay coordination.

### 3. Deduplicate Events

The same event can arrive from multiple relays. Events have globally unique IDs
(SHA-256 of serialized content), so deduplication is straightforward.

**Regular events (kinds 1-9999 excluding replaceable):**

```typescript
const seen = new Set<string>();

function processEvent(event: NostrEvent): boolean {
  if (seen.has(event.id)) return false; // duplicate
  seen.add(event.id);
  // process event...
  return true;
}
```

**Replaceable events (kinds 0, 3, 10000-19999):**

Keep only the latest per `pubkey + kind`. When a newer event arrives, replace
the old one. Break ties by lowest `id` (lexicographic comparison).

```typescript
const replaceableKey = `${event.pubkey}:${event.kind}`;
const existing = replaceableStore.get(replaceableKey);
if (existing) {
  if (event.created_at < existing.created_at) return false;
  if (event.created_at === existing.created_at && event.id >= existing.id) {
    return false;
  }
}
replaceableStore.set(replaceableKey, event);
```

**Addressable events (kinds 30000-39999):**

Same as replaceable, but key includes the `d` tag value:

```typescript
const dTag = event.tags.find((t) => t[0] === "d")?.[1] ?? "";
const addressableKey = `${event.pubkey}:${event.kind}:${dTag}`;
```

**Memory management:** Use an LRU cache or periodic cleanup for the `seen` set.
In long-running clients, unbounded sets will leak memory.

### 4. Implement Optimistic UI for Publishing

Show events immediately in the UI before relay confirmation. Handle failures
gracefully.

**The flow:**

```
User action → Create event → Show in UI (optimistic) → Sign → Publish
                                                                  ↓
                                                          Wait for OK
                                                         ↙          ↘
                                                   OK:true        OK:false
                                                   Confirm        Show error
                                                                  Allow retry
```

**Implementation:**

1. Create the unsigned event from user input
2. Add to local state with status `"pending"`
3. Sign the event (NIP-07 browser extension or local key)
4. Send `["EVENT", <signed-event>]` to connected relays
5. Track OK responses per relay:
   - `["OK", "<id>", true, ""]` → mark relay as confirmed
   - `["OK", "<id>", true, "duplicate:"]` → also success (relay already had it)
   - `["OK", "<id>", false, "reason"]` → track failure reason
6. Update UI status:
   - At least one `true` → status `"confirmed"`
   - All relays responded `false` → status `"failed"`, show error, allow retry
   - Timeout (e.g., 10s) with no OK → status `"timeout"`, allow retry

**OK message reason prefixes:**

| Prefix           | Meaning                | Action                   |
| ---------------- | ---------------------- | ------------------------ |
| `duplicate:`     | Already have it        | Treat as success         |
| `pow:`           | Proof of work issue    | Add PoW and retry        |
| `blocked:`       | Client/user blocked    | Show error, don't retry  |
| `rate-limited:`  | Too many events        | Backoff and retry        |
| `invalid:`       | Protocol violation     | Fix event and retry      |
| `restricted:`    | Permission denied      | Show error, don't retry  |
| `auth-required:` | Need NIP-42 auth first | Authenticate, then retry |
| `error:`         | General relay error    | Retry after backoff      |

### 5. Handle Reconnection

When a relay disconnects, reconnect without losing events or duplicating
subscriptions.

**Reconnection strategy:**

1. Detect disconnect (WebSocket `close` or `error` event)
2. Set relay state to `disconnected`
3. Calculate backoff: `min(baseDelay * 2^retryCount + jitter, maxDelay)`
   - Recommended: base=1s, max=60s, jitter=0-1s random
4. After backoff, set state to `connecting`, open new WebSocket
5. On successful connect:
   - Reset `retryCount` to 0
   - Re-authenticate if relay previously required NIP-42 auth
   - Re-send all active subscriptions with `since` parameter set to the last
     EOSE timestamp for that relay + subscription
6. On failed connect: increment `retryCount`, go to step 3

**Gap-free event delivery:**

The key insight: track the `created_at` of the last event received before
disconnect (or the EOSE timestamp). On reconnect, add `since: lastTimestamp` to
the filter to fetch only events you missed. This avoids re-fetching the entire
history.

```typescript
function reconnectSubscription(
  relay: RelayConnection,
  subId: string,
  originalFilter: Filter,
) {
  const lastSeen = relay.lastEoseTimestamps.get(subId);
  const reconnectFilter = lastSeen
    ? { ...originalFilter, since: lastSeen }
    : originalFilter;
  relay.ws.send(JSON.stringify(["REQ", subId, reconnectFilter]));
}
```

### 6. Cache Events Locally

Reduce bandwidth and improve load times by caching events.

**Cache strategies:**

- **IndexedDB** (browser): Store events by id, index by kind, pubkey,
  created_at. Good for offline-first clients.
- **SQLite** (desktop/mobile): Same schema, better query performance.
- **In-memory LRU** (ephemeral): For deduplication and short-term caching.

**Cache-first loading pattern:**

1. Load cached events matching the filter → display immediately
2. Open subscription with `since: latestCachedTimestamp`
3. Merge new events into cache and UI
4. On EOSE, cache is now up-to-date

**For replaceable events:** Only cache the latest version. When a newer version
arrives, replace the cached entry.

## Checklist

- [ ] Relay pool tracks per-relay connection state with proper lifecycle
- [ ] One WebSocket per relay URL (normalized)
- [ ] Exponential backoff with jitter on reconnection
- [ ] Subscriptions track EOSE per relay, transition loading → live correctly
- [ ] CLOSED messages handled by reason prefix (auth, error, restricted)
- [ ] Events deduplicated by id before processing
- [ ] Replaceable events keep only latest (by created_at, then lowest id)
- [ ] Optimistic UI shows events before relay confirmation
- [ ] OK messages parsed with reason prefix for error handling
- [ ] Reconnection re-subscribes with `since` to avoid gaps
- [ ] Event cache used for faster initial loads

## Common Mistakes

| Mistake                                   | Why It Breaks                                              | Fix                                                         |
| ----------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------- |
| Opening multiple WebSockets to same relay | Violates NIP-01, wastes resources, causes duplicate events | Normalize URL and enforce one connection per relay          |
| Treating EOSE as global (not per-relay)   | Loading state never resolves if one relay is slow          | Track EOSE per relay per subscription, use timeout fallback |
| No deduplication of events                | Same event processed multiple times, corrupts counts/UI    | Deduplicate by `event.id` using a Set before processing     |
| Replacing events by `created_at` only     | Tie-breaking is undefined without `id` comparison          | On equal `created_at`, keep the event with the lowest `id`  |
| Showing "failed" on `duplicate:` OK       | Duplicate means the relay already has it — that's success  | Check the reason prefix, not just the boolean               |
| Fixed retry delay (no backoff)            | Hammers relay during outages, may get IP-banned            | Use exponential backoff: `min(base * 2^n + jitter, max)`    |
| Not re-authenticating after reconnect     | NIP-42 auth is per-connection, lost on disconnect          | Store challenge, re-send AUTH event after reconnect         |
| Reconnecting without `since` filter       | Re-fetches entire history, wastes bandwidth                | Track last EOSE timestamp, use `since` on reconnect         |
| Unbounded dedup Set                       | Memory leak in long-running clients                        | Use LRU cache or periodic cleanup                           |
| Ignoring CLOSED messages                  | Subscription silently stops receiving events               | Handle CLOSED, re-subscribe if appropriate                  |

## Quick Reference

| Message        | Direction    | Format                       | Purpose                 |
| -------------- | ------------ | ---------------------------- | ----------------------- |
| `REQ`          | Client→Relay | `["REQ", subId, ...filters]` | Subscribe to events     |
| `EVENT` (send) | Client→Relay | `["EVENT", event]`           | Publish an event        |
| `CLOSE`        | Client→Relay | `["CLOSE", subId]`           | End a subscription      |
| `AUTH`         | Client→Relay | `["AUTH", signedEvent]`      | Authenticate (NIP-42)   |
| `EVENT` (recv) | Relay→Client | `["EVENT", subId, event]`    | Deliver matching event  |
| `OK`           | Relay→Client | `["OK", eventId, bool, msg]` | Publish acknowledgment  |
| `EOSE`         | Relay→Client | `["EOSE", subId]`            | End of stored events    |
| `CLOSED`       | Relay→Client | `["CLOSED", subId, msg]`     | Subscription terminated |
| `NOTICE`       | Relay→Client | `["NOTICE", msg]`            | Human-readable info     |
| `AUTH`         | Relay→Client | `["AUTH", challenge]`        | Auth challenge (NIP-42) |

## Key Principles

1. **One connection per relay** — Normalize URLs and enforce a single WebSocket
   per relay. Multiple connections cause duplicate events, wasted bandwidth, and
   violate NIP-01.

2. **EOSE is the loading/live boundary** — Before EOSE, you're receiving stored
   history. After EOSE, you're receiving live events. This distinction drives UI
   state (loading spinners, "new event" indicators).

3. **Deduplicate before processing** — Events have globally unique IDs. Check
   the dedup set before any processing, state updates, or UI rendering. For
   replaceable events, also compare `created_at` and `id` for tie-breaking.

4. **Optimistic with recovery** — Show events immediately, confirm via OK. Parse
   OK reason prefixes to distinguish retriable errors (rate-limited, auth) from
   permanent failures (blocked, restricted).

5. **Reconnect without gaps** — Track the last-seen timestamp per relay per
   subscription. On reconnect, use `since` to fetch only missed events. Always
   re-authenticate and re-subscribe after reconnection.
