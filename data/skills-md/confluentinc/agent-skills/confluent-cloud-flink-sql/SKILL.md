---
name: confluent-cloud-flink-sql
description: "Write and debug Flink SQL that runs on Confluent Cloud, enforcing the CC-vs-Apache-Flink (OSS) dialect boundary. Use when the working directory is a Confluent Cloud Flink workspace, when a Flink SQL statement needs checking before it runs on a CC compute pool, or when the user mentions CC Flink, Confluent Cloud Flink SQL, the `confluent flink` CLI, a CFU compute pool, `CREATE CONNECTION`, or asks to check or debug Flink SQL whose runtime is Confluent Cloud. Also trigger when a Flink SQL question is posed and nothing establishes an Apache Flink OSS runtime. Do NOT trigger for: building or deploying Flink UDFs in Java (UDF/UDTF/PTF — use flink-udf); a full CDC pipeline from a database through Flink into Tableflow/Iceberg/Delta Lake (use confluent-cloud-cdc-tableflow); Kafka Streams topology work (use kafka-streams-programming); or Flink SQL confirmed to run on Apache Flink OSS, not Confluent Cloud."
compatibility: Requires the `confluent` CLI (authenticated session) and an active Confluent Cloud compute pool — statement runs consume CFUs. Terraform is optional, needed only if managing `CREATE CONNECTION` credentials via the Confluent Terraform provider.
metadata:
  author: confluent
  version: "1.1.0"
  last_updated: "2026-09-18"
---

# Confluent Cloud Flink SQL

Enforce the CC-Flink-vs-OSS-Flink dialect boundary and the CLI-driven verification loop for any Confluent Cloud Flink SQL work. Apache Flink OSS training data is a trap — CC rejects or silently mishandles a long list of otherwise-valid Flink SQL constructs.

Scope note: this skill's reference material is built around the OSS-vs-CC dialect boundary — traps in constructs that exist in both dialects but behave differently. It does not yet catalog CC-only DDL that has no OSS counterpart (e.g. `CREATE MATERIALIZED TABLE`, `CREATE MODEL`/`AI_COMPLETE`, `CREATE AGENT`, `USE CATALOG`). For those, verify directly against the [CC Flink SQL reference](https://docs.confluent.io/cloud/current/flink/reference/overview.md) rather than expecting a trap entry here.

## Non-negotiables

