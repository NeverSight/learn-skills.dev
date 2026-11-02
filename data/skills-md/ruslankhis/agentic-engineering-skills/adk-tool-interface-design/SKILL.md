---
name: adk-tool-interface-design
license: MIT
description: Design, diagnose or review the model-facing interface of Python Google ADK tools and tool-like sub-agents, including FunctionTool docstrings and parameter schemas, naming and namespacing, consolidation versus splitting, tool-count budgets and dynamic toolsets, result shaping and size, actionable error returns, and the choice between AgentTool, sub_agents and single_turn mode. Use when the model picks the wrong tool or arguments, tool results bloat context, or a new tool or toolset needs a schema. Do not activate for retries, deadlines or idempotency of the external call (safe-api-tool-calls), credentials and identity (adk-tool-auth-and-secrets), budgets and approval policy (adk-operational-guardrails), measurement over a case set (adk-agent-evaluation), agent instruction text (adk-agent-instructions) or output schemas (adk-model-and-output-contracts).
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-framework"
  verified-against: "google-adk 2.8.0 source and adk-python main CHANGELOG, 2026-10-06"
  version: "2026.10.28"
---

# ADK tool interface design

Deliver a small, verified change to what the model sees of a tool (name,
description, parameters, result) or of a delegated agent (name, description,
request parameters, return path), or an actionable review of those interfaces.
Work inside the target's existing tools, agents, pins and tests. The model
cannot see Python; it sees one declaration per tool and one result dict per
call. Every recommendation here pairs with an observable check.

## Inspect before choosing a mode

1. Read the tool functions, toolsets, agent definitions (`tools=`,
   `sub_agents=`, `mode=`, `description=`), the instruction text that mentions
   tools, callbacks that touch tool arguments or results, and the existing tool
   tests. Note which tools read, which write, and which are server-supplied
   (MCP, OpenAPI).
2. Identify the pinned `google-adk` and `google-genai` versions from the
   manifests and lockfile. Read [compatibility](references/compatibility.md):
   on 2.8.0 the docstring is the entire description and **no per-parameter
   description reaches the model** (`Annotated` metadata is preserved from
   2.10.0), so parameter names and the docstring body carry the semantics.
   Preserve the pin; propose an upgrade as a decision, not a side effect.
