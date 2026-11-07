---
name: technical-debt-audit
description: "Finds and orders technical debt that slows delivery or threatens reliability, ties each item to its real cost, separates it from optional polish, and sequences cleanup by leverage. Use when major roadmap work is coming, a repository is being audited, or change keeps getting harder. Not for one defect or for judging a single change."
---

# Technical Debt Audit

## Purpose
Produce a debt register in which every item has a cost to the team or users, a priority, and a place in a cleanup sequence.

## When to use
- Use when: delivery is slowing, a large piece of work is coming, or a repository is being audited.
- Do not use when: the problem is a single defect (use `bug-fix`), the question is structural fit to goals (use `architecture-review`), or the concern is security weaknesses (use `security-audit`).

## Inputs
- Required: the repository or area in scope, and the delivery goals or decision horizon the audit serves.
- Optional: known pain points, incident history, and test, build, and dependency health data.
- Assumptions: with no goal or horizon, state one and ask for confirmation before ranking.

## Process
1. Inventory debt across code quality, tests, build and release, dependencies, documentation, and operations in the scope.
2. For each item, state the evidence, the cost it imposes (slower changes, defects, outage risk, onboarding pain), and a rough effort band.
3. Drop items that are preference or polish with no stated cost, or list them separately.
4. Rank by delivery leverage: how much the fix speeds or de-risks the goals stated.
5. Sequence cleanup so risk falls early and dependent items follow their prerequisites.

## Rules and heuristics
- Required: an item without a stated cost is not debt. Do not invent impact.
- Required: evidence for each item is a file, a measurement, or an incident, not a general impression.
- Recommended: prefer incremental cleanup tied to upcoming work over a rewrite, and say when a rewrite is truly warranted and what it would cost.

## Checks
- Every item has evidence, cost, and effort.
- Polish is not ranked among debt.
- The ranking follows the stated goals.

## Output
Return: the debt register, a priority ranking with reasoning, a cleanup sequence, and risk notes including what the audit did not cover.

## Completion criteria
- Someone could start the top item from the register alone.
- Every ranking can be traced to a stated goal and a stated cost.
