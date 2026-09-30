---
name: coding-standards
description: Load this skill when writing or reviewing code - naming, structure, style, and diff discipline this project enforces. Load before any edit or code review.
user-invocable: true
---

# Coding Standards

Category: Rules (Governance)

## Purpose

Keep code consistent with the project's conventions and keep changes
reviewable. Repo convention outranks personal taste; the diff outranks the
file.

## Precedence

1. Explicit standards in this repo's `AGENTS.md` and linting config.
2. The existing style of the file and its neighbors (read before writing).
3. This skill's defaults, where the repo is silent.

## Diff discipline

- **Minimal diff.** Change only what the task requires. Reformatting or
  renaming beyond the task turns a reviewable change into an unreviewable
  one - if cleanup is warranted, propose it as a separate change.
- **Remove completely.** Deleted code is deleted: no `_unused` renames, no
  commented-out blocks, no wrapper shims "for safety". Every call site is
  updated in the same change.
- **No orphans.** No unused imports, no dead branches, no flag parameters
  nobody flips. If it has no effect, it is not in the diff.

## Code shape

- **Naming states intent**: what it does or holds, not how it is
  implemented (`activeUsers`, not `arr2`). Booleans read as assertions
  (`isValid`, not `flag`).
- **Functions do one thing** and return early; nesting beyond two levels
  usually means extraction.
- **Error handling lives at boundaries** (parse, I/O, entry points) - not
  sprinkled as try/catch that swallows. Errors are handled or propagated
  with context, never silenced.
- **Duplication rule:** two occurrences is fine, three gets extracted -
  only when the copies are actually the same concept, not just similar
  text.
- **Comments explain why; the code explains what.** A comment narrating the
  code is noise.

## Change hygiene

- Tests are updated in the same change as the behavior they cover.
- Commit messages: imperative subject line, body explains why when it is
  not obvious.
- Public API, config, or schema changes note their consumers.

## Review gate

Before submitting: the diff contains only task-relevant change, the file
still matches its neighborhood, tests moved with behavior, and nothing
dead or defensive remains.
