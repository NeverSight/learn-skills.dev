---
name: hack23-isms-compliance
description: Strategic skill for ensuring all Hack23 repositories comply with ISMS requirements (ISO 27001, NIST CSF 2.0, CIS Controls)
license: Apache-2.0
---

# Hack23 ISMS Compliance Skill

## Purpose

This skill ensures all code, documentation, and configurations comply with Hack23's Information Security Management System (ISMS) aligned with ISO 27001:2022, NIST CSF 2.0, and CIS Controls v8.1.

## Strategic Principles

### 1. Security by Design
- Security is integrated from the start, not added later
- Every design decision considers security implications
- Defense-in-depth is mandatory
- Least privilege is the default

### 2. Compliance as Code
- All compliance requirements are codified and automated
- Documentation is evidence
- Controls are verifiable through automation
- Audit readiness is continuous, not periodic

### 3. Transparency First
- Follow Hack23's public ISMS model
- Document all security decisions
- Make security architecture visible
- Share lessons learned

### 4. Risk-Based Approach
- Prioritize based on risk assessment
- Document risk acceptance decisions
- Continuously reassess threats
- Implement appropriate controls

## Required Documentation Portfolio

### Security Documentation (MANDATORY)

Every Hack23 repository MUST have:

\`\`\`
SECURITY_ARCHITECTURE.md    # Current security controls
THREAT_MODEL.md            # STRIDE analysis
FUTURE_SECURITY_ARCHITECTURE.md  # Security roadmap
\`\`\`

**SECURITY_ARCHITECTURE.md** must include:
- Defense-in-depth layers
- Compliance framework mapping (ISO 27001 + NIST CSF + CIS Controls)
- Authentication and authorization architecture
- Data protection mechanisms
- Network security topology
- Security monitoring approach
- Incident response procedures

**THREAT_MODEL.md** must include:
- STRIDE threat analysis for all components
- Attack surface identification
- Likelihood and impact ratings
- Mitigation strategies
- Residual risk documentation

**FUTURE_SECURITY_ARCHITECTURE.md** must include:
- Security enhancement roadmap
- Risk mitigation timelines
- Planned compliance improvements
- Technology evolution plans

### Architecture Documentation Portfolio (MANDATORY)

#### Current State
\`\`\`
ARCHITECTURE.md     # C4 models (Context, Container, Component)
DATA_MODEL.md       # Data structures and relationships
FLOWCHART.md        # Business processes and workflows
STATEDIAGRAM.md     # State transitions and lifecycles
MINDMAP.md          # Conceptual relationships
SWOT.md             # Strategic analysis
\`\`\`

#### Future State
\`\`\`
FUTURE_ARCHITECTURE.md      # Architectural evolution
FUTURE_DATA_MODEL.md        # Enhanced data architecture
FUTURE_FLOWCHART.md         # Improved workflows
FUTURE_STATEDIAGRAM.md      # Advanced state management
FUTURE_MINDMAP.md           # Capability expansion
FUTURE_SWOT.md              # Future opportunities
\`\`\`

## Compliance Framework Mapping

### ISO 27001:2022 Annex A Controls

Always map implementations to these controls:

| Control | Focus Area | Implementation Examples |
|---------|-----------|------------------------|
| **A.9.2** | User Access Management | MFA, SSH keys, GPG signing |
| **A.9.4** | System/App Access Control | RBAC, least privilege |
| **A.10.1** | Cryptographic Controls | TLS 1.3, HTTPS-only, encryption at rest |
| **A.12.4** | Logging and Monitoring | Audit logs, security monitoring |
| **A.13.1** | Network Security | Firewalls, DDoS protection, security headers |
| **A.14.2** | Secure Development | SAST, DAST, dependency scanning |
| **A.16.1** | Incident Management | Response procedures, forensics |

### NIST CSF 2.0 Functions

Map all security measures to functions:

| Function | Purpose | Key Categories |
|----------|---------|---------------|
| **GOVERN (GV)** | Organizational context | Risk management strategy, policies |
| **IDENTIFY (ID)** | Understand risks | Asset management, risk assessment |
| **PROTECT (PR)** | Implement safeguards | Access control, data security |
| **DETECT (DE)** | Find anomalies | Monitoring, threat detection |
| **RESPOND (RS)** | Take action | Response planning, communications |
| **RECOVER (RC)** | Restore services | Recovery planning, improvements |

### CIS Controls v8.1

Implement applicable controls by Implementation Group:

**IG1 (Basic Cyber Hygiene)**:
- 1.1: Inventory of Assets
- 2.1: Inventory of Software
- 3.10: Encrypt Data in Transit
- 4.1: Secure Configuration
- 5.1: Account Inventory
- 6.8: Role-Based Access Control

**IG2 (Enterprise Security)**:
- 8.2: Collect Audit Logs
- 10.1: Deploy Anti-Malware
- 13.1: Security Event Alerting
- 16.1: Secure Development Process

## DevSecOps Requirements

### CI/CD Security

All workflows must:
1. Use **step-security/harden-runner** for egress auditing
2. Implement **least privilege permissions**
3. Pin actions to **SHA commits** (not tags)
4. Scan dependencies with **Dependabot**
5. Run **CodeQL** or equivalent SAST
6. Enable **secret scanning**
7. Implement **quality gates** (fail on security issues)

Example:
\`\`\`yaml
permissions:
  contents: read  # Least privilege

steps:
  - name: Harden Runner
    uses: step-security/harden-runner@e3f713f2d8f53843e71c69a996d56f51aa9adfb9
    with:
      egress-policy: audit
\`\`\`

### Security Scanning

Required scans:
- **SAST**: CodeQL, Semgrep, or equivalent
- **Dependency**: Dependabot, Snyk, or equivalent
- **Secret**: GitHub secret scanning
- **DAST**: For web applications (planned/future)

### Access Control

- **MFA required** for all contributors
- **SSH keys** with passphrase protection
- **GPG signing** required for commits
- **Branch protection** on main/master
- **Required reviews** before merge

## Threat Modeling (STRIDE)

For every component, analyze:

| Threat | Description | Example Mitigations |
|--------|-------------|-------------------|
| **S**poofing | Identity theft | MFA, strong authentication |
| **T**ampering | Data modification | Input validation, integrity checks |
| **R**epudiation | Deny actions | Audit logs, digital signatures |
| **I**nformation Disclosure | Expose info | Encryption, access control |
| **D**enial of Service | Disrupt service | Rate limiting, DDoS protection |
| **E**levation of Privilege | Gain unauthorized access | Least privilege, RBAC |

## Compliance Verification Checklist

Before completing any task, verify:

- [ ] All required security documentation exists and is current
- [ ] All required architecture documentation exists and is current
- [ ] Security controls are mapped to ISO 27001/NIST CSF/CIS Controls
- [ ] Threat model is complete with STRIDE analysis
- [ ] CI/CD workflows are security-hardened
- [ ] Access controls follow least privilege
- [ ] All security findings are documented and addressed
- [ ] Compliance gaps are identified and tracked

## Audit Evidence

Maintain evidence for:
1. **Control implementation**: Configuration files, screenshots
2. **Control effectiveness**: Test results, monitoring logs
3. **Control coverage**: Mapping matrices, gap analysis
4. **Continuous monitoring**: Scan results, alerts
5. **Incident response**: Procedures, exercises, post-mortems

## Remember

- **If it's not documented, it doesn't exist** - Auditors need evidence
- **Compliance is continuous** - Not a one-time checkbox
- **Security by design** - Easier than retrofitting
- **Defense in depth** - Multiple layers of protection
- **Least privilege** - Minimize access by default
- **Transparency** - Follow Hack23's open security model

## References

### Hack23 ISMS Core Policies
- [Information Security Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Information_Security_Policy.md) - Master ISMS framework
- [Information Security Strategy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Information_Security_Strategy.md) - Strategic security roadmap
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md) - SDLC security requirements
- [Open Source Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Open_Source_Policy.md) - Open source governance
- [Threat Modeling Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Threat_Modeling.md) - Systematic threat analysis

### Compliance & Classification
- [Compliance Checklist](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Compliance_Checklist.md) - Multi-framework mapping
- [Classification Framework](https://github.com/Hack23/ISMS-PUBLIC/blob/main/CLASSIFICATION.md) - Business impact analysis
- [CRA Conformity Assessment](https://github.com/Hack23/ISMS-PUBLIC/blob/main/CRA_Conformity_Assessment_Process.md) - EU Cyber Resilience Act

### Risk & Incident Management
- [Risk Register](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Risk_Register.md) - Enterprise risk management
- [Risk Assessment Methodology](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Risk_Assessment_Methodology.md) - Risk evaluation framework
- [Incident Response Plan](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Incident_Response_Plan.md) - Security incident procedures
- [Business Continuity Plan](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Business_Continuity_Plan.md) - BCP/DR processes

### Technical Controls
- [Access Control Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Access_Control_Policy.md) - IAM and authentication
- [Cryptography Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Cryptography_Policy.md) - Encryption standards
- [Network Security Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Network_Security_Policy.md) - Network controls
- [Vulnerability Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Vulnerability_Management.md) - Vuln scanning and remediation
- [Backup Recovery Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Backup_Recovery_Policy.md) - Data protection
- [Change Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Change_Management.md) - Change control

### Supporting Documents
- [Asset Register](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Asset_Register.md) - Information assets
- [Data Classification Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Data_Classification_Policy.md) - Data handling
- [Acceptable Use Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Acceptable_Use_Policy.md) - Usage guidelines
- [Segregation of Duties Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Segregation_of_Duties_Policy.md) - SoD compensating controls
- [Third Party Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Third_Party_Management.md) - Supplier security
- [Physical Security Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Physical_Security_Policy.md) - Physical controls
- [AI Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/AI_Policy.md) - AI governance
- [Privacy Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Privacy_Policy.md) - GDPR compliance

### Example Implementations
- [CIA Security Architecture](https://github.com/Hack23/cia/blob/master/SECURITY_ARCHITECTURE.md) - Full authentication stack
- [CIA Threat Model](https://github.com/Hack23/cia/blob/master/THREAT_MODEL.md) - Comprehensive threat analysis
- [CIA Compliance Manager Security](https://github.com/Hack23/cia-compliance-manager/blob/main/docs/architecture/SECURITY_ARCHITECTURE.md) - Frontend-only security
- [Black Trigram Security](https://github.com/Hack23/blacktrigram/blob/main/SECURITY_ARCHITECTURE.md) - Gaming security
- [Riksdagsmonitor Security](https://github.com/Hack23/riksdagsmonitor/blob/main/SECURITY_ARCHITECTURE.md) - Static site security

### Compliance Frameworks
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Information security management
- [NIST CSF 2.0](https://www.nist.gov/cyberframework) - Cybersecurity Framework
- [CIS Controls v8.1](https://www.cisecurity.org/controls) - Security best practices
- [NIS2 Directive](https://eur-lex.europa.eu/eli/dir/2022/2555) - EU cybersecurity requirements
- [EU CRA](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act) - Cyber Resilience Act
- [GDPR](https://gdpr.eu/) - Data protection regulation
