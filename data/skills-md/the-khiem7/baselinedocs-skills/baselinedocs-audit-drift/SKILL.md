---
name: baselinedocs-audit-drift
description: Audit which baseline documents have fallen behind the code or behind a closed decision, ranking the code half by `code_ref` frontmatter provenance, and report without modifying files. Use automatically when staleness or alignment between docs, code, and decisions is uncertain. For whether an individual statement is supported by evidence, use `baselinedocs-audit-claims` instead.
---

# Baseline Docs Audit Drift

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Purpose

Report where baseline truth drift exists.

## Use When

- the user wants an audit before syncing
- the team wants to know what is stale first
- trust in alignment between code and docs is uncertain

## Core Behavior

1. Read `status`, `updated`, and `code_ref` frontmatter to prioritize likely stale documents.
2. Compare scoped code changes after `code_ref`, document claims, and decision records.
3. Identify mismatch categories.
4. Report affected files and likely impact.
5. Recommend follow-up actions, naming the repair skill for each finding: `baselinedocs-sync-codebase` for code drift, `baselinedocs-sync-decisions` for a closed decision that has not reached the pack, `baselinedocs-sync-reconcile` for documents contradicting each other.

Treat a newer commit as a drift signal, not automatic proof that every document is stale.

A closed decision has no provenance field, so decision drift is found by comparing `hallucination` against what the other documents still assert, never by ranking. Ranking would silence it: a document whose `code_ref` is current still describes an option a decision rejected, and that document sorts to the bottom of a provenance-ordered list.

## Primary Output

- drift report

## Non-Goals

- audit-first, not auto-fix-first
- not a claim-level evidence check; `baselinedocs-audit-claims` does that
