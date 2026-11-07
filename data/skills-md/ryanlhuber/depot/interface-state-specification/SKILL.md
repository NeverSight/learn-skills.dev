---
name: interface-state-specification
description: "Enumerates and specifies every state a screen or component can be in, including content, actions, messaging, and exits. Use when specifying or reviewing a screen for completeness beyond the ideal case."
---

# Interface State Specification

## Purpose
Enumerate and specify every state a screen or component can be in, including what the user sees, can do, and is told in each, so design and implementation cover more than the ideal case.

## When to use
- Use when: a screen, component, or flow is being specified or reviewed for completeness.
- Do not use when: the question is visual style only, with no behavior or content variation.
- Pairs with: `interface-state-implementation` builds the states this skill specifies.

## Inputs
- Required: the screen or component, its purpose, and the data or conditions that change what it shows.
- Optional: requirements, user flows, system rules (permissions, limits, latency), content examples, platform constraints.
- Assumptions: any state not confirmed by inputs is marked as assumed.

## Process
1. Identify the variables that change the interface: data presence, quantity, loading progress, user permission, connectivity, validity, selection, and user input.
2. Enumerate states from those variables. Consider at least: initial, loading, empty (first use and no results), partial, populated, long or extreme content, error (recoverable and not), disabled or unavailable, in-progress action, success, and offline or stale data.
3. For each state, specify: trigger, visible content, available actions, messaging, focus and announcement behavior for assistive technology, and the exit transitions.
4. Define transitions between states, including interruption and retry.
5. Identify impossible or contradictory combinations and state how they are prevented or handled.
6. Mark which states are in scope and which are deliberately excluded, with reasons.

## Rules and heuristics
- Required: every state has at least one defined way out, or is explicitly terminal.
- Required: every error state says what happened, what the user can do next, and whether data was lost.
- Required: state changes that occur without user action define how they are communicated, including to assistive technology.
- Recommended: show loading states only where wait time is likely to be perceptible.
- Recommended: specify extreme content (very long text, large counts, missing optional fields).

## Checks
- States cover all variables from step 1.
- Each state has trigger, content, actions, messaging, and exits.
- No state leaves the user without a next step.
- Excluded states are listed with reasons.

## Output
Return a state table (state, trigger, content, actions, messaging, accessibility behavior, exits), a transition list, the excluded states, and open questions.

## Completion criteria
- All identified variables map to specified states.
- Every state has a defined exit or terminal status.
- Assumptions and exclusions are explicit.