1. **CC Flink ≠ Apache Flink.** Verify every API, SQL construct, and runtime behavior against:
   - [Confluent Cloud Flink docs](https://docs.confluent.io/cloud/current/flink/overview.md)
   - [CC Flink SQL reference](https://docs.confluent.io/cloud/current/flink/reference/overview.md)
   - [Confluent Terraform provider](https://registry.terraform.io/providers/confluentinc/confluent/latest/docs)
   - Live `confluent flink shell` against the user's compute pool
2. **No mocks in verification.** Integration claims require real `confluent` CLI runs. Unit tests may mock; anything calling itself "end-to-end verification" may not.
3. **Record decisions somewhere durable.** Ask the user where they want dialect traps and verification notes tracked (e.g. `docs/flink-dialect-traps.md` in their project) before writing any new file — don't assume a `docs/` layout.
4. **Secrets never in repo.** `CREATE CONNECTION` parameters are Terraform-injected, never hardcoded. Gitignore `.tfvars`, `.tfstate*`, `*.secret*` from day one.
5. **EXPLAIN before CREATE.** Always `EXPLAIN` a query before `statement create` — catches parse/type errors without consuming CFUs.
6. **Don't invent identifiers.** Use `<placeholder>` for any topic, table, statement, or resource name you haven't verified.

## Stream Processing Workflow

When a user asks to build, modify, or troubleshoot a Flink SQL streaming solution, first understand the streaming problem and identify the required data and processing semantics before generating SQL.

Use this workflow:

1. Understand the requirement
2. Discover existing Confluent resources
3. Establish the required streaming semantics (when needed)
4. Propose the processing design (when needed)
5. Confirm the design before modifying resources
6. Generate and validate Flink SQL
7. Execute the statement when explicitly approved
8. Observe and verify the result

Do not ask clarifying questions if a request is complete (i.e., all required information, context, and parameters are provided or retrievable via available MCP tools). Skip directly to implementation and validation. 

Only ask questions when critical information is missing and cannot be resolved through existing context or tools.

### 1. Understand the Requirement

Before generating Flink SQL, determine what the user is trying to accomplish.

Establish, when relevant:

- What streaming problem is being solved?
- What data/events should be processed?
- What are the input sources?
- What should the output represent?
- Where should the output go?
- What business conditions determine which records are processed?
- What are the required time semantics?
- What should happen with duplicates, late events, or invalid data?
- Are there important assumptions that could change the result?

Ask only questions that materially affect the pipeline design.

Do not ask for information that is already available in the conversation.

### 2. Discover Existing Confluent Resources

When MCP tools are available, prefer inspecting existing Confluent resources over asking the user for information that can be discovered.

For referenced input resources:

1. Find the relevant topic/table.
2. Inspect its schema.
3. Inspect representative records when necessary.
4. Identify relevant keys and timestamp fields.
5. Confirm the fields required by the proposed transformation.
6. Identify the target resource if it already exists.

Do not invent topic names, table names, column names, schemas, or timestamp fields.

If multiple resources could match the request, present the candidates and ask the user to select one.

### 3. Establish Streaming Semantics (when needed)

Before generating SQL, determine the semantics that materially affect the result. Skip this step if all relevant semantics are already established from the user's prompt or the discovery step.

Examples include:

- Event time vs processing time
- Window duration and behavior
- Grouping keys
- Join keys and temporal semantics
- Deduplication key and ordering
- Late-event handling
- Output granularity
- Whether the result represents individual events, aggregates, alerts, or another derived stream

### 4. Propose the Processing Design (when needed)

For non-trivial requests, summarize the proposed design before generating executable SQL. For simple, fully specified requests, this can be reduced to a brief summary or skipped entirely.

Use:

**Input**
- Relevant topic/table(s)
- Relevant fields

**Processing**
- Main transformations
- Joins/enrichment
- Aggregation/windowing
- Other required operations

**Output**
- Target topic/table
- Output semantics

**Assumptions**
- Material assumptions that have not been explicitly specified

Ask the user to confirm or correct the design before creating or modifying resources.

### 5. Plan Before Execute

Before creating, modifying, or deleting a Confluent resource, present the execution plan.

The plan should identify:

1. Resources that will be inspected.
2. SQL that will be validated.
3. Statements/resources that will be created or modified.
4. MCP tools or CLI commands that will be used.
5. How the resulting pipeline will be verified.

Wait for explicit user confirmation before performing resource-modifying operations.

Read-only discovery and inspection may be performed before confirmation.

### 6. Generate and Validate Flink SQL

After the design is confirmed, generate and validate the SQL:

1. Generate the Flink SQL.
2. Validate it against the Confluent Cloud Flink SQL dialect.
3. Use `EXPLAIN` where appropriate to catch parse/type errors without consuming CFUs.
4. Follow the existing resource-modification and safety guidance.

Use the existing dialect, SQL pattern, CLI, and troubleshooting references for implementation details.

### 7. Execute the Statement

Create or modify the Flink statement only after receiving explicit user confirmation:

1. Create the statement using the CLI or MCP tools.
2. Wait for the statement to reach RUNNING state.
3. Surface any PENDING or FAILED states immediately — do not silently retry.

### 8. Observe and Verify the Result

After the statement is running:

1. Inspect a sample of records from the output topic to confirm that expected records are being produced.
2. Monitor statement status and exceptions.
3. If the output is unexpected, inspect the input data and statement configuration before making changes.

### Requirements Gathering Guardrails

Requirements gathering must be adaptive rather than a fixed questionnaire.

- Do not ask for information already provided.
- Do not ask for information that can be reliably discovered through available MCP tools.
- Do not ask every possible question before performing useful read-only discovery.
- Ask follow-up questions only when missing information materially affects correctness or semantics.
- Prefer a clearly stated, low-risk assumption over unnecessary questioning.
- When an assumption could materially change the result, ask the user to confirm it.

## Reference files

Load these on demand when the topic matches — do not read them all upfront:

| File | When to load |
|------|-------------|
| [references/dialect-traps.md](references/dialect-traps.md) | Before writing ANY Flink SQL — 22 CC-vs-OSS traps, single source of truth |
| [references/cli-reference.md](references/cli-reference.md) | Before running `confluent` CLI — flag schemas, carry-over recipe, timing, token expiry |
| [references/sql-patterns-cc.md](references/sql-patterns-cc.md) | When writing SQL — CC-validated patterns: windows, joins, dedup, MATCH_RECOGNIZE, JSON, External Tables |
| [references/formats-and-serialization.md](references/formats-and-serialization.md) | When configuring table formats — 7 supported formats, id-encoding, consume flags |
| [references/troubleshooting-cc.md](references/troubleshooting-cc.md) | When debugging errors — CC-specific error to cause to fix |
| [references/reserved-words.md](references/reserved-words.md) | When hitting parse errors — must-backquote identifiers |

## Red flags

Stop and consult `references/dialect-traps.md` if you catch yourself writing any of these:

- DataStream API (Java/Scala) — not supported on CC. Table API + PTF are GA in Java; Python Table API is Open Preview with no PTF yet
- `CREATE CATALOG ...` — catalog = CC environment, not creatable
- `SET 'execution.checkpointing.*'` — CC-managed, not settable
- `CREATE TABLE ... WITH ('connector' = 'kafka', ...)` — tables auto-map from topics
- `'value.format' = 'json'` — must be `'json-registry'` (or another SR-backed format)
- `WITH cte AS (...) INSERT INTO ...` — CC requires the CTE AFTER `INSERT INTO`
- `GROUP BY TUMBLE(ts, INTERVAL ...)` — must use the TVF form: `TUMBLE(TABLE t, DESCRIPTOR(ts), ...)`
- `LATERAL TABLE(UNNEST(...))` — parse error; use `CROSS JOIN UNNEST(...)`
- `PROCTIME()` — not supported; use External Tables/`KEY_SEARCH_AGG` or an event-time temporal join (avoid a regular join against an upsert-kafka topic — it retains the whole table in state)
- `CREATE FUNCTION f AS '...'` without `USING JAR` — CC UDFs require an uploaded artifact
- Savepoints / `STOP WITH SAVEPOINT` — not exposed on CC
- `--sql-file` flag — doesn't exist; use `--sql "$(cat file.sql)"`
- `DROP TABLE` — deletes the physical Kafka topic and its data on CC, not just metadata; confirm before running

## Verification loop

Canonical validation loop for any CC Flink SQL claim:

0. **EXPLAIN** the query in `flink shell` — catches syntax and type errors for free.
1. Write a minimal reproducer.
2. **Present the plan and wait for explicit user confirmation** before running anything that creates or modifies a real resource. State: the statement name and SQL, the compute pool/database/environment it targets, and any side effects (DDL creates a Kafka topic and Schema Registry subject; every run consumes CFUs). Do not proceed to step 3 without a go-ahead.
3. Run: `confluent flink statement create <name> --sql "$(cat repro.sql)" --compute-pool <id> --database <cluster> --environment <env> --wait`
4. Observe. Consume downstream: `confluent kafka topic consume <topic> --cluster <id> --from-beginning --value-format <matching-format> 2>/dev/null | grep -v '^%'` — match `<matching-format>` to the sink's `value.format` (see [references/formats-and-serialization.md](references/formats-and-serialization.md); `jsonschema` for `json-registry`, `avro` for `avro-registry`, `protobuf` for `proto-registry`, `string` for `raw`)
5. Record the command + output for later reference.

Escalation-required states (no silent workarounds):

- Statement `PENDING` > 60s → `confluent flink statement exception list <name> --cloud <provider> --region <region>`
- UDF deploy "jar not found" → `confluent flink artifact list --cloud <provider> --region <region>`
- Schema mismatch → `DESCRIBE <table>`, diff against the producer schema
- Egress denied → check `CREATE CONNECTION` + `USING CONNECTIONS` clause

See [references/cli-reference.md](references/cli-reference.md) for full flag schemas and timing expectations.

## Anti-patterns

- Apache Flink docs or Stack Overflow answers tagged `apache-flink` cited as CC authority
- LLM memory of "Flink SQL syntax" used without CC verification
- Mocking the `confluent` CLI in anything claiming end-to-end verification
- `terraform apply -auto-approve` on the first run of a root module
- Committing `.tfvars`, `.tfstate*`, `.terraform/`, `*.secret*`
- Swallowing Flink statement exceptions — fail loud; read `statement exception list`
- Hardcoded secrets in `CREATE CONNECTION` or UDF source

## Tutorials

[developer.confluent.io/tutorials/#flink](https://developer.confluent.io/tutorials/#flink) mixes OSS and CC tutorials.

**Filter rule:** Only use tutorials that list "Confluent Cloud" in prerequisites or use `confluent flink shell`. Apply the dialect trap table to any SQL copied from a tutorial — many target OSS Flink or Kafka Streams and are not CC-compatible as-is.

## Source-of-truth hierarchy

1. `references/dialect-traps.md` (this skill) — canonical, consolidated
2. Per-project `CLAUDE.md` — references this skill, adds project-specific context
3. A per-project trap log, if the user wants one kept — ask where before creating it

When a new trap is discovered during a session, tell the user so they can decide whether to record it in their project's own notes. Do not edit this skill's own installed files (`references/dialect-traps.md` or elsewhere) — propose the change and let the user (or a separate PR to this skill's repo) apply it.

## References

- [Confluent Cloud Flink docs](https://docs.confluent.io/cloud/current/flink/overview.md)
- [Confluent Cloud Flink SQL reference](https://docs.confluent.io/cloud/current/flink/reference/overview.md)
- [Confluent Terraform provider](https://registry.terraform.io/providers/confluentinc/confluent/latest/docs)
- [Confluent CLI reference — Flink](https://docs.confluent.io/confluent-cli/current/command-reference/flink/index.md)
- [Tutorials (filter for CC only)](https://developer.confluent.io/tutorials/#flink)
