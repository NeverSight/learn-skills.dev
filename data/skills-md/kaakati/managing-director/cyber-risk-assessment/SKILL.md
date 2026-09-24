---
name: cyber-risk-assessment
description: >
  Cybersecurity risk assessment engine using NIST CSF 2.0, ISO 27001, and
  CIS Controls v8. Produces maturity assessments, threat landscape analyses,
  control gap remediation plans, and cyber risk quantification using FAIR
  methodology. USE THIS SKILL when the user mentions cybersecurity posture,
  cyber risk, threat assessment, NIST CSF, ISO 27001, CIS Controls,
  vulnerability assessment, crown jewel analysis, FAIR methodology, cyber
  risk quantification, third-party cyber risk, incident response readiness,
  security architecture review, or cybersecurity investment prioritization.
---

# Cyber Risk Assessment

## Required Inputs

- **Organization**: Company name, industry, size (employees, revenue), and technology footprint.
- **Scope**: Enterprise-wide or specific business unit / system / application.
- **Framework Preference**: NIST CSF 2.0, ISO 27001, CIS Controls v8, or hybrid.
- **Current Security Posture**: Existing security program documentation, prior assessments, audit results.
- **Regulatory Requirements**: Applicable cybersecurity regulations (SOC 2, GDPR, HIPAA, PCI-DSS, CMMC, etc.).
- **Known Incidents**: Past security incidents, breaches, or near-misses.
- **Technology Stack**: Key platforms, cloud providers, network architecture overview.
- **Budget Context**: Current cybersecurity spend and investment capacity.

## Execution Steps

### 1. Framework Selection Guidance

Select the appropriate framework based on organizational context.

**Framework Comparison Matrix**

| Criterion | NIST CSF 2.0 | ISO 27001:2022 | CIS Controls v8 |
|---|---|---|---|
| **Best For** | Comprehensive risk-based program design | Formal ISMS certification | Tactical, prioritized implementation |
| **Approach** | Outcomes-based, flexible | Requirements-based, prescriptive | Safeguard-based, prioritized |
| **Structure** | 6 Functions, 22 Categories, 106 Subcategories | 93 controls in 4 themes | 18 Controls, 153 Safeguards in 3 IGs |
| **Certification** | No formal certification | Yes (accredited certification) | No formal certification |
| **Regulatory Mapping** | Maps to most US/intl regulations | Recognized globally for compliance | Maps to NIST CSF and ISO 27001 |
| **Maturity Model** | 4 tiers (Partial to Adaptive) | Binary (conforms / does not conform) | 3 Implementation Groups (IG1-IG3) |
| **Effort to Implement** | Medium-High | High (requires formal ISMS) | Low-Medium (start with IG1) |
| **Ideal Org Size** | Mid-large, any industry | Any size seeking certification | Small-mid, or starting a security program |

**Recommended Selection Logic**

```
IF regulatory requirement mandates specific framework --> Use that framework
ELIF organization needs certification --> ISO 27001
ELIF organization is starting from scratch --> CIS Controls v8 (begin with IG1)
ELIF organization needs comprehensive program assessment --> NIST CSF 2.0
ELIF defense contractor or US government supply chain --> NIST CSF 2.0 + CMMC
ELSE --> NIST CSF 2.0 as primary, map to ISO 27001/CIS as needed
```

### 2. NIST CSF 2.0 Maturity Assessment

Assess current maturity across all 6 functions, 22 categories.

**Maturity Tier Definitions**

| Tier | Name | Definition |
|---|---|---|
| 1 | Partial | Ad hoc, reactive. Risk management not formalized. Limited awareness. |
| 2 | Risk Informed | Risk management practices approved but may not be organization-wide. Some processes defined. |
| 3 | Repeatable | Formal policies and procedures, consistently implemented. Regular updates. Risk-informed decisions. |
| 4 | Adaptive | Organization adapts practices based on lessons learned and predictive indicators. Continuous improvement. |

**NIST CSF 2.0 Assessment Matrix**

