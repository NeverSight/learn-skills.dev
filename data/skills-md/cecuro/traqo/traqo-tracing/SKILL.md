---
name: traqo-tracing
description: >-
  Read, analyze, and visualize traqo JSONL traces for application observability.
  Use when: (1) reading or debugging .jsonl/.jsonl.gz trace files, (2) investigating
  token usage or costs, (3) analyzing pipeline execution flow or errors,
  (4) adding tracing instrumentation to Python code, (5) querying trace data
  with shell commands, (6) launching the trace viewer UI. Triggers on phrases
  like "read the trace", "what happened in the pipeline", "token usage",
  "why did it fail", "add tracing", "trace this function", "check the logs",
  "show me the traces", "open the dashboard", "visualize the run".
---

# traqo Trace Analysis

Analyze JSONL traces produced by the `traqo` Python package.

## Trace File Structure

Traces are stored as compressed `.jsonl.gz` files, optionally with a `.content.jsonl.zst` sidecar for externalized large span inputs. The raw `.jsonl` buffer is deleted after compression. Last line is always `trace_end` with summary stats. Start there.

For compressed traces, large `span_start` inputs (>10 KB) are replaced with `{"_ref": "<span_id>", "_size": N}` stubs. The full input lives in the companion `.content.jsonl.zst` file. If you see a `_ref` stub, use `traqo ui` (loads on click) or the Python `read_content()` API to retrieve the original input.

## Event Types

| Event | Key Fields |
|-------|------------|
| `trace_start` | `tracer_version`, `input`, `metadata`, `tags`, `thread_id` |
| `span_start` | `id`, `parent_id`, `name`, `input`, `metadata`, `tags`, `kind` |
| `span_end` | `id`, `parent_id`, `name`, `duration_s`, `status`, `output`, `metadata`, `tags`, `kind` |
| `event` | `name`, `data` (arbitrary dict) |
| `trace_end` | `duration_s`, `output`, `stats`, `children` |

Every event has `id`, `parent_id`, and `ts` (ISO timestamp). `span_start` and `span_end` share the same `id` — use it to correlate a span's start with its end. The `kind` field categorizes spans: `"llm"` (model calls), `"tool"` (tool executions), `"chain"` (orchestration/graph nodes), `"retriever"` (search/RAG). LLM-specific data (`model`, `provider`, `token_usage`) lives in `metadata`. `tags` is a list of strings for filtering. `thread_id` groups traces into conversations. `event` is a point-in-time log entry (via `tracer.log()`) — no duration, just a name and arbitrary data dict (e.g. checkpoints, metrics).

Error spans have `status: "error"` and an `error` object with `{type, message, traceback}` (e.g. `{"type": "APITimeoutError", "message": "Request timed out.", "traceback": "..."}`). Success spans have `status: "ok"`.

## Event Structure

```json
{"type":"trace_start","ts":"2026-02-20T10:00:00Z","tracer_version":"0.2.0","input":{"query":"hello"},"tags":["production"],"thread_id":"conv-123","metadata":{"run_id":"abc"}}
```

```json
{"type":"span_start","id":"x1y2z3","parent_id":"a1b2c3","ts":"2026-02-20T10:00:01Z","name":"classify","kind":"llm","tags":["gpt-4o"],"input":[{"role":"user","content":"..."}],"metadata":{"provider":"openai","model":"gpt-4o"}}
```

```json
{"type":"span_end","id":"x1y2z3","parent_id":"a1b2c3","ts":"2026-02-20T10:00:03Z","name":"classify","kind":"llm","duration_s":1.8,"status":"ok","output":"...","metadata":{"provider":"openai","model":"gpt-4o","token_usage":{"input_tokens":1500,"output_tokens":800,"reasoning_tokens":200,"cache_read_tokens":1200,"cache_creation_tokens":0}}}
```

```json
{"type":"trace_end","ts":"2026-02-20T10:05:00Z","duration_s":300.0,"output":{"response":"..."},"stats":{"spans":15,"events":5,"total_input_tokens":45000,"total_output_tokens":12000,"total_cache_read_tokens":30000,"total_cache_creation_tokens":5000,"total_reasoning_tokens":2000,"errors":0},"children":[{"name":"agent_a","file":"agent_a_20260220T100000_abc12345.jsonl.gz","duration_s":45.2,"spans":3,"total_input_tokens":5000,"total_output_tokens":2000,"total_reasoning_tokens":500}]}
```

