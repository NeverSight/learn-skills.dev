---
name: integrate-arcjet-guard-claude-agent-sdk-py
description: Integrate Arcjet Guard into the Python Claude Agent SDK — wrap authored @tool with guard_tool, and use guard_hooks for UserPromptSubmit inbound plus PreToolUse on unwrapped built-ins / MCP. Use when asked to add Arcjet to claude-agent-sdk, rate limit those tools, screen inbound prompts, or block prompt injection / PII. This is Python claude-agent-sdk, not the JS adapter and not Claude Managed Agents hosted sessions.
license: Apache-2.0
compatibility: Requires Python >= 3.10 and official claude-agent-sdk>=0.2.127,<1 via arcjet[claude-agent-sdk] (safe extra, no chromadb). Until-published — pin arcjet to git SHA 582372916d70311873ef24b7a72443c098b3aec9; not in PyPI 1.0.0.
metadata:
  author: arcjet
  type: core
  library: arcjet
---

# Integrate Arcjet Guard into the Python Claude Agent SDK

`arcjet.guard.claude_agent_sdk` wraps the agent's existing Arcjet client.
It never talks to the Arcjet API itself. Shared Guard fundamentals
(client, rules, labels, decisions, capture, registration) live in
[../arcjet/references/guards_python.md](../arcjet/references/guards_python.md).
Load that reference for anything that is not Claude Agent SDK-specific.

