---
name: tdd
description: Test-driven development discipline. Use when building or fixing code test-first, when red-green-refactor is requested, or when an implementation skill needs a reliable testing loop.
---

# Test-Driven Development

TDD is the red-to-green loop. Tests verify behavior through public interfaces, not
implementation details, and each cycle lands one narrow vertical slice.

## Process

1. Read the active project's `CONTEXT.md`, relevant ADRs, approved spec, and ticket
   before testing. Identify the highest existing public seam that demonstrates the
   required behavior. If a new seam is needed, propose it before writing tests.

   Done when the test seam is agreed and named in the implementation work.

2. Write one failing behavior test at that seam. Use an independent expected value
   and avoid internal mocks, private methods, call-order assertions, and database
   side-channel verification.

   Done when the test fails for the missing behavior.

3. Write only the implementation needed to make that test pass. Run the focused test
   and typecheck regularly.

   Done when the focused test passes without speculative behavior.

4. Repeat one vertical slice at a time. Mock only system boundaries such as external
   APIs, time, randomness, and sometimes file systems or databases. Prefer real test
   infrastructure where practical.

   Done when all approved behavior at the seam is covered by behavior-focused tests.

5. Run the repository's coverage tooling for changed code. Target 100% coverage and
   require at least 95%, unless the user or repository explicitly opts out. Improve
   meaningful missing coverage rather than adding tautological tests.

   Done when coverage meets the agreed threshold or the explicit exception is
   recorded in the implementation artifact.
