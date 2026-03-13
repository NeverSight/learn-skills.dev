---
name: accessibility-design
description: "Accessibility-first design workflow for specifying semantics, keyboard/focus behavior, readability, and assistive-technology expectations. Use when UI accessibility behavior must be defined before implementation or design sign-off; do not use for backend data modeling or deployment pipeline decisions."
---

# Accessibility Design

## Overview
Use this skill to define concrete accessibility behavior that implementation teams can build and verify without ambiguity.

## Scope Boundaries
- Accessibility behavior for flows or components is undefined or inconsistent.
- Teams need implementation-ready accessibility requirements before release.
- Design changes risk keyboard, screen-reader, or readability regressions.

## Templates And Assets
- Accessibility spec template:
  - `assets/accessibility-spec-template.md`
- Accessibility review checklist:
  - `assets/accessibility-review-checklist.md`

## Inputs To Gather
- Critical user journeys and high-risk interaction points.
- Existing accessibility defects and known constraints.
- Platform scope and assistive technology targets.
- Required policy/baseline level for the project.

## Deliverables
- Accessibility spec per flow/component (semantics, interaction, feedback).
- Prioritized defect/remediation list with user impact.
- Verification checklist for design review and implementation QA.
- Residual risk log for unresolved issues.

## Workflow
1. Identify critical journeys and map accessibility-sensitive interactions.
2. Specify semantic roles, labels, headings, and landmark expectations.
3. Define keyboard behavior, focus order, and focus visibility rules.
4. Define readable visual behavior (contrast, scaling, non-color cues).
5. Define assistive-technology announcements for dynamic state changes.
6. Validate requirements against testability and implementation feasibility.

## Quality Standard
- Interaction semantics are explicit for all actionable elements.
- Keyboard and focus behavior is fully specified across states.
- Error and status feedback is perceivable and understandable.
- Requirements are testable with manual and automated checks.

## Failure Conditions
- Stop when critical journeys lack explicit accessibility behavior.
- Stop when requirements are non-testable in target environments.
- Escalate when unresolved critical accessibility issues block safe release.
