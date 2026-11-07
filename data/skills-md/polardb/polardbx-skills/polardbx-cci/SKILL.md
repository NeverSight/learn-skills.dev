---
name: polardbx-cci
description: |
  Create and use Clustered Columnar Index (CCI) for OLAP/HTAP analytical queries on PolarDB-X 2.0 Enterprise Edition. Covers CCI creation syntax, partition/sort key selection, query optimization, snapshots (AS OF TSO), SHOW/CHECK commands, DDL limitations, CCI vs GSI.
  Use when the user needs analytical queries (aggregation, wide table scans, reports) on PolarDB-X, wants to enable HTAP, or asks about columnar storage.
  Triggers: "CCI", "列存索引", "columnar index", "OLAP", "分析查询", "HTAP", "宽表聚合", "CLUSTERED COLUMNAR", "行列混存", "列存快照", "AS OF TSO", "SHOW COLUMNAR", "排序键", "sort key"
metadata:
  version: 0.4.1
---

# PolarDB-X CCI — Clustered Columnar Index for OLAP/HTAP

CCI accelerates OLAP analytical queries on PolarDB-X Enterprise Edition (AUTO mode) via columnar storage on OSS. OLTP uses row-store; OLAP uses CCI — transparent HTAP.

**Scope**: Enterprise Edition + AUTO mode.

| Feature | Minimum Version |
|---------|----------------|
| CCI creation | >= 5.4.19 |
| Snapshot features | >= 5.4.19-20250305 or >= 5.4.20 |
| COLUMNAR_OPTIONS / columnar_set_config | >= 5.4.20 |

## Core Workflow

1. Confirm OLAP need (aggregation, reports, HTAP)
2. Select partition key (frequent GROUP BY / JOIN column, HASH recommended)
3. Select sort key (range query column or ORDER BY column)
4. Create CCI with `partition_count = nodes * cores`
5. `SET ENABLE_COLUMNAR_OPTIMIZER = true;` for automatic routing
6. Verify with `EXPLAIN`

## When to Use / Not Use

| Use CCI | Don't use CCI |
|---------|---------------|
| Wide table aggregation (SUM/COUNT/AVG) | Point queries / small range scans → use GSI |
| Complex reports and dashboards | Tables < 100K rows |
| HTAP: OLTP + OLAP on same data | Real-time read requirements (CCI has CDC delay) |
| Cold data archival with TTL | Write-heavy tables requiring instant read-after-write |
| Historical snapshot query (AS OF TSO) | No PK on table (CCI requires explicit PK) |

## Creation Syntax

```sql
-- Full syntax
CREATE CLUSTERED COLUMNAR INDEX index_name
  ON tbl_name (sort_key_col, ...)
  [PARTITION BY HASH|KEY|RANGE|LIST(...) PARTITIONS n]
  [COLUMNAR_OPTIONS = '{"key":"value", ...}']

-- Add to existing table
CREATE CLUSTERED COLUMNAR INDEX cci_seller
  ON t_order(seller_id)
  PARTITION BY HASH(order_id) PARTITIONS 16;

-- With snapshot
CREATE CLUSTERED COLUMNAR INDEX cci ON tb1(id)
  PARTITION BY KEY(id) PARTITIONS 16
  COLUMNAR_OPTIONS = '{"TYPE":"SNAPSHOT","SNAPSHOT_RETENTION_DAYS":"7","AUTO_GEN_COLUMNAR_SNAPSHOT_INTERVAL":"30"}';

-- Inline in CREATE TABLE
CREATE TABLE t_order (
  id BIGINT PRIMARY KEY, seller_id BIGINT, amount DECIMAL(10,2),
  CLUSTERED COLUMNAR INDEX cci_seller(seller_id)
    PARTITION BY KEY(seller_id) PARTITIONS 16
) PARTITION BY KEY(id) PARTITIONS 16;
```

**Constraints**: Table must have PK. Sort key is REQUIRED. Index name is REQUIRED. No prefix index. Partition defaults to PK + HASH if not specified. One CCI per table by default (`SET MAX_CCI_COUNT = N;` to allow more).

## Key Selection Quick Reference

| Item | Recommendation |
|------|---------------|
| **Partition strategy** | HASH/KEY (default). RANGE for TTL cold archive. LIST for multi-tenant. |
| **Partition key** | Uniformly distributed, frequent GROUP BY/JOIN column. **Avoid date/time** (use as secondary partition instead). |
| **Partition count** | `nodes * cores`. Keep consistent across JOIN-related tables. |
| **Sort key** | Range query column, or ORDER BY column, or partition key. |
| **Verify** | `CHECK COLUMNAR PARTITION db.tbl;` — check for data skew. |

## COLUMNAR_OPTIONS

| Parameter | Default | Description |
|-----------|---------|-------------|
| `TYPE` | `default` | `default` / `snapshot` / `archive` |
| `SNAPSHOT_RETENTION_DAYS` | `7` | Snapshot retention (1-366). TYPE=snapshot only. |
| `AUTO_GEN_COLUMNAR_SNAPSHOT_INTERVAL` | `-1` | Auto snapshot interval in minutes (>=5 or -1). TYPE=snapshot only. |

TYPE transitions: default↔snapshot (OK), default↔archive (OK), archive↔snapshot (**FORBIDDEN**).

## Query with CCI

