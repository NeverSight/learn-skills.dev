---
name: refactor
description: "Improves code structure while keeping behavior the same, in small steps each verified against a safety net. Use when code needs decomposition, clearer boundaries, naming, or maintainability work. Not for changing behavior, fixing defects, or choosing an architecture."
---

# Refactor

## Purpose
Reduce the cost of future change in specific code without changing what it does.

## When to use
- Use when: named code is hard to change, understand, or test and the outcome wanted is structural.
- Do not use when: behavior is meant to change (use `feature-build`), the problem is a defect (use `bug-fix`), or the structure question is system-wide (use `architecture-review`).

## Inputs
- Required: the target code and the maintainability outcome wanted.
- Optional: existing tests, constraints such as frozen public contracts, and verification commands.
- Assumptions: if tests are thin, the safety net must be built before the structure changes.

## Process
1. State the behavior that must remain stable, including public contracts.
2. Establish a safety net. Run existing tests; where coverage of the target is thin, add tests that pin current behavior first and say so.
3. Pick the smallest structural improvement with a real payoff.
4. Change in small steps. Re-run the safety net after each step and stop at the first difference.
5. Keep public contracts stable unless the task explicitly changes them.
6. Report what changed, what stayed the same, and the debt that remains.

## Rules and heuristics
- Required: behavior preservation is the default. A needed behavior change stops the refactor and is reported as separate work.
- Required: no new abstraction without a stated payoff. Prefer readable code over clever code.
- Required: never report tests as passing unless they ran.
- Recommended: keep structural and behavioral changes in separate commits or clearly separated steps so a reviewer can tell them apart.

## Checks
- The safety net passed before the first change and after the last.
- Public contracts are unchanged, or each change is called out.
- No behavior change is hidden inside the diff.

## Output
Return: the refactor, behavior-preservation notes, verification results, and remaining debt.

## Completion criteria
- The target is structurally better by the stated outcome and the safety net is green.
- A reviewer can confirm from the report that behavior did not change.
