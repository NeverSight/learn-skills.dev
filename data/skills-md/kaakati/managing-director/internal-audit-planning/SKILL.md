---
name: internal-audit-planning
description: >
  Internal audit planning engine that builds risk-based audit universes,
  prioritizes engagements, designs control testing programs, and produces
  audit committee-ready reports. USE THIS SKILL when the user mentions
  internal audit plan, audit universe, control testing, audit program,
  audit committee reporting, audit risk assessment, sampling methodology,
  audit findings, issue tracking, or quality assurance and improvement
  program (QAIP). Covers the full audit lifecycle from planning through
  follow-up.
---

# Internal Audit Planning

## Required Inputs

- **Organization**: Company name, industry, and organizational structure.
- **Audit Period**: Fiscal year or period covered by the audit plan.
- **Available Audit Resources**: Number of auditors, total available audit days, budget.
- **Prior Audit Results**: Previous findings, open issues, and management action plans.
- **Risk Assessment Output**: Enterprise risk register or risk assessment (link to `enterprise-risk-assessment` skill if needed).
- **Regulatory Environment**: Key regulations and compliance obligations.
- **Stakeholder Priorities**: Board, audit committee, and management concerns.

## Execution Steps

### 1. Define the Audit Universe

Map every auditable entity in the organization. The audit universe is exhaustive -- nothing is excluded without documented justification.

**Audit Universe Categories**

| Category | Examples | Typical Entities |
|---|---|---|
| Business Units | Divisions, subsidiaries, regions | 5-50 per organization |
| Core Processes | Revenue cycle, procurement, payroll, treasury | 8-15 standard processes |
| IT Systems | ERP, CRM, cloud platforms, custom applications | 10-30+ systems |
| Compliance Programs | SOX, data privacy, anti-corruption, AML | 3-10 programs |
| Third Parties | Key vendors, outsourced functions, JV partners | 5-20 critical relationships |
| Projects & Initiatives | Major transformations, M&A integration, system implementations | 2-10 active projects |
| Governance Functions | Board processes, ethics program, enterprise risk management | 3-5 functions |

**Audit Universe Template**

| Entity ID | Entity Name | Category | Business Owner | Last Audited | Last Rating | Risk Score | Audit Cycle |
|---|---|---|---|---|---|---|---|
| AU-001 | [Entity] | [Category] | [Role] | [Date or Never] | [Satisfactory/Needs Improvement/Unsatisfactory/N/A] | [1-25] | [Annual/Biennial/Triennial] |

### 2. Risk-Based Audit Prioritization

Score each auditable entity on weighted risk factors to determine audit priority.

**Risk Factor Scoring Model**

| Risk Factor | Weight | Score 1 (Low) | Score 3 (Medium) | Score 5 (High) |
|---|---|---|---|---|
| Financial Impact | 20% | <$1M revenue/assets | $1M-$50M | >$50M |
| Regulatory Exposure | 20% | Minimal regulatory oversight | Moderate regulation | Heavy regulation, recent enforcement |
| Operational Complexity | 15% | Simple, stable process | Moderate complexity | Highly complex, many handoffs |
| Change Velocity | 15% | No significant changes | Moderate changes (new system, reorg) | Major transformation underway |
| Prior Audit Results | 15% | Clean, no issues | Minor findings | Significant findings or repeat issues |
| Time Since Last Audit | 10% | <12 months | 12-24 months | >24 months or never audited |
| Management Concern | 5% | No concerns raised | Some concerns | Specific request from board/management |

**Composite Risk Score Calculation**

```
Composite Score = SUM(Factor Weight x Factor Score)
Range: 1.00 (lowest risk) to 5.00 (highest risk)
```

**Priority Classification**