| Function | Category | Category ID | Current Tier | Target Tier | Gap | Priority |
|---|---|---|---|---|---|---|
| **GOVERN** | Organizational Context | GV.OC | [1-4] | [1-4] | [0-3] | [C/H/M/L] |
| **GOVERN** | Risk Management Strategy | GV.RM | [1-4] | [1-4] | [0-3] | |
| **GOVERN** | Roles, Responsibilities, Authorities | GV.RR | [1-4] | [1-4] | [0-3] | |
| **GOVERN** | Policy | GV.PO | [1-4] | [1-4] | [0-3] | |
| **GOVERN** | Oversight | GV.OV | [1-4] | [1-4] | [0-3] | |
| **GOVERN** | Cybersecurity Supply Chain Risk Mgmt | GV.SC | [1-4] | [1-4] | [0-3] | |
| **IDENTIFY** | Asset Management | ID.AM | [1-4] | [1-4] | [0-3] | |
| **IDENTIFY** | Risk Assessment | ID.RA | [1-4] | [1-4] | [0-3] | |
| **IDENTIFY** | Improvement | ID.IM | [1-4] | [1-4] | [0-3] | |
| **PROTECT** | Identity Management, Auth, Access Control | PR.AA | [1-4] | [1-4] | [0-3] | |
| **PROTECT** | Awareness and Training | PR.AT | [1-4] | [1-4] | [0-3] | |
| **PROTECT** | Data Security | PR.DS | [1-4] | [1-4] | [0-3] | |
| **PROTECT** | Platform Security | PR.PS | [1-4] | [1-4] | [0-3] | |
| **PROTECT** | Technology Infrastructure Resilience | PR.IR | [1-4] | [1-4] | [0-3] | |
| **DETECT** | Continuous Monitoring | DE.CM | [1-4] | [1-4] | [0-3] | |
| **DETECT** | Adverse Event Analysis | DE.AE | [1-4] | [1-4] | [0-3] | |
| **RESPOND** | Incident Management | RS.MA | [1-4] | [1-4] | [0-3] | |
| **RESPOND** | Incident Analysis | RS.AN | [1-4] | [1-4] | [0-3] | |
| **RESPOND** | Incident Response Reporting and Communication | RS.CO | [1-4] | [1-4] | [0-3] | |
| **RESPOND** | Incident Mitigation | RS.MI | [1-4] | [1-4] | [0-3] | |
| **RECOVER** | Incident Recovery Plan Execution | RC.RP | [1-4] | [1-4] | [0-3] | |
| **RECOVER** | Incident Recovery Communication | RC.CO | [1-4] | [1-4] | [0-3] | |

**Overall Maturity Score**

```
Function Score = Average of Category Tiers within Function
Overall Score = Weighted Average of Function Scores

Recommended Weights:
  Govern: 15%   Identify: 15%   Protect: 25%
  Detect: 20%   Respond: 15%   Recover: 10%
```

### 3. Threat Landscape Analysis

**Threat Actor Profiling**

| Actor Type | Motivation | Capability | Targeting | Relevance to Organization |
|---|---|---|---|---|
| **Nation-State (APT)** | Espionage, disruption, IP theft | Very High | Specific sectors: defense, energy, finance, healthcare, tech | [High/Medium/Low] |
| **Organized Crime** | Financial gain | High | Opportunistic + targeted (high-value data, ransomware) | [High/Medium/Low] |
| **Hacktivists** | Ideological, reputational damage | Medium | Visible brands, controversial industries | [High/Medium/Low] |
| **Insider Threat** | Financial, grievance, negligence | Varies | Direct access to sensitive data and systems | [High/Medium/Low] |
| **Competitors** | Competitive advantage, IP theft | Medium | Trade secrets, customer data, pricing | [High/Medium/Low] |
| **Script Kiddies** | Notoriety, curiosity | Low | Opportunistic (unpatched, exposed systems) | [High/Medium/Low] |

**Attack Vector Mapping**