```sql
-- Auto routing (needs ENABLE_COLUMNAR_OPTIMIZER = true on columnar read-only instance)
SELECT seller_id, SUM(amount) FROM t_order GROUP BY seller_id;

-- Force CCI
SELECT * FROM t_order FORCE INDEX(cci_seller) WHERE seller_id = 's1';
SELECT /*+TDDL:INDEX(t_order, cci_seller)*/ * FROM t_order;
SELECT * FROM t_order USE INDEX(cci_seller) WHERE seller_id = 's1';
SELECT * FROM t_order IGNORE INDEX(cci_seller) WHERE seller_id = 's1';

-- Multi-table JOIN
SELECT a.*, b.order_id FROM t_seller a
  JOIN t_order b FORCE INDEX(cci_seller) ON a.seller_id = b.seller_id;
```

## Snapshot (AS OF TSO)

```sql
-- Generate snapshot (returns TSO)
CALL polardbx.columnar_flush('schema', 'table', 'cci_name');  -- table-level
CALL polardbx.columnar_flush();                                 -- instance-level

-- Query snapshot
SELECT * FROM tb1 AS OF TSO <tso> FORCE INDEX(cci) ORDER BY id;

-- Restore from snapshot
INSERT INTO target SELECT * FROM source AS OF TSO <tso> FORCE INDEX(cci);
```

Snapshot uses latest table schema regardless of snapshot point. INSERT SELECT requires `autocommit=true`.

## Management Commands

```sql
SHOW COLUMNAR INDEX;                         -- CCI metadata (partition, sort key, status)
SHOW COLUMNAR STATUS;                        -- CCI data status (see fields below)
SHOW FULL COLUMNAR STATUS;                   -- instance-level
SHOW DDL;                                    -- creation progress
CHECK COLUMNAR INDEX idx ON tbl;             -- data consistency
CHECK COLUMNAR PARTITION tbl;                -- partition distribution
CHECK COLUMNAR SNAPSHOT tbl;                 -- snapshot status
```

**SHOW COLUMNAR STATUS output fields**: `TSO | SCHEMA_NAME | TABLE_NAME | INDEX_NAME | ID | ROWS | CSV_FILES | ORC_FILES | DEL_FILES | FILES_SIZE | DN_TABLE_SIZE | COMPRESSION_RATIO | STATUS`

- `ROWS`: row count in CCI
- `CSV_FILES` / `ORC_FILES` / `DEL_FILES`: file counts by type
- `FILES_SIZE`: total file size on OSS
- `COMPRESSION_RATIO`: compression ratio

## Drop / Rename / Modify

```sql
DROP INDEX cci_name ON tbl;
ALTER TABLE tbl DROP INDEX cci_name;
ALTER TABLE tbl RENAME INDEX old_cci TO new_cci;
DROP COLUMNAR INDEX FOR TABLES IN db_name;

-- Modify parameters at runtime
CALL polardbx.columnar_set_config(param_key, param_val);                          -- instance-level
CALL polardbx.columnar_set_config(cci_id, param_key, param_val);                  -- by CCI ID
CALL polardbx.columnar_set_config(schema, table, cci_name, param_key, param_val); -- by name
```

## CCI vs Clustered GSI

| Feature | Clustered GSI | CCI |
|---------|--------------|-----|
| Storage | Row-store (DN local) | Columnar (OSS, lower cost) |
| Best for | **Point queries, small range scans** | Large scans, aggregations |
| Data freshness | **Real-time** (strong consistency) | **Eventually consistent** (CDC delay, seconds-level lag) |
| Snapshot | No | Yes (AS OF TSO) |

**Key guidance**: For point lookups (e.g., `WHERE user_id = ?`), always recommend **Clustered GSI** (row-store), NOT CCI. CCI has eventual consistency due to CDC replication delay and is optimized for scan/aggregation workloads, not single-row lookups.

## DDL Limitations

Supported: DROP/TRUNCATE/RENAME TABLE, ADD/DROP/MODIFY COLUMN, ADD/DROP INDEX, RENAME CCI INDEX, ADD RANGE PARTITION.
**Not supported**: DROP PRIMARY KEY, ALTER INDEX VISIBLE/INVISIBLE, CCI partition changes.

Control: `SET [GLOBAL] forbid_ddl_with_cci = true|false;`
Modify CCI critical columns: `SET ENABLE_MODIFY_CCI_CRITICAL_COLUMN = TRUE;` (may trigger rebuild).

## Row-Column Routing

`ENABLE_COLUMNAR_OPTIMIZER = true` → OLTP queries go to row-store, OLAP queries go to CCI automatically. Auto-routing only works on **columnar read-only instances**; on primary instances use FORCE INDEX.

## CCI + TTL

Hot data in row-store, cold data archived to CCI on OSS. Use the `polardbx-ttl20` skill for setup.

## Best Practices

1. Partition key = most frequent GROUP BY/JOIN column, HASH strategy.
2. Sort key = range query column or ORDER BY column.
3. Partition count = nodes * cores; keep consistent across JOIN tables.
4. Use EXPLAIN to verify CCI path.
5. ENABLE_COLUMNAR_OPTIMIZER for transparent routing.
6. Combine with TTL for cold data cost optimization.
7. Verify partition quality: `CHECK COLUMNAR PARTITION`.
8. Create multiple CCIs for different analytical dimensions (e.g., by seller, by region).

## Reference

| Reference | Description |
|-----------|-------------|
| [references/cci.md](references/cci.md) | Deep dive: full partition syntax, secondary partitions, detailed DDL limitations, data type restrictions, column change constraints, parameter config, FAQ |
