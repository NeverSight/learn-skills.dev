---
name: ux-vocabulary
version: 1.0.0
author: rawktron
license: MIT
description: >
  A shared UX vocabulary for precise conversational descriptions of interfaces.
  Use this skill whenever the user describes a UI, UX flow, interaction, or layout
  using words from the UX glossary -- such as morph, grow, yield, rail, selectable,
  overlay, skeleton, snappy, mark-and-undo, etc. Also trigger when the user is
  describing any interface behavior and you need to resolve ambiguity about what
  they mean. This skill defines ~40 words with exact meanings so the user can
  describe UX in plain English while remaining precise. When you see these words,
  do NOT interpret them loosely -- they have specific agreed-upon definitions.
---

# UX Vocabulary

## What This Is

A glossary of ~40 words with precise, unambiguous meanings for describing user
interfaces. The user writes in plain conversational English and reaches for these
words when precision matters. Everything else stays natural.

**Your job**: when you see a glossary word, treat it as a precise specification,
not a suggestion. "The card morphs into the editor" is not a vibe -- it means
the card element literally animates/reshapes into the editor view.

## How The User Writes

They write like this:

> I want a rail on the left with a selectable list of projects. The main area
> shows the active project. When you select a project, the list item grows into
> the main area and the old content yields. Going back shrinks it. Tasks and
> sessions stacked in the rail. Tasks feeds sessions. The whole thing should
> feel snappy and physical. Loading is skeleton.

Every italicized-style word above has an exact definition below. Non-glossary
words ("projects", "left", "active", "going back") are plain English and you
interpret normally.

## The Glossary

See `references/glossary.md` for the full glossary organized by question.
Read it before interpreting any UX description.

## Interpreting a Description

1. Identify all glossary words in the user's description
2. Map each to its exact definition -- do not soften or reinterpret
3. Everything NOT a glossary word is normal English -- use judgment
4. If the user uses a word that's close to a glossary term but not exact,
   ask which they mean. Don't assume.
5. If the description has gaps (e.g. they describe layout but not transitions),
   fill in sensible defaults but flag what you assumed

## When Something Is Ambiguous

If the user says something that conflicts or is unclear even with the glossary:
- Quote back the ambiguous part
- Offer 2 concrete interpretations using glossary terms
- Ask which they mean

Do NOT silently pick one.

## Defaults

When the user doesn't specify:
- Transitions: **replace** (instant, no animation)
- Loading: **skeleton**
- Destructive actions: **mark-and-undo(5s)**
- Vibe: **snappy**
- Persistence: things are visible when relevant, hidden when not (use judgment)

## Extending the Glossary

If the user defines a new term ("let's call X a ___"), add it to the working
vocabulary for the conversation. If they say "we need a word for ___", propose
one and confirm before using it.
