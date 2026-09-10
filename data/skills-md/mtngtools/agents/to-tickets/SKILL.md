---
name: to-tickets
description: Break a plan, spec, or the current conversation into tracer-bullet tickets with blocking edges, published to the configured tracker. Called by /specs-to-tickets; do not reach for it on your own initiative.
argument-hint: "The source to slice — a spec path, an issue number or URL, or nothing to use the conversation"
metadata:
  type: command
  invocation: skill-callable
  applies-to: [planning, tickets, tracker, slicing, github]
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

**Not model-discoverable in practice.** A human may name it, and `/specs-to-tickets` calls it — one spec at a time, at its step 3. Do not invoke it because a plan or a spec happens to be in front of you: publishing a set of tickets to a shared tracker is asked for, never volunteered, and a slice made outside a settled spec slices a plan nobody has agreed to yet.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

Adapted from Matt Pocock's `/to-tickets`; the slicing method below is his.

**Approvals go on the tracker.** The granularity chosen at step 3, and every merge or split the human asks for at step 5, are decisions — follow the `approval-policy` skill for recording them. A ticket body says what to build; if the human's reasoning for a boundary needs keeping, it goes in a comment on the ticket or the parent, never inside the spec being sliced.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Settle the granularity before drafting

The slice rules below decide what a *valid* ticket is; they do not decide **how many**. That is the human's call, and asking after the breakdown is drafted is asking them to re-read the whole thing. Ask first — one question, these two options:

- **Follow the slice boundaries** — cut wherever the [slice rules](#4-draft-vertical-slices) say a boundary falls, and let the count be whatever that produces. The default: each ticket is demoable on its own, and the edges between them are real.
- **Target minimal tickets** — the fewest tickets that still obey the rules. Slices that would be separate only because a boundary *exists* get merged; a boundary is only cut when the rules force it — the piece can't land green alone, or it can't fit one fresh context window.

**Minimal is a ceiling on the count, never a licence to break the rules.** Under it, every ticket is still vertical, still demoable, still context-sized; what changes is that you stop cutting the moment those hold, instead of cutting wherever you could.

**If the caller already settled this**, use their answer and don't re-ask. `/specs-to-tickets` slices several specs in a row and asks once for the whole run — a per-spec re-ask is the thing that makes that skill unusable.

**Done when:** you know which of the two you are drafting to, and where the answer came from — the human, or the caller.

### 4. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

Under **minimal**, the migrate batches are the place the count actually moves: batch by the coarsest unit that still lands green, not by the finest one that could.

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 6. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `/setup-matt-pocock-skills` configured; the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking / sub-issue relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. Apply the `ready-for-agent` triage label unless instructed otherwise; the tickets are agent-grabbable by construction.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None (can start immediately)".

**Status:** ready-for-agent

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

- A reference to each blocking ticket, or "None (can start immediately)".

</issue-template>

In either form, avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Where this sits in the flow

`/specs-to-tickets` routes a map's settled specs here, one at a time, and links what this skill publishes back under the map — this skill leaves the parent issue alone by design. A human may also name it directly against a spec, an issue, or the conversation. Either way the tickets it publishes are the build backlog `/implement` works through.
