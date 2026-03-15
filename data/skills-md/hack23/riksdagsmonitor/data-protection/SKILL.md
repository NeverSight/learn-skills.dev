---
name: data-protection
description: Data protection, privacy-by-design, GDPR compliance, data classification, and secure data handling practices
license: Apache-2.0
---

# Data Protection Skill

## Purpose
Defines data protection practices ensuring privacy-by-design, GDPR compliance, and secure data handling across all Hack23 projects.

## Data Classification Levels
| Level | Description | Handling |
|-------|-------------|----------|
| PUBLIC | Open data, published information | No restrictions |
| INTERNAL | Operational data, system metadata | Access controlled |
| CONFIDENTIAL | Personal data, business sensitive | Encrypted, logged |
| RESTRICTED | Credentials, keys, PII aggregation | Encrypted, MFA required |

## Privacy-by-Design Principles
1. **Proactive** — Prevent privacy issues before they occur
2. **Default** — Maximum privacy as default setting
3. **Embedded** — Privacy built into design
4. **Positive-Sum** — Privacy AND functionality
5. **End-to-End** — Full lifecycle protection
6. **Transparency** — Open and documented
7. **User-Centric** — Respect user privacy

## GDPR Requirements
- Lawful basis for processing
- Data minimization (collect only what's needed)
- Purpose limitation
- Storage limitation (retention policies)
- Data subject rights (access, deletion, portability)
- Privacy impact assessments for new features

## Static Site Considerations
- No cookies without consent
- Privacy-preserving analytics only
- No tracking pixels or fingerprinting
- Secure external links (rel="noopener noreferrer")
- No PII in URLs or query parameters

## ISO 27001 Mapping
- A.5.34 — Privacy and protection of PII
- A.8.11 — Data masking
- A.8.12 — Data leakage prevention

## Related Policies
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
