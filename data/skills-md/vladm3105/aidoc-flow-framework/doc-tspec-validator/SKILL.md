---
name: doc-tspec-validator
description: Validate Test Specification (TSPEC) documents against Layer 10 schema standards
metadata:
  tags:
    - sdd-workflow
    - layer-10-artifact
    - validation
    - shared-architecture
  custom_fields:
    layer: 10
    artifact_type: TSPEC
    architecture_approaches: [ai-agent-based, traditional-8layer]
    priority: shared
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [SPEC]
    downstream_artifacts: [TASKS]
    version: "1.3"
    last_updated: "2026-02-27"
  versioning_policy: "tracks TSPEC-MVP-TEMPLATE schema_version"
---

# doc-tspec-validator

Validate Test Specification (TSPEC) documents against Layer 10 schema standards.

## Purpose

Validates TSPEC documents for:

- YAML frontmatter metadata compliance
- Section structure (test specification sections)
- Document Control completeness
- Cumulative tagging (8 required: @brd, @prd, @ears, @bdd, @adr, @sys, @req, @spec)
- TASKS-Ready scoring
- File naming convention (TSPEC-NN_{slug}.md or {TYPE}-NN_{slug}.md)
- Element ID format (TSPEC.NN.TT.SS where TT is 40-43)
- Test type validation (UTEST/ITEST/STEST/FTEST)

## Activation

Invoke when:

- User requests validation of TSPEC documents
- After creating/modifying TSPEC artifacts
- Before generating downstream artifacts (TASKS)
- As part of quality gate checks
- Validating test coverage matrices

## Schema Reference

| Item | Value |
|------|-------|
| TSPEC Index | `ai_dev_ssd_flow/10_TSPEC/TSPEC-00_index.md` |
| UTEST Template | `ai_dev_ssd_flow/10_TSPEC/UTEST/UTEST-MVP-TEMPLATE.md` |
| ITEST Template | `ai_dev_ssd_flow/10_TSPEC/ITEST/ITEST-MVP-TEMPLATE.md` |
| STEST Template | `ai_dev_ssd_flow/10_TSPEC/STEST/STEST-MVP-TEMPLATE.md` |
| FTEST Template | `ai_dev_ssd_flow/10_TSPEC/FTEST/FTEST-MVP-TEMPLATE.md` |
| Layer | 10 |
| Artifact Type | TSPEC |

## Validation Checklist

### 0. Folder Structure Validation (BLOCKING)

**Nested Folder Rule**: ALL TSPEC documents MUST be in nested folders regardless of size.

**Required Structure**:

| TSPEC Type | Required Location |
|------------|-------------------|
| UTEST | `docs/10_TSPEC/UTEST/UTEST-NN_{slug}/UTEST-NN_{slug}.md` |
| ITEST | `docs/10_TSPEC/ITEST/ITEST-NN_{slug}/ITEST-NN_{slug}.md` |
| STEST | `docs/10_TSPEC/STEST/STEST-NN_{slug}/STEST-NN_{slug}.md` |
| FTEST | `docs/10_TSPEC/FTEST/FTEST-NN_{slug}/FTEST-NN_{slug}.md` |
| PTEST | `docs/10_TSPEC/PTEST/PTEST-NN_{slug}/PTEST-NN_{slug}.md` |
| SECTEST | `docs/10_TSPEC/SECTEST/SECTEST-NN_{slug}/SECTEST-NN_{slug}.md` |

**Validation**:

```
1. Check document is inside a nested folder: docs/10_TSPEC/{TYPE}/{TYPE}-NN_{slug}/
2. Verify folder name matches TSPEC ID pattern: {TYPE}-NN_{slug}
3. Verify file name matches folder: {TYPE}-NN_{slug}.md
4. Parent path must be: docs/10_TSPEC/{TYPE}/
```

**Example Valid Structure**:

```
docs/10_TSPEC/
├── UTEST/
│   ├── UTEST-01_auth_service/
│   │   ├── UTEST-01_auth_service.md   ✓ Valid
│   │   ├── UTEST-01.A_audit_report_v001.md
│   │   ├── UTEST-01.R_review_report_v001.md
│   │   └── .drift_cache.json
│   └── UTEST-02_session_service/
│       └── UTEST-02_session_service.md ✓ Valid
├── ITEST/
│   └── ITEST-01_api_integration/
│       └── ITEST-01_api_integration.md ✓ Valid
├── STEST/
│   └── STEST-01_deployment_smoke/
│       └── STEST-01_deployment_smoke.md ✓ Valid
└── FTEST/
    └── FTEST-01_user_workflow/
        └── FTEST-01_user_workflow.md   ✓ Valid
```

**Invalid Structure**:

```
docs/10_TSPEC/
├── UTEST/
│   ├── UTEST-01_auth_service.md       ✗ NOT in nested folder
```

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| TSPEC-E030 | ERROR | TSPEC not in nested folder (BLOCKING) |
| TSPEC-E031 | ERROR | Folder name doesn't match TSPEC ID |
| TSPEC-E032 | ERROR | File name doesn't match folder name |
| TSPEC-E033 | ERROR | TSPEC not in correct type subdirectory |

**This check is BLOCKING** - TSPEC must pass folder structure validation before other checks proceed.

---

### 1. Metadata Validation

```yaml
Required custom_fields:
  document_type: ["tspec", "utest", "itest", "stest", "ftest", "template"]
  artifact_type: "TSPEC"
  layer: 10
  architecture_approaches: [array format]
  priority: ["primary", "shared", "fallback"]
  development_status: ["active", "draft", "deprecated", "reference"]

Required tags:
  - tspec (or utest, itest, stest, ftest)
  - layer-10-artifact

Forbidden tag patterns:
  - "^test-specification$"
  - "^tspec-\\d{3}$"
  - "^unit-test$"
  - "^integration-test$"
```

### 2. Structure Validation

**Required Sections (Individual Test Type TSPECs - UTEST/ITEST/STEST/FTEST/PTEST/SECTEST)**:

| Section | Title | Required |
|---------|-------|----------|
| 1 | Document Control | MANDATORY |
| 2 | Test Scope | MANDATORY |
| 3 | Test Case Index | MANDATORY |
| 4 | Test Case Details (includes Error Cases) | MANDATORY |
| 5 | Coverage Matrix | MANDATORY |
| 6 | Traceability | MANDATORY |

**Note**: Error Cases are embedded within Section 4 (Test Case Details), not a separate section.

**Section Format**: `## N. Title` (numbered H2 headings)

### 3. Document Control Required Fields

| Field | Description | Required |
|-------|-------------|----------|
| Status | Draft/Review/Approved/Implemented | MANDATORY |
| Version | Semantic versioning (X.Y.Z) | MANDATORY |
| Date Created | YYYY-MM-DD format | MANDATORY |
| Last Updated | YYYY-MM-DD format | MANDATORY |
| Author | Test author name | MANDATORY |
| Component | Component/module under test | MANDATORY |
| SPEC Reference | SPEC-NN | MANDATORY |
| Coverage Target | XX% | MANDATORY |
| TASKS-Ready Score | `XX/100 (Target: see type-specific)` | MANDATORY |

### 4. Test Type Element Codes

| Test Type | Code | Abbreviation | TASKS-Ready Target |
|-----------|------|--------------|-------------------|
| Unit Test | 40 | UTEST | >=90% |
| Integration Test | 41 | ITEST | >=90% |
| Smoke Test | 42 | STEST | 100% |
| Functional Test | 43 | FTEST | >=90% |
| Performance Test | 44 | PTEST | >=85% |
| Security Test | 45 | SECTEST | >=90% |

### 5. Element ID Format

