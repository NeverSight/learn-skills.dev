---
name: postgres
description: "PostgreSQL reference (versions 14–18, plus PostgreSQL 19 changes) to consult before writing or changing anything that runs on Postgres. Use for any SQL or database work that touches Postgres, even when the user only asks to build a feature: queries, schemas, DDL, migrations, indexes, constraints, data types, functions, triggers, PL/pgSQL, RLS, and ORM or query-builder code that emits Postgres SQL; reviewing or debugging SQL; EXPLAIN plans; locking, transactions, VACUUM, WAL, partitioning, replication, backup, upgrades, pooling, monitoring, tuning, and security. Also covers JSONB, full-text search, BM25 ranking, message queues, UUIDs, timestamptz, COPY, catalogs, and extensions (pgvector, PostGIS, TimescaleDB, Citus, pg_trgm, pg_cron, pg_partman, pg_textsearch, pgmq). Load it whenever the project uses Postgres (a postgres:// URL, a Postgres driver, .sql files, a migrations folder) and read the matching references before writing SQL, so version differences and known pitfalls are checked first."
---


# PostgreSQL Skill

This skill is the working reference for **PostgreSQL 16, 17, and 18** (current baseline: PG16). Cross-version notes go back to PG14 where behavior changed; PG13 and earlier are out of scope. PG14 reached end-of-life on 2026-11-12 (final minor 14.25); flag upgrade urgency when a user is on it. PostgreSQL 19 is a release candidate with GA planned for 2026-11-19; its changes live in `100-pg-versions-features.md` and in `PostgreSQL 19` callouts in topic files.

The skill is provider-neutral: bare-metal/self-hosted, containers, and Kubernetes operators are all covered. Managed-service limitations are called out categorically ("most managed providers disable X") without naming or recommending any specific vendor.

Each topic lives in its own reference file under `references/`. SKILL.md routes a user question to the right reference; the reference contains the executable detail, version admonitions, and primary-source citations.


## Usage Workflow


When this skill is loaded, follow these steps to answer the user's question:

1. **Identify the topic.** Match the user's question against the **Routing Table** below using the keyword column. For multi-topic questions (e.g. "the locking behavior of REINDEX CONCURRENTLY") select multiple files.
2. **Load the matched reference file(s).** Use the Read tool against `references/NN-topic.md`. Do not paraphrase from memory; use the reference's version notes and primary-source URLs.
3. **Follow See Also.** Each reference ends with a **See Also** section linking related files. Follow it for cross-cutting questions (e.g. a VACUUM question pulls in MVCC, autovacuum, and wraparound).
4. **Answer using the file.** Lead with the direct answer or code, then version notes via admonitions, then caveats, then citation URLs.
5. **Verify high-risk instructions against primary sources.** These references are a working compilation, not a substitute for the matching PostgreSQL manual. Before advising recovery, durability changes, failover, privilege changes, or destructive maintenance, fetch the cited upstream section for the actual server version. Resolve conflicting advice before giving commands; identify anything you could not verify.
6. **Assume PG16 unless told otherwise.** If the user does not state a version, answer for PG16 and add a one-line note for differences on PG17/PG18 (and PG19, a release candidate until GA). Only ask the user which version they are on if the answer materially changes across supported versions (e.g. wraparound mechanics, planner statistics behavior, archive_command vs archive_library). When the project pins a version (a Docker tag, a CI service image, `SELECT version()`), use that one.

**When the task is to build, not to answer.** Writing a schema, migration, query, index, trigger, function, or ORM model that targets Postgres goes through the same lookup, before any code is written:

1. **List the Postgres operations the change involves:** new tables, column types, keys and constraints, indexes, `ALTER` on a populated table, JSONB access, bulk loads, queue or locking patterns.
2. **Route each operation through the Routing Table and read the matching sections.** Common starting points:
    - Column types: 14, 17, 18, 19.
    - Keys and constraints: 37, 38.
    - Indexes: 22, then the type-specific file.
    - DDL on live tables: 01 for lock levels, 43, and 26 for `CONCURRENTLY`.
    - Partitioning: 35.
    - RLS: 47.
    - Bulk loads: 66.
    - Work queues: 104 or 43.
3. **Write the code the references support.** In the reply, name any pitfall the references raised that shaped the code, such as a lock level, a type choice, or a version difference.

> [!NOTE]
> When a Postgres question does not obviously match a single file, load these cross-cutting entry points first: `references/102-skill-cookbook.md` (symptom-driven recipes spanning multiple files), `references/22-indexes-overview.md` (index decision routing), `references/56-explain.md` (plan reading), `references/64-system-catalogs.md` (catalog introspection).


## User Response Format


Structure every answer using this skill as follows:

