---
name: provider-denial-workup
description: "Reasoning skill for healthcare revenue cycle denial management. Use when the user needs to appeal a claim denial, draft a payer-ready denial appeal letter, analyze a denial reason code, or determine whether a denied claim should be overturned, pended, or accepted. Triggers include \"appeal a claim denial\", \"draft denial appeal\", \"write appeal letter\", \"CO-50 denial\", \"medical necessity denial\", \"CARC code appeal\", \"RARC code\", \"overturn denial\", \"prior auth denial\", \"timely filing denial\", \"denial workup\", \"payer denial response\", \"claim denial overturn\", \"CO-96 denial\", \"CO-97 denial\", \"denial letter\", \"denial management\", \"remittance advice denial\", \"835 denial\", \"authorization required denial\", \"ERISA denial\", \"Medicaid managed care denial\", \"visit limit denial\", \"benefit limit denial\", \"inpatient denial\", \"observation downgrade\"."
usage: Invoke when asked to appeal a claim denial, classify a CARC/RARC denial, or draft a provider-to-payer appeal letter.
version: 1.0.0
tags: [skill, category:reasoning, revenue-cycle, denials, hcls]
---

# Provider Denial Workup — Reasoning Skill

## Overview


Guide the agent through structured analysis of payer claim denials: classify the denial
category, determine the appropriate appeal posture, and draft a payer-ready appeal letter.
This skill encodes CARC/RARC interpretation, appeal pathway logic, and letter-drafting
standards for revenue cycle staff.

## When to Use

- A claim has been denied and the user wants to understand why and what to do next
- The user provides a remittance advice (835 ERA) showing a denial and asks for next steps
- The user needs a draft appeal letter for a specific denial reason
- The user wants to classify a denial as actionable (appealable) vs. non-actionable

---

## Response Format

Structure each response in this order:

1. **Classification** — denial type + CARC/RARC code identified
2. **Determination** — MEETS / DOES NOT MEET with specific requirements mapped
3. **Posture** — OVERTURN / PEND / ADVISE / ACCEPT with rationale
4. **Draft** — the appeal letter (or a memo if posture is ADVISE)
5. **Checklist** — reviewer items (missing docs, bracketed citations to verify) + appeal deadline

- Omit background the user already knows — they asked the question
- Target: 300–500 words for analysis; include the full letter or memo when requested

The decision trees and appeal frameworks in this skill are for internal reasoning only.
Apply them to reach your conclusion but do not reproduce them verbatim in your response.
Present only the final classification, posture, and letter — never narrate the tree traversal.

---

## Guardrails

- **No fabrication** — if a fact is not in the user-supplied input, flag it as `[needed from reviewer]`; never invent clinical dates, policy numbers, or procedure details
- **Human-in-the-loop** — never auto-submit; always present the draft for explicit reviewer approval
- **PHI** — echo only the patient identifiers the letter requires; do not expand or infer beyond what was provided
- **Honest posture** — never manufacture arguments to avoid ADVISE; an overconfident appeal that misrepresents the record creates compliance risk

---

## Core Procedure

### Step 1 — Validate Inputs

Extract the following from the denial text. For any required field that cannot be found, ask the user before proceeding — do not guess or leave bracketed:

| Field | Source | Required? |
|---|---|---|
| Denial date | EOB / denial letter | Yes — needed to calculate appeal deadline |
| CARC / reason code | EOB | Yes — drives the entire appeal strategy |
| Payer name | EOB / letter header | Yes |
| Claim number | EOB | Yes |
| Member ID | EOB | Yes |
| Date of service | EOB / claim | Yes |
| CPT code(s) | EOB / claim | Yes |
| Payer's stated rationale | Denial letter verbatim | Yes |
| Patient name | EOB / letter | Preferred — skip if unavailable |
| ICD-10 diagnosis code(s) | EOB / claim | Preferred — skip if unavailable |

