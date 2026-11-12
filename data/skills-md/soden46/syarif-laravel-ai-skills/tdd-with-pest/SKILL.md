---
name: tdd-with-pest
description: Laravel guidance to apply RED-GREEN-REFACTOR with Pest or PHPUnit; use factories, feature tests for HTTP, and parallel test runners; verify failures before implementation
tags:
  - laravel
  - php
---

# Tdd With Pest

Use this skill when a Laravel task involves tdd with pest.

This skill is adapted to the personal Laravel standards in this repository. It maps the public `tdd-with-pest` topic from `jpcaparas/superpowers-laravel` into the local `tdd-with-pest` catalog without copying third-party skill body text.

## Syarif Defaults

- Follow Laravel conventions before introducing custom abstractions.
- Prefer project-local patterns when they are explicit and tested.
- Keep controllers focused on HTTP orchestration.
- Put validation, authorization, transactions, side effects, and integrations at clear boundaries.
- Keep client names, credentials, internal URLs, provider secrets, and project-specific business rules out of reusable standards.
- Verify important behavior with the smallest meaningful tests and quality checks.

## Workflow

1. Detect the Laravel version, PHP version, runner, package manager, and existing project conventions.
2. Identify the smallest local skill set that overlaps this topic.
3. Implement or review the change using Laravel-native APIs first.
4. Add abstractions only when they reduce real complexity or protect a meaningful boundary.
5. Run targeted tests and available quality checks before handoff.

## Checkpoints

- Authorization and validation boundaries are explicit.
- Query shape, transactions, queues, cache, files, and external calls are intentional when touched.
- User-facing behavior has feature, unit, browser, or integration tests at the right level.
- Logs and errors are useful without exposing secrets or unnecessary personal data.
- Documentation or proposals avoid importing source-project names or one-off business rules.

## Related Skills

- `using-laravel-standards`
- `architecture`
- `testing`

## Context Efficiency

Layer: 4 (Verification)

Load this skill only when TDD is needed. Do not load with unrelated skills. RED-GREEN-REFACTOR, but keep it tight: one failing test, smallest passing implementation, refactor only when it simplifies. No per-function suites unless asked.
- `security`
