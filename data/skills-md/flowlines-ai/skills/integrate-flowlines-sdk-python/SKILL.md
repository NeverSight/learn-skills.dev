---
name: integrate-flowlines-sdk-python
description: Integrates Flowlines observability SDK into Python LLM applications. Use when adding Flowlines telemetry, instrumenting LLM providers, or setting up OpenTelemetry-based LLM monitoring.
---

# Flowlines SDK for Python — Agent Skill

## What is Flowlines

Flowlines is an observability SDK for LLM-powered Python applications. It instruments LLM provider APIs using OpenTelemetry, automatically capturing requests, responses, timing, and errors. It filters telemetry to only LLM-related spans and exports them via OTLP/HTTP to the Flowlines backend.

Supported LLM providers: OpenAI, Anthropic, AWS Bedrock, Cohere, Google Generative AI, Vertex AI, Together AI.
Supported frameworks/tools: LangChain, LlamaIndex, MCP, Pinecone, ChromaDB, Qdrant.

## Installation

Requires Python 3.11+.

```bash
pip install flowlines
```

Then install instrumentation extras for the providers used in the project:

```bash
# Single provider
pip install flowlines[openai]

# Multiple providers
pip install flowlines[openai,anthropic]

# All supported providers
pip install flowlines[all]
```

Available extras: `openai`, `anthropic`, `bedrock`, `cohere`, `google-generativeai`, `vertexai`, `together`, `pinecone`, `chromadb`, `qdrant`, `langchain`, `llamaindex`, `mcp`.

## Integration

There are three integration modes. Pick the one that matches the project's OpenTelemetry situation.

### Mode A — No existing OpenTelemetry setup (default)

Use this when the project does NOT already have its own OpenTelemetry `TracerProvider`. This is the most common case.

```python
from flowlines import Flowlines

flowlines = Flowlines(api_key="<FLOWLINES_API_KEY>")
```

This single call:
1. Creates an OpenTelemetry `TracerProvider`
2. Auto-detects which LLM libraries are installed and instruments them
3. Filters spans to only export LLM-related telemetry
4. Sends data to the Flowlines backend via OTLP/HTTP

### Mode B1 — Existing OpenTelemetry setup (`has_external_otel=True`)

Use this when the project already manages its own `TracerProvider`.

```python
from flowlines import Flowlines
from opentelemetry.sdk.trace import TracerProvider

flowlines = Flowlines(api_key="<FLOWLINES_API_KEY>", has_external_otel=True)

provider = TracerProvider()

# Add the Flowlines span processor to the existing provider
processor = flowlines.create_span_processor()
provider.add_span_processor(processor)

# Instrument providers using the Flowlines instrumentor registry
for instrumentor in flowlines.get_instrumentors():
    instrumentor.instrument(tracer_provider=provider)
```

- `create_span_processor()` must be called exactly once.
- `get_instrumentors()` returns instrumentor instances only for libraries that are currently installed.

### Mode B2 — Traceloop already initialized (`has_traceloop=True`)

Use this when Traceloop SDK is already initialized. Traceloop must be initialized BEFORE Flowlines.

```python
from flowlines import Flowlines

flowlines = Flowlines(api_key="<FLOWLINES_API_KEY>", has_traceloop=True)
```

Flowlines adds its span processor to the existing Traceloop `TracerProvider`. No instrumentor registration needed.

## Critical rules

1. **Initialize Flowlines BEFORE creating LLM clients.** The `Flowlines()` constructor must run before any LLM provider client is instantiated (e.g., `OpenAI()`, `Anthropic()`). If the client is created first, its calls will not be captured.

2. **Flowlines is a singleton.** Only one `Flowlines()` instance may exist. A second call raises `RuntimeError`. Store the instance and reuse it. Do NOT instantiate it multiple times.

3. **`has_external_otel` and `has_traceloop` are mutually exclusive.** Setting both to `True` raises `ValueError`.

4. **`user_id` is mandatory in `context()`.** The context manager requires `user_id` as a keyword argument. `session_id` and `agent_id` are optional.

5. **Context does not auto-propagate to child threads/tasks.** If using threads or async tasks, set context in each thread/task explicitly.

## User, session, and agent tracking

Tag LLM calls with user/session/agent IDs using the context manager:

```python
with flowlines.context(user_id="user-42", session_id="sess-abc", agent_id="agent-1"):
    client.chat.completions.create(...)  # this span gets user_id, session_id, and agent_id
```

`session_id` and `agent_id` are optional:

```python
with flowlines.context(user_id="user-42"):
    client.chat.completions.create(...)
```

For cases where a context manager doesn't fit (e.g., across request boundaries in web frameworks), use the imperative API:

```python
token = Flowlines.set_context(user_id="user-42", session_id="sess-abc", agent_id="agent-1")
try:
    client.chat.completions.create(...)
finally:
    Flowlines.clear_context(token)
```

`set_context()` / `clear_context()` are static methods on the `Flowlines` class.

## Context integration guidance

When integrating `flowlines.context()`, you MUST wrap LLM calls with context. Follow these steps:

1. **Identify existing data** in the codebase that maps to `user_id`, `session_id`, and `agent_id`:
   - `user_id`: the end-user making the request (e.g., authenticated user ID, email, API key owner)
   - `session_id`: the conversation or session grouping multiple interactions (e.g., chat thread ID, session token, conversation UUID)
   - `agent_id`: the AI agent or assistant handling the request (e.g., agent name, bot identifier, assistant ID)

2. **If obvious mappings exist**, use them directly. For example, if the app has `request.user.id` and a `thread_id`, wire them in:
   ```python
   with flowlines.context(user_id=request.user.id, session_id=thread_id):
       ...
   ```

3. **If mappings are unclear**, ask the user which variables or fields should be used for `user_id`, `session_id`, and `agent_id`.

4. **If no data is available yet**, propose using placeholder values with TODO comments so the integration is functional and easy to complete later:
   ```python
   with flowlines.context(
       user_id="anonymous",  # TODO: replace with actual user identifier
       session_id=f"sess-{uuid.uuid4().hex[:8]}",  # TODO: replace with actual session/conversation ID
       agent_id="my-agent",  # TODO: replace with actual agent identifier
   ):
       ...
   ```
   Only include fields that are relevant. `session_id` and `agent_id` can be omitted entirely if not applicable.

## Constructor parameters

```python
Flowlines(
    api_key: str,                    # Required. The Flowlines API key.
    endpoint: str = "https://ingest.flowlines.ai",  # Backend URL.
    has_external_otel: bool = False,  # True if project has its own TracerProvider.
    has_traceloop: bool = False,      # True if Traceloop is already initialized.
    verbose: bool = False,            # True to enable debug logging to stderr.
)
```

## Public API summary

| Method / attribute | Description |
|-|-|
| `Flowlines(api_key, ...)` | Constructor. Initializes the SDK (singleton). |
| `flowlines.context(user_id=..., session_id=..., agent_id=...)` | Context manager to tag spans with user/session/agent. |
| `Flowlines.set_context(user_id=..., session_id=..., agent_id=...)` | Static. Imperative context setting; returns a token. |
| `Flowlines.clear_context(token)` | Static. Restores previous context using the token. |
| `flowlines.create_span_processor()` | Returns a `SpanProcessor`. Mode B1 only. Call once. |
| `flowlines.get_instrumentors()` | Returns list of available instrumentor instances. |
| `flowlines.shutdown()` | Flush and shut down. Called automatically via `atexit`. |

## Imports

The public API is exported from the top-level package:

```python
from flowlines import Flowlines
from flowlines import FlowlinesExporter  # only needed for advanced use
```

## Verbose / debug mode

Pass `verbose=True` to print debug information to stderr:

```python
flowlines = Flowlines(api_key="...", verbose=True)
```

This logs instrumentor discovery, span filtering, and export results.

## Shutdown

`flowlines.shutdown()` is registered as an `atexit` handler automatically. It is idempotent — safe to call multiple times. You can call it explicitly if you need to ensure spans are flushed before the process ends (e.g., in serverless environments).

## Common mistakes to avoid

- Do NOT create the LLM client before initializing Flowlines — spans will be missed.
- Do NOT instantiate `Flowlines()` more than once — it raises `RuntimeError`.
- Do NOT set both `has_external_otel=True` and `has_traceloop=True`.
- Do NOT forget to install the instrumentation extras for the providers you use (e.g., `flowlines[openai]`).
- Do NOT assume context propagates to child threads — set it explicitly in each thread/task.
