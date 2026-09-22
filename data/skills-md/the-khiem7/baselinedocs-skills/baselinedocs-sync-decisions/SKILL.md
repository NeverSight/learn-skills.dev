---
name: baselinedocs-sync-decisions
description: Apply closed decisions to every baseline document they affect, from one targeted section to the whole pack. Use automatically when a resolved risk or business decision has not reached every affected document, including a single atomic decision update.
---

# Baseline Docs Sync Decisions

## Purpose

Apply already-closed decisions to the documents they affect, whether that is one section or the whole pack.

## Use When

- one or more hallucination risks were closed
- exactly one decision was just closed and only a narrow patch is needed
- decisions are recorded but not reflected elsewhere
- multiple baseline files still describe outdated options or uncertainty

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Core Behavior

1. Read the closed decisions.
2. Identify every affected baseline file and section, whether that is one section or many.
3. Propagate the chosen direction into the pack.
4. Patch only the sections the decision reaches. An agent that has just read the pack will see other things worth fixing; folding them into this pass makes the change impossible to review against the decision that motivated it.
5. Preserve decision history while removing active ambiguity.
6. Refresh `updated` and `code_ref` only in documents that changed, and only where implementation evidence was rechecked.

## Primary Output

- introduction, roadmap, sourcecode, and useguide aligned to the chosen decisions

## Non-Goals

- not for code drift syncing; `baselinedocs-sync-codebase` does that
