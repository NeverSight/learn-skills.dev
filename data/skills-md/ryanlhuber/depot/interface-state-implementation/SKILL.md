---
name: interface-state-implementation
description: "Implements the states a screen or component can be in beyond the ideal case (loading, empty, partial, error, disabled, offline, long or missing content) from a state specification, so each state is representable, rendered, announced, recoverable, and demonstrable. Use when a screen or component with specified states is being built, or when an existing one handles only the ideal case."
---

# Interface State Implementation

## Purpose
Make every specified state real in code: represented in data, rendered distinctly, communicated to all users including those using assistive technology, left through defined actions, and demonstrable without waiting for a real failure.

## When to use
- Use when: a screen or component with a state specification is being built.
- Use when: an existing screen goes blank, stale, or stuck outside the ideal case.
- Do not use when: the states, copy, or recovery behavior are undecided. This work implements decisions. It does not make them.
- Pairs with: `interface-state-specification` defines the states to build; use it first when they are not yet specified.

## Inputs
- Required: the state specification (each state's trigger, content, actions, and exit) and the shape of the data the interface receives (values, in-flight indication, errors).
- Optional: copy, visual design, accessibility requirements, existing components for notices and placeholders, supported browsers.
- Assumptions: an unspecified state is reported as a gap. No copy, behavior, or recovery path is invented for it.

## Process
1. List every specified state with its trigger, what is shown, the available actions, and how it exits. Mark states the interface can reach but the specification omits as gaps.
2. Represent the current state as one value from a closed set, not as independent flags that can combine into impossible states. List the impossible combinations this removes.
3. Define transitions: which events move between states, including retry, cancel, timeout, and partial success. State what happens to existing content during a reload, whether it stays visibly marked as stale or is cleared, as the specification says or as an open question.
4. Render each state distinctly in the same layout region so content does not jump. Reserve space where the specification requires it.
5. Communicate state changes. Announce information that changes without a page navigation through a status or live-region mechanism. Define when focus moves, such as to an error summary after a failed submit, and when it must stay put. Never rely on color or motion alone, and respect reduced-motion preferences for loading animation.
6. Provide actions and exits: retry, dismiss, or an alternative path. No state is a dead end. A disabled control remains discoverable and its reason is given where the specification requires one.
7. Handle content extremes: empty, a single item, very long text, missing optional fields, and longer translations. Truncate only where specified and keep the full text reachable.
8. Make each state demonstrable without a real failure, using a fixture, a parameter, or a state override in the project's existing preview or test mechanism.
9. Test the transitions and the announcements.

## Rules and heuristics
- Required: no invented copy, states, or recovery behavior. Placeholder text is labeled as placeholder.
- Required: error messages say what happened and what the user can do, as written in the specification, and are associated with the failing control or region.
- Required: information conveyed by a state change reaches users who cannot see it.
- Required: every loading state has a bound. Define behavior for a long wait and for failure, or flag the gap. Never wait indefinitely.
- Recommended: keep user input when an error occurs.
- Recommended: show a loading indicator only after a delay threshold if the specification gives one. Otherwise raise the question rather than choosing a value.

## Checks
- Each specified state has a rendering, a trigger path, and an exit, listed in a coverage table, and gaps are listed.
- The state model cannot express the impossible combinations listed.
- For each state change, what a keyboard-only user and a screen-reader user experience is verified, or marked unverified.
- Extreme-content cases are rendered at a narrow width and with long text.
- Each state is demonstrable without a real failure, and the transition tests were run or the omission is stated.

## Output
Return the coverage table (state, trigger, rendering, announcement, focus behavior, actions, exit, evidence), the state model, the code, gaps and assumptions, and the checks performed and not performed.

## Completion criteria
- Every specified state is reachable and demonstrable, and none is a dead end.
- Gaps are reported and not filled.
- Verification and its limits are stated.