| Priority | Composite Score | Audit Frequency | Resource Allocation |
|---|---|---|---|
| Mandatory | N/A (regulatory) | Annual | As required |
| Priority 1 | 4.01 - 5.00 | Annual | Full-scope audit |
| Priority 2 | 3.01 - 4.00 | Annual or biennial | Full or targeted audit |
| Priority 3 | 2.01 - 3.00 | Biennial or triennial | Targeted or limited review |
| Priority 4 | 1.00 - 2.00 | Triennial or risk-monitored | Continuous monitoring only |

### 3. Annual Audit Plan Construction

Translate prioritized entities into a resourced, scheduled audit plan.

**Resource Allocation Formula**

```
Available Audit Days = (Number of Auditors x Working Days) - Training - Admin - Carry-forward
Typical: 1 auditor = 220 working days - 20 training - 30 admin = 170 available audit days
```

**Engagement Effort Estimates**

| Engagement Type | Typical Duration (Days) | Team Size | Total Effort |
|---|---|---|---|
| Full-scope audit | 15-30 | 2-3 | 30-90 days |
| Targeted/focused audit | 8-15 | 1-2 | 8-30 days |
| Follow-up review | 3-5 | 1 | 3-5 days |
| Continuous monitoring | Ongoing | 0.5 FTE | 85 days/year |
| Advisory/consulting | 5-15 | 1-2 | 5-30 days |
| Investigation | Variable | 2-3 | 20-60 days |

**Annual Audit Plan Template**

| Engagement ID | Entity | Type | Objective | Q1 | Q2 | Q3 | Q4 | Lead Auditor | Est. Days | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| IA-2025-001 | [Entity] | Full-scope | [Objective] | X | | | | [Name/Role] | [Days] | P1 |
| IA-2025-002 | [Entity] | Targeted | [Objective] | | X | | | [Name/Role] | [Days] | P1 |

**Plan Coverage Analysis**

```
Audit Universe Coverage = Entities Planned for Audit / Total Entities in Universe
Target: 100% coverage within a 3-year rolling cycle
Annual coverage target: 33-50% of audit universe
```

### 4. Audit Scope and Objectives Framework

For each engagement, define scope, objectives, and approach before fieldwork begins.

**Engagement Planning Memo Template**

| Element | Detail |
|---|---|
| Engagement Title | [Descriptive title] |
| Auditable Entity | [From audit universe] |
| Audit Objective | [What the audit will assess -- controls, compliance, efficiency] |
| Scope Period | [Transaction period under review] |
| Scope Boundaries | [In scope / out of scope] |
| Key Risks | [Top 3-5 risks from risk assessment] |
| Audit Criteria | [Standards, policies, regulations against which to assess] |
| Methodology | [Interviews, walkthroughs, sample testing, data analytics] |
| Timeline | [Fieldwork start/end, draft report, final report] |
| Team | [Lead, staff, specialists] |
| Budget | [Planned hours/days] |

### 5. Control Testing Methodology

Test controls for both design effectiveness and operating effectiveness.

**Phase A: Design Effectiveness (Does the control address the risk?)**

| Test | Question | Evidence |
|---|---|---|
| Control objective alignment | Does the control directly mitigate the identified risk? | Policy, procedure documentation |
| Completeness | Are all key risk scenarios addressed by at least one control? | Control-risk matrix |
| Authority and segregation | Are appropriate approvals and segregation of duties in place? | Org chart, access matrix |
| Timeliness | Is the control performed at the right frequency? | Procedure documentation |
| Information quality | Does the control use reliable, complete information? | Data source analysis |

**Phase B: Operating Effectiveness (Is the control working as designed?)**

| Test Type | When to Use | Example |
|---|---|---|
| Inquiry | Always (but never alone) | Interview the control operator about how they perform the control |
| Observation | Real-time processes | Watch a supervisor review and approve journal entries |
| Inspection | Document-based controls | Examine signed approvals on purchase orders |
| Reperformance | Calculated/automated controls | Independently recalculate a reconciliation |
| Data analytics | High-volume transactions | Run full-population analysis on payment data |

