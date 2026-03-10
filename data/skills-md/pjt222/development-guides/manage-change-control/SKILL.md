---
name: manage-change-control
description: >
  Manage change control for validated computerized systems. Covers change
  request triage (emergency, standard, minor), impact assessment on validated
  state, revalidation scope determination, approval workflows, implementation
  tracking, and post-change verification. Use when a validated system requires
  a software upgrade, patch, or configuration change; when infrastructure
  changes affect validated systems; when a CAPA requires system modification;
  or when emergency changes need expedited approval and retrospective
  documentation.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: compliance
  complexity: intermediate
  language: multi
  tags: gxp, change-control, revalidation, impact-assessment, compliance
---

# Manage Change Control

Evaluate, approve, implement, and verify changes to validated computerized systems while maintaining their validated state.

## When to Use

- A validated system requires a software upgrade, patch, or configuration change
- Infrastructure changes (server migration, OS upgrade, network change) affect validated systems
- A CAPA or audit finding requires system modification
- Business process changes require system reconfiguration
- Emergency changes need expedited approval and retrospective documentation

## Inputs

- **Required**: Change description (what is changing and why)
- **Required**: System(s) affected and their current validated state
- **Required**: Change requestor and business justification
- **Optional**: Vendor release notes or technical documentation
- **Optional**: Related CAPA or audit finding references
- **Optional**: Existing validation documentation for affected system(s)

## Procedure

### Step 1: Create and Classify the Change Request

```markdown
# Change Request
## Document ID: CR-[SYS]-[YYYY]-[NNN]

### 1. Change Description
**Requestor:** [Name, Department]
**Date:** [YYYY-MM-DD]
**System:** [System name and version]
**Current State:** [Current configuration/version]
**Proposed State:** [Target configuration/version]

### 2. Justification
[Business, regulatory, or technical reason for the change]

### 3. Classification
| Type | Definition | Approval Path | Timeline |
|------|-----------|--------------|----------|
| **Emergency** | Urgent fix for safety, data integrity, or regulatory compliance | System owner + QA (retrospective CCB) | Implement immediately, document within 5 days |
| **Standard** | Planned change with potential impact on validated state | CCB approval before implementation | Per CCB schedule |
| **Minor** | Low-risk change with no impact on validated state | System owner approval | Documented before implementation |

**This change is classified as:** [Emergency / Standard / Minor]
**Rationale:** [Why this classification]
```

**Expected:** Change request has a unique ID, clear description, and justified classification.
**On failure:** If classification is disputed, default to Standard and let the CCB adjudicate.

### Step 2: Perform Impact Assessment

Evaluate the change against all dimensions of the validated state:

```markdown
# Impact Assessment
## Change Request: CR-[SYS]-[YYYY]-[NNN]

### Impact Matrix
| Dimension | Affected? | Details | Risk |
|-----------|-----------|---------|------|
| Software configuration | Yes/No | [Specific parameters changing] | [H/M/L] |
| Source code | Yes/No | [Modules, functions, or scripts affected] | [H/M/L] |
| Database schema | Yes/No | [Tables, fields, constraints changing] | [H/M/L] |
| Infrastructure | Yes/No | [Servers, network, storage affected] | [H/M/L] |
| Interfaces | Yes/No | [Upstream/downstream system connections] | [H/M/L] |
| User access/roles | Yes/No | [Role changes, new access requirements] | [H/M/L] |
| SOPs/work instructions | Yes/No | [Procedures requiring update] | [H/M/L] |
| Training | Yes/No | [Users requiring retraining] | [H/M/L] |
| Data migration | Yes/No | [Data transformation or migration needed] | [H/M/L] |
| Audit trail | Yes/No | [Impact on audit trail continuity] | [H/M/L] |

### Regulatory Impact
- [ ] Change affects 21 CFR Part 11 controls
- [ ] Change affects EU Annex 11 controls
- [ ] Change affects data integrity (ALCOA+)
- [ ] Change requires regulatory notification
```

**Expected:** Every dimension is assessed with a clear yes/no and rationale.
**On failure:** If impact cannot be determined without testing, classify the dimension as "Unknown — requires investigation" and mandate a sandbox evaluation before production change.

### Step 3: Determine Revalidation Scope

Based on the impact assessment, define what validation activities are needed:

```markdown
# Revalidation Determination

| Revalidation Level | Criteria | Activities Required |
|--------------------|----------|-------------------|
| **Full revalidation** | Core functionality changed, new GAMP category, or major version upgrade | URS review, RA update, IQ, OQ, PQ, TM update, VSR |
| **Partial revalidation** | Specific functions affected, configuration changes | Targeted OQ for affected functions, TM update |
| **Documentation only** | No functional impact, administrative changes | Update validation documents, change log entry |
| **None** | No impact on validated state (e.g., cosmetic change) | Change log entry only |

### Determination for CR-[SYS]-[YYYY]-[NNN]
**Revalidation level:** [Full / Partial / Documentation only / None]
**Rationale:** [Specific reasoning based on impact assessment]

### Required Activities
| Activity | Owner | Deadline |
|----------|-------|----------|
| [e.g., Execute OQ test cases TC-OQ-015 through TC-OQ-022] | [Name] | [Date] |
| [e.g., Update traceability matrix for URS-007] | [Name] | [Date] |
| [e.g., Update SOP-LIMS-003 section 4.2] | [Name] | [Date] |
```

**Expected:** Revalidation scope is proportional to the change impact — no more, no less.
**On failure:** If revalidation scope is contested, err on the side of more testing. Under-validation is a regulatory risk; over-validation is only a resource cost.

### Step 4: Obtain Approval

Route the change through the appropriate approval workflow:

```markdown
# Change Approval

### Approval for: CR-[SYS]-[YYYY]-[NNN]

| Role | Name | Decision | Signature | Date |
|------|------|----------|-----------|------|
| System Owner | | Approve / Reject / Defer | | |
| QA Representative | | Approve / Reject / Defer | | |
| IT Representative | | Approve / Reject / Defer | | |
| Validation Lead | | Approve / Reject / Defer | | |

### Conditions (if any)
[Any conditions attached to the approval]

### Planned Implementation Window
- **Start:** [Date/Time]
- **End:** [Date/Time]
- **Rollback deadline:** [Point of no return]
```

**Expected:** All required approvers have signed before implementation begins (except emergency changes).
**On failure:** For emergency changes, obtain verbal approval from system owner and QA, implement the change, and complete formal documentation within 5 business days.

### Step 5: Implement and Verify

Execute the change and perform post-change verification:

```markdown
# Implementation Record

### Pre-Implementation
- [ ] Backup of current system state completed
- [ ] Rollback procedure documented and tested
- [ ] Affected users notified
- [ ] Test environment validated (if applicable)

### Implementation
- **Implemented by:** [Name]
- **Date/Time:** [YYYY-MM-DD HH:MM]
- **Steps performed:** [Detailed implementation steps]
- **Deviations from plan:** [None / Description]

### Post-Change Verification
| Verification | Result | Evidence |
|--------------|--------|----------|
| System accessible and functional | Pass/Fail | [Screenshot/log reference] |
| Changed functionality works as specified | Pass/Fail | [Test case reference] |
| Unchanged functionality unaffected (regression) | Pass/Fail | [Test case reference] |
| Audit trail continuity maintained | Pass/Fail | [Audit trail screenshot] |
| User access controls intact | Pass/Fail | [Access review reference] |

### Closure
- [ ] All verification activities completed successfully
- [ ] Validation documents updated per revalidation determination
- [ ] SOPs updated and effective
- [ ] Training completed for affected users
- [ ] Change record closed in change control system
```

**Expected:** Implementation matches the approved plan, and all verification activities pass.
**On failure:** If verification fails, execute the rollback procedure immediately and document the failure as a deviation. Do not proceed without QA concurrence.

## Validation

- [ ] Change request has unique ID, description, and classification
- [ ] Impact assessment covers all dimensions (software, data, infrastructure, SOPs, training)
- [ ] Revalidation scope is defined with rationale
- [ ] All required approvals obtained before implementation (or within 5 days for emergency)
- [ ] Pre-implementation backup and rollback procedure documented
- [ ] Post-change verification demonstrates the change works and nothing else broke
- [ ] Validation documents updated to reflect the change
- [ ] Change record formally closed

## Common Pitfalls

- **Skipping impact assessment for "small" changes**: Even minor changes can have unexpected impacts. A configuration toggle that seems harmless may disable an audit trail or change a calculation.
- **Emergency change abuse**: If more than 10% of changes are classified as "emergency," the change process is being circumvented. Review and tighten the emergency criteria.
- **Incomplete rollback planning**: Assuming rollback is "just restore the backup" ignores data created between backup and rollback. Define data disposition for every rollback scenario.
- **Approval after implementation**: Retrospective approval (except for documented emergencies) is a compliance violation. The CCB must approve before work begins.
- **Missing regression testing**: Verifying only the changed functionality is insufficient. Regression testing must confirm that existing validated functions remain unaffected.

## Related Skills

- `design-compliance-architecture` — defines the governance framework including change control board
- `write-validation-documentation` — create the revalidation documentation triggered by changes
- `perform-csv-assessment` — full CSV reassessment for major changes requiring full revalidation
- `write-standard-operating-procedure` — update SOPs affected by the change
- `investigate-capa-root-cause` — when changes are triggered by CAPAs
