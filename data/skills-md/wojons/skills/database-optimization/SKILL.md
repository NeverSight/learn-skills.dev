---
name: database-optimization
description: Use when you need to optimize database performance, schema design, indexing, and query performance across different database systems
license: MIT
compatibility: opencode
metadata:
  audience: database-admins, developers
  category: database
---

# Database Optimization

Optimize database performance, schema design, indexing, and query performance across different database systems including SQL (PostgreSQL, MySQL, SQL Server) and NoSQL (MongoDB, Cassandra, Redis) databases. This skill provides comprehensive database optimization strategies and tools.

## When to use me

Use this skill when:
- Database performance is degrading and queries are slow
- You need to optimize database schema and indexing strategies
- You want to analyze and optimize query performance
- You need to tune database configuration parameters
- You're migrating databases and need optimization guidance
- You want to implement database monitoring and alerting
- You need to optimize database for specific workloads (OLTP, OLAP, hybrid)
- You want to reduce database costs through optimization

## What I do

- **Query performance analysis**: Analyze and optimize SQL and NoSQL queries
- **Index optimization**: Analyze and optimize database indexes
- **Schema optimization**: Optimize database schema design and normalization
- **Configuration tuning**: Tune database configuration parameters for optimal performance
- **Connection pooling optimization**: Optimize database connection management
- **Locking and concurrency optimization**: Optimize locking strategies and concurrency control
- **Storage optimization**: Optimize database storage and partitioning strategies
- **Replication and sharding optimization**: Optimize replication and sharding strategies
- **Backup and recovery optimization**: Optimize backup and recovery strategies
- **Database monitoring**: Implement database performance monitoring and alerting

## Examples

```bash
# Analyze query performance
./scripts/analyze-database-optimization.sh --query-analysis --database postgresql

# Optimize database indexes
./scripts/analyze-database-optimization.sh --index-optimization --database mysql

# Tune database configuration
./scripts/analyze-database-optimization.sh --configuration-tuning --database mongodb

# Generate optimization report
./scripts/analyze-database-optimization.sh --report --output optimization-report.json

# Monitor database performance
./scripts/analyze-database-optimization.sh --performance-monitoring --interval 60
```

## Output format