- **Lead with the direct answer or pattern.** If a SQL snippet or `psql` command satisfies the question, put that first.
- **Add version admonitions inline.** Use `> [!NOTE] PostgreSQL 17` for new-in-17 features, `> [!WARNING] Removed/Deprecated` for things gone (with the version they were removed in and the replacement).
- **Call out managed-service limitations categorically** when relevant. Phrase as "most managed providers disable X" — never name a specific provider.
- **End with source links.** Cite the official PostgreSQL docs pinned to the correct major version (e.g. `https://www.postgresql.org/docs/16/sql-vacuum.html`, not `/docs/current/`).
- **For longer answers**, use headers matching the reference file's section headings so the user can jump to the source.
- **For version-sensitive answers**, default to PG16 + add inline `> [!NOTE] PG17` / `> [!NOTE] PG18` / `PostgreSQL 19` deltas. Only ask the user to confirm version when the answer flips between supported majors.
- **For performance investigations**, explain the plan tree from leaf inputs toward their parents. Compare estimated `rows` with `actual rows` per loop; use `loops` to calculate total work separately. A 10× mismatch is a useful investigation threshold, not proof of a root cause. Account for LIMIT, early termination, and unexecuted nodes. PostgreSQL executes plans on demand, not in a strict deepest-node-first sequence.


<constraints>

## Operational Safety


