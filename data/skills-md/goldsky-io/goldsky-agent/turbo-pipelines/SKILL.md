---
name: turbo-pipelines
description: "Goldsky Turbo pipeline YAML reference — the authoritative source for field names, required vs optional fields, and valid values. Use whenever the user asks about specific YAML fields: what does `start_at: earliest` vs `latest` do, what fields does a postgres/clickhouse/kafka sink require, what is the `from:` field in a sink, how does `checkpoint` work, what's the syntax for `batch_size` or `primary_key`. Also use for validation errors like 'unknown field' or 'missing required field'. For interactive pipeline building end-to-end, use /turbo-builder instead."
---

# Turbo Pipeline Configuration Reference

YAML configuration reference for Turbo pipelines. This is a lookup reference — for interactive pipeline building, use `/turbo-builder`. For pipeline troubleshooting, use `/turbo-doctor`.

> **CRITICAL:** Always validate YAML with `goldsky turbo validate <file.yaml>` before showing complete pipeline YAML to the user or deploying.

---

## Quick Start

Deploy a minimal pipeline:

```yaml
name: my-first-pipeline
resource_size: s
sources:
  transfers:
    type: dataset
    dataset_name: base.erc20_transfers
    version: 1.2.0
    start_at: latest
transforms: {}
sinks:
  output:
    type: blackhole
    from: transfers
```

```bash
# Validate first:
goldsky turbo validate pipeline.yaml

# Then deploy:
goldsky turbo apply pipeline.yaml -i
```

---

## Prerequisites

- [ ] **Goldsky CLI installed** - `curl https://goldsky.com | sh`
- [ ] **Turbo CLI extension installed** (SEPARATE binary!) - `curl https://install-turbo.goldsky.com | sh`
  - Note: Run `goldsky turbo list` - if you see "The turbo binary is not installed", install it first
- [ ] **Logged in** - `goldsky login`
- [ ] Pipeline YAML file ready
- [ ] Secrets created for sinks (if using PostgreSQL, ClickHouse, Kafka, etc.)

## Discovering Available Data Sources

**For dataset discovery, invoke the `datasets` skill.**

Quick reference for common datasets:

| What They Want             | Dataset to Use             |
| -------------------------- | -------------------------- |
| Token transfers (fungible) | `<chain>.erc20_transfers`  |
| NFT transfers              | `<chain>.erc721_transfers` |
| All contract events        | `<chain>.logs`             |
| Block data                 | `<chain>.blocks`           |
| Transaction data           | `<chain>.transactions`     |

For full chain prefixes, dataset types, and version discovery, use `/datasets`.

---

## Quick Reference

### Installation Commands

| Action                  | Command                                        |
| ----------------------- | ---------------------------------------------- |
| Install Goldsky CLI     | `curl https://goldsky.com \| sh`               |
| Install Turbo extension | `curl https://install-turbo.goldsky.com \| sh` |
| Verify Turbo installed  | `goldsky turbo list`                           |

### Pipeline Commands

| Action                  | Command                                                |
| ----------------------- | ------------------------------------------------------ |
| List datasets           | `goldsky dataset list` ⚠️ **Slow (30-60s)**            |
| **Validate (REQUIRED)** | `goldsky turbo validate pipeline.yaml` ✓ **Fast (3s)** |
| Deploy/Update           | `goldsky turbo apply pipeline.yaml`                    |
| Deploy + Inspect        | `goldsky turbo apply pipeline.yaml -i`                 |
| List pipelines          | `goldsky turbo list`                                   |
| View live data          | `goldsky turbo inspect <name>`                         |
| Inspect node            | `goldsky turbo inspect <name> -n <node>`               |
| View logs               | `goldsky turbo logs <name>`                            |
| Follow logs             | `goldsky turbo logs <name> --follow`                   |
| List secrets            | `goldsky secret list`                                  |

For pause, resume, restart, and delete commands, see `/turbo-lifecycle`.

---

## Configuration Reference

### Pipeline Structure

Every Turbo pipeline YAML has this structure:

```yaml
name: my-pipeline # Required: unique identifier
resource_size: s # Required: s, m, or l
description: "Optional desc" # Optional: what the pipeline does

sources:
  source_name: # Define data inputs
    type: dataset
    # ... source config

transforms: # Optional: process data
  transform_name:
    type: sql
    # ... transform config

sinks:
  sink_name: # Define data outputs
    type: postgres
    # ... sink config
```

### Top-Level Fields