If more than two required fields are missing, ask for them all in one message rather than drip-asking. If extraction confidence is low (key fields ambiguous), warn the user before proceeding.

### Step 2 — Classify the Denial Category

Map the CARC (Claim Adjustment Reason Code) to one of five denial categories:

| Category | Typical CARC Codes | Root Cause |
|---|---|---|
| Medical necessity | CO-50, CO-56, CO-57 | Service not deemed necessary per payer criteria |
| Authorization / referral | CO-4, CO-15, CO-197 | Missing, expired, or wrong-provider authorization |
| Benefit exclusion | CO-96, PR-204 | Service not covered under the patient's plan |
| Timely filing | CO-29 | Claim submitted outside the payer's filing window |
| Documentation / coding error | CO-16, CO-252, CO-4, CO-11 | Missing info, wrong code, or incomplete submission |

Read the RARC (Remark Code) alongside the CARC for the specific gap.

### Step 3 — Determine Appeal Posture

```
Is the denial category "benefit exclusion" (CO-96, PR-204)?
├─ YES
│   ├─ Is the service actually covered under a different benefit category?
│   │   ├─ YES → OVERTURN — argue misclassification
│   │   └─ NO → ACCEPT (or advise plan change / patient financial counseling)
└─ NO
    ├─ Medical necessity (CO-50, CO-56)?
    │   ├─ Red flag present (cauda equina, progressive neuro deficit, malignancy)?
    │   │   └─ YES → OVERTURN immediately; flag as urgent
    │   ├─ Does clinical documentation meet the payer's published criteria?
    │   │   ├─ YES, and records were not submitted → PEND (gather and resubmit)
    │   │   ├─ YES, and records were submitted → OVERTURN (documentation gap, not clinical gap)
    │   │   └─ NO → ADVISE (criteria not met; escalate to peer-to-peer or clinical review)
    ├─ Authorization (CO-4, CO-197)?
    │   ├─ Was auth obtained but submitted incorrectly? → PEND (correct and resubmit)
    │   ├─ Was auth never obtained? → ADVISE (retroactive auth rarely granted)
    │   └─ Was auth obtained for wrong provider / wrong service? → OVERTURN if payer error
    ├─ Timely filing (CO-29)?
    │   ├─ Was the claim submitted on time? → OVERTURN (provide proof of timely submission)
    │   └─ Was the claim late? → ACCEPT unless payer-side delay is documented
    └─ Documentation / coding (CO-16, CO-252)?
        ├─ Is the missing info available? → PEND (correct and resubmit or provide addendum)
        └─ Is the code wrong? → PEND (correct claim resubmission)
```

**Key thresholds:**
- Conservative therapy requirement: ≥6 weeks (most imaging policies)
- Appeal window (commercial): 60–180 days from denial date
- Appeal window (Medicare Advantage): 60 calendar days
- Expedited appeal decision (payer): 72 hours
- Payer decision deadline on standard appeal: 30 days from receipt
- If <14 days remain before appeal deadline: flag **URGENT**

**Posture definitions:**
- **OVERTURN** — strong case; draft full appeal letter. Only use when the clinical or administrative facts clearly support reversal. Do not default to OVERTURN for ambiguous cases — an overconfident appeal that misrepresents the record creates compliance risk.
- **PEND** — fixable gap; correct submission before appealing
- **ADVISE** — weak or non-appealable case; explain options to the reviewer. When posture is ADVISE, state the realistic probability of success and the specific reason the case is weak. Never manufacture arguments to avoid ADVISE.
- **ACCEPT** — denial is correct; no appeal warranted

### Step 4 — Check Appeal Deadlines

| Payer Type | Standard Appeal Window | Expedited Window |
|---|---|---|
| Commercial (typical) | 180 days from denial date | 72 hours if urgent |
| Medicare Part A/B | 120 days (redetermination) | 72 hours (expedited) |
| Medicare Advantage (Part C) | 60 days (organization determination) | 72 hours |
| Medicaid (varies by state) | 30–90 days | 24–72 hours |

