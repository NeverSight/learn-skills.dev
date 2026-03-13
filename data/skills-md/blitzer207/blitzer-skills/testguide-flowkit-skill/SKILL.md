---
name: testguide-flowkit-skill
description: Create, debug, and optimize flow.kit-based test.guide workflows in `flow_definition.py` (flow bundle). Use when designing or modifying flows with `FlowBuilder`/`add_block_with`/`Assign`, selecting/connecting flow.kit blocks (triggers, test.guide, control-flow, user-code), running `main.py` to validate/execute/visualize, or consulting `.vscode/flow-kit-snippets.code-snippets` and `flow_kit/**/*.pyi` / `site-packages/**/*.pyi` for API details.
---

# test.guide flow.kit Workflow Assistant

## Goal

- Create, debug, and optimize `test.guide` automation workflows using the flow.kit flow bundle structure (main editing file: `flow_definition.py`).
- Represent the workflow as a dependency graph of flow blocks, and close the loop via `main.py` (validate/execute/visualize).

## flow.kit Key Concepts (Understand This Before Writing a Flow)

### 1) What are flow.kit, a flow bundle, a flow definition, and a flow block?

- **flow.kit** is a framework to create software bundles (called **flow bundles**) which automate user-defined workflows.
- A **flow bundle** combines the flow.kit runtime with your **flow definition** (`flow_definition.py`). It is designed to be self-contained for workflow automation.
- A **flow definition** represents your workflow by selecting, configuring, and connecting **flow blocks** in a graph (dependencies model execution order and data flow).
- A **flow block** represents one action in the workflow. Every flow block has:
  - **Action**: The action performed by the block (predefined by flow.kit or user-defined).
  - **Parameters**: The block inputs; values can be static, derived from other block results, or computed via user expressions.
  - **Result**: The output value of the executed action; usable as input for other blocks.
  - **Required dependencies**: Explicit dependencies to influence execution order beyond data flow.

### 2) Dependencies and execution (How does the execution engine run the graph?)

- During execution, the flow.kit execution engine runs blocks individually and respects their dependencies.
- Flow blocks can depend on each other in two ways:
  - **Explicit dependencies** via `required_blocks=[...]`.
  - **Implicit dependencies** when a downstream parameter uses an upstream result (e.g. `Assign(...).to_block_result(upstream)` or `to_user_expression("alias.field")` referencing a `result_alias`).
- A block is executed only after all dependency blocks have been executed successfully. If no dependency is defined between blocks, they can be executed in any order.

### 3) Block states (Observable states during execution)

- `INIT`: Block was not executed yet.
- `FINISHED`: Block was executed successfully.
- `ABORTED`: Block was executed and resulted in an error.
- `SKIPPED`:
  - The block was explicitly set to `SKIPPED` (e.g. `ConditionalSkip`), or
  - A dependency block is `SKIPPED` or `ABORTED`.
- The flow execution is finished once all blocks are in one of the final states `FINISHED`, `ABORTED`, or `SKIPPED`.

### 4) Typical execution illustrated with an ASCII diagram

Example workflow (dependency graph of 6 blocks):

```
        ┌─────────┐
        │  [1]    │
        └───┬─────┘
            │
   ┌────────┴────────┐
   │                 │
┌──▼───┐         ┌───▼──┐
│ [2]  │         │ [3]  │
└──┬───┘         └──┬───┘
   │                 │
┌──▼───┐         ┌───▼──┐
│ [4]  │         │ [5]  │
└──┬───┘         └──────┘
   │
┌──▼───┐
│ [6]  │
└──────┘
```

Explanation: the execution engine selects blocks whose dependencies are satisfied and executes them. Below, `READY` means “ready for execution” (not a final state).

```
Step 1: [1]=READY, [2-6]=INIT
Step 2: [1]=FINISHED, [2]=READY, [3]=READY
Step 3: [2]=ABORTED (error), [3]=READY
Step 4: [4]=SKIPPED (dependency [2] is ABORTED)
Step 5: [6]=SKIPPED (dependency [4] is SKIPPED)
Step 6: [3]=FINISHED → [5]=READY
Step 7: [5]=FINISHED → flow finished (all blocks are FINISHED/ABORTED/SKIPPED)
```

## Workflow: Create/Debug/Optimize `flow_definition.py`

### 1) Define the trigger and inputs

- Use exactly one trigger block per flow definition, and ensure it matches the triggering event type.
- For local execution, ensure the root `payload.json` matches the expected trigger payload schema (field names/casing/nesting must match).

### 2) Select blocks (prefer snippets)

