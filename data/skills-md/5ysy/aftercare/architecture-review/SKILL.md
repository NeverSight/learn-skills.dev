---
name: architecture-review
description: review completed or nearly completed code for structural fit, misplaced responsibilities, architecture drift, and maintainability risk. use after feature implementation, before merge, or when a working diff still feels wrong at the repo level — specifically when orchestration and logic appear mixed, when a "shared" module has quietly grown, when the center of decision-making is not where the layering implies it should be, or when a reader needs to hop between multiple unrelated folders to understand one feature.
---

# Architecture Review

Announce at the start: "I'm using architecture-review to inspect structural fit before treating this work as done."

## Core idea

A change can pass tests and still damage the repo. Architecture review asks whether responsibilities landed in the right places, whether boundaries are still legible, and whether the next engineer will be able to change this area without fighting it. It is about *fit*, not taste.

## Workflow

1. Read the change diff at a high level. Map the files touched to responsibilities (entry point, orchestration, domain logic, adapter, test).
2. Identify the real center of decision-making for the feature. If the decisions live in the controller or adapter, that is a finding.
3. Walk [`checklist.md`](./checklist.md) against the changed area.
4. Cross-check against [`anti-patterns.md`](./anti-patterns.md) for the common drift shapes.
5. Classify findings using [`../../references/severity-model.md`](../../references/severity-model.md). Ground each finding in [`../../references/engineering-principles.md`](../../references/engineering-principles.md) — state which principle the code is violating and why it matters *here*.
6. Write the report using [`report-template.md`](./report-template.md). See [`examples/good-report.md`](./examples/good-report.md) and [`examples/bad-report.md`](./examples/bad-report.md) for what "grounded" vs "ungrounded" looks like.

## Heuristics

- The layer that makes the decision should be the layer that names the concept. If the domain is named in the controller and the adapter owns the policy, the layering is inverted.
- A reader who opens one file should be able to find the next relevant file in one hop, not four.
- A new shared module is guilty until proven innocent.

## Do not

- confuse style disagreements with architecture failures
- recommend rewrites when staged repair is enough (see [`../refactor-planning/SKILL.md`](../refactor-planning/SKILL.md))
- demand idealized layering the repo does not otherwise use
- flag every deviation from a textbook pattern; flag deviations that will cost future changes

## Supporting files

- [`checklist.md`](./checklist.md) — inspection steps for layers, responsibilities, coupling, and test shape.
- [`anti-patterns.md`](./anti-patterns.md) — architecture-specific anti-patterns extending [`../../references/anti-patterns.md`](../../references/anti-patterns.md).
- [`report-template.md`](./report-template.md) — architecture-review report extending [`../../references/report-templates.md`](../../references/report-templates.md).
- [`examples/good-report.md`](./examples/good-report.md) and [`examples/bad-report.md`](./examples/bad-report.md) — contrast of a grounded vs ungrounded review.

## Output

Use [`report-template.md`](./report-template.md). Every finding names the principle it violates, the concrete cost to a likely next change, and the smallest repair path. If the repair is non-trivial, hand off to [`../refactor-planning/SKILL.md`](../refactor-planning/SKILL.md).
