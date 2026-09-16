---
name: pandera
description: This skill should be used when the user asks to "validate a DataFrame with pandera", "write a pandera schema", "use pandera DataFrameModel", "add data validation to a pipeline", or needs guidance on pandera best practices for data quality.
---

# Pandera: DataFrame Validation

Pandera is an open-source framework for validating DataFrame-like objects at runtime. Define schemas once and reuse them across pandas, polars, Dask, Modin, PySpark, and Ibis backends.

## Import Convention

Since pandera v0.24.0, use the backend-specific module. Using the top-level `pandera` module produces a `FutureWarning` and will be deprecated in v0.29.0.

```python
import pandera.pandas as pa          # pandas (recommended)
import pandera.polars as pa          # polars
from pandera.typing.pandas import DataFrame, Series, Index
```

## Two Schema Styles

### Object-based API (`DataFrameSchema`)

Suitable for dynamic schema construction or when schemas need to be built programmatically.

```python
import pandas as pd
import pandera.pandas as pa

schema = pa.DataFrameSchema({
    "user_id": pa.Column(int, pa.Check.gt(0)),
    "email": pa.Column(str, pa.Check.str_matches(r"^[^@]+@[^@]+\.[^@]+$")),
    "score": pa.Column(float, [pa.Check.ge(0.0), pa.Check.le(1.0)]),
    "status": pa.Column(str, pa.Check.isin(["active", "inactive", "banned"])),
})

validated = schema.validate(df)
```

### Class-based API (`DataFrameModel`) — preferred

Pydantic-style syntax with type annotations. Produces cleaner, reusable schemas that integrate with `@pa.check_types`.

```python
import pandera.pandas as pa
from pandera.typing.pandas import DataFrame, Series

class UserSchema(pa.DataFrameModel):
    user_id: int = pa.Field(gt=0)
    email: str = pa.Field(str_matches=r"^[^@]+@[^@]+\.[^@]+$")
    score: float = pa.Field(ge=0.0, le=1.0)
    status: str = pa.Field(isin=["active", "inactive", "banned"])

    class Config:
        strict = True       # reject extra columns
        coerce = False      # do not silently cast types

# Validate directly
UserSchema.validate(df)

# Or via typing annotation + decorator
@pa.check_types
def process(df: DataFrame[UserSchema]) -> DataFrame[UserSchema]:
    return df
```

## Checks

### Built-in Checks (prefer these over lambdas)

```python
pa.Check.gt(0)               # greater than
pa.Check.ge(0)               # greater than or equal
pa.Check.lt(100)             # less than
pa.Check.le(100)             # less than or equal
pa.Check.eq("value")         # equal to
pa.Check.ne("value")         # not equal to
pa.Check.isin(["a", "b"])    # membership
pa.Check.notin(["x"])        # exclusion
pa.Check.str_matches(r"^\d+$")  # regex match
pa.Check.in_range(0, 100)    # closed interval
pa.Check.str_startswith("prefix")
pa.Check.str_endswith("suffix")
pa.Check.str_length(1, 255)  # min/max string length
```

### Custom Checks

```python
# Vectorized (default, faster — operates on the whole Series)
pa.Check(lambda s: s.str.len() <= 255)

# Element-wise (scalar input, use only when vectorized is impractical)
pa.Check(lambda x: x > 0, element_wise=True)

# Always add an error message
pa.Check(lambda s: s > 0, error="values must be positive")
```

### DataFrame-level Checks

```python
schema = pa.DataFrameSchema(
    columns={...},
    checks=pa.Check(lambda df: df["end_date"] >= df["start_date"]),
)
```

In `DataFrameModel`, use `@pa.dataframe_check`:

```python
class Schema(pa.DataFrameModel):
    start_date: int
    end_date: int

    @pa.dataframe_check
    @classmethod
    def end_after_start(cls, df: pd.DataFrame) -> pd.Series:
        return df["end_date"] >= df["start_date"]
```

## Nullable and Optional Columns

```python
# Object API: allow nulls in a column
pa.Column(float, nullable=True)

# DataFrameModel: make a column optional (may be absent)
from typing import Optional

class Schema(pa.DataFrameModel):
    required_col: Series[int]
    optional_col: Optional[Series[float]]
```

## Coercion

Enable coercion to cast data to the declared type before validation. Use deliberately — coercion can hide upstream data issues.

