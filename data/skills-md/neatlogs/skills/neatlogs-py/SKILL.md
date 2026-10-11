---
name: neatlogs-py
description: >
  NeatLogs is an AI agent debugging and observability platform. Use this skill when
  instrumenting Python LLM applications with neatlogs for tracing, monitoring, debugging,
  observability, decorators, spans, or instrumentation of
  LLM providers and agent frameworks.
---

# NeatLogs — Agent Skill

NeatLogs auto-instruments LLM calls, agent frameworks, and custom code. The small public API most integrations need:
`init()`, `flush()`, `shutdown()`, `@span()`, `trace()`, `identify()`, `inject_trace_context()`, and `extract_trace_context()`.

---

## Installation

Always install the latest published version — pass `--upgrade` so an already-installed older version is bumped:

```bash
pip install --upgrade neatlogs
# uv: uv add --upgrade neatlogs · poetry: poetry add neatlogs@latest
```

Optional extras install the actual underlying LLM / framework libraries (same `--upgrade` rule applies):

```bash
pip install --upgrade neatlogs[openai]
pip install --upgrade neatlogs[anthropic]
pip install --upgrade neatlogs[google-genai]
pip install --upgrade neatlogs[langchain]
pip install --upgrade neatlogs[langchain,langgraph]
pip install --upgrade neatlogs[crewai]
pip install --upgrade neatlogs[litellm]
pip install --upgrade neatlogs[mcp]
```

Combine multiple extras with commas: `pip install --upgrade neatlogs[crewai,google-genai]`

Requires Python >= 3.10, < 3.14. Notable version pins: `crewai >= 1.9.3`.

---

## Core Principles

