---
name: ai-policy-generator
description: AI governance policy creation for nonprofits and enterprises with frameworks, risk assessment, ethical guidelines, and compliance templates. Use when drafting AI usage policies, responsible AI frameworks, or organizational AI governance documents.
---

# AI Policy Generator

Comprehensive frameworks for creating organizational AI governance policies covering acceptable use, risk management, ethical guidelines, data handling, and compliance requirements.

## AI Policy Structure

### Standard AI Policy Template

```
AI GOVERNANCE POLICY — [ORGANIZATION NAME]

1. PURPOSE AND SCOPE
   - Why this policy exists
   - Who it applies to (employees, contractors, vendors)
   - What AI systems are covered
   - Effective date and review cadence

2. DEFINITIONS
   - AI / Machine Learning
   - Generative AI
   - Automated decision-making
   - Personal data / Sensitive data
   - High-risk AI use cases

3. ACCEPTABLE USE
   - Approved AI tools and platforms
   - Permitted use cases by department
   - Prohibited uses (explicit list)
   - Approval process for new AI tools

4. DATA AND PRIVACY
   - Data classification for AI inputs
   - Prohibited data types (PII, PHI, confidential)
   - Data retention and deletion
   - Third-party data sharing restrictions

5. RISK ASSESSMENT
   - Risk classification framework (low/medium/high/critical)
   - Required assessments by risk level
   - Approval chain for high-risk deployments
   - Ongoing monitoring requirements

6. TRANSPARENCY AND DISCLOSURE
   - When to disclose AI use to stakeholders
   - Labeling AI-generated content
   - Customer/client notification requirements
   - Internal documentation standards

7. HUMAN OVERSIGHT
   - Human-in-the-loop requirements
   - Decision review thresholds
   - Escalation procedures
   - Override authority

8. BIAS AND FAIRNESS
   - Bias testing requirements
   - Fairness metrics and thresholds
   - Protected class considerations
   - Remediation procedures

9. SECURITY
   - AI-specific security controls
   - Prompt injection prevention
   - Model access controls
   - Incident response for AI failures

10. COMPLIANCE
    - Applicable regulations (EU AI Act, state laws, industry)
    - Audit requirements
    - Record-keeping obligations
    - Reporting requirements

11. TRAINING AND AWARENESS
    - Required training by role
    - Training frequency
    - Competency assessment

12. ENFORCEMENT
    - Violation reporting
    - Consequences framework
    - Appeal process

13. GOVERNANCE
    - AI governance committee composition
    - Review and update cadence
    - Policy exception process
    - Version control
```

## Risk Classification Framework

### AI Use Case Risk Levels

| Risk Level | Description | Examples | Requirements |
|-----------|-------------|----------|-------------|
| **Low** | Minimal impact on individuals or operations | Summarizing meeting notes, drafting internal emails, code formatting | Self-service, basic training |
| **Medium** | Moderate impact, reversible decisions | Customer service drafts, content generation, data analysis | Manager approval, human review |
| **High** | Significant impact on individuals or finances | Hiring screening, credit decisions, medical triage | Committee approval, bias audit, monitoring |
| **Critical** | Potential for serious harm, legal liability | Autonomous decisions affecting rights, safety-critical systems | Board approval, external audit, ongoing review |

### Risk Assessment Checklist

```
AI USE CASE RISK ASSESSMENT

Use Case: _____________________
Department: ___________________
Requested By: _________________
Date: ________________________

IMPACT ASSESSMENT:
  [ ] Affects individual rights or opportunities?
  [ ] Involves personal or sensitive data?
  [ ] Makes or influences financial decisions?
  [ ] Affects health, safety, or welfare?
  [ ] Has legal or regulatory implications?
  [ ] Could cause reputational harm?
  [ ] Involves vulnerable populations?

DATA ASSESSMENT:
  [ ] What data types are used as inputs?
  [ ] Is PII/PHI/confidential data involved?
  [ ] Where is data stored and processed?
  [ ] What third parties receive data?
  [ ] Is data retention compliant with policy?

TRANSPARENCY ASSESSMENT:
  [ ] Are affected parties informed of AI use?
  [ ] Is the AI's role in decisions clear?
  [ ] Can decisions be explained?
  [ ] Is there an appeal/override mechanism?

RISK LEVEL: [ ] Low  [ ] Medium  [ ] High  [ ] Critical

REQUIRED APPROVALS:
  [ ] Manager (all levels)
  [ ] AI Governance Committee (medium+)
  [ ] Legal review (high+)
  [ ] Board approval (critical)
  [ ] External audit (critical)
```

