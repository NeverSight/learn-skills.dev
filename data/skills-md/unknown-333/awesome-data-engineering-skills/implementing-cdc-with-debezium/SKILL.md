---
name: implementing-cdc-with-debezium
description: Capture database changes with Debezium change data capture — connector setup for Postgres/MySQL/SQL Server, snapshot vs streaming phases, handling inserts/updates/deletes and tombstones, schema changes, and applying the change stream idempotently to a warehouse/lake. Use when setting up CDC, replicating an OLTP database, capturing deletes, or consuming a Debezium change stream.
---

# Implementing CDC with Debezium

## When to use

- Replicating an operational database (Postgres/MySQL/SQL Server) to a
  warehouse/lake in near real time.
- You need **deletes** and every intermediate change (watermark extraction can't
  see deletes).
- Consuming or applying a Debezium change stream idempotently.
- Do NOT use for simple periodic batch pulls (use `building-ingestion-pipelines`).

## Workflow

```
- [ ] Enable the DB log (Postgres logical replication / MySQL binlog / MSSQL CDC)
- [ ] Configure the Debezium connector (tables, snapshot mode, keys)
- [ ] Handle the initial snapshot, then streaming changes
- [ ] Apply changes idempotently: MERGE keyed on PK, ordered by log position
- [ ] Handle deletes (tombstones) and schema changes
```

1. **Enable the log.** Debezium reads the DB transaction log: Postgres logical
   replication (`wal_level=logical` + a publication/slot), MySQL binlog
   (`ROW` format), or SQL Server CDC. Grant the connector the needed privileges.
2. **Configure the connector** with the tables to capture, the snapshot mode, and
   the primary key. It emits an initial **snapshot**, then live **change events**.
3. **Apply idempotently.** Each event carries `before`/`after`/`op` and a log
   position (LSN/GTID). MERGE on the primary key and order by the position so
   out-of-order or replayed events converge to the correct state.
4. **Deletes** arrive as `op=d` (plus a null-value tombstone for log compaction);
   apply as a delete or soft-delete flag.
5. **Schema changes** flow through; pair with `handling-schema-evolution`.

## Patterns

**Apply a change event with MERGE (soft delete):**

```sql
MERGE INTO dwh.customers t
USING cdc_batch s ON t.id = s.id
WHEN MATCHED AND s.op = 'd' THEN UPDATE SET t.is_deleted = TRUE, t.updated_lsn = s.lsn
WHEN MATCHED AND s.lsn > t.updated_lsn THEN UPDATE SET t.name = s.name, t.updated_lsn = s.lsn
WHEN NOT MATCHED AND s.op <> 'd' THEN INSERT (id, name, is_deleted, updated_lsn)
  VALUES (s.id, s.name, FALSE, s.lsn);
```

The `lsn` guard makes application idempotent and order-safe: replayed or older
events are ignored.

**Snapshot then stream** — the snapshot backfills current state; streaming keeps it
fresh. Deduplicate the overlap by log position.

## Common pitfalls

- **Ignoring log position ordering** — applying events out of order corrupts state;
  guard updates with the LSN/GTID.
- **Not handling deletes/tombstones** — target diverges from source over time.
- **Non-idempotent apply** — connector restarts replay events and duplicate rows;
  MERGE by PK.
- **Replication slot not consumed** (Postgres) — WAL accumulates and fills the
  disk; monitor slot lag and keep the consumer running.
- **Forgetting schema-change handling** — a source DDL breaks the sink; plan for
  additive evolution.
- **Snapshot on a huge table with no throttling** — hammers the source; use
  incremental snapshotting.
