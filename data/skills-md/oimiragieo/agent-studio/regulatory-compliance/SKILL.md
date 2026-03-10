---
name: regulatory-compliance
description: Validate systems and processes against GDPR/CCPA privacy regulations, privacy-by-design principles, ADA/WCAG accessibility standards, data processing agreements (DPAs), and provide compliance checklists with regulatory change monitoring guidance.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Glob, Grep, Skill]
agents: [compliance-checker]
category: 'Compliance & Legal'
tags: [gdpr, ccpa, privacy, wcag, ada, accessibility, dpa, compliance, regulatory]
error_handling: graceful
streaming: supported
best_practices:
  - Validate all applicable regulations (GDPR, CCPA, state laws) — not just one
  - Never report PASS on partial compliance; use CONDITIONAL with remediation tasks
  - Include specific remediation steps and owning agent for every FAIL/CONDITIONAL
  - Regulatory landscape changes — always link to authoritative source URLs
  - Privacy-by-design must be verified at design time, not retrofitted
verified: true
lastVerifiedAt: 2026-03-02T00:00:00.000Z
---

# Regulatory Compliance Skill

## Overview

Assess systems, processes, and artifacts against major regulatory frameworks:

- **GDPR/CCPA** — Data privacy compliance for EU and California/US state laws
- **Privacy-by-Design** — Proactive privacy embedding following Ann Cavoukian's 7 principles
- **ADA/WCAG** — Web and software accessibility under ADA and WCAG 2.1/2.2 AA standards
- **DPA Validation** — Data Processing Agreement completeness and correctness checks
- **Regulatory Monitoring** — Guidance on tracking regulatory changes across jurisdictions

Output is structured as PASS / CONDITIONAL / FAIL with severity-rated findings and actionable remediation tasks.

## When to Use

- Before deploying any feature that collects, processes, or stores personal data
- During architecture review for systems touching PII or user data
- When validating third-party vendor agreements and DPAs
- Before launching products in EU, California, or any jurisdiction with active privacy law
- When auditing accessibility compliance for public-facing interfaces
- As part of CI compliance gates for data pipelines and APIs

## Iron Laws

1. **NEVER report PASS on partial compliance** — if any item fails, the result is CONDITIONAL or FAIL; partial compliance masks violations.
2. **ALWAYS include remediation tasks with specific owning agents** — vague findings don't produce fixes; every FAIL/CONDITIONAL must specify who fixes it and how.
3. **NEVER skip multi-jurisdiction check** — GDPR, CCPA, and 20+ US state laws may all apply; document scope clearly.
4. **ALWAYS verify privacy-by-design at design time** — retrofitting privacy after deployment is significantly more costly and less effective.
5. **NEVER treat accessibility as optional** — ADA/WCAG compliance carries active litigation risk (ADA lawsuits up 37% H1 2025); all public interfaces must be validated.
6. **ALWAYS document regulation version and date assessed** — regulatory guidance evolves; stamp every report with the regulation version and assessment date.

## Workflow

### Step 1: Scope Definition

Define which regulations apply to the subject of the assessment:

```markdown
## Compliance Scope

- Subject: [System / Feature / DPA / Interface being assessed]
- Jurisdictions: [EU / California / Virginia / Colorado / Other states]
- Applicable Regulations:
  - [ ] GDPR (EU General Data Protection Regulation)
  - [ ] CCPA/CPRA (California Consumer Privacy Act / California Privacy Rights Act)
  - [ ] US State Laws (VCDPA, CPA, CTDPA, etc.)
  - [ ] ADA / Section 508 (US accessibility)
  - [ ] WCAG 2.1/2.2 AA (Web Content Accessibility Guidelines)
  - [ ] DPA Review (vendor data processing agreement)
- Personal Data Categories Involved: [list data types]
- Assessment Date: [YYYY-MM-DD]
- Regulation Versions Referenced: [e.g., GDPR as amended 2024, CPRA effective 2023]
```

### Step 2: GDPR/CCPA Compliance Checklist

Execute checklist items relevant to the assessed subject:

#### Data Inventory & Mapping

- [ ] All personal data types cataloged (name, email, IP, behavioral data, biometrics, etc.)
- [ ] Data flows documented: collection → processing → storage → sharing → deletion
- [ ] Purpose for each data type explicitly defined and limited
- [ ] Legal basis for processing documented (consent, legitimate interest, contract, legal obligation)
- [ ] Data retention periods defined per data type

#### Consent Management

- [ ] GDPR: Granular consent obtained per processing purpose (not blanket acceptance)
- [ ] GDPR: Consent as easy to withdraw as to give (one-click unsubscribe)
- [ ] CCPA: Opt-out mechanism present for data sale/sharing ("Do Not Sell or Share My Personal Information")
- [ ] Consent records maintained (who consented, when, to what)
- [ ] Cookie consent implemented for tracking cookies (GDPR only)

#### Consumer Rights Processing

- [ ] Right of access request mechanism exists (DSR/DSAR portal or process)
- [ ] Right to deletion honored within required timeframe (GDPR: 30 days, CCPA: 45 days)
- [ ] Right to portability supported (GDPR: structured, machine-readable format)
- [ ] Right to correct/rectify inaccurate data supported
- [ ] DSR records maintained for 24+ months (audit trail)

#### Third-Party & Vendor Management

- [ ] DPAs in place with all vendors processing personal data
- [ ] Vendor list maintained and reviewed annually
- [ ] Standard Contractual Clauses (SCCs) present for international data transfers
- [ ] Sub-processor notifications in DPAs

#### Security Requirements

- [ ] Reasonable security measures implemented (encryption at rest and in transit)
- [ ] Access controls and principle of least privilege enforced
- [ ] Breach notification procedure documented (GDPR: 72 hours to supervisory authority)
- [ ] Security risk assessment conducted for processing activities

### Step 3: Privacy-by-Design Review

Evaluate against Ann Cavoukian's 7 Foundational Principles:

| Principle                     | Assessment                                                      |
| ----------------------------- | --------------------------------------------------------------- |
| 1. Proactive, not reactive    | Is privacy built in from design stage, not added after?         |
| 2. Privacy as default         | Is the most privacy-protective setting the default?             |
| 3. Privacy embedded in design | Is privacy integral to system architecture, not a bolt-on?      |
| 4. Full functionality         | Does privacy coexist with legitimate business objectives?       |
| 5. End-to-end security        | Is full lifecycle security ensured from collection to deletion? |
| 6. Visibility & transparency  | Are policies and practices open and verifiable?                 |
| 7. Respect for user privacy   | Is user-centricity maintained in all design decisions?          |

Record each principle as: **Implemented / Partial / Missing / Not Applicable**

### Step 4: ADA/WCAG Accessibility Audit

Evaluate against WCAG 2.1 AA (minimum standard) / WCAG 2.2 AA (current standard):

#### POUR Principles

- **Perceivable**: All non-text content has text alternatives; audio/video has captions/transcripts; content is not restricted to color alone; minimum 4.5:1 contrast ratio for normal text
- **Operable**: All functionality available via keyboard; no keyboard traps; skip navigation links present; sufficient time to interact; no content that seizures (no flashing >3Hz)
- **Understandable**: Language of page set in HTML; error messages are descriptive and helpful; consistent navigation across pages; form labels and instructions clear
- **Robust**: Valid HTML/ARIA; compatible with current assistive technologies; ARIA labels and roles correctly applied

#### AI Interface Specific (2025+)

- [ ] Chatbot interfaces keyboard accessible and screen reader compatible
- [ ] AI-generated content has proper semantic structure
- [ ] Alt text provided for AI-generated images
- [ ] Voice interfaces have visual alternatives

#### Severity Classification for Accessibility

- **CRITICAL**: Completely blocks access for users with disabilities (missing keyboard navigation, no screen reader support)
- **HIGH**: Significantly impedes usage (poor contrast, missing alt text on key images)
- **MEDIUM**: Creates friction but workarounds exist (missing skip links, inconsistent labels)
- **LOW**: Best practice improvement (decorative image has non-empty alt text)

### Step 5: DPA Validation Checklist

If reviewing a Data Processing Agreement:

#### Required DPA Elements (GDPR Article 28)

- [ ] Parties clearly identified (controller name/address, processor name/address)
- [ ] Subject matter, nature, and purpose of processing defined
- [ ] Type of personal data and categories of data subjects specified
- [ ] Duration of processing specified
- [ ] Controller obligations and rights documented
- [ ] Processor obligations:
  - [ ] Process only on documented controller instructions
  - [ ] Ensure confidentiality of processing personnel
  - [ ] Implement appropriate technical/organizational security measures
  - [ ] Sub-processor rules: require prior written consent; flow-down obligations
  - [ ] Assist controller with DSARs and Article 32-36 obligations
  - [ ] Delete or return data at end of service
  - [ ] Provide audit cooperation and information
- [ ] International transfer mechanism specified (SCCs, adequacy decision, etc.)
- [ ] Breach notification procedure: processor notifies controller without undue delay
- [ ] DPA update trigger: reviewed annually or upon significant processing changes

#### DPA Quality Flags

- [ ] No vague processing descriptions ("process data as needed") — specificity required
- [ ] Security measures described with appropriate detail (encryption, access controls, staff training)
- [ ] Sub-processor list available and maintained
- [ ] Transfer Impact Assessment (TIA) conducted for high-risk countries

