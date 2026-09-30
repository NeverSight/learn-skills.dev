---
name: privacy-compliance
description: Handle privacy compliance tasks such as GDPR, CCPA, DPAs, DSARs, deletion, transfers, and breach notices.
---

## Global Privacy Landscape

### EU General Data Protection Regulation (GDPR)

**Territorial reach**: Governs the processing of personal data belonging to individuals located in the EU/EEA, irrespective of where the processing entity is based.

**Core obligations for in-house legal teams**:
- **Legal basis documentation**: Every processing activity must rest on one of six recognized grounds -- consent, contractual necessity, legitimate interest, statutory obligation, protection of vital interests, or public authority function
- **Individual rights fulfillment**: Requests for access, correction, deletion, portability, processing restriction, and objection must be resolved within one calendar month, with a two-month extension available for particularly involved requests
- **Impact assessments (DPIAs)**: Mandatory when processing is expected to create elevated risk for individuals
- **Incident reporting**: The competent supervisory authority must be notified within 72 hours of detecting a personal data breach; affected individuals require prompt notification when the breach poses high risk
- **Processing inventory**: Maintain the register of processing activities mandated by Article 30
- **Cross-border safeguards**: Transfers outside the EEA require valid mechanisms such as Standard Contractual Clauses, adequacy determinations, or Binding Corporate Rules
- **Data Protection Officer**: Appointment is required in specific situations -- public bodies, organizations conducting large-scale processing of sensitive categories, or those engaged in systematic large-scale monitoring

**Where in-house teams most often engage**:
- Evaluating vendor DPAs for regulatory alignment
- Counseling product teams on embedding privacy into design
- Managing communications with supervisory authorities
- Maintaining and updating transfer mechanisms
- Reviewing consent flows and privacy disclosures

### California CCPA / CPRA

**Territorial reach**: Applies to businesses handling the personal information of California residents that satisfy specified revenue, data volume, or data monetization thresholds.

**Core obligations**:
- **Disclosure right**: Individuals may request a full accounting of personal information collected, used, and disclosed
- **Deletion right**: Individuals may demand erasure of their personal information
- **Opt-out right**: Individuals may prohibit the sale or sharing of their personal information
- **Correction right**: Individuals may require amendment of inaccurate records (added by CPRA)
- **Sensitive data limitation**: Individuals may restrict the use of sensitive personal information to enumerated purposes (added by CPRA)
- **Equal treatment**: Organizations may not penalize individuals who exercise their statutory rights
- **Collection notice**: A privacy disclosure must be provided at or before the point of collection, detailing categories gathered and their purposes
- **Vendor agreements**: Contracts with service providers must confine personal information use to the specified business function

**Fulfillment deadlines**:
- Acknowledge receipt: 10 business days
- Provide substantive response: 45 calendar days, with a 45-day extension available upon notice

### Additional Jurisdictions to Track

| Framework | Territory | Distinguishing Features |
|---|---|---|
| **LGPD** | Brazil | Closely modeled on GDPR; DPO appointment mandatory; enforced by the ANPD |
| **POPIA** | South Africa | Overseen by the Information Regulator; processing registration required |
| **PIPEDA** | Canada (federal) | Consent-centric model; OPC oversight; modernization in progress |
| **PDPA** | Singapore | Includes Do Not Call registry; mandatory breach notification; PDPC enforcement |
| **Privacy Act** | Australia | Australian Privacy Principles (APPs); notifiable data breaches scheme |
| **PIPL** | China | Stringent cross-border transfer requirements; data localization mandates; CAC oversight |
| **UK GDPR** | United Kingdom | Post-Brexit adaptation; ICO supervision; substantively parallel to EU GDPR with UK-specific adequacy framework |

## Data Processing Agreement Review

When evaluating a DPA or data processing addendum, verify the presence and adequacy of the following elements.

### Mandatory Components (per GDPR Article 28)

