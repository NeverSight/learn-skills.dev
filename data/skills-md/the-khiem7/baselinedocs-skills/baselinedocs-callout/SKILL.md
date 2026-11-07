---
name: baselinedocs-callout
description: Create, update, or retire a temporary callout group inside an existing baseline pack - a named routing table that maps short group labels onto the pack elements they point at, so a later thread can name a slice of work in two words instead of restating it. Use explicitly when the user wants a shorthand to call out part of a pack in a new conversation, or when an existing callout group has met its stated deletion condition.
version: "3.3.0"
---

# Baseline Docs Callout

Point at a slice of the pack by name, and store nothing while doing it.

`<core-dir>` is the folder `baseline-core`, a sibling of the folder this SKILL.md sits in (`<skill-dir>/../baseline-core`). When it is not there, stop and tell the user to install `baseline-core`; never write or report on a pack from memory instead.

Read `<core-dir>/references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `<core-dir>/references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

Run `sh <core-dir>/scripts/packtool.sh check <pack-dir>` after every pack write and before reporting it, and allocate every new identifier with `sh <core-dir>/scripts/packtool.sh next-id <pack-dir> <D|Q|P> [PREFIX]`, never from memory. A new pack's first identifier needs its PREFIX. Never report a write as done while `check` prints a FAIL line: a duplicate identifier or a missing index row resolves citations to the wrong entry, and nothing else detects it. Without `sh`, say the checks were not run.

## What a callout group is

A named table of short labels, each pointing at pack elements that already exist. It stores nothing: every row is an address, and the thing at that address is the only source. Read it to decide what to open, never as the answer. It expires.

It exists because a long thread produces a set of questions or workstreams the user wants to raise again days later, and naming them costs a paragraph every time. One table turns that paragraph into two words.

## Preconditions

Refuse and route, rather than proceeding, when any of these holds.

1. No pack exists at the baseline root. A callout group over nothing is a table of dead links; `baselinedocs-init` creates a pack and `baselinedocs-adopt` converts an existing document into one.
2. An element the group would point at is not written yet. A callout group never creates pack content and never records a fact of its own; `baselinedocs-save` captures what the thread established, and the group is built afterwards.
3. The user has not said what ends the group. Ask for it. A group with no deletion condition is permanent, and a permanent routing table is a second index nobody maintains.
4. The proposed labels collide with identifiers the pack already uses for decisions, questions, phases, or risks. Choose others.

## Workflow

1. Read the pack's `introduction`, and read every element the group will point at. A row written from memory of a conversation is the failure this skill exists to prevent.
2. Verify each identifier resolves to a real heading or phase in the pack. Report any that does not and stop; do not write a row you could not resolve.
3. Agree the group name with the user. It is what they will type in a later thread, so it is theirs to choose, two to four words, no identifier prefix.
4. Agree the labels. One letter or one short tag per group member.
5. Agree the deletion condition, and make it objectively checkable by a reader who was not in this conversation.
6. Write the section, using the shape below.
7. Report the group name, its labels, and its deletion condition back to the user, so what they type later is something they have seen.

## Placement

- Single pack: a `## Callout Group: <Name>` section in `introduction`, above `## Scope`.
- Multi-pack initiative: the same section in `<initiative>/<initiative>.index.md`, which is already routing metadata.

The section goes above `## Scope` because the group's only job is to be found before anything else is read, and a reader who has already reached `Current Truth` did not need it.

Never create a new file for a callout group, and never add a document type for one. The pack contract defines the document set, and a seventh file ships to nobody: it would be invisible to every skill that reads the pack by role.

## Section shape

Four parts, in this order, and none is optional.

1. The word `Temporary`, then one sentence stating the group is a routing aid and not a source.
2. The deletion condition, stated as a condition a reader can evaluate.
3. The date it was opened and one sentence on what the labels are scoped to.
4. The table: label, what it covers, where it lives. Three columns. Values that need a path, a digest, a full sentence, or a quotation go in bullets under the table, never inside a cell.

## Behaviour rules

- A row is a locator, not a source. It states what an element is about and nothing more: never the reasoning, never the outcome, never a summary a reader could act on. A row carrying reasoning is a second copy of the element, and the two drift with nothing to compare them against.
- An answer that turns on a row whose element was not read is unbacked. Say so and offer to read the element. This is the rule the agent most wants to break, because a row usually looks like enough.
- Labels are scoped to the group and the section says so. A letter here is not a pack identifier and never becomes one, so a later reader cannot mistake `B` in a callout group for a decision or a phase.
- One label, one subject. A label covering two unrelated things is two labels.
- Every row points at something that exists. Nothing is written into a pack to give a row a destination.
- The group holds no status. Phase status lives in `roadmap`, and a status duplicated here goes stale the first time the phase moves.
- Record the reasoning behind the group nowhere. A routing table has no reasoning to record, and an entry in `hallucination` explaining why a shorthand was chosen is the edit commentary the contract forbids.
- Content that turns out to need a home, rather than a pointer, belongs in the document whose role covers it. Route it to `baselinedocs-save` rather than widening a row to hold it.

## Updating a group

- Rows change when the elements they point at change identity, not when those elements change content. A row that reads correctly after an element was rewritten is still correct.
- A label whose subject is settled is removed from the table in the same edit that settles it, not kept with a note. The settled material is already in the pack and a row is not where it is read.
- A group that has lost every label but one is a group that has ended. Retire it.

## Retiring a group

1. Evaluate the stated deletion condition against the pack, not against the conversation.
2. Confirm every element the group pointed at is still reachable by its own identifier without the table.
3. Delete the section. It is routing metadata and carries no fact, so nothing is relocated and the disproven-claims rule does not reach it.
4. Say which condition was met and which section was removed.

Deleting a callout group is not deleting a pack claim. The distinction matters because this is the only delete in the family that is not a relocation, and an agent that generalizes from it will start pruning content that must be kept.

## Non-Goals

- not a pack update; `baselinedocs-save` captures what the thread established, and this skill points at it afterwards
- not an entry index; the `hallucination` index covers every entry permanently, and `<core-dir>/references/pack-contract.md` defines it
- not a multi-pack index; `baselinedocs-init` creates that, and `baselinedocs-maintain-split` creates one when a pack divides
- not a brief; `baselinedocs-brief` reports where work stands, and a callout group reports nothing
- not a summary of the pack, and not a place to read one
