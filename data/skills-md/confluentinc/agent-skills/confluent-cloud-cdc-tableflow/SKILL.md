---
name: confluent-cloud-cdc-tableflow
description: Set up end-to-end Change Data Capture (CDC) pipelines on Confluent Cloud using Debezium source connectors, Flink for transformation, and Tableflow for data lake integration. Supports JSON_SR, Avro, and Protobuf formats. Handles schemaless topics (plain JSON without SR) and multi-event topics. This skill handles the complete workflow from database to Iceberg/Delta tables. Use this skill when users want to capture database changes and materialize them into Iceberg or Delta Lake tables via Confluent Cloud Tableflow. Trigger phrases include "CDC to Tableflow", "database to Iceberg", "database to Delta Lake", "stream database changes to data lake", "set up Tableflow pipeline", "schemaless topic to Tableflow", or "multi-event topic to Iceberg". Do NOT trigger for general CDC, Debezium, or database replication requests that do not involve Tableflow or Iceberg/Delta Lake as the destination.
metadata:
  version: "1.0.0"
---

# Confluent Cloud CDC to Tableflow Pipeline

Build production-ready Change Data Capture pipelines that stream database changes through Confluent Cloud to Iceberg or Delta Lake tables using Debezium, Flink, and Tableflow.

## Overview

This skill automates the setup of a complete CDC pipeline:

**Database → Debezium CDC Connector → Kafka + Schema Registry → Flink (decode & transform) → Tableflow → Iceberg/Delta Tables**

### Supported Databases (Fully-Managed Debezium Connectors Only)
- Microsoft SQL Server CDC Source V2
- MySQL CDC Source V2
- PostgreSQL CDC Source V2
- Oracle XStream CDC Source
- DynamoDB CDC Source

### Key Components
1. **Debezium CDC Source Connector**: Captures database changes as events
2. **Schema Registry**: Manages Avro/JSON/Protobuf schemas (default: JSON_SR)
3. **Confluent Cloud Flink**: Decodes Debezium envelopes and transforms data
4. **Tableflow**: Native Confluent Cloud feature that materializes Kafka topics as Iceberg or Delta tables

### Critical Architecture Rules

**1. NEVER enable Tableflow directly on CDC source topics.**

Always use the Flink decode pattern: CDC Source Topic → Flink INSERT → Target Topic (`changelog.mode = 'upsert'`) → Tableflow.

CDC connectors with `tombstones.on.delete=true` produce null-value Kafka records (tombstones) on DELETE operations. If Tableflow is enabled directly on the CDC source topic, it will use APPEND mode by default and immediately suspend when it encounters a tombstone: *"Tableflow will be suspended because we detected a Kafka record with a null value."*

The Flink decode layer solves this by interpreting Debezium CDC semantics natively — it translates DELETEs into proper retract/tombstone messages that upsert-mode Tableflow handles correctly.

**Do NOT use `after.state.only=true`** as a shortcut to bypass the Flink decode step. While it strips the Debezium envelope, tombstone records from DELETEs still break APPEND-mode Tableflow. Additionally, `OracleXStreamSource` does not support the `after.state.only` configuration option at all.

**2. Tableflow changelog mode is IMMUTABLE after first materialization.**

Tableflow caches the changelog mode (APPEND or UPSERT) when it first materializes data. Once set, it cannot be changed — even by altering the Kafka topic's `changelog.mode` property or by deleting and recreating the Tableflow topic. The S3 `table_path` is keyed by Kafka topic name, so recreating a Tableflow topic reuses the same S3 path and cached state.

Attempting to change the mode causes: *"The changelog mode for this topic has been modified since table materialization began."* Flip-flopping the mode further corrupts state with: *"Incompatible schema evolution detected."*

**To change changelog mode**, you must delete the Tableflow topic, delete the underlying Kafka topic, and recreate both from scratch. This is why it's critical to create target topics with `'changelog.mode' = 'upsert'` from the start.

**3. Pipeline cleanup order matters.**

When resetting a CDC-to-Tableflow pipeline, delete resources in this order:
1. Tableflow topics (on target topics)
2. Flink INSERT statements
3. Flink target tables (DROP TABLE)
4. Target Kafka topics
5. CDC connectors
6. CDC source Kafka topics (including dbhistory/schema-changes topics)
7. All associated schemas from Schema Registry (both `-key` and `-value` subjects)

**Never delete CDC source Kafka topics while the connector is still running** — the connector cannot recover or re-snapshot and must be fully recreated.

