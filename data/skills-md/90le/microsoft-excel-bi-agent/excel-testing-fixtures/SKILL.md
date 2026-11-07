---
name: excel-testing-fixtures
description: Use when creating customer-data-free Excel fixtures, regression cases, smoke workbooks, sample queries, or forward-test inputs for workbook automation and validation.
---

# Excel Testing Fixtures

## Core Rule

Use sanitized fixtures to prove tooling behavior without moving customer workbooks into the plugin package. Fixtures should be small, deterministic, and explicit about what they do not prove.

## Fixture Types

- CUBE and model-report structure: `tools/create_cube_formula_fixture.py`.
- Workbook formulas, names, tables, and charts: `tools/create_workbook_surface_fixture.py`.
- Formula quality edge cases: `tools/create_formula_quality_fixture.py`.
- Controls, hidden sheets, protection, filters, and validation: `tools/create_workbook_controls_fixture.py`.
- External dependencies and pure deliverable cleanup: existing external dependency fixtures and cleanup-plan tools.
- Power Query source-lineage samples: `tools/build_sanitized_fixture_bundle.py`.
- Provider environment drift logic: `tools/create_provider_environment_fixture.py`.
- Cross-agent prompts and response stubs: `tools/build_cross_agent_forward_test_pack.py`, `tools/build_cross_agent_forward_test_runbook.py`, and related scoring tools.

## Workflow

1. Choose the smallest fixture that covers the behavior under test.
2. Generate the fixture into a temporary folder or a task-local test folder.
3. Run the target report, linter, or release-gate smoke against the fixture.
4. Record the expected counts and boundaries.
5. Delete or keep outputs according to whether they are generic package fixtures or task-local evidence.

## Evidence Rules

- A fixture proves the parser, reporter, or workflow path for the designed case.
- A fixture does not prove every customer workbook shape.
- Generated sample responses prove scorer mechanics only, not real external-agent behavior.
- Keep customer data, screenshots, and machine-specific reports out of reusable fixture folders.

## Boundaries

- Do not fabricate customer-like sensitive data.
- Do not use fixtures to claim live Power Query refresh, VBA execution, Data Model evaluation, or provider availability unless the fixture actually runs that runtime path.
- Prefer temp paths for generated validation reports.

## References

- Read `references/fixture-design-rules.md` before adding a new smoke fixture or forward-test case.
