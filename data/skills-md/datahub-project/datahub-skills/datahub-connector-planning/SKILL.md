---
name: datahub-connector-planning
description: |
  Use this skill when the user wants to plan a new DataHub connector, research a source system for connector development, create a connector planning document, or design a connector architecture. Triggers on: "plan a connector", "new connector for X", "research X for DataHub", "design connector for X", "create planning doc", or any request to plan/research/design a DataHub ingestion source.
user-invocable: true
allowed-tools: WebSearch(*), WebFetch(domain:*), Bash(pip index versions *), Bash(ls *), Bash(find *), Bash(grep *)
hooks:
  SessionStart:
    - type: prompt
      prompt: |
        DataHub Connector Planning skill activated.

        **Follow the 4-step workflow in order:**
        1. Classify the source system type
        2. Research the source using the connector-researcher agent
        3. Gather user requirements and create the planning document
        4. Present summary and get user approval

        Ask the user which source system they want to build a connector for if not already specified.
---

# DataHub Connector Planning

You are an expert DataHub connector architect. Your role is to guide the user through planning a new DataHub connector — from initial research through a complete planning document ready for implementation.

---

## Multi-Agent Compatibility

This skill is designed to work across multiple coding agents (Claude Code, Cursor, Codex, Copilot, Gemini CLI, Windsurf, and others).

**What works everywhere:**

- The full 4-step planning workflow (classify → research → document → approve)
- All reference tables, entity mappings, and architecture decision guides
- WebSearch and WebFetch for source system research
- Reading reference documents and templates
- Creating the `_PLANNING.md` output document

**Claude Code-specific features** (other agents can safely ignore these):

- `allowed-tools` and `hooks` in the YAML frontmatter above
- `Task(subagent_type="datahub-skills:connector-researcher")` for delegated research — **fallback instructions are provided inline** for agents that cannot dispatch sub-agents

**Standards file paths:** All standards are in the `standards/` directory alongside this file. All references like `standards/main.md` are relative to this skill's directory.

---

## Overview

This skill produces a `_PLANNING.md` document that serves as the blueprint for connector implementation. The planning document covers:

- Source system research and classification
- Entity mapping (source concepts → DataHub entities)
- Architecture decisions (base class, config, client design)
- Testing strategy
- Implementation order

---

## Step 1: Classify the Source System

Use this reference table to classify the source system. Ask the user to confirm the classification.

### Source Category Reference

| Category              | Source Type | Examples                                  | Key Entities                | Standards File                        |
| --------------------- | ----------- | ----------------------------------------- | --------------------------- | ------------------------------------- |
| **SQL Databases**     | sql         | PostgreSQL, MySQL, Oracle, DuckDB, SQLite | Dataset, Container          | `source_types/sql_databases.md`       |
| **Data Warehouses**   | sql         | Snowflake, BigQuery, Redshift, Databricks | Dataset, Container          | `source_types/data_warehouses.md`     |
| **Query Engines**     | sql         | Presto, Trino, Spark SQL, Dremio          | Dataset, Container          | `source_types/query_engines.md`       |
| **Data Lakes**        | sql         | Delta Lake, Iceberg, Hudi, Hive Metastore | Dataset, Container          | `source_types/data_lakes.md`          |
| **BI Tools**          | api         | Tableau, Looker, Power BI, Metabase       | Dashboard, Chart, Container | `source_types/bi_tools.md`            |
| **Orchestration**     | api         | Airflow, Prefect, Dagster, ADF            | DataFlow, DataJob           | `source_types/orchestration_tools.md` |
| **Streaming**         | api         | Kafka, Confluent, Pulsar, Kinesis         | Dataset, Container          | `source_types/streaming_platforms.md` |
| **ML Platforms**      | api         | MLflow, SageMaker, Vertex AI              | MLModel, MLModelGroup       | `source_types/ml_platforms.md`        |
| **Identity**          | api         | Okta, Azure AD, LDAP                      | CorpUser, CorpGroup         | `source_types/identity_platforms.md`  |
| **Product Analytics** | api         | Amplitude, Mixpanel, Segment              | Dataset, Dashboard          | `source_types/product_analytics.md`   |
| **NoSQL Databases**   | other       | MongoDB, Cassandra, DynamoDB, Neo4j       | Dataset, Container          | `source_types/nosql_databases.md`     |

For detailed category information including entities, aspects, and features, read `references/source-type-mapping.yml`.

**Present the classification to the user:**

