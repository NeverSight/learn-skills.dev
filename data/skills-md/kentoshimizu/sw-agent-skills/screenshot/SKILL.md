---
name: screenshot
description: "Visual evidence capture workflow for reproducible screenshots in engineering and QA tasks. Use when bug reports, regression checks, or implementation proof require stable screenshot artifacts; do not use for design-source extraction or architecture documentation."
---

# Screenshot

## Overview
Use this skill to capture reproducible screenshot evidence that is easy to review and trace back to exact system state.

## Scope Boundaries
- Bugs or regressions need visual evidence for triage.
- Before/after comparison is required for implementation validation.
- QA or review comments require precise state capture.

## Templates And Assets
- Screenshot evidence template:
  - `assets/screenshot-evidence-template.md`

## Inputs To Gather
- Capture intent (bug, regression, implementation proof).
- Exact target state (environment, route, data fixture, viewport, locale).
- Storage location and sharing audience.

## Deliverables
- Screenshot set with stable names and reproducible capture context.
- Metadata log (state, environment, timestamp, operator).
- Optional before/after pair for direct comparison.

## Workflow
1. Define the minimum state required to prove the target issue or behavior.
2. Set deterministic capture conditions (viewport, theme, locale, seed data).
3. Capture screenshots at the smallest useful scope while preserving diagnostic context.
4. Verify key evidence is legible (labels, errors, indicators, timestamps if relevant).
5. Store artifacts under predictable naming and attach reproduction steps.

## Quality Standard
- Reviewers can reproduce the captured state from metadata.
- Artifact names encode purpose and scenario.
- Sensitive data is masked before external sharing.
- Comparison captures use consistent viewport and state conditions.

## Failure Conditions
- Stop when screenshot permissions are unavailable.
- Stop when required masking cannot be completed safely.
- Escalate when capture conditions are non-deterministic and evidence is unreliable.
