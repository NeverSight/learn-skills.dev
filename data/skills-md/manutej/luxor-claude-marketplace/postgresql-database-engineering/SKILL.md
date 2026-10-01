---
name: postgresql-database-engineering
description: Comprehensive PostgreSQL database engineering skill covering indexing strategies, query optimization, performance tuning, partitioning, replication, backup and recovery, high availability, and production database management. Master advanced PostgreSQL features including MVCC, VACUUM operations, connection pooling, monitoring, and scalability patterns.
---

# PostgreSQL Database Engineering

A comprehensive skill for professional PostgreSQL database engineering, covering everything from query optimization and indexing strategies to high availability, replication, and production database management. This skill enables you to design, optimize, and maintain high-performance PostgreSQL databases at scale.

## When to Use This Skill

Use this skill when:

- Designing database schemas for high-performance applications
- Optimizing slow queries and improving database performance
- Implementing indexing strategies for complex query patterns
- Setting up partitioning for large tables (100M+ rows)
- Configuring streaming replication and high availability
- Tuning PostgreSQL configuration for production workloads
- Implementing backup and recovery procedures
- Debugging performance issues and query bottlenecks
- Setting up connection pooling with pgBouncer or PgPool
- Monitoring database health and performance metrics
- Planning database migrations and schema changes
- Implementing database security and access controls
- Scaling PostgreSQL databases horizontally or vertically
- Managing VACUUM operations and database maintenance
- Setting up logical replication for data distribution

## Core Concepts

### PostgreSQL Architecture

PostgreSQL uses a process-based architecture with several key components:

- **Postmaster Process**: Main server process that manages connections
- **Backend Processes**: One per client connection, handles queries
- **Shared Memory**: Shared buffers, WAL buffers, lock tables
- **Background Workers**: Autovacuum, checkpointer, WAL writer, statistics collector
- **Write-Ahead Log (WAL)**: Transaction log for durability and replication
- **Storage Layer**: TOAST for large values, FSM for free space, VM for visibility

### MVCC (Multi-Version Concurrency Control)

PostgreSQL's foundational concurrency mechanism:

- **Snapshots**: Each transaction sees a consistent snapshot of data
- **Tuple Versions**: Multiple row versions coexist for concurrent access
- **Transaction IDs**: xmin (creating transaction), xmax (deleting transaction)
- **Visibility Rules**: Determines which row versions are visible to transactions
- **VACUUM**: Reclaims space from dead tuples and prevents transaction wraparound
- **FREEZE**: Marks old rows as visible to all transactions

**Key Implications:**
- No read locks - readers never block writers
- Writers never block readers
- Updates create new row versions
- Regular VACUUM is essential
- Dead tuples accumulate until vacuumed

### Transaction Isolation Levels

PostgreSQL supports four isolation levels:

1. **Read Uncommitted**: Treated as Read Committed in PostgreSQL
2. **Read Committed** (default): Sees committed data at statement start
3. **Repeatable Read**: Sees snapshot from transaction start
4. **Serializable**: True serializable isolation with SSI

**Choosing Isolation:**
- Read Committed: Most applications, best performance
- Repeatable Read: Reports, analytics needing consistency
- Serializable: Financial transactions, critical consistency needs

### Index Types

PostgreSQL offers multiple index types for different use cases:

#### 1. B-Tree (Default)
- **Use for**: Equality, range queries, sorting
- **Supports**: <, <=, =, >=, >, BETWEEN, IN, IS NULL
- **Best for**: Most general-purpose indexing
- **Example**: Primary keys, foreign keys, timestamps

#### 2. Hash
- **Use for**: Equality comparisons only
- **Supports**: = operator
- **Best for**: Large tables with equality lookups
- **Limitation**: Not WAL-logged before PG 10, no range queries

#### 3. GiST (Generalized Search Tree)
- **Use for**: Geometric data, full-text search, custom types
- **Supports**: Overlaps, contains, nearest neighbor
- **Best for**: Spatial data, ranges, full-text search
- **Example**: PostGIS geometries, tsvector, ranges

