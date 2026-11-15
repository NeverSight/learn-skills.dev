---
name: learner
description: "Reflect on completed work and turn observed failures or successes into durable, testable process improvements. Use for retrospectives and prompt or workflow learning."
---

# Learner

Analyze the supplied run history, artifacts, review feedback, outcomes, and
human decisions. Accept the material as text, structured data, or
caller-selected files.

## Method

- Separate observed evidence from speculation.
- Identify the decision or behavior that caused each material success, retry,
  failure, or delay.
- Prefer a narrow correction to a universal rule.
- Propose a durable rule only when it changes future behavior and can be
  evaluated.
- Convert reusable corrections into fresh scenarios with observable expected
  behaviors; do not encode the answer in the scenario.
- Avoid duplicating an existing rule or scenario supplied by the caller.

## Result

Return `learning` containing:

- `observations`: evidence-backed successes and failure modes.
- `recommendations`: concrete process or instruction changes.
- `scenario_proposals`: target capability, situation, and expected behaviors.
- `followups`: issues that need product or infrastructure work instead of a
  prompt rule.

When invoked directly, present the result in the response. Persist proposals
only when the caller provides a destination and asks for persistence.
