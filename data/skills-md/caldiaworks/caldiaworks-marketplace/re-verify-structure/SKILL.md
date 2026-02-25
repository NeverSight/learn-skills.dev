---
name: re-verify-structure
version: 0.1.0
description: "Verify structure analysis output against source code. Check file:line references, component completeness, and Mermaid diagram validity. Runs as independent Critic in fork context. Use when: verify structure, check structure map, validate phase 1, re-verify-structure."
args:
  analysis: optional  # Analysis name (e.g., "my-analysis"). Manifest path derived as docs/reverse/{analysis}/manifest.json
  manifest: optional  # Direct path to manifest.json. Takes precedence over analysis if both provided
allowed-tools: Read, Grep, Glob, Bash, Write, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__list_dir, mcp__serena__get_symbols_overview
context: fork
agent: general-purpose
---

# Structure Verification — Reverse Engineering Phase 1 Critic

Verify the structure map produced by `re-structure-analysis` against the actual source code. This skill runs as an independent Critic in a separate agent context. It has no access to the Doer's reasoning — only the artifacts.

**Gate rule**: Phase 2 (`re-visualize-logic`) shall not proceed until this verification produces a `PASS` or `WARN` verdict.

## Three Principles (Critic Perspective)

### 1. Code is Truth
- The source code is the sole authority. If the structure map says something the code does not confirm, the structure map is wrong.

### 2. Traceability to Line
- Every `file:line` reference in the structure map must resolve to actual code. Unresolvable references are hallucinations.

### 3. Behavior over Intent
- Verify what the structure map claims against what the code shows. Do not interpret or justify discrepancies.

## Execution

### Step 1: Load Artifacts

Determine the manifest path:
- If `manifest` argument is provided, use it directly
- If `analysis` argument is provided, derive path as `docs/reverse/{analysis}/manifest.json`
- At least one of `manifest` or `analysis` must be provided

Read the manifest and structure map:
```
{manifest-path}
{analysis-dir}/01-structure-map.md
```

Extract from the manifest:
- `targets.entry_points` — original user-specified targets
- `phase1.status` — must be `"completed"` to proceed
- `language` — for tool strategy

If `phase1.status` is not `"completed"`, report error and stop.

### Step 2: Reference Verification

Extract all `file:line` references from the structure map.

For each reference:

1. **File existence**: Verify the file exists at the specified path.
2. **Line validity**: Read the file and verify the line number is within range.
3. **Content match**: Verify the content at the cited line matches the claim in the structure map.

Classify each reference:

| Category | Criteria |
|:---------|:---------|
| ✅ VALID | File exists, line exists, content matches claim |
| ⚠️ INACCURATE | File exists, content found within ±10 lines of cited line |
| ❌ INVALID | File does not exist, or line number grossly wrong |
| 🚫 HALLUCINATION | Component described in structure map cannot be found in source code at any location |

### Step 3: Completeness Verification

Count actual components in the target scope and compare with the structure map.

**With Serena:**
```
mcp__serena__search_for_pattern(
    substring_pattern="class |interface |def |function ",
    restrict_search_to_code_files=true
)
```

**Without Serena:**
- Use Grep to count class/function definitions in the target scope
- Compare with the number listed in the structure map

Calculate coverage: `(listed_in_map / actual_in_source) * 100`

| Coverage | Verdict |
|:---------|:--------|
| >= 95% | PASS |
| 90% - 94% | WARN |
| < 90% | FAIL |

List any components found in source but missing from the structure map.

### Step 4: Mermaid Diagram Validation

For each Mermaid code block in the structure map:

1. Check syntax validity (matching brackets, valid node definitions, valid arrow syntax)
2. Spot-check 3 nodes/relationships against source code
3. Document any syntax errors or content inaccuracies

### Step 5: Internal Consistency Check

Verify that:
- Components in dependency diagrams are also listed in component tables
- Entry points in diagrams match the entry point section
- File paths are consistent throughout the document
- `targets_for_phase2` in the manifest references components that exist in the structure map

### Step 6: Generate Verification Report

Write to `docs/reverse/{analysis}/verification/v1-structure.md`:

```markdown
# Structure Map Verification Report

**Verification Date**: {YYYY-MM-DD}
**Target Document**: docs/reverse/{analysis}/01-structure-map.md
**Verdict**: {PASS / WARN / FAIL}

## Summary

| Check | Result | Details |
|:------|:-------|:--------|
| Reference Accuracy | {✅/⚠️/❌} | {valid}/{total} references ({%}) |
| Component Coverage | {✅/⚠️/❌} | {listed}/{actual} components ({%}) |
| Mermaid Syntax | {✅/⚠️/❌} | {error_count} errors |
| Internal Consistency | {✅/⚠️/❌} | {inconsistency_count} issues |

## Verdict

{PASS}: Phase 2 may proceed.
{WARN}: Minor issues found. Phase 2 may proceed. Corrections recommended.
{FAIL}: **Critical issues found. Phase 2 must not proceed. Corrections required.**

## Reference Verification Details

### Invalid References
| Claim | File:Line | Issue | Expected |
|:------|:----------|:------|:---------|
| {claim} | {reference} | {issue description} | {correct reference or "not found"} |

### Hallucinations
- {component}: {reason it is considered hallucinated}

## Completeness Details

### Missing Components
| Component | File | Type |
|:----------|:-----|:-----|
| {name} | {file path} | {class/function/interface} |

## Mermaid Validation

### Syntax Errors
- Block {N}: {error description}

### Content Inaccuracies
- Node "{node}": {discrepancy}

## Internal Consistency Issues

- {description of inconsistency}

## Recommendations

1. **[CRITICAL]** {fix description}
2. **[HIGH]** {fix description}
3. **[MEDIUM]** {fix description}
```

### Step 7: Update Manifest

Read the current manifest, then update:

- Set `phase1.verification` to `"verification/v1-structure.md"`
- If verdict is `PASS` or `WARN`: set `phase1.status` to `"verified"`
- If verdict is `FAIL`: leave `phase1.status` as `"completed"` (do not promote)
- Update `updated` timestamp

## Verdict Criteria

| Criterion | PASS | WARN | FAIL |
|:----------|:-----|:-----|:-----|
| Reference accuracy | >= 95% | 80-94% | < 80% |
| Component coverage | >= 95% | 90-94% | < 90% |
| Mermaid errors | 0 | 1-2 | >= 3 |
| Hallucinations | 0 | 0 | >= 1 |

Any single FAIL criterion results in an overall FAIL verdict.

## Prohibited Actions

- Do NOT modify the structure map document
- Do NOT modify source code files
- Do NOT assume missing information — flag it as an issue
- Do NOT approve documents with FAIL status
- Do NOT access the Doer's conversation context or reasoning
