---
name: integrate-arcjet-guard-strands-agents-py
description: Integrate Arcjet Guard into Python Strands Agents — wrap authored @tool with guard_tool, and put guard_hooks on Agent(hooks=) for unwrapped / MCP tools via BeforeToolCallEvent.cancel_tool. Use when asked to add Arcjet to strands / strands-agents, rate limit those tools, screen inbound messages, or block prompt injection / PII. This is Python strands, not JS @strands-agents/sdk.
license: Apache-2.0
compatibility: Requires Python >= 3.10 and official strands-agents>=1.11.0,<2 via arcjet[strands-agents] (safe extra, no chromadb). 1.11.0 is the first 1.x with BeforeToolCallEvent.cancel_tool. Until-published — pin arcjet to git SHA 582372916d70311873ef24b7a72443c098b3aec9; not in PyPI 1.0.0.
metadata:
  author: arcjet
  type: core
  library: arcjet
---

# Integrate Arcjet Guard into Python Strands Agents

`arcjet.guard.strands_agents` wraps the agent's existing Arcjet client.
It never talks to the Arcjet API itself. Shared Guard fundamentals
(client, rules, labels, decisions, capture, registration) live in
[../arcjet/references/guards_python.md](../arcjet/references/guards_python.md).
Load that reference for anything that is not Strands-specific.

