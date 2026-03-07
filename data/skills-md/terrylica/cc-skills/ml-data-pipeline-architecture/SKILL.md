---
name: ml-data-pipeline-architecture
description: Patterns for efficient ML data pipelines using Polars, Arrow, and ClickHouse. TRIGGERS - data pipeline, polars vs pandas, arrow format, clickhouse ml, efficient loading, zero-copy, memory optimization.
allowed-tools: Read, Grep, Glob
---

# ML Data Pipeline Architecture

Patterns for efficient ML data pipelines using Polars, Arrow, and ClickHouse.

**ADR**: [2026-01-22-polars-preference-hook](/docs/adr/2026-01-22-polars-preference-hook.md) (efficiency preferences framework)

> **Note**: A PreToolUse hook enforces Polars preference. To use Pandas, add `# polars-exception: <reason>` at file top.

## When to Use This Skill

Use this skill when:

- Deciding between Polars and Pandas for a data pipeline
- Optimizing memory usage with zero-copy Arrow patterns
- Loading data from ClickHouse into PyTorch DataLoaders
- Implementing lazy evaluation for large datasets
- Migrating existing Pandas code to Polars

---

## 1. Decision Tree: Polars vs Pandas

```
Dataset size?
├─ < 1M rows → Pandas OK (simpler API, richer ecosystem)
├─ 1M-10M rows → Consider Polars (2-5x faster, less memory)
└─ > 10M rows → Use Polars (required for memory efficiency)

Operations?
├─ Simple transforms → Either works
├─ Group-by aggregations → Polars 5-10x faster
├─ Complex joins → Polars with lazy evaluation
└─ Streaming/chunked → Polars scan_* functions

Integration?
├─ scikit-learn heavy → Pandas (better interop)
├─ PyTorch/custom → Polars + Arrow (zero-copy to tensor)
└─ ClickHouse source → Arrow stream → Polars (optimal)
```

---

## 2. Zero-Copy Pipeline Architecture

### The Problem with Pandas

```python
# BAD: 3 memory copies
df = pd.read_sql(query, conn)     # Copy 1: DB → pandas
X = df[features].values           # Copy 2: pandas → numpy
tensor = torch.from_numpy(X)      # Copy 3: numpy → tensor
# Peak memory: 3x data size
```

### The Solution with Arrow

```python
# GOOD: 0-1 memory copies
import clickhouse_connect
import polars as pl
import torch

client = clickhouse_connect.get_client(...)
arrow_table = client.query_arrow("SELECT * FROM bars")  # Arrow in DB memory
df = pl.from_arrow(arrow_table)                          # Zero-copy view
X = df.select(features).to_numpy()                       # Single allocation
tensor = torch.from_numpy(X)                             # View (no copy)
# Peak memory: 1.2x data size
```

---

## 3. ClickHouse Integration Patterns

### Pattern A: Arrow Stream (Recommended)

```python
def query_arrow(client, query: str) -> pl.DataFrame:
    """ClickHouse → Arrow → Polars (zero-copy chain)."""
    arrow_table = client.query_arrow(f"{query} FORMAT ArrowStream")
    return pl.from_arrow(arrow_table)

# Usage
df = query_arrow(client, "SELECT * FROM bars WHERE ts >= '2024-01-01'")
```

### Pattern B: Polars Native (Simpler)

```python
# Polars has native ClickHouse support (see pola.rs for version requirements)
df = pl.read_database_uri(
    query="SELECT * FROM bars",
    uri="clickhouse://user:pass@host/db"
)
```

### Pattern C: Parquet Export (Batch Jobs)

```python
# For reproducible batch processing
client.query("SELECT * FROM bars INTO OUTFILE 'data.parquet' FORMAT Parquet")
df = pl.scan_parquet("data.parquet")  # Lazy, memory-mapped
```

---

## 4. PyTorch DataLoader Integration

### Minimal Change Pattern

```python
from torch.utils.data import TensorDataset, DataLoader

# Accept both pandas and polars
def prepare_data(df) -> tuple[torch.Tensor, torch.Tensor]:
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    X = df.select(features).to_numpy()
    y = df.select(target).to_numpy()

    return (
        torch.from_numpy(X).float(),
        torch.from_numpy(y).float()
    )

X, y = prepare_data(df)
dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=32, pin_memory=True)
```

### Custom PolarsDataset (Large Data)

```python
class PolarsDataset(torch.utils.data.Dataset):
    """Memory-efficient dataset from Polars DataFrame."""

    def __init__(self, df: pl.DataFrame, features: list[str], target: str):
        self.arrow = df.to_arrow()  # Arrow backing for zero-copy slicing
        self.features = features
        self.target = target

    def __len__(self) -> int:
        return self.arrow.num_rows

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        row = self.arrow.slice(idx, 1)
        x = torch.tensor([row[f][0].as_py() for f in self.features], dtype=torch.float32)
        y = torch.tensor(row[self.target][0].as_py(), dtype=torch.float32)
        return x, y
```

---

## 5. Lazy Evaluation Patterns

### Pipeline Composition

