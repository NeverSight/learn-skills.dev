---
name: pandas-performance
description: Advanced sub-skill for pandas focused on memory optimization, execution speed, and handling large-scale datasets (10M+ rows). Covers low-level dtypes, efficient indexing, and vectorization of complex logic.
version: 2.2
license: BSD-3-Clause
---

# pandas - Performance & Memory Management

Standard pandas code is often memory-hungry and slow. This sub-skill provides the techniques to make pandas 10x faster and use 5x less RAM by understanding its internal architecture (BlockManager and Arrow backend).

## When to Use

- Your DataFrame is larger than 1GB and causes RAM pressure.
- `pd.read_csv` is taking too long to load data.
- Row-wise operations (`apply`, `iterrows`) are creating bottlenecks.
- You need to perform complex joins or lookups on millions of rows.
- Preparing data for high-performance ML models.

## Reference Documentation

- **Official Performance Guide**: https://pandas.pydata.org/docs/user_guide/enhancingperf.html
- **Scaling to Large Data**: https://pandas.pydata.org/docs/user_guide/scale.html
- **Search patterns**: `df.memory_usage`, `pd.to_numeric(downcast=...)`, `pd.Categorical`, `DataFrame.eval()`

## Core Principles

### RAM is the Bottleneck

Pandas usually creates copies of data during operations. To handle large data, you must minimize copies and use the most efficient bit-width for your data types.

### Vectorization vs. Loops

- **Level 1 (Best)**: Built-in NumPy/Pandas vectorized functions.
- **Level 2 (Good)**: `df.eval()` or `df.query()` for complex math.
- **Level 3 (Average)**: `np.vectorize` or `df.apply()` (only if logic is complex).
- **Level 4 (Worst)**: `iterrows()` or `itertuples()`.

## Memory Optimization Patterns

### 1. The "Downcasting" Workflow

Standard integer and float columns use 64 bits by default. Most scientific data fits in 16 or 32 bits.

```python
import pandas as pd
import numpy as np

def optimize_memory(df):
    start_mem = df.memory_usage().sum() / 1024**2
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
            else:
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
        else:
            # Convert low-cardinality strings to Categorical
            num_unique = df[col].nunique()
            if num_unique / len(df) < 0.5:
                df[col] = df[col].astype('category')
                
    end_mem = df.memory_usage().sum() / 1024**2
    print(f'Memory reduced by {100 * (start_mem - end_mem) / start_mem:.1f}%')
    return df
```

### 2. Modern PyArrow Backend (Pandas 2.0+)

Use the Arrow backend for massive speedups in string operations and faster loading.

```python
# Load with Arrow engine for 2-3x speedup
df = pd.read_csv("data.csv", engine="pyarrow", dtype_backend="pyarrow")
```

## Speed Optimization Patterns

### 1. Vectorizing Complex "If-Else" (Instead of .apply)

Instead of calling a Python function for every row:

```python
# ❌ SLOW:
# df['status'] = df.apply(lambda x: 'High' if x['val'] > 100 else 'Low', axis=1)

# ✅ FAST:
df['status'] = np.where(df['val'] > 100, 'High', 'Low')

# ✅ FAST (Multiple conditions):
conditions = [
    (df['val'] > 100),
    (df['val'] > 50) & (df['val'] <= 100),
    (df['val'] <= 50)
]
choices = ['High', 'Medium', 'Low']
df['status'] = np.select(conditions, choices, default='Unknown')
```

### 2. High-Speed Lookups

If you need to map values from a dictionary/other table millions of times:

```python
# ❌ SLOW: df.merge() or df['id'].map(large_dict)
# ✅ FAST: Use a Series as a lookup table with index
lookup_table = pd.Series(data=values, index=keys)
result = lookup_table.reindex(df['target_ids']).values
```

## Efficient I/O

### 1. Parquet with Filtering (Predicate Pushdown)

Never use CSV for large data storage. Use Parquet.

```python
# Save as partitioned parquet
df.to_parquet('data_dir', partition_cols=['year', 'month'])

# Load only specific columns and rows (Fast)
df_subset = pd.read_parquet('data_dir', columns=['price', 'id'], 
                            filters=[('year', '==', 2023)])
```

### 2. Chunking for Memory-Limited Systems

If the file is 50GB and you have 16GB RAM:

```python
# Process in chunks of 100k rows
chunk_size = 100_000
for chunk in pd.read_csv("massive.csv", chunksize=chunk_size):
    # Perform aggregation
    summary = chunk.groupby('id')['value'].sum()
    # Save or update a running total
```

## Critical Rules for Performance

### ✅ DO

- **Use In-place operations sparingly** - Contrary to myth, `inplace=True` often creates internal copies anyway. Focus on dtypes instead.
- **Sort Index for Slicing** - If you slice a large DataFrame by index, ensure it is sorted: `df.sort_index(inplace=True)`. This turns an O(N) operation into O(log N).
- **Use pd.to_datetime with format** - Specifying the format (`%Y-%m-%d`) is much faster than automatic parsing.
- **Leverage .eval()** - For complex arithmetic like `(A + B) / (C * D)`, `df.eval()` is faster and more memory-efficient as it uses numexpr.

### ❌ DON'T

- **Never iterate with iterrows()** - It converts each row into a Series object, which is incredibly slow.
- **Avoid object dtypes** - Any column with object dtype (usually strings) is a pointer to a Python object, which is memory-intensive. Use `category` or `string[pyarrow]`.
- **Don't use append() in a loop** - It creates a full copy of the DataFrame every time. Collect data in a list and use `pd.concat()`.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Growing a DataFrame row by row
df = pd.DataFrame()
for data in large_source:
    df = pd.concat([df, pd.DataFrame([data])]) # ❌ Disaster for performance!

# ✅ GOOD: List of dicts to DataFrame
data_list = []
for data in large_source:
    data_list.append(data)
df = pd.DataFrame(data_list)

# ❌ BAD: Manual string formatting
# df['name'].apply(lambda x: f"USER_{x}")

# ✅ GOOD: Vectorized string accessor
df['name'] = "USER_" + df['name'].astype(str)
```

## Practical Workflows

### 1. Identifying Memory Hogs

```python
# Get detailed memory breakdown (including object overhead)
print(df.memory_usage(deep=True))

# Identify columns with too many unique strings (bad for 'category')
for col in df.select_dtypes(include=['object']):
    print(f"{col}: {df[col].nunique() / len(df):.2%}")
```

### 2. Fast Deduplication of 10M+ Rows

```python
# Using sorting + shift is often faster than drop_duplicates
df = df.sort_values(['id', 'timestamp'])
mask = (df['id'] != df['id'].shift())
df_unique = df[mask]
```

### 3. Merging with Multi-Index

```python
# If you join on multiple columns, setting them as an index 
# and using join() can be 5x faster than merge()
df1.set_index(['key1', 'key2'], inplace=True)
df2.set_index(['key1', 'key2'], inplace=True)
result = df1.join(df2, how='inner')
```

This sub-skill turns pandas from a prototyping tool into a high-performance engine capable of handling industrial-scale scientific data.
