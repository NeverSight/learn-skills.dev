---
name: deephaven-core-query-writing
description: Work with Deephaven for real-time data processing. Use for table queries, joins, aggregations, time-series, UI dashboards, plotting (dx), Kafka streaming, Iceberg integration. Triggers on mentions of Deephaven, tables or queries, and related concepts.
license: Apache-2.0
metadata:
  author: Deephaven Data Labs
  version: "0.1.0"
---

# Deephaven Development

## Mandatory Reference Reading

**BEFORE writing ANY code involving these topics, you MUST read the reference file:**

| Topic | Reference File | Read BEFORE writing code that... |
|-------|----------------|----------------------------------|
| Joins | `references/joins.md` | uses natural_join, aj, raj, exact_join, range_join |
| Aggregations | `references/aggregations.md` | uses agg_by, sum_by, avg_by, count_by, etc. |
| Update-by | `references/updateby.md` | uses rolling ops, cumulative ops, EMAs, forward fill |
| Time | `references/time-operations.md` | parses, bins, or manipulates timestamps |
| Kafka | `references/kafka.md` | consumes from or produces to Kafka |
| Iceberg | `references/iceberg.md` | reads/writes Iceberg tables |
| UI | `references/ui.md` | creates dashboards, components, or uses hooks |
| Plotting | `references/plotting.md` | creates charts or visualizations with dx |
| CSV | `references/csv.md` | imports/exports CSV files, fixes column types, parses dates from CSVs |
| Sitemap | `references/sitemap.md` | needs to look up additional documentation URLs |

If you read Aggregations you must also read update-by, as they often go hand-in-hand.

**Do NOT guess or rely on memory.** Deephaven APIs have specific patterns that differ from similar libraries. Reading the reference ensures correct usage.

**When debugging errors:**
1. Re-read the relevant reference file for the operation that failed
2. Compare your code against the reference examples
3. Check for common mistakes noted in the reference

**YOU NEVER ADD PRINT STATEMENTS TO PRINT TABLES, DO NOT CONVERT TO PANDAS JUST TO PRINT**

**Fetch online docs when needed:**
- Read the sitemap reference if you need to look up documentation URLs for specific operations or classes.

---

## Table Operations

### Core Principles

**Do as much in-engine as possible.** Deephaven's Java engine is highly optimized. Prefer built-in operations over Python UDFs.

**Avoid Python UDFs in query strings.** Each Python call crosses the Python-Java boundary (~30x slower). Use built-in functions from `java.lang.Math`, time functions, and auto-imported query language functions instead.

**Use the right column operation:**
- `select`/`update`: Materialize in RAM - use for expensive formulas accessed frequently
- `view`/`update_view`: On-demand calculation - use for fast formulas or infrequent access
- `lazy_update`: Cache results - use for repeated values

**Filter early.** Place partition/grouping column filters first in `where()` to exclude data early.

### Table Creation

```python
from deephaven import empty_table, new_table, ring_table, time_table
from deephaven.column import double_col, string_col

# Empty table with formulas
t = empty_table(100).update(["X = i", "Y = X * 2"])

# New table from columns
t = new_table(
    [string_col("Sym", ["AAPL", "GOOG"]), double_col("Price", [150.0, 140.0])]
)

# Ticking time table (real-time)
t = time_table("PT1s")  # ticks every second

# Ring table (bounded size, keeps last N rows)
source = time_table("PT1s")
t = ring_table(source, capacity=1000)
```

### Table Types

| Type | Memory | Use Case |
|------|--------|----------|
| Static | Fixed | Imported files, snapshots |
| Append-only | Unbounded | Complete history from streams |
| Blink | Bounded | Current cycle only (Kafka default) |
| Ring | Bounded | Last N rows only |

### Extracting Scalar Values

`print(table)` only shows the object reference. To get actual values for a specific cell:

```python
from deephaven import empty_table

table = empty_table(1).update(["ColName = 42.5"])

# Get a scalar from a 1-row result table
value = table.j_table.getColumnSource("ColName").get(
    table.j_table.getRowSet().firstRowKey()
)
print(f"Result: {value:,.2f}")
```

### Column Operations

```python
from deephaven import empty_table

t = empty_table(100).update(["A = i", "B = i * 2", "OldName = i", "Unwanted = i"])

# select - new table with specified columns (materialized)
t.select(["A", "B", "C = A + B"])

# view - formula table (calculated on access)
t.view(["A", "B", "C = A + B"])

# update - add columns to existing (materialized)
t.update(["C = A + B", "D = sqrt(C)"])

# update_view - add columns (calculated on access)
t.update_view(["C = A + B"])

# drop_columns - remove columns
t.drop_columns(["Unwanted"])

# rename_columns - rename columns
t.rename_columns(["NewName = OldName"])
```

### Filtering

