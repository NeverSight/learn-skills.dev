---
name: office-environment-diagnostics
description: Use when checking whether a platform, Office version, machine, or recipient supports Excel COM, VBA, Power Query, Data Model, PDF export, ACE/OLEDB, MSOLAP, ADOMD, offline, Mac, Windows, Linux, or web execution.
---

# Office Environment Diagnostics

## Core Rule

Diagnose the machine before blaming the workbook. Capture provider and runtime facts, then decide which workbook operations can be validated on the current system.

## Environment And Evidence Contract

Record two environments separately:

- **Execution environment**: where the agent, scripts, and probes run.
- **Target environment**: where the workbook will be authored, automated, consumed, or delivered.

A captured probe is evidence about its execution environment only. Do not transfer its conclusions to a different target environment without matching platform, Office version, bitness, providers, and policy.

Use three evidence levels:

- **Structural evidence**: cross-platform package, OpenXML, formula, and source checks. This cannot prove desktop Excel behavior.
- **Runtime capability evidence**: local registration, COM activation, object-model access, and generated-fixture smoke tests.
- **Workbook behavior evidence**: workbook-specific calculation, refresh, VBA, Data Model, endpoint, and rendered-output validation in the target host.

## Workflow

1. **Probe compatibility capabilities**
   - Run `tools/probe_excel_capabilities.ps1 -OutJson <path> -Profile inventory` for non-Excel inventory evidence.
   - Use `-Profile runtime` only when generated-workbook Excel runtime smoke is intended.
   - Build the decision report with `tools/build_excel_compatibility_report.py --probe-json <path>`.
   - Add one or more `--require-capability <id>` arguments only for capabilities the requested operation actually requires.

2. **Preserve provider detail when needed**
   - Run `tools/probe_excel_bi_providers.ps1` on Windows.
   - Add `-RunExcelComSmoke` when Excel automation must be proven.
   - Add `-RunAdoWorkbookSmoke` when ACE/OLEDB workbook SQL must be proven.
   - From Git Bash, use `tools/invoke_excel_bi_com.sh provider-probe`.

3. **Build a reviewer-facing provider report**
   - Run `tools/build_provider_environment_report.py` against the probe JSON.
   - Use `--baseline-json` and `--fail-on-drift` when comparing machines or checking provider drift.
   - Use `tools/create_provider_environment_fixture.py` only to test report logic without live Office.

4. **Validate specialized endpoints**
   - For ADO workbook SQL, run `tools/test_excel_ado_sql_access.ps1`.
   - For ADOMD COM activation, run `tools/test_excel_adomd_query.ps1 -ProbeOnly`.
   - For a real cube/model endpoint, require an explicit connection string and MDX query.

5. **State platform fallbacks**
   - Windows desktop Excel can validate Excel COM, VBA, Power Query refresh, Data Model, and CUBE recalculation.
   - macOS and Excel for web are target hosts with different automation surfaces; do not substitute Windows COM evidence for them.
   - Linux and third-party spreadsheet tools can run structural OpenXML and source checks, but cannot prove desktop Excel runtime behavior.
   - Git Bash on Windows is a shell wrapper path; it still depends on Windows Excel and providers.
   - When runtime probing is unavailable, use captured probe evidence for its source environment and mark target-host behavior unknown until validated there.

## Required Evidence

- Probe command and result path.
- Excel/Office bitness when available.
- Provider availability and smoke status.
- Explicit list of operations that are safe to run on the current machine.
- Explicit execution environment, target environment, and evidence level for every compatibility conclusion.

## Boundaries

- A provider probe does not prove a customer workbook's business logic.
- A synthetic provider fixture proves report behavior only, not local Office readiness.
- Do not claim missing providers are package failures without separating environment capability from workbook defects.

## References

- Read `references/environment-decision-tree.md` when diagnosing Excel COM, provider, bitness, Trust Center, or refresh-readiness failures.
