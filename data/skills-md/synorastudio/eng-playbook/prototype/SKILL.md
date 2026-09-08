---
name: prototype
description: Build a throwaway Prototype that answers one design question. Use when the user explicitly asks to prototype, compare UI variants, or test uncertain logic, state, workflow, or data before production. Do not use for ordinary production implementation.
---

# Prototype

A prototype is throwaway code that answers a question. The answer is valuable; the prototype is disposable.

## Choose the branch

- Logic, state, workflow, or data-model uncertainty -> follow `LOGIC.md`.
- UI, screen, component, layout, or visual direction uncertainty -> follow `UI.md`.

If the question is ambiguous, ask. If the user is unavailable, choose the branch that best matches the surrounding code and state the assumption.

## Rules

- Mark prototype code clearly as prototype-only.
- Keep it close to the code or product area it explores.
- Provide one command or route to run it.
- Avoid persistence unless persistence is the question being tested.
- Skip production polish, generalized abstractions, and broad error handling.
- Surface the relevant state or variant differences.
- Delete or absorb the prototype when the question is answered.

## Capture the answer

Before deleting or absorbing the prototype, capture:

- The question the prototype answered.
- The verdict.
- Any decision that should become an ADR.
- Any docs, issue, or architecture update needed.

Do not leave unexplained prototype code in the repo.

Finish when the prototype has produced a verdict, the verdict is recorded in the smallest relevant artifact, and no unexplained prototype code remains.