| Attack Vector | Likelihood | Common Techniques | Primary Targets | Current Defense Maturity |
|---|---|---|---|---|
| Phishing / Social Engineering | Very High | Spear phishing, BEC, vishing, smishing | Email users, executives, finance | [1-4] |
| Ransomware | High | Encryption, double extortion, RaaS | Endpoints, file servers, backups | [1-4] |
| Supply Chain Compromise | High | Software supply chain, vendor access abuse | Third-party integrations, SaaS | [1-4] |
| Credential Theft / Abuse | High | Credential stuffing, password spray, MFA bypass | Identity systems, VPN, cloud | [1-4] |
| Vulnerability Exploitation | High | Zero-day, N-day, unpatched systems | Public-facing applications, infrastructure | [1-4] |
| Insider Threat | Medium | Data exfiltration, privilege abuse, sabotage | Sensitive data stores, admin systems | [1-4] |
| Cloud Misconfiguration | Medium | Exposed storage, overprivileged IAM, public APIs | Cloud workloads, storage, databases | [1-4] |
| DDoS | Medium | Volumetric, application-layer | Public-facing services, DNS | [1-4] |
| Physical Access | Low | Tailgating, USB drops, device theft | Offices, data centers, laptops | [1-4] |

### 4. Vulnerability Assessment Methodology

**Assessment Layers**

| Layer | Method | Frequency | Tools/Approach |
|---|---|---|---|
| Network infrastructure | Automated vulnerability scanning | Monthly (external), Quarterly (internal) | Nessus, Qualys, Rapid7 |
| Web applications | DAST + SAST + manual testing | Per release + quarterly | Burp Suite, OWASP ZAP, Checkmarx |
| Cloud configuration | Cloud security posture management (CSPM) | Continuous | Prisma Cloud, Wiz, AWS Config |
| Endpoint | EDR telemetry + vulnerability scanning | Continuous + monthly | CrowdStrike, SentinelOne, Microsoft Defender |
| Identity and access | Access review + privilege audit | Quarterly | SailPoint, Azure AD access reviews |
| Third-party / SaaS | Vendor security assessment + SaaS posture | At onboarding + annually | SecurityScorecard, BitSight, questionnaires |

**Vulnerability Severity Classification (CVSS-Aligned)**

| Severity | CVSS Score | Remediation SLA | Escalation if SLA Missed |
|---|---|---|---|
| Critical | 9.0 - 10.0 | 24-72 hours | CISO immediately |
| High | 7.0 - 8.9 | 7-14 days | CISO weekly |
| Medium | 4.0 - 6.9 | 30-60 days | Security team lead |
| Low | 0.1 - 3.9 | 90 days or next patch cycle | Standard reporting |
| Informational | 0.0 | Track only | N/A |

### 5. Crown Jewel Analysis

Identify and classify the organization's most critical digital assets.

**Asset Classification Matrix**

| Asset Category | Examples | Confidentiality Impact | Integrity Impact | Availability Impact | Overall Criticality |
|---|---|---|---|---|---|
| Customer PII/PHI | Customer database, health records | Catastrophic | Major | Major | **Critical** |
| Financial data | Banking credentials, financial statements pre-release | Catastrophic | Catastrophic | Major | **Critical** |
| Intellectual property | Source code, formulas, designs, trade secrets | Catastrophic | Major | Moderate | **Critical** |
| Authentication systems | Active Directory, SSO, PKI, MFA infrastructure | Major | Catastrophic | Catastrophic | **Critical** |
| Core business applications | ERP, CRM, manufacturing systems | Moderate | Major | Catastrophic | **High** |
| Employee PII | HRIS, payroll, benefits data | Major | Moderate | Moderate | **High** |
| Communication systems | Email, messaging, collaboration platforms | Moderate | Moderate | Major | **High** |
| Public-facing systems | Website, customer portal, mobile apps | Moderate | Major | Major | **High** |
| Internal documentation | Policies, procedures, internal wikis | Low | Moderate | Low | **Medium** |
| Development/test systems | Non-production environments | Low | Low | Low | **Low** |

**Crown Jewel Prioritization**

```
Crown Jewel Score = (Confidentiality Impact x 0.4) + (Integrity Impact x 0.3) + (Availability Impact x 0.3)

Scoring: Catastrophic = 5, Major = 4, Moderate = 3, Minor = 2, Negligible = 1
Crown Jewels = Assets scoring >= 4.0
```

### 6. Control Gap Analysis and Remediation Prioritization

**Gap Analysis Matrix**

