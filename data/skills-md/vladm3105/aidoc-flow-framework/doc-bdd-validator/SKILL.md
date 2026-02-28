---
name: doc-bdd-validator
description: Validate Behavior-Driven Development (BDD) documents against Layer 4 schema standards
metadata:
  tags:
    - sdd-workflow
    - layer-4-artifact
    - quality-assurance
  custom_fields:
    layer: 4
    artifact_type: BDD
    architecture_approaches: [ai-agent-based, traditional-8layer]
    priority: shared
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [BDD]
    downstream_artifacts: []
    version: "1.2"
    last_updated: "2026-02-27"
  versioning_policy: "tracks BDD-MVP-TEMPLATE schema_version"
---

# doc-bdd-validator

Validate Behavior-Driven Development (BDD) documents against Layer 4 schema standards.

## Activation

Invoke when user requests validation of BDD documents or after creating/modifying BDD artifacts.

## Validation Schema Reference

Schema: `ai_dev_ssd_flow/04_BDD/BDD_MVP_SCHEMA.yaml`
Layer: 4
Artifact Type: BDD

## Validation Checklist

### 0. Folder Structure Validation (BLOCKING)

**Nested Folder Rule**: ALL BDD documents MUST be in nested folders regardless of size.

**Required Structure**:

| BDD Type | Required Location |
|----------|-------------------|
| Markdown | `docs/04_BDD/BDD-NN_{slug}/BDD-NN_{slug}.md` |
| Feature | `docs/04_BDD/BDD-NN_{slug}/BDD-NN_{slug}.feature` |

**Validation**:

```
1. Check document is inside a nested folder: docs/04_BDD/BDD-NN_{slug}/
2. Verify folder name matches BDD ID pattern: BDD-NN_{slug}
3. Verify file name matches folder: BDD-NN_{slug}.md or .feature
4. Parent path must be: docs/04_BDD/
```

**Example Valid Structure**:

```
docs/04_BDD/
├── BDD-01_f1_iam/
│   ├── BDD-01_f1_iam.md           ✓ Valid
│   ├── BDD-01_f1_iam.feature      ✓ Valid (optional companion)
│   ├── BDD-01.A_audit_report_v001.md
│   ├── BDD-01.R_review_report_v001.md  (legacy)
│   └── .drift_cache.json
├── BDD-02_f2_session/
│   └── BDD-02_f2_session.md       ✓ Valid
```

**Invalid Structure**:

```
docs/04_BDD/
├── BDD-01_f1_iam.md               ✗ NOT in nested folder
```

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| BDD-E020 | ERROR | BDD not in nested folder (BLOCKING) |
| BDD-E021 | ERROR | Folder name doesn't match BDD ID |
| BDD-E022 | ERROR | File name doesn't match folder name |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |

**This check is BLOCKING** - BDD must pass folder structure validation before other checks proceed.

---

### 1. Metadata Validation

```yaml
Required custom_fields:
  - document_type: ["bdd", "template"]
  - artifact_type: "BDD"
  - layer: 4
  - architecture_approaches: [array format]
  - priority: ["primary", "shared", "fallback"]
  - development_status: ["active", "draft", "deprecated", "reference"]

Required tags:
  - bdd (or bdd-template)
  - layer-4-artifact

Forbidden tag patterns:
  - "^behavior-driven$"
  - "^bdd-\\d{3}$"
```

### 2. Structure Validation

**Required Sections:**
- Title (H1): `# BDD-NNN: Title`
- Document Control (Section 1)
- Feature Overview (Section 2)
- Scenarios (Section 3)
- Scenario Outlines (Section 4)
- Background Steps (Section 5)
- Tags and Hooks (Section 6)
- Test Data (Section 7)
- Traceability (Section 8)
- Change History (Section 9)

**Document Control Required Fields:**
- BDD ID
- Document Name
- Version
- Date Created
- Last Updated
- Author
- Status
- Source EARS

**File Naming:**
Pattern: `BDD-NNN_descriptive_name.md`

### 3. Content Validation

**Gherkin Syntax:**
```gherkin
Feature: [Feature Name]
  As a [role]
  I want [feature]
  So that [benefit]

  Scenario: [Scenario Name]
    Given [context]
    When [action]
    Then [expected outcome]
    And [additional outcome]
```

**Scenario Format:**
- Pattern: `Scenario: Description`
- Required steps: Given, When, Then
- Optional steps: And, But

**Scenario Outline Format:**
```gherkin
Scenario Outline: [Description]
  Given [context with <variable>]
  When [action with <variable>]
  Then [outcome with <variable>]

  Examples:
    | variable | value |
    | data1    | val1  |
```

