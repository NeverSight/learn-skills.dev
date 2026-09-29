---
name: improve-test-cases
description: Analyze and improve existing markdown manual test cases for clarity, structure, and Test Management Tool format compliance.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Improve Test Cases

Analyze and improve existing markdown manual test cases to make them clearer for the QA team:
- Improve test titles for clarity.
- Enhance test descriptions.
- Fix broken formatting and markdown syntax.
- Standardize test structure to Test Management Tool format.
- Ensure consistent terminology and language.
- Update tags and labels.

**DO NOT CHANGE:**
- Original test/suite IDs.
- Original test intent.
- Original language (fix only clarity, grammar, typos).

## Step 1: Locate Test Files

- Find markdown test files (`.test.md` or `.md`) in common locations: `./manual-tests`, `./tests/manual`, `./docs/tests`.
- If none found, scan the whole project for `.md` files with test case content.
- If still none, ask the user for the test directory path.

## Step 2: Analyze Test Quality

Read each test and flag issues:

Titles:
- Unclear or vague test title.
- Missing action-object format.
- Not specific enough to understand what is being tested.

Descriptions:
- Vague or unclear test purpose.
- Missing or incomplete description.

Steps and expected results:
- Missing expected results.
- Inconsistent step format.
- Unclear actions.
- Steps not ordered logically.
- Expected results not relevant to the steps.
- Missing pass/fail criteria.

Formatting:
- Broken markdown syntax.
- Missing sections.
- Inconsistent header hierarchy.

Ambiguity:
- Generic or subjective terms ("should work", "might fail").
- Vague language that could be interpreted multiple ways.
- Steps that cannot be verified objectively.
- Missing specific values, data, or conditions.

## Step 3: Show Summary to User

- List issues found per test.
- Give specific recommendations for improvements.
- **Ask the user to confirm before proceeding.**
- If the user does not confirm, do not change anything.

## Step 4: Improve Tests

Titles:
- Make clear and specific.
- Use action-result format: "Verify [action] results in [expected]".
- Ensure the title reflects the actual test purpose.

Descriptions:
- Make purpose clear and concise.
- Include context from the parent suite when relevant.
- Fix grammar and spelling only.

Steps:
- Give each step an explicit expected result.
  - Nested format: "- Step action..." with indented "_Expected_: ...".
- Make actions specific and reproducible.
- Add measurable pass/fail criteria.
- Ensure results are directly relevant to the step action.
- Make results measurable and verifiable.
- Avoid vague terms; use specific values and conditions.

Ambiguity:
- Replace generic terms with specific, testable language.
- Avoid subjective terms ("should work", "might fail").
- Ensure steps can be verified objectively.

Metadata:
- Set `type: manual` in test metadata.
- Use only these priority values: `low`, `normal`, `important`, `high`, `critical`.

## Step 5: Save Changes

- Overwrite the original files.
- Keep the same file names and directory structure.
- **Preserve all original test/suite IDs.**

## Step 6: Show Final Summary

- Number of files modified.
- Number of tests improved.
- Key improvements made.

## Reference

TMS markdown format example: [references/TESTOMAT_MARKDOWN_EXAMPLE.md](references/TESTOMAT_MARKDOWN_EXAMPLE.md)
