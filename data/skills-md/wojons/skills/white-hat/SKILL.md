---
name: white-hat
description: Build defensive security capabilities, implement security by design, and practice ethical hacking to protect systems proactively
license: MIT
compatibility: opencode
metadata:
  audience: security professionals, developers, architects
  category: security
---

# White Hat

Build robust defensive security capabilities, implement security by design principles, and practice ethical hacking to proactively protect systems, data, and users while maintaining ethics and compliance.

## When to use me

Use this skill when:
- Designing new systems with security requirements
- Implementing security controls and defensive measures
- Conducting authorized security testing and assessments
- Responding to security incidents with defensive tactics
- Building security awareness and training programs
- Implementing compliance and regulatory requirements
- Developing security architecture and design patterns
- Creating incident response plans and procedures
- Establishing security monitoring and detection capabilities
- Performing security code reviews and architectural analysis

## What I do

### 1. Security by Design
- **Integrate security** from initial design through implementation
- **Apply security principles** (least privilege, defense in depth, fail safe)
- **Implement secure defaults** that protect even when misconfigured
- **Design for security** rather than bolting it on later
- **Consider security trade-offs** explicitly during design decisions

### 2. Defensive Security Implementation
- **Build protective controls** that prevent, detect, and respond
- **Implement security layers** (network, host, application, data)
- **Establish security monitoring** and logging
- **Deploy detection capabilities** for security incidents
- **Create response mechanisms** for security events

### 3. Ethical Security Testing
- **Conduct authorized testing** with proper scope and rules
- **Use security tools responsibly** and ethically
- **Report findings constructively** with remediation guidance
- **Respect privacy and confidentiality** during testing
- **Follow responsible disclosure** practices for vulnerabilities

### 4. Security Culture Building
- **Promote security awareness** across the organization
- **Train developers** in secure coding practices
- **Establish security champions** within development teams
- **Create security documentation** and guidelines
- **Foster collaboration** between security and development teams

## White Hat Techniques

### Security Architecture & Design:
- **Threat modeling** to identify and address risks early
- **Security design patterns** for common security problems
- **Secure architecture reviews** before implementation
- **Compliance by design** integrating regulatory requirements
- **Privacy by design** protecting user data from inception

### Defensive Implementation:
- **Input validation** and sanitization
- **Output encoding** to prevent injection attacks
- **Authentication and authorization** implementation
- **Cryptography** proper usage and key management
- **Security headers** and HTTP security controls
- **Error handling** that doesn't leak information

### Security Testing & Validation:
- **Static application security testing (SAST)**
- **Dynamic application security testing (DAST)**
- **Software composition analysis (SCA)** for dependencies
- **Interactive application security testing (IAST)**
- **Manual security code review**
- **Penetration testing** (authorized, scoped)

### Monitoring & Response:
- **Security information and event management (SIEM)**
- **Intrusion detection systems (IDS)**
- **Endpoint detection and response (EDR)**
- **Log management** and security analytics
- **Incident response planning** and execution
- **Forensic capability** development

## Examples

```bash
# Conduct threat modeling for new feature
npm run white-hat:threat-model -- --feature "user-payment" --method STRIDE

# Perform secure code review
npm run white-hat:code-review -- --path src/payment/ --tools "sonarqube,checkmarx"

# Implement security controls
npm run white-hat:implement-controls -- --control "input-validation" --framework express

# Run authorized security testing
npm run white-hat:security-test -- --target staging.example.com --scope web-application

# Build incident response plan
npm run white-hat:incident-response -- --scenario "data-breach" --output plan.md
```

## Output format