**Pattern**: `TSPEC.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

**Valid Element Type Codes**: 40, 41, 42, 43, 44, 45

**Examples**:

| Element ID | Valid | Test Type |
|------------|-------|-----------|
| `TSPEC.01.40.01` | Yes | Unit Test |
| `TSPEC.01.41.01` | Yes | Integration Test |
| `TSPEC.01.42.01` | Yes | Smoke Test |
| `TSPEC.01.43.01` | Yes | Functional Test |
| `TSPEC.01.44.01` | Yes | Performance Test |
| `TSPEC.01.45.01` | Yes | Security Test |
| `TSPEC.01.46.01` | No | Invalid code (46 not in 40-45) |
| `TC-001` | No | Legacy pattern |
| `UT-001` | No | Legacy pattern |

**Deprecated Patterns (Do NOT use)**:

- `TC-XXX` - Use `TSPEC.NN.TT.SS` instead
- `UT-XXX` - Use `TSPEC.NN.40.SS` instead
- `IT-XXX` - Use `TSPEC.NN.41.SS` instead
- `ST-XXX` - Use `TSPEC.NN.42.SS` instead
- `FT-XXX` - Use `TSPEC.NN.43.SS` instead

### 6. Naming Compliance (doc-naming integration)

**File Naming Patterns**:

| Pattern | Example | Document Type |
|---------|---------|---------------|
| `UTEST-NN_{slug}.md` | `UTEST-01_auth_service_unit.md` | Unit Test |
| `ITEST-NN_{slug}.md` | `ITEST-01_api_integration.md` | Integration Test |
| `STEST-NN_{slug}.md` | `STEST-01_deployment_smoke.md` | Smoke Test |
| `FTEST-NN_{slug}.md` | `FTEST-01_order_processing.md` | Functional Test |

**Directory Structure**:

```
docs/10_TSPEC/
  UTEST/
    UTEST-01_{slug}.md
  ITEST/
    ITEST-01_{slug}.md
  STEST/
    STEST-01_{slug}.md
  FTEST/
    FTEST-01_{slug}.md
  TSPEC-00_TRACEABILITY_MATRIX.md
```

### 7. Cumulative Tagging Requirements

**Layer 10 Cumulative Tags (8 Required)**:

```markdown
@brd: BRD.NN.TT.SS
@prd: PRD.NN.TT.SS
@ears: EARS.NN.25.SS
@bdd: BDD.NN.14.SS
@adr: ADR-NN
@sys: SYS.NN.26.SS
@req: REQ.NN.27.SS
@spec: SPEC-NN
```

**Optional (9th tag if CTR exists)**:

```markdown
@ctr: CTR-NN
```

**Tag Format Convention**:

| Notation | Format | Artifacts |
|----------|--------|-----------|
| Dash | TYPE-NN | ADR, SPEC, CTR |
| Dot | TYPE.NN.TT.SS | BRD, PRD, EARS, BDD, SYS, REQ, TSPEC |

### 8. Test Case Format Requirements

Each test case MUST include:

```markdown
### TSPEC.NN.TT.SS: [Test Name]

**Category**: [Logic] | [State] | [Validation] | [Edge] | [Integration] | [Critical Path]

**Traceability**:
- @req: REQ.NN.27.XX
- @spec: SPEC-NN (Section X.Y)

**Input/Output Table**:

| Input | Expected Output | Notes |
|-------|-----------------|-------|
| `param1="valid"` | `True` | Happy path |
| `param1=""` | `ValidationError` | Empty input |

**Pseudocode**:
GIVEN valid input parameters
WHEN function_under_test(param1) is called
THEN result equals expected_output
AND no side effects occur

**Error Cases**:

| Error Condition | Expected Behavior |
|-----------------|-------------------|
| Invalid input type | Raise `TypeError` |
```

### 9. Coverage Matrix Validation

**Required Format**:

```markdown
## Coverage Matrix