#### 4. GIN (Generalized Inverted Index)
- **Use for**: Multi-valued columns (arrays, JSONB, full-text)
- **Supports**: Contains, exists operators
- **Best for**: JSONB queries, array operations, full-text search
- **Tradeoff**: Slower updates, faster queries

#### 5. BRIN (Block Range Index)
- **Use for**: Very large tables with natural ordering
- **Supports**: Range queries on sorted data
- **Best for**: Time-series data, append-only tables
- **Advantage**: Tiny index size, scales to billions of rows

#### 6. SP-GiST (Space-Partitioned GiST)
- **Use for**: Non-balanced data structures
- **Supports**: Points, ranges, IP addresses
- **Best for**: Quadtrees, k-d trees, radix trees

### Query Planning and Optimization

PostgreSQL's query planner determines execution strategies:

**Planner Components:**
- **Statistics**: Table and column statistics for cardinality estimation
- **Cost Model**: CPU, I/O, and memory cost estimation
- **Plan Types**: Sequential scan, index scan, bitmap scan, joins
- **Join Methods**: Nested loop, hash join, merge join
- **Optimization**: Query rewriting, predicate pushdown, join reordering

**Key Statistics:**
- `n_distinct`: Number of distinct values (for selectivity)
- `correlation`: Physical row ordering correlation
- `most_common_vals`: MCV list for skewed distributions
- `histogram_bounds`: Value distribution histogram

**Understanding EXPLAIN:**
- **Cost**: Startup cost .. total cost (arbitrary units)
- **Rows**: Estimated row count
- **Width**: Average row size in bytes
- **Actual Time**: Real execution time (with ANALYZE)
- **Loops**: Number of times node executed

### Partitioning Strategies

Table partitioning for managing large datasets:

#### Range Partitioning
- **Use for**: Time-series data, sequential values
- **Example**: Partition by date ranges (daily, monthly, yearly)
- **Benefit**: Easy data lifecycle management, faster queries

#### List Partitioning
- **Use for**: Discrete categorical values
- **Example**: Partition by country, region, status
- **Benefit**: Logical data separation, partition pruning

#### Hash Partitioning
- **Use for**: Even data distribution
- **Example**: Partition by hash(user_id)
- **Benefit**: Balanced partition sizes, parallel queries

**Partition Pruning:**
- Planner eliminates irrelevant partitions
- Drastically reduces query scope
- Essential for partition performance

**Partition-Wise Operations:**
- Partition-wise joins: Join matching partitions directly
- Partition-wise aggregation: Aggregate within partitions
- Parallel partition processing

### Replication and High Availability

PostgreSQL replication options:

#### Streaming Replication (Physical)
- **Type**: Binary WAL streaming to standby servers
- **Modes**: Asynchronous, synchronous, quorum-based
- **Use for**: High availability, read scalability
- **Failover**: Automatic with tools like Patroni, repmgr

**Synchronous vs Asynchronous:**
- Synchronous: Zero data loss, higher latency
- Asynchronous: Low latency, potential data loss
- Quorum: Balance between safety and performance

#### Logical Replication
- **Type**: Row-level change stream
- **Use for**: Selective replication, upgrades, multi-master
- **Benefit**: Replicate specific tables, cross-version
- **Limitation**: No DDL replication, overhead

#### Cascading Replication
- Standbys replicate from other standbys
- Reduces load on primary
- Geographic distribution

### Connection Pooling

Managing database connections efficiently:

#### pgBouncer
- **Type**: Lightweight connection pooler
- **Modes**: Session, transaction, statement pooling
- **Use for**: High connection count applications
- **Benefit**: Reduced connection overhead, resource limits

**Pooling Modes:**
- **Session**: Client connects for entire session
- **Transaction**: Connection per transaction
- **Statement**: Connection per statement (rarely used)

#### PgPool-II
- **Type**: Feature-rich middleware
- **Features**: Connection pooling, load balancing, query caching
- **Use for**: Read/write splitting, connection management
- **Benefit**: Advanced routing, in-memory cache

