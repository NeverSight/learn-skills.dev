---
name: wkc-plan
description: Write or update the ROADMAP, the ordered milestones that deliver an approved SPEC, each with an outcome, scope, dependencies, and an exit check, then hand an approved milestone to wkc-backlog for tickets. Use when a design is ready to be broken into milestones, or when a PRD, SPEC, or request adds, moves, or drops milestone scope.
argument-hint: "[a change to the ROADMAP]"
disable-model-invocation: true
---

# wkc-plan

- **What it does:** writes the ROADMAP at `roadmap_file`: milestones in delivery order, each with an
  outcome someone can check. Once the user approves it, `wkc-backlog` turns a milestone into tickets.
- **When to use it:** after `wkc-architect` approves a SPEC, or when a PRD or SPEC change, or a
  request, adds, moves, or drops milestone scope. A bug, a request inside a milestone's scope, or a
  change to tickets goes to `wkc-backlog` instead. Callers are people.
- **Dependencies:** `prd_file`, `spec_file`, and `roadmap_file` from `docs/dev-agents/config.md`,
  falling back to `docs/dev-agents/PRD.md`, `SPEC.md`, and `ROADMAP.md` when there is no config.
  The `wkc-tracker` skill for reads only: `list`, `show`, and `milestone`, in its `list` and `show`
  forms. The `wkc-backlog` skill for a milestone's tickets.
- **Input:** free text: a change to the ROADMAP, such as a milestone to add, split, reorder, or
  drop. With nothing given, read the documents and the tracker, and write or update the ROADMAP.
- **Output:** the ROADMAP file and its status line, and a short report that names the next
  milestone for `wkc-backlog`.

Writes only the ROADMAP. Never creates, edits, links, or moves a ticket, and never reads or writes
ticket files, `gh`, or Linear itself. Never edits the PRD or SPEC, their status lines included, and
writes no code or config. Keep what the user wrote in the ROADMAP unless they ask to change it.

## 1. Read before asking

Read, in this order, whatever exists:

- `docs/dev-agents/config.md`, the configured `context_file`, and the rule files in `rules_dir`.
- The PRD, the SPEC, and the current ROADMAP.
- The tracker's milestones, with `wkc-tracker milestone list`, and `milestone show <name>` for each
  milestone the change touches, so you know which milestones already have tickets. Use `list` and
  `show` only where a ticket's substance decides where scope belongs. If `wkc-tracker` cannot run,
  say why, and plan without it.

The SPEC is approved only when the line under its title reads `Status: approved (YYYY-MM-DD)`.
With no SPEC, or a draft one, stop and ask. Recommend finishing and approving it with
`wkc-architect` first, and offer to plan from intent the user states here. If the user already said
to go ahead, do not ask again. Approving the PRD or SPEC belongs to `wkc-research` and
`wkc-architect`: never offer to approve one here.

Classify the request before writing:

- A change to what the PRD or SPEC says, such as a new goal, a dropped requirement, or a different
  contract: name it, send it to `wkc-research` for the PRD or `wkc-architect` for the SPEC, and plan
  nothing that depends on it.
- A bug, discovered work, a request inside an existing milestone's scope, or a change to existing
  tickets: that is `wkc-backlog`'s work. Say so, offer to run it, and write nothing.
- A change that adds, moves, or drops milestone scope, or reorders milestones: a ROADMAP change.

Where a milestone needs a decision the SPEC does not make, such as a missing contract field or an
unchosen option, do not make it. Name it under the milestone's **Depends on** and in the report as
work for `wkc-architect`; `wkc-backlog` turns it into a spike or decision ticket.

## 2. Write the ROADMAP

Milestones in the order they ship. Each is a slice someone can check working end to end, not a
layer such as "database" or "API". Order by real dependencies first, then put what the SPEC's
**Risks and dependencies** and **Open unknowns** flag as risky early. One milestone is a valid
ROADMAP. Use the outline as a guide and drop lines that say nothing.

```markdown
# <Product> ROADMAP

Status: draft

## M1: <name>
Outcome: <what a person can do or see once it ships>
Scope: <PRD goals and SPEC sections it delivers>
Depends on: <earlier milestones, outside dependencies>
Exit check: <how to tell it is done: a command, a demo, a measure>

## Changes   <!-- dated, newest first, for updates -->
```

The heading after `## ` is the milestone's name in the tracker too. The ROADMAP holds intent and
order, never progress: no status, checkboxes, assignees, completion dates, or ticket lists. The
tracker owns those, and `wkc-tracker list <milestone>` shows a milestone's tickets.

The ROADMAP states the current plan, like the PRD and SPEC. When updating it, rewrite only the
affected milestones, then add a one-line **Changes** entry: the date, what changed and why, and what
it replaced. Do not rename a milestone that already has tickets; the tracker cannot rename one.
When a change moves scope out of a milestone that has tickets, name those tickets as work for
`wkc-backlog`; never change them here.

## 3. Approval

Show the ROADMAP, or what changed in it, and for each changed milestone that already has tickets,
its counts from `milestone show` and the ticket work the change leaves for `wkc-backlog`.

A question ends its turn. Number the options, put the recommended one first, and accept a digit:

1. Approve the ROADMAP, then draft tickets for <milestone> with `wkc-backlog`.
2. Approve the ROADMAP only.
3. Change something first.

Option 1 names the first milestone in order whose scope has no tickets yet; with none, drop it.

The line under the title records approval: `Status: draft` until the user approves the ROADMAP,
then `Status: approved (YYYY-MM-DD)` with that day's date. Write it only on approval in this
conversation. Changing a milestone's outcome, scope, dependencies, or exit check, or adding,
removing, or reordering milestones, sets an approved ROADMAP back to `Status: draft`. Wording
fixes and **Changes** entries keep the approval.

On option 1, write the status line, then invoke the `wkc-backlog` skill for that milestone. It
drafts the tickets and asks for its own approval before it publishes anything.

## 4. Report

Say what changed in the ROADMAP and its status line, the open decisions for `wkc-architect`, the
ticket work a change leaves for `wkc-backlog`, and the next milestone that needs tickets. Run
`wkc-backlog <milestone>` when a milestone needs tickets.
