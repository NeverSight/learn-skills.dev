---
name: starrocks-expert
description: Expert guidance for StarRocks database operations including table management, data loading, query optimization, materialized views, partitioning strategies, and cluster configuration. Use when working with StarRocks databases, OLAP queries, data warehousing, ETL pipelines, or when the user mentions StarRocks, distributed analytics, or columnar storage.
license: Apache-2.0
metadata:
    author: "Tiansu Yu"
    version: "1.0"
---

# StarRocks Expert

StarRocks is a next-generation sub-second MPP OLAP database for full analytics scenarios, including multi-dimensional analytics, real-time analytics, and ad-hoc queries.

## Quick Reference

### Common Operations

**Check table structure:**
```sql
SHOW CREATE TABLE database_name.table_name;
DESC database_name.table_name;
```

**View partitions:**
```sql
SHOW PARTITIONS FROM database_name.table_name;
```

**Check data loading status:**
```sql
SHOW LOAD WHERE label = 'your_load_label';
SHOW STREAM LOAD;
```

**Query execution analysis:**
```sql
EXPLAIN VERBOSE SELECT ...;
SHOW QUERY PROFILE '<query_id>';
```

### Key Concepts

**Table Types:**
- **Duplicate Key**: No unique constraint, best for raw data logging
- **Aggregate Key**: Pre-aggregates data during ingestion
- **Unique Key**: Enforces uniqueness, supports upserts
- **Primary Key**: Similar to Unique Key with better update performance

**Data Loading Methods:**
- **Stream Load**: HTTP-based, real-time loading
- **Broker Load**: Batch loading from external storage (S3, HDFS)
- **Routine Load**: Continuous loading from Kafka
- **INSERT INTO**: Direct SQL insertion

**Materialized Views:**
- **Asynchronous MV**: Scheduled refresh, complex transformations
- **Synchronous Rollup**: Auto-maintained aggregations

## When to Use This Skill

Use this skill when:
- Creating or modifying StarRocks table schemas
- Setting up data loading pipelines from S3, HDFS, or Kafka
- Optimizing slow queries or analyzing query plans
- Configuring partitioning and bucketing strategies
- Troubleshooting data loading failures
- Setting up materialized views or rollups
- Managing cluster resources and configurations

## Core Sections

### 1. Table Design

For detailed table design guidance, see [TABLE.md](references/TABLE.md):
- Table types (Duplicate, Aggregate, Unique, Primary Key)
- Partitioning strategies with `date_trunc()` expressions
- Bucketing and distribution
- Indexes (prefix, bloom filter, bitmap, ngram)

### 2. Infrastructure Configuration and Management

For detailed infrastructure guidance, see [INFRA.md](references/INFRA.md):
- Cluster setup and configuration (FE/BE/Broker)
- Resource management and resource groups
- Monitoring and maintenance
- Backup and recovery

### 3. Query and Task Skills

For detailed query optimization guidance, see [QUERY.md](references/QUERY.md):
- Data loading patterns (Stream Load, Broker Load, Routine Load)
- Query optimization techniques
- Materialized view design
- ETL pipeline patterns
- Performance troubleshooting
- Common anti-patterns

## Table Creation Pattern

```sql
CREATE TABLE IF NOT EXISTS database_name.table_name (
    event_time DATETIME NOT NULL COMMENT 'Event timestamp',
    id BIGINT NOT NULL COMMENT 'Business ID',
    amount DECIMAL(18, 2) COMMENT 'Transaction amount',
    status VARCHAR(50) COMMENT 'Status code',
    created_at DATETIME COMMENT 'Creation timestamp'
)
DUPLICATE KEY (event_time, id)
PARTITION BY date_trunc('day', event_time)  -- Expression-based partitioning
DISTRIBUTED BY HASH(id) BUCKETS 16
PROPERTIES (
    "replication_num" = "3",
    "storage_medium" = "SSD",
    "storage_cooldown_time" = "2024-12-31 23:59:59"
);
```

See [TABLE.md](references/TABLE.md) for detailed guidance on table types, partitioning strategies, and index selection.

## Data Loading Pattern

### Stream Load (HTTP-based)
```bash
curl --location-trusted -u user:password \
    -H "label:load_label_$(date +%s)" \
    -H "column_separator:," \
    -H "columns:date_col,id,amount,status,created_at" \
    -T data.csv \
    http://fe_host:8030/api/database_name/table_name/_stream_load
```

### Broker Load (S3)
```sql
LOAD LABEL database_name.load_label_20240101
(
    DATA INFILE("s3://bucket/path/data_*.parquet")
    INTO TABLE table_name
    FORMAT AS "parquet"
)
WITH BROKER
(
    "aws.s3.access_key" = "your_access_key",
    "aws.s3.secret_key" = "your_secret_key",
    "aws.s3.region" = "us-east-1"
)
PROPERTIES (
    "timeout" = "3600"
);
```

## Query Optimization Checklist

When optimizing queries:

- [ ] Check if partition pruning is working (verify in EXPLAIN)
- [ ] Ensure appropriate indexes exist (prefix bloom filter, bitmap)
- [ ] Verify JOIN order (small table on right for broadcast join)
- [ ] Check if materialized views can be used
- [ ] Analyze data distribution (avoid data skew)
- [ ] Review bucket count (optimal: 2-8 per BE core)
- [ ] Consider using colocate groups for frequent JOINs

## Partition Management

