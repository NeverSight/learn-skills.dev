---
name: wkc-architect
description: Write or update the technical specification (SPEC) from an approved PRD and the existing code, covering components, contracts, data, failure handling, and the decisions behind them, with ADRs for the big ones. Use when a product or change needs technical design before it is planned or built.
argument-hint: "[change summary, file paths, or URLs]"
disable-model-invocation: true
---

# wkc-architect

- **What it does:** turns approved product intent and the existing code into the SPEC at
  `spec_file`: what gets built, the contracts between the parts, and why the big choices went the
  way they did. Writes an ADR only for a decision that is costly to reverse.
- **When to use it:** after `wkc-research` approves a PRD, or for a change that needs new contracts,
  components, or a decision someone will later ask about. Re-run it when the PRD changes. A small
  feature or fix that fits the current design does not need it: do the work and update the SPEC
  afterwards if something it says changed. Callers are people.
- **Dependencies:** `prd_file` and `spec_file` from `docs/dev-agents/config.md`, falling back to
  `docs/dev-agents/PRD.md` and `docs/dev-agents/SPEC.md` when there is no config. `wkc-tracker`
  `list`, only when updating a SPEC in a project with a configured tracker.
- **Input:** free text: a change to design, file paths, or URLs. With nothing given, read the PRD and
  any existing SPEC, then write the missing SPEC, or say where the SPEC no longer matches the PRD.
- **Output:** the SPEC file, any ADRs, and a short report of what changed, which decisions are still
  open, and whether the SPEC is approved. `wkc-plan` reads an approved SPEC next and owns the ROADMAP.

Writes only the SPEC and ADRs: no PRD, product code, scaffolding, ROADMAP, tickets, or config. Keep what
the user wrote in the SPEC unless they ask to change it.

## 1. Read before asking

Read, in this order, whatever exists:

- `docs/dev-agents/config.md`, the configured `context_file`, and the rule files in `rules_dir`.
- The PRD, the current SPEC, and existing ADRs. Use the project's ADR folder if it has one (such as
  `docs/adr/`); otherwise ADRs go in an `adr/` folder beside the SPEC.
- The code the work touches, when there is code. Read the area being changed, not the whole
  repository.

The PRD is approved only when the line under its title reads `Status: approved (YYYY-MM-DD)`.
With no PRD, or a draft one, stop and ask. Recommend finishing and approving it with `wkc-research`
first, and offer to go ahead with intent the user states here, which the SPEC then records under
**Overview**. If the user already said to go ahead, do not ask again. When the PRD's **Changes**
entries name SPEC work to review, start there.

## 2. Ask only what the material leaves open

The design needs answers to: stack and existing expertise, where it runs and the budget ceiling,
who maintains it, hard requirements (latency, uptime, data residency), and the systems it must
integrate with. Read the PRD's **Notes for architecture** first and ask only what is still open.

A question ends its turn. Number the options, put the recommended one first, and accept a digit.
Ask questions whose answers change later questions one round at a time.

## 3. Decide

A choice with two or more viable options and a real tradeoff gets its options shown to the user
before the SPEC commits to one: each option's gains, costs, and what it rules out, with your
recommendation first. That presentation is a question and ends the turn. The user decides.

Write an ADR only when the decision is costly to reverse, such as the database, hosting model,
auth approach, sync versus async processing, or build versus buy. Every other decision is one line
under **Decisions** in the SPEC. Routine choices (formatter, folder names) get neither.

```markdown
# ADR-NNN: <title>

Date: YYYY-MM-DD. Status: accepted | superseded by ADR-NNN

## Context
## Options        <!-- each with gains, costs, what it rules out -->
## Decision       <!-- what, and why -->
## Consequences   <!-- what it forecloses, risks accepted -->
```

Number ADRs after the highest existing one. A decision that replaces an old one gets a new ADR,
and the old one's status becomes `superseded by ADR-NNN`.

When a decision depends on what a service or library can do today, check its current
documentation instead of relying on memory. An unknown that reading cannot settle becomes a spike
for `wkc-backlog`: name the question the spike must answer and the section it blocks. Do not write
experimental code to answer it.

## 4. Write the SPEC

Scale it to the work: a small service may need a page. Use the outline as a guide and drop
sections that say nothing.

```markdown
# <Product> SPEC

Status: draft

## Overview          <!-- prose, plus a Mermaid diagram when it helps -->
## Components        <!-- responsibility, interface, dependencies -->
## Contracts         <!-- APIs, schemas, events: fields, types, error responses -->
## Data
## Failure handling
## Security          <!-- authn/authz, secrets, data classification -->
## Requirements      <!-- measurable: latency, scale, cost, availability -->
## Boundaries        <!-- what it must not become, from the PRD non-goals -->
## Deployment        <!-- environments, CI/CD shape, rollback -->
## Development environment   <!-- toolchain, package manager, test and lint commands -->
## Coverage          <!-- each PRD goal -> the components or contracts that deliver it -->
## Decisions         <!-- one line each; ADR links for the big ones -->
## Risks and dependencies   <!-- for wkc-plan to order milestones by -->
## Open unknowns     <!-- spikes, each with its question and the section it blocks -->
## Changes           <!-- dated, newest first, for updates -->
```

Every PRD goal maps to a component or contract, and every non-goal to a boundary. Contracts that
later work builds against need concrete fields, types, and error responses; leave the rest at the
level the work needs.

**Existing code.** The code already says what it does, so do not copy it into the SPEC. Write what
the code cannot tell a reader, for the area being changed: what stays, what changes, why it was
built that way when known, known debt, and contracts with outside systems. Cite the files read.

The SPEC states the current design, like the PRD. When updating it, rewrite only the affected
sections: a contract or decision that a new one replaces is rewritten or removed, never kept beside
it. Then add a one-line **Changes** entry: the date, what changed and why, what it replaced, and any
ROADMAP milestones that should be reviewed. Git history keeps the replaced text.

When the update changes a contract and a tracker is configured, list open tickets through the
`wkc-tracker` skill's `list` verb, not by reading the backend directly, and name the ones that build
against the old contract. Report them; never edit them. If the tracker cannot be read, say so
instead of guessing.

## 5. Approval

The line under the title records approval: `Status: draft` until the user approves the SPEC, then
`Status: approved (YYYY-MM-DD)` with that day's date. Write the approved line only when the user
approves in this conversation.

Show the open decisions and unknowns and ask for approval. An update that changes a component,
contract, data model, or decision sets an approved SPEC back to `Status: draft`. Clarifications
and **Changes** entries keep the approval.

## 6. Report

Say what changed, which ADRs were written, which decisions and unknowns are still open, any
tickets the change affects, and the status line as it now stands. When the SPEC names a test
command that `test_command` in the config lacks or contradicts, say so; the user updates the config. When the SPEC is
approved, the next step is `wkc-plan`.