## Acceptable Use Guidelines

### Approved vs Prohibited Uses

```
APPROVED USES (with appropriate safeguards):

CONTENT AND COMMUNICATION:
  + Drafting internal communications
  + Summarizing documents and meetings
  + Translating content between languages
  + Brainstorming and ideation
  + Editing and proofreading

RESEARCH AND ANALYSIS:
  + Market research synthesis
  + Data analysis and visualization
  + Literature review assistance
  + Trend identification
  + Competitive analysis

PRODUCTIVITY:
  + Code generation and review
  + Template creation
  + Process documentation
  + FAQ and knowledge base content
  + Scheduling optimization

PROHIBITED USES:

  - Inputting confidential business data into public AI tools
  - Uploading PII, PHI, or financial records to unapproved platforms
  - Using AI for final hiring, firing, or disciplinary decisions
  - Generating content that impersonates real individuals
  - Making autonomous decisions that affect individual rights
  - Bypassing security controls or access restrictions
  - Generating misleading, deceptive, or fraudulent content
  - Using AI to surveil employees without disclosure
  - Submitting AI-generated work as original without disclosure
  - Using AI for any illegal purpose
```

## Regulatory Landscape

### Key Regulations by Jurisdiction

| Regulation | Jurisdiction | Key Requirements | Effective |
|-----------|-------------|-----------------|-----------|
| **EU AI Act** | European Union | Risk-based classification, prohibited uses, transparency | 2024-2027 (phased) |
| **Colorado AI Act** | Colorado, USA | Algorithmic discrimination prevention, impact assessments | 2026 |
| **NYC Local Law 144** | New York City | Bias audits for automated employment decisions | 2023 |
| **CPRA** | California, USA | Right to opt out of automated decision-making | 2023 |
| **GDPR Art. 22** | EU/EEA | Right not to be subject to solely automated decisions | 2018 |
| **Executive Order 14110** | US Federal | AI safety standards, risk management | 2023 |
| **NIST AI RMF** | US (voluntary) | Risk management framework for AI systems | 2023 |
| **ISO/IEC 42001** | International | AI management system standard | 2023 |

### Compliance Mapping Template

```
COMPLIANCE MAPPING:

Regulation: [Name]
Applicable: [ ] Yes  [ ] No  [ ] Partially
Scope: [Which AI uses fall under this regulation]

REQUIREMENT                          | STATUS    | OWNER     | DUE DATE
Risk assessment completed            | [ ]       | [Name]    | [Date]
Transparency notices deployed        | [ ]       | [Name]    | [Date]
Bias audit conducted                 | [ ]       | [Name]    | [Date]
Data protection measures in place    | [ ]       | [Name]    | [Date]
Human oversight mechanism active     | [ ]       | [Name]    | [Date]
Documentation/records maintained     | [ ]       | [Name]    | [Date]
Training completed for staff         | [ ]       | [Name]    | [Date]
Incident response plan updated       | [ ]       | [Name]    | [Date]
```

## Ethical AI Framework

### Principles-Based Approach

| Principle | Definition | Implementation |
|-----------|-----------|---------------|
| **Fairness** | AI should not discriminate or create disparate impact | Regular bias audits, diverse training data review |
| **Transparency** | AI use and decision-making should be understandable | Explainability requirements, disclosure policies |
| **Accountability** | Clear ownership of AI decisions and outcomes | Governance structure, audit trails |
| **Privacy** | Respect for data rights and minimization | Data classification, consent frameworks |
| **Safety** | AI should not cause harm to individuals or groups | Testing protocols, human oversight, kill switches |
| **Beneficence** | AI should benefit the organization and society | Impact assessment, stakeholder engagement |

