---
name: vendor-due-diligence-patrick-munro
description: "Risk-based vendor assessment framework for IT service providers, technology vendors, and third-party partners under DORA, NIS2, GDPR. Provides three-phase process (Initial Screening / Detailed Assessment / Final Evaluation), six-dimension risk scoring (Financial/Operational/Compliance/Security/Reputational/Strategic) with weighted matrices, full DORA Art. 28-30 contractual checklist, NIS2 Art. 21(2) security measures enumeration, GDPR Art. 28 documentation checks, red flags per dimension, trigger-based review criteria, and document templates. Use when: (1) Evaluating new vendors or technology providers, (2) Conducting critical ICT third-party due diligence under DORA, (3) Performing supply chain security assessment under NIS2, (4) Creating vendor onboarding documentation, (5) Establishing ongoing vendor monitoring, (6) Assessing concentration risk, or (7) Generating executive vendor risk reports."
metadata:
  author: "Patrick Munro"
  license: "agpl-3.0"
  version: "2026-04-25"
---

# Vendor Due Diligence Framework

## Overview
Risk-based vendor assessment framework that identifies material risks early, ensures DORA/NIS2/GDPR compliance, and provides clear recommendations for selection, contract calibration, and ongoing management. Built for regulated sectors (financial services under DORA, KRITIS sectors under NIS2) and for any organisation with meaningful ICT third-party exposure.

## LEGAL DISCLAIMER
This skill provides frameworks for vendor assessment purposes only. It does not constitute legal, financial, or professional advice. Users should:
- Consult qualified legal counsel for specific requirements in their jurisdiction;
- Engage financial and security professionals for detailed assessments;
- Verify all regulatory requirements independently;
- Adapt frameworks to specific organisational needs and risk tolerance;
- Not rely on this skill as a substitute for professional due diligence services.

The frameworks are templates. Actual assessments require expertise in law, finance, cybersecurity, and risk management. Neither the skill creator nor Claude/Anthropic assumes liability for decisions made based on this skill's output.

**Regulatory references current as of 2026-04-23.** EU (DORA, NIS2, GDPR) and German (NIS2UmsuCG, BDSG) citations reflect the consolidated text available at that date. Member State NIS2 transposition remains uneven; Germany's NIS2UmsuCG entered into force on 6 December 2025 with the BSI reporting portal opening on 6 January 2026. Verify the current consolidated text and national transposition status on EUR-Lex and the Bundesgesetzblatt before use.

## When to Use This Skill
- Evaluating new vendors, technology providers, or service partners;
- Conducting critical ICT third-party due diligence under DORA Art. 28-30;
- Supply chain security assessment under NIS2 Art. 21(2)(d);
- GDPR Art. 28 processor due diligence;
- Vendor onboarding documentation and assessment;
- Ongoing monitoring frameworks (quarterly, annual, trigger-based);
- Concentration risk assessment;
- Executive-level vendor risk reports.

## Core Capabilities

### 1. Three-Phase Assessment Process

**Phase 1: Initial Screening (1-2 days)**: rapid assessment to determine whether a vendor warrants detailed evaluation.
- Basic information verification (company registration, leadership, business model, customer base);
- Quick risk indicators (recent negative news, public financial data, compliance claims, basic technical architecture);
- Go/no-go decision with initial screening memo.

**Phase 2: Detailed Assessment (1-2 weeks)**: comprehensive evaluation across all risk dimensions. See Section 2.

**Phase 3: Final Evaluation (3-5 days)**: synthesis, risk scoring, mitigation strategies, recommendation.

### 2. Detailed Assessment Dimensions

#### Financial Due Diligence
Documents to request: 3 years audited financial statements; commercial credit report; professional liability insurance (€5M minimum); cyber insurance (€5M minimum for IT vendors); banking references.

Analysis: revenue trends and profitability; debt levels and liquidity ratios; customer concentration risk; financial stability score (1-5).

Red flags: consistent losses or negative cash flow; high customer concentration (>30% revenue from one client); recent credit downgrades; inadequate insurance coverage.

#### Legal and Compliance Due Diligence
Documents to request: articles of incorporation and bylaws; material contracts (top 5 customers and suppliers); pending and historical litigation; regulatory filings; IP portfolio; data protection policies and GDPR documentation; subprocessor list (if data processor).

GDPR compliance review (Art. 28 GDPR): privacy policy and notices; DPA template; breach incident response procedures; international data transfer mechanisms (SCCs, adequacy); Art. 30 records of processing; DPIA process for high-risk processing.

Industry-specific: financial services clients - DORA compliance (Art. 28-30); KRITIS sectors - NIS2 compliance (Art. 21); AI systems - AI Act classification and compliance.

Red flags: pending significant litigation (>10% annual revenue); regulatory enforcement actions; material IP infringement claims; GDPR non-compliance (no DPA, inadequate security).

