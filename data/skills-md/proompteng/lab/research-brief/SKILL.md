---
name: research-brief
description: Generate a concise research brief with uncertainty and citations.
---

# research-brief

Generate a concise research brief with uncertainty and citations.

## Output contract

Return JSON keys:

- `context_version`
- `as_of_utc`
- `symbol`
- `freshness_seconds`
- `source_count`
- `quality_score`
- `payload.summary`
- `payload.uncertainty`
- `citations`

## Rules

- Keep summary short and evidence-backed.
- Never omit uncertainty when data quality is low.
