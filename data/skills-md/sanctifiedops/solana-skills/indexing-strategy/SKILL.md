---
name: indexing-strategy
description: Decide when and how to index Solana data vs direct RPC reads. Covers event design, backfill, storage, and performance. Use for data architecture decisions.
---

# Indexing Strategy

Role framing: You are a data architect. Your goal is to choose an indexing approach that meets freshness and cost needs without overbuilding.

## Initial Assessment
- What data is needed (events, account states, historical candles)?
- Freshness and latency requirements?
- Query patterns (by owner, by mint, by time)?
- Expected scale and retention?

## Core Principles
- Index only when RPC queries become too heavy or slow; start simple.
- Emit structured events to simplify indexing; include versioning.
- Backfill first, then stream; ensure idempotency.
- Storage schema matches query needs; avoid over-normalizing hot paths.

## Workflow
1) Decide necessity
   - Try getProgramAccounts + caches first; move to indexer if slow or large.
2) Event design
   - Add program logs/events with discriminators and key fields; avoid verbose logs.
3) Choose stack
   - Options: custom listener + DB, Helius/webhooks to queue, GraphQL subgraph equivalents, or hosted indexers.
4) Backfill
   - Use getSignaturesForAddress/getTransaction or snapshot; store cursor; verify counts.
5) Live ingestion
   - Subscribe to logs or webhooks; ensure dedupe and ordering by slot + tx index.
6) Query API
   - Expose REST/GraphQL tailored to frontend/bot needs; add caching.
7) Monitoring
   - Lag metrics (slots behind), error rate, queue depth; alerts.

## Templates / Playbooks
- Event schema: event_name, version, keys..., values... with borsh or base64 payloads.
- Backfill checkpoint table: slot, signature, processed flag.
- Storage patterns: wide tables for hot paths; partition by day for history.

## Common Failure Modes + Debugging
- Missing key fields in events -> hard queries; add indexes or emit new version.
- Backfill gaps from rate limits; implement retries and cursors.
- Duplicate processing on reorgs; use slot+sig idempotency key.
- Unbounded storage growth; set retention or cold storage.

## Quality Bar / Validation
- Clear rationale for indexing vs RPC; event design documented.
- Backfill completed with verification counts; lag monitored.
- APIs tested against target queries with latency targets met.

## Output Format
Provide indexing decision, event schema, ingestion plan (backfill + live), storage/query design, and monitoring plan.

## Examples
- Simple: Small app uses RPC + caching; no indexer needed; document reasons.
- Complex: High-volume protocol emits events; uses webhooks to queue -> worker -> Postgres; backfill from slot X; exposes GraphQL; monitors lag < 5 slots.