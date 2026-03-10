---
name: monitor-data-integrity
description: >
  Design and operate a data integrity monitoring programme based on ALCOA+
  principles. Covers detective controls, audit trail review schedules,
  anomaly detection patterns (off-hours activity, sequential modifications,
  bulk changes), metrics dashboards, investigation triggers, and escalation
  matrix definition. Use when establishing a data integrity monitoring
  programme for GxP systems, preparing for inspections where data integrity
  is a focus area, after a data integrity incident requiring enhanced
  monitoring, or when implementing MHRA, WHO, or PIC/S guidance.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: compliance
  complexity: advanced
  language: multi
  tags: gxp, data-integrity, alcoa, monitoring, anomaly-detection, compliance
---

# Monitor Data Integrity

Design and operate a programme that continuously monitors data integrity across validated systems using ALCOA+ principles and anomaly detection.

## When to Use

- Establishing a data integrity monitoring programme for GxP systems
- Regulatory inspection preparation where data integrity is a focus area
- After a data integrity incident requiring enhanced monitoring
- Periodic review of existing data integrity controls
- Implementing MHRA, WHO, or PIC/S data integrity guidance

## Inputs

- **Required**: Systems in scope and their ALCOA+ risk profile
- **Required**: Applicable guidance (MHRA Data Integrity, WHO TRS 996, PIC/S PI 041)
- **Required**: Current audit trail capabilities of each system
- **Optional**: Previous data integrity findings or regulatory observations
- **Optional**: Existing monitoring procedures or metrics
- **Optional**: User access matrices and role definitions

## Procedure

### Step 1: Assess Current ALCOA+ Posture

Evaluate each system against all ALCOA+ principles:

```markdown
# Data Integrity Assessment
## Document ID: DIA-[SITE]-[YYYY]-[NNN]

### ALCOA+ Assessment Matrix

| Principle | Definition | Assessment Questions | System 1 | System 2 |
|-----------|-----------|---------------------|----------|----------|
| **Attributable** | Who performed the action and when? | Are all entries linked to unique user IDs? Is the timestamp system-generated? | G/A/R | G/A/R |
| **Legible** | Can data be read and understood? | Are records readable throughout retention period? Are formats controlled? | G/A/R | G/A/R |
| **Contemporaneous** | Was data recorded at the time of the activity? | Are timestamps real-time? Are backdated entries detectable? | G/A/R | G/A/R |
| **Original** | Is this the first-captured data? | Are original records preserved? Is there a clear original vs copy distinction? | G/A/R | G/A/R |
| **Accurate** | Is the data correct and truthful? | Are calculations verified? Are transcription errors detectable? | G/A/R | G/A/R |
| **Complete** | Is all data present? | Are deletions detectable? Are all expected records present? | G/A/R | G/A/R |
| **Consistent** | Are data elements consistent across records? | Do timestamps follow logical sequence? Are versions consistent? | G/A/R | G/A/R |
| **Enduring** | Will data survive for the required retention period? | Is the storage medium reliable? Are backups verified? | G/A/R | G/A/R |
| **Available** | Can data be accessed when needed? | Are retrieval procedures documented? Are access controls appropriate? | G/A/R | G/A/R |

Rating: G = Good (controls adequate), A = Adequate (minor improvements needed), R = Remediation required
```

**Expected:** Every system has a rated ALCOA+ assessment with specific findings for each principle.
**On failure:** If a system cannot be assessed (e.g., no audit trail capability), flag it as a critical gap requiring immediate remediation.

### Step 2: Design Detective Controls

Define the monitoring activities that detect data integrity violations:

```markdown
# Detective Controls Design
## Document ID: DCD-[SITE]-[YYYY]-[NNN]

### Audit Trail Review Schedule
| System | Review Type | Frequency | Reviewer | Scope |
|--------|-----------|-----------|----------|-------|
| LIMS | Comprehensive | Monthly | QA | All data modifications, deletions, and access events |
| ERP | Targeted | Weekly | QA | Batch record modifications and approvals |
| R/Shiny | Comprehensive | Per analysis | Statistician | All input/output/parameter changes |

### Review Checklist
For each audit trail review cycle:
- [ ] All data modifications have documented justification
- [ ] No unexplained deletions or void entries
- [ ] Timestamps are sequential and consistent with business operations
- [ ] No off-hours activity without documented justification
- [ ] No shared account usage detected
- [ ] Failed login attempts are within normal thresholds
- [ ] No privilege escalation events outside change control
```

