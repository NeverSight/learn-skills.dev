---
name: integrate-arcjet-guard-crewai
description: Integrate Arcjet Guard into official CrewAI — register process-wide PRE_TOOL_CALL with register_arcjet_hooks, or wrap a standalone BaseTool you call yourself with guard_tool. Use when asked to add Arcjet to CrewAI, LiteAgent, crew-injected tools, rate limit those tools, screen inbound messages before kickoff, or block prompt injection / PII. Official crewai only; not an npm CrewAI port and not LangChain Crew wrappers.
license: Apache-2.0
compatibility: Requires Python >= 3.10, official crewai>=1.15.3,<2 installed by the user, PyPI arcjet 1.0.0, and a blocking Guard client (launch_arcjet_sync). There is no arcjet[crewai] extra.
metadata:
  author: arcjet
  type: core
  library: arcjet
---

# Integrate Arcjet Guard into CrewAI

`arcjet.guard.crewai` wraps the agent's existing Arcjet client. It never
talks to the Arcjet API itself. Shared Guard fundamentals (client, rules,
labels, decisions, capture, registration) live in
[../arcjet/references/guards_python.md](../arcjet/references/guards_python.md).
Load that reference for anything that is not CrewAI-specific.

Official `crewai` only — not community forks, not LangChain Crew wrappers,
not an npm CrewAI port. There is **no** `arcjet[crewai]` extra: CrewAI
hard-depends on `chromadb`, which carries unpatched RCE CVE-2026-45829,
so an Arcjet extra must not pull it in. Install CrewAI yourself. Importing
`arcjet.guard.crewai` does not load LangChain.

Exports: `register_arcjet_hooks`, `unregister_arcjet_hooks`,
`ArcjetCrewAIHooks`, `guard_tool`, `ToolPolicy`, `sanitize_tool_name`,
`free_text_arguments`. There is no `guard_crew`.

Two surfaces, one decision rule:

- **A tool a crew, LiteAgent, MCP adapter, or crew-injected list executes**
  → `register_arcjet_hooks` + `ToolPolicy`. Gate is process-wide
  `PRE_TOOL_CALL` only. DENY raises `HookAborted(reason=..., source="arcjet")`.
- **A CrewAI `BaseTool` you call yourself** → `guard_tool`. This is the
  **only** CrewAI path that raises `ArcjetDeniedError` /
  `ArcjetUnavailableError`. `BaseTool.run` never dispatches
  `PRE_TOOL_CALL`.

Docs: https://docs.arcjet.com/guards/crewai/.

## The gate is process-wide `PRE_TOOL_CALL`, once

`register_arcjet_hooks` registers on CrewAI's dispatcher. A `DENY` (or
unevaluated Guard under the default `on_guard_error="deny"`) raises
`HookAborted(reason=..., source="arcjet")` so the tool never runs. CrewAI
swallows every other exception — raising `ArcjetDeniedError` /
`ArcjetUnavailableError` from the hook would *run* the tool. The hook
path is **sync only** — pass `launch_arcjet_sync` / `ArcjetGuardSync`. An
async client is refused at registration (`ArcjetMisconfiguration`). A
second `register_arcjet_hooks` in the same process is also
`ArcjetMisconfiguration` (CrewAI's registry appends and would
double-evaluate); call `unregister()` on the handle first.

## `POST_TOOL_CALL` is never registered

Only PRE is installed. The decision is captured in PRE. POST is not a
policy surface. The agent always sees
`Tool execution blocked by hook. Tool: {name}`. `HookAborted.reason` is
telemetry only. A proceed still records `success` — do not read CrewAI
hook capture as the five-value `metadata.outcome` table used by
`guard_action` / LangChain helpers.

## `human_input` is not a policy gate

Agent/Task `human_input` and `request_human_input` are human-in-the-loop.
Same trap as JS `humanInTheLoopMiddleware`, LangGraph `interrupt()`,
OpenAI Agents `needsApproval`, and Genkit `interrupt()`. There is no
inbound helper and no approval helper.

## Questions to ask the human first

Ask only what you cannot infer from the code; suggest defaults.

1. Which tools are **risky** (external side effects, irreversible, spends
   money, sends messages)? Crew-executed tools get
   `register_arcjet_hooks`. A standalone `BaseTool` you invoke yourself
   gets `guard_tool`.
2. What **limits**? (e.g. "10 lookups/min per user" → `TokenBucket`.)
3. Who is the **user** for metadata — an opaque user/tenant ID (never PII)?
   Default: none. Crew, task, and agent names are metadata, never minted
   into a correlation id. Use a caller-owned `correlation_id` /
   `arcjet_sequence`.
4. Is an Arcjet outage unacceptable? Every helper defaults to
   `on_guard_error="deny"`. Ask explicitly about inbound screening before
   `crew.kickoff`: failing closed there means the crew does not run, so
   `"allow"` is a routine and legitimate choice at that one call site.

## The things readers get wrong

1. **There is no `arcjet[crewai]` extra.** Install `crewai>=1.15.3,<2`
   yourself. `arcjet.guard.crewai` ships in PyPI `arcjet` 1.0.0.
