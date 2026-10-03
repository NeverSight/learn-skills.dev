---
name: implement
description: Implement a spec or ticket in narrow, verified slices with tests and a closing review. Use when an approved spec or ticket is ready to build.
license: MIT
disable-model-invocation: true
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Implement

Implement the user-provided spec or tickets in narrow, verifiable slices.

1. Read the supplied source, confirm the intended behavior and pre-agreed test seams, and record the review fixed point before changing code.
2. Use the `tdd` skill for every testable slice at the agreed seams. Keep feedback tight with relevant type checks and focused tests as each slice changes.
3. Commit the verified implementation to the current branch, then use the `code-review` skill against the recorded fixed point.
4. Address review findings, rerun the affected verification and the full suite, then commit any resulting changes.

**Complete when:** every specified behavior is implemented and verified at its agreed seam, the full suite passes, review findings are addressed, and all resulting work is committed.
