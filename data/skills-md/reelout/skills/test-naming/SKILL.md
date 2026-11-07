---
name: test-naming
description: "Helps write, rename, and review precise test titles based on asserted behavior and local conventions in JavaScript and TypeScript suites, including Jest, Vitest, Playwright, and Cypress. Use when the user asks to name or improve test titles."
license: MIT
---

# Test Naming

Write test titles that make clear what the test verifies and, when relevant, under which condition. A useful title helps readers understand a test failure from the report without opening the file. Apply these principles to JavaScript and TypeScript suites, including Jest, Vitest, Playwright, Cypress, and similar frameworks.

## Workflow

1. **Inspect the test and its context.** Read its assertions, setup, fixtures, title syntax, and parent suite names. For a rename or review, check nearby tests for local conventions without repeating vague wording.
2. **Identify what the test verifies.** Determine the observable behavior asserted: a result, return value, side effect, state change, rejection, or interaction.
3. **Draft a precise title.** Name the outcome and include a condition when it distinguishes the case or changes the expected behavior. Do not narrate setup or invent details the test does not establish.
4. **Check the title against the assertions.** Ensure it neither overstates nor understates what they verify, and that it remains clear in the test report alongside any parent suite title.
5. **Respect the requested scope.** For a review, explain the issue and suggest a replacement; do not edit unless asked. For a rename, change only the requested titles. Do not modify test logic, assertions, fixtures, or production code unless separately requested.
6. **Surface uncertainty.** If the setup or assertions do not establish the behavior clearly enough for an accurate title, do not guess. Explain the ambiguity and ask for clarification when it cannot be resolved from nearby code.

## Naming Principles

- **Describe behavior, not implementation.** Prefer the observable result, return value, state change, error, or meaningful interaction over incidental details such as helper names, internal calls, or mock setup.
  - **Prefer:** `persists the session token after a successful login`
  - **Avoid:** `calls setItem`
- **Choose verbs that match the assertion.** Distinguish a synchronous throw from a rejected promise when relevant. Describe resolved values, rendered state, or emitted events only as observed.
- **Name interactions when they are the contract.** Some tests verify collaboration or a dependency call rather than a user-visible outcome. Name the relevant actor and interaction; include arguments, counts, or ordering only when asserted.
- **Include the distinguishing condition.** Name the input, state, role, event, boundary, or context that separates this case from related tests. Avoid generic titles such as `handles invalid input`.
  - **Prefer:** `rejects uploads larger than the configured size limit`
  - **Avoid:** `handles invalid uploads`
- **State negative outcomes explicitly.** Say what is rejected, prevented, denied, or absent, and include the relevant condition when it aids understanding.
  - **Prefer:** `does not retry the request after a 401 response`
  - **Avoid:** `does not work with expired tokens`
- **State the claim, not every step.** When a test checks several details of one contract, describe their shared outcome. Do not turn setup or assertion mechanics into a step-by-step title, and do not split or rewrite the test unless asked.
- **Be concise without losing meaning.** Remove filler. Words such as `should` and `correctly` are useful only when they express the expectation or match local style.
- **Use the parent suite as context.** Avoid repeating information that is clear from the enclosing suite, while keeping the test title understandable in reports.
- **Follow clear local conventions.** Match neighboring tests' capitalization, tense, punctuation, and phrasing unless that would reduce accuracy or clarity.
- **Do not invent details.** Use specific values and names only when supported by the test or needed to describe its asserted scenario; do not add them merely to make a title sound precise.

## Useful Title Patterns

A useful starting pattern is:

> `[verified outcome] when [distinguishing condition]`

This is a guide, not a required formula. For a particular test, structures such as `given [context]`, `while [state]`, or an event-driven title may be clearer.

| Verified case            | Example title                                                   |
| ------------------------ | --------------------------------------------------------------- |
| Successful outcome       | `returns discounted pricing when the account qualifies`         |
| Rejection                | `rejects the upload when the file exceeds its configured limit` |
| Non-occurrence           | `does not send a notification when alerts are disabled`         |
| State-dependent behavior | `disables submit while payment is processing`                   |
| Error contract           | `throws InvalidTokenError when the token signature is invalid`  |

Use actual error names, configured thresholds, units, and values when they matter to the assertion. For boundary cases, use the tested value and relevant limit; never guess or substitute illustrative values.

## Parameterized Tests

- Make each generated title identify the case when different data produces different expected behavior.
- Preserve the framework's interpolation syntax; do not introduce unsupported placeholders.
- Include a value in the rendered title only if it clarifies the failing case or exercised condition. Indistinguishable raw data can make reports noisy.
- When practical, inspect representative rendered titles as well as the template. Ensure placeholders produce useful, unambiguous output without missing or duplicated values.

## Final Review Checklist

Before proposing or applying a title, confirm:

- It describes what the assertions verify, not what the test author may have intended.
- The outcome and any necessary condition are specific and unambiguous.
- Any negative result is stated explicitly.
- It does not duplicate context already supplied by the parent suite title.
- It follows local conventions without compromising accuracy or clarity.
- It makes sense in test output, including for parameterized cases.
- Its verbs accurately describe the observed result, including synchronous errors versus asynchronous rejections where relevant.
