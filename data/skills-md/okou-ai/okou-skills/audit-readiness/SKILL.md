---
name: audit-readiness
description: Prepare audit workpapers, control tests, samples, evidence, deficiencies, and remediation tracking.
---

## SOX 404 Testing Lifecycle

### End-to-End Phases

1. **Scoping:** Determine which accounts and processes carry enough risk to warrant control coverage
2. **Risk evaluation:** Assess the probability and magnitude of potential misstatement for each in-scope account
3. **Control mapping:** Document the specific controls that mitigate each identified risk
4. **Effectiveness testing:** Evaluate whether controls are properly engineered (design) and consistently executed (operation)
5. **Deficiency assessment:** Judge the severity of any control gaps uncovered during testing
6. **Management reporting:** Formalize the overall ICFR assessment and disclose any material weaknesses

### Determining Which Accounts Are In Scope

An account enters scope when it carries a non-remote probability of containing a misstatement that is material on its own or in combination with others.

**Size-based indicators:**
- The balance surpasses the quantitative materiality benchmark (commonly 3-5% of a reference figure such as revenue, assets, or pre-tax income)
- High transaction throughput increases the statistical likelihood of error
- The balance depends heavily on estimates or management judgment

**Risk-based indicators:**
- The accounting is inherently complex (multi-element revenue arrangements, derivative instruments, pension obligations)
- The account is a common fraud target (cash, revenue, related-party activity)
- Historical audit adjustments or prior restatements have affected the account
- Significant management estimates or subjective assumptions underlie the balance
- The account or process is new, or has undergone material change

### Financial Statement Assertions by Account Category

| Account Category | Primary Assertions to Address |
|---|---|
| Revenue | Occurrence, Completeness, Measurement, Period allocation |
| Trade receivables | Existence, Valuation (reserve adequacy), Ownership rights |
| Inventory | Existence, Valuation, Completeness |
| Property & equipment | Existence, Valuation, Completeness, Ownership rights |
| Trade payables | Completeness, Measurement, Existence |
| Accrued obligations | Completeness, Valuation, Measurement |
| Shareholders' equity | Completeness, Measurement, Presentation |
| Close & reporting process | Presentation, Measurement, Completeness |

### Design vs. Operating Effectiveness

**Design effectiveness** asks: Is the control architected to intercept or surface a material misstatement in the targeted assertion?
- Assessed via end-to-end walkthroughs (trace a representative transaction through the full process)
- Confirm the control sits at the correct process juncture
- Confirm the control directly addresses the specified risk
- Re-evaluate at least annually, or whenever the process changes

**Operating effectiveness** asks: Has the control actually functioned as intended across the entire period under review?
- Assessed via inspection, observation, recalculation, or inquiry (with corroboration)
- Requires sample sizes large enough to support a reliable conclusion
- Must span the full reliance period (not just a single point in time)

## Sampling Methodologies

### Statistical Random Sampling

**Applicability:** Standard approach for high-volume, transaction-level controls.

**Steps:**
1. Define the universe: every transaction subject to the control during the test period
2. Assign a sequential identifier to each population item
3. Apply a random-number generator to draw the sample
4. Confirm every item had an equal selection probability (no systematic exclusion)

**Strengths:** Statistically defensible, free of selection bias
**Limitations:** May not capture high-risk outliers; requires a complete population listing

### Risk-Directed (Judgmental) Sampling

**Applicability:** Complements random sampling by targeting items with elevated risk characteristics; serves as the primary method for small or heterogeneous populations.

**Targeting criteria:**
- Transactions above a defined dollar threshold
- Atypical or non-standard entries
- Activity near the period boundary (cut-off exposure)
- Related-party transactions
- Manual overrides or exception-processed items
- First-time vendors or customers

**Strengths:** Focuses testing effort on highest-risk items
**Limitations:** Not statistically representative; must document the selection rationale

### Unstructured (Haphazard) Sampling

**Applicability:** Situations where a numbered population is unavailable and items are relatively uniform.

**Steps:**
1. Select items without a deliberate pattern
2. Distribute selections across the entire test period
3. Guard against unconscious tendencies (gravitating toward top-of-list, round figures, etc.)

**Strengths:** Simple, requires no tooling
**Limitations:** Not statistically valid; vulnerable to unintentional bias

### Interval-Based (Systematic) Sampling

**Applicability:** Sequential populations where uniform period coverage is desired.

**Steps:**
1. Compute the selection interval: total population count divided by target sample size
2. Pick a random starting point within the first interval
3. Select every Nth item from that starting point forward

**Illustration:** 1,000-item population, 25-item sample -> interval of 40. Random start at item 12. Selections: 12, 52, 92, 132 ...

