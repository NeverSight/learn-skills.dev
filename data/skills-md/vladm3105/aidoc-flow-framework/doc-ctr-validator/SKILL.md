---
name: doc-ctr-validator
description: Validate Data Contracts (CTR) documents against Layer 8 schema standards
tags:
  - sdd-workflow
  - layer-8-artifact
  - quality-assurance
custom_fields:
  layer: 8
  artifact_type: CTR
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: quality-assurance
  upstream_artifacts: [CTR]
  downstream_artifacts: []
  version: "1.2"
  last_updated: "2026-02-11T18:00:00"
---

# doc-ctr-validator

Validate Data Contracts (CTR) documents against Layer 8 schema standards.

## Activation

Invoke when user requests validation of CTR documents or after creating/modifying CTR artifacts.

## Validation Schema Reference

Schema: `ai_dev_ssd_flow/08_CTR/CTR_SCHEMA.yaml`
Layer: 8
Artifact Type: CTR

## Validation Checklist

### 0. Folder Structure Validation (BLOCKING)

**Nested Folder Rule**: ALL CTR documents MUST be in nested folders regardless of size.

**Required Structure**:

| CTR Type | Required Location |
|----------|-------------------|
| Dual-File | `docs/08_CTR/CTR-NN_{slug}/CTR-NN_{slug}.md` + `CTR-NN_{slug}.yaml` |

**Validation**:

```
1. Check document is inside a nested folder: docs/08_CTR/CTR-NN_{slug}/
2. Verify folder name matches CTR ID pattern: CTR-NN_{slug}
3. Verify both .md and .yaml files exist with matching names
4. Parent path must be: docs/08_CTR/
```

**Example Valid Structure**:

```
docs/08_CTR/
├── CTR-01_f1_iam_api/
│   ├── CTR-01_f1_iam_api.md       ✓ Valid
│   ├── CTR-01_f1_iam_api.yaml     ✓ Valid (companion schema)
│   ├── CTR-01.R_review_report_v001.md
│   └── .drift_cache.json
├── CTR-02_f2_session_api/
│   ├── CTR-02_f2_session_api.md   ✓ Valid
│   └── CTR-02_f2_session_api.yaml ✓ Valid
```

**Invalid Structure**:

```
docs/08_CTR/
├── CTR-01_f1_iam_api.md           ✗ NOT in nested folder
├── CTR-01_f1_iam_api.yaml         ✗ NOT in nested folder
```

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| CTR-E020 | ERROR | CTR not in nested folder (BLOCKING) |
| CTR-E021 | ERROR | Folder name doesn't match CTR ID |
| CTR-E022 | ERROR | File name doesn't match folder name |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |

**This check is BLOCKING** - CTR must pass folder structure validation before other checks proceed.

---

### 1. Metadata Validation

```yaml
Required custom_fields:
  - document_type: ["ctr", "template"]
  - artifact_type: "CTR"
  - layer: 8
  - architecture_approaches: [array format]
  - priority: ["primary", "shared", "fallback"]
  - development_status: ["active", "draft", "deprecated", "reference"]

Required tags:
  - ctr (or ctr-template)
  - layer-8-artifact

Forbidden tag patterns:
  - "^ctr-document$"
  - "^contract$"
  - "^api-contract$"
  - "^ctr-\\d{3}$"
```

### 2. Structure Validation (Dual-File Format)

**File Format:**
- Documentation: `.md` file
- Schema: `.yaml` file
- Pattern: `CTR-NNN_descriptive_name.md` + `CTR-NNN_descriptive_name.yaml`

**Required Sections (12 Sections + 2 Optional Appendices):**

| Section | Title | Required |
|---------|-------|----------|
| Title | `# CTR-NN: Title` (H1) | MANDATORY |
| 1 | Document Control | MANDATORY |
| 2 | Context | MANDATORY |
| 3 | Contract Definition | MANDATORY |
| 4 | Requirements Satisfied | MANDATORY |
| 5 | Interface Definition | MANDATORY |
| 6 | Error Handling | MANDATORY |
| 7 | Quality Attributes | MANDATORY |
| 8 | Versioning Strategy | MANDATORY |
| 9 | Examples | MANDATORY |
| 10 | Verification | MANDATORY |
| 11 | Traceability | MANDATORY |
| 12 | References | MANDATORY |

**Optional Appendices**:
| Section | Title | Required |
|---------|-------|----------|
| Appendix A | Alternatives Considered | OPTIONAL |
| Appendix B | Implementation Notes | OPTIONAL |

**Document Control Required Fields:**
- Project Name
- Document Version
- Date
- Document Owner
- Prepared By
- Status

### 3. Content Validation

**Status Values:**
- Draft
- In Review
- Approved
- Active
- Deprecated

**Communication Patterns:**
- Synchronous: REST, gRPC, GraphQL
- Asynchronous: Event-driven, Message Queue, Pub/Sub

**Error Code Format:**
- Pattern: `^[A-Z_]+$`
- Examples: INVALID_INPUT, INSUFFICIENT_DATA, RATE_LIMITED, SERVICE_UNAVAILABLE, INTERNAL_ERROR

