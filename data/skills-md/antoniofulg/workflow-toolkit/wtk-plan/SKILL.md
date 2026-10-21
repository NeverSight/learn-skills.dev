---
name: wtk-plan
description: 'Turn decided sources into modular tasks with observable criteria and explicit scope. Use when writing tasks from a PRD, design, RFC, or ticket; not discovery or implementation.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 0.2.0
---

# TLC Plan

Turn decided work into `.tasks/<name>.md` with observable criteria with concrete values, grounded
in the repository. A one-line ticket can be a decision; an unshaped wish belongs in discovery.
This skill plans modular work and does not implement it.

When implementing a selected image or design, freeze [the UI contract](../wtk/references/ui-ux.md)
before coding and carry its source and evidence requirements through build and independent verification.
Use the `ui` profile for binding interface sources.

## Source and scope

Apply [project requirements](../wtk/references/project-requirements.md) before deriving criteria:
read applicable project rules and selected required driver instructions, then land their obligations
in the task's native fields. Its fresh criteria review must complete before dependent feature build.

Read the source and the code relevant to its claims. Resolve factual questions from existing code,
conventions and documentation. Correct factual source errors within the authorized scope; a conflict
with an approved product decision needs clarification, not a silent rewrite.

Each criterion must describe an observable outcome with a concrete field, status, bound or other
value and an explicit boundary. It must be possible to name an execution that settles the claim.
Separate behavior from distributional service targets such as p95 latency or uptime; record how the
target is measured under observability instead of letting a behavior test claim to prove it.

For a guarantee that something will not happen, identify the mechanism preventing it, either in
existing code or a `Decided` row. Check relevant failure paths: a retry after remote success and
local failure is different from a retry after nothing happened. An absent mechanism is a decision
gap, not a guaranteed outcome.

Keep new capabilities outside the task unless the user authorizes them. Preserve already-settled
intent and use the task as the feature contract; the
[project decision store](../wtk/references/artifacts.md#decision-store) retains lasting rationale.
If linked sources later diverge on a binding decision, resolve that conflict before building.

When the source requires reuse, construction order or approval, apply
[construction constraints](../wtk/references/construction-constraints.md) while writing criteria.
At handoff, resume or compaction, use [context recovery](../wtk/references/context-handoff.md).

## Slice and task boundaries

A slice is one observable outcome, not a layer such as schema or endpoints. Enumerate the source's
slices, then default to one task for the whole source. Split only for a demonstrated order constraint,
an answer only another party can supply, or different team ownership.

Use project conventions or reachable issue-tracker evidence for task size; git history describes
pull-request size, not task size. For a large task, show its irreversible decisions and actual seams
so the user can choose a meaningful cut. Do not impose a fixed slice, file or agent count.

Ground what the change disturbs: existing terms, data and callers, plus choices that introduce a new
pattern. `Decided` records only hard-to-reverse choices, their literal shape and rejected alternative.
Reversible placement, helpers and class structure belong to the builder and the diff.

## Surface and requirement coverage

Walk only the surface kinds the source exposes. Record each applicable item's landing in
`## Observable`: an existing criterion, `existing - <what>`, `n/a - <reason>`, or `Unresolved <n>`.
Use `None - no user-facing surface` when appropriate. A missing decision becomes a question; the
walk never creates a criterion just to fill a row.

| Surface | Decisions to account for |
| --- | --- |
| Screen/view | Empty, loading, error and unauthorized states; density, ordering and destructive confirmation |
| API/webhook | Response and error shapes/codes, caller authority, versioning and rate-limit behavior |
| Command/job | Output, verbosity, flags/defaults, exit codes and partial failure |
| Document/copy | Structure, tone, depth and the reader's next action |
| Organized collection | Grouping, naming, ordering, duplicates and exceptions |

Record the landing for each of the nine implicit dimensions in `Swept`: validation, failure modes,
idempotency and retry, authorization, concurrency and ordering, data lifecycle, external-dependency
failure, state transitions, and observability. Each lands on an existing criterion, existing behavior,
`n/a` with a reason, or `Unresolved`; these dimensions do not authorize extra scope.

A cited criterion must observe that dimension. For example, rejecting an existing duplicate does
not prove concurrent writes are safe, and event deduplication does not prove ordering. Keep the
landings explicit so `wtk-implement` can derive proofs from them without repeating the discovery.

## Decisions and unresolved questions

Resolve routine facts and reversible choices from the repository and existing authorization. Ask
only when a material choice belongs to the user and remains unsettled; continue independent work
while waiting. Give concrete options and a recommendation when useful, without manufacturing a
quota of questions or requiring a particular answer format.

Use safe defaults for non-blocking ambiguity, marking `Kind: open` and the default in `Until answered`.
Mark missing decisions that prevent a satisfiable criterion as `blocks`; prerequisites
that only prevent real-world activation use `blocks go-live`. Preserve the output contract's literal
fields and values. A proposed default is not approval; explicit delegation such as “you decide” is,
and is recorded as `user delegated` on the Sources line.

## Deliverable

When writing the task, read [document-format.md](references/document-format.md). Keep its literal
headings and required fields, including `Observable`, `Swept`, `Decided` and `Unresolved`.
Use existing source material to complete the artifact without asking the user to repeat it.

Present the task or justified split, followed by unresolved decisions with blockers first. Complete
the requested planning artifact and its applicable checks; do not begin implementation unless it
was also authorized. A source with unresolved product intent remains provisional.

Tasks are verification units; pull requests are review units. Preparation may belong in a commit
or PR without being its own task. If review needs smaller PRs, propose that separately using the
project's review conventions; preserve order constraints needed for safe intermediate states.

For library-specific facts not established locally, use the project's documentation tools and
current official documentation. Record uncertainty rather than inventing an API or behavior.
