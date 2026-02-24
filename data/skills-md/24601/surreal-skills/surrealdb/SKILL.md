---
name: surrealdb
description: "Expert SurrealDB 3 architect and developer skill. SurrealQL mastery, multi-model data modeling (document, graph, vector, time-series, geospatial), schema design, security, deployment, performance tuning, SDK integration (JS, Python, Go, Rust), Surrealism WASM extensions, and full ecosystem (Surrealist, Surreal-Sync, SurrealFS). Universal skill for 30+ AI agents."
license: MIT
metadata:
  version: "1.0.5"
  author: "24601"
  snapshot_date: "2026-02-24"
  repository: "https://github.com/24601/surreal-skills"
requires:
  binaries:
    - name: surreal
      install: "brew install surrealdb/tap/surreal"
      purpose: "SurrealDB CLI for server management, SQL REPL, import/export"
      optional: false
    - name: python3
      version: ">=3.10"
      purpose: "Required for skill scripts (doctor.py, schema.py, onboard.py)"
      optional: false
    - name: uv
      install: "brew install uv"
      purpose: "PEP 723 script runner -- installs script deps automatically"
      optional: false
    - name: docker
      purpose: "Containerized SurrealDB instances"
      optional: true
  env_vars:
    - name: SURREAL_ENDPOINT
      purpose: "SurrealDB server URL"
      default: "http://localhost:8000"
      sensitive: false
    - name: SURREAL_USER
      purpose: "Authentication username"
      default: "root"
      sensitive: true
    - name: SURREAL_PASS
      purpose: "Authentication password"
      default: "root"
      sensitive: true
    - name: SURREAL_NS
      purpose: "Default namespace"
      default: "test"
      sensitive: false
    - name: SURREAL_DB
      purpose: "Default database"
      default: "test"
      sensitive: false
security:
  no_network: false
  no_network_note: "Scripts connect to a user-specified SurrealDB endpoint for health checks and schema introspection. No external/third-party network calls."
  no_credentials: false
  no_credentials_note: "Scripts accept SURREAL_USER/SURREAL_PASS for DB authentication. No credentials are stored in the skill itself."
  no_env_write: true
  no_file_write: true
  no_shell_exec: false
  no_shell_exec_note: "Scripts invoke surreal CLI and gh for health checks."
  scripts_auditable: true
  scripts_use_pep723: true
  no_obfuscated_code: true
  no_binary_blobs: true
  no_minified_scripts: true
  no_curl_pipe_sh: false
  no_curl_pipe_sh_note: "Documentation mentions curl|sh as ONE install option alongside safer alternatives (brew, Docker, package managers). The skill itself never executes curl|sh."
---

# SurrealDB 3 Skill

Expert-level SurrealDB 3 architecture, development, and operations. Covers SurrealQL, multi-model data modeling, graph traversal, vector search, security, deployment, performance tuning, SDK integration, and the full SurrealDB ecosystem.

## For AI Agents

Get a full capabilities manifest, decision trees, and output contracts:

```bash
uv run {baseDir}/scripts/onboard.py --agent
```

See [AGENTS.md]({baseDir}/AGENTS.md) for the complete structured briefing.

| Command | What It Does |
|---------|-------------|
| `uv run {baseDir}/scripts/doctor.py` | Health check: verify surreal CLI, connectivity, versions |
| `uv run {baseDir}/scripts/doctor.py --check` | Quick pass/fail check (exit code only) |
| `uv run {baseDir}/scripts/schema.py introspect` | Dump full schema of a running SurrealDB instance |
| `uv run {baseDir}/scripts/schema.py tables` | List all tables with field counts and indexes |
| `uv run {baseDir}/scripts/onboard.py --agent` | JSON capabilities manifest for agent integration |

## Prerequisites