### VACUUM and Maintenance

Critical maintenance operations:

#### VACUUM
- **Purpose**: Reclaim dead tuple space, update statistics
- **Types**: Regular VACUUM, VACUUM FULL
- **When**: After large updates/deletes, regularly via autovacuum
- **Impact**: Regular VACUUM is non-blocking

#### ANALYZE
- **Purpose**: Update planner statistics
- **When**: After data changes, schema modifications
- **Impact**: Minimal, fast on most tables

#### REINDEX
- **Purpose**: Rebuild indexes, fix bloat
- **When**: Index corruption, significant bloat
- **Impact**: Locks table, use REINDEX CONCURRENTLY (PG 12+)

#### Autovacuum
- **Purpose**: Automated VACUUM and ANALYZE
- **Configuration**: Threshold-based triggering
- **Tuning**: Balance resource usage vs. responsiveness
- **Monitoring**: Track autovacuum runs, prevent wraparound

### Performance Tuning

Key configuration parameters:

#### Memory Settings
```
shared_buffers: 25% of RAM (start point)
effective_cache_size: 50-75% of RAM
work_mem: Per-operation memory (sort, hash)
maintenance_work_mem: VACUUM, CREATE INDEX memory
```

#### Checkpoint and WAL
```
checkpoint_timeout: How often to checkpoint
max_wal_size: WAL size before checkpoint
checkpoint_completion_target: Spread checkpoint I/O
wal_buffers: WAL write buffer size
```

#### Query Planner
```
random_page_cost: Relative cost of random I/O
effective_io_concurrency: Concurrent I/O operations
default_statistics_target: Histogram detail level
```

#### Connection Settings
```
max_connections: Maximum client connections
connection_limit: Per-database/user limits
```

## Index Strategies

### Choosing the Right Index

**Decision Matrix:**

| Query Pattern | Index Type | Reason |
|--------------|------------|---------|
| `WHERE id = 5` | B-tree | Equality lookup |
| `WHERE created_at > '2024-01-01'` | B-tree | Range query |
| `ORDER BY name` | B-tree | Sorting support |
| `WHERE tags @> ARRAY['sql']` | GIN | Array containment |
| `WHERE data->>'status' = 'active'` | GIN (jsonb_path_ops) | JSONB query |
| `WHERE to_tsvector(content) @@ query` | GIN | Full-text search |
| `WHERE location <-> point(0,0)` | GiST | Nearest neighbor |
| `WHERE timestamp BETWEEN ... (large table)` | BRIN | Sequential time-series |
| `WHERE ip_address << '192.168.0.0/16'` | GiST or SP-GiST | IP range query |

### Composite Indexes

Multi-column indexes for complex queries:

**Column Ordering Rules:**
1. Equality columns first
2. Sort/range columns last
3. High-selectivity columns first
4. Match query patterns exactly

**Example:**
```sql
-- Query: WHERE status = 'active' AND created_at > '2024-01-01' ORDER BY created_at
-- Optimal index: (status, created_at)
CREATE INDEX idx_users_status_created ON users(status, created_at);
```

### Partial Indexes

Index subset of rows:

**Benefits:**
- Smaller index size
- Faster updates on non-indexed rows
- Targeted query optimization

**Use Cases:**
- Index only active records: `WHERE deleted_at IS NULL`
- Index recent data: `WHERE created_at > NOW() - INTERVAL '90 days'`
- Index specific states: `WHERE status IN ('pending', 'processing')`

### Expression Indexes

Index computed values:

**Examples:**
```sql
-- Case-insensitive search
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Date truncation
CREATE INDEX idx_events_date ON events(DATE(created_at));

-- JSONB field
CREATE INDEX idx_data_status ON documents((data->>'status'));
```

### Covering Indexes (INCLUDE)

Include non-key columns for index-only scans:

```sql
CREATE INDEX idx_users_email_include
ON users(email)
INCLUDE (first_name, last_name, created_at);
```

**Benefit:** Query satisfied entirely from index, no table lookup

### Index Maintenance