## Nested Traces

Pipelines can split work into **child traces** — separate `.jsonl.gz` files for each sub-task (e.g. one per agent, batch item, or concurrent worker). The parent trace's `trace_end` lists all children in its `children` array. Each child entry has: `name`, `file` (the `.jsonl.gz` filename), `duration_s`, `spans`, `total_input_tokens`, `total_output_tokens`, `total_reasoning_tokens`.

A child trace is a complete, self-contained trace file with its own `trace_start`/`trace_end`. Navigate to it by downloading the file referenced in `children[].file`. Child traces may themselves have children (arbitrary nesting depth).

## Reading Traces

### File formats

Traces are stored as compressed `.jsonl.gz` files, with an optional `.content.jsonl.zst` sidecar for large span inputs:

```bash
ls traces/    # Look for .jsonl.gz and .content.jsonl.zst
```

Use `zcat` (Linux) or `gzcat` (macOS) to read, then pipe to `grep`/`jq`:

```bash
# macOS
gzcat trace.jsonl.gz | tail -1 | jq .

# Linux
zcat trace.jsonl.gz | tail -1 | jq .
```

**Tip:** For large traces, prefer `traqo ui` over shell commands.

### Downloading traces from cloud storage
```bash
# GCS
gcloud storage cp gs://bucket/prefix/trace.jsonl.gz /tmp/
gcloud storage cp "gs://bucket/prefix/*.jsonl.gz" /tmp/traces/

# S3
aws s3 cp s3://bucket/prefix/trace.jsonl.gz /tmp/
aws s3 cp s3://bucket/prefix/ /tmp/traces/ --recursive --exclude "*" --include "*.jsonl.gz"
```

### Navigation
```bash
# Overview (always start here — last line is trace_end with stats)
gzcat trace.jsonl.gz | tail -1 | jq .

# Compact stats (use this for large traces with many children)
gzcat trace.jsonl.gz | tail -1 | jq '{duration_s, stats, children_count: (.children // [] | length)}'

# Trace context (first line has trace name, input, tags, metadata)
gzcat trace.jsonl.gz | head -1 | jq .

# Follow child traces (file field matches the .jsonl.gz filename on disk/cloud)
# Pipelines often split work into child traces (e.g. one per agent or batch item).
# The parent trace_end lists all children with their file, stats, and duration.
gzcat trace.jsonl.gz | tail -1 | jq '(.children // [])[] | {name, file, spans, total_input_tokens}'
```

**Tip:** For traces with many children, limit output with `| .[:10]` (jq array slice) or pipe through `| head -20`.

### Token Usage
```bash
# Per-span tokens from metadata (input_tokens includes cached)
gzcat trace.jsonl.gz | jq 'select(.metadata.token_usage) | {name, id, model: .metadata.model, tokens: .metadata.token_usage}'

# Total from summary (includes cache and reasoning breakdown)
gzcat trace.jsonl.gz | tail -1 | jq '.stats | {total_input_tokens, total_output_tokens, total_cache_read_tokens, total_cache_creation_tokens, total_reasoning_tokens}'
```

### Errors
```bash
# Single file — error has {type, message, traceback}
gzcat trace.jsonl.gz | jq 'select(.status == "error") | {name, kind, error_type: .error.type, message: .error.message}'

# Multiple files
for f in traces/*.jsonl.gz; do
  gzcat "$f" | jq 'select(.status == "error") | {file: "'"$(basename "$f")"'", name, error_type: .error.type, message: .error.message}'
done

# Total error count from trace summary
gzcat trace.jsonl.gz | tail -1 | jq '.stats.errors'
```

### LLM Spans
```bash
# All LLM span_end events with model, duration, and token usage
gzcat trace.jsonl.gz | jq 'select(.type == "span_end" and .kind == "llm") | {name, model: .metadata.model, duration_s, tokens: .metadata.token_usage}'

# Just model names used in a trace
gzcat trace.jsonl.gz | jq -r 'select(.type == "span_end" and .kind == "llm") | .metadata.model' | sort -u

# Count LLM spans and total duration
gzcat trace.jsonl.gz | jq -s '[.[] | select(.type == "span_end" and .kind == "llm")] | {count: length, total_duration_s: (map(.duration_s) | add)}'
```