- Start with the snippet library: search `references/flow-kit-snippets.code-snippets` by block class name (e.g. `GetArtifact`, `StartReportGeneration`) and use the snippet `body` as a starting template.
- Snippet structure (JSON):
  - Top-level key = snippet name (usually the block class name)
  - `prefix` = what you type in the editor to trigger the snippet
  - `scope` = language scope (usually `python`)
  - `body` = the actual code template (each entry is one line; `\t` indicates indentation)
- How to retrieve a snippet quickly:
  - Search by key: `"GetArtifact": { ... }`
  - Or search by prefix: `"prefix": "GetArtifact"`
  - Copy/paste the `body` lines into `flow_definition.py`, then:
    - move the suggested `from ... import ...` line to the top of the file
    - replace `block_name`, label, and constructor arguments (`...`)
    - fill required parameters by replacing `.to_` with `.to_static_value(...)` / `.to_block_result(...)` / `.to_user_expression(...)`
    - uncomment `result_alias=...` and/or `required_blocks=[...]` when needed
- To look up the block’s module path, parameter identifiers (`PAR__...`), types, and descriptions, use `docs/Block documentation/**.html`.
- If types/interfaces are unclear, inspect type stubs:
  - flow.kit: `flow_kit/**/*.pyi`
  - External dependencies: `site-packages/**/*.pyi`

### 3) Implement the flow definition (in `flow_definition.py`)

- Build the flow in `get_flow() -> Flow` using the chained form `FlowBuilder().add_block_with(...).build()`.
- Keep block references with the walrus operator to reuse them in `to_block_result(...)`, `required_blocks=[...]`, or as `out_block`:
  - Example: `template_list_block := RetrieveAllTemplates()`
- Add a human-readable label for reporting/visualization with `.with_label("...")`.
- Assign parameter values with `Assign(...)` (see `references/how_to_build_a_flow_definition.md`):
  - `to_static_value(...)` for immutable values
  - `to_block_result(upstream_block)` to pass an upstream result (creates an implicit dependency)
  - `to_user_expression("alias.field")` for simple field access/transformations; for more complex conversions, insert a `GenericUserCode` block
- When referencing an upstream result in `to_user_expression(...)`:
  - Set `result_alias="alias"` on the upstream block and reference it as `alias.xxx` in the expression
  - If ordering is unclear or dependency resolution is fragile, add explicit `required_blocks=[...]`
- Optimization hints:
  - Prefer trigger filter conditions over `ConditionalSkip` blocks inside the flow definition when possible (skips earlier and saves runner time)
  - Use `BatchProcessing` for loops over lists (see `examples/batch_processing_usage.py`)

### 4) Validate

- Execute validation after every change to detect static errors early.
- Validation includes:
  - ensuring the flow definition can be parsed successfully
  - checking that the necessary parameters for all blocks are set
  - checking that parameter values match the expected parameter types
  - optionally running pytest unit tests in `test_user_code.py` (methods with the prefix `test_`)
- Run via:
  - CLI: `python main.py --validate` (add `--validate-runs-unittests` if needed)
  - VS Code: `.vscode/launch.json` → “Validate flow bundle (debug)”

### 5) Execute (Fast local feedback)

- Local execution requires:
  - `payload.json` next to your `flow_definition.py` (payload used to execute the flow bundle locally)
  - `.env` in the root of the flow bundle for required environment variables (create it from `.env.sample`; do not commit `.env`)
- Run via:
  - CLI: `python main.py --execute` (add `--validate-runs-unittests` if needed)
  - VS Code: `.vscode/launch.json` → “Execute flow bundle (debug)”
- Safety: keep `.env` in `.gitignore`. For debugging, set `FLOW_KIT_HIDE_TEST_GUIDE_AUTH_KEY=True` to avoid leaking secrets in logs.

### 6) Visualize (experimental feature)

- Run via:
  - CLI: `python main.py --visualize`
  - VS Code: `.vscode/launch.json` → “Visualize flow definition [experimental] (debug)”
- Output: generates a `*.puml` file that can be rendered with PlantUML.

## References (Load on demand)

- Flow definition syntax and special blocks: `references/how_to_build_a_flow_definition.md`
- Block snippets (VS Code snippets JSON): `references/flow-kit-snippets.code-snippets`
  - Search by block name (e.g. `GetArtifact`) and use the `body` as a template in `flow_definition.py`
- For API/type uncertainties:
  - Check `flow_kit/**/*.pyi` first
  - Then check `site-packages/**/*.pyi`

## Repository Quick Reference

- `flow_definition.py`: flow definition (main editing file)
- `main.py`: entry point (validate/execute/visualize)
- `.vscode/launch.json`: debug/run configurations
- `payload.json`: local execution trigger payload
- `.env` / `.env.sample`: local execution environment variables (do not commit `.env`)
- `test_user_code.py`: pytest unit tests executed during validation (`test_` prefix)
- `examples/batch_processing_usage.py`: full `BatchProcessing` example
