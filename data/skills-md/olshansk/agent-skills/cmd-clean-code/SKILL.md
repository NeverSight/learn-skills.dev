---
name: cmd-clean-code
description: Improve code readability without altering functionality using idiomatic best practices
disable-model-invocation: true
---

# Clean Code

Use these rules to improve code readability without altering functionality unless explicitly requested.

## Core Principles

- Minimize cognitive load for human readers and agents.
- Apply idiomatic best practices where they fit.
- Preserve all business logic unless told otherwise.
- Clarify comments and structure with bullet points where possible.

## Accepted Inputs

- Full source files (`.proto`, `.go`, `.py`, `.md`, etc.).
- Partial comments: package headers, method docs, inline notes.
- Whole or partial functions.
- Arbitrary code snippets (or any mix of the above).

## Response Requirements

- Return the cleaned code wrapped in triple back-ticks.
- Keep all identifiers (fields, params, classes, methods, etc.).
- Add strategic whitespace for readability.
- Convert paragraph-style comments into bullet points when feasible.
- Do **not** delete or change original content unless asked.
- Favor bullet lists whenever information is list-like.

## Team-Specific Edge Cases

- Leave `TODO_???(???)` tags untouched.
- Preserve callouts like `IMPORTANT`, `DEV_NOTE`, etc.
- Maintain references to GitHub issues/PRs (e.g. "As of #XX ...").
- Keep every link and external reference.
- Retain markers such as `CRITICAL`, `NB`, `DEV_NOTE`, `NOTE`; just clean up the following text.

### Handling Long Snippets

- For grouped code (~5 lines) followed by a blank line, add a brief comment atop the block.
- Keep existing comment hierarchy; just enhance readability.

## Nits & Edits

- Don't create a list with only one item -- write it as plain text.
- Never remove existing links while editing.