**Monitoring Index Usage:**
```sql
-- Unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Detecting Bloat:**
```sql
-- Index bloat estimation
SELECT schemaname, tablename, indexname,
       pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
       idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Query Optimization

### Using EXPLAIN ANALYZE

Understanding query execution:

```sql
-- Basic EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- EXPLAIN ANALYZE (actually runs query)
EXPLAIN ANALYZE SELECT * FROM users WHERE created_at > '2024-01-01';

-- Detailed output
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.*, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';
```

**Key Metrics:**
- **Planning Time**: Time to generate plan
- **Execution Time**: Actual query runtime
- **Shared Hit vs Read**: Buffer cache hits vs disk reads
- **Rows**: Estimated vs actual row counts
- **Filter vs Index Cond**: Post-scan filtering vs index usage

### Common Query Anti-Patterns

#### 1. N+1 Queries
**Problem:** One query per row in a loop
**Solution:** JOIN or batch queries

#### 2. SELECT *
**Problem:** Fetches unnecessary columns
**Solution:** Select only needed columns

#### 3. Implicit Type Conversions
**Problem:** Index not used due to type mismatch
**Solution:** Ensure query types match column types

#### 4. Function on Indexed Column
**Problem:** `WHERE UPPER(email) = 'USER@EXAMPLE.COM'`
**Solution:** Use expression index or compare correctly

#### 5. OR Conditions
**Problem:** `WHERE status = 'A' OR status = 'B'`
**Solution:** Use `IN`: `WHERE status IN ('A', 'B')`

### Join Optimization

**Join Types:**

1. **Nested Loop**
   - Best for: Small outer table, indexed inner table
   - How: For each outer row, scan inner table
   - When: Small result sets, good indexes

2. **Hash Join**
   - Best for: Large tables, no good indexes
   - How: Build hash table of smaller table
   - When: Equality joins, sufficient memory

3. **Merge Join**
   - Best for: Pre-sorted data, equality joins
   - How: Sort both inputs, merge scan
   - When: Both inputs sorted or can be sorted cheaply

**Join Order Matters:**
- Planner reorders joins for optimization
- Statistics guide join order decisions
- Can force order with `SET join_collapse_limit`

### Aggregation Optimization

**Techniques:**
- **Partial Aggregates**: Partition-wise aggregation
- **Hash Aggregates**: In-memory grouping
- **Sorted Aggregates**: Pre-sorted input
- **Parallel Aggregation**: Multiple workers

**Materialized Views:**
- Pre-compute expensive aggregations
- Refresh on schedule or trigger
- Trade freshness for query speed

### Query Caching

**Levels:**
1. **Shared Buffers**: PostgreSQL page cache
2. **OS Page Cache**: Operating system cache
3. **Application Cache**: Redis, Memcached
4. **Prepared Statements**: Reuse query plans

## Partitioning

### Implementing Range Partitioning

**Time-series example:**

```sql
-- Create partitioned table
CREATE TABLE events (
    id BIGSERIAL,
    event_type TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    data JSONB,
    created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_01 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE events_2024_02 PARTITION OF events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Default partition for data outside ranges
CREATE TABLE events_default PARTITION OF events DEFAULT;

-- Indexes on partitions
CREATE INDEX idx_events_2024_01_user ON events_2024_01(user_id);
CREATE INDEX idx_events_2024_02_user ON events_2024_02(user_id);
```

### Partition Automation

**Automated partition management:**

```sql
-- Function to create monthly partitions
CREATE OR REPLACE FUNCTION create_monthly_partition(
    base_table TEXT,
    partition_date DATE
) RETURNS VOID AS $$
DECLARE
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    partition_name := base_table || '_' || TO_CHAR(partition_date, 'YYYY_MM');
    start_date := DATE_TRUNC('month', partition_date);
    end_date := start_date + INTERVAL '1 month';

    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF %I
         FOR VALUES FROM (%L) TO (%L)',
        partition_name, base_table, start_date, end_date
    );

    -- Create indexes
    EXECUTE format(
        'CREATE INDEX IF NOT EXISTS %I ON %I(user_id)',
        'idx_' || partition_name || '_user', partition_name
    );
END;
$$ LANGUAGE plpgsql;
```

