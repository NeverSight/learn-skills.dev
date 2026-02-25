---
name: envio
description: Envio blockchain data stack — HyperSync, HyperIndex, HyperRPC; fast indexing and data APIs.
metadata:
  author: hairy
  version: "2026.2.9"
  source: Generated from https://github.com/enviodev/docs (docs), scripts at https://github.com/antfu/skills
---

> Skill is based on Envio docs (enviodev/docs), generated at 2026-02-09.

Envio provides high-performance blockchain data access and indexing: HyperSync (raw data API), HyperIndex (indexer + GraphQL), and HyperRPC (read-only JSON-RPC). This skill covers product choice, client usage, queries, API tokens, and supported networks.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | HyperSync, HyperIndex, HyperRPC; when to use each | [core-overview](references/core-overview.md) |
| HyperSync | Client setup, query shape, streaming, field selection | [core-hypersync](references/core-hypersync.md) |
| HyperIndex | config.yaml, schema.graphql, event handlers, deployment | [core-hyperindex](references/core-hyperindex.md) |
| HyperRPC | When to use, supported methods, endpoint and token | [core-hyperrpc](references/core-hyperrpc.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| API Tokens | Generation, usage in clients, security | [features-api-tokens](references/features-api-tokens.md) |
| Supported Networks | HyperSync/HyperRPC URLs and tiers | [features-networks](references/features-networks.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Query Design | Field selection, join modes, limits, streaming, tip handling | [best-practices-queries](references/best-practices-queries.md) |
