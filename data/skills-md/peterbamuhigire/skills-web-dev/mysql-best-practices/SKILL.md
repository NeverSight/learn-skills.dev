---
name: mysql-best-practices
description: "MySQL 8.x best practices for high-performance, secure SaaS applications. Use when designing database schemas, writing queries, optimizing performance, implementing multi-tenant isolation, configuring servers, setting up replication, hardening security, or troubleshooting slow queries. Covers indexing, EXPLAIN analysis, transactions, locking, advanced SQL (CTEs, window functions), backup, and server tuning."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# MySQL Best Practices for SaaS

Production-grade MySQL patterns for high-performance, secure, scalable SaaS applications.

**Core Principle:** Performance is query response time. Optimize queries and indexes first, tune server second, scale hardware last.

**Access Policy (Required):** Frontend clients must never access the database directly. All data access must flow through backend services exposed via APIs.

**Deep References:** `references/query-performance.md`, `references/indexing-deep-dive.md`, `references/server-tuning-mycnf.md`, `references/security-hardening.md`, `references/high-availability.md`, `references/advanced-sql-patterns.md`, `references/backup-recovery.md`, `references/transaction-locking.md`

**SQL References:** `references/stored-procedures.sql`, `references/triggers.sql`, `references/partitioning.sql`

## Deployment Environments

| Environment | OS | Database | Notes |
|---|---|---|---|
| **Development** | Windows 11 (WAMP) | MySQL 8.4.7 | User: `root`, no password |
| **Staging** | Ubuntu VPS | MySQL 8.x | User: `peter`, password required |
| **Production** | Debian VPS | MySQL 8.x | User: `peter`, password required |

**Cross-platform rules:**
- Always use `utf8mb4_unicode_ci` collation (never `utf8mb4_0900_ai_ci` or `utf8mb4_general_ci`)
- Never use platform-specific SQL features; test on MySQL 8.x
- Production migrations go in `database/migrations-production/` with `-production` suffix

## When to Use

✅ Designing MySQL schemas ✅ Optimizing queries ✅ Multi-tenant isolation ✅ Transactional systems ✅ Security hardening ✅ Server tuning ✅ Replication setup ✅ Advanced SQL

❌ NoSQL databases ❌ OLAP/data warehouses ❌ Non-MySQL databases

---

## Schema Design

### Database & Table Defaults

```sql
CREATE DATABASE saas_platform
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE users (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tenant_id INT UNSIGNED NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_tenant (tenant_id),
  UNIQUE KEY uk_tenant_email (tenant_id, email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
```

**Always:** `ENGINE=InnoDB` (ACID, row-level locking, crash recovery), `utf8mb4`, `ROW_FORMAT=DYNAMIC`.

### Data Types — Choose Smallest Sufficient

```sql
-- Integers (use smallest that fits)
TINYINT UNSIGNED     -- 0-255 (status codes, booleans)
SMALLINT UNSIGNED    -- 0-65,535 (categories, small counts)
INT UNSIGNED         -- 0-4.2B (most FKs, tenant_id)
BIGINT UNSIGNED      -- >4.2B (PKs, high-volume tables)

-- Financial — NEVER use FLOAT/DOUBLE
amount DECIMAL(13, 2) NOT NULL  -- Exact precision

-- Fixed-length codes
currency CHAR(3) NOT NULL DEFAULT 'UGX'
country_code CHAR(2) NOT NULL

-- Enums for fixed sets
status ENUM('pending', 'active', 'suspended') NOT NULL

-- Timestamps — store UTC, convert at app layer
TIMESTAMP            -- 4 bytes, auto UTC conversion
DATETIME             -- 8 bytes, no timezone handling
```

**Less data = more performance.** Smaller types mean more rows per InnoDB page (16KB), better buffer pool utilization, faster I/O.

### Normalization (3NF Default)

```sql
-- 1NF: Atomic values (no CSV in columns)
-- 2NF: Depend on entire key (not partial)
-- 3NF: Depend only on PK (no transitive dependencies)

-- Strategic denormalization ONLY for proven performance needs
-- Keep denormalized data in sync via triggers
```

### Foreign Keys

```sql
FOREIGN KEY fk_tenant (tenant_id) REFERENCES tenants(id)
  ON DELETE RESTRICT ON UPDATE CASCADE
```

**Strategies:** `RESTRICT` (prevent orphans), `CASCADE` (delete children), `SET NULL` (optional relationships).

---

## Indexing

**The #1 performance lever.** Every slow query starts here.

📖 **See `references/indexing-deep-dive.md` for B-tree internals, ICP, covering indexes**

### Leftmost Prefix Rule (CRITICAL)