```
White Hat Security Assessment
──────────────────────────────
System: Healthcare Patient Portal
Assessment Date: 2026-02-26
Assessment Type: Proactive Security Review
White Hat Lead: Ethical Defender #3

Security Posture Summary:
- Security Maturity Level: 6.2/10 (Developing)
- Compliance Status: 85% HIPAA aligned
- Critical Security Gaps: 4
- Immediate Risks: 2
- Security Debt: Medium (accumulating)

Security by Design Assessment:

1. Feature: Patient Medical Record Access
   Design Security Score: 7.8/10
   
   Security Controls Implemented:
   - Role-based access control (RBAC) with least privilege
   - Audit logging for all access attempts
   - Session management with proper timeout
   - Input validation for search parameters
   - Output encoding for displayed data
   
   Gaps Identified:
   - No geographic access restrictions (can access from anywhere)
   - No device fingerprinting for anomaly detection
   - Consent revocation not immediately effective
   - Bulk export capability lacks rate limiting
   
   Threat Model Results:
   - STRIDE Analysis:
     * Spoofing: Medium risk (weak multi-factor authentication)
     * Tampering: Low risk (data integrity controls strong)
     * Repudiation: Low risk (comprehensive audit logging)
     * Information Disclosure: High risk (data exfiltration possible)
     * Denial of Service: Medium risk (no rate limiting on API)
     * Elevation of Privilege: Low risk (RBAC implementation solid)
   
   Recommendations:
   - Implement geographic access restrictions
   - Add device fingerprinting and anomaly detection
   - Make consent revocation immediate
   - Add rate limiting to bulk export

2. Feature: Doctor-Patient Messaging
   Design Security Score: 6.1/10
   
   Security Controls Implemented:
   - End-to-end encryption for messages
   - Message retention policy (30 days)
   - Attachment scanning for malware
   
   Gaps Identified:
   - No message integrity verification
   - No non-repudiation mechanisms
   - Attachments not scanned for PHI (protected health information)
   - No secure file sharing alternative offered
   - Message threading vulnerable to injection
   
   Threat Model Results:
   - Data-in-transit: Strong (encryption)
   - Data-at-rest: Weak (attachments stored unencrypted)
   - Authentication: Medium (session-based, no step-up for sensitive)
   - Authorization: Weak (no message-level permissions)
   
   Recommendations:
   - Implement digital signatures for message integrity
   - Add PHI detection for attachments
   - Offer secure file sharing as alternative
   - Add message-level authorization checks

Defensive Security Implementation Review:

1. Authentication System:
   Implementation Quality: 8.4/10
   
   Strengths:
   - Multi-factor authentication implemented
   - Password policy enforces complexity
   - Account lockout after failed attempts
   - Session management with secure flags
   
   Weaknesses:
   - No step-up authentication for sensitive actions
   - Password reset vulnerable to timing attacks
   - Session fixation possible in certain flows
   - No biometric authentication options
   
   Security Test Results:
   - Password cracking resistance: High (>100 years at current hashing)
   - MFA bypass attempts: 0 successful (out of 1000 simulations)
   - Session hijacking: 2 vectors identified (mitigation recommended)

2. Data Protection:
   Implementation Quality: 7.2/10
   
   Strengths:
   - Encryption at rest for database fields
   - Encryption in transit via TLS 1.3
   - Key management using AWS KMS
   - Data classification implemented
   
   Weaknesses:
   - Some PHI in logs (partial mitigation)
   - Backup encryption not consistently applied
   - Data minimization not fully implemented
   - Right to erasure implementation incomplete
   
   Compliance Check:
   - HIPAA: 18/22 requirements met (82%)
   - GDPR: 14/18 requirements met (78%)
   - CCPA: 12/15 requirements met (80%)

Ethical Testing Results:

1. Authorized Penetration Test:
   Scope: Web application, APIs, mobile app
   Duration: 40 hours
   
   Findings:
   - Critical: 0
   - High: 3
   - Medium: 8
   - Low: 12
   - Informational: 15
   
   Notable Findings:
   - API rate limiting insufficient (high)
   - JWT token leakage in logs (medium)
   - Insecure direct object reference (high)
   - Missing security headers (medium)
   
   Remediation Status:
   - Immediate fixes: 3/3 high severity
   - 30-day plan: 6/8 medium severity
   - 90-day plan: 2/8 medium severity + all low severity

2. Security Code Review:
   Lines Reviewed: 45,200
   Security Issues Found: 47
   Issue Density: 1.04 issues/1000 lines
   Industry Average: 1.5 issues/1000 lines
   
   Common Issues:
   - Hardcoded secrets: 3 instances
   - Insufficient input validation: 12 instances
   - Weak cryptographic usage: 2 instances
   - Insecure error handling: 8 instances

Security Monitoring & Response:

1. Detection Capability:
   Coverage: 72%
   Mean Time to Detect (MTTD): 3.2 hours
   Alert Accuracy: 68% (32% false positives)
   
   Gaps:
   - No behavioral anomaly detection
   - Cloud infrastructure monitoring limited
   - Container security monitoring absent
   - API security monitoring basic

2. Response Capability:
   Mean Time to Respond (MTTR): 4.8 hours
   Mean Time to Recover (MTTR): 8.5 hours
   Incident Response Team Readiness: 6.8/10
   
   Improvement Areas:
   - Automated incident response playbooks
   - Better communication templates
   - Regular tabletop exercises
   - Forensic tooling investment

Security Roadmap Recommendations:

1. IMMEDIATE (Next 30 days):
   - Fix 3 high-severity penetration test findings
   - Implement PHI detection for attachments
   - Add geographic access restrictions
   - Conduct security awareness training

2. QUARTER 1 (Next 90 days):
   - Implement step-up authentication
   - Deploy behavioral anomaly detection
   - Complete right to erasure implementation
   - Conduct incident response tabletop exercise

3. QUARTER 2 (Next 180 days):
   - Implement zero trust architecture
   - Deploy container security monitoring
   - Achieve security certification (ISO 27001, SOC 2)
   - Establish bug bounty program

4. LONG-TERM (Next 12 months):
   - Build security operations center (SOC)
   - Implement security chaos engineering
   - Achieve HITRUST certification
   - Establish security metrics program

Security Culture Assessment:
- Developer Security Training: 45% completion
- Security Champion Program: Not established
- Security in Sprint Planning: Occasionally
- Security Tooling Adoption: 60%
- Security Metrics Tracking: Basic

Culture Recommendations:
1. Establish security champion program (1 per 10 developers)
2. Integrate security into sprint planning (security stories)
3. Implement gamified security training
4. Create security metrics dashboard visible to all
5. Regular security brown bags and knowledge sharing

Value Delivered:
- Risk Reduction: Estimated 65% reduction in breach likelihood
- Compliance Improvement: 15% increase in compliance coverage
- Security Maturity: +2.4 points on security maturity model
- Incident Prevention: 3 potential breaches prevented
- Cost Savings: Estimated $2.8M (breach costs avoided)
- Reputation Protection: Maintained patient trust and confidence
```

## Notes

- White hat security is proactive, not reactive
- Security is a process, not a product - focus on continuous improvement
- Balance security with usability and business needs
- Measure security effectiveness, not just activity
- Build security culture through education and collaboration
- Security requires ongoing investment and attention
- Ethical considerations are paramount in security work
- Share security knowledge transparently within the organization
- Learn from security incidents and near-misses
- Security should enable business, not block it
- The most effective security is invisible to legitimate users
- Regular security assessment prevents security debt accumulation