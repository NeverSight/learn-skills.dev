---
name: quick-refactor
description: Propose a small refactor PR that improves encapsulation, abstraction, and testability, delivered as a validated offline HTML report with before/after diagrams. Use when the user asks for a quick refactor opportunity or a before-and-after refactor proposal.
---

# Quick Refactor

Find one cohesive responsibility whose ownership and tests can improve. Show the requested target design and the smallest useful first PR separately. Preserve behavior and public contracts within the refactor.

## Trace

- Read repo instructions and status; preserve unrelated work.
- Inspect the target, constructor, callers, wiring, collaborators, and tests. Verify the current code.
- Trace state, dependencies, side effects, and lifecycle. For async resources, identify who creates, awaits, cancels, and closes them.
- Note oversized test graphs and private-field assertions.

Stop tracing when source evidence for ownership, lifecycle, callers, and tests is sufficient to assess the proposal. Run focused tests or probes only when they resolve a concrete uncertainty.

## Bound

- Prefer an existing owner; add a class only for state, invariants, or lifecycle. Use functions for stateless work.
- Give the new owner a narrow interface and dependencies, not the whole worker or callback bag.
- Compare at most two options. Show the requested end state clearly, then identify the smallest independently useful first PR, its acceptance criteria, and deferred work; say when no useful refactor exists.
- Keep policy with its domain owner. Separate bug fixes and behavior changes from the refactor.

Done when responsibility, dependencies, files, and tests are bounded.

## Own

Show what moves: methods, state, duplicates, interface, caller duties, ordering, resources, failures, cancellation, and reusable teardown guarantees. Every affected behavior and state must have one owner; the interface must be testable without the original large object.

## Render

Use one content JSON file plus referenced `.mmd` files as the report's source of truth. Start from [examples/proposal.json](examples/proposal.json); consult [the renderer reference](scripts/README.md) for the schema and runtime requirements. Put follow-up edits and optional sections in those sources, then rerender.

Lead with the recommendation and paired before/after flowcharts of the overall process. Add class diagrams when they explain ownership and sequence diagrams when they explain timing, ordering, failures, or cancellation. Choose diagrams by the question they answer, regardless of implementation style. All after views depict the target design; identify the first PR separately.

Label evidence as **reproduced behavior**, **source-supported risk**, or **proposed improvement**. Cite the reproduction or source location; keep illustrative examples distinct from confirmed runtime bugs. Distinguish executed validation from proposed checks.

Resolve `SKILL_DIR` to the directory containing this skill's `SKILL.md`, then run from any working directory:

```sh
python3 "$SKILL_DIR/scripts/render_proposal.py" proposal.json --output report.html
```

The renderer bundles pinned Mermaid, compiles offline to embedded SVGs, and validates the artifact before replacing it. It generates navigation and numbering from core and optional sections. Use neutral diagram styling by default; add a legend in the section's `body_html` only for semantic colors actually used in its diagrams.

Keep the report glanceable: one idea per bullet, usually 3–7 bullets per group; tables for repeated comparisons. Collapse supporting evidence, validation, and tradeoffs. Keep the recommendation, overall process, target design, and first PR visible.

Done when the single render command produces a validated offline report with required core sections, compiled diagram pairs, valid navigation and unique IDs, and no unresolved tokens.

## Prove

- Propose focused interface tests asserting results or collaborator effects; retain integration tests for ordering, persistence, and teardown.
- Cover meaningful success, failure, timeout, rejection, skip, and cancellation paths. Distinguish proposed checks from executed checks.
- Implement only when authorized. Commit, push, or open a PR only when requested.
- Preview the HTML when possible; inspect overflow, diagrams, and readability. Report preview limits honestly.

Deliver the HTML link, a short recommendation, and validation status. Do not duplicate the report in chat.