### Important Clarifications
- **Tableflow is NOT a connector.** It is a native topic-level feature enabled via the Tableflow API or Confluent Cloud UI.
- **Confluent Cloud Flink auto-discovers CDC tables.** You do NOT need to manually create source tables — topics with Schema Registry schemas are automatically available as Flink tables.
- **Topics without SR schemas** can still be handled — register a JSON schema (partial is fine), use schema inference, or use Flink's raw BYTES with JSON functions. See `references/connector-configs.md` "Handling Topics Without Schema Registry".
- **All SR-backed formats work identically** — `JSON_SR`, `AVRO`, and `PROTOBUF` all support Flink auto-discovery and Tableflow. Choose based on throughput needs vs. debuggability.
- **Managed connectors use `output.data.format`**, not `key.converter`/`value.converter` classes.

## Workflow Phases

### Phase 0: Tool Selection & MCP Server Validation (CRITICAL)

**Default: Use Confluent MCP Server.** The MCP server is the preferred method for all Confluent Cloud operations. Only fall back to the Confluent CLI (`confluent` command) and REST APIs if the MCP server is not installed or unavailable.

#### 0.1 Verify MCP Server Availability

Check for `mcp__confluent__*` tools (list-environments, create-connector, create-flink-statement, create-tableflow-topic, list-schemas, list-topics, consume-messages, search-topics-by-name).

**If MCP is not available**, fall back to the Confluent CLI (`confluent` command) and REST APIs for all operations. The CLI fallback should mirror the same workflow phases but use CLI commands instead of MCP tool calls.

**CLI Fallback Examples:**
```bash
# Environment & cluster discovery
confluent environment list
confluent kafka cluster list --environment <env-id>

# Connector operations
confluent connect cluster create --config-file connector-config.json --cluster <cluster-id> --environment <env-id>
confluent connect cluster describe <connector-id>
confluent connect cluster list --cluster <cluster-id> --environment <env-id>

# Flink operations
confluent flink compute-pool create <pool-name> --cloud <cloud> --region <region> --environment <env-id>
confluent flink statement create <statement-name> --sql "<SQL>" --compute-pool <pool-id> --environment <env-id>
confluent flink statement describe <statement-name> --environment <env-id>
confluent flink statement delete <statement-name> --environment <env-id>

# Topic & schema operations
confluent kafka topic list --cluster <cluster-id> --environment <env-id>
confluent schema-registry subject list --environment <env-id>

# Tableflow operations
confluent tableflow topic enable <topic-name> --cluster <cluster-id> --environment <env-id> --storage-type MANAGED --table-formats ICEBERG
confluent tableflow topic list --cluster <cluster-id> --environment <env-id>
confluent tableflow topic describe <topic-name> --cluster <cluster-id> --environment <env-id>
confluent tableflow topic disable <topic-name> --cluster <cluster-id> --environment <env-id>
```

**REST API Fallback:** If neither MCP nor CLI is available, use the Confluent Cloud REST APIs directly. All calls use HTTP Basic Auth with a **Cloud API Key** (not a Kafka API key). See `references/rest-api.md` for endpoint patterns and examples.

#### 0.2 Gather Confluent Cloud Details from the User

Ask the user to provide the following Confluent Cloud details:

| Detail | Example | Used For |
|---|---|---|
| Environment ID | `env-0ypxv6` | `environmentId` in all MCP calls |
| Kafka Cluster ID | `lkc-qo5k36` | `clusterId` in all MCP calls |
| Flink Compute Pool ID | `lfcp-3v39xw` | `computePoolId` in Flink statements |
| Flink Catalog Name | `my_environment` | `catalogName` in Flink statements |
| Flink Database Name | `cluster_0` | `databaseName` in Flink statements |

**Credentials:** Generate a `cdc-credentials.properties` file with placeholders for: Kafka API Key/Secret (cluster-scoped), Database Username/Password. Have the user populate it in their editor and add it to `.gitignore`. If the user prefers Claude not read the file, fall back to CLI: generate `connector-config.json` with placeholders, user fills it in, then `confluent connect cluster create --config-file connector-config.json`.

#### 0.3 Verify MCP Cluster Targeting

**Quick verification:**
1. Run `mcp__confluent__list-topics` to confirm the MCP server is connected to the expected cluster
2. Run `mcp__confluent__list-schemas` to verify Schema Registry is accessible

