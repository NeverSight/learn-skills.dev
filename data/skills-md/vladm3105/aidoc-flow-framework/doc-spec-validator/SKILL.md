---
name: doc-spec-validator
description: Validate Technical Specifications (SPEC) documents against Layer 9 schema standards
metadata:
  tags:
    - sdd-workflow
    - layer-9-artifact
    - quality-assurance
  custom_fields:
    layer: 9
    artifact_type: SPEC
    architecture_approaches: [ai-agent-based, traditional-8layer]
    priority: shared
    development_status: active
    skill_category: quality-assurance
    upstream_artifacts: [SPEC]
    downstream_artifacts: []
    version: "1.4"
    last_updated: "2026-02-27"
  versioning_policy: "tracks SPEC_MVP_SCHEMA schema_version"
---

# doc-spec-validator

Validate Technical Specifications (SPEC) documents against Layer 9 schema standards.

## Activation

Invoke when user requests validation of SPEC documents or after creating/modifying SPEC artifacts.

## Validation Schema Reference

Schema: `ai_dev_ssd_flow/09_SPEC/SPEC_MVP_SCHEMA.yaml`
Layer: 9
Artifact Type: SPEC

## Validation Checklist

### 0. Folder Structure Validation (BLOCKING)

**Nested Folder Rule**: ALL SPEC documents MUST be in nested folders regardless of size.

**Required Structure**:

| SPEC Type | Required Location |
|-----------|-------------------|
| YAML | `docs/09_SPEC/SPEC-NN_{slug}/SPEC-NN_{slug}.yaml` |

**Validation**:

```
1. Check document is inside a nested folder: docs/09_SPEC/SPEC-NN_{slug}/
2. Verify folder name matches SPEC ID pattern: SPEC-NN_{slug}
3. Verify file name matches folder: SPEC-NN_{slug}.yaml
4. Parent path must be: docs/09_SPEC/
```

**Example Valid Structure**:

```
docs/09_SPEC/
├── SPEC-01_f1_iam/
│   ├── SPEC-01_f1_iam.yaml        ✓ Valid
│   ├── SPEC-01.A_audit_report_v001.md (preferred)
│   ├── SPEC-01.R_review_report_v001.md (legacy-compatible)
│   └── .drift_cache.json
├── SPEC-02_f2_session/
│   └── SPEC-02_f2_session.yaml    ✓ Valid
```

**Invalid Structure**:

```
docs/09_SPEC/
├── SPEC-01_f1_iam.yaml            ✗ NOT in nested folder
```

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| SPEC-E020 | ERROR | SPEC not in nested folder (BLOCKING) |
| SPEC-E021 | ERROR | Folder name doesn't match SPEC ID |
| SPEC-E022 | ERROR | File name doesn't match folder name |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |

**This check is BLOCKING** - SPEC must pass folder structure validation before other checks proceed.

---

### 1. File Format Validation

```yaml
File Format:
  - Extension: .yaml (NOT .md)
  - Naming pattern: SPEC-NNN_descriptive_name.yaml
  - Encoding: UTF-8
  - YAML version: 1.2
```

### 2. Required Top-Level Fields

```yaml
Required fields:
  - id: Component identifier (snake_case)
  - summary: Single-sentence description (10-200 chars)
  - metadata: Document control and versioning
  - traceability: Upstream and downstream references
  - architecture: Component architecture and dependencies
  - interfaces: Interface definitions (classes, methods)
  - behavior: Behavioral specifications
  - performance: Performance targets
  - security: Security specifications
  - observability: Metrics, logging, health checks
  - verification: Test scenarios
  - implementation: Implementation specifics

Optional fields:
  - caching
  - rate_limiting
  - circuit_breaker
  - operations
  - changelog
  - maintenance
  - notes
```

### 3. Metadata Section Validation

**Required Fields:**
- version: Semantic version (MAJOR.MINOR.PATCH)
- status: draft | review | approved | implemented | deprecated
- created_date: YYYY-MM-DD format
- last_updated: YYYY-MM-DD format
- authors: Array with at least one author (name required)

**Optional Fields:**
- task_ready_score
- reviewers
- owners

### 4. Interfaces Section Validation

**Class Requirements:**
- name: PascalCase format
- description: Required
- methods: At least one method required per class

**Method Requirements:**
- name: snake_case format
- description: Required
- input: Optional parameters object
- output: Optional return object
- errors: Optional error definitions

### 5. Performance Section Validation

**Required Fields:**
- latency_targets:
  - p50_milliseconds
  - p95_milliseconds
  - p99_milliseconds
- throughput_targets:
  - sustained_requests_per_second
- resource_limits:
  - cpu_cores_allocated
  - memory_mb_allocated

**Validation Rules:**
- p95 must be greater than p50
- p99 must be greater than p95

### 6. Security Section Validation

**Required Fields:**
- authentication.required: boolean
- authentication.methods: array
- authorization.enabled: boolean
- input_validation.strategy: string

### 7. Observability Section Validation

**Required Fields:**
- metrics.standard_metrics: array (min 1 item)
- logging.level: DEBUG | INFO | WARN | ERROR
- logging.format: json | text | structured
- health_checks.enabled: boolean
- health_checks.endpoints: array

### 8. Traceability Validation

**Layer 9 Cumulative Tags:**
- @brd: BRD.NN.EE.SS (required)
- @prd: PRD.NN.EE.SS (required)
- @ears: EARS.NN.24.SS (required)
- @bdd: BDD.NN.13.SS (required)
- @adr: ADR-NN (required)
- @sys: SYS.NN.25.SS (required)
- @req: REQ.NN.26.SS (required)
- @ctr: CTR-NN (optional)

