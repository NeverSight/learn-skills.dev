---
name: langfuse-model-list
description: List all Langfuse models with their pricing. Use when checking model costs, verifying pricing configuration, or getting an overview of model definitions.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-model-list.ts*)
---

# Langfuse Model List

List all registered models and their pricing information.

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Checking the model list
- Verifying pricing configuration
- "What models are available?"
- "I want to check pricing"

## Commands

### 1. Get Model List

```bash
npx tsx scripts/langfuse-model-list.ts
```

### 2. JSON Output (for programmatic processing)

```bash
npx tsx scripts/langfuse-model-list.ts --json
```

## Output Example

```
Langfuse Models
===============

Model Name                                        Input $/1M Output $/1M  Match Pattern
----------------------------------------------------------------------------------------------------
deepseek-v3                                           $0.2000      $0.6000  (?i)^deepseek-v3$
qwen/qwen3-32b                                        $0.2900      $0.5900  (?i)^qwen/qwen3-32b$

Total: 2 models
```

## Fields

| Field | Description |
|-------|-------------|
| Model Name | Model identifier |
| Input $/1M | Cost per 1M input tokens (USD) |
| Output $/1M | Cost per 1M output tokens (USD) |
| Match Pattern | Regex pattern for model name matching |