Schema Registry is shared at the environment level across all clusters.

### Phase 1: Discovery & Validation

#### 1.1 Check Existing Setup

Use MCP to check what already exists:

```
mcp__confluent__list-connectors(environmentId, clusterId)  →  Existing CDC connectors
mcp__confluent__list-flink-statements(environmentId, computePoolId)  →  Existing Flink jobs
mcp__confluent__list-tableflow-topics(environmentId, clusterId)  →  Existing Tableflow topics
```

Ask the user:
- "Do you have any CDC connectors already running?"
- "Do you have a Flink compute pool you'd like to use, or should I create one?"
- "Is your database already configured for CDC?"

#### 1.2 Validate Topic Prefix Uniqueness

Before proceeding, validate that the chosen `topic.prefix` won't collide with existing topics:

```
mcp__confluent__search-topics-by-name(topicName: "<proposed-prefix>", environmentId, clusterId)
```

Or via CLI:
```bash
confluent kafka topic list --cluster <cluster-id> --environment <env-id> | grep "^<proposed-prefix>"
```

If any existing topics share the proposed prefix, warn the user and recommend a unique prefix. A prefix collision silently merges CDC data with unrelated topics, which can corrupt both pipelines.

#### 1.3 Check Schema Registry Compatibility

Default `BACKWARD` compatibility can halt CDC connectors when database columns are dropped. Set `FULL_TRANSITIVE` for CDC subjects after the connector creates them:

```bash
confluent schema-registry config update --subject "<topic-prefix>.<schema>.<table>-value" --compatibility FULL_TRANSITIVE --environment <env-id>
```

#### 1.4 Gather Required Information

**Database Configuration:**
- Database type (SQL Server, MySQL, PostgreSQL, Oracle, or DynamoDB)
- Connection details (hostname, port, database name)
- Credentials (populated by the user in the credentials file)
- Specific tables to capture (format: `schema.table`)

**Schema Format:** Ask the user: `JSON_SR` (default, human-readable), `AVRO` (smaller payloads, high-throughput), or `PROTOBUF` (strongly typed). All work identically with Flink auto-discovery and Tableflow. **Never use plain `JSON`** — it breaks both. See `references/connector-configs.md` for detailed comparison.

**Existing Topics Without SR:** See `references/connector-configs.md` "Handling Topics Without Schema Registry" for options (register JSON schema, schema inference, or Flink raw BYTES).

**Tableflow Destination:**
- Target format: Iceberg or Delta Lake
- Storage: Managed (recommended, Confluent manages S3) or BYOB (user's own S3 bucket, requires Provider Integration ID)

**Naming Convention:**
- Default: `cdc-pipeline-skill-{database-type}-{YYYYMMDD}`
- Example: `cdc-pipeline-skill-postgres-20260323`

#### 1.5 Validate Database Prerequisites

Each database requires specific CDC setup. Read `references/database-prerequisites.md` for details:
- PostgreSQL: WAL level = logical, replication slots, publication
- MySQL: binlog format = ROW, GTID mode
- SQL Server: CDC enabled on database and tables, SQL Server Agent running
- **Oracle XStream: GoldenGate replication enabled (`enable_goldengate_replication=TRUE`), ARCHIVELOG mode, supplemental logging, XStream admin user with `DBMS_XSTREAM_AUTH` privileges, XStream outbound server created via `DBMS_XSTREAM_ADM.CREATE_OUTBOUND`, connector user with XStream connect privilege. Full prereqs: https://docs.confluent.io/cloud/current/connectors/cc-oracle-xstream-cdc-source/prereqs-validation.md**
- DynamoDB: Streams enabled with NEW_AND_OLD_IMAGES

If the database isn't properly configured, guide the user through setup before proceeding.

**Oracle XStream important limitations:**
- Only supports non-CDB architecture on Amazon RDS for Oracle
- Does NOT support Oracle Autonomous Databases or Oracle Standby (Data Guard)
- Does NOT support Downstream Capture
- `after.state.only` is NOT supported by `OracleXStreamSource`
- Requires a valid Confluent license for XStream Out

### Phase 2: Planning

Generate the complete configuration plan and present it to the user for approval.

#### 2.1 Connector Configuration

Based on the database type, generate the connector configuration using the appropriate template from `references/connector-configs.md`. The templates include all required fields (`name`, `connector.class`, `topic.prefix`, `kafka.api.key`, `output.data.format`, `decimal.handling.mode`, etc.) and database-specific settings.

**Set the schema format** based on user preference (default `JSON_SR`):
```json
{
  "output.data.format": "JSON_SR",
  "output.key.format": "JSON_SR"
}
```
Replace `JSON_SR` with `AVRO` or `PROTOBUF` if the user requested a different format. Both key and value formats should match. All other connector settings remain the same regardless of format choice.

**Topic Naming Pattern:**
`{topic.prefix}.{schema}.{table}`
Example with `topic.prefix = "postgres-cdc"`: `postgres-cdc.public.customers`

#### 2.2 Flink SQL Statements

In Confluent Cloud Flink, the CDC source table is **auto-discovered** from the Kafka topic. You only need to:

**Note:** The examples below use a `customers` table with illustrative column names. Substitute the user's actual table name, columns, and types based on the schema discovered from their CDC topic.

1. **Create a target table** (for plain JSON_SR output to Tableflow):
```sql
CREATE TABLE `target_customers` (
  `id` INT NOT NULL,
  `name` STRING,
  `email` STRING,
  `created_at` TIMESTAMP_LTZ(3),
  PRIMARY KEY (`id`) NOT ENFORCED
) WITH (
  'changelog.mode' = 'upsert'
);
```

2. **Create an INSERT statement** (continuous job to decode and transform):
```sql
INSERT INTO `target_customers`
SELECT
  `id`,
  `name`,
  `email`,
  TO_TIMESTAMP_LTZ(`created_at` / 1000, 3)
FROM `postgres-cdc.public.customers`;
```

**IMPORTANT Cloud Flink differences:**
- Do NOT specify `'connector'`, `'value.format'`, `'properties.bootstrap.servers'`, or Schema Registry URLs in CREATE TABLE — Cloud Flink handles all of this automatically
- Do NOT create source tables for CDC topics — they are auto-discovered
- Do NOT reference `after.*` fields or filter by `op` — Flink interprets CDC changelog semantics natively
- Use `TIMESTAMP_LTZ(3)` for Debezium timestamps, not `TIMESTAMP(3)`

**DynamoDB CDC is different from SQL CDC in Flink.** The auto-discovered table has columns `id` (key) and `val` (a complex ROW type containing the CDC envelope with `op`, `before.document`, `after.document`). Flink does NOT auto-decode this envelope like it does for SQL Debezium connectors. You must manually extract fields:
```sql
CREATE TABLE `target_dynamodb` (
  `id` STRING NOT NULL,
  `document` STRING,
  PRIMARY KEY (`id`) NOT ENFORCED
) WITH ('changelog.mode' = 'upsert');

INSERT INTO `target_dynamodb`
SELECT `id`, `val`.`after`.`document`
FROM `dynamodb-cdc-source-topic`;
```
The `document` field is a JSON string of the DynamoDB item in DynamoDB's native type format (e.g., `{"name":{"S":"Alice"},"age":{"N":"30"}}`).

**Debezium Type Conversions:** See `references/flink-sql-patterns.md` for the full type mapping table. Key conversions: use `TO_TIMESTAMP_LTZ(col / 1000, 3)` for MicroTimestamp, `TO_TIMESTAMP_LTZ(col, 3)` for Timestamp, and ensure `decimal.handling.mode=string` is set on the connector (BYTES default is unusable in Flink).

#### 2.3 Tableflow Configuration

Tableflow is a **native topic-level feature**, not a connector. It is enabled per-topic.

**Storage Options:**
- **Managed** (recommended): Confluent manages the S3 storage. No credentials needed.
- **BYOB (Bring Your Own Bucket)**: User provides their S3 bucket. Requires a Provider Integration ID set up in Confluent Cloud (Settings → Provider Integrations).

**Table Formats:** Iceberg (recommended) or Delta Lake

#### 2.4 Present the Plan

Show the user:
1. Connector configuration (with sensitive fields masked)
2. Flink compute pool to use
3. Flink SQL statements (target table + INSERT)
4. Tableflow config (storage type, format)
5. Expected topic names

Wait for explicit confirmation before proceeding.

### Phase 3: Execution

Execute step-by-step using MCP tools, checking status after each component.

#### 3.1 Create CDC Source Connector

Build the connector configuration using the template for the user's database type from `references/connector-configs.md`. Each template includes all required fields, including the `name` field.

**Using MCP:**
```
mcp__confluent__create-connector(
  connectorName: "<connector-name>",
  environmentId: "<env-id>",
  clusterId: "<cluster-id>",
  connectorConfig: { <config from references/connector-configs.md> }
)
```

**Verify:** Managed connectors take **2-5 minutes** to provision. Poll `mcp__confluent__read-connector` — `tasks: []` means still provisioning; `tasks: [{...}]` means ready. Then verify schemas with `mcp__confluent__list-schemas(subjectPrefix: "postgres-cdc")`. If no schemas after 5 min with tasks assigned, check database connectivity. Use Confluent Cloud UI for connector error logs (MCP doesn't expose them).

#### 3.2 Create Flink Compute Pool (if needed)

If the user doesn't have an existing Flink compute pool, create one before executing SQL:

```
confluent flink compute-pool create <pool-name> --cloud <cloud-provider> --region <region> --environment <env-id>
```

Use the same cloud provider and region as the Kafka cluster. Wait for the pool status to be `RUNNING` before proceeding.

#### 3.3 Execute Flink SQL

**Step 1: Verify CDC table is auto-discovered:**
```
mcp__confluent__create-flink-statement(
  statementName: "show-tables-check",
  statement: "SHOW TABLES;",
  environmentId: "<env-id>",
  computePoolId: "<pool-id>",
  catalogName: "<environment-display-name>",
  databaseName: "<cluster-display-name>"
)
```
Then read results:
```
mcp__confluent__read-flink-statement(statementName: "show-tables-check", environmentId: "<env-id>")
```
Look for the CDC topic table (e.g., `postgres-cdc.public.customers`). If not present, the connector hasn't produced data yet — wait and retry.

**Step 2: Create target table:**
```
mcp__confluent__create-flink-statement(
  statementName: "cdc-create-target-customers",
  statement: "CREATE TABLE `target_customers` (...) WITH ('changelog.mode' = 'upsert');",
  environmentId, computePoolId, catalogName, databaseName
)
```

**Step 3: Create INSERT job:**
```
mcp__confluent__create-flink-statement(
  statementName: "cdc-decode-customers",
  statement: "INSERT INTO `target_customers` SELECT ... FROM `postgres-cdc.public.customers`;",
  environmentId, computePoolId, catalogName, databaseName
)
```

The INSERT creates a continuous Flink job. Verify it transitions to RUNNING (not FAILED):
```
mcp__confluent__read-flink-statement(statementName: "cdc-decode-customers", environmentId)
```

**Common INSERT failures:**
- "Table does not exist" → CDC source table not yet auto-discovered; wait for connector
- "Incompatible types for sink column" → Type mismatch; check Debezium type mappings above
- "Unsupported format" → Remove any explicit format properties from CREATE TABLE

**Advisory warnings (can be ignored):**
- "Primary key does not match upsert key" — Expected for CDC decode patterns
- "Highly state-intensive operators without TTL" — Advisory; set TTL if needed for production

#### 3.4 Enable Tableflow

**Using MCP:**
```
mcp__confluent__create-tableflow-topic(
  tableflowTopicConfig: {
    "display_name": "target_customers",
    "storage": { "kind": "Managed", "bucket_name": "managed", "provider_integration_id": "managed" },
    "table_formats": ["ICEBERG"],
    "config": { "record_failure_strategy": "SUSPEND", "retention_ms": "6048000000" }
  }
)
```

**KNOWN LIMITATION:** The MCP `create-tableflow-topic` tool does NOT accept `environmentId` or `clusterId` parameters. It defaults to the cluster configured in the MCP server. If the MCP server points to a different cluster than where the target topic exists, this will fail with "topic not found". Use the CLI or UI as a workaround.

**Using CLI:**
```bash
# Managed storage (Confluent manages S3)
confluent tableflow topic enable target_customers \
  --cluster <cluster-id> \
  --environment <env-id> \
  --storage-type MANAGED \
  --table-formats ICEBERG

# BYOB / BYOS (user's own S3 bucket)
confluent tableflow topic enable target_customers \
  --cluster <cluster-id> \
  --environment <env-id> \
  --storage-type BYOS \
  --provider-integration <provider-integration-id> \
  --bucket-name <bucket-name> \
  --table-formats ICEBERG

# Azure Data Lake Storage Gen2
confluent tableflow topic enable target_customers \
  --cluster <cluster-id> \
  --environment <env-id> \
  --storage-type AzureDataLakeStorageGen2 \
  --provider-integration <provider-integration-id> \
  --storage-account-name <account-name> \
  --container-name <container-name> \
  --table-formats DELTA
```

Use `--table-formats DELTA` for Delta Lake instead of Iceberg.

**Verify Tableflow is enabled:**
```
mcp__confluent__list-tableflow-topics(environmentId, clusterId)
```

Or via CLI:
```bash
confluent tableflow topic describe target_customers --cluster <cluster-id> --environment <env-id>
confluent tableflow topic list --cluster <cluster-id> --environment <env-id>
```
Status will transition from `PENDING` → `ACTIVE`.

### Phase 4: Verification & Troubleshooting

#### 4.1 Verify End-to-End Pipeline

**Large Table Snapshots:** If the connector was created with `snapshot.mode: initial` on a large table, verification may take hours. To distinguish a running snapshot from a broken pipeline:
1. Confirm connector has tasks assigned (`read-connector` → `tasks` is non-empty)
2. Confirm schemas are registered (`list-schemas` → key/value schemas exist) — this means the snapshot has started producing
3. Monitor the source topic message count in Confluent Cloud UI — a steady stream means progress

If you used `snapshot.mode: schema_only` for initial validation, insert a test row in the source database to trigger a CDC event and verify the full pipeline. See `references/troubleshooting.md` for detailed snapshot troubleshooting.

**Check each component:**

| Check | MCP Tool | What to Look For |
|-------|----------|-----------------|
| Connector running | `read-connector` | `tasks` array is non-empty |
| Schemas registered | `list-schemas(subjectPrefix)` | Key and value schemas for CDC topic |
| CDC table in Flink | `create-flink-statement("SHOW TABLES")` | CDC topic appears as table |
| Flink job running | `read-flink-statement` | No error in response |
| Target topic has data | `consume-messages(topicNames)` | Messages appear (note: consumer starts at latest offset) |
| Tableflow enabled | `list-tableflow-topics` | Status is PENDING or ACTIVE |

**Consume from target topic to verify decoded data:**
```
mcp__confluent__consume-messages(
  topicNames: ["target_customers"],
  value: { "useSchemaRegistry": true },
  key: { "useSchemaRegistry": true },
  maxMessages: 5,
  timeoutMs: 15000
)
```

Note: The consumer starts at the latest offset. If the initial snapshot already completed, you may see 0 messages until a new database change occurs.

**Test real-time CDC by inserting a row in the source database** (adapt table name and columns to match the user's actual schema):
```sql
INSERT INTO public.customers (name, email, created_at)
VALUES ('Test User', 'test@example.com', NOW());
```

#### 4.2 Troubleshooting

For detailed troubleshooting, see `references/troubleshooting.md`.

**Quick reference — pipeline-blocking issues:**

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Connector tasks stay empty | Still provisioning | Wait 2-5 minutes, retry |
| No schemas after 5 min | DB connectivity or credentials | Check host, port, user, password; verify DB CDC config |
| SHOW TABLES missing CDC table | Connector not producing yet | Verify schemas exist first, then wait |
| INSERT: "Incompatible types" | Debezium type mismatch | Use TIMESTAMP_LTZ(3) + TO_TIMESTAMP_LTZ; see `references/flink-sql-patterns.md` |
| Tableflow: "topic not found" | MCP cluster mismatch | Use CLI: `confluent tableflow topic enable` or Confluent Cloud UI |
| Topic exists but not in SHOW TABLES | No schema in SR | Register a JSON schema in SR or use schema inference; see `references/connector-configs.md` |

### Phase 5: Documentation

After successful setup, provide the user with:

1. **Pipeline Summary Table**: All component names, IDs, and statuses
2. **Topic Names**: Source CDC topic and target topic (with schema format used)
3. **Monitoring**: Check connector, Flink job, and Tableflow status in Confluent Cloud UI
4. **Test Command**: SQL INSERT to verify real-time CDC

## References

- Database Prerequisites: `references/database-prerequisites.md`
- Connector Configurations: `references/connector-configs.md`
- Flink SQL Patterns: `references/flink-sql-patterns.md`
- Troubleshooting Guide: `references/troubleshooting.md`
- REST API Reference: `references/rest-api.md`
- Confluent Cloud Flink Docs: https://docs.confluent.io/cloud/current/flink/overview.md
- Tableflow Docs: https://docs.confluent.io/cloud/current/topics/tableflow/overview.md
- Debezium CDC Docs: https://debezium.io/documentation/
- Confluent MCP Server: https://github.com/confluentinc/mcp-confluent
