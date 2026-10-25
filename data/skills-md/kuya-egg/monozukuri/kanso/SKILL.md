---
name: kanso
description: "Choose simple, maintainable software designs by removing speculative complexity, comparing alternatives, and making explicit tradeoffs. Use for architecture, API, data-model, dependency, and scope decisions."
---

# Kanso

Kanso is deliberate simplicity. In software, choose the smallest complete
design that solves the real problem and can be changed safely later. This is a
Japanese-inspired engineering metaphor that complements YAGNI, KISS, and
sound design practice.

## Use this skill when

- selecting an architecture for a greenfield project;
- choosing between implementation or integration approaches;
- designing a public API, data model, module boundary, or extension point;
- deciding whether to add a dependency, abstraction, service, or configuration;
- a solution feels clever, generic, or larger than the requirement; or
- a successful first version is at risk of becoming an overbuilt second system.

## Outcome

Produce a design decision that explains:

- the actual requirement and constraints;
- the simplest viable approach;
- alternatives considered and why they were rejected;
- complexity introduced and where it lives;
- invariants, failure behavior, and likely change points;
- how the design will be tested and observed; and
- what is explicitly out of scope.

## Workflow

### 1. Name the problem

Separate the required behavior from imagined future capability. Identify the
smallest useful user or system outcome and the constraints that make it real.

### 2. Generate bounded alternatives

Compare two or three materially different shapes only when the choice matters.
For each, name concepts added, operational cost, failure modes, migration cost,
and reversibility. Do not create a catalogue of theoretical architectures.

### 3. Apply the simplicity tests

Ask:

1. Is this complexity required today?
2. Does it reduce a known risk or future change cost?
3. Does it make the behavior easier to understand and test?
4. Can local duplication be clearer than a new abstraction?
5. Can the design be removed or simplified if the assumption is wrong?

Reject speculative frameworks, wrappers, plugin points, generic serializers,
configuration matrices, and distributed components unless a concrete need pays
for them.

### 4. Preserve a useful seam

Make likely change local and explicit without guessing every future feature.
Keep boundaries cohesive, contracts small, and complexity in the layer best
able to own it. Document the reason for non-obvious placement.

Existing repository conventions take precedence over stylistic defaults when
they are documented, coherent, and not causing the current problem. Change a
convention only with evidence and a clear boundary. Do not reformat untouched
code or apply broad lint fixes while making a focused design change.

### 5. Decide and verify

State the chosen approach, tradeoffs, and non-goals. Define the first vertical
slice and the evidence that would prove the design works. Do not hide an
unresolved decision behind implementation momentum.

## Evidence standard

Every added abstraction, dependency, service, or configuration option needs a
concrete requirement, constraint, or measured problem. Every rejected simpler
option needs a reason grounded in the actual system.

## Boundaries

- Do not confuse extensibility with maintainability.
- Do not optimize theoretical scale before measuring required scale.
- Do not pursue aesthetic purity at the expense of clear delivery.
- Do not use “future-proof” as evidence.
- Do not force a rewrite when a small seam or incremental change is safer.

## Handoff

End with a short decision record and the first verifiable slice. Hand off to
`kata` when implementation is ready, or back to `nemawashi` when a requirement
or stakeholder decision remains open. Use `kodawari` after implementation to
check whether the design stayed as simple as promised.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