MySQL can only use an index starting from the leftmost column:

```sql
-- Index: KEY idx_abc (a, b, c)
-- ✓ Uses index: WHERE a = ?
-- ✓ Uses index: WHERE a = ? AND b = ?
-- ✓ Uses index: WHERE a = ? AND b = ? AND c = ?
-- ✗ Cannot use: WHERE b = ?        (skips leftmost)
-- ✗ Cannot use: WHERE b = ? AND c = ?  (skips leftmost)
```

### ESR Rule (Equality, Sort, Range)

Order composite index columns: equality first, sort next, range last.

```sql
-- Query: WHERE tenant_id = ? AND status = ? ORDER BY created_at DESC WHERE amount > ?
KEY idx_esr (tenant_id, status, created_at DESC, amount)
--           ^equality   ^equality  ^sort              ^range (last!)
```

Range conditions (`<`, `>`, `BETWEEN`, `LIKE 'prefix%'`) stop further index column use.

### Index Types

```sql
-- Primary key (clustered — table data stored IN this index)
id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY

-- Unique (uniqueness enforcement + fast lookup)
UNIQUE KEY uk_email (tenant_id, email)

-- Regular (WHERE, JOIN, ORDER BY)
KEY idx_tenant_status (tenant_id, status)

-- Fulltext (text search)
FULLTEXT INDEX ft_search (title, content)

-- Descending (MySQL 8.0+ — for ORDER BY col DESC)
KEY idx_created_desc (tenant_id, created_at DESC)
```

### EXPLAIN — Always Verify

```sql
EXPLAIN FORMAT=JSON SELECT * FROM orders WHERE tenant_id = 1 AND status = 'active';

-- EXPLAIN ANALYZE (MySQL 8.0.18+) — measures actual execution time
EXPLAIN ANALYZE SELECT * FROM orders WHERE tenant_id = 1 ORDER BY created_at DESC LIMIT 25;
```

**Access types (best to worst):**

| type | Meaning | Action |
|------|---------|--------|
| `const` | Unique index, 1 row | Ideal |
| `eq_ref` | Unique index in JOIN | Ideal |
| `ref` | Non-unique index | Good |
| `range` | Index range scan | Good |
| `index` | Full index scan | Review |
| `ALL` | **Full TABLE scan** | **FIX IMMEDIATELY** |

**Red flags:** `type: ALL` with `key: NULL` = no usable index. `select_full_join > 0` = unindexed join. Stop and fix.

### Index Anti-Patterns

```sql
-- ✗ Redundant indexes (KEY(a) is redundant if KEY(a,b) exists)
-- ✗ Low-cardinality solo indexes (KEY(is_deleted) — only 2 values)
-- ✗ Over-indexing (each index = write amplification)
-- ✗ Missing join indexes (every JOIN column needs an index)

-- Monitor unused indexes
SELECT object_name, index_name FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE count_read = 0 AND index_name != 'PRIMARY' AND object_schema = 'your_db';
```

---

## Query Performance

**Performance = query response time.** The only metric users experience.

📖 **See `references/query-performance.md` for profiling workflow, 9 essential metrics, query load**

### Optimization Workflow

1. **Profile** — Enable slow query log or use Performance Schema to find slowest queries
2. **EXPLAIN** — Analyze execution plan; look for `type: ALL`, missing indexes
3. **Index** — Create/modify indexes following ESR rule
4. **Verify** — Re-EXPLAIN, confirm improvement
5. **Monitor** — Track response time continuously

### Query Rules

```sql
-- ✓ DO: Select only needed columns
SELECT id, name, total FROM orders WHERE tenant_id = ? LIMIT 25;

-- ✗ DON'T: SELECT * (wastes I/O, prevents covering indexes)
SELECT * FROM orders;

-- ✓ DO: Parameterized queries (security + plan reuse)
PREPARE stmt FROM 'SELECT * FROM users WHERE tenant_id = ? AND id = ?';
EXECUTE stmt USING @tenant_id, @user_id;

-- ✓ DO: Keyset pagination (fast at any offset)
SELECT id, name FROM items WHERE tenant_id = ? AND id < ? ORDER BY id DESC LIMIT 25;

-- ✗ DON'T: Large OFFSET (scans and discards rows)
SELECT * FROM items LIMIT 25 OFFSET 100000;

-- ✓ DO: JOINs with indexed columns
SELECT o.id, c.name FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.tenant_id = ?;

-- ✗ DON'T: Subqueries where JOINs work
SELECT * FROM orders WHERE customer_id IN (SELECT id FROM customers WHERE name LIKE '%smith%');
```

