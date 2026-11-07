---
name: component-api-design
description: "Specifies a reusable UI component's public interface: inputs, variants, state ownership, events, composition points, styling hooks, and accessibility contract. Use when a component will be shared across screens or teams, or when an existing component's interface has become inconsistent or hard to use correctly."
---

# Component API Design

## Purpose
Define the public interface of a reusable UI component so consumers can use it correctly, extend it safely, and so its internals can change without breaking them.

## When to use
- Use when: a new shared component is being specified, or several one-off versions are being consolidated.
- Use when: an existing component has accumulated flags, overlapping options, or behavior that is easy to misuse.
- Do not use when: an element appears once on one screen with no planned reuse.
- Do not use to decide how the component looks; its appearance comes from the design and its tokens.

## Inputs
- Required: the component's purpose, the real usage cases it must serve (existing call sites or at least two distinct contexts), and the conventions of the codebase it lives in.
- Optional: design specification and states, sibling components and their naming, accessibility requirements, browser and device support, performance limits.
- Assumptions: usage cases that were not supplied are listed as assumptions. Consumers are never invented.

## Process
1. List the usage cases and the variation each needs. Separate variation that changes meaning or behavior from variation that is only visual.
2. Check whether a native platform element or an existing component already covers the need. If so, extend or compose it instead of duplicating it.
3. State the component's single responsibility and what it deliberately does not do.
4. Define each input: name, allowed values or type, default, required or optional, and what it changes. Prefer a small closed set of named options over free-form values.
5. Define the state model: which state the component owns and which the consumer controls. Say whether it supports controlled use, uncontrolled use, or both, and how a consumer chooses.
6. Define outputs: events or callbacks, named for what happened, with their payload and when they fire relative to the state change.
7. Define composition points (content regions, child parts) and what may go in them.
8. Define styling hooks: the tokens, custom properties, or parts consumers may customize, and what stays private.
9. Define the accessibility contract: native element or role, source of the accessible name, keyboard interaction, focus behavior, and how state changes are exposed.
10. Define the behavior for invalid combinations, the defaults, and how a later breaking change would be announced and migrated.
11. For each non-obvious input, write one correct use and one common misuse.

## Rules and heuristics
- Required: every input has a default or is marked required, and none changes meaning depending on an undocumented other input.
- Required: invalid combinations are either impossible to express or fail in a documented, visible way.
- Required: behaviors the component owns, such as keyboard operation and accessible state, are fixed by the interface and not left to each consumer.
- Recommended: prefer composition over adding boolean flags. When two or more flags interact, replace them with one named option or separate parts.
- Recommended: name by purpose, not appearance ("danger", not "red"), and match sibling components.
- Recommended: expose the smallest surface that serves the usage cases. Adding later is cheap; removing breaks consumers.

## Checks
- Every usage case can be expressed with the interface, and every input serves at least one.
- No two inputs overlap in meaning.
- Every piece of state has exactly one owner.
- Every interactive part has a name source and a keyboard behavior.
- Names are consistent with sibling components, or the difference is justified.
- The surface that would be breaking to change is listed.

## Output
Return the interface specification (purpose and non-goals, inputs, state model, events, composition, styling hooks, accessibility contract, invalid-combination behavior, correct use and misuse), the usage cases mapped to it, assumptions, and open decisions. Use the [component API specification](templates/component-api-spec.md).

## Completion criteria
- Another developer could implement the component, and another team could use it, from the specification alone.
- Assumed usage cases and unresolved decisions are labeled, not hidden.
