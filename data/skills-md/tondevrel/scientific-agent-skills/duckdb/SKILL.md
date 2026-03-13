---
name: duckdb
description: An analytical in-process SQL database management system. Designed for fast analytical queries (OLAP). Highly interoperable with Python's data ecosystem (Pandas, NumPy, Arrow, Polars). Supports querying files (CSV, Parquet, JSON) directly without an ingestion step. Use for complex SQL queries on Pandas/Polars data, querying large Parquet/CSV files directly, joining data from different sources, analytical pipelines, local datasets too big for Excel, intermediate data storage and feature engineering for ML.
version: 0.10
license: MIT
---

# DuckDB - The SQL Engine for Scientific Data

DuckDB brings the power of professional SQL to the Python data science stack. It is optimized for "Online Analytical Processing" (OLAP), meaning it excels at large-scale aggregations, joins, and complex queries on datasets that are larger than memory.

## When to Use

- Performing complex SQL queries (JOINs, Window functions) on Pandas or Polars data.
- Querying large Parquet or CSV files directly without loading them into memory.
- Efficiently joining data from different sources (e.g., a CSV file and a Pandas DataFrame).
- Building analytical pipelines where SQL is more concise or faster than DataFrame code.
- Managing local datasets that are too big for Excel but don't need a full PostgreSQL server.
- Intermediate data storage and feature engineering for Machine Learning.

## Reference Documentation

**Official docs**: https://duckdb.org/docs/  
**Python API**: https://duckdb.org/docs/api/python/overview  
**Search patterns**: `duckdb.sql`, `duckdb.query`, `duckdb.read_parquet`, `duckdb.from_df`

## Core Principles

### In-Process Execution

DuckDB runs inside your Python process. There is no server to start or manage. The data can be stored in a file (.db) or kept entirely in memory.

### Columnar Engine

Like Polars, DuckDB uses a columnar storage and vectorized execution engine, making it orders of magnitude faster than row-based databases (like SQLite) for analytical tasks.

### Seamless Interoperability

DuckDB can "see" your Python variables. You can run a SQL query directly against a Pandas DataFrame variable as if it were a table in the database.

## Quick Reference

### Installation

```bash
pip install duckdb
```

### Standard Imports

```python
import duckdb
import pandas as pd
import numpy as np
```

### Basic Pattern - Querying Python Data

```python
import duckdb
import pandas as pd

# 1. Create a sample DataFrame
df = pd.DataFrame({"id": [1, 2, 3], "val": [10.5, 20.0, 15.2]})

# 2. Query the DataFrame directly via SQL
# DuckDB automatically finds the 'df' variable in the local scope
result_df = duckdb.sql("SELECT id, val * 2 AS doubled FROM df WHERE val > 12").df()

print(result_df)
```

## Critical Rules

### ✅ DO

- **Query Files Directly** - Use `SELECT * FROM 'data.parquet'` instead of loading the file first. DuckDB will only read the required columns and rows.
- **Use the .df(), .pl(), .arrow() methods** - Efficiently convert query results to your preferred format (Pandas, Polars, or Arrow).
- **Use Persistent Storage for Large Data** - Use `duckdb.connect('my_data.db')` if you want your data to persist between script runs.
- **Leverage Parquet** - DuckDB is a "best-in-class" engine for Parquet files; use them for maximum speed.
- **Use Wildcards** - Query thousands of files at once using `FROM 'data/*.parquet'`.
- **Use EXPLAIN** - Prefix your query with `EXPLAIN ANALYZE` to see how DuckDB is executing the query and find bottlenecks.

### ❌ DON'T

- **Use for High-Frequency Writes (OLTP)** - DuckDB is for analysis. If you need to insert rows one by one thousands of times per second, use SQLite or PostgreSQL.
- **Ignore the Connection** - If you are using a file-based database, ensure you close the connection or use a context manager to avoid file locking.
- **Manually Load CSVs if not needed** - Don't do `pd.read_csv()` then query it. Query the file path directly for better performance.

## Anti-Patterns (NEVER)

```python
import duckdb
import pandas as pd

# ❌ BAD: Loading everything into Pandas just to do a simple filter
# df = pd.read_csv("massive.csv") 
# result = df[df['val'] > 100]

# ✅ GOOD: Let DuckDB filter while reading (saves RAM)
result = duckdb.sql("SELECT * FROM 'massive.csv' WHERE val > 100").df()

# ❌ BAD: Manual string formatting for SQL queries (SQL Injection risk)
# duckdb.sql(f"SELECT * FROM data WHERE name = '{user_input}'")

# ✅ GOOD: Use prepared statements or parameters
duckdb.execute("SELECT * FROM data WHERE name = ?", [user_input]).df()

# ❌ BAD: Re-reading the same file in a loop
# for i in range(10): 
#    res = duckdb.sql("SELECT mean(val) FROM 'large.parquet'").df()

# ✅ GOOD: Create a VIEW or TABLE first
duckdb.sql("CREATE VIEW data_view AS SELECT * FROM 'large.parquet'")
for i in range(10):
    res = duckdb.sql("SELECT mean(val) FROM data_view").df()
```

## SQL Features and Operations

### Querying Different Sources

```python
# Query a CSV
res_csv = duckdb.sql("SELECT * FROM read_csv_auto('data.csv')").df()

# Query a Parquet file
res_pq = duckdb.sql("SELECT * FROM 'data.parquet' WHERE price > 50").df()

# Query multiple Parquet files and join with a Pandas DF
df_metadata = pd.DataFrame(...)
query = """
    SELECT p.*, m.category 
    FROM 'raw_data/*.parquet' p
    JOIN df_metadata m ON p.id = m.id
    LIMIT 10
"""
res = duckdb.sql(query).df()
```

