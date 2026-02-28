---
name: doc-tspec
description: Create Test Specifications (TSPEC) - Layer 10 artifact for unit, integration, smoke, and functional test cases
metadata:
  tags:
    - sdd-workflow
    - layer-10-artifact
    - shared-architecture
  custom_fields:
    layer: 10
    artifact_type: TSPEC
    architecture_approaches: [ai-agent-based, traditional-8layer]
    priority: shared
    development_status: active
    skill_category: core-workflow
    upstream_artifacts: [BRD, PRD, EARS, BDD, ADR, SYS, REQ, CTR, SPEC]
    downstream_artifacts: [TASKS, Code]
    version: "1.2"
    last_updated: "2026-02-27"
  versioning_policy: "tracks TSPEC-MVP-TEMPLATE schema_version"
---

# doc-tspec

## Purpose

Create **Test Specifications (TSPEC)** - Layer 10 artifact in the SDD workflow that defines test cases for Test-Driven Development (TDD) between SPEC (Layer 9) and TASKS (Layer 11).

**Layer**: 10

**Upstream**: BRD (Layer 1), PRD (Layer 2), EARS (Layer 3), BDD (Layer 4), ADR (Layer 5), SYS (Layer 6), REQ (Layer 7), CTR (Layer 8), SPEC (Layer 9)

**Downstream Artifacts**: TASKS (Layer 11), Code (Layer 12)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating this document, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/01_BRD/ docs/02_PRD/ docs/03_EARS/ docs/04_BDD/ docs/05_ADR/ docs/06_SYS/ docs/07_REQ/ docs/08_CTR/ docs/09_SPEC/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags
3. **Use `null`** only when upstream artifact type genuinely doesn't exist
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`
5. **Do NOT create missing upstream artifacts** - skip functionality instead


Before creating TSPEC, read:

1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Upstream SPEC**: Read technical specifications (PRIMARY SOURCE)
3. **Upstream REQ**: Read atomic requirements
4. **Template by Type**:
   - UTEST: `ai_dev_ssd_flow/10_TSPEC/UTEST/UTEST-MVP-TEMPLATE.md`
   - ITEST: `ai_dev_ssd_flow/10_TSPEC/ITEST/ITEST-MVP-TEMPLATE.md`
   - STEST: `ai_dev_ssd_flow/10_TSPEC/STEST/STEST-MVP-TEMPLATE.md`
   - FTEST: `ai_dev_ssd_flow/10_TSPEC/FTEST/FTEST-MVP-TEMPLATE.md`
5. **TSPEC README**: `ai_dev_ssd_flow/10_TSPEC/README.md`

## When to Use This Skill

Use `doc-tspec` when:
- Have completed BRD through SPEC (Layers 1-9)
- Ready to define test cases before implementation
- Following Test-Driven Development workflow
- Need to specify unit, integration, smoke, or functional tests
- You are at Layer 10 of the SDD workflow

## Reserved ID Exemption (TSPEC-00_*)

**Scope**: Documents with reserved ID `000` are FULLY EXEMPT from validation.

**Pattern**: `TSPEC-00_*.md`, `{TYPE}-00_*.md` (where TYPE is UTEST/ITEST/STEST/FTEST)

**Document Types**:
- Index documents (`TSPEC-00_index.md`)
- Traceability matrix templates (`TSPEC-00_TRACEABILITY_MATRIX-TEMPLATE.md`)
- Glossaries, registries, checklists

**Rationale**: Reserved ID 000 documents are framework infrastructure (indexes, templates, reference materials), not project artifacts requiring traceability or quality gates.

**Validation Behavior**: Skip all checks when filename matches `TSPEC-00_*` or `{TYPE}-00_*` pattern.

## Element ID Format (MANDATORY)

**Pattern**: `TSPEC.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Test Category | Example |
|--------------|------|---------------|---------|
| Unit Test Case | 40 | UTEST | TSPEC.01.40.01 |
| Integration Test Case | 41 | ITEST | TSPEC.01.41.01 |
| Smoke Test Case | 42 | STEST | TSPEC.01.42.01 |
| Functional Test Case | 43 | FTEST | TSPEC.01.43.01 |
| Performance Test Case | 44 | PTEST | TSPEC.01.44.01 |
| Security Test Case | 45 | SECTEST | TSPEC.01.45.01 |

