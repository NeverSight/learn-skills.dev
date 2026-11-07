---
name: design-to-implementation-qa
description: "Compares a built interface with its design specification and reports mismatches in layout, visual values, content, states, and behavior. Use when an implementation must be verified against an approved design."
---

# Design-to-Implementation QA

## Purpose
Compare a built interface with its design specification and report mismatches in layout, visual values, content, states, and behavior.

## When to use
- Use when: an implementation must be verified against an approved design or specification.
- Do not use when: no specification exists; use a requirements or usability review instead.
- Pairs with: `design-spec-intake` checks the material is build-ready before the build starts.

## Inputs
- Required: the design specification (visuals, tokens, states, behavior notes) and the implemented interface, observable in a rendered or running form.
- Optional: requirements, supported viewports and conditions, accessibility targets, known accepted deviations.
- Assumptions: if the specification is ambiguous, record the interpretation used.

## Process
1. Fix the comparison scope: screens, components, states, viewports, and themes to check.
2. Capture the implemented interface in each in-scope condition as observable evidence.
3. For each, compare against the specification: structure and order, spacing and sizes, typography, color and theme values, imagery, content and copy, and component variants.
4. Compare states and interactions: hover or pointer, focus, pressed, disabled, loading, empty, error, transitions, and keyboard behavior.
5. Compare responsive behavior at the specified change points and at in-between sizes.
6. Record each mismatch with the location, expected value, observed value, and evidence.
7. Classify each mismatch: defect, specification ambiguity, accepted deviation, or specification gap. Rate its impact on users and on requirements.
8. Note anything implemented that the specification does not cover.

## Rules and heuristics
- Required: every mismatch cites the specification source and the observed evidence.
- Required: do not mark an item as passing for a condition that was not observed; mark it unverified.
- Required: a deviation that affects accessibility or a stated requirement is rated by that impact, not by visual size.
- Recommended: group repeated mismatches by shared cause (for example one incorrect value used in many places).
- Recommended: tolerate differences below a stated threshold, and state the threshold.

## Checks
- Every in-scope condition has been captured and compared, or is listed as unverified.
- Each mismatch has expected, observed, evidence, classification, and impact.
- Specification ambiguities are reported, not silently decided.

## Output
Return a coverage summary, a prioritized mismatch list with evidence, grouped root causes, specification gaps or ambiguities, and unverified items. Use the [mismatch report](templates/mismatch-report.md).

## Completion criteria
- Scope is stated and every in-scope condition is compared or marked unverified.
- All mismatches are classified with impact.
