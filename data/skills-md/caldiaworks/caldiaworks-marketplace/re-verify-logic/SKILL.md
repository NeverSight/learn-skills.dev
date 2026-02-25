---
name: re-verify-logic
version: 0.1.0
description: "Verify logic diagrams against source code. Check line-number accuracy, Mermaid syntax, node completeness, and side effect documentation. Runs as independent Critic in fork context. Use when: verify logic, check logic diagram, validate phase 2, re-verify-logic."
args:
  analysis: required  # Analysis name. Reads from docs/reverse/{analysis}/manifest.json
  component: optional  # Specific component to verify. If omitted, verifies all completed Phase 2 components without verification
allowed-tools: Read, Grep, Glob, Bash, Write, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview
context: fork
agent: general-purpose
---

# Logic Verification — Reverse Engineering Phase 2 Critic

Verify logic diagrams produced by `re-visualize-logic` against actual source code. Runs as an independent Critic in a separate agent context.

**Gate rule**: Phase 3 (`re-extract-requirements`) shall not proceed until verification produces a `PASS` or `WARN` verdict for all components.

## Three Principles (Critic Perspective)

### 1. Code is Truth
- The source code is the sole authority. If the logic diagram says something the code does not confirm, the diagram is wrong.

### 2. Traceability to Line
- Every line number in the diagram must resolve to actual code. Unresolvable references are hallucinations.

### 3. Behavior over Intent
- Verify what the diagram claims against what the code shows. Do not interpret or justify discrepancies.

## Execution

### Step 1: Load Artifacts

Read `docs/reverse/{analysis}/manifest.json`.

Determine which components to verify:
- If `component` argument is provided, verify only that component
- If omitted, verify all entries in `phase2.completed` that have `verification: null`

For each component, read the logic diagram: `docs/reverse/{analysis}/02-logic-{component}.md`

### Step 2: Line Number Verification

For each node in the Mermaid diagram and each row in the node-to-line mapping table:

1. Extract the cited line number
2. Read the source file at that line
3. Compare the code at that line with the claim

Classify:
- ✅ **MATCH**: Code at cited line matches the description
- ⚠️ **OFFSET**: Code found within ±5 lines
- ❌ **MISMATCH**: Code at cited line does not match
- 🚫 **HALLUCINATION**: Described behavior not found in source at any location

### Step 3: Mermaid Syntax Validation

Check each Mermaid code block for:
- Valid node definitions and arrow syntax
- No prohibited characters (`!=`, `>=`, `[]`, `()` in text)
- Parseable structure (matching brackets, valid subgraphs)

### Step 4: Completeness Check

Compare the logic diagram against the source method:
- Count control flow branches in source (if/else, switch cases, loops)
- Count corresponding nodes in the diagram
- Flag missing branches

Check side effects documentation:
- Grep source for database operations, network calls, file I/O, logging
- Verify each is documented in the side effects summary

### Step 5: Generate Verification Report

Write to `docs/reverse/{analysis}/verification/v2-logic-{component}.md`:

```markdown
# Logic Diagram Verification: {component}

**Verification Date**: {YYYY-MM-DD}
**Target Document**: 02-logic-{component}.md
**Verdict**: {PASS / WARN / FAIL}

## Summary

| Check | Result | Details |
|:------|:-------|:--------|
| Line Number Accuracy | {✅/⚠️/❌} | {match}/{total} nodes ({%}) |
| Mermaid Syntax | {✅/⚠️/❌} | {error_count} errors |
| Branch Coverage | {✅/⚠️/❌} | {covered}/{total} branches ({%}) |
| Side Effects | {✅/⚠️/❌} | {documented}/{total} side effects ({%}) |

## Verdict

{PASS/WARN/FAIL}: {explanation}

## Details

### Line Number Issues
| Node | Claimed Line | Actual Line | Issue |
|:-----|:-------------|:------------|:------|

### Missing Branches
- {description of missing branch at file:line}

### Missing Side Effects
- {description of undocumented side effect at file:line}

## Recommendations

1. **[{severity}]** {fix description}
```

### Step 6: Update Manifest

For each verified component:
- Update `phase2.completed[].verification` to `"verification/v2-logic-{component}.md"`

After all components are verified:
- If all verdicts are PASS or WARN: set `phase2.status` to `"verified"`
- If any verdict is FAIL: leave `phase2.status` as `"completed"`
- Update `updated` timestamp

## Verdict Criteria

| Criterion | PASS | WARN | FAIL |
|:----------|:-----|:-----|:-----|
| Line number accuracy | >= 95% match | 80-94% | < 80% |
| Mermaid syntax errors | 0 | 1-2 | >= 3 |
| Branch coverage | >= 90% | 75-89% | < 75% |
| Side effect documentation | 100% | >= 80% | < 80% |
| Hallucinations | 0 | 0 | >= 1 |

Any single FAIL criterion results in overall FAIL.

## Prohibited Actions

- Do NOT modify logic diagram documents
- Do NOT modify source code files
- Do NOT approve documents with FAIL status
- Do NOT access the Doer's conversation context