All integrations (OpenAI, Anthropic, Gemini, LangChain, cc-sync) use consistent metadata field names: `model`, `model_parameters`, `time_to_first_token_s`, and `token_usage` with keys `input_tokens`, `output_tokens`, `reasoning_tokens`, `cache_read_tokens`, `cache_creation_tokens`.

### Tool Usage
```bash
# Count tool calls by name
gzcat trace.jsonl.gz | jq -r 'select(.type == "span_end" and .kind == "tool") | .name' | sort | uniq -c | sort -rn

# Tool spans with duration and output preview
gzcat trace.jsonl.gz | jq 'select(.type == "span_end" and .kind == "tool") | {name, duration_s, output: (.output | tostring | .[:100])}'
```

### LLM Reasoning / Thinking
LLM span output is a string for text-only responses, or `{"text": "...", "reasoning": "..."}` when the model produced thinking/reasoning content.

```bash
# Extract reasoning content from LLM spans
gzcat trace.jsonl.gz | jq 'select(.type == "span_end" and .kind == "llm" and (.output | type) == "object" and .output.reasoning) | {name, reasoning: .output.reasoning}'

# All LLM outputs (handles both string and object formats)
gzcat trace.jsonl.gz | jq 'select(.type == "span_end" and .kind == "llm") | {name, output_type: (.output | type), has_reasoning: ((.output | type) == "object" and (.output.reasoning | length) > 0)}'
```

### Span Tree
```bash
# Root span (first span_start — in child traces, parent_id points to the parent trace)
gzcat trace.jsonl.gz | jq -s '[.[] | select(.type == "span_start")][0] | {id, parent_id, name, kind}'

# Top-level spans (direct children of root)
gzcat trace.jsonl.gz | jq -s '([.[] | select(.type == "span_start")][0].id) as $root | [.[] | select(.type == "span_start" and .parent_id == $root)] | map({id, name, kind})'

# All spans flat list (parent_id links to parent span)
gzcat trace.jsonl.gz | jq 'select(.type == "span_start") | {id, parent_id, name, kind}'

# Span kinds breakdown
gzcat trace.jsonl.gz | jq -r 'select(.type == "span_end") | .kind' | sort | uniq -c | sort -rn

# Search spans by name pattern (case-insensitive)
gzcat trace.jsonl.gz | jq 'select(.name // "" | test("pattern"; "i")) | {type, name, kind}'
```

**Note:** The first two commands use `jq -s` (slurp) which loads the entire file into memory. For large traces (100K+ spans), use `traqo ui` instead. For visual tree exploration with waterfall timing, prefer `traqo ui ./traces/` over shell commands.

### Common Investigations

```bash
# Find the slowest child trace
gzcat root.jsonl.gz | tail -1 | jq '(.children // []) | sort_by(-.duration_s) | .[0] | {name, file, duration_s, spans}'

# Find the most expensive child trace (by input tokens)
gzcat root.jsonl.gz | tail -1 | jq '(.children // []) | sort_by(-.total_input_tokens) | .[0] | {name, file, total_input_tokens}'

# Download a specific child trace by name (from the children list)
gzcat root.jsonl.gz | tail -1 | jq -r '(.children // [])[] | .file' | grep "agent_name" | xargs -I{} gcloud storage cp "gs://bucket/prefix/{}" /tmp/traces/

# Find which child traces had errors (requires downloading them first)
for f in traces/*.jsonl.gz; do
  errors=$(gzcat "$f" | jq -s '[.[] | select(.status == "error")] | length')
  [ "$errors" -gt 0 ] && echo "$f: $errors errors"
done || true
```

**Note:** `jq -s` (slurp) loads the entire file into memory. For very large traces (100K+ spans), prefer line-by-line `jq` or use `traqo ui` instead.

### Python reader API
```python
from traqo.reader import iter_llm_spans, aggregate_tokens
from pathlib import Path

# Iterate LLM spans (handles .jsonl and .jsonl.gz transparently)
for span in iter_llm_spans(Path("trace.jsonl.gz")):
    print(f"{span.model}: {span.input_tokens}in/{span.output_tokens}out ({span.duration_s}s)")

# Aggregate tokens by model
aggregate_tokens(Path("trace.jsonl.gz"))
# {'gpt-4o': {'input': 45000, 'output': 12000}}
```

### Retrieving externalized content

When a `span_start` input was too large (>10 KB), it gets replaced with a reference stub:
```json
{"type":"span_start","id":"abc123","input":{"_ref":"abc123","_size":245000}}
```

The full input lives in the `.content.jsonl.zst` sidecar file. To retrieve it:

```python
from traqo.compress import read_content
from pathlib import Path

# read_content streams the zst file and stops at the matching span — ~1 MB memory
data = read_content(Path("trace.content.jsonl.zst"), "abc123")
# Returns the original input dict, or None if not found
```

In the **trace viewer UI** (`traqo ui`), externalized inputs show a "Load full input" button that fetches on click via the `/api/content` endpoint — no manual work needed.

## Claude Code Integration

Convert Claude Code session transcripts into traqo traces.

```bash
# Sync a single session
traqo cc-sync path/to/session.jsonl

# Sync all sessions from ~/.claude/projects/
traqo cc-sync --all --output-dir ./traces

# As a Claude Code Stop hook (~/.claude/settings.json)
# { "hooks": { "Stop": [{ "type": "command", "command": "traqo cc-sync --hook" }] } }
```

Produces one trace per session with turn spans, LLM spans (with token usage including cache breakdown), tool call spans, and subagent hierarchy.

## Trace Viewer UI

Built-in React web dashboard. Bundled with the pip package — no extra install needed.

```bash
# Local traces
traqo ui traces/

# Custom port
traqo ui traces/ --port 8080

# S3 or GCS
traqo ui s3://bucket/prefix
traqo ui gs://bucket/prefix
```

Features: span tree with waterfall timing, tag/status filtering, search, token usage charts, cache token totals, keyboard shortcuts (↑/↓ navigate, Esc back, ? help). Handles compressed `.jsonl.gz` traces and loads externalized span inputs on demand via "Load full input" button. Suggest the UI when the user wants to visually explore or browse traces.

## Adding Tracing to Code

### Decorate a function
```python
from traqo import trace

@trace()
async def my_function(data):
    return process(data)

@trace(metadata={"component": "auth"}, tags=["auth"], kind="tool")
def login(user):
    return authenticate(user)
```

### Access current span from decorated function
```python
from traqo import trace, get_current_span

@trace()
def classify(text):
    span = get_current_span()
    if span:
        span.set_metadata("confidence", 0.95)
    return result
```

### Wrap an LLM client
```python
from traqo.integrations.openai import traced_openai
client = traced_openai(OpenAI(), operation="classify")

from traqo.integrations.anthropic import traced_anthropic
client = traced_anthropic(AsyncAnthropic(), operation="analyze")

from traqo.integrations.langchain import traced_model
model = traced_model(ChatOpenAI(), operation="summarize")
```

### Trace a Claude Agent SDK session
```python
from claude_agent_sdk import query, ClaudeAgentOptions
from traqo.integrations.claude_agent_sdk import traqo_agent

# Standalone
async with traqo_agent("code-review", output_dir="./traces", tags=["review"]) as hooks:
    async for msg in query(prompt="Review this PR", options=ClaudeAgentOptions(hooks=hooks)):
        print(msg)

# Nested inside a parent pipeline trace
with Tracer(Path("traces/pipeline.jsonl"), tags=["ci"]) as tracer:
    async with traqo_agent("code-review", tags=["review"]) as hooks:
        async for msg in query(prompt="Review", options=ClaudeAgentOptions(hooks=hooks)):
            ...
```

### Use spans with metadata
```python
from traqo import get_tracer

tracer = get_tracer()
if tracer:
    with tracer.span("my_step", input=data, metadata={"model": "gpt-4o"}, tags=["llm"], kind="llm") as span:
        result = call_llm()
        span.set_metadata("token_usage", {"input_tokens": 100, "output_tokens": 50})
        span.set_output(result)
```

### Log a custom event
```python
from traqo import get_tracer
tracer = get_tracer()
if tracer:
    tracer.log("checkpoint", {"count": len(results)})
```

### Activate tracing
```python
from traqo import Tracer
from pathlib import Path

with Tracer(
    Path("traces/run.jsonl"),
    input={"query": "hello"},
    metadata={"run_id": "abc123"},
    tags=["production"],
    thread_id="conv-456",
) as tracer:
    result = await main()
    tracer.set_output({"response": result})
```

### Child tracer for concurrent agents
```python
child = tracer.child("my_agent", Path("traces/agents/my_agent.jsonl"))
with child:
    await run_agent()
```