**Downstream Expected:**
- TASKS documents
- Code (src/...)
- Tests (tests/...)

**Same-Type References:**
- related_spec: [SPEC-NN]
- depends_spec: [SPEC-NN]

## Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| SPEC-E001 | error | File is not valid YAML |
| SPEC-E002 | error | Missing required top-level field |
| SPEC-E003 | error | Missing required metadata field |
| SPEC-E004 | error | Invalid version format |
| SPEC-E005 | error | Invalid status value |
| SPEC-E006 | error | Invalid date format |
| SPEC-E007 | error | No authors specified |
| SPEC-E008 | error | No classes defined in interfaces |
| SPEC-E009 | error | Class has no methods |
| SPEC-E010 | error | Missing latency_targets in performance |
| SPEC-E011 | error | Missing authentication in security |
| SPEC-E012 | error | Missing metrics in observability |
| SPEC-E013 | warning | File name does not match format |
| SPEC-E014 | error | Missing traceability section |
| SPEC-E015 | error | Missing cumulative_tags in traceability |
| SPEC-W001 | warning | Missing business_requirements in upstream |
| SPEC-W002 | warning | Missing cumulative tags for traceability |
| SPEC-W003 | warning | No BDD scenarios in verification |
| SPEC-W004 | warning | p95 latency not greater than p50 |
| SPEC-W005 | warning | p99 latency not greater than p95 |
| SPEC-W006 | warning | Method name not in snake_case |
| SPEC-W007 | warning | Class name not in PascalCase |
| SPEC-W008 | warning | id field does not match file name |
| SPEC-W009 | warning | task_ready_score below target |
| SPEC-I001 | info | Consider adding caching section |
| SPEC-I002 | info | Consider adding rate_limiting section |
| SPEC-I003 | info | Consider adding circuit_breaker section |
| SPEC-I004 | info | Consider adding operations runbook |

## Validation Commands

```bash
# Validate single SPEC document
python3 ai_dev_ssd_flow/09_SPEC/scripts/validate_spec.py docs/09_SPEC/SPEC-001_example/SPEC-001_example.yaml

# Validate all SPEC documents
find docs/09_SPEC -name "SPEC-*.yaml" -exec python3 ai_dev_ssd_flow/09_SPEC/scripts/validate_spec.py {} \;

# Check with verbose output
python3 ai_dev_ssd_flow/09_SPEC/scripts/validate_spec_implementation_readiness.py docs/09_SPEC/SPEC-001_example/SPEC-001_example.yaml --verbose
```

## Validation Workflow

1. Verify file is valid YAML
2. Check all required top-level fields present
3. Validate metadata section (version, status, dates, authors)
4. Check interfaces section (classes with methods)
5. Validate performance section (latency targets, p50 < p95 < p99)
6. Check security section (authentication, authorization)
7. Validate observability section (metrics, logging, health)
8. Check traceability cumulative tags (7 required)
9. Verify verification section (BDD scenarios)
10. Validate implementation section
11. Check file naming convention
12. Generate validation report

## Integration

- Invoked by: doc-flow, doc-spec (post-creation)
- Feeds into: trace-check (cross-document validation)
- Reports to: quality-advisor

## Output Format

```
SPEC Validation Report
======================
Document: SPEC-001_example.yaml
Status: PASS/FAIL

YAML Validity: Valid/Invalid

Required Sections:
- metadata: Present/Missing
- traceability: Present/Missing
- architecture: Present/Missing
- interfaces: Present/Missing
- behavior: Present/Missing
- performance: Present/Missing
- security: Present/Missing
- observability: Present/Missing
- verification: Present/Missing
- implementation: Present/Missing

Interface Summary:
- Classes defined: N
- Methods defined: N

Performance Targets:
- p50: Nms
- p95: Nms (> p50: Yes/No)
- p99: Nms (> p95: Yes/No)

Errors: N
Warnings: N
Info: N

[Details listed by severity]
```

## Related Resources

- **SPEC Skill**: `.claude/skills/doc-spec/SKILL.md`
- **Naming Standards**: `.claude/skills/doc-naming/SKILL.md` (ID and naming conventions)
- **SPEC Validation Rules**: `ai_dev_ssd_flow/09_SPEC/SPEC_MVP_VALIDATION_RULES.md`
- **SPEC Schema**: `ai_dev_ssd_flow/09_SPEC/SPEC_MVP_SCHEMA.yaml`

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.4 | 2026-02-27 | Normalized metadata schema and command references to canonical `ai_dev_ssd_flow/09_SPEC/scripts` validators | System |
| 1.3 | 2026-02-26 | Fixed schema path to ai_dev_ssd_flow/09_SPEC/; Updated cumulative tag formats to unified dot notation; Fixed validation rules paths | System |
| 1.2 | 2026-02-11 | **Nested Folder Rule**: Added Section 0 Folder Structure Validation (BLOCKING); SPEC must be in `docs/09_SPEC/SPEC-NN_{slug}/` folders; Added error codes SPEC-E020, SPEC-E021, SPEC-E022 | System |
| 1.1.0 | 2026-02-08 | Updated layer assignment from 10 to 9 per LAYER_REGISTRY v1.6; removed @impl from cumulative tags | System |
| 1.0.0 | 2025-01-15 | Initial validator skill definition | System |
