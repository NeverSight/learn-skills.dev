---
name: archivist-check
description: Read docs/archivist/ and judge whether the document set meets the shipping condition. Reports broken links, skipped layers, cycles, and documents whose realization does not yet exist. Writes nothing. Use after a reduction, or to see where things stand.
---

# archivist-check

**Writes nothing.** Reads only; changes neither content nor file names. Fixing is
the work of whoever writes the realization, and of whoever adds articles.

## Input

The articles under `docs/archivist/L4_articles/`, and the whole document tree.
The articles say what the documents above them are supposed to carry; without
them, only broken links can be found.

## What it judges

**Link resolution** — does the relative path exist. References run to a file;
nothing inside a file is judged. Anchors are nobody's to generate here, so a
hand-written one is neither required nor checked.

**Layer step** — a reference must land on one of:

- a node in the layer directly below
- a node in the same layer the graph gives a direction to (`structure --> terms`).
  `spec` and `design` are **not** such a pair: a reference either way is a violation
- a document inside the same node
- `L4_articles`, which any layer may cite directly

Anything else is a skip, and a violation.

**Cycles** — do references inside one node form a loop. A loop leaves no way to
tell which is the original.

**Realization against what exists** — the condition differs per layer. What is judged is the
existence of the thing the document names, never any output produced by running it.

| Layer | Becomes fact when |
| --- | --- |
| design | the files in the `target_file` column of Parts exist |
| spec | every item carries `Means:`, and declared file paths exist |
| feature | the spec and design its Coverage table cites are both fact |
| structure / terms / articles | always fact. Settled is all they need to be |

**Verification detail** — two judgements, one per L2 node.

- a spec item must be implementable as **debug** reading nothing but its spec.
  Raise items that presume the internal make-up
- a design item must be implementable as **test** reading nothing but its design.
  Raise items that cite a spec, or that only restate an outside promise

**Verification means** — does each item carry `Means:`. A file path must exist; a
`checklist` must be detailed enough to run on its own. Means in place is enough for
the document to be fact. Whether it passes is out of scope.

**Coverage** — the feature's table is the only place spec and design meet, so it is
the only place their disagreement is visible. Two defects, both of which stop
shipping.

- a row with an empty `spec` cell — built without being promised
- a row with an empty `design` cell — promised without being solved

An `R` in a spec, or a `T` in a design, that no row cites is not a defect. An
article can act directly on a spec or a design, and the table demands nothing in
that direction.

Report which of the two a defect is. It says whether the spec or the design is the
loose one, and it says so before implementation starts.

**Diagrams against reality** — every diagram carries prose saying what it is.
Set three against each other.

- Does the prose contradict what the diagram draws. Prose that supplements what
  a diagram cannot hold is fine; prose that states a rule the diagram omits is not
- Does what is drawn hold in the repository as it stands
- Where a label has the shape of a path or a name declared elsewhere, does it exist

A rule stated in prose but missing an edge in the diagram is the common failure,
and nothing else catches it.

**Exposed units against features** — where an article names what the project
exposes, set that set against `L1_features/` and raise what exists on one
side only.

## Report

One line per document whose realization is not yet there, saying what is missing.
A document nobody is waiting on is not listed.

## The shipping condition

The layers the topic touched are filled, and links run unbroken from the bottom up.
A layer left untouched is not a violation. **Not skipping layers and writing one
document per layer are different things.**
