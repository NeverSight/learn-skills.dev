---
name: ste-report
description: >
  Write findings and reports as one line per finding — location, label,
  problem, fix — in plain language (ISO 24495-1) and ASD-STE100 Simplified
  Technical English. Use when writing review findings, audit results, or a
  handover or status report, or when code-review asks for one.
---

# STE report

A reader acts on a finding without a second read. Each finding is one line:
where, how bad, what breaks, what to do.

## Finding line

```
`<file>:<line>` · <label> — <problem>. <fix>.
```

- **Location:** an exact file and line, or a line range (`:88-140`). Use a
  component or document name when there is no file.
- **Label:** the caller's scale (for example `P1 · high`). Without a scale,
  use `bug`, `risk`, `nit`, or `question`.
- **Problem:** what breaks, for whom, and when. Start with the problem.
- **Fix:** one concrete change, as an instruction. Name the symbol to add or
  change.
- **Why:** add one more sentence only when the problem does not show the
  consequence.

Write symbols, functions, files, and commands in backticks, with their exact
names.

```
`src/user.ts:42` · P1 · high — `user` is null when `.find()` gets no match, so `.email` throws. Add a guard before `.email`.
`src/api.ts:23` · P2 · medium — A 429 response fails the sync with no retry. Wrap the call in `withBackoff(3)`.
`src/order.ts:88-140` · P3 · high — `submit()` validates, normalizes, persists, and notifies. Extract `validate()` and `persist()`.
```

## Language

Write in plain language per ISO 24495-1:2023: the reader finds what they
need, understands it on the first read, and can act on it. At sentence level,
use ASD-STE100 Simplified Technical English. Two additions:

- Write complete sentences with articles.
- Uncertainty goes in the label, as the confidence or as `question`.

## Paragraph cases

Write a short paragraph, at most six sentences, for:

- a security finding: the attack, the precondition, and a reference
- an architectural disagreement: the rationale and what the alternative buys

Return to one line per finding after the paragraph.
