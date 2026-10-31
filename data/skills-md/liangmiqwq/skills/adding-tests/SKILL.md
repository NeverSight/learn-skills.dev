---
name: adding-tests
description: Load this skill when you add a test, including modifying a test to fit an added function. Do not load this skill when you are deleting tests or modifying a test to fit a deleted feature.
---

# Adding Tests

## Core Principle

**One test is usually enough. Only add multiple tests if the bug manifests differently under multiple conditions.**

**Test behavior, not implementation. Validate outcomes, not code paths.**

A test's value is measured by:

1. Does it fail when user-facing behavior breaks?
2. Does it stay green when internals are refactored?
3. Does it catch the real issue it was written for?

## Routing

Identify your context, then read the corresponding file:

| Context     | When to use                                        | Reference                 |
| ----------- | -------------------------------------------------- | ------------------------- |
| Bug fix     | Fixing a reported issue, adding a regression guard | `branches/bug-fix.md`     |
| New feature | Adding new behavior, validating a spec             | `branches/new-feature.md` |

## Universal Rules

These apply regardless of context:

- **Prefer integration tests** — they catch real bugs; unit tests rarely do for most projects
- **Mock as little as possible** — use real deps, temp dirs, test guards
- **One behavior per test** — don't combine multiple assertions for unrelated behaviors
- **Test the public surface** — never modify production code (add params, expose internals) to make a test work

Read the relevant branch file for context-specific guidance.

## Transparent Response

For the every test you added, you should mention and explain what is used for in the final response that displays to the users.

Use `list` and `table` markdown grammar and explain the exact role clearly. Sometimes, one test function or one fixture includes more than one purpose or item, you are still required to describe them. You are allowed to use nested `list` (no more than 2 layers)

That means, every test you added will be shown to the users, you should control the number of tests at a reasonable count otherwise you might annoy users.
