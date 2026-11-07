---
name: mz-dbt
description: >-
  Using the dbt-materialize adapter to manage Materialize streaming
  pipelines with dbt. Covers materializations (source, source_table,
  view, materialized_view, sink, table, seed), profile configuration,
  index creation, blue/green deployments (deploy_init, deploy_promote,
  deploy_cleanup), cluster management, strict mode, and testing. Use
  this skill whenever the user asks about writing dbt models for
  Materialize, configuring dbt profiles for Materialize, running
  dbt against Materialize, blue/green or zero-downtime deployments
  with dbt, creating sources or sinks in dbt, troubleshooting
  dbt-materialize issues, or migrating existing dbt projects to
  Materialize. Also trigger when the user mentions dbt-materialize,
  materialized_view materialization, deploy_init, deploy_promote,
  deploy_await, strict_mode, refresh_interval, retain_history, or
  partition_by in a dbt context.
---

# dbt-materialize

The `dbt-materialize` adapter lets you manage Materialize streaming pipelines using dbt's model-based workflow. It extends dbt-postgres with Materialize-specific materializations, blue/green deployment macros, and cluster management.

## How to Use This Skill

This skill is self-contained. Everything needed to help users write dbt models, configure profiles, run deployments, and troubleshoot is documented below. No access to the dbt-materialize source code or Materialize monorepo is required.

1. **User wants to set up dbt with Materialize**: See Profile Configuration below.
2. **User asks about a specific materialization**: See the Materializations section.
3. **User wants blue/green deployments**: See the Blue/Green Deployment section.
4. **User asks about indexes, clusters, or config**: See the Indexes, Strict Mode, or Cluster Management sections.
5. **User hits an error or unexpected behavior**: See Gotchas at the end.

For deeper adapter internals (rarely needed), the source lives in `misc/dbt-materialize/` in the MaterializeInc/materialize repo on GitHub. The official user-facing docs are at https://materialize.com/docs/manage/dbt/.

## Installation

```bash
pip install dbt-core dbt-materialize
```

Requires Materialize v0.68.0+.

## Profile Configuration

In `~/.dbt/profiles.yml`:

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: materialize
      host: <host>
      port: 6875
      user: <user>
      pass: <password>
      dbname: materialize
      schema: <dbt_schema>
      cluster: <cluster_name>       # optional, defaults to user's default cluster
      sslmode: require
      threads: 1                    # must be 1, Materialize does not support concurrent sessions
```

Key points:
- `threads` must be `1`. Materialize does not support concurrent DDL sessions.
- `cluster` is optional but recommended. If omitted, the user's default cluster is used.
- Autocommit is always on. Materialize does not support arbitrary queries in transactions.
- Use a service account for production deployments.

## Materializations

### materialized_view (primary pattern)

The most common materialization for streaming transformations. Creates an incrementally maintained view that updates automatically as upstream data changes.

```sql
-- models/order_totals.sql
{{ config(materialized='materialized_view') }}

SELECT
    customer_id,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
FROM {{ ref('orders') }}
GROUP BY customer_id
```

Supports `WITH` clause options via config:

```yaml
config:
  materialized: materialized_view
  cluster: analytics
  refresh_interval:
    every: '1 hour'
    aligned_to: '00:00:00'
  partition_by: [region, created_date]
  retain_history: '1 hour'