**Expected:** Detective controls are scheduled, assigned, and documented with clear review criteria.
**On failure:** If audit trail reviews are not performed on schedule, document the gap and escalate to QA management. Missed reviews accumulate risk.

### Step 3: Define Anomaly Detection Patterns

Create specific patterns that trigger investigation:

```markdown
# Anomaly Detection Patterns

### Pattern 1: Off-Hours Activity
**Trigger:** Data creation, modification, or deletion outside business hours (defined as [06:00-20:00 local time, Monday-Friday])
**Threshold:** Any GxP-critical data modification outside defined hours
**Response:** Verify with user and supervisor within 2 business days
**Exceptions:** Documented shift work, approved overtime, automated processes

### Pattern 2: Sequential Modifications
**Trigger:** Multiple modifications to the same record within a short timeframe
**Threshold:** >3 modifications to the same record within 60 minutes
**Response:** Review modification reasons; verify each change has documented justification
**Exceptions:** Initial data entry corrections within [grace period, e.g., 30 minutes]

### Pattern 3: Bulk Changes
**Trigger:** Unusually high volume of data modifications by a single user
**Threshold:** >50 modifications per user per day (baseline: [calculate from normal usage])
**Response:** Verify business justification for bulk activity
**Exceptions:** Documented batch operations, data migration activities under change control

### Pattern 4: Delete/Void Spikes
**Trigger:** Unusual number of record deletions or voidings
**Threshold:** >5 delete/void events per user per week
**Response:** Immediate QA review of deleted/voided records
**Exceptions:** None — all delete/void events require documented justification

### Pattern 5: Privilege Escalation
**Trigger:** User access changes granting administrative or elevated privileges
**Threshold:** Any privilege change outside the user access management SOP
**Response:** Verify with IT security and system owner within 24 hours
**Exceptions:** Emergency access per documented emergency access procedure

### Pattern 6: Audit Trail Gaps
**Trigger:** Missing or interrupted audit trail entries
**Threshold:** Any gap > 0 entries (audit trail should be continuous)
**Response:** Immediate investigation — potential system malfunction or tampering
**Exceptions:** None — audit trail gaps are always critical
```

**Expected:** Patterns are specific, measurable, and actionable with defined thresholds and response procedures.
**On failure:** If thresholds are set too low (excessive false positives), adjust based on baseline data. If too high (missing real issues), tighten after the first monitoring cycle.

### Step 4: Build Metrics Dashboard

```markdown
# Data Integrity Metrics Dashboard
## Document ID: DIMD-[SITE]-[YYYY]-[NNN]

### Key Performance Indicators

| KPI | Metric | Target | Yellow Threshold | Red Threshold | Source |
|-----|--------|--------|-----------------|---------------|--------|
| DI-01 | Audit trail review completion rate | 100% | <95% | <90% | Review log |
| DI-02 | Anomalies detected per month | Trending down | >10% increase MoM | >25% increase MoM | Anomaly log |
| DI-03 | Anomaly investigation closure rate | <15 business days | >15 days | >30 days | Investigation log |
| DI-04 | Open data integrity CAPAs | 0 overdue | 1-2 overdue | >2 overdue | CAPA tracker |
| DI-05 | Shared account instances detected | 0 | 1-2 | >2 | Access review |
| DI-06 | Unauthorised access attempts | <5/month | 5-10/month | >10/month | System logs |
| DI-07 | Audit trail gap events | 0 | N/A | >0 (always red) | System monitoring |

### Reporting Cadence
| Report | Frequency | Audience | Owner |
|--------|-----------|----------|-------|
| DI Metrics Summary | Monthly | QA Director, System Owners | QA Analyst |
| DI Trend Report | Quarterly | Quality Council | QA Manager |
| DI Annual Review | Annual | Site Director | QA Director |
```

