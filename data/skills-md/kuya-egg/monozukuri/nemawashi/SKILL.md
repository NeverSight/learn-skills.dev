---
name: nemawashi
description: "Clarify software goals, constraints, stakeholders, and risks before consequential design or implementation work. Use for greenfield ideas, ambiguous requirements, architecture decisions, or changes where misunderstanding would be costly."
---

# Nemawashi

Nemawashi is the practice of preparing the ground before a consequential
change. In software, it means building shared understanding before building
the system. This is a Japanese-inspired engineering metaphor, not a claim
about how every team works.

## Use this skill when

- the request is ambiguous or has competing interpretations;
- a new project is starting from scratch;
- architecture, data shape, public API, migration, or operational behavior
  could be difficult to reverse;
- multiple people, systems, or teams depend on the outcome; or
- implementation would otherwise require guessing.

Do not use a long interview for a clear, low-risk edit. Ask only questions
whose answers can change the work.

## Outcome

Produce a concise engineering brief containing:

- the problem and why it matters;
- users, systems, or stakeholders affected;
- desired behavior and explicit non-goals;
- constraints and success criteria;
- facts, decisions, assumptions, and open risks separated clearly;
- the smallest useful next step; and
- how the result will be verified.

## Workflow

### 1. Establish the frontier

State what is already known and identify the first uncertainty that could
change the design. Do not ask for information that will not affect the next
decision.

### 2. Interview deliberately

Ask one focused question at a time. Prefer questions about:

- the user-visible outcome;
- the boundary of the request;
- data ownership and lifecycle;
- compatibility and migration needs;
- failure tolerance and recovery;
- security and authorization;
- performance or scale that is actually required; and
- what “done” means.

When a reasonable default exists, state it and continue rather than creating an
endless questionnaire. Ask for confirmation when the default changes risk,
scope, or external behavior.

### 3. Make the shape explicit

Summarize the problem in plain language. Name what will change, what will not
change, and which decisions are reversible. For a greenfield project, include
the first vertical slice rather than designing the entire future platform.

### 4. Stop at the right boundary

Stop interviewing when the next work can be planned and verified without
guessing. If a critical question remains unresolved, stop before
implementation and explain why it matters.

## Evidence standard

Do not present an assumption as a fact. Label statements as `Observed`,
`Decided`, `Assumed`, or `Open`. For an existing project, point to the files,
commands, documentation, or behavior that support important claims.

## Boundaries

- Do not make architecture decisions merely to end the interview.
- Do not expand a feature into a platform because future use is imaginable.
- Do not substitute consensus theater for a concrete decision.
- Do not block a reversible prototype on questions that only matter at scale.
- Do not implement while a material ambiguity remains hidden.

## Handoff

End with a short brief another engineer can act on. Recommend the next
focused skill only when useful: `genchi-genbutsu` for evidence, `kanso` for
design, or `kata` for an already settled implementation.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