| REQ ID | REQ Title | Test IDs | Coverage |
|--------|-----------|----------|----------|
| REQ.NN.27.01 | [Title] | TSPEC.NN.40.01, TSPEC.NN.40.03 | Covered |
| REQ.NN.27.02 | [Title] | - | NOT COVERED |

**Coverage Summary**:
- Total REQ elements: [N]
- Covered: [N]
- Coverage: [XX]%
```

### 10. Type-Specific Requirements

#### UTEST (Unit Tests - Code 40)

| Requirement | Value |
|-------------|-------|
| TASKS-Ready Target | >=90% |
| Required Tags | @req, @spec |
| Test Categories | [Logic], [State], [Validation], [Edge] |
| Function Coverage | >=90% |
| Branch Coverage | >=80% |

#### ITEST (Integration Tests - Code 41)

| Requirement | Value |
|-------------|-------|
| TASKS-Ready Target | >=90% |
| Required Tags | @ctr, @sys, @spec |
| Test Categories | [Integration], [Contract], [Sequence] |
| Sequence Diagrams | Required for complex interactions |
| Mock Strategy | Must be documented |

#### STEST (Smoke Tests - Code 42)

| Requirement | Value |
|-------------|-------|
| TASKS-Ready Target | 100% |
| Required Tags | @ears, @bdd, @req |
| Test Categories | [Critical Path], [Health Check], [Deployment] |
| Execution Time | <5 minutes total |
| Critical Path Coverage | 100% |

#### FTEST (Functional Tests - Code 43)

| Requirement | Value |
|-------------|-------|
| TASKS-Ready Target | >=90% |
| Required Tags | @sys, @threshold |
| Test Categories | [Functional], [Scenario], [End-to-End] |
| SYS Coverage | Required |
| Threshold References | Must include @threshold tags |

## Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| TSPEC-E001 | ERROR | Missing required tag 'tspec' (or type-specific: utest/itest/stest/ftest) |
| TSPEC-E002 | ERROR | Missing required tag 'layer-10-artifact' |
| TSPEC-E003 | ERROR | Invalid document_type value |
| TSPEC-E004 | ERROR | Invalid architecture_approaches format (must be array) |
| TSPEC-E005 | ERROR | Forbidden tag pattern detected |
| TSPEC-E006 | ERROR | Missing required section |
| TSPEC-E007 | ERROR | Multiple H1 headings detected |
| TSPEC-E008 | ERROR | Section numbering not sequential |
| TSPEC-E009 | ERROR | Document Control missing required fields |
| TSPEC-E010 | ERROR | Missing Test Case Details (Section 4) |
| TSPEC-E011 | ERROR | Invalid element type code (must be 40-43) |
| TSPEC-E012 | ERROR | Missing cumulative tags (requires 8: @brd through @spec) |
| TSPEC-E013 | ERROR | Invalid element ID format (not TSPEC.NN.TT.SS) |
| TSPEC-E014 | ERROR | Missing upstream @spec tag |
| TSPEC-E015 | ERROR | Missing Coverage Matrix (Section 5) |
| TSPEC-E016 | ERROR | Missing SPEC Reference in Document Control |
| TSPEC-E017 | ERROR | Deprecated ID pattern used (TC-XXX, UT-XXX, IT-XXX, ST-XXX, FT-XXX) |
| TSPEC-E018 | ERROR | Element type code mismatch (e.g., using 40 in ITEST document) |
| TSPEC-E019 | ERROR | Missing I/O table for test case |
| TSPEC-E020 | ERROR | Missing traceability section |
| TSPEC-W001 | WARNING | File name does not match format {TYPE}-NN_{slug}.md |
| TSPEC-W002 | WARNING | Missing pseudocode for complex test case |
| TSPEC-W003 | WARNING | TASKS-Ready Score below type-specific target |
| TSPEC-W004 | WARNING | Coverage percentage below target |
| TSPEC-W005 | WARNING | Missing error cases documentation |
| TSPEC-W006 | WARNING | Missing test fixtures documentation |
| TSPEC-W007 | WARNING | Missing mock strategy (ITEST only) |
| TSPEC-W008 | WARNING | Execution time exceeds 5 minutes (STEST only) |
| TSPEC-W009 | WARNING | Missing @threshold tags (FTEST only) |
| TSPEC-W010 | WARNING | Missing sequence diagrams for complex interactions (ITEST only) |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |
| TSPEC-I001 | INFO | Consider adding performance targets for test execution |
| TSPEC-I002 | INFO | Consider adding test data setup documentation |
| TSPEC-I003 | INFO | Consider adding CI/CD integration notes |

## Validation Commands

```bash
# Validate by type
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_utest.py docs/10_TSPEC/UTEST/
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_itest.py docs/10_TSPEC/ITEST/
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_stest.py docs/10_TSPEC/STEST/
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_ftest.py docs/10_TSPEC/FTEST/
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_ptest.py docs/10_TSPEC/PTEST/
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_sectest.py docs/10_TSPEC/SECTEST/