```

| Config | Purpose |
|--------|---------|
| `cluster` | Run on a specific cluster |
| `refresh_interval` | Schedule-based refresh instead of continuous |
| `partition_by` | Internal storage ordering for filter pushdown |
| `retain_history` | Keep historical data for a period |

### view

Standard SQL view. Use for lightweight transformations where you do not need results stored in memory.

```sql
{{ config(materialized='view') }}
SELECT * FROM {{ ref('raw_events') }} WHERE status = 'active'
```

### source

Defines an external data source (Kafka, PostgreSQL, MySQL). Requires a pre-existing CONNECTION created outside dbt (e.g., via Terraform or SQL).

```sql
-- models/staging/kafka_events.sql
{{ config(materialized='source') }}
FROM KAFKA CONNECTION kafka_connection (TOPIC 'events')
FORMAT AVRO USING CONFLUENT SCHEMA REGISTRY CONNECTION csr_connection
```

```sql
-- models/staging/pg_source.sql
{{ config(materialized='source') }}
FROM POSTGRES CONNECTION pg_connection (PUBLICATION 'mz_source')
FOR ALL TABLES
```

Sources that use `FOR ALL TABLES` automatically create subsources. Define these as dbt sources in a YAML file to reference them in downstream models.

Use `-- depends_on: {{ ref('pg_source') }}` to force execution ordering when a model depends on a source's subsources.

### source_table

Newer materialization for creating tables from sources, with better support for source versioning.

```sql
{{ config(materialized='source_table', strict_mode=True) }}
FROM SOURCE {{ ref('kafka_events') }} (REFERENCE "events_topic")
```

With `strict_mode: True`, the model skips recreation if the object already exists. Use `force_recreate: True` to override.

### sink

Exports data to an external system. Requires a pre-existing CONNECTION.

```sql
{{ config(materialized='sink') }}
FROM {{ ref('order_totals') }}
INTO KAFKA CONNECTION kafka_connection (TOPIC 'order-totals-output')
FORMAT JSON
ENVELOPE DEBEZIUM
```

Sinks must be in a dedicated schema (enforced when `strict_mode` is on). During blue/green deployments, sinks are automatically cut over to new upstream definitions.

### table

Maps to `CREATE MATERIALIZED VIEW` in Materialize (true table support is planned). Use `materialized_view` directly for clarity.

### seed

Standard dbt seeds work. Creates a table and inserts CSV data. Configure a cluster for seed operations:

```yaml
seeds:
  +cluster: seed_cluster
```

### Unsupported

- **incremental**: Use `materialized_view` instead. Materialize handles incrementality natively.
- **snapshot**: Not supported. Consider `materialized_view` with `retain_history`.

## Indexes

Add indexes to views, materialized views, sources, and tables to enable fast point lookups:

```yaml
config:
  indexes:
    - columns: [customer_id]
    - columns: [region, created_date]
      cluster: serving_cluster
    - default: true              # index all columns
```

Indexes are created after the relation. If `cluster` is not specified, the model's cluster is used.

## Strict Mode

Enable `strict_mode: True` in model config to enforce production isolation rules:

- Source tables can only share a schema with other source tables and seeds
- Sinks can only share a schema with other sinks
- Sources can only share a schema with other sources
- Standard models (views, materialized views) cannot share schemas with sources, sinks, or source tables

Validation happens at compile time using the dbt manifest.

## Blue/Green Deployment

Zero-downtime deployments by building into a parallel environment and atomically swapping.

### Prerequisites

Configure deployment targets in `dbt_project.yml`:

```yaml
vars:
  deployment:
    default:
      clusters:
        - production_cluster
      schemas:
        - public
```

The role running dbt must own the schemas and clusters being deployed. Sinks must be in a dedicated schema and cluster that are NOT listed in the deployment config.

### Workflow

**1. Initialize deployment environment:**
```bash
dbt run-operation deploy_init
```
Creates `<schema>_dbt_deploy` and `<cluster>_dbt_deploy` by cloning configuration, grants, and default privileges from production. Validates that production schemas and clusters exist, that they contain no sinks, and that the executing role has ownership. Use `--args '{ignore_existing_objects: True}'` to skip errors if deploy objects already exist.

For managed clusters, creates new clusters with the same size, replication factor, and schedule. For unmanaged clusters, clones replicas including size and availability zone.

**2. Build into the green environment:**
```bash
dbt run --vars 'deploy: True' --exclude config.materialized:source config.materialized:sink
```
Models are transparently routed to `_dbt_deploy` schemas and clusters. Always exclude sources and sinks.

If you get `String 'deploy:' is not valid YAML` (common on Windows/PowerShell), use `--vars "{\"deploy\": true}"` instead.

**3. Wait for hydration (recommended):**
```bash
dbt run-operation deploy_await
```
Polls cluster readiness with a single consolidated query (reduces catalog server load). Default: polls every 15 seconds, waits for lag under 1 second. Configure with `--args '{poll_interval: 30, lag_threshold: "5s"}'`.

Readiness checks evaluate three things in order:
- **Replica health**: Flags clusters where all replicas have 3+ OOM kills in the last 24 hours
- **Hydration status**: Counts hydrated vs total objects per cluster
- **Lag threshold**: Checks wallclock global lag is below the threshold

**4. Promote to production:**
```bash
dbt run-operation deploy_promote
```
Performs atomic `ALTER SCHEMA ... SWAP WITH` and `ALTER CLUSTER ... SWAP WITH` in a single transaction. Schemas are swapped before clusters to avoid stranding object references. Retries automatically on concurrent DDL conflicts (SQLSTATE 40001, up to 3 retries by default).

After swapping, the macro discovers sinks whose upstream dependencies changed and runs `ALTER SINK ... SET FROM` to cut them over to the new upstream definitions. It also tags deployed schemas with a comment containing the deploying user, timestamp, and git commit SHA.

| Argument | Default | Purpose |
|----------|---------|---------|
| `dry_run` | `false` | Print swap commands without executing |
| `wait` | `false` | Wait for hydration before swapping |
| `poll_interval` | `15` | Seconds between readiness checks (when `wait` is true) |
| `lag_threshold` | `"1s"` | Max lag for readiness (when `wait` is true) |
| `max_retries` | `3` | Retry count for concurrent DDL conflicts |

**5. Cleanup:**
```bash
dbt run-operation deploy_cleanup
```
Drops the `_dbt_deploy` schemas and clusters (CASCADE).

Any active `SUBSCRIBE` commands on the swapped clusters will break. On retry, clients reconnect to the newly deployed cluster automatically.

## Cluster Management Macros

```bash
# Create a managed cluster
dbt run-operation create_cluster --args '{cluster_name: analytics, size: "100cc", replication_factor: 1}'

