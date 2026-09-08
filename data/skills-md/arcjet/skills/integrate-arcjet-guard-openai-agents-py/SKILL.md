---
name: integrate-arcjet-guard-openai-agents-py
description: Integrate Arcjet Guard into Python OpenAI Agents — wrap FunctionTool / function_tool with guard_tool and read a caller-owned session or conversation id via openai_agents_context. Use when asked to add Arcjet to openai-agents, Runner.run, rate limit those tools, screen inbound messages, or block prompt injection / PII. This is Python openai-agents, not the JS @openai/agents adapter.
license: Apache-2.0
compatibility: Requires Python >= 3.10 and official openai-agents>=0.19.0,<1 via arcjet[openai-agents] on PyPI arcjet 1.0.0. This is text Agent + Runner.run + authored FunctionTool — not Realtime, Sandbox, hosted, MCP, Computer / Shell / ApplyPatch, handoffs, or Agent.as_tool().
metadata:
  author: arcjet
  type: core
  library: arcjet
---

# Integrate Arcjet Guard into Python OpenAI Agents

`arcjet.guard.openai_agents` wraps the agent's existing Arcjet client. It
never talks to the Arcjet API itself. Shared Guard fundamentals (client,
rules, labels, decisions, capture, registration) live in
[../arcjet/references/guards_python.md](../arcjet/references/guards_python.md).
Load that reference for anything that is not OpenAI Agents-specific.