**Control Conclusion Matrix**

| Design Effective? | Operating Effective? | Overall Conclusion |
|---|---|---|
| Yes | Yes | Effective -- rely on control |
| Yes | No | Operating deficiency -- finding required |
| No | Not tested | Design deficiency -- finding required |
| No | N/A | Material weakness candidate |

### 6. Sampling Methodology

**Sample Size Guidance (Attribute Testing)**

| Population Size | Expected Deviation Rate 0% | Expected Deviation Rate 1-2% | Expected Deviation Rate 3-5% |
|---|---|---|---|
| < 50 | Test all | Test all | Test all |
| 50-100 | 25-30 | 30-40 | 40-50 |
| 101-500 | 25-30 | 30-45 | 45-60 |
| 501-2,000 | 25-30 | 35-50 | 50-60 |
| 2,001-10,000 | 25-30 | 40-55 | 55-60 |
| > 10,000 | 25-30 | 45-60 | 58-60 |

**Sampling Method Selection**

| Method | When to Use |
|---|---|
| Random | Standard attribute testing, unbiased population |
| Stratified | Population has distinct subgroups (e.g., by dollar amount or location) |
| Haphazard | Quick directional testing only, not for formal conclusions |
| Judgmental | Targeted high-risk items (large dollar, unusual transactions) |
| Full population (data analytics) | Preferred when feasible -- eliminates sampling risk entirely |

### 7. Audit Finding Severity Classification

Align with the practice risk rating scale but add audit-specific context.

| Severity | Definition | Management Response Timeline | Escalation |
|---|---|---|---|
| **Critical** | Control failure that has resulted in or could imminently result in material financial loss, regulatory sanction, or safety incident. Immediate executive and audit committee notification required. | Immediate action plan; remediation within 30 days | Audit Committee, CEO |
| **High** | Significant control deficiency with high likelihood of material impact if not remediated. No compensating controls in place. | Action plan within 5 business days; remediation within 60 days | CAE, CFO, relevant C-suite |
| **Medium** | Moderate control weakness. Compensating controls partially mitigate risk. Repeat finding elevates to High. | Action plan within 10 business days; remediation within 90 days | CAE, business unit head |
| **Low** | Minor control improvement opportunity. Unlikely to result in material impact. Best practice recommendation. | Addressed in normal course; remediation within 180 days | Audit management, process owner |
| **Advisory** | Observation or efficiency recommendation. Not a control deficiency. | Optional | Process owner |

### 8. Reporting Templates

**Individual Audit Report Structure**

```markdown
## Internal Audit Report: [Engagement Title]
### Report ID: [IA-YYYY-NNN]

| Field | Detail |
|---|---|
| Entity Audited | [Name] |
| Audit Period | [Start - End] |
| Report Date | [Date] |
| Overall Rating | [Satisfactory / Needs Improvement / Unsatisfactory] |
| Lead Auditor | [Name] |
| Distribution | [Names and roles] |

### Executive Summary
[2-3 paragraph summary: scope, key findings, overall opinion]

### Overall Opinion
[Satisfactory / Needs Improvement / Unsatisfactory] with basis for opinion.

### Scope and Methodology
- Objectives: [What we assessed]
- Period: [Transaction dates reviewed]
- Methodology: [Testing approach]
- Limitations: [Any scope restrictions]

### Findings and Recommendations
#### Finding 1: [Title]
| Attribute | Detail |
|---|---|
| Severity | [Critical/High/Medium/Low] |
| Condition | [What we found] |
| Criteria | [What should be] |
| Cause | [Why the gap exists] |
| Effect | [Actual or potential impact] |
| Recommendation | [What to do] |
| Management Response | [Agree/Disagree + action plan] |
| Target Date | [Remediation deadline] |
| Responsible Owner | [Name and role] |

### Appendices
- A: Detailed test results
- B: Population and sample details
- C: Documents reviewed
```

**Quarterly Audit Committee Summary**

```markdown
## Internal Audit Quarterly Report to Audit Committee
### Period: [Q# FY####]

### Plan Execution Status
| Metric | Target | Actual | Variance |
|---|---|---|---|
| Audits completed | [#] | [#] | [+/-] |
| Audit days used | [#] | [#] | [+/-] |
| Plan completion (YTD) | [%] | [%] | [+/-] |

### Completed Audits This Quarter
| Engagement | Rating | Critical | High | Medium | Low |
|---|---|---|---|---|---|
| [Name] | [Rating] | [#] | [#] | [#] | [#] |

### Open Findings Aging
| Aging Bucket | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Current (within target date) | [#] | [#] | [#] | [#] | [#] |
| Overdue 0-30 days | [#] | [#] | [#] | [#] | [#] |
| Overdue 31-90 days | [#] | [#] | [#] | [#] | [#] |
| Overdue > 90 days | [#] | [#] | [#] | [#] | [#] |

### Key Themes and Emerging Risks
[Narrative on patterns across audits, new risks identified]

### Plan Amendments
[Any changes to the annual plan with rationale]

### Resource and Budget Update
[Staffing, co-source usage, budget status]
```

### 9. Follow-Up and Issue Tracking Framework

**Issue Lifecycle**

```
Finding Issued --> Management Response (5-10 days) --> Action Plan Agreed
--> Implementation In Progress --> Validation Testing --> Closed / Escalated
```

**Follow-Up Cadence**

| Finding Severity | Follow-Up Frequency | Validation Method |
|---|---|---|
| Critical | Every 2 weeks until closed | Full retest required |
| High | Monthly until closed | Full retest required |
| Medium | Quarterly until closed | Evidence review + targeted retest |
| Low | Semi-annually | Evidence review |

**Escalation Protocol**

| Trigger | Action |
|---|---|
| Management response not received within deadline | Escalate to next management level |
| Target date missed once | Extend with CAE approval; report to audit committee |
| Target date missed twice | Mandatory audit committee agenda item |
| Finding open > 12 months | Automatic escalation to audit committee chair |
| Management accepts risk (no remediation) | Document risk acceptance with sign-off at appropriate level |

### 10. Quality Assurance and Improvement Program (QAIP)

Per IIA Standard 1300 -- maintain a QAIP covering all aspects of the internal audit activity.

**Internal Assessments (Ongoing + Periodic)**

| Assessment Type | Frequency | Performed By | Focus |
|---|---|---|---|
| Engagement supervision | Every engagement | Audit management | Workpaper review, conclusion support |
| Post-engagement survey | Every engagement | Auditee feedback | Professionalism, communication, value |
| KPI monitoring | Monthly | CAE | Plan completion, cycle time, findings trends |
| Self-assessment | Annually | Audit team | Conformance with IIA Standards |

**External Assessment**

| Requirement | Detail |
|---|---|
| Frequency | At least every 5 years (IIA Standard 1312) |
| Performed By | Qualified, independent assessor or assessment team |
| Scope | Full conformance with IIA Standards and Code of Ethics |
| Output | Opinion: Generally Conforms / Partially Conforms / Does Not Conform |
| Reporting | Results reported to audit committee |

**Key Performance Indicators (KPIs)**

| KPI | Target | Measurement |
|---|---|---|
| Audit plan completion rate | >= 90% | Completed audits / planned audits |
| Report cycle time | <= 15 business days from fieldwork end | Average days to final report |
| Finding closure rate | >= 80% closed on time | On-time closures / total closures |
| Stakeholder satisfaction | >= 4.0 / 5.0 | Post-engagement survey average |
| Repeat finding rate | <= 10% | Repeat findings / total findings |
| Budget variance | +/- 10% | Actual vs. planned audit days |

### 11. Audit Committee Communication Protocol

**Standing Agenda Items (Quarterly)**

