---
name: realtime-sync
description: 'Low-latency synchronization with WebTransport, pub/sub messaging, CRDTs, and AI stream orchestration. Covers bidirectional streaming, transactional outbox patterns, sequence tracking, and collaborative editing. Use when building real-time collaborative UIs, implementing pub/sub messaging, handling WebTransport or WebSocket connections, orchestrating live AI token streams, or resolving conflicts with CRDTs.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
user-invocable: false
---

# Realtime Sync

## Overview

Architects high-concurrency, sub-50ms latency synchronization between distributed clients and servers. Covers WebTransport (HTTP/3) bidirectional streaming, transactional outbox patterns for database-to-sync consistency, CRDTs for collaborative editing, and AI token stream orchestration.

Core principles: the database is the source of truth (real-time channels notify, not persist), CRDTs eliminate locking for concurrent edits, and backpressure management prevents UI jitter from high-frequency streams.

**When to use:** Real-time collaborative UIs, pub/sub messaging, WebTransport/WebSocket connections, live AI token streams, presence tracking, conflict resolution with CRDTs, multiplayer applications.

**When NOT to use:** Batch processing pipelines, static content delivery, request-response APIs without real-time requirements, offline-only applications.

## Quick Reference

| Pattern               | Approach                                     | Key Points                                               |
| --------------------- | -------------------------------------------- | -------------------------------------------------------- |
| WebTransport          | `new WebTransport(url)` + `await ready`      | HTTP/3 multiplexed; replaces WebSockets for new projects |
| Bidirectional stream  | `transport.createBidirectionalStream()`      | Returns `{ readable, writable }` for request-response    |
| Unidirectional stream | `transport.createUnidirectionalStream()`     | Returns a `WritableStream` directly for one-way pushes   |
| Datagrams             | `transport.datagrams.writable`               | UDP-like unreliable delivery for high-frequency state    |
| Connection stats      | `transport.getStats()`                       | Returns `smoothedRtt`, `bytesSent`, `packetsLost`        |
| Transactional outbox  | DB write + outbox insert in one transaction  | CDC worker pushes to channel; prevents state drift       |
| Sequence tracking     | Sequence IDs on every message                | Rewind on reconnect to fetch missed messages             |
| CRDT collaboration    | Yjs (text) or Automerge (JSON state)         | Conflict-free concurrent editing without locks           |
| CRDT awareness        | `y-protocols/awareness` module               | Tracks cursors, selections, and user presence            |
| CRDT undo/redo        | `Y.UndoManager` with `trackedOrigins`        | Tracks only local user operations for selective undo     |
| Presence              | Heartbeat-based user tracking                | Epidemic broadcast for reliable zombie cleanup           |
| AI stream batching    | `requestAnimationFrame` for token rendering  | Prevents UI jitter from high-frequency updates           |
| Buffer-and-batch      | `useTransition` for sync-triggered updates   | Defers non-urgent re-renders during sync bursts          |
| Backpressure          | Buffer size limit with forced flush          | Prevents memory buildup when tokens outpace rendering    |
| WebSocket fallback    | Detect WebTransport support first            | Enterprise firewalls may block UDP/HTTP/3                |
| Serialization         | Protocol Buffers or MessagePack              | Avoid JSON.stringify on 100Hz+ streams                   |
| Web Worker transport  | Handle WebTransport in a Web Worker          | Prevents blocking the UI thread                          |
| Channel multiplexing  | Subscribe to multiple channels on one socket | All subscriptions share a single transport connection    |

## Common Mistakes

| Mistake                                                        | Correct Pattern                                                      |
| -------------------------------------------------------------- | -------------------------------------------------------------------- |
| Using real-time messages as the primary source of truth        | State lives in the database; real-time is the notification of change |
| Using JSON.stringify on high-frequency streams (100Hz+)        | Use Protocol Buffers or MessagePack for serialization                |
| Ignoring sequence drift when a client misses messages          | Implement Sequence IDs and a rewind mechanism on the client          |
| Implementing global locks for concurrent access                | Use Optimistic UI and CRDTs for conflict-free collaboration          |
| Sticking with WebSockets for new projects needing multiplexing | Use WebTransport (HTTP/3) for bidirectional, multiplexed streams     |
| CRDT document bloat from unbounded history                     | Use snapshotting (LWW) for fields that do not need history           |
| Failing to close WebTransport streams on unmount               | Explicitly close streams to prevent transport crashes                |
| Importing Awareness from `yjs` instead of `y-protocols`        | Use `import { Awareness } from 'y-protocols/awareness'`              |
| Using `ydoc.clientID` as UndoManager tracked origin            | Use custom transaction origins passed to `doc.transact()`            |
| One React re-render per AI token received                      | Batch tokens with `requestAnimationFrame` and flush once per frame   |
| Not handling WebTransport `closed` promise                     | Monitor `transport.closed` to detect unexpected disconnections       |

## Delegation

> If the `local-first` skill is available, delegate local-first architecture decisions, sync engine comparison, and client storage selection to it.
> If the `electricsql` skill is available, delegate ElectricSQL shape-based Postgres sync patterns to it.

- **Explore transport protocol options and latency benchmarks**: Use `Explore` agent to compare WebTransport, SSE, and WebSocket tradeoffs
- **Implement transactional outbox pattern with CDC pipeline**: Use `Task` agent to set up database triggers, outbox table, and background worker
- **Design real-time architecture for collaborative editing**: Use `Plan` agent to map CRDT strategy, presence management, and conflict resolution flow
- **Build multi-stream AI orchestration component**: Use `Task` agent to implement parallel token stream rendering with backpressure
- **Audit real-time connection lifecycle management**: Use `Review` agent to check for stream leaks, missing cleanup, and reconnection handling

## References

- [WebTransport streaming and worker patterns](references/webtransport.md)
- [Pub/sub messaging and guaranteed delivery](references/pubsub-delivery.md)
- [CRDTs and collaborative editing](references/crdt-collaboration.md)
- [AI stream orchestration patterns](references/ai-stream-orchestration.md)
- [Collaborative undo and redo patterns](references/undo-redo.md)