| Control Area | Required Control | Current State | Gap Description | Risk If Unaddressed | Remediation Effort | Priority Score |
|---|---|---|---|---|---|---|
| [Area] | [Control description] | [Implemented/Partial/Missing] | [Specific gap] | [Critical/High/Med/Low] | [Low/Med/High] | [Calculated] |

**Remediation Priority Score Calculation**

```
Priority Score = Risk Impact (1-5) x Likelihood of Exploitation (1-5) / Implementation Effort (1-5)

Score > 5.0  --> Immediate (Sprint 1)
Score 3.0-5.0 --> Near-term (30-90 days)
Score 1.0-3.0 --> Medium-term (90-180 days)
Score < 1.0  --> Long-term (180-365 days)
```

**Quick Wins Identification (High Impact, Low Effort)**

| Quick Win | Effort | Risk Reduction | Typical Cost |
|---|---|---|---|
| Enable MFA on all external-facing accounts | Low | Very High | $2-5/user/month |
| Disable legacy authentication protocols | Low | High | $0 (configuration) |
| Implement email authentication (SPF, DKIM, DMARC) | Low | High | $0-500/year |
| Deploy endpoint detection and response (EDR) | Medium | Very High | $5-15/endpoint/month |
| Implement privileged access management (PAM) | Medium | Very High | $20K-100K+ |
| Enable cloud security posture management (CSPM) | Medium | High | $10K-50K/year |
| Conduct phishing simulation and training | Low | Medium | $3-8/user/year |
| Review and restrict admin accounts | Low | High | $0 (process) |

### 7. Cyber Risk Quantification (FAIR Methodology)

**Factor Analysis of Information Risk (FAIR) Framework**

```
Risk ($) = Loss Event Frequency (LEF) x Loss Magnitude (LM)

Where:
  LEF = Threat Event Frequency (TEF) x Vulnerability (Vuln)
  TEF = Contact Frequency (CF) x Probability of Action (PoA)
  LM  = Primary Loss + Secondary Loss

Primary Loss = Productivity Loss + Response Cost + Replacement Cost + Fines/Judgments
Secondary Loss = Reputation Damage x Secondary Loss Event Frequency (SLEF)
```

**FAIR Risk Scenario Template**

