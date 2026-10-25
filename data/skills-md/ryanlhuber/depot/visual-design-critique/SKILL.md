---
name: visual-design-critique
description: "Assesses visual hierarchy, spacing, typography, alignment, and consistency, separating requirements, conventions, heuristics, and aesthetic preference. Use when a visual design needs structured feedback."
---

# Visual Design Critique

## Purpose
Assess visual hierarchy, spacing, typography, alignment, and consistency, and return findings that clearly separate requirements, conventions, heuristics, and aesthetic preference.

## When to use
- Use when: a visual design needs structured feedback on how well it communicates and holds together.
- Do not use when: the question is only whether it meets an accessibility standard; that needs its own conformance check.

## Inputs
- Required: the design under review and its purpose, audience, and primary tasks.
- Optional: brand or design-system constraints, requirements, platform conventions, intended mood or direction.
- Assumptions: unstated goals are stated as assumed.

## Process
1. Restate the design's goal and the one or two things a viewer must notice or do first.
2. Assess hierarchy: whether emphasis, size, weight, color, and position direct attention to the intended elements in a sensible order.
3. Assess spacing and grouping: whether proximity and whitespace group related items and separate unrelated ones, and whether rhythm is consistent.
4. Assess typography: legibility at intended sizes, scale and weight consistency, line length and spacing, and the number of styles in use.
5. Assess alignment and layout: grid or alignment logic, edge consistency, and balance.
6. Assess color and contrast use: meaning, restraint, consistency, and legibility of text and interactive elements.
7. Assess consistency of components and states against the design system or against itself.
8. Classify each finding as requirement, platform convention, heuristic, or aesthetic preference, and describe its effect on the design's goal.

## Rules and heuristics
- Required: label aesthetic preferences as preferences; they never override requirements, accessibility, or relevant user evidence.
- Required: do not state a visual choice improves usability without support; present it as a heuristic concern.
- Required: tie each finding to the design's goal, not to personal taste.
- Recommended: describe the observed effect first, then suggest the smallest change that addresses it.
- Recommended: note what works so it is preserved through revisions.

## Checks
- Each finding names the element, the effect, the classification, and a suggested change.
- No preference is phrased as a requirement or fact.
- Findings are prioritized by effect on the primary goal.
- Fields follow the [repository finding structure](../../../docs/contribution-evidence-and-quality-standards.md#review-finding-structure).

## Output
Return a goal summary, prioritized findings with classification, strengths, and questions that need design-intent clarification. Use the [critique report](templates/critique-report.md).

## Completion criteria
- Hierarchy, spacing, typography, alignment, color, and consistency are each assessed or marked out of scope.
- Every finding is classified and tied to the design goal.