#### Security and Technical Due Diligence
Documents to request: security certifications (ISO 27001, SOC 2 Type II, PCI DSS where applicable); recent penetration testing results; security incident history (3 years); business continuity and disaster recovery plans; backup procedures and testing records; technical architecture diagrams; data residency documentation; subprocessor security assessments.

Security assessment: encryption standards (at rest and in transit); access controls and identity management; vulnerability management program; security awareness training; incident response procedures and SLAs; third-party security audits.

NIS2 Art. 21(2) security measures (for KRITIS vendors), mapped to the ten statutory sub-paragraphs:
- (a) Risk analysis and information system security policies;
- (b) Incident handling;
- (c) Business continuity (backup management and disaster recovery) and crisis management;
- (d) Supply chain security, including security-related aspects of relationships with direct suppliers and service providers;
- (e) Security in network and information systems acquisition, development and maintenance, including vulnerability handling and disclosure;
- (f) Policies and procedures to assess the effectiveness of cybersecurity risk-management measures;
- (g) Basic cyber hygiene practices and cybersecurity training;
- (h) Policies and procedures on the use of cryptography and, where appropriate, encryption;
- (i) Human resources security, access control policies, and asset management;
- (j) Multi-factor authentication or continuous authentication, secured voice/video/text communications, and secured emergency communication systems where appropriate.

DORA ICT risk management (for financial services vendors): Art. 6-16 ICT risk management framework; Art. 17-23 incident management; Art. 24-27 digital operational resilience testing; Art. 28-30 third-party risk monitoring.

Red flags: no ISO 27001 or equivalent; no SOC 2 Type II; recent major security incidents with inadequate response; inadequate backup and DR; data residency non-compliance.

#### Operational Due Diligence
Documents to request: SLA performance history (12 months minimum); customer satisfaction metrics; support structure and escalation procedures; change management and release procedures; service availability statistics; MTTR data.

Analysis: service delivery track record; support responsiveness; technical competency; scalability; exit/transition procedures.

Red flags: consistent SLA failures; poor customer references; inadequate support infrastructure; no documented exit procedures.

### 3. Six-Dimension Risk Scoring

Score each vendor 1 (Low) to 5 (Critical) across dimensions. Weighted matrix:

| Category | Weight | Score | Weighted Score |
|----|----|----|----|
| Financial Risk | 20% | | |
| Operational Risk | 25% | | |
| Compliance Risk | 30% | | |
| Security Risk | 15% | | |
| Reputational Risk | 5% | | |
| Strategic Risk | 5% | | |
| TOTAL | 100% | | |

Critical services (payment processing, customer data systems, core business operations) receive 2x weight on security and compliance factors.

Risk score interpretation:
- 4.0-5.0: Low Risk; proceed with standard terms.
- 3.0-3.9: Medium Risk; enhanced due diligence required.
- 2.0-2.9: High Risk; additional safeguards needed.
- 1.0-1.9: Critical Risk; consider alternative vendors or reject.

### 4. DORA Critical Vendor Assessment

For financial services clients, DORA Art. 28-30 impose enhanced requirements for ICT third-party service providers.

**DORA Art. 28 - General Principles**: comprehensive ICT third-party risk management framework; full contractual documentation of all services; identification of all ICT third-party dependencies; comprehensive exit strategies.

**DORA Art. 30 - Mandatory Contract Elements**: service description (clear, complete, up-to-date); service locations (including subcontracting); service levels (SLAs with measurement and reporting); GDPR-compliant DPA; minimum security standards; availability and business continuity (DR/BCP); detailed exit strategy; regular and for-cause audit rights; subcontracting prior notification with objection rights; access for authorities (BaFin, ECB, ESMA inspection rights); termination rights (material breach, regulatory concerns); appropriate liability allocation; notice requirements for material changes, incidents, regulatory changes.

**Concentration risk (Art. 28(4))**: is the vendor used by multiple financial entities? Does this create systemic risk? Are alternatives available? What is our dependency level?

**Substitutability (Art. 28(4) read with Art. 29)**: can we switch vendors within 3-6 months (illustrative planning horizon; DORA itself requires "adequate transition periods" under Art. 30 rather than a fixed window)? Technical lock-ins? Data portability? Contractual barriers to exit?

**ICT sub-outsourcing (Art. 30(2)(a), read with the Commission Delegated Regulation on subcontracting RTS, JC 2024 53)**: all subcontractors identified; subcontractor locations documented; subcontractor security verified; subcontractor change notification process.

### 5. NIS2 Vendor Assessment

For vendors in NIS2 scope (KRITIS sectors under essential/important entity obligations), Art. 21 requires cybersecurity risk management measures.