**Versioning:**
- Format: MAJOR.MINOR.PATCH (Semantic versioning)

**YAML Schema Requirements:**
- OpenAPI 3.x or JSON Schema format
- Required: info (title, version, description), paths, components/schemas
- All endpoints must have request and response schemas

### 4. Traceability Validation

**Layer 8 Cumulative Tags:**
- @brd: BRD.NN.EE.SS (required)
- @prd: PRD.NN.EE.SS (required)
- @ears: EARS.NN.EE.SS (required)
- @bdd: BDD.NN.EE.SS (required)
- @adr: ADR-NN (required)
- @sys: SYS.NN.EE.SS (required)
- @req: REQ.NN.EE.SS (required)

**Downstream Expected:**
- SPEC documents
- TASKS documents
- Code (src/...)

**Same-Type References:**
- @related-ctr: CTR-NN
- @depends-ctr: CTR-NN

## Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| CTR-E001 | error | Missing required tag 'ctr' |
| CTR-E002 | error | Missing required tag 'layer-8-artifact' |
| CTR-E003 | error | Invalid document_type |
| CTR-E004 | error | Invalid architecture_approaches format |
| CTR-E005 | error | Forbidden tag pattern detected |
| CTR-E006 | error | Missing required section |
| CTR-E007 | error | Multiple H1 headings detected |
| CTR-E008 | error | Section numbering not sequential (1-12) |
| CTR-E009 | error | Document Control missing required fields |
| CTR-E010 | error | Missing companion YAML schema file |
| CTR-E011 | error | YAML schema is not valid OpenAPI 3.x or JSON Schema |
| CTR-E012 | error | Missing request/response schemas for endpoints |
| CTR-E013 | error | Missing Error Handling section |
| CTR-E014 | warning | File name does not match format |
| CTR-E015 | error | Contract Definition missing Provider/Consumer |
| CTR-E016 | error | Error Codes table missing |
| CTR-W001 | warning | Missing Context Problem Statement |
| CTR-W002 | warning | Missing success/failure examples |
| CTR-W003 | warning | Missing upstream tags (require 7) |
| CTR-W004 | warning | Missing Versioning Strategy Version Policy |
| CTR-W005 | warning | Error responses not defined in YAML schema |
| CTR-W006 | warning | Missing contract testing requirements |
| CTR-I001 | info | Consider adding performance metrics |
| CTR-I002 | info | Consider documenting migration strategy |
| CTR-I003 | info | Consider adding alternative approaches |

## Validation Commands

```bash
# Validate single CTR document (validates both .md and .yaml)
python ai_dev_flow/scripts/validate_ctr.py docs/08_CTR/CTR-001_example.md

# Validate all CTR documents
python ai_dev_flow/scripts/validate_ctr.py docs/08_CTR/

# Check with verbose output
python ai_dev_flow/scripts/validate_ctr.py docs/08_CTR/ --verbose
```

## Validation Workflow

1. Parse YAML frontmatter
2. Check required metadata fields
3. Validate tag taxonomy
4. Verify section structure (1-12)
5. Validate Document Control table
6. Check companion YAML schema file exists
7. Validate YAML schema (OpenAPI 3.x or JSON Schema)
8. Check Error Handling section (Error Codes table)
9. Verify Provider/Consumer in Contract Definition
10. Check Examples section (success and failure)
11. Validate upstream references (7 required)
12. Verify file naming convention
13. Generate validation report

## Integration

- Invoked by: doc-flow, doc-ctr (post-creation)
- Feeds into: trace-check (cross-document validation)
- Reports to: quality-advisor

## Output Format

```
CTR Validation Report
=====================
Document: CTR-001_example.md
Status: PASS/FAIL

Dual-File Check:
- Markdown file: Present
- YAML schema file: Present/Missing
- Schema valid: Yes/No

Contract Structure:
- Provider defined: Yes/No
- Consumer defined: Yes/No
- Error codes table: Present/Missing

Schema Coverage:
- OpenAPI/JSON Schema: Valid/Invalid
- Request schemas: Complete/Incomplete
- Response schemas: Complete/Incomplete
- Error responses: Defined/Missing

Errors: N
Warnings: N
Info: N

[Details listed by severity]
```

## Related Resources

- **CTR Skill**: `.claude/skills/doc-ctr/SKILL.md`
- **Naming Standards**: `.claude/skills/doc-naming/SKILL.md` (ID and naming conventions)
- **CTR Validation Rules**: `ai_dev_ssd_flow/08_CTR/CTR_MVP_VALIDATION_RULES.md`
- **CTR Schema**: `ai_dev_ssd_flow/08_CTR/CTR_SCHEMA.yaml`

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.2 | 2026-02-11 | **Nested Folder Rule**: Added Section 0 Folder Structure Validation (BLOCKING); CTR must be in `docs/08_CTR/CTR-NN_{slug}/` folders; Added error codes CTR-E020, CTR-E021, CTR-E022 |
| 1.1.0 | 2026-02-08 | Updated layer assignment from 9 to 8 per LAYER_REGISTRY v1.6; removed @impl from cumulative tags | System |
| 1.0.0 | 2025-01-15 | Initial validator skill definition | System |