If fewer than 14 days remain before the deadline, flag as **URGENT** at the top of the response.

### Step 5 — Draft the Appeal Letter

Use this structure for all OVERTURN posture letters:

```
[Provider Name and NPI]
[Provider Address]
[Date]

[Payer Name]
[Appeals Department Address]

RE: Appeal of Claim Denial
Patient: [Patient Name] | DOB: [Date of Birth] | Member ID: [ID]
Claim #: [Claim Number] | Date of Service: [DOS] | CPT: [Code(s)]
Denial Reason: [CARC Code] — [Description] | RARC: [Code if applicable]

Dear Appeals Coordinator,

[Provider Name] is submitting this formal appeal of the denial issued on [denial date]
for [service description]. The denial was issued under [CARC code]: [denial rationale
quoted verbatim from remittance].

[PARAGRAPH 1 — Refute the denial rationale directly. Cite specific clinical findings,
dates, and documentation that address the payer's stated reason for denial. Quote the
payer's own published criteria (policy number, version, and page) where available.]

[PARAGRAPH 2 — Summarize the supporting documentation attached. List each attachment
explicitly: e.g., "Attached Exhibit A: office note dated [date] documenting [finding]."]

[PARAGRAPH 3 — State the requested action: reverse the denial and process for payment
at the contracted rate. Include the specific CPT code(s) and expected reimbursement
amount if known.]

Based on the foregoing, we respectfully request that [Payer Name] overturn this denial
and reprocess claim #[Claim Number] for payment. Please respond within [applicable
timeframe] as required under [cite applicable regulation, e.g., 45 CFR §147.136 for
commercial, or 42 CFR §422.568 for Medicare Advantage].

Sincerely,
[Authorized Signatory Name and Title]
[Contact Phone and Fax]

Attachments: [List all exhibits]
```

### Step 6 — Identify Supporting Documentation

| Denial Type | Key Documents to Attach |
|---|---|
| Medical necessity | Clinical notes, lab/imaging results, treatment history, published guidelines (NCCN, ACS, ACR) |
| Authorization | Auth approval confirmation, fax confirmation, payer auth number |
| Timely filing | Clearinghouse acceptance report, claims submission log with timestamp |
| Coding error | Corrected claim (CMS-1500 or 837P), coder attestation if applicable |
| Benefit exclusion | Plan summary of benefits, EOB showing prior payment for same service |

**Guideline citation discipline:** When citing society guidelines, name the exact organization and document (e.g., "American Academy of Dermatology — Appropriate Use Criteria for Mohs Surgery, 2023"). Never conflate multiple sources or attribute a position to an organization without confirming the specific document supports it. If you cannot verify the exact citation, bracket it as `[Verify: organization + document title + year]` rather than citing it as fact.

**Medicare LCD currency:** LCD criteria are revised periodically. Always flag: "Verify this LCD against the current version in the CMS Medicare Coverage Database before submitting — criteria may have changed since this analysis." Do not present LCD criteria as static facts.

---

## MCP Tool Integration (Optional Enhancement)

If a claims/835-ERA MCP tool is available in your environment, use it to pull the
remittance detail directly:

1. Call the tool with the claim number or member ID to retrieve the 835 ERA segment
2. Extract the CAS segment (CARC code), MOA segment (RARC code), and claim-level
   payment information
3. Use the retrieved values to populate the denial classification in Step 2

If no MCP tool is available, reason from the remittance information the user provides.

---

## When NOT to Use This Skill

- Clinical coverage determinations requiring a licensed physician — use `pa-clinical-policy`
- Billing compliance audits or FWA investigations — use `claims-billing-rules`

## When to Escalate to a Human Expert

- Denials involving experimental or investigational determinations requiring peer-to-peer
  review by the treating physician
- Potential payer bad-faith denials that may warrant state insurance department complaint
- Denials with legal exposure (e.g., ERISA external review, Medicaid fair hearing)

---

