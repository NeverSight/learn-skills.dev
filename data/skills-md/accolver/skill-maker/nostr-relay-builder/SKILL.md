---
name: nostr-relay-builder
description: Build a Nostr relay from scratch with WebSocket handling, NIP-01 event validation (id computation, Schnorr signature verification), filter matching, subscription management, and progressive NIP support (NIP-11, NIP-09, NIP-42, NIP-50). Use when building a Nostr relay, implementing the Nostr relay protocol, handling Nostr WebSocket connections, validating Nostr events, matching Nostr filters, or adding NIP support to a relay. Also use when the user mentions relay development, nostr server, event storage, or subscription handling.
---

# Nostr Relay Builder

Build a Nostr relay from scratch: WebSocket server, NIP-01 message protocol,
event validation (id + signature), filter matching, subscription management, and
progressive NIP support.

## Overview

A Nostr relay is a WebSocket server that receives, validates, stores, and
distributes events. This skill walks through building one step by step, starting
with the mandatory NIP-01 protocol and progressively adding optional NIPs.

## When to use

- When building a Nostr relay from scratch
- When adding NIP support to an existing relay
- When implementing event validation (id computation, signature verification)
- When building filter matching logic for Nostr subscriptions
- When handling WebSocket connections for the Nostr protocol
- When implementing replaceable/addressable event storage

**Do NOT use when:**

- Building a Nostr client (use nostr-client-patterns instead)
- Working only with event creation/signing (use nostr-event-builder instead)
- Setting up NIP-05 verification (use nostr-nip05-setup instead)

## Workflow

### 1. Set up the WebSocket server

Create a WebSocket endpoint that accepts connections. The relay MUST:

- Accept WebSocket upgrade requests on the root path
- Handle multiple concurrent connections
- Track per-connection state (subscriptions, auth status)
- Implement ping/pong for connection health
- Parse incoming messages as JSON arrays

```typescript
// Bun example — minimal WebSocket server
Bun.serve({
  port: 3000,
  fetch(req, server) {
    // NIP-11: serve relay info on HTTP GET with Accept: application/nostr+json
    if (req.headers.get("Accept") === "application/nostr+json") {
      return Response.json(relayInfo, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Headers": "Accept",
          "Access-Control-Allow-Methods": "GET",
        },
      });
    }
    if (server.upgrade(req)) return;
    return new Response("Connect via WebSocket", { status: 400 });
  },
  websocket: {
    open(ws) {
      ws.data = { subscriptions: new Map() };
    },
    message(ws, raw) {
      handleMessage(ws, JSON.parse(raw));
    },
    close(ws) {/* cleanup subscriptions */},
  },
});
```

### 2. Implement the NIP-01 message protocol

Handle the three client message types and respond with the five relay message
types. See [references/message-protocol.md](references/message-protocol.md) for
the complete format reference.

```typescript
function handleMessage(ws, msg: unknown[]) {
  const verb = msg[0];
  switch (verb) {
    case "EVENT":
      return handleEvent(ws, msg[1]);
    case "REQ":
      return handleReq(ws, msg[1], msg.slice(2));
    case "CLOSE":
      return handleClose(ws, msg[1]);
    default:
      return send(ws, ["NOTICE", `unknown message type: ${verb}`]);
  }
}
```

**Critical rules:**

- `EVENT` → always respond with `OK` (true/false + message)
- `REQ` → send matching stored events, then `EOSE`, then stream new matches
- `CLOSE` → remove the subscription, no response required
- Subscription IDs are per-connection, max 64 chars, non-empty strings
- A new `REQ` with an existing subscription ID replaces the old subscription

### 3. Implement event validation

Every received event MUST be validated before storage. Follow the checklist in
[references/event-validation.md](references/event-validation.md). The two
critical checks:

**ID verification** — recompute and compare:

```typescript
import { sha256 } from "@noble/hashes/sha256";
import { bytesToHex } from "@noble/hashes/utils";

function computeEventId(event): string {
  const serialized = JSON.stringify([
    0,
    event.pubkey,
    event.created_at,
    event.kind,
    event.tags,
    event.content,
  ]);
  return bytesToHex(sha256(new TextEncoder().encode(serialized)));
}
```

**Signature verification** — Schnorr over secp256k1:

```typescript
import { schnorr } from "@noble/curves/secp256k1";

function verifySignature(event): boolean {
  return schnorr.verify(event.sig, event.id, event.pubkey);
}
```

If validation fails, respond with
`["OK", event.id, false, "invalid: <reason>"]`.