```
Database Optimization Analysis
─────────────────────────────────────
Analysis Date: 2025-01-15T10:30:00Z
Database System: PostgreSQL 14.8
Database Size: 245 GB
Analysis Duration: 15 minutes

PERFORMANCE METRICS:
────────────────────
Current Performance Score: 72/100
Query Response Time: 85th percentile: 450ms (Target: < 200ms)
Transactions per Second: 125 (Target: > 200)
Connection Pool Utilization: 92% (Target: < 80%)
Cache Hit Ratio: 78% (Target: > 90%)

QUERY PERFORMANCE ANALYSIS:
───────────────────────────
Slow Queries Identified: 42
Total Query Execution Time: 85% spent on 5 queries

Top 5 Slowest Queries:
1. Query: SELECT * FROM orders WHERE customer_id = ? AND status = ? ORDER BY created_at DESC LIMIT 100
   Average Execution Time: 1,250ms
   Execution Count: 12,850/day
   Issue: Missing composite index on (customer_id, status, created_at)
   Optimization: Add index: CREATE INDEX idx_orders_customer_status_created ON orders(customer_id, status, created_at DESC)

2. Query: SELECT p.*, c.name FROM products p JOIN categories c ON p.category_id = c.id WHERE p.price > ? AND p.stock > 0
   Average Execution Time: 890ms
   Execution Count: 8,420/day
   Issue: Sequential scan on products table (245,000 rows)
   Optimization: Add index: CREATE INDEX idx_products_price_stock ON products(price) WHERE stock > 0

3. Query: UPDATE inventory SET quantity = quantity - ? WHERE product_id = ? AND warehouse_id = ?
   Average Execution Time: 650ms
   Execution Count: 15,230/day
   Issue: Row-level locking contention
   Optimization: Implement optimistic locking or batch updates

4. Query: SELECT user_id, COUNT(*) as order_count FROM orders WHERE created_at > NOW() - INTERVAL '30 days' GROUP BY user_id HAVING COUNT(*) > 5
   Average Execution Time: 1,850ms
   Execution Count: 1,250/day
   Issue: Full table scan with aggregation
   Optimization: Create summary table or materialized view

5. Query: DELETE FROM sessions WHERE expires_at < NOW()
   Average Execution Time: 2,150ms
   Execution Count: 850/day
   Issue: Table bloat and vacuum overhead
   Optimization: Implement batch deletion with index on expires_at

INDEX OPTIMIZATION ANALYSIS:
─────────────────────────────
Current Indexes: 48
Duplicate Indexes: 7
Unused Indexes: 12
Missing Indexes: 9

Index Issues:
• Duplicate: idx_orders_customer (customer_id) and idx_orders_customer_status (customer_id, status)
• Unused: idx_products_supplier (supplier_id) - 0 uses in 30 days
• Missing: idx_orders_created_status (created_at, status) - would benefit 3 frequent queries

Index Recommendations:
1. Drop 7 duplicate indexes: Free 2.8GB storage
2. Drop 12 unused indexes: Free 4.2GB storage
3. Add 9 missing indexes: Improve query performance 35-85%

SCHEMA OPTIMIZATION:
────────────────────
Normalization Issues:
• products table has redundant category_name field (denormalized)
• orders table missing foreign key constraint on customer_id
• users table has JSONB field with frequently queried data (should be separate columns)

Schema Recommendations:
1. Remove redundant category_name from products table
2. Add foreign key constraint: ALTER TABLE orders ADD CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
3. Extract frequently queried JSONB fields to separate columns
4. Consider partitioning orders table by created_at month

CONFIGURATION TUNING:
──────────────────────
Current Configuration Issues:
• shared_buffers: 128MB (Recommended: 4-8GB for 32GB RAM)
• work_mem: 4MB (Recommended: 64MB for complex queries)
• maintenance_work_mem: 64MB (Recommended: 1-2GB)
• effective_cache_size: 4GB (Recommended: 24GB)
• random_page_cost: 4.0 (Recommended: 1.1 for SSDs)

Configuration Recommendations:
shared_buffers = 8GB
work_mem = 64MB
maintenance_work_mem = 2GB
effective_cache_size = 24GB
random_page_cost = 1.1

CONNECTION POOLING ANALYSIS:
────────────────────────────
Current: 200 connections, 184 active (92% utilization)
Issues: Connection pool exhaustion during peak hours
Recommendations:
• Increase connection pool to 300
• Implement connection pool with pgbouncer
• Set idle connection timeout to 300 seconds

LOCKING AND CONCURRENCY:
─────────────────────────
Lock Wait Events: 12,850/day
Deadlocks: 8/day
Issues: High row-level locking on inventory table
Recommendations:
• Implement optimistic locking for inventory updates
• Use SKIP LOCKED for batch processing
• Reduce transaction isolation level where appropriate

STORAGE OPTIMIZATION:
──────────────────────
Table Sizes:
• orders: 85GB (35% of database)
• products: 42GB (17% of database)
• users: 28GB (11% of database)

Storage Issues:
• orders table has high bloat (32% dead tuples)
• No partitioning on time-series data
• Uncompressed JSONB columns

Storage Recommendations:
1. Vacuum aggressive on orders table
2. Implement partitioning on orders by created_at (monthly)
3. Enable compression for historical data
4. Archive old orders to cold storage

REPLICATION AND SHARDING:
─────────────────────────
Current: Single primary with 2 read replicas
Issues: Replication lag up to 45 seconds during peak
Recommendations:
• Add 1 more read replica
• Implement connection routing (primary for writes, replicas for reads)
• Consider sharding by customer_id for orders table

BACKUP AND RECOVERY:
─────────────────────
Current: Daily full backup, 7-day retention
Issues: Backup takes 4 hours, affects performance
Recommendations:
• Implement incremental backups with WAL archiving
• Increase retention to 30 days
• Test recovery procedure monthly

PERFORMANCE MONITORING:
────────────────────────
Current Monitoring: Basic (CPU, memory, disk)
Missing: Query performance, index usage, lock monitoring
Recommendations:
• Implement pg_stat_statements for query monitoring
• Set up alerts for slow queries (> 500ms)
• Monitor index usage and bloat weekly

COST OPTIMIZATION:
──────────────────
Current Monthly Cost: $1,850 (AWS RDS)
Optimization Opportunities:
• Right-size instance: Save $450/month
• Reserved instance: Save $650/month (3-year)
• Storage optimization: Save $125/month
• Archive old data: Save $85/month

Total Potential Savings: $1,310/month (71%)

IMPLEMENTATION ROADMAP:
────────────────────────
Phase 1: Immediate (1-2 days):
• Add 5 missing indexes for slowest queries
• Drop 7 duplicate indexes
• Tune critical configuration parameters

Phase 2: Short-term (1-2 weeks):
• Implement connection pooling
• Add query performance monitoring
• Optimize backup strategy

Phase 3: Medium-term (3-4 weeks):
• Implement table partitioning
• Add read replica
• Optimize schema (remove redundancy, add constraints)

Phase 4: Long-term (2-3 months):
• Implement sharding strategy
• Archive historical data
• Comprehensive performance testing

EXPECTED RESULTS:
─────────────────
• Query performance improvement: 45-85%
• Storage reduction: 15-25%
• Cost reduction: 50-70%
• Availability improvement: 99.9% → 99.95%
• Maintenance overhead reduction: 40-60%
```

## Notes

- Database optimization is an iterative process; measure before and after changes
- Different database systems require different optimization approaches
- Consider workload patterns (OLTP vs OLAP) when optimizing
- Test optimization changes in staging before production
- Monitor the impact of optimization changes on application performance
- Regular maintenance (vacuum, analyze, reindex) is essential for sustained performance
- Consider both read and write performance when optimizing
- Balance normalization with performance requirements
- Implement comprehensive monitoring to detect performance regressions