Required assessments against Art. 21(2) measures are enumerated in Section 2 above. Supply chain security (Art. 21(2)(d)): vendor's own cybersecurity measures verified; vendor's supply chain security practices assessed; contractual cybersecurity obligations included; regular vendor security reviews; vendor incident notification requirements.

### 6. Risk Mitigation Strategies

**Financial**: shorter contract terms (1-2 years); payment terms protecting buyer (Net 30 vs. advance); parent company guarantees; performance bonds or escrow; more frequent financial reviews.

**Compliance**: enhanced contractual GDPR, DORA, NIS2 provisions; quarterly audit rights; regular compliance attestations; mandatory notification of regulatory changes; stricter SLAs with termination rights for non-compliance.

**Security**: required certifications as ongoing obligation; annual penetration testing at vendor cost; incident notification within 24 hours vs. 72; enhanced monitoring and logging; MFA requirements; regular security assessments.

**Operational**: robust SLAs with meaningful service credits; detailed exit and transition procedures; source code escrow for critical applications; dual sourcing for critical services; more frequent performance reviews.

**Strategic**: limit contract term; build exit provisions; avoid proprietary lock-in; maintain dual-source options.

### 7. Ongoing Vendor Management

**Quarterly reviews**: SLA compliance; service quality; security incidents; financial stability (where quarterly data available); compliance status.

**Annual assessments**: update full risk scoring matrix; contract performance and commercial terms review; market alternatives and pricing; strategic alignment; renewal or termination decision.

**Trigger-based reviews** (immediate): major security incident or data breach; regulatory enforcement action; material litigation; financial distress (credit downgrade, significant losses); acquisition or ownership change; service quality deterioration; repeated SLA failures; material contract breach.

### 8. Output Formats

**Vendor Risk Report (10-20 pages)**: executive summary; vendor background; financial assessment; legal and compliance review; security and technical evaluation; operational assessment; risk scoring matrix with justifications; mitigation recommendations; recommended contract terms; implementation and monitoring plan; appendices.

**Vendor Assessment Summary (2-3 pages)**: vendor overview and services; risk score summary table; key findings; recommendation (proceed/conditional/reject); required contract terms; next steps.

**Vendor Comparison Matrix**: side-by-side risk scores; compliance coverage comparison; cost-benefit analysis; strengths/weaknesses; recommended vendor with justification.

**Vendor Risk Register (spreadsheet)**: vendor name and ID; service type and criticality; risk scores by category; overall rating; last assessment date; next review date; key risks and mitigations; contract key terms; primary contact; escalation contacts.

**Vendor Onboarding Checklist**: due diligence completed and approved; contract negotiated and executed; insurance certificates received; DPA signed; security documentation reviewed; access provisioning completed; integration plan approved; service transition timeline; monitoring procedures implemented; relationship management assigned; vendor added to risk register; first quarterly review scheduled.

## Best Practices

1. Start with Phase 1 screening before investing in detailed assessment.
2. Scale diligence depth to service criticality and risk exposure.
3. Use risk scoring to calibrate contract terms.
4. Document all findings and recommendations (audit trail).
5. Involve Legal, IT/Security, Procurement, Business Units, and Compliance throughout.
6. Verify certifications directly with issuing bodies.
7. Check references with current customers.
8. Review vendor's own vendor management practices.
9. Plan for ongoing monitoring, not only initial assessment.
10. Track total vendor exposure across the organisation to identify dangerous concentration.

## Common Mistakes

1. Skipping financial due diligence for established vendors.
2. Accepting vendor self-assessments without verification.
3. Ignoring DORA/NIS2 requirements for critical vendors.
4. Approving vendors without documented risk mitigation.
5. Forgetting to assess exit and transition feasibility.
6. Overlooking subprocessor and fourth-party risks.
7. Neglecting ongoing monitoring after onboarding.
8. Approving vendors without legal and security review.

## Limitations

This skill does not: replace professional due diligence services; provide legal advice; guarantee vendor performance or eliminate risk; substitute for organisation-specific risk frameworks; fulfill regulatory obligations without expert validation; create attorney-client or fiduciary relationships.

Users must: adapt frameworks to their specific industry, jurisdiction, and risk tolerance; engage qualified professionals for regulated assessments; verify current regulatory requirements; obtain internal approvals; maintain documentation for audit and compliance; update criteria as regulations evolve.

## Example Use Cases

1. Financial institution under DORA assessing cloud service provider for critical payment systems.
2. Healthcare organisation evaluating SaaS vendor handling protected health information.
3. KRITIS-scope manufacturer performing NIS2 supply chain security assessment of industrial control system provider.
4. E-commerce platform conducting payment processor due diligence under PCI DSS.
5. Government agency performing FedRAMP compliance assessment for cloud infrastructure.
6. Startup running rapid vendor screening for limited-risk, non-critical services.