---
name: archivist-feature
description: Write the feature an article defines into docs/archivist/L1_features/. Use when the unit a user can name gets settled, or when something the user can name has no promise written for it.
---

# archivist-feature

Read `TEMPLATE.md` in this directory for the form. It is not copied here.

## What to read

The article, `docs/archivist/L2_*/`, and the units the project exposes to a user.

## The starting point is the article

**Do not build it as a summary of the specs and designs.** The decomposition into
features does not come out of L2. What comes out of L2 is not the answer to "what
can a user name" - that is an article about what the product exposes.

Treated as a summary, and because reduction travels upward, by the time L1 is
reached there is no moment left to question the decomposition. It merely ratifies
how the layers below were written.

## The unit

**What counts as one nameable unit is itself an article.** Read the unit out of
the article. Do not derive it from how the implementation happens to be divided.

Set the units the project exposes against the features.

| Difference | Meaning |
| --- | --- |
| More units | Nameable, but no promise written |
| More features | A promise with nothing behind it |

## Availability

What a user can do, as a bullet list. Do not step into requirements or design -
those belong to L2. Each item carries a number, `A1`, `A2`, ...

Background carries why it was needed.

## Coverage

Spec and design never cite each other, so this table is the only place they meet.
One row is one availability item; the spec column holds `R` numbers, the design
column holds `T` numbers, written bare. Which documents they live in is held by
References, which links each of them as a whole file.

| Blank | Meaning |
| --- | --- |
| No spec | Built without being promised |
| No design | Promised without being solved |

Both stop shipping. An `R` or a `T` that appears in no row is not a defect: an
article can act directly on a spec or a design, and the table demands nothing in
that direction. This is the point before implementation where a loose spec or a
loose design shows itself.

## One file per run

## Language

Write the prose in the language the project's existing documents use.
