---
name: regulatory-review
description: This skill should be used when the user asks to "analyze regulations", "regulatory landscape", "compliance requirements", "legal considerations", "regulatory risk", "industry regulations", "compliance analysis", "regulatory trends", or needs guidance on understanding regulatory environments, compliance requirements, or legal market factors.
version: 0.6.0
---

# Regulatory Review

## Overview

Regulatory review assesses the legal and compliance landscape affecting markets and products. This skill covers frameworks for understanding regulatory requirements, risks, and trends.

## Required Frameworks

| Framework | Output Section | Required | Condition |
|-----------|---------------|----------|-----------|
| Framework Identification | Applicable Frameworks | yes | — |
| Industry-to-Framework Mapping | Regulatory Mapping | yes | — |
| Penalty Ranges | Enforcement & Penalties | yes | — |
| Risk Matrix | Risk Assessment | yes | — |
| Cross-border Mechanisms | Cross-border Analysis | conditional | Multi-jurisdiction scope in elicitation |

**Trend Indicators**: Load and apply the trend indicator definitions from `protocols/TREND-INDICATORS.md`.

## Regulatory Dimensions

### Direct Regulations
- Industry-specific rules (fintech, healthcare, etc.)
- Product safety requirements
- Licensing and certification
- Operational standards

### Data & Privacy
- Data protection laws (GDPR, CCPA, etc.)
- Cross-border data transfer
- Consent requirements
- Breach notification

### Consumer Protection
- Advertising standards
- Fair trading practices
- Warranty requirements
- Dispute resolution

### Competition/Antitrust
- Market dominance rules
- M&A restrictions
- Pricing practices
- Distribution agreements

## Major Regulatory Frameworks

### Data Privacy

| Framework | Jurisdiction | Key Requirements |
|-----------|--------------|------------------|
| GDPR | EU | Consent, data rights, DPO, breach notification |
| CCPA/CPRA | California | Disclosure, opt-out, deletion rights |
| LGPD | Brazil | Similar to GDPR, local DPO |
| PIPL | China | Consent, localization, cross-border rules |

### Financial Services

| Framework | Jurisdiction | Scope |
|-----------|--------------|-------|
| Dodd-Frank | US | Banking, consumer protection |
| PSD2 | EU | Payment services, open banking |
| MiCA | EU | Crypto assets |
| SOX | US | Public company reporting |

### Healthcare

| Framework | Jurisdiction | Scope |
|-----------|--------------|-------|
| HIPAA | US | Health information privacy |
| FDA 21 CFR | US | Medical devices, pharma |
| MDR | EU | Medical devices |
| HITECH | US | Health IT security |

### Children's Privacy

| Framework | Jurisdiction | Scope |
|-----------|--------------|-------|
| COPPA | US | Children under 13 online privacy, parental consent |
| COPPA 2.0 (proposed) | US | Expanded age range, stricter consent |
| Age-Appropriate Design Code | California/UK | Privacy-by-design for minors |

**COPPA Parental Consent Methods** (FTC-approved):
- Signed consent form (mail/fax/scan)
- Credit card transaction verification
- Government ID check
- Knowledge-based authentication
- Video conference verification
- FTC-approved verifiable parental consent method

**Key COPPA Thresholds**:
- Under 13: Full COPPA applies; verifiable parental consent required before collecting ANY personal information
- CCPA/CPRA: Under 16 requires opt-in for sale/sharing of personal data; under 13 requires parental opt-in

### Consumer & Advertising

| Framework | Jurisdiction | Scope |
|-----------|--------------|-------|
| FTC Act Section 5 | US | Unfair/deceptive practices, advertising substantiation |
| FCA (Financial Conduct Authority) | UK | Financial services authorization and conduct |
| Proposition 65 | California | Chemical exposure warnings |
| FDA DSHEA | US | Dietary supplement labeling and safety |

### AI/Technology

| Framework | Jurisdiction | Scope |
|-----------|--------------|-------|
| EU AI Act | EU | AI risk classification, requirements |
| NYC Local Law 144 | NYC | AI in employment decisions (bias audits required) |
| State AI bills | Various US | Emerging requirements (IL, CO, MD) |
| EEOC AI Guidance | US | Anti-discrimination for AI hiring tools |

### AI/ML Bias Audit Requirements

When the product uses AI/ML in decisions affecting people (hiring, lending, insurance, housing), these specific requirements apply:

| Requirement | Source | Detail |
|-------------|--------|--------|
| Annual bias audit by independent auditor | NYC Local Law 144 | Must test for disparate impact across race/ethnicity and gender; publish summary results |
| 10-day candidate notice | NYC Local Law 144 | Notify candidates that AEDT is used; describe data collected and data retention policy |
| High-risk AI conformity assessment | EU AI Act | Employment, education, law enforcement AI classified as high-risk; requires risk management system, data governance, human oversight |
| Adverse impact analysis | EEOC/Title VII | Four-fifths rule for selection rates across protected categories; document validation studies |
| Algorithmic fairness assessment | Colorado SB 21-169 | Developers and deployers of high-risk AI must provide impact assessments |

## Industry-Framework Mapping

Use this table to quickly identify primary and secondary regulatory frameworks based on the user's industry:

| Industry | Primary Frameworks | Secondary Frameworks |
|----------|-------------------|----------------------|
| Healthcare/Telehealth | HIPAA, HITECH, FDA 21 CFR | GDPR (EU), State telehealth laws |
| Fintech/Crypto | Dodd-Frank, SEC, FCA (UK) | MiCA (EU), State MSB licensing, BSA/FinCEN |
| AI/ML in Employment | NYC Local Law 144, EEOC, EU AI Act | State AI bills, CCPA/CPRA |
| Children's Apps/Games | COPPA, FTC Act | CCPA minors provisions, App store policies |
| Medical Devices | FDA 21 CFR, EU MDR | TGA (AU), PMDA (JP), ISO 13485 |
| E-commerce/Supplements | FDA DSHEA, FTC Act, Prop 65 | CCPA/CPRA, cGMP (21 CFR 111) |
| SaaS/Data Processing | GDPR, CCPA/CPRA | ePrivacy, Sector-specific (HIPAA, PCI DSS) |

## Regulatory Risk Assessment

### Risk Categories

**Compliance Risk**
- Failure to meet existing requirements
- Likelihood: Based on current gaps
- Impact: Fines, operational restrictions

**Regulatory Change Risk**
- New or changing regulations
- Likelihood: Based on legislative trends
- Impact: Cost of compliance, market access

**Enforcement Risk**
- Increased regulatory scrutiny
- Likelihood: Based on enforcement patterns
- Impact: Investigations, penalties

**Reputational Risk**
- Public perception of compliance
- Likelihood: Based on sensitivity of issues
- Impact: Customer trust, brand damage

### Risk Matrix

| Risk | Likelihood | Impact | Trend | Mitigation |
|------|------------|--------|-------|------------|
| [Risk] | H/M/L | H/M/L | INC/DEC/CONST | [Action] |

## Regulatory Trend Analysis

### Trend Indicators

**INC (Increasing regulation)**
- New legislation proposed/passed
- Increased enforcement actions
- Growing public/political attention
- International coordination

**DEC (Decreasing regulation)**
- Deregulation initiatives
- Reduced enforcement
- Political shift toward less oversight

**CONST (Stable regulation)**
- Established framework
- Predictable enforcement
- No major changes pending

### Current Global Trends

| Area | Direction | Key Developments |
|------|-----------|------------------|
| Data Privacy | INC | More countries adopting GDPR-style laws |
| AI/ML | INC | EU AI Act, emerging US frameworks |
| Crypto/Fintech | INC | Global frameworks emerging |
| Competition/Big Tech | INC | Antitrust scrutiny increasing |
| ESG/Sustainability | INC | Disclosure requirements expanding |
| Cybersecurity | INC | Mandatory breach reporting |
| Children's Privacy | INC | COPPA 2.0, Kids Online Safety Act, state children's codes |
| Supplement/Consumer Products | INC | FDA mandatory listing, FTC enforcement of health claims |

## Compliance Assessment

### Gap Analysis Framework

| Requirement | Current State | Gap | Priority | Remediation |
|-------------|---------------|-----|----------|-------------|
| [Req 1] | Compliant/Partial/Non | Description | H/M/L | Action needed |

### Compliance Cost Estimation

| Component | One-Time | Ongoing Annual |
|-----------|----------|----------------|
| Technology | $X | $X |
| Personnel | $X | $X |
| Legal/Consulting | $X | $X |
| Training | $X | $X |
| Audit/Certification | $X | $X |
| **Total** | $X | $X |

## Jurisdiction Analysis

### Market Entry Considerations

| Jurisdiction | Key Regulations | Complexity | Barrier Level |
|--------------|-----------------|------------|---------------|
| US | Federal + 50 states | High | Medium |
| EU | GDPR + sector regs | High | High |
| UK | Post-Brexit regime | Medium | Medium |
| APAC | Varies widely | Variable | Variable |