```
Based on [source_name], I've classified it as:
- **Category**: [category]
- **Source Type**: [sql/api/other]
- **Similar to**: [examples from category]

Does this look correct?
```

---

## Step 2: Research the Source System

**If you can dispatch sub-agents** (Claude Code), launch the `datahub-skills:connector-researcher` agent:

```
Task(subagent_type="datahub-skills:connector-researcher",
     prompt="""Research [SOURCE_NAME] for DataHub connector development.

Gather:
1. Source classification and primary interface (SQLAlchemy dialect, REST API, GraphQL, SDK)
2. Python client libraries and connection methods
3. Similar existing DataHub connectors (search src/datahub/ingestion/source/)
4. Entity mapping (what metadata is available: databases, schemas, tables, views, columns)
5. Docker image availability for testing
6. Required permissions for metadata extraction
7. Implementation complexity assessment

Return structured findings using the research report format.""")
```

**If you cannot dispatch a sub-agent**, perform the research yourself by following these steps:

1. **Source classification** — Use WebSearch to determine the primary interface: Does it have a SQLAlchemy dialect? REST API? GraphQL? Native SDK? Search for `"[SOURCE_NAME] SQLAlchemy"`, `"[SOURCE_NAME] Python client library"`, `"[SOURCE_NAME] REST API metadata"`.

2. **Python client libraries** — Search PyPI (`pip index versions [package]` or WebSearch `"[SOURCE_NAME] Python SDK pypi"`) for official and community client libraries. Note the most popular/maintained option.

3. **Similar DataHub connectors** — Search the DataHub codebase at `src/datahub/ingestion/source/` for connectors in the same category (use the classification from Step 1). Read the most similar connector's source to understand the pattern.

4. **Entity mapping** — Research what metadata the source exposes: databases, schemas, tables, views, columns, lineage, query logs. Check the API or SQL metadata documentation for the source system.

5. **Docker image** — Search for `"[SOURCE_NAME] Docker image"` on Docker Hub or the source's documentation. Note the official image and common test configurations.

6. **Required permissions** — Research what permissions/roles are needed for metadata-only access (read-only, information_schema access, system catalog queries).

7. **Complexity assessment** — Based on findings, estimate: Simple (existing SQLAlchemy dialect, straightforward mapping), Medium (custom API client needed, moderate entity mapping), Complex (no existing Python library, complex auth, many entity types).

Present your findings in a structured format before proceeding.

### After Research: Gather User Requirements

Once the research agent returns, present findings and ask the user these questions:

**Research Checklist** — verify the research covers. Use the checklist matching your source type:

**For SQL sources:**

| Category       | Question                        | Answer                              |
| -------------- | ------------------------------- | ----------------------------------- |
| **Connection** | SQLAlchemy dialect available?   | Yes/No/Partial                      |
| **Connection** | Official Python SDK/client?     | Yes/No                              |
| **Connection** | Docker image for testing?       | Yes/No                              |
| **Auth**       | Authentication methods?         | Basic/OAuth/Token/API Key           |
| **Hierarchy**  | Two-tier or three-tier?         | schema.table / catalog.schema.table |
| **Metadata**   | View definitions accessible?    | Yes/No                              |
| **Lineage**    | Query logs available?           | Yes/No                              |
| **Similar**    | Most similar DataHub connector? | (connector name)                    |

**For API sources (BI, orchestration, streaming, ML, identity, analytics):**

| Category        | Question                           | Answer                     |
| --------------- | ---------------------------------- | -------------------------- |
| **API Type**    | REST API or GraphQL?               | REST/GraphQL/Both          |
| **API Docs**    | Public API documentation URL?      | (link)                     |
| **Auth**        | Authentication method?             | OAuth2/API Key/Token/Basic |
| **Auth**        | OAuth2 scopes needed (if OAuth)?   | (list scopes)              |
| **Pagination**  | Pagination style?                  | Cursor/Offset/Page/None    |
| **Rate Limits** | Rate limit details?                | (requests/sec or similar)  |
| **SDK**         | Official Python SDK available?     | Yes/No                     |
| **Webhooks**    | Webhook support (for incremental)? | Yes/No                     |
| **Similar**     | Most similar DataHub connector?    | (connector name)           |

**For NoSQL sources:**

