---
name: sync-topic
description: "Use this skill when implementing event streams with @valentinkolb/sync topic: publishing typed events with idempotency, consumer-group processing with commit for at-least-once delivery, live replay from any cursor, retention tuning, and multi-tenant stream isolation. Also use when choosing between topic (pub/sub events) vs queue (work distribution)."
---

# Sync Topic

Typed event streams backed by Redis Streams. Two consumption modes: **reader** (consumer groups, at-least-once, commit-based) and **live** (stateless fan-out/replay).

## Decision Guide: reader() vs live()

- **reader(group)**: durable, at-least-once. Each group tracks its own cursor. Call `commit()` after processing. Use for event-driven workers (mailer, projections, analytics).
- **live({ after })**: stateless fan-out. No group state, no commit. Use for real-time dashboards, debugging, or replay from `"0-0"`.

## Decision Guide: topic vs queue

- **topic**: events are broadcast to all consumer groups independently. No ack/nack per message — use `commit()`. Best for fan-out, event sourcing, audit.
- **queue**: work items are distributed to exactly one consumer. Use `ack()`/`nack()` per message. Best for task distribution, job pipelines. See `sync-queue` skill.

## Gotchas

- `commit()` is per-delivery, not per-batch. Always commit after processing each event.
- Invalid payloads on the read path are auto-acknowledged and skipped (logged, not thrown).
- `reader().stream({ wait: true })` auto-retries transient errors. Do not wrap with `retry()`.
- `live()` also auto-retries while preserving cursor progression.
- `retentionMs` defaults to 7 days. Events older than this are trimmed.
- `idempotencyKey` deduplication uses a separate SET key with configurable TTL (default 7 days).
- Payload max is 128KB by default (`limits.payloadBytes`).
- No XAUTOCLAIM: dead consumers' pending entries are NOT auto-recovered. Design consumers to be restartable.

## API Reference

Read full API/types/config/defaults in [references/api.md](references/api.md).
