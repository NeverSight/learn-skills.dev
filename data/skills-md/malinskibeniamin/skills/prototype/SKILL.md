---
name: prototype
description: Build disposable evidence for unresolved logic, interaction, or visual questions. Use when runnable evidence would resolve behavior or UI uncertainty before commitment.
---

Answer one named question with evidence, not an early production branch.

Choose cheapest faithful shape: logic/state executable model ([LOGIC.md](LOGIC.md)); UI several meaningful variants ([UI.md](UI.md)); API/tool minimal sandbox/fixture call.

Use `.context/prototypes/<question>/`, or target-adjacent only when real runtime must load it; mark in-tree artifacts.

## Retention

Keep the finished runnable prototype as a primary source; never merge prototype-only code to main.

- When the requested endpoint authorizes commits, use isolated `prototype/<name>` plus an issue/decision context pointer.
- Otherwise keep under `.context/prototypes/<question>/`, report path, and move/copy in-tree artifacts there before cleaning the ship diff. Do not delete.

Record the question, evidence, and verdict in an issue, ADR, implementation notes, or implementing commit. Main keeps only validated production decision.

## Constraints

1. Standard library/existing deps; no unrelated scaffolding.
2. One run command; scratch/in-memory persistence.
3. Show relevant state/observations.
4. Before trusting verdict, `/dogfood` once through decisive path and likely boundary, not every edit.
5. Apply retention after the answer.

If evidence contradicts the plan, revisit that decision before production.