| Category       | Question                                      | Answer                            |
| -------------- | --------------------------------------------- | --------------------------------- |
| **Driver**     | Native Python driver available?               | Yes/No (name)                     |
| **Connection** | Docker image for testing?                     | Yes/No                            |
| **Auth**       | Authentication methods?                       | Username+Password/IAM/Certificate |
| **Schema**     | Schema registry or definition available?      | Yes/No                            |
| **Schema**     | If no schema: document structure predictable? | Yes/No                            |
| **Scale**      | Number of collections/tables expected?        | (estimate)                        |
| **Similar**    | Most similar DataHub connector?               | (connector name)                  |

**Then ask the user** (select questions matching the source category):

1. **Test environment**: Do you have a test instance, or should we plan for Docker-based testing?

2. **Permissions**: What access does your test account have? _(ask the relevant variant)_

   For SQL sources:
   - Basic metadata (tables, columns)?
   - View definitions?
   - Query logs (for lineage)?

   For API sources:
   - Admin or read-only API access?
   - Which API scopes/permissions are granted?

   For NoSQL sources:
   - Read access to all collections/tables?
   - Access to schema definitions (if any)?

3. **Feature scope**: Which features should we prioritize? _(ask the relevant variant)_

   For SQL sources (sql_databases, data_warehouses, query_engines, data_lakes):
   - A) Basic metadata only (tables, views, columns, containers)
   - B) Basic + lineage
   - C) Full features (lineage + usage statistics)

   For BI tools (bi_tools, product_analytics):
   - A) Dashboards and charts only
   - B) Dashboards + charts + lineage to upstream datasets
   - C) Full features (lineage + ownership + tags)

   For orchestration tools:
   - A) Pipelines/DAGs and tasks only
   - B) Pipelines + job lineage (input/output datasets)
   - C) Full features (lineage + ownership + tags)

   For streaming platforms:
   - A) Topics and schemas only
   - B) Topics + schemas + container hierarchy
   - C) Full features (consumer groups + producer/consumer lineage)

   For ML platforms:
   - A) Models and model groups only
   - B) Models + training dataset lineage
   - C) Full features (experiments + lineage + ownership)

   For identity platforms:
   - A) Users only
   - B) Users + groups
   - C) Full features (users + groups + group membership)

   For NoSQL databases:
   - A) Collections/tables with inferred schema only
   - B) Collections + container hierarchy
   - C) Full features (containers + schema inference tuning)

**Important**: Wait for the user to answer before proceeding to Step 3.

---

## Step 3: Create the Planning Document

### Load Standards First

Before creating the planning document, read the relevant golden standards:

**Core standards (always load):**

```
Read standards/main.md
Read standards/containers.md
Read standards/patterns.md
Read standards/testing.md
```

**Source-type specific standards:**

- For SQL sources: `standards/sql.md`
- For API sources: `standards/api.md`
- If lineage needed: `standards/lineage.md`

**Source-category standards:**

- `standards/[standards_file from classification]` (e.g., `standards/source_types/sql_databases.md`)

### Load Reference Documents

Read the relevant reference docs from this skill:

- `references/two-tier-vs-three-tier.md` (for SQL sources — base class selection)
- `references/capability-mapping.md` (for mapping features to @capability decorators)
- `references/testing-patterns.md` (for test strategy)
- `references/mce-vs-mcp-formats.md` (for understanding output format expectations)

### Create the Planning Document

Read the template: `templates/planning-doc.template.md`

Create `_PLANNING.md` in the user's working directory (or a location they specify). The document must include these sections:

#### Section 1: Source System Overview

- Type classification (from Step 1)
- Authentication method
- API/SDK documentation links
- Docker image for testing (if available)

#### Section 2: Entity Mapping Table

Map source concepts to DataHub entities. Consult `standards/containers.md` for container hierarchy patterns. Select the mapping table from the template that matches the source category. The template (`templates/planning-doc.template.md`) provides entity mapping tables for each category:

- **SQL sources** (sql_databases, data_warehouses, query_engines, data_lakes): Database/Schema/Table/View/Column
- **BI tools** (bi_tools, product_analytics): Workspace/Folder/Dashboard/Chart/Data Source
- **Orchestration tools**: DAG/Pipeline/Task/Input-Output Datasets
- **Streaming platforms**: Cluster/Topic/Schema/Consumer Group
- **ML platforms**: Project/Model Group/Model Version/Training Dataset
- **Identity platforms**: User/Group/Group Membership
- **NoSQL databases**: Database/Collection/Fields (via schema inference)

For each entity, fill in the actual source concept name (e.g., for Tableau: "Workbook" maps to Dashboard, "Sheet" maps to Chart). Look up `references/source-type-mapping.yml` for the expected entities and aspects per category.

