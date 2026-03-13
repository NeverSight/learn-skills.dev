---
name: polars
description: Blazingly fast DataFrame library written in Rust. Features a multi-threaded query engine, lazy evaluation, and efficient memory usage via Apache Arrow. Designed for high-performance data processing on a single machine. Use for large datasets (1GB-100GB+), fast data transformations, Parquet/CSV processing, complex query pipelines, memory-efficient operations, and when speed is critical (10-100x faster than pandas).
version: 0.20
license: MIT
---

# Polars - High-Performance Dataframes

Polars is designed for speed. Unlike pandas, which processes data sequentially on a single CPU core, Polars parallelizes operations across all available cores. Its "Lazy API" allows it to optimize queries before execution, significantly reducing memory overhead and processing time.

## When to Use

- Processing large datasets (1GB - 100GB+) that struggle in pandas.
- When execution speed is a priority (Polars is often 10-100x faster than pandas).
- Working with complex data transformation pipelines (Lazy evaluation).
- Systems with limited RAM (Polars is more memory-efficient than pandas).
- Situations requiring strict type safety and consistent null handling.
- Reading/writing large Parquet, CSV, or Avro files.

## Reference Documentation

**Official docs**: https://docs.pola.rs/  
**User Guide**: https://docs.pola.rs/user-guide/  
**Search patterns**: `pl.DataFrame`, `pl.LazyFrame`, `pl.col`, `df.select`, `df.filter`, `df.group_by`

## Core Principles

### Eager vs. Lazy API

- **Eager**: Operations are executed immediately (like pandas).
- **Lazy**: Operations are queued into a query plan. Polars optimizes the plan (e.g., predicate pushdown, projection pushdown) and executes it only when called.

### The Expression API

Polars uses a declarative syntax. Instead of writing loops or complex lambdas, you write expressions using `pl.col()`. These expressions are highly optimized and run in parallel.

### Apache Arrow

Polars stores data in the Apache Arrow format, enabling zero-copy data exchange with other tools like PyArrow and DuckDB.

## Quick Reference

### Installation

```bash
pip install polars
# For Excel/Cloud support
pip install 'polars[all]'
```

### Standard Imports

```python
import polars as pl
import numpy as np
```

### Basic Pattern - Lazy Workflow (The "Polars Way")

```python
import polars as pl

# 1. Scan (Lazy) - doesn't load data yet
lf = pl.scan_csv("massive_data.csv")

# 2. Build Query Plan
query = (
    lf.filter(pl.col("age") > 25)
    .group_by("city")
    .agg([
        pl.col("salary").mean().alias("avg_salary"),
        pl.col("name").count().alias("count")
    ])
    .sort("avg_salary", descending=True)
)

# 3. Collect (Execute)
df = query.collect()
```

## Critical Rules

### ✅ DO

- **Prefer Lazy API (scan_*)** - This allows Polars to optimize memory and skip unnecessary data.
- **Use Expressions** - Always use `pl.col("name")` instead of selecting columns via strings or indices.
- **Method Chaining** - Polars is built for clean, readable pipelines.
- **Specify Schema** - When reading CSVs, providing a schema prevents type inference errors and speeds up loading.
- **Use collect(streaming=True)** - For datasets larger than RAM, streaming allows Polars to process data in chunks.
- **Parquet over CSV** - Use Parquet for permanent storage; it is significantly faster and stores type information.

### ❌ DON'T

- **Avoid .apply()** - Custom Python functions are slow because they break the Rust/parallel optimization. Use built-in expressions.
- **Don't use inplace=True** - Polars (like JAX) favors immutability; transformations return new DataFrames.
- **Don't convert to pandas early** - Keep data in Polars as long as possible to maintain speed.
- **Avoid Row Iteration** - `for row in df` is an anti-pattern; use vectorized expressions.

## Anti-Patterns (NEVER)

```python
import polars as pl

# ❌ BAD: Using Python lambdas for simple math
# df.select(pl.col("val").map_elements(lambda x: x * 2)) # Slow!

# ✅ GOOD: Use expressions
df.select(pl.col("val") * 2) # Fast, parallelized in Rust

# ❌ BAD: Filtering after a heavy operation
# df.group_by("id").mean().filter(pl.col("id") == 5)

# ✅ GOOD: Lazy API will automatically "push down" the filter
(pl.scan_csv("data.csv")
 .filter(pl.col("id") == 5) # Optimized to read only id=5
 .group_by("id").mean())

# ❌ BAD: Converting to pandas just to check .head()
# df.to_pandas().head() 

# ✅ GOOD: Polars has its own fast .head() and rich printing
print(df.head())
```

## Expression API Deep Dive

### Selection and Transformation

```python
df.select([
    pl.col("name"),
    pl.col("price") * 1.2, # Scalar math
    pl.col("category").str.to_uppercase(), # String methods
    pl.col("date").dt.year().alias("year") # Date methods
])
```

### Filtering

```python
# Multiple conditions
df.filter(
    (pl.col("price") < 100) & 
    (pl.col("status") == "active") |
    (pl.col("category").is_in(["A", "B"]))
)
```

