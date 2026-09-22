---
name: baselinedocs-sync-reconcile
description: Reconcile contradictions inside an existing adaptive baseline pack. Use automatically when core or conditional documents disagree about current truth or status.
---

# Baseline Docs Sync Reconcile

## Purpose

Restore one canonical truth across the baseline pack.

## Use When

- baseline files contradict each other
- one file says implemented while another still says planned
- the pack has internal truth drift even before checking the codebase

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Core Behavior

1. Compare files inside the pack.
2. Detect contradictions.
3. Prefer code evidence and explicit user decisions.
4. Rewrite conflicting sections to converge on one truth.
5. Use frontmatter as routing metadata, but verify body claims before changing status.

## Primary Output

- a consistent baseline pack

## Non-Goals

- not for creating a new pack
- not for code-first syncing after implementation changes; `baselinedocs-sync-codebase` does that