# Drop a cluster
dbt run-operation drop_cluster --args '{cluster: analytics}'

# Set the active cluster for a session
dbt run-operation set_cluster --args '{cluster: analytics}'
```

## Slim Deployments

For development environments where downtime is acceptable:

1. Store the production `manifest.json` in blob storage after each deploy
2. Download the manifest in CI
3. Run only modified models:
   ```bash
   dbt build --select state:modified+ --state ./ --defer
   ```

## Node Selection

```bash
# Run specific models
dbt run --select "model_name"
dbt run --select "tag:nightly"

# Exclude sources and sinks (common in blue/green)
dbt run --exclude config.materialized:source config.materialized:sink
```

Or use `selectors.yml`:

```yaml
selectors:
  - name: exclude_sources_and_sinks
    default: true
    definition:
      union:
        - method: fqn
          value: "*"
        - exclude:
            - 'config.materialized:source'
            - 'config.materialized:sink'
```

## Testing

**Standard tests** work normally. Configure where failures are stored:

```yaml
store_failures: true
store_failures_as: materialized_view  # or 'view' (default: 'table')
```

**Unit tests** require dbt-materialize v1.8.0+ and upstream dependencies must exist in the database:

```bash
dbt test --select test_type:unit
```

**Source freshness** checks are not supported (sources in Materialize are always fresh by definition).

## Model Contracts

Enable contract enforcement to validate column types at compile time:

```yaml
models:
  - name: order_totals
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: text
        constraints:
          - type: not_null    # the only enforced constraint
```

Only `not_null` is enforced (via `ASSERT NOT NULL`). All other constraint types (`unique`, `primary_key`, `foreign_key`, `check`) are not supported.

## Gotchas

- **threads must be 1**: Materialize does not support concurrent DDL sessions. Setting threads > 1 will cause errors.
- **No transactions**: Autocommit is always on. Some dbt internal macros may behave differently.
- **LIMIT performance**: `dbt show` uses LIMIT, which has performance implications in Materialize. Use sparingly.
- **Connections are external**: Sources and sinks need pre-existing CONNECTIONs (created via Terraform, SQL, or other tooling). dbt does not manage connections.
- **Clusters must pre-exist**: dbt does not implicitly create clusters. Create them before running models, either via SQL, Terraform, or the `create_cluster` macro.
- **Grants not supported**: dbt's built-in grants configuration raises an error. Use Terraform or SQL for RBAC.
- **Incremental not supported**: Use `materialized_view` instead; Materialize handles incrementality natively.
- **Blue/green requires sink isolation**: Sinks must live in dedicated schemas and clusters not listed in the deployment config.
- **Relation name limit**: 255 characters (much longer than PostgreSQL's 63).
