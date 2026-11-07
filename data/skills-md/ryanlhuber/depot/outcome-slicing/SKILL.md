---
name: outcome-slicing
description: "Turns a framed goal into epics, each defined by an outcome, a boundary, and ordered delivery slices that each show something observable, and checks that the epics cover the goal and its success measures. Use when a goal is too large to break straight into work items. Not for writing the work items themselves and not for ranking epics."
---

# Outcome Slicing

## Purpose
Divide a goal into epics that are defined by what changes for someone, not by components or layers, and order their slices so that the first one delivers something real end to end.

## When to use
- Use when: a framed goal is too large to break directly into work items, or an existing epic is really a bucket of unrelated work.
- Do not use when: the goal is already small enough for a single breakdown, or the need is a priority order (use a prioritization step).

## Inputs
- Required: the goal with its success measures and constraints, ideally as a problem frame.
- Optional: an assumption register, existing epics, and the structure of the existing system.
- Assumptions: if no success measures exist, say so and derive provisional ones, marked Assumed.

## Process
1. List the distinct outcomes the goal should produce, each phrased as a change someone can observe.
2. Group by outcome, not by component or layer. Each group becomes an epic.
3. For each epic, write the outcome, the boundary (what is in and what is out), and the success measure it serves.
4. Cut each epic into slices. Make the first slice the smallest thing that works end to end for a real user or owner, and say what each later slice adds that can be observed.
5. Check coverage: every success measure traces to an epic, and every epic traces to a success measure or a named constraint.
6. Flag epics with no observable outcome, overlapping boundaries, and slices that deliver nothing visible on their own.
7. Complete the [epic outline](templates/epic-outline.md).

## Rules and heuristics
- Required: an epic is defined by an outcome. "Backend", "Cleanup", and "Misc" are buckets, not epics; regroup them.
- Required: slice vertically. A slice that only delivers one layer must say which later slice makes it visible and why it cannot be merged with that one.
- Required: every success measure maps to at least one epic. Report any that do not.
- Recommended: if there are more than about seven epics, regroup before continuing.
- Recommended: the first slice of the first epic should expose the largest unknown in the plan.

## Checks
- Each epic has an outcome, a boundary, and a success measure or constraint it serves.
- The first slice of each epic is observable end to end.
- Every success measure traces to an epic, and unmapped ones are reported.
- No epic is a layer or a bucket.

## Output
Return the epic outline: each epic with outcome, boundary, ordered slices and what each shows, the coverage check, and any flagged problems. Use the [epic outline](templates/epic-outline.md).

## Completion criteria
- The epics together cover the goal and every success measure, or the gaps are named.
- Each epic's first slice delivers something observable.
- The outline can be handed to a breakdown step without further explanation.
