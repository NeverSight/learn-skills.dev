---
name: detect-duplicate-test-cases
description: Find duplicate, near-duplicate, and overlapping test cases across the test suite. Identifies exact matches, semantically similar tests, and tests that are subsets of other tests. Provides recommendations for which tests to keep, merge, or remove.
---

# Detect Duplicate Test Cases

Detect duplicate test cases in the user's project. Recommend cleanup actions.

## Workflow

### 1. Collect Test Cases

- Find all manual and automated test cases in the repository.
  - Manual: markdown files inside `/tests/`, `.feature` files (Gherkin).
  - Automated: `*.spec.ts`, `*.test.js`, `*.cy.js`, etc.
- Parse each test to extract: title, steps, expected results, tags, and suite location.

### 2. Analyze Duplicates

Normalize test content before comparison:
- Convert titles to lowercase.
- Remove punctuation and formatting differences.
- Normalize step wording where possible.
- Ignore framework syntax (`describe`, `Scenario`, `it`, etc.) when analyzing intent.
- Treat parameterized values (emails, IDs, usernames) as variable data.

Compare tests using multiple similarity signals:
- Title similarity.
- Step similarity.
- Expected result similarity.
- Preconditions or setup.
- Shared tags or metadata.
- Test location or suite context.

Score each pair using the scoring rules in `./references/DUPLICATE_INSTRUCTIONS.md`.
Classify each pair into a detection level (defined in the same reference):
- Level 1: exact duplicates.
- Level 2: semantic duplicates.
- Level 3: overlapping / subset tests.
- Level 4: redundant variations.

Build duplicate groups where multiple tests represent the same testing intent.
Each group includes:
- All related tests.
- Similarity score.
- Detection level.
- Proposed canonical test.

### 3. Generate Report

Follow the report template in `./references/DUPLICATE_INSTRUCTIONS.md`. Include:
- Summary statistics (total scanned, duplicates found by category).
- Each duplicate group with test details and locations.
- Similarity percentage.
- Recommendation for each group (`keep`/`merge`/`remove`).
- Suggested actions.

### 4. Execute Actions

**Apply actions only after the user approves the recommendations.**

- Merge: combine duplicate or highly similar tests into one canonical test.
  - Preserve the original test structure used by the framework (e.g., Gherkin, Markdown, Jest, Cypress).
  - Retain the primary test ID from the canonical test.
  - Merge tags, labels, and metadata from all source tests (deduplicate where possible).
  - Preserve important assertions, steps, and expected results.
  - Add references to the original test files or IDs that were merged.
- Remove: delete duplicate or redundant test files or test entries.
  - Ensure the canonical or replacement test already exists.
  - Add a reference in the canonical test noting which tests were removed.
  - **Do not remove tests that contain unique steps, tags, or coverage.**
- Keep: keep both tests but document their relationship.
  - Add cross-reference notes between related tests.
  - Indicate the reason both tests remain (e.g., different environments, data sets, or coverage).

## Preservation Rules

When merging or rewriting tests, preserve:
- Test IDs: keep the canonical ID and reference any merged IDs.
- Tags / labels: retain and merge all relevant tags.
- Framework structure: keep the original format (e.g., `Scenario`, `describe/it`, Markdown sections).
- File organization: maintain the existing test directory conventions.
- Traceability metadata: keep links to requirements, issues, or tickets if present.

**Never break framework syntax or remove traceability metadata when rewriting tests.**
