---
name: langfuse-observation-view
description: View Langfuse observation (Generation/Span) details. Use when checking specific LLM call input/output, debugging issues, or analyzing costs.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-observation-view.ts*)
---

# Langfuse Observation View

Display detailed information for a specific Observation (Generation/Span).

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Checking specific LLM call details
- Viewing input/output
- Checking costs and token usage
- Viewing prompts used

## Commands

### 1. Get Observation Details

```bash
npx tsx scripts/langfuse-observation-view.ts <observationId>
```

### 2. Show Full Input/Output

```bash
npx tsx scripts/langfuse-observation-view.ts <observationId> --full
```

### 3. JSON Output

```bash
npx tsx scripts/langfuse-observation-view.ts <observationId> --json
```

## Output Example

```
Langfuse Observation Detail
===========================

ID:          obs_abc123
Trace ID:    trace_xyz789
Type:        GENERATION
Name:        chat
Start Time:  2026-01-21 10:30:45
Duration:    2.35s
Level:       DEFAULT

--- Model Info ---
Model:       qwen/qwen3-32b
Parameters:  {"temperature":0.7}

--- Usage & Cost ---
Input Tokens:   1500
Output Tokens:  350
Total Tokens:   1850
Input Cost:     $0.000435
Output Cost:    $0.000207
Total Cost:     $0.000642

--- Prompt ---
Prompt:      librarian-system (v3)
Prompt ID:   prompt_def456

--- Input ---
[{"role":"system","content":"You are..."}]

--- Output ---
Here are the search results...
```

## Fields

| Field | Description |
|-------|-------------|
| Type | GENERATION (LLM call), SPAN (processing span), EVENT (event) |
| Duration | Processing time |
| Model | Model used |
| Input/Output Tokens | Token usage |
| Calculated Cost | Computed cost |
| Prompt | Langfuse prompt used |
