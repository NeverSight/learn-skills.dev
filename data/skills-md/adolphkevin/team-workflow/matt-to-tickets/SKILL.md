---
name: matt-to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
disable-model-invocation: true
---

Before using this method, read the [knowledge and team rules](../team-workflow/references/matt-integration.md): project knowledge comes from team-knowledge (`tw brief`).


# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

Use the project tracker and labels already configured. If absent, retain a local task draft.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

For team work, establish the parent business journey and its acceptance before decomposition. Give each child its real entrypoint, expected behavior and verification requirements; the parent retains its own end-to-end acceptance. Explain unresolved decisions with their scenario, source, options and consequences in each relevant ticket, not just a parent comment identifier.

Break work into **tracer bullet** tickets when decomposition is useful. A simple team task may remain in its existing issue; do not create child tickets merely to satisfy a stage checklist. Assess each proposed task's complexity, risk, effort, uncertainty and required capabilities separately from the parent plan.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. No blocking tickets means only that execution dependencies are clear. For team work, assess implementation readiness under the team delivery rules before starting or marking a ticket ready.

**Wide refactors are the exception to vertical slicing.** Follow the project compatibility policy: if it explicitly permits a direct cutover and forbids parallel runtimes, use one coordinated change with joint validation instead of expand–contract. A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Carry forward existing decisions. Ask only about unresolved scope or dependencies that materially change delivery.

### 5. Publish the tickets to the configured tracker

When publishing is authorized, publish the approved tickets. **How** depends on the project tracker; the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. If the source was an existing issue, make each ticket its sub-issue (tracker doc's operation). For team work, apply an implementation-ready label only after `start` confirms readiness. Otherwise retain a draft or pending-review state with the specific missing condition. Publishing a ticket does not approve its implementation plan.

Work the **frontier**: tickets whose execution dependencies and applicable plan/review conditions are satisfied. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

For a team task, use the [current contracts](../team-workflow/references/contracts.md): associate each actual child with its parent, plan ID and task sections, retaining its own assessment, scope, acceptance and execution prerequisites. Approval concerns named plan sections; confirmed decomposition need not be approved again. A handoff or verification link alone does not authorize closure: actual acceptance, knowledge completion, final delivery checks and existing closure authorization are required.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None (dependency status only)".

**Status:** draft / pending review / ready, determined by the applicable team readiness check

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None (dependency status only)". Omit this section when blockers were set as native edges.

</issue-template>

In either form, avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.