| FAIR Factor | Low Estimate | Most Likely | High Estimate | Basis for Estimate |
|---|---|---|---|---|
| **Threat Event Frequency** (per year) | [#] | [#] | [#] | [Industry data, threat intelligence, historical incidents] |
| **Vulnerability** (probability of success given attempt) | [0-1] | [0-1] | [0-1] | [Control effectiveness, pentest results, maturity assessment] |
| **Loss Event Frequency** (per year) | [Calc] | [Calc] | [Calc] | TEF x Vulnerability |
| **Primary Loss** ($) | [$] | [$] | [$] | [Direct cost estimation] |
| - Productivity Loss | [$] | [$] | [$] | [Hourly revenue x downtime hours] |
| - Response Cost | [$] | [$] | [$] | [IR firm, forensics, legal, overtime] |
| - Replacement Cost | [$] | [$] | [$] | [System rebuild, data restoration] |
| - Fines and Judgments | [$] | [$] | [$] | [Regulatory penalty ranges, litigation estimates] |
| **Secondary Loss** ($) | [$] | [$] | [$] | [Reputation, customer churn] |
| - Customer Notification Cost | [$] | [$] | [$] | [$5-50/record industry average] |
| - Credit Monitoring | [$] | [$] | [$] | [$10-30/person x affected population] |
| - Customer Churn | [$] | [$] | [$] | [Churn rate increase x customer LTV] |
| - Brand/Reputation | [$] | [$] | [$] | [Revenue impact estimate] |
| **Annualized Loss Expectancy** | [$] | [$] | [$] | LEF x Total Loss Magnitude |

**Loss Exceedance Curve Output**

| Probability of Exceeding | Annual Loss Amount |
|---|---|
| 90% (likely exceeds) | $[amount] |
| 50% (median scenario) | $[amount] |
| 10% (worst case plausible) | $[amount] |
| 5% (tail risk) | $[amount] |

### 8. Third-Party / Supply Chain Cyber Risk Assessment

**Vendor Risk Tiering**

| Tier | Criteria | Assessment Rigor | Frequency |
|---|---|---|---|
| **Critical** | Access to crown jewels, critical business function, > $1M spend, or single-source dependency | Full security assessment + onsite/virtual audit + continuous monitoring | Annual assessment + continuous |
| **High** | Access to sensitive data, important business function, $100K-$1M spend | Detailed questionnaire (SIG/CAIQ) + evidence review + external scoring | Annual |
| **Medium** | Limited data access, replaceable function, $10K-$100K spend | Standard questionnaire + external risk rating review | Biennial |
| **Low** | No data access, commodity service, < $10K spend | External risk rating only | At onboarding |

**Third-Party Assessment Checklist (Critical/High Tier)**

| Domain | Key Questions | Evidence Required |
|---|---|---|
| Governance | Security program, CISO role, board reporting | Security policy, org chart |
| Access Control | SSO, MFA, privileged access, access reviews | Access control policy, PAM evidence |
| Data Protection | Encryption (transit + rest), DLP, classification | Encryption standards, DLP policy |
| Incident Response | IR plan, breach notification SLA, past incidents | IR plan, notification procedures |
| Business Continuity | DR plan, RTO/RPO, testing frequency | DR test results |
| Compliance | SOC 2 Type II, ISO 27001, relevant certifications | Current audit reports, certificates |
| Vulnerability Management | Scanning frequency, patching SLAs, pentest schedule | Scan reports (redacted), pentest summary |
| Subcontractor Management | Fourth-party risk assessment process | Subcontractor policy, list of critical subs |

### 9. Incident Response Readiness Evaluation

**IR Readiness Scorecard**

| Capability | Maturity Level (1-4) | Evidence | Gap |
|---|---|---|---|
| IR plan documented and approved | [1-4] | [Plan document, approval date] | [Gap if any] |
| IR team identified with roles and contact info | [1-4] | [Team roster, contact card] | |
| IR playbooks for top threat scenarios | [1-4] | [Playbook documents] | |
| Detection capability (SIEM, EDR, NDR) | [1-4] | [Tool inventory, coverage map] | |
| Forensic capability (in-house or retained) | [1-4] | [Retainer agreement, tool inventory] | |
| Legal/breach counsel pre-retained | [1-4] | [Retainer agreement] | |
| Cyber insurance in force | [1-4] | [Policy summary] | |
| Tabletop exercise conducted (last 12 months) | [1-4] | [Exercise report] | |
| Technical IR drill conducted (last 12 months) | [1-4] | [Drill report] | |
| Communication templates pre-approved | [1-4] | [Template documents] | |
| Regulatory notification procedures documented | [1-4] | [Procedure document per jurisdiction] | |
| Backup and recovery tested | [1-4] | [Recovery test results] | |

**IR Readiness Score**: Sum of all scores / 48 (max) = [X]%

| Score Range | Readiness Level | Recommendation |
|---|---|---|
| 85-100% | Advanced | Maintain and continuously improve |
| 70-84% | Established | Address specific gaps identified |
| 50-69% | Developing | Significant investment needed; prioritize detection and playbooks |
| < 50% | Initial | IR program build required; engage external support |

### 10. Security Architecture Review Checklist

**Network Architecture**

| Control | Expected State | Current State | Finding |
|---|---|---|---|
| Network segmentation (microsegmentation for crown jewels) | Implemented | [Status] | [Finding] |
| Zero trust network access (ZTNA) for remote access | Implemented or planned | [Status] | |
| Web application firewall (WAF) on all public apps | Implemented | [Status] | |
| DDoS protection on public-facing services | Implemented | [Status] | |
| DNS security (DNSSEC, DNS filtering) | Implemented | [Status] | |
| East-west traffic monitoring | Implemented | [Status] | |

**Identity and Access**

| Control | Expected State | Current State | Finding |
|---|---|---|---|
| MFA on all accounts (phishing-resistant preferred) | Enforced | [Status] | [Finding] |
| SSO for all SaaS and enterprise applications | Implemented | [Status] | |
| Privileged access management (PAM) with session recording | Implemented | [Status] | |
| Just-in-time (JIT) access for admin privileges | Implemented | [Status] | |
| Automated access provisioning/deprovisioning | Implemented | [Status] | |
| Service account management and rotation | Implemented | [Status] | |

**Data Protection**

| Control | Expected State | Current State | Finding |
|---|---|---|---|
| Encryption at rest (AES-256 or equivalent) | All sensitive data | [Status] | [Finding] |
| Encryption in transit (TLS 1.2+ minimum) | All connections | [Status] | |
| Data loss prevention (DLP) | Implemented at key egress points | [Status] | |
| Data classification and labeling | Implemented | [Status] | |
| Backup encryption and immutability | Implemented | [Status] | |
| Key management (HSM or cloud KMS) | Implemented | [Status] | |

**Endpoint and Cloud**

| Control | Expected State | Current State | Finding |
|---|---|---|---|
| EDR on all endpoints (servers + workstations) | 100% coverage | [Status] | [Finding] |
| Mobile device management (MDM) | All corporate/BYOD devices | [Status] | |
| CSPM for all cloud environments | Implemented | [Status] | |
| Container security (image scanning, runtime protection) | If using containers | [Status] | |
| Infrastructure as code (IaC) security scanning | If using IaC | [Status] | |
| Cloud workload protection platform (CWPP) | If using cloud compute | [Status] | |

### 11. Cybersecurity Investment Prioritization

**Risk Reduction per Dollar (RRPD) Framework**

```
RRPD = Annualized Risk Reduction ($) / Total Cost of Ownership (3-year)

Where:
  Annualized Risk Reduction = ALE(before control) - ALE(after control)
  Total Cost = Implementation + Annual Operation x 3 + Training

Higher RRPD = Better investment
```

**Investment Prioritization Matrix**

| Investment | ALE Before | ALE After | Risk Reduction | 3-Year TCO | RRPD Ratio | Rank |
|---|---|---|---|---|---|---|
| [Security control/tool] | [$] | [$] | [$] | [$] | [X.X] | [#] |

**Investment Decision Categories**

| RRPD Ratio | Decision | Justification |
|---|---|---|
| > 3.0 | Strong invest | Risk reduction far exceeds cost |
| 1.5 - 3.0 | Invest | Positive ROI on risk reduction |
| 1.0 - 1.5 | Consider | Marginal return; evaluate alternatives |
| 0.5 - 1.0 | Defer unless regulatory | Cost exceeds quantified risk reduction |
| < 0.5 | Do not invest | Poor risk-adjusted return; seek alternatives |

### 12. Regulatory Mapping

**Cybersecurity Regulation Cross-Reference**

| Control Domain | NIST CSF 2.0 | SOC 2 (TSC) | GDPR | HIPAA | PCI-DSS 4.0 | ISO 27001 |
|---|---|---|---|---|---|---|
| Access Control | PR.AA | CC6.1-6.3 | Art. 32 | 164.312(a)(1) | Req 7-8 | A.9 |
| Data Encryption | PR.DS | CC6.1, CC6.7 | Art. 32 | 164.312(a)(2)(iv) | Req 3-4 | A.10 |
| Logging/Monitoring | DE.CM, DE.AE | CC7.1-7.2 | Art. 32 | 164.312(b) | Req 10 | A.12.4 |
| Incident Response | RS.MA, RS.AN | CC7.3-7.5 | Art. 33-34 | 164.308(a)(6) | Req 12.10 | A.16 |
| Vulnerability Mgmt | ID.RA, PR.PS | CC7.1 | Art. 32 | 164.308(a)(1) | Req 6, 11 | A.12.6 |
| Vendor Management | GV.SC | CC9.2 | Art. 28 | 164.308(b)(1) | Req 12.8 | A.15 |
| Security Training | PR.AT | CC1.4 | Art. 39 | 164.308(a)(5) | Req 12.6 | A.7.2.2 |
| Risk Assessment | ID.RA, GV.RM | CC3.1-3.2 | Art. 35 | 164.308(a)(1)(ii)(A) | Req 12.2 | A.8.2 |
| Business Continuity | PR.IR, RC.RP | A1.1-A1.3 | Art. 32 | 164.308(a)(7) | Req 12.10 | A.17 |
| Data Retention/Disposal | PR.DS | CC6.5 | Art. 5(1)(e), 17 | 164.310(d)(2) | Req 3.1, 9.4 | A.8.3 |

**Compliance Gap Heat Map**

| Regulation | Current Compliance | Gap Count (Critical) | Gap Count (High) | Gap Count (Medium) | Overall Status |
|---|---|---|---|---|---|
| [Regulation] | [%] | [#] | [#] | [#] | [Red/Yellow/Green] |

## Output Template

```markdown
## Cybersecurity Risk Assessment: [Organization]

### Assessment Parameters
| Field | Detail |
|---|---|
| Framework(s) | [NIST CSF 2.0 / ISO 27001 / CIS Controls v8] |
| Scope | [Enterprise / specific systems] |
| Assessment Date | [Date] |
| Assessor | [Name/team] |
| Classification | [Confidential] |

### Executive Summary
[Overall cybersecurity posture, maturity score, top 3-5 critical findings,
headline risk quantification, investment recommendation]

### Maturity Assessment Summary
| NIST CSF Function | Current Tier | Target Tier | Gap |
|---|---|---|---|
| Govern | [1-4] | [Target] | [Gap] |
| Identify | [1-4] | [Target] | [Gap] |
| Protect | [1-4] | [Target] | [Gap] |
| Detect | [1-4] | [Target] | [Gap] |
| Respond | [1-4] | [Target] | [Gap] |
| Recover | [1-4] | [Target] | [Gap] |
| **Overall** | [Weighted] | [Target] | [Gap] |

### Threat Landscape
[Threat actor relevance assessment, top attack vectors, industry-specific threats]

### Crown Jewel Analysis
[Critical asset inventory with classification and current protection assessment]

### Control Gap Analysis
[Prioritized gaps with remediation recommendations]

### Cyber Risk Quantification (FAIR)
| Risk Scenario | Annualized Loss Expectancy | 90th Percentile Loss |
|---|---|---|
| [Scenario 1] | [$X] | [$X] |
| [Scenario 2] | [$X] | [$X] |
| **Total Cyber Risk Exposure** | **[$X]** | **[$X]** |

### Third-Party Risk Summary
[Vendor tier distribution, critical vendor assessment status, key findings]

### Investment Roadmap
| Phase | Investment | Cost | Risk Reduction | RRPD |
|---|---|---|---|---|
| Immediate (0-30 days) | [Quick wins] | [$X] | [$X] | [X.X] |
| Near-term (30-90 days) | [High-priority controls] | [$X] | [$X] | [X.X] |
| Medium-term (90-180 days) | [Program maturity] | [$X] | [$X] | [X.X] |
| Long-term (180-365 days) | [Advanced capabilities] | [$X] | [$X] | [X.X] |

### Regulatory Compliance Status
[Compliance gap summary per applicable regulation]

### Appendices
- A: Detailed NIST CSF 2.0 assessment (all 106 subcategories)
- B: Vulnerability scan summary (redacted)
- C: Third-party vendor risk register
- D: FAIR model assumptions and data sources
- E: Regulatory mapping detail
```

## Quality Checks

- [ ] Framework selection is justified based on organizational context, not assumed.
- [ ] NIST CSF 2.0 assessment covers all 6 functions including Govern (added in CSF 2.0).
- [ ] Threat landscape analysis is specific to the organization's industry and profile, not generic.
- [ ] Crown jewel analysis identifies specific critical assets with CIA impact ratings.
- [ ] Control gap analysis includes both the gap description and a prioritized remediation recommendation.
- [ ] FAIR risk quantification uses ranges (low/most likely/high), not single-point estimates.
- [ ] Third-party risk assessment tiers vendors by data access and business criticality.
- [ ] Incident response readiness evaluation produces a scored assessment, not just a checklist.
- [ ] Security architecture review covers network, identity, data, endpoint, and cloud layers.
- [ ] Investment prioritization uses Risk Reduction per Dollar (RRPD) to rank spending decisions.
- [ ] Regulatory mapping cross-references specific control requirements across all applicable regulations.
- [ ] Vulnerability remediation SLAs are defined by CVSS severity with escalation procedures.
