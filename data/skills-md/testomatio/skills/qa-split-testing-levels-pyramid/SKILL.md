---
name: qa-split-testing-levels-pyramid
description: Apply the testing pyramid to a feature — divide test scenarios across levels (unit, integration, e2e), assign each scenario to the cheapest sufficient level, and produce a coverage split per level. Use when asked "unit, integration or e2e?", "what level should this test be?", "how should we test this feature?", "what test coverage do we need?", or to apply the test pyramid to a feature or project.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# QA Split Testing Levels — Test Pyramid

Applies the testing pyramid to a feature: each scenario goes to the cheapest level that can still catch its failure.
Input: a feature description, or risk scenarios from a prior QA analysis.

## Testing levels

Default layers, bottom to top:

- **unit + integration**
- **e2e**
- **manual**

A layer can hold several kinds of tests with separate runners: `e2e api` / `e2e web` / `e2e mobile`.
Other testing layers a project may have instead: component, functional, contract, visual.
**Take the testing layers and kinds from the project; use the default only when the scan finds nothing.**

## Workflow

1. Inventory existing tests with the `scan-automation-project` skill.
2. Detect the project's testing layers and the kinds of tests inside them.
3. Assign each scenario to the lowest layer that catches its failure, and to a kind within it.
4. Recommend a coverage split per layer and kind.

## Rules

- Do not recommend manual verification for scenarios already covered by automated tests.
- Explain why a scenario cannot sit at a lower layer when assigning it upward.
- A kind never covers another kind of the same layer: `e2e web` does not cover `e2e api`.
- Generalize existing automated scenarios; expand only when the user asks.

## Output

- Section `📐 Testing levels`: the layers and kinds used, when they differ from the default.
- Section `☑️ What is already tested`: number and scope of existing tests per layer and kind.
- Section `🧪 Testing plan`: scenario → layer and kind (`e2e / api`), with reasoning.
- When the environment can render charts, add a pie chart or test pyramid: test count and share per layer and kind. Skip the diagram in plain terminal output.
- For manual items: how to verify (`action → expected result`).

## Next actions

Offer after the plan:

- Write manual test cases or a checklist → `qa-write-test-cases` skill.
- Automate manual cases into autotests → `automate-manual-test-cases` skill.
- Map tests to source files for change-aware runs → `qa-test-code-coverage` skill.
