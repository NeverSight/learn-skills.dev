---
name: re-verify-report
version: 0.1.0
description: "Verify consolidated As-Is specification for completeness, traceability, and accuracy. Cross-checks report against Phase 1-3 artifacts. Runs as independent Critic in fork context. Use when: verify report, check specification, validate phase 4, re-verify-report."
args:
  analysis: required  # Analysis name. Reads from docs/reverse/{analysis}/manifest.json
allowed-tools: Read, Grep, Glob, Bash, Write
context: fork
agent: general-purpose
---

# Report Verification — Reverse Engineering Phase 4 Critic

Verify the consolidated As-Is specification produced by `re-generate-report` against the Phase 1-3 source artifacts. Runs as an independent Critic in a separate agent context.

## Three Principles (Critic Perspective)

### 1. Code is Truth
- Phase 1-3 artifacts are the sole authority. If the report states something not present in the artifacts, the report is wrong.

### 2. Traceability to Line
- Every requirement in the traceability matrix must trace back to a Phase 3 document and ultimately to source code. Broken chains are failures.

### 3. Behavior over Intent
- Verify what the report claims against what the artifacts show. Do not interpret or justify discrepancies.

## Execution

### Step 1: Load Artifacts

Read `docs/reverse/{analysis}/manifest.json`.

Verify `phase4.status` is `"completed"` — if not, report error and stop.

Load:
- Report: `docs/reverse/{analysis}/04-report.md`
- Structure map: `docs/reverse/{analysis}/01-structure-map.md`
- All logic diagrams: `docs/reverse/{analysis}/02-logic-*.md`
- All requirements: `docs/reverse/{analysis}/03-requirements-*.md`

### Step 2: Completeness Verification

Check that the report includes all artifacts:

**Module coverage:**
- Count components in structure map
- Count components in report's module catalog
- Flag missing components

**Requirements coverage:**
- Count requirements across all Phase 3 documents
- Count requirements in report's requirements catalog
- Flag missing or extra requirements

**Logic diagram coverage:**
- Count logic diagrams in Phase 2
- Count diagrams referenced in report's appendix
- Flag missing diagrams

### Step 3: Traceability Matrix Verification

For each entry in the traceability matrix:
1. Verify the REQ-ID exists in the corresponding Phase 3 document
2. Verify the source file:line matches between report and Phase 3 document
3. Verify the EARS type classification matches
4. Flag discrepancies

### Step 4: Cross-Reference Consistency

Check internal consistency of the report:
- Components in executive summary match module catalog
- Requirement counts in summary match actual count in catalog
- EARS type distribution table is arithmetically correct
- Question list items trace to Phase 1-3 question lists

### Step 5: Factual Accuracy Spot Check

Select 5 requirements at random from the report. For each:
1. Trace back to the Phase 3 document
2. Trace back to the source code
3. Verify the chain is unbroken and accurate

### Step 6: Generate Verification Report

Write to `docs/reverse/{analysis}/verification/v4-report.md`:

```markdown
# Report Verification: {analysis}

**Verification Date**: {YYYY-MM-DD}
**Target Document**: 04-report.md
**Verdict**: {PASS / WARN / FAIL}

## Summary

| Check | Result | Details |
|:------|:-------|:--------|
| Module Completeness | {✅/⚠️/❌} | {in_report}/{in_source} components ({%}) |
| Requirements Completeness | {✅/⚠️/❌} | {in_report}/{in_phase3} requirements ({%}) |
| Logic Diagram Coverage | {✅/⚠️/❌} | {in_report}/{in_phase2} diagrams ({%}) |
| Traceability Matrix | {✅/⚠️/❌} | {valid}/{total} entries ({%}) |
| Internal Consistency | {✅/⚠️/❌} | {issues} inconsistencies |
| Spot Check Accuracy | {✅/⚠️/❌} | {accurate}/{checked} samples |

## Verdict

{PASS/WARN/FAIL}: {explanation}

## Details

### Missing Modules
| Component | Present In | Missing From |
|:----------|:-----------|:-------------|

### Missing Requirements
| REQ-ID | Phase 3 Document | Issue |
|:-------|:-----------------|:------|

### Traceability Issues
| REQ-ID | Issue | Report Says | Source Says |
|:-------|:------|:------------|:------------|

### Internal Consistency Issues
- {description}

### Spot Check Results
| # | REQ-ID | Report → Phase 3 | Phase 3 → Source | Verdict |
|:--|:-------|:------------------|:-----------------|:--------|

## Recommendations

1. **[{severity}]** {fix description}
```

### Step 7: Update Manifest

- Set `phase4.verification` to `"verification/v4-report.md"`
- If verdict is PASS or WARN: set `phase4.status` to `"verified"`
- If verdict is FAIL: leave `phase4.status` as `"completed"`
- Update `updated` timestamp

## Verdict Criteria

| Criterion | PASS | WARN | FAIL |
|:----------|:-----|:-----|:-----|
| Module completeness | 100% | >= 90% | < 90% |
| Requirements completeness | 100% | >= 95% | < 95% |
| Logic diagram coverage | 100% | >= 90% | < 90% |
| Traceability matrix accuracy | >= 95% | 85-94% | < 85% |
| Internal consistency issues | 0 | 1-2 | >= 3 |
| Spot check accuracy | 5/5 | 4/5 | <= 3/5 |

Any single FAIL criterion results in overall FAIL.

## Prohibited Actions

- Do NOT modify the report document
- Do NOT modify Phase 1-3 artifacts
- Do NOT approve documents with FAIL status
- Do NOT access the Doer's conversation context