- [ ] **Processing scope and timeline**: Clearly articulated subject matter, duration, and boundaries
- [ ] **Processing activities**: Specific description of what operations will be performed and for what business reason
- [ ] **Data categories**: Enumeration of the types of personal data involved
- [ ] **Data subject populations**: Identification of whose data is being processed
- [ ] **Controller prerogatives**: Specification of the controller's instruction authority and oversight rights

### Processor Commitments

- [ ] **Instruction adherence**: Processor undertakes to act solely on documented controller instructions, except where overridden by applicable law
- [ ] **Personnel confidentiality**: All individuals authorized to handle personal data have binding confidentiality commitments
- [ ] **Security posture**: Adequate technical and organizational safeguards are described, referencing Article 32 standards
- [ ] **Sub-processing governance**:
  - [ ] Prior written authorization requirement (general or specific)
  - [ ] For general authorization: advance notification of sub-processor changes with a meaningful objection window
  - [ ] Sub-processors contractually bound to equivalent obligations
  - [ ] Processor retains liability for sub-processor conduct
- [ ] **Rights request support**: Processor commits to assisting the controller with individual rights fulfillment
- [ ] **Incident and assessment support**: Processor provides assistance with security compliance, breach reporting, impact assessments, and prior consultation
- [ ] **End-of-term data handling**: Upon contract conclusion, all personal data is deleted or returned at the controller's election; residual copies are destroyed unless law mandates retention
- [ ] **Verification rights**: Controller holds the right to audit and inspect, or to accept independent third-party audit reports
- [ ] **Breach alerting**: Processor will report personal data breaches without undue delay, ideally within 24 to 48 hours, ensuring the controller can meet the 72-hour regulatory window

### International Transfer Provisions

- [ ] **Mechanism specified**: SCCs, adequacy determination, Binding Corporate Rules, or other recognized safeguard identified
- [ ] **SCC version**: Current EU SCCs (adopted June 2021) employed where applicable
- [ ] **Module selection**: Correct SCC module chosen for the relationship (Controller-to-Processor, Controller-to-Controller, Processor-to-Processor, Processor-to-Controller)
- [ ] **Transfer risk evaluation**: Completed for destinations lacking an adequacy determination
- [ ] **Supplemental safeguards**: Technical, organizational, or contractual measures addressing gaps revealed by the transfer risk evaluation
- [ ] **UK coverage**: If UK personal data is within scope, the UK International Data Transfer Addendum is appended

### Operational Alignment

- [ ] **Liability coordination**: DPA liability terms are consistent with (and do not undermine) the master services agreement
- [ ] **Term synchronization**: DPA duration aligns with the underlying services contract
- [ ] **Geographic specificity**: Processing locations are enumerated and acceptable
- [ ] **Security certifications**: Relevant standards or attestations required (SOC 2 Type II, ISO 27001, etc.)
- [ ] **Risk transfer**: Adequate insurance coverage for data processing activities confirmed

### Recurring DPA Weaknesses

| Weakness | Exposure | Recommended Position |
|---|---|---|
| Blanket sub-processor approval without notification | Erodes controller oversight of the processing chain | Mandate advance notice with right to object |
| Breach notification window exceeding 72 hours | Controller may miss regulatory reporting deadline | Set notification at 24 to 48 hours |
| Audit rights limited to third-party reports only | No direct verification capability | Accept SOC 2 Type II as baseline plus direct audit on cause |
| No data deletion timeline specified | Data may persist indefinitely after contract end | Require deletion within 30 to 90 days of termination |
| Processing locations undisclosed | Data could move to any jurisdiction without notice | Require enumeration of all processing locations |
| Legacy SCCs still referenced | Transfer mechanism may be legally invalid | Mandate current 2021 EU SCCs |

## Individual Rights Request Management

### Intake Procedure

When an individual rights request arrives:

1. **Categorize the request**:
   - Access (provide a copy of their personal data)
   - Correction (fix inaccurate records)
   - Erasure (remove personal data, the "right to be forgotten")
   - Processing restriction (pause certain uses)
   - Portability (deliver data in a structured, machine-readable format)
   - Objection (challenge a specific processing activity)
   - Sale/sharing opt-out (CCPA/CPRA)
   - Sensitive data use limitation (CPRA)

2. **Determine governing law**:
   - Where does the individual reside?
   - Which statutes apply given the organization's geographic presence and activities?
   - What specific procedural requirements and deadlines govern?

3. **Authenticate the requester**:
   - Confirm the individual's identity through proportionate verification measures
   - Scale verification rigor to the sensitivity of the data involved
   - Avoid demanding excessive proof that could itself become a barrier to exercising rights

4. **Record the request**:
   - Date of receipt
   - Request category
   - Requester identity
   - Applicable statute(s)
   - Response due date
   - Assigned team member

### Statutory Deadlines

| Statute | Initial Acknowledgment | Full Response | Available Extension |
|---|---|---|---|
| GDPR | Best practice: promptly | 30 calendar days | +60 days with notice |
| CCPA/CPRA | 10 business days | 45 calendar days | +45 days with notice |
| UK GDPR | Best practice: promptly | 30 calendar days | +60 days with notice |
| LGPD | Not prescribed | 15 calendar days | Narrow extension options |

### Grounds for Declining or Limiting Fulfillment

Assess whether any recognized exception applies before acting on a request:

**Widely recognized exceptions**:
- Establishment, exercise, or defense of legal claims
- Retention mandated by law or regulation
- Public interest or exercise of official functions
- Freedom of expression and information (erasure context)
- Archival, scientific, or historical research purposes in the public interest

**Organization-specific factors**:
- Active litigation hold: data under legal preservation cannot be destroyed
- Regulatory retention schedules: financial records, employment files, and other categories may have prescribed minimum retention periods
- Third-party rights: fulfilling the request could adversely affect the rights or freedoms of another individual

### Fulfillment Workflow

1. Locate all personal data pertaining to the requester across organizational systems
2. Evaluate and document any applicable exceptions
3. Prepare the response: honor the request or clearly explain why it cannot be fulfilled (in whole or in part)
4. For any partial or full refusal: cite the precise legal basis
5. Advise the requester of their right to file a complaint with the relevant supervisory authority
6. Retain a complete record of the request, the response, and the supporting rationale

## Staying Current with Regulatory Change

### Areas to Monitor

Keep a continuous watch on:
- **Supervisory authority publications**: New or revised guidance from the ICO, CNIL, FTC, state attorneys general, and comparable bodies
- **Enforcement activity**: Penalties, orders, and settlements that reveal regulatory priorities and thresholds
- **Legislative movement**: Enactment of new privacy statutes, amendments to existing law, and implementing regulations
- **Technical standards evolution**: Revisions to ISO 27001, SOC 2, NIST frameworks, and sector-specific requirements
- **Transfer mechanism developments**: New or revoked adequacy decisions, SCC modifications, data localization mandates

### Practical Monitoring Approach

1. **Official channels**: Subscribe to regulatory authority email alerts, RSS feeds, and formal gazette notices
2. **Legal analysis**: Follow reputable privacy law publications that contextualize new developments
3. **Industry bodies**: Monitor trade association and industry group communications for sector-tailored guidance
4. **Compliance calendar**: Maintain a timeline of known effective dates, filing deadlines, and compliance milestones
5. **Team updates**: Regularly brief the legal team on developments that affect the organization's data processing activities

### When to Escalate

Bring regulatory developments to senior counsel or leadership attention when:
- New legislation or guidance directly impacts the organization's core processing activities
- An enforcement action in the organization's industry signals increased regulatory focus
- An approaching compliance deadline requires operational or technical changes
- A transfer mechanism the organization depends on faces legal challenge or invalidation
- A supervisory authority opens a formal inquiry or investigation involving the organization
