---
name: doc-prd-audit
description: Unified PRD audit wrapper that runs validator then reviewer and produces a combined report for fixer consumption

metadata:
  tags:
    - sdd-workflow
    - quality-assurance
    - prd-audit
    - layer-2-artifact
    - shared-architecture
  custom_fields:
    layer: 2
    artifact_type: PRD
    architecture_approaches: [ai-agent-based]
    priority: primary
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [PRD]
    downstream_artifacts: [Audit Report, Fix Cycle]
    version: "2.3"
    last_updated: "2026-03-02"
  versioning_policy: "tracks PRD-MVP-TEMPLATE schema_version"

---

# doc-prd-audit

## Purpose

Run a **unified PRD audit workflow** that combines structural validation and content quality checks into a single pass, producing one **combined report** optimized for `doc-prd-fixer` input.

**2-Skill Model**: This skill replaces the separate `doc-prd-validator` and `doc-prd-reviewer` skills (now deprecated). All validation and review logic is consolidated here.

**Deprecated Skills**:
| Skill | Status | Replacement |
|-------|--------|-------------|
| `doc-prd-validator` | DEPRECATED | Merged into `doc-prd-audit` |
| `doc-prd-reviewer` | DEPRECATED | Merged into `doc-prd-audit` |

**Layer**: 2 (PRD Quality Gate Wrapper)

**Upstream**: PRD file(s)

**Downstream**:
- Combined Audit Report: `PRD-NN.A_audit_report_vNNN.md`
- Optional Fix Cycle trigger for `doc-prd-fixer`

---

## Why This Skill Exists

The 2-skill model (`doc-prd-audit` + `doc-prd-fixer`) simplifies the PRD quality workflow.

| Concern | Owner Skill |
|---------|-------------|
| All validation + scoring | `doc-prd-audit` (this skill) |
| Apply fixes from audit report | `doc-prd-fixer` |

---

## Fresh Audit Policy (MANDATORY)

**ALWAYS run the audit from scratch.** Do NOT:
- Reference previous audit reports for scoring decisions
- Skip validation steps based on drift cache history
- Assume compliance from prior fix history
- Use cached results from previous runs

**ALWAYS**:
- Run all validation scripts fresh every time
- Re-check all structure/schema compliance
- Re-compute EARS-Ready and SYS-Ready scores independently
- Generate a new audit report with incremented version

---

## When to Use

Use `doc-prd-audit` when:
- You want one command for PRD quality checks
- You need a combined report for `doc-prd-fixer`
- You are running CI/manual QA before EARS generation

Do NOT use when:
- PRD does not exist (use `doc-prd` / `doc-prd-autopilot` generation first)
- You only need one specific check domain (use validator or reviewer directly)

---

## Execution Contract

### Input
- PRD path (`docs/02_PRD/PRD-NN_*/...`)
- Optional: threshold (default review threshold: 90)

### Sequence (Mandatory)

```text
1) Run doc-prd-validator (internal)
2) Run doc-prd-reviewer (internal)
3) Normalize and merge findings
4) Write PRD-NN.A_audit_report_vNNN.md
5) Create/Update .drift_cache.json (MANDATORY)
6) If auto-fixable findings exist, hand off to doc-prd-fixer
```

### Drift Cache Creation (MANDATORY)

After every audit, the skill MUST create or update `.drift_cache.json` in the PRD folder.

**Location**: `docs/02_PRD/{PRD_folder}/.drift_cache.json`

**Schema** (v1.2):
```json
{
  "schema_version": "1.2",
  "document_id": "PRD-NN",
  "document_version": "X.Y",
  "upstream_mode": "brd",
  "upstream_ref_path": "../../01_BRD/BRD-NN_{slug}/",
  "drift_detection_skipped": false,
  "last_reviewed": "YYYY-MM-DDTHH:MM:SS",
  "last_fixed": "YYYY-MM-DDTHH:MM:SS",
  "reviewer_version": "2.2",
  "fixer_version": null,
  "autopilot_version": null,
  "upstream_documents": {
    "../../01_BRD/BRD-NN_{slug}/BRD-NN.0_index.md": {
      "hash": "sha256:<64-hex-chars>",
      "last_modified": "YYYY-MM-DDTHH:MM:SS",
      "file_size": 12345,
      "version": "X.Y"
    }
  },
  "review_history": [
    {
      "date": "YYYY-MM-DDTHH:MM:SS",
      "score": 100,
      "drift_detected": false,
      "report_version": "vNNN",
      "review_type": "audit",
      "status": "PASS"
    }
  ],
  "fix_history": []
}
```