**ADR-Ready Score:**
- Minimum threshold: 90%
- Components: Scenario coverage, step clarity, data completeness, traceability

### 4. Traceability Validation

**Layer 4 Cumulative Tags:**
- @brd: BRD.NN.01.SS (required)
- @prd: PRD.NN.07.SS (required)
- @ears: EARS.NN.24.SS (required)

**Downstream Expected:**
- ADR documents
- SYS requirements
- Test implementations

**Same-Type References:**
- @related-bdd: BDD-NN
- @depends-bdd: BDD-NN

## Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| BDD-E001 | error | Missing required tag 'bdd' |
| BDD-E002 | error | Missing required tag 'layer-4-artifact' |
| BDD-E003 | error | Invalid document_type |
| BDD-E004 | error | Invalid architecture_approaches format |
| BDD-E005 | error | Forbidden tag pattern detected |
| BDD-E006 | error | Missing required section |
| BDD-E007 | error | Multiple H1 headings detected |
| BDD-E008 | error | Section numbering not sequential |
| BDD-E009 | error | Document Control missing required fields |
| BDD-E010 | error | Invalid Gherkin syntax |
| BDD-E011 | error | Scenario missing Given-When-Then |
| BDD-E012 | error | Missing Traceability (Section 8) |
| BDD-E013 | warning | File name does not match format |
| BDD-W001 | warning | Scenario missing Then step |
| BDD-W002 | warning | Missing upstream tags (@brd, @prd, @ears) |
| BDD-W003 | warning | ADR-Ready Score below 90% |
| BDD-W004 | warning | Scenario Outline missing Examples |
| BDD-W005 | warning | Test data incomplete |
| BDD-I001 | info | Consider adding Background steps |
| BDD-I002 | info | Consider adding negative scenarios |

## Validation Commands

```bash
# Validate single BDD document
python ai_dev_ssd_flow/04_BDD/scripts/validate_bdd.py docs/04_BDD/BDD-001_example.md

# Validate all BDD documents
python ai_dev_ssd_flow/04_BDD/scripts/validate_bdd.py docs/04_BDD/

# Validate .feature files
python ai_dev_ssd_flow/04_BDD/scripts/validate_bdd.py tests/bdd/features/

# Check with verbose output
python ai_dev_ssd_flow/04_BDD/scripts/validate_bdd.py docs/04_BDD/ --verbose
```

## Validation Workflow

1. Parse YAML frontmatter
2. Check required metadata fields
3. Validate tag taxonomy
4. Verify section structure (1-9)
5. Validate Document Control table
6. Check Gherkin syntax compliance
7. Verify Given-When-Then structure
8. Validate Scenario Outline Examples
9. Validate upstream references
10. Calculate ADR-Ready Score
11. Verify file naming convention
12. Generate validation report

## Gherkin Pattern Detection

```python
patterns = {
    'feature': r'^Feature:\s+.+',
    'scenario': r'^Scenario:\s+.+',
    'scenario_outline': r'^Scenario Outline:\s+.+',
    'given': r'^\s*Given\s+.+',
    'when': r'^\s*When\s+.+',
    'then': r'^\s*Then\s+.+',
    'and': r'^\s*And\s+.+',
    'but': r'^\s*But\s+.+',
    'background': r'^Background:',
    'examples': r'^\s*Examples:'
}
```

## Integration

- Invoked by: doc-flow, doc-bdd (post-creation)
- Feeds into: trace-check (cross-document validation)
- Reports to: quality-advisor

## Output Format

```
BDD Validation Report
=====================
Document: BDD-001_example.md
Status: PASS/FAIL

Scenario Summary:
- Total Scenarios: N
- With Given-When-Then: N
- Scenario Outlines: N
- With Examples: N

Errors: N
Warnings: N
Info: N

[Details listed by severity]
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.2 | 2026-02-27 | Migrated frontmatter to `metadata`; updated valid structure example for preferred `BDD-NN.A_audit_report_vNNN.md` with legacy reviewer compatibility; corrected validator command paths to `ai_dev_ssd_flow/04_BDD/scripts` | System |
| 1.1 | 2026-02-11 | **Nested Folder Rule**: Added Section 0 Folder Structure Validation (BLOCKING); BDD must be in `docs/04_BDD/BDD-NN_{slug}/` folders; Added error codes BDD-E020, BDD-E021, BDD-E022 |
| 1.0 | 2026-02-08 | Initial validator skill definition with YAML frontmatter | System |
