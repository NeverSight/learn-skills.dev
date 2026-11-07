---
name: adk-model-and-output-contracts
description: >-
  Design, harden or review what a Python Google ADK agent asks the model to
  emit and which model and settings produce it: output_schema contracts and
  their validation, repair loops, output_schema together with tools, Gemini
  model selection and lifecycle, thinking and sampling settings,
  and model failover. Use for structured output that arrives as prose, fenced
  JSON or invalid data, response-schema design, choosing or escalating a
  Gemini model, retrying the model's own 429 or quota errors, or
  FallbackModel decisions. Do not activate for measuring
  quality on a labelled set (adk-agent-evaluation), SQL wire schemas
  (adk-sql-agent-engineering), prompt wording (adk-agent-instructions), tool
  parameter schemas (adk-tool-interface-design), hosting-level latency
  (optimise-adk-on-google-cloud), budget and degradation policy
  (adk-operational-guardrails), tool API retries (safe-api-tool-calls) or a
  release's model migration (adk-release-engineering).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-framework"
  verified-against: "google-adk 2.8.0 source and adk-python main CHANGELOG, 2026-10-06"
  version: "2026.10.28"
---

# ADK model and output contracts

Decide what the model is asked to emit, which model and settings produce it, and how code proves it. Deliver the smallest change to an existing agent or a review with observable findings. Keep the model deciding and code copying identifiers; keep the schema minimal; keep thinking on; keep every claim tied to the pinned ADK version.

## Inspect before choosing a mode

