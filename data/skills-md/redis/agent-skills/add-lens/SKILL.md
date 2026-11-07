---
name: add-lens
description: Add Redis Iris Lens tracing to an existing AI agent through redis-iris, so every agent turn is one trace in the Lens UI with its LLM calls, tokens, tool calls, memory and document retrievals, and which of them entered the prompt. Detects how the agent runs (LangGraph or ADK attach, workflows.turn, another framework, or a plain loop), installs redis-iris[llm-tracing], calls lens.init(agent_id=...), opens one lens.turn() per turn where Iris does not open it already, and covers coexistence with an OpenTelemetry setup or LLM instrumentation the app already has. Use when the user asks to add Lens, tracing, observability, or per-turn traces to their agent, or asks why their Lens traces are missing.
license: MIT
metadata:
  author: redis
  version: "1.0.0"
---

# Add Lens

One trace per agent turn, visible in the Lens UI under the agent's `agent_id`. Lens runs inside `redis-iris`; it has no service to provision and no CLI. Two lines at start-up, one turn per message, then close the gaps the agent has. Lens sits next to any other Iris product, or none.

Full reference: Lens (`docs/core/lens.md` in `redis-iris`).

## 1. Discover

Read the project:

- **The turn**: where one user message becomes one answer (`app.invoke`, `Runner.run`, `runner.run_async`, `agent.run`, `kickoff`, or the handler around a hand-written loop).
- **The ids**: where the agent's own name lives, and where each request's session or thread id and user id live. Always set both `agent_id` and `session_id`. Every Lens UI view is filtered by `agent_id`, so a trace without one never shows. Turns are shown grouped by session, so a turn without a session id does not show either (showing turns without a session is an upcoming feature).
- **Start-up**: the one place that runs before the first turn (app factory, `main`, worker boot).
- **The model client**: the library that finally calls the model, under any framework. Lens instruments four: `openai`, `anthropic`, `botocore` (Bedrock) and `langchain_core`. Many frameworks call one of these underneath; confirm in step 2. Any other client (for example `google-genai` or `litellm`) records no LLM span and no tokens unless step 6 adds an instrumentor for it.
- **Existing telemetry**: `opentelemetry`, `TracerProvider`, `opentelemetry-instrument`, `OTEL_*` variables, or another LLM instrumentation. Note who installs the global provider and when.
- **The gaps** in step 5: `.client` calls, custom retrieval, thread pools, process hops, short-lived processes.

Then match the shape. It decides who opens the turn:

| The agent | Turn opened by | You add |
|---|---|---|
| `redis_iris.integrations.langgraph.attach(hooks, graph)` | `attach`, on every `invoke` / `stream` and async twin, session from `configurable.thread_id`, user from `configurable.user_id` | `lens.init()` only |
| `workflows.turn(...)` / `workflows.aturn(...)` | `workflows.turn`, from `session=` and `owner=` | `lens.init()` only |
| LangGraph without `attach` | you | `lens.turn()` around `app.invoke` / `app.ainvoke`, thread id as the session |
| Google ADK, including `redis_iris.integrations.adk.attach` | you: ADK `attach` does not open one, so `before` and `after` would be two traces | `lens.turn()` around `runner.run_async` |
| OpenAI Agents SDK | you | `lens.turn()` around `Runner.run` |
| Pydantic AI, CrewAI, any other framework | you | `lens.turn()` around `agent.run` / `kickoff` |
| Plain loop (`openai`, `anthropic`, another client) | you | `lens.turn()` around the handler for one message, not around one model call |

Two loops in one process: each opens its own turns at its own seam. A turn already open is kept; `attach` and `workflows.turn` add none inside it.

## 2. Get current facts from MCP

Do this before writing code. Never guess framework APIs from memory.