### Cross-Border Considerations

- Data localization requirements
- Licensing reciprocity
- Contractual restrictions
- IP protection differences

### Cross-Border Data Transfer Mechanisms

When operations span multiple jurisdictions, identify which transfer mechanism applies:

| Mechanism | Use When | Key Requirements |
|-----------|----------|------------------|
| Standard Contractual Clauses (SCCs) | Transferring EU/UK data to non-adequate countries | 2021 version required; Transfer Impact Assessment mandatory |
| Adequacy Decisions | Transferring to countries with EU adequacy status | Verify current adequacy status (can be invalidated — see Schrems II) |
| Binding Corporate Rules (BCRs) | Intra-group transfers within multinational corporations | DPA approval required; lengthy approval process |
| Data Localization | Country requires data to remain within borders | China, Russia, India (proposed); may require local infrastructure |
| Consent-based Transfer | Individual explicitly consents to cross-border transfer | Not suitable for systematic/bulk transfers under GDPR |

## Output Rules

These rules are mandatory for every regulatory review output. They ensure consistency and completeness regardless of the specific industry or prompt:

1. **Use exact section headings** from the Output Structure below. Do not rename or skip sections.
2. **Every Risk Matrix row MUST include a Trend column** using exactly one of: `INC`, `DEC`, or `CONST`.
3. **Every Trend Analysis bullet MUST use the format**: `Area: INC/DEC/CONST - [Evidence sentence]`.
4. **Recommendations MUST include at least one of each**: Immediate action, Medium-term action, and Monitoring action.
5. **Compliance Assessment MUST use status symbols**: `✓` (compliant), `△` (partial), `✗` (non-compliant).
6. **Never use the phrase** "This is not legal advice" in the output. The skill disclaimer is in SKILL.md, not in outputs.
7. **Always include a Monitoring Indicators section** with at least 3 specific indicators (regulatory body names, legislative tracking sources).
8. **Cross-border data transfer**: When a prompt involves operations in multiple jurisdictions, always discuss data transfer mechanisms (SCCs, adequacy decisions, data localization).
9. **Children's data**: When the product involves users who may be minors, always address COPPA and parental consent requirements specifically.
10. **Compliance costs**: Always provide estimated ranges (not exact figures) broken down by Technology, Personnel, Legal/Consulting, Training, and Audit/Certification.

## Output Structure

```markdown
## Regulatory Review Summary

### Regulatory Landscape
[Overview of applicable regulations]

### Key Frameworks
| Framework | Applicability | Status |
|-----------|---------------|--------|
| [Name] | Direct/Indirect | Applicable/Monitor |

### Compliance Assessment
| Area | Status | Gap | Priority |
|------|--------|-----|----------|
| Data Privacy | ✓/△/✗ | [Gap] | H/M/L |
| [Other] | ✓/△/✗ | [Gap] | H/M/L |

### Regulatory Risk Matrix
| Risk | Likelihood | Impact | Trend |
|------|------------|--------|-------|
| [Risk] | H/M/L | H/M/L | INC/DEC/CONST |

### Trend Analysis
- Data Privacy: INC/DEC/CONST - [Evidence]
- Industry-Specific: INC/DEC/CONST - [Evidence]
- Enforcement: INC/DEC/CONST - [Evidence]

### Estimated Compliance Costs
[Cost breakdown]

### Recommendations
1. [Immediate action]
2. [Medium-term action]
3. [Monitoring action]

### Monitoring Indicators
- [Regulatory body announcements]
- [Legislative calendars]
- [Enforcement actions]
```

## Emerging Regulations to Monitor

These proposed or recently enacted regulations are not yet fully in force but will affect multiple industries. Reference them in Trend Analysis and Monitoring Indicators when relevant:

| Regulation | Jurisdiction | Status | Expected Impact |
|------------|-------------|--------|-----------------|
| COPPA 2.0 (FTC rulemaking) | US | Proposed rule | Expanded age range, stricter consent, limits on data use for marketing to children |
| Kids Online Safety Act (KOSA) | US | Passed Senate, House pending | Duty of care for platforms serving minors; impact assessments required |
| EU AI Act implementing rules | EU | Phased implementation 2024-2027 | High-risk AI requirements; prohibited practices; GPAI model obligations |
| Digital Markets Act (DMA) | EU | In force, enforcement ongoing | Gatekeeper obligations; interoperability; data portability for large platforms |
| State AI employment laws | US (IL, CO, MD, NY+) | Various stages | Bias audits, transparency, impact assessments for AI in hiring/employment |
| Federal privacy legislation | US | Proposed (APRA and others) | Potential national data privacy standard preempting state laws |
| India DPDP Act | India | Enacted, rules pending | Consent-based processing, data localization, significant penalty structure |

