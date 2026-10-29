---
name: plan-feature
description: Turn a request, idea or spec into a planned feature — triage it, write docs/features/NNNN-*.md with deliverables and acceptance criteria, and split it into vertical slices, on GitHub a feature issue with the slices as its sub-issues. Use when someone wants something built that is bigger than a quick fix.
---

# plan-feature

Turn a request into something an agent can build and a human can check.

Only plan: don't write code. Building happens in `build-slice` or `drive-feature`.

`docs/` here means the folder set by `docs` in `AGENTS.md` (default `docs`).

## Triage first

A request may hold several unrelated changes; triage and plan each on its own. Choose the lightest route that's safe, and say which you chose:
- **direct:** small, low-risk and obvious. Just do it; no plan.
- **ticket:** one slice. A single issue with acceptance criteria.
- **feature:** anything bigger, or touching money, auth, deleting data, the data model, or a new external service.

Then ask: **does this change the architecture?** A new component, storage, service or deployment shape, or a change across the codebase (auth, background jobs). If so, decide it before slicing: ADRs (use the `adr` skill) and `docs/ARCHITECTURE.md`, then make the first slice a thin path through the new structure, end to end. Usually the answer is no, in one line.

## The feature doc

`docs/features/NNNN-short-slug.md`. Cover:
- **why:** the problem and who has it
- **deliverables:** what will exist when it's done
- **acceptance criteria:** observable and testable
- **core flows:** which flows in `docs/PRODUCT.md` the feature adds or changes, or none
- **out of scope**
- **risk:** inherits the project default; any override needs a reason
- **slices:** with links to the feature issue and the slices' issues, and which slices can be built together
- **assumptions and decisions** made along the way. Owner decisions go in PRODUCT.md or an ADR; link to them rather than repeating them.
- **status:** `planned`, `building` or `shipped`

Describe what and why. Leave the how to the builder, except where architecture or third-party choices need deciding (use the `adr` skill).

## Slices

- Each slice is vertical: it works end to end and delivers something observable.
- Size slices by what they deliver, not by count. One slice is fine; so is ten.
- Before slicing, settle in the feature doc any rule that several slices share (how a value is parsed, shown or checked), asking as below, so slices built in parallel don't each invent their own.
- Where two cuts are equally vertical, choose the one that lets more slices be built together. Never give up verticality for it: no slice becomes a layer (only the schema, only the API) to free up another.
- Each slice has its own acceptance criteria and notes any known risks, its dependencies, and what it touches: screens, tables, modules, rules.
- In the feature doc, show which slices can be built together: those with no dependency between them and no screen, table or module in common. A shared rule is fine once the feature doc settles it. For example: "1 first; then 2, 3 and 4 together; 5 after 3."

## Issues

Create issues with `gh` (omp's `github` tool can't create them), adding any missing label with `gh label create`. Each body starts with the command that builds it, so a session started from the issue runs the right skill: create the issue, then put that line at the top with `gh issue edit`.
- **Feature:** one issue labelled `feature`, `feature:NNNN` and `ready-for-agent`, starting `/drive-feature <its URL>`, then a short summary and a link to the feature doc. Don't copy the deliverables or acceptance criteria; the doc stays the truth. Link the issue from the doc.
- **Slices:** each a sub-issue, `gh issue create --parent <feature issue> --label slice,feature:NNNN,ready-for-agent`, starting `/build-slice <its URL>`, then its acceptance criteria, dependencies, the slices it can be built with, and what it touches.
- **Ticket:** one issue labelled only `ready-for-agent`, starting `/build-slice <its URL>`, then its acceptance criteria.

With no issue tracker, list the slices in the feature doc.

## Working with the human

- Start from whatever exists, from a one-line idea to a full spec. What they wrote is binding; fill only the gaps.
- Ask about business rules the docs don't settle (what gets recorded, money, who can do what, what users see), as far as `risk` says. `low`: only when you can't go on without an answer. `medium`: where a wrong guess records wrong data or is hard to undo. `high`: any rule that isn't written down. Never guess silently: whatever you don't ask goes in the doc as an assumption.
- Decide technical questions yourself and record them in the doc. Architecture, and anything that commits outside the codebase (a new service, cost, data leaving the system), goes in a `proposed` ADR for the human to accept.
- Ask in one batch, each question with your default; replying `go` accepts them all. If `approve` includes `spec` or `plan`, put the questions in that stop instead of stopping twice.
- Read `approve` from `AGENTS.md` when you get there; the human may have changed it. If it includes `spec`, stop once the deliverables and acceptance criteria are written, before slicing. If it includes `plan`, stop once the slices are planned, before building. At a stop, say exactly what to do, what to check, and what happens after ("reply `go` and I'll …").
- Otherwise go straight on: `build-slice` for a ticket, `drive-feature` for a feature.