### Partition Maintenance

**Dropping old partitions:**

```sql
-- Detach partition (fast, non-blocking)
ALTER TABLE events DETACH PARTITION events_2023_01;

-- Drop detached partition
DROP TABLE events_2023_01;

-- Or archive before dropping
CREATE TABLE archive.events_2023_01 AS SELECT * FROM events_2023_01;
DROP TABLE events_2023_01;
```

## High Availability and Replication

### Setting Up Streaming Replication

**Primary server configuration (postgresql.conf):**

```conf
# Replication settings
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
synchronous_commit = on  # or off for async
synchronous_standby_names = 'standby1,standby2'  # for sync replication
```

**Create replication user:**

```sql
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'secure_password';
```

**pg_hba.conf on primary:**

```conf
# Allow replication connections
host replication replicator standby_ip/32 md5
```

**Standby server setup:**

```bash
# Stop standby PostgreSQL
systemctl stop postgresql

# Remove old data directory
rm -rf /var/lib/postgresql/14/main

# Base backup from primary
pg_basebackup -h primary_host -D /var/lib/postgresql/14/main \
              -U replicator -P -v -R -X stream -C -S standby1

# Start standby
systemctl start postgresql
```

**Standby configuration (created by -R flag):**

```conf
# standby.signal file created automatically
# postgresql.auto.conf contains:
primary_conninfo = 'host=primary_host port=5432 user=replicator password=secure_password'
primary_slot_name = 'standby1'
```

### Monitoring Replication

**On primary:**

```sql
-- Check replication status
SELECT client_addr, state, sync_state, replay_lag
FROM pg_stat_replication;

-- Check replication slots
SELECT slot_name, active, restart_lsn, confirmed_flush_lsn
FROM pg_replication_slots;
```

**On standby:**

```sql
-- Check replication lag
SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;

-- Check recovery status
SELECT pg_is_in_recovery();
```

### Failover and Switchover

**Promoting standby to primary:**

```bash
# Trigger failover
pg_ctl promote -D /var/lib/postgresql/14/main

# Or using SQL
SELECT pg_promote();
```

**Controlled switchover:**

```bash
# 1. Stop writes on primary
# 2. Wait for standby to catch up
# 3. Promote standby
# 4. Reconfigure old primary as new standby
```

### Logical Replication Setup

**On publisher (source):**

```sql
-- Create publication
CREATE PUBLICATION my_publication FOR TABLE users, orders;

-- Or all tables
CREATE PUBLICATION all_tables FOR ALL TABLES;
```

**On subscriber (destination):**

```sql
-- Create subscription
CREATE SUBSCRIPTION my_subscription
    CONNECTION 'host=publisher_host dbname=mydb user=replicator password=pass'
    PUBLICATION my_publication;

-- Monitor subscription
SELECT * FROM pg_stat_subscription;
```

## Backup and Recovery

### Physical Backups

**pg_basebackup:**

```bash
# Full physical backup
pg_basebackup -h localhost -U postgres -D /backup/base \
              -F tar -z -P -v

# With WAL files for point-in-time recovery
pg_basebackup -h localhost -U postgres -D /backup/base \
              -X stream -F tar -z -P
```

**Continuous archiving (WAL archiving):**

```conf
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /archive/wal/%f'
```

### Logical Backups

**pg_dump:**

```bash
# Single database
pg_dump -h localhost -U postgres -F c -b -v -f mydb.dump mydb

# All databases
pg_dumpall -h localhost -U postgres -f all_databases.sql

# Specific tables
pg_dump -h localhost -U postgres -t users -t orders -F c -f tables.dump mydb

# Schema only
pg_dump -h localhost -U postgres --schema-only -F c -f schema.dump mydb
```

**pg_restore:**

```bash
# Restore database
pg_restore -h localhost -U postgres -d mydb -v mydb.dump

# Parallel restore
pg_restore -h localhost -U postgres -d mydb -j 4 -v mydb.dump

# Restore specific tables
pg_restore -h localhost -U postgres -d mydb -t users -v mydb.dump
```

