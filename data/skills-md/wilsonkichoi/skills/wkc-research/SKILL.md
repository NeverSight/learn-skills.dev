---
name: wkc-research
description: Write or update the product requirements document (PRD) from research material and an interview, covering the problem, who it serves, goals, non-goals, and the evidence behind them. Use when starting a product or making a change that shifts its goals, users, or scope.
argument-hint: "[idea, notes, file paths, or URLs]"
disable-model-invocation: true
---

# wkc-research

- **What it does:** turns research material and the user's answers into the PRD at `prd_file`:
  what the product is for, who it serves, and which evidence supports that.
- **When to use it:** starting a product, or a change that shifts its goals, users, or scope. Re-run
  it when new research arrives. A small feature or fix that fits the current intent does not need
  it: do the work and update the PRD afterwards if something it says changed. Callers are people.
- **Dependencies:** `prd_file` from `docs/dev-agents/config.md`, falling back to
  `docs/dev-agents/PRD.md` when there is no config. The harness's own tools for reading files,
  documents, images, and URLs. No tracker.
- **Input:** free text: an idea, notes, file paths, or URLs. With nothing given, read the existing
  PRD and project context, then ask what changed, or, with no PRD, what problem the product solves.
- **Output:** the PRD file, plus a short report of what changed, what is still open, and whether the
  PRD is approved. `wkc-architect` reads an approved PRD next.

Writes only the PRD. Keep what the user wrote in it unless they ask to change it.

## 1. Read before asking

Read, in this order, whatever exists:

- `docs/dev-agents/config.md`, the configured `context_file`, and the rule files in `rules_dir`.
- The current PRD.
- Everything the user supplied, and research folders the project already keeps, such as `research/`.
  Do not create folders that are not there.

Note contradictions between sources, claims with no source, and material that could not be read.
Material that could not be read is reported by name, never filled in from guesses.

## 2. Ask only what the material leaves open

The PRD needs answers to: what problem, for whom and not for whom, what value, what observable
outcome shows it worked, what is out of scope, and what constrains it (time, budget, platforms,
integrations). Ask about the ones the material does not settle. With no material at all, interview
from zero. An internal tool, or the maintainer themselves, is a valid customer.

The PRD records decisions, not wishes. When an answer is vague or the material contradicts it,
push back once, then accept the user's call.

A question ends its turn. Number the options, put the recommended one first, and accept a digit.
Ask questions whose answers change later questions one round at a time. Never ask for something
the material or an earlier answer already gave.

## 3. Write the PRD

Scale it to the product: a small internal tool may need a page, not every heading below. Use the
outline as a guide and drop sections that say nothing.

```markdown
# <Product> PRD

Status: draft

## Problem
## Who it is for   <!-- and who it is not for -->
## Outcomes        <!-- observable signs that it worked -->
## Goals           <!-- ranked, each phrased as an outcome -->
## Non-goals
## Constraints
## Assumptions     <!-- believed, not yet confirmed -->
## Open questions
## Evidence        <!-- links to the sources behind the claims above -->
## Notes for architecture
## Changes         <!-- dated, newest first, for updates -->
```

Keep three kinds of statement apart: what a source shows (link it), what the user decided, and
what you inferred (label it as an assumption). Never cite a source you did not read, and never
invent market or usage figures.

Technical ideas from the research go under **Notes for architecture** as input, not decisions.
Choosing the stack and designing contracts is `wkc-architect`'s job.

The PRD always states current intent, not a history of requests. When updating it, rewrite only
the affected sections: a requirement that a new one replaces is rewritten or removed, never kept
beside it. Then add a one-line **Changes** entry: the date, what changed and why, what it replaced,
and which known downstream work (SPEC sections, tickets) should be reviewed. Name downstream work
from what you already know; do not scan the tracker. Git history keeps the replaced text.

## 4. Approval

The line under the title records approval: `Status: draft` until the user approves the PRD, then
`Status: approved (YYYY-MM-DD)` with that day's date. Write the approved line only when the user
approves in this conversation.

Show the draft's open questions and ask for approval. An update that changes goals, users,
non-goals, or constraints sets an approved PRD back to `Status: draft`. Clarifications, new
evidence that agrees with it, and **Changes** entries keep the approval.

## 5. Report

Say what changed, which questions are still open, and the status line as it now stands. When the
PRD is approved, the next step is `wkc-architect`.