```python
# Define transformations lazily (no computation yet)
pipeline = (
    pl.scan_parquet("raw_data.parquet")
    .filter(pl.col("timestamp") >= start_date)
    .with_columns([
        (pl.col("close").pct_change()).alias("returns"),
        (pl.col("volume").log()).alias("log_volume"),
    ])
    .select(features + [target])
)

# Execute only when needed
train_df = pipeline.filter(pl.col("timestamp") < split_date).collect()
test_df = pipeline.filter(pl.col("timestamp") >= split_date).collect()
```

### Streaming for Large Files

```python
# Process file in chunks (never loads full file)
def process_large_file(path: str, chunk_size: int = 100_000):
    reader = pl.scan_parquet(path)

    for batch in reader.iter_batches(n_rows=chunk_size):
        # Process each chunk
        features = compute_features(batch)
        yield features.to_numpy()
```

---

## 6. Schema Validation

### Pydantic for Config

```python
from pydantic import BaseModel, field_validator

class FeatureConfig(BaseModel):
    features: list[str]
    target: str
    seq_len: int = 15

    @field_validator("features")
    @classmethod
    def validate_features(cls, v):
        required = {"returns_vs", "momentum_z", "atr_pct"}
        missing = required - set(v)
        if missing:
            raise ValueError(f"Missing required features: {missing}")
        return v
```

### DataFrame Schema Validation

```python
def validate_schema(df: pl.DataFrame, required: list[str], stage: str) -> None:
    """Fail-fast schema validation."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"[{stage}] Missing columns: {missing}\n"
            f"Available: {sorted(df.columns)}"
        )
```

---

## 7. Performance Benchmarks

| Operation      | Pandas | Polars | Speedup |
| -------------- | ------ | ------ | ------- |
| Read CSV (1GB) | 45s    | 4s     | 11x     |
| Filter rows    | 2.1s   | 0.4s   | 5x      |
| Group-by agg   | 3.8s   | 0.3s   | 13x     |
| Sort           | 5.2s   | 0.4s   | 13x     |
| Memory peak    | 10GB   | 2.5GB  | 4x      |

_Benchmark: 50M rows, 20 columns, MacBook M2_

---

## 8. Migration Checklist

### Phase 1: Add Arrow Support

- [ ] Add `polars = "<version>"` to dependencies (see [PyPI](https://pypi.org/project/polars/))
- [ ] Implement `query_arrow()` in data client
- [ ] Verify zero-copy with memory profiler

### Phase 2: Polars at Entry Points

- [ ] Add `pl.from_pandas()` wrapper at trainer entry
- [ ] Update `prepare_sequences()` to accept both types
- [ ] Add schema validation after conversion

### Phase 3: Full Lazy Evaluation

- [ ] Convert file reads to `pl.scan_*`
- [ ] Compose transformations lazily
- [ ] Call `.collect()` only before `.to_numpy()`

---

## 9. Anti-Patterns to Avoid

### DON'T: Mix APIs Unnecessarily

```python
# BAD: Convert back and forth
df_polars = pl.from_pandas(df_pandas)
df_pandas_again = df_polars.to_pandas()  # Why?
```

### DON'T: Collect Too Early

```python
# BAD: Defeats lazy evaluation
df = pl.scan_parquet("data.parquet").collect()  # Full load
filtered = df.filter(...)  # After the fact

# GOOD: Filter before collect
df = pl.scan_parquet("data.parquet").filter(...).collect()
```

### DON'T: Ignore Memory Pressure

```python
# BAD: Loads entire file
df = pl.read_parquet("huge_file.parquet")

# GOOD: Stream in chunks
for batch in pl.scan_parquet("huge_file.parquet").iter_batches():
    process(batch)
```

---

## References

- [Polars User Guide](https://docs.pola.rs/)
- [Polars Migration Guide](https://docs.pola.rs/user-guide/migration/pandas/)
- [Apache Arrow Python](https://arrow.apache.org/docs/python/)
- [ClickHouse Python Client](https://clickhouse.com/docs/integrations/python)
- [PyTorch Data Loading](https://pytorch.org/tutorials/beginner/data_loading_tutorial.html)
- [Polars Preference Hook ADR](/docs/adr/2026-01-22-polars-preference-hook.md)

---

## Troubleshooting

| Issue                       | Cause                            | Solution                                             |
| --------------------------- | -------------------------------- | ---------------------------------------------------- |
| Memory spike during load    | Collecting too early             | Use lazy evaluation, call collect() only when needed |
| Arrow conversion fails      | Unsupported data type            | Check for object columns, convert to native types    |
| ClickHouse connection error | Wrong port or credentials        | Verify host:8123 (HTTP) or host:9000 (native)        |
| Zero-copy not working       | Intermediate pandas conversion   | Remove to_pandas() calls, stay in Arrow/Polars       |
| Polars hook blocking code   | Pandas used without exception    | Add `# polars-exception: reason` comment at file top |
| Slow group-by operations    | Using pandas for large datasets  | Migrate to Polars for 5-10x speedup                  |
| Schema validation failure   | Column names case-sensitive      | Verify exact column names from source                |
| PyTorch DataLoader OOM      | Loading full dataset into memory | Use PolarsDataset with Arrow backing for lazy access |
| Parquet scan performance    | Not using predicate pushdown     | Add filters before collect() for lazy evaluation     |
| Type mismatch in tensor     | Float64 vs Float32 mismatch      | Explicitly cast with .cast(pl.Float32) before numpy  |