- **surreal CLI** -- `brew install surrealdb/tap/surreal` (macOS) or see [install docs](https://surrealdb.com/docs/surrealdb/installation)
- **Python 3.10+** -- Required for skill scripts
- **uv** -- `brew install uv` (macOS) or `pip install uv` or see [uv docs](https://docs.astral.sh/uv/getting-started/installation/)

Optional:

- **Docker** -- For containerized SurrealDB instances (`docker run surrealdb/surrealdb:v3`)
- **SDK of choice** -- JavaScript, Python, Go, Rust, Java, .NET, C, PHP, or Dart

> **Security note**: This skill's documentation references package manager installs
> (brew, pip, cargo, npm, Docker) as the recommended install method. If you
> encounter `curl | sh` examples in the rules files, prefer your OS package
> manager or download-and-review workflow instead.

## Quick Start

> **Credential warning**: Examples below use `root/root` for **local development
> only**. Never use default credentials against production or shared instances.
> Create scoped, least-privilege users for non-local environments.

```bash
# Start SurrealDB in-memory for LOCAL DEVELOPMENT ONLY
surreal start memory --user root --pass root --bind 127.0.0.1:8000

# Start with persistent RocksDB storage (local dev)
surreal start rocksdb://data/mydb.db --user root --pass root

# Start with SurrealKV (time-travel queries supported, local dev)
surreal start surrealkv://data/mydb --user root --pass root

# Connect via CLI REPL (local dev)
surreal sql --endpoint http://localhost:8000 --user root --pass root --ns test --db test

# Import a SurrealQL file
surreal import --endpoint http://localhost:8000 --user root --pass root --ns test --db test schema.surql

# Export the database
surreal export --endpoint http://localhost:8000 --user root --pass root --ns test --db test backup.surql

# Check version
surreal version

# Run the skill health check
uv run {baseDir}/scripts/doctor.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SURREAL_ENDPOINT` | SurrealDB server URL | `http://localhost:8000` |
| `SURREAL_USER` | Root or namespace username | `root` |
| `SURREAL_PASS` | Root or namespace password | `root` |
| `SURREAL_NS` | Default namespace | `test` |
| `SURREAL_DB` | Default database | `test` |

These map directly to the `surreal sql` CLI flags (`--endpoint`, `--user`, `--pass`, `--ns`, `--db`) and are recognized by official SurrealDB SDKs.

## Core Capabilities

### SurrealQL Mastery

Full coverage of the SurrealQL query language: `CREATE`, `SELECT`, `UPDATE`, `UPSERT`, `DELETE`, `RELATE`, `INSERT`, `LIVE SELECT`, `DEFINE`, `REMOVE`, `INFO`, subqueries, transactions, futures, and all built-in functions (array, crypto, duration, geo, math, meta, object, parse, rand, string, time, type, vector).

See: `rules/surrealql.md`

### Multi-Model Data Modeling

Design schemas that leverage SurrealDB's multi-model capabilities -- document collections, graph edges, relational references, vector embeddings, time-series data, and geospatial coordinates -- all in a single database with a single query language.

See: `rules/data-modeling.md`

### Graph Queries

First-class graph traversal without JOINs. `RELATE` creates typed edges between records. Traverse with `->` (outgoing), `<-` (incoming), and `<->` (bidirectional) operators. Filter, aggregate, and recurse at any depth.

See: `rules/graph-queries.md`

### Vector Search

Built-in vector similarity search using HNSW and brute-force indexes. Define vector fields, create indexes with configurable distance metrics (cosine, euclidean, manhattan, minkowski), and query with `vector::similarity::*` functions. Build RAG pipelines and semantic search directly in SurrealQL.

See: `rules/vector-search.md`

### Security and Permissions

Row-level security via `DEFINE TABLE ... PERMISSIONS`, namespace/database/record-level access control, `DEFINE ACCESS` for JWT/token-based auth, `DEFINE USER` for system users, and `$auth`/`$session` runtime variables for permission predicates.

See: `rules/security.md`

### Deployment and Operations

Single-binary deployment, Docker, Kubernetes (Helm charts), storage engine selection (memory, RocksDB, SurrealKV, TiKV for distributed), backup/restore, monitoring, and production hardening.

See: `rules/deployment.md`

### Performance Tuning

Index strategies (unique, search, vector HNSW, MTree), query optimization with `EXPLAIN`, connection pooling, storage engine trade-offs, batch operations, and resource limits.

See: `rules/performance.md`

### SDK Integration

Official SDKs for JavaScript/TypeScript (Node.js, Deno, Bun, browser), Python, Go, Rust, Java, .NET, C, PHP, and Dart. Connection protocols (HTTP, WebSocket), authentication flows, live query subscriptions, and typed record handling.

See: `rules/sdks.md`

### Surrealism WASM Extensions

New in SurrealDB 3: extend the database with custom functions, analyzers, and logic written in Rust and compiled to WASM. Define, deploy, and manage Surrealism modules.

See: `rules/surrealism.md`

### Ecosystem Tools

- **Surrealist** -- Official IDE and GUI for SurrealDB (schema designer, query editor, graph visualizer)
- **Surreal-Sync** -- Change Data Capture (CDC) for migrations from other databases
- **SurrealFS** -- AI agent filesystem built on SurrealDB
- **SurrealML** -- Machine learning model management and inference within SurrealDB

See: `rules/surrealist.md`, `rules/surreal-sync.md`, `rules/surrealfs.md`

## Doctor / Health Check

```bash
# Full diagnostic (Rich output on stderr, JSON on stdout)
uv run {baseDir}/scripts/doctor.py

# Quick check (exit code 0 = healthy, 1 = issues found)
uv run {baseDir}/scripts/doctor.py --check

# Check a specific endpoint
uv run {baseDir}/scripts/doctor.py --endpoint http://my-server:8000
```

The doctor script verifies: surreal CLI installed and on PATH, server reachable, authentication succeeds, namespace and database exist, version compatibility, and storage engine status.

## Schema Introspection

```bash
# Full schema dump (all tables, fields, indexes, events, accesses)
uv run {baseDir}/scripts/schema.py introspect

# List tables with summary
uv run {baseDir}/scripts/schema.py tables

# Inspect a specific table
uv run {baseDir}/scripts/schema.py table <table_name>

# Export schema as SurrealQL (reproducible DEFINE statements)
uv run {baseDir}/scripts/schema.py export --format surql

# Export schema as JSON
uv run {baseDir}/scripts/schema.py export --format json
```

Introspection uses `INFO FOR DB`, `INFO FOR TABLE`, and `INFO FOR NS` to reconstruct the full schema.

## Rules Reference

| Rule File | Coverage |
|-----------|----------|
| `rules/surrealql.md` | SurrealQL syntax, statements, functions, operators, idioms |
| `rules/data-modeling.md` | Schema design, record IDs, field types, relations, normalization |
| `rules/graph-queries.md` | RELATE, graph traversal operators, path expressions, recursive queries |
| `rules/vector-search.md` | Vector fields, HNSW/brute-force indexes, similarity functions, RAG patterns |
| `rules/security.md` | Permissions, access control, authentication, JWT, row-level security |
| `rules/deployment.md` | Installation, storage engines, Docker, Kubernetes, production config |
| `rules/performance.md` | Indexes, EXPLAIN, query optimization, batch ops, resource tuning |
| `rules/sdks.md` | JavaScript, Python, Go, Rust SDK usage, connection patterns, live queries |
| `rules/surrealism.md` | WASM extensions, custom functions, Surrealism module authoring |
| `rules/surrealist.md` | Surrealist IDE/GUI usage, schema designer, query editor |
| `rules/surreal-sync.md` | CDC migration tool, source/target connectors, migration workflows |
| `rules/surrealfs.md` | AI agent filesystem, file storage, metadata, retrieval patterns |

## Workflow Examples

### New Project Setup

```bash
# 1. Verify environment
uv run {baseDir}/scripts/doctor.py

# 2. Start SurrealDB
surreal start rocksdb://data/myproject.db --user root --pass root

# 3. Design schema (use rules/data-modeling.md for guidance)
# 4. Import initial schema
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db production schema.surql

# 5. Introspect to verify
uv run {baseDir}/scripts/schema.py introspect
```

### Migration from SurrealDB v2

```bash
# 1. Export v2 data
surreal export --endpoint http://old-server:8000 --user root --pass root \
  --ns myapp --db production v2-backup.surql

# 2. Review breaking changes (see rules/surrealql.md v2->v3 migration section)
# Key changes: range syntax 1..4 is now exclusive of end, new WASM extension system

# 3. Import into v3
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db production v2-backup.surql

# 4. Verify schema
uv run {baseDir}/scripts/schema.py introspect
```

### Data Modeling for a New Domain

```bash
# 1. Read rules/data-modeling.md for schema design patterns
# 2. Read rules/graph-queries.md if your domain has relationships
# 3. Read rules/vector-search.md if you need semantic search
# 4. Draft schema.surql with DEFINE TABLE, DEFINE FIELD, DEFINE INDEX
# 5. Import and test
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns dev --db test schema.surql
uv run {baseDir}/scripts/schema.py introspect
```

### Deploying to Production

```bash
# 1. Read rules/deployment.md for storage engine selection and hardening
# 2. Read rules/security.md for access control setup
# 3. Read rules/performance.md for index strategy
# 4. Run doctor against production endpoint
uv run {baseDir}/scripts/doctor.py --endpoint https://prod-surreal:8000
# 5. Verify schema matches expectations
uv run {baseDir}/scripts/schema.py introspect --endpoint https://prod-surreal:8000
```

## Upstream Source Check

```bash
# Check if upstream SurrealDB repos have changed since this skill was built
uv run {baseDir}/scripts/check_upstream.py

# JSON-only output for agents
uv run {baseDir}/scripts/check_upstream.py --json

# Only show repos that have new commits
uv run {baseDir}/scripts/check_upstream.py --stale
```

Compares current HEAD SHAs and release tags of all tracked repos against the
baselines in `SOURCES.json`. Use this to plan incremental skill updates.

## Source Provenance

This skill was built on **2026-02-19** from these upstream sources:

| Repository | Release | Snapshot Date |
|------------|---------|---------------|
| [surrealdb/surrealdb](https://github.com/surrealdb/surrealdb) | v3.0.0 | 2026-02-19 |
| [surrealdb/surrealist](https://github.com/surrealdb/surrealist) | v3.7.2 | 2026-02-21 |
| [surrealdb/surrealdb.js](https://github.com/surrealdb/surrealdb.js) | v1.3.2 | 2026-02-20 |
| [surrealdb/surrealdb.js](https://github.com/surrealdb/surrealdb.js) (v2 beta) | v2.0.0-beta.1 | 2026-02-20 |
| [surrealdb/surrealdb.py](https://github.com/surrealdb/surrealdb.py) | v1.0.8 | 2026-02-03 |
| [surrealdb/surrealdb.go](https://github.com/surrealdb/surrealdb.go) | v1.3.0 | 2026-02-12 |
| [surrealdb/surreal-sync](https://github.com/surrealdb/surreal-sync) | v0.3.4 | 2026-02-12 |
| [surrealdb/surrealfs](https://github.com/surrealdb/surrealfs) | -- | 2026-01-29 |

Documentation: [surrealdb.com/docs](https://surrealdb.com/docs) snapshot 2026-02-22.

Machine-readable provenance: `SOURCES.json`.

## Output Convention

All Python scripts in this skill follow a dual-output pattern:

- **stderr**: Rich-formatted human-readable output (tables, panels, status indicators)
- **stdout**: Machine-readable JSON for programmatic consumption by AI agents

This means `2>/dev/null` hides the human output, and piping stdout gives clean JSON for downstream processing.
