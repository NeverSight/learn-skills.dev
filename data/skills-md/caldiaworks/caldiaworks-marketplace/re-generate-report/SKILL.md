---
name: re-generate-report
version: 0.1.0
description: "Aggregate reverse engineering artifacts into consolidated As-Is specification. Reads all phase outputs from manifest.json. Creates traceability matrix, cross-validates findings, and generates stakeholder-ready document. Use when: generate report, As-Is specification, consolidate analysis, final report, re-generate-report."
args:
  analysis: required  # Analysis name. Reads from docs/reverse/{analysis}/manifest.json
allowed-tools: Read, Grep, Glob, Bash, Write
context: fork
agent: general-purpose
---

# Integrated Report — Reverse Engineering Phase 4

Aggregate ALL reverse engineering artifacts from Phase 1-3 into a consolidated As-Is specification document. This skill reads the manifest to discover all artifacts and produces a single comprehensive report.

## Three Principles

### 1. Code is Truth
- As-Is spec documents ACTUAL code behavior
- Suspected bugs remain in Question List, not removed from spec
- No editorial improvements or "should" statements

### 2. Traceability to Line
- Traceability matrix links every requirement to source line
- All findings traceable to Phase 1-3 artifacts
- Orphaned findings (no source) flagged for review

### 3. Behavior over Intent
- Executive summary focuses on "what" system does, not "why"
- Architectural patterns described from observed structure
- No assumptions about business intent

## Execution

### Step 1: Load Manifest and Collect Artifacts

Read `docs/reverse/{analysis}/manifest.json`.

Verify:
- `phase3.status` is `"verified"` — if not, report error and stop

Collect all artifacts:
- Phase 1: `phase1.output` → structure map
- Phase 2: `phase2.completed[].output` → logic diagrams
- Phase 3: `phase3.completed[].output` → requirements documents

Read each artifact and extract key sections.

Set `phase4.status` to `"in_progress"`.

### Step 2: Cross-Reference Verification

**Requirements → Logic Diagrams:**
For each requirement, find corresponding nodes in Phase 2 logic diagrams. Confirm line numbers match.

**Logic Diagrams → Structure Map:**
For each logic diagram, confirm the source file is listed in the Phase 1 structure map.

**Log inconsistencies:**
| Finding | Artifact A | Artifact B | Issue |
|:--------|:-----------|:-----------|:------|

### Step 3: Build Traceability Matrix

Combine requirements from all Phase 3 documents:

| Module | REQ-ID | EARS Type | Requirement | Source File:Line | Evidence Strength |
|:-------|:-------|:----------|:------------|:-----------------|:------------------|

Evidence strength:
- ✅ **Strong**: Implementation + verified by Critic
- ⚠️ **Medium**: Implementation + partial verification
- ❌ **Weak**: Implementation only

### Step 4: Consolidate Question Lists

Merge from all phases and prioritize:

- **🔴 Critical**: Suspected bugs with high impact (data loss, crashes)
- **🟡 Important**: Architecture/design clarity questions
- **🟢 Informational**: Optimization opportunities, style concerns

### Step 5: Generate Executive Summary

Summarize from collected artifacts:
- System type and technology stack
- Primary functions (from structure map)
- Analysis scope and coverage
- Key findings and technical debt count

### Step 6: Generate Report

Write to `docs/reverse/{analysis}/04-report.md`:

```markdown
# As-Is Specification: {analysis}

**Document Version**: 1.0
**Analysis Date**: {YYYY-MM-DD}
**Target System**: {system description}
**Language**: {language}
**Framework**: {framework and version}
**Analysis Scope**: {scope description}

---

## Executive Summary

### System Overview

**System Type**: {description}

**Primary Functions**:
- {function 1}
- {function 2}

**Technology Stack**:
- **Language**: {language and version}
- **Framework**: {framework}
- **Database**: {if applicable}
- **Messaging**: {if applicable}

### Analysis Scope

**Files Analyzed**: {count}
**Components Analyzed**: {count}
**Requirements Extracted**: {count} EARS requirements
**Coverage**: {percentage} of target scope

### Key Findings

- **Technical Debt**: {count} suspected issues
  - 🔴 Critical: {count}
  - 🟡 Important: {count}
  - 🟢 Informational: {count}

---

## Technology Stack

{detailed technology stack from structure map}

---

## Module Catalog

{component listing from structure map, organized by category}

---

## Requirements Catalog (EARS)

### By Module

{requirements grouped by component}

### By EARS Type

| EARS Type | Count | Percentage |
|:----------|:------|:-----------|
| Ubiquitous | {n} | {%} |
| Event-driven | {n} | {%} |
| Unwanted | {n} | {%} |
| State-driven | {n} | {%} |
| Optional | {n} | {%} |
| **Total** | **{N}** | **100%** |

---

## Appendix A: Logic Diagrams

{embedded or linked logic diagrams from Phase 2}

---

## Appendix B: Traceability Matrix

{full traceability matrix from Step 3}

---

## Appendix C: Question List (Prioritized)

### 🔴 Critical

{critical questions with source references and recommendations}

### 🟡 Important

{important questions}

### 🟢 Informational

{informational items}

---

## Appendix D: Analysis Constraints

### Confidence Factors
{from structure map}

### Evidence Strength Distribution
| Strength | Count | Percentage |
|:---------|:------|:-----------|
| ✅ Strong | {n} | {%} |
| ⚠️ Medium | {n} | {%} |
| ❌ Weak | {n} | {%} |

---

**Document Control**

| Version | Date | Description |
|:--------|:-----|:------------|
| 1.0 | {YYYY-MM-DD} | Initial As-Is specification |
```

### Step 7: Update Manifest

- Set `phase4.status` to `"completed"`
- Set `phase4.output` to `"04-report.md"`
- Update `updated` timestamp

## Validation Before Completion

After writing the report, re-read it and verify every number against the source data. Counting errors in the executive summary undermine confidence in the entire report.

- [ ] All Phase 1-3 artifacts collected and referenced
- [ ] Cross-reference verification completed
- [ ] Traceability matrix links all requirements to source
- [ ] Question list prioritized (Critical / Important / Informational)
- [ ] **Count verification**: Total requirements in executive summary matches actual count in requirements catalog. EARS type distribution sums to the total. Question list count matches actual items in Appendix C. Re-count by enumerating each item — do not rely on numbers from Phase 3 documents or your own earlier statements
- [ ] Executive summary reflects actual findings (no speculation)
- [ ] No requirements added that aren't in Phase 3 documents
- [ ] manifest.json updated

## Prohibited Actions

- Do NOT add requirements not present in Phase 3 artifacts
- Do NOT editorialize or propose improvements in As-Is spec
- Do NOT remove suspected bugs — they belong in the Question List
- Do NOT speculate on business intent
- Do NOT modify Phase 1-3 artifacts