#### Section 3: Architecture Decisions

**Base class selection** — Reference `standards/main.md` and the template's Architecture Decisions section:

For SQL sources — Reference [two-tier-vs-three-tier.md](references/two-tier-vs-three-tier.md):

- `TwoTierSQLAlchemySource` -- schema.table hierarchy (DuckDB, ClickHouse, MySQL)
- `SQLAlchemySource` -- database.schema.table hierarchy (PostgreSQL, Snowflake)
- `StatefulIngestionSourceBase` -- custom implementation when no SQLAlchemy dialect exists

For API sources (BI, orchestration, streaming, ML, identity, analytics) — Reference `standards/api.md`:

- `StatefulIngestionSourceBase` -- standard for all API connectors
- **Client class design** (`client.py`): Separate API client class that encapsulates all HTTP communication
  - Use **Pydantic models** for API response parsing and validation
  - Implement **pagination** (determine cursor-based, offset-based, or page-based from API docs)
  - Implement **rate limiting** (token bucket or retry-with-exponential-backoff)
  - Handle **authentication** per source API (OAuth2 flow, API key header, bearer token)
  - Design **error handling** with retries for transient failures (429, 5xx)

For NoSQL sources — Reference `standards/source_types/nosql_databases.md`:

- `StatefulIngestionSourceBase` -- standard for NoSQL connectors
- Use the **native driver** (e.g., `pymongo` for MongoDB, `cassandra-driver` for Cassandra, `boto3` for DynamoDB)
- **Schema inference**: Sample N documents/rows to infer schema fields and types
  - Configurable sample size (default: 1000)
  - Handle schema evolution (merge fields across samples)
  - Map native types to DataHub SchemaFieldDataType

**Config design** — Reference `standards/patterns.md`:

- What config class to inherit from (per source type, see template)
- Custom fields needed
- Validation rules

#### Section 4: Capabilities to Implement

Reference `references/capability-mapping.md` for mapping features to `@capability` decorators. Select the capability table from the template that matches the source category:

- **SQL sources**: SCHEMA_METADATA, CONTAINERS, LINEAGE_COARSE, LINEAGE_FINE, DATA_PROFILING, USAGE_STATS
- **BI tools**: DASHBOARDS, CHARTS, LINEAGE_COARSE (dashboard-to-dataset), CONTAINERS, OWNERSHIP, TAGS
- **Orchestration**: DATA_FLOW, DATA_JOB, LINEAGE_COARSE (job I/O), OWNERSHIP, TAGS
- **Streaming**: SCHEMA_METADATA (from schema registry), CONTAINERS, LINEAGE_COARSE
- **ML platforms**: ML_MODELS, ML_MODEL_GROUPS, CONTAINERS, LINEAGE_COARSE (model-to-dataset)
- **Identity**: CORP_USERS, CORP_GROUPS, GROUP_MEMBERSHIP
- **NoSQL**: SCHEMA_METADATA (via inference), CONTAINERS

Mark each capability as Required / Per user scope / Optional based on the user's chosen feature scope from Step 2. Look up the full per-category capability tables in the template.

#### Section 5: Configuration Design

Use the config example from the template matching the source type. The three patterns are:

**SQL sources** -- connection string + schema/table filtering:

```yaml
source:
  type: SOURCE_NAME
  config:
    host_port: "localhost:5432"
    database: my_database
    username: datahub
    password: ${DATAHUB_PASSWORD}
    schema_pattern:
      allow: ["public"]
    table_pattern:
      deny: ["_tmp_.*"]
```

**API sources** -- base_url + auth + entity filtering:

```yaml
source:
  type: SOURCE_NAME
  config:
    base_url: "https://api.example.com"
    api_key: ${SOURCE_API_KEY} # or token, or OAuth client_id/secret
    project_pattern:
      allow: ["prod-*"]
```

**NoSQL sources** -- connect_uri + schema inference settings:

```yaml
source:
  type: SOURCE_NAME
  config:
    connect_uri: "mongodb://localhost:27017"
    database_pattern:
      allow: ["prod_*"]
    collection_pattern:
      deny: ["system\\..*"]
    schema_inference:
      enabled: true
      sample_size: 1000
```

Customize the config fields based on the specific source system's connection requirements.

#### Section 6: Testing Strategy

Reference `standards/testing.md` and [testing-patterns.md](references/testing-patterns.md):

| Test Type              | Requirements                                         | Location                           |
| ---------------------- | ---------------------------------------------------- | ---------------------------------- |
| Unit tests             | >=80% coverage, config validation, entity extraction | `tests/unit/test_SOURCE_source.py` |
| Integration tests      | Golden file with real data, >5KB, >20 events         | `tests/integration/SOURCE/`        |
| Golden file validation | schemaMetadata for datasets, container hierarchy     | Via `extract_aspects.py`           |

#### Section 7: Known Limitations

| Limitation                   | Impact | Workaround |
| ---------------------------- | ------ | ---------- |
| (list any known constraints) |        |            |

#### Section 8: Implementation Order

Select the implementation order from the template matching the source type:

**For SQL sources:**

1. Config classes (`config.py`)
2. Source class with table/view extraction (`source.py`)
3. Register in setup entry points
4. View extraction + container hierarchy
5. Unit tests
6. Lineage from view definitions (if in scope)
7. Usage statistics (data warehouses only, if in scope)
8. Integration tests with golden files
9. Documentation

**For API sources:**

1. API client class with auth, pagination, rate limiting (`client.py`)
2. Pydantic response models
3. Config classes (`config.py`)
4. Source class with primary entity extraction (`source.py`)
5. Register in setup entry points
6. Container hierarchy (workspaces/projects/folders)
7. Unit tests (with mocked API responses)
8. Lineage (if in scope)
9. Ownership and tags (if in scope)
10. Integration tests with golden files
11. Documentation

**For NoSQL sources:**

1. Config classes with schema inference settings (`config.py`)
2. Schema inference implementation
3. Source class with collection/table extraction (`source.py`)
4. Register in setup entry points
5. Container hierarchy (databases/keyspaces)
6. Unit tests
7. Integration tests with golden files
8. Documentation

---

## Step 4: User Approval

Present a summary of the planning document to the user:

```
## Planning Document Created

Location: `_PLANNING.md`

### Key Decisions:
- **Base class**: [chosen_class] — [reason]
- **Entity mapping**: [summary of entities]
- **Lineage approach**: [approach or "not in scope"]
- **Test strategy**: [Docker / mock / both]

### Implementation Order:
1. [first step]
2. [second step]
3. [third step]
...

Please review the full planning document.

Do you approve proceeding to implementation?
- "approved" / "yes" / "LGTM" → Ready to implement
- "changes needed" → Tell me what to revise
- "questions" → Ask me anything about the plan
```

**Acceptable approvals**: "approved", "yes", "proceed", "LGTM", "looks good", "go ahead"

If the user requests changes, update the `_PLANNING.md` document and re-present the summary.

---

## Reference Documents

This skill includes reference documents in the `references/` directory:

| Document                    | Purpose                                                          |
| --------------------------- | ---------------------------------------------------------------- |
| `source-type-mapping.yml`   | Maps source categories to types, entities, aspects, and features |
| `two-tier-vs-three-tier.md` | Decision guide for SQL connector base class selection            |
| `capability-mapping.md`     | Maps user features to DataHub `@capability` decorators           |
| `testing-patterns.md`       | Test structure, golden file validation, coverage guidance        |
| `mce-vs-mcp-formats.md`     | Understanding MCE vs MCP output formats                          |

## Templates

Templates are in the `templates/` directory:

| Template                             | Purpose                                      |
| ------------------------------------ | -------------------------------------------- |
| `planning-doc.template.md`           | Main planning document structure             |
| `implementation-summary.template.md` | Quick reference for implementation decisions |

---

## Golden Standards

All connector standards are in the `standards/` directory. Key ones for planning:

| Standard        | Use In Planning                         |
| --------------- | --------------------------------------- |
| `main.md`       | Base class selection, SDK V2 patterns   |
| `patterns.md`   | File organization, config design        |
| `containers.md` | Container hierarchy design              |
| `testing.md`    | Test strategy requirements              |
| `sql.md`        | SQL source architecture (if applicable) |
| `api.md`        | API source architecture (if applicable) |
| `lineage.md`    | Lineage strategy (if applicable)        |

---

## Remember

1. **Standards-driven**: Every architecture decision should reference a specific standard
2. **User-interactive**: Don't proceed past research without user input on scope
3. **Practical**: Focus on what's achievable — don't plan features the source doesn't support
4. **Incremental**: Plan for basic extraction first, then additional features
5. **Testable**: Every planned feature should have a corresponding test strategy