1. Audit plan execution status and any proposed amendments
2. Completed audit results with ratings and significant findings
3. Open findings aging and overdue issue escalation
4. Emerging risks identified through audit activities
5. Resource and budget update
6. External audit coordination summary

**Ad Hoc Communications (Triggered by Events)**

| Trigger | Communication | Timeline |
|---|---|---|
| Critical finding identified | Immediate notification to audit committee chair | Within 24 hours of confirmation |
| Fraud or suspected fraud | Immediate notification to audit committee chair and general counsel | Within 24 hours |
| Scope limitation imposed by management | Written notification to audit committee | Within 5 business days |
| Significant change to audit plan | Approval request with rationale | Before implementation |
| CAE independence threat | Direct communication to audit committee chair | Immediately |

## Output Template

```markdown
## Internal Audit Plan: [Organization] -- [Fiscal Year]

### Approved By
| Role | Name | Date |
|---|---|---|
| Chief Audit Executive | [Name] | [Date] |
| Audit Committee Chair | [Name] | [Date] |

### Audit Universe Summary
| Category | Total Entities | P1 | P2 | P3 | P4 | Mandatory |
|---|---|---|---|---|---|---|
| Business Units | [#] | [#] | [#] | [#] | [#] | [#] |
| Core Processes | [#] | [#] | [#] | [#] | [#] | [#] |
| IT Systems | [#] | [#] | [#] | [#] | [#] | [#] |
| Compliance Programs | [#] | [#] | [#] | [#] | [#] | [#] |
| Third Parties | [#] | [#] | [#] | [#] | [#] | [#] |
| Projects | [#] | [#] | [#] | [#] | [#] | [#] |
| **Total** | [#] | [#] | [#] | [#] | [#] | [#] |

### Resource Budget
| Resource Category | Days |
|---|---|
| Total available audit days | [#] |
| Planned engagements | [#] |
| Follow-up reviews | [#] |
| Advisory/consulting reserve | [#] |
| Investigation reserve | [#] |
| Training and development | [#] |
| Administration | [#] |
| Unallocated reserve (contingency) | [#] |

### Annual Audit Plan
| ID | Entity | Type | Objective | Quarter | Lead | Days | Priority |
|---|---|---|---|---|---|---|---|
| IA-YYYY-001 | [Entity] | [Type] | [Objective] | Q# | [Lead] | [#] | [P#] |

### Three-Year Rolling Coverage
| Entity | Current Year | Year +1 | Year +2 | Cycle |
|---|---|---|---|---|
| [Entity] | Full audit | Monitor | Targeted | Biennial |

### Key Risk Themes Driving the Plan
1. [Theme]: [Which audits address this risk]
2. [Theme]: [Which audits address this risk]

### QAIP Summary
[Current conformance status, planned assessments, KPI targets]
```

## Quality Checks

- [ ] Audit universe is exhaustive -- all business units, processes, IT systems, compliance programs, third parties, and projects identified.
- [ ] Risk-based prioritization uses weighted, documented scoring -- not gut feel.
- [ ] Resource allocation is mathematically feasible (planned days <= available days with contingency reserve).
- [ ] Every engagement has a defined objective, scope, and methodology.
- [ ] Control testing covers both design effectiveness and operating effectiveness.
- [ ] Sampling methodology is documented and defensible.
- [ ] Finding severity classification aligns with the practice risk rating scale (Critical/High/Medium/Low).
- [ ] Individual audit reports use the Condition-Criteria-Cause-Effect format.
- [ ] Quarterly audit committee reporting covers plan status, findings aging, and emerging risks.
- [ ] Follow-up cadence matches finding severity with defined escalation triggers.
- [ ] QAIP includes both internal assessments (ongoing) and external assessment (every 5 years per IIA Standard 1312).
- [ ] Three-year rolling coverage ensures 100% audit universe coverage within the cycle.
