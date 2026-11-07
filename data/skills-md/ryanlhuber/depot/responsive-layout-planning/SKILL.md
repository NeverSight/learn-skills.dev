---
name: responsive-layout-planning
description: "Specifies how a layout adapts across viewport sizes, input modes, and user text-size and zoom settings. Use when a screen or component must work across multiple sizes, orientations, or input types."
---

# Responsive Layout Planning

## Purpose
Specify how a layout adapts across viewport sizes, input modes, and user settings, so content stays usable at every supported condition.

## When to use
- Use when: a screen or component must work across multiple sizes, orientations, or input types.
- Do not use when: the target is a single fixed, known display and no user scaling is expected.
- Pairs with: `responsive-implementation` builds the plan this skill produces.

## Inputs
- Required: the content and functions on the screen, and the range of supported viewports and input modes.
- Optional: content priority, design tokens, platform conventions, user zoom or text-size expectations, performance constraints.
- Assumptions: unspecified ranges are stated as assumed.

## Process
1. List the supported conditions: smallest and largest viewports, orientations, pointer and touch input, and user-controlled text size and zoom.
2. Rank content and actions by importance for each primary task.
3. Define the layout at the smallest supported condition first, with everything essential present and reachable.
4. Define the points where the layout must change, based on when content or layout breaks, not on specific device models. For each, state what reflows, resizes, collapses, or relocates.
5. Specify how long content, large counts, and varied language lengths behave in each layout.
6. Specify touch and pointer behavior: target sizes, spacing, hover alternatives, and gestures with non-gesture alternatives.
7. Verify that essential content and actions remain available, in a logical reading and focus order, when enlarged text, increased zoom, or reflow is applied.
8. Record behavior for orientation changes and for conditions between defined change points.

## Rules and heuristics
- Required: no essential content or action is lost, obscured, or requires two-dimensional scrolling at the supported zoom and text-size conditions.
- Required: interactive targets meet the applicable minimum size and spacing requirements.
- Required: the reading and focus order matches the visual order in every layout.
- Recommended: prefer flexible sizing and content-driven change points over fixed device sizes.
- Recommended: avoid hiding features on smaller viewports; reprioritize and relocate instead.

## Checks
- Each supported condition has a layout description.
- Content priority is preserved across layouts.
- Target size, order, and enlarged-text checks are recorded.
- Edge cases (long text, many items, narrow or very wide) are covered.

## Output
Return a layout spec per range (structure, reflow rules, change points, target sizes), the content priority order, edge-case behavior, verification results, and open questions.

## Completion criteria
- Every supported condition has defined behavior.
- Required usability and accessibility checks pass or failures are reported.
