---
name: scenario-workflow-authoring
description: "Use when a task involves creating or editing a Scenario workflow graph through MCP: building an app from a brief, adding or rewiring nodes (models, prompts, approval gates, loops), authoring editor_info, publishing, unpublishing or renaming, importing an exported workflow JSON, migrating a graph built in Weavy, ComfyUI, or another node tool, copying a workflow, or turning a prompt chain into an app. Running or pricing a workflow is scenario-workflows. Keywords: node graph, editor_info, CEL."
license: MIT
---

# Scenario Workflow Authoring

## Overview

A workflow has two representations: `editor_info` (the editable node graph: `nodes`, `edges`, `inputKeys`) and `flow` (the compiled runnable form). Authoring through MCP means writing the whole `editor_info` document: there are no per-node editing tools; every change is a read, modify, write of the full graph through `workflow_create` or `workflow_update`. Never hand-write `flow`: `workflow_publish` compiles `editor_info` into it and flips status to `ready`. Editing a ready workflow's `editor_info` leaves the stale `flow` running until you publish again.

Read [references/editor-info.md](references/editor-info.md) before writing any graph: it holds the node type vocabulary, the node choice doctrine (when an `llm` node is legitimate), the edge direction rule, per-node data contracts, and a validated minimal example. Create, update, publish, copy and delete live in the tool catalog (`scenario_tools_search` plus the matching executor, see the `scenario` skill). `workflows_list`, `workflow_get` and `workflow_run` are direct tools: scope and `dry_run` go in their top-level arguments, never an executor wrapper. Running and pricing: the `scenario-workflows` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step              | Call                                 | Notes                                    |
| ----------------- | ------------------------------------ | ---------------------------------------- |
| 1. Study a graph  | `workflow_get` on a working workflow | Copy the shape, never ids                |
| 2. Model contract | `model_schema_get`                   | Handle names and required inputs         |
| 3. Author         | `editor_info` + `inputs_definition`  | Per the reference file                   |
| 4. Create         | `workflow_create`                    | Non-atomic, see below                    |
| 5. Publish        | `workflow_publish`                   | Compiles `flow`, needs input+output pins |
| 6. Validate       | `workflow_run` with `dry_run=true`   | Prices and runs the real validator       |

`workflow_create` is two calls under the hood: a failed create may still have created a draft whose id is in the error. Recover with `workflow_update` on that id; re-creating duplicates. Seed step 1 with `workflow_get`: it returns the full graph of any workflow whose id you have, public ones included (an id or app URL the user supplies, or your own team's from `workflows_list`). To find a public template, use `search` with `target="workflows"`, `public=true`, a keyword `query`, `limit=3`, and your scope; for example, `query="image"` with raw `filter: 'status = "ready"'`. Read ids from `workflows`, then fetch the chosen graph with `workflow_get`; search hits are summaries, not graph documents. Workflow search supports keyword text and filters only, so omit image and semantic options. Use `workflows_list` for browsing your saved workflows. [scripts/fetch_workflow_examples.py](scripts/fetch_workflow_examples.py) bulk-exports trimmed featured-workflow graphs for maintainers (setup in its header).

## Worked example: a text-to-image app

1. `recommend` with `capability: "txt2img"` and the user's brief as `prompt`, following the `scenario` skill's `next_step` discipline, then `model_schema_get`: its input names become the model node's handle names, and its `required` flag marks what must be wired. Use `search` instead when the user names a model.
2. Author `editor_info`: `text1` with `data.isInput: true`, `model1` with `type: "model"`, `data.modelId` and `data.isOutput: true`, one edge from `model1`'s input to `text1`'s output (edges name the downstream node as `source`, see the reference), `inputKeys: ["text1"]`.
3. `workflow_create` with `name`, `editor_info`, and `inputs_definition` naming `text1` as a string input. The published input key is the node id, which is why run inputs have names like `text1`.
4. `workflow_publish`, then `workflow_run` with `dry_run=true` to validate and price. Fix the graph and re-publish if validation fails.

## Migrating a graph from another node tool

A pipeline exported by Weavy, ComfyUI, or another node editor does not import: only Scenario's own export round-trips. It is translated node by node, then created, published, and dry-run as above. The mapping table, member resolution, and the report the user gets are in [references/foreign-graph-import.md](references/foreign-graph-import.md); read it before touching such an export, since its first rule is to reduce the file to a table locally rather than paste it into the conversation.

## Common mistakes

- Writing UI palette names as node types: persisted types are the camelCase vocabulary in the reference, and every generator is `type: "model"`.
- Wiring edges producer to consumer: persisted edges point the other way.
- Expecting an `editor_info` update to change a live app without re-publishing.
- Retrying a failed `workflow_create` with a second create instead of `workflow_update` on the id from the error.
- Publishing with no pins: at least one `data.isInput` node listed in `inputKeys` and one `data.isOutput` node.
- Gating a text node in front of a builder or model: a branch skips only the node wired to its handle, so the consumer stays pending and the job never completes. Gate the node that does the work, or use a CEL ternary for conditional prompt text, per the reference's `ifElse` section.
- Double-quoted CEL literals: they evaluate but corrupt the canvas editor, single quotes only.
- Sending `workflow_id` to `workflow_copy`: get, update, publish, run and delete take `workflow_id`, but copy takes `source_workflow_id`; the copy inherits everything verbatim and needs its own publish.
