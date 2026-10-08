---
name: pa-clinical-policy
description: >
  Reasoning skill for prior authorization clinical policy evaluation. Use when the user asks about
  payer clinical criteria, step therapy requirements, medical necessity definitions, CMS LCD/NCD
  coverage rules, appeals documentation strategy, formulary tier implications, or FHIR Da Vinci PAS
  implementation guidance. Triggers include "prior auth policy", "step therapy", "medical necessity",
  "coverage determination", "LCD", "NCD", "formulary tier", "PA appeal", "peer-to-peer review",
  "Da Vinci PAS", "clinical criteria", "PA denial", "drug authorization", "utilization management".
usage: Use when evaluating prior authorization clinical policies, coverage rules, or appeal strategies.
version: 1.0.0
tags: [skill, category:reasoning, prior-authorization, clinical-policy, hcls]
---

# Prior Authorization Clinical Policy Reasoning

## Overview

Guide the agent through structured evaluation of prior authorization (PA) clinical policies,
coverage determinations, step therapy protocols, and appeals processes. This skill encodes
payer policy logic so the agent can assess whether a requested service meets authorization
criteria, identify documentation gaps, and recommend appeal strategies.

## Usage

- Invoke when evaluating whether a service meets prior authorization clinical criteria
- Use for step therapy evaluation, medical necessity assessment, or appeal strategy
- Activate for CMS LCD/NCD coverage rules or Da Vinci PAS implementation guidance

## Core Concepts

## Response Format

- Lead with the direct recommendation or classification (≤3 sentences)
- Structure as: recommendation → justification (citing specific criteria/thresholds) → caveats
- Use tables for comparisons; bullet points for criteria lists
- Omit background the user already knows — they asked the question
- Target: 200-400 words unless the user requests exhaustive detail
The decision trees and frameworks in this skill are for internal reasoning only. Apply them to reach your conclusion, but do not reproduce them in your response. Present only the final recommendation with supporting evidence.


## 1. Prior Authorization Decision Framework

When a user asks about a PA decision, follow this sequence:

1. **Identify the service type**: drug (pharmacy benefit), procedure, DME, or imaging
2. **Determine the payer**: commercial, Medicare, Medicaid, or Medicare Advantage
3. **Locate the applicable policy**: formulary, LCD/NCD, or internal clinical criteria
4. **Evaluate medical necessity**: match diagnosis + clinical evidence to criteria
5. **Check step therapy**: confirm required prior treatments were attempted
6. **Assess documentation completeness**: verify all required supporting information
7. **Recommend action**: approve path, identify gaps, or outline appeal strategy

## 2. Clinical Criteria Structures

### 2.1 Medical Necessity Definition

Medical necessity requires ALL of the following:

1. **Clinically appropriate**: consistent with diagnosis, symptoms, and accepted standards of care
2. **Not primarily for convenience**: of the patient, provider, or payer
3. **Most cost-effective level**: among equally effective alternatives
4. **Not experimental**: FDA-approved or supported by peer-reviewed evidence
5. **Expected to improve outcome**: measurable clinical benefit anticipated

### 2.3 Diagnosis-Specific Criteria Examples

| Condition | Requested Service | Required Criteria |
|-----------|-------------------|-------------------|
| Rheumatoid Arthritis | Biologic (TNF inhibitor) | Failure of ≥1 conventional DMARD (methotrexate) for ≥3 months |
| Multiple Sclerosis | Disease-modifying therapy | Confirmed MS diagnosis (McDonald criteria), relapse history |
| Chronic Pain | Opioid >90 MME/day | Pain management referral, urine drug screen, treatment agreement |
| Diabetes (Type 2) | GLP-1 receptor agonist | HbA1c ≥7% on metformin, or metformin contraindication documented |
| Cancer | PET/CT scan | Staging of newly diagnosed cancer or restaging after treatment |
| Sleep Apnea | CPAP device | AHI ≥5 on polysomnography, clinical symptoms documented |

## 3. Step Therapy Requirements

### 3.1 Step Therapy Logic

Step therapy mandates that lower-cost or first-line treatments are tried before authorizing
higher-cost alternatives. The general pattern:

```
Step 1: Generic / first-line therapy
  ↓ (documented failure, intolerance, or contraindication)
Step 2: Preferred brand / second-line therapy
  ↓ (documented failure, intolerance, or contraindication)
Step 3: Non-preferred / specialty therapy
```