> **REMOVED PATTERNS** - Do NOT use legacy formats:
> - `TC-XXX` - Use `TSPEC.NN.TT.SS` instead
> - `UT-XXX` - Use `TSPEC.NN.40.SS` instead
> - `IT-XXX` - Use `TSPEC.NN.41.SS` instead
> - `ST-XXX` - Use `TSPEC.NN.42.SS` instead
> - `FT-XXX` - Use `TSPEC.NN.43.SS` instead

**Reference**: [doc-naming skill](../doc-naming/SKILL.md) for complete element type codes.

## TSPEC Types Overview

| Type | Code | Abbreviation | Purpose | Primary Source |
|------|------|--------------|---------|----------------|
| Unit Test | 40 | UTEST | Individual function/method tests | REQ (L7), SPEC (L9) |
| Integration Test | 41 | ITEST | Component interaction tests | CTR (L8), SYS (L6) |
| Smoke Test | 42 | STEST | Post-deployment health checks | EARS (L3), BDD (L4) |
| Functional Test | 43 | FTEST | System behavior validation | SYS (L6) |
| Performance Test | 44 | PTEST | Load, stress, and response time testing | SYS (L6), SPEC (L9) |
| Security Test | 45 | SECTEST | Vulnerability and threat testing | SYS (L6), ADR (L5) |

**Note**: Acceptance tests remain in BDD (Layer 4), not duplicated in TSPEC.

## TSPEC-Specific Guidance

### 1. Test Document Structure

**Directory Structure**:
```
docs/10_TSPEC/
├── UTEST/
│   ├── UTEST-01_{component}_unit.md
│   └── UTEST-02_{component}_unit.md
├── ITEST/
│   ├── ITEST-01_{component}_integration.md
│   └── ITEST-02_{component}_integration.md
├── STEST/
│   ├── STEST-01_{component}_smoke.md
│   └── STEST-02_{component}_smoke.md
├── FTEST/
│   ├── FTEST-01_{component}_functional.md
│   └── FTEST-02_{component}_functional.md
└── TSPEC-00_TRACEABILITY_MATRIX.md
```

### 2. Required Sections (All TSPEC Types)

**Document Control** (MANDATORY - First section):

| Item | Details |
|------|---------|
| Status | Draft / Review / Approved / Implemented |
| Version | 0.1.0 |
| Date Created | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |
| Author | [Author name] |
| Component | [Component/module name] |
| SPEC Reference | SPEC-NN |
| Coverage Target | XX% |
| TASKS-Ready Score | [XX]% (Target: see type-specific) |

**Core Sections**:
1. **Document Control**: Metadata and version tracking
2. **Test Scope**: Component under test, categories, dependencies
3. **Test Case Index**: Summary table of all test cases
4. **Test Case Details**: Full specification per test case
5. **Coverage Matrix**: REQ/SPEC coverage tracking
6. **Traceability**: Cumulative upstream/downstream tags

### 3. Test Case Format

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

```
GIVEN valid input parameters
WHEN function_under_test(param1) is called
THEN result equals expected_output
AND no side effects occur
```

**Error Cases**:

| Error Condition | Expected Behavior |
|-----------------|-------------------|
| Invalid input type | Raise `TypeError` |
```

### 4. Type-Specific Requirements

#### UTEST (Unit Tests - Code 40)

**TASKS-Ready Score Target**: >=90%

**Required Tags**: `@req`, `@spec`

**Test Categories**: [Logic], [State], [Validation], [Edge]

**Coverage Requirements**:
- Function coverage: >=90%
- Branch coverage: >=80%
- REQ element coverage: >=90%

#### ITEST (Integration Tests - Code 41)

**TASKS-Ready Score Target**: >=90%

**Required Tags**: `@ctr`, `@sys`, `@spec`

**Test Categories**: [Integration], [Contract], [Sequence]

**Requirements**:
- Sequence diagrams for complex interactions
- CTR contract validation
- Mock/stub strategy documented

#### STEST (Smoke Tests - Code 42)

**TASKS-Ready Score Target**: 100%

**Required Tags**: `@ears`, `@bdd`, `@req`

**Test Categories**: [Critical Path], [Health Check], [Deployment]

**Requirements**:
- Total execution time <5 minutes
- Rollback procedures documented
- Critical path coverage 100%

#### FTEST (Functional Tests - Code 43)

**TASKS-Ready Score Target**: >=90%

**Required Tags**: `@sys`, `@threshold`

**Test Categories**: [Functional], [Scenario], [End-to-End]

**Requirements**:
- SYS requirement coverage
- Threshold registry references for performance assertions

### 5. Coverage Matrix Format

```markdown
## Coverage Matrix

| REQ ID | REQ Title | Test IDs | Coverage |
|--------|-----------|----------|----------|
| REQ.NN.27.01 | [Title] | TSPEC.NN.40.01, TSPEC.NN.40.03 | Covered |
| REQ.NN.27.02 | [Title] | TSPEC.NN.40.02 | Covered |
| REQ.NN.27.03 | [Title] | - | NOT COVERED |

**Coverage Summary**:
- Total REQ elements: [N]
- Covered: [N]
- Coverage: [XX]%
```

## Cumulative Tagging Requirements

**Layer 10 (TSPEC)**: Must include tags from Layers 1-9

**Tag Count**: 8 required tags (minimum), 9 if CTR created

### Element Type Codes for Cumulative Tags

| Artifact | Element Type | Code | Example |
|----------|--------------|------|---------|
| BRD | Business Requirement | 01 | BRD.01.01.03 |
| PRD | Product Feature | 07 | PRD.01.07.02 |
| EARS | EARS Statement | 25 | EARS.01.25.01 |
| BDD | Scenario | 14 | BDD.01.14.01 |
| ADR | Document reference | - | ADR-033 (dash notation) |
| SYS | System Requirement | 26 | SYS.01.26.01 |
| REQ | Atomic Requirement | 27 | REQ.01.27.01 |
| SPEC | Document reference | - | SPEC-01 (dash notation) |

**Minimum (8 tags - CTR skipped)**:
```markdown
## Traceability

**Required Tags** (Cumulative Tagging Hierarchy - Layer 10):