3. Run the read-only linter from this skill's directory with an available
   Python 3.11+ interpreter ([interpreters](references/operating-rules.md#helper-scripts-and-interpreters)):

   ```bash
   python "$SKILL_DIR/scripts/lint_tool_schemas.py" --project . --max-tools 20
   ```

   It parses source with `ast`, never imports the project, and prints
   identifiers, counts and `file:line` only. Findings are review prompts
   (missing or one-line docstrings, untyped or generic parameters, mutually
   exclusive booleans, non-dict or status-less returns, raise without an error
   dict, blocking I/O in a sync tool, near-duplicate names or descriptions,
   tool counts, short sub-agent descriptions, identity parameters). A
   `partial: true` result means an area was not scanned.
4. If recorded events exist (an `adk web` session export or test capture),
   measure result cost:

   ```bash
   python "$SKILL_DIR/scripts/report_tool_result_sizes.py" --events events.json
   ```

5. Record the current declaration text and size for each tool you will touch
   ([validation](references/validation.md), step 2). This is the "before".

Ask only for decisions the source cannot settle: which tools must stay
separate for policy reasons, what result size the application tolerates, and
whether a sub-agent needs user interaction.

## Choose the relevant path

| Mode | Decision and reference |
| --- | --- |
| (a) New tool or toolset design | Read the [FunctionTool contract](references/function-tool-contract.md) for what the pinned version declares, then [naming and consolidation](references/naming-and-consolidation.md) for the docstring template, parameter rules and when to merge or split. For more than about 20 tools, or any MCP/OpenAPI toolset, also read [tool count and toolsets](references/tool-count-and-toolsets.md). |
| (b) Wrong tool or wrong parameter diagnosis | Dump the live declarations and compare against the prompt that failed. Fix the description or name before touching the instruction ([naming and consolidation](references/naming-and-consolidation.md)); check the error dicts the model saw before the mistake ([results and errors](references/results-and-errors.md)); check the active tool count ([tool count](references/tool-count-and-toolsets.md)). Hand the accuracy measurement to `adk-agent-evaluation`. |
| (c) Result and context-cost review | Read [results and errors](references/results-and-errors.md): status taxonomy, fields for the next step, pagination and truncation defaults, durable store plus opaque reference, actionable error dicts, treatment of server-supplied text. Measure with the result-size report before and after. |
| (d) Delegation interface review | Read [delegation interfaces](references/delegation-interfaces.md) to choose between `chat` sub-agents, `task`, `single_turn` and `AgentTool`, set `skip_summarization`, and write the sub-agent description the parent model will read verbatim. `adk-workflow-design` owns the control flow; `adk-agent-instructions` owns the wording. |
| (e) Review or recommendation | Use the references above; report each finding with its `file:line`, the declaration or result it affects, the observable check that would show the fix, and the evidence label (vendor guidance, documented behaviour, independent evidence, source-verified). Change nothing unless asked. |

A request may need several rows; keep them in one change set and one report.

When the project has `agents-cli-manifest.yaml`, consult the installed
`google-agents-cli-adk-code` skill (`references/adk-python.md`, "Tools", or
the `long-horizon-harness` recipe for a guard chain and result pruning); if it
is not installed, adk-engineer explains how to get it. Its tool rules are the
scaffold's conventions; the declaration dump on the pinned version decides
what the model sees.

## Implement the smallest coherent change

State the affected tools, agents and tests before editing. Then:

- Write the docstring as the whole interface: what it does and returns, when
  to use it and when not (name the alternative), one line per parameter with
  format and example, and the return structure with its `status` values and
  example dicts. Do not mention the injected `ToolContext` parameter; the model
  never sees it and the ADK docs say it can confuse the model.
- Name tools `verb_noun`, prefix by service when several services are present,
  and keep names unique per agent; ADK shadows duplicates with a warning.
- Prefer few parameters of primitive type (`str`, `int`, `float`, `bool`,
  `list[str]`, `dict[str, Any]`, `Optional[T]`, an `Enum`). Avoid bare `list`
  or `dict`, unions of several types and nested models; check PEP 604 unions
  and `anyOf` against the pinned builder and API variant. Give defaults only to
  tuning knobs (page size, format), never to values the user supplies.
- Never ask the model for identity, tenant, secrets or the current date; read
  them from `ToolContext` or configuration (`adk-tool-auth-and-secrets`).
- Return a dict with `status` and, on failure, `error_message` (or `error`) and
  a `hint` saying what to do next; never raise for expected failures and never
  return a bare string. Bound list sizes with a default and a ceiling; move
  large payloads to a durable store and return a reference.
- Use `async def` for I/O tools so ADK can run independent calls
  concurrently, and make tools that may be selected together side-effect-safe
  in any order.
- Place guardrails where they belong: argument validation that returns an
  error dict in `before_tool_callback` (return `None`, not `{}`, to let the
  tool run), output trimming or artifact offload in `after_tool_callback`,
  policy that depends on `ToolContext.state` inside the tool. Budgets and
  approval policy stay with `adk-operational-guardrails`.
- For delegation, prefer `mode='single_turn'` sub-agents over direct
  `AgentTool` unless you need the isolated session, and write the description
  as a tool docstring. Wrap built-in tools (Google Search, code execution) in
  an `AgentTool` or set `bypass_multi_tools_limit` when other tools are
  present; see [delegation interfaces](references/delegation-interfaces.md).

Do not edit `generate_content_config.tools`; ADK rejects it. Forcing
selection (`function_calling_config` modes, `allowed_function_names`) is a
request setting, not prompt text; verify the enum in the pinned `google-genai`.

## Permissions and consequential operations

<!-- shared:consequential-operations-brief -->
Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
<!-- /shared:consequential-operations-brief -->

Linting is read-only. Changing a docstring or schema changes what the model
may do next; a tool that becomes easier to select is called more often. Before
enabling live tests, show the exact model, project, case count and cost
ceiling; keep paid runs with `adk-agent-evaluation`. Never widen an MCP allow-list to make a test pass, and
never derive write or confirmation policy from server-supplied annotations.

## Validate and finish

Read [validation](references/validation.md). Produce, for each changed tool or
sub-agent: the linter diff, the live declaration dump with its byte size, a
scripted-model Runner test asserting the tool ran with the designed arguments
and returned the designed shape (including one error branch with its hint),
the result-size report on recorded events, and the per-agent tool count. Then
hand the case set and budgets to `adk-agent-evaluation` as described in
[evaluation hooks](references/evaluation-hooks.md); selection and parameter
accuracy on a real model are its results, not this skill's.

Report files changed, commands and actual output. A fact read in the
installed package is `offline (source read)` and a scripted-model run
`local (mocked)`; every threshold taken from a vendor is `vendor-measured`. On
a second invocation, reread the existing declarations and tests before adding
another wrapper, toolset or test double.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

Independent community project; not affiliated with or endorsed by Google.
