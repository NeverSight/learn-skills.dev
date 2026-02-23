---
name: altinity-expert-clickhouse-part-log
description: Diagnose ClickHouse issues by analyzing system.part_log (part creation, merges, mutations, downloads, removals, moves). Use for too many parts / micro-batch inserts, merge backlog or slow merges, mutation storms (ALTER DELETE/UPDATE), unusual replication DownloadPart churn, unexpected RemovePart spikes, or ZooKeeper/Keeper znode growth correlated with part activity.
---

# Part Log Based Diagnostics

Run all queries from `checks.sql` (cluster-wide) and interpret the top offenders by **rate** (events/min), **volume** (rows/bytes), and **errors**.

Notes:
- Default timeframes are relative (e.g., last 1h/6h/24h). Only switch to an explicit time range when the user provides one in the prompt.
- Replace `{cluster}` with your ClickHouse cluster name (DataGrip).
- Keep queries time-bounded (`event_time > now() - INTERVAL ...`) and use `LIMIT`.
- If a query fails due to schema differences, run `DESCRIBE TABLE system.part_log` and drop only missing fields.

Cross-module triggers:
- High `NewPart` rate / micro-batches → load `altinity-expert-clickhouse-ingestion` + `altinity-expert-clickhouse-merges`
- High `MutatePart` rate → load `altinity-expert-clickhouse-mutations`
- Many `DownloadPart` → load `altinity-expert-clickhouse-replication`
- Merge saturation / slow merges → load `altinity-expert-clickhouse-merges` + `altinity-expert-clickhouse-storage`