| Field           | Required | Description                                     |
| --------------- | -------- | ----------------------------------------------- |
| `name`          | Yes      | Unique pipeline identifier (lowercase, hyphens)                  |
| `resource_size` | Yes      | Worker allocation: `s`, `m`, or `l`                              |
| `description`   | No       | Human-readable description                                       |
| `job`           | No       | `true` for one-time batch jobs (default: `false` = streaming)    |
| `sources`       | Yes      | Data input definitions                                           |
| `transforms`    | No       | Data processing definitions                                      |
| `sinks`         | Yes      | Data output definitions                                          |

### Job Mode

Set `job: true` for one-time batch processing (historical backfills, data exports):

```yaml
name: backfill-usdc-history
resource_size: l
job: true

sources:
  logs:
    type: dataset
    dataset_name: ethereum.raw_logs
    version: 1.0.0
    start_at: earliest
    end_block: 19000000
    filter: >-
      address = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
transforms: {}
sinks:
  output:
    type: s3_sink
    from: logs
    endpoint: https://s3.amazonaws.com
    bucket: my-backfill-bucket
    prefix: usdc/
    secret_name: MY_S3
```

**Job mode rules:**
- Runs to completion and auto-cleans up ~1 hour after finishing
- **Must `goldsky turbo delete` before redeploying** — cannot update in-place
- **Cannot use `restart`** — use delete + apply instead
- Use `end_block` to bound the range (otherwise processes to chain tip and stops)
- Best with `resource_size: l` for faster backfills

> **For architecture guidance on when to use job vs streaming mode, see `/turbo-architecture`.**

### Resource Sizes

| Size | Workers | Use Case                           |
| ---- | ------- | ---------------------------------- |
| `s`  | 1       | Testing, low-volume data           |
| `m`  | 2       | Production, moderate volume        |
| `l`  | 4       | High-volume, multi-chain pipelines |

---

## Source Configuration

### Dataset Source

```yaml
sources:
  my_source:
    type: dataset
    dataset_name: <chain>.<dataset_type>
    version: <version>
    start_at: latest | earliest # EVM chains
    # OR
    start_block: <slot_number> # Solana only
```

### Source Fields

| Field          | Required | Description                                              |
| -------------- | -------- | -------------------------------------------------------- |
| `type`         | Yes      | `dataset` for blockchain data                            |
| `dataset_name` | Yes      | Format: `<chain>.<dataset_type>`                         |
| `version`      | Yes      | Dataset version (e.g., `1.2.0`)                          |
| `start_at`     | EVM      | `latest` or `earliest`                                   |
| `start_block`  | Solana   | Specific slot number (omit for latest)                   |
| `end_block`    | No       | Stop processing at this block (for bounded backfills)    |
| `filter`       | No       | SQL WHERE clause to pre-filter at source level (efficient)|

### Source-Level Filtering

Use `filter` to reduce data volume **before** it reaches transforms. This is significantly more efficient than filtering in SQL transforms because it eliminates data at the ingestion layer:

```yaml
sources:
  usdc_logs:
    type: dataset
    dataset_name: base.raw_logs
    version: 1.0.0
    start_at: earliest
    filter: >-
      address = lower('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913')
      AND block_number >= 10000000
```

**Best practices:**
- Use `filter` for contract addresses and block ranges (coarse pre-filtering)
- Use transform `WHERE` for event types, parameter values, exclusions (fine-grained)
- `filter` uses standard SQL WHERE syntax (same as DataFusion)
- Combine `filter` with `start_at: earliest` + `end_block` for precise bounded backfills

### Chains and Dataset Types

For the full list of chains, prefixes, and dataset types, see `/datasets`. Key points:

- **EVM chains:** `ethereum`, `base`, `matic` (Polygon — not `polygon`), `arbitrum`, `optimism`, `bsc`, `avalanche`
- **Non-EVM:** `solana` (uses `start_block` not `start_at`), `bitcoin.raw`, `stellar_mainnet`, `sui`, `near`, `starknet`, `fogo`
- **EVM dataset types:** `raw_logs`, `raw_transactions` (**not** `transactions`), `blocks`, `raw_traces`, `erc20_transfers`, `erc721_transfers`, `decoded_logs`

---

## Transform Configuration

### Transform Types

| Type            | Use Case                              |
| --------------- | ------------------------------------- |
| `sql`           | Filtering, projections, SQL functions |
| `script`        | Custom TypeScript/WASM logic          |
| `handler`       | Call external HTTP APIs to enrich data|
| `dynamic_table` | Lookup tables backed by a database    |

### SQL Transform

Most common transform type:

```yaml
transforms:
  filtered:
    type: sql
    primary_key: id
    sql: |
      SELECT
        id,
        sender,
        recipient,
        amount
      FROM source_name
      WHERE amount > 1000
```

| Field         | Required | Description                            |
| ------------- | -------- | -------------------------------------- |
| `type`        | Yes      | `sql`                                  |
| `primary_key` | Yes      | Column for uniqueness/ordering         |
| `sql`         | Yes      | SQL query (reference sources by name)  |
| `from`        | No       | Override default source (for chaining) |

### TypeScript Transform

For complex logic that SQL can't handle (runs in WASM sandbox):

```yaml
transforms:
  custom:
    type: script
    primary_key: id
    language: typescript
    from: source_name
    schema:
      id: string
      sender: string
      amount: string
      processed_at: string
    script: |
      function invoke(data) {
        if (data.amount < 1000) return null;  // Filter out
        return {
          id: data.id,
          sender: data.sender,
          amount: data.amount,
          processed_at: new Date().toISOString()
        };
      }
```

> **For full TypeScript transform documentation, schema types, and examples, see `/turbo-transforms`.**

### Dynamic Table Transform

Updatable lookup tables for runtime filtering (allowlists, blocklists, enrichment):

```yaml
transforms:
  tracked_wallets:
    type: dynamic_table
    backend_type: Postgres        # or: InMemory
    backend_entity_name: tracked_wallets
    secret_name: MY_DB            # required for Postgres
```

Use with `dynamic_table_check()` in SQL transforms:

```sql
WHERE dynamic_table_check('tracked_wallets', sender)
```

> **For full dynamic table documentation, backend options, and examples, see `/turbo-transforms`.**

### Handler Transform

Call external HTTP APIs to enrich data:

```yaml
transforms:
  enriched:
    type: handler
    primary_key: id
    from: my_source
    url: https://my-api.example.com/enrich
    headers:
      Authorization: Bearer my-token
    batch_size: 100
    timeout_ms: 5000
```

> **For full handler transform documentation, see `/turbo-transforms`.**

### Transform Chaining

Chain transforms using `from`:

```yaml
transforms:
  step1:
    type: sql
    primary_key: id
    sql: SELECT * FROM source WHERE amount > 100

  step2:
    type: sql
    primary_key: id
    from: step1
    sql: SELECT *, 'processed' as status FROM step1
```

---

## Sink Configuration

### Common Sink Fields

| Field         | Required | Description                         |
| ------------- | -------- | ----------------------------------- |
| `type`        | Yes      | Sink type                           |
| `from`        | Yes      | Source or transform to read from    |
| `secret_name` | Varies   | Secret for credentials (most sinks) |
| `primary_key` | Varies   | Column for upserts (database sinks) |

### Blackhole Sink (Testing)

```yaml
sinks:
  test_output:
    type: blackhole
    from: my_transform
```

### PostgreSQL Sink

```yaml
sinks:
  postgres_output:
    type: postgres
    from: my_transform
    schema: public
    table: my_table
    secret_name: MY_POSTGRES_SECRET
    primary_key: id
```

**Secret format:** PostgreSQL connection string:
```
postgres://username:password@host:port/database
```

### PostgreSQL Aggregate Sink

Real-time aggregations in PostgreSQL using database triggers. Data flows into a landing table, and a trigger maintains aggregated values in a separate table.

```yaml
sinks:
  balances:
    type: postgres_aggregate
    from: transfers
    schema: public
    landing_table: transfer_log
    agg_table: account_balances
    primary_key: transfer_id
    secret_name: MY_POSTGRES
    group_by:
      account:
        type: text
    aggregate:
      balance:
        from: amount
        fn: sum
```

Supported aggregation functions: `sum`, `count`, `avg`, `min`, `max`

### ClickHouse Sink

```yaml
sinks:
  clickhouse_output:
    type: clickhouse
    from: my_transform
    table: my_table
    secret_name: MY_CLICKHOUSE_SECRET
    primary_key: id
```

**Secret format:** ClickHouse connection string:
```
https://username:password@host:port/database
```

### Kafka Sink

```yaml
sinks:
  kafka_output:
    type: kafka
    from: my_transform
    topic: my-topic
    topic_partitions: 10
    data_format: avro          # or: json
    schema_registry_url: http://schema-registry:8081  # required for avro
```

### Webhook Sink

> **Note:** Turbo webhook sinks do **not** support Goldsky's native secrets management. Include auth headers directly in the pipeline config.

