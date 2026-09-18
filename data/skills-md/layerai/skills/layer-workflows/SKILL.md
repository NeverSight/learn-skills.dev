---
name: layer-workflows
description: "Use when running a saved Layer Blueprint workflow rather than a single generation: discovering what workflows a workspace has, reading a workflow's input schema, estimating and executing a run, polling its steps, or cancelling it. Also when a repeatable multi-step pipeline exists for a task, when the user names a workflow, or when a workflow input expects a style or a file. Keywords: workflow, blueprint, pipeline, app, multi-step, run, node graph."
license: MIT
---

# Layer Workflows

## Overview

A workflow is a multi-step pipeline a studio built in Layer's Blueprint editor and published. Where
Forge runs one model with parameters you choose, a workflow runs a graph someone already designed,
tested, and standardised. When one exists for the task, it is usually the better answer: it encodes
decisions the studio has already made.

Call `get_workflow_instructions` before the first workflow run in a session. The shared loop and the
spend gate are in the `layer` skill.

If a sibling skill named here is missing from your available skills, ask the user to install it
(`npx skills add layerai/skills --skill <name>`); unattended, proceed from tool schemas and flag the
gap.

## Check for one first

Before building a multi-step sequence out of Forge runs, call `list_workflows` with the workspace id
and the `fulltext` filter set to what the user is trying to make. Results come back ordered by
relevance. A studio that has a published pipeline for character turnarounds does not want an
improvised one, and the improvised version will not match the assets already in the game.

This is worth one cheap read-only call at the start of any task with more than one generation step.

## The input schema is the contract

Every workflow defines its own inputs, and `list_workflows` returns the full JSON schema per
workflow. Treat that schema as the source of truth, not the workflow's name or description. Two
workflows that both say "character sheet" can take entirely different inputs.

Read it before composing the run, and pass exactly what it declares. Two input types have traps:

- **Files.** Upload first and pass the returned `file_id`, or pass the `file_id` an earlier run
  already produced. Never pass a URL where the schema wants a file id.
- **Styles.** A style input takes a reference set's `set_id` from `list_reference_sets`. A
  `base_model_id` is not a valid value there, and passing one fails in a way that reads like a
  workflow bug.

When a required input has no obvious value, ask the user rather than inventing one. A workflow run
that completes with a wrong input still costs full price.

## Estimate, execute, poll

`estimate_workflow_price` with the workflow id and the intended inputs returns the price without
executing. Present it as a table: what the workflow produces, which workspace pays, price against
balance. Above 20 CUs, ask and wait for an explicit yes.

`execute_workflow` returns a `run_id` and `poll_interval_seconds`. `get_workflow_run` reports status
through `PENDING`, `RUNNING`, then `SUCCESS`, `FAILURE`, or `CANCELLED`, and reports step information
while running.

Workflows take longer than single generations, so report progress periodically as
"completed steps / total steps" rather than polling silently. `cancel_workflow_run` stops a run and
releases reserved Creative Units; units already consumed are not refunded.

## Worked example

"Run our character turnaround pipeline on this concept."

1. `list_workflows` with `fulltext: "turnaround"`, which returns the workflow and its input schema.
2. Read the schema. It wants a `character_image` file id, a `view_count` integer, and an optional
   style.
3. The concept came from an earlier run, so it already has a `file_id`. No upload needed.
4. `estimate_workflow_price` with those inputs. It returns 34 CUs against a balance of 900, which is
   over the gate, so present the table and wait for an explicit yes.
5. `execute_workflow`, with a `session_name` so the outputs group in the Layer app.
6. `get_workflow_run` at `poll_interval_seconds`, reporting "3 / 7 steps" as it goes.
7. On `SUCCESS`, present the outputs as a table with links. Each output carries a `file_id` that can
   feed the next run directly.

## Common mistakes

- Improvising a multi-step sequence in Forge without checking `list_workflows` first.
- Guessing inputs from the workflow's name instead of reading its schema.
- Passing a `base_model_id` to a style input that wants a reference set `set_id`.
- Passing a URL where the schema declares a file id.
- Executing without an estimate, or clearing 20 CUs without an explicit yes.
- Polling a long run silently, with no step progress reported.
- Re-uploading an asset that a previous run already produced.