### Point-in-Time Recovery (PITR)

**Setup:**

1. Take base backup
2. Configure WAL archiving
3. Store WAL files safely

**Recovery:**

```bash
# 1. Restore base backup
tar -xzf base.tar.gz -C /var/lib/postgresql/14/main

# 2. Create recovery.signal file
touch /var/lib/postgresql/14/main/recovery.signal

# 3. Configure recovery target (postgresql.conf or postgresql.auto.conf)
restore_command = 'cp /archive/wal/%f %p'
recovery_target_time = '2024-01-15 14:30:00'
# Or: recovery_target_name = 'before_disaster'
# Or: recovery_target_lsn = '0/3000000'

# 4. Start PostgreSQL
systemctl start postgresql
```

### Backup Strategies

**3-2-1 Rule:**
- 3 copies of data
- 2 different media types
- 1 offsite backup

**Backup Schedule:**
- **Daily**: Incremental WAL archiving
- **Weekly**: Full pg_basebackup
- **Monthly**: Long-term retention

**Testing Backups:**
- Regularly restore to test environment
- Verify data integrity
- Measure restore time

## Performance Monitoring

### Key Metrics to Monitor

**Database Health:**
- Active connections
- Transaction rate
- Cache hit ratio
- Deadlocks
- Checkpoint frequency
- Autovacuum runs

**Query Performance:**
- Slow query log
- Query execution time
- Lock waits
- Sequential scans

**System Resources:**
- CPU utilization
- Memory usage
- Disk I/O
- Network bandwidth

### Essential Monitoring Queries

**Connection stats:**

```sql
SELECT count(*) as total_connections,
       count(*) FILTER (WHERE state = 'active') as active,
       count(*) FILTER (WHERE state = 'idle') as idle,
       count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction
FROM pg_stat_activity;
```

**Cache hit ratio:**

```sql
SELECT sum(heap_blks_read) as heap_read,
       sum(heap_blks_hit) as heap_hit,
       sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS ratio
FROM pg_statio_user_tables;
```

**Table bloat:**

```sql
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
       n_dead_tup,
       n_live_tup,
       round(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

**Long-running queries:**

```sql
SELECT pid, now() - query_start AS duration, state, query
FROM pg_stat_activity
WHERE state != 'idle'
  AND query NOT LIKE '%pg_stat_activity%'
ORDER BY duration DESC;
```

**Lock monitoring:**

```sql
SELECT blocked_locks.pid AS blocked_pid,
       blocked_activity.usename AS blocked_user,
       blocking_locks.pid AS blocking_pid,
       blocking_activity.usename AS blocking_user,
       blocked_activity.query AS blocked_statement,
       blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted
  AND blocking_locks.granted;
```

### pg_stat_statements

**Installation:**

```sql
CREATE EXTENSION pg_stat_statements;
```

**Configuration (postgresql.conf):**

```conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
pg_stat_statements.max = 10000
```

**Top queries by total time:**

```sql
SELECT query,
       calls,
       total_exec_time,
       mean_exec_time,
       max_exec_time,
       rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

**Top queries by average time:**

```sql
SELECT query,
       calls,
       mean_exec_time,
       total_exec_time
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_exec_time DESC
LIMIT 20;
```

## Best Practices

### Schema Design

**Normalization:**
- Normalize to 3NF for transactional systems
- Denormalize selectively for read-heavy workloads
- Use foreign keys for data integrity
- Consider partitioning for very large tables

**Data Types:**
- Use smallest appropriate data type
- BIGINT for large IDs, INTEGER for smaller ranges
- NUMERIC for exact decimal values
- TIMESTAMP WITH TIME ZONE for timestamps
- TEXT over VARCHAR unless length constraint needed
- UUID for distributed ID generation
- JSONB for semi-structured data

**Constraints:**
- Primary keys on all tables
- Foreign keys for referential integrity
- CHECK constraints for business rules
- NOT NULL where appropriate
- UNIQUE constraints for uniqueness
- Use constraint names for maintainability

