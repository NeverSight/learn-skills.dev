---
name: dataset-management
description: "Use when creating datasets, uploading files, managing schemas, or configuring dataset connections"
---

# Dataset Management Patterns

Reference patterns for creating and managing Dataiku datasets via the Python API.

## Dataset Types

| Type | Use When | Creation Method |
|------|----------|-----------------|
| **Managed** | Output of recipes, stored in a connection (SQL, HDFS, etc.) | `project.new_managed_dataset(name)` |
| **Uploaded** | Importing local files (CSV, Excel, etc.) | `project.create_upload_dataset(name)` or `project.create_dataset(name, "UploadedFiles", ...)` |
| **SQL Table** | Pointing to an existing database table | `project.create_dataset(name, "Snowflake", ...)` |

## Create a Managed Dataset

```python
builder = project.new_managed_dataset("MY_OUTPUT")
builder.with_store_into("connection_name")
ds = builder.create()

# Configure table location (SQL databases)
settings = ds.get_settings()
raw = settings.get_raw()
raw["params"]["schema"] = "MY_SCHEMA"
raw["params"]["table"] = "MY_OUTPUT"
settings.save()
```

## Upload a File

```python
ds = project.create_dataset(
    "my_dataset", "UploadedFiles",
    params={"uploadConnection": "filesystem_managed"}
)

with open("path/to/data.csv", "rb") as f:
    ds.uploaded_add_file(f, "data.csv")

# Auto-detect schema from file contents
settings = ds.autodetect_settings(infer_storage_types=True)
settings.save()
```

**Simpler alternative:** Use `create_upload_dataset` to skip the manual `params` configuration:

```python
ds = project.create_upload_dataset("my_dataset")

with open("path/to/data.csv", "rb") as f:
    ds.uploaded_add_file(f, "data.csv")
```

## Common Column Types

| Dataiku Type | Description |
|--------------|-------------|
| `string` | Text |
| `int` / `bigint` | Integer / Large integer |
| `double` / `float` | Decimal numbers |
| `boolean` | True/False |
| `date` | Date only |

See [references/column-types.md](references/column-types.md) for the full type table.

## Core Schema Operations

### Get Schema
```python
ds = project.get_dataset("my_dataset")
schema = ds.get_settings().get_schema()
for col in schema["columns"]:
    print(f"{col['name']}: {col['type']}")
```

### Set Schema
```python
settings = ds.get_settings()
settings.set_schema({"columns": [
    {"name": "id", "type": "string"},
    {"name": "amount", "type": "double"},
]})
settings.save()
```

### Auto-detect Schema
```python
settings = dataset.autodetect_settings()
settings.save()
```

> **Note:** `autodetect_settings()` is a method on `DSSDataset`, not on `DSSDatasetSettings`. It returns a new settings object with the detected schema applied.

See [references/schema-operations.md](references/schema-operations.md) for join compatibility checks, helper functions, and advanced operations.

## SQL Schema Rule

Output datasets for SQL-based recipes **MUST** have schemas set before building. Without this, Dataiku generates `CREATE TABLE () ...` which fails.

For SQL databases (Snowflake, BigQuery), use **UPPERCASE** column names. Lowercase names get quoted, causing "invalid identifier" errors.

```python
# Normalize column names to uppercase for SQL
raw = settings.get_raw()
for col in raw.get("schema", {}).get("columns", []):
    col["name"] = col["name"].upper()
settings.save()
```

## List Datasets in Project

```python
datasets = project.list_datasets()
for ds in datasets:
    print(f"- {ds['name']} ({ds.get('type', 'unknown')})")
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Schema mismatch | Recipe output doesn't match | Run `autodetect_settings()` |
| Join fails | Key type mismatch | Check types, cast if needed |
| Missing columns | Schema not updated | Rebuild dataset, update schema |
| Parse errors | Wrong type detection | Manually set schema |

## Detailed References

- [references/column-types.md](references/column-types.md) — Full column type table with Python equivalents
- [references/schema-operations.md](references/schema-operations.md) — All schema operations, join compatibility checks, helper functions

