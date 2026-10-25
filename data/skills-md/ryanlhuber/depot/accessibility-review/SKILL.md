---
name: accessibility-review
description: "Evaluates an interface against a recognized accessibility standard and returns verified, prioritized findings with remediation guidance. Use when a design, prototype, or build needs an accessibility check; it does not replace testing with assistive-technology users."
---

# Accessibility Review

## Purpose
Evaluate an interface against a recognized accessibility standard and return verified, prioritized findings with remediation guidance.

## When to use
- Use when: a design, prototype, or built interface must be checked for accessibility barriers.
- Do not use when: only visual preference is in question. Accessibility results do not replace validation with people who use assistive technology.

## Inputs
- Required: the interface under review (design, rendered view, or implementation) and the accessibility standard and conformance target that apply.
- Optional: user flows, supported platforms and assistive technologies, requirements, jurisdiction or policy context, prior audit results.
- Assumptions: if no target is supplied, state the assumed standard and level.

## Process
1. Confirm scope: the screens, states, and flows in review, and the standard and level in force.
2. Inventory in-scope interactive and informational elements, including states such as error, focus, and expanded.
3. Check each element against the standard's principles: perceivable (text alternatives, contrast, resizing, reflow, no reliance on color alone, timing), operable (keyboard access, focus order and visibility, target size, no traps, alternatives to gestures), understandable (labels, instructions, error identification and recovery, consistency), and robust (accurate name, role, value, and state exposed programmatically).
4. Use automated checks only for the rules they can observe, and perform manual checks for the rest: keyboard-only traversal, focus management on dynamic changes, reading and announcement order, and meaningful alternative text.
5. Where behavior needs assistive-technology verification and none is available, record it as unverified.
6. For each finding, record the element, the failed requirement, who is affected and how, evidence, severity, and a remediation.
7. Recheck each remediated element when remediation is supplied.

## Rules and heuristics
- Required: a conformance requirement is distinguished from a usability recommendation.
- Required: never state that automated results prove accessibility; ARIA, a component, or a tool score is not a substitute for correct semantics and operable behavior.
- Required: report jurisdiction-, platform-, and version-specific limits instead of implying universal legal compliance.
- Required: accessibility requirements are not overridden by aesthetic preference.
- Recommended: order findings by impact on task completion, then breadth, then effort.

## Checks
- Every in-scope element and state is accounted for as pass, fail, not applicable, or unverified.
- Each finding has a requirement reference, evidence, severity, and remediation.
- Unverified items state what verification is needed.
- Finding fields follow the [repository finding structure](../../../docs/contribution-evidence-and-quality-standards.md#review-finding-structure).

## Output
Return the scope and standard, prioritized findings (observation, classification, impact and severity, evidence, confidence, recommended action), unverified items with required verification, and a coverage summary. Use the [finding report](templates/finding-report.md).

## Completion criteria
- Scope, standard, and target are stated.
- Every in-scope element is accounted for.
- Findings and unverified items are explicit; no pass is claimed beyond the evidence.