**Strengths:** Guarantees even distribution across the population
**Limitations:** Periodic patterns in the data could skew results

### Sample Size Reference Table

| Control Cadence | Approximate Population | Lower-Risk Sample | Moderate-Risk Sample | Higher-Risk Sample |
|---|---|---|---|---|
| Annual | 1 | 1 | 1 | 1 |
| Quarterly | 4 | 2 | 2 | 3 |
| Monthly | 12 | 2 | 3 | 4 |
| Weekly | ~52 | 5 | 8 | 15 |
| Daily | ~250 | 20 | 30 | 40 |
| Per-transaction (under 250) | < 250 | 20 | 30 | 40 |
| Per-transaction (250+) | 250+ | 25 | 40 | 60 |

**Conditions that warrant larger samples:**
- Elevated inherent risk in the account or process
- The control is the only safeguard for a significant risk (no backup control)
- A deficiency was noted in a prior testing cycle
- The control is newly implemented and untested historically
- External auditors plan to rely on management's testing results

## Workpaper & Evidence Standards

### Required Workpaper Sections

1. **Control profile:**
   - Unique control identifier
   - Narrative description (who does what, how frequently)
   - Classification (manual, automated, IT-dependent manual)
   - Execution frequency
   - Targeted risk and assertion

2. **Test blueprint:**
   - Stated objective of the test
   - Detailed procedural steps
   - Description of expected evidence when the control is working
   - Sampling method and rationale for approach chosen

3. **Execution record:**
   - Population description and total count
   - Sample items selected (method and specific identifiers)
   - Item-by-item results (pass/fail with the specific evidence inspected)
   - Full narrative for every exception observed

4. **Overall conclusion:**
   - Effectiveness rating (effective / deficiency / significant deficiency / material weakness)
   - Reasoning supporting the conclusion
   - Magnitude assessment for any exceptions
   - Compensating controls evaluated, if relevant

5. **Accountability:**
   - Tester signature and date
   - Reviewer signature and date

### What Constitutes Adequate Evidence

**Acceptable:**
- System screenshots capturing enforced controls or configurations
- Documents bearing a signature, initials, or electronic approval stamp
- Email trails with an identifiable approver and a discernible date
- Application audit logs recording the actor, action, and timestamp
- Independent recalculations that reproduce the recorded result
- Written observation notes specifying date, location, and observer

**Not sufficient on its own:**
- Oral statements without corroboration
- Documents lacking a date
- Evidence with no identifiable performer or approver
- System-generated output missing date/time metadata
- Notes reading "per conversation with [name]" absent supporting documentation

### File Organization Convention

```
ICFR Testing/
  [Fiscal Year]/
    Scoping & Risk Assessment/
    Revenue Process/
      Control Matrix
      Walkthrough Narrative
      Individual Test Workpapers
      Evidence Attachments
    Purchase-to-Pay Process/
    Payroll Process/
    Financial Close Process/
    Treasury Process/
    Capital Assets Process/
    IT General Controls/
    Organization-Level Controls/
    Aggregation & Conclusions/
      Deficiency Evaluation Workpaper
      Management ICFR Assessment
```

## Deficiency Severity Framework

### Simple Deficiency

A gap exists when a control's design or execution does not enable personnel to prevent or detect misstatements in the ordinary course of their responsibilities.

**Evaluation dimensions:**
- How likely is it that the gap could produce a misstatement?
- How large could the resulting misstatement be?
- Does a compensating control reduce the residual exposure?

### Significant Deficiency

A deficiency (or cluster of deficiencies) that falls short of material-weakness severity but is consequential enough to require governance-body attention.

**Hallmarks:**
- Could produce a misstatement that is more than trivial but less than material
- Probability of material misstatement is above remote but below reasonably possible
- Involves a key control where compensating measures do not fully offset the gap
- Several individually minor gaps that, taken together, raise substantive concern

### Material Weakness

A deficiency (or cluster of deficiencies) creating a reasonable possibility that a material financial-statement misstatement will escape prevention or detection.

**Strong indicators:**
- Senior management fraud of any dollar magnitude
- Restatement of previously filed financials to correct a material error
- Auditor detection of a material misstatement that the entity's own controls missed
- Breakdown in audit-committee oversight of the financial reporting process
- Failure of a pervasive control (organization-level or IT general) with downstream impact across multiple cycles

### Aggregation Analysis

Individually minor gaps may be severe in combination:

1. Collect all deficiencies affecting the same process or assertion
2. Evaluate whether their combined effect could permit a material misstatement
3. Consider whether a weakness in a compensating control amplifies other gaps
4. Document the aggregation logic and the resulting severity classification

### Remediation Protocol

