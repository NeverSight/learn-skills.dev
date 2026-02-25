---
name: re-verify-requirements
version: 0.1.0
description: "Verify extracted EARS requirements against source code. Check traceability, EARS classification accuracy, concrete value correctness, and completeness. Runs as independent Critic in fork context. Use when: verify requirements, check requirements, validate phase 3, re-verify-requirements."
args:
  analysis: required  # Analysis name. Reads from docs/reverse/{analysis}/manifest.json
  component: optional  # Specific component to verify. If omitted, verifies all unverified Phase 3 components
allowed-tools: Read, Grep, Glob, Bash, Write, mcp__serena__find_symbol, mcp__serena__search_for_pattern
context: fork
agent: general-purpose
---

# Requirements Verification — Reverse Engineering Phase 3 Critic

Verify EARS requirements produced by `re-extract-requirements` against actual source code. Runs as an independent Critic in a separate agent context.

**Gate rule**: Phase 4 (`re-generate-report`) shall not proceed until verification produces a `PASS` or `WARN` verdict for all components.

## Three Principles (Critic Perspective)

### 1. Code is Truth
- The source code is the sole authority. If a requirement claims behavior not present in code, the requirement is wrong.

### 2. Traceability to Line
- Every `file:line` reference in the requirements must resolve to actual code. Unresolvable references are hallucinations.

### 3. Behavior over Intent
- Verify what the requirement claims against what the code shows. Do not interpret or justify discrepancies.

## Execution

### Step 1: Load Artifacts

Read `docs/reverse/{analysis}/manifest.json`.

Determine which components to verify:
- If `component` argument is provided, verify only that component
- If omitted, verify all entries in `phase3.completed` that have `verification: null`

For each component, read the requirements document: `docs/reverse/{analysis}/03-requirements-{component}.md`

### Step 2: Source Traceability Verification

For each requirement in the document:

1. Extract the cited `file:line` reference
2. Read the source file at that line
3. Verify the code matches the requirement statement

Classify:
- ✅ **TRACEABLE**: Source line exists and matches requirement
- ⚠️ **OFFSET**: Source found within ±5 lines
- ❌ **UNTRACEABLE**: Source does not match at cited location
- 🚫 **HALLUCINATION**: Described behavior not found in source

### Step 3: EARS Classification Verification

For each requirement, verify the EARS type is correct:
- **Ubiquitous**: Confirm no conditional wrapper in source
- **Event-driven**: Confirm an explicit trigger/event exists
- **Unwanted**: Confirm an error/validation condition exists
- **State-driven**: Confirm a state loop or state check exists
- **Optional**: Confirm a configuration/feature check exists

Flag misclassified requirements.

### Step 4: Concrete Value Verification

For each concrete value cited in requirements:
1. Read the source at the cited line
2. Verify the exact value matches (thresholds, timeouts, error messages, config keys)
3. Flag any discrepancies

### Step 5: Completeness Check

Compare requirements against the source code and Phase 2 logic diagram:
- Count control flow branches in source
- Count requirements covering those branches
- Flag branches with no corresponding requirement

### Step 6: Ambiguity Check

Scan all requirement statements for prohibited words:
- appropriate, suitable, fast, slow, easy, simple, etc., some, several, as needed, user-friendly, flexible, support, handle, properly, correctly, reasonable, efficiently, should (in specs)

### Step 7: Generate Verification Report

Write to `docs/reverse/{analysis}/verification/v3-requirements-{component}.md`:

```markdown
# Requirements Verification: {component}

**Verification Date**: {YYYY-MM-DD}
**Target Document**: 03-requirements-{component}.md
**Verdict**: {PASS / WARN / FAIL}

## Summary

| Check | Result | Details |
|:------|:-------|:--------|
| Source Traceability | {✅/⚠️/❌} | {traceable}/{total} requirements ({%}) |
| EARS Classification | {✅/⚠️/❌} | {correct}/{total} classifications ({%}) |
| Concrete Values | {✅/⚠️/❌} | {verified}/{total} values ({%}) |
| Branch Completeness | {✅/⚠️/❌} | {covered}/{total} branches ({%}) |
| Ambiguity | {✅/⚠️/❌} | {violations} prohibited words found |

## Verdict

{PASS/WARN/FAIL}: {explanation}

## Details

### Traceability Issues
| REQ-ID | Cited Source | Issue | Actual Location |
|:-------|:------------|:------|:----------------|

### Classification Issues
| REQ-ID | Claimed Type | Correct Type | Reason |
|:-------|:-------------|:-------------|:-------|

### Concrete Value Discrepancies
| REQ-ID | Claimed Value | Actual Value | Source |
|:-------|:--------------|:-------------|:-------|

### Missing Requirements
- {branch at file:line with no covering requirement}

### Ambiguity Violations
| REQ-ID | Prohibited Word | Context |
|:-------|:----------------|:--------|

## Recommendations

1. **[{severity}]** {fix description}
```

### Step 8: Update Manifest

For each verified component:
- Update `phase3.completed[].verification` to `"verification/v3-requirements-{component}.md"`

After all components are verified:
- If all verdicts are PASS or WARN: set `phase3.status` to `"verified"`
- If any verdict is FAIL: leave `phase3.status` as `"completed"`
- Update `updated` timestamp

## Verdict Criteria

| Criterion | PASS | WARN | FAIL |
|:----------|:-----|:-----|:-----|
| Source traceability | >= 95% | 85-94% | < 85% |
| EARS classification | 100% | >= 90% | < 90% |
| Concrete values | 100% | >= 90% | < 90% |
| Branch completeness | >= 90% | 75-89% | < 75% |
| Ambiguity violations | 0 | 1-2 | >= 3 |
| Hallucinations | 0 | 0 | >= 1 |

Any single FAIL criterion results in overall FAIL.

## Prohibited Actions

- Do NOT modify requirements documents
- Do NOT modify source code files
- Do NOT approve documents with FAIL status
- Do NOT access the Doer's conversation context
