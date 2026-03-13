---
name: data-engineering-storage-remote-access-integrations-iceberg
description: "Apache Iceberg catalog configuration for cloud storage (S3, GCS, Azure). Covers AWS Glue and REST catalogs, table scanning, and append/overwrite operations."
dependsOn: ["@data-engineering-storage-lakehouse", "@data-engineering-storage-authentication"]
---

# Apache Iceberg with Cloud Storage

Configuring PyIceberg catalogs to store Iceberg tables on S3, GCS, or Azure Blob Storage.

## Installation

```bash
pip install pyiceberg[pyarrow,pandas,aws]  # AWS backend
# or
pip install pyiceberg[pyarrow,rest]       # REST catalog
```

## Catalog Configuration

### AWS Glue Catalog

```python
from pyiceberg.catalog import load_catalog

catalog = load_catalog(
    "glue",
    **{
        "type": "glue",
        "s3.region": "us-east-1",
        "s3.access-key-id": "AKIA...",        # Optional: uses env/IAM if omitted
        "s3.secret-access-key": "...",
    }
)
```

Credentials are read from environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) or IAM roles by default. Pass explicitly only when necessary.

### REST Catalog (Tabular, custom REST service)

```python
catalog = load_catalog(
    "rest",
    **{
        "uri": "https://iceberg-catalog.example.com",
        "s3.endpoint": "http://minio:9000",
        "s3.access-key-id": "minioadmin",
        "s3.secret-access-key": "minioadmin",
    }
)
```

### Hive Metastore

```python
catalog = load_catalog(
    "hive",
    **{
        "uri": "thrift://localhost:9083",
        "s3.endpoint": "http://minio:9000",
    }
)
```

### Local Development (No Catalog)

```python
from pyiceberg.catalog import InMemoryCatalog

catalog = InMemoryCatalog("local")
# Tables stored in ~/.pyiceberg/ by default (local file-based catalog)
```

## Table Operations

```python
# Load existing table
table = catalog.load_table("db.my_table")

# Scan with filter pushdown
scan = table.scan(
    row_filter="year = 2024 AND country = 'USA'",
    selected_fields=("id", "value", "timestamp")
)
df = scan.to_pandas()  # or .to_arrow(), .to_polars()

# Append data
import pyarrow as pa
new_data = pa.table({
    "id": [4, 5],
    "value": [400.0, 500.0],
    "year": [2024, 2024]
})
table.append(new_data)

# Overwrite (replaces entire table)
table.overwrite(new_data)
```

## Schema Evolution

```python
# Add column (non-breaking)
with table.update_schema() as update:
    update.add_column("country", StringType(), required=False)

# Upgrade column type (e.g., int → long)
with table.update_schema() as update:
    update.upgrade_column("population", IntegerType(), required=False)
```

## Cloud Storage Authentication

See `@data-engineering-storage-authentication` for:
- AWS: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, IAM roles
- GCS: `GOOGLE_APPLICATION_CREDENTIALS`
- Azure: `AZURE_STORAGE_ACCOUNT`, `AZURE_STORAGE_KEY`

PyIceberg catalogs automatically detect these environment variables. Only provide explicit credentials for local development or non-standard setups.

## Best Practices

1. ✅ **Use a catalog** - Never manage Iceberg tables without catalog metadata
2. ✅ **Leverage partition evolution** - Change partition specs without rewriting data
3. ✅ **Archive old snapshots** - Run `expire_snapshots()` to limit metadata growth
4. ✅ **Schema evolution over schema enforcement** - Iceberg is designed for evolving schemas
5. ⚠️ **Monitor table metadata size** - Large histories slow operations
6. ⚠️ **Don't use local filesystem for production** - Use a shared catalog (Glue, Hive, REST)

## Performance

- ✅ **Predicate pushdown**: Use `row_filter` in `scan()` to skip irrelevant files
- ✅ **Column pruning**: Use `selected_fields` to read only needed columns
- ✅ **Batch operations**: Append multiple records at once for better throughput
- ✅ **PyArrow backend**: Use PyArrow tables (not pandas) for zero-copy operations

## Related Skills

- `@data-engineering-storage-lakehouse/iceberg.md` - Iceberg concepts and detailed API
- `@data-engineering-storage-lakehouse` - Delta Lake vs Iceberg comparison
- `@data-engineering-storage-remote-access/libraries/pyarrow-fs` - PyArrow filesystem for direct S3/GCS access

---

## References

- [PyIceberg Documentation](https://pyiceberg.readthedocs.io/)
- [Apache Iceberg Specification](https://iceberg.apache.org/spec/)
- [Iceberg Catalog Configurations](https://iceberg.apache.org/docs/latest/catalog/)
