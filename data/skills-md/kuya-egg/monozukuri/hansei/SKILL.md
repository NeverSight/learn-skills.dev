---
name: hansei
description: "Reflect on failures, incidents, reviews, and completed software work to turn evidence into durable tests, guardrails, documentation, and process improvements."
---

# Hansei

Hansei is disciplined reflection. In software, examine what happened, why it
happened, and how the system allowed it so the lesson becomes a durable
improvement. This is a Japanese-inspired engineering metaphor, practiced
without blame or ritual for its own sake.

## Use this skill when

- an incident, outage, regression, or escaped defect occurred;
- a review found a recurring quality problem;
- a release or project completed and important lessons should be preserved;
- a workaround has become normal behavior; or
- the team wants to improve its engineering system rather than only patch code.

## Outcome

Produce a concise reflection with:

- the observed impact and timeline;
- contributing technical, process, and communication conditions;
- what made detection, diagnosis, or recovery easier or harder;
- what worked and should be preserved;
- actionable improvements with owners or clear scope; and
- a follow-up test, guardrail, document, signal, or process change.

## Workflow

### 1. Establish the facts

Use logs, traces, tests, diffs, deployments, timelines, and direct reports.
Separate what is known from what is inferred. Do not begin with blame or a
preferred narrative.

### 2. Trace the system's contribution

Ask how the defect could be introduced, remain undetected, reach users, and
persist. Look at missing tests, weak boundaries, confusing ownership, unsafe
defaults, poor observability, rushed handoffs, and misleading documentation.

### 3. Preserve the good

Record the checks, habits, design choices, and response actions that reduced
impact or sped recovery. Reflection should reinforce effective practice, not
only list failure.

### 4. Choose durable actions

Prefer a small number of specific actions that change the system: a regression
test, invariant, validation rule, alert, runbook, decision record, ownership
boundary, or workflow improvement. Assign a clear completion condition.

### 5. Verify the lesson

Confirm that each important action would have prevented, detected, explained,
or reduced the original problem. Remove vague actions that cannot be checked.

## Evidence standard

Use a timeline and concrete artifacts where possible. Do not claim a root cause
that the evidence cannot support. State uncertainty and residual risk plainly.

## Boundaries

- Do not use reflection to identify scapegoats.
- Do not create a long report with no owner or completion condition.
- Do not stop at “be more careful” when a mechanical guardrail is possible.
- Do not reopen unrelated design debates unless the evidence connects them to
  the failure.
- Do not treat a completed meeting as a completed improvement.

## Handoff

Hand off concrete actions to `poka-yoke`, `andon`, `kaizen`, or `shukka` as
appropriate. Revisit the reflection after actions land and verify that the
original failure mode is now harder to repeat.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
