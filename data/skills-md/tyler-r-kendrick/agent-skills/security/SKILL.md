---
name: security
description: |
    Use when addressing cross-cutting security concerns that apply to all languages, frameworks, and platforms. Covers OWASP standards, threat modeling, authentication, cryptography, supply chain security, and AI security.
    USE FOR: application security strategy, security architecture, choosing security controls, OWASP compliance, security tool selection, secure development lifecycle
    DO NOT USE FOR: specific language security implementations (use language-specific skills), infrastructure hardening (use iac skills), network security appliance configuration
license: MIT
metadata:
  displayName: "Security"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "OWASP Foundation"
    url: "https://owasp.org"
  - title: "NIST Cybersecurity Framework"
    url: "https://www.nist.gov/cyberframework"
  - title: "OWASP Top Ten Project"
    url: "https://owasp.org/www-project-top-ten/"
---

# Security

## Overview

Security is a cross-cutting concern that spans every layer of software development, from design through deployment and operations. Rather than being confined to a single language or framework, security principles such as defense in depth, least privilege, and secure defaults apply universally. This skill serves as the root entry point for all security-related guidance, organizing sub-skills around the major domains of application security: standards compliance (OWASP), threat modeling, authentication and authorization, cryptography, API security, input validation, data protection, supply chain integrity, security testing, logging and monitoring, secure SDLC practices, and the emerging field of AI security. Use this skill to navigate the security landscape and identify which specialized sub-skill addresses your specific concern.

## Knowledge Map

```
+-----------------------------------------------------------------------+
|                     Governance & Compliance                           |
|            (Secure SDLC, Policies, Standards, Regulations)            |
+-----------------------------------------------------------------------+
|                       Application Security                            |
|  +-------------+  +-----------+  +--------------+  +---------------+  |
|  +--------+  +--------+  +-----------+  +-----------+  +--------+     |
|  |  Auth   |  | Crypto |  |Input/Output|  |API Security|  |Hygiene |     |
|  |(AuthN/Z)|  |(TLS,HE)|  |(Validate) |  |(REST,GQL) |  |(Trust  |     |
|  +--------+  +--------+  +-----------+  +-----------+  |Boundaries)|  |
|                                                         +--------+     |
|  +---------------------+  +--------------------------------------+    |
|  |   Data Protection    |  |         Supply Chain Security        |    |
|  | (Encryption at Rest, |  | (Dependencies, SBOMs, Signing)      |    |
|  |  Masking, PII)       |  +--------------------------------------+    |
|  +---------------------+                                              |
+-----------------------------------------------------------------------+
|                          Foundation                                    |
|  +------------------+  +-------------------+  +--------------------+  |
|  +----------------+ +----------------+ +------------------+ +--------+  |
|  | Threat Modeling | | Security Tests | | Logging/Monitor  | | Pen    |  |
|  | (STRIDE,DREAD)  | | (SAST,DAST,SCA)| | (SIEM,Alerting)  | | Test & |  |
|  +----------------+ +----------------+ +------------------+ | Red    |  |
|                                                              | Team   |  |
|                                                              +--------+  |
+-----------------------------------------------------------------------+
|  <<cross-cutting>>         AI Security                                |
|  (Prompt Injection, Model Poisoning, LLM Top 10, AI Supply Chain)     |
+-----------------------------------------------------------------------+
```

## Canonical Works

| Title | Author(s) | Year | Focus |
|-------|-----------|------|-------|
| The Web Application Hacker's Handbook | Dafydd Stuttard & Marcus Pinto | 2011 | Web app vulnerability discovery and exploitation techniques |
| Penetration Testing | Georgia Weidman | 2014 | Hands-on penetration testing methodology and tools |
| Red Team Development and Operations | Joe Vest & James Tubberville | 2020 | Planning and executing red team engagements |
| Threat Modeling: Designing for Security | Adam Shostack | 2014 | Systematic approach to identifying and mitigating security threats |
| NIST Cybersecurity Framework 2.0 | NIST | 2024 | Risk-based framework for managing cybersecurity across organizations |
| OWASP Top 10 (2021) | OWASP Foundation | 2021 | Top 10 most critical web application security risks |
| OWASP API Security Top 10 (2023) | OWASP Foundation | 2023 | Top 10 most critical API security risks |
| OWASP Top 10 for LLM Applications (2025) | OWASP Foundation | 2025 | Top 10 security risks specific to large language model applications |

## Choosing the Right Sub-Skill

| Problem | Look In |
|---------|---------|
| Need to understand common web vulnerabilities and compliance baselines | `owasp` |
| Designing a system and need to identify threats early | `threat-modeling` |
| Implementing login, OAuth, SSO, or access control | `authentication` |
| Choosing or implementing encryption, hashing, or key management | `cryptography` |
| Securing REST or GraphQL APIs against abuse | `api-security` |
| Sanitizing user input or preventing injection attacks | `input-validation` |
| Enforcing sanitization and canonicalization at every component boundary (including internal data) | `hygiene` |
| Protecting PII, encrypting data at rest, or masking sensitive fields | `data-protection` |
| Auditing dependencies, generating SBOMs, or verifying artifact integrity | `supply-chain` |
| Running SAST, DAST, or SCA scans in CI/CD | `security-testing` |
| Setting up security logging, alerting, or incident detection | `logging-monitoring` |
| Embedding security gates into the development lifecycle | `secure-sdlc` |
| Securing LLM-powered applications against prompt injection or model abuse | `ai-security` |
| Planning or conducting authorized penetration tests against applications and infrastructure | `penetration-testing` |
| Adversarial red team engagements, MITRE ATT&CK simulation, purple teaming, AI red teaming | `red-teaming` |

## Best Practices

- **Defense in depth**: never rely on a single security control; layer multiple defenses so that a failure in one does not compromise the system.
- **Least privilege**: grant the minimum permissions necessary for any user, service, or process to perform its function.
- **Secure defaults**: ship systems in a secure configuration; require explicit action to weaken security posture rather than to strengthen it.
- **Shift left**: integrate security analysis (threat modeling, SAST, dependency scanning) as early as possible in the development lifecycle.
- **Zero trust mindset**: authenticate and authorize every request regardless of network location; assume the perimeter has already been breached.
- **Automate security gates**: use CI/CD pipelines to enforce security scanning, secret detection, and compliance checks before code reaches production.
- **Keep dependencies current**: regularly update libraries and frameworks, monitor for CVEs, and generate Software Bills of Materials (SBOMs) for auditability.
- **Treat security as a team responsibility**: security is not solely the security team's job; every developer, operator, and architect shares accountability for building and maintaining secure systems.
