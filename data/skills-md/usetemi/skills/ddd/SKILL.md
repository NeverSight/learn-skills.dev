---
name: ddd
description: >-
  Write, revise, or consolidate DOMAIN.md, a repository's domain model, by
  interviewing the user as the domain expert. Use to create DOMAIN.md, to model
  a domain with domain-driven design (ubiquitous language, entities, value
  objects, domain services, aggregates, domain events, rules and invariants),
  when a task introduces a term, rule, or concept absent from DOMAIN.md, when
  code and DOMAIN.md disagree, or to remove inconsistencies and redundancies
  from an existing DOMAIN.md. Produces the document only; it does not implement
  or refactor code.
---

# Domain-Driven Design

Agents already know domain-driven design. What they lack is the domain: the
terms, rules, and boundaries of this business. `DOMAIN.md` supplies that. It
records the ubiquitous language, the model, and the rules and invariants, so
every later task starts from the same model instead of re-deriving one from
code.

This skill writes and maintains `DOMAIN.md` at the repository root. Treat the
user as the domain expert: extract rules through concrete scenarios and write
down only what they confirm. The skill does not change code. Bringing the
implementation in line with the model is separate work that reads `DOMAIN.md`.

[`references/domain-driven-design.md`](references/domain-driven-design.md) is
this skill's definition of domain-driven design. Read it:

- before the first interview in a repository, for the interview technique and
  the modeling concepts
- when mapping evidence from an existing system to concepts; its "Bring Key
  Concepts Into Light" and "Review an Existing System" sections say what to
  look for
- during a consolidation pass, for what makes a term or boundary precise

The reference says to keep the model and the implementation aligned. That
alignment is the goal; a lag is the expected state. This skill keeps the model
explicit and current, and closing the gap is code work outside it.

## Operating Contract

- Never invent domain rules. Ask the user when behavior, terminology,
  invariants, or exceptions are unclear.
- Write only confirmed content. An assumption the user approves is a rule;
  write it as one. Open questions stay in the conversation, never in
  `DOMAIN.md`.
- `DOMAIN.md` describes the goal state: how the software is supposed to work.
  The implementation may lag it. Never rewrite the document to match the code
  without asking. When code and document disagree, ask whether the model was
  incomplete or the code drifted.
- Edit `DOMAIN.md` only. Do not edit implementation files, tests, or schemas.
- Prefer entities, value objects, domain services, aggregates, factories,
  repositories, and domain events when they clarify the model. Do not force a
  pattern without a concrete domain responsibility.
- Do not require classes, inheritance, mutable objects, or object-oriented
  programming. The model is independent of programming paradigm.
- Do not introduce or recommend bounded contexts. Keep this skill focused on
  domain knowledge, explicit models, consistency boundaries, and evolution.

## Workflow

### 1. Establish The Evidence

Read `DOMAIN.md` first when it exists. For an existing system, also inspect the
relevant code, tests, schemas, interfaces, documentation, and recent changes
before interviewing the user. This step is read-only. Identify:

- current domain terms and competing synonyms
- behavior and rules embedded in conditionals or orchestration
- identities, values, state transitions, and consistency boundaries
- duplicated or scattered domain logic
- concepts present in the code but absent from `DOMAIN.md`, and the reverse

Evidence produces questions, not rules. Code shows what is implemented, not
what is intended.

For a new system, begin with the user's stated problem, actors, desired
outcomes, and representative scenarios. Do not design from nouns or storage
structures alone.

Do not stop after announcing that inspection or an interview is needed. Inspect
available artifacts in the current turn. If no relevant artifacts are available,
start the domain interview immediately.

### 2. Interview The Domain Expert

Use the available interactive question tool. If none is available, ask concise
questions in prose. Ask no more than three or four questions per round and run
additional rounds until material ambiguity is resolved.

Ground questions in concrete cases:

1. Ask what happens in a representative scenario from beginning to end.
2. Clarify the terms the user uses for actors, concepts, actions, and outcomes.
3. Ask what must always be true before and after meaningful operations.
4. Probe exceptions, rejected actions, state transitions, and competing cases.
5. Test the emerging model with counterexamples and boundary cases.

Do not ask the user to choose technical patterns. Ask domain questions, then map
the answers to modeling tools. When an answer exposes a contradiction or a term
with multiple meanings, continue the interview instead of resolving it silently.

### 3. Write DOMAIN.md

The file is the proposal. Draft or edit `DOMAIN.md`, then have the user review
the change and correct it. Iterate until they confirm. Revise an existing file
in place: change the affected terms and rules where they live instead of
appending a new section or a changelog.

Open the document with a short statement of what it is: the source of truth for
the ubiquitous language, domain rules, and how the software is supposed to work;
a living goal-state document that implementation may lag.

A useful outline, to adapt rather than fill in:

1. **Ubiquitous language**: each term and its precise meaning
2. **Model**: entities and aggregates, domain services, domain events
3. **Rules and invariants**: what must always hold, grouped by topic
4. **Lifecycles and processes**: states, transitions, and sequences

Include only what the domain needs. Omit a section or pattern that has no
concrete domain responsibility instead of adding placeholders.

Writing rules:

- One term, one meaning. Pick one name per concept and use it everywhere. Give
  each overloaded word's distinct meanings their own names.
- State each rule once, in the one place that owns it. Elsewhere, refer to that
  place instead of restating the rule.
- Define terms by behavior: what the concept does, permits, and forbids, and
  how it differs from its neighbors. A synonym is not a definition.
- State rules in domain language, not in database tables, columns, endpoints,
  or classes.
- Keep current-state content out: no implementation notes, migration status,
  TODOs, open questions, or "not yet built" caveats. Report gaps between code
  and model to the user in the conversation.
- When two neighboring terms are easily confused, say how they differ.

### 4. Make It Load

`DOMAIN.md` only guides agents that read it. If the repository's agent
instructions (`AGENTS.md`, `CLAUDE.md`, or equivalent) do not already load it,
suggest that the user add:

- a reference that loads `DOMAIN.md` for every task
- a rule to use its language, follow its rules as written, and revise
  `DOMAIN.md` first before introducing a concept, workflow, or policy absent
  from it

Suggest the change; do not edit agent instructions unasked.

## Consolidate

An actively revised `DOMAIN.md` accumulates redundancy and contradiction. On
request, or when the evidence step finds them, remove self-contained
inconsistencies and redundancies. The two are handled differently:

- **Redundancy**: the same rule or definition stated in more than one place.
  Merge it into the one owning place and make the others refer to it. The
  meaning must not change.
- **Inconsistency**: two statements that disagree, or one term used with two
  meanings. Do not pick a side. Show the user both statements and ask which is
  authoritative, then write the answer in the owning place.

Read the whole document before editing. Finish by reporting what was merged and
which conflicts the user decided.

## Revisit

Treat the confirmed model as current, not final. Revisit `DOMAIN.md` when
business behavior changes, when a task needs a concept the document lacks, or
when recurring confusion shows the language is not working:

1. Re-interview the user with concrete changed scenarios.
2. Revise the affected terms, model, and rules in place.
3. Remove concepts and terms that no longer belong to the model.
4. Have the user confirm the revision.

Model evolution is expected. Do not protect an obsolete model merely because it
matches the current implementation, and do not retreat from a confirmed model
merely because the implementation has not caught up.
