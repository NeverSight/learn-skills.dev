---
name: documentation-pass
description: "Improves a repository's documentation for a named reader: finds missing, stale, duplicate, or hard-to-navigate guidance, fixes it using real files and commands, and verifies the links. Use when docs are missing or out of date, or before a release or handoff. Not a substitute for implementation, code review, or decisions."
---

# Documentation Pass

## Purpose
Make documentation usable by its intended reader without hidden context, and make sure every reference in it is true.

## When to use
- Use when: documentation is missing, stale, contradictory, or hard to navigate, or a release or onboarding needs it.
- Do not use when: the real gap is an undecided product or technical choice (record the open question; do not write around it), or the task is to implement or review code.

## Inputs
- Required: the existing documentation and the repository it describes.
- Optional: the intended reader, the workflow they need to complete, and known gaps.
- Assumptions: if the reader is unknown, state the one assumed and proceed; if the audience would change the result a lot, ask.

## Process
1. Name the reader and the task they are trying to do.
2. Audit the current docs against the repository: missing steps, wrong commands, stale paths, duplicated or conflicting guidance, and broken links.
3. Rewrite or add only what that reader needs, referring to real files, commands, and outputs. Remove duplicate and contradictory text.
4. Run the commands and follow the steps you document where you can. Mark any you could not run.
5. Check links, anchors, and formatting.

## Rules and heuristics
- Required: never invent product behavior, commands, or decisions. Where the facts are unknown, leave a clearly marked open question.
- Required: every file path and link must resolve.
- Recommended: put the first action the reader needs near the top, and link to canonical text instead of copying it.

## Checks
- The reader and task are stated.
- Links and paths resolve.
- Documented commands were run or marked not run.

## Output
Return: the updated documentation, a list of what changed and why, steps not verified, and remaining gaps.

## Completion criteria
- The named reader can complete the task from the docs alone.
- No statement in the docs is unverified without being marked as such.
