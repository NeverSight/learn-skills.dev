---
name: layer-workflow-import
description: "Use when bringing a workflow built in another tool into Layer: an exported workflow file, a node-graph JSON from any node editor, a screenshot of a node canvas, or a pipeline described in prose. Also when converting, porting, migrating or rebuilding a pipeline as a Layer Blueprint workflow. Keywords: import workflow, export file, node graph, node editor, convert, port, migrate, rebuild, blueprint."
license: MIT
---

# Layer Workflow Import

## Overview

Read what the source does, rebuild it from Layer's node kinds, and hand the whole graph to
`import_workflow`. The result is always private; sharing is a separate step in the Layer app. To run
a workflow that already exists, use `layer-workflows`. The spend gate and polling rules live in the `layer` skill.

If a sibling skill named here is missing from your available skills, ask the user to install it
(`npx skills add layerai/skills --skill <name>`); unattended, proceed from tool schemas and flag the
gap.

## Translate intent, not nodes

Other tools expose the machinery; Layer exposes the task. A low-level text-to-image graph is a model
loader, a text encoder per prompt, an empty latent, a sampler and a decoder. In Layer that is one
generate node. Read what goes in, what each step does, and what comes out, then use the fewest Layer
nodes that do the same job.

How to read an unfamiliar source, and what common node patterns mean, is in
[references/sources.md](references/sources.md).

## Quick reference

| Step            | Tool                                          | Notes                                                        |
| --------------- | --------------------------------------------- | ------------------------------------------------------------ |
| Learn the parts | `get_blueprint_system_config`                 | Node kinds, their ports and value schemas. Call once, reuse. |
| Pick models     | `list_base_models`, `get_base_model`          | Discover by use case. Never copy the source's model name.    |
| Sample files    | `request_file_upload_url` or `upload_file`    | Only for the proof run: a file input's value is a `file_id`. |
| Check the graph | `import_workflow` with `validate_only: true`  | Creates nothing. Fix every problem it reports.               |
| Import          | `import_workflow`                             | Publishes privately by default so it can run.                |
| Prove it runs   | `estimate_workflow_price`, `execute_workflow` | Run shape as in `layer-workflows`. Poll `get_workflow_run`.  |
| File it         | `list_projects`, then `project_id` on import  | Optional: land the workflow in a project for review.         |

## The graph

`graph` is an open object with three maps: `inputs` (parameter key to input parameter), `nodes` (node
id to node) and `outputs` (parameter key to output parameter). No public surface defines the fields
inside them, so do not assume a shape. Node kinds, port keys, port types and value schemas come from
`get_blueprint_system_config`; `validate_only` names whatever is missing or misnamed.

There is no edge list. Whatever is fed names its source in `refs`, `{"_default": [...]}`, holding
`nodes::<node id>[<kind key>]::<port key>` for a node output or `blueprint::<input key>` for a
workflow input.

An output of type A may feed an input of type B only when A equals B or (A, B) is a casting rule. A
rule carrying a `transformer` is blocked, not allowed: insert the named transformer node kind between
the two and wire through it.

Static values must conform to their type's JSON schema in the system config. Where a port selects a
model, discover it with `list_base_models` filtered by the use case that node serves.

## The loop

1. `get_blueprint_system_config` for the workspace.
2. Read the source and write down inputs, steps and outputs in plain words.
3. Map each step to a node kind. When nothing fits, stop and tell the user which step has no Layer
   equivalent, rather than approximating it with an unrelated node.
4. Build the graph, then `import_workflow` with `validate_only: true`. The result groups problems by
   node, input and output. Fix and repeat until `is_valid` is true.
5. `import_workflow` for real, with a clear `name` and a `description` that says where it came from.
   Pass `project_id` when the user wants it filed in a project.
6. Prove it: upload a sample for each file input, `estimate_workflow_price`, confirm above 20 CUs, then
   `execute_workflow` with a `session_name` and poll. A graph that validates can still produce the
   wrong thing; look at the output.
7. Report: the workflow id, what was mapped to what, and anything dropped or approximated.

`publish: false` keeps a draft instead of a runnable workflow, and is accepted even with validation
problems. Use it only when the user wants to finish the graph by hand in the editor.

## Worked example

"Import this workflow." The user attaches a node-graph JSON: a top-level `nodes` list and a `links`
list of `[link, from node, from slot, to node, to slot]`.

1. Reading it: a checkpoint loader, a pixel-art style adapter, positive and negative text encoders,
   an empty 1024x1024 latent, a sampler, a decoder, a 2x upscale and a save node.
2. Intent: text in, pixel-art image out, upscaled 2x. Inputs: the prompt. Fixed: size, the style.
3. `get_blueprint_system_config`, then pick generate-image and upscale node kinds whose ports fit. If
   the generate kind has a style port, check `list_reference_sets` for a pixel-art set; otherwise
   fold the style into the prompt.
4. `list_base_models` with the text-to-image use case; take the first result for the generate node.
5. Graph: input `prompt`; the generate node's prompt port refs `blueprint::prompt`; the upscale
   node's image port refs `nodes::<generate id>[<generate kind>]::<image port>`; an output refs the
   upscale node's output.
6. `validate_only` reports the upscale node's image port as the wrong type. The casting rule for that
   pair carries a `transformer`, so it is blocked: insert that transformer node kind and wire through it.
7. Import, estimate (6 CUs), execute with a `session_name` and a sample prompt, poll, and check the
   image is upscaled and pixel-styled.
8. Report: "Imported as a private workflow. The sampler, latent and decoder plumbing became one
   generate node. The style adapter became a reference set. The negative prompt was dropped: the
   chosen model has no negative prompt port."

## Common mistakes

- Copying a checkpoint or weights file name into a model port instead of discovering a `base_model_id`.
- Inventing field names inside `graph` instead of taking them from the system config and validation.
- Wiring a pair whose casting rule carries a `transformer` instead of routing through that node kind.
- Silently approximating a step Layer has no node for. Say which step and why.
- Promising the workflow is shared. It is private; sharing happens in the Layer app.
- Skipping the test run. Validation checks wiring, not whether the output is right.
