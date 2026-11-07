---
name: simplification-review
description: "Finds what an implementation or design can drop, merge, or defer while still delivering its goal, and protects what must stay. Use when something looks overbuilt or a plan has more mechanism than its goal needs. Not for cutting backlog scope (use scope-cutting) and not for changing code."
---

# Simplification Review

## Purpose
Recommend a leaner path to the same outcome, with a clear list of what to keep, remove, and defer, and what each removal risks.

## When to use
- Use when: an implementation, design, or technical plan seems to contain more layers, options, steps, or dependencies than the goal needs.
- Do not use when: the question is which backlog items to cut (use `scope-cutting`), the goal is to restructure working code (use `refactor`), or the work is bound by compliance that requires the complexity.

## Inputs
- Required: the implementation or design under review, and its goal with success criteria.
- Optional: constraints, known risks, and the people or systems that depend on it.
- Assumptions: if the success criteria are unclear, restate the goal and confirm before recommending removals.

## Process
1. State the essential outcome and the behavior users rely on.
2. List the mechanisms that serve it: features, abstractions, configuration, steps, and dependencies.
3. For each, ask what breaks or is lost if it is removed, merged, or deferred.
4. Separate safe simplifications from shortcuts that add risk.
5. Return a keep, remove, and defer list with the reason and the cost of each.
6. Name the parts that must stay intact.

## Rules and heuristics
- Required: simplify toward the goal, not toward underbuilding. Never recommend removing safety, accessibility, data protection, legal, or security behavior without flagging it as the owner's decision.
- Required: tie each recommendation to evidence in the artifact.
- Recommended: prefer removing a mechanism over replacing it with a different one.
- Do not make the changes; recommend them.

## Checks
- Every recommendation states what is lost or risked.
- Protected behavior is listed.
- The leaner path still meets the stated success criteria.

## Output
Return: the keep, remove, and defer list with reasons and costs, risk notes, and the next actions.

## Completion criteria
- The owner can accept or reject each item independently.
- Nothing essential to the goal appears on the remove list.
