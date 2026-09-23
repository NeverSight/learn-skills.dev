---
name: postgres
description: >-
  Operate PostgreSQL instances safely: configuration review, index and
  query-plan analysis, vacuum and bloat management, WAL archiving and
  point-in-time recovery, replication and failover, extensions, major-version
  upgrades, and evidence-based diagnostics with the bundled read-only pgdiag
  script. Use when running or inspecting a PostgreSQL server, diagnosing
  performance or backup health, or planning an upgrade or failover. Do not use
  for application-level data access patterns (that's backend-engineering) or
  schema design (that's data-architect/data-engineering).
license: MIT
compatibility: >-
  The bundled pgdiag script runs on Python 3.9+ and needs no PostgreSQL server
  for --help. Live diagnostics require the psql client (PostgreSQL 10+ servers)
  and socket or network access to the instance.
metadata:
  source: https://www.postgresql.org/docs/current/
  research_checked: "2026-08-03"
---

# PostgreSQL Operations

Use this skill to operate PostgreSQL safely as the database engine it is: review configuration against workload, find index and query-plan problems, manage vacuum and bloat, set up and verify WAL archiving and point-in-time recovery, run replication with a defensible failover plan, handle extensions, plan major-version upgrades, and diagnose incidents with evidence. This is a **tool skill** for one named tool (PostgreSQL). Database *methodology* — backup strategy across engines, migration patterns, SQL analytical patterns — lives in [data-engineering](../data-engineering/SKILL.md); application-level data access patterns belong to [backend-engineering](../backend-engineering/SKILL.md); schema and data modeling belong to [data-architect](../data-architect/SKILL.md) and `data-engineering`. Supabase platform administration is [supabase](../supabase/SKILL.md).

## Operating contract

1. **Read-only discovery before any mutation.** Inspect configuration, catalog statistics, and logs first. The bundled `pgdiag` script collects read-only evidence and opens every session with `default_transaction_read_only=on`.
2. **Confirm the target, scope, and rollback path before acting.** Read-only discovery may proceed without confirmation. Mutations — a `pg_ctl` stop, a promotion, an extension install, a `pg_upgrade` run — require an explicit human directive naming the instance.
3. **A backup is not recovery evidence.** Verify restore on a scratch instance on a schedule; never claim recoverability from a backup log alone.
4. **Keep evidence bounded.** Summarize catalog queries and log excerpts; never dump full logs, `postgresql.conf`, or connection strings with passwords into chat.
5. **Verify at the delivery boundary.** A `SELECT 1` answer proves connectivity, not health; a replayed `pg_basebackup` proves recoverability, not that today's WAL is being archived.

## The pgdiag script

`scripts/pgdiag` is an agent-first, read-only diagnostic collector. It shells out to `psql`, opens every session with `default_transaction_read_only=on`, and emits bounded JSON. `--help` works with no server and no psql installed.

```bash
scripts/pgdiag --help                      # no cluster needed
scripts/pgdiag --json                      # all checks, machine-readable
scripts/pgdiag --host db1 --dbname app --json
scripts/pgdiag --check identity --check wal_archive --json
scripts/pgdiag --plan-for "SELECT * FROM orders WHERE id = 42" --json
```

Exit codes: 0 ok, 1 runtime/collection error, 2 usage error, 127 psql binary not found, 124 timeout. `--check` runs a named subset; `--plan-for` adds an `EXPLAIN (FORMAT JSON)` plan for one read-only statement. The script never issues data-changing statements, and the server-side read-only session setting rejects any that slip through.

## Operating loop

1. **Identify the instance**: version, recovery state, configuration file locations, connection string shape, and whether this is primary or standby.
2. **Collect evidence**: `pgdiag --json` for config, connections, index usage, bloat signals, WAL archiving, recovery, replication, extensions, and database sizes.
3. **Triage against the symptom**: map the reported problem to the evidence (slow queries → plans and index usage; stalled backups → archiver; drift → replication lag).
4. **Act with confirmation**: bounded, scoped mutations after a human directive, with a rollback path named first.
5. **Verify**: re-run the relevant check and confirm the observable at the delivery boundary.

## Configuration

- The runtime source of truth is `pg_settings`, not the file: `SHOW`/`current_setting()` reflect reloads and overrides (ALTER SYSTEM, command-line `-c`, env `PGOPTIONS`). `pgdiag`'s `config` check lists the operator-critical values.
- Know which changes need a reload (`pg_ctl reload` / `SELECT pg_reload_conf()`) versus a restart: memory (shared_buffers, max_connections, wal_level, max_wal_senders) requires restart; most tuning and logging parameters reload.
- Check `log_destination`, `logging_collector`, and `log_min_duration_statement` so slow-query evidence exists before you need it; `track_io_timing=on` makes `pg_stat_database` I/O timing meaningful.
- Connection pressure: compare `pg_stat_activity` state counts against `max_connections`; a connection pooler is an application-architecture decision for [backend-engineering](../backend-engineering/SKILL.md).
- GUC rationale, reload-versus-restart tables, and parameter-change review patterns: `references/01-configuration.md`.

## Indexes and query plans

- Evidence first: `pg_stat_user_indexes` shows `idx_scan`/`idx_tup_read`/`idx_tup_fetch`; a table scanned sequentially with a large `seq_tup_read` while a filter exists is a candidate for a missing index.
- `EXPLAIN (ANALYZE, BUFFERS)` on the real workload query beats guessing; compare estimated to actual rows — a large mismatch points at stale planner statistics (a `pg_statistic` freshness problem) or a bad parameter (random_page_cost, effective_cache_size).
- Unused indexes (`idx_scan = 0` over a long window) cost writes and maintenance; invalid indexes (`pg_index.indisvalid = false`) are dropped on next vacuum and should be repaired or removed deliberately.
- Index choices (BRIN vs btree, partial indexes, covering indexes) are schema design and belong to [data-architect](../data-architect/SKILL.md); this skill owns measuring and operating what exists.
- Query-plan reading, index-usage SQL probes, and plan-review checklists: `references/02-indexes-and-query-plans.md`.

## Vacuum and bloat

- Vacuum reclaims dead tuples and refreshes planner statistics; autovacuum should do this on its own. Verify it is actually running: `autovacuum=on`, worker count, and per-table `relfrozenxid`/`n_dead_tup` trends.
- Bloat is the gap between table file size and live data: `pg_stat_user_tables.n_dead_tup` rising faster than vacuum runs is the leading signal; heap bloat from failed or skipped vacuum shows as large `relpages` with low live tuples.
- If autovacuum lags, the response is a targeted, confirmed maintenance window (`VACUUM` on specific tables, not a firehose), then a check of why autovacuum fell behind (long transactions, connection saturation, worker starvation).
- Never treat `VACUUM FULL` as routine: it rewrites the table, takes locks, and needs a maintenance window plus a verified backup path.
- Bloat measurement probes and autovacuum tuning patterns: `references/03-vacuum-and-bloat.md`.

## Backups: WAL archiving and point-in-time recovery

- The recovery model: a base backup plus a continuous WAL archive gives point-in-time recovery (PITR) — restore the base, replay archived WAL up to the target time.
- Recovery targets come in two families: time-based (the `pitr|point.in.time` pattern is the shorthand for this family — a wall-clock target such as "yesterday 02:00") and position-based (a specific LSN or timeline marker). Both are valid `recovery_target` inputs.
- WAL archiving readiness is `archive_mode=on` with a working `archive_command` and a healthy archiver: `pg_stat_archiver` must show `archived_count` growing, `failed_count` stable, and `last_failed_wal` empty or old.
- `wal_level` must be `replica` (or higher) for both archiving and streaming replication; changing it requires a restart.
- Back up with `pg_basebackup` (or a dedicated tool) consistently with WAL: label each backup, record its `pg_stop_backup()` LSN / timeline, and test restore with the archive before trusting it.
- PITR procedure, `recovery_target` options, restore-to-point-in-time steps, and RPO/RTO framing (methodology in [data-engineering](../data-engineering/SKILL.md)): `references/04-backups-wal-pitr.md`.

## Replication and failover

- Streaming replication: standby connects with a replication slot, receives WAL continuously; verify with `pg_stat_replication` (`state=streaming`, `replay_lsn` keeping up, small `replay_lag`) and the standby's recovery state.
- Decide synchronous vs asynchronous deliberately: synchronous (`synchronous_standby_names`) trades commit latency for a durability guarantee; asynchronous risks losing the last commits on failover.
- A failover plan is more than a `pg_ctl promote`: it names who promotes, how clients are redirected, what happens to the old primary on return, and how to verify data (lag at promotion, timeline divergence).
- Promotion is a mutation — confirm the target and scope first. With a replication-manager tool (Patroni, repmgr), use its switchover command instead of manual promotion; rejoin the old primary as a standby, never let two primaries write.
- Streaming setup, slot management, lag measurement, and failover runbooks: `references/05-replication-and-failover.md`.

## Extensions

- Inventory first: `pg_extension` (installed) and `pg_available_extensions` (available) tell you what exists and what versions are on disk; `pgdiag`'s `extensions` check does this.
- Extension installs change the shared catalog and some extensions change the database in ways that are hard to reverse — an install is a mutation with a rollback path, not a `CREATE EXTENSION` reflex.
- Major-version upgrades usually require re-installing or re-building extensions (e.g., PostGIS, pgvector) on the new binaries; check each extension's upgrade notes before `pg_upgrade`.
- Trusted extensions can be installed by non-superusers into their own databases; extension policy and shared-library availability are infrastructure decisions for [platform-engineering](../platform-engineering/SKILL.md).
- Common extensions, lifecycle, and version-upgrade gotchas: `references/06-extensions.md`.

## Upgrades

- Minor upgrades are in-place binary swaps (restart); major upgrades (e.g., 15 → 16) change on-disk format and need `pg_upgrade` or a logical dump/restore.
- Plan the path first: read the release notes and upgrade guide for the full version span, check extensions and unsupported features, pick the method (`pg_upgrade` with link mode, or logical), and rehearse in a scratch environment with the real data shape.
- `pg_upgrade` is a mutation requiring downtime and a verified backup: stop writes, run the upgrade with the `--old`/`--new` binaries, run `analyze` on the new cluster, and verify at the application boundary before decommissioning the old.
- Logical replication (publisher/subscriber) can serve as a near-zero-downtime major-upgrade path; it is also a migration pattern whose methodology lives in [data-engineering](../data-engineering/SKILL.md).
- Version matrices, upgrade runbooks, and rollback decisions: `references/07-upgrades.md`.

## Diagnostics with evidence

Diagnose in evidence order: identity/version → configuration → connections → index usage and plans → vacuum/bloat → WAL archiving → replication → extensions.

- `pgdiag --json` gathers the first evidence layer in one bounded payload; re-run the affected check after any change.
- Slow query → `EXPLAIN (ANALYZE, BUFFERS)` plus `pg_stat_user_indexes`/`seq_tup_read`; check planner statistics freshness before touching `random_page_cost`.
- Backup stalled → `pg_stat_archiver`: `failed_count`, `last_failed_wal`, and the archive target's disk/network.
- Standby falling behind → `pg_stat_replication` lag columns, slot retention (`pg_replication_slots`), and network saturation between primary and standby.
- Never present correlation as cause: a slow query and a high `n_dead_tup` are evidence, not a diagnosis — state what was measured, what changed, and what was verified.
- Failure-mode routing and symptom→probe→fix tables: `references/08-diagnostics.md`.

## Reference routing

| Load when | Reference |
|---|---|
| Tuning, GUC review, reload vs restart | `references/01-configuration.md` |
| Slow queries, index usage, plan review | `references/02-indexes-and-query-plans.md` |
| Autovacuum, dead tuples, bloat measurement | `references/03-vacuum-and-bloat.md` |
| WAL archiving, base backups, PITR, restore drills | `references/04-backups-wal-pitr.md` |
| Streaming setup, slots, lag, failover runbooks | `references/05-replication-and-failover.md` |
| Extension inventory and upgrade gotchas | `references/06-extensions.md` |
| Minor and major upgrades, pg_upgrade, rollback | `references/07-upgrades.md` |
| Symptom-to-probe diagnosis tables | `references/08-diagnostics.md` |
| Sources, version observations, refresh procedure | `references/00-source-index.md` |

## Included artifacts

- `scripts/pgdiag`: read-only diagnostic collector (stdlib-only, `--json`, `--check`, `--plan-for`, `--help` without a cluster).
- `tests/test_pgdiag.py`: deterministic tests against a fake psql stub, including the read-only contract.
- `references/`: nine dated, source-indexed references covering the operational topics above.

## Verification boundary

| Claim | Minimum evidence |
|---|---|
| Instance is reachable and versioned | `pgdiag --check identity --json` parses and reports version and recovery state |
| Configuration is known | `pgdiag` `config` check lists the operator-critical GUCs |
| Archiving is healthy | `pg_stat_archiver`: `archived_count` increasing, `failed_count` not climbing, `last_failed_wal` stale |
| Replication is current | `pg_stat_replication`: `state=streaming` and lag within the agreed bound |
| Backups support recovery | A restore of a base backup + WAL replayed to a target time on a scratch instance |
| A diagnosis is sound | Evidence was collected before the claim, and the fix was verified by re-running the check |

## Hard boundaries

- Never run a mutation (`pg_ctl stop`, promote, `pg_upgrade`, extension install, maintenance `VACUUM`) without an explicit human directive naming the target and a stated rollback path. Read-only discovery may proceed freely.
- Never present unverified claims as evidence: state what was measured, when, and how.
- Never expose full logs, `postgresql.conf` contents, or connection strings containing passwords.
- Never run `pgdiag` with a write-capable session; the tool itself is read-only by design.

## When not to use

- **Application-level data access patterns** (connection pooling in app code, ORM usage, query construction, transactions in services) — that is [backend-engineering](../backend-engineering/SKILL.md).
- **Schema design and data modeling** (tables, keys, normalization, dimensional models) — that is [data-architect](../data-architect/SKILL.md) and [data-engineering](../data-engineering/SKILL.md).
- **Database methodology across engines** (backup strategy, migration patterns, analytical SQL) — that is `data-engineering`.
- **Supabase platform administration** (managed projects, CLI stack, the self-hosted Supabase stack) — that is [supabase](../supabase/SKILL.md); plain PostgreSQL operations without Supabase conventions belong here. To measure an agent's Supabase task competence, use the skill's [agent evals harness reference](../supabase/references/agent-evals.md).
- **Other database engines** (Redis, MongoDB, Elasticsearch, vector stores) — those stay in `data-engineering` references; this skill owns PostgreSQL only.
