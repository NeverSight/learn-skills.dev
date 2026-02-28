---
name: doc-ears-validator
description: Validate EARS (Easy Approach to Requirements Syntax) documents against Layer 3 schema standards
metadata:
  tags:
    - sdd-workflow
    - layer-3-artifact
    - quality-assurance
  custom_fields:
    layer: 3
    artifact_type: EARS
    architecture_approaches: [ai-agent-based, traditional-8layer]
    priority: shared
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [EARS]
    downstream_artifacts: []
    version: "1.3"
    last_updated: "2026-02-26"
---

# doc-ears-validator

Validate EARS (Easy Approach to Requirements Syntax) documents against Layer 3 schema standards.

## Activation

Invoke when user requests validation of EARS documents or after creating/modifying EARS artifacts.

## Validation Schema Reference

Schema: `ai_dev_ssd_flow/03_EARS/EARS_MVP_SCHEMA.yaml`
Layer: 3
Artifact Type: EARS

## Validation Checklist

### 0. Folder Structure Validation (BLOCKING)

**Nested Folder Rule**: ALL EARS documents MUST be in nested folders regardless of size.

**Required Structure**:

| EARS Type | Required Location |
|-----------|-------------------|
| Monolithic | `docs/03_EARS/EARS-NN_{slug}/EARS-NN_{slug}.md` |

**Validation**:

```
1. Check document is inside a nested folder: docs/03_EARS/EARS-NN_{slug}/
2. Verify folder name matches EARS ID pattern: EARS-NN_{slug}
3. Verify file name matches folder: EARS-NN_{slug}.md
4. Parent path must be: docs/03_EARS/
```

**Example Valid Structure**:

```
docs/03_EARS/
├── EARS-01_f1_iam/
│   ├── EARS-01_f1_iam.md          ✓ Valid
│   ├── EARS-01.A_audit_report_v001.md
│   ├── EARS-01.R_review_report_v001.md  (legacy)
│   └── .drift_cache.json
├── EARS-02_f2_session/
│   └── EARS-02_f2_session.md      ✓ Valid
```

**Invalid Structure**:

```
docs/03_EARS/
├── EARS-01_f1_iam.md              ✗ NOT in nested folder
```

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| EARS-E020 | ERROR | EARS not in nested folder (BLOCKING) |
| EARS-E021 | ERROR | Folder name doesn't match EARS ID |
| EARS-E022 | ERROR | File name doesn't match folder name |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |

**This check is BLOCKING** - EARS must pass folder structure validation before other checks proceed.

---

### 1. Metadata Validation

```yaml
Required custom_fields:
  - document_type: ["ears", "template"]
  - artifact_type: "EARS"
  - layer: 3
  - architecture_approaches: [array format]
  - priority: ["primary", "shared", "fallback"]
  - development_status: ["active", "draft", "deprecated", "reference"]

Required tags:
  - ears (or ears-template)
  - layer-3-artifact

Forbidden tag patterns:
  - "^ears-requirements$"
  - "^ears-\\d{3}$"
```

### 2. Structure Validation

**Required Sections (6-Section MVP Structure):**
- Title (H1): `# EARS-NN: Title`
- Document Control (unnumbered) - Metadata with BDD-Ready Score
- Section 1: Purpose and Context - Business and technical objectives
- Section 2: EARS in Development Workflow - SDD position and EARS role
- Section 3: Requirements - Event-Driven, State-Driven, Unwanted Behavior, Ubiquitous
- Section 4: Quality Attributes - Performance, Security, Reliability
- Section 5: Traceability - Upstream sources, downstream artifacts, tags
- Section 6: References - Internal and external documentation

**Document Control Required Fields:**
- EARS ID
- Document Name
- Version
- Date Created
- Last Updated
- Author
- Status
- Source PRD

**File Naming:**
Pattern: `EARS-NNN_descriptive_name.md`

### 3. Content Validation

**EARS Requirement Patterns:**

| Type | Pattern | Example |
|------|---------|---------|
| Ubiquitous | The [system] SHALL [action] | The system SHALL log all errors |
| Event-Driven | WHEN [trigger] THE [system] SHALL [action] | WHEN user clicks submit THE system SHALL validate input |
| State-Driven | WHILE [state] THE [system] SHALL [action] | WHILE connected THE system SHALL maintain heartbeat |
| Unwanted | IF [condition] THEN THE [system] SHALL [action] | IF timeout occurs THEN THE system SHALL retry |
| Optional | WHERE [feature] IS SUPPORTED THE [system] SHALL [action] | WHERE dark mode IS SUPPORTED THE system SHALL apply theme |
| Complex | Combination of patterns | WHEN user logs in WHILE session active THE system SHALL refresh token |

