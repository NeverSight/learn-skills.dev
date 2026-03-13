---
name: contract-reviewer
description: >
  Review business contracts for risks, missing clauses, unfavorable terms, and compliance gaps.
  Use when analyzing NDAs, MSAs, SaaS agreements, vendor contracts, SOWs, or employment agreements.
  Generates a structured risk report with recommendations. Built by AfrexAI.
metadata:
  version: 1.0.0
  author: AfrexAI
  tags: [legal, contracts, risk, compliance, business]
---

# Contract Reviewer

Review any business contract for risks, gaps, and unfavorable terms. Outputs a structured risk report.

## When to Use

- Reviewing NDAs, MSAs, SaaS agreements, vendor contracts, SOWs
- Pre-signature risk assessment
- Comparing contract terms against industry standards
- Identifying missing protective clauses
- Compliance gap analysis (GDPR, SOC 2, HIPAA references)

## How to Use

1. User provides contract text (paste, file, or URL)
2. Agent analyzes against the framework below
3. Outputs structured risk report

## Analysis Framework

### 1. Contract Metadata
Extract and confirm:
- **Parties**: Who is bound? Are entities correctly named?
- **Effective date & term**: Start, duration, auto-renewal?
- **Governing law & jurisdiction**: Which state/country?
- **Contract type**: NDA / MSA / SaaS / SOW / Employment / Vendor / Other

### 2. Financial Terms Review
Flag issues with:
- **Payment terms**: Net 30/60/90? Late payment penalties?
- **Price escalation**: Annual increases capped? CPI-linked?
- **Hidden fees**: Setup, overage, early termination, minimum commitments
- **Currency & tax**: Who bears tax obligations?

### 3. Risk Clauses (RED FLAGS)
Score each 🔴 High / 🟡 Medium / 🟢 Low:

| Clause | What to Check |
|--------|--------------|
| **Limitation of liability** | Is it capped? Mutual? Carve-outs for IP/data? |
| **Indemnification** | One-sided or mutual? Uncapped exposure? |
| **Termination** | Can either party terminate for convenience? Notice period? |
| **Auto-renewal** | Silent renewal? Opt-out window too short? |
| **IP ownership** | Who owns work product? License-back provisions? |
| **Data handling** | DPA included? Breach notification timeline? Data return/deletion? |
| **Non-compete / non-solicit** | Scope, duration, geography reasonable? |
| **Force majeure** | Included? Pandemic/cyber covered? |
| **Assignment** | Can they assign without consent? Change of control? |
| **Warranty disclaimers** | "As-is" without recourse? SLA commitments? |
| **Confidentiality** | Mutual? Duration? Carve-outs? Survival period? |
| **Dispute resolution** | Arbitration vs litigation? Venue favorable? |

### 4. Missing Clauses Check
Flag if absent:
- [ ] Data Processing Agreement (if personal data involved)
- [ ] SLA with uptime commitments and credits
- [ ] Insurance requirements
- [ ] Audit rights
- [ ] Subcontractor approval rights
- [ ] Escrow provisions (for critical software)
- [ ] Business continuity / disaster recovery obligations
- [ ] Right to terminate for cause (material breach + cure period)

### 5. Plain Language Issues
- Ambiguous terms ("reasonable efforts" without definition)
- Undefined capitalized terms
- Conflicting clauses (e.g., termination vs auto-renewal)
- Missing exhibits or schedules referenced but not attached

## Output Format

```markdown
# Contract Review Report

## Summary
- **Contract**: [type] between [Party A] and [Party B]
- **Overall Risk Level**: 🔴/🟡/🟢
- **Top 3 Concerns**: [bullet list]
- **Recommendation**: Sign / Negotiate / Walk Away

## Detailed Findings

### 🔴 High Risk
[numbered list with clause reference, issue, recommendation]

### 🟡 Medium Risk
[numbered list with clause reference, issue, recommendation]

### 🟢 Low Risk / Acceptable
[numbered list noting well-drafted provisions]

## Missing Clauses
[checklist of what should be added]

## Suggested Redlines
[specific language changes recommended, with before/after]

## Next Steps
1. [prioritized action items]
```

## Important Notes

- This is an **AI-assisted review**, not legal advice
- Always have a qualified attorney review before signing
- Flag jurisdiction-specific requirements the model may miss
- For regulated industries (healthcare, finance), additional compliance review needed

## AfrexAI

Built by [AfrexAI](https://afrexai-cto.github.io/aaas/landing.html) — AI agents for business operations.
Need a full-time AI legal operations agent? We deploy managed AI agents starting at $1,500/month.