### Step 6: Regulatory Monitoring Guidance

Provide guidance on maintaining ongoing compliance:

#### Monitoring Sources

- **GDPR**: European Data Protection Board (EDPB) — <https://edpb.europa.eu/>
- **CCPA/CPRA**: California Privacy Protection Agency — <https://cppa.ca.gov/>
- **US State Laws**: IAPP State Privacy Legislation Tracker — <https://iapp.org/resources/article/us-state-privacy-legislation-tracker/>
- **WCAG**: W3C WAI — <https://www.w3.org/WAI/>
- **ADA**: US DOJ ADA.gov — <https://www.ada.gov/>

#### Monitoring Cadence

- **Monthly**: Review enforcement actions from supervisory authorities
- **Quarterly**: Check for new or amended state privacy laws
- **Annually**: Full DPA review with all processors; full accessibility audit
- **On Change**: Re-assess whenever data processing activities, vendors, or interfaces change materially

### Step 7: Produce Compliance Decision

Output one of three decisions:

```json
{
  "decision": "PASS | CONDITIONAL | FAIL",
  "regulationsAssessed": ["GDPR", "CCPA", "WCAG 2.1 AA", "DPA"],
  "assessmentDate": "YYYY-MM-DD",
  "findings": [
    {
      "id": "RC-001",
      "regulation": "GDPR",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "category": "Consent Management",
      "description": "Cookie consent banner missing for analytics tracking cookies",
      "status": "FAIL",
      "remediation": "Implement cookie consent platform with granular purpose-based opt-in",
      "owner": "developer",
      "deadline": "Before next deployment"
    }
  ],
  "requiredMitigations": [],
  "evidencePaths": [".claude/context/reports/compliance/"],
  "regulatoryLinks": [
    "https://edpb.europa.eu/our-work-tools/documents/public-consultations/2023/guidelines-032023-deceptive-design-patterns_en"
  ],
  "nextReviewDate": "YYYY-MM-DD",
  "recommendedNextStep": "Assign RC-001 to developer agent; re-assess after remediation"
}
```

**Decision Rules:**

- `PASS`: All applicable checklist items verified, no open findings
- `CONDITIONAL`: Minor or medium findings present; allowed to proceed with documented remediation plan
- `FAIL`: Critical or high findings present; must remediate before deployment

## Output Protocol

### Report Location

Save compliance reports to: `.claude/context/reports/compliance/`

**Naming**: `{subject}-compliance-{YYYY-MM-DD}.md`

### Report Sections (Required)

1. Scope definition (Step 1 output)
2. GDPR/CCPA checklist results (Step 2)
3. Privacy-by-design assessment (Step 3)
4. Accessibility audit results (Step 4, if applicable)
5. DPA validation (Step 5, if applicable)
6. Structured decision JSON (Step 7)
7. Remediation task list with owners and deadlines
8. Regulatory monitoring recommendations

## Anti-Patterns

| Anti-Pattern                                 | Why It Fails                           | Correct Approach                                                |
| -------------------------------------------- | -------------------------------------- | --------------------------------------------------------------- |
| Checking GDPR only, ignoring CCPA/state laws | Multi-jurisdiction exposure missed     | Always assess all applicable jurisdictions                      |
| Reporting PASS when most items pass          | Partial compliance is non-compliance   | CONDITIONAL/FAIL for any open finding                           |
| Generic "implement encryption" remediation   | Developer cannot act on vague guidance | Specific: "AES-256 encryption for PII fields in users table"    |
| One-time audit treated as ongoing compliance | Regulations change quarterly           | Establish continuous monitoring cadence                         |
| Treating accessibility as a nice-to-have     | ADA lawsuits are an active legal risk  | WCAG 2.1 AA compliance is non-negotiable for public interfaces  |
| DPA with vague processing description        | Regulators reject vague DPAs           | Specify exact data types, processing purpose, retention periods |

## Enforcement Hooks

Input validated against `schemas/input.schema.json` before execution.
Output contract defined in `schemas/output.schema.json`.
Pre-execution hook: `hooks/pre-execute.cjs`
Post-execution hook: `hooks/post-execute.cjs` (emits observability event)

## Memory Protocol

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

Check for:

- Previous compliance assessments on similar systems
- Known regulatory patterns and documented decisions
- Outstanding compliance blockers in issues.md

**After completing:**

- New compliance findings → Append to `.claude/context/memory/issues.md`
- Regulatory decisions → Append to `.claude/context/memory/decisions.md`
- Successful compliance patterns → Append to `.claude/context/memory/learnings.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