@brd: BRD.01.01.03
@prd: PRD.01.07.02
@ears: EARS.01.25.01
@bdd: BDD.01.14.01
@adr: ADR-033, ADR-045
@sys: SYS.01.26.01
@req: REQ.01.27.01
@spec: SPEC-01
```

**Maximum (9 tags - CTR included)**:
```markdown
@brd: BRD.01.01.03
@prd: PRD.01.07.02
@ears: EARS.01.25.01
@bdd: BDD.01.14.01
@adr: ADR-033, ADR-045
@sys: SYS.01.26.01
@req: REQ.01.27.01
@ctr: CTR-01
@spec: SPEC-01
```

## Tag Format Convention (By Design)

The SDD framework uses two distinct notation systems for cross-references:

| Notation | Format | Artifacts | Purpose |
|----------|--------|-----------|---------|
| Dash | TYPE-NN | ADR, SPEC, CTR | Technical artifacts - references to files/documents |
| Dot | TYPE.NN.TT.SS | BRD, PRD, EARS, BDD, SYS, REQ, TSPEC | Hierarchical artifacts - references to elements inside documents |

**Key Distinction**:
- `@adr: ADR-033` - Points to the document `ADR-033_risk_limit_enforcement.md`
- `@brd: BRD.17.01.01` - Points to element 01.01 inside document `BRD-017.md`

## Validation Checks

### Tier 1: Errors (Blocking)

| Check | Description |
|-------|-------------|
| CHECK 1 | Filename format valid ({TYPE}-NN_{slug}.md) |
| CHECK 2 | YAML frontmatter present with required fields |
| CHECK 3 | Document Control table complete |
| CHECK 4 | All required sections present |
| CHECK 5 | Element ID format compliance (TSPEC.NN.TT.SS) |
| CHECK 6 | Element type code matches document type (40/41/42/43) |
| CHECK 7 | All 8 required traceability tags present |
| CHECK 8 | Parent SPEC reference valid and file exists |

### Tier 2: Warnings

| Check | Description |
|-------|-------------|
| CHECK W1 | I/O table present for each test case |
| CHECK W2 | Pseudocode provided for complex tests |
| CHECK W3 | Coverage matrix complete |
| CHECK W4 | TASKS-Ready Score meets type-specific target |
| CHECK W5 | Error cases documented |

### Tier 3: Info

| Check | Description |
|-------|-------------|
| CHECK I1 | Test fixtures documented |
| CHECK I2 | Mock strategy specified |
| CHECK I3 | Performance targets defined (FTEST) |

## Creation Process

### Step 1: Identify Test Type Needed

Determine which TSPEC type(s) to create based on requirements:
- UTEST for unit testing individual functions
- ITEST for component integration testing
- STEST for deployment health verification
- FTEST for system behavior validation

### Step 2: Read Upstream Artifacts

Focus on SPEC (Layer 9) and REQ (Layer 7) as primary sources.

### Step 3: Reserve ID Number

Check `docs/10_TSPEC/{TYPE}/` for next available ID number.

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- Correct: UTEST-01, ITEST-02, STEST-99
- Incorrect: UTEST-001, ITEST-009 (extra leading zero not required)

### Step 4: Create TSPEC File

**File naming**: `docs/10_TSPEC/{TYPE}/{TYPE}-NN_{slug}.md`

**Examples**:
- `docs/10_TSPEC/UTEST/UTEST-01_auth_service_unit.md`
- `docs/10_TSPEC/ITEST/ITEST-01_api_integration.md`
- `docs/10_TSPEC/STEST/STEST-01_deployment_smoke.md`
- `docs/10_TSPEC/FTEST/FTEST-01_order_processing_functional.md`

### Step 5: Fill Document Control Section

Complete metadata including SPEC Reference and TASKS-Ready Score.

### Step 6: Define Test Scope

Document component under test, test categories, and dependencies.

### Step 7: Create Test Case Index

Summary table listing all test cases with priority.

### Step 8: Write Test Case Details

For each test case:
- Assign Element ID (TSPEC.NN.TT.SS)
- Define category
- Add traceability tags
- Create I/O table
- Write pseudocode
- Document error cases

### Step 9: Build Coverage Matrix

Map test cases to REQ elements, calculate coverage percentage.

### Step 10: Add Cumulative Tags

Include all 8-9 upstream tags (@brd through @spec).

### Step 11: Create/Update Traceability Matrix

**MANDATORY**: Update `docs/10_TSPEC/TSPEC-00_TRACEABILITY_MATRIX.md`

### Step 12: Validate TSPEC

```bash
# Type-specific validation
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_utest.py docs/10_TSPEC/UTEST/UTEST-01_*.md
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_itest.py docs/10_TSPEC/ITEST/ITEST-01_*.md
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_stest.py docs/10_TSPEC/STEST/STEST-01_*.md
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_ftest.py docs/10_TSPEC/FTEST/FTEST-01_*.md

# Combined quality score
bash ai_dev_ssd_flow/10_TSPEC/scripts/validate_tspec_quality_score.sh docs/10_TSPEC/

# Cumulative tagging validation
python ai_dev_ssd_flow/scripts/validate_tags_against_docs.py \
  --artifact UTEST-01 \
  --expected-layers brd,prd,ears,bdd,adr,sys,req,spec \
  --strict