Official `claude-agent-sdk>=0.2.127,<1` only — not the JS
`@anthropic-ai/claude-agent-sdk` adapter
(`@arcjet/guard/claude-agent-sdk/v0`, docs
https://docs.arcjet.com/guards/claude-agent-sdk/), not Vercel AI, not
community forks, and not Claude Managed Agents hosted
`client.beta.sessions` (`arcjet.guard.claude_managed_agents`). Importing
`arcjet.guard.claude_agent_sdk` does not load LangChain, CrewAI, or the
JS adapter. The extra is safe (no chromadb).

Exports: `guard_tool`, `guard_hooks`, `claude_agent_context`. Authored
`@tool` + `create_sdk_mcp_server` for tools you own; `guard_hooks` for
inbound `UserPromptSubmit` and unwrapped built-ins / MCP `PreToolUse`.
There is no inbound helper and no `guard_can_use_tool`.

Three surfaces, one decision rule:

- **An authored `@tool`** → `guard_tool`. Denial is JSON-in-content +
  `is_error: True`. Python does **not** forward `structuredContent`
  (that is the JS adapter). Do **not** raise.
- **Inbound text** → `guard_hooks` `UserPromptSubmit` (`decision:
  "block"`). That is the only place a turn can be declined before the
  model reads the prompt.
- **Built-ins / unwrapped MCP** → `guard_hooks` `PreToolUse`
  (`permissionDecision: "deny"`). `PostToolUse` is capture only.
- **Correlation** → `claude_agent_context` reads a caller-owned UUID
  `session_id`. It never mints.

Docs: https://docs.arcjet.com/guards/claude-agent-sdk/.

## Unwrapped tools deny on `PreToolUse` via `guard_hooks`

Built-ins (Bash, Write, …) and MCP tools you did not pass through
`guard_tool` have no authored handler. `PreToolUse` is the only deny for
those. `PostToolUse` cannot undo a tool that already ran. List every
`guard_tool` wrapper in `exclude` or each authored tool is guarded twice
(two round trips, two quota units). Entries match the reported name:
pass `{"server": "support", "name": "lookup_order"}` for an authored MCP
tool (it resolves to `mcp__support__lookup_order`) and a bare string for
a built-in such as `"Bash"`. A bare authored name deliberately does not
match every server's tool of that name.

## Authored `@tool` denial is JSON-in-content + `is_error: True`

`guard_tool` wraps the `@tool` definition so the handler never runs on
`DENY` (or unevaluated Guard under the default `on_guard_error="deny"`).
The model receives the `ArcjetDenialResult` as JSON text on `content`
with `is_error: True`. Do **not** set `structuredContent` (JS only). Do
**not** raise: a throw is a raw exception; omitting `is_error` looks
like success. Same fail-closed default as
[#196](https://github.com/arcjet/arcjet-py/pull/196): only `"allow"`
fails open; a `DENY` always blocks. Core `guard()` still fails open.

## `can_use_tool` is not a policy gate

`can_use_tool` is human-in-the-loop. `allowed_tools`, allow rules, and
`bypassPermissions` / `acceptEdits` skip it. Same trap as CrewAI
`human_input`, JS `canUseTool`, LangGraph `interrupt()`, and OpenAI
Agents `needs_approval`. There is no inbound helper — screen prompt
injection on `guard_hooks` `UserPromptSubmit`.

## Questions to ask the human first

Ask only what you cannot infer from the code; suggest defaults.

1. Which tools are **risky** (external side effects, irreversible, spends
   money, sends messages)? Those get `guard_tool`. Built-ins and
   unwrapped MCP get `guard_hooks` `PreToolUse`.
2. What **limits**? (e.g. "10 lookups/min per user" → `TokenBucket`.)
3. Who is the **user** for metadata — an opaque user/tenant ID (never PII)?
   Default: none. Session id is the correlation id, not the user. The
   Claude SDK requires `session_id` to be a UUID and allows a given id
   to be created only once — later turns use `resume`.
4. Is an Arcjet outage unacceptable? Every helper defaults to
   `on_guard_error="deny"`. Ask explicitly about inbound
   `UserPromptSubmit`: failing closed there means the agent stops
   answering, so `"allow"` is a routine and legitimate choice at that
   one call site.

## The things readers get wrong

1. **This is not the JS adapter and not Claude Managed Agents.** Do not
   import `@arcjet/guard/claude-agent-sdk/v0` or
   `arcjet.guard.claude_managed_agents`.
2. **There is no inbound helper.** Screen on `UserPromptSubmit` via
   `guard_hooks`.
3. **`can_use_tool` is HITL, not policy.**
4. **Python does not forward `structuredContent`.** Authored deny is
   JSON-in-content + `is_error: True`.
5. **`session_id` is a UUID, and only once.** Later turns: `resume`.
   `claude_agent_context` never mints.
6. **List every `guard_tool` wrapper in `exclude`.** Missing exclude
   double-calls Guard.
7. **Key rate limits on the authenticated caller**, not a model-supplied
   order id. Hand `query` / `create_sdk_mcp_server` the copy
   `guard_tool` returns.
8. **Do not hand-wrap every tool with raw `guard()`.**
9. **Isolation needs both `setting_sources=[]` and
   `strict_mcp_config=True`.** One without the other still exposes an
   unguarded path.
10. **Two distinct ids.** `ClaudeAgentOptions.session_id` is a unique
    UUID per run (`resume` later). The Guard `session_id` is a
    long-lived actor id. A missing decision is not a denial.

## Step 1: Install and find the guard client

Until-published: PyPI `arcjet` 1.0.0 does not include this module. Pin
`arcjet` to git SHA `582372916d70311873ef24b7a72443c098b3aec9` (current
`main`, includes the extra):

```bash
pip install "arcjet[claude-agent-sdk] @ git+https://github.com/arcjet/arcjet-py.git@582372916d70311873ef24b7a72443c098b3aec9"
```

If the agent has no guard client yet, launch one **once at module scope**:

```python
import os
from arcjet.guard import launch_arcjet

aj = launch_arcjet(key=os.environ["ARCJET_KEY"])
```

## Step 2: Gate authored tools — `guard_tool`

```python
from claude_agent_sdk import ClaudeAgentOptions, create_sdk_mcp_server, query, tool
from arcjet.guard import DetectPromptInjection, TokenBucket, launch_arcjet
from arcjet.guard.claude_agent_sdk import guard_hooks, guard_tool

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
# Caller-owned UUID for this conversation. Later turns: resume=session_id.
session_id = conversation_id

@tool("lookup_order", "Look up an order by number", {"order_id": str})
async def lookup_order(args: dict) -> dict:
    return {
        "content": [{"type": "text", "text": f"{args['order_id']}: shipped"}],
    }

lookup_order = guard_tool(
    guard=aj,
    tool=lookup_order,
    action="order.looked-up",
    rules=[lookup_limit(key=user_id, requested=1)],
    on_guard_error="deny",
)
# can_use_tool=... is HITL — not this policy gate
```

## Step 3: Screen inbound and gate unwrapped tools — `guard_hooks`

```python
async for message in query(
    prompt=user_text,
    options=ClaudeAgentOptions(
        session_id=session_id,  # later turns: resume=session_id instead
        mcp_servers={
            "support": create_sdk_mcp_server(name="support", tools=[lookup_order]),
        },
        hooks=guard_hooks(
            guard=aj,
            session_id=session_id,
            exclude=[{"server": "support", "name": "lookup_order"}],
            inbound={
                "action": "message.received",
                "rules": lambda ctx: [inbound(ctx["prompt"])],
            },
            action="mcp.invoked",
            rules=lambda ctx: [mcp_limit(key=user_id, requested=1)],
            on_guard_error="deny",
        ),
    ),
):
    pass
```

## Step 4: Correlation

`claude_agent_context(session_id=session_id)` reads that same
caller-owned UUID (hook `session_id` first, then `options.session_id`).
It never mints. Pass the id you already have into `guard_hooks` and
`ClaudeAgentOptions` — do not derive a new one per turn. The Claude SDK
also requires `session_id` to be a UUID and allows a given id to be
created only once — later turns use `resume`.

## Verify the integration

1. `python -m py_compile` (or the project's type-check) passes.
2. Exercise inbound PI (`UserPromptSubmit` block), an authored-tool deny
   (JSON-in-content + `is_error: True`, no `structuredContent`), a
   built-in / unwrapped MCP deny (`PreToolUse`), a rate limit, and
   fail-closed (an unreachable guard). Confirm a wrapped tool produces
   **one** guard decision per invocation — a second decision under the
   `PreToolUse` action means a missing `exclude` entry.
3. Confirm in the Arcjet Console / CLI that decisions share the
   caller-owned UUID `session_id`.
4. Manual E2E with a real `ARCJET_KEY` is still-to-verify until you run it.

The example `fastapi-claude-agent-sdk-guard` stays with Runtime — do not
invent a new example name. Do not add an example in this skills repo.
