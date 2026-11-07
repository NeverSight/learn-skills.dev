---
name: to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as text in one file per ticket locally, or native blocking links on a real tracker.
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets** — tracer-bullet vertical slices, each declaring the tickets that **block** it.

Read `docs/agents/issue-tracker.md` and the configured triage vocabulary before publishing. Follow its ownership, Project mapping, and final PR policy. If tracker configuration is absent, tell the user to run `/setup-matt-pocock-skills`.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer-bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges** — the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose blast radius fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket — green is promised only there.

### Issue dependencies versus delivery topology

The `Blocked by` edges are the real product and implementation dependencies. Preserve them accurately; do not add an edge merely because two tickets will be reviewed in sequence.

Stacked PRs are an optional delivery topology, not a replacement for the blocker graph:

- `gh-stack` supports a strictly linear chain of branches.
- A linear ticket chain can be suggested as one stack, with foundational tickets at the bottom.
- A fork should either remain parallel with independent/dependent PRs or be explicitly serialized after the user accepts the throughput tradeoff.
- A join ticket remains blocked by every genuine prerequisite. It should not be treated as the top of a stack until those prerequisites are available in its parent branch.
- A branch must not be shared across multiple stacks; if sibling work needs the same parent, use one deliberate linear stack or ordinary dependent PRs.

After the ticket breakdown is approved, optionally produce a short **delivery topology** for `/implement`:

```text
Issue blockers: #101 → (#102, #103, #104)
Suggested stack: #101 → #104 → #105
Parallel lane: #103
Join: #106 after #102, #103, #105, and #107
```

This topology is guidance for branch/PR operations. It must not replace or silently rewrite the `Blocked by` section in a published ticket.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct — does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?
- If stacked PRs are desired and the graph forks or joins, should the work be serialized into a linear stack or should parallelism be preserved with independent/dependent PRs?

Iterate until the user approves the breakdown and, when relevant, the delivery topology.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `/setup-matt-pocock-skills` configured — the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below — one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Keep the textual `Blocked by` edges, and use the platform's native relationship when it supports one. On GitHub, a declared parent makes native sub-issue attachment part of publishing, not an optional follow-up: create a child with `gh issue create --parent <parent>` when possible, or attach an existing child with `gh issue edit <parent> --add-sub-issue <child>`. A textual parent reference alone is not sufficient. Apply the `ready-for-agent` triage label unless instructed otherwise — the tickets are agent-grabbable by construction.

For GitHub, assign newly created children to the parent's assignees unless the user explicitly divided ownership. If the parent is unassigned or absent, use the developer driving the session (`gh api user --jq .login` unless another developer was named). Preserve existing assignments on retries. Follow the tracker document to ensure membership in the selected Project and initialize new work as `todo`; retain existing progress when resuming. Use Project Status rather than lifecycle labels when Project tracking is configured.

Fetch every published child and verify its assignees and, when configured, Project membership and expected Status. Report tracking failures separately with the existing issue URLs so retries update those issues instead of creating duplicates.

For GitHub native sub-issues, verify the result before reporting publication complete: the parent’s `sub_issues` list must contain every child, and each child’s `parent` endpoint must point back to that parent. If attachment or verification fails because of permissions, tracker support, or an API/CLI error, report the concrete blocker instead of claiming the hierarchy was published.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom. For a graph with forks, multiple frontier tickets may be independently implementable unless the user chose to serialize them into one stack.

Do NOT close or edit a parent issue's body or status. Attaching a child through the native sub-issue relationship is explicitly allowed and required when GitHub is the configured tracker; it changes hierarchy metadata, not the parent's content.

<local-ticket-template>

# <NN> — <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective — not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None — can start immediately".

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective — not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None — can start immediately".

</issue-template>

In either form, avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.