# Validate all TSPEC types
bash ai_dev_ssd_flow/10_TSPEC/scripts/validate_all_tspec.sh docs/10_TSPEC/

# Quality score validation
bash ai_dev_ssd_flow/10_TSPEC/scripts/validate_tspec_quality_score.sh docs/10_TSPEC/

# Cross-document validation
python ai_dev_ssd_flow/scripts/validate_cross_document.py --document docs/10_TSPEC/UTEST/UTEST-01.md --auto-fix

# Cumulative tagging validation
python ai_dev_ssd_flow/scripts/validate_tags_against_docs.py \
  --artifact UTEST-01 \
  --expected-layers brd,prd,ears,bdd,adr,sys,req,spec \
  --strict
```

## Validation Workflow

1. Parse YAML frontmatter
2. Check required metadata fields (document_type, artifact_type, layer)
3. Validate tag taxonomy (tspec/utest/itest/stest/ftest, layer-10-artifact)
4. Verify section structure (6 required sections)
5. Validate Document Control table completeness
6. Check SPEC Reference presence
7. Validate element ID format (TSPEC.NN.TT.SS)
8. Verify element type code matches document type:
   - UTEST: code 40
   - ITEST: code 41
   - STEST: code 42
   - FTEST: code 43
9. Validate cumulative tags (8 required: @brd through @spec)
10. Check Coverage Matrix completeness
11. Validate I/O tables present for all test cases
12. Check pseudocode for complex tests
13. Verify error cases documented
14. Calculate TASKS-Ready Score
15. Verify file naming convention
16. Detect deprecated patterns (TC-XXX, UT-XXX, etc.)
17. Run type-specific validations
18. Generate validation report

## Auto-Fix Actions

| Issue | Auto-Fix Action |
|-------|-----------------|
| Missing cumulative tags | Add with upstream document reference |
| Invalid element ID format | Convert to TSPEC.NN.TT.SS format |
| Missing traceability section | Insert from template |
| Missing Document Control fields | Add placeholder fields |
| Deprecated ID patterns | Convert to unified format (TC-001 to TSPEC.NN.TT.01) |
| Wrong element type code | Correct based on document type (UTEST=40, ITEST=41, etc.) |
| Missing Coverage Matrix | Insert template structure |
| Missing TASKS-Ready Score | Calculate and insert |

## Integration

- **Invoked by**: doc-flow, doc-tspec (post-creation), quality-advisor
- **Invoked by**: doc-flow, doc-tspec (post-creation), quality-advisor, doc-tspec-audit
- **Feeds into**: trace-check (cross-document validation)
- **Reports to**: quality-advisor
- **Validates output from**: doc-tspec skill

## Output Format

```
TSPEC Validation Report
=======================
Document: UTEST-01_auth_service_unit.md
Type: UTEST (Unit Test)
Status: PASS/FAIL

TASKS-Ready Score: 92% (Target: >=90%) [PASS]

