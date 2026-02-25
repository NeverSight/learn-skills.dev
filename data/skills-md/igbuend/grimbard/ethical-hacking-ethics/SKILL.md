---
name: ethical-hacking-ethics
description: Legal and ethical guidelines for bug bounties, pentesting, and security research. Use when conducting authorized security testing.
aliases:
  - ethical-hacking
  - bug-bounty-ethics
  - pentest-ethics
---

# Ethical Hacking Ethics

Guidance for ethical hacking: bug bounties, pentesting, and security research.

## When to Use This Skill

- Participating in bug bounty programs (HackerOne, Bugcrowd, Intigriti, YesWeHack)
- Conducting authorized penetration testing
- Performing security research on your own systems
- Evaluating legality of security testing activities
- Creating vulnerability disclosure reports

## DO's - Always Do These

### 1. Obtain Explicit Authorization
- Get written permission before testing any system you don't own
- Verify scope - know exactly what assets are authorized
- Document authorization - keep records of written consent
- Check safe harbor status - confirm program has safe harbor policy

### 2. Follow Platform Rules of Engagement
- Read and understand program-specific rules before testing
- Adhere to testing timeframes specified by the program
- Use only authorized testing methods
- Report through official channels only
- **Human-in-the-loop required**: HackerOne requires human validation before submitting findings

### 3. Practice Good Faith Security Research
Access systems solely for good-faith testing, avoid harm to individuals/public, use findings to improve security.

### 4. Document Everything
- Keep detailed logs of all testing activities
- Capture evidence of vulnerabilities for reports
- Record timeline of discovery and reporting
- Document all communication with program owners

### 5. Practice Responsible Disclosure
- Report vulnerabilities promptly through official channels
- Allow reasonable time for remediation before disclosure
- Coordinate disclosure with affected organization
- Follow platform-specific disclosure guidelines

### 6. Respect Data Privacy
- Minimize data access to only what's necessary for testing
- Don't store or share personal data discovered during testing
- Report data exposure vulnerabilities without exploiting them
- Follow GDPR and local data protection laws

## DON'Ts - Never Do These

### 1. Never Test Without Authorization
- Never access systems without explicit permission
- Don't assume permission - verify scope explicitly
- Never test "out of scope" assets even if you find them
- Don't exceed authorized access - stay within defined boundaries

**Legal risk**: CFAA (US) and CMA 1990 (UK) prohibit unauthorized access. Penalties include imprisonment.

### 2. Never Cause Harm
- Don't modify or destroy data during testing
- Never create backdoors or permanent access mechanisms
- Don't disrupt services or availability
- Never exfiltrate data beyond what's necessary for proof

### 3. Never Blackmail or Extort
- Never threaten to publish vulnerabilities for payment
- Don't use vulnerabilities for extortion
- Never demand bounties as condition for not publishing
- **Result**: Permanent platform ban + potential criminal charges

### 4. Never Disclose Prematurely
- Don't publish vulnerability details before remediation
- Never share findings with third parties without permission
- Don't post proof-of-concept code publicly without coordination
- Never disclose program existence for private programs

### 5. Never Use Deceptive Practices
- Don't impersonate authorized security researchers
- Never falsify vulnerability reports or evidence
- Don't misrepresent your identity or affiliation
- Never submit false reports for rewards

### 6. Never Violate Privacy Laws
- Don't access personal data beyond testing scope
- Never store or share PII discovered during testing
- Don't bypass privacy controls beyond what's necessary
- Follow GDPR/data protection requirements

## Scope Verification Checklist

Before beginning any testing, verify:

- [ ] **Authorization Document**: Written permission to test?
- [ ] **In-Scope Assets**: All authorized targets identified?
- [ ] **Out-of-Scope Assets**: Know what's explicitly prohibited?
- [ ] **Testing Methods**: Required or prohibited techniques?
- [ ] **Time Restrictions**: Designated testing windows?
- [ ] **Safe Harbor**: Program has and honors safe harbor policies?
- [ ] **Reporting Channel**: Know official vulnerability submission process?
- [ ] **Disclosure Policy**: Understand when/how you can publish findings?

## Authorization Types

| Type | Authorization | Safe Harbor | Notes |
|------|--------------|-------------|-------|
| **Bug Bounty** | Implicit via program | If offered | Follow program rules |
| **Pentest** | Written contract/SOW | Per contract | May require NDA |
| **VDP** | Program invitation | Varies | Usually no rewards |
| **CTF** | Competition rules | Within boundaries | Legal only in competition |

### Authorization Best Practices

