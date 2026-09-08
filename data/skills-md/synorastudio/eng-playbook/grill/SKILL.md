---
name: grill
description: Run a Grilling Session over a concrete plan or design. Use when the user asks to grill or challenge it through a decision-by-decision interview before implementation. Do not use for ordinary planning, review, or implementation.
---

# Grill

Stress-test a concrete plan before implementation.

This skill does not ingest broad project context, initialize an Agent Operating System, create issues, or manage living docs. Use `intake`, `init-agent-os`, `write-issues`, or `maintain-living-docs` for those workflows.

## Core instruction

Interview the user relentlessly about every aspect of the plan until there is shared understanding.

Walk down every branch of the design tree, resolving dependencies between decisions one by one. Ask one question at a time. For each question, provide your recommended answer when you have enough context to do so.

If a question can be answered by inspecting the repo or existing docs, inspect those instead of asking.

## Inputs

Before grilling, read relevant existing artifacts when available:

- `LANGUAGE.md` and local `LANGUAGE.md` files.
- `LANGUAGE-MAP.md` if multiple language contexts exist.
- Relevant durable docs under `docs/`, including living docs and ADRs.
- The linked Decision Map and Decision Issue when the Grilling Session is resolving a mapped branch.
- The specific plan, feature, design, or architecture proposal being grilled.

If the user has not provided a concrete plan or design to grill, ask them to provide one or suggest running `intake` first.

## Grilling posture

Start as a collaborative skeptic. Escalate when ambiguity, contradiction, or risk remains.

Push especially hard on:

- Ambiguous product language.
- Hidden assumptions.
- User-facing scope.
- Domain boundaries.
- Data ownership.
- State transitions.
- Failure modes.
- Auth, permissions, and security.
- External dependencies and vendor lock-in.
- Irreversible or expensive architecture choices.
- Places where the proposed design conflicts with existing docs or code.

## Design Tree method

Work from broad decisions to dependent details:

1. Clarify the target outcome.
2. Identify the main design branches.
3. Pick the branch that blocks the most downstream decisions.
4. Ask the next decision-forcing question.
5. Resolve or explicitly defer that branch.
6. Move to the next dependent branch.
7. Continue until no major branch is vague enough to threaten implementation.

Do not batch a long questionnaire. Ask one question, wait, then continue.

## Handle each turn

When the user replies with a question, uncertainty, a proposed alternative, or a prompt like "thoughts?", stay on the current branch. Answer the user's question, refine the recommendation, and wait for an explicit resolution before asking the next design-tree question.

Treat these as signals to pause progression:

- The user asks for thoughts, trade-offs, or clarification.
- The user challenges the recommendation.
- The user proposes another framing or doc location.
- The user says to hold the next question.

Only move to the next branch when the current decision is accepted, rejected, explicitly deferred, or clearly resolved by the user's response.

## Update docs during grilling

Use docs only for durable knowledge discovered during the interview. When a decision resolves a vocabulary ambiguity or other durable documentation point, update the smallest relevant doc immediately before moving to the next design branch.

Update `LANGUAGE.md` when a project-specific term is clarified, unless the user has asked not to edit files. Follow `../maintain-language/LANGUAGE-FORMAT.md`.

Prefer tightening an existing term over adding a new term when the decision is that a proposed phrase should not become project language.

After each inline doc update, briefly state:

- The resolved decision.
- The file changed.
- The next branch or question.

Offer an ADR only when all three are true:

1. The decision is hard to reverse.
2. The decision would be surprising without context.
3. The decision came from a real trade-off.

When an ADR is clearly warranted, offer to write it immediately and follow `../write-adr/ADR-FORMAT.md`.

When the session owns a linked Decision Issue, record its accepted resolution and update the parent Decision Map before moving on. Keep the full reasoning in the Decision Issue and only a linked summary in the map.

Do not update living docs, write a Spec, create Feature Issues, or initialize Agent OS files from this skill unless the user explicitly asks to switch workflows.

## Completion criteria

Complete the grilling session when:

- The plan's goal and non-goals are clear.
- Every Design Tree branch that could change scope, system boundaries, data ownership, state, security, or an expensive dependency has been resolved or named.
- Blocking decisions are resolved or explicitly deferred.
- Key terms are aligned with `LANGUAGE.md`.
- ADR-worthy decisions have been identified.
- Each remaining uncertainty has an owner or a named next workflow.

End with a compact decision summary, explicit deferrals, doc changes, ADR candidates, and the next recommended action. Return to `map-decisions` when other mapped branches remain. Suggest `write-spec` only when an established Milestone needs product review or must survive across agent sessions.
