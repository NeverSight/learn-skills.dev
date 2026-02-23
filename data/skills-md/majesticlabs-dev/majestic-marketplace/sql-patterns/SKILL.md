---
name: sql-patterns
description: Advanced SQL patterns including window functions, CTEs, recursive queries, and optimization techniques.
allowed-tools: Read Write Edit Grep Glob Bash
---

# SQL-Patterns

Advanced SQL patterns for data engineering beyond basic SELECT/JOIN.

## Common Table Expressions (CTEs)

```sql
-- Chain transformations readably
WITH
  active_users AS (
    SELECT user_id, email
    FROM users
    WHERE status = 'active'
  ),
  user_orders AS (
    SELECT u.user_id, COUNT(*) as order_count
    FROM active_users u
    JOIN orders o ON u.user_id = o.user_id
    GROUP BY u.user_id
  )
SELECT * FROM user_orders WHERE order_count > 5;
```

## Window Functions

```sql
-- Row numbering within groups
SELECT *,
  ROW_NUMBER() OVER (PARTITION BY category ORDER BY created_at DESC) as rn
FROM products;

-- Running totals
SELECT
  date,
  revenue,
  SUM(revenue) OVER (ORDER BY date) as cumulative_revenue
FROM daily_sales;

-- Percent of total
SELECT
  category,
  sales,
  sales * 100.0 / SUM(sales) OVER () as pct_of_total
FROM category_sales;

-- Lead/Lag for time series
SELECT
  date,
  value,
  LAG(value, 1) OVER (ORDER BY date) as prev_value,
  value - LAG(value, 1) OVER (ORDER BY date) as change
FROM metrics;

-- Ranking with ties
SELECT *,
  RANK() OVER (ORDER BY score DESC) as rank,       -- 1,2,2,4
  DENSE_RANK() OVER (ORDER BY score DESC) as drank -- 1,2,2,3
FROM scores;
```

## Recursive CTEs

```sql
-- Hierarchical data (org chart, categories)
WITH RECURSIVE org_tree AS (
  -- Base case: top-level managers
  SELECT id, name, manager_id, 1 as depth
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive case: subordinates
  SELECT e.id, e.name, e.manager_id, t.depth + 1
  FROM employees e
  JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;

-- Generate date series
WITH RECURSIVE dates AS (
  SELECT DATE '2024-01-01' as dt
  UNION ALL
  SELECT dt + INTERVAL '1 day'
  FROM dates
  WHERE dt < DATE '2024-12-31'
)
SELECT * FROM dates;
```

## CASE Expressions

```sql
-- Simple CASE
SELECT
  CASE status
    WHEN 'A' THEN 'Active'
    WHEN 'I' THEN 'Inactive'
    ELSE 'Unknown'
  END as status_label
FROM users;

-- Searched CASE for ranges
SELECT
  CASE
    WHEN age < 18 THEN 'Minor'
    WHEN age < 65 THEN 'Adult'
    ELSE 'Senior'
  END as age_group
FROM users;

-- Conditional aggregation
SELECT
  COUNT(*) as total,
  COUNT(*) FILTER (WHERE status = 'active') as active_count,  -- PostgreSQL
  SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_count  -- ANSI
FROM users;
```

## UPSERT Patterns

```sql
-- PostgreSQL: INSERT ON CONFLICT
INSERT INTO inventory (sku, quantity, updated_at)
VALUES ('ABC123', 100, NOW())
ON CONFLICT (sku) DO UPDATE SET
  quantity = EXCLUDED.quantity,
  updated_at = EXCLUDED.updated_at;

-- MySQL: INSERT ON DUPLICATE KEY
INSERT INTO inventory (sku, quantity, updated_at)
VALUES ('ABC123', 100, NOW())
ON DUPLICATE KEY UPDATE
  quantity = VALUES(quantity),
  updated_at = VALUES(updated_at);

-- SQLite: INSERT OR REPLACE
INSERT OR REPLACE INTO inventory (sku, quantity, updated_at)
VALUES ('ABC123', 100, datetime('now'));
```

## Efficient Pagination

```sql
-- BAD: OFFSET for large pages
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 10000;

-- GOOD: Keyset pagination
SELECT * FROM orders
WHERE id > 10000  -- last seen id
ORDER BY id
LIMIT 20;
```

## Batch Operations

```sql
-- Batch DELETE with limit (avoid long locks)
DELETE FROM logs
WHERE created_at < NOW() - INTERVAL '90 days'
LIMIT 10000;

-- Batch UPDATE
UPDATE orders
SET status = 'archived'
WHERE id IN (
  SELECT id FROM orders
  WHERE status = 'completed'
  AND completed_at < NOW() - INTERVAL '1 year'
  LIMIT 1000
);
```

## Index-Friendly Queries

```sql
-- BAD: Function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- GOOD: Store lowercase or use expression index
SELECT * FROM users WHERE email_lower = 'test@example.com';
-- Or: CREATE INDEX idx_email_lower ON users (LOWER(email));

-- BAD: Leading wildcard
SELECT * FROM products WHERE name LIKE '%widget%';

-- GOOD: Full-text search or prefix match
SELECT * FROM products WHERE name LIKE 'widget%';
```

## NULL Handling

```sql
-- COALESCE for defaults
SELECT COALESCE(nickname, first_name, 'Anonymous') as display_name
FROM users;

-- NULLIF to convert values to NULL
SELECT NULLIF(status, '') as status  -- empty string -> NULL
FROM records;

-- IS DISTINCT FROM (NULL-safe comparison)
SELECT * FROM a
WHERE a.value IS DISTINCT FROM b.value;  -- treats NULL != NULL as false
```

## LATERAL Joins

```sql
-- Top N per group
SELECT d.name, t.product, t.revenue
FROM departments d
CROSS JOIN LATERAL (
  SELECT product, revenue
  FROM sales
  WHERE sales.dept_id = d.id
  ORDER BY revenue DESC
  LIMIT 3
) t;
```

## Materialized Views

```sql
-- Create for expensive aggregations
CREATE MATERIALIZED VIEW daily_stats AS
SELECT
  DATE_TRUNC('day', created_at) as date,
  COUNT(*) as total_orders,
  SUM(amount) as revenue
FROM orders
GROUP BY 1;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_stats;
```

## Query Optimization Checklist

1. **Check EXPLAIN ANALYZE** - Look for sequential scans on large tables
2. **Add missing indexes** - Columns in WHERE, JOIN, ORDER BY
3. **Avoid SELECT *** - Fetch only needed columns
4. **Use EXISTS over IN** - For correlated subqueries
5. **Batch large operations** - Avoid long-running transactions
6. **Partition large tables** - By date or category
7. **Use connection pooling** - Avoid connection overhead
