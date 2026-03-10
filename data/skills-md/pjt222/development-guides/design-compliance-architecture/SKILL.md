---
name: design-compliance-architecture
description: >
  Design a compliance architecture that maps applicable regulations to
  computerized systems. Covers system inventory, criticality classification
  (GxP-critical, GxP-supporting, non-GxP), GAMP 5 category assignment,
  regulatory requirements traceability, and governance structure definition.
  Use when establishing a new regulated facility, formalising compliance
  across multiple systems, addressing a regulatory gap analysis, harmonising
  compliance after mergers or reorganisations, or preparing a site master
  file that references computerized systems.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: compliance
  complexity: advanced
  language: multi
  tags: gxp, compliance, architecture, regulatory, gamp-5, governance
---

# Design Compliance Architecture

Establish the top-level compliance framework that maps regulations to systems, classifies criticality, and defines governance for a regulated environment.

## When to Use

- A new regulated facility, department, or programme is being established
- An existing organisation needs to formalise its compliance posture across multiple systems
- A regulatory gap analysis reveals missing system classification or validation strategy
- Mergers, acquisitions, or reorganisations require harmonising compliance across entities
- Preparing a site master file or quality manual that references computerized systems

## Inputs

- **Required**: List of computerized systems in scope (name, purpose, vendor/custom)
- **Required**: Applicable regulatory frameworks (21 CFR Part 11, EU Annex 11, GMP, GLP, GCP, ICH Q7, ICH Q10)
- **Required**: Organisational context (department, site, product types)
- **Optional**: Existing validation master plan or quality manual
- **Optional**: Previous audit findings or regulatory inspection observations
- **Optional**: Organisational chart with quality and IT reporting lines

## Procedure

### Step 1: Build the System Inventory

Create a comprehensive inventory of all computerized systems:

```markdown
# System Inventory
## Document ID: SI-[SITE]-[YYYY]-[NNN]

| ID | System Name | Version | Vendor | Purpose | Department | Data Types | Users |
|----|-------------|---------|--------|---------|------------|------------|-------|
| SYS-001 | LabWare LIMS | 8.1 | LabWare Inc. | Sample management and testing | QC | Test results, COA | 45 |
| SYS-002 | SAP ERP | S/4HANA | SAP SE | Batch release and inventory | Production | Batch records, BOM | 120 |
| SYS-003 | Custom R/Shiny | 2.1.0 | Internal | Statistical analysis | Biostatistics | Clinical data | 8 |
| SYS-004 | Windows Server | 2022 | Microsoft | File server | IT | Documents | 200 |
```

**Expected:** Every system that creates, modifies, stores, retrieves, or transmits GxP-relevant data is listed.
**On failure:** If system owners cannot provide complete information, document the gap and schedule a discovery workshop. Missing systems are a critical compliance risk.

### Step 2: Classify System Criticality

Assign each system a criticality tier:

```markdown
# System Criticality Classification
## Document ID: SCC-[SITE]-[YYYY]-[NNN]

### Classification Criteria

| Tier | Definition | Validation Required | Examples |
|------|-----------|-------------------|----------|
| **GxP-Critical** | Directly impacts product quality, patient safety, or data integrity. Generates or processes GxP records. | Full CSV per GAMP 5 | LIMS, ERP (batch), CDMS, MES |
| **GxP-Supporting** | Supports GxP processes but does not directly generate GxP records. Failure has indirect impact. | Risk-based qualification | Email, document management, scheduling |
| **Non-GxP** | No impact on product quality, safety, or data integrity. | IT standard controls only | HR systems, cafeteria, general web |

### System Classification Matrix

| System ID | System | Tier | Rationale |
|-----------|--------|------|-----------|
| SYS-001 | LabWare LIMS | GxP-Critical | Generates test results used for batch release |
| SYS-002 | SAP ERP | GxP-Critical | Manages batch records and material traceability |
| SYS-003 | R/Shiny App | GxP-Critical | Performs statistical analysis for regulatory submissions |
| SYS-004 | Windows Server | GxP-Supporting | Stores controlled documents but does not generate GxP data |
```

**Expected:** Every system has a tier assignment with documented rationale.
**On failure:** If a system's criticality is disputed, escalate to the quality council. When in doubt, classify one tier higher and reassess after a formal risk assessment.

### Step 3: Assign GAMP 5 Software Categories

For each GxP-Critical and GxP-Supporting system, assign the GAMP 5 category:

```markdown
# GAMP 5 Category Assignment

| System ID | System | GAMP Category | Rationale | Validation Effort |
|-----------|--------|---------------|-----------|-------------------|
| SYS-001 | LabWare LIMS | 4 — Configured Product | COTS with extensive workflow configuration | Medium-High |
| SYS-002 | SAP ERP | 4 — Configured Product | COTS with custom transactions | Medium-High |
| SYS-003 | R/Shiny App | 5 — Custom Application | Internally developed | High — Full lifecycle |
| SYS-004 | Windows Server | 1 — Infrastructure | Operating system, no custom configuration | Low — Verify installation |
```

Category reference:
- **Category 1**: Infrastructure (OS, firmware) — verify installation
- **Category 3**: Non-configured COTS — verify functionality as-is
- **Category 4**: Configured product — verify all configurations
- **Category 5**: Custom application — full lifecycle validation

**Expected:** Category assignment aligns with how the system is used, not just what it is.
**On failure:** If a system spans categories (e.g., COTS with custom add-ons), classify the custom portions as Category 5 and the base as Category 4.

### Step 4: Map Regulatory Requirements to Systems

Create a regulatory requirements traceability matrix:

```markdown
# Regulatory Requirements Traceability Matrix
## Document ID: RRTM-[SITE]-[YYYY]-[NNN]

| Regulation | Clause | Requirement | Applicable Systems | Control Type |
|-----------|--------|-------------|-------------------|--------------|
| 21 CFR 11 | 11.10(a) | Validation | SYS-001, SYS-002, SYS-003 | Procedural + Technical |
| 21 CFR 11 | 11.10(d) | Access controls | SYS-001, SYS-002, SYS-003, SYS-004 | Technical |
| 21 CFR 11 | 11.10(e) | Audit trail | SYS-001, SYS-002, SYS-003 | Technical |
| 21 CFR 11 | 11.50 | Signature manifestation | SYS-001, SYS-002 | Technical |
| EU Annex 11 | §4 | Validation | SYS-001, SYS-002, SYS-003 | Procedural + Technical |
| EU Annex 11 | §7 | Data storage and backup | All | Technical |
| EU Annex 11 | §9 | Audit trail | SYS-001, SYS-002, SYS-003 | Technical |
| EU Annex 11 | §12 | Security and access | All | Technical |
| ICH Q10 | §3.2 | Change management | All GxP-Critical | Procedural |
| ICH Q10 | §1.8 | Knowledge management | SYS-001, SYS-003 | Procedural |
```

**Expected:** Every applicable regulatory clause maps to at least one system, and every GxP-Critical system maps to the relevant regulatory clauses.
**On failure:** Unmapped clauses represent compliance gaps. Create a remediation plan with timelines for each gap.

### Step 5: Define Validation Strategy Per System

Based on criticality, category, and regulatory mapping:

```markdown
# Validation Strategy Summary

| System | Category | Criticality | Validation Approach | Key Deliverables |
|--------|----------|------------|--------------------|--------------------|
| LabWare LIMS | 4 | Critical | Prospective CSV | URS, RA, VP, IQ, OQ, PQ, TM, VSR |
| SAP ERP | 4 | Critical | Prospective CSV | URS, RA, VP, IQ, OQ, TM, VSR |
| R/Shiny App | 5 | Critical | Prospective CSV + code review | URS, RA, VP, IQ, OQ, PQ, TM, VSR, code audit |
| Windows Server | 1 | Supporting | Installation qualification | IQ checklist |
```

Abbreviations: URS (User Requirements), RA (Risk Assessment), VP (Validation Plan), IQ/OQ/PQ (Installation/Operational/Performance Qualification), TM (Traceability Matrix), VSR (Validation Summary Report).

**Expected:** Validation effort is proportional to risk — Category 5 GxP-Critical systems get full lifecycle; Category 1 infrastructure gets streamlined IQ.
**On failure:** If stakeholders push for reduced validation of critical systems, document the risk acceptance with QA sign-off.

### Step 6: Design Governance Structure

Define the organisational framework for sustaining compliance:

```markdown
# Compliance Governance Structure

## Roles and Responsibilities
| Role | Responsibility | Authority |
|------|---------------|-----------|
| Quality Director | Overall compliance accountability | Approve validation strategies, accept risks |
| System Owner | Day-to-day system compliance | Approve changes, ensure validated state |
| Validation Lead | Plan and coordinate validation activities | Define validation scope and approach |
| IT Operations | Technical infrastructure and security | Implement technical controls |
| QA Reviewer | Independent review of validation deliverables | Accept or reject validation evidence |

## Governance Committees
| Committee | Frequency | Purpose | Members |
|-----------|-----------|---------|---------|
| Change Control Board | Weekly | Review and approve system changes | System owners, QA, IT, validation |
| Periodic Review Committee | Quarterly | Review system compliance status | Quality director, system owners, QA |
| Audit Programme Committee | Annual | Plan internal audit schedule | Quality director, lead auditor, QA |

## Escalation Matrix
| Issue | First Escalation | Second Escalation | Timeline |
|-------|-----------------|-------------------|----------|
| Critical audit finding | System Owner → QA Director | QA Director → Site Director | 24 hours |
| Validated state breach | Validation Lead → System Owner | System Owner → Quality Director | 48 hours |
| Data integrity incident | System Owner → QA Director | QA Director → Regulatory Affairs | 24 hours |
```

**Expected:** Clear accountability for every compliance activity with no orphaned responsibilities.
**On failure:** If roles overlap or are unassigned, convene a RACI workshop to resolve. Ambiguous ownership is a recurring regulatory citation.

### Step 7: Compile the Compliance Architecture Document

Assemble all components into the master document:

```markdown
# Compliance Architecture
## Document ID: CA-[SITE]-[YYYY]-[NNN]
## Version: 1.0

### 1. Purpose and Scope
[Organisation, site, product scope, regulatory scope]

### 2. System Inventory
[From Step 1]

### 3. Criticality Classification
[From Step 2]

### 4. GAMP 5 Category Assignments
[From Step 3]

### 5. Regulatory Requirements Traceability
[From Step 4]

### 6. Validation Strategy
[From Step 5]

### 7. Governance Structure
[From Step 6]

### 8. Periodic Review Schedule
- System inventory refresh: Annual
- Criticality re-assessment: When new systems added or regulations change
- Regulatory mapping update: When new guidance issued
- Governance review: Annual or after organisational change

### 9. Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Quality Director | | | |
| IT Director | | | |
| Regulatory Affairs | | | |
```

**Expected:** A single document that serves as the compliance blueprint for the entire regulated environment.
**On failure:** If the document exceeds practical size, create a master document with references to subsidiary documents per system or domain.

## Validation

- [ ] System inventory includes every system that handles GxP data
- [ ] Every system has a criticality tier with documented rationale
- [ ] GAMP 5 categories assigned to all GxP-Critical and GxP-Supporting systems
- [ ] Regulatory requirements traceability matrix covers all applicable clauses
- [ ] Every GxP-Critical system has a defined validation strategy
- [ ] Governance structure defines roles, committees, and escalation paths
- [ ] All documents have unique IDs and version control
- [ ] Compliance architecture document is approved by quality and IT leadership

## Common Pitfalls

- **Incomplete inventory**: Missing systems are invisible to compliance. Use network scans, software asset management tools, and department interviews — not just asking IT.
- **Binary thinking**: Systems are not simply "GxP" or "not GxP." The three-tier model (Critical, Supporting, Non-GxP) avoids both over-validation and under-validation.
- **Category confusion**: GAMP 5 category describes what the software IS, but validation effort should reflect how it is USED. A Category 4 system used for batch release needs more testing than a Category 4 system used for scheduling.
- **Static architecture**: The compliance architecture is a living document. New systems, regulatory changes, and audit findings all require updates.
- **Governance without teeth**: Committees that exist on paper but never meet provide no compliance value. Define meeting cadence and quorum requirements.

## Related Skills

- `perform-csv-assessment` — execute the validation strategy defined here for individual systems
- `manage-change-control` — operationalise the change control process defined in governance
- `implement-electronic-signatures` — implement e-signature controls mapped in the regulatory matrix
- `prepare-inspection-readiness` — use this architecture as the foundation for inspection preparation
- `conduct-gxp-audit` — audit against the compliance architecture as the baseline
