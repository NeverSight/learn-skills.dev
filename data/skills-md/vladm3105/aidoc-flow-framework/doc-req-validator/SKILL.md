---
name: doc-req-validator
description: Validate Atomic Requirements (REQ) documents against Layer 7 schema standards
metadata:
  tags:
    - sdd-workflow
    - layer-7-artifact
    - quality-assurance
  custom_fields:
    layer: 7
    artifact_type: REQ
    architecture_approaches: [ai-agent-based, traditional-8layer]
    priority: shared
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [REQ]
    downstream_artifacts: []
    version: "1.2"
    last_updated: "2026-02-27"
  versioning_policy: "tracks REQ_MVP_SCHEMA schema_version"
---

# doc-req-validator

Validate Atomic Requirements (REQ) documents against Layer 7 schema standards.

## Activation

Invoke when user requests validation of REQ documents or after creating/modifying REQ artifacts.

## Validation Schema Reference

Schema: `ai_dev_ssd_flow/07_REQ/REQ_MVP_SCHEMA.yaml`
Layer: 7
Artifact Type: REQ

## Validation Checklist

### 0. Folder Structure Validation (BLOCKING)

**Nested Folder Rule**: ALL REQ documents MUST be in nested folders regardless of size.

**Required Structure**:

| REQ Type | Required Location |
|----------|-------------------|
| Monolithic | `docs/07_REQ/REQ-NN_{slug}/REQ-NN_{slug}.md` |

**Validation**:

```
1. Check document is inside a nested folder: docs/07_REQ/REQ-NN_{slug}/
2. Verify folder name matches REQ ID pattern: REQ-NN_{slug}
3. Verify file name matches folder: REQ-NN_{slug}.md
4. Parent path must be: docs/07_REQ/
```

**Example Valid Structure**:

```
docs/07_REQ/
├── REQ-01_f1_iam/
│   ├── REQ-01_f1_iam.md           ✓ Valid
│   ├── REQ-01.R_review_report_v001.md
│   └── .drift_cache.json
├── REQ-02_f2_session/
│   └── REQ-02_f2_session.md       ✓ Valid
```

**Invalid Structure**:

```
docs/07_REQ/
├── REQ-01_f1_iam.md               ✗ NOT in nested folder
```

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| REQ-E020 | ERROR | REQ not in nested folder (BLOCKING) |
| REQ-E021 | ERROR | Folder name doesn't match REQ ID |
| REQ-E022 | ERROR | File name doesn't match folder name |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |

**This check is BLOCKING** - REQ must pass folder structure validation before other checks proceed.

---

### 1. Metadata Validation

```yaml
Required custom_fields:
  - document_type: ["req", "template"]
  - artifact_type: "REQ"
  - layer: 7
  - architecture_approaches: [array format]
  - priority: ["primary", "shared", "fallback"]
  - development_status: ["active", "draft", "deprecated", "reference"]

Required tags:
  - req (or req-template)
  - layer-7-artifact

Forbidden tag patterns:
  - "^req-document$"
  - "^requirements$"
  - "^atomic-requirements$"
  - "^req-\\d{3}$"
```

### 2. Structure Validation

**Required Sections (11 sections - MVP):**
- Title (H1): `# REQ-NN: [RESOURCE_TYPE] Title`
- Section 1: Document Control
- Section 2: Requirement Description
- Section 3: Functional Specification
- Section 4: Interface Definition
- Section 5: Error Handling
- Section 6: Quality Attributes
- Section 7: Configuration
- Section 8: Testing Requirements
- Section 9: Acceptance Criteria (≥3 measurable criteria)
- Section 10: Traceability
- Section 11: Implementation Notes

**Note**: MVP template intentionally omits Change History to maintain 11-section structure.

**Document Control Required Fields:**
- Status
- Version
- Date Created
- Last Updated
- Author
- Priority
- Category
- Source Document
- Verification Method
- Assigned Team
- SPEC-Ready Score

**File Naming:**
Pattern: `REQ-NNN_descriptive_name.md`

### 3. Content Validation

**Requirement Keywords:**
- SHALL: Mandatory requirement
- SHOULD: Recommended requirement
- MAY: Optional requirement

**Acceptance Criteria Format:**
- Pattern: `AC-NNN`
- Minimum count: 15 criteria
- Categories: Primary Functional (5), Error/Edge Case (5), Quality/Constraint (3), Data Validation (2), Integration (3)

**Interface Specifications:**
- Protocol/ABC definition with type hints
- DTO definitions (dataclass or Pydantic)
- REST endpoints (optional)

**Data Schema Patterns:**
- JSON Schema (draft-07)
- Pydantic BaseModel with validators
- Database schema (optional)

