---
name: turbo-builder
description: "Use this skill when the user wants to build, create, or set up a new Goldsky Turbo pipeline from scratch. Triggers when someone describes data they want to move — specifying a source (chain, dataset, contract) and a destination (postgres, clickhouse, kafka, s3, webhook) — or asks to be walked through pipeline creation. Also triggers for phrases like 'help me build', 'I want to index', 'set up a pipeline', or 'track X on Y chain'. Covers the full workflow: gathering requirements, selecting datasets, generating YAML, validating, and deploying. Do NOT use for debugging existing pipelines (use /turbo-doctor), YAML syntax lookups (use /turbo-pipelines), or questions about specific fields/configuration options without intent to build."
---

# Pipeline Builder

## Boundaries

- Build NEW pipelines. Do not diagnose broken pipelines — that belongs to `/turbo-doctor`.
- Do not serve as a YAML reference. If the user only needs to look up a field or syntax, use the `/turbo-pipelines` skill instead.
- For dataset lookups, use `/datasets`.

Walk the user through building a complete pipeline from scratch, step by step. Generate a valid YAML configuration, validate it, and deploy it.

## Mode Detection

Before running any commands, check if you have the `Bash` tool available:

- **If Bash is available** (CLI mode): Execute commands, validate YAML, and deploy directly.
- **If Bash is NOT available** (reference mode): Generate the complete YAML configuration and provide copy-paste instructions for the user to validate and deploy manually.

## Builder Workflow

### Step 1: Verify Authentication

Run `goldsky project list 2>&1` to check login status.

- **If logged in:** Note the current project and continue.
- **If not logged in:** Use the `/auth-setup` skill for guidance.

### Step 2: Understand the Goal

Ask the user what they want to index. Good questions:

- What blockchain/chain? (Ethereum, Base, Polygon, Solana, etc.)
- What data? (transfers, swaps, events from a specific contract, all transactions, etc.)
- Where should the data go? (PostgreSQL, ClickHouse, Kafka, S3, etc.)
- Do they need transforms? (filtering, aggregation, enrichment)
- One-time backfill or continuous streaming?

If the user already described their goal, extract answers from their description.

### Step 3: Choose the Dataset

Use the `/datasets` skill to find the right dataset.

Key points:
- Common datasets: `<chain>.decoded_logs`, `<chain>.raw_transactions`, `<chain>.erc20_transfers`, `<chain>.raw_traces`
- For decoded contract events, use `<chain>.decoded_logs` with a filter on `address` and `topic0`
- For Solana: use `solana.transactions`, `solana.token_transfers`, etc.

Present the dataset choice to the user for confirmation.

### Step 4: Configure the Source

Build the source section of the YAML:

```yaml
sources:
  my_source:
    type: dataset
    dataset_name: <chain>.<dataset>
    version: 1.0.0
    start_at: earliest  # or a specific block number
```

Ask about:
- **Start block:** `earliest` (from genesis), `latest` (from now), or a specific block number
- **End block:** Only for job-mode/backfill pipelines. Omit for streaming.
- **Source-level filter:** Optional filter to reduce data at the source (e.g., specific contract address)

### Step 5: Configure Transforms (if needed)

If the user needs transforms, use the `/turbo-transforms` skill to help:

- **SQL transforms** — filter, aggregate, join, or reshape data using DataFusion SQL
- **TypeScript transforms** — custom logic, external API calls, complex processing
- **Dynamic tables** — join with a PostgreSQL table or in-memory allowlist

Build the transforms section:

```yaml
transforms:
  my_transform:
    type: sql
    primary_key: id
    sql: |
      SELECT * FROM my_source
      WHERE <conditions>
```

### Step 6: Configure the Sink

Ask where the data should go. Use the `/turbo-pipelines` skill for sink configuration:

| Sink | Key config |
|------|-----------|
| PostgreSQL | `secret_name`, `schema`, `table`, `primary_key` |
| ClickHouse | `secret_name`, `table`, `order_by` |
| Kafka | `secret_name`, `topic` |
| S3 | `bucket`, `region`, `prefix`, `format` |
| Webhook | `url`, `format` |

For sinks requiring `secret_name`, check if the secret exists:

```bash
goldsky secret list
```

If it doesn't exist, help create it using the `/secrets` skill.

### Step 7: Choose Mode

Use the `/turbo-architecture` skill to decide:

- **Streaming** (default) — continuous processing, no `end_block`, runs indefinitely
- **Job mode** — one-time backfill, set `job: true` and `end_block`

### Step 8: Generate, Validate, and Present

Assemble the complete pipeline YAML. Use a descriptive name following the convention: `<chain>-<data>-<sink>` (e.g., `base-erc20-transfers-postgres`).

**CLI mode (Bash available):**

1. Write the YAML file to disk (e.g., `<pipeline-name>.yaml`).
2. Run validation BEFORE showing the YAML to the user:

```bash
goldsky turbo validate -f <pipeline-name>.yaml
```

3. If validation fails, fix the issues and re-validate. Do NOT present the YAML until validation passes. Common fixes:
   - Missing `version` field on dataset source
   - Invalid dataset name (check chain prefix)
   - Missing `secret_name` for database sinks
   - SQL syntax errors in transforms

4. Once validation passes, present the full YAML to the user for review.

**Reference mode (no Bash):**

1. Perform the structural self-check from `turbo-pipelines/references/validation-checklist.md`.
2. Present the YAML with the checklist results.
3. Instruct the user to run `goldsky turbo validate -f <file>.yaml` before deploying.

### Step 9: Deploy

After user confirms the YAML looks good:

```bash
goldsky turbo apply <pipeline-name>.yaml
```

### Step 10: Verify

After deployment:

```bash
goldsky turbo list
```

Suggest running inspect to verify data flow:

```bash
goldsky turbo inspect <pipeline-name>
```

Present a summary:

```
## Pipeline Deployed

**Name:** [name]
**Chain:** [chain]
**Dataset:** [dataset]
**Sink:** [sink type]
**Mode:** [streaming/job]

**Next steps:**
- Monitor with `goldsky turbo inspect <name>`
- Check logs with `goldsky turbo logs <name>`
- Use /turbo-doctor if you run into issues
```

## Important Rules

- Always validate before presenting complete YAML to the user. Never show unvalidated complete pipeline YAML.
- Always validate before deploying.
- Always show the user the complete YAML before deploying.
- For job-mode pipelines, remind the user they auto-cleanup ~1hr after completion.
- Use `blackhole` sink for testing pipelines without writing to a real destination.
- If the user wants to modify an existing pipeline, check if it's streaming (update in place) or job-mode (must delete first).
- Default to `start_at: earliest` unless the user specifies otherwise.
- Always include `version: 1.0.0` on dataset sources.

## Related

- **`/turbo-pipelines`** — YAML syntax reference for sources, transforms, and sinks
- **`/turbo-doctor`** — Diagnose and fix pipeline issues
- **`/turbo-architecture`** — Pipeline design patterns and architecture decisions
- **`/turbo-transforms`** — SQL and TypeScript transform reference
- **`/datasets`** — Dataset names and chain prefixes
- **`/secrets`** — Sink credential management