Official `openai-agents>=0.19.0,<1` only — not the JS `@openai/agents`
adapter (`@arcjet/guard/openai-agents/v0`, docs
https://docs.arcjet.com/guards/openai-agents/), not community forks.
Importing `arcjet.guard.openai_agents` does not load LangChain.

Exports: `guard_tool`, `openai_agents_context`. Authored `FunctionTool` /
`@function_tool` only. Not hosted tools, MCP, Computer / Shell /
ApplyPatch, handoffs, or `Agent.as_tool()`.

Two surfaces, one decision rule:

- **An authored `FunctionTool`** → `guard_tool`. Gate is
  `FunctionTool.tool_input_guardrails` + `reject_content` (JSON of
  `ArcjetDenialResult`). Do **not** raise.
- **Correlation** → `openai_agents_context` reads a caller-owned session
  / conversation id. It never mints. It never reads `trace_id`.

Docs: https://docs.arcjet.com/guards/openai-agents/.

## The gate is `tool_input_guardrails` + `reject_content`

`guard_tool` returns a copy whose input guardrails start with Arcjet, so
`on_invoke_tool` never runs on `DENY` (or unevaluated Guard under the
default `on_guard_error="deny"`). Denial is
`ToolGuardrailFunctionOutput.reject_content` with JSON of
`ArcjetDenialResult` (`{ arcjetDenied: true, … }`). Do **not** raise —
`raise_exception()` is a tripwire halt, and a raise from
`on_invoke_tool` is swallowed by `default_tool_error_function`. Same
fail-closed default as [#196](https://github.com/arcjet/arcjet-py/pull/196):
only `"allow"` fails open; a `DENY` always blocks. Core `guard()` still
fails open (`has_failed_open()`).

## `needs_approval` is not a policy gate

`needs_approval` is human-in-the-loop (`state.approve` / `state.reject`).
Same trap as JS OpenAI Agents `needsApproval`, LangGraph `interrupt()`,
and Genkit `interrupt()`. There is no inbound helper and no approval
helper. `RunConfig.tool_execution.pre_approval_tool_input_guardrails=True`
is an application opt-in only — this helper does not set it.

## Screen inbound before `Runner.run`

There is no inbound helper. SDK `input_guardrails` / `output_guardrails`
/ tool output guardrails are the SDK's own tripwires, not Arcjet. Call
`aj.guard(...)` in the application and **act on the decision**. Core
`guard()` fails open: `ALLOW` is not proof the rules ran. Gate on
`decision.has_failed_open()` if this call site must fail closed;
`guard_tool` already defaults to that.

## Questions to ask the human first

Ask only what you cannot infer from the code; suggest defaults.

1. Which tools are **risky** (external side effects, irreversible, spends
   money, sends messages)? Those get `guard_tool`. Hosted / MCP /
   handoffs / `as_tool` are out of scope.
2. What **limits**? (e.g. "10 lookups/min per user" → `TokenBucket`.)
3. Who is the **user** for metadata — an opaque user/tenant ID (never PII)?
   Default: none. Put the conversation / session id you already have on
   the app context you pass to `Runner.run`. That id is the correlation
   id, not the user.
4. Is an Arcjet outage unacceptable? Every helper defaults to
   `on_guard_error="deny"`. Ask explicitly about inbound screening before
   `Runner.run`: failing closed there means the agent does not run, so
   `"allow"` is a routine and legitimate choice at that one call site.

## The things readers get wrong

1. **This is not the JS adapter.** Do not import
   `@arcjet/guard/openai-agents/v0`.
2. **There is no inbound helper.** SDK guardrails are not Arcjet. Screen
   with core `guard()` before `Runner.run`.
3. **`needs_approval` is HITL, not policy.**
4. **Denial is `reject_content` only.** A raise is a tripwire halt or is
   swallowed by `default_tool_error_function`.
5. **Correlation is read, never minted.** Never `trace_id`. Never
   construct `OpenAIConversationsSession()`.
6. **Key rate limits on the authenticated caller**, not a model-supplied
   order id. Hand the agent the copy `guard_tool` returns — the original
   stays unguarded.
7. **Do not hand-wrap every tool with raw `guard()`.**
8. **`inputs=` is accepted.** A missing decision is not a denial —
   verify in Console/CLI.

## Step 1: Install and find the guard client

This module ships in PyPI `arcjet` **1.0.0**:

```bash
pip install "arcjet[openai-agents]"
```

If the agent has no guard client yet, launch one **once at module scope**:

```python
import os
from arcjet.guard import launch_arcjet

aj = launch_arcjet(key=os.environ["ARCJET_KEY"])
```

## Step 2: Gate authored tools — `guard_tool`

```python
from agents import Agent, Runner, function_tool
from arcjet.guard import DetectPromptInjection, TokenBucket, launch_arcjet
from arcjet.guard.openai_agents import guard_tool, openai_agents_context

aj = launch_arcjet(key=os.environ["ARCJET_KEY"])
lookup_limit = TokenBucket(
    label="order.looked-up",
    bucket="lookups",
    refill_rate=10,
    interval_seconds=60,
    max_tokens=10,
)
user_id = authenticated_user_id

@function_tool  # needs_approval=... is HITL — not this policy gate
def lookup_order(order_number: str) -> dict:
    """Look up an order by number."""
    return {"order_number": order_number, "status": "shipped"}

lookup_order = guard_tool(
    guard=aj,
    tool=lookup_order,
    action="order.looked-up",
    rules=[lookup_limit(key=user_id, requested=1)],
    on_guard_error="deny",
)

agent = Agent(
    name="support-agent",
    instructions="Help the user.",
    tools=[lookup_order],
)
```

Use `action` + `rules` on `guard_tool`.

## Step 3: Screen inbound before `Runner.run`

```python
inbound = DetectPromptInjection()
app_context = {"session_id": conversation_id}
derived = openai_agents_context(app_context)
decision = await aj.guard(
    label="message.received",
    rules=[inbound(user_text)],
    correlation_id=derived.correlation_id,
)
if decision.conclusion == "DENY":
    raise Exception("message blocked")
if decision.has_failed_open():
    raise Exception("inbound guard unavailable")

await Runner.run(agent, user_text, context=app_context)
```

There is no inbound helper.

## Step 4: Correlation

`openai_agents_context` reads a caller-owned id. Preference: fields on
`runContext.context` / a bare app object (`correlation_id`, then
`session_id`, then `conversation_id`, then `group_id`, snake or
camelCase), then the same names on the envelope, then
`correlation_id=` / `session_id=` kwargs, then an enclosing
`arcjet_sequence`. It returns `OpenAIAgentsContext` — pass
`.correlation_id` to `guard()`. It never mints an id. It never reads
`trace_id`. It never constructs `OpenAIConversationsSession()`. Do not
invent a correlation id per turn.

## Verify the integration

1. `python -m py_compile` (or the project's type-check) passes.
2. Exercise inbound PI (before `Runner.run`), a tool deny
   (`reject_content`, not a raise), a rate limit, and fail-closed (an
   unreachable guard). Confirm `needs_approval` is never treated as the
   gate.
3. Confirm in the Arcjet Console / CLI that decisions share the
   caller-owned session / conversation id — not a `trace_id`.
4. Manual E2E with a real `ARCJET_KEY` is still-to-verify until you run it.

The example `fastapi-openai-agents-guard` stays with Runtime — do not
invent a new example name. Do not add an example in this skills repo.