## Penalty Reference Ranges

Use these ranges to calibrate risk impact assessments. Cite specific enforcement examples when relevant to the user's industry:

| Framework | Maximum Penalty | Notable Enforcement Examples |
|-----------|----------------|------------------------------|
| GDPR | Up to 4% of global annual revenue or EUR 20M | Meta EUR 1.2B (2023, data transfers); Amazon EUR 746M (2021, targeting) |
| HIPAA | $50K-$1.9M per violation category per year | Anthem $16M (2018, breach); Premera $6.85M (2020, breach) |
| COPPA | $50,120 per violation (adjusted annually) | Epic Games $275M (2022, Fortnite); Microsoft/Xbox $20M (2023) |
| FTC Act | Varies; injunctive relief + restitution | FTC v. Kochava (2022, location data); numerous supplement enforcement |
| NYC Local Law 144 | $500-$1,500 per violation per day | Enforcement began July 2023; first actions pending |
| SEC (Securities) | Varies widely; disgorgement + penalties | BlockFi $100M (2022, crypto lending); multiple crypto actions |
| FDA (Medical Devices) | Warning letters, seizure, injunction, criminal prosecution | Numerous 510(k) enforcement; import alerts |

## Pre-Output Checklist

Before finalizing output, verify every item. This prevents common omissions that weaken the analysis:

1. [ ] **Regulatory Landscape section** opens the output with a narrative overview (not just a table)
2. [ ] **Key Frameworks table** lists at least 3 frameworks with Applicability and Status columns
3. [ ] **Compliance Assessment** uses `✓/△/✗` symbols and includes Priority column (H/M/L)
4. [ ] **Risk Matrix** has Likelihood, Impact, AND Trend columns; every row has INC/DEC/CONST
5. [ ] **Trend Analysis** has at least 3 bullet points, each using `INC/DEC/CONST - [Evidence]` format
6. [ ] **Recommendations** include at least one Immediate, one Medium-term, and one Monitoring action
7. [ ] **Monitoring Indicators** lists at least 3 specific sources (named regulatory bodies, legislative trackers)
8. [ ] **Compliance Costs** table is present with Technology, Personnel, Legal/Consulting, Training, and Audit rows
9. [ ] **No forbidden phrases** appear: "This is not legal advice", "I cannot provide legal advice", "consult a lawyer" (the disclaimer in SKILL.md handles this)
10. [ ] **Cross-border transfers** are addressed when multiple jurisdictions are involved (SCCs, adequacy, data localization)

## Best Practices

- Findings are research-grade, not compliance-grade — flag regulatory dependencies for qualified review
- Monitor regulatory developments continuously
- Consider both current and proposed regulations
- Assess both direct and indirect impacts
- Factor compliance costs into business planning

## Disclaimer

This skill provides research frameworks only. Consult qualified legal counsel for compliance decisions.

## Additional Resources

For detailed frameworks, see:
- `references/privacy-frameworks.md` - Data privacy details
- `references/compliance-checklist.md` - Compliance templates
- `examples/regulatory-analysis.md` - Sample analysis

## Orchestration Hints

**Confidence tiers (universal scale):**
- **High**: 3+ independent, recent (<12mo) sources that converge
- **Medium**: 2 sources OR sources >12mo old OR indirect evidence
- **Low**: Single source, inference, or extrapolation

Dimension-specific confidence criteria below REFINE (not replace) these universal definitions.

- **Cross-reference dimensions**: trends (regulatory trends and policy direction), competitive (compliance status of competitors)
- **Alert triggers**:
  - New regulation with <12 months to compliance deadline
  - Regulatory action against a major competitor
  - Policy shift that could enable or block market entry
- **Confidence rules**:
  - High: Published regulation or official government announcement
  - Medium: Proposed regulation in comment period or credible policy analysis
  - Low: Speculative based on political signals or advocacy positions
- **Conflict detection**:
  - Compliance timeline vs trend dimension's market entry projections
  - Regulatory burden cost vs financial dimension's unit economics
  - Compliance requirements vs tech dimension's feasibility assessment
