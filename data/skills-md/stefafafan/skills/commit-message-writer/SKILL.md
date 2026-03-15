---
name: commit-message-writer
description: Draft conventional commit messages that explain why a change exists instead of listing what changed. Use when trying to write a git commit message.
---

# Commit Message Writer

## Overview

Draft commit messages from intent. Explain why the change exists, not just what changed.

## Workflow

1. Gather the rationale from the user-agent conversation, project docs, explored implementation, or recent git history.
2. Infer the most defensible reason when the diff does not state it explicitly.
3. Choose the narrowest conventional commit type that fits the change.
4. Write a why-first subject line.
5. Add a body only when extra context helps.

## Subject

Use the form `type(scope): why`.

Prefer these conventional commit types:
- `feat`: introduce user-facing capability
- `fix`: correct broken or risky behavior
- `refactor`: improve structure without intended behavior change
- `perf`: improve performance characteristics
- `test`: add or fix tests
- `docs`: change documentation only
- `build`, `ci`, `chore`: repository or tooling maintenance

- Stay at 50 characters or fewer.
- Focus on intent or effect, not implementation steps or file edits.
- Use a scope only when it adds meaning.
- Avoid vague summaries such as `update`, `change`, `modify` or `move`.

Examples:
- `fix(auth): block expired token reuse`
- `refactor(api): simplify pagination flow`
- `feat(billing): support invoice retry recovery`

## Body

When needed, leave the second line blank and start the body on the third line.

- Wrap every body line at 72 characters.
- Use the body for motivation, constraints, tradeoffs, or follow-up context.
- Do not repeat the diff unless that detail is needed to explain why.