**Requirement ID Format:**
- Pattern: `EARS.NN.EE.SS` (4-segment format)
- Example: `EARS.01.24.01`

**BDD-Ready Score:**
- Minimum threshold: 90%
- Components: Pattern compliance, requirement clarity, testability, traceability

### 4. Traceability Validation

**Layer 3 Cumulative Tags:**
- @brd: BRD.NN.01.SS (required)
- @prd: PRD.NN.07.SS (required)

**Downstream Expected:**
- BDD scenarios
- ADR documents
- SYS requirements

**Same-Type References:**
- @related-ears: EARS-NN
- @depends-ears: EARS-NN

## Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| EARS-E001 | error | Missing required tag 'ears' |
| EARS-E002 | error | Missing required tag 'layer-3-artifact' |
| EARS-E003 | error | Invalid document_type |
| EARS-E004 | error | Invalid architecture_approaches format |
| EARS-E005 | error | Forbidden tag pattern detected |
| EARS-E006 | error | Missing required section |
| EARS-E007 | error | Multiple H1 headings detected |
| EARS-E008 | error | Section numbering not sequential |
| EARS-E009 | error | Document Control missing required fields |
| EARS-E010 | error | Invalid EARS pattern detected |
| EARS-E011 | error | Missing Traceability (Section 5) |
| EARS-E012 | warning | File name does not match format |
| EARS-W001 | warning | Requirement not using EARS syntax |
| EARS-W002 | warning | Missing upstream @brd or @prd tag |
| EARS-W003 | warning | BDD-Ready Score below 90% |
| EARS-W004 | warning | Requirement missing SHALL keyword |
| EARS-W005 | warning | Complex requirement too long |
| EARS-I001 | info | Consider adding unwanted behavior handling |
| EARS-I002 | info | Consider adding timing constraints (WITHIN) |

## Validation Commands

```bash
# Validate single EARS document
python ai_dev_ssd_flow/03_EARS/scripts/validate_ears.py docs/03_EARS/EARS-001_example.md

# Validate all EARS documents
python ai_dev_ssd_flow/03_EARS/scripts/validate_ears.py docs/03_EARS/

# Check with verbose output
python ai_dev_ssd_flow/03_EARS/scripts/validate_ears.py docs/03_EARS/ --verbose
```

## Validation Workflow

1. Parse YAML frontmatter
2. Check required metadata fields
3. Validate tag taxonomy
4. Verify section structure (6-section MVP)
5. Validate Document Control table
6. Check EARS pattern compliance
7. Verify SHALL/SHOULD/MAY keywords
8. Validate upstream references
9. Calculate BDD-Ready Score
10. Verify file naming convention
11. Generate validation report

## EARS Pattern Detection

```python
patterns = {
    'ubiquitous': r'^The\s+\[?\w+\]?\s+SHALL\s+',
    'event_driven': r'^WHEN\s+.+\s+THE\s+\[?\w+\]?\s+SHALL\s+',
    'state_driven': r'^WHILE\s+.+\s+THE\s+\[?\w+\]?\s+SHALL\s+',
    'unwanted': r'^IF\s+.+\s+THEN\s+THE\s+\[?\w+\]?\s+SHALL\s+',
    'optional': r'^WHERE\s+.+\s+IS\s+SUPPORTED\s+THE\s+\[?\w+\]?\s+SHALL\s+'
}
```

## Integration

- Invoked by: doc-flow, doc-ears (post-creation)
- Feeds into: trace-check (cross-document validation)
- Reports to: quality-advisor

## Output Format

```
EARS Validation Report
======================
Document: EARS-001_example.md
Status: PASS/FAIL

Pattern Compliance:
- Ubiquitous: N requirements
- Event-Driven: N requirements
- State-Driven: N requirements
- Unwanted: N requirements
- Optional: N requirements

Errors: N
Warnings: N
Info: N

[Details listed by severity]
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.3 | 2026-02-26 | Migrated frontmatter to `metadata`; updated validator command paths to `ai_dev_ssd_flow/03_EARS/scripts`; aligned valid structure examples with audit-wrapper compatibility | System |
| 1.1 | 2026-02-11 | **Nested Folder Rule**: Added Section 0 Folder Structure Validation (BLOCKING); EARS must be in `docs/03_EARS/EARS-NN_{slug}/` folders; Added error codes EARS-E020, EARS-E021, EARS-E022 |
| 1.0 | 2026-02-08 | Initial validator skill definition with YAML frontmatter | System |