Cumulative Tags:
  @brd: BRD.01.01.01 [PRESENT]
  @prd: PRD.01.07.01 [PRESENT]
  @ears: EARS.01.25.01 [PRESENT]
  @bdd: BDD.01.14.01 [PRESENT]
  @adr: ADR-01 [PRESENT]
  @sys: SYS.01.26.01 [PRESENT]
  @req: REQ.01.27.01 [PRESENT]
  @spec: SPEC-01 [PRESENT]
  Tags: 8/8 [COMPLETE]

Coverage Summary:
  REQ Elements: 15/18 covered (83%)
  Target: >=90%
  Status: [BELOW TARGET]

Test Cases: 12
  Element IDs Valid: 12/12
  I/O Tables Present: 11/12
  Pseudocode Present: 10/12

Errors: 0
Warnings: 3
Info: 1

[TSPEC-W002] WARNING: Missing pseudocode for TSPEC.01.40.05
[TSPEC-W004] WARNING: Coverage percentage (83%) below target (90%)
[TSPEC-W019] WARNING: Missing I/O table for TSPEC.01.40.12
[TSPEC-I002] INFO: Consider adding test data setup documentation
```

## Related Resources

- **TSPEC Skill**: `.claude/skills/doc-tspec/SKILL.md`
- **Naming Standards**: `.claude/skills/doc-naming/SKILL.md` (element IDs, element type codes)
- **Quality Advisor**: `.claude/skills/quality-advisor/SKILL.md`
- **TSPEC Index**: `ai_dev_ssd_flow/10_TSPEC/TSPEC-00_index.md`
- **Traceability Matrix Template**: `ai_dev_ssd_flow/10_TSPEC/TSPEC-00_TRACEABILITY_MATRIX-TEMPLATE.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`

### Templates

- `ai_dev_ssd_flow/10_TSPEC/UTEST/UTEST-MVP-TEMPLATE.md`
- `ai_dev_ssd_flow/10_TSPEC/ITEST/ITEST-MVP-TEMPLATE.md`
- `ai_dev_ssd_flow/10_TSPEC/STEST/STEST-MVP-TEMPLATE.md`
- `ai_dev_ssd_flow/10_TSPEC/FTEST/FTEST-MVP-TEMPLATE.md`

### Quality Gates

- `ai_dev_ssd_flow/10_TSPEC/UTEST/UTEST_MVP_QUALITY_GATES.md`
- `ai_dev_ssd_flow/10_TSPEC/ITEST/ITEST_MVP_QUALITY_GATES.md`
- `ai_dev_ssd_flow/10_TSPEC/STEST/STEST_MVP_QUALITY_GATES.md`
- `ai_dev_ssd_flow/10_TSPEC/FTEST/FTEST_MVP_QUALITY_GATES.md`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3 | 2026-02-27 | Normalized frontmatter to `metadata` schema with `versioning_policy`; replaced legacy monolithic validator command examples with type-specific validators + `validate_all_tspec.sh`; aligned cross-document/tag validation references to `ai_dev_ssd_flow/scripts/*`; added audit-report example path compatibility |
| 1.2 | 2026-02-26 | Added PTEST (code 44) and SECTEST (code 45) validation; Fixed template paths to ai_dev_ssd_flow/10_TSPEC/; Updated section count from 7 to 6 (Error Cases in Section 4); Added PTEST/SECTEST to nested folder table |
| 1.1 | 2026-02-11 | **Nested Folder Rule**: Added Section 0 Folder Structure Validation (BLOCKING); TSPEC must be in `docs/10_TSPEC/{TYPE}/{TYPE}-NN_{slug}/` folders; Added error codes TSPEC-E030 through TSPEC-E033 |
| 1.0 | 2026-02-08 | Initial release: Full TSPEC validation for UTEST/ITEST/STEST/FTEST (codes 40-43), cumulative tagging (8 required), type-specific requirements, doc-naming integration |
