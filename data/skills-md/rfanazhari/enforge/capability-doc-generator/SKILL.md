---
name: capability-doc-generator
description: "Generate a business capability document (BR-XXX rules in Given/When/Then form) from a business context description, before any code exists. Use this whenever the user says 'capability doc', 'capability document', 'BR-XXX rules', 'business rules doc', or asks to turn a feature description, requirement, or business explanation into structured business-rule documentation for a service. Also use when the user describes a new module or a change to an existing flow and wants the business intent captured as a document — even if they don't say the word 'capability'. Trigger prefix: capability-doc:"
---

# Capability Doc Generator

Turn a business context description into a **draft capability document**: the business
rules of one capability, written as `BR-XXX-0NN` statements in Given/When/Then form, with
the business reason recorded for each.

## Why this exists

Rules can be reverse-engineered from code. The **reason** behind a rule cannot. Once a
feature ships, the "why" lives only in someone's memory and disappears when they leave the
team. This skill captures that reasoning while it is still fresh — before implementation,
when the business intent is being discussed.

The **Why** line under each rule is the highest-value part of the output. Never skip it,
never fill it with a restatement of the rule.

## Scope boundaries

This skill writes **one capability document at a time**, describing intended behaviour.

Do NOT do these, even if asked mid-task — offer them as separate follow-up work instead:

- Write or update a **journey document** (`UJ-00N`). Journeys reference capabilities, not
  the other way round — that is the `journey` skill's job. Point the user there (compose
  mode once the capabilities exist; discovery mode to find out which ones are needed).
- Write to a `policies/` folder. Output always goes to `capabilities/`.
- Claim the rules are implemented. See "Honest status" below.
- Write the implementation code.

## Honest status

The document describes what *should* be true, not what *is* true. Verifying rules against
real code is separate work with different evidence requirements. So:

| Field | Value | Reason |
|---|---|---|
| `status:` | `planned` | Nothing has been verified against code yet |
| `implementation:` | empty | This field means "the rule is proven to be enforced here" — an unverified guess must never be recorded as proof |
| `## Known gaps` | `Not yet implemented — verify against code after implementation.` | A gap is a mismatch between rules and code; with no verified code there is nothing to compare |

When the user names existing files as reference or as the likely target of change, record
them under `## Related` as a reference bullet — never in `implementation:`. Keeping guesses
out of the frontmatter is what makes the field trustworthy later.

## Input needed

Collect these before writing. Ask for whatever is missing rather than inventing it.

1. **Service** — which service owns this capability (`ciam`, `task`, ...). Determines the
   output folder and the `BR-` prefix.
2. **Capability name** — becomes the `id` (kebab-case) and the H1 title. If the user asks
   for a naming suggestion, offer 2–3 options derived from the business context and let
   them choose. Never silently invent one.
3. **Business context** — free-form: a written requirement, meeting notes, or a verbal
   explanation. Whatever form it takes, extract actors, triggers, rules, and reasons from it.
4. **Existing files** (optional) — reference code or the expected target of change.

If the business context is thin enough that the rules would be guesswork, say so and ask
for the missing part. A document full of invented rules is worse than no document.

## Step 1 — Locate the repo and the capabilities folder

Read `AGENTS.md` or `CLAUDE.md` at the repo root to learn the repo name and layout. The
layout differs between mono-repo and poly-repo, so derive the path rather than assuming:

```
<service-root>/docs/business/capabilities/<id>.md
```

If the folder does not exist yet, this is the service's first capability doc — say so, and
confirm the path with the user before writing.

## Step 2 — Determine rule numbering

Rule IDs use the pattern `BR-<SERVICE>-0NN`, where `<SERVICE>` is the service name in
uppercase (`ciam` → `BR-CIAM`). If the service name is long or hyphenated, propose an
abbreviation and confirm it.

Numbers are grouped in semantic blocks, not assigned sequentially. A real service looks
like this:

```
BR-TASK-001..006   BR-TASK-010..017   BR-TASK-020..023   BR-TASK-030..041
```

Each block covers a related area of behaviour. Which block a new capability belongs to is
a judgement about meaning, not arithmetic — so **do not guess**:

1. Scan every `.md` in the capabilities folder and collect the rule IDs in use.
2. Show the user the occupied blocks and what each appears to cover.
3. Ask whether to continue an existing block or open a new one.
4. Only then assign numbers.

Skip the scan only when the folder is empty — then propose starting at `001` and confirm.

## Step 3 — Write the document

Use this structure exactly. Keep every heading, in this order, even when a section is short.

```markdown
---
id: <kebab-case-capability-id>
service: <service>
status: planned
rules: BR-XXX-0NN..BR-XXX-0NN
updated: YYYY-MM-DD
implementation:
---

# <Capability Name>

## Purpose

Two or three sentences: what business outcome this capability delivers and for whom.

## Ubiquitous language

| Term | Meaning |
|---|---|
| **<Term>** | <Business definition — not a field description> |

## Actors and triggers

| Trigger | Actor | Effect |
|---|---|---|
| <event or action> | <user / scheduler / inbound event> | <what happens> |

## Rules

### BR-XXX-0NN — <Statement of the rule>

**Given** <precondition>
**When** <trigger>
**Then** <required outcome>

**Why:** <the business reason — the part not recoverable from the code>

## Edge cases

| Situation | Expected behaviour | Rule |
|---|---|---|
| <situation> | <behaviour> | `BR-XXX-0NN` |

## Examples

| Input | Expected outcome |
|---|---|
| <concrete values> | <concrete result> |

## Known gaps

Not yet implemented — verify against code after implementation.

## Open questions

<Unresolved product decisions, each with who needs to decide. "None." if there are none.>

## Related

- Existing flow reference: `<path>` — <why it is relevant>
- Sibling capabilities: [`<name>`](./<name>.md)
- Source document: <original requirement or design doc, if any>
```

### Section notes

**Purpose** — state the business outcome, not the mechanism. "Decides who may read the
member directory" is useful; "Handles the GET /members endpoint" is not.

**Ubiquitous language** — only terms this capability introduces. Terms already defined in
the service overview or the global glossary belong there, so link instead of redefining.
When unsure whether a term is already defined elsewhere, leave it out and note it as an
open question — a duplicated definition that later drifts out of sync is worse than a
missing one.

**Rules** — one rule per distinct decision. If a rule's Then clause contains "and also",
it is probably two rules. Write **Why** as the business consequence of not having the rule,
which is what makes it impossible to recover from reading code later.

**Edge cases** — the situations someone would get wrong when implementing. Every row cites
a rule; if a row has no rule to cite, either a rule is missing or the row is noise.

**Examples** — concrete values, not placeholders. These become test cases.

**Open questions** — genuinely useful here. Gaps in the business context surface as
questions rather than as invented rules. Name who decides.

## Step 4 — Report back

After writing the file, tell the user:

- Where it was written
- Which rule IDs were assigned, and which block they went into
- Which sections need human input — typically Open questions, and anything derived from
  thin context
- That `status`, `implementation:` and Known gaps stay unfilled until the rules are
  verified against real code
