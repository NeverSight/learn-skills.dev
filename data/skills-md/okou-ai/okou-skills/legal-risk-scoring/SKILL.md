---
name: legal-risk-scoring
description: Score legal risks by severity and likelihood, assign ratings, and document escalation paths.
---

## Scoring Model

### Two-Axis Evaluation Grid

Every legal risk is measured across two independent axes:

**Impact Magnitude** (consequences if the risk becomes reality):

| Rating | Descriptor | Meaning |
|---|---|---|
| 1 | **Trivial** | Minimal disruption; no meaningful financial, operational, or reputational consequence. Absorbed within day-to-day operations. |
| 2 | **Minor** | Contained impact; financial exposure under 1% of the relevant contract or transaction value; brief operational hiccup; no public visibility. |
| 3 | **Substantial** | Tangible impact; financial exposure in the 1-5% range of relevant value; noticeable operational interference; possibility of limited external attention. |
| 4 | **Serious** | Major impact; financial exposure between 5-25% of relevant value; significant operational disruption; probable public scrutiny; potential for regulatory interest. |
| 5 | **Severe** | Existential-level impact; financial exposure exceeding 25% of relevant value; core business operations threatened; material reputational harm; regulatory action anticipated; potential personal exposure for directors and officers. |

**Occurrence Probability** (how likely the risk is to materialize):

| Rating | Descriptor | Meaning |
|---|---|---|
| 1 | **Negligible** | Essentially theoretical; no known precedent in comparable situations; would demand extraordinary circumstances. |
| 2 | **Low** | Conceivable but not anticipated; sparse precedent; requires specific precipitating events. |
| 3 | **Moderate** | Plausible; some analogous situations have materialized; precipitating conditions are foreseeable. |
| 4 | **Elevated** | Expected to happen; clear precedent exists; precipitating conditions are commonplace in analogous contexts. |
| 5 | **Near Certain** | Virtually guaranteed; strong historical pattern; precipitating conditions are already present or imminent. |

### Computing the Score

**Risk Score = Impact Magnitude x Occurrence Probability**

| Score Band | Category | Indicator |
|---|---|---|
| 1-4 | **Baseline Risk** | GREEN |
| 5-9 | **Intermediate Risk** | YELLOW |
| 10-15 | **Elevated Risk** | ORANGE |
| 16-25 | **Acute Risk** | RED |

### Visual Grid

```
                     OCCURRENCE PROBABILITY
               Negligible  Low   Moderate  Elevated  Near Certain
                  (1)      (2)     (3)       (4)        (5)
IMPACT
Severe    (5) |   5    |   10   |   15   |   20   |     25     |
Serious   (4) |   4    |    8   |   12   |   16   |     20     |
Substantial(3)|   3    |    6   |    9   |   12   |     15     |
Minor     (2) |   2    |    4   |    6   |    8   |     10     |
Trivial   (1) |   1    |    2   |    3   |    4   |      5     |
```

## Category Profiles and Response Protocols

### GREEN -- Baseline Risk (Score 1-4)

**Profile**:
- Low-consequence issues with negligible probability
- Routine operational risks with well-established controls already in place
- Familiar risk patterns that the organization regularly manages

**Protocol**:
- **Accept**: Proceed with existing controls in place
- **Log**: Enter into the risk register for ongoing visibility
- **Periodic check**: Revisit during quarterly or annual review cycles
- **No escalation**: The responsible team member manages independently

**Typical scenarios**:
- Vendor agreement with a small deviation from preferred terms in a non-material area
- Standard confidentiality agreement with a reputable counterparty in a familiar jurisdiction
- Routine administrative compliance task with a clear owner and deadline

### YELLOW -- Intermediate Risk (Score 5-9)

**Profile**:
- Issues of moderate consequence that could arise under realistic conditions
- Risks deserving active attention without requiring emergency response
- Situations where precedent provides a management roadmap

**Protocol**:
- **Reduce exposure**: Deploy targeted controls or negotiate improved terms
- **Active surveillance**: Review monthly or upon occurrence of defined trigger events
- **Thorough documentation**: Capture the risk, all mitigation steps, and decision rationale in the register
- **Designated owner**: A specific individual holds accountability for tracking and mitigation
- **Stakeholder communication**: Relevant business contacts are informed of the risk and the mitigation approach
- **Escalation triggers**: Define specific conditions that would push this risk to a higher category

**Typical scenarios**:
- Agreement with a liability ceiling below the preferred level but within a negotiable range
- Vendor processing personal data in a territory with uncertain adequacy status
- Regulatory development that may affect a business line over the medium term
- IP provision that is broader than optimal but consistent with market practice

### ORANGE -- Elevated Risk (Score 10-15)

**Profile**:
- Weighty issues with a realistic chance of materializing
- Risks capable of producing significant financial, operational, or public-facing harm
- Situations demanding senior-level attention and structured mitigation

**Protocol**:
- **Senior counsel involvement**: Brief the head of legal or designated senior attorney
- **Structured mitigation plan**: Build a concrete, time-bound plan to reduce the risk
- **Leadership awareness**: Ensure relevant business leaders understand the risk and the recommended path
- **Frequent review**: Weekly check-ins or milestone-based reassessment
- **External counsel assessment**: Engage outside specialists for domain-specific guidance as warranted
- **Detailed written analysis**: Produce a full risk memorandum covering analysis, alternatives, and recommendations
- **Contingency planning**: Define the response playbook if the risk materializes

**Typical scenarios**:
- Agreement containing uncapped indemnification in a material obligation area
- Data processing operation that may violate regulatory requirements without restructuring
- Credible litigation threat from a significant counterparty
- Intellectual property infringement allegation with a plausible basis
- Formal regulatory inquiry or audit notification