For every identified gap:

1. **Root-cause diagnosis:** Determine why the control failed (design flaw, execution lapse, resource constraint, training gap, system limitation)
2. **Corrective action plan:** Define specific steps to restore effectiveness (redesign, additional staffing, enhanced training, system configuration change, added review layer)
3. **Target completion date:** Set a realistic but firm deadline
4. **Accountable owner:** Assign a named individual responsible for execution
5. **Validation procedure:** Specify how and when the remediated control will be re-tested to confirm it is operating effectively

## Control Taxonomy

### IT General Controls (ITGCs)

Infrastructure-level controls ensuring that application controls and automated processes function reliably.

**Logical access governance:**
- New-user provisioning requires documented, pre-implementation approval
- Terminated-user accounts are disabled within a defined SLA
- Privileged/administrator access is restricted and subject to enhanced monitoring
- Periodic recertification reviews validate that access remains appropriate
- Password standards enforce complexity, rotation, and lockout thresholds
- Conflicting duties are systematically prevented through role-based access design

**Change governance:**
- Every change request is documented and approved prior to deployment
- Changes are validated in a non-production environment before promotion
- Development and production environments are logically or physically separated
- Emergency changes follow a defined expedited path with post-implementation sign-off
- Post-deployment reviews confirm changes behave as intended

**Operational continuity:**
- Automated job scheduling is monitored with exception alerting
- Backups execute on schedule and restore procedures are periodically tested
- System uptime and performance are tracked against defined SLAs
- Incident response and escalation procedures are documented and rehearsed
- Disaster recovery plans are maintained and tested at defined intervals

### Manual (Human-Performed) Controls

Controls relying on individual judgment, typically involving review, approval, or verification activities.

**Representative controls:**
- Leadership review of financial results and operating metrics
- Supervisory sign-off on journal entries exceeding a dollar threshold
- Three-way matching of purchase order, goods receipt, and vendor invoice
- Preparation and independent review of account reconciliations
- Physical observation and counting of inventory
- Authorization of vendor or customer master-data changes
- Credit-limit approval for new or expanded customer relationships

**Attributes to verify during testing:**
- The control was performed by someone with proper authority
- Execution occurred within the prescribed time window
- Observable evidence of the review exists (signature, initials, system notation, email)
- The reviewer had access to sufficient supporting information
- Identified exceptions were investigated and appropriately resolved

### Automated (System-Enforced) Controls

Controls embedded in application logic that execute without human intervention.

**Representative controls:**
- Workflow engines that block progression without required approvals
- Automated three-way match that withholds payment when PO, receipt, and invoice disagree
- Duplicate-detection algorithms that flag or reject repeated invoice submissions
- Credit-limit enforcement that prevents order entry beyond the approved threshold
- System-calculated depreciation, amortization, interest, and tax computations
- Role-based access configurations that prevent users from holding conflicting privileges
- Field-level validations (mandatory fields, format masks, range constraints)
- Automated transaction-matching within reconciliation modules

**Testing approach:**
- Confirm the system configuration enforces the control as specified (design test)
- For unchanged configurations, a single successful test typically covers the period (operating effectiveness), provided change-management ITGCs are also effective
- If the configuration was modified during the period, re-test post-change

### IT-Dependent Manual Controls

Manual review or approval activities that depend on the completeness and accuracy of system-produced data.

**Representative controls:**
- Management review of a system-generated exception or outlier report
- Reserve estimation based on a system-generated aging analysis
- Account reconciliation performed using system-extracted trial balance data
- Transaction approvals triggered by system-generated workflow notifications

**Testing approach:**
- Test the human element (review quality, follow-up on exceptions, evidence of approval)
- Separately validate the information produced by the entity (IPE) — confirm the underlying report or data extract is complete and accurate
- IPE testing ensures the reviewer's conclusions rest on reliable inputs

### Organization-Level Controls

Broad governance mechanisms that set the tone and operating environment for the entire control framework.

**Representative controls:**
- Executive tone and ethical standards (code of conduct, leadership messaging)
- Enterprise risk assessment process
- Audit committee oversight of external and internal reporting
- Internal audit charter, scope, and activities
- Fraud risk assessment and anti-fraud programs
- Ethics hotline / whistleblower mechanism
- Management's ongoing monitoring of control health
- Financial reporting competency standards (hiring qualifications, continuing education)
- Period-end reporting procedures (close governance, GAAP compliance checkpoints)

**Significance in evaluation:**
- Organization-level controls can supplement but generally cannot substitute for process-level controls
- Failures in tone-at-the-top or audit-committee oversight are potent indicators of material weakness
- Robust organization-level controls may justify reduced sample sizes or narrower scope at the process level
