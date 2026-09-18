---
name: w-tdd
description: Implement a requested increment with red-green-refactor.
disable-model-invocation: true
---

Use TDD only when the user asked for it or the repository requires it. Follow the repo testing MDX and `vitest-v5` (or the stack's test skill). Do not commit unless asked.

1. Red: write a failing test for the desired behavior. Use real APIs where the repo tests do; mock only at documented boundaries.
2. Green: write the smallest implementation that passes that test.
3. Refactor: improve structure while tests stay green.
4. Repeat for the next increment. Run the focused test file each cycle, then the affected suite.
5. Docs: `/w-docs` if behavior or commands changed.
