---
name: prepare-inspection-readiness
description: >
  Prepare an organisation for regulatory inspection by assessing readiness
  against agency-specific focus areas (FDA, EMA, MHRA). Covers warning letter
  and 483 theme analysis, mock inspection protocols, document bundle
  preparation, inspection logistics, and response template creation. Use when
  a regulatory inspection has been announced or is anticipated, when a periodic
  self-assessment is due, when new systems have been implemented since the last
  inspection, or after a significant audit finding that may attract regulatory
  attention.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: compliance
  complexity: advanced
  language: multi
  tags: gxp, inspection, fda, ema, mhra, readiness, compliance, 483
---

# Prepare Inspection Readiness

Assess and improve organisational readiness for regulatory inspection, covering documentation, personnel preparation, logistics, and response planning.

## When to Use

- A regulatory inspection has been announced or is anticipated
- Periodic self-assessment of inspection readiness is due
- New systems or processes have been implemented since the last inspection
- Industry trends (warning letters, 483s) indicate an emerging focus area
- After a significant audit finding that may attract regulatory attention

## Inputs

- **Required**: Inspecting authority (FDA, EMA, MHRA, or other)
- **Required**: Expected inspection scope (data integrity, CSV, GMP, GLP, GCP)
- **Required**: Compliance architecture and system inventory
- **Optional**: Previous inspection reports and observations
- **Optional**: Recent industry warning letters and 483 themes
- **Optional**: Open CAPAs and audit findings

## Procedure

### Step 1: Analyse Agency-Specific Focus Areas

Research the inspecting authority's current priorities:

```markdown
# Inspection Focus Area Analysis
## Document ID: IFA-[SITE]-[YYYY]-[NNN]

### FDA Current Focus Areas
| Focus Area | Regulatory Basis | Recent 483 Trends | Risk to This Site |
|-----------|-----------------|-------------------|-------------------|
| Data integrity | 21 CFR Part 11, CGMP | #1 cited observation in drug 483s since 2016 | [H/M/L] |
| Audit trail | 21 CFR 11.10(e) | Disabled/incomplete audit trails | [H/M/L] |
| Electronic signatures | 21 CFR 11.50-11.300 | Missing manifestation, shared accounts | [H/M/L] |
| Computer system validation | GAMP 5, FDA guidance | Inadequate validation of Category 4/5 systems | [H/M/L] |
| Change control | ICH Q10 | Undocumented or retrospective changes | [H/M/L] |
| Laboratory controls | 21 CFR 211.160-211.176 | OOS investigation, test repetition | [H/M/L] |

### EMA/MHRA-Specific Considerations
| Area | EU Annex 11 Reference | Focus | Risk to This Site |
|------|----------------------|-------|-------------------|
| Computerized system validation | §4, §5 | Risk-based validation, supplier assessment | [H/M/L] |
| Operational phase | §6-§13 | Security, audit trail, backup, business continuity | [H/M/L] |
| Cloud and outsourced systems | §3.4 | Service level agreements, data sovereignty | [H/M/L] |
| Data governance | MHRA DI guidance | ALCOA+, culture of integrity | [H/M/L] |
```

**Expected:** A risk-rated analysis of inspection focus areas specific to the inspecting authority.
**On failure:** If recent 483/warning letter data is unavailable, consult the FDA warning letter database, EMA inspection reports, or industry publications for the most current trends.

### Step 2: Conduct Readiness Self-Assessment

Evaluate the site against each focus area:

```markdown
# Inspection Readiness Assessment
## Document ID: IRA-[SITE]-[YYYY]-[NNN]

### Readiness Scoring
| Focus Area | Weight | Current State | Score (1-5) | Gap | Remediation Priority |
|-----------|--------|--------------|-------------|-----|---------------------|
| Data integrity controls | High | [Description of current state] | [1-5] | [Gap description] | [Critical/High/Medium/Low] |
| Validation documentation | High | [Description] | [1-5] | [Gap] | [Priority] |
| Audit trail compliance | High | [Description] | [1-5] | [Gap] | [Priority] |
| Electronic signatures | Medium | [Description] | [1-5] | [Gap] | [Priority] |
| Change control | Medium | [Description] | [1-5] | [Gap] | [Priority] |
| Training records | Medium | [Description] | [1-5] | [Gap] | [Priority] |
| SOPs (current, approved) | Medium | [Description] | [1-5] | [Gap] | [Priority] |
| CAPA management | Medium | [Description] | [1-5] | [Gap] | [Priority] |
| Vendor qualification | Low | [Description] | [1-5] | [Gap] | [Priority] |
| Periodic review | Low | [Description] | [1-5] | [Gap] | [Priority] |

Score: 1 = Critical gaps, 5 = Fully compliant
Overall readiness score: [Sum / Max] = [X]%

### Remediation Plan
| Gap ID | Description | Owner | Action | Deadline | Status |
|--------|------------|-------|--------|----------|--------|
| GAP-001 | [Gap] | [Name] | [Remediation action] | [Date] | [Open/In Progress/Closed] |
```

