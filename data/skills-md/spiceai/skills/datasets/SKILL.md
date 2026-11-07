---
name: datasets
description: Connect Spice to data sources and query across them with federated SQL — including datasets, catalogs, views, and writes. Use this skill whenever the user wants to set up federated queries across multiple sources, create views, configure catalogs (Unity Catalog, Databricks, Iceberg), write data with INSERT INTO, or understand how Spice's query federation works. This skill focuses on the federation layer — cross-source joins, views, catalogs, and data writes. For configuring individual data source connectors (PostgreSQL params, S3 file formats, etc.), see connectors.
---

# Connect to Data Sources

Spice federates SQL queries across 30+ data sources without ETL. Connect databases, data lakes, warehouses, and APIs, then query across them with standard SQL.

## Version Compatibility

Written for **Spice v2.4.x** (checked against v2.4.0-rc.2). Check the user's runtime version before recommending configuration:

- **Find it**: `spice version` (CLI and runtime), `spiced --version`, or the image tag (`spiceai/spiceai:<tag>`, Helm `image.tag`). Not the runtime version: `version: v2` in `spicepod.yaml` (manifest schema) or SQL `version()` (DataFusion).
- **Markers**: unmarked content applies to v2.0.0 and later. Later additions are marked `(vX.Y.Z+)`; changes are marked **Removed**, **Deprecated**, **Changed**, or **Breaking in vX.Y.Z**.
- **Older runtime**: don't recommend a newer feature — offer `spice upgrade` or an alternative — and read that release line's docs, e.g. `https://spiceai.org/docs/v2.2/...` (`/docs/next/` tracks trunk, not a release). On v1.x, use the [v1.11 docs](https://spiceai.org/docs/v1.11) and the [v2.0 upgrade guide](https://spiceai.org/releases/v2.0-stable#upgrade-guide-from-v1x).
- **Newer runtime**: check the [release notes](https://spiceai.org/releases) for changes after v2.4.0-rc.2.

| Old | Change | Use instead |
| --- | --- | --- |
| `schema_inference` dataset field | Removed in v2.2.0 (fails to load) | Delete it — inference is always on |
| `acceleration.ready_state` (datasets and views) | Deprecated in v2.3.0 | `ready_state` on the dataset or view |
| Durable write-back with `mode: memory`, retention, a multi-column key, or `DELETE`/`TRUNCATE` | Breaking in v2.3.0 (rejected) | `mode: file`, a single-column `primary_key`, no retention, writes in one `BEGIN; …; COMMIT;` |
| Metadata columns `location`, `last_modified`, `size` | Renamed in v2.0.0 | `_location`, `_last_modified`, `_size` |
| `pg_replication_temporary_slot` | Deprecated in v2.2.0 (ignored) | Delete it |
| ScyllaDB in the default build | Breaking in v2.3.0 | `--features scylladb` build, or Spice.ai Enterprise |

## Dataset interfaces

Keep dataset names consistent between `spicepod.yaml`, SQL table names, CLI `spice datasets`, and
runtime `GET /v1/datasets`. Use CLI help for dataset creation or inspection commands available in
the installed release. Use `spice refresh <dataset>` or
`POST /v1/datasets/{name}/acceleration/refresh` for an explicitly requested acceleration refresh.
Use `connectors` for source-specific parameters, `sql` to query the result, and `sdk` for application
code. A dataset definition is runtime configuration; Cloud project lifecycle belongs to `cloud`.

## How Federation Works

Configure datasets pointing to different sources. Spice's query planner (built on Apache DataFusion) optimizes and routes queries with filter pushdown and column projection:

```yaml
datasets:
  - from: postgres:customers
    name: customers
    params:
      pg_host: db.example.com
      pg_user: ${ secrets:PG_USER }
  - from: s3://bucket/orders/
    name: orders
    params:
      file_format: parquet
  - from: snowflake:ANALYTICS.PUBLIC.SALES
    name: sales
```

```sql
-- Query across all three sources in one statement
SELECT c.name, o.order_total, s.region
FROM customers c
  JOIN orders o ON c.id = o.customer_id
  JOIN sales s ON o.id = s.order_id
WHERE s.region = 'EMEA';
```

## Dataset Configuration

```yaml
datasets:
  - from: <connector>:<identifier>
    name: <dataset_name>
    params:
      # connector-specific parameters
    acceleration:
      enabled: true # optional: materialize locally (see acceleration)
```

## Supported Connectors

### Databases

| Connector     | From Format             | Status                        |
| ------------- | ----------------------- | ----------------------------- |
| PostgreSQL    | `postgres:schema.table` | Stable (native WAL CDC; also Amazon Redshift) |
| MySQL         | `mysql:schema.table`    | Stable (native binlog CDC v2.2.0+) |
| DuckDB        | `duckdb:database.schema.table` | Stable                 |
| DynamoDB      | `dynamodb:table`        | Stable (with Streams)         |
| Azure Cosmos DB | `cosmosdb:database.container` | Release Candidate      |
| MS SQL Server | `mssql:database.schema.table` | Beta                    |
| MongoDB       | `mongodb:collection`    | Alpha (Change Streams)        |
| ClickHouse    | `clickhouse:db.table`   | Alpha                         |
| Oracle        | `oracle:schema.table`   | Alpha                         |
| ScyllaDB      | `scylladb:table`        | Alpha (Spice.ai Enterprise; out of default OSS build in v2.3.0) |

### Data Warehouses

| Connector               | From Format                       | Status            |
| ----------------------- | --------------------------------- | ----------------- |
| Databricks              | `databricks:catalog.schema.table` | Stable with `mode: delta_lake`; Beta with `mode: spark_connect` (the default) |
| Snowflake               | `snowflake:DB.SCHEMA.TABLE`       | Release Candidate |
| Spark                   | `spark:db.table`                  | Beta              |

### Data Lakes & Object Storage

| Connector    | From Format                  | Status            |
| ------------ | ---------------------------- | ----------------- |
| S3           | `s3://bucket/path/`          | Stable            |
| Delta Lake   | `delta_lake:/path/to/delta/` | Stable            |
| File (local) | `file:./path/to/data`        | Stable            |
| Iceberg      | `iceberg:https://<catalog>/v1/namespaces/<ns>/tables/<table>` | Release Candidate (read+write) |
| DuckLake     | `ducklake:table`             | Beta              |
| Azure BlobFS | `abfs://container/path/`     | Alpha             |
| Google Cloud Storage | `gs://bucket/path/`  | Alpha             |
| AWS Glue     | `glue:db.table`              | Alpha             |

### Other Sources

| Connector    | From Format                           | Status            |
| ------------ | ------------------------------------- | ----------------- |
| Spice.ai     | `spice.ai/<org>/<app>/datasets/<name>` | Stable           |
| Dremio       | `dremio:source.table`                 | Stable            |
| GitHub       | `github:github.com/owner/repo/issues` | Stable            |
| Git          | `git:https://host/owner/repo.git@<ref>` | Release Candidate |
| GraphQL      | `graphql:https://host/graphql`        | Release Candidate |
| ADBC         | `adbc:table`                          | Release Candidate |
| FlightSQL    | `flightsql:catalog.schema.table`      | Beta              |
| ODBC         | `odbc:path.to.table`                  | Beta (Spice.ai Enterprise) |
| SharePoint   | `sharepoint:drive:<name>/path:/<folder>` | Beta           |
| FTP/SFTP     | `sftp://host/path/`                   | Alpha             |
| HTTP/HTTPS   | `https://url/path/data.csv`           | Alpha             |
| Kafka        | `kafka:topic`                         | Alpha             |
| Debezium CDC | `debezium:topic` (Kafka), `cdc:name` (HTTP push, v2.2.0+) | Alpha |
| Elasticsearch | `elasticsearch:index`                | Alpha (Spice.ai Enterprise) |
| IMAP         | `imap:<email_address>`                | Alpha             |
| localpod     | `localpod:dataset`                    | Alpha             |
| SMB          | `smb://host/share/path/`              | Alpha             |
| NFS          | `nfs://host/path/`                    | Alpha (Spice.ai Enterprise) |

Spice.ai Enterprise connectors are not in the default OSS build ([Distributions](https://spiceai.org/docs/reference/distributions)).

## Common Examples

### PostgreSQL

```yaml
datasets:
  - from: postgres:public.users
    name: users
    params:
      pg_host: localhost
      pg_port: 5432
      pg_user: ${ env:PG_USER }
      pg_pass: ${ env:PG_PASS }
    acceleration:
      enabled: true
```

For the per-connector `from:` and `params:` reference — S3, GitHub (v2.3.0 review/release/repo
tables), local files, MySQL CDC, HTTP APIs, BigQuery-via-ADBC, Databricks (Unity Catalog streaming
tables and views, v2.3.0+), and the rest — see connectors.

## File Formats

File-based connectors (S3, ABFS, GCS, HTTP/S, FTP/SFTP, SMB, NFS, local `file:`) support:

| Format         | `file_format` | Status | Type       |
| -------------- | ------------- | ------ | ---------- |
| Apache Parquet | `parquet`     | Stable | Structured |
| CSV            | `csv`         | Stable | Structured |
| JSON           | `json`        | Stable | Structured |
| Markdown       | `md`          | Stable | Document   |
| Text           | `txt`         | Stable | Document   |
| PDF            | `pdf`         | Beta   | Document   |
| Microsoft Word | `docx`        | Alpha  | Document   |
| Microsoft Excel | `xlsx`       | Alpha  | Document   |
| PowerPoint     | `pptx`        | Alpha  | Document   |

Document files produce one row per file with `location` and `content` columns (not `_location`):

```yaml
datasets:
  - from: file:docs/decisions/
    name: my_documents
    params:
      file_format: md
```

### Hive Partitioning

```yaml
datasets:
  - from: s3://bucket/data/
    name: partitioned_data
    params:
      file_format: parquet
      hive_partitioning_enabled: true
```

```sql
SELECT * FROM partitioned_data WHERE year = '2024' AND month = '01';
```

## Dataset Naming

- `name: foo` → `spice.public.foo`
- `name: myschema.foo` → `spice.myschema.foo`
- Use `.` to organize datasets into schemas

## Catalogs

Catalog connectors expose external data catalogs, preserving the source schema hierarchy. Tables are accessed as `<catalog>.<schema>.<table>`.

> **Note:** Only the `pg` catalog can be accelerated as a whole (v2.2.0+, Alpha). On every other
> catalog an `acceleration` block is a configuration error, not a silent no-op — accelerate an
> individual table by defining it as a dataset instead.

```yaml
catalogs:
  - from: <connector>[:<catalog_path>]
    name: <catalog_name>
    params:
      # connector-specific parameters
    include:
      - 'schema.*' # optional: filter with glob patterns
```

### Supported Catalogs

| Connector       | `from`                                                          | Status |
| --------------- | --------------------------------------------------------------- | ------ |
| Unity Catalog   | `unity_catalog:https://<host>/api/2.1/unity-catalog/catalogs/<catalog>` | Stable |
| Databricks      | `databricks:<catalog>`                                          | Beta   |
| Iceberg         | `iceberg:https://<host>/v1/namespaces/<namespace>`              | Beta   |
| Spice.ai        | `spice.ai/<org>/<app>`                                          | Beta   |
| DuckLake        | `ducklake:<metadata>` (e.g. `ducklake:s3://bucket/metadata.ducklake`) | Beta |
| PostgreSQL      | `pg`                                                            | Beta   |
| AWS Glue        | `glue` or `glue:<catalog_id>`                                   | Alpha  |
| Snowflake       | `snowflake:<DATABASE>`                                          | Alpha  |
| MySQL           | `mysql`                                                         | Alpha  |
| MS SQL Server   | `mssql`                                                         | Alpha  |
| ADBC            | `adbc`                                                          | Alpha  |
| Oracle          | `oracle`                                                        | Alpha  |

### Catalog Example

```yaml
catalogs:
  # The catalog URL in `from` is required; there is no separate endpoint parameter
  - from: unity_catalog:https://my-workspace.cloud.databricks.com/api/2.1/unity-catalog/catalogs/main
    name: unity
    params:
      unity_catalog_token: ${ secrets:UC_TOKEN }
      unity_catalog_credential_vending: enabled # v2.1.0+; or unity_catalog_aws_* etc. in dataset_params
    include:
      - 'my_schema.*'
```

```sql
SELECT * FROM unity.my_schema.customers LIMIT 10;
```

### PostgreSQL Catalog CDC (v2.2.0+, Alpha)

One block bootstraps and CDC-accelerates every table the `include` patterns match. All tables share
one replication slot and publication derived from the catalog `name`, so the WAL is decoded once.

```yaml
catalogs:
  - from: pg
    name: my_pg
    include:
      - 'public.*'
    acceleration:
      engine: cayenne # optional; cayenne is the only supported engine
      refresh_mode: changes # required — no catalog-level default, and `full` is unsupported
    params:
      pg_connection_string: postgresql://${ secrets:PG_USER }:${ secrets:PG_PASS }@localhost:5432/mydb
```

Needs `wal_level = logical`, the replication privilege, and a free slot if the catalog's slot is new
(all checked at load). Tables without a usable replica identity are skipped with a warning. Alpha:
configuration may change, and v2.2.0 notes a durable catalog acceleration can come back empty after
a restart.

## Views

Views are virtual tables defined by SQL queries — useful for pre-aggregations, transformations, and simplified access:

```yaml
views:
  - name: daily_sales
    sql: |
      SELECT CAST(created_at AS DATE) as day, SUM(amount) as total, COUNT(*) as orders
      FROM orders
      GROUP BY CAST(created_at AS DATE)

  - name: order_details
    sql: |
      SELECT o.id, c.name as customer, p.name as product, o.quantity
      FROM orders o
      JOIN customers c ON o.customer_id = c.id
      JOIN products p ON o.product_id = p.id
```

Views can be accelerated:

```yaml
views:
  - name: rankings
    sql: |
      SELECT product_id, SUM(quantity) as total_sold
      FROM orders GROUP BY product_id ORDER BY total_sold DESC LIMIT 100
    acceleration:
      enabled: true
      refresh_check_interval: 1h
```

Views are read-only and queried like regular tables: `SELECT * FROM daily_sales`.

## Writing Data

Set `access: read_write` on a dataset (or catalog) from a write-capable connector:

| Connector                                 | Statements                                               |
| ----------------------------------------- | -------------------------------------------------------- |
| PostgreSQL, Snowflake, DynamoDB           | `INSERT`, `UPDATE`, `DELETE`                             |
| Iceberg, AWS Glue (incl. Amazon S3 Tables) | `INSERT INTO` (append-only); `iceberg:` also `DELETE FROM` on v2+ tables |
| DuckLake                                  | `INSERT INTO` (DDL via the catalog with `access: read_write_create`) |

```yaml
datasets:
  - from: iceberg:https://catalog.example.com/v1/namespaces/sales/tables/transactions
    name: transactions
    access: read_write # required for writes
```

```sql
INSERT INTO transactions SELECT * FROM staging_transactions;
```

Accelerated datasets route writes by `acceleration.write_mode`. Durable write-back
(`write_mode: write_back`, Cayenne over PostgreSQL) is covered in acceleration — **Breaking in
v2.3.0**, it rejects unsafe configurations at load and rejects `DELETE`, `TRUNCATE`, and `MERGE`.

### Deleting from Iceberg

`DELETE FROM` needs an Iceberg v2+ table and is written as an **equality delete file** — "remove rows
whose key columns equal these values". That key cannot carry float/double columns (`NaN` is not equal
to itself), nested columns, or any column without a Parquet field ID. A `WHERE` clause reading a
column outside the key is not expressible exactly, so rather than delete the row beside the one
selected, Spice **refuses** the statement and names the offending column (**Changed in v2.3.0** —
earlier builds ran it and could delete rows that did not match). Also refused: a subquery predicate
(run it first and delete by the values it returns), a volatile predicate such as `random()`, and any
`WHERE` on a table with no keyable column. `DELETE FROM t` with no condition and a key-columns-only
`WHERE` both work; `UPDATE` is not supported.

## Referencing Secrets

Use `${ store_name:KEY }` syntax in params. See secrets for full configuration:

```yaml
params:
  pg_user: ${ env:PG_USER }
  pg_pass: ${ secrets:PG_PASSWORD }
```

## Verify

Check each source on its own before debugging a federated query, view, or write:

```bash
curl -s http://127.0.0.1:8090/v1/ready                  # "ready" once every component has loaded
curl -s 'http://127.0.0.1:8090/v1/datasets?status=true' # every dataset "status": "Ready"
curl -s -X POST http://127.0.0.1:8090/v1/sql -H 'Content-Type: text/plain' -d 'SELECT * FROM orders LIMIT 1'
```

Then run the join or view. A dataset with `"status": "Error"` reports why in `error_message`.
setup's `spice-local.sh verify <dir> --dataset orders --dataset customers` checks several at once.

## Documentation

- [Data Connectors](https://spiceai.org/docs/components/data-connectors)
- [Datasets Reference](https://spiceai.org/docs/reference/spicepod/datasets)
- [Catalogs](https://spiceai.org/docs/components/catalogs)
- [Views](https://spiceai.org/docs/features/views)
- [Query Federation](https://spiceai.org/docs/features/query-federation)
- [Data Ingestion / Writes](https://spiceai.org/docs/features/data-ingestion)
