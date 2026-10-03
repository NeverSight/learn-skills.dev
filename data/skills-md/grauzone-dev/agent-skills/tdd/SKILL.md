---
name: tdd
description: "Test-driven development at agreed seams: red, green, refactor. Use when implementing behavior that needs tests or when the user asks for test-first work."
license: MIT
disable-model-invocation: true
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Test-driven development

Work in a **red → green → refactor** loop at agreed seams.

Before exploring behavior or naming tests, read `docs/agents/domain.md` when it exists and follow its domain-documentation contract. Otherwise, read the relevant `CONTEXT.md` and ADRs.

## Tests

Test behavior through public interfaces. Name the capability the caller gains; expected values come from an independent source such as a known literal, worked example, or the spec.

For test examples, read [tests.md](references/tests.md). When a test reaches an external boundary, read [mocking.md](references/mocking.md).

## Seams — where tests go

A **seam** is the public boundary where behavior is observed without reaching inside. Before writing a test, record the seams under test and confirm them with the user.

When the shape of that interface is itself in question — how deep the module is, where the seam belongs, what the interface should expose — load the `codebase-design` skill for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel.
- **Tautological** — recomputes the expected value the way the code does.
- **Horizontal slicing** — writes tests in bulk instead of one **tracer bullet** at a time.

## Loop

1. **Red.** Write one failing test at an agreed seam.
2. **Green.** Write only the implementation needed for that test to pass.
3. **Refactor.** Improve the design while every existing test remains green.

**Complete when:** every agreed behavior is covered by a passing public-interface test, and the suite remains green after the final refactor.
