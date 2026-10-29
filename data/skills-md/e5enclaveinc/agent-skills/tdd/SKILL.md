---
name: tdd
description: "Apply the red-green-refactor loop with no skipped steps. Use when building a feature or fixing a bug test-first, or when a test must prove missing behavior before code exists."
metadata:
  version: "1.0.0"
  adapted-from: "mattpocock/skills (MIT) — method only; no code or text copied"
  signed: false
---

# TDD

> **Attribution:** Adapted from mattpocock/skills (MIT). Upstream is canonical; this adaptation adds E5's curation and promotion-gate framing.
>
> Method only; no code or text copied. See `LICENSE` for the upstream MIT license notice.

Red, green, refactor. In that order, every time.

## The loop

1. **Red:** write a failing test for one behavior. Watch it fail — a test
   that passes before the code exists proves nothing.
2. **Green:** write the smallest code that makes it pass. No more.
3. **Refactor:** clean the code while the test stays green.

## Rules

- One behavior per test. A test that checks three things checks nothing
  when it fails.
- Never write production code without a failing test first — no
  exceptions for "trivial" code.
- When the design fights the tests, listen: the friction is information
  about the design.