### Slow Query Log

```ini
# my.cnf
slow_query_log = 1
long_query_time = 1              # Log queries > 1 second
log_queries_not_using_indexes = 1 # Also log queries without indexes
log_slow_extra = ON              # MySQL 8.0.14+ — extra metrics
```

---

## Security

**Never use root for application connections.** Principle of least privilege.

📖 **See `references/security-hardening.md` for TDE, SSL/TLS, audit, firewall, RBAC**

### Application User

```sql
-- Create dedicated application user with minimal privileges
CREATE USER 'saas_app'@'%' IDENTIFIED BY 'strong_random_password_here';
GRANT SELECT, INSERT, UPDATE, DELETE ON saas_platform.* TO 'saas_app'@'%';
-- Never grant: FILE, PROCESS, SHUTDOWN, SUPER, CREATE USER, GRANT OPTION

-- Read-only user for reporting/replicas
CREATE USER 'saas_readonly'@'%' IDENTIFIED BY 'another_strong_password';
GRANT SELECT ON saas_platform.* TO 'saas_readonly'@'%';
```

### Encryption

```ini
# my.cnf — TDE (Transparent Data Encryption)
early-plugin-load=keyring_file.so
default-table-encryption = ON

# SSL/TLS (encrypt in transit)
require_secure_transport = ON
ssl_ca=/path/to/ca-cert.pem
ssl_cert=/path/to/server-cert.pem
ssl_key=/path/to/server-key.pem
```

```sql
-- Application-level encryption for sensitive columns
phone_encrypted VARBINARY(255)  -- AES-256 at app layer via PHP openssl_encrypt()
```

### Multi-Tenant Isolation (CRITICAL)

```sql
-- EVERY query MUST include tenant filter
SELECT * FROM orders WHERE tenant_id = ? AND id = ?;

-- Never allow cross-tenant access
-- Always verify tenant_id at application layer before query
-- Use UUIDs for public-facing IDs (prevent enumeration)

-- Stored procedures must enforce tenant_id
CREATE PROCEDURE sp_get_order(IN p_tenant_id INT, IN p_order_id BIGINT)
BEGIN
  SELECT * FROM orders WHERE tenant_id = p_tenant_id AND id = p_order_id;
END;
```

### SQL Injection Prevention

```sql
-- ✓ CORRECT: Parameterized queries
PREPARE stmt FROM 'SELECT * FROM users WHERE email = ? AND tenant_id = ?';
EXECUTE stmt USING @email, @tenant_id;

-- ✗ WRONG: String concatenation (VULNERABLE!)
SET @q = CONCAT('SELECT * FROM users WHERE email = "', @email, '"');
```

---

## Transactions & Locking

📖 **See `references/transaction-locking.md` for MVCC, gap locks, deadlock patterns**

### Isolation Levels

| Level | Gap Locks | Phantom Rows | Use Case |
|-------|-----------|-------------|----------|
| READ COMMITTED | No | Yes | **Recommended for most SaaS apps** — reduces locking contention |
| REPEATABLE READ | Yes | No (InnoDB) | Default — more locking, stronger consistency |

```sql
-- Set per-session (recommended for SaaS)
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### Deadlock Prevention

```sql
-- ✓ DO: Lock rows in consistent order
START TRANSACTION;
SELECT * FROM accounts WHERE id = LEAST(100, 200) FOR UPDATE;
SELECT * FROM accounts WHERE id = GREATEST(100, 200) FOR UPDATE;
-- ... update both ...
COMMIT;

-- ✓ DO: Keep transactions short
-- ✓ DO: Use IN() instead of BETWEEN (fewer gap locks)
-- ✗ DON'T: Long-running transactions (block purging, grow undo log)
-- ✗ DON'T: BEGIN without COMMIT/ROLLBACK (stalled transactions)
```

### Transaction Best Practices

```sql
-- Always use explicit transactions for multi-statement operations
START TRANSACTION;
  INSERT INTO orders (...) VALUES (...);
  INSERT INTO order_items (...) VALUES (...);
  UPDATE inventory SET quantity = quantity - ? WHERE id = ? AND quantity >= ?;
  -- Check affected rows — if 0, ROLLBACK (insufficient inventory)
COMMIT;
```

---

## Advanced SQL

📖 **See `references/advanced-sql-patterns.md` for full patterns, recursive CTEs, pivots**

### Key Patterns

```sql
-- CTE with window function
WITH monthly AS (
  SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, SUM(total) AS revenue
  FROM orders WHERE tenant_id = ? GROUP BY month
)
SELECT month, revenue, revenue - LAG(revenue) OVER (ORDER BY month) AS change
FROM monthly;

