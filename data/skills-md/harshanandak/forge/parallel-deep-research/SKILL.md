---
name: parallel-deep-research
description: "Deep market analysis and comprehensive research reports using Parallel AI Task API with pro/ultra processors. Multi-source synthesis with citations. No binary install — requires PARALLEL_API_KEY in .env.local."
compatibility: Requires PARALLEL_API_KEY in .env.local. Uses curl. Takes 3-25 minutes.
metadata:
  author: harshanandak
  version: "1.0.0"
---

# Parallel Deep Research

Comprehensive research reports with multi-source synthesis. Use `pro` (3-9 min, $0.10) or `ultra` (5-25 min, $0.30) for deep analysis.

> **CLI alternative (recommended)**: Install `parallel-cli` for official skill:
> `npx skills add parallel-web/parallel-agent-skills --skill parallel-deep-research`

## Setup

```bash
API_KEY=$(grep "^PARALLEL_API_KEY=" .env.local | cut -d= -f2)
```

## Create Research Task

```bash
curl -s -X POST "https://api.parallel.ai/v1beta/tasks/runs" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Analyze the AI chatbot market. Include: size, growth, key players, trends, competitive threats",
    "processor": "pro",
    "output_schema": "text"
  }'
```

Response: `{"id": "task_abc123", "status": "queued"}`

## Polling Loop

```bash
TASK_ID="task_abc123"

while true; do
  RESULT=$(curl -s "https://api.parallel.ai/v1beta/tasks/runs/$TASK_ID" \
    -H "x-api-key: $API_KEY")

  STATUS=$(echo $RESULT | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

  if [ "$STATUS" = "completed" ]; then
    echo "$RESULT"
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Task failed: $RESULT"
    break
  fi

  sleep 5
done
```

## Processors

| Processor | Speed | Cost | Use For |
|-----------|-------|------|---------|
| pro | 3-9 min | $0.10/task | Market analysis, strategic reports |
| ultra | 5-25 min | $0.30/task | Comprehensive deep research |

## Example: Market Analysis

```json
{
  "input": "Analyze the AI chip market in 2024. Include market size, growth rate, key players (NVIDIA, AMD, Intel), emerging competitors, and 2025 outlook.",
  "processor": "pro",
  "output_schema": "text"
}
```

Result: Markdown report with citations.

## When to Use

- Market research and competitive analysis
- Strategic reports requiring multiple sources
- Research that needs synthesis across many documents

For quick facts, use `parallel-web-search`. For structured data extraction, use `parallel-data-enrichment`.

## Timeout

Set polling timeout to 1800s (30 min) for ultra tasks. Pro tasks typically complete in 3-9 min.
