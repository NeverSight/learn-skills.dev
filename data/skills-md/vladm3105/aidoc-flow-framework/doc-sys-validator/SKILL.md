---
name: doc-sys-validator
description: Validate System Requirements (SYS) documents against Layer 6 schema standards
metadata:
  tags:
    - sdd-workflow
    - layer-6-artifact
    - quality-assurance
  custom_fields:
    layer: 6
    artifact_type: SYS
    architecture_approaches: [ai-agent-based, traditional-8layer]
    priority: shared
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [SYS]
    downstream_artifacts: []
    version: "1.2"
    last_updated: "2026-02-27"
  versioning_policy: "tracks SYS-MVP_SCHEMA schema_version"
---

# doc-sys-validator

Validate System Requirements (SYS) documents against Layer 6 schema standards.

## Activation

Invoke when user requests validation of SYS documents or after creating/modifying SYS artifacts.

## Validation Schema Reference

Schema: `ai_dev_ssd_flow/06_SYS/SYS_MVP_SCHEMA.yaml`
Layer: 6
Artifact Type: SYS

## Validation Checklist

### 0. Folder Structure Validation (BLOCKING)

**Nested Folder Rule**: ALL SYS documents MUST be in nested folders regardless of size.

**Required Structure**:

| SYS Type | Required Location |
|----------|-------------------|
| Monolithic | `docs/06_SYS/SYS-NN_{slug}/SYS-NN_{slug}.md` |

**Validation**:

```
1. Check document is inside a nested folder: docs/06_SYS/SYS-NN_{slug}/
2. Verify folder name matches SYS ID pattern: SYS-NN_{slug}
3. Verify file name matches folder: SYS-NN_{slug}.md
4. Parent path must be: docs/06_SYS/
```

**Example Valid Structure**:

```
docs/06_SYS/
├── SYS-01_f1_iam/
│   ├── SYS-01_f1_iam.md           ✓ Valid
│   ├── SYS-01.R_review_report_v001.md
│   └── .drift_cache.json
├── SYS-02_f2_session/
│   └── SYS-02_f2_session.md       ✓ Valid
```

**Invalid Structure**:

```
docs/06_SYS/
├── SYS-01_f1_iam.md               ✗ NOT in nested folder
```

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| SYS-E020 | ERROR | SYS not in nested folder (BLOCKING) |
| SYS-E021 | ERROR | Folder name doesn't match SYS ID |
| SYS-E022 | ERROR | File name doesn't match folder name |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |

**This check is BLOCKING** - SYS must pass folder structure validation before other checks proceed.

---

### 1. Metadata Validation

```yaml
Required custom_fields:
  - document_type: ["sys", "template"]
  - artifact_type: "SYS"
  - layer: 6
  - architecture_approaches: [array format]
  - priority: ["primary", "shared", "fallback"]
  - development_status: ["active", "draft", "deprecated", "reference"]

Required tags:
  - sys (or sys-template)
  - layer-6-artifact

Forbidden tag patterns:
  - "^system-requirements$"
  - "^sys-doc$"
  - "^sys-\\d{3}$"
```

### 2. Structure Validation

**Required Sections (15 sections):**
- Title (H1): `# SYS-NNN: Title`
- Section 1: Document Control
- Section 2: Executive Summary
- Section 3: Scope (Boundaries, Inclusions, Exclusions)
- Section 4: Functional Requirements (SYS.NN.01.SS format)
- Section 5: Quality Attributes (Performance, Reliability, Security)
- Section 6: Interface Specifications
- Section 7: Data Management
- Section 8: Testing Requirements
- Section 9: Deployment Requirements
- Section 10: Compliance Requirements
- Section 11: Acceptance Criteria
- Section 12: Risk Assessment
- Section 13: Traceability
- Section 14: Implementation Notes
- Section 15: Change History

**Document Control Required Fields:**
- SYS ID
- Document Name
- Version
- Date Created
- Last Updated
- Author
- Reviewer
- Status

**File Naming:**
Pattern: `SYS-NNN_descriptive_name.md`

### 3. Content Validation

**Functional Requirement Format:**
- Pattern: `SYS.NN.01.SS` (unified 4-segment format)
- Table columns: SYS ID, Requirement, Priority, Source, Verification Method
- Element type code: 01 = Functional Requirement
- Priority values: Must Have, Should Have, Could Have, Won't Have

**Quality Attribute Format (4-segment):**
- Pattern: `SYS.NN.02.SS` (02 = Quality Attribute type)
- Example: `SYS.08.02.15`
- Categories: Performance, Reliability, Scalability, Security, Observability, Maintainability

**Quality Attribute Metrics:**

