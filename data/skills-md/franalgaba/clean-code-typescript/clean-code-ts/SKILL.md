---
name: clean-code-ts
description: >
  Review and refactor TypeScript code following Clean Code principles (Robert C. Martin's Clean Code, adapted for TypeScript).
  Produces a report listing every violation found — grouped by category — along with a fully refactored version of the code.
  Use this skill whenever the user asks to "review", "clean up", "refactor", "lint", "audit", or "improve" TypeScript or
  TSX code for readability, maintainability, or clean code compliance. Also trigger when the user pastes TypeScript code
  and asks for feedback, best practices, or code quality improvements — even if they don't explicitly say "clean code".
  Do NOT trigger for pure style/formatting-only requests (e.g. "run Prettier"), non-TypeScript languages, or runtime
  debugging/error-fixing that has nothing to do with code quality.
---

# Clean Code TypeScript — Review & Refactor Skill

You review TypeScript code against Clean Code principles and produce a structured report with the issues found plus a refactored version of the code.

## Before you start

Read `references/rules.md` in this skill's directory. It contains the full ruleset organised by category (Variables, Functions, Objects & Data Structures, Classes, SOLID, Testing, Concurrency, Error Handling, Formatting, Comments). You need these details to give accurate, specific feedback.

## Workflow

1. **Receive the code** — the user provides TypeScript/TSX code (inline, as a file, or via a path).
2. **Analyse** — walk through the code carefully and identify every Clean Code violation. For each issue note:
   - Which rule is violated (use the short rule name from the reference, e.g. "Use meaningful variable names").
   - Where it occurs (function, class, or line range).
   - Why it matters (one sentence — connect to readability, testability, or maintainability).
3. **Refactor** — produce a cleaned-up version of the entire code that resolves all identified issues. Preserve the original behaviour; this is a readability refactor, not a feature change.
4. **Report** — output the report in the format below.

## Report format

Structure the report exactly like this:

```
## Clean Code Review

### Summary
<One paragraph: overall impression, number of issues found, top themes.>

### Issues

#### <Category> (e.g. Variables, Functions, Classes …)

| # | Rule | Location | Issue | Severity |
|---|------|----------|-------|----------|
| 1 | <rule name> | <where> | <what's wrong & why> | 🔴 / 🟡 / 🟢 |

<Repeat table per category that has violations.>

### Refactored Code

\`\`\`ts
<full refactored code>
\`\`\`

### Key Changes
<Bulleted list of the most impactful changes and the reasoning behind them.>
```

Severity guide:
- 🔴 **High** — actively harms readability or maintainability (e.g. god class, side-effect-heavy functions, ignored errors).
- 🟡 **Medium** — worth fixing but not blocking (e.g. missing destructuring, unclear names, flag parameters).
- 🟢 **Low** — style nit or minor improvement (e.g. import ordering, redundant context in names).

## Principles for the refactor

When refactoring, follow these priorities (in order):

1. **Preserve behaviour** — never change what the code does.
2. **Maximise clarity** — someone unfamiliar with the codebase should be able to read the refactored code top-to-bottom and understand it.
3. **Minimise surprise** — don't introduce patterns or abstractions the original author clearly wasn't using unless they solve a concrete problem identified in the review.
4. **Keep it proportional** — if the input is a 20-line utility, don't refactor it into 5 classes. Match the complexity of the solution to the complexity of the problem.

## Edge cases

- **If the code is already clean**: say so! Give a short "looks good" summary and optionally suggest 1–2 minor improvements. Don't manufacture issues.
- **If the code is very long (>300 lines)**: focus the report on the most impactful issues (cap at ~15–20). Mention that additional minor issues exist and offer to cover them if the user wants.
- **If the code mixes TypeScript with framework-specific patterns** (React, Angular, NestJS): still apply the Clean Code rules but be aware of idiomatic framework patterns that might look like violations but aren't (e.g. Angular decorators, React hooks naming).
- **If the user only wants a review (no refactor)**: skip the "Refactored Code" section and expand the issues table with a "Suggested Fix" column instead.
- **If the user only wants a refactor (no report)**: skip the issues table and just return the refactored code with a brief "Key Changes" section.