### 4. Implement filter matching

Filters determine which events match a subscription. The logic is:

- **Within a single filter:** all specified conditions must match (AND)
- **Across multiple filters in a REQ:** any filter matching is sufficient (OR)
- **List fields** (ids, authors, kinds, #tags): event value must be in the list
  (OR within field)

```typescript
function matchesFilter(event, filter): boolean {
  if (filter.ids && !filter.ids.includes(event.id)) return false;
  if (filter.authors && !filter.authors.includes(event.pubkey)) return false;
  if (filter.kinds && !filter.kinds.includes(event.kind)) return false;
  if (filter.since && event.created_at < filter.since) return false;
  if (filter.until && event.created_at > filter.until) return false;

  // Tag filters: #e, #p, #a, etc.
  for (const [key, values] of Object.entries(filter)) {
    if (key.startsWith("#") && key.length === 2) {
      const tagName = key.slice(1);
      const eventTagValues = event.tags
        .filter((t) => t[0] === tagName)
        .map((t) => t[1]);
      if (!values.some((v) => eventTagValues.includes(v))) return false;
    }
  }
  return true;
}
```

**`limit` handling:** only applies to the initial query (not streaming). Return
the newest `limit` events, ordered by `created_at` descending. On ties, lowest
`id` (lexicographic) first.

### 5. Implement event storage with kind-based rules

Different kind ranges have different storage semantics:

| Kind Range            | Type        | Storage Rule                                     |
| --------------------- | ----------- | ------------------------------------------------ |
| 1, 2, 4-44, 1000-9999 | Regular     | Store all events                                 |
| 0, 3, 10000-19999     | Replaceable | Keep only latest per `pubkey` + `kind`           |
| 20000-29999           | Ephemeral   | Do NOT store; broadcast only                     |
| 30000-39999           | Addressable | Keep only latest per `pubkey` + `kind` + `d` tag |

For replaceable/addressable events with the same `created_at`, keep the one with
the lowest `id` (lexicographic order).

```typescript
function getEventDTag(event): string {
  const dTag = event.tags.find((t) => t[0] === "d");
  return dTag ? dTag[1] : "";
}

function isReplaceable(kind: number): boolean {
  return kind === 0 || kind === 3 || (kind >= 10000 && kind < 20000);
}

function isAddressable(kind: number): boolean {
  return kind >= 30000 && kind < 40000;
}

function isEphemeral(kind: number): boolean {
  return kind >= 20000 && kind < 30000;
}
```

### 6. Implement subscription management

Track active subscriptions per connection:

```typescript
function handleReq(ws, subId: string, filters: object[]) {
  if (!subId || subId.length > 64) {
    return send(ws, ["CLOSED", subId, "invalid: bad subscription id"]);
  }

  // Replace existing subscription with same ID
  ws.data.subscriptions.set(subId, filters);

  // Query stored events matching any filter
  const matches = queryEvents(filters);
  for (const event of matches) {
    send(ws, ["EVENT", subId, event]);
  }
  send(ws, ["EOSE", subId]);

  // New events will be checked against this subscription in real-time
}

function handleClose(ws, subId: string) {
  ws.data.subscriptions.delete(subId);
}
```

When a new event is stored, broadcast it to all connections with matching
subscriptions (skip the `limit` check — it only applies to initial queries).

### 7. Add progressive NIP support

After NIP-01 is solid, add NIPs in this order:

**NIP-11 — Relay information document:** Serve JSON at the WebSocket URL when
the HTTP request has `Accept: application/nostr+json`. Must include CORS
headers. See the example in Step 1.

**NIP-09 — Event deletion:** Handle kind 5 events. Delete referenced events (by
`e` and `a` tags) only if the deletion request's `pubkey` matches the referenced
event's `pubkey`.

**NIP-42 — Client authentication:** Send `["AUTH", "<challenge>"]` to clients.
Accept `["AUTH", <signed-event>]` responses. The auth event must be kind 22242
with `relay` and `challenge` tags. Verify `created_at` is within ~10 minutes.
Use `auth-required:` prefix in OK/CLOSED messages when auth is needed.

**NIP-45 — Event counting:** Handle `["COUNT", subId, ...filters]` messages.
Respond with `["COUNT", subId, {"count": N}]`.

**NIP-50 — Search:** Support a `search` field in filters. Implement full-text
search over event `content`.

## Checklist

- [ ] WebSocket server accepts connections and parses JSON arrays
- [ ] EVENT messages are validated (id + signature) and stored
- [ ] OK responses sent for every EVENT (true/false + prefix message)
- [ ] REQ creates subscriptions, returns matching events + EOSE
- [ ] CLOSE removes subscriptions
- [ ] Filter matching handles ids, authors, kinds, #tags, since, until, limit
- [ ] Replaceable events (kind 0, 3, 10000-19999) keep only latest per
      pubkey+kind
- [ ] Addressable events (kind 30000-39999) keep only latest per
      pubkey+kind+d-tag
- [ ] Ephemeral events (kind 20000-29999) are broadcast but not stored
- [ ] New events broadcast to connections with matching subscriptions
- [ ] NIP-11 info document served on HTTP GET with correct Accept header

## Common Mistakes

| Mistake                                          | Fix                                                                             |
| ------------------------------------------------ | ------------------------------------------------------------------------------- |
| Computing event ID with whitespace in JSON       | Use `JSON.stringify` with no spacer argument — zero whitespace                  |
| Forgetting to verify signature after ID check    | Both checks are mandatory; an event with valid ID but bad sig is invalid        |
| Applying `limit` to streaming events             | `limit` only applies to the initial stored-event query, not real-time           |
| Storing ephemeral events (kind 20000-29999)      | Ephemeral events must be broadcast only, never persisted                        |
| Using global subscription IDs                    | Subscription IDs are scoped per WebSocket connection                            |
| Not replacing subscription on duplicate REQ ID   | A new REQ with the same sub ID must replace the old subscription                |
| Missing CORS headers on NIP-11 response          | NIP-11 requires `Access-Control-Allow-Origin: *` and related headers            |
| Tag filter matching all tag elements             | Only the first value (index 1) of each tag is indexed/matched                   |
| Returning OK without the machine-readable prefix | Failed OK messages must use prefixes: `invalid:`, `duplicate:`, `error:`, etc.  |
| Not handling replaceable event timestamp ties    | When `created_at` is equal, keep the event with the lowest `id` (lexicographic) |

## Quick Reference

| Message        | Direction      | Format                                  |
| -------------- | -------------- | --------------------------------------- |
| EVENT (client) | Client → Relay | `["EVENT", <event>]`                    |
| REQ            | Client → Relay | `["REQ", <sub_id>, <filter1>, ...]`     |
| CLOSE          | Client → Relay | `["CLOSE", <sub_id>]`                   |
| EVENT (relay)  | Relay → Client | `["EVENT", <sub_id>, <event>]`          |
| OK             | Relay → Client | `["OK", <event_id>, <bool>, <message>]` |
| EOSE           | Relay → Client | `["EOSE", <sub_id>]`                    |
| CLOSED         | Relay → Client | `["CLOSED", <sub_id>, <message>]`       |
| NOTICE         | Relay → Client | `["NOTICE", <message>]`                 |
| AUTH (relay)   | Relay → Client | `["AUTH", <challenge>]`                 |
| AUTH (client)  | Client → Relay | `["AUTH", <signed-event>]`              |

| OK Prefix        | Meaning                                         |
| ---------------- | ----------------------------------------------- |
| `duplicate:`     | Event already stored                            |
| `invalid:`       | Failed validation (bad id, bad sig, bad format) |
| `blocked:`       | Pubkey or IP is blocked                         |
| `rate-limited:`  | Too many events                                 |
| `restricted:`    | Not authorized to write                         |
| `pow:`           | Proof-of-work related                           |
| `error:`         | Internal relay error                            |
| `auth-required:` | Must authenticate first (NIP-42)                |

## Key Principles

1. **Validate everything** — Never store an event without verifying both the id
   (SHA-256 of canonical serialization) and the signature (Schnorr secp256k1). A
   relay that skips validation poisons the network.

2. **OK is mandatory** — Every EVENT from a client MUST receive an OK response,
   whether accepted or rejected. Silent drops break client retry logic.

3. **Subscriptions are per-connection** — Never share subscription state across
   WebSocket connections. Each connection maintains its own subscription map.

4. **Kind semantics are non-negotiable** — Replaceable events (0, 3,
   10000-19999) keep only the latest. Addressable events (30000-39999) key on
   pubkey+kind+d-tag. Ephemeral events (20000-29999) are never stored. Getting
   this wrong corrupts user data.

5. **Progressive enhancement** — Start with NIP-01 only. Add NIPs one at a time,
   updating `supported_nips` in the NIP-11 info document as you go. A relay that
   does NIP-01 perfectly is more useful than one that does 10 NIPs poorly.