2. **There is no `guard_crew`.** Use `register_arcjet_hooks`.
3. **The hook path is sync only.** Pass `launch_arcjet_sync`.
4. **Raise `HookAborted` from the hook, not Arcjet errors.** CrewAI
   swallows anything else and the tool runs.
5. **`human_input` is HITL, not policy.**
6. **Screen inbound with core `guard` / `guard_sync` before
   `crew.kickoff`.** Core `guard()` fails open.
7. **Key rate limits on the authenticated caller**, not a model-supplied
   order id. `sanitize_tool_name` matches `Send Email` and `send_email`.
8. **Do not hand-wrap every CrewAI tool with raw `guard()`.**
9. **`inputs=` is accepted.** The hook resolver is `(arguments, ctx)`.
   A missing decision is not a denial — verify in Console/CLI.

## Step 1: Install and find the guard client

```bash
pip install arcjet
pip install "crewai>=1.15.3,<2"
```

Launch a **sync** client at module scope for the hook path:

```python
import os
from arcjet.guard import launch_arcjet_sync

aj = launch_arcjet_sync(key=os.environ["ARCJET_KEY"])
```

Use `launch_arcjet` only from async application code, or from
`guard_tool` when you call `arun()`.

## Step 2: Gate crew-executed tools — `register_arcjet_hooks`

`ToolPolicy` is `action` + `rules`, keyed by tool name. Keys and the
optional `tools=` filter go through `sanitize_tool_name` (CrewAI
1.15.3+). Tools without a matching policy still get
`"{sanitized_tool_name}.invoked"` and the registrar-level `rules` (empty
still contacts Guard) unless you pass `tools=`. `free_text_arguments`
strips opaque ids (`tool_call_id`, `*_id`, …) when you want only free
text for a scanning rule — the hook itself hands resolvers the tool's
own argument mapping unfiltered. Already-`guard_tool`-wrapped tools are
skipped so Guard is not called twice. Tear down with
`unregister_arcjet_hooks(hooks)` or `hooks.unregister()`.

```python
from crewai import Agent, Crew, Task
from arcjet.guard import DetectPromptInjection, TokenBucket, launch_arcjet_sync
from arcjet.guard.crewai import ToolPolicy, register_arcjet_hooks, unregister_arcjet_hooks

aj = launch_arcjet_sync(key=os.environ["ARCJET_KEY"])
lookup_limit = TokenBucket(
    label="order.looked-up",
    bucket="lookups",
    refill_rate=10,
    interval_seconds=60,
    max_tokens=10,
)
inbound = DetectPromptInjection()
user_id = authenticated_user_id

hooks = register_arcjet_hooks(
    guard=aj,
    policies={
        "lookup_order": ToolPolicy(
            action="order.looked-up",
            rules=[lookup_limit(key=user_id, requested=1)],
        ),
    },
    tools=["lookup_order"],
    on_guard_error="deny",
)

agent = Agent(
    role="Support",
    goal="Look up orders",
    backstory="Help the user with order status.",
    # human_input=True is HITL — not this policy gate
)
task = Task(
    description="Look up the user's order",
    expected_output="Order status",
    agent=agent,
)
crew = Crew(agents=[agent], tasks=[task])

decision = aj.guard(
    label="message.received",
    rules=[inbound(user_text)],
)
if decision.conclusion == "DENY":
    raise RuntimeError("message blocked")
if decision.has_failed_open():
    raise RuntimeError("inbound guard unavailable")

crew.kickoff()
unregister_arcjet_hooks(hooks)
```

## Step 3: Gate a `BaseTool` you call — `guard_tool`

Hand the crew the copy this returns (it carries the brand the hook
skips). The original stays unguarded on purpose — if you pass that to a
crew, the hook still covers it. A sync call needs a blocking client; an
async call needs an awaitable one.

```python
from arcjet.guard.crewai import guard_tool

guarded = guard_tool(
    guard=aj,
    tool=lookup_order,
    action="order.looked-up",
    rules=[lookup_limit(key=user_id, requested=1)],
    on_guard_error="deny",
)
result = guarded.run(order_id=order_id)
```

## Step 4: Correlation

Use a caller-owned `correlation_id` / `arcjet_sequence`. Crew, task, and
agent names are metadata, never minted into an id. If nothing valid
remains, the call is uncorrelated rather than joined to a generated id.

## Verify the integration

1. `python -m py_compile` (or the project's type-check) passes.
2. Exercise inbound PI (before `kickoff`), a `PRE_TOOL_CALL` deny
   (`HookAborted`, agent sees `Tool execution blocked by hook. Tool:
   {name}`), a standalone `guard_tool` deny (`ArcjetDeniedError`), a
   rate limit, and fail-closed (an unreachable guard). Confirm
   `POST_TOOL_CALL` is not registered and `human_input` is never treated
   as the gate.
3. Confirm in the Arcjet Console / CLI that decisions share the
   caller-owned correlation id — not a crew/task/agent name.
4. Manual E2E with a real `ARCJET_KEY` is still-to-verify until you run it.

Do not invent a CrewAI example name in this skills repo.
