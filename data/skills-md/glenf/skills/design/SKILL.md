---
name: design
description: >
  Settle the shape of one change before code: facts, open forks, two candidate
  shapes, decisions, acceptance criteria, and seams. Confirms the shape with
  the human before writing the spec, then stops for approval. Use when a change
  crosses a module boundary, has more than one plausible shape, needs a spec
  before slicing, or spans more than one session. Not for one-line or mechanical
  changes, task slicing, code, or long-lived system structure.
argument-hint: "[goal sentence | brief | spec path]"
---

# design

A change is cheap to reshape on paper and expensive to reshape in code. Settle
what the change is and where its state and behaviour live. Write the design
down for the human to confirm, then write the spec, and stop. Slicing and code
follow the approval, in another stage.

## Size it first

Skip design when the approach is obvious and the blast radius is local: a
one-line fix, a rename, a mechanical edit, a change inside one function.

Run it when any of these holds:

- the change crosses a module, package, or process boundary;
- more than one shape would plausibly work;
- someone will need to read the spec to review or resume the work;
- the change spans more than one session, agent, or person.

Unsure? Weigh the cost of designing against the cost of the wrong shape. A
ceremony on a local change is waste; improvising a boundary change is worse.

## 1. Read the inputs

Gather what already exists before forming an opinion:

- the goal sentence from `north-star`, and the brief from `find-the-core`;
- the triage path, and which stage handed this over;
- the code in the affected area, read rather than recalled;
- `GLOSSARY.md` and any ADR that binds the area;
- an existing spec, treated as a draft to revise.

Find where the project keeps specs before writing: `AGENTS.md`,
`CLAUDE.md`, or `CONTRIBUTING.md`; existing `docs/specs/` or `docs/plans/`;
then the git remote host. Nothing found means ask. Do not invent a location.

## 2. Gather the facts

Write the questions before reading, so the answers are not shaped by a fix you
already have in mind. Ask what the code does, who calls it, what data it holds,
what tests pin it, and what outside constraint binds it.

Answer with `file:line` evidence, and mark what you could not settle as a gap,
with what would close it. Propose nothing while gathering. Method and sources:
[`references/research.md`](references/research.md).

Done when every question has evidence or is a gap with an owner.

## 3. Split the open forks

Every fork gets one treatment. Misplacing it is how design stalls.

| Fork | Treatment |
|---|---|
| Judgment call | Ask the user: options, a recommendation, and why. |
| Empirical fork | `prototype`. Never a question to the user. |
| Settled by ADR, glossary, or earlier decision | Record it. Do not ask again. |
| Missing fact | Research it. Do not ask what the repo can answer. |

Ask judgment questions one at a time, in the order they block the shape. An
answer of "you decide" is a settled decision with an owner, not an open fork.

## 4. Sketch two shapes

Sketch two genuinely different shapes: types, signatures, and module
boundaries. Not two file layouts of the same design. Enough detail to see where
state lives and what a caller must know.

Pick the shape where:

- each piece of state has one owner;
- each task has one way to do it, so the implementer need not choose;
- callers need to know least;
- the legal states are the only ones the types can hold.

Record the rejected shape and the reason it lost. A shape rejected on evidence
is the stronger record; a shape rejected for taste is still a decision, so say
so. For a decision prose cannot carry, a prototype's output can go in the spec:
a state machine, a schema, a type shape. Nothing else from code.

## 5. Confirm the shape

Write the design down for review: a short message, or a design note in the
project's docs if it keeps them. It is not the spec. Keep it to a handful of
lines:

- the shape you chose, in one or two lines;
- what the change includes and what it leaves alone;
- the decisions and risks that could still change the shape;
- the shape obeys the project's rules, including any rule the change itself
  adds;
- the acceptance criteria, one line each.

A written design note starts at `Status: draft`. Mark it `approved` only when
the human confirms it. If the design is wrong, revise it and ask again. Do not
write the spec, a task, a tracker entry, or code until the human confirms. The
confirmation is the decision; the spec is only its record.

## 6. Write the spec

Only after the shape is confirmed, write the spec. Use
[`references/spec.md`](references/spec.md) for the template, a worked example,
and the standard each section is held to.

The spec carries, in order: current state and desired end state; decisions with
rejected options; acceptance criteria; seams; what is not being done; open
risks; research notes as an appendix.

- For a behaviour change, an acceptance criterion is observable from outside
  the code and false before the change. For a refactor, pair the pinned
  behaviour that must stay true with the structural change that is false
  before. Each names its proof on the real surface.
- A seam states what it catches and what it misses. A seam that catches
  everything is not a seam.
- No implementation paths or code snippets, except decision-rich prototype
  output. A `file:line` cite as evidence is not a path.
- No user-story padding, no restatement of the brief, no estimates.

Write the spec at `Status: draft`. Record the confirmed shape. If writing turns
up a new decision, stop and confirm it before adding it; do not settle it in the
spec.

## 7. Approve and stop

Present the spec and ask once whether it records the confirmed shape. This is a
read, not a second review; do not re-open settled decisions. If the spec changes
or adds to the shape, return to step 5.

On approval, set `Status: approved` and record the approver. Then stop: no
tasks, no code, no tracker. The next stage is `spec-and-tasks`. If the spec
fails in code it returns here, never sideways into implementation.

## Boundaries

`design` owns the behaviour and shape of one change. It does not own:

- **Order and proof per slice**: that is `spec-and-tasks`.
- **Long-lived structure** across the system, or ADRs: point to `architecture`.
- **Answers only code can give**: `prototype` settles them, then design
  resumes.
- **Intent the record holds**: read the record, and cite it in the spec. For a
  dedicated history pass, ask the user to run `why`.
- **Code, review, or fixes**: never in this stage.

If the change turns out to be mechanical while you read, say so and hand it
back. A smaller stage is not a failure of this one.
