---
name: soc2-readiness
description: Prepare an organization for a SOC 2 Type I or II audit — trust services criteria mapping, evidence collection, control implementation, and remediation planning. Use when starting a SOC 2 journey or preparing for an audit window.
---

# SOC 2 Readiness

Drive an organization from "no controls documented" to audit-ready.

## 1. Scoping

- Determine report type: Type I (point-in-time) vs Type II (period of time — start the observation window early)
- Define the system description: services in scope, infrastructure, boundaries (subprocessors, cloud providers)
- Select Trust Services Criteria: Security (required) + Availability, Confidentiality, Processing Integrity, Privacy as applicable

## 2. Gap Assessment

Map current practices to the criteria:

| Area | Typical Criteria | Common Gaps |
|---|---|---|
| Access control | CC6.1–CC6.3 | No MFA, no role-based access, shared accounts |
| Change management | CC8.1 | No peer review on deploys, no environment separation |
| Risk assessment | CC3.1–CC3.4 | No annual risk assessment or vendor reviews |
| Monitoring | CC7.1–CC7.3 | No log review, no alerting on anomalies |
| Incident response | CC7.4–CC7.5 | No IR plan or tabletop evidence |
| BC/DR | A1.2–A1.3 | Untested backups, no documented RTO/RPO |
| Vendor management | CC9.2 | No subprocessor due diligence |
| Onboarding/offboarding | CC6.1 | Access removal not timely or evidenced |

## 3. Remediation

- Prioritize by audit-blocker status first, then risk
- Implement policy + practice + evidence together: a policy without execution evidence fails
- Typical timeline: 2–4 months for a Type I; Type II needs 2–12 months of operating evidence

## 4. Evidence Package

Per control: policy documents, implementation artifacts (screenshots, configs), and dated operating evidence over the review period (access reviews, change tickets, training logs, IR exercises)

## 5. Audit Logistics

- Choose auditor; confirm scope wording matches your system description
- Readiness assessment (optional but useful) → fieldwork → draft report review
- Track findings/exceptions honestly; management responses documented

## Output

Gap register with owners and dates, control matrix mapped to criteria, evidence repository structure, and auditor-ready system description.