### 3.2 Step Therapy Evaluation Rules

1. **Adequate trial duration**: each step must be tried for the clinically appropriate duration
   - Most oral medications: 30–90 days
   - Biologics: 12–16 weeks
   - Behavioral health: 8–12 weeks
2. **Documented failure**: objective evidence of inadequate response (lab values, symptom scores)
3. **Intolerance**: documented adverse effects that preclude continued use
4. **Contraindication**: clinical reason the step cannot be attempted (allergy, drug interaction, comorbidity)
5. **Step skip exceptions**: life-threatening conditions, prior step completed at another plan

### 3.3 Common Step Therapy Sequences

| Drug Class | Step 1 | Step 2 | Step 3 |
|------------|--------|--------|--------|
| Statins | Generic atorvastatin/rosuvastatin | Preferred brand statin | PCSK9 inhibitor |
| Antidepressants | Generic SSRI (sertraline, fluoxetine) | Generic SNRI (venlafaxine) | Brand atypical (Trintellix) |
| Biologics (RA) | Methotrexate + conventional DMARD | Preferred TNF inhibitor | Non-preferred biologic/JAK inhibitor |
| Diabetes | Metformin | Sulfonylurea or SGLT2 | GLP-1 RA or insulin |
| Asthma | ICS (fluticasone) | ICS/LABA combination | Biologic (omalizumab, dupilumab) |

## 4. CMS Coverage Determinations

### 4.1 NCD vs LCD

| Attribute | NCD (National) | LCD (Local) |
|-----------|----------------|-------------|
| Issuer | CMS central | Medicare Administrative Contractor (MAC) |
| Scope | All Medicare nationwide | MAC jurisdiction (A/B or DME) |
| Override | Cannot be overridden locally | Must comply with any applicable NCD |
| Appeal path | ALJ → Medicare Appeals Council → Federal court | Redetermination → QIC → ALJ |
| Update frequency | Infrequent (years) | More frequent (annual review) |

### 4.2 LCD Evaluation Checklist

When assessing whether a service is covered under an LCD:

- [ ] Identify the MAC jurisdiction for the provider's location
- [ ] Search the CMS Medicare Coverage Database for active LCDs
- [ ] Check the LCD's ICD-10 code list — is the patient's diagnosis included?
- [ ] Review the "Indications and Limitations" section for clinical criteria
- [ ] Verify the CPT/HCPCS code is listed as covered under the LCD
- [ ] Check for any associated billing article with documentation requirements
- [ ] Confirm no superseding NCD exists for the same service

## 5. Formulary Tier Structure

### 5.1 Formulary Exception Process

1. **Standard exception**: prescriber submits clinical rationale for non-formulary drug
2. **Expedited exception**: urgent clinical need, 24-hour turnaround required
3. **Tier reduction**: request lower cost-sharing based on medical necessity
4. **Required documentation**: letter of medical necessity, prior treatment history, lab results

## 6. Appeals Process

### 6.1 Appeal Levels (Commercial)

| Level | Action | Timeline | Decision Maker |
|-------|--------|----------|----------------|
| 1 | Internal appeal | 30 days (standard), 72 hours (expedited) | Payer medical director |
| 2 | External review | 45 days (standard), 72 hours (expedited) | Independent Review Organization (IRO) |
| 3 | State regulatory | Varies by state | Department of Insurance |

### 6.2 Appeal Levels (Medicare Part C/D)

| Level | Action | Timeline |
|-------|--------|----------|
| 1 | Plan redetermination | 7 days (expedited), 30 days (standard) |
| 2 | Independent Review Entity (IRE) | 7 days (expedited), 30 days (standard) |
| 3 | Administrative Law Judge (ALJ) | Amount in controversy ≥$180 (2024) |
| 4 | Medicare Appeals Council | No minimum amount |
| 5 | Federal District Court | Amount in controversy ≥$1,760 (2024) |

### 6.3 Peer-to-Peer Review Best Practices

When preparing for a peer-to-peer review with the payer medical director:

1. **Know the specific denial reason**: request the denial letter and clinical policy cited
2. **Prepare clinical evidence**: relevant labs, imaging, treatment history, specialist notes
3. **Reference guidelines**: cite society guidelines (ACR, NCCN, AAN) supporting the request
4. **Document prior treatments**: list all failed/tried therapies with dates and outcomes
5. **Articulate medical necessity**: explain why this specific service is required for this patient
6. **Note urgency**: if delay poses clinical risk, document the time-sensitive nature

### 6.4 Documentation Checklist for Appeals

- [ ] Copy of the denial letter with specific reason codes
- [ ] Letter of medical necessity from treating physician
- [ ] Relevant clinical notes (last 6–12 months)
- [ ] Lab results supporting the diagnosis and treatment need
- [ ] Prior treatment history with dates, doses, and outcomes
- [ ] Society guideline excerpts supporting the requested service
- [ ] Peer-reviewed literature (if off-label or emerging therapy)
- [ ] Patient statement (if relevant to functional impact)

## 7. FHIR Da Vinci PAS Implementation

### 7.1 Overview

The Da Vinci Prior Authorization Support (PAS) Implementation Guide defines a FHIR-based
workflow for submitting and tracking prior authorization requests. CMS mandates payer support
by 2026.

### 7.2 PAS Workflow Sequence

1. Provider EHR constructs a PAS `Bundle` with `Claim` + supporting resources
2. EHR submits `$submit` operation to payer's PAS endpoint
3. Payer returns `ClaimResponse` with disposition: `approved`, `denied`, or `pended`
4. If pended, payer may request additional info via `CommunicationRequest`
5. Provider submits updated `Bundle` with requested documentation
6. Payer issues final `ClaimResponse`
7. Provider queries `$inquire` operation for status updates

## When NOT to Use This Skill

- Making coverage determinations for individual patients (requires licensed clinician)
- When payer-specific contracts override published clinical policies
- Adjudicating appeals that require medical record review

## When to Escalate to a Human Expert

- Peer-to-peer review preparation (needs treating physician)
- When denial involves experimental/investigational determination
- When state Medicaid rules conflict with commercial payer policies

## 8. Common Mistakes

- **Wrong:** Assuming all payers use the same clinical criteria for a given service
  **Right:** Always check the specific payer's published clinical policy before submitting a PA request
  **Why:** Each payer maintains independent policies; criteria that work for one payer may not apply to another

- **Wrong:** Skipping step therapy documentation when the patient tried a drug at a prior plan
  **Right:** Document all prior treatments with dates, doses, duration, and outcomes — even from previous plans
  **Why:** Without documented evidence of prior steps, the payer will deny regardless of actual treatment history

- **Wrong:** Submitting appeals without addressing the specific denial reason code or cited criteria
  **Right:** Reference the exact denial reason and provide evidence directly addressing each unmet criterion
  **Why:** Generic appeals that don't target the specific denial rationale are almost always upheld

- **Wrong:** Applying an LCD from one MAC jurisdiction to a provider in a different MAC's territory
  **Right:** Identify the correct MAC jurisdiction for the provider's location and use that MAC's LCD
  **Why:** LCDs are jurisdiction-specific; coverage rules from one MAC have no authority in another

- **Wrong:** Treating LCDs and NCDs as equivalent or interchangeable
  **Right:** Always check for an applicable NCD first — NCDs take precedence and cannot be overridden by LCDs
  **Why:** An LCD cannot contradict or override a National Coverage Determination

- **Wrong:** Missing formulary exception deadlines, especially for expedited requests
  **Right:** Track and meet all turnaround requirements — 24 hours for expedited exceptions
  **Why:** Missed deadlines result in automatic denials and delayed patient access to needed medications

- **Wrong:** Conducting peer-to-peer reviews without citing published clinical guidelines
  **Right:** Reference specific society guidelines (ACR, NCCN, AAN) that support the requested service
  **Why:** Peer-to-peer reviews are significantly more effective when backed by authoritative guideline citations

- **Wrong:** Attaching clinical documentation as unstructured PDFs in Da Vinci PAS bundles
  **Right:** Structure clinical documentation in the `supportingInfo` field using proper FHIR resource references
  **Why:** Unstructured attachments cannot be processed by automated adjudication systems, causing delays

- **Wrong:** Applying commercial appeal timelines and processes to Medicare PA requests
  **Right:** Use Medicare-specific appeal levels and timelines (redetermination → IRE → ALJ → MAC → Federal court)
  **Why:** Medicare has distinct appeal levels, timelines, and amount-in-controversy thresholds

- **Wrong:** Failing to track PA expiration dates after authorization is granted
  **Right:** Monitor authorization validity periods and reauthorize before expiration if services are ongoing
  **Why:** Services rendered after PA expiration require new authorization — retroactive approval is rarely granted