**Required Actions**:
1. **Create** if `.drift_cache.json` does not exist
2. **Update** `last_reviewed` timestamp
3. **Append** to `review_history` array with current audit results
4. **Compute** SHA-256 hashes for all tracked upstream BRD documents
5. **Set** `drift_detected: true` if any upstream hash changed since last review

**Hash Computation**:
```bash
sha256sum <upstream_file> | cut -d' ' -f1
```

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-D006 | Info | Cache created (first review) |
| VAL-H001 | Error | Drift cache missing hash for upstream document |
| VAL-H002 | Error | Invalid hash format (must be sha256:<64 hex chars>) |

### Combined Status Rules

- `PASS`: Validator PASS AND Reviewer score >= threshold AND no blocking issues
- `FAIL`: Validator FAIL OR Reviewer score < threshold OR blocking/manual-required issues present

### Diagram Contract Gate (BLOCKING for PRD)

Audit MUST fail when any blocking diagram code is present:
- `PRD-E023` missing `@diagram: c4-l2`
- `PRD-E024` missing `@diagram: dfd-l1`
- `PRD-E025` missing `@diagram: sequence-*`
- `PRD-E026` sequence diagram missing `alt/else` exception path

Also include warning diagnostics when present:
- `PRD-W011` diagram intent metadata incomplete

### Element Code Contract Gate (BLOCKING for PRD)

Audit MUST fail when element type codes violate naming standards:
- `PRD-E020` Element type code not valid for PRD (must be in VALID_PRD_CODES set)
- `PRD-E022` Section-element type code mismatch (e.g., Section 5 metrics must use type `08`)

**Valid PRD Type Codes**: `01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 22, 24, 32`

**Section-Element Mapping (Enforced)**:
| Section | Expected Type Code | Element Type |
|---------|-------------------|--------------|
| 5 | 08 | Metric/KPI |
| 7 | 09 | User Story |
| 8 | 01 | Functional Requirement |
| 9 | 02 | Quality Attribute |
| 10 | 32 | Architecture Topic |
| 12 | 07 | Risk |
| 14 | 06 | Acceptance Criteria |

**Validation Command**:
```bash
bash ai_dev_ssd_flow/02_PRD/scripts/prd_standardized_element_codes_hook.sh <path>
```

---

## Validation Checks (from deprecated doc-prd-validator)

### 1. Metadata Validation

```yaml
Required custom_fields:
  document_type: ["prd", "template"]
  artifact_type: "PRD"
  layer: 2
  architecture_approaches: [array format]
  priority: ["primary", "shared", "fallback"]
  development_status: ["active", "draft", "deprecated", "reference"]

Required tags:
  - prd (or prd-template)
  - layer-2-artifact

Forbidden tag patterns:
  - "^product-requirements$"
  - "^product-prd$"
  - "^feature-prd$"
```

### 2. Structure Validation (MVP Template - 17 Sections)

**Required Sections (MVP Template)**:

| Section | Title | Required |
|---------|-------|----------|
| 1 | Document Control | MANDATORY |
| 2 | Executive Summary | MANDATORY |
| 3 | Problem Statement | MANDATORY |
| 4 | Target Audience & User Personas | MANDATORY |
| 5 | Success Metrics (KPIs) | MANDATORY |
| 6 | Scope & Requirements | MANDATORY |
| 7 | User Stories & User Roles | MANDATORY |
| 8 | Functional Requirements | MANDATORY |
| 9 | Quality Attributes | MANDATORY |
| 10 | Architecture Requirements | MANDATORY |
| 11 | Constraints & Assumptions | MANDATORY |
| 12 | Risk Assessment | MANDATORY |
| 13 | Implementation Approach | MANDATORY |
| 14 | Acceptance Criteria | MANDATORY |
| 15 | Budget & Resources | MANDATORY |
| 16 | Traceability | MANDATORY |
| 17 | Glossary | Optional |
| 18 | Appendix A: Future Roadmap | Optional |
| 19 | Migration to Full PRD Template | Optional |

### 3. Document Control Required Fields

| Field | Description | Required |
|-------|-------------|----------|
| Status | Draft/Review/Approved/Implemented | MANDATORY |
| Version | Semantic versioning (X.Y.Z) | MANDATORY |
| Date Created | YYYY-MM-DD format | MANDATORY |
| Last Updated | YYYY-MM-DD format | MANDATORY |
| Author | Product Manager/Owner Name | MANDATORY |
| Reviewer | Technical reviewer name | MANDATORY |
| Approver | Final approver name | MANDATORY |
| BRD Reference | `@brd: BRD.NN.TT.SS` format | MANDATORY |
| SYS-Ready Score | `XX/100 (Target: ≥90)` | MANDATORY |
| EARS-Ready Score | `XX/100 (Target: ≥90)` | MANDATORY |

### 4. Dual Scoring Requirements

| Score | Threshold |
|-------|-----------|
| SYS-Ready Score | ≥90% |
| EARS-Ready Score | ≥90% |

Both scores must be present and meet thresholds for downstream artifact generation.

### 5. File Naming Convention

**Pattern**: `PRD-NN_{descriptive_slug}.md`

- `NN`: 2+ digit number (01, 02, ... 99, 100)
- `descriptive_slug`: lowercase with underscores

### 6. Traceability Validation

**Layer 2 Cumulative Tags (Required)**:

```markdown
@brd: BRD.NN.TT.SS
```

**Unified Element ID Format**: `PRD.NN.TT.SS`

### 7. Structure Compliance (Nested Folder Rule)

**ALL PRDs MUST use nested folders regardless of size.**

| PRD Type | Required Location |
|----------|-------------------|
| Monolithic | `docs/02_PRD/PRD-NN_{slug}/PRD-NN_{slug}.md` |
| Sectioned | `docs/02_PRD/PRD-NN_{slug}/PRD-NN.0_index.md`, `PRD-NN.1_*.md`, etc. |

---

## Review Checks (from deprecated doc-prd-reviewer)

### 1. Link Integrity

Validates all internal document links resolve correctly.

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-L001 | Error | Broken internal link |
| REV-L002 | Warning | External link unreachable |
| REV-L003 | Info | Link path uses absolute instead of relative |

### 2. Threshold Consistency

Verifies performance metrics match across all sections.

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-T001 | Error | Threshold mismatch across PRD sections |
| REV-T002 | Error | Threshold differs from BRD source |
| REV-T003 | Warning | Threshold unit inconsistency (ms vs s) |
| REV-T004 | Info | Threshold stricter than BRD (acceptable) |

### 3. Diagram Contract Compliance

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-DC001 | Error | Missing required PRD diagram tag (`c4-l2`, `dfd-l1`, or `sequence-*`) |
| REV-DC002 | Error | Required sequence flow missing explicit exception path |
| REV-DC003 | Warning | Diagram intent header missing required fields |

### 4. BRD Alignment

Validates PRD requirements accurately reflect BRD source.

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-A001 | Error | PRD requirement without BRD source |
| REV-A002 | Warning | BRD requirement without PRD mapping |
| REV-A003 | Error | Scope mismatch (PRD vs BRD) |
| REV-A004 | Info | Requirement correctly marked as deferred |

### 5. Placeholder Detection

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-P001 | Error | [TODO] placeholder found |
| REV-P002 | Error | [TBD] placeholder found |
| REV-P003 | Warning | Template date not replaced |
| REV-P004 | Warning | Template name not replaced |
| REV-P005 | Warning | Empty section content |

### 6. Traceability Tags

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-TR001 | Error | @brd tag references non-existent BRD ID |
| REV-TR002 | Warning | @depends references non-existent PRD |
| REV-TR003 | Info | @discoverability is forward reference |
| REV-TR004 | Warning | Tag format malformed |

### 7. Section Completeness

**Minimum Word Counts** (configurable):
| Section | Minimum Words |
|---------|---------------|
| Executive Summary | 100 |
| Problem Statement | 75 |
| Functional Requirements | 200 |
| Quality Attributes | 100 |
| Customer Content | 100 |
| Risk Assessment | 75 |
| Appendices | 200 |

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-S001 | Error | Required section missing entirely |
| REV-S002 | Warning | Section below minimum word count |
| REV-S003 | Warning | Table has no data rows |
| REV-S004 | Error | Mermaid diagram syntax error |

### 8. Customer Content Review

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-C001 | Error | Section 10 missing |
| REV-C002 | Warning | Section 10 is placeholder content |
| REV-C003 | Info | Technical jargon in customer content |
| REV-C004 | Flag | Requires marketing/business review |

### 9. Naming Compliance

**Error Codes**:
| Code | Severity | Description |
|------|----------|-------------|
| REV-N001 | Error | Invalid element ID format |
| REV-N002 | Error | Element type code not valid for PRD |
| REV-N003 | Error | Legacy pattern detected (US-NNN, FR-NNN, etc.) |
| REV-N004 | Error | Threshold tag missing document reference |
| REV-N005 | Warning | Threshold key format non-standard |

### 10. Upstream Drift Detection

**Cache File**: `docs/02_PRD/{PRD_folder}/.drift_cache.json`

**Error Codes**:
| Code | Severity | Description | Trigger |
|------|----------|-------------|---------|
| REV-D001 | Warning | Upstream document modified after PRD creation | mtime > PRD date (no cache) |
| REV-D002 | Warning | Referenced content has changed | hash mismatch (with cache) |
| REV-D003 | Info | Upstream document version incremented | version field changed |
| REV-D004 | Info | New content added to upstream | file size increased >10% |
| REV-D005 | Error | Critical modification (>20% change) | hash diff >20% |
| REV-D006 | Info | Cache created (first review) | no prior cache existed |
| REV-D009 | Error | Invalid hash placeholder detected | hash is invalid format |

---

## Validator Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| PRD-E001 | ERROR | Missing required tag 'prd' |
| PRD-E002 | ERROR | Missing required tag 'layer-2-artifact' |
| PRD-E003 | ERROR | Invalid document_type value |
| PRD-E004 | ERROR | Invalid architecture_approaches format (must be array) |
| PRD-E005 | ERROR | Forbidden tag pattern detected |
| PRD-E006 | ERROR | Missing required section |
| PRD-E007 | ERROR | Multiple H1 headings detected |
| PRD-E008 | ERROR | Section numbering not sequential |
| PRD-E009 | ERROR | Document Control missing required fields |
| PRD-E010 | ERROR | Missing User Stories (Section 7) |
| PRD-E011 | ERROR | Missing Functional Requirements (Section 8) |
| PRD-E012 | ERROR | Missing Traceability (Section 16) |
| PRD-E013 | ERROR | Missing upstream @brd tag |
| PRD-E014 | ERROR | Invalid element ID format (not PRD.NN.TT.SS) |
| PRD-E015 | ERROR | SYS-Ready Score missing or below threshold |
| PRD-E016 | ERROR | EARS-Ready Score missing or below threshold |
| PRD-E017 | ERROR | Deprecated ID pattern used (US-NNN, FR-NNN, etc.) |
| PRD-E018 | ERROR | Invalid threshold tag format (must be @threshold: PRD.NN.key) |
| PRD-E019 | ERROR | Element type code not valid for PRD (see doc-naming) |
| PRD-E020 | ERROR | PRD not in nested folder structure (must be in `docs/02_PRD/PRD-NN_{slug}/`) |
| PRD-E021 | ERROR | PRD folder name doesn't match PRD ID |
| PRD-E022 | ERROR | Monolithic PRD not in nested folder (must be `PRD-NN_{slug}/PRD-NN_{slug}.md`) |
| PRD-E023 | ERROR | Missing required PRD diagram tag `@diagram: c4-l2` |
| PRD-E024 | ERROR | Missing required PRD diagram tag `@diagram: dfd-l1` |
| PRD-E025 | ERROR | Missing required PRD diagram tag `@diagram: sequence-*` |
| PRD-E026 | ERROR | Sequence diagram missing explicit exception/alternate path (`alt/else`) |
| PRD-W001 | WARNING | File name does not match format PRD-NN_{slug}.md |
| PRD-W002 | WARNING | Missing optional section (Glossary, Appendix) |
| PRD-W003 | WARNING | Score below recommended threshold but above minimum |
| PRD-W004 | WARNING | Missing Document Revision History table |
| PRD-W005 | WARNING | Architecture Decision Requirements reference ADR numbers |
| PRD-W011 | WARNING | Diagram intent header missing required fields |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |
| PRD-I001 | INFO | Consider adding success metrics with quantified targets |
| PRD-I002 | INFO | Consider adding competitive analysis |

---

## Combined Report Format (for doc-prd-fixer)

Output file: `PRD-NN.A_audit_report_vNNN.md`

Required sections:

1. `## Summary`
   - PRD ID, timestamp (EST), overall status
   - Validator status, reviewer score
2. `## Score Calculation (Deduction-Based)`
   - Formula: `100 - total_deductions`
   - Deductions grouped by: contamination (max 50), FR completeness (max 30), structure/quality (max 20)
   - Threshold comparison (`>=90` pass gate)
3. `## Validator Findings`
   - List by severity/code
4. `## Reviewer Findings`
   - List by severity/code
5. `## Diagram Contract Findings`
   - Required PRD tags status (`c4-l2`, `dfd-l1`, `sequence-*`)
   - Exception-flow evidence status (`alt/else`)
   - Intent header completeness status
6. `## Fix Queue for doc-prd-fixer`
   - `auto_fixable`
   - `manual_required`
   - `blocked`
7. `## Recommended Next Step`
   - `run doc-prd-fixer`
   - or `manual update required`

### Fix Queue Normalization

Each finding MUST include:
- `source`: `validator` | `reviewer`
- `code`: issue code
- `severity`: `error|warning|info`
- `file`: relative path
- `section`: heading/anchor if known
- `action_hint`: short imperative guidance
- `confidence`: `high|medium|manual-required`

---

## Hand-off Contract to doc-prd-fixer

`doc-prd-fixer` MUST accept combined audit report as equivalent upstream input:
- `PRD-NN.A_audit_report_vNNN.md` (preferred)
- `PRD-NN.R_review_report_vNNN.md` (legacy compatibility)

If both exist, fixer should prefer latest timestamp.

---

## Validation Commands

```bash
# Canonical wrapper (core only; pre-commit/CI parity)
bash ai_dev_ssd_flow/02_PRD/scripts/prd_core_wrapper_hook.sh ai_dev_ssd_flow/02_PRD

# Strict PRD ID checks (same quality class as BRD ID checks)
bash ai_dev_ssd_flow/02_PRD/scripts/prd_standardized_element_codes_hook.sh ai_dev_ssd_flow/02_PRD
bash ai_dev_ssd_flow/02_PRD/scripts/prd_legacy_pattern_hook.sh ai_dev_ssd_flow/02_PRD

# Canonical wrapper (core + advisory)
bash ai_dev_ssd_flow/02_PRD/scripts/validate_prd_wrapper.sh docs/02_PRD

# Validate single PRD document (must be in nested folder)
python ai_dev_ssd_flow/02_PRD/scripts/validate_prd.py docs/02_PRD/PRD-01_example/PRD-01_example.md

# Validate all PRD documents in directory
python ai_dev_ssd_flow/02_PRD/scripts/validate_prd.py docs/02_PRD/

# Validate with verbose output
python ai_dev_ssd_flow/02_PRD/scripts/validate_prd.py docs/02_PRD/ --verbose

# Validate with auto-fix (includes structure fixes)
python ai_dev_ssd_flow/02_PRD/scripts/validate_prd.py docs/02_PRD/ --auto-fix

# Cross-document validation
python ai_dev_ssd_flow/scripts/validate_cross_document.py --document docs/02_PRD/PRD-01_slug/PRD-01_slug.md --auto-fix

# Layer-wide validation
python ai_dev_ssd_flow/scripts/validate_cross_document.py --layer PRD --auto-fix
```

---

## Example Invocation

```bash
/doc-prd-audit docs/02_PRD/PRD-01_f1_iam/PRD-01_f1_iam.md
```

Expected outcome:
1. validator runs (internal)
2. reviewer runs (internal)
3. combined audit report generated
4. fixer can execute directly from combined report

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `doc-naming` | Naming standards for element IDs and threshold tags |
| `doc-prd-autopilot` | Invokes this skill in Phase 5 |
| `doc-prd-validator` | **DEPRECATED** - merged into this skill |
| `doc-prd-reviewer` | **DEPRECATED** - merged into this skill |
| `doc-prd-fixer` | Applies fixes based on audit findings |
| `doc-prd` | PRD creation rules |
| `doc-brd-audit` | BRD source validation (unified quality gate) |
| `doc-ears-autopilot` | Downstream consumer |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.3 | 2026-03-02 | **Drift Cache Creation (MANDATORY)**: Added automatic `.drift_cache.json` creation/update after every audit; Schema v1.2 with upstream BRD hash tracking; Aligned with doc-brd-audit drift cache implementation |
| 2.2 | 2026-03-02 | **Element Code Contract Gate (BLOCKING)**: Added element type code validation as blocking gate; `PRD-E020` and `PRD-E022` now fail audit; Added section-element type mapping enforcement; Integrated with `prd_standardized_element_codes_hook.sh` |
| 2.1 | 2026-03-02 | **2-Skill Model**: Deprecated `doc-prd-validator` and `doc-prd-reviewer`; Added Fresh Audit Policy (MANDATORY); All validation and scoring unified in this skill; Aligned with `doc-brd-audit` v2.1 architecture |
| 1.0 | 2026-02-26 | Initial PRD audit wrapper; validator→reviewer orchestration; blocking PRD diagram contract gate; combined report contract for fixer |

## Implementation Plan Consistency (IPLAN-004)

- Treat plan-derived outputs as valid source mode and verify intent preservation from implementation plan scope/objectives.
- Validate upstream autopilot precedence assumption: `--iplan > --ref > --prompt`.
- Flag objective/scope conflicts between plan context and artifact output as blocking issues requiring clarification.
- Do not introduce legacy fallback paths such as `docs-v2.0/00_REF`.

