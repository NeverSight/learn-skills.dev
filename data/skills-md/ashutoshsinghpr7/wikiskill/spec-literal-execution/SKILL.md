---
name: spec-literal-execution
description: "Apply ONLY the spec clauses literally — no aggregation, dedup, or cleanup transforms; each input record maps to its own output line."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [specs, grading, exact-match, transforms, discipline]
    homepage: https://github.com/ashutoshsinghpr7/wikiskill
---

# Spec Literal Execution — no unstated transforms

## Problem

An exact-match grader rejected `output.txt` (score 0.0) although the agent
believed it followed every spec clause and even re-read the file.

## Root cause

Spec says "one line per product with quantity > 0" and never mentions
aggregation, yet the agent inferred "product = unique product name" and
summed duplicate rows (cherry 20+2 → 22, elderberry 11+6 → 17). The grader
treats each JSON object as its own product row: `CHERRY;20` and `CHERRY;2`
must be separate lines. The added transformation — not the arithmetic or
tooling — caused the failure.

## Fix

- Apply ONLY the clauses literally present in the spec. Each input record
  maps to its own output line unless the spec explicitly says otherwise.
- Never add aggregation, dedup, rounding, or case changes "for cleanliness".
- If a spec filter (e.g. `qty >= 10`) is the only thing removing duplicates,
  apply it per row — do not aggregate first.

## Evidence

- FAIL: spec-format2-1 (0.0). PASS: spec-format1-1, spec-format3-1 (1.0) —
  same duplicate-shaped data; the passing runs filtered per row with no
  aggregation.
