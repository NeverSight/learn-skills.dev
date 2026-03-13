---
name: rill-clickhouse
description: Use when reviewing, refactoring, or creating ClickHouse-targeted Rill models from source info with diagnostics, rule-cited findings, and approval-gated edits.
---

# Rill ClickHouse Model Workflow

This skill orchestrates `$rilldata` and `$clickhouse-best-practices` for two modes:

- **Mode A: Review/Refactor Existing Model**
- **Mode B: Create ClickHouse Model From Scratch (for example from S3 path/source info)**

Keep existing model intent when refactoring and avoid unnecessary churn.

## 1. Prerequisite Check (Hard Gate)

1. Confirm the `clickhouse-best-practices` skill is available and installed from `https://github.com/ClickHouse/agent-skills`.
2. If the skill is missing or install origin cannot be confirmed, stop immediately and help the user install it with:

```bash
npx skills add clickhouse/agent-skills
```

3. After providing the install command, instruct the user to rerun the task once installation is complete.
4. Do not run diagnostics, propose plans, or generate model files until the prerequisite is satisfied.

## 2. Load Required Guidance

Always load relevant guidance from both skill sets.

Rill rule files:
- `../rilldata/rules/runtime-model.md` (source: `https://github.com/rilldata/rill/blob/main/runtime/ai/instructions/data/resources/model.md`)
- `../rilldata/rules/project-files-models.md` (source: `https://docs.rilldata.com/reference/project-files/models`)
- `../rilldata/rules/runtime-rillyaml.md` (source: `https://github.com/rilldata/rill/blob/main/runtime/ai/instructions/data/resources/rillyaml.md`)
- `../rilldata/rules/project-files-rill-yaml.md` (source: `https://docs.rilldata.com/reference/project-files/rill-yaml`)
- `../rilldata/rules/project-files-connectors.md` when connector definitions are needed (source: `https://docs.rilldata.com/reference/project-files/connectors`)

ClickHouse rules:
- Load applicable rules from `clickhouse-best-practices/rules/*`.
- Always include primary key/order, partitioning, data type, join, and index/skipping-index checks when relevant.

## 3. Startup

Start Rill with:

```bash
rill start . --no-ui --no-open --verbose --log-format json 2>&1 | tee /tmp/rill-no-ui.log
```

Keep the runtime available while running diagnostics.

## 4. Connector Resolution Logic

1. Read `rill.yaml` and capture `olap_connector`.
2. Determine effective output connector:
   - **Mode A:** Read target model YAML/SQL and determine explicit output connector (for example model-level `connector` or `output.connector` when present).
   - **Mode B:** Infer intended output from user request plus project defaults, and use project `olap_connector` when model output connector is not specified.
3. Connector decision:
   - If effective connector is `clickhouse`, proceed.
   - Otherwise stop and report the task is out of scope for this skill.

## 5. Query Diagnostics via Rill

Run diagnostics through `rill query` first, for example:

```bash
rill query --local --path . --connector clickhouse --sql "SELECT partition, count() AS parts, sum(rows) AS rows FROM system.parts WHERE active AND table='<model-name>' GROUP BY partition ORDER BY partition DESC LIMIT 20" --limit 20
```

Also run model-aware variants for additional target tables when needed (for joins, staging tables, or referenced outputs).

## 6. Dev-Data Sufficiency Rule

In `dev`, if returned rows/partitions are too limited to support a confident ClickHouse best-practice assessment:

1. Increase both SQL `LIMIT` and CLI `--limit` together using steps such as `20 -> 100 -> 500 -> 1000`.
2. After each increase, re-run diagnostics and reassess evidence quality.
3. Record:
   - original limits
   - updated limits
   - why the increase was needed
4. Stop increasing once evidence is sufficient. Do not use unnecessarily high limits.

## 7. Mode A: Review / Refactor Existing Model

1. Analyze existing model SQL/YAML plus runtime diagnostics.
2. Evaluate against applicable ClickHouse and Rill rules.
3. Prepare minimal, intent-preserving refactor plan before any edits.

## 8. Mode B: Create Model From Scratch

### 8.1 Parameter Checklist Template (Required Before SQL/YAML)

Always output a checklist template and fill what is known before producing model YAML/SQL:

- target model name
- source connector/type (for example `s3`, `gcs`, `https`, warehouse connector)
- source path/URI or table reference
- file/data format (`Parquet`, `CSV`, `JSON`, table)
- event time column (if available)
- expected grain and primary query/filter patterns
- date partition hints from path/table (if any)
- expected volume and refresh expectations
- environment assumptions (`dev`/`prod`)
- existing connector resources found in project

### 8.2 Best-Effort Input Policy

1. Use known inputs first.
2. Ask targeted follow-up questions only for missing fields that materially affect correctness.
3. Continue with safe defaults for non-critical unknowns.
4. Explicitly document assumptions before approval.

### 8.3 Model Creation Defaults

Use a conservative baseline unless evidence supports more:

- `type: model`
- `materialize: true`
- explicit ClickHouse output targeting behavior aligned with project defaults
- `output.order_by` is required for materialized ClickHouse tables

If source info indicates date-like partitioned paths/tables (for example `year=.../month=.../day=...`), prefer incremental partitioned shape:

- `incremental: true`
- `partitions.glob` (or equivalent partition declaration)
- partition-aware SQL using `{{ .partition.uri }}` where appropriate

Set `output.primary_key` and `output.partition_by` only when supported by observed source structure, query patterns, or diagnostics evidence.

### 8.4 Artifact Policy

After approval:

- Create or update the target model file.
- Create or update connector YAML only if the required connector is missing or invalid.
- Keep edits minimal and consistent with existing project conventions.

## 9. Rule-Driven Review (Both Modes)

Evaluate findings and/or generated design against applicable ClickHouse rules and Rill constraints.

ClickHouse focus (as applicable):
- PK/order design and filter alignment
- partition strategy and lifecycle
- data type selection
- joins and join filtering strategy
- index/skipping-index opportunities

Rill focus:
- valid model syntax/properties
- connector/output semantics
- project-level default connector behavior

## 10. Planning and Approval Gate

1. Produce a concrete edit plan first.
2. Pause for user review and explicit approval.
3. Do not modify or create model/connector files before approval.
4. After approval, apply only approved edits.

## 11. Required Output Format

Use exactly these sections:

- `## Rules Checked`
- `## Findings`
- `## Proposed Plan`
- `## User Approval Status`
- `## Applied Changes`
- `## Verification Results`

Additional requirements:

- In create-from-scratch tasks, include the completed parameter checklist and explicit assumptions in `## Findings`.
- If approval has not been granted, `## Applied Changes` must state that no changes were made.

## 12. Citation Requirements

1. Cite each ClickHouse rule by rule name (for example `schema-pk-plan-before-creation`).
2. Cite each consulted Rill rule file by filename and include the corresponding source URL.
