---
name: infrahub-teaching-concepts
description: >-
  Teaches Infrahub concepts (schema, objects, branches, proposed changes,
  checks, transforms, generators, menus) from wherever the learner is,
  using their own repo files and live instance as lesson material.
  TRIGGER when: the user wants to learn or understand an Infrahub concept,
  asks "teach me", "explain how X works in my instance", "I'm new to
  Infrahub", asks what the equivalent of a NetBox/Nautobot concept is in
  Infrahub, wants a guided tour, or wants to resume a learning session.
  DO NOT TRIGGER when: the user wants the work done for them (use the
  infrahub-managing-* skills), wants live operational answers (use
  infrahub-analyzing-data), or is debugging a failure (use
  infrahub-collecting-diagnostics).
argument-hint: "[concept-or-question]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Concept Tutor

## Overview

A tutor protocol, not a textbook. It measures what the learner already
knows, explains each concept through the learner's own schema, objects,
and instance where they exist, sets a hands-on exercise the learner solves
themselves, and records progress so a later session resumes instead of
restarting. Exercises are verified solvable before they are shown.

## When to Use

- "Teach me how relationships work" or any concept question asked to learn
  rather than to delegate.
- "Why does my instance behave this way?" when the goal is understanding.
- "What's the NetBox/Nautobot equivalent of X in Infrahub?" taught as a
  translation (see `rules/grounding-competitor-mapping.md`).
- "Where were we?" to resume from `.infrahub-learning/progress.md`.

## Environment Detection

Detect once per session, in this order, and prefer the richest source:

1. Repo files in the cwd (schema YAML, object files, `.infrahub.yml`):
   teach through the learner's own artifacts.
2. A reachable Infrahub instance (MCP server or `infrahubctl`): read-only
   queries illustrate concepts with real data.
3. Neither: use the generic examples in `references/concept-map.md`.

Before writing the first Explain section, read
[rules/grounding-own-artifacts.md](./rules/grounding-own-artifacts.md) —
a generic example when the learner has their own file is a violation,
not a fallback.

Instance safety has three tiers; the full ladder is in
[rules/safety-instance-writes.md](./rules/safety-instance-writes.md).
Read it before any command that could write, which includes the steps
you tell the learner to run. The short form: read-only by default,
author in local files, and write to the instance only after explicit
consent, only in a `learning-*` branch, never merged, always deleted.

## Workflow

1. On first contact, offer to create the learning workspace and read
   `references/lesson-protocol.md` for the exact file layout and lesson
   shape. On resume, read `.infrahub-learning/progress.md` first.
2. Pick the concept with `references/concept-map.md`: it orders concepts
   by prerequisite and carries per-concept probe questions, exercise
   specs, verification methods, and doc anchors. A topic with no row is
   taught off-map through the shared docs fallback
   ([rules/grounding-off-map-lookup.md](./rules/grounding-off-map-lookup.md)).
3. Before writing any lesson file, read
   [rules/protocol-structured-lessons.md](./rules/protocol-structured-lessons.md)
   — the Probe/Explain/Exercise/Check shape and its order are fixed.
4. Open with Probe, never with the explanation. Read
   [rules/protocol-probe-first.md](./rules/protocol-probe-first.md) for
   how many questions and what they have to establish.
5. Write Explain against the learner's own artifacts, and cite the docs
   page for every behavior claim:
   [rules/grounding-cite-docs.md](./rules/grounding-cite-docs.md). For a
   "what's the NetBox/Nautobot equivalent" lesson, the credibility gate
   is in
   [rules/grounding-competitor-mapping.md](./rules/grounding-competitor-mapping.md).
6. Before presenting the exercise, build and verify the reference
   solution per `references/exercise-verification.md` and
   [rules/exercise-verify-solution.md](./rules/exercise-verify-solution.md)
   — an exercise you have not solved yourself cannot ship. Assign the
   work; do not do it:
   [rules/exercise-learner-authors.md](./rules/exercise-learner-authors.md).
7. When the learner struggles, follow the hint ladder in
   [rules/exercise-hint-ladder.md](./rules/exercise-hint-ladder.md)
   before revealing anything, and log each rung to
   `.infrahub-learning/hints/<concept>.md` as you give it.
8. Record progress at the end of every lesson, before you reply:
   [rules/protocol-record-progress.md](./rules/protocol-record-progress.md).
9. Close each concept by naming the sibling skill that does this work on
   real projects:
   [rules/handoff-graduation.md](./rules/handoff-graduation.md).

## Rule Categories

| Priority | Category | Prefix | Description |
| -------- | -------- | ------ | ----------- |
| CRITICAL | Protocol | `protocol-` | Probe before teaching, the fixed lesson shape, progress recording |
| CRITICAL | Safety | `safety-` | Instance writes: opt-in, `learning-*` branch only, cleanup, never the default branch |
| HIGH | Exercise | `exercise-` | Verified reference solutions, learner-authored artifacts, the hint ladder |
| HIGH | Grounding | `grounding-` | Teach through the learner's own artifacts, cite docs for behavior claims, off-map lookup, sourced comparisons |
| MEDIUM | Handoff | `handoff-` | Graduation pointers to the sibling skills |

Full scope per prefix is in `rules/_sections.md`. Read the rules for the
lesson phase you are in; they are short and binding.

## Supporting References

- `references/lesson-protocol.md`: the workspace contract and lesson
  shape. This file is the single home for those values.
- `references/concept-map.md`: the curriculum.
- `references/exercise-verification.md`: how to prove an exercise is
  solvable before showing it.
- `../infrahub-common/`: shared GraphQL syntax and `.infrahub.yml` format.