- **XID hard stop:** connect to the affected database as a superuser, resolve old transaction and slot horizons, then run ordinary database-wide `VACUUM` outside a transaction block. Do not use `FULL`, `FREEZE`, or routine single-user recovery. `VACUUM FREEZE` and `VACUUM (FREEZE)` are equivalent. Follow the [version-pinned recovery procedure](https://www.postgresql.org/docs/16/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND).
- **Corruption salvage:** preserve the complete stopped cluster, including external WAL and tablespaces. Work on an isolated copy. `pg_resetwal` is only a last resort for WAL/control corruption that prevents startup, not an XID-exhaustion repair. Its dry run does not prove consistency; use same-major binaries, then dump and restore into a separate new cluster. Do not replace individual live relation files from an old backup.
- **Destructive decisions:** resolve prepared transactions with their coordinator, confirm a slot's consumer before dropping it, and fence the former primary before failover. State data-loss and rebuild consequences before presenting the operation.
- **Verification limits:** successful `pg_dump`, `pg_amcheck`, or checksum checks do not prove absence of every corruption class or application inconsistency. Distinguish a documented procedure, a tested example, and an unverified assumption.

</constraints>


## Routing Table


Keywords are matched case-insensitively. A single file can match multiple keyword phrases.

| Keywords | File | Scope |
|---|---|---|
| CREATE TABLE, ALTER TABLE, DROP TABLE, schema, sequence, generated column, identity column, IF NOT EXISTS | [`references/01-syntax-ddl.md`](references/01-syntax-ddl.md) | DDL syntax reference |
| SELECT, JOIN, LATERAL, subquery, UNION, INTERSECT, EXCEPT, DISTINCT ON, LIMIT, OFFSET, FETCH FIRST | [`references/02-syntax-dql.md`](references/02-syntax-dql.md) | Query (DQL) reference |
| INSERT, UPDATE, DELETE, RETURNING, ON CONFLICT, upsert, MERGE, DEFAULT VALUES | [`references/03-syntax-dml.md`](references/03-syntax-dml.md) | DML reference |
| WITH, CTE, recursive CTE, WITH RECURSIVE, MATERIALIZED, modifying CTE | [`references/04-ctes.md`](references/04-ctes.md) | Common Table Expressions |
| view, CREATE VIEW, updatable view, INSTEAD OF, security_barrier, security_invoker, materialized view, REFRESH MATERIALIZED VIEW CONCURRENTLY | [`references/05-views.md`](references/05-views.md) | Views and materialized views |
| CREATE FUNCTION, LANGUAGE, IMMUTABLE, STABLE, VOLATILE, PARALLEL SAFE, SECURITY DEFINER, RETURNS TABLE, polymorphic | [`references/06-functions.md`](references/06-functions.md) | Functions |
| CREATE PROCEDURE, CALL, transaction control in procedure, COMMIT in procedure | [`references/07-procedures.md`](references/07-procedures.md) | Procedures |
| PL/pgSQL, plpgsql, DECLARE, BEGIN, EXCEPTION, RAISE, FOR LOOP, cursor in plpgsql, GET STACKED DIAGNOSTICS | [`references/08-plpgsql.md`](references/08-plpgsql.md) | PL/pgSQL deep dive |
| plpython3u, plperl, plperlu, pltcl, plv8, procedural language, untrusted PL | [`references/09-procedural-languages.md`](references/09-procedural-languages.md) | Non-pgSQL procedural languages |
| EXECUTE, dynamic SQL, format(), quote_ident, quote_literal, SQL injection in plpgsql | [`references/10-dynamic-sql.md`](references/10-dynamic-sql.md) | Dynamic SQL |
| OVER, PARTITION BY, window function, ROWS BETWEEN, RANGE BETWEEN, GROUPS, LAG, LEAD, FIRST_VALUE, LAST_VALUE, NTH_VALUE, RANK, DENSE_RANK, ROW_NUMBER, NTILE | [`references/11-window-functions.md`](references/11-window-functions.md) | Window functions |
| aggregate, FILTER, GROUPING SETS, ROLLUP, CUBE, percentile_cont, percentile_disc, ordered-set aggregate, CREATE AGGREGATE | [`references/12-aggregates-grouping.md`](references/12-aggregates-grouping.md) | Aggregates & grouping |
| DECLARE CURSOR, FETCH, MOVE, WITH HOLD, scrollable cursor, refcursor, PREPARE, EXECUTE, DEALLOCATE, plan_cache_mode | [`references/13-cursors-and-prepares.md`](references/13-cursors-and-prepares.md) | Cursors & prepared statements |
| text, varchar, char, numeric, decimal, real, double precision, integer, boolean, bytea, inet, cidr, macaddr, bit, varbit | [`references/14-data-types-builtin.md`](references/14-data-types-builtin.md) | Built-in types |
| CREATE TYPE, composite type, CREATE DOMAIN, ENUM, ALTER TYPE ADD VALUE, range type, multirange | [`references/15-data-types-custom.md`](references/15-data-types-custom.md) | Custom types (composite/domain/enum/range) |
| array, ARRAY[], unnest, array_agg, array_position, ANY, ALL, GIN on array | [`references/16-arrays.md`](references/16-arrays.md) | Arrays |
| JSON, JSONB, ->, ->>, #>, #>>, @>, jsonb_set, jsonb_insert, jsonb_path_query, jsonpath, JSON_TABLE, jsonb_ops, jsonb_path_ops | [`references/17-json-jsonb.md`](references/17-json-jsonb.md) | JSON / JSONB |
| uuid, gen_random_uuid, uuidv7, uuid-ossp, NUMERIC precision, money, serial, bigserial, IDENTITY column | [`references/18-uuid-numeric-money.md`](references/18-uuid-numeric-money.md) | UUID, numeric, money, identity |
| timestamp, timestamptz, AT TIME ZONE, interval, date_trunc, date_part, timezone, DST, infinity timestamp | [`references/19-timestamp-timezones.md`](references/19-timestamp-timezones.md) | Timestamps & time zones |
| tsvector, tsquery, to_tsvector, to_tsquery, plainto_tsquery, phraseto_tsquery, websearch_to_tsquery, ts_rank, ts_headline, FTS, full-text search | [`references/20-text-search.md`](references/20-text-search.md) | Full-text search |
| hstore | [`references/21-hstore.md`](references/21-hstore.md) | hstore extension |
| index decision, choose index type, multicolumn index, partial index, expression index, INCLUDE | [`references/22-indexes-overview.md`](references/22-indexes-overview.md) | Index decision matrix |
| B-tree, btree, deduplication, bottom-up index deletion, fillfactor, INCLUDE columns, covering index | [`references/23-btree-indexes.md`](references/23-btree-indexes.md) | B-tree indexes |
| GIN, GiST, KNN-GiST, jsonb_ops, jsonb_path_ops, EXCLUDE USING gist, fastupdate, gin_pending_list_limit | [`references/24-gin-gist-indexes.md`](references/24-gin-gist-indexes.md) | GIN & GiST indexes |
| BRIN, minmax_multi, bloom index, hash index, SP-GiST | [`references/25-brin-hash-spgist-bloom-indexes.md`](references/25-brin-hash-spgist-bloom-indexes.md) | BRIN, hash, SP-GiST, bloom |
| CREATE INDEX CONCURRENTLY, REINDEX CONCURRENTLY, INVALID index, pg_repack, pg_squeeze, REPACK, REPACK CONCURRENTLY, index bloat | [`references/26-index-maintenance.md`](references/26-index-maintenance.md) | Index maintenance |
| MVCC, xmin, xmax, cmin, cmax, infomask, tuple visibility, snapshot, xip, MultiXact | [`references/27-mvcc-internals.md`](references/27-mvcc-internals.md) | MVCC internals |
| VACUUM, autovacuum, VACUUM FULL, VACUUM FREEZE, autovacuum_vacuum_scale_factor, pg_stat_progress_vacuum, visibility map, parallel vacuum | [`references/28-vacuum-autovacuum.md`](references/28-vacuum-autovacuum.md) | VACUUM & autovacuum |
| transaction id wraparound, XID wraparound, datfrozenxid, autovacuum_freeze_max_age, MultiXact wraparound, 64-bit XID | [`references/29-transaction-id-wraparound.md`](references/29-transaction-id-wraparound.md) | TXID wraparound |
| HOT update, heap-only tuple, n_tup_hot_upd, HOT chain | [`references/30-hot-updates.md`](references/30-hot-updates.md) | HOT updates |
| TOAST, oversized attribute, storage strategy, PLAIN, EXTENDED, EXTERNAL, MAIN, pglz, lz4 compression | [`references/31-toast.md`](references/31-toast.md) | TOAST |
| shared_buffers, buffer manager, clock sweep, bgwriter, pg_buffercache, ring buffer | [`references/32-buffer-manager.md`](references/32-buffer-manager.md) | Buffer manager |
| WAL, wal_level, full_page_writes, archive_command, archive_library, wal_compression, wal_segment_size, pg_waldump | [`references/33-wal.md`](references/33-wal.md) | Write-Ahead Log |
| checkpoint, checkpointer, checkpoint_timeout, max_wal_size, checkpoint_completion_target, bgwriter_lru_maxpages, pg_stat_checkpointer | [`references/34-checkpoints-bgwriter.md`](references/34-checkpoints-bgwriter.md) | Checkpoints & bgwriter |
| partition, RANGE partition, LIST partition, HASH partition, partition pruning, ATTACH PARTITION, DETACH PARTITION, DEFAULT partition, partition-wise join | [`references/35-partitioning.md`](references/35-partitioning.md) | Declarative partitioning |
| inheritance, INHERITS, ONLY clause | [`references/36-inheritance.md`](references/36-inheritance.md) | Table inheritance |
| CHECK constraint, NOT NULL, UNIQUE, UNIQUE NULLS NOT DISTINCT, EXCLUDE constraint, NOT VALID, VALIDATE CONSTRAINT, deferrable | [`references/37-constraints.md`](references/37-constraints.md) | Constraints |
| foreign key, FOREIGN KEY, REFERENCES, ON DELETE CASCADE, ON DELETE SET NULL, deferrable FK, partitioned FK, circular FK | [`references/38-foreign-keys-deep.md`](references/38-foreign-keys-deep.md) | Foreign keys |
| CREATE TRIGGER, BEFORE trigger, AFTER trigger, INSTEAD OF, FOR EACH ROW, FOR EACH STATEMENT, NEW, OLD, transition table, REFERENCING NEW TABLE | [`references/39-triggers.md`](references/39-triggers.md) | Triggers |
| event trigger, CREATE EVENT TRIGGER, ddl_command_start, ddl_command_end, sql_drop, table_rewrite, pg_event_trigger_ddl_commands | [`references/40-event-triggers.md`](references/40-event-triggers.md) | Event triggers |
| BEGIN, COMMIT, ROLLBACK, SAVEPOINT, subtransaction, PREPARE TRANSACTION, 2PC, idle_in_transaction_session_timeout, autocommit | [`references/41-transactions.md`](references/41-transactions.md) | Transactions |
| Read Committed, Repeatable Read, Serializable, SSI, snapshot isolation, default_transaction_isolation, serialization failure, retry pattern | [`references/42-isolation-levels.md`](references/42-isolation-levels.md) | Isolation levels |
| lock, FOR UPDATE, FOR NO KEY UPDATE, FOR SHARE, FOR KEY SHARE, NOWAIT, SKIP LOCKED, AccessExclusiveLock, RowExclusiveLock, pg_locks, pg_blocking_pids, deadlock | [`references/43-locking.md`](references/43-locking.md) | Locking |
| advisory lock, pg_advisory_lock, pg_advisory_xact_lock, pg_try_advisory_lock | [`references/44-advisory-locks.md`](references/44-advisory-locks.md) | Advisory locks |
| LISTEN, NOTIFY, UNLISTEN, pg_notify, notification queue | [`references/45-listen-notify.md`](references/45-listen-notify.md) | LISTEN/NOTIFY |
| CREATE ROLE, GRANT, REVOKE, ALTER DEFAULT PRIVILEGES, pg_read_all_data, pg_monitor, SET ROLE, REASSIGN OWNED, INHERIT, NOINHERIT, BYPASSRLS | [`references/46-roles-privileges.md`](references/46-roles-privileges.md) | Roles & privileges |
| row-level security, RLS, CREATE POLICY, USING, WITH CHECK, FORCE ROW LEVEL SECURITY, ENABLE ROW LEVEL SECURITY | [`references/47-row-level-security.md`](references/47-row-level-security.md) | Row-Level Security |
| pg_hba.conf, authentication method, scram-sha-256, md5, peer, trust, ident, ldap, gss, cert auth | [`references/48-authentication-pg-hba.md`](references/48-authentication-pg-hba.md) | pg_hba.conf & auth |
| SSL, TLS, sslmode, verify-full, channel binding, server cert, client certificate, ssl_ciphers | [`references/49-tls-ssl.md`](references/49-tls-ssl.md) | TLS/SSL |
| pgcrypto, encrypt, decrypt, pgp_sym_encrypt, digest, crypt, gen_salt, TDE | [`references/50-encryption-pgcrypto.md`](references/50-encryption-pgcrypto.md) | pgcrypto |
| pgaudit, audit log, session auditing, object auditing, compliance logging | [`references/51-pgaudit.md`](references/51-pgaudit.md) | pgaudit |
| CREATE RULE, rule system, ON SELECT DO INSTEAD | [`references/52-rules-system.md`](references/52-rules-system.md) | Rule system |
| postgresql.conf, postgresql.auto.conf, GUC, pg_settings, ALTER SYSTEM, reload, pg_reload_conf, parameter context | [`references/53-server-configuration.md`](references/53-server-configuration.md) | Configuration |
| shared_buffers, effective_cache_size, work_mem, hash_mem_multiplier, maintenance_work_mem, autovacuum_work_mem, temp_buffers, wal_buffers, huge_pages | [`references/54-memory-tuning.md`](references/54-memory-tuning.md) | Memory tuning |
| ANALYZE, pg_statistic, pg_stats, default_statistics_target, extended statistics, CREATE STATISTICS, ndistinct, dependencies, MCV | [`references/55-statistics-planner.md`](references/55-statistics-planner.md) | Statistics & planner input |
| EXPLAIN, EXPLAIN ANALYZE, EXPLAIN (BUFFERS), Seq Scan, Index Scan, Index Only Scan, Bitmap Heap Scan, Nested Loop, Hash Join, Merge Join, Memoize, Gather, Append, row estimate, plan node | [`references/56-explain.md`](references/56-explain.md) | EXPLAIN deep dive |
| pg_stat_statements, query stats, top queries, calls, mean_exec_time, shared_blks_hit | [`references/57-pg-stat-statements.md`](references/57-pg-stat-statements.md) | pg_stat_statements |
| pg_stat_activity, wait_event, pg_stat_user_tables, pg_stat_user_indexes, pg_stat_database, pg_stat_io, pg_stat_wal, pg_stat_progress_*, performance diagnostics | [`references/58-performance-diagnostics.md`](references/58-performance-diagnostics.md) | pg_stat_* diagnostics |
| random_page_cost, seq_page_cost, cpu_tuple_cost, effective_io_concurrency, enable_seqscan, enable_hashjoin, join_collapse_limit, geqo, planner tuning | [`references/59-planner-tuning.md`](references/59-planner-tuning.md) | Planner tuning |
| parallel query, max_parallel_workers, max_parallel_workers_per_gather, max_parallel_maintenance_workers, parallel append, parallel hash join, force_parallel_mode | [`references/60-parallel-query.md`](references/60-parallel-query.md) | Parallel query |
| JIT, jit_above_cost, jit_inline_above_cost, LLVM, just-in-time compilation | [`references/61-jit-compilation.md`](references/61-jit-compilation.md) | JIT compilation |
| tablespace, CREATE TABLESPACE, default_tablespace, temp_tablespaces, SET TABLESPACE | [`references/62-tablespaces.md`](references/62-tablespaces.md) | Tablespaces |
| postmaster, backend process, autovacuum launcher, walwriter, walsender, walreceiver, archiver, bgwriter, checkpointer, logical replication worker, shared memory architecture, fork per connection | [`references/63-internals-architecture.md`](references/63-internals-architecture.md) | Process & memory architecture |
| pg_catalog, pg_class, pg_attribute, pg_index, pg_namespace, pg_constraint, pg_proc, pg_type, pg_depend, pg_inherits, pg_partitioned_table, pg_publication, pg_subscription, pg_extension, pg_authid, pg_roles, pg_database, pg_tablespace, pg_settings, relkind, information_schema, ECHO_HIDDEN, catalog exploration | [`references/64-system-catalogs.md`](references/64-system-catalogs.md) | System catalogs & exploration recipes |
| collation, ICU, libc, deterministic collation, nondeterministic collation, case-insensitive UNIQUE, collation version, encoding, UTF-8, client_encoding | [`references/65-collations-encoding.md`](references/65-collations-encoding.md) | Collations & encoding |
| COPY, \\copy, bulk load, CSV import, HEADER, DELIMITER, FREEZE, ON_ERROR, LOG_VERBOSITY, parallel COPY | [`references/66-bulk-operations-copy.md`](references/66-bulk-operations-copy.md) | COPY / bulk |
| psql, \\d, \\dt, \\di, \\df, \\dn, \\dx, \\timing, \\watch, \\gexec, pg_isready, createdb, dropdb, vacuumdb, reindexdb, clusterdb | [`references/67-cli-tools.md`](references/67-cli-tools.md) | CLI tools |
| pgbench, benchmark, TPC-B, -c clients, -j threads, scaling factor, custom pgbench script | [`references/68-pgbench.md`](references/68-pgbench.md) | pgbench |
| CREATE EXTENSION, ALTER EXTENSION UPDATE, pg_extension, trusted extension, contrib | [`references/69-extensions.md`](references/69-extensions.md) | Extensions overview |
| FDW, foreign data wrapper, CREATE FOREIGN TABLE, postgres_fdw, file_fdw, IMPORT FOREIGN SCHEMA, dblink, pushdown | [`references/70-fdw.md`](references/70-fdw.md) | FDW |
| large object, lo_create, lo_open, lo_read, lo_export, lo_import, pg_largeobject, vacuumlo, bytea vs LO | [`references/71-large-objects.md`](references/71-large-objects.md) | Large objects |
| extension development, PGXS, PG_MODULE_MAGIC, PG_FUNCTION_INFO_V1, .control, hooks, C extension | [`references/72-extension-development.md`](references/72-extension-development.md) | Extension development |
| streaming replication, primary_conninfo, primary_slot_name, standby.signal, recovery.signal, synchronous_standby_names, synchronous_commit, cascading replication, hot_standby_feedback | [`references/73-streaming-replication.md`](references/73-streaming-replication.md) | Streaming replication |
| logical replication, CREATE PUBLICATION, CREATE SUBSCRIPTION, FOR ALL TABLES, FOR TABLES IN SCHEMA, row filter, column list, replication origin, DDL replication, two-phase decoding | [`references/74-logical-replication.md`](references/74-logical-replication.md) | Logical replication |
| replication slot, pg_create_physical_replication_slot, pg_create_logical_replication_slot, max_slot_wal_keep_size, max_replication_slots, max_wal_senders, pg_replication_slots, slot invalidation | [`references/75-replication-slots.md`](references/75-replication-slots.md) | Replication slots |
| logical decoding, pgoutput, wal2json, decoderbufs, test_decoding, CDC, REPLICA IDENTITY, START_REPLICATION SLOT LOGICAL | [`references/76-logical-decoding.md`](references/76-logical-decoding.md) | Logical decoding |
| standby, hot standby, max_standby_streaming_delay, hot_standby_feedback, pg_promote, pg_rewind, timeline ID, failover, switchover | [`references/77-standby-failover.md`](references/77-standby-failover.md) | Standby & failover |
| HA, high availability, Patroni, repmgr, pg_auto_failover, Stolon, cluster manager, fencing, split brain, witness | [`references/78-ha-architectures.md`](references/78-ha-architectures.md) | HA architectures |
| Patroni, patroni.yml, DCS, etcd, consul, zookeeper, REST API, /failover, /switchover, watchdog | [`references/79-patroni.md`](references/79-patroni.md) | Patroni |
| connection pool, pool sizing, transaction pool, session pool, statement pool, process-per-connection | [`references/80-connection-pooling.md`](references/80-connection-pooling.md) | Connection pooling concepts |
| pgBouncer, pool_mode, default_pool_size, reserve_pool_size, server_idle_timeout, prepared statement pgbouncer, SHOW POOLS, SHOW STATS | [`references/81-pgbouncer.md`](references/81-pgbouncer.md) | pgBouncer |
| monitoring, postgres_exporter, prometheus, pg_stat_*, alerting thresholds, log-based metrics | [`references/82-monitoring.md`](references/82-monitoring.md) | Monitoring |
| pg_dump, pg_dumpall, pg_restore, custom format, directory format, parallel dump, --filter, --on-conflict-do-nothing | [`references/83-backup-pg-dump.md`](references/83-backup-pg-dump.md) | Logical backup |
| pg_basebackup, base backup, archive_command, restore_command, recovery_target_time, recovery_target_xid, PITR, point-in-time recovery, continuous archiving | [`references/84-backup-physical-pitr.md`](references/84-backup-physical-pitr.md) | Physical backup & PITR |
| pgBackRest, Barman, WAL-G, incremental backup, retention policy, S3 backup | [`references/85-backup-tools.md`](references/85-backup-tools.md) | Backup tooling |
| pg_upgrade, --link, --clone, major upgrade, statistics preservation, preflight check | [`references/86-pg-upgrade.md`](references/86-pg-upgrade.md) | pg_upgrade |
| major version upgrade, blue-green upgrade, logical replication upgrade, near-zero downtime, catalog version | [`references/87-major-version-upgrade.md`](references/87-major-version-upgrade.md) | Major-version upgrade strategy |
| corruption, data_checksums, pg_amcheck, pg_checksums, pg_resetwal, single-user mode, zero_damaged_pages | [`references/88-corruption-recovery.md`](references/88-corruption-recovery.md) | Corruption recovery |
| pg_rewind, divergent timeline, wal_log_hints, --source-server, --source-pgdata | [`references/89-pg-rewind.md`](references/89-pg-rewind.md) | pg_rewind |
| disaster recovery, RPO, RTO, DR drill, runbook, failover bookkeeping | [`references/90-disaster-recovery.md`](references/90-disaster-recovery.md) | Disaster recovery |
| docker postgres, docker-entrypoint-initdb.d, POSTGRES_PASSWORD, healthcheck postgres container, volume PGDATA | [`references/91-docker-postgres.md`](references/91-docker-postgres.md) | Docker postgres image |
| Kubernetes postgres, CloudNativePG, CNPG, postgres-operator, Zalando, Crunchy PGO, StatefulSet | [`references/92-kubernetes-operators.md`](references/92-kubernetes-operators.md) | K8s operators |
| pg_trgm, trigram, similarity, % operator, GIN trigram, LIKE acceleration, word_similarity | [`references/93-pg-trgm.md`](references/93-pg-trgm.md) | pg_trgm |
| pgvector, vector, embedding, HNSW, IVFFLAT, <->, <=>, <#>, halfvec, sparsevec, m, ef_construction, ef_search, lists, probes, ANN | [`references/94-pgvector.md`](references/94-pgvector.md) | pgvector |
| PostGIS, geometry, geography, SRID, ST_Transform, ST_DWithin, ST_Intersects, ST_Buffer, spatial index | [`references/95-postgis.md`](references/95-postgis.md) | PostGIS |
| TimescaleDB, hypertable, continuous aggregate, compression, retention policy, chunk | [`references/96-timescaledb.md`](references/96-timescaledb.md) | TimescaleDB |
| Citus, distributed table, reference table, coordinator, worker, shard, colocated join, columnar storage | [`references/97-citus.md`](references/97-citus.md) | Citus |
| pg_cron, cron.schedule, cron.job, cron.job_run_details, scheduled VACUUM, scheduled REFRESH MATERIALIZED VIEW | [`references/98-pg-cron.md`](references/98-pg-cron.md) | pg_cron |
| pg_partman, partman.create_parent, run_maintenance_proc, partition retention, partman.part_config, sub-partition | [`references/99-pg-partman.md`](references/99-pg-partman.md) | pg_partman |
| pg_textsearch, BM25, bm25 index, `<@>`, to_bm25query, ranked keyword search, hybrid search, RRF, reciprocal rank fusion | [`references/103-pg-textsearch.md`](references/103-pg-textsearch.md) | pg_textsearch (BM25 ranked search) |
| pgmq, message queue, pgmq.send, pgmq.read, pgmq.pop, pgmq.archive, visibility timeout, vt, outbox, job queue, FIFO queue | [`references/104-pgmq.md`](references/104-pgmq.md) | pgmq (Postgres message queue) |
| PG14, PG15, PG16, PG17, PG18, PG19, release notes, version features, support policy, EOL, minor release, CVE, REPACK | [`references/100-pg-versions-features.md`](references/100-pg-versions-features.md) | Per-major-version feature highlights |
| managed Postgres, managed PaaS, hosted Postgres, bare-metal, self-hosted, superuser restriction, extension allowlist, shared_preload_libraries restriction, vendor lock-in | [`references/101-managed-vs-baremetal.md`](references/101-managed-vs-baremetal.md) | Managed vs bare-metal trade-offs (provider-agnostic) |
| recipe, cookbook, bloat triage, slow-query investigation, deadlock investigation, replication lag investigation, PITR walkthrough, upgrade playbook, catalog exploration | [`references/102-skill-cookbook.md`](references/102-skill-cookbook.md) | Multi-file recipes & catalog exploration |


## Disambiguation Tips


Some terms route to multiple files — load both when in doubt.

| Term | Primary file | Secondary file | Why |
|---|---|---|---|
| `VACUUM` blocking | [28-vacuum-autovacuum.md](references/28-vacuum-autovacuum.md) | [27-mvcc-internals.md](references/27-mvcc-internals.md), [29-transaction-id-wraparound.md](references/29-transaction-id-wraparound.md) | Why VACUUM exists is MVCC; what it must do is bounded by wraparound |
| `EXPLAIN` plan | [56-explain.md](references/56-explain.md) | [55-statistics-planner.md](references/55-statistics-planner.md), [59-planner-tuning.md](references/59-planner-tuning.md) | Misestimates point to stats; tuning may need GUC changes |
| `Index choice` | [22-indexes-overview.md](references/22-indexes-overview.md) | [23-btree-indexes.md](references/23-btree-indexes.md) through [25-brin-hash-spgist-bloom-indexes.md](references/25-brin-hash-spgist-bloom-indexes.md) | Overview routes to specifics |
| `Deadlock` | [43-locking.md](references/43-locking.md) | [42-isolation-levels.md](references/42-isolation-levels.md) | Predicate locks (SSI) cause different deadlocks |
| `Replication is lagging` | [73-streaming-replication.md](references/73-streaming-replication.md) | [75-replication-slots.md](references/75-replication-slots.md), [82-monitoring.md](references/82-monitoring.md) | Lag could be stream pressure or slot retention |
| `Upgrade` | [86-pg-upgrade.md](references/86-pg-upgrade.md) | [87-major-version-upgrade.md](references/87-major-version-upgrade.md) | pg_upgrade is one strategy; the other file covers blue/green and logical-repl-based upgrades |
| `JSON column performance` | [17-json-jsonb.md](references/17-json-jsonb.md) | [24-gin-gist-indexes.md](references/24-gin-gist-indexes.md) | JSONB indexing happens via GIN |
| `Full-text search ranking` | [20-text-search.md](references/20-text-search.md) | [103-pg-textsearch.md](references/103-pg-textsearch.md), [24-gin-gist-indexes.md](references/24-gin-gist-indexes.md) | Core FTS ranks with `ts_rank` over GIN; BM25 ranking needs pg_textsearch |
| `Job queue / message queue` | [104-pgmq.md](references/104-pgmq.md) | [43-locking.md](references/43-locking.md), [45-listen-notify.md](references/45-listen-notify.md) | pgmq packages the `SKIP LOCKED` pattern from 43; NOTIFY in 45 wakes consumers |
| `Bulk load slow` | [66-bulk-operations-copy.md](references/66-bulk-operations-copy.md) | [33-wal.md](references/33-wal.md), [28-vacuum-autovacuum.md](references/28-vacuum-autovacuum.md) | WAL volume and post-load vacuum dominate |
| `Catalog exploration / inspection` | [64-system-catalogs.md](references/64-system-catalogs.md) | [102-skill-cookbook.md](references/102-skill-cookbook.md) | The cookbook has runnable recipes |
| `shared_buffers` | [32-buffer-manager.md](references/32-buffer-manager.md) | [54-memory-tuning.md](references/54-memory-tuning.md) | Mechanics live in 32; sizing guidance lives in 54 |
| `work_mem` / `hash_mem_multiplier` | [54-memory-tuning.md](references/54-memory-tuning.md) | [59-planner-tuning.md](references/59-planner-tuning.md), [56-explain.md](references/56-explain.md) | Sizing in 54; planner cost interaction in 59; spill-to-disk diagnosis in 56 |
| `archive_command` / `archive_library` | [33-wal.md](references/33-wal.md) | [84-backup-physical-pitr.md](references/84-backup-physical-pitr.md), [85-backup-tools.md](references/85-backup-tools.md) | WAL-level mechanics in 33; PITR consumer side in 84; pgBackRest/Barman/WAL-G in 85 |
| `wal_level` | [33-wal.md](references/33-wal.md) | [74-logical-replication.md](references/74-logical-replication.md), [76-logical-decoding.md](references/76-logical-decoding.md) | Setting + implications in 33; `logical` consumers in 74/76 |
| `pg_basebackup` | [84-backup-physical-pitr.md](references/84-backup-physical-pitr.md) | [89-pg-rewind.md](references/89-pg-rewind.md), [73-streaming-replication.md](references/73-streaming-replication.md) | Base backup in 84; rebuild-after-divergence alternative in 89; standby provisioning in 73 |
| `Partition rotation / retention` | [35-partitioning.md](references/35-partitioning.md) | [99-pg-partman.md](references/99-pg-partman.md), [98-pg-cron.md](references/98-pg-cron.md) | Native partitioning in 35; lifecycle automation in 99; scheduling in 98 |
| `Slow query` | [56-explain.md](references/56-explain.md) | [57-pg-stat-statements.md](references/57-pg-stat-statements.md), [58-performance-diagnostics.md](references/58-performance-diagnostics.md), [55-statistics-planner.md](references/55-statistics-planner.md), [102-skill-cookbook.md](references/102-skill-cookbook.md) | Workload-wide via 57; plan via 56; misestimate root cause in 55; full investigation walk in 102 |
| `Connection storm / too many connections` | [80-connection-pooling.md](references/80-connection-pooling.md) | [81-pgbouncer.md](references/81-pgbouncer.md), [63-internals-architecture.md](references/63-internals-architecture.md), [46-roles-privileges.md](references/46-roles-privileges.md) | Pooling concepts in 80; pgBouncer config in 81; fork-per-connection cost in 63; per-role connection limits in 46 |
| `Failover / promote` | [77-standby-failover.md](references/77-standby-failover.md) | [78-ha-architectures.md](references/78-ha-architectures.md), [79-patroni.md](references/79-patroni.md), [89-pg-rewind.md](references/89-pg-rewind.md) | Manual mechanics in 77; cluster-manager landscape in 78; Patroni-specific in 79; rejoin-old-primary in 89 |


## Versioning & Provider Neutrality


- **Target compatibility baseline:** every SQL example must run on PostgreSQL 16 unless explicitly marked otherwise.
- **Version-pin docs URLs.** Cite `https://www.postgresql.org/docs/16/...`, not `/docs/current/`. The `current` alias moves with each annual release.
- **Provider neutrality is mandatory.** Never recommend a managed provider over another. When discussing managed-service limitations, phrase categorically ("most managed providers disable untrusted PLs"), not by name.


## Sources


Primary documentation roots (re-fetch before citing in any reference file; version-pin URLs to the matching major):

- PostgreSQL 14 manual (cross-version notes only): <https://www.postgresql.org/docs/14/index.html>
- PostgreSQL 15 manual (cross-version notes only): <https://www.postgresql.org/docs/15/index.html>
- PostgreSQL 16 manual (default baseline): <https://www.postgresql.org/docs/16/index.html>
- PostgreSQL 17 manual: <https://www.postgresql.org/docs/17/index.html>
- PostgreSQL 18 manual: <https://www.postgresql.org/docs/18/index.html>
- PostgreSQL 19 release notes (RC until GA, planned 2026-11-19): <https://www.postgresql.org/docs/19/release-19.html>
- Security advisories (CVE list per minor release): <https://www.postgresql.org/support/security/>
- Per-version release notes: <https://www.postgresql.org/docs/release/>
- Versioning + support policy: <https://www.postgresql.org/support/versioning/>
- PostgreSQL Wiki: <https://wiki.postgresql.org/>
- Source code mirror: <https://github.com/postgres/postgres>
