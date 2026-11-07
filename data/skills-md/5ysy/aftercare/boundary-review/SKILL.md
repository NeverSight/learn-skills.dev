---
name: boundary-review
description: review completed work for boundary leaks across layers, modules, packages, and ownership lines. use when changes cross directory boundaries, touch shared modules, introduce imports between previously independent features, or produce a diff that feels tightly coupled in a way that will age badly.
---

# Boundary Review

Announce at the start: "I'm using boundary-review to check the dependency direction and responsibility ownership of the change."

## Core idea

Most architecture decay happens at boundaries — layer boundaries, package boundaries, module boundaries, ownership lines. A diff can look fine in each individual file and still quietly punch a hole through a line that was holding the system together. The review focuses on direction and ownership, not on code quality inside a single file.

## Workflow

1. Identify the boundaries the change crosses: layer (controller ↔ domain ↔ adapter), package, feature module, ownership line (team A's code ↔ team B's code), public API vs internal.
2. For each crossing, run [`checklist.md`](./checklist.md): is the direction correct, is the crossing through a sanctioned surface, is the receiving side prepared for this coupling?
3. When unsure whether a crossing is a real boundary violation or merely a style preference, walk [`decision-tree.md`](./decision-tree.md).
4. Cross-check against [`anti-patterns.md`](./anti-patterns.md) for the common boundary-leak shapes.
5. Classify findings using [`../../references/severity-model.md`](../../references/severity-model.md). A dependency backflow on a load-bearing boundary is High or Critical; a stylistic layer crossing with no damage is Low.
6. See [`examples/boundary-leak.md`](./examples/boundary-leak.md) for a worked case.

## Workflow output per finding

For every crossing flagged, produce:

1. The intended boundary (drawn in one sentence).
2. The specific import, call, or data flow that crossed it.
3. Why that crossing matters — the concrete next-change cost.
4. The smallest useful repair (usually a single import removed, a single interface narrowed, or a single piece of logic moved one layer).

## Heuristics

- Dependency direction should match the layer diagram the repo implicitly uses. Inversions deserve scrutiny.
- Cross-feature imports should go through each feature's public surface, not into its internals.
- Shared modules should know about types, not about feature-specific behavior.

## Do not

- flag every cross-folder import; many are legitimate
- propose a full layering redesign when one import needs to move
- mistake "I would have organized this differently" for a boundary violation

## Supporting files

- [`checklist.md`](./checklist.md) — per-crossing inspection steps.
- [`anti-patterns.md`](./anti-patterns.md) — boundary-specific anti-patterns extending [`../../references/anti-patterns.md`](../../references/anti-patterns.md).
- [`decision-tree.md`](./decision-tree.md) — deciding violation vs preference.
- [`examples/boundary-leak.md`](./examples/boundary-leak.md) — worked example of a High-severity boundary leak.

## Output

Use the review-report format in [`../../references/report-templates.md`](../../references/report-templates.md). State verdicts with clear blocker vs backlog language: Critical and High findings either block merge or are explicitly accepted as known risk in writing.
