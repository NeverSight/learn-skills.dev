---
name: spice-setup
description: Get started with Spice.ai — install the runtime, initialize a project, run the runtime, and use the CLI. Use when setting up a new Spice project, installing Spice, running spice run, looking up CLI commands, API endpoints, deployment models, or creating a spicepod.yaml.
---

# Getting Started with Spice

Spice is an open-source SQL query, search, and LLM-inference engine written in Rust. It federates queries across 30+ data sources, accelerates data locally, and integrates search and AI — all configured declaratively in YAML.

Spice is **not** a replacement for PostgreSQL/MySQL (use those for transactional workloads) or a data warehouse (use Snowflake/Databricks for centralized analytics). Think of it as the operational data & AI layer between your applications and your data infrastructure.

## Install

### macOS / Linux / WSL

```bash
curl https://install.spiceai.org | /bin/bash
```

### Homebrew

```bash
brew install spiceai/spiceai/spice
```

### Windows (PowerShell)

```powershell
iex ((New-Object System.Net.WebClient).DownloadString("https://install.spiceai.org/Install.ps1"))
```

### Verify & Upgrade

```bash
spice version
spice upgrade
```

If `command not found`, add to PATH: `export PATH="$PATH:$HOME/.spice/bin"`

## Quick Start

```bash
spice init my_app
cd my_app
spice run
```

In another terminal:

```bash
spice sql
sql> show tables;
```

## Spicepod Configuration (`spicepod.yaml`)

The Spicepod manifest defines all components for a Spice application:

```yaml
version: v1
kind: Spicepod
name: my_app

secrets:
  - from: env
    name: env

datasets:
  - from: <connector>:<path>
    name: <dataset_name>

models:
  - from: <provider>:<model>
    name: <model_name>

embeddings:
  - from: <provider>:<model>
    name: <embedding_name>
```

### All Sections

| Section        | Purpose                            | Skill              |
| -------------- | ---------------------------------- | ------------------ |
| `datasets`     | Data sources for SQL queries       | spice-connect-data |
| `models`       | LLM/ML models for inference        | spice-ai           |
| `embeddings`   | Embedding models for vector search | spice-search       |
| `secrets`      | Secure credential management       | spice-secrets      |
| `catalogs`     | External data catalog connections  | spice-connect-data |
| `views`        | Virtual tables from SQL queries    | spice-connect-data |
| `tools`        | LLM function calling capabilities  | spice-ai           |
| `workers`      | Model load balancing and routing   | spice-ai           |
| `runtime`      | Server ports, caching, telemetry   | spice-caching      |
| `snapshots`    | Acceleration snapshot management   | spice-acceleration |
| `evals`        | Model evaluation definitions       | spice-ai           |
| `dependencies` | Dependent Spicepods                | (below)            |

### Dependencies

```yaml
dependencies:
  - lukekim/demo
  - spiceai/quickstart
```

## CLI Commands

| Command                   | Description                      |
| ------------------------- | -------------------------------- |
| `spice init <name>`       | Initialize a new Spicepod        |
| `spice run`               | Start the Spice runtime          |
| `spice sql`               | Start interactive SQL REPL       |
| `spice chat`              | Start chat REPL (requires model) |
| `spice search`            | Perform embeddings-based search  |
| `spice add <spicepod>`    | Add a Spicepod dependency        |
| `spice datasets`          | List loaded datasets             |
| `spice models`            | List loaded models               |
| `spice catalogs`          | List loaded catalogs             |
| `spice status`            | Show runtime status              |
| `spice refresh <dataset>` | Refresh an accelerated dataset   |
| `spice login`             | Login to the Spice.ai Platform   |
| `spice version`           | Show CLI and runtime version     |
| `spice upgrade`           | Upgrade CLI to latest version    |

## Runtime Endpoints

| Service       | Default Address         | Protocol                  |
| ------------- | ----------------------- | ------------------------- |
| HTTP API      | `http://127.0.0.1:8090` | REST, OpenAI-compatible   |
| Arrow Flight  | `127.0.0.1:50051`       | Arrow Flight / Flight SQL |
| Metrics       | `127.0.0.1:9090`        | Prometheus                |
| OpenTelemetry | `127.0.0.1:50052`       | OTLP gRPC                 |

## HTTP API Paths

| Path                        | Description             |
| --------------------------- | ----------------------- |
| `POST /v1/sql`              | Execute SQL query       |
| `POST /v1/search`           | Embeddings-based search |
| `POST /v1/nsql`             | Natural language to SQL |
| `POST /v1/chat/completions` | OpenAI-compatible chat  |
| `POST /v1/embeddings`       | Generate embeddings     |
| `GET /v1/datasets`          | List datasets           |
| `GET /v1/models`            | List models             |
| `GET /health`               | Health check            |

## Deployment Models

Spice ships as a single ~140MB binary with no external dependencies.

| Model        | Best For                                              |
| ------------ | ----------------------------------------------------- |
| Standalone   | Development, edge devices, simple workloads           |
| Sidecar      | Low-latency access, microservices                     |
| Microservice | Heavy or varying traffic behind a load balancer       |
| Cluster      | Large-scale data, horizontal scaling                  |
| Cloud        | Auto-scaling, built-in observability (Spice.ai Cloud) |

## Use Cases

| Use Case                   | How Spice Helps                                                              |
| -------------------------- | ---------------------------------------------------------------------------- |
| Operational Data Lakehouse | Serve real-time workloads from Iceberg/Delta/Parquet with sub-second latency |
| Data Lake Accelerator      | Accelerate queries from seconds to milliseconds locally                      |
| Enterprise Search          | Combine semantic and full-text search across data                            |
| RAG Pipelines              | Federated data + vector search + LLMs                                        |
| Agentic AI                 | Tool-augmented LLMs with fast data access                                    |
| Real-Time Analytics        | Stream from Kafka/DynamoDB with sub-second latency                           |

## Full Example

```yaml
version: v1
kind: Spicepod
name: ai_app

secrets:
  - from: env
    name: env

embeddings:
  - from: openai:text-embedding-3-small
    name: embed
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }

datasets:
  - from: postgres:public.users
    name: users
    params:
      pg_host: localhost
      pg_user: ${ env:PG_USER }
      pg_pass: ${ env:PG_PASS }
    acceleration:
      enabled: true
      engine: duckdb
      refresh_check_interval: 5m

  - from: memory:store
    name: llm_memory
    access: read_write

models:
  - from: openai:gpt-4o
    name: assistant
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
      tools: auto, memory, search
```

## Documentation

- [Getting Started](https://spiceai.org/docs/getting-started)
- [Installation](https://spiceai.org/docs/installation)
- [Spicepod Reference](https://spiceai.org/docs/reference/spicepod)
- [CLI Reference](https://spiceai.org/docs/cli/reference)
- [API Reference](https://spiceai.org/docs/api)