## Common Mistakes

- **Wrong:** Arguing medical necessity for a CO-96/PR-204 (benefit exclusion) denial.
  **Right:** CO-96 means the service is not a covered benefit — argue plan misclassification
  or guide the patient to a plan that covers it; medical necessity arguments are irrelevant.

- **Wrong:** Citing a payer policy number without verifying it is current.
  **Right:** Leave unverified policy numbers bracketed as `[Policy # — verify before sending]`
  and flag for the reviewer to confirm the current version.

- **Wrong:** Treating every "does not meet criteria" denial as unappealable.
  **Right:** Check whether the gap is a documentation gap (records exist but were not
  attached) vs. a clinical gap (criteria genuinely not met). A documentation gap is PEND or
  OVERTURN; a clinical gap is ADVISE.

- **Wrong:** Drafting a strong overturn letter when the clinical criteria are genuinely not met.
  **Right:** Use ADVISE posture — explain the weakness to the reviewer. Never manufacture
  arguments or misrepresent the clinical record to strengthen a weak appeal.

- **Wrong:** Ignoring the appeal filing deadline.
  **Right:** Always surface the deadline from the denial letter. If fewer than 14 days remain,
  flag the letter as URGENT and recommend submitting within 24–48 hours.

- **Wrong:** Using generic language such as "please reconsider this claim" without addressing
  the specific denial reason.
  **Right:** Quote the CARC code and the payer's stated rationale verbatim, then refute or
  address each point directly with clinical evidence or documentation.

- **Wrong:** Citing a society guideline without specifying the exact organization, document title, and year.
  **Right:** Name the precise source (e.g., "NCCN Clinical Practice Guidelines in Oncology — Non-Small Cell Lung Cancer, v3.2024"). If the exact document cannot be confirmed, bracket it as `[Verify: source + year]` rather than asserting it as fact.

- **Wrong:** Defaulting to OVERTURN when the clinical criteria are ambiguous or genuinely in doubt.
  **Right:** Assess honestly — if there is real uncertainty whether criteria are met, use ADVISE and state the realistic probability of overturn and the compliance risk of overstating the case.

- **Wrong:** Treating Medicare LCD criteria as static facts.
  **Right:** Always instruct the reviewer to verify the current LCD version in the CMS Medicare Coverage Database before submitting — criteria are revised periodically and an outdated citation undermines the appeal.

- **Wrong:** Fabricating clinical dates, procedure details, or policy citations not in the user-supplied input.
  **Right:** If a fact is not in the input, flag it as `[needed from reviewer]` — never invent supporting details to strengthen the letter.

- **Wrong:** Bundling multiple denial reasons into one vague appeal paragraph.
  **Right:** Address each CARC code separately with its own argument and supporting evidence — reviewers evaluate each denial reason independently.

---

## Quick Reference: CARC → Posture Map

| CARC | Description | Default Posture |
|---|---|---|
| CO-4 | Authorization required | PEND or OVERTURN (if auth exists) |
| CO-11 | Diagnosis inconsistent with procedure | PEND (correct claim) |
| CO-15 | Authorization number invalid | PEND (obtain correct auth number) |
| CO-16 | Claim lacks information | PEND (resubmit with missing info) |
| CO-29 | Timely filing expired | OVERTURN (if proof of timely filing exists) or ACCEPT |
| CO-50 | Non-covered / not medically necessary | OVERTURN or ADVISE |
| CO-56 | Not medically necessary | OVERTURN or ADVISE |
| CO-57 | Denied: not consistent with payer guidelines | OVERTURN or ADVISE |
| CO-96 | Non-covered charge | ACCEPT (or argue misclassification) |
| CO-97 | Bundled / included in another service | PEND (correct coding) |
| CO-197 | Precertification absent | PEND (retroactive auth) or ADVISE |
| CO-252 | Additional documentation requested | PEND (submit documentation) |
| PR-204 | Service not covered by plan | ACCEPT (patient financial counseling) |
