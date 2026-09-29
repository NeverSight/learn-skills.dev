---
name: shape
description: Discuss agreed project work with the user to shape observable feature behaviour and boundaries before Design.
---

# Shape

Shape is an iterative design discussion about work that belongs in the project.
Its purpose is shared understanding of observable behaviour before Design.
The brief records what survives that discussion. The user names the item or
related work to shape. Shape starts only from an existing Backlog item with
`Status: Ready for Shape`. It may prepare related Ready items together, but it
selects at most one Ready Feature Brief for Design.

## Orient and bound the work

Find the existing Backlog item for the requested work. If none exists, return
the work to Direction to decide whether it belongs in the intended end state.
If its status is `Needs Direction`, identify the relevant unresolved question
in Direction and return to that discussion. Do not create an item or start a
Feature Brief from Shape. Return any other status besides `Ready for Shape` to
Direction for review. Read the relevant `.workflow/direction.md` sections,
linked topic documents, the Ready item, existing briefs, and decisions. Inspect
repository behaviour before relying on claims about the current system.
Investigate prior art when it can change behaviour or feature boundaries.
Read only context relevant to the active question.

Start with a concrete proposal, example, or consequence drawn from that context.
Explain what follows from Direction and current system behaviour. Give the user
something to react to, even when the prompt names only a Backlog item.

Identify the feature or small group of Ready items under discussion. Shape
related items together only while their boundaries or order need joint
reasoning. Leave independent items for later rounds. Direction and Backlog
wording supplies ideas, not accepted requirements.

## Explore behaviour

Build a current understanding of the feature with the user. Propose behaviour
and simpler boundaries. Compare meaningful alternatives, construct examples
and counterexamples, and find hidden consequences or missing behaviour. Revise
the proposal when the user disagrees. Keep one consequential issue active, and
explore coupled issues together when separating them hides a trade-off. Do not
ask through a requirements checklist.

Reason as far as the context allows before asking for product judgment.
Investigate repository behaviour or prior art when evidence can settle a
question. State supported facts clearly and explain the reasoning behind a
proposal. Offer options or a recommendation when they help the user judge a
real trade-off. Ask a focused question when the user's judgment is needed.
A normal turn can contain a proposal, its reason, a counterexample, and one
important question. Do not make most turns mainly questions.

Before raising an objection, test it: "If this feature ships as currently described, Y happens because Z." Y is a concrete consequence. Z is the mechanism, supported by repository evidence, external evidence, or a specific unresolved choice. If either part cannot be named, drop the objection. Investigate an important unknown or keep it as an open question instead of calling it a defect. State what is verified, inferred, and still unknown. Name the evidence that could change the assessment. Investigate checkable uncertainty before asking the user to decide a product question.

Discuss one consequential issue until it is understood, resolved, or safely
deferred. One answer does not close an issue by itself. When the user disagrees,
revise the current model of the feature and test its consequences. Explore a
coupled issue that the answer exposes. Challenge weak reasoning and
inconsistencies with evidence, then let the user make the product judgment.
Preserve material feature-behaviour questions in a Draft Feature Brief when one
exists. Keep unresolved end-state questions in Direction and link to them.

Use concrete stories when they expose ambiguity or test proposed behaviour.
Examine successful behaviour, failures, permissions, persistence, lifecycle,
compatibility, and safety when relevant. Use these as lenses, not a fixed
question sequence. State scope and non-goals as understanding improves. Keep
uncertain behaviour in Draft until the user resolves, verifies, removes, or
safely defers it.

Prefer the smallest coherent feature with an independently observable outcome.
Do not invent an actor or story to make internal engineering work appear to be
a feature. Keep refactors, helper work, module changes, migrations, and other
implementation steps within the owning feature's later Design or Implementation.
If technical work may be a separate project capability, return it to Direction
to decide. Do not use Shape to choose internal APIs, modules, data structures,
libraries, implementation plans, or test code.

## Maintain durable records

Create or update a Feature Brief when enough useful behavioural understanding
exists to preserve. Record material changes to a behaviour, boundary, or open
question in an existing brief. Continue the discussion after an edit. Do not
create a brief merely because Shape has started, and do not rewrite it after
every exploratory turn. Mark tentative parts of a Draft clearly.

Use `backlog-document` to update an existing item's agreed boundaries or
relationships when Shape changes them. Direction decides whether discovered
work merits a new item and when an item becomes Ready for Shape. Return such
work to Direction; do not create or promote a Backlog item in Shape. Use
`feature-brief-document` when the discussion has enough useful behaviour to
preserve. Keep each existing draft current with material agreements and open
questions.

Draft Feature Briefs are durable memory of shared behavioural understanding.
They support the discussion instead of driving it. Do not create separate Shape
notes, context dumps, or handoff documents. Keep stable relationships between
future work in the Backlog.

Use `context-document` for agreed project terms and `pdr-document` for durable product decisions whose rationale matters beyond one feature. Use `adr-document` only when an architectural choice must be settled to establish feasibility, observable behaviour, or feature boundaries. Link each affected Feature Brief to shared decisions and constraints. If evidence challenges Direction or an existing decision, return the question to its owning workflow instead of silently changing it.

## Establish acceptance and readiness

As behaviour becomes agreed, express useful stories and observable acceptance
criteria. Give every Ready feature at least one user or system story. Give each
Ready story acceptance coverage. Trace each criterion to its story or a named
feature-wide constraint. Include relevant failures and boundaries. Keep
acceptance criteria about behaviour, not internal design or test implementation.

When Design appears possible, review the brief for one coherent feature,
agreed behaviour, explicit scope and non-goals, failures, acceptance coverage,
linked shared decisions, and material assumptions. Design must be able to
proceed without making product decisions. Discuss unresolved concerns with the
user. Set `Status: Ready` only after the user explicitly agrees. Complete
sections or a passed checklist do not make a brief Ready.

If later evidence requires a material change to behaviour, scope, stories, or acceptance criteria, return the brief to Shape. Set `Status: Draft` before changing that contract. Update the Backlog with the resulting boundaries and durable relationships. Ready briefs that are not selected remain available for later work.

Select no more than one Ready brief as the next Design input. Do not send a Draft brief to Design to resolve a product question. A Shape session may end with only Backlog or Draft brief progress.

## Session boundaries

An ordinary response does not end the Shape session. Continue the feature
discussion across normal turns, including turns after document updates. Do not
interrupt those turns with document reports, lint output, readiness checklists,
workflow bookkeeping, `/clear`, or next-step prompts.

Give an end-of-step report only when the user finishes Shape, requests Design,
agrees that a brief is Ready and transitions, or a context reset is useful.
Then state what changed, what remains open, and the status of affected briefs.
When a Ready brief is selected, name Design and its feature ID. Give a Design
handoff only for a Ready brief. Suggest `/clear` and a copyable prompt only
when a context reset is useful. If repository changes remain before Design,
tell the user about Design's clean-tree entry gate. Do not continue Design in
the Shape context.