- Always get it in writing - verbal authorization is insufficient
- Define scope explicitly - "everything except X" is too vague
- Specify time boundaries - testing windows and deadlines
- Include escalation procedures - what to do if issues arise

## Responsible Disclosure Process

1. **Validate** - Reproduce issue, document PoC, assess severity, check for duplicates
2. **Submit** - Use official channels, include description + steps + impact + remediation
3. **Coordinate** - Allow validation time, respond to questions, agree on timeline
4. **Verify** - Confirm fix applied, test that vulnerability is remediated
5. **Disclose** - Per agreed terms (coordinated, limited, full, or non-disclosure)

## Red Lines - Violation Severity

| Severity | Violations | Consequence |
|----------|-----------|-------------|
| **Critical** | Unauthorized access, data theft, service disruption, extortion, social engineering, physical breach | Permanent ban + legal action |
| **Severe** | Premature disclosure, prohibited techniques, third-party sharing, withholding details | Warnings + potential ban |
| **Minor** | Unintentional scope violation, incomplete reports, format issues | Education + warning |

## When to Stop and Escalate

### Stop Immediately If:

| Situation | Action |
|-----------|--------|
| Outside scope | Halt, document, report, await guidance |
| Sensitive data exposure | Stop exploration, don't download, report immediately |
| Service disruption (or near) | Stop, document, report, await instructions |
| Asked to stop | Cease all activities, get written confirmation |

### Escalate When:

- **Legal questions** - Consult legal counsel
- **Disputes** - Request platform mediation
- **Unresponsive programs** - Follow platform escalation procedures
- **Criminal activity discovered** - Report to authorities
- **Safety concerns** - Escalate if human safety at risk

## Legal Framework Summary

| Jurisdiction | Law | Key Points |
|-------------|-----|------------|
| **US** | CFAA (18 U.S.C. § 1030) | Prohibits unauthorized access. Van Buren (2021) narrowed scope. |
| **UK** | CMA 1990 | No "good faith" defense. Section 1: up to 2 years. No safe harbor equivalent. |
| **EU** | GDPR | Legal basis required for data. Report breaches within 72 hours. |

**Other jurisdictions**: Canada, Australia, Germany, France, Japan have similar laws. Research local laws before international testing.

**References**: [CFAA](https://www.law.cornell.edu/uscode/text/18/1030) | [CMA](https://www.cps.gov.uk/prosecution-guidance/computer-misuse-act) | [GDPR](https://gdpr.eu/)

## Standards Compliance

| Standard | Use Case | Reference |
|----------|----------|-----------|
| **PTES** | General pentesting (7 stages) | [pentest-standard.org](http://www.pentest-standard.org/) |
| **OWASP WSTG** | Web application testing | [owasp.org/wstg](https://owasp.org/www-project-web-security-testing-guide/) |
| **NIST SP 800-115** | Government/compliance testing | [csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/115/final) |
| **OSSTMM** | Metrics-based security testing | [isecom.org](https://www.isecom.org/) |

## Platform Quick Reference

| Platform | Safe Harbor | Disclosure | Key Requirement |
|----------|-------------|------------|-----------------|
| **HackerOne** | Gold Standard (GSSH) | Program-specific | Human-in-the-loop validation |
| **Bugcrowd** | Disclose.io framework | Coordinated/Custom/Non | Secure POC sharing |
| **Intigriti** | Varies | Coordinated | GDPR compliance |
| **YesWeHack** | Varies | Program-specific | Follow program brief |

**Platform Docs**: [HackerOne](https://docs.hackerone.com/) | [Bugcrowd](https://docs.bugcrowd.com/) | [Intigriti](https://www.intigriti.com/) | [YesWeHack](https://www.yeswehack.com/)

## Certifications Reference

| Certification | Focus | Ethics Requirement |
|--------------|-------|-------------------|
| **OSCP** | Practical exploitation | Legal boundaries, documentation |
| **CEH** | Theory + practical | Code of ethics required |
| **GPEN** | Advanced pentesting | Legal/ethical training |
| **CREST/CHECK** | UK government schemes | Background checks, conduct codes |
| **PCI-DSS** | Cardholder data environments | Qualified assessor, documentation |

## References

**Platforms**: [HackerOne Docs](https://docs.hackerone.com/) | [Bugcrowd Docs](https://docs.bugcrowd.com/researchers/) | [Disclose.io](https://disclose.io/)

**Standards**: [PTES](http://www.pentest-standard.org/) | [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/) | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)

**Legal**: [CFAA](https://www.law.cornell.edu/uscode/text/18/1030) | [CMA 1990](https://www.cps.gov.uk/prosecution-guidance/computer-misuse-act)

For detailed reference material, see the `references/` directory.
