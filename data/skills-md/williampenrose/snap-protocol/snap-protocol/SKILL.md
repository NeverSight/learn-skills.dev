---
name: snap-protocol
description: "SNAP (Signed Network Agent Protocol) for decentralized agent-to-agent communication. Covers: identity (Bitcoin P2TR addresses), message format, authentication (BIP-340 Schnorr signatures), methods, task states, Agent Cards, error codes, and Nostr-based discovery. Use when the user mentions SNAP protocol, agent identity, P2TR addresses, or agent-to-agent messaging."
---

# SNAP Protocol

Decentralized agent-to-agent communication with self-sovereign identity.

## Identity

Every agent is identified by a Bitcoin P2TR (Pay-to-Taproot) address derived from a private key using BIP-341 taproot tweak.

P2TR address rules:
- Exactly 62 characters
- Prefix: `bc1p` (mainnet) or `tb1p` (testnet)
- Bech32m encoded, witness version 1
- Encodes the BIP-341 tweaked output key (not the internal key)

Key derivation flow:
```
Private Key (32 bytes)
    ├─→ Internal Key (P)  → hex pubkey (used by Nostr)
    └─→ Internal Key (P)  → Taproot Tweak → Output Key (Q) → Bech32m → P2TR address
```

Important: `publicKeyToP2TR()` and `p2trToPublicKey()` are NOT inverses. The taproot tweak is irreversible — you cannot recover the Nostr pubkey from a P2TR address.

## Message Format

Every SNAP message is a JSON object with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique message ID (1-128 chars, `[a-zA-Z0-9_-]`) |
| `version` | string | Protocol version, must be `"0.1"` |
| `from` | string | Sender P2TR address |
| `to` | string | Recipient P2TR address. **Optional** — omit for Agent-to-Service (e.g. `service/call`). |
| `type` | string | `request`, `response`, or `event` |
| `method` | string | Method name (e.g. `message/send`) |
| `payload` | object | Method-specific data (max 1 MB, max depth 10) |
| `timestamp` | integer | Unix seconds (UTC), must be within ±60s of current time |
| `sig` | string | 128 hex chars (64-byte BIP-340 Schnorr signature, signs with tweaked key) |

## Authentication

Messages are signed using BIP-340 Schnorr signatures with the taproot-tweaked private key. The signature covers a canonical JSON serialization of all message fields (excluding `sig`).

Verification steps:
1. Extract tweaked output key Q from the `from` P2TR address
2. Reconstruct canonical signing payload from message fields
3. Verify BIP-340 Schnorr signature against Q

## Methods

| Method | Type | Description |
|--------|------|-------------|
| `message/send` | request-response | Single message exchange |
| `message/stream` | streaming | Streaming response (chunks) |
| `tasks/send` | request-response | Create a new task |
| `tasks/get` | request-response | Get task status |
| `tasks/cancel` | request-response | Cancel a running task |
| `tasks/resubscribe` | streaming | Resume a task stream |
| `service/call` | Agent→Service | Call an HTTP service capability |
| `agent/card` | request-response | Get agent's capability card |
| `agent/ping` | request-response | Health check |

Custom methods MAY be used as long as they match `^[a-z]+/[a-z_]+$`.

## Task States

```
submitted → working → completed
                   → failed
                   → canceled
         → input_required → working (after user responds)
```

| State | Description |
|-------|-------------|
| `submitted` | Queued, not yet started |
| `working` | Currently processing |
| `input_required` | Waiting for user input |
| `completed` | Finished successfully |
| `failed` | Finished with error |
| `canceled` | Canceled by user |

## Agent Card

An Agent Card describes an agent's identity, capabilities, endpoints, and skills. Published as a Nostr replaceable event (kind 31337) for discovery.

Required fields: `name`, `description`, `version`, `identity` (P2TR), `skills`, `defaultInputModes`, `defaultOutputModes`.

Optional fields: `endpoints` (HTTP/WS URLs), `nostrRelays`, `protocolVersion`, `capabilities` (streaming, push), `provider`, `trust`, `iconUrl`.

## Critical Constraints

| Field | Rule |
|-------|------|
| P2TR address | Exactly 62 chars, prefix `bc1p` or `tb1p` |
| Message ID | 1-128 chars, `[a-zA-Z0-9_-]` only |
| Timestamp | Unix seconds, ±60s from current time |
| Signature | 128 lowercase hex chars (64-byte Schnorr, BIP-340) |
| Version | Must be `"0.1"` |
| Payload | Max 1 MB serialized, max depth 10 |
| Network | If `to` is present, `from` and `to` must be same network (both mainnet or both testnet) |

For complete field constraints, see [references/constraints.md](references/constraints.md).

## Error Codes

| Range | Category |
|-------|----------|
| 1xxx | Task/Message errors (invalid format, unknown method) |
| 2xxx | Authentication errors (bad signature, expired timestamp, replay) |
| 3xxx | Discovery errors (agent not found, invalid card) |
| 4xxx | Transport errors (timeout, connection refused) |
| 5xxx | System errors (rate limit, maintenance) |

Errors are returned in the message payload, not as HTTP status codes. All SNAP responses use HTTP 200.

For complete error code listing, see [references/error-codes.md](references/error-codes.md).

## Nostr Integration

Default relay: `wss://snap.onspace.ai`

| Kind | Type | Purpose |
|------|------|---------|
| 31337 | Replaceable (NIP-33) | Agent Card publication |
| 21339 | Ephemeral (NIP-16) | Real-time encrypted SNAP message (default) |
| 4339 | Regular (storable) | Persistent/offline SNAP message |

Messages are encrypted end-to-end using NIP-44. The relay only sees ciphertext. By default, real-time messages use ephemeral kind 21339 (not stored). Set `persist: true` for storable kind 4339 (offline retrieval).

For Nostr event structure and offline messaging, see [references/nostr-transport.md](references/nostr-transport.md).

## SDK Implementations

| Language | Skill |
|----------|-------|
| TypeScript | [typescript/SKILL.md](typescript/SKILL.md) |
