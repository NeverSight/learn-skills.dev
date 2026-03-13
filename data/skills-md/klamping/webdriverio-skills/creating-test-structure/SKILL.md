---
name: creating-test-structure
description: Use when creating or extending WebdriverIO test structure from a markdown test plan by adding describe/it/hooks and pseudo-code comments without implementing WDIO commands yet.
---

# Creating Test Structure

Build the test skeleton first, then implementation.

This skill converts a markdown test plan into test scaffolding by either:
- creating a new spec file, or
- inserting new suites/tests/hooks into an existing spec file.

It produces:
- real `describe` / `it` / hook blocks
- readable test names
- pseudo-code comments for every setup, action, and assertion

## When to Use

- You have a test plan and need a fast, consistent scaffold.
- You need to append new test sections to an existing spec.
- You want to separate structure decisions from implementation details.
- You want a handoff file for `writing-webdriverio-code`.

## When Not to Use

- You need concrete selectors, WDIO commands, waits, or assertions.
- You are fixing flaky runtime behavior (use `writing-webdriverio-code`).
- You only need small edits to already-implemented test logic.

## Required Inputs

- Path to a markdown test plan.
- Target spec file path (new or existing).
- Existing suite conventions (Mocha/Jasmine style, naming, hooks).

## Project Context Files

Before scaffolding, read project cache files when available:

- `.webdriverio-skills/project-context.md`
- `.webdriverio-skills/project-context.json`
- `.webdriverio-skills/custom-rules.md`
- `references/website-analysis/<target>/website-analysis.md`
- `references/website-analysis/<target>/website-analysis.json`

Use these files to align naming, hook usage, test organization, and team conventions.

Use website analysis references to target high-impact routes/components and preserve section/sequence terminology in pseudo-code.

Resolve `<target>` as lowercase site host (prefer user URL or project `baseUrl` host). If unknown, use `unknown-target`.

If files are missing or stale, run `managing-project-customizations` first.

## Choose the Right Test Level

- Prefer the lowest level that can prove behavior with confidence.
- Use component-level tests for isolated UI behavior.
- Use UI integration tests for front-end flows with mocked/stubbed backend behavior.
- Use E2E tests for a small set of high-value end-to-end business paths.
- Do not force every scenario into E2E if a lower level is faster and more stable.

## Small Independent Tests vs Long Flows

- Default to small, independent tests that set up their own required state.
- Avoid test-order dependencies (`test B` requiring `test A` to run first).
- If a long flow is used, keep it intentional and limited to a single high-value journey.
- Prefer API/state setup over UI-only setup when preparing preconditions.
- Ensure every scaffolded test can run in isolation unless the plan explicitly says otherwise.

## Output Contract

- Output is valid JavaScript/TypeScript test structure.
- Existing implemented code is preserved.
- New scaffolding is inserted in the appropriate suite/context.
- Each hook/test body contains pseudo-code comments only.
- One comment line per intended step.
- Expected values are written as indented comment lines.

## Pseudo-Code Comment Format

- Use imperative verbs: `// Click ...`, `// Assert ...`.
- Keep each line atomic (single action/assertion).
- Keep implementation-neutral language (no selector syntax).
- Preserve business terms from the plan.

## Workflow

1. Parse plan sections and scenarios.
2. Load project context and custom rules for style and structure constraints.
3. Detect whether target file is new or existing.
4. For existing files, locate the correct insertion point and preserve existing code.
5. Map major sections to nested `describe` blocks.
6. Place setup/teardown in the narrowest valid hooks.
7. Create `it` blocks with sentence-style names.
8. Add pseudo-code steps in execution order.
9. Save scaffolded spec file with seamless formatting and style.

## Quick Reference

| Plan content | Scaffold result |
|---|---|
| Feature area | `describe(...)` |
| Context/state | nested `describe(...)` |
| Scenario | `it(...)` |
| Shared precondition | `before` / `beforeEach` |
| Shared cleanup | `after` / `afterEach` |

## Common Mistakes

- Writing WDIO commands in scaffold comments.
- Overwriting or restructuring unrelated existing tests.
- Putting global setup into every test instead of hooks.
- Using vague test names like `should work`.
- Encoding selector details in pseudo-code.

## Example

```js
describe('Homepage', function () {
  describe('Logged In', function () {
    before(async function () {
      // Log in via API using user1 fixture
      // Navigate to / load the home page
    });

    it('should show both feed tabs', async function () {
      // Retrieve visible feed tab labels
      // Assert tabs equal:
      //   ['Your Feed', 'Global Feed']
    });
  });
});
```

Handoff complete when structure is stable and pseudo-code is explicit enough to implement line-by-line.
