---
name: unslop
description: Rewrite text so it reads like a person wrote it, not a template.
disable-model-invocation: true
license: MIT
compatibility: "No external tools required."
---

# Unslop

Rewrite the requested text so the reader can understand it on the first pass. Preserve the author's meaning and tone. Change wording only unless structural edits are in scope.

Edit the supplied files when asked to edit files. For pasted text, return the rewrite directly. Complete the edit instead of handing back a list of writing problems.

## Make each sentence useful

- Replace vague praise with what something does. Cut sentences that add no fact, instruction, or necessary context.
- Remove filler, repeated conclusions, flattery, and support-chat endings.
- Replace anonymous authority such as "experts believe" with an existing source, or flag the unsupported claim. Never invent evidence.
- Preserve qualifications that affect the meaning. Shorter wording must not turn an estimate into a fact.

## Use plain language

- Prefer "use" to "utilize" or "leverage", and "is" to "serves as".
- Replace abstract metaphors and stock phrases with the actual thing or action.
- State the point directly. Avoid "not just X, but Y", forced groups of three, and multiple synonyms for the same thing.
- Name the actor when it matters. Split sentences that require a second reading.
- Keep complete sentences. Do not compress prose into fragments, arrows, or unexplained abbreviations.

## Keep formatting quiet

Use sentence case headings and only enough structure to help the reader. Remove decorative emoji, excessive bold, and labels that repeat their own explanation. Use periods or commas instead of dashes joining clauses.

Read the result once more for meaning and flow. Preserve commands, paths, numbers, citations, and direct quotes. Leave license text unchanged. If a factual problem needs work beyond the edit, name it briefly without pretending it was resolved.
