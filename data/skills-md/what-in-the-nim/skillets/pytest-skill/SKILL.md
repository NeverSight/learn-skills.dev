---
name: pytest-skill
description: >
  Pytest syntax and examples for fixtures, parametrization, markers, mocking,
  and conftest configuration. Use when writing Python tests or answering pytest
  usage questions. Companion reference to testing-principle.
languages:
  - Python
category: unit-testing
license: MIT
metadata:
  author: TestMu AI
  version: "1.0"
---

# Pytest Reference

Apply [testing-principle](../testing-principle/SKILL.md) for test design and repository conventions. These examples illustrate syntax; adapt their layout, classes, dependencies, and mocks to that policy.

Read only the relevant section of [the playbook](reference/playbook.md):

| Need | Section |
|------|---------|
| Basic assertions, fixtures, parametrization, markers, CLI commands | Basic patterns |
| Configuration and coverage | §1 |
| Fixture scope, factories, teardown, temporary files | §2 |
| IDs, combinations, indirect parametrization | §3 |
| Mocking, spies, environment patches | §4 |
| Async tests and fixtures | §5 |
| Exceptions and warnings | §6 |
| Markers and collection hooks | §7 |
| Test classes | §8 |
| CI | §9 |
| Troubleshooting | §10 |
| Production checklist | §11 |

Mock only justified boundaries. Assert interactions when the outgoing interaction is the contract; prefer destination, payload, or result assertions over incidental call counts.
