---
name: dify-workflow-dsl
description: >
  Create, modify, review, migrate, and debug import-ready Dify App DSL YAML for
  DSL 0.6.0 and 0.7.0. Use for Workflow, Chatflow, Agent App, Agent v2 workflow
  nodes, Human Input, graph wiring, variables, plugin dependencies, tools,
  database operations, and import/export compatibility.
---

# Dify Workflow DSL

Produce import-ready Dify App DSL YAML. Treat official Dify source as schema
authority and exported files from the target workspace as authority for dynamic
plugin/tool fields.

## Core Workflow

1. Identify the target Dify/DSL version before authoring. For a new file, default
   to DSL `0.7.0` (Dify 1.16.x). Use `0.6.0` for Dify 1.15.x compatibility.
   Preserve an existing supported version unless the user asks to migrate it.
   Always quote `version`.
2. Choose the app mode:
   - `workflow` for one-shot, batch, triggered, integration, and structured-output
     automations.
   - `advanced-chat` for multi-turn chat, memory, `sys.query`, `sys.files`, and
     `answer` nodes.
   - `agent` only for a top-level portable Agent App in DSL `0.7.0`.
3. Clarify only import-blocking facts: inputs, outputs, model/provider, installed
   plugins, knowledge bases, secrets, trigger source, or required Agent package.
4. Sketch the graph or Agent package before writing YAML. A graph needs an entry,
   connected processing nodes, and a reachable `end`/`answer` unless a triggered
   side-effect workflow intentionally returns nothing.
5. Add a top-level dependency for every referenced marketplace/package/GitHub
   plugin. Preserve exact exported identifiers.
6. Write stable string IDs and connect edges with existing endpoints, matching
   `sourceType`/`targetType`, and valid branch `sourceHandle` values.
7. Run `python3 scripts/validate_dsl.py --strict --target-version <version> <file.yml>`.
   Fix all errors and warnings unless a warning is an intentional, documented
   behavior risk.
8. When a matching Dify source environment is available, run
   `scripts/validate_with_dify_source.py` before claiming source compatibility.
   This uses Dify's own node and Agent models; it does not replace a real
   workspace import and execution test.

## Version Policy

| Target | Use | Key capabilities |
| --- | --- | --- |
| Dify 1.15.x / compatibility | `"0.6.0"` | Workflow, Chatflow, legacy model-config apps and legacy Agent nodes |
| Dify 1.16.x / new generation | `"0.7.0"` | Everything above plus top-level Agent App packages and portable Agent v2 workflow nodes |

Do not upgrade by changing only the version string. A 0.7.0 Agent App or Agent v2
node needs the package structures described below. When the target workspace is
unknown and import compatibility matters, state the 1.16.x assumption.

## DSL 0.7.0 Rules

- Top-level Agent App shape:

  ```yaml
  version: "0.7.0"
  kind: app
  app: {name: "Agent", mode: agent}
  agent: {package_ref: agent_1}
  agent_packages:
    agent_1:
      schema_version: 1
      metadata: {name: "Agent", description: "", role: ""}
      soul: {schema_version: 1}
      omitted_assets: []
  dependencies: []
  ```

- Portable Agent v2 workflow nodes use `data.type: agent`, `version: "2"`,
  `agent_node_kind: dify_agent`, `agent_binding.package_ref`, and `agent_job`.
  Their referenced package must exist in top-level `agent_packages`.
- If `agent_job.declared_outputs` is empty, runtime outputs are `text`, `files`,
  and `json`; otherwise use the declared output names.
- Agent exports deliberately omit or sanitize credentials, uploaded files,
  skills, and workspace bindings. Tell the user to review import warnings and
  reconnect missing assets in the target workspace.
- Human Input uses `delivery_methods`, `form_content`, `inputs`, `user_actions`,
  `timeout`, and `timeout_unit`. Each outgoing edge uses a `user_actions[].id` as
  `sourceHandle` (or `__timeout` for timeout); input names and the special
  `__action_id`, `__action_value`, and `__rendered_content` fields are outputs.
- LLM nodes require `model`, `prompt_template`, and `context`. Even when context
  retrieval is disabled, include `context: {enabled: false,
  variable_selector: []}` because Dify's node model requires the object.

## Scalable Generation

For a large workflow, separate probabilistic generation from deterministic
assembly:

1. Build a compact plan/IR listing node IDs, types, inputs, outputs, branches,
   package refs, and dependencies.
2. Generate independent leaf-node payloads from that plan. Do not let separate
   builders invent conflicting IDs or edges.
3. Assemble nodes and edges centrally; normalize IDs, handles, layout, package
   refs, selectors, and dependencies.
4. Validate structure, reachability, cycles, references, branch handles, package
   refs, and plugin coverage. Regenerate only the failing component.

This mirrors Dify 1.16's workflow-generator direction: planning and node building
can be model-assisted, while post-processing and structural validation remain
deterministic.

## Reference Map