1. **Import order matters**: `neatlogs.init()` MUST be called **before** importing any LLM libraries for auto-instrumentation patching to work. If the project uses `dotenv` / `load_dotenv()`, call it **before** `neatlogs.init()` so `NEATLOGS_API_KEY` from `.env` is available. Correct order: `import neatlogs` → `load_dotenv()` → `neatlogs.init()` → LLM library imports.
2. **Scripts**: end with `neatlogs.flush()` then `neatlogs.shutdown()`. **Servers**: call `init()` once at startup; do NOT call `flush()` / `shutdown()` per request — see [Long-Running Servers](#long-running-servers) below.
3. **One capture owner per operation** — wrappers, callback handlers, hooks, processors, native telemetry, and provider instrumentors own the spans they capture. Use `@span` for your own orchestration. Use manual `trace(kind="LLM")` only when no supported capture layer owns the LLM call.
4. **Prefer the framework/provider-specific integration** over manual instrumentation. Never combine two capture layers for the same operation.
5. **Init is single-shot**: `neatlogs.init()` configures the global telemetry provider. Calling it again is a no-op — it will NOT switch projects, even with a different `api_key`/`workflow_name`. If you need to reinitialize the SAME project, call `neatlogs.shutdown()` first (rare). If the need is a genuinely DIFFERENT project (different API key) from the same process, that's not a second `init()` at all — see [Multiple Projects](#multiple-projects-secondary-clients) below.
6. **Region endpoint**: for EU projects, set `endpoint="https://eu.ingest.neatlogs.com"` in `neatlogs.init()`. For other managed projects, omit `endpoint` and `NEATLOGS_ENDPOINT`. Preserve an explicit self-hosted endpoint.
7. **Read reference docs** before implementing — NeatLogs updates frequently.

### Transport selection

Use this SDK for Python. Neatlogs also has SDKs for TypeScript/Node.js and Go. For a language without a supported Neatlogs SDK, default to the dependency-free HTTP ingest endpoint `POST /v1/trace`; if that project already emits OpenTelemetry, OTLP/gRPC is also supported. Use the `neatlogs-ingest` skill for the complete HTTP and gRPC contracts. Do not confuse `/v1/trace` nested JSON with the `/v1/traces` OTLP/HTTP protobuf route.

---

## Quick Start

End-to-end example showing a provider wrapper plus a custom orchestration span:

```python
import neatlogs

neatlogs.init(api_key="your-api-key", workflow_name="my-app")

from openai import OpenAI
client = neatlogs.wrap(OpenAI())


@neatlogs.span(kind="AGENT", name="researcher", role="Research Analyst")
def researcher(query: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content


@neatlogs.span(kind="WORKFLOW")
def run(query: str) -> str:
    return researcher(query)


if __name__ == "__main__":
    print(run("Explain quantum computing briefly."))
    neatlogs.flush()
    neatlogs.shutdown()
```

This produces `WORKFLOW → AGENT → LLM`. The wrapper owns the single canonical LLM span; no manual LLM decorator is added.

> **On the `@span(kind="WORKFLOW")` root:** a single parentless LLM call is already root-eligible, so the decorator is **not** required just to make a trace appear. Standalone non-root manual operations receive one automatic workflow parent. Add `@span(kind="WORKFLOW")` (or `AGENT`/`CHAIN`) when the function owns a real request, job, agent loop, or pipeline stage with meaningful pre/post work or multiple captured children, as in this multi-step example. If a root is already active, automatic rooting steps aside (no double root).

---

## Long-Running Servers

For server applications, call `neatlogs.init()` **once at startup** and flush/shutdown **once at shutdown**. Spans batch automatically every `flush_interval` (default 5 s) — do not call `flush()` / `shutdown()` per request.

Decorate each AI endpoint handler with `@span(kind="WORKFLOW")` so the whole request (its LLM calls, tools, and your own steps) groups under one root per request. A lone instrumented LLM call is itself a valid root, but decorating the handler gives the request a single, meaningfully named root that everything nests under.

```python
import neatlogs
from fastapi import FastAPI
from contextlib import asynccontextmanager

neatlogs.init(
    api_key="...",  # Get from https://app.neatlogs.com/settings/api-keys (or set NEATLOGS_API_KEY env var)
    workflow_name="my-api",
    instrumentations=["openai"],
)

from openai import OpenAI  # Import AFTER init()

client = OpenAI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Called once when the server shuts down — flush remaining spans
    import asyncio
    await asyncio.to_thread(neatlogs.flush)
    await asyncio.to_thread(neatlogs.shutdown)

app = FastAPI(lifespan=lifespan)

@app.get("/ask")
@neatlogs.span(kind="WORKFLOW", name="ask_workflow")
async def ask(q: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": q}],
    )
    return {"answer": response.choices[0].message.content}
    # DO NOT call flush() here — would flush on every request (performance issue)
```

For non-FastAPI servers, hook `neatlogs.flush()` + `neatlogs.shutdown()` into the framework's shutdown event (or an `atexit` handler). See [`references/troubleshooting.md` §5](references/troubleshooting.md#5-flush--shutdown-gotcha) for the async gotcha.

---

## Multiple Projects (Secondary Clients)

**Python only, `neatlogs>=1.4.19`.** This is for a narrower, rarer need than [Long-Running Servers](#long-running-servers) above: some traces from this SAME process need to go to a genuinely DIFFERENT Neatlogs project — different API key, fully isolated pipeline — not just a different `workflow_name` label in the same project. The usual trigger is multi-tenant: each tenant has their own Neatlogs project.

Do NOT call `neatlogs.init()` a second time for this — it's a no-op (see Core Principle 5 above). Use `neatlogs.Client(...)` instead:

```python
import neatlogs

# The process-wide default — unchanged, still called once.
neatlogs.init(api_key=os.environ["NEATLOGS_API_KEY"], workflow_name="my-service")

# A second, fully isolated project for this tenant — NOT another init().
tenant_client = neatlogs.Client(
    api_key=tenant_api_key,
    workflow_name=f"tenant-{tenant_id}",
    capture_logs=True,   # only if you also want neatlogs.log() routed to this client
)

with tenant_client.activate():
    # Everything in here — wrap(), trace(), @span, log() — routes to
    # tenant_client's pipeline. contextvars-scoped, so concurrent requests
    # for DIFFERENT tenants never leak into each other's traces.
    client = neatlogs.wrap(OpenAI())
    with neatlogs.trace("handle_request", kind="WORKFLOW"):
        response = client.chat.completions.create(...)

# Outside the block, back to the default init() pipeline.
```

`tenant_client.wrap(target)` is a shortcut for `with tenant_client.activate(): neatlogs.wrap(target)` in one call. Each `Client` has its own `flush()`/`shutdown()`, independent of the default pipeline and of every other `Client` — flushing one never flushes another. `Client` has no singleton guard like `init()` does — a real multi-tenant app builds/caches ONE per tenant, keyed by tenant id, not a single hardcoded extra one.

Two gotchas: if the same logical run can be entered more than once in-process (e.g. a handler invoked directly for the same request), track the active `WORKFLOW` span (a `ContextVar` works) and reuse it instead of activating again — otherwise you get a `WORKFLOW`-inside-`WORKFLOW` staircase; only the outermost call should flush. And in a long-running process, call `flush()` explicitly at the end of each run — the `atexit` hook only fires at process exit, so relying on it alone delays visibility until shutdown.

**Being mounted/routed differently within one process is not itself a signal for anything — almost everything stays on one project.** Different features, different routes, even a sub-app mounted into the same process (`app.mount(...)` or equivalent) all just get their own `workflow_name`; a separately-booted worker process gets its own ordinary `init()` call with the SAME key, no conflict. `Client` is for a narrower, different situation: this code's telemetry genuinely belongs to a DIFFERENT project — either (a) different tenants/customers routed at runtime (explicit multi-tenant SaaS), or (b) this code reads/analyzes ANOTHER project's traces as its own input data, so its own traces landing there would corrupt what it's analyzing (not just an organizational preference — a structural conflict). Both are real ownership/architecture facts, never inferred from code structure — confirm with the user rather than guessing. If you find an EXISTING second `init()`-style call already trying to target different credentials inside one process, flag it explicitly — it is very likely silently non-functional (`init()` warns and returns on a second call, it does not "isolate" anything, even when the second call is inside something mounted separately). TypeScript and Go have no equivalent yet.

---

## Decorator Ordering

`@neatlogs.span()` MUST be placed **below** (closest to `def`) any framework decorators that transform the function into a different object (e.g. `@function_tool`, `@tool`, `@task`). Framework decorators above `@neatlogs.span` is fine only when they preserve the callable (e.g. `@app.get`, `@app.post`).

```python
# CORRECT — @function_tool wraps the span-decorated function
@function_tool
@neatlogs.span(kind="TOOL", tool_name="search")
def search(query: str) -> str:
    ...

# WRONG — @neatlogs.span receives a FunctionTool object, crashes
@neatlogs.span(kind="TOOL", tool_name="search")
@function_tool
def search(query: str) -> str:
    ...
```

---

## Instrumentation Workflow

1. **Assess**: Detect what LLM providers / frameworks the project uses.
2. **Instrument**: Pick the right approach:
   - The provider/framework-specific wrapper, callback handler, hook, processor, native telemetry, or provider instrumentor
   - **`@span` decorators** for your own orchestration functions
   - **`trace()`** for custom direct-API spans (`RERANKER`, `VECTOR_STORE`, or an LLM call with no supported capture owner)
3. **Init**: Add `neatlogs.init()` **BEFORE** any LLM library imports with the correct `instrumentations=[...]` list. If the project uses `load_dotenv()`, call it before `init()`.
4. **Verify**: run existing tests/import checks, restart long-running processes, exercise the real instrumented path, and confirm a new dashboard trace with one canonical span per operation.

## Safety gate

Before any edit, confirm this service is Python. Identify the active interpreter
and package manager from its manifests and lockfiles, then read the declared and
installed SDK version. Do not install or change dependencies during this
inspection. Run Doctor through the active interpreter so it can use only the
installed SDK:

```bash
python -m neatlogs doctor --local --json
```

Do not substitute `npx`, `uvx`, `pipx run`, a Wizard command, or another
downloaded Doctor. Local mode must be read-only and network-free. It requires no
credential and must not change source or configuration. Require
`format_version: "neatlogs.doctor/v2"`, `runtime.language: "python"`, and
`runtime.schema_version: "2"`. Treat `runtime.sdk_version` as evidence of the
installed package, not as an exact-version allowlist.

If the command is missing or its result has the wrong format, language, or
schema, fail closed. Check the canonical package registry for the latest
published stable release. If the project uses an older release, show the exact
upgrade command for the detected package manager and obtain explicit user
approval before running it. Accept newer compatible releases and never
downgrade one. If the installed release is already current but lacks Doctor v2,
stop and give safe manual/support remediation. Rerun local Doctor after any
approved upgrade. Do not edit while this gate is unresolved.

A local `pass` proves only that the installed SDK produced and validated its
controlled in-process envelope. It does not prove that the application is
instrumented, that anything was exported, or that a hosted trace is visible.
Preserve every `reason_code` and `remediation_code` exactly. Treat a warning,
failure, or unknown future code as manual/support remediation unless the code is
explicitly safe/fixable here. The only source fixes allowed by this gate are:

- `INSTRUMENTOR_INACTIVE`: apply only this skill's documented initialization or
  wrapper step.
- `ROOT_MISSING`: add only the already-requested, documented WORKFLOW boundary
  at a confirmed entry point.
- `ROOT_NOT_ENDED`: add only this skill's documented lifecycle hook.

Do not edit for credential, authentication, transport, backend, ambiguous
ownership, or unknown codes. Never reproduce backend PII, routing, mapping, or
finalization implementation. Before any build, test, or user-workflow command,
show the exact command and obtain explicit user approval. Make reruns idempotent:
reread the target first and never duplicate initialization, wrappers, roots, or
shutdown hooks. Keep a pre-edit diff. If an approved check fails, use the
rollback plan to revert only the edits from this run when they can be isolated
safely. Otherwise, stop and give manual recovery instructions that preserve
unrelated user work.

After instrumentation, obtain approval for the project checks and one
representative real workflow. Obtain separate approval for the authenticated
probe. Use only a credential already supplied through the process environment.
Never print it, place it in command arguments or files, copy it into output, or
put it in agent context.

```bash
python -m neatlogs doctor --probe --json
```

Probe mode sends one controlled four-span trace through `POST /v1/traces` with
`x-neatlogs-doctor: v1`, then reads that exact trace through
`GET /api/traces/v3/{trace_id}` with the same project credential. Accept a
probe `pass` only when capture and readback trace IDs match, the trace is
finalized, exactly four spans contain one meaningful WORKFLOW root with
AGENT→LLM and root→TOOL relationships, there are no duplicates, required
semantics and I/O are present, and token values remain numeric. Never infer
success from installation, local logs, exporter flush, HTTP 2xx, or any
uncorrelated trace. Probe success proves the controlled path only. Verify the
real user workflow separately through the completion gate below.

## Public CLI credentials after SDK verification

The project key supports SDK Doctor probe readback without public CLI login.
If it is the only credential available, report optional CLI readback as
**waiting on a human** and verify the application's exact trace separately in
the dashboard. A controlled probe is not proof of the real workflow.

For terminal readback, follow the `neatlogs-public-api-cli` skill or
https://docs.neatlogs.com/cli if that skill is unavailable. Its 0.2.1 guidance
uses explicit dashboard host, OAuth profile or service-token selection, and
project discovery before project-scoped reads. Keep the SDK key available to
the app; it must not override CLI authentication. Check publication and installed
version before using 0.2.1 options; the CLI skill documents the 0.2.0 fallback.

## Completion gate

After local Doctor passes and the requested instrumentation is in place:

1. Show the exact project build, test, and real-workflow commands and obtain
   explicit user approval before running them.
2. Run only the approved checks. Restart a long-running process so it loads the
   new initialization and wrappers; keep reruns idempotent.
3. Exercise one representative real user workflow. End every opened span and
   use the documented flush/shutdown lifecycle for that process type.
4. Through the target project's normal product trace view or supported public
   read path, verify that exact run is finalized, has one meaningful root and
   the expected semantic hierarchy, and contains no duplicate operation spans.
   If using a terminal public read, follow the separate
   `neatlogs-public-api-cli` skill; its app-origin credentials and
   `neatlogs traces get` command are not the SDK's ingest key or Doctor. Its
   root and parent checks cover the canonical public projection, not emitted
   span topology.

Keep project credentials in the process environment or client secret storage;
never put them in commands, output, files, or agent context. Do not use a
legacy marker-discovery protocol. Installation, local
logs, exporter flush, HTTP 2xx, a local Doctor pass, and a separate probe pass
are not proof that the application's real workflow is correct. If the exact
user trace cannot be inspected, report the missing access or observation as a
blocker and provide rollback/manual recovery instructions without claiming
completion.

## `neatlogs.init()` Reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str` | `None` | API key (or set `NEATLOGS_API_KEY` env var). If neither is set, spans are created locally but **silently not exported** — no error is raised |
| `workflow_name` | `str` | `None` | Name for this workflow / application |
| `instrumentations` | `list[str]` | `None` | Libraries to auto-instrument (e.g. `["openai", "langchain"]`) |
| `tags` | `list[str]` | `None` | Tags for filtering in dashboard |
| `user_id` | `str` | `None` | The **operator** running the SDK (developer / service account) — NOT your app's end-user. For end-user/session identity see [Sessions & End-Users](#sessions--end-users) |
| `debug` | `bool` | `False` | Enable verbose logging to stderr |
| `pii_enabled` | `Optional[bool]` | `None` | Override the team-level server-side PII redaction setting. `True` = enable, `False` = disable, `None` (default) = use the team setting in the NeatLogs dashboard |
| `pii_entities` | `Optional[list[str]]` | `None` | Which Presidio entities to redact, e.g. `["PERSON", "EMAIL_ADDRESS"]`. Persisted to the project. `None` = keep the project's saved selection |
| `pii_span_types` | `Optional[list[str]]` | `None` | Override which span types have PII redaction applied. `None` = use team dashboard config |
| `capture_logs` | `bool` | `False` | Capture `neatlogs.log()`, stdlib `logging.*()`, and `print()` (via `capture_stdout=True` on `@span`) as LOG spans |
| `mask` | `callable` | `None` | Client-side mask function `(span_dict) -> span_dict` — see [Data Masking](#data-masking-and-pii) |
| `isolate` | `Optional[bool]` | `None` | Route ALL neatlogs spans through a private tracer provider. `None` = auto-detect (isolates when a co-tenant LLM-observability tool like OpenLLMetry / Langfuse owns the global provider); `True`/`False` force the decision |
| `tracer_provider` | `Optional[Any]` | `None` | A private `TracerProvider` you created but did NOT install as the OTel global — neatlogs emits every span into it and never claims the global meter/logger. For full isolation from a co-tenant OTel pipeline. Implies isolation |

---

## Sessions & End-Users

Attaching session + end-user identity lets you analyze usage / cost / errors per customer and segment, view multi-turn conversation timelines, and replay a customer's conversation.

Model: **one turn = one trace**; a **session** groups the turns of one conversation (same `session_id` on every turn); the **end-user** is per session (same `end_user_id` on every turn). Identity is stamped on the **trace root only** — child spans ignore these params; the backend rolls it up. There is NO session or end-user param on `init()`.

Set identity in one of three ways:

```python
# 1. On a trace root
with neatlogs.trace("turn", session_id="conv_123", end_user_id="u_456", end_user_metadata={"plan": "pro"}):
    ...

# 2. On a @span root (WORKFLOW / AGENT / CHAIN)
@neatlogs.span(kind="WORKFLOW", session_id="conv_123", end_user_id="u_456", end_user_metadata={"plan": "pro"})
def handle_turn(...):
    ...

# 3. Wrapper-only code (you only call neatlogs.wrap(...) and have no root of your own).
# The wrapped call's trace root inherits the identify() context (framework roots do too):
with neatlogs.identify(session_id="conv_123", end_user_id="u_456", end_user_metadata={"plan": "pro"}):
    client.chat.completions.create(...)
```

Session lineage has two fixed IDs plus arbitrary fields supplied by the application:

```python
with neatlogs.identify(
    session_id="child_123",
    parent_session_id="parent_456",
    session_custom_fields={"feature_name": "chat", "entry_point": "slack", "tenant": "acme"},
):
    client.chat.completions.create(...)
```

`session_custom_fields` is a free-form dict encoded as `neatlogs.session.custom_fields`; do not invent fixed SDK parameters for individual custom keys.

---

## Cross-Process Propagation

To keep **one logical trace** when a request crosses a service boundary (Python → Python/Go, gateway → worker), carry the active span as W3C `traceparent`/`tracestate` headers: the **caller injects**, the **callee extracts**. Both helpers use NeatLogs' **private** propagator — they never read or replace the global OTel propagator, so propagation stays isolated from any co-tenant tracer (Datadog / Langfuse / OpenLLMetry).

- **`neatlogs.inject_trace_context(carrier) -> bool`** — caller side, right before an outbound request. `carrier` is any mutable header mapping (a `dict`, a `requests` `CaseInsensitiveDict`, …). Returns `True` when a NeatLogs span was active and headers were written; `False` when nothing is active (carrier untouched). An upstream `traceparent` already present is preserved, not overwritten.
- **`neatlogs.extract_trace_context(carrier, *, session_id=None, parent_session_id=None, session_custom_fields=None, end_user_id=None, end_user_metadata=None)`** — callee side, a **context manager**. Inside it the next `trace()` / `@span` / `wrap()` root nests under the remote span and shares its `trace_id`. No valid `traceparent` → no-op passthrough (identity still binds).

```python
import neatlogs, requests

# Caller — inject before sending.
with neatlogs.trace("caller"):
    headers = {"content-type": "application/json"}
    if neatlogs.inject_trace_context(headers):
        requests.post(url, headers=headers, json=payload)

# Callee (e.g. a FastAPI/Flask handler) — extract to continue the trace.
@app.post("/tool")
def handle(req):
    with neatlogs.extract_trace_context(
        req.headers,
        session_id=req.session_id,   # identity does NOT ride the wire — re-bind it here
        parent_session_id=req.parent_session_id,
        session_custom_fields=req.session_custom_fields,
        end_user_id=req.user_id,
    ):
        with neatlogs.trace("do_tool"):   # joins the caller's trace as a child
            ...
```

> Use these helpers, **NOT** a bare `opentelemetry.propagate.inject(headers)` — the bare call reads the global propagator, which under NeatLogs' private-provider isolation does not see the active span and writes an empty carrier. Identity does not travel on the `traceparent`; re-bind it on the callee from the request payload. Peers in Go and TypeScript (`injectTraceContext` / `extractTraceContext`) speak the same W3C wire format.

---

## Supported Instrumentations

Pass these string values in the `instrumentations=[]` list to `neatlogs.init()`.

### LLM Providers

| Key | Library | Notes |
|---|---|---|
| `openai` | OpenAI (`OpenAI()` and `AzureOpenAI()`) | Tested end-to-end |
| `anthropic` | Anthropic | Tested |
| `google_genai` | Google Generative AI (`google.genai`) | Tested. Client must be created **after** `init()` — see troubleshooting |
| `azure_ai_inference` | Azure AI Inference | Tested for direct Azure AI Inference calls |
| `litellm` | LiteLLM | Tested end-to-end with `gemini/*` message lists |
| `bedrock` | AWS Bedrock | Tested. `boto3>=1.42.11` |

### Agent Frameworks

| Key | Framework | Notes |
|---|---|---|
| `langchain` | LangChain (incl. LangGraph execution) | Tested end-to-end |
| `langgraph` | LangGraph — use `instrumentations=["langchain"]` | Tested via LangChain |
| `crewai` | CrewAI | Valid zero-touch path for a bare Crew; no provider key is needed. Prefer `wrap(crew)` for workflow metadata and use it for Flows / standalone Agents |

#### CrewAI routing rule

The CrewAI hook patches `LLM.call` directly, independent of whether the model is OpenAI, Azure, Gemini, Anthropic, or local. Use `instrumentations=["crewai"]` alone for a bare Crew, or `neatlogs.wrap(crew)` as the preferred instance path. Do not pair CrewAI with a provider key based on the model string; that can double-fire the LLM span.

### Vector Databases

| Key | Library | Notes |
|---|---|---|
| `chromadb` | ChromaDB | Auto-instrumented |
| `pinecone` | Pinecone | Auto-instrumented |
| `qdrant` | Qdrant | Auto-instrumented |
| `weaviate` | Weaviate | Auto-instrumented |

> If you use LangChain retrievers wrapping these (very common for RAG apps), `instrumentations=["langchain"]` already captures the retrieval spans automatically — a dedicated vector-DB key is only needed when you call the DB client directly.

### Other

| Key | Library | Notes |
|---|---|---|
| `mcp` | Model Context Protocol | Tested |

---

## Reference Docs

For deep dives, see the companion reference files:

- **Custom instrumentation** with decorators and traces → [`references/decorators-and-traces.md`](references/decorators-and-traces.md)
- **Framework-specific** integration patterns → [`references/framework-integrations.md`](references/framework-integrations.md)
- **Troubleshooting** and common mistakes → [`references/troubleshooting.md`](references/troubleshooting.md)
- **Multiple independent workflows in one codebase** (a copilot + a summarizer + a background job, each a distinct dashboard workflow) → use the `neatlogs-multi-workflow` skill. `init(workflow_name=...)` is process-wide/single-shot; give each feature its own `WORKFLOW` root and set the canonical per-root `neatlogs.workflow.name` attribute via `span.set_attribute(...)`.

---

## Environment Variables

| Variable | Description |
|---|---|
| `NEATLOGS_API_KEY` | API key (alternative to `api_key` param) |

---

## Data Masking and PII

NeatLogs supports both client-side and server-side PII redaction.

### Client-Side Masking

Provide a `mask` callback to `init()` to redact sensitive data before spans leave the process. You can also pass `mask=fn` per-span via `@span(mask=fn)` or `trace(..., mask=fn)`.

The mask function receives a span dict and should return the (possibly mutated) span dict:

```python
def redact_pii(span):
    attrs = span.get("attributes", {})
    for key in list(attrs):
        if "email" in key or "password" in key:
            attrs[key] = "[REDACTED]"
    return span

neatlogs.init(mask=redact_pii)
```

The example above is illustrative — real redaction logic should target the specific attribute names your application writes (common ones: `input.value`, `output.value`, `llm.input_messages.*.message.content`).

### Server-Side PII Redaction

Enable automatic server-side redaction via `init()`. `pii_entities` / `pii_span_types` are
persisted to the project, so the dashboard reflects whatever you pass here:

```python
neatlogs.init(
    pii_enabled=True,
    pii_entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"],  # None = keep saved selection
    pii_span_types=["LLM", "TOOL"],                            # None = keep saved selection
)
```

---

## Documentation

Full documentation: [https://docs.neatlogs.com/](https://docs.neatlogs.com/)
