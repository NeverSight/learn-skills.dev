---
name: writing-changelogs
description: Use when writing a changelog entry, release notes, or a "what shipped" summary after completing work. Encodes the entry shape, the handover template, and the honesty conventions. Use after shipping meaningful work, even if the user just says "summarize what we did".
---

# Writing changelogs

**REQUIRED BACKGROUND:** the `technical-writing` skill (hard rules, truth rules, style).

## Overview

The changelog's subject is the change, not the current state; migration docs and release notes are the other document types with that subject. It is historical: entries are never rewritten, only appended.

## When to invoke, and not

Invoke after shipping a meaningful change (a feature, a fix of real size, a removal), when writing release notes, or when summarizing what shipped. Do NOT invoke for trivial edits (roughly three changed files, or three commits), and never rewrite or delete existing entries.

## Rules

- One entry per shipped change, newest first, ISO dates, grouped by version where versions exist.
- Standard categories where the file uses them: Added / Changed / Deprecated / Fixed / Removed / Security. A Deprecated entry carries the removal date and the replacement.
- **Breaking changes lead the entry**, above the categories, each with the required migration action stated (and the migration guide linked when one exists).
- User-visible impact over implementation detail.
- Present tense, active voice, and no jargon the reader would not know.
- Group related changes, and never duplicate an existing entry.
- Record removals, not just additions.
- Release notes are the audience-facing cut of the same facts: what changed, who it affects, what to do about it. The changelog speaks to engineers; release notes to users of the system. Both draw on the same sources and must never contradict each other.

## Entry shape

**Document-type exception:** the bold leads required below override the shared ban on bold-lead bullets. The exception covers changelog outcomes and the named known-issue, deferred-item, and omission categories only. Repeated label-value bullets remain banned elsewhere.

**Bold lead stating the outcome**, then root cause, then the fix, with exact names inline:

```markdown
- **Reference-to-video routing fixed.** The resolver only knew three operation
  kinds, so requests with reference media routed to image-to-video. A
  `hasReferenceMedia()` check now gives reference-to-video a higher-priority
  branch.
```

Fixed entries explain the failure mode, not the diff. The bold lead carries the user impact, which lets a reader triage a change list.

## Honesty conventions

Three entry types make a changelog citable:

- **Known issues** surfaced but not fixed in this change, named as such.
- **Deferred items** still owed ("one deploy needed to restore the webhook key").
- **Deliberate omissions**, described by category, so the same omission is not re-litigated or mistaken for an oversight.

Never mark anything implemented, deployed, or verified unless that exact action was completed and checked. Distinguish implemented (in the repo) from deployed (live) from externally verified.

## Handover / completion summary

For handing finished work to a reviewer or operator, cover these sections in order:

1. Why this work exists
2. What shipped
3. Where to point the review (the decisions a reviewer must understand before judging)
4. Verification status: exact commands and their results, never a bare checkmark
5. Honest caveats and things I got wrong
6. Residual risks and what NOT to do
7. State and what is owed (merged-not-pushed, migrations, ordered steps with the consequence of wrong ordering)
