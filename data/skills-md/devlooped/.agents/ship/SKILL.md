---
name: ship
description: Rebase this session's work onto the default branch, commit to a dev/ branch, open a labeled PR, enable rebase auto-merge, babysit it, and land the merge locally.
disable-model-invocation: true
argument-hint: optional label
---

# /ship

Ship this session's changes as a labeled PR. Partition pending work into logical groups; with more than one group, print a sequence of ships and wait for a selector.

1. Read `procedure.md`.
2. Extra text after `/ship` is an optional label, then a group selector (`all`, index, slug) or title/slug hint. Label names come from `.github/.labels`, refreshed at most every 30 days.