Official Python `strands` / `strands-agents>=1.11.0,<2` only — not JS
`@arcjet/guard/strands-agents/v1` (docs
https://docs.arcjet.com/guards/strands-agents/), not community forks.
Importing `arcjet.guard.strands_agents` does not load LangChain, CrewAI,
or JS `@arcjet/guard/strands-agents/v1`. Unlike CrewAI (no extra), the
`arcjet[strands-agents]` extra exists at the pin
(`strands-agents = ["strands-agents>=1.11.0,<2"]` in `pyproject.toml`).
The extra is safe (no chromadb).

Exports: `guard_tool`, `guard_hooks`, `strands_agent_context`. Authored
`@tool` plus `Agent(hooks=)` / `add_hook`.

Three surfaces, one decision rule:

- **An authored `@tool`** → `guard_tool`. Hand the agent the copy this
  returns — the original stays unguarded.
- **Unwrapped / MCP tools** → `guard_hooks`. Gate is per-tool
  `BeforeToolCallEvent.cancel_tool` (`True` or `str`). Already-wrapped
  tools are skipped so Guard is not called twice.
- **Correlation** → `strands_agent_context` reads a caller-owned id from
  `invocation_state`. It never mints. It never reads `trace_id`.

Docs: https://docs.arcjet.com/guards/strands-agents/. Example:
[`examples/fastapi-strands-agents-guard`](https://github.com/arcjet/arcjet-py/tree/main/examples/fastapi-strands-agents-guard)
(pins `58237291`; no verify fixture). Do not invent a second example
name.

## The gate is per-tool `BeforeToolCallEvent.cancel_tool`

`guard_hooks` registers on that event so the tool never runs on `DENY`
(or unevaluated Guard under the default `on_guard_error="deny"`). A
string is the cancel message (JSON of `ArcjetDenialResult`); `True` uses
Strands' default message and drops the fields. Fail closed: always set
`cancel_tool` on error — do not leave it unset and do not raise. Same
fail-closed default as [#196](https://github.com/arcjet/arcjet-py/pull/196):
only `"allow"` fails open; a `DENY` always blocks. Core `guard()` still
fails open (`has_failed_open()`).

## `event.interrupt()` is not a policy gate

`BeforeToolCallEvent.interrupt()` / resume is human-in-the-loop. Same
trap as CrewAI `human_input`, JS `humanInTheLoopMiddleware`, LangGraph
`interrupt()`, OpenAI Agents `needsApproval`, and Genkit `interrupt()`.
There is no inbound helper and no approval helper.

## Screen inbound before `Agent(...)` / `__call__` / `stream_async`

There is no inbound helper. Call `aj.guard(...)` in the application and
**act on the decision**. Core `guard()` fails open: `ALLOW` is not proof
the rules ran. Gate on `decision.has_failed_open()` if this call site
must fail closed; `guard_tool` / `guard_hooks` already default to that.

## Questions to ask the human first

Ask only what you cannot infer from the code; suggest defaults.

1. Which tools are **risky** (external side effects, irreversible, spends
   money, sends messages)? Those get `guard_tool`. MCP / unwrapped tools
   you did not author get `guard_hooks`.
2. What **limits**? (e.g. "10 lookups/min per user" → `TokenBucket`.)
3. Who is the **user** for metadata — an opaque user/tenant ID (never PII)?
   Default: none. Put the conversation / session id you already have on
   `invocation_state` *and* on `guard_hooks(...)`. That id is the
   correlation id, not the user.
4. Is an Arcjet outage unacceptable? Every helper defaults to
   `on_guard_error="deny"`. Ask explicitly about inbound screening
   before the agent runs: failing closed there means the agent does not
   run, so `"allow"` is a routine and legitimate choice at that one
   call site.

## The things readers get wrong

1. **This is not JS `@arcjet/guard/strands-agents/v1`.** Import
   `arcjet.guard.strands_agents`.
2. **There is no inbound helper.** Screen with core `guard()` before
   `Agent(...)` / `__call__` / `stream_async`.
3. **`event.interrupt()` is HITL, not policy.** Deny is
   `cancel_tool` (`True` or `str`).
4. **Fail closed = always set `cancel_tool` on error.** Do not raise
   and do not leave it unset.
5. **Correlation is read, never minted.** Never `trace_id`, never
   `agent.id`, never SessionManager auto-ids.
6. **Already-wrapped tools are skipped** by `guard_hooks` so Guard is
   not called twice. Hand the agent the copy `guard_tool` returns.
7. **Key rate limits on the authenticated caller**, not a model-supplied
   order id.
8. **Do not hand-wrap every Strands tool with raw `guard()`.**
9. **`inputs=` is accepted.** A missing decision is not a denial —
   verify in Console/CLI.

## Step 1: Install and find the guard client

Until-published: PyPI `arcjet` 1.0.0 does not include this module. Pin
`arcjet` to git SHA `582372916d70311873ef24b7a72443c098b3aec9` (current
`main`, includes the extra):

```bash
pip install "arcjet[strands-agents] @ git+https://github.com/arcjet/arcjet-py.git@582372916d70311873ef24b7a72443c098b3aec9"
```

If the agent has no guard client yet, launch one **once at module scope**:

```python
import os
from arcjet.guard import launch_arcjet

aj = launch_arcjet(key=os.environ["ARCJET_KEY"])
```

## Step 2: Gate authored tools — `guard_tool`

```python
from strands import Agent, tool
from arcjet.guard import DetectPromptInjection, TokenBucket, launch_arcjet
from arcjet.guard.strands_agents import guard_hooks, guard_tool, strands_agent_context

aj = launch_arcjet(key=os.environ["ARCJET_KEY"])
lookup_limit = TokenBucket(
    label="order.looked-up",
    bucket="lookups",
    refill_rate=10,
    interval_seconds=60,
    max_tokens=10,
)
mcp_limit = TokenBucket(
    label="mcp.invoked",
    bucket="mcp-access",
    refill_rate=20,
    interval_seconds=60,
    max_tokens=20,
)
inbound = DetectPromptInjection()
user_id = authenticated_user_id

@tool  # event.interrupt() is HITL — not this policy gate
def lookup_order(order_id: str) -> dict:
    """Look up an order by ID."""
    return {"order_id": order_id, "status": "shipped"}

lookup_order = guard_tool(
    guard=aj,
    tool=lookup_order,
    action="order.looked-up",
    rules=[lookup_limit(key=user_id, requested=1)],
    on_guard_error="deny",
)
```

## Step 3: Gate unwrapped / MCP tools — `guard_hooks`

```python
mcp_tools = []  # from an MCP client you did not wrap with guard_tool
agent = Agent(
    tools=[lookup_order, *mcp_tools],
    # The agent-wide gate for tools guard_tool did not wrap.
    # Already-wrapped tools are skipped, so Guard is not called twice.
    # BeforeToolCallEvent.cancel_tool is True or a str (JSON of the payload).
    hooks=[
        guard_hooks(
            guard=aj,
            action="mcp.invoked",
            rules=[mcp_limit(key=user_id, requested=1)],
            session_id=conversation_id,
            on_guard_error="deny",
        ),
    ],
)
```

## Step 4: Screen inbound before the agent runs

```python
invocation_state = {"sessionId": conversation_id}
derived = strands_agent_context(invocation_state)
decision = await aj.guard(
    label="message.received",
    rules=[inbound(user_text)],
    correlation_id=derived.correlation_id,
)
if decision.conclusion == "DENY":
    raise RuntimeError("message blocked")
if decision.has_failed_open():
    raise RuntimeError("inbound guard unavailable")

agent(user_text, invocation_state=invocation_state)
```

There is no inbound helper.

## Step 5: Correlation

`strands_agent_context` reads a caller-owned id from
`invocation_state`: `correlationId`, then `sessionId`, then `requestId`.
It never mints an id. It never reads `trace_id`. It never reads
`agent.id` or SessionManager auto-ids. Do not invent a correlation id
per turn. Put the same id on the invocation *and* on `guard_hooks(...)`.

## Verify the integration

1. `python -m py_compile` (or the project's type-check) passes.
2. Exercise inbound PI (before the agent runs), a `guard_tool` deny, a
   `guard_hooks` deny on an unwrapped tool (`cancel_tool` is `True` or
   a str), a rate limit, and fail-closed (an unreachable guard). Confirm
   `event.interrupt()` is never called as the gate.
3. Confirm in the Arcjet Console / CLI that decisions share the
   caller-owned session / request id — not a `trace_id` or `agent.id`.
4. Manual E2E with a real `ARCJET_KEY` is still-to-verify until you run it.

Worked example:
[`examples/fastapi-strands-agents-guard`](https://github.com/arcjet/arcjet-py/tree/main/examples/fastapi-strands-agents-guard).
Do not invent a second example name. Do not add an example in this
skills repo.