```yaml
sinks:
  webhook_output:
    type: webhook
    from: my_transform
    url: https://api.example.com/webhook
    one_row_per_request: true
    headers:
      Authorization: Bearer your-token
      Content-Type: application/json
```

### S3 Sink

```yaml
sinks:
  s3_output:
    type: s3_sink
    from: my_transform
    endpoint: https://s3.amazonaws.com
    bucket: my-bucket
    prefix: data/
    secret_name: MY_S3_SECRET
```

**Secret format:** `access_key_id:secret_access_key` (or `access_key_id:secret_access_key:session_token` for temporary credentials)

### S2 Sink

Publish to [S2.dev](https://s2.dev) streams — a serverless alternative to Kafka.

```yaml
sinks:
  s2_output:
    type: s2_sink
    from: my_transform
    access_token: your_access_token
    basin: your-basin-name
    stream: your-stream-name
```

---

## Starter Templates

> **Template files are available in the `templates/` folder.** Copy and customize these for your pipelines.

| Template                       | Description                       | Use Case                     |
| ------------------------------ | --------------------------------- | ---------------------------- |
| `minimal-erc20-blackhole.yaml` | Simplest pipeline, no credentials | Quick testing                |
| `filtered-transfers-sql.yaml`  | Filter by contract address        | USDC, specific tokens        |
| `postgres-output.yaml`         | Write to PostgreSQL               | Production data storage      |
| `multi-chain-pipeline.yaml`    | Combine multiple chains           | Cross-chain analytics        |
| `solana-transfers.yaml`        | Solana SPL tokens                 | Non-EVM chains               |
| `multi-sink-pipeline.yaml`     | Multiple outputs                  | Archive + alerts + streaming |

**To use a template:**

```bash
# Copy template to your project
cp templates/minimal-erc20-blackhole.yaml my-pipeline.yaml

# Customize as needed, then validate
goldsky turbo validate my-pipeline.yaml

# Deploy
goldsky turbo apply my-pipeline.yaml -i
```

**Template location:** `templates/` (relative to this skill's directory)

---

## Common Update Patterns

### Adding a SQL Transform

**Before:**

```yaml
transforms: {}
sinks:
  output:
    type: blackhole
    from: transfers
```

**After:**

```yaml
transforms:
  filtered:
    type: sql
    primary_key: id
    sql: |
      SELECT * FROM transfers WHERE amount > 1000000
sinks:
  output:
    type: blackhole
    from: filtered # Changed from 'transfers'
```

### Adding a PostgreSQL Sink

```yaml
sinks:
  existing_sink:
    type: blackhole
    from: my_transform
  # Add new sink
  postgres_output:
    type: postgres
    from: my_transform
    schema: public
    table: my_data
    secret_name: MY_POSTGRES_SECRET
    primary_key: id
```

### Changing Resource Size

```yaml
resource_size: m # was: s
```

### Adding a New Source

```yaml
sources:
  eth_transfers:
    type: dataset
    dataset_name: ethereum.erc20_transfers
    version: 1.0.0
    start_at: latest
  # Add new source
  base_transfers:
    type: dataset
    dataset_name: base.erc20_transfers
    version: 1.2.0
    start_at: latest
```

---

## Checkpoint Behavior

### Understanding Checkpoints

When you update a pipeline:

- **Checkpoints are preserved by default** - Processing continues from where it left off
- **Source checkpoints are tied to source names** - Renaming a source resets its checkpoint
- **Pipeline checkpoints are tied to pipeline names** - Renaming the pipeline resets all checkpoints

### Resetting Checkpoints

**Option 1:** Rename the source

```yaml
sources:
  transfers_v2: # Changed from 'transfers'
    type: dataset
    dataset_name: base.erc20_transfers
    version: 1.2.0
    start_at: earliest # Will process from beginning
```

**Option 2:** Rename the pipeline

```yaml
name: my-pipeline-v2 # Changed from 'my-pipeline'
```

**Warning:** Resetting checkpoints means reprocessing all historical data.

---

## Troubleshooting

See `references/troubleshooting.md` for:
- CLI hanging / Turbo binary not found fixes
- Common validation errors (unknown dataset, missing primary_key, bad source reference)
- Common runtime errors (auth failed, connection refused, Neon size limit)
- Quick troubleshooting table

Also see `/turbo-monitor-debug` for error patterns and log analysis.

---

## Related

- **`/turbo-builder`** — Interactive wizard to build pipelines step-by-step
- **`/turbo-doctor`** — Diagnose and fix pipeline issues
- **`/datasets`** — Dataset names and chain prefixes
