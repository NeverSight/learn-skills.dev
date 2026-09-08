---
name: integrate-arcjet-guard-claude-managed-agents-py
description: Integrate Arcjet Guard into Python Claude Managed Agents — screen user.message with guard_events before sessions.events.send, and gate custom tools on agent.custom_tool_use with guard_custom_tool. Use when asked to add Arcjet to hosted Claude Managed Agents, anthropic beta sessions, rate limit custom tools, or block prompt injection on hosted sessions. Not Claude Agent SDK local query() / PreToolUse.
license: Apache-2.0
compatibility: Requires Python >= 3.10 and official anthropic>=0.92.0,<2 via arcjet[claude-managed-agents] (safe extra, no chromadb). Peer is anthropic, not claude-agent-sdk. Until-published — pin arcjet to git SHA 582372916d70311873ef24b7a72443c098b3aec9; not in PyPI 1.0.0.
metadata:
  author: arcjet
  type: core
  library: arcjet
---

# Integrate Arcjet Guard into Python Claude Managed Agents

`arcjet.guard.claude_managed_agents` wraps the agent's existing Arcjet
client. It never talks to the Arcjet API itself. Shared Guard
fundamentals (client, rules, labels, decisions, capture, registration)
live in
[../arcjet/references/guards_python.md](../arcjet/references/guards_python.md).
Load that reference for anything that is not Claude Managed
Agents-specific.

Official `anthropic>=0.92.0,<2` only — not `claude-agent-sdk`, not
`arcjet.guard.claude_agent_sdk`, not the JS
`@anthropic-ai/claude-agent-sdk` adapter, and not JS Claude Managed
Agents (`@arcjet/guard/claude-managed-agents/v0`, docs
https://docs.arcjet.com/guards/claude-managed-agents/). Importing
`arcjet.guard.claude_managed_agents` does not load Claude Agent SDK,
LangChain, or CrewAI. The extra is safe (no chromadb).

This is the hosted Claude Managed Agents harness
(`client.beta.sessions`). Anthropic runs the agent loop and the built-in
toolset (`bash`, files, web_*). The agent toolset defaults to
`always_allow`, so there is **no customer pre-exec** for bash/files —
`agent.tool_use` / `agent.tool_result` fire after the built-in already
ran. There is no `PreToolUse`. Do not paper over that gap with
`always_ask`. It is not Claude Agent SDK local `query()` / `guard_hooks`.

Exports: `guard_custom_tool`, `guard_events`,
`claude_managed_agents_context`. There is no `guard_inbound`, no
`guard_tool`, and no `guard_tool_confirmation`.

Three surfaces, one decision rule:

- **Inbound text** (`user.message` / `initial_events`) → `guard_events`
  wraps `sessions.events.send`. DENY raises `ArcjetDeniedError` /
  `ArcjetUnavailableError` and does not call send.
- **A custom tool you execute** (`agent.custom_tool_use`) →
  `guard_custom_tool(run=…)`. DENY does not run the original `run`; the
  helper sends `user.custom_tool_result` with schema field `is_error`.
- **Correlation** → `claude_managed_agents_context` reads a caller-owned
  `correlation_id` / `session_id`. It never mints. It never reads
  Anthropic `session.id` / `sevt_…`.

Docs: https://docs.arcjet.com/guards/claude-managed-agents/ (shared
JS+Python page). Do not use `/guards/claude-agent-sdk/`. There is no separate
`/guards/claude-managed-agents-py/` page. JS adapter is not in npm
1.11.0 — pin `@arcjet/guard` to `cb35c8f92c3a2fb63fbeb9b386d79b1878c19d92`.

## The real gates are inbound `user.message` and custom tools

`guard_events(send=client.beta.sessions.events.send, …)` wraps the send
callable so `user.message` / `initial_events` are evaluated **before**
the original send runs — the only place a turn can be declined before
the hosted harness reads the prompt. Inbound `rules` receive
`{"prompt", "content", "type"}` from `message_arguments()` — not the JS
`{ text, events }`. `guard_custom_tool(run=…)` returns
`await handler(event, send=…, session_id=…)`. Built-ins never enter that
handler. Optional `tool=` wraps a self-hosted `@beta_tool` `run` the
same way; the CLI worker cannot register custom tools.