1. Record the pinned `google-adk` and `google-genai` versions from the manifest and lockfile. Most behaviour below is for **2.8.0**; [compatibility](references/compatibility.md) lists what changed in 2.6 to 2.11. Keep pins unchanged unless a version decision is requested.
2. Find every model reference: string literals, `model=` arguments, `Gemini(...)`, `LiteLlm(...)`, `FallbackModel(...)`, `-latest` aliases and the agent default (`LlmAgent.DEFAULT_MODEL` is `gemini-3.5-flash` in 2.8.0).
3. Find `generate_content_config`, `planner`, `output_schema`, `output_key`, `mode` and `tools` on each `LlmAgent`. Note which agents combine `output_schema` with `tools`.
4. Identify the backend: `GOOGLE_GENAI_USE_ENTERPRISE` (the deprecated spelling `GOOGLE_GENAI_USE_VERTEXAI` still works with a `DeprecationWarning` in 2.8.0), project and location, or an API key. The backend decides how a schema is enforced ([output schema and tools](references/output-schema-and-tools.md)). In an Agents CLI project (`agents-cli-manifest.yaml` present) the scaffold writes `GOOGLE_GENAI_USE_ENTERPRISE=true` and `gemini-3.8-flash`; consult the installed `google-agents-cli-adk-code` skill (`references/adk-python.md`) for those conventions; if it is not installed, adk-engineer explains how to get it.
5. Run the two helpers with an available Python 3.11+ interpreter ([interpreters](references/operating-rules.md#helper-scripts-and-interpreters)) after resolving `SKILL_DIR` to this skill's directory. They read source only; they never import the project or call a provider.

```bash
python "$SKILL_DIR/scripts/audit_model_config.py" --project .
python -c 'from app.schemas import Decision; import json; print(json.dumps(Decision.model_json_schema()))' > .adk-evidence/decision.json
python "$SKILL_DIR/scripts/check_response_schema.py" --schema .adk-evidence/decision.json --pydantic-json
```

The audit reports model strings with a lifecycle status from a dated table (`assets/model-lifecycle-2026-10-01.json`, refresh it before trusting it), rejected `generate_content_config` fields, thinking and temperature mismatches, planner precedence and schema-with-tools combinations. The schema checker reports keywords outside the Gemini documented subset, depth, property and enum counts, nullable styles and unresolved `$ref`s. Both direct inspection; neither certifies provider acceptance. Exit 1 from the audit means a partial scan; exit 1 from the checker means unsupported keywords.

## Choose the relevant mode

| Mode | Read | Produce |
| --- | --- | --- |
| (a) Design an output contract | [output contracts](references/output-contracts.md) | A minimal schema in the documented subset with a nullable refusal path; the model decides, code copies identifiers |
| (b) Harden an existing contract (fences, prose instead of JSON, nulls, validation failures) | [validation and repair](references/validation-and-repair.md), then [output schema and tools](references/output-schema-and-tools.md) when tools are present | The 2.8.0 save path understood, a bounded repair loop with an explicit failure outcome, finish reasons handled |
| (c) Choose or escalate a model | [model selection](references/model-selection.md) | Current model IDs with dates, a measured comparison handed to adk-agent-evaluation's two-stage escalation |
| (d) Configure thinking and sampling | [reasoning and sampling](references/reasoning-and-sampling.md) | `thinking_level` on Gemini 3, temperature left at 1.0, one place for thinking config, output limit covering thought tokens |
| (e) Add failover | [failover and providers](references/failover-and-providers.md) | `FallbackModel` from 2.9.0 or an application-level alternative on 2.8.0, global endpoint decision, LiteLLM caveats |
| (f) Review | All of the above as needed, plus [validation](references/validation.md) | Findings with file and line, each tied to a source-verified behaviour, with the test that would prove the fix |

Modes compose. A model escalation that changes thinking defaults is (c) plus (d); a schema that stops validating after a model change is (b) plus (c).

## Implement the contract

- Put the schema on `LlmAgent.output_schema` and the key on `output_key`. `generate_content_config` rejects `tools`, `system_instruction` and `response_schema` with a `ValueError` in 2.8.0, and a base URL in `http_options`. Keep thinking in one place: a `BuiltInPlanner.thinking_config` overwrites `generate_content_config.thinking_config` and ADK warns at construction.
- Keep the schema small enough to describe in one sentence per field. Ask for a decision, a short reason and identifiers the model saw; copy everything else from trusted data in code. Give refusal a first-class shape (a status enum plus nullable payload fields) so a valid "no" survives `exclude_none=True`.
- With tools present, decide on which backend the agent runs. On Vertex (enterprise mode) with a Gemini model, 2.8.0 sets the native response schema alongside tools; on the API-key backend it adds a `set_model_response` tool and an instruction, which is best-effort. A formatting sub-agent without tools is the dependable alternative.
- Treat a validation failure as a product outcome. In 2.8.0, `validate_schema` strips a whole-payload code fence, then raises on invalid JSON or a Pydantic error; the exception leaves the agent run. Catch it at a boundary you own, retry within an attempt budget with the error as feedback, then emit the explicit failure shape. Record which attempt succeeded.
- On Gemini 3 use `thinking_level`, leave temperature at its default of 1.0, and size `max_output_tokens` for thinking plus output. Prefer minimal or low thinking for classification and lookup; keep thinking on for decisions. Reasoning happens before the constrained answer, in the same call or a prior one.
- Choose models by measured quality on the project's development set, then cost, then lifecycle. A cheaper model is a hypothesis until the four metrics in [validation](references/validation.md) say otherwise.

## Validate and finish

Read [validation](references/validation.md). Three checks are observable without a live model:

1. A scripted-model test in which the model returns invalid JSON, fenced JSON and schema-valid wrong data; it proves the attempt budget, the explicit failure outcome and that wrong-valid-schema is counted separately from invalid output.
2. A request-capture test (a `before_model_callback` or a transport double) showing which config field carried the schema (`response_schema` plus `response_mime_type` in 2.8.0) and whether the tools list contains `set_model_response`, so the native or workaround path is known rather than assumed.
3. A development-set comparison through adk-agent-evaluation reporting schema validity, answer accuracy, executable or actionable accuracy and wrong-valid-schema separately, with finish reason and thought tokens recorded per run.

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

Live model calls, model switches in production and new quota or endpoint settings are among them: present model, backend, project, location, request count and cost ceiling. Keep configuration examples synthetic.

Report what was inspected, what the helpers found, which tests ran and what remains unverified. A scripted-model test is `local (mocked)`. Record every URL with its page date; model availability and defaults change faster than this skill.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

Independent community project; not affiliated with or endorsed by Google.
