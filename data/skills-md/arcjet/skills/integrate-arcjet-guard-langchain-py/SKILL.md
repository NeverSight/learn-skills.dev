---
name: integrate-arcjet-guard-langchain-py
description: Integrate Arcjet Guard into Python LangChain — wrap a BaseTool you call with guard_tool, put ArcjetMiddleware + ToolPolicy on create_agent, or observe a chain with ArcjetCaptureHandler. Use when asked to add Arcjet to LangChain, create_agent, langchain-core tools, rate limit those tools, screen inbound messages, or block prompt injection / PII. This is Python LangChain, not LangChain JS createAgent and not LangGraph JS.
license: Apache-2.0
compatibility: Requires Python >= 3.10 and PyPI arcjet 1.0.0. A BaseTool you call needs arcjet[langchain] (langchain-core>=1.2.5,<2). create_agent needs arcjet[langchain-agents] (langchain>=1.3,<2, langgraph>=1.2,<2).
metadata:
  author: arcjet
  type: core
  library: arcjet
---

# Integrate Arcjet Guard into Python LangChain

`arcjet.guard.langchain` wraps the agent's existing Arcjet client. It never
talks to the Arcjet API itself. Shared Guard fundamentals (client, rules,
labels, decisions, capture, registration) live in
[../arcjet/references/guards_python.md](../arcjet/references/guards_python.md).
Load that reference for anything that is not LangChain-specific.

Four surfaces, one decision rule:

- **Any Python callable** → `guard_action` / `guard_action_sync` in core
  `arcjet.guard`. No LangChain extra. Details in the shared Python Guard
  reference.
