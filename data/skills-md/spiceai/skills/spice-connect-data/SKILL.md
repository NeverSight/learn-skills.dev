---
name: spice-connect-data
description: Connect Spice to data sources and query across them with federated SQL. Use when connecting to databases (Postgres, MySQL, DynamoDB), data lakes (S3, Delta Lake, Iceberg), warehouses (Snowflake, Databricks), files, APIs, or catalogs; configuring datasets; creating views; writing data; or setting up cross-source queries.
---

# Connect to Data Sources

Spice federates SQL queries across 30+ data sources without ETL. Connect databases, data lakes, warehouses, and APIs, then query across them with standard SQL.

## How Federation Works

Configure datasets pointing to different sources. Spice's query planner (built on Apache DataFusion) optimizes and routes queries with filter pushdown and column projection:

```yaml
datasets:
  - from: postgres:customers
    name: customers
    params:
      pg_host: db.example.com
      pg_user: ${secrets:PG_USER}
  - from: s3://bucket/orders/
    name: orders
    params:
      file_format: parquet
  - from: snowflake:analytics.sales
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
      enabled: true # optional: materialize locally (see spice-acceleration)
```

## Supported Connectors

### Databases

| Connector     | From Format             | Status                        |
| ------------- | ----------------------- | ----------------------------- |
| PostgreSQL    | `postgres:schema.table` | Stable (also Amazon Redshift) |
| MySQL         | `mysql:schema.table`    | Stable                        |
| DuckDB        | `duckdb:database.table` | Stable                        |
| MS SQL Server | `mssql:db.table`        | Beta                          |
| DynamoDB      | `dynamodb:table`        | Release Candidate             |
| MongoDB       | `mongodb:collection`    | Alpha                         |
| ClickHouse    | `clickhouse:db.table`   | Alpha                         |

### Data Warehouses

| Connector               | From Format                       | Status |
| ----------------------- | --------------------------------- | ------ |
| Snowflake               | `snowflake:db.schema.table`       | Beta   |
| Databricks (Delta Lake) | `databricks:catalog.schema.table` | Stable |
| Spark                   | `spark:db.table`                  | Beta   |

### Data Lakes & Object Storage

| Connector    | From Format                  | Status |
| ------------ | ---------------------------- | ------ |
| S3           | `s3://bucket/path/`          | Stable |
| Delta Lake   | `delta_lake:/path/to/delta/` | Stable |
| Iceberg      | `iceberg:table`              | Beta   |
| Azure BlobFS | `abfs://container/path/`     | Alpha  |
| File (local) | `file:./path/to/data`        | Stable |

### Other Sources

| Connector    | From Format                           | Status            |
| ------------ | ------------------------------------- | ----------------- |
| Spice.ai     | `spice.ai:path/to/dataset`            | Stable            |
| Dremio       | `dremio:source.table`                 | Stable            |
| GitHub       | `github:github.com/owner/repo/issues` | Stable            |
| GraphQL      | `graphql:endpoint`                    | Release Candidate |
| FlightSQL    | `flightsql:query`                     | Beta              |
| ODBC         | `odbc:connection`                     | Beta              |
| FTP/SFTP     | `sftp://host/path/`                   | Alpha             |
| HTTP/HTTPS   | `https://url/path/data.csv`           | Alpha             |
| Kafka        | `kafka:topic`                         | Alpha             |
| Debezium CDC | `debezium:topic`                      | Alpha             |
| SharePoint   | `sharepoint:site/path`                | Alpha             |
| IMAP         | `imap:mailbox`                        | Alpha             |

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

### S3 with Parquet

```yaml
datasets:
  - from: s3://my-bucket/data/sales/
    name: sales
    params:
      file_format: parquet
      s3_region: us-east-1
    acceleration:
      enabled: true
      engine: duckdb
```

### GitHub Issues

```yaml
datasets:
  - from: github:github.com/spiceai/spiceai/issues
    name: spiceai.issues
    params:
      github_token: ${ secrets:GITHUB_TOKEN }
    acceleration:
      enabled: true
      refresh_mode: append
      refresh_check_interval: 24h
      refresh_data_window: 14d
```

### Local File

```yaml
datasets:
  - from: file:./data/sales.parquet
    name: sales
```

## File Formats

Connectors reading from object stores (S3, ABFS) or network storage (FTP, SFTP) support:

| Format         | `file_format` | Type       |
| -------------- | ------------- | ---------- |
| Apache Parquet | `parquet`     | Structured |
| CSV            | `csv`         | Structured |
| Markdown       | `md`          | Document   |
| Text           | `txt`         | Document   |
| PDF            | `pdf`         | Document   |
| Microsoft Word | `docx`        | Document   |

Document files produce a table with `location` and `content` columns:

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

> **Note:** Acceleration is not supported for catalog tables. Use datasets for accelerated access.

```yaml
catalogs:
  - from: <connector>
    name: <catalog_name>
    params:
      # connector-specific parameters
    include:
      - 'schema.*' # optional: filter with glob patterns
```

### Supported Catalogs

| Connector     | From Value      | Status |
| ------------- | --------------- | ------ |
| Unity Catalog | `unity_catalog` | Stable |
| Databricks    | `databricks`    | Beta   |
| Iceberg       | `iceberg`       | Beta   |
| Spice.ai      | `spice.ai`      | Beta   |
| AWS Glue      | `glue`          | Alpha  |

### Catalog Example

```yaml
catalogs:
  - from: unity_catalog
    name: unity
    params:
      unity_catalog_endpoint: https://my-workspace.cloud.databricks.com
      databricks_token: ${ secrets:DATABRICKS_TOKEN }
    include:
      - 'my_schema.*'
```

```sql
SELECT * FROM unity.my_schema.customers LIMIT 10;
```

## Views

Views are virtual tables defined by SQL queries — useful for pre-aggregations, transformations, and simplified access:

```yaml
views:
  - name: daily_sales
    sql: |
      SELECT DATE(created_at) as date, SUM(amount) as total, COUNT(*) as orders
      FROM orders
      GROUP BY DATE(created_at)

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

Spice supports writing to Apache Iceberg tables and Amazon S3 Tables via `INSERT INTO`:

```yaml
datasets:
  - from: iceberg:https://catalog.example.com/v1/namespaces/sales/tables/transactions
    name: transactions
    access: read_write # required for writes
```

```sql
INSERT INTO transactions SELECT * FROM staging_transactions;
```

## Referencing Secrets

Use `${ store_name:KEY }` syntax in params. See spice-secrets for full configuration:

```yaml
params:
  pg_user: ${ env:PG_USER }
  pg_pass: ${ secrets:PG_PASSWORD }
```

## Documentation

- [Data Connectors](https://spiceai.org/docs/components/data-connectors)
- [Datasets Reference](https://spiceai.org/docs/reference/spicepod/datasets)
- [Catalogs](https://spiceai.org/docs/components/catalogs)
- [Views](https://spiceai.org/docs/components/views)
- [Query Federation](https://spiceai.org/docs/features/query-federation)
- [Data Ingestion / Writes](https://spiceai.org/docs/features/data-ingestion)