**Expected:** A quantified readiness assessment with prioritised remediation actions.
**On failure:** If overall readiness is below 70%, consider requesting an inspection delay (if permitted) and implementing emergency remediation.

### Step 3: Prepare Document Bundles

Organise documentation into inspection-ready packages:

```markdown
# Inspection Document Bundles

### Bundle 1: Validation Pack (per system)
- [ ] Current validation status summary (one-page per system)
- [ ] User Requirements Specification (URS)
- [ ] Risk Assessment
- [ ] Validation Plan
- [ ] IQ Protocol and Report
- [ ] OQ Protocol and Report
- [ ] PQ Protocol and Report (if applicable)
- [ ] Traceability Matrix
- [ ] Validation Summary Report
- [ ] Periodic review records
- [ ] Change control history since last validation

### Bundle 2: Data Integrity Evidence
- [ ] Data integrity policy and programme
- [ ] ALCOA+ assessment results
- [ ] Audit trail review records (last 12 months)
- [ ] Data integrity monitoring metrics and trends
- [ ] Data integrity training records

### Bundle 3: Operational Evidence
- [ ] Current SOPs (master list with effective dates)
- [ ] Training matrix (all GxP personnel)
- [ ] Change control log (last 24 months)
- [ ] Deviation/incident log (last 24 months)
- [ ] CAPA log with closure status
- [ ] Internal audit reports and CAPA follow-up

### Bundle 4: System Configuration Evidence
- [ ] User access list (current active users with roles)
- [ ] System configuration documentation
- [ ] Backup and recovery test records
- [ ] Security patch log
- [ ] Business continuity/disaster recovery plan
```

**Expected:** All bundles are assembled, indexed, and accessible within 30 minutes of an inspector's request.
**On failure:** If documents are missing or incomplete, create a gap list, prioritise remediation, and document the plan. Inspectors notice disorganisation.

### Step 4: Design Mock Inspection Protocol

```markdown
# Mock Inspection Protocol
## Document ID: MIP-[SITE]-[YYYY]-[NNN]

### Scope
- **Focus areas:** [Top 3-5 risk areas from readiness assessment]
- **Systems in scope:** [Systems likely to be inspected]
- **Duration:** [1-2 days]

### Participants
| Role | Name | Mock Inspection Role |
|------|------|---------------------|
| Mock inspector | [Experienced QA or external consultant] | Ask questions, request documents |
| System owner(s) | [Names] | Respond to questions, demonstrate systems |
| QA | [Name] | Observe, note findings |
| Back room coordinator | [Name] | Locate and provide documents |

### Mock Inspection Scenarios
| Scenario | Focus | Inspector Might Ask |
|----------|-------|-------------------|
| 1: Show me the audit trail | Data integrity | "Show me the audit trail for batch record BR-2025-1234" |
| 2: Walk me through a change | Change control | "Show me the change control for the last system upgrade" |
| 3: Show training records | Training | "Show me the training records for user [Name] on system [X]" |
| 4: Explain your validation | CSV | "Walk me through how you validated this system" |
| 5: Show a deviation | CAPA | "Show me your last critical deviation and its CAPA" |
| 6: User access review | Access control | "Show me how you manage user access when people leave" |

### Post-Mock Assessment
| Scenario | Outcome | Findings | Actions |
|----------|---------|----------|---------|
| [#] | [Satisfactory/Needs Work] | [Description] | [Remediation if needed] |
```

**Expected:** Mock inspection reveals issues before the real inspection does.
**On failure:** If mock inspection reveals critical gaps, treat them as critical findings with the same urgency as real inspection observations.

### Step 5: Plan Inspection Logistics

```markdown
# Inspection Logistics Plan

### Room Setup
| Room | Purpose | Equipment | Assigned To |
|------|---------|-----------|-------------|
| Front room | Inspector workspace | Table, chairs, network access, printer | Facility manager |
| Back room | Document retrieval and strategy | Copier, network access, phone | QA team |
| Demo room | System demonstrations | Workstation with system access | IT support |

### Roles During Inspection
| Role | Person | Responsibilities |
|------|--------|-----------------|
| Inspection coordinator | [Name] | Single point of contact with inspector, schedule management |
| Subject matter experts | [Names] | Answer technical questions in their domain |
| Back room lead | [Name] | Coordinate document retrieval, track requests |
| Scribe | [Name] | Document all questions, requests, and responses |
| Executive sponsor | [Name] | Available for escalation, opening/closing meetings |

### Communication Protocol
- All document requests flow through the back room lead
- No documents provided without QA review
- Questions requiring research get a "we will get back to you" response (track and follow up)
- Daily debrief with inspection team after each day
```

**Expected:** Logistics plan ensures a professional, organised response to the inspection.
**On failure:** If key personnel are unavailable on the inspection date, identify and brief alternates.

### Step 6: Create Response Templates

```markdown
# Inspection Response Templates

### Template 1: 483 Observation Response
[Date]
[FDA District Office Address]

Re: FDA Form 483 Observations — [Inspection Dates] — [Facility Name]

Dear [Inspector Name],

We appreciate the opportunity to address the observations identified during the inspection of [facility] on [dates].

**Observation [N]:** [Quote the exact observation text]

**Response:**
- **Root Cause:** [Brief root cause description]
- **Immediate Corrective Action:** [What was done immediately]
  - Completed: [Date]
- **Long-term Corrective Action:** [Systemic fix]
  - Target completion: [Date]
- **Preventive Action:** [How recurrence will be prevented]
  - Target completion: [Date]
- **Effectiveness Verification:** [How effectiveness will be measured]
  - Target verification date: [Date]

### Template 2: Immediate Correction During Inspection
When an inspector identifies an issue that can be corrected immediately:
1. Acknowledge the observation
2. Implement the correction (if feasible)
3. Document the correction with before/after evidence
4. Inform the inspector that the correction has been made
5. Include in the formal response as "corrected during inspection"
```

**Expected:** Response templates enable rapid, structured replies to inspection observations.
**On failure:** If response templates are generic and do not address the specific observation, customise each response with specific evidence and timelines.

## Validation

- [ ] Agency-specific focus areas analysed with risk ratings
- [ ] Readiness self-assessment completed with quantified scores
- [ ] Remediation plan created for all gaps with owners and deadlines
- [ ] Document bundles assembled and indexed for all in-scope systems
- [ ] Mock inspection conducted with documented findings and follow-up
- [ ] Inspection logistics plan defines rooms, roles, and communication protocol
- [ ] Response templates prepared for common observation types
- [ ] All critical remediation items closed before the inspection date

## Common Pitfalls

- **Last-minute preparation**: Inspection readiness is a continuous programme, not a cramming exercise. Organisations that scramble produce disorganised, incomplete responses.
- **Hiding problems**: Inspectors are experienced professionals who detect concealment. Transparency with a clear remediation plan is always better than attempted concealment.
- **Over-volunteering information**: Answer the question that was asked. Providing unsolicited information can open new lines of inquiry.
- **Untrained personnel**: Subject matter experts who have never practiced responding to inspector questions perform poorly. Mock inspections are essential practice.
- **Ignoring the back room**: The back room (document retrieval and strategy coordination) is as important as the front room. Poor document retrieval creates the impression of disorganisation.

## Related Skills

- `design-compliance-architecture` — the foundation document inspectors will want to see
- `conduct-gxp-audit` — internal audits should mimic inspection methodology
- `monitor-data-integrity` — data integrity is the top FDA inspection focus area
- `investigate-capa-root-cause` — CAPAs must be thoroughly investigated before inspection
- `qualify-vendor` — vendor qualifications are frequently requested during inspections
