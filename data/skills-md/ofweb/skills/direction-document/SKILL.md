---
name: direction-document
description: Create or revise the main Direction document and optional topic documents when the project's intended end state changes.
---

# Direction document

The Direction documents hold the project's current intended end state. The main
document synthesizes every topic. Optional topic documents hold detail for a
coherent part of that destination. They are authoritative about the destination,
not accepted feature behaviour or implementation.

Direction maintains `.workflow/direction.md` and optional files at
`.workflow/direction/<topic>.md` with the user. Use a short, stable, lowercase
hyphenated topic filename. Shape may read these files but must not silently
redefine them. Before creating a file, check for the same material elsewhere.
Do not create a duplicate or migrate an existing document in this skill. Ask
for a separate migration.

## Content

Use this structure for the main document, with topic sections and links where
useful:

```markdown
# Direction

## Goal

## Intended end state

### Topic name

Current summary of this topic. Link to its topic document when one exists.

## Boundaries and tensions

## Open questions
```

State the overall goal, the mature user or system experience, long-term
capabilities, and shared boundaries. Keep Goal and Intended end state in the
main document. Represent every current topic in its Intended end state section,
including topics with their own file. Omit Boundaries and tensions or Open
questions when empty. State unresolved end-state questions and tensions
precisely. Link PDRs, References entries, or research needed to understand a
statement.

Create a topic document when a coherent topic needs more room or is clearer on
its own. Give it a clear title and a link back to the main document. State its
detailed intended end state, topic boundaries, tensions, and open questions.
Omit sections that add no value. Link the topic document from its current
summary in the main document. The topic document owns detailed claims; the
main document owns the project-wide synthesis. Do not copy detailed claims
between them.

Do not add a Backlog, roadmap, delivery order, progress report, feature
requirements, architecture, task list, or completed-work catalogue. Keep
transient ideas in discussion until the user adopts them as Direction. Put
agreed future features in the Backlog and durable product reasoning
in a PDR.

## Maintenance

Create the main document when the project first agrees on an intended end
state. Revise the affected documents when that understanding materially changes
or an important unresolved end-state question needs to remain visible. A small
wording improvement or feature completion alone does not require a revision.
Rewrite sections as current understanding, not a chronological record. Remove
superseded wording. Keep a
genuine unresolved question visible without weakening settled statements.

After any main or topic edit, check the other affected documents. Update the
main summary and links when topic detail changes. Rebalance material when
topic boundaries change. Remove obsolete topic files and stale links after
their current material has a canonical home. Keep topic filenames stable when
titles change. Git preserves earlier states.

Keep all Direction documents concise without a normal word target. The main
document has a 4,000-word hard limit. Each topic document has a 2,000-word hard
limit. Near a limit, first remove resolved questions, superseded direction,
feature detail, copied PDR rationale, and research detail. Rebalance topic
material when that improves the document set. Link to canonical material and
compress wording without losing meaning. Do not use these files as a history
log.

Link related Backlog items, PDRs, Context terms, References, or research when
those links help a fresh reader. Keep one canonical home for each conclusion.
A Backlog item or Feature Brief may link directly to the relevant topic document.

Invoke `concise-prose` before writing or revising Direction. Follow its STE100
and Vale repair loop until `prose-check` passes. Install
`workflow-document-check` alongside this skill and use it after the edit.
Treat a hard-limit failure as a reason to prune or rebalance. Before finishing,
check that the main document represents every topic and orients a fresh context
without delivery detail. Check that each topic file agrees with its main
summary and that links work.
