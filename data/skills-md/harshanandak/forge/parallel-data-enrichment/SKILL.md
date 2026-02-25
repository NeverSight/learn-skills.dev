---
name: parallel-data-enrichment
description: "Structured company and entity data enrichment using Parallel AI Task API with core/base processors. Returns typed JSON output. No binary install — requires PARALLEL_API_KEY in .env.local."
compatibility: Requires PARALLEL_API_KEY in .env.local. Uses curl. Takes 15s-5min.
metadata:
  author: harshanandak
  version: "1.0.0"
---

# Parallel Data Enrichment

Enrich company or entity data into structured JSON using the Task API. Use `core` (1-5 min, $0.025) or `base` (15-100s, $0.01) for structured output.

> **CLI alternative (recommended)**: Install `parallel-cli` for official skill:
> `npx skills add parallel-web/parallel-agent-skills --skill parallel-data-enrichment`

## Setup

```bash
API_KEY=$(grep "^PARALLEL_API_KEY=" .env.local | cut -d= -f2)
```

## Create Enrichment Task

```bash
curl -s -X POST "https://api.parallel.ai/v1beta/tasks/runs" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "OpenAI",
    "processor": "core",
    "output_schema": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "founded_year": {"type": "integer"},
        "headquarters": {"type": "string"},
        "employee_count": {"type": "integer"},
        "key_products": {"type": "array", "items": {"type": "string"}}
      }
    }
  }'
```

Response: `{"id": "task_abc123", "status": "queued"}`

## Check Result

```bash
curl -s "https://api.parallel.ai/v1beta/tasks/runs/task_abc123" \
  -H "x-api-key: $API_KEY"
```

```json
{
  "id": "task_abc123",
  "status": "completed",
  "result": {
    "content": {
      "name": "OpenAI",
      "founded_year": 2015,
      "headquarters": "San Francisco, CA",
      "employee_count": 770,
      "key_products": ["ChatGPT", "GPT-4", "DALL-E", "Whisper"]
    },
    "basis": {
      "citations": [{"url": "...", "excerpt": "..."}]
    }
  }
}
```

## Processors

| Processor | Speed | Cost | Use For |
|-----------|-------|------|---------|
| base | 15-100s | $0.01/task | Quick lookups, simple data |
| core | 1-5 min | $0.025/task | Enrichment, verification, structured data |

## Tips for output_schema

- Keep schemas simple — fewer fields = more reliable
- Use `"type": "string"` broadly; avoid strict enums
- Omit optional fields from the schema

## When to Use

- Company or person data enrichment
- Structured data extraction with typed schemas
- Lead qualification, CRM enrichment, research

For narrative reports, use `parallel-deep-research`. For web search, use `parallel-web-search`.
