---
name: research-and-vault
description: >-
  Chain web research, atomic extraction, and durable note capture when the same
  research-to-notes sequence must repeat. Do not use this skill to design or evaluate an
  investigation; use `research-methodology` for research questions, methods, and evidence
  assessment.
---

# Research and Vault

## Quick Start

Load this skill when the task requires the full research-to-note sequence.

Use this thin orchestrator when a task needs the same sequence repeatedly:

1. Research the target with the available web-research skill.
2. Capture source URLs and dates before interpretation.
3. Extract independent atomic claims before synthesis.
4. Write the durable note only after the source coverage and gaps are explicit.
5. Report the output path and unresolved gaps.

This skill composes existing capabilities; it does not duplicate their methodology. If the task is a single lookup or a single note, load the domain skill directly instead.

## When not to use

Do not use this skill for a one-off lookup or a single note — load the domain skill directly instead. It only adds value when the same research-to-notes sequence repeats and needs to be captured durably.