```python
import datetime

from deephaven import new_table
from deephaven.column import datetime_col, double_col, string_col

t = new_table(
    [
        string_col("Sym", ["AAPL", "GOOG", "MSFT", "AMZN"]),
        double_col("Price", [150.0, 140.0, 200.0, 50.0]),
        string_col("Description", ["no error", "has error", "fine", "ok"]),
        datetime_col(
            "Timestamp",
            [
                datetime.datetime(2024, 6, 1, tzinfo=datetime.timezone.utc),
                datetime.datetime(2024, 6, 2, tzinfo=datetime.timezone.utc),
                datetime.datetime(2024, 6, 3, tzinfo=datetime.timezone.utc),
                datetime.datetime(2024, 6, 4, tzinfo=datetime.timezone.utc),
            ],
        ),
    ]
)

filter_table = new_table([string_col("Sym", ["AAPL", "GOOG"])])

# Basic where
t.where("Price > 100")
t.where(["Sym = `AAPL`", "Price > 100"])  # AND logic

# String matching (Java String methods)
t.where("Sym.startsWith(`A`)")
t.where("Description.contains(`error`)")

# Set membership (fast)
t.where("Sym in `AAPL`, `GOOG`, `MSFT`")
t.where_in(filter_table, "Sym")
t.where_not_in(filter_table, "Sym")

# Time filtering
t.where("Timestamp > parseInstant(`2024-01-01T00:00:00 America/New_York`)")
```

### Joins Overview

**Read `references/joins.md` before using joins.**

| Join | Use Case | Match Type |
|------|----------|------------|
| `natural_join` | Add columns from right, NULL if no match | Exact |
| `exact_join` | Add columns, error if not exactly one match | Exact |
| `join` | All matching combinations | Exact |
| `aj` | As-of join: find closest <= timestamp | Time-series |
| `raj` | Reverse as-of: find closest >= timestamp | Time-series |
| `range_join` | Match within ranges, aggregate results | Range |

### Aggregations Overview

**Read `references/aggregations.md` before using aggregations.**

**Dedicated (single operation):**
```python
from deephaven import new_table
from deephaven.column import double_col, int_col, string_col

t = new_table(
    [
        string_col("Sym", ["AAPL", "AAPL", "GOOG", "GOOG"]),
        double_col("Price", [150.0, 152.0, 140.0, 142.0]),
        int_col("Qty", [100, 200, 150, 250]),
    ]
)

t.sum_by("Sym")  # Sum all numeric columns
t.avg_by("Sym")  # Average
t.count_by("Count", "Sym")  # Count rows
t.first_by("Sym")  # First row per group
t.last_by("Sym")  # Last row per group
```

**Combined (multiple operations):**
```python
from deephaven import agg, new_table
from deephaven.column import double_col, int_col, string_col

t = new_table(
    [
        string_col("Sym", ["AAPL", "AAPL", "GOOG", "GOOG"]),
        double_col("Price", [150.0, 152.0, 140.0, 142.0]),
        int_col("Qty", [100, 200, 150, 250]),
    ]
)

t.agg_by(
    [
        agg.avg(cols=["AvgPrice = Price"]),
        agg.sum_(cols=["TotalQty = Qty"]),
        agg.count_(col="Count"),
    ],
    by=["Sym"],
)
```

### Query String Syntax

**Literals:**
- Boolean: `true`, `false` (lowercase)
- Int: `42`, Long: `42L`, Double: `3.14` (underscores like `1_000L` are NOT supported)
- String: backticks `` `hello` ``
- DateTime: `parseInstant(\`2024-01-01T12:00:00 America/New_York\`)` (short aliases like `NY` do NOT work)
- Duration: `'PT1h30m'`, Period: `'P1y2m3d'`

**Built-in variables:**
- `i` - row index (0-based)
- `ii` / `k` - row key (stable identifier)

**Ternary operator:**
```python
from deephaven import empty_table

t = empty_table(10).update(["Price = i * 25.0"])
t.update(["Category = Price > 100 ? `High` : `Low`"])
```

**Null handling:**
```python
from deephaven import empty_table

t = empty_table(10).update(["Value = i % 2 == 0 ? NULL_INT : i"])
t.update(["Safe = isNull(Value) ? 0 : Value"])
```

### Data Import/Export

```python
from deephaven import empty_table, read_csv, write_csv
from deephaven.parquet import read, write

t = empty_table(10).update(["X = i", "Y = X * 2"])

# CSV
write_csv(t, "/tmp/output.csv")
t_csv = read_csv("/tmp/output.csv")

# Parquet
write(t, "/tmp/output.parquet")
t_parquet = read("/tmp/output.parquet")
```

---

## Reference Documentation

| Reference | Content |
|-----------|---------|
| `references/joins.md` | All 6 join types with examples, match syntax, performance tips |
| `references/aggregations.md` | Dedicated and combined aggregations, 20+ aggregators, common patterns |
| `references/updateby.md` | Rolling/cumulative ops, EMAs, MACD/Bollinger patterns |
| `references/time-operations.md` | Time literals, parsing, binning, calendars, timezone conversion |
| `references/kafka.md` | Kafka consumption/production, table types, key/value specs |
| `references/iceberg.md` | Catalog types, reading/writing tables, partitioned writes |
| `references/ui.md` | Dashboard structure, hooks, components, ui.table, styling |
| `references/plotting.md` | Deephaven Express (dx), all plot types, subplots, interactivity |
| `references/csv.md` | CSV import/export, column types, renaming, date parsing, messy files |
| `references/sitemap.md` | Full documentation URL lookup |
