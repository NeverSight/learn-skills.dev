---
name: baselinedocs-maintain-split
description: Split one overloaded baseline pack into directly addressable domain packs with an initiative index. Use automatically when mixed workstreams or cross-domain dependencies reduce resume quality.
---

# Baseline Docs Maintain Split

## Purpose

Break one overloaded baseline into clearer bounded packs.

## Use When

- one pack covers too many unrelated tasks
- roadmap scope became too large
- multiple workstreams are mixed together and hard to resume

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Core Behavior

1. Identify natural split boundaries.
2. Group content by topic, feature, or workstream.
3. Produce smaller packs with clearer scope and ownership.
4. Create an initiative index containing direct links, status, and dependency edges.
5. Move shared reusable guidance to the wiki instead of a general wrapper pack.

## Primary Output

- multiple scoped baseline packs

## Non-Goals

- not for simple pruning or compaction alone
- not for hiding child packs behind a duplicated general pack
