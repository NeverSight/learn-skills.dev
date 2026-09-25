---
name: scenario-workflows
description: "Use when a task involves running a Scenario workflow through MCP, including anything the user calls a Scenario app, a saved pipeline, or a multi-step generation graph. Triggers include listing workflows, building workflow_run's inputs object, pricing a run with a dry run, approving or rejecting a stuck approval node, a run rejected for input length, or a workflows_list reply flooding the context. Creating or editing graphs is scenario-workflow-authoring. Keywords: workflow, app, approval gate."
license: MIT
---

# Scenario Workflows

## Overview

A Scenario workflow is a saved node graph chaining several models into one call; users say "app" and mean one whose status is `ready`. `workflow_run` returns a job tracked like any other generation.

Only `workflows_list`, `workflow_get` and `workflow_run` are listed by default; approve and reject run through `scenario_tools_search` plus their executor lane. Connection and the core loop: the `scenario` skill. Creating, editing and publishing graphs: the `scenario-workflow-authoring` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step                  | Call                                              | Notes                          |
| --------------------- | ------------------------------------------------- | ------------------------------ |
| 1. List               | `workflows_list` `status="ready"`                 | Always cap `limit`             |
| 2. Read the contract  | list `inputs[]`, get `workflow.inputs_definition` | `name` is the run key          |
| 3. Price and validate | `workflow_run` with `dry_run=true`                | Returns cost, creates no job   |
| 4. Run                | `workflow_run` with `inputs`                      | Returns a job                  |
| 5. Wait               | `jobs_wait`                                       | Re-call with `pending_job_ids` |

Ids are prefixed `wflow_`; copy them from `workflows_list` or `search`, never construct them. For a named app or a public template, call `search` with `target="workflows"`, a keyword `query`, `limit=3`, and your scope; add `public=true` for the public catalog. Workflows support keyword text and filters, not image or semantic search. To find ready apps, add the raw `filter: 'status = "ready"'` (not `filters.status`). Read hits from `workflows`, then call `workflow_get` on the chosen id and read the contract from `workflow.inputs_definition`: search summaries contain neither the run inputs nor the editable graph. Search uses `offset`, not `page_token`; heed any `_hint` on an empty page instead of repeating the same search.

## Cap every list call

Each record carries the compiled `flow` and the whole `editorInfo` node graph, and the tool exposes no compact flag: the two fields made up three quarters of the bytes in live records, which ran from about 1,900 to 22,000 characters, and a draft with `flow: []` still ships its `editorInfo`. Cap `limit` at 3 or fewer, read only `id`, `name`, `hasFlow` and `inputs`, and page with `page_token` set to the previous reply's `nextPaginationToken`, absent on the last page. The tool schema advertised a ceiling of 200 at authoring time while the API rejects anything past 100 with a 400 naming `pageSize` and the range [1; 100], so the schema's maximum is not a value to send.

Only `draft` and `ready` filter server-side; other statuses filter each page client-side (flagged `_workflowListStatusFilter`); there an empty page beside a `nextPaginationToken` means keep paging.

## The input contract

`workflow_run`'s `inputs` object is keyed by `inputs[].name`, taken verbatim from the record. Each name is the id of the node behind it, so names can be positional (`text2`, `text3`), neither contiguous nor ordered.

- `label` and `description` carry the human intent, not the key.
- Never harvest keys from `editorInfo.nodes[].data.name`; node names go stale.
- `required` is an object: test `required.always === true`, a truthiness check reads `{"always": false}` as required too.
- Inputs are typed: `string`, `file`, `file_array`, `string_array`, more. `file` takes an asset id (upload first). Match the type: the API drops scalar-for-array mismatches silently and still charges; `workflow_run` wraps simple scalars into arrays, but only simple ones.
- `inputs[]` is not the whole contract: a string input inherits the length ceiling of the node behind it (a model's own prompt cap, observed as low as 4000 characters), which the record never lists and which surfaces only at run time as a 400 quoting the cap but not the input key. The dry run enforces the same validator at zero cost: route long texts through `dry_run=true` and shorten to fit rather than retrying verbatim, and with several string inputs bisect with dry runs to find the offender.
- `workflow_get` wraps `inputs_definition`/`editor_info` in `workflow`; `workflows_list` wraps `inputs`/`editorInfo` in `workflows`.

## Worked example: run a saved app

1. `workflows_list` with `status="ready"`, `limit=3`, plus `team_id` and `project_id`. Read `id`, `name` and `inputs` off each record; ignore `flow` and `editorInfo`.
2. An `inputs[]` entry `{"name": "text1", "required": {"always": false}}` runs with `{"text1": "..."}`.
3. `workflow_run` with `workflow_id`, `dry_run=true`, and the full `inputs` object. The reply is `creativeUnitsCost`, `creativeUnitsDiscount` and an empty `job`; quote the cost first. It also runs the real validator.
4. Repeat without `dry_run`, then `jobs_wait` on the returned job, re-calling with `pending_job_ids` while it runs.
5. `asset_display` each output asset, one per id.

## Common mistakes

- Guessing input keys from labels or the node graph instead of reading `inputs[]`.
- Skipping the dry run: two of three ready workflows failed its validation with correctly named inputs; report that error, not the payload.
- Reading cost or attribution off the parent job: a finished workflow job bills `cuCost: 0` and lists `assetIds` with no per-model attribution. Every node ran as its own child job carrying the real `cuCost` (together they equal the dry-run quote), and `job_get` `verbose=true` on the workflow job returns `metadata.flow` mapping each node to its child `jobId`, `modelId` and output asset ids.
- Running a draft: `flow: []` and `hasFlow: false` while `inputs` looks complete. Publishing: see `scenario-workflow-authoring`.
- Calling `workflow_approve` or `workflow_reject` without all three of `workflow_id`, `workflow_job_id` and `node_id`: the gate is per node; a parked run never finishes on its own. Find the run with `jobs_list`, read it with `job_get` `verbose=true` (compact replies omit `metadata`): `metadata.flow` lists per-node statuses, the pending approval node's id is `node_id`, the job's id is `workflow_job_id`, its `workflowId` the `workflow_id`. Reject cancels the run.
