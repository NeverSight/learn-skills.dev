---
name: user-flow-mapping
description: "Maps the steps, decisions, and outcomes a user follows to reach a goal and identifies friction, dead ends, and missing paths. Use when a multi-screen task path must be understood or verified."
---

# User Flow Mapping

## Purpose
Map the steps, decisions, and outcomes a user passes through to reach a goal, and identify friction, dead ends, and missing paths.

## When to use
- Use when: a task spans several screens, states, or decisions and its path must be understood or verified.
- Use when: an existing flow shows drop-off, errors, or confusion that needs structured analysis.
- Do not use when: only a single screen or component is in question.

## Inputs
- Required: the user goal, the starting context, and the intended end state.
- Optional: user types, entry points, system rules or permissions, known pain points, any usage or support evidence.
- Assumptions: any step not supported by the inputs is marked as assumed.

## Process
1. State the user goal, entry point(s), and success end state.
2. List the steps in order as user action → system response. Use one action per step.
3. Mark each decision point with its branches and the condition that selects each branch.
4. Add alternate and failure paths: errors, cancellations, back-navigation, interruption, missing permissions, empty or no-result cases, and recovery.
5. Mark each step for effort and risk: required input, waiting, memory load, irreversible action, or likely confusion.
6. Identify dead ends (no way forward or back), unreachable states, loops without exit, and steps that could be removed or merged.
7. Check that every branch ends in a defined outcome.

## Rules and heuristics
- Required: every path from an entry point ends in a success, a recoverable state, or an explicit exit.
- Required: label friction claims as observation, heuristic, or evidence-backed; do not assert drop-off causes without data.
- Recommended: map the primary path first, then exceptions; show only meaningful steps.
- Recommended: note where the user must recall information shown earlier.

## Checks
- Each step has exactly one user action and one system response.
- All decision branches are labeled and lead somewhere.
- Error and cancellation paths exist for each step that can fail.
- Dead ends and loops are listed or explicitly absent.

## Output
Return the flow as an ordered step list with branches (or an equivalent structured form), a list of friction points with classification and evidence basis, a list of unresolved questions, and recommended simplifications.

## Completion criteria
- Primary, alternate, and failure paths are all mapped to defined outcomes.
- Friction and dead ends are identified with their basis.
- Assumed steps are labeled.