**SPEC-Ready Score:**
- Minimum threshold: 90%
- Components: Interface completeness, data schema, error handling, configuration, quality attributes, implementation guidance, acceptance criteria, traceability

### 4. Traceability Validation

**Layer 7 Cumulative Tags:**
- @brd: BRD.NN.EE.SS (required)
- @prd: PRD.NN.EE.SS (required)
- @ears: EARS.NN.EE.SS (required)
- @bdd: BDD.NN.EE.SS (required)
- @adr: ADR-NN (required)
- @sys: SYS.NN.EE.SS (required)

**Downstream Expected:**
- IMPL documents
- CTR documents
- SPEC documents
- TASKS documents

**Same-Type References:**
- @related-req: REQ-NN
- @depends-req: REQ-NN

## Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| REQ-E001 | error | Missing required tag 'req' |
| REQ-E002 | error | Missing required tag 'layer-7-artifact' |
| REQ-E003 | error | Invalid document_type |
| REQ-E004 | error | Invalid architecture_approaches format |
| REQ-E005 | error | Forbidden tag pattern detected |
| REQ-E006 | error | Missing required section |
| REQ-E007 | error | Multiple H1 headings detected |
| REQ-E008 | error | Section numbering not sequential (1-11) |
| REQ-E009 | error | Document Control missing required fields |
| REQ-E010 | error | Missing Interface Specifications (Section 3) |
| REQ-E011 | error | Missing Data Schemas (Section 4) |
| REQ-E012 | error | Missing Error Handling (Section 5) |
| REQ-E013 | error | Missing Acceptance Criteria (Section 9) |
| REQ-E014 | warning | File name does not match format |
| REQ-E015 | error | Missing Protocol/ABC definition |
| REQ-E016 | error | Missing JSON Schema or Pydantic models |
| REQ-E017 | error | Missing Exception Catalog |
| REQ-W001 | warning | SPEC-Ready Score below 90% |
| REQ-W002 | warning | Acceptance Criteria count below 15 |
| REQ-W003 | warning | Missing upstream tags (require 6) |
| REQ-W004 | warning | Missing Description Context subsections |
| REQ-W005 | warning | Missing Performance targets (p50/p95/p99) |
| REQ-W006 | warning | Missing Implementation Guidance patterns |
| REQ-W007 | warning | Code paths appear to be placeholders |
| REQ-I001 | info | Consider adding database schema |
| REQ-I002 | info | Consider adding REST endpoints |
| REQ-I003 | info | Python code should include type hints |

## Validation Commands

```bash
# Validate single REQ document
./ai_dev_ssd_flow/07_REQ/scripts/validate_req_template.sh docs/07_REQ/REQ-001_example/REQ-001_example.md

# Validate all REQ documents
find docs/07_REQ -name "REQ-*.md" -exec ./ai_dev_ssd_flow/07_REQ/scripts/validate_req_template.sh {} \;

# Check with verbose output
python3 ai_dev_ssd_flow/07_REQ/scripts/validate_req_spec_readiness.py docs/07_REQ/REQ-001_example/REQ-001_example.md --verbose
```

## Validation Workflow

1. Parse YAML frontmatter
2. Check required metadata fields
3. Validate tag taxonomy
4. Verify section structure (1-11)
5. Validate Document Control table
6. Check Interface Specifications (Protocol/ABC)
7. Check Data Schemas (JSON/Pydantic)
8. Check Error Handling (Exception Catalog)
9. Verify Acceptance Criteria count (≥15)
10. Validate upstream references (6 required)
11. Calculate SPEC-Ready Score
12. Verify file naming convention
13. Generate validation report

## Integration

- Invoked by: doc-flow, doc-req (post-creation)
- Feeds into: trace-check (cross-document validation)
- Reports to: quality-advisor

## Output Format

```
REQ Validation Report
=====================
Document: REQ-001_example.md
Status: PASS/FAIL

Interface Coverage:
- Protocol/ABC: Present/Missing
- DTOs: Present/Missing
- REST Endpoints: Present/Missing

Data Schema Coverage:
- JSON Schema: Present/Missing
- Pydantic Models: Present/Missing
- Database Schema: Present/Missing

Acceptance Criteria: N/15

Errors: N
Warnings: N
Info: N

[Details listed by severity]
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.1 | 2026-02-11 | **Nested Folder Rule**: Added Section 0 Folder Structure Validation (BLOCKING); REQ must be in `docs/07_REQ/REQ-NN_{slug}/` folders; Added error codes REQ-E020, REQ-E021, REQ-E022 |
| 1.0 | 2026-02-08 | Initial validator skill definition with YAML frontmatter | System |
