---
name: doc-tasks-validator
description: Validate Task Breakdown (TASKS) documents against Layer 11 schema standards
tags:
  - sdd-workflow
  - layer-11-artifact
  - quality-assurance
custom_fields:
  layer: 11
  artifact_type: TASKS
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: quality-assurance
  upstream_artifacts: [TASKS]
  downstream_artifacts: []
  version: "1.1"
  last_updated: "2026-02-11T18:00:00"
---

# doc-tasks-validator

Validate Task Breakdown (TASKS) documents against Layer 11 schema standards.

## Activation

Invoke when user requests validation of TASKS documents or after creating/modifying TASKS artifacts.

## Validation Schema Reference

Schema: `ai_dev_flow/TASKS/TASKS_SCHEMA.yaml`
Layer: 11
Artifact Type: TASKS

## Validation Checklist

### 0. Folder Structure Validation (BLOCKING)

**Nested Folder Rule**: ALL TASKS documents MUST be in nested folders regardless of size.

**Required Structure**:

| TASKS Type | Required Location |
|------------|-------------------|
| Monolithic | `docs/11_TASKS/TASKS-NN_{slug}/TASKS-NN_{slug}.md` |

**Validation**:

```
1. Check document is inside a nested folder: docs/11_TASKS/TASKS-NN_{slug}/
2. Verify folder name matches TASKS ID pattern: TASKS-NN_{slug}
3. Verify file name matches folder: TASKS-NN_{slug}.md
4. Parent path must be: docs/11_TASKS/
```

**Example Valid Structure**:

```
docs/11_TASKS/
├── TASKS-01_f1_iam/
│   ├── TASKS-01_f1_iam.md         ✓ Valid
│   ├── TASKS-01.R_review_report_v001.md
│   └── .drift_cache.json
├── TASKS-02_f2_session/
│   └── TASKS-02_f2_session.md     ✓ Valid
```

**Invalid Structure**:

```
docs/11_TASKS/
├── TASKS-01_f1_iam.md             ✗ NOT in nested folder
```

**Error Codes**:

| Code | Severity | Description |
|------|----------|-------------|
| TASKS-E020 | ERROR | TASKS not in nested folder (BLOCKING) |
| TASKS-E021 | ERROR | Folder name doesn't match TASKS ID |
| TASKS-E022 | ERROR | File name doesn't match folder name |
| VAL-H001 | ERROR | Drift cache missing hash for upstream document |
| VAL-H002 | ERROR | Invalid hash format (must be sha256:<64 hex chars>) |

**This check is BLOCKING** - TASKS must pass folder structure validation before other checks proceed.

---

### 1. Metadata Validation

```yaml
Required custom_fields:
  - document_type: ["tasks", "template"]
  - artifact_type: "TASKS"
  - layer: 11
  - architecture_approaches: [array format]
  - priority: ["primary", "shared", "fallback"]
  - development_status: ["active", "draft", "deprecated", "reference"]

Required tags:
  - tasks (or tasks-template)
  - layer-11-artifact

Forbidden tag patterns:
  - "^task-breakdown$"
  - "^implementation-tasks$"
  - "^tasks-\\d{3}$"
```

### 2. Structure Validation

**Required Sections (12 sections):**
- Title (H1): `# TASKS-NNN: Title`
- Section 1: Document Control
- Section 2: Executive Summary (Objectives, Scope, Dependencies)
- Section 3: Scope (Inclusions, Exclusions, Boundaries)
- Section 4: Implementation Plan (Phases, Tasks, Dependencies)
- Section 5: Implementation Contracts (Protocols, Exceptions, State Machines)
- Section 6: Constraints (Technical, Business, Operational)
- Section 7: Acceptance Criteria (Functional, Technical, Quality)
- Section 8: Risk Assessment (Risk Matrix, Mitigation Strategies)
- Section 9: Success Metrics (Completion, Quality, Performance)
- Section 10: Traceability
- Section 11: Implementation Notes
- Section 12: Change History

**Optional Sections:**
- Section 13: References

**Document Control Required Fields:**
- TASKS ID
- Document Name
- Version
- Date Created
- Last Updated
- Author
- Status
- Source SPEC

**File Naming:**
Pattern: `TASKS-NNN_descriptive_name.md`

### 3. Content Validation

**Task Format:**
- Pattern: `TASK-NNN`
- Components: task_id, task_name, description, dependencies, acceptance_criteria, estimated_hours, status

**Phase Format:**
- Pattern: `Phase N:`
- Structure: phase_number, phase_name, objective, tasks, deliverables, duration

**Task Status Values:**
- Not Started
- In Progress
- Blocked
- Review
- Completed
- Deferred

**Implementation Contracts Categories:**
- Protocol Interfaces: `typing.Protocol` with type hints
- Exception Hierarchies: `class XxxError(BaseError)` with error codes
- State Machine Contracts: `enum State` with transitions
- Data Models: Pydantic BaseModel with validation
- Dependency Injection: ABC interface patterns

**Implementation-Ready Score:**
- Minimum threshold: 90%
- Components: Task completeness (20%), Dependency mapping (15%), Acceptance criteria (20%), Implementation contracts (15%), Risk assessment (10%), Effort estimation (10%), Traceability (10%)

### 4. Traceability Validation

**Layer 11 Cumulative Tags:**
- @brd: BRD.NN.EE.SS (required)
- @prd: PRD.NN.EE.SS (required)
- @ears: EARS.NN.EE.SS (required)
- @bdd: BDD.NN.EE.SS (required)
- @adr: ADR-NN (required)
- @sys: SYS.NN.EE.SS (required)
- @req: REQ.NN.EE.SS (required)
- @spec: SPEC-NN (required)
- @impl: IMPL.NN.EE.SS (optional)
- @ctr: CTR-NN (optional)

**Implementation Contracts Tags:**
- @icon: TASKS-NN:ContractName
- @icon-role: provider|consumer (optional)

**Downstream Expected:**
- Code (src/...)
- Tests (tests/...)

**Same-Type References:**
- @related-tasks: TASKS-NN
- @depends-tasks: TASKS-NN

## Error Codes

| Code | Severity | Description |
|------|----------|-------------|
| TASKS-E001 | error | Missing required tag 'tasks' |
| TASKS-E002 | error | Missing required tag 'layer-11-artifact' |
| TASKS-E003 | error | Invalid document_type |
| TASKS-E004 | error | Invalid architecture_approaches format |
| TASKS-E005 | error | Forbidden tag pattern detected |
| TASKS-E006 | error | Missing required section |
| TASKS-E007 | error | Multiple H1 headings detected |
| TASKS-E008 | error | Section numbering not sequential (1-12) |
| TASKS-E009 | error | Document Control missing required fields |
| TASKS-E010 | error | Missing Implementation Plan (Section 4) |
| TASKS-E011 | error | Missing Traceability (Section 10) |
| TASKS-E012 | error | Implementation Plan has no Phases |
| TASKS-E013 | warning | File name does not match format |
| TASKS-E014 | error | Source SPEC not in valid format |
| TASKS-W001 | warning | Tasks not using TASK-NNN format |
| TASKS-W002 | warning | Phase has no tasks defined |
| TASKS-W003 | warning | Task missing acceptance criteria |
| TASKS-W004 | warning | Missing upstream tags (require 8) |
| TASKS-W005 | warning | Implementation-Ready Score below 90% |
| TASKS-W006 | warning | Task missing effort estimate |
| TASKS-W007 | warning | Implementation Contracts empty but parallel development indicated |
| TASKS-I001 | info | Consider defining Implementation Contracts |
| TASKS-I002 | info | Consider adding Risk Assessment for complex tasks |
| TASKS-I003 | info | Consider using @icon tags for contracts |

## Validation Commands

```bash
# Validate single TASKS document
python ai_dev_flow/scripts/validate_tasks.py docs/11_TASKS/TASKS-001_example.md

# Validate all TASKS documents
python ai_dev_flow/scripts/validate_tasks.py docs/11_TASKS/

# Check with verbose output
python ai_dev_flow/scripts/validate_tasks.py docs/11_TASKS/ --verbose
```

## Validation Workflow

1. Parse YAML frontmatter
2. Check required metadata fields
3. Validate tag taxonomy
4. Verify section structure (1-12)
5. Validate Document Control table
6. Check Implementation Plan (at least one Phase)
7. Validate Task format (TASK-NNN)
8. Check each task has acceptance criteria
9. Validate Implementation Contracts (if parallel development)
10. Validate upstream references (8 required)
11. Calculate Implementation-Ready Score
12. Verify file naming convention
13. Generate validation report

## Integration

- Invoked by: doc-flow, doc-tasks (post-creation)
- Feeds into: trace-check (cross-document validation)
- Reports to: quality-advisor

## Output Format

```
TASKS Validation Report
=======================
Document: TASKS-001_example.md
Status: PASS/FAIL

Implementation Plan:
- Phases defined: N
- Total tasks: N
- Using TASK-NNN format: N

Task Coverage:
- With acceptance criteria: N/N
- With effort estimates: N/N
- With dependencies: N/N

Implementation Contracts:
- Protocols: N
- Exceptions: N
- State Machines: N
- Data Models: N

Implementation-Ready Score: N%

Errors: N
Warnings: N
Info: N

[Details listed by severity]
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.1 | 2026-02-11 | **Nested Folder Rule**: Added Section 0 Folder Structure Validation (BLOCKING); TASKS must be in `docs/11_TASKS/TASKS-NN_{slug}/` folders; Added error codes TASKS-E020, TASKS-E021, TASKS-E022 |
| 1.0 | 2026-02-08 | Initial validator skill definition with YAML frontmatter | System |
