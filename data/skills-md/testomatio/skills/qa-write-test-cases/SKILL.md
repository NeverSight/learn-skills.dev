---
name: qa-write-test-cases
description: Generate test cases and checklists for software testing. Use this skill whenever the user asks to create test cases, test scenarios, test plans, checklists, QA documentation, or mentions testing activities like "write tests for feature", "create a test checklist", "generate test scenarios from requirements", or similar. This skill works better if user provides documentation, requirements, etc., or it can create test cases based on the user prompt without any additional context.
---

# Test Case & Checklist Generator

Generates test cases and checklists for software testing from the context the user provides.

References:

- [Test Case Format](./references/test-case-format.md) — markdown format for suites, tests, and steps (Testomat.io-friendly)
- [Writing Rules](./references/writing-rule.md) — rules for suites, tests, preconditions, steps, and AI writing patterns to avoid
- [Testomat.io TMS Guide](./references/testomat-tms-guide.md) — Testomat.io conventions and MCP tools

## Prerequisites

- Project structure checked (source code, e2e tests, test cases) via the /scan-automation-project skill.
- Existing Testomat.io tests pulled via the /sync-test-cases-with-tms skill.
- PLAN mode enabled, if available, for the interview steps.

## User interaction

- **Always generate a checklist before test cases**, even if the user asks for test cases directly.
- **Do not skip steps. Get user approval at each gate before moving to the next step.**
- Strictly recommend PLAN mode. Switch to Edit mode only on the last step — writing test cases to md files.
- Use the Ask tool for choices when available.
- Fill input fields with suggestions when asking the user for input.
- Mark questions with ❓ and numbered options:

```
❓ Do you want to:

1. action 1
2. action 2
3. type something else
```

## Workflow

1. Gather context and show sources — approval gate
2. Ask for coverage scope — approval gate
3. Ask for role — approval gate; skipped for smoke
4. Generate checklist — approval gate
5. Generate detailed test cases
6. Show summary

### Step 1: Gather context

Understand:

- the feature/functionality under test and its business goals
- main testing flows and user journeys
- specific areas of concern

Information sources:

- User prompt
- Task tracking systems (Jira, etc.)
- Requirements documents (Confluence, etc.)
- Design mockups (Figma, Miro, etc.)
- Existing test cases (TestRail, Testomat.io, etc.)
- Source code:
  - manual test files: `.test.md` or `.md` in folders like `manual-tests`, `tests`, `manual`, `qa`, `spec`
  - automated test files (spec, test, cy files, etc.)
  - project structure

Sources may come as pasted text, links, or MCP tools. Ask the user for MCP configuration if needed.

Analyzing source code:

- Usually this skill runs from an automation project without application code. Check which case this is.
- Automation-only project: scan briefly, focus on test files.
- Application + automation project: scan the application code thoroughly; skip unit-test depth unless the user asks.

#### Testomat.io TMS detection

Detect if this is a Testomat.io project. Two options:

Option 1 — MCP. If the `testomatio` MCP is available, gather context:

- `suites_list`, `suites_search` — existing structure
- `tests_search`, `tests_list` — existing tests, avoid duplicates
- `steps_list`, `steps_search` — reusable shared steps
- `tags_list`, `labels_list` — project conventions

Option 2 — `sync-test-cases-with-tms` skill (with `check-tests` lib). Run it with the `pull` action, then analyze the downloaded files for:

- existing structure and suites
- current test cases (to avoid duplicates)
- project conventions (tags, labels, priority levels)

If existing test cases intersect with the feature under test, report them to the user and suggest expanding them or creating a new suite.

#### Approval gate

Show the list of sources (names only, no content) and ask:

```markdown
I've gathered information from the following sources:

- Jira issue ABC-123
- Confluence
- Figma

❓ Do you want to:

1. ➡️ Go to next step
2. ✏️ Type changes
```

### Step 2: Ask for coverage scope

The scope sets the initial checklist size; the user can still fine-tune it in Step 4.

- **Compute approximate test counts per tier from your Step 1 analysis. Do not use generic or hardcoded ranges** — the numbers must reflect the specific feature under test.
- If you can't reasonably estimate (feature too vague, context too thin), say so and either omit the numbers or go back to Step 1.
- If the user picks ✏️ Other, accept a number ("around 10") or a free-form description ("just the API contract, no UI") and size the checklist from it.

Show each option as a block: bold label with test count on the first line, description on the next. Replace `<N>` with your estimates:

```markdown
❓ **How much coverage do you want?**

**1. 🚀 Smoke** ~<N> tests
Critical-path only

**2. ⚖️ Balanced** ~<N> tests
Happy path, key negative and common edge cases

**3. 🧨 Exhaustive** ~<N> tests
Full coverage incl. error states, boundaries, and security/perf/i18n where relevant

**4. ✏️ Other**
Proceed to specific role selection, type a number of tests, or describe scope in your own words
```

### Step 3: Ask for role

- If the user picked 🚀 Smoke in Step 2: **skip this step** — auto-apply ⚙️ default and go straight to Step 4. A smoke suite is too small to benefit from a specialized role.
- Otherwise show the roles (markdown table with name and short description) and ask the user to pick one. Recommend a role based on context.
- Use ⚙️ default if the user does not specify a role.
- If the user selects 🔧 other, ask them to define a custom role.
- If you show only some roles, add a "Show all available roles" option:

```
❓ Choose role:

1. default (or recommended role based on context)
2. ☰ Show all available roles
3. ✏️ Type role name
```

#### Roles

| Role               | Description                              |
| ------------------ | ---------------------------------------- |
| **⚙️ default**     | **balanced** approach                    |
| **🌈 optimist**    | **positive** flows, happy path           |
| **🤓 nerd**        | **details**, dependencies, perfectionist |
| **🔪 psycho**      | **edge cases**                           |
| **🔐 pentest**     | **security**                             |
| **🎨 picasso**     | **ui/ux**                                |
| **⚖️ lawyer**      | **texts**, error messages, typos, etc.   |
| **🌐 polyglot**    | **localization**, translations           |
| **📈 performance** | **performance**, load, stress, etc.      |
| 🔧 other           | **specify your own role**                |

### Step 4: Generate checklist

Create a hierarchical, categorized checklist from the gathered context.

Size it to the Step 2 tier:

- 🚀 smoke — only critical paths
- ⚖️ balanced — happy path, key negative, common edge cases
- 🧨 exhaustive — full coverage
- ✏️ other — follow what the user described

Example:

```markdown
- Signup
  - Signup with valid email
  - Signup with valid phone number

- Login
  - Login with valid email
  - Login with valid phone number
  - Login with invalid password
```

#### Approval gate

- If a multi-select/checkbox Ask tool is available: present leaf items as checkboxes, prefixed with their category (e.g. `Login: valid email`), with the recommended subset for the chosen tier pre-checked. The ticked items become the test cases in Step 5.
- Otherwise: show the markdown checklist and ask the user to add/remove/change items.

Always ask about the amount of cases / level of detail:

```
❓ Do you want to:

1. 👍 Keep as is
2. ➖ Less details
3. ➕ More details
4. ✏️ Type anything you want to change
```

- More details → enable the 🤓 nerd role.
- User modifies the checklist → regenerate (Step 4).
- User not satisfied → go back to Step 1 for more context.
- Approved → Step 5.

### Step 5: Generate detailed test cases

If the user originally asked only for a checklist, first ask: "Do you want to generate test cases for this checklist?"

Where to store test cases:

- Empty or manual-tests-only workspace → project root
- End-to-end testing project → `manual-tests/` directory
- Any other case → `.testeiya/manual-tests/` (ensure `.testeiya/` exists and is git-ignored)

Generation rules:

- Name files `feature-name.test.md` (always the `.test.md` extension).
- Multiple features or whole product → one file per feature.
- **Don't change the user's source code. Only generate `*.test.md` files.**
- **Keep scope**: test only the functionality under test; don't test linked features unless the user explicitly asks.

Format rules:

- Strictly follow [Test Case Format](./references/test-case-format.md) for suites, tests, and steps. Only exception: the user specifies their own format in the prompt.
- Strictly follow [Writing Rules](./references/writing-rule.md) for suite/test descriptions, preconditions, steps, expected results, and anti-patterns.
- Follow the [Testomat.io TMS Guide](./references/testomat-tms-guide.md) for conventions (priority levels, tags, labels), especially when using the testomatio MCP.
- Wrap test cases in `<!-- suite ... -->` and `<!-- test ... -->` blocks.
- If required, put `tags:` and `labels:` inside each `<!-- test ... -->` metadata block (see [test metadata](./references/test-case-format.md#test-metadata)), not only on the suite block.
- Reuse existing tags and labels obtained via MCP or from other test cases.
- Do not use labels if you are not aware of any existing ones.
- If reasonable, add test metadata (priority, preconditions, test data, labels, tags) based on the analyzed context.
- Use concrete, executable values. **Do NOT introduce `${...}` placeholders in first-pass generation.** Parametrize only genuinely reused or data-driven values; format them as `${variable}` in backticks.
- **NEVER generate test or suite IDs of any kind:**
  - Do NOT include Testomat.io IDs (`id: @T*`, `id: @S*`, e.g. `@T12345678`, `@S380c64db`).
  - Do NOT include custom/random IDs (e.g. `TC-001`, `TC-R001`, `SUITE-01`) in `id:` fields, titles, or anywhere else.
  - Testomat.io IDs are server-generated and assigned when the user runs `check-tests push` with `--update-ids` (or via the `sync-test-cases-with-tms` skill). Never add IDs at generation time.

#### Matching existing test case formats

When the user provides an existing test case example or asks for "similar" test cases:

DO match:

- writing style and level of detail
- field structure (Priority, Preconditions, Type, Test Data, etc.)
- additional fields like labels and tags
- original case language

DON'T copy:

- any IDs from the example — neither Testomat.io IDs (`@T...`, `@S...`) nor custom prefixes (e.g. `TC-R001`, `TC-001`)
- original test case intent

### Step 6: Show summary

- Show a concise summary (markdown table works well): number of test cases and suites, generated files, destination folder.
- Ask the user to review the files and request changes if needed.
- Suggest uploading the test cases to Testomat.io via the `sync-test-cases-with-tms` skill.
