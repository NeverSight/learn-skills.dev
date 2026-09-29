---
name: context-document
description: Record agreed project-specific concepts in .workflow/context.md. Use when a collaborative workflow resolves terminology that must remain stable across features or fresh contexts.
---

# Context document

Context records the project's agreed language. It is authoritative for the
meaning of defined terms, not for project direction, feature behaviour, or
architecture. A code or document scan can suggest terms; it cannot authorize
an entry. The collaborative workflow and user establish the canonical meaning.
This skill records it.

## Check the language

Read `.workflow/context.md` first when it exists. Scan material that uses the
candidate term. Find competing names for one concept or one name used for
different concepts. Return unresolved ambiguity to the owning workflow.
Do not choose a canonical term or meaning silently.

Add an entry only when the concept is project-specific and needs one stable
meaning across features, documents, code, or fresh contexts. The definition
must resolve competing names, prevent meaning drift, or separate concepts that
readers could confuse. A named feature part, state, or action does not qualify
only because a document describes it. Keep its behavior in the Feature Brief
or decision record unless its name also meets the vocabulary test. Reject
ordinary programming and framework vocabulary. Do not add a term only to
satisfy an STE or prose check. Create `.workflow/context.md` when the first
term qualifies.
Put legitimate domain words without a project-specific meaning in
`.workflow/ste-glossary.json` when STE100 does not approve them.
If a copy exists elsewhere, do not create a duplicate or migrate it here.
Keep only terms whose canonical meaning the user has agreed. Leave candidate
terms in the owning workflow until that agreement exists.

## Record the agreement

Use one short entry per concept:

```markdown
# Context

## Signal

- Meaning: A Signal is a project event that starts a review.
- STE class: Technical name
- Forms: <comma-separated approved forms, when needed>
- Avoid: Misleading synonyms, when needed.
- Distinguish from: Related concept and its difference, when needed.
```

The heading gives the canonical spelling. `STE class` is document-skill-derived
metadata consumed by `prose-check`; it is not a user decision. Context defines
vocabulary. Each `Meaning:` must use one or two normal STE100 description
sentences with a subject and a complete statement. Name the term in the
sentence. The heading and `STE class` do not replace words in it. Keep
meaningful distinctions and approved forms explicit. The user agrees spelling,
meaning, distinctions, misleading synonyms, and semantically important forms
through the owning workflow. Derive the STE class from that agreed meaning and
usage. Use `Technical name` for a concept used as a noun. Use `Technical verb`
for a named action. Do not ask the user to classify the term. List approved
forms as comma-separated spellings. Omit optional fields with no value. Link
related entries or records when a definition depends on them.

Revise a definition when the user changes the agreed meaning. Check affected
uses in project documents and code. Route a behavioural change to a PDR or
Feature Brief, and an architectural change to an ADR; do not hide either in
Context. Remove obsolete entries, duplicate terms, stale links, and repeated
explanations. Git preserves earlier definitions. Do not add conversation
history or generic project documentation.

Aim for 20–50 words per concept. The hard limit is 80 words per concept and
1,500 words for the whole file. Near a limit, look for terms that no longer
need a project-specific definition, duplicate concepts, distinctions that can
be simpler, and implementation vocabulary. Do not split Context just to meet
the limit; growth may mean it has become general project memory.

Invoke `concise-prose` before writing or revising Context. Follow its STE100 and
Vale repair loop until `prose-check` passes. `prose-check` derives its
project vocabulary from agreed Context entries. `workflow-document-check` must
be installed alongside this skill; use it after the edit. Prune or restructure
after a hard-limit failure. Check each
entry for user-agreed meaning and unresolved ambiguity.