### Expression-based partitioning (Modern, Recommended)
Partitions are created automatically based on data:
```sql
-- Partitions auto-created on INSERT
CREATE TABLE events (
    event_time DATETIME,
    user_id BIGINT
)
DUPLICATE KEY (event_time)
PARTITION BY date_trunc('day', event_time)  -- Auto-creates daily partitions
DISTRIBUTED BY HASH(user_id) BUCKETS 16;

-- Hourly granularity for high-frequency data
PARTITION BY date_trunc('hour', event_time)

-- Monthly for long-term storage
PARTITION BY date_trunc('month', event_time)
```

### Composite partitioning (Multi-tenant)
```sql
CREATE TABLE metrics (
    tenant_id INT,
    dt DATETIME,
    metric_name STRING,
    value DOUBLE
)
PRIMARY KEY (tenant_id, dt, metric_name)
PARTITION BY tenant_id, date_trunc('day', dt)
DISTRIBUTED BY HASH(tenant_id) BUCKETS 16;
```

### Drop old partitions
```sql
-- Show partitions first
SHOW PARTITIONS FROM table_name;

-- Drop specific partition by name
ALTER TABLE table_name DROP PARTITION p20230101_10001;
```

## Materialized View Pattern

```sql
CREATE MATERIALIZED VIEW mv_daily_summary
BUILD IMMEDIATE
REFRESH ASYNC START('2024-01-01 00:00:00') EVERY(INTERVAL 1 DAY)
AS
SELECT
    date_col,
    status,
    COUNT(*) as total_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM database_name.table_name
GROUP BY date_col, status;
```

## Troubleshooting Quick Guide

### Data loading fails
1. Check error message: `SHOW LOAD WHERE label = 'your_label'`
2. Verify data format matches column definitions
3. Check broker connectivity (for Broker Load)
4. Verify resource availability: `SHOW PROC '/backends'`

### Query is slow
1. Run `EXPLAIN VERBOSE` to check execution plan
2. Verify partition pruning is active
3. Check for data skew in distribution
4. Review JOIN strategy (broadcast vs shuffle)
5. Consider creating materialized views

### Compaction issues
```sql
-- Check compaction status
SHOW PROC '/backends';
SHOW TABLET STATUS FROM table_name;

-- Trigger manual compaction if needed
ALTER TABLE table_name COMPACT;
```

## Best Practices

### Table Design
- Choose appropriate table type based on use case
- Use `date_trunc()` expressions for time-based partitioning
- Set replication_num based on cluster size (typically 3)
- Bucket count = 2-8 × (number of BE cores)
- Keep total partition count under 100k (watch composite partitions)

### Query Performance
- Always filter on partition key when possible
- Use prefix bloom filter for high-cardinality string columns
- Avoid SELECT * in production queries
- Use appropriate JOIN types (prefer INNER JOIN when possible)

### Data Loading
- Use Stream Load for real-time, small batches (<10GB)
- Use Broker Load for large batch loads from object storage
- Set appropriate timeout based on data volume
- Monitor load job status and handle failures

### Maintenance
- Enable dynamic partitioning for time-series tables
- Regularly drop old partitions to manage storage
- Monitor tablet distribution across BEs
- Set up alerts for load failures and query timeouts

## Common Anti-Patterns to Avoid

❌ **Don't** use VARCHAR for time columns that will be partitioned
❌ **Don't** apply functions to partition columns in WHERE (breaks pruning)
❌ **Don't** create too many buckets (causes small files)
❌ **Don't** create too few buckets (causes data skew)
❌ **Don't** skip partition pruning predicates
❌ **Don't** use UNIQUE KEY if you only need deduplication (use DUPLICATE + GROUP BY)
❌ **Don't** load data without labels (prevents duplicate detection)
❌ **Don't** create composite partitions that exceed 100k total partitions

## Additional Resources

- **Infrastructure details**: See [INFRA.md](references/INFRA.md) for cluster setup, table design patterns, and resource management
- **Query optimization**: See [QUERY.md](references/QUERY.md) for advanced query tuning, loading patterns, and ETL workflows

## Key Configuration Properties

### Table Properties
```properties
"replication_num" = "3"                      # Number of replicas
"storage_medium" = "SSD"                     # Storage type (SSD/HDD)
"enable_persistent_index" = "true"           # For primary key tables
"bloom_filter_columns" = "id,email"          # Bloom filter index
"colocate_with" = "group_name"              # Colocate tables
```

### Session Variables
```sql
SET enable_pipeline_engine = true;           # Enable vectorized execution
SET pipeline_dop = 0;                        # Parallelism (0 = auto)
SET query_timeout = 300;                     # Query timeout in seconds
SET enable_spill = true;                     # Enable disk spill for large joins
```

## Getting Started Workflow

When working with a new StarRocks project:

1. **Understand the use case**
   - OLAP analytics vs real-time reporting
   - Query patterns (aggregations, joins, filters)
   - Data volume and retention requirements

2. **Design table schema**
   - Choose appropriate key type (Duplicate/Aggregate/Unique/Primary)
   - Define partition strategy (range by date)
   - Calculate bucket count based on data volume
   - Read [INFRA.md](references/INFRA.md) for detailed guidance

3. **Set up data pipeline**
   - Select loading method (Stream/Broker/Routine Load)
   - Configure error handling and retry logic
   - Read [QUERY.md](references/QUERY.md) for loading patterns

4. **Optimize queries**
   - Analyze query patterns
   - Create materialized views for common aggregations
   - Tune partition and bucket strategies
   - Read [QUERY.md](references/QUERY.md) for optimization techniques

5. **Monitor and maintain**
   - Set up monitoring for load jobs and query performance
   - Configure automatic partition management
   - Plan for data retention and archival