| Category | Keywords | Metrics |
|----------|----------|---------|
| Performance | latency, response time, throughput, p50/p95/p99 | Response Time, Throughput, Latency |
| Reliability | uptime, availability, MTBF, MTTR | Availability, Error Rate |
| Scalability | concurrent, horizontal, vertical | Concurrent Users, Data Volume |
| Security | auth, encrypt, RBAC, compliance | Authentication, Authorization |
| Observability | log, monitor, alert, trace | Logging, Monitoring, Alerting |
| Maintainability | coverage, deploy, CI/CD | Code Coverage, Deploy Frequency |

**REQ-Ready Score:**
- Minimum threshold: 90%
- Components: Functional completeness, quality attributes, interfaces, data management, testing, acceptance criteria, traceability

### 4. Traceability Validation

**Layer 6 Cumulative Tags:**
- @brd: BRD.NN.01.SS (required)
- @prd: PRD.NN.07.SS (required)
- @ears: EARS.NN.24.SS (required)
- @bdd: BDD.NN.13.SS (required)
- @adr: ADR-NN (required)

**Downstream Expected:**
- REQ documents
- SPEC documents
- TASKS documents

**Same-Type References:**
- @related-sys: SYS-NN
- @depends-sys: SYS-NN

## Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| SYS-E001 | error | Missing required tag 'sys' |
| SYS-E002 | error | Missing required tag 'layer-6-artifact' |
| SYS-E003 | error | Invalid document_type |
| SYS-E004 | error | Invalid architecture_approaches format |
| SYS-E005 | error | Forbidden tag pattern detected |
| SYS-E006 | error | Missing required section |
| SYS-E007 | error | Multiple H1 headings detected |
| SYS-E008 | error | Section numbering not sequential (1-15) |
| SYS-E009 | error | Document Control missing required fields |
| SYS-E010 | error | Missing Functional Requirements (Section 4) |
| SYS-E011 | error | Missing Quality Attributes (Section 5) |
| SYS-E012 | error | Missing Traceability (Section 13) |
| SYS-E013 | warning | File name does not match format |
| SYS-W001 | warning | Functional requirements not using SYS.NN.01.SS |
| SYS-W002 | warning | Quality attributes not using 4-segment format |
| SYS-W003 | warning | Missing Performance category |
| SYS-W004 | warning | Missing Security category |
| SYS-W005 | warning | Missing upstream tags (require 5) |
| SYS-W006 | warning | REQ-Ready Score below 90% |
| SYS-W007 | warning | Testing Requirements missing coverage |
| SYS-I001 | info | Consider adding p50/p95/p99 latency |
| SYS-I002 | info | Consider adding MTBF/MTTR metrics |

## Validation Commands

```bash
# Validate single SYS document
python ai_dev_ssd_flow/06_SYS/scripts/validate_sys.py docs/06_SYS/SYS-01_example/SYS-01_example.md

# Validate all SYS documents
python ai_dev_ssd_flow/06_SYS/scripts/validate_sys.py docs/06_SYS/

# Check with verbose output
python ai_dev_ssd_flow/06_SYS/scripts/validate_sys.py docs/06_SYS/ --verbose
```

## Validation Workflow

1. Parse YAML frontmatter
2. Check required metadata fields
3. Validate tag taxonomy
4. Verify section structure (1-15)
5. Validate Document Control table
6. Check functional requirement format
7. Check quality attribute format
8. Verify quality categories coverage
9. Validate upstream references (5 required)
10. Calculate REQ-Ready Score
11. Verify file naming convention
12. Generate validation report

## Integration

- Invoked by: doc-flow, doc-sys (post-creation)
- Feeds into: trace-check (cross-document validation)
- Reports to: quality-advisor

## Output Format

```
SYS Validation Report
=====================
Document: SYS-001_example.md
Status: PASS/FAIL

Quality Attribute Coverage:
- Performance: Present/Missing
- Reliability: Present/Missing
- Security: Present/Missing
- Scalability: Present/Missing
- Observability: Present/Missing

Errors: N
Warnings: N
Info: N

[Details listed by severity]
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.2 | 2026-02-27 | Migrated frontmatter to `metadata`; aligned schema to `SYS_MVP_SCHEMA.yaml`; normalized validation commands to `ai_dev_ssd_flow/06_SYS/scripts/validate_sys.py` | System |
| 1.1 | 2026-02-11 | **Nested Folder Rule**: Added Section 0 Folder Structure Validation (BLOCKING); SYS must be in `docs/06_SYS/SYS-NN_{slug}/` folders; Added error codes SYS-E020, SYS-E021, SYS-E022 |
| 1.0 | 2026-02-08 | Initial validator skill definition with YAML frontmatter | System |