Load only what is needed:

- `references/official-0.7-target.md`: current 0.7.0 source-backed rules, Agent
  packages, Agent v2, Human Input, import/export behavior, and generation scale.
- `references/official-0.6-target.md`: 0.6.0 compatibility baseline.
- `references/dsl-structure.md`: top-level YAML, variables, graph wrappers,
  dependencies, selectors, and edges.
- `references/node-schemas.md`: node payload schemas and examples.
- `references/database-tools.md`: PostgreSQL/SQL read-write patterns.
- `references/usecase-node-selection.md`: business requirement to graph pattern.
- `references/plugin-marketplace-tools.md`: rare/dynamic plugin schema workflow.
- `references/real-world-yml-study.md`: legacy and real-world design evidence.
- `references/complete-examples.md`: complete 0.7.0 graph examples.
- `references/dify-1.16-evaluation.md`: ten-scenario source-backed evaluation,
  results, reproduction command, and remaining workspace-only checks.
- `examples/dify-1.16.0/`: maintained import-oriented examples covering core
  graph, container, Human Input, Agent v2, and Agent App scenarios.

## Authoring Rules

- `workflow.graph.nodes` and `workflow.graph.edges` must both exist for graph
  modes. Node wrapper `type` is normally `custom`; `data.type` is the runtime
  node kind. `custom-note` is non-executable.
- `workflow` entries are `start` or trigger nodes. Non-trigger workflows need a
  reachable `end`; `advanced-chat` needs exactly one `start` and a reachable
  `answer`.
- Every runtime node must be reachable. Do not create accidental cycles.
- `if-else` outgoing handles are case IDs or `false`; question classifier handles
  are class IDs; Human Input handles are user-action IDs.
- Selectors are arrays such as `["node_id", "text"]`; prompt interpolation is
  `{{#node_id.field#}}`. Refer only to declared/known outputs.
- Python Code nodes define `def main(...)`; JavaScript/TypeScript Code nodes
  define `main`. Return keys match `outputs`.
- Tool nodes include exact `provider_id`, `provider_name`, `provider_type`,
  `tool_name`, `tool_label`, and `tool_parameters`. Preserve optional exported
  plugin/tool metadata rather than inventing it.
- `provider_type` can be `builtin`, `api`, `workflow`, or `mcp`. Workspace-local
  Workflow/API/MCP identities may be non-portable.
- Dify runtime interpolation restricts the node-id part of
  `{{#node_id.field#}}` to 1-50 letters, numbers, or underscores even though
  edge and array selectors can still reference IDs containing hyphens.
- Accept both `["sys", "query"]` and Dify frontend system selectors such as
  `[startNodeId, "sys.query"]`. Assigner v2 reads its source selector from
  `items[].value`.
- Never hardcode API keys, database passwords, webhook secrets, credential IDs,
  or private dataset IDs. Use authorization, environment variables, or explicit
  placeholders.
- Prefer parameterized SQL. Treat interpolated SQL, multi-statements, mutation,
  and DDL as risks requiring explicit review.

## Dynamic Plugin Reliability

For a plugin/tool not covered by known schemas, use evidence in this order:

1. Minimal export from the user's target Dify workspace.
2. Plugin source or `.difypkg` metadata.
3. Marketplace documentation.
4. Tool name alone only as a clearly labeled draft.

Do not promise import-and-run reliability without exact provider, tool,
parameters, authorization schema, and dependency identity.

## Validation

```bash
# Human-readable validation
python3 scripts/validate_dsl.py workflow.yml

# Enforce a target version
python3 scripts/validate_dsl.py --target-version 0.7.0 workflow.yml

# CI-friendly output; warnings also fail in strict mode
python3 scripts/validate_dsl.py --format json --strict workflow.yml

# Run the maintained regression set
python3 -m unittest discover -s tests -v

# Strictly validate the maintained versioned fixtures
python3 scripts/validate_dsl.py --strict --target-version 0.7.0 tests/fixtures/valid/*.yml
python3 scripts/validate_dsl.py --strict --target-version 0.6.0 tests/fixtures/valid-0.6/*.yml

# Strictly validate the ten Dify 1.16 scenarios
python3 scripts/validate_dsl.py --strict --target-version 0.7.0 examples/dify-1.16.0/*.yml

# Optional: run Dify 1.16's own node and Agent models
python scripts/validate_with_dify_source.py \
  --dify-source /path/to/dify-1.16.0 \
  examples/dify-1.16.0/*.yml
```

The validator supports 0.6.0 and 0.7.0 and checks version/mode compatibility,
strict Agent package/job/output schemas, graph endpoints and reachability,
cycles, branch coverage, containers, nested selectors, runtime-compatible
template IDs, Human Input schemas, dependencies, node basics, and SQL risks.

If the user requests only review, report import blockers and behavioral defects
first with precise locations. If asked to create or modify a DSL, write the YAML,
validate it, and report the target version plus any remaining workspace-specific
steps.
