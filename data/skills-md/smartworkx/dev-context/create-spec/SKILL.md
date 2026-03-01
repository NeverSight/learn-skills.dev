---
name: create-spec
description: >-
  Write BDD test scenarios in Gherkin for a feature.
  TRIGGER when: user asks to write, create, or add specs, scenarios, or Gherkin features.
  Examples: "write specs for...", "create a feature file", "add BDD scenarios for user export".
  DO NOT TRIGGER when: user wants to run tests, write unit tests, or implement a feature.
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
---

Write BDD-style test scenarios in Gherkin before implementation.

## Steps

1. Determine the feature — the argument can be:
   - A **GitHub issue number or URL** → fetch with `gh issue view` for context (do NOT embed the issue number in the spec)
   - A **feature description** → use as the feature name
   - Nothing → ask the user what feature to specify

2. Explore the codebase for related context:
   - Read `CLAUDE.md` for project conventions
   - Check existing code and tests related to the feature
   - Check `doc/adr/` and `doc/` for relevant decisions and documentation

3. Check `doc/spec/` for an existing spec that covers this feature:
   - If found → add new scenarios to the existing file
   - If not found → create a new file: `doc/spec/<kebab-case-feature-name>.feature`

4. Write scenarios using this template:

```gherkin
Feature: <Feature Title>
  <Brief description of the feature>

  Scenario: <scenario name>
    Given <precondition>
    When <action>
    Then <expected result>
```

5. Tell the user what was created or updated and its path

## Guidelines

Based on [el-feo/ai-context/cucumber-gherkin](https://skills.sh/el-feo/ai-context/cucumber-gherkin) conventions.

- **Declarative over imperative** — focus on *what* not *how* (say "the user is logged in", not "the user enters credentials and clicks login")
- **No technical implementation details** — specs describe behavior from the user's perspective, not the technology behind it. Say "a chat widget is visible", not "the Matrix/Element widget is embedded". Technology choices belong in ADRs, not specs.
- Keep scenarios concise — 3-5 steps
- Use domain language stakeholders understand
- One behavior per scenario
- Use `Background` for shared preconditions (4 lines max)
- Use `Rule` to group related scenarios under a business rule
- Use `Scenario Outline` with `Examples` for data-driven scenarios
- Move implementation complexity into step definitions, not scenario text
- Do NOT reference issue numbers in the spec — specs are standing documentation

## Rules

- Specs live in `doc/spec/` as `.feature` files
- Filenames are kebab-case: `doc/spec/user-export.feature`
- Prefer extending an existing spec over creating a new one when the feature overlaps