**Expected:** Dashboard provides at-a-glance compliance status with clear escalation triggers.
**On failure:** If data sources cannot support automated metrics, implement manual collection and document the plan to automate.

### Step 5: Establish Investigation Triggers and Escalation

```markdown
# Investigation and Escalation Matrix

### Investigation Triggers
| Trigger | Severity | Response Time | Investigator |
|---------|----------|---------------|-------------|
| Audit trail gap detected | Critical | Immediate (within 4 hours) | IT + QA |
| Confirmed data falsification | Critical | Immediate (within 4 hours) | QA Director |
| Anomaly pattern confirmed after review | Major | Within 5 business days | QA Analyst |
| Repeated anomalies from same user | Major | Within 5 business days | QA + HR |
| Overdue audit trail review | Minor | Within 10 business days | QA Manager |

### Escalation Path
| Level | Escalated To | When |
|-------|-------------|------|
| 1 | System Owner | Any confirmed anomaly |
| 2 | QA Director | Major or critical finding |
| 3 | Site Director | Critical finding or potential regulatory impact |
| 4 | Regulatory Affairs | Confirmed data integrity failure requiring regulatory notification |
```

**Expected:** Every investigation has a defined severity, timeline, and escalation path.
**On failure:** If investigations are not completed within defined timelines, escalate to the next level.

### Step 6: Compile the Monitoring Plan

Assemble all components into the master data integrity monitoring plan:

```markdown
# Data Integrity Monitoring Plan
## Document ID: DI-MONITORING-PLAN-[SITE]-[YYYY]-[NNN]

### 1. Purpose and Scope
[From assessment scope]

### 2. ALCOA+ Assessment Summary
[From Step 1]

### 3. Detective Controls
[From Step 2]

### 4. Anomaly Detection Rules
[From Step 3]

### 5. Metrics and Reporting
[From Step 4]

### 6. Investigation and Escalation
[From Step 5]

### 7. Periodic Review
- Monitoring plan review: Annual
- Anomaly thresholds: Adjust after each quarterly review
- ALCOA+ re-assessment: When systems change or new systems are added

### 8. Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| QA Director | | | |
| IT Director | | | |
| Site Director | | | |
```

**Expected:** A single, approved document that defines the complete data integrity monitoring programme.
**On failure:** If the plan is too large for a single document, create a master plan with references to system-specific monitoring procedures.

## Validation

- [ ] ALCOA+ assessment completed for all in-scope systems
- [ ] Audit trail review schedule defined with frequency, scope, and responsible reviewer
- [ ] At least 5 anomaly detection patterns defined with specific thresholds
- [ ] Metrics dashboard has KPIs with green/yellow/red thresholds
- [ ] Investigation triggers defined with severity and response timelines
- [ ] Escalation matrix reaches regulatory affairs for critical findings
- [ ] Monitoring plan approved by QA and IT leadership
- [ ] Periodic review schedule established

## Common Pitfalls

- **Monitoring without action**: Collecting metrics but never investigating anomalies provides a false sense of security and is worse than no monitoring (it generates evidence of ignored findings).
- **Static thresholds**: Thresholds based on guesswork rather than baseline data generate excessive false positives, leading to alert fatigue.
- **Audit trail review as checkbox**: Reviewing audit trails without understanding what to look for is ineffective. Train reviewers on anomaly detection patterns.
- **Ignoring system limitations**: Some systems have poor audit trail capabilities. Document limitations and implement compensating controls rather than pretending the limitation doesn't exist.
- **No trending**: Individual anomalies may seem minor, but patterns across time or users reveal systemic issues. Always trend data integrity metrics.

## Related Skills

- `design-compliance-architecture` — identifies systems requiring data integrity monitoring
- `implement-audit-trail` — the technical foundation that monitoring relies on
- `investigate-capa-root-cause` — when monitoring detects issues requiring formal investigation
- `conduct-gxp-audit` — audits assess the effectiveness of the monitoring programme
- `prepare-inspection-readiness` — data integrity is a primary regulatory inspection focus area
