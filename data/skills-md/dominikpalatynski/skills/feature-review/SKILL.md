---
name: feature-review
description: Critically review a brief, specification, stage breakdown, or implementation of one feature stage. Check assumptions, scope boundaries, criteria, and evidence; report concrete gaps. Use for a separate design or diff review before user assessment.
---

# Feature Review

Assess whether the design or change achieves the intended outcome and whether
sufficient evidence supports it. Work without edits by default. An explicit
request for fixes expands the scope; review alone does not authorize publishing
comments, approving a PR, or merging.

## Context

Identify the review target: design and stage breakdown, or implementation of
a particular stage. Read the source material, relevant repository instructions,
and code. For implementation, establish the diff scope and current commit or
working-tree state. Treat the author's summary as a guide and inspect requirements
and artifacts yourself.

A fresh session with the stage document, relevant shared contracts, code, and
diff is the preferred setting for a separate review. If working in the author's
session, perform the checks but explicitly call them a self-review. Do not start
additional agents merely to attach an "independent" label.

## Design and stage breakdown

- Does the goal address the user's need, and are key decisions justified?
  Check ownership boundaries and assumptions about the mechanisms being used.
- Is each mechanism necessary for a current requirement or concrete safety need?
  Test a simpler alternative against the same guarantees. Challenge unnecessary
  complexity inherited from the specification too; smaller stages alone do not
  fix an overbuilt design. Distinguish safe failure from automatic recovery.
- Does every part of the scope have an owner and stage, and do dependencies allow
  the stated order? Identify omissions, cycles, and unnecessary scope expansion.
- Does each stage produce one useful demonstrable outcome without implementing
  its successor? Assess size against the ability to review and verify the change.
- Do the criteria actually prove the goal, including a meaningful failure?
  Failure handling and data protection belong with the operation that needs them.
- Are accepted decisions, proposals, dependencies, and unperformed experiments
  distinguished? Does partial deployment leave the system in a valid state?

## Implementation

- Compare the diff with the goal, criteria, and shared contract. Check both
  omissions and scope added without a need.
- For new persisted state or abstractions, trace the present need beyond their
  readers: code using a field does not justify the machinery that introduced it.
  Look for configuration copied into records, redundant facts, and future-only
  consumers; retain state needed for current integrity and safe recovery.
- Trace the main path and realistic failures. Examine authorization, durability,
  concurrency, retries, or migration when the change touches those boundaries.
- Assess tests and evidence. Run useful missing checks when the environment
  allows; do not repeat expensive verification without a reason.
- Verify what actually works in the demonstration and which boundaries use test
  doubles. A screenshot does not prove data durability, and a deployment plan
  does not confirm permissions on a live service.
- Separate code readiness, completeness of evidence, and user acceptance.
  Changes to the diff after review require reassessing affected conclusions.

## Result

Lead with the most important findings, ordered by impact. Each finding includes
a location, concrete scenario, consequence, evidence, and resolution criterion.
Separate blockers, material fixes, and optional suggestions. Do not manufacture
findings to fill a list. Label an unconfirmed concern as a question or missing
evidence rather than presenting it as a discovered defect.
Require a concrete failure scenario under current supported use or a violated
accepted requirement for a blocker. Keep speculative hardening optional; report
simplifications that change accepted guarantees as design proposals with costs.

If there are no findings, say so directly and state the scope and limitations
of the review. List actual checks and missing evidence. Recommend a verdict
appropriate to the material: ready for user review, needs fixes, or lacks evidence.
For criteria that depend on an environment, explain what can proceed and what
remains unverified. AI reviewer approval does not replace the user's decision.

State whether findings require changes to the main specification or future stages.
Put the report in the response; save or publish it only within the requested scope.
Continue fixes or follow-up work already requested in the conversation; completing
the review does not require the user to repeat that instruction. For review-only
requests, finish with the findings and verdict. Respond naturally in the user's
language, identifying any decision or missing evidence needed to proceed.