### RED -- Acute Risk (Score 16-25)

**Profile**:
- The most consequential issues, with high or near-certain probability of materializing
- Risks that threaten fundamental business viability, expose officers and directors, or endanger key stakeholders
- Demands immediate executive engagement and rapid mobilization

**Protocol**:
- **Immediate executive briefing**: Notify General Counsel, C-suite, and Board as the situation warrants
- **Outside counsel retention**: Engage specialized external lawyers without delay
- **Dedicated response team**: Stand up a cross-functional team with clearly defined roles and authority
- **Insurance notification**: Alert carriers where coverage may apply
- **Crisis protocols**: Activate crisis management procedures when reputational exposure exists
- **Evidence preservation**: Institute a litigation hold if legal proceedings are a possibility
- **Continuous monitoring**: Daily or more frequent status reviews until resolved or downgraded
- **Board-level reporting**: Include in governance risk reporting as appropriate
- **Regulatory communication**: File any mandatory regulatory notifications

**Typical scenarios**:
- Pending litigation with substantial financial exposure
- Personal data breach affecting regulated information
- Active regulatory enforcement proceeding
- Material breach of or against the organization under a significant contract
- Government investigation
- Infringement claim targeting a core product or revenue-generating service

## Formal Documentation Standards

### Risk Assessment Memorandum

Every formal evaluation should follow this structure:

```

## Legal Risk Evaluation

**Prepared**: [date]
**Analyst**: [name of person conducting the evaluation]
**Subject**: [description of the matter under review]
**Privilege designation**: [Yes/No -- mark as attorney-client privileged where applicable]

### 1. Risk Statement
[Precise, concise articulation of the legal risk]

### 2. Factual Background
[Relevant facts, chronology, and business context]

### 3. Scoring Analysis

#### Impact Magnitude: [1-5] - [Descriptor]
[Supporting rationale including potential financial exposure, operational consequences, and reputational dimensions]

#### Occurrence Probability: [1-5] - [Descriptor]
[Supporting rationale including precedent, triggering conditions, and current circumstances]

#### Composite Score: [Number] - [GREEN/YELLOW/ORANGE/RED]

### 4. Aggravating Factors
[Elements that amplify the risk]

### 5. Countervailing Factors
[Elements that dampen the risk or contain exposure]

### 6. Mitigation Alternatives

| Alternative | Effectiveness | Resource Demand | Recommended? |
|---|---|---|---|
| [Option A] | [High/Med/Low] | [High/Med/Low] | [Yes/No] |
| [Option B] | [High/Med/Low] | [High/Med/Low] | [Yes/No] |

### 7. Recommended Course of Action
[Specific recommendation with supporting rationale]

### 8. Post-Mitigation Risk Level
[Projected risk category after implementing recommended measures]

### 9. Ongoing Monitoring Plan
[Frequency and method of review; conditions that would trigger reassessment]

### 10. Immediate Next Steps
1. [Task - Responsible party - Due date]
2. [Task - Responsible party - Due date]
```

### Risk Register Format

For entry into the team's centralized risk tracker:

| Field | Content |
|---|---|
| Identifier | Unique tracking code |
| Discovery Date | When the risk first came to light |
| Summary | Brief characterization |
| Domain | Contract / Regulatory / Litigation / IP / Data Privacy / Employment / Corporate / Other |
| Impact Rating | 1-5 with descriptor |
| Probability Rating | 1-5 with descriptor |
| Composite Score | Calculated value |
| Category | GREEN / YELLOW / ORANGE / RED |
| Accountable Person | Individual responsible for monitoring |
| Active Controls | Mitigations currently deployed |
| Disposition | Open / Mitigated / Accepted / Closed |
| Next Review | Scheduled reassessment date |
| Remarks | Supplementary context |

## Criteria for Engaging Outside Counsel

### Situations Requiring External Representation

- **Filed litigation**: Any lawsuit brought by or against the organization
- **Government proceedings**: Any inquiry from a regulatory agency, government body, or law enforcement
- **Criminal risk**: Any scenario involving potential criminal liability for the entity or its people
- **Capital markets implications**: Any matter that could affect securities disclosures or regulatory filings
- **Governance-level matters**: Any issue necessitating board notification or board-level approval

### Situations Strongly Favoring External Engagement

- **Uncharted legal territory**: Questions lacking settled authority where the organization's position could establish precedent
- **Multi-jurisdictional complexity**: Matters spanning unfamiliar or conflicting legal regimes
- **Outsized financial stakes**: Exposure exceeding the organization's defined risk appetite thresholds
- **Specialist knowledge gaps**: Subject areas not covered by in-house expertise (antitrust, anti-corruption, patent prosecution, etc.)
- **Major regulatory shifts**: New legal frameworks that require compliance program construction or significant adaptation
- **Strategic transactions**: Mergers, acquisitions, or major deals requiring diligence, structuring, and regulatory clearance

### Situations Worth Evaluating for External Support

- **Significant contractual disputes**: Substantial disagreements over interpretation with important business partners
- **Workforce claims**: Actual or threatened claims involving discrimination, harassment, wrongful termination, or retaliation
- **Data security events**: Incidents that may trigger mandatory notification duties
- **IP conflicts**: Infringement allegations (inbound or outbound) involving material products or services
- **Coverage disagreements**: Disputes with insurance carriers over claim coverage

### Selecting the Right Firm

When recommending outside engagement, prompt the user to weigh:
- Subject matter depth and track record
- Familiarity with the relevant jurisdiction
- Industry sector experience
- Conflict clearance status
- Fee structure expectations (hourly, flat, blended, contingency)
- Firm diversity commitments
- Pre-existing relationships (panel membership, prior engagements)