### Relational API (Programmatic SQL)

If you prefer a Pythonic method-chaining style over raw SQL:

```python
rel = duckdb.from_df(df)
res = rel.filter("val > 15").project("id, val * 2").order("val").limit(5)
print(res.df())
```

### Advanced SQL: Window Functions and Aggregations

DuckDB supports full modern SQL, which is often easier for complex statistics than Pandas.

```python
query = """
    SELECT 
        date,
        station_id,
        temp,
        AVG(temp) OVER (PARTITION BY station_id ORDER BY date ROWS BETWEEN 7 PRECEDING AND CURRENT ROW) as rolling_7d_avg,
        temp - LAG(temp) OVER (PARTITION BY station_id ORDER BY date) as daily_change
    FROM 'weather_data.parquet'
"""
df_stats = duckdb.sql(query).df()
```

### Working with Persistent Databases

```python
# Create or open a database file
con = duckdb.connect('scientific_project.db')

# Create a table from a dataframe
con.execute("CREATE TABLE experiment_results AS SELECT * FROM df")

# Check tables
print(con.execute("SHOW TABLES").df())

# Close connection
con.close()
```

## Performance Optimization

### 1. External Aggregation (Disk Spilling)

If a query exceeds your RAM, DuckDB can "spill to disk" to finish the calculation.

```python
# Enable temp directory for large queries
duckdb.sql("SET temp_directory='/tmp/duckdb_temp/'")
duckdb.sql("SET max_memory='4GB'") # Limit RAM usage
```

### 2. Parallel Processing

DuckDB is parallel by default. You can control the number of threads.

```python
duckdb.sql("SET threads TO 8")
```

### 3. Sampling for Exploratory Analysis

Querying a sample of a massive file is instantaneous.

```python
# Random 10% sample
df_sample = duckdb.sql("SELECT * FROM 'huge.parquet' USING SAMPLE 10%").df()
```

## Practical Workflows

### 1. The "Big Data" Cleaning Pipeline

```python
def process_experiment_logs(glob_pattern):
    """Clean and aggregate TBs of log data across many files."""
    query = f"""
    WITH clean_data AS (
        SELECT 
            timestamp::TIMESTAMP as ts,
            sensor_id,
            value
        FROM read_csv_auto('{glob_pattern}')
        WHERE value IS NOT NULL AND value != -999
    )
    SELECT 
        time_bucket(INTERVAL '1 hour', ts) as hour,
        sensor_id,
        AVG(value) as avg_val
    FROM clean_data
    GROUP BY 1, 2
    ORDER BY 1, 2
    """
    return duckdb.sql(query).df()
```

### 2. Fast Feature Engineering for ML

```python
def create_features(df_train):
    # Use SQL to create complex lag and moving average features
    return duckdb.sql("""
        SELECT *,
               AVG(price) OVER (PARTITION BY item ORDER BY date ROWS 3 PRECEDING) as ma3,
               COUNT(*) OVER (PARTITION BY user) as user_activity_count
        FROM df_train
    """).df()
```

### 3. Interop: DuckDB to PyTorch/TensorFlow

```python
# Query data and convert to Arrow for zero-copy transfer to Deep Learning
arrow_table = duckdb.sql("SELECT * FROM 'data.parquet'").arrow()

# Then in PyTorch (requires torch.utils.dlpack or similar)
# Or just use the fast arrow-to-numpy/tensor path
```

## Common Pitfalls and Solutions

### The "Variable Not Found" Error

DuckDB looks for variables in the scope where `duckdb.sql()` is called.

```python
# ✅ Solution: If calling inside a function, ensure the variable is local or passed
def my_query(my_df):
    return duckdb.sql("SELECT * FROM my_df").df()
```

### Locked Database File

If two processes try to open the same .db file as 'write', it will fail.

```python
# ✅ Solution: Open as read-only for secondary processes
con = duckdb.connect('data.db', read_only=True)
```

### Date/Time Parsing

CSVs often have weird date formats.

```python
# ✅ Solution: Use strptime or let DuckDB auto-detect
# SELECT strptime(date_col, '%d/%m/%Y') FROM 'data.csv'
```

## Best Practices

1. **Query files directly** - Use `SELECT * FROM 'file.parquet'` instead of loading into memory first.
2. **Use appropriate output format** - Use `.df()` for Pandas, `.pl()` for Polars, `.arrow()` for Arrow.
3. **Create views for repeated queries** - Avoid re-reading the same file multiple times.
4. **Use prepared statements** - Prevent SQL injection and improve performance for repeated queries.
5. **Leverage Parquet format** - DuckDB excels at Parquet; use it for maximum performance.
6. **Use wildcards for multiple files** - Query many files at once with `FROM 'data/*.parquet'`.
7. **Enable disk spilling for large queries** - Set `temp_directory` and `max_memory` for out-of-memory operations.
8. **Use EXPLAIN ANALYZE** - Understand query execution and identify bottlenecks.
9. **Close connections properly** - Use context managers or explicitly close file-based connections.
10. **Prefer SQL for complex aggregations** - Window functions and complex joins are often clearer in SQL than DataFrame code.

DuckDB is the bridge between the analytical power of SQL and the flexibility of Python. It eliminates the "data loading tax" and allows scientists to focus on asking complex questions of their data at lightning speeds.