-- Ranking
SELECT id, name, RANK() OVER (PARTITION BY category ORDER BY total DESC) AS rank
FROM products WHERE tenant_id = ?;

-- ROLLUP subtotals
SELECT COALESCE(category, 'TOTAL') AS category, SUM(amount)
FROM sales WHERE tenant_id = ? GROUP BY category WITH ROLLUP;

-- Recursive CTE (hierarchy)
WITH RECURSIVE tree AS (
  SELECT id, name, 1 AS depth FROM employees WHERE supervisor_id IS NULL AND tenant_id = ?
  UNION ALL
  SELECT e.id, e.name, t.depth + 1 FROM employees e JOIN tree t ON e.supervisor_id = t.id
)
SELECT * FROM tree ORDER BY depth, name;
```

---

## Server Tuning

📖 **See `references/server-tuning-mycnf.md` for 70+ metrics, complete my.cnf template**

### Critical Variables

| Variable | Default | Recommendation |
|----------|---------|----------------|
| `innodb_buffer_pool_size` | 128MB | **70-80% of server RAM** (most important variable) |
| `innodb_buffer_pool_instances` | 8 | 8-24 for high concurrency |
| `innodb_redo_log_capacity` | 100MB | 1-4GB for write-heavy workloads (8.0.30+) |
| `innodb_log_buffer_size` | 16MB | 48MB for heavy transactions |
| `innodb_flush_log_at_trx_commit` | 1 | **Keep at 1** (ACID durability) |
| `max_connections` | 151 | 500+ for production |
| `innodb_dedicated_server` | OFF | ON for dedicated MySQL servers (8.0.14+) |

**Do NOT randomly tune variables.** The buffer pool is the overwhelmingly most impactful setting. Optimize queries and indexes first.

### Monitoring

```sql
-- Buffer pool hit rate (should be > 99%)
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
-- Hit rate = read_requests / (read_requests + reads) * 100

-- Active threads (should be low single digits normally)
SHOW GLOBAL STATUS LIKE 'Threads_running';

-- Row lock contention (should be near zero)
SHOW GLOBAL STATUS LIKE 'Innodb_row_lock%';

-- Table maintenance
ANALYZE TABLE customers, orders;  -- Update index statistics
OPTIMIZE TABLE large_table;       -- Reclaim space (locks table — off-peak only)
```

---

## Operations

📖 **See `references/backup-recovery.md`** (mysqldump, XtraBackup, point-in-time recovery) | **`references/high-availability.md`** (GTID replication, InnoDB Cluster, failover)

```bash
# Essential backup command
mysqldump --single-transaction --routines --triggers --all-databases > backup.sql
```

### Migrations

```bash
# Pre-migration checklist: 1) grep references, 2) check stored procs, 3) backup
grep -r "table_name" --include="*.php" --include="*.sql" .
mysqldump --single-transaction database_name > backup_pre_migration.sql
```

```sql
ALTER TABLE orders ADD COLUMN tracking VARCHAR(50) DEFAULT NULL;  -- Non-breaking
```

---

## Checklist

**Schema:** ✅ UTF8MB4 + InnoDB + ROW_FORMAT=DYNAMIC ✅ Smallest sufficient data types ✅ DECIMAL for money ✅ 3NF normalized ✅ Foreign keys with RESTRICT/CASCADE

**Indexing:** ✅ ESR composite indexes ✅ Leftmost prefix satisfied ✅ No redundant indexes ✅ Join columns indexed ✅ EXPLAIN verified on critical queries ✅ No `type: ALL` in EXPLAIN

**Performance:** ✅ No SELECT * ✅ Keyset pagination for large offsets ✅ Covering indexes for hot queries ✅ Slow query log enabled ✅ Buffer pool sized to 70-80% RAM ✅ ANALYZE TABLE regular

**Security:** ✅ Application user (not root) ✅ Minimal privileges ✅ Parameterized queries only ✅ TDE + SSL encryption ✅ tenant_id in EVERY query ✅ UUIDs for public IDs

**Transactions:** ✅ READ COMMITTED isolation for SaaS ✅ Consistent lock ordering ✅ Short transactions ✅ IN() over BETWEEN for less locking ✅ No stalled transactions

**Operations:** ✅ Binary logging enabled ✅ Regular backups tested ✅ Monitoring active ✅ Migration checklist followed

---

**Sources:** Efficient MySQL Performance (Nichter 2022), Mastering MySQL Administration (Kumar et al. 2024), Leveling Up with SQL (Simon 2023)
**Last Updated:** 2026-03-04
**Maintained by:** Peter Bamuhigire