- **A LangChain `BaseTool` you call yourself** → `guard_tool`. DENY raises
  `ArcjetToolDeniedError` (the tool's `handle_tool_error` may convert it).
- **`create_agent` (the model chooses tools)** → `ArcjetMiddleware` +
  `ToolPolicy`. Tools without a policy pass through.
- **Observe a chain or agent** → `ArcjetCaptureHandler` /
  `ArcjetAsyncCaptureHandler`. These cannot deny.

This is Python `create_agent`. The merged page
https://docs.arcjet.com/guards/langchain/ covers both languages — JS is
`@arcjet/guard/langchain/v1` (`createAgent` / `wrapToolCall`), not this
module. It is not LangGraph JS `StateGraph` / `ToolNode` (docs
https://docs.arcjet.com/guards/langgraph/).
Importing `arcjet.guard.langchain` does not load LangGraph. Referencing
`ArcjetMiddleware` or `ToolPolicy` without `arcjet[langchain-agents]`
raises and names that extra.

## Screen inbound before `agent.ainvoke` — there is no inbound helper

There is no inbound helper. Put prompt-injection (and other inbound rules)
in the application with core `aj.guard(...)` before `ainvoke` / `invoke`.
Core `guard()` fails open: `ALLOW` is not proof the rules ran. Gate on
`decision.has_failed_open()` when this call site must fail closed.
`guard_tool` / `ArcjetMiddleware` already default to that.

## Capture handlers never block

LangChain ignores what a callback returns. `ArcjetCaptureHandler` only
records. Policy lives in `guard_action` / `guard_tool` / `ArcjetMiddleware`.

## Configure the tool before `guard_tool()`

Narrow `args_schema`, set `handle_tool_error` / `callbacks` /
`response_format` on the tool you still hold, then wrap. Changes on the
guarded handle do not reach the call.

## Questions to ask the human first

Ask only what you cannot infer from the code; suggest defaults.

1. Which tools are **risky** (external side effects, irreversible, spends
   money, sends messages)? A tool you call yourself gets `guard_tool`. A
   tool the model picks gets `ToolPolicy` on `ArcjetMiddleware`.
2. What **limits**? (e.g. "10 lookups/min per user" → `TokenBucket`.)
3. Who is the **user** for metadata — an opaque user/tenant ID (never PII)?
   Default: none. The conversation / session id you already have is the
   correlation id, not the user. Put it on
   `config["configurable"]["arcjet_correlation_id"]` or
   `with arcjet_sequence(correlation_id=...)`.
4. Is an Arcjet outage unacceptable? Every helper defaults to
   `on_guard_error="deny"`. Ask explicitly about inbound screening before
   `ainvoke`: failing closed there means the agent does not run for the
   duration of the outage, so `"allow"` is a routine and legitimate
   choice at that one call site.

## The things readers get wrong

1. **This is not LangChain JS and not LangGraph JS.** Do not import
   `@arcjet/guard/langchain/v1` or `@arcjet/guard/langgraph/v1`.
2. **There is no inbound helper.** Screen with core `guard()` before
   `ainvoke`.
3. **`ArcjetCaptureHandler` cannot deny.** Policy is `guard_tool` or
   `ArcjetMiddleware`.
4. **Correlation is caller-owned, never minted.** Do not mint a new id per
   turn. LangChain's `run_id` is not used. The config key wins over an
   enclosing `arcjet_sequence`; `configurable` is checked before
   `metadata`.
5. **Pass `tools=` the same sequence you gave `create_agent`.** A typo in
   a policy key is refused at construction instead of leaving that tool
   unguarded.
6. **Key rate limits on the authenticated caller**, not a model-supplied
   order id.
7. **`success` on helper capture is not "the action ran".**
   `guard_action` / `guard_tool` / `ArcjetMiddleware` write
   `metadata.outcome`. See the shared Python Guard reference.
8. **`rules=` is a static sequence**, not a lambda – a callable raises
   `TypeError`. Put per-argument checks in the tool body, or use
   `inputs=` (this adapter accepts typed inputs; the resolver is
   `(arguments, config)`).
9. **A missing decision is not a denial.** Verify in Console/CLI.

## Step 1: Install and find the guard client

These helpers ship in PyPI `arcjet` **1.0.0**. Install with the
project's package manager. Do not hand-edit `requirements.txt` with a
guessed version.

```bash
# guard_tool + capture handlers
pip install "arcjet[langchain]"
# ArcjetMiddleware + ToolPolicy
pip install "arcjet[langchain-agents]"
```

If the agent has no guard client yet, launch one **once at module scope**.
Use `launch_arcjet` in async code and `launch_arcjet_sync` in sync code.

```python
import os
from arcjet.guard import launch_arcjet

aj = launch_arcjet(key=os.environ["ARCJET_KEY"])
```

## Step 2: Gate a `BaseTool` you call — `guard_tool`

```python
from arcjet.guard.langchain import guard_tool

send_email.args_schema = PublicEmailArgs  # narrow first, then wrap
guarded = guard_tool(
    guard=aj,
    tool=send_email,
    action="email.sent",
    rules=[email_limit(key=user_id, requested=1)],
    on_guard_error="deny",
)
```

Needs `arcjet[langchain]`. The result is still a `BaseTool`. DENY raises
`ArcjetToolDeniedError`; unavailable raises `ArcjetToolUnavailableError`.
If you can name the tool at wiring time, `guard_tool` is the smaller
change.

## Step 3: Gate `create_agent` — `ArcjetMiddleware`

```python
from langchain.agents import create_agent
from arcjet.guard.langchain import ArcjetMiddleware, ToolPolicy

tools = [send_email, search_orders]
agent = create_agent(
    model="openai:gpt-4o",
    tools=tools,
    middleware=[
        ArcjetMiddleware(
            guard=aj,
            policies={
                "send_email": ToolPolicy(
                    action="email.sent",
                    rules=[email_limit(key=user_id, requested=1)],
                ),
            },
            tools=tools,
            on_guard_error="deny",
        )
    ],
)

await agent.ainvoke(
    {"messages": [...]},
    config={"configurable": {"arcjet_correlation_id": session.id}},
)
```

Needs `arcjet[langchain-agents]`. `guard=` is optional if you already
`register_arcjet()`. They compose: a guarded tool inside a guarded agent
evaluates each policy once and both land on the same Sequence.

## Step 4: Observe a chain — `ArcjetCaptureHandler`

```python
from arcjet.guard.langchain import ArcjetAsyncCaptureHandler, ArcjetCaptureHandler

# invoke → ArcjetCaptureHandler; ainvoke → ArcjetAsyncCaptureHandler
chain.invoke(inputs, config={"callbacks": [ArcjetCaptureHandler(guard=aj)]})
await chain.ainvoke(
    inputs, config={"callbacks": [ArcjetAsyncCaptureHandler(guard=aj)]}
)
```

Same extra as `guard_tool`. Pair the handler with the call. Neither can
deny a call.

## Step 5: Screen inbound and correlate

```python
from arcjet.guard import DetectPromptInjection

inbound = DetectPromptInjection()
decision = await aj.guard(
    label="message.received",
    rules=[inbound(user_text)],
)
if decision.conclusion == "DENY":
    raise RuntimeError("message blocked")
if decision.has_failed_open():
    raise RuntimeError("inbound guard unavailable")
```

Keep a whole run on one Sequence with
`with arcjet_sequence(correlation_id=session.id):` or
`config={"configurable": {"arcjet_correlation_id": session.id}}`. Do not
mint a new id per turn.

## Verify the integration

1. `python -m py_compile` (or the project's type-check) passes.
2. Exercise inbound PI (before `ainvoke`), a `guard_tool` deny, a
   middleware deny on a named policy, a capture-only handler that does
   **not** block, a rate limit, and fail-closed (an unreachable guard).
3. Confirm in the Arcjet Console / CLI (`guards list`) that decisions
   share the caller-owned correlation id.
4. Manual E2E with a real `ARCJET_KEY` is still-to-verify until you run it.

Worked example:
[`examples/fastapi-langchain-guard`](https://github.com/arcjet/arcjet-py/tree/main/examples/fastapi-langchain-guard).
Do not invent a second example name. Do not add an example in this skills
repo.