## Custom-tool denial is `user.custom_tool_result` with `is_error`

On `DENY` (or unevaluated Guard under the default
`on_guard_error="deny"`) the original `run` is not called. The helper
sends a real `user.custom_tool_result` (`custom_tool_use_id`, JSON of
`ArcjetDenialResult` on `content`, **`is_error`** — that field is on the
events schema; do not invent a second one). Do **not** raise from the
hosted handler: a throw leaves the session idle. Omitting `is_error`
looks like success. This is not Claude Agent SDK `structuredContent`.
Same fail-closed default as
[#196](https://github.com/arcjet/arcjet-py/pull/196). Core `guard()`
still fails open.

## `always_ask` + `user.tool_confirmation` is not HITL-as-policy

Permission policies apply to the agent toolset and MCP, not custom
tools. Same trap as CrewAI `human_input`, JS `canUseTool`, and LangGraph
`interrupt()`. MCP Guard only on servers you host — Anthropic is the
MCP client. `web_search` / `web_fetch` always run on Anthropic.

## Questions to ask the human first

Ask only what you cannot infer from the code; suggest defaults.

1. Which **custom tools** does the app execute on
   `agent.custom_tool_use`? Those get `guard_custom_tool`. Built-ins
   under `always_allow` cannot.
2. What **limits**? (e.g. "10 lookups/min per user" → `TokenBucket`.)
3. Who is the **user** for metadata — an opaque user/tenant ID (never PII)?
   Default: none. Anthropic `session.id` / `sevt_…` are not the
   correlation id.
4. Is an Arcjet outage unacceptable? Every helper defaults to
   `on_guard_error="deny"`. Ask explicitly about inbound `guard_events`:
   failing closed there means the turn is not sent, so `"allow"` is a
   routine and legitimate choice at that one call site.

## The things readers get wrong

1. **This is not the Claude Agent SDK.** No `guard_tool`, no
   `guard_hooks`, no `PreToolUse`, no `UserPromptSubmit`. Do not also
   wrap with `arcjet.guard.claude_agent_sdk` or
   `@arcjet/guard/claude-agent-sdk/v0`.
2. **There is no `guard_inbound`.** The helper is `guard_events`.
3. **Inbound ctx is `{"prompt", "content", "type"}`**, not JS
   `{ text, events }`.
4. **Correlation is caller-owned, never minted.** Do not pass Anthropic
   `session.id` / `sevt_…` / `trace_id` as correlation.
5. **Default `always_allow` cannot be gated.** Do not claim we can block
   Anthropic-cloud bash/files.
6. **On custom-tool DENY, send `user.custom_tool_result` with
   `is_error`.** Do not raise. On ALLOW the caller still sends the
   success result or the session idles.
7. **`always_ask` + `user.tool_confirmation` is opt-in confirmation,
   not policy.**
8. **Do not hand-wrap every session event with raw `guard()`.**
9. **`guard_events` has no `inbound=`.** `action` and `rules` sit at
   the top level; it takes `send=`; the returned callable replaces
   `send` and raises on DENY. `guard_custom_tool` takes `run=`, not
   `tool=<function>`. A missing decision is not a denial.

## Step 1: Install and find the guard client

Until-published: PyPI `arcjet` 1.0.0 does not include this module. Pin
`arcjet` to git SHA `582372916d70311873ef24b7a72443c098b3aec9` (current
`main`, includes the extra):

```bash
pip install "arcjet[claude-managed-agents] @ git+https://github.com/arcjet/arcjet-py.git@582372916d70311873ef24b7a72443c098b3aec9"
```

If the agent has no guard client yet, launch one **once at module scope**:

```python
import os
from arcjet.guard import launch_arcjet

aj = launch_arcjet(key=os.environ["ARCJET_KEY"])
```

Worked example:
[`examples/fastapi-claude-managed-agents-guard`](https://github.com/arcjet/arcjet-py/tree/main/examples/fastapi-claude-managed-agents-guard)
(pins `58237291`).

## Step 2: Screen inbound before `sessions.events.send`

```python
from anthropic import Anthropic
from arcjet.guard import DetectPromptInjection, TokenBucket, launch_arcjet
from arcjet.guard.claude_managed_agents import (
    claude_managed_agents_context,
    guard_custom_tool,
    guard_events,
)

client = Anthropic()
aj = launch_arcjet(key=os.environ["ARCJET_KEY"])
inbound = DetectPromptInjection()
user_id = authenticated_user_id
conversation_id = authenticated_conversation_id
derived = claude_managed_agents_context(session_id=conversation_id)

send = guard_events(
    guard=aj,
    send=client.beta.sessions.events.send,
    action="message.received",
    # Python inbound ctx is {"prompt", "content", "type"} — not JS { text, events }.
    rules=lambda ctx: [inbound(ctx["prompt"])],
    session_id=derived.correlation_id or conversation_id,
    on_guard_error="deny",
)

session = client.beta.sessions.create(agent=agent_id, environment_id=environment_id)
# Anthropic minted session.id — pass it to the sessions API, not as correlation.

# Screen user.message before the hosted harness reads it. DENY raises
# ArcjetDeniedError / ArcjetUnavailableError and does not send.
await send(
    session.id,
    events=[{"type": "user.message", "content": [{"type": "text", "text": user_text}]}],
)
```

## Step 3: Gate custom tools on `agent.custom_tool_use`

```python
lookup_limit = TokenBucket(
    label="order.looked-up",
    bucket="lookups",
    refill_rate=10,
    interval_seconds=60,
    max_tokens=10,
)

async def lookup_order(event) -> dict:
    order_id = event.input["order_id"]
    return {"content": [{"type": "text", "text": f"{order_id}: shipped"}]}

handle_lookup = guard_custom_tool(
    guard=aj,
    action="order.looked-up",
    run=lookup_order,
    rules=[lookup_limit(key=user_id, requested=1)],
    session_id=derived.correlation_id or conversation_id,
    on_guard_error="deny",
)

with client.beta.sessions.events.stream(session_id=session.id) as stream:
    for event in stream:
        if event.type == "agent.custom_tool_use" and event.name == "lookup_order":
            # DENY posts user.custom_tool_result with is_error. Do not raise.
            await handle_lookup(
                event,
                send=client.beta.sessions.events.send,
                session_id=session.id,
            )
        # agent.tool_use / always_ask + user.tool_confirmation are not this policy gate
```

Key rate limits on the authenticated caller, not a model-supplied order
id. On ALLOW the caller still sends the success `user.custom_tool_result`.

## Step 4: Correlation

`claude_managed_agents_context` is a reader that returns
`ClaudeManagedAgentsContext` (a dataclass) — not a context manager and
not a contextvar setter. It reads a **caller-owned** `correlation_id` /
`session_id`. It never mints. It never reads Anthropic `id` / `event_id`
/ `session.id` (`ses_…`) / `sevt_…` / `trace_id`. Passing an Anthropic
Session object is safe — those minted ids are ignored. An invalid
candidate is skipped; if nothing valid remains the call is uncorrelated
rather than joined to a generated id. Helpers also re-read
`session_id=` / `correlation_id=` internally.

## Verify the integration

1. `python -m py_compile` (or the project's type-check) passes.
2. Exercise inbound PI (send is not called), a custom-tool deny
   (`user.custom_tool_result` with `is_error`; `run` is not called), a
   rate limit, and fail-closed (an unreachable guard). Confirm
   `always_ask` / `user.tool_confirmation` is never treated as the gate
   and built-in `agent.tool_use` is observe-only.
3. Confirm in the Arcjet Console / CLI that decisions share the
   caller-owned conversation id — not an Anthropic `session.id` /
   `sevt_…`.
4. Manual E2E with a real `ARCJET_KEY` is still-to-verify until you run it.

Worked example:
[`examples/fastapi-claude-managed-agents-guard`](https://github.com/arcjet/arcjet-py/tree/main/examples/fastapi-claude-managed-agents-guard).
Do not invent a second example name. Do not add an example in this
skills repo.
