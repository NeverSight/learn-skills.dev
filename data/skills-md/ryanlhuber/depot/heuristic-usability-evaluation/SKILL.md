---
name: heuristic-usability-evaluation
description: "Evaluates an interface against established usability heuristics and returns prioritized findings with severity and confidence. Use when a design or build needs an expert usability review before or alongside user testing."
---

# Heuristic Usability Evaluation

## Purpose
Evaluate an interface against established usability heuristics and return prioritized findings with severity, confidence, and recommended actions.

## When to use
- Use when: a design or build needs an expert review for usability problems before or alongside user testing.
- Do not use when: representative-user evidence is the question; a heuristic review cannot replace it.

## Inputs
- Required: the interface or flow under review and the primary user tasks.
- Optional: requirements, personas or scenarios, platform conventions, analytics or support evidence, the heuristic set to apply.
- Assumptions: if no heuristic set is given, state the one applied (for example a widely used set of general usability principles).

## Process
1. Define scope: the tasks, flows, and states to evaluate, and the heuristic set.
2. Walk each task end to end as the intended user, recording each point where the interface helps or hinders.
3. For each issue, identify the heuristic it relates to and describe the observed behavior and its consequence for the task.
4. Check coverage of key concerns: visibility of status, match with user language, user control and recovery, consistency, error prevention and messages, recognition over recall, efficiency for frequent use, and clarity of content.
5. Classify each finding: platform convention, heuristic concern, evidence-backed usability issue, or assumption.
6. Rate severity by frequency, impact on task completion, and persistence. Rate confidence separately.
7. Merge duplicates and group related findings by cause.
8. Identify findings that need validation with representative users.

## Rules and heuristics
- Required: heuristics are judgment aids, not empirical findings. State a finding as a concern unless direct evidence supports it.
- Required: severity and confidence are independent; a severe issue may have low confidence.
- Required: aesthetic disagreement is not a finding unless it affects usability, accessibility, or a requirement.
- Recommended: tie each finding to a task, not just a screen.
- Recommended: include what works well when it informs what to preserve.

## Checks
- Every in-scope task was walked through.
- Each finding has an observation, heuristic, impact, severity, confidence, and action.
- No finding is presented as proven without evidence.
- Fields follow the [repository finding structure](../../../docs/contribution-evidence-and-quality-standards.md#review-finding-structure).

## Output
Return the scope and heuristic set, prioritized findings, strengths worth preserving, and the findings that need user validation with a suggested validation approach. Use the [finding report](templates/finding-report.md).

## Completion criteria
- All in-scope tasks are evaluated.
- Findings are classified, rated, and actionable.
- Items requiring user validation are explicitly listed.