### Migration Strategies

**Zero-Downtime Migrations:**

1. **Add new column**
   ```sql
   ALTER TABLE users ADD COLUMN email_verified BOOLEAN;
   ```

2. **Backfill data** (in batches)
   ```sql
   UPDATE users SET email_verified = false
   WHERE email_verified IS NULL
   LIMIT 10000;
   ```

3. **Add NOT NULL constraint**
   ```sql
   ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;
   ```

**Index Creation:**
- Use `CREATE INDEX CONCURRENTLY` in production
- No table locks, allows reads/writes
- Takes longer but doesn't block
- Monitor progress with `pg_stat_progress_create_index`

**Large Table Modifications:**
- Use `pg_repack` for table rewrites
- Partition large tables before modifications
- Schedule during maintenance windows
- Test on production-like datasets

### Security Best Practices

**Authentication:**
- Use strong passwords or certificate authentication
- SCRAM-SHA-256 for password encryption
- Separate users for different applications
- Avoid superuser for application connections

**Authorization:**
- Grant minimal required privileges
- Use role-based access control
- Revoke PUBLIC access
- Row-level security for multi-tenant

**Network Security:**
- Configure pg_hba.conf restrictively
- Use SSL/TLS for connections
- Firewall database ports
- VPN or private networks for replication

**Audit Logging:**
- Enable connection logging
- Log DDL statements
- Use pgAudit extension for detailed auditing
- Monitor for suspicious activity

### Maintenance Schedule

**Daily:**
- Monitor slow queries
- Check replication lag
- Review autovacuum activity
- Monitor disk space

**Weekly:**
- Analyze top queries
- Review index usage
- Check for bloat
- Backup verification

**Monthly:**
- Full VACUUM on critical tables
- REINDEX bloated indexes
- Review configuration parameters
- Capacity planning

**Quarterly:**
- Review and optimize indexes
- Schema optimization opportunities
- Upgrade planning
- Performance baseline updates

## Advanced Topics

### Parallel Query Execution

**Configuration:**

```conf
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
parallel_setup_cost = 1000
parallel_tuple_cost = 0.1
min_parallel_table_scan_size = 8MB
```

**Forcing parallel execution:**

```sql
SET max_parallel_workers_per_gather = 4;
EXPLAIN ANALYZE SELECT COUNT(*) FROM large_table;
```

**When parallelism helps:**
- Large sequential scans
- Large aggregations
- Hash joins on large tables
- Bitmap heap scans

### Custom Functions and Procedures

**Stored procedures:**

```sql
CREATE OR REPLACE PROCEDURE update_user_statistics()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users SET
        order_count = (SELECT COUNT(*) FROM orders WHERE user_id = users.id),
        last_order_date = (SELECT MAX(created_at) FROM orders WHERE user_id = users.id);

    COMMIT;
END;
$$;
```

**Functions with proper error handling:**

```sql
CREATE OR REPLACE FUNCTION create_user(
    p_email TEXT,
    p_name TEXT
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    INSERT INTO users (email, name)
    VALUES (p_email, p_name)
    RETURNING id INTO v_user_id;

    RETURN v_user_id;
EXCEPTION
    WHEN unique_violation THEN
        RAISE EXCEPTION 'Email already exists: %', p_email;
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error creating user: %', SQLERRM;
END;
$$;
```

### Foreign Data Wrappers

**Access external data sources:**

```sql
-- Install postgres_fdw
CREATE EXTENSION postgres_fdw;

-- Create server
CREATE SERVER remote_db
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'remote_host', dbname 'remote_database', port '5432');

-- Create user mapping
CREATE USER MAPPING FOR current_user
SERVER remote_db
OPTIONS (user 'remote_user', password 'remote_password');

-- Import foreign schema
IMPORT FOREIGN SCHEMA public
FROM SERVER remote_db
INTO local_schema;

-- Query foreign table
SELECT * FROM local_schema.remote_table;
```

### JSON and JSONB Operations

**Indexing JSONB:**

```sql
-- GIN index for containment queries
CREATE INDEX idx_data_gin ON documents USING GIN (data);

-- Expression index for specific field
CREATE INDEX idx_data_status ON documents ((data->>'status'));

-- GIN index with jsonb_path_ops (smaller, faster for @> queries)
CREATE INDEX idx_data_path_ops ON documents USING GIN (data jsonb_path_ops);
```

**Efficient JSONB queries:**

```sql
-- Containment query (uses GIN index)
SELECT * FROM documents WHERE data @> '{"status": "active"}';

-- Existence query
SELECT * FROM documents WHERE data ? 'email';

-- Path query
SELECT * FROM documents WHERE data->'user'->>'email' = 'user@example.com';

-- Array operations
SELECT * FROM documents WHERE data->'tags' @> '["sql", "postgres"]';
```

### Full-Text Search

**Basic setup:**

```sql
-- Add tsvector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Generate search vector
UPDATE articles SET search_vector =
    to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''));

-- Create GIN index
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Trigger for automatic updates
CREATE TRIGGER articles_search_update
BEFORE INSERT OR UPDATE ON articles
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', title, content);
```

**Search queries:**

```sql
-- Basic search
SELECT title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql & database') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Phrase search
SELECT title FROM articles
WHERE search_vector @@ phraseto_tsquery('english', 'database engineering');

-- Search with highlighting
SELECT title,
       ts_headline('english', content, query) AS snippet
FROM articles, to_tsquery('english', 'postgresql') query
WHERE search_vector @@ query;
```

## Troubleshooting

### Common Issues

**Problem: Slow Queries**
- Check EXPLAIN ANALYZE output
- Verify indexes exist and are used
- Update table statistics: `ANALYZE table_name`
- Check for missing indexes on foreign keys
- Look for function calls on indexed columns

**Problem: High CPU Usage**
- Identify expensive queries with pg_stat_statements
- Check for missing indexes causing sequential scans
- Review parallel query settings
- Look for inefficient joins or aggregations

**Problem: Connection Exhaustion**
- Increase max_connections (requires restart)
- Implement connection pooling (pgBouncer)
- Identify connection leaks in application
- Monitor with `pg_stat_activity`

**Problem: Autovacuum Not Keeping Up**
- Increase autovacuum_max_workers
- Adjust autovacuum thresholds
- Reduce autovacuum_naptime
- Increase autovacuum_work_mem
- Check for long-running transactions blocking VACUUM

**Problem: Replication Lag**
- Check network bandwidth between primary and standby
- Verify standby hardware resources
- Check for long-running queries on standby
- Monitor WAL generation rate
- Consider increasing wal_sender_timeout

**Problem: Transaction ID Wraparound**
- Monitor age of oldest transaction
- Run VACUUM FREEZE on old tables
- Check autovacuum_freeze_max_age
- Increase autovacuum aggressiveness
- Run manual VACUUM FREEZE if necessary

### Diagnostic Queries

**Find missing indexes on foreign keys:**

```sql
SELECT c.conrelid::regclass AS table,
       c.confrelid::regclass AS referenced_table,
       string_agg(a.attname, ', ') AS foreign_key_columns
FROM pg_constraint c
JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid
      AND c.conkey[1:array_length(c.conkey, 1)]
          OPERATOR(pg_catalog.@>) i.indkey[0:array_length(c.conkey, 1) - 1]
  )
GROUP BY c.conrelid, c.confrelid, c.conname;
```

**Identify blocking queries:**

```sql
SELECT activity.pid,
       activity.usename,
       activity.query,
       blocking.pid AS blocking_id,
       blocking.query AS blocking_query
FROM pg_stat_activity AS activity
JOIN pg_stat_activity AS blocking ON blocking.pid = ANY(pg_blocking_pids(activity.pid));
```

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Database Engineering, Performance Optimization, Data Architecture
**Compatible With**: PostgreSQL 12+, 13, 14, 15, 16
**Prerequisites**: SQL knowledge, basic database concepts, Linux command line