### Bias Testing Protocol

```
BIAS TESTING PROTOCOL:

PRE-DEPLOYMENT:
  1. Define protected characteristics relevant to use case
  2. Prepare representative test datasets
  3. Run model outputs across demographic groups
  4. Calculate disparate impact ratios
  5. Document results and remediation if needed

ONGOING MONITORING:
  Frequency: [Monthly / Quarterly / per regulation]
  Metrics:
    - Demographic parity: Equal selection rates across groups
    - Equalized odds: Equal error rates across groups
    - Calibration: Equal accuracy across groups
  Threshold: Disparate impact ratio < 0.8 triggers review

REMEDIATION:
  1. Identify root cause (data, model, process)
  2. Document corrective action plan
  3. Implement fix and retest
  4. Report to governance committee
```

## Data Handling Guidelines

### Data Classification for AI

| Classification | AI Input Allowed? | Conditions | Examples |
|---------------|------------------|-----------|---------|
| **Public** | Yes, any approved tool | Standard use policy | Published reports, press releases |
| **Internal** | Yes, approved enterprise tools only | No public AI tools | Internal memos, strategy docs |
| **Confidential** | Limited, with approval | Approved tools + DPA in place | Financial data, customer info |
| **Restricted** | No (or extreme controls) | CTO/CISO approval + encryption | PII, PHI, trade secrets, credentials |

### Vendor Assessment Checklist

```
AI VENDOR ASSESSMENT:

Vendor: _____________________
Tool/Service: _______________
Assessment Date: _____________

DATA HANDLING:
  [ ] Data processing agreement (DPA) in place?
  [ ] Where is data processed and stored?
  [ ] Is data used to train vendor's models?
  [ ] Can training opt-out be enforced?
  [ ] Data retention and deletion policies?
  [ ] Encryption at rest and in transit?
  [ ] SOC 2 Type II or equivalent certification?

SECURITY:
  [ ] Access controls and authentication?
  [ ] Audit logging available?
  [ ] Incident response procedures?
  [ ] Penetration testing conducted?
  [ ] Vulnerability management program?

COMPLIANCE:
  [ ] GDPR compliance (if applicable)?
  [ ] HIPAA compliance (if applicable)?
  [ ] Sector-specific certifications?
  [ ] Subprocessor transparency?

RECOMMENDATION: [ ] Approve  [ ] Conditional  [ ] Reject
```

## Training Program Design

### Role-Based Training Requirements

| Role | Training Topics | Frequency | Assessment |
|------|----------------|-----------|-----------|
| **All employees** | AI policy overview, acceptable use, data handling | Annual | Quiz (80% pass) |
| **Managers** | Risk assessment, approval workflows, oversight | Annual + refresher | Scenario-based |
| **IT/Engineering** | Security controls, prompt injection, model management | Semi-annual | Technical assessment |
| **Legal/Compliance** | Regulatory landscape, audit procedures, incident response | Semi-annual | Case study review |
| **AI Governance Committee** | Full policy, emerging regulations, industry best practices | Quarterly | Participation-based |
| **Executives** | Strategic implications, liability, governance | Annual | Briefing attendance |

## Policy Maintenance

### Review and Update Cadence

```
POLICY REVIEW SCHEDULE:

ANNUAL REVIEW (minimum):
  - Full policy review by governance committee
  - Regulatory landscape update
  - Incident review and lessons learned
  - Stakeholder feedback incorporation

TRIGGERED REVIEWS:
  - New regulation enacted affecting AI use
  - Significant AI incident (internal or industry)
  - Major new AI tool adoption
  - Organizational restructure
  - Merger/acquisition
  - Audit finding requiring policy change

VERSION CONTROL:
  Version: [X.X]
  Last Updated: [Date]
  Approved By: [Name/Committee]
  Next Review: [Date]
  Change Log: [Summary of changes per version]
```

## See Also

- [Legal Compliance](../legal-compliance/SKILL.md)
- [Risk Management](../risk-management/SKILL.md)
- [Security](../security/SKILL.md)