### Aggregation and Grouping

#### High-Performance Stats

```python
results = df.group_by("department").agg([
    pl.col("salary").sum(),
    pl.col("salary").max().alias("max_pay"),
    pl.col("name").n_unique().alias("unique_employees"),
    # Advanced: conditional aggregation inside group
    pl.col("salary").filter(pl.col("role") == "manager").mean().alias("manager_avg")
])
```

### Joins and Concatenation

#### SQL-like operations

```python
# Joins: 'inner', 'left', 'outer', 'semi', 'anti', 'cross'
df_joined = df_a.join(df_b, on="id", how="left")

# As-of join (for time-series alignment)
df_aligned = df_trades.join_asof(df_quotes, on="timestamp", by="symbol")

# Concatenation
df_stacked = pl.concat([df1, df2], how="vertical")
```

### Reshaping (Pivot and Melt)

```python
# Pivot
pivoted = df.pivot(values="sales", index="date", columns="region", aggregate_function="sum")

# Melt (Unpivot)
melted = df.melt(id_vars="date", value_vars=["store_a", "store_b"])
```

## Practical Workflows

### 1. Large-Scale Data Cleaning Pipeline

```python
def clean_and_optimize(path):
    return (
        pl.scan_parquet(path)
        .drop_nulls(subset=["user_id"])
        .with_columns([
            pl.col("email").str.to_lowercase(),
            pl.col("timestamp").str.to_datetime("%Y-%m-%d %H:%M:%S"),
            (pl.col("income") / 1000).cast(pl.Float32) # Downcast for memory
        ])
        .filter(pl.col("timestamp") > pl.date(2023, 1, 1))
        .collect(streaming=True)
    )
```

### 2. Time-Series Feature Engineering

```python
def engineer_features(df):
    return df.with_columns([
        # Rolling average
        pl.col("price").rolling_mean(window_size="7d", by="date").alias("rolling_7d"),
        # Lead/Lag
        pl.col("price").shift(1).alias("prev_price"),
        # Cumulative sum
        pl.col("sales").cum_sum().over("category")
    ])
```

### 3. Fast JSON/Log Parsing

```python
def parse_logs(path):
    return (
        pl.scan_ndjson(path) # Read line-delimited JSON
        .select([
            "level",
            pl.col("message").str.extract(r"Error: (.*)", 1),
            pl.col("metadata").struct.field("user_id") # Access nested fields
        ])
        .collect()
    )
```

## Performance Optimization

### The Power of with_columns

Instead of creating one column at a time, use `with_columns` to run multiple calculations in parallel.

```python
# All 3 columns are calculated simultaneously in different threads
df = df.with_columns([
    (pl.col("a") + pl.col("b")).alias("sum"),
    (pl.col("a") * pl.col("b")).alias("prod"),
    pl.col("c").str.len().alias("c_len")
])
```

### Column Selection via Dtypes

Rapidly apply transformations to groups of columns.

```python
# Multiply all float columns by 100
df = df.with_columns(
    pl.col(pl.Float64) * 100
)
```

## Common Pitfalls and Solutions

### The .apply() Trap

Python functions in `.map_elements()` (formerly `.apply()`) are slow.

```python
# ❌ Problem: Using custom Python code
# df.select(pl.col("txt").map_elements(my_custom_func))

# ✅ Solution: Use Polars native expressions or pl.when()
df.select(
    pl.when(pl.col("score") > 50).then(pl.lit("Pass")).otherwise(pl.lit("Fail"))
)
```

### Memory Errors on Large Files

If you hit OOM with `.collect()`, you might be trying to load too much data into memory.

```python
# ✅ Solution: 
# 1. Use .filter() early in the Lazy plan.
# 2. Use streaming: .collect(streaming=True).
# 3. Select only the columns you need.
```

### String vs Categorical

For low-cardinality strings (like "City" or "Gender"), use Categorical.

```python
# ✅ Solution: Saves massive amounts of RAM and speeds up joins
df = df.with_columns(pl.col("category").cast(pl.Categorical))
```

## Best Practices

1. **Always use Lazy API for large files** - Start with `scan_csv()` or `scan_parquet()` instead of `read_csv()` or `read_parquet()`.
2. **Build complete query plans before collecting** - Let Polars optimize the entire pipeline.
3. **Use expressions over Python functions** - Leverage `pl.col()` expressions for maximum performance.
4. **Specify schemas when reading CSVs** - Prevents type inference overhead and errors.
5. **Use streaming for out-of-memory datasets** - Enable `streaming=True in collect()`.
6. **Prefer Parquet format** - Faster reads/writes and preserves type information.
7. **Cast to Categorical for low-cardinality strings** - Significant memory and performance gains.
8. **Use with_columns for multiple transformations** - Parallelizes column creation.
9. **Filter early in lazy queries** - Predicate pushdown reduces data scanned.
10. **Avoid converting to pandas** - Stay in Polars ecosystem for maximum speed.

Polars is the new gold standard for single-node data processing. By combining the safety of Rust with the flexibility of Python, it provides a seamless and incredibly fast experience for modern data science.