## 9. Decision Tree: PA Request Evaluation

```
Is the service on the payer's PA-required list?
├── NO → No PA needed; proceed with service
└── YES
    ├── Is there an applicable NCD?
    │   ├── YES → Does the request meet NCD criteria?
    │   │   ├── YES → Approve (document NCD compliance)
    │   │   └── NO → Deny (cite NCD; appeal to ALJ if Medicare)
    │   └── NO → Check for LCD or plan-specific policy
    │       ├── LCD exists → Evaluate LCD criteria
    │       └── Plan policy exists → Evaluate plan criteria
    │           ├── Medical necessity met?
    │           │   ├── YES → Check step therapy
    │           │   │   ├── Step therapy satisfied → Approve
    │           │   │   └── Step therapy NOT satisfied
    │           │   │       ├── Exception applies? → Approve with exception
    │           │   │       └── No exception → Deny (cite step therapy)
    │           │   └── NO → Deny (cite medical necessity)
    │           └── Documentation incomplete?
    │               └── Pend for additional information
```

## 10. Quick Reference: Denial Reason Categories

| Category | CARC Code Range | Example | Recommended Action |
|----------|-----------------|---------|-------------------|
| Medical necessity not met | 50, 56 | Diagnosis does not support service | Appeal with clinical evidence |
| Step therapy not completed | 149 | Required prior drug not tried | Document prior treatments |
| Not a covered benefit | 96, 97 | Service excluded from plan | Formulary exception or plan change |
| Documentation insufficient | 16, 252 | Missing clinical notes | Resubmit with complete records |
| Experimental/investigational | 56 | Off-label use not approved | Cite peer-reviewed evidence |
| Out of network | 151 | Provider not in network | Network exception or referral |
| Duplicate authorization | 18 | PA already exists for service | Verify existing PA status |

## 11. PA Turnaround Time Requirements

| Request Type | Commercial (typical) | Medicare Part C | Medicare Part D |
|-------------|---------------------|-----------------|-----------------|
| Standard (non-urgent) | 15 calendar days | 14 calendar days | 72 hours (standard) |
| Expedited (urgent) | 72 hours | 72 hours | 24 hours |
| Retrospective | 30 calendar days | 30 calendar days | N/A |
| Extension (pend for info) | +14 days (one extension) | +14 days | +14 days |

### Urgency Determination Rules

A request qualifies as **expedited** when:

1. Applying standard timeframe could seriously jeopardize the patient's life or health
2. Applying standard timeframe could jeopardize the patient's ability to regain maximum function
3. A physician indicates the request is urgent (physician attestation)
4. The patient is currently undergoing treatment that would be interrupted

## 12. Quantity Limits and Site-of-Care Policies

### 12.1 Quantity Limit Structures

| Limit Type | Description | Example |
|-----------|-------------|---------|
| Per-fill limit | Maximum units per prescription fill | 30-day supply for controlled substances |
| Per-period limit | Maximum units over a time period | 9 fills per year for triptan medications |
| Lifetime limit | Maximum total units ever | Gene therapy — single administration |
| Diagnosis-based limit | Quantity varies by condition | Higher opioid limits for cancer pain |

### 12.2 Site-of-Care Optimization

Payers increasingly require lower-cost sites for infusion and injection therapies:

```
Is the drug available for home infusion?
├── YES → Home infusion preferred (lowest cost)
│   ├── Patient clinically stable? → Approve home infusion
│   └── Patient requires monitoring? → Approve outpatient infusion center
└── NO → Is outpatient infusion center available?
    ├── YES → Outpatient preferred over hospital outpatient
    └── NO → Hospital outpatient department approved
```

## 13. Regulatory Timeline: Key PA Reform Dates

| Date | Regulation | Impact |
|------|-----------|--------|
| Jan 2024 | CMS Interoperability Rule (CMS-0057-F) finalized | Payers must implement FHIR PAS API |
| Jan 2026 | FHIR PAS API mandate effective | Payers must accept electronic PA via Da Vinci PAS |
| Jan 2026 | PA decision transparency | Payers must provide specific denial reasons and applicable criteria |

### Gold Carding Programs

Several states require payers to exempt providers from PA if they demonstrate ≥90% approval rate for a specific service over 12 months. Exemption lasts 12 months, subject to audit, and is revoked if approval rate drops below threshold.