- Framework docs: query an available docs MCP (Context7, or the framework's own) for the installed version's run entry point, which model client it calls underneath, whether it emits OpenTelemetry spans of its own, and whether it runs work on threads or other processes.
- Redis docs: if the Redis docs MCP is connected, use it for Lens concepts.
- No MCP available: read the installed package source in the virtualenv. Say so in the report.

## 3. Install and configure

Always install the extra. It brings the instrumentation `lens.init()` starts for OpenAI, Anthropic, Bedrock and LangChain, `mcp` and `threading`; without it there are no LLM spans and no token totals.

- `uv.lock` or `[tool.uv]` present: `uv add 'redis-iris[llm-tracing]'`.
- Poetry: `poetry add 'redis-iris[llm-tracing]'`.
- Otherwise add `redis-iris[llm-tracing]` to the project's requirements file.

The endpoint and the agent key come from the Lens UI. There is no CLI command that mints them, so hand off: tell the person to open the Lens UI, copy the Lens endpoint, create an agent key, and put both in `.env` as below. Never ask for the key in chat, pass it on a command line, or echo, `cat` or `grep` an env file.

```bash
IRIS_LENS_ENDPOINT=   # the Iris host, such as https://iris.example.com
IRIS_LENS_API_KEY=    # the Lens agent key
```

Add the same two names to `.env.example` with empty values. Never commit `.env`. On-prem inside the cluster, the endpoint can be plain http (`http://lens-dataplane:9000`) only with `IRIS_LENS_ALLOW_INSECURE=true`.

Leave content capture at its default. Do not ask about it.

## 4. Wire

At start-up, once, before the first turn and after the app's own OpenTelemetry setup (step 6):

```python
import logging

from redis_iris import lens

lens.init(agent_id="support-bot")  # always: every Lens UI view is filtered by agent_id
state = lens.instrumentation()
if state.get("lens") != "on":
    logging.warning("Lens is not recording: %s", state)
```

Always pass `agent_id`, even though the signature does not force it: a trace without one never shows in the Lens UI. Pick it from the agent's own name and confirm it with the person. `lens.init()` reads the endpoint and key from the environment and never raises. Its return value only says an endpoint is set and Lens is not switched off; it is still `True` for a refused endpoint or a missing extra, so check `lens.instrumentation()` instead.

Then, where step 1 says "you", wrap one turn:

```python
with lens.turn(thread_id, user_id=user_id) as t:
    answer = await Runner.run(agent, message)  # the framework's run call, unchanged
    t.set_outcome("completed")
```

`async with` is not needed: `lens.turn()` is a plain context manager and works around `await`. The first argument is the session id. Always pass the request's real thread or session id, never a constant and never `None`: the Lens UI shows turns by session, and a turn without one does not show yet. Set `IRIS_LENS_STRICT=true` while wiring so a missing session id raises instead of being stamped with a sentinel. `t.trace_id` is the turn's id in Lens, worth logging next to the request id.

## 5. Close the gaps

Only the ones step 1 found.

**`.client` calls.** `memory.client`, `playbook.client` and the other `.client` properties are the generated SDK; Lens does not patch them, so the turn shows a gap. Prefer the goal-object method. Otherwise wrap the call:

```python
with lens.span("agent_memory.get_long_term_memory", memory_id=memory_id):
    raw = memory.client.get_long_term_memory(memory_id=memory_id)
```

**Custom retrieval.** A vector store, search API or database read that feeds the prompt: record what came back, then what entered the prompt, so the trace shows "5 retrieved, 3 used".

```python
with lens.retrieval(query=message, data_source="kb") as r:
    docs = index.search(message, k=5)
    r.results([(d.id, d.score, d.text) for d in docs])

with lens.prompt_assembly() as p:
    p.fetched([(d.id, d.score, d.text) for d in docs])
    p.used([(d.id, d.score, d.text) for d in docs[:3]])  # whatever survived the token limit
```

Memory the agent reads from its own store uses `lens.memory_recall(query=, store_id=)` the same way. Iris `hooks()` and `disclosure()` record their own `prompt_assembly`; do not add one for their block.

**Thread pools.** `ThreadPoolExecutor` work keeps the turn only with the `threading` instrumentation from `[llm-tracing]` under `lens.init()`. `asyncio` tasks and `asyncio.to_thread` keep it anyway. If `IRIS_LENS_INSTRUMENT_THREADS=false` is set, remove it.

**Process hops.** A queue, Celery task, subprocess or worker the turn hands off to starts a new trace unless the context travels with it:

```python
payload["lens"] = lens.inject()  # sender, inside the turn

with lens.continue_from(payload.get("lens")):  # receiver, around the work
    handle(payload)
```

Send the carrier only to your own services, never to a third party or an MCP call's `meta`, and never pass `continue_from` a carrier built from an untrusted caller's headers. The receiving process calls `lens.init()` with the same `agent_id`. HTTP calls already instrumented by OpenTelemetry carry `traceparent` themselves.

**Short-lived processes.** A script, CLI, batch job or test run can exit before the exporter flushes. Call `lens.shutdown(timeout_millis=5_000)` once, at the very end. It turns Lens off for the rest of the process, so never call it per turn, per request, or per warm Lambda invocation.

## 6. Live with existing telemetry

Lens never replaces a provider. If the app has an OpenTelemetry SDK `TracerProvider`, Lens adds its processor to it at the first turn; if there is none, Lens installs one.

| The app already has | Do |
|---|---|
| Its own OpenTelemetry SDK setup, or `opentelemetry-instrument` | Make sure it runs before the first turn. If the app configures OpenTelemetry late, set `IRIS_LENS_OWN_PROVIDER=false` so Lens waits for it instead of installing one first. The app's own exporters then also receive the spans recorded inside a turn, content included, and a turn is its own trace, linked to the request span. |
| An instrumentation that already wraps one of Lens's four clients | Lens leaves that client alone (`other_instrumentation`). Its spans reach Lens inside a turn when it records on the same global provider; set it up before `lens.init()` and the first turn. |
| A model client Lens does not instrument | Add an OpenTelemetry instrumentor for that client, or turn on the framework's own OpenTelemetry tracing (step 2 says whether it has one), recording on the global provider. Its spans inside a turn go to Lens, and the turn's token totals count them when they carry `gen_ai.usage.input_tokens` / `output_tokens` (or the `prompt_tokens` / `completion_tokens` names). Ask the person before adding a dependency. |
| A tracer provider that is not the OpenTelemetry SDK's | Lens cannot add its processor and logs `iris.lens: could not attach, telemetry disabled`. Report it; do not change the app's tracing. |
| A sampler below 100% | Lens force-samples turns by default. `IRIS_LENS_SAMPLE_TURNS=inherit` lets the app's sampler drop them. |

Set nothing in `OTEL_EXPORTER_OTLP_*` for Lens: its exporter reads no `OTEL_EXPORTER_OTLP_*` variable. It does honour `HTTPS_PROXY`, `NO_PROXY` and `SSL_CERT_FILE`.

## 7. Verify

1. Run the agent's start-up and print `lens.instrumentation()` after the LLM client is imported. Expect `'lens': 'on'` and, when the agent uses OpenAI, Anthropic, Bedrock or LangChain, that client under `providers` as `instrumented` or `other_instrumentation`. Any other client has no entry there; check its own instrumentor's spans in step 4 instead.
2. A value is wrong? Read the cause from `lens.instrumentation()`:

   | Value | Cause | Fix |
   |---|---|---|
   | `lens: off` | No `IRIS_LENS_ENDPOINT` in the process, `IRIS_LENS_ENABLED=false`, or `opentelemetry-sdk` is missing (a `--no-deps` install) | Load `.env` before `lens.init()`; unset the switch; reinstall with dependencies |
   | `lens: endpoint_refused` | The endpoint is not https and not loopback | https, or `IRIS_LENS_ALLOW_INSECURE=true` on-prem |
   | `lens: shut_down` | `lens.shutdown()` ran earlier in the process | Move it to the end of the process |
   | `providers.<client>: instrumentor_missing` or `needs_wrapt` | `[llm-tracing]` is not installed in this environment | Install the extra in the environment the agent runs in |
   | `providers.<client>: needs_init` | Lens is on from the environment, but `lens.init()` never ran | Call it at start-up |
   | `providers.<client>: disabled` | `IRIS_LENS_AUTO_INSTRUMENT=false` | Unset it |
   | `providers.<client>: failed` | Patching did not apply | Read the `iris.lens: could not auto-instrument` warning. It is logged at `lens.init()`, or later, when the app first imports the client |

3. Run one real turn with a real session id and log `t.trace_id` (or `lens.current_trace_id()` from inside the run).
4. Open the Lens UI, filter by the `agent_id`, and find the session and that turn. It should show the LLM call, its tokens, and every Iris product, tool and retrieval span the turn made.
5. Empty UI with `lens: on`: check the `iris.lens` warnings (a 401 or 403 on export means a wrong or revoked key), that the turn ended before the process did (step 5, short-lived processes), and `lens.stats()`: `iris.lens.spans_exported` should grow, `iris.lens.export_failures` stay 0, and `iris.lens.identity_unassigned` stay 0 (non-zero means a turn was opened without a session id, so it does not show in the UI).

## 8. Report

List the agent shape and who opens the turn, the `agent_id`, where the session and user ids come from, the model client and whether Lens instruments it, the gaps you closed, how Lens coexists with the existing telemetry, the `lens.instrumentation()` output, the trace id you found in the Lens UI, and anything you could not confirm over MCP.

## Rules

- Keep the user's framework, graph, and prompts. Smallest diff.
- Only use APIs in `redis_iris.lens`. Never call `trace.set_tracer_provider()` or `trace.get_tracer()` for Lens.
- Lens never raises into the agent (except under `IRIS_LENS_STRICT`), so it needs no try/except.
- Never ask for a secret in chat. Never commit `.env`.
- Other Iris products: `add-redis-iris`.