```

### Step 13: Commit Changes

Commit TSPEC file and traceability matrix.

## Validation

### Automated Validation

```bash
# All TSPEC types
bash ai_dev_ssd_flow/10_TSPEC/scripts/validate_all_tspec.sh docs/10_TSPEC/

# Type-specific validation
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_utest.py docs/10_TSPEC/UTEST/*.md
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_itest.py docs/10_TSPEC/ITEST/*.md
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_stest.py docs/10_TSPEC/STEST/*.md
python ai_dev_ssd_flow/10_TSPEC/scripts/validate_ftest.py docs/10_TSPEC/FTEST/*.md

# Cross-document validation
python ai_dev_ssd_flow/scripts/validate_cross_document.py --document docs/10_TSPEC/UTEST/UTEST-01_*.md
```

### Manual Checklist

- [ ] Document Control section at top
- [ ] Test Scope defines component and categories
- [ ] Test Case Index lists all tests with priority
- [ ] Each test case has TSPEC.NN.TT.SS ID
- [ ] Element type code matches document type (40/41/42/43)
- [ ] I/O tables present for all test cases
- [ ] Pseudocode provided for complex logic
- [ ] Error cases documented
- [ ] Coverage Matrix complete
- [ ] TASKS-Ready Score meets type-specific target
- [ ] Cumulative tags: @brd through @spec (8-9 tags)
- [ ] Traceability matrix updated

### Diagram Standards

All diagrams MUST use Mermaid syntax. Text-based diagrams (ASCII art, box drawings) are prohibited.
See: `ai_dev_ssd_flow/DIAGRAM_STANDARDS.md` and `mermaid-gen` skill.

## Common Pitfalls

1. **Wrong element type code**: Use 40 for UTEST, 41 for ITEST, 42 for STEST, 43 for FTEST
2. **Missing I/O tables**: Every test case needs input/output specification
3. **No coverage matrix**: Must track REQ element coverage
4. **Wrong tag format**: Use TSPEC.NN.TT.SS for elements, TYPE-NN for documents
5. **Missing cumulative tags**: Layer 10 requires all 8-9 upstream tags
6. **Legacy test IDs**: Use TSPEC.NN.TT.SS, NOT TC-XXX, UT-XXX, etc.
7. **No pseudocode**: Complex tests require algorithm specification
8. **Incomplete error cases**: Document expected behavior for all error conditions

## Post-Creation Validation (MANDATORY - NO CONFIRMATION)

**CRITICAL**: Execute this validation loop IMMEDIATELY after document creation. Do NOT proceed to next document until validation passes.

### Automatic Validation Loop

```
LOOP:
  1. Run: python ai_dev_ssd_flow/scripts/validate_cross_document.py --document {doc_path} --auto-fix
  2. IF errors fixed: GOTO LOOP (re-validate)
  3. IF warnings fixed: GOTO LOOP (re-validate)
  4. IF unfixable issues: Log for manual review, continue
  5. IF clean: Mark VALIDATED, proceed
```

### Validation Command

```bash
# Per-document validation (Phase 1)
python ai_dev_ssd_flow/scripts/validate_cross_document.py --document docs/10_TSPEC/UTEST/UTEST-NN_slug.md --auto-fix

# Layer validation (Phase 2) - run when all TSPEC documents complete
python ai_dev_ssd_flow/scripts/validate_cross_document.py --layer TSPEC --auto-fix
```

### Layer-Specific Upstream Requirements

| This Layer | Required Upstream Tags | Count |
|------------|------------------------|-------|
| TSPEC (Layer 10) | @brd, @prd, @ears, @bdd, @adr, @sys, @req, @spec (+ @ctr if created) | 8-9 tags |

### Auto-Fix Actions (No Confirmation Required)

| Issue | Fix Action |
|-------|------------|
| Missing upstream tag | Add with upstream document reference |
| Invalid tag format | Correct to TYPE.NN.TT.SS (4-segment) or TYPE-NN format |
| Broken link | Recalculate path from current location |
| Missing traceability section | Insert from template |

### Validation Codes Reference

| Code | Description | Severity |
|------|-------------|----------|
| XDOC-001 | Referenced requirement ID not found | ERROR |
| XDOC-002 | Missing cumulative tag | ERROR |
| XDOC-003 | Upstream document not found | ERROR |
| XDOC-006 | Tag format invalid | ERROR |
| XDOC-007 | Gap in cumulative tag chain | ERROR |
| XDOC-009 | Missing traceability section | ERROR |

### Quality Gate

**Blocking**: YES - Cannot proceed to next document until Phase 1 validation passes with 0 errors.

---

## Next Skill

After creating TSPEC, use:

**`doc-tasks`** - Create Task Breakdown (Layer 11)

The TASKS will:
- Reference this TSPEC for test implementation
- Include all 9-10 upstream tags
- Break SPEC and TSPEC into actionable tasks
- Provide AI-structured TODO format

## Reference Documents

TSPEC artifacts do not support REF documents. Reference documents are limited to **BRD and ADR types only** per the SDD framework.

For supplementary documentation needs, create:
- **BRD-REF**: Business context documentation
- **ADR-REF**: Test strategy guides, coverage analysis reports

## Related Resources

- **Templates**:
  - `ai_dev_ssd_flow/10_TSPEC/UTEST/UTEST-MVP-TEMPLATE.md`
  - `ai_dev_ssd_flow/10_TSPEC/ITEST/ITEST-MVP-TEMPLATE.md`
  - `ai_dev_ssd_flow/10_TSPEC/STEST/STEST-MVP-TEMPLATE.md`
  - `ai_dev_ssd_flow/10_TSPEC/FTEST/FTEST-MVP-TEMPLATE.md`
- **TSPEC README**: `ai_dev_ssd_flow/10_TSPEC/README.md`
- **TSPEC Index**: `ai_dev_ssd_flow/10_TSPEC/TSPEC-00_index.md`
- **Traceability Matrix Template**: `ai_dev_ssd_flow/10_TSPEC/TSPEC-00_TRACEABILITY_MATRIX-TEMPLATE.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
- **doc-naming skill**: `.claude/skills/doc-naming/SKILL.md` (element type codes)
- **doc-spec skill**: `.claude/skills/doc-spec/SKILL.md` (upstream SPEC creation)
- **quality-advisor skill**: `.claude/skills/quality-advisor/SKILL.md` (quality guidance)

## Quick Reference

**TSPEC Purpose**: Test specifications for TDD workflow

**Layer**: 10

**Element ID Format**: `TSPEC.NN.TT.SS`
- Unit Test = 40
- Integration Test = 41
- Smoke Test = 42
- Functional Test = 43

**Removed Patterns**: TC-XXX, UT-XXX, IT-XXX, ST-XXX, FT-XXX

**Tags Required**: @brd through @spec (8-9 tags)

**Format**: Markdown with I/O tables and pseudocode

**TSPEC Types**:
- UTEST: Unit tests (>=90% coverage, REQ-focused)
- ITEST: Integration tests (>=85% coverage, CTR-focused)
- STEST: Smoke tests (100% critical paths, <5min execution)
- FTEST: Functional tests (>=85% SYS coverage)

**Key Sections**:
- Document Control
- Test Scope (component, categories, dependencies)
- Test Case Index
- Test Case Details (I/O tables, pseudocode, error cases)
- Coverage Matrix
- Traceability (cumulative tags)

**Quality Gate**: Type-specific TASKS-Ready Score

**Next**: doc-tasks

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2026-02-27 | Normalized frontmatter to `metadata` schema with `versioning_policy`; aligned cross-document/tag validation command examples to canonical `ai_dev_ssd_flow/scripts/*` locations |
| 1.1 | 2026-02-26 | Added PTEST (code 44) and SECTEST (code 45) support; Fixed template paths to ai_dev_ssd_flow/10_TSPEC/ |
| 1.0 | 2026-02-08 | Initial release with UTEST/ITEST/STEST/FTEST support (codes 40-43) |
