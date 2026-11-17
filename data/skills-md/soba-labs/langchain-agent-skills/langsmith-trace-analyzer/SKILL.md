---
name: langsmith-trace-analyzer
description: "Fetch, organize, and analyze LangSmith traces for debugging and evaluation. Use when you need to: query traces/runs by project, metadata, status, or time window; download traces to JSON; organize outcomes into passed/failed/error buckets; analyze token/message/tool-call patterns; compare passed vs failed behavior; or investigate benchmark and production failures."
---

# LangSmith Trace Analyzer

Use this skill to move from raw LangSmith traces to actionable debugging/evaluation insights.

## Quick Start

```bash
# Install dependencies
uv pip install langsmith langsmith-fetch

# Auth
export LANGSMITH_API_KEY=<your_langsmith_api_key>
```

### Fast workflow

1. Download traces with `scripts/download_traces.py` (or `scripts/download_traces.ts`).
2. Analyze downloaded JSON with `scripts/analyze_traces.py`.
3. Load targeted references only when needed:
   - `references/filtering-querying.md` for query/filter syntax
   - `references/analysis-patterns.md` for deeper diagnostics
   - `references/benchmark-analysis.md` for benchmark-specific workflows

## Decision Guide

1. **Known trace IDs**  
Use `langsmith-fetch trace <id>` directly, or `--trace-ids` in downloader scripts.

2. **Need to discover traces first**  
Use LangSmith SDK `list_runs/listRuns` with filters, then download selected trace IDs.

3. **Need aggregate insights**  
Run `analyze_traces.py` for summary stats, patterns, and passed-vs-failed comparisons.

## Core Workflows

### 1) Download and organize traces

Python:

```bash
uv run skills/langsmith-trace-analyzer/scripts/download_traces.py \
  --project "my-project" \
  --filter "job_id=abc123" \
  --last-hours 24 \
  --limit 100 \
  --output ./traces \
  --organize
```

TypeScript:

```bash
ts-node skills/langsmith-trace-analyzer/scripts/download_traces.ts \
  --project "my-project" \
  --filter "job_id=abc123" \
  --last-hours 24 \
  --limit 100 \
  --output ./traces
```

Output layout:

```text
traces/
├── manifest.json
└── by-outcome/
    ├── passed/
    ├── failed/
    └── error/
        ├── GraphRecursionError/
        ├── TimeoutError/
        └── DaytonaError/
```

Notes:
- Python script supports `--organize/--no-organize`.
- Both scripts use SDK filtering plus `langsmith-fetch` for full trace payload export.

### 2) Analyze downloaded traces

```bash
# Markdown report
uv run skills/langsmith-trace-analyzer/scripts/analyze_traces.py ./traces --output report.md

# JSON output
uv run skills/langsmith-trace-analyzer/scripts/analyze_traces.py ./traces --json

# Compare passed vs failed (expects by-outcome folders)
uv run skills/langsmith-trace-analyzer/scripts/analyze_traces.py ./traces --compare --output comparison.md
```

The analyzer reports:
- message/tool-call/token/duration summaries
- top tool usage
- anomaly patterns (high message count, repeated tools, quick failures)
- passed-vs-failed metric deltas when comparison is enabled

### 3) Query traces correctly (SDK)

Use official LangSmith run filter syntax via `filter` and/or `start_time`:

```python
from datetime import datetime, timedelta, timezone
from langsmith import Client

client = Client()

start = datetime.now(timezone.utc) - timedelta(hours=24)
filter_query = 'and(eq(metadata_key, "job_id"), eq(metadata_value, "abc123"))'

runs = client.list_runs(
    project_name="my-project",
    is_root=True,
    start_time=start,
    filter=filter_query,
)
```

For TypeScript:

```ts
import { Client } from "langsmith";

const client = new Client();
for await (const run of client.listRuns({
  projectName: "my-project",
  isRoot: true,
  filter: 'and(eq(metadata_key, "job_id"), eq(metadata_value, "abc123"))',
})) {
  console.log(run.id, run.status);
}
```

## Accuracy and Schema Notes

- LangSmith run fields are commonly top-level (`status`, `error`, `total_tokens`, `start_time`, `end_time`).
- Some exported traces also include nested metadata (`metadata` or `extra.metadata`) and/or `messages`.
- `analyze_traces.py` is resilient to multiple payload shapes, including raw array payloads.
- For full conversation content, prefer downloaded trace payloads over bare `list_runs` results.

## Troubleshooting

| Issue | Likely Cause | Action |
|---|---|---|
| `LANGSMITH_API_KEY` missing | Auth not configured | `export LANGSMITH_API_KEY=<your_langsmith_api_key>` |
| No runs returned | Wrong project/filter/time range | Verify project name and filter syntax |
| Empty/partial message arrays | Run schema differs or incomplete data | Use downloaded trace JSON and inspect `status/error` fields |
| JSON parse error on downloaded files | Bad/incomplete export | Re-download trace; use `--format raw` paths in scripts |
| Re-downloading same traces repeatedly | Existing files in nested folders | Use current scripts (they check existing files across output tree) |

## Safety for Open Source

- Do not commit downloaded trace artifacts (`manifest.json`, trace JSON dumps) unless sanitized.
- Trace payloads can contain user prompts, outputs, metadata, and other sensitive runtime data.
- Keep this skill repository focused on scripts/templates, not production trace exports.

## Resources

### scripts/

- `scripts/download_traces.py`: Python downloader + organizer
- `scripts/download_traces.ts`: TypeScript downloader + organizer
- `scripts/analyze_traces.py`: Offline analysis and reporting

### references/

- `references/filtering-querying.md`: LangSmith query/filter examples
- `references/analysis-patterns.md`: Diagnostic patterns and heuristics
- `references/benchmark-analysis.md`: Benchmark-oriented analysis