```python
# Per-column
pa.Column(int, coerce=True)

# Schema-wide via Config
class Schema(pa.DataFrameModel):
    year: int = pa.Field(gt=2000, coerce=True)

    class Config:
        coerce = True
```

## Lazy Validation — Collect All Errors

By default pandera raises on the first error. Use `lazy=True` to collect all failures before raising, useful for batch reporting.

```python
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as exc:
    print(exc.failure_cases)   # DataFrame of all failures
```

## Decorator Integration

Integrate validation transparently into pipelines using decorators.

```python
# DataFrameModel + check_types (recommended)
@pa.check_types
def transform(df: DataFrame[InputSchema]) -> DataFrame[OutputSchema]:
    return df.assign(revenue=df["units"] * df["price"])

# Object API: check_input / check_output
@pa.check_input(input_schema)
@pa.check_output(output_schema)
def pipeline_step(df):
    return df

# check_io: concisely specify both
@pa.check_io(raw=input_schema, out=output_schema)
def pipeline_step(raw):
    return raw
```

Decorators work on sync/async functions, methods, class methods, and static methods.

## Schema Inheritance

Build specialized schemas from a base to avoid repetition.

```python
class BaseEvent(pa.DataFrameModel):
    event_id: str
    timestamp: int = pa.Field(gt=0)

class ClickEvent(BaseEvent):
    url: str
    user_agent: str

    class Config:
        strict = True
```

## Schema Persistence (YAML / Script)

Serialize and reload schemas to keep validation reproducible.

```python
import pandera.io

# Save
pandera.io.to_yaml(schema, "./schema.yaml")

# Load
schema = pandera.io.from_yaml("./schema.yaml")

# Generate Python script
pandera.io.to_script(schema, "./schema_definition.py")
```

## Schema Inference (Prototyping Only)

Infer a schema from existing data to bootstrap development. Always review and tighten the generated schema before using in production.

```python
import pandera.pandas as pa

inferred = pa.infer_schema(df)
print(inferred.to_script())   # inspect then copy-edit
```

## Dropping Invalid Rows

Use `drop_invalid_rows=True` on `DataFrameSchema` to filter out failing rows instead of raising an error. Supported on pandas and polars.

```python
schema = pa.DataFrameSchema(
    {"score": pa.Column(float, pa.Check.ge(0))},
    drop_invalid_rows=True,
)
cleaned = schema.validate(df_with_bad_rows)
```

## Error Handling

```python
from pandera.errors import SchemaError, SchemaErrors

# Single error (eager validation)
try:
    schema.validate(df)
except SchemaError as exc:
    print(exc.failure_cases)   # Series/DataFrame of failures

# Multiple errors (lazy validation)
try:
    schema.validate(df, lazy=True)
except SchemaErrors as exc:
    # Structured dict with SCHEMA and DATA keys
    print(exc.error_counts)
    print(exc.failure_cases)
```

## Key Configuration Options (`Config`)

| Option | Type | Effect |
|---|---|---|
| `strict` | `bool` | Raise if extra columns present |
| `coerce` | `bool` | Cast columns to declared dtypes |
| `ordered` | `bool` | Require columns in declared order |
| `name` | `str` | Schema name shown in error messages |
| `add_missing_columns` | `bool` | Insert columns with default values |

## Best Practices

- **Use `DataFrameModel`** over `DataFrameSchema` for new code — cleaner syntax, inheritance, and type-annotation integration.
- **Prefer `strict=True`** to catch unexpected extra columns early.
- **Use built-in checks** (`Check.gt`, `Check.isin`, etc.) over custom lambdas where possible — they produce better error messages.
- **Write vectorized checks** (`element_wise=False`, the default) for performance; only use `element_wise=True` when the logic is truly scalar.
- **Always add `error=` messages** to custom `Check` objects to improve debuggability.
- **Use lazy validation** in pipelines that process large batches so all failures surface in one pass.
- **Never rely on inferred schemas in production** — always explicitly define constraints.
- **Use `coerce=True` deliberately** — set at the column level to limit scope; avoid schema-wide coercion unless certain.
- **Prefer `raise_warning=True`** only for non-critical informational checks (e.g., normality tests), not for data integrity constraints.

## Additional Resources

- **`references/checks-and-validation.md`** — Built-in check catalog, groupby checks, wide checks, hypothesis testing
- **`references/dataframe-models.md`** — Field spec, schema inheritance, MultiIndex, aliases, parsers, Polars usage
