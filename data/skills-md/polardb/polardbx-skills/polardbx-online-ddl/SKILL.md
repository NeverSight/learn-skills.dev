---
name: polardbx-online-ddl
description: |
  Online DDL safety assessment and lock-free execution for PolarDB-X 2.0 Enterprise Edition. Determines if DDL locks the table via EXPLAIN ONLINE_DDL, rewrites with ALGORITHM=OMC for lock-free execution, checks long transactions before DDL, and guides safe DDL execution with user confirmation.
  Use when executing DDL on PolarDB-X and needing to assess table-locking risk, when DDL would lock the table and a lock-free alternative is needed, or when checking long transactions before DDL.
  Triggers: "Online DDL", "DDL锁表", "lock-free DDL", "OMC", "MDL lock", "DDL安全", "EXPLAIN ONLINE_DDL", "DDL进度", "长事务检查", "无锁变更", "DDL locks table", "lock-free change", "DDL progress", "safe DDL"
metadata:
  version: 0.1.1
---

# PolarDB-X Online DDL — Safe DDL Assessment & Lock-Free Execution

Assess whether DDL operations lock the table and execute them safely on PolarDB-X 2.0 Enterprise Edition (AUTO mode). This skill covers the complete DDL safety workflow: assessment → lock-free rewriting → long transaction checks → user confirmation → execution.

**Scope**: PolarDB-X 2.0 Enterprise Edition + AUTO mode database only.

**Version requirement**: Instance version >= `5.4.20-20241224` for `EXPLAIN ONLINE_DDL` and OMC support. For older versions, see reference guide for legacy compatibility methods.

## Core Workflow (Follow each time)

> **Important**: DDL is a high-risk operation. NEVER execute DDL directly without presenting assessment results and obtaining explicit user confirmation.

1. **Assess table-locking risk** with `EXPLAIN ONLINE_DDL`:
   ```sql
   EXPLAIN ONLINE_DDL ALTER TABLE ...;
   ```
   Check the `DDL TYPE` in the result.

2. **Determine execution strategy** based on `DDL TYPE`:
   - `ONLINE_DDL` → Execute the original SQL directly (no table lock).
   - `LOCK_TABLE` → Rewrite with `ALGORITHM=OMC` and re-EXPLAIN to confirm lock-free:
     ```sql
     EXPLAIN ONLINE_DDL ALTER TABLE t1 MODIFY COLUMN b text, ALGORITHM=OMC;
     -- Confirm: DDL TYPE = ONLINE_DDL, ALGORITHM = OMC
     ```

3. **Check long transactions** on the target table:
   ```sql
   SELECT TRX_ID, PROCESS_ID, SCHEMA, START_TIME,
          ROUND(DURATION_TIME/1000/1000, 3) AS 'Duration(s)',
          SQL AS 'Current SQL'
   FROM INFORMATION_SCHEMA.POLARDBX_TRX
   WHERE DURATION_TIME > 15 * 1000 * 1000;
   ```
   If long transactions exist, assess risk before proceeding.

4. **Present results to user and obtain explicit confirmation** before executing DDL.

## DDL TYPE / ALGORITHM Quick Reference

| DDL TYPE | ALGORITHM | Description | Business Impact |
|----------|-----------|-------------|-----------------|
| ONLINE_DDL | INSTANT / META_ONLY | Metadata-only change, completes in seconds | Minimal |
| ONLINE_DDL | INPLACE / OMC / OSC | No table lock, duration depends on data volume | Small |
| LOCK_TABLE | COPY | Locks table, table not writable during execution | Large |

## Common DDL Operations Assessment

| Operation | Typical DDL TYPE | ALGORITHM |
|-----------|-----------------|-----------|
| Add column | ONLINE_DDL | INSTANT |
| Add partition | ONLINE_DDL | META_ONLY |
| Add index | ONLINE_DDL | INPLACE |
| Modify column type | LOCK_TABLE | COPY → rewrite with OMC |
| Drop column | ONLINE_DDL | INPLACE |

## OMC Lock-Free Column Type Change

When `EXPLAIN ONLINE_DDL` returns `LOCK_TABLE`, append `ALGORITHM=OMC` to avoid table locking:

```sql
-- Before: locks table
ALTER TABLE t1 MODIFY COLUMN c bigint;

-- After: lock-free via OMC
ALTER TABLE t1 MODIFY COLUMN c bigint, ALGORITHM=OMC;
```

Here, "lock-free" means avoiding COPY-style table locking that prevents writes during the data-change phase. Like INPLACE and INSTANT DDL, OMC still acquires metadata locks; metadata-lock and cutover waits can occur.

**OMC trade-offs**: Executes slower and consumes more resources than native DDL. Only use when avoiding table lock is critical.

## Long Transaction Decision Matrix

| Situation | Recommended Action |
|-----------|-------------------|
| Long transaction is unexpected | Investigate business logic, resolve before DDL |
| Long transaction is expected + high priority | Postpone DDL |
| Long transaction is expected + low priority | Can proceed; DDL will kill the connection (default 15s timeout) |

**Side effect of MDL preemption**: Connections with transactions/queries exceeding 15 seconds will be killed. Avoid DDL during DataWorks/DTS/mysqldump executions.

## Monitor DDL Progress

For long-running DDL operations (OMC, INPLACE with data backfill):

```sql
SELECT JOB_ID, TABLE_NAME, STATE, PROGRESS, CURRENT_SPEED, DDL_STMT
FROM INFORMATION_SCHEMA.DDL_PROGRESS;
```

## Best Practices

1. **Always EXPLAIN before executing**: Never run DDL without first checking `EXPLAIN ONLINE_DDL`.
2. **Prefer native Online DDL over OMC**: Only use OMC when the operation would lock the table.
3. **Check long transactions**: Especially for tables with known long-running sync tasks.
4. **Schedule DDL during low-traffic windows**: Online DDL consumes IO/CPU resources and can encounter metadata-lock waits.
5. **Monitor progress for large tables**: Use `DDL_PROGRESS` view for operations involving data backfill.

## Reference

| Reference | Description |
|-----------|-------------|
| [references/online-ddl.md](references/online-ddl.md) | Complete Online DDL guide: EXPLAIN ONLINE_DDL, OMC, MDL optimizations, long transaction checks, DMS integration, legacy version compatibility |
