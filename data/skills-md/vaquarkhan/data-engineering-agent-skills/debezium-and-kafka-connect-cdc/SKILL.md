---
name: debezium-and-kafka-connect-cdc
description: Guides agents through Debezium and Kafka Connect CDC workflows. Use when streaming database changes into Kafka topics, managing connectors, snapshots, schema evolution, or downstream CDC consumers.
---

# Debezium And Kafka Connect CDC

## Overview

Use this skill when database changes must be captured and delivered through `Debezium` and `Kafka Connect`. It helps agents define connector safety, snapshot behavior, schema handling, and downstream CDC contracts.

## When to Use

- setting up `Debezium` connectors for `PostgreSQL`, `MySQL`, `MongoDB`, `SQL Server`, or `Oracle`
- designing Kafka-based CDC from transactional databases
- handling initial snapshots, incremental streaming, and connector recovery
- feeding downstream stream processors, lakehouse sinks, or search indexes
- managing schema evolution when source tables change

Do not use this when changes can be captured through application-level events or batch extracts are sufficient for freshness requirements.

## Workflow

1. Define source tables, keys, and change event semantics.
   Include:
   - which tables to capture and which to exclude
   - primary key and unique key strategy for each table
   - expected change operations: inserts, updates, deletes, truncates
   - whether tombstone records are needed for compacted topics
   - expected change volume and peak throughput

2. Plan snapshot behavior explicitly.
   - initial snapshot: full table scan on first connector start
   - define snapshot mode: `initial`, `schema_only`, `never`, or `when_needed`
   - understand lock behavior during snapshot (especially for `PostgreSQL` and `MySQL`)
   - plan for snapshot duration on large tables — can take hours
   - document what happens if a snapshot is interrupted

3. Configure connector for operational resilience.
   - set appropriate `max.batch.size` and `poll.interval.ms`
   - configure heartbeat intervals to prevent WAL/binlog retention issues
   - define slot or binlog retention policies on the source database
   - plan for connector task failures and automatic restarts
   - monitor connector lag and offset position

4. Define topic contracts and downstream expectations.
   - topic naming convention: `{prefix}.{schema}.{table}`
   - event envelope format: include before/after, operation type, source metadata
   - schema registry integration for event contracts
   - retention and compaction policy per topic
   - document which consumers depend on each topic

5. Handle schema evolution safely.
   - source DDL changes (column adds, renames, type changes) propagate through CDC
   - define compatibility policy in schema registry (backward, forward, full)
   - test that downstream consumers handle schema changes without failure
   - plan for breaking changes: connector restart, re-snapshot, or topic migration

6. Plan recovery, replay, and operational safety.
   - define what happens when the connector falls too far behind (slot overflow, binlog expiry)
   - document re-snapshot procedure for recovery
   - plan for database failover: does the connector reconnect automatically?
   - define monitoring alerts: lag, errors, rebalances, and dead-letter routing

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "CDC is just a connector — set it and forget it." | Connectors require active monitoring, offset management, and schema evolution handling. Neglected connectors silently lose data. |
| "We don't need to worry about snapshots after the first one." | Database failovers, slot loss, and connector resets can trigger re-snapshots. The team must plan for snapshot impact on source load. |
| "Schema changes in the source don't affect CDC." | Every DDL change propagates through the CDC stream. Without compatibility policies, downstream consumers break silently. |
| "Kafka handles deduplication for us." | Debezium provides at-least-once delivery. Consumers must handle duplicates or use idempotent processing patterns. |

## Red Flags

- no monitoring of connector lag or WAL/binlog retention
- snapshot mode is undefined or set to `always` without understanding impact
- no schema registry integration for CDC topics
- downstream consumers assume exactly-once delivery without deduplication logic
- heartbeat intervals are not configured, risking WAL bloat on the source
- no documented recovery procedure for slot loss or binlog expiry
- topic retention is unlimited with no compaction policy
- connector runs with a single task on high-volume multi-table sources

## Verification

- [ ] Source tables, keys, and change semantics are explicitly documented
- [ ] Snapshot behavior and impact on source database are understood and planned
- [ ] Topic contracts include naming, envelope format, retention, and schema compatibility
- [ ] Schema evolution paths are tested for both additive and breaking changes
- [ ] Connector monitoring covers lag, errors, rebalances, and offset position
- [ ] Recovery procedures for slot loss, binlog expiry, and database failover are documented
- [ ] Downstream consumers handle at-least-once delivery with deduplication or idempotency
