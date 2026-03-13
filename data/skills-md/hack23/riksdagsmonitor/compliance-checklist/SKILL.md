---
name: compliance-checklist
description: Unified compliance mapping across ISO 27001:2022, NIST CSF 2.0, CIS Controls v8.1, NIS2, EU CRA, GDPR, SOC 2, PCI DSS, HIPAA
license: Apache-2.0
---

# Compliance Checklist Skill

## Purpose

This skill provides comprehensive guidance for multi-framework compliance alignment, demonstrating how a single set of ISMS controls can satisfy multiple international frameworks and regulatory requirements simultaneously.

## Strategic Principles

### 1. Unified Compliance Framework
- **Single Control Set**: One ISMS architecture satisfies multiple frameworks
- **Evidence-Based Mapping**: Traceable controls to requirements
- **Continuous Compliance**: Not one-time certification
- **Transparency**: Public ISMS demonstrates capability

### 2. Framework Coverage

| Framework | Purpose | Key Focus |
|-----------|---------|-----------|
| **ISO 27001:2022** | Control backbone (Annex A) | Organizational, people, physical, technological controls |
| **NIST CSF 2.0** | Risk-based framework | 6 functions (Govern, Identify, Protect, Detect, Respond, Recover) |
| **CIS Controls v8.1** | Operational security | Implementation Groups (IG1, IG2, IG3) |
| **NIS2 Directive** | EU cybersecurity | Governance, risk management, incident handling |
| **EU CRA** | Product cybersecurity | Annex I essential requirements, Annex II critical products |
| **GDPR** | Data protection | Privacy by design/default, breach notification |
| **SOC 2 Type II** | Trust services | Operational effectiveness over time |
| **PCI DSS v4.0** | Payment security | Cardholder data protection (SAQ A focus) |
| **HIPAA** | Healthcare data | PHI safeguards (consulting readiness) |

## ISO 27001:2022 Annex A Control Mapping

### Organizational Controls (A.5)

**A.5.1 Policies for Information Security**
- **Implementation**: Information Security Policy
- **NIST CSF 2.0**: GV.PO-01 (Policy established and communicated)
- **CIS v8.1**: 14.1 (Security policy dissemination)
- **Evidence**: Policy documents, version control, approval records

**A.5.2 Roles & Responsibilities**
- **Implementation**: Security roles defined in Information Security Policy
- **NIST CSF 2.0**: GV.RR-02 (Roles and authorities established)
- **CIS v8.1**: 14.3 (Document security responsibilities)
- **Evidence**: Role descriptions, RACI matrix, responsibility assignments

**A.5.3 Segregation of Duties**
- **Implementation**: Segregation of Duties Policy with compensating controls
- **NIST CSF 2.0**: PR.AC-03 (Privileged access managed)
- **CIS v8.1**: 6.1 (Access workflow enforcing SoD)
- **Evidence**: SoD matrix, compensating controls, audit logs

**A.5.4 Management Responsibilities**
- **Implementation**: Management commitment in Information Security Policy
- **NIST CSF 2.0**: GV.OV-01 (Leadership supports risk management)
- **CIS v8.1**: 17.1 (Designate incident handling leadership)
- **Evidence**: Management review records, resource allocation

**A.5.7 Threat Intelligence**
- **Implementation**: Risk Register, Threat Modeling Policy
- **NIST CSF 2.0**: ID.RA-04 (Threat intelligence informs risk)
- **CIS v8.1**: 7.1 (Vulnerability/threat intake)
- **Evidence**: Threat assessments, risk register updates

**A.5.8 Security in Project Management**
- **Implementation**: Secure Development Policy, Change Management
- **NIST CSF 2.0**: PR.IP-01 (System development processes)
- **CIS v8.1**: 16.1 (Secure application development)
- **Evidence**: SDLC documentation, security requirements

**A.5.9 Asset Inventory**
- **Implementation**: Asset Register
- **NIST CSF 2.0**: ID.AM-01 (Assets inventoried)
- **CIS v8.1**: 1.1 (Enterprise asset inventory)
- **Evidence**: Asset register, discovery scans

**A.5.10 Acceptable Use**
- **Implementation**: Acceptable Use Policy
- **NIST CSF 2.0**: PR.AC-01 (Identities managed)
- **CIS v8.1**: 14.1 (Security awareness including acceptable use)
- **Evidence**: Policy acceptance records, training logs

**A.5.12 Information Classification**
- **Implementation**: Data Classification Policy, CLASSIFICATION framework
- **NIST CSF 2.0**: ID.AM-03 (Data assets classified)
- **CIS v8.1**: 3.4 (Data classification scheme)
- **Evidence**: Classification schema, labeled assets

### People Controls (A.6)

**A.6.2 Terms & Conditions of Employment**
- **Implementation**: Access Control Policy, employment contracts
- **NIST CSF 2.0**: GV.RR-01 (Policies for managing cybersecurity workforce)
- **CIS v8.1**: 14.2 (Security awareness training)
- **Evidence**: Employment agreements, security clauses

**A.6.4 Access to Assets**
- **Implementation**: Access Control Policy
- **NIST CSF 2.0**: PR.AC-04 (Access permissions managed)
- **CIS v8.1**: 6.1 (Least privilege access)
- **Evidence**: Access control lists, permission reviews

### Physical Controls (A.7)

**A.7.1 Physical Security Perimeters**
- **Implementation**: Physical Security Policy (home office + AWS inherited controls)
- **NIST CSF 2.0**: PR.AC-02 (Physical access managed)
- **CIS v8.1**: 4.1 (Secure configuration baseline)
- **Evidence**: Office security measures, cloud certifications

### Technological Controls (A.8)

**A.8.2 Privileged Access Rights**
- **Implementation**: Access Control Policy with MFA
- **NIST CSF 2.0**: PR.AC-03 (Privileged access managed)
- **CIS v8.1**: 6.8 (Role-based access control)
- **Evidence**: MFA implementation, access reviews

**A.8.3 Information Access Restriction**
- **Implementation**: Access Control Policy, Network Security Policy
- **NIST CSF 2.0**: PR.AC-04 (Access permissions)
- **CIS v8.1**: 6.1 (Access control implementation)
- **Evidence**: Firewall rules, access logs

**A.8.9 Configuration Management**
- **Implementation**: Change Management, Secure Development Policy
- **NIST CSF 2.0**: PR.IP-01 (Configuration management)
- **CIS v8.1**: 4.1 (Secure configuration)
- **Evidence**: Configuration baselines, change records

**A.8.10 Information Deletion**
- **Implementation**: Data Classification Policy, Asset Register
- **NIST CSF 2.0**: PR.DS-03 (Data disposal)
- **CIS v8.1**: 3.12 (Data disposal processes)
- **Evidence**: Data retention policy, disposal logs

**A.8.12 Data Leak Prevention**
- **Implementation**: Cryptography Policy, Network Security Policy
- **NIST CSF 2.0**: PR.DS-01 (Data at rest protected)
- **CIS v8.1**: 3.10 (Encrypt data in transit)
- **Evidence**: Encryption implementation, DLP controls

**A.8.19 Security in Development**
- **Implementation**: Secure Development Policy
- **NIST CSF 2.0**: PR.IP-01 (Secure development practices)
- **CIS v8.1**: 16.1 (Secure development process)
- **Evidence**: SAST/DAST results, code reviews

**A.8.23 Web Filtering**
- **Implementation**: Network Security Policy
- **NIST CSF 2.0**: PR.PT-04 (Communications protected)
- **CIS v8.1**: 9.2 (DNS filtering)
- **Evidence**: Content filtering rules, logs

**A.8.28 Secure Coding**
- **Implementation**: Secure Development Policy
- **NIST CSF 2.0**: PR.IP-01 (Secure coding standards)
- **CIS v8.1**: 16.1 (Secure development)
- **Evidence**: Coding standards, security reviews

## NIST CSF 2.0 Function Mapping

### GOVERN (GV)
- **GV.PO**: Policies establish cybersecurity expectations
- **GV.RR**: Roles and responsibilities defined
- **GV.OV**: Leadership provides oversight
- **GV.RM**: Risk management strategy implemented

### IDENTIFY (ID)
- **ID.AM**: Assets inventoried and classified
- **ID.RA**: Risks assessed and prioritized
- **ID.IM**: Improvements identified
- **ID.BE**: Business environment understood

### PROTECT (PR)
- **PR.AC**: Access controls implemented
- **PR.DS**: Data security measures in place
- **PR.IP**: Information protection processes
- **PR.PT**: Protective technology deployed

### DETECT (DE)
- **DE.AE**: Anomalies detected
- **DE.CM**: Continuous monitoring active
- **DE.DP**: Detection processes established

### RESPOND (RS)
- **RS.MA**: Response management coordinated
- **RS.AN**: Incidents analyzed
- **RS.CO**: Response communications managed
- **RS.MI**: Mitigation activities performed

### RECOVER (RC)
- **RC.RP**: Recovery planning documented
- **RC.IM**: Improvements identified
- **RC.CO**: Recovery communications managed

## CIS Controls v8.1 Implementation Groups

### IG1 (Basic Cyber Hygiene)
- **1.1**: Inventory of Assets ✅
- **2.1**: Inventory of Software ✅
- **3.10**: Encrypt Data in Transit ✅
- **4.1**: Secure Configuration ✅
- **5.1**: Account Inventory ✅
- **6.8**: Role-Based Access Control ✅

### IG2 (Enterprise Security)
- **8.2**: Collect Audit Logs ✅
- **10.1**: Deploy Anti-Malware ✅
- **13.1**: Security Event Alerting ✅
- **16.1**: Secure Development Process ✅

### IG3 (Advanced/Enterprise)
- **7.1**: Threat Intelligence ✅
- **11.1**: Data Recovery Capability ✅
- **14.1**: Security Awareness Program ✅
- **17.1**: Incident Response Planning ✅

## NIS2 Directive Compliance

### Article 20: Governance
- Risk management measures approved by management
- Business continuity plans documented
- Supply chain security managed
- **Evidence**: [Business Continuity Plan](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Business_Continuity_Plan.md), [Third Party Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Third_Party_Management.md)

### Article 21: Technical/Operational Measures
- Incident handling policies
- Business continuity and disaster recovery
- Security of network and information systems
- **Evidence**: [Incident Response Plan](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Incident_Response_Plan.md), [Network Security Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Network_Security_Policy.md)

### Article 23: Incident Reporting
- 24-hour early warning for significant incidents
- 72-hour formal notification
- Progress reports and final reports
- **Evidence**: [Incident Response Plan § Reporting](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Incident_Response_Plan.md)

## EU Cyber Resilience Act (CRA)

### Annex I Essential Requirements
- **Secure by Design**: Security throughout product lifecycle
- **Vulnerability Management**: Handling and disclosure process
- **Security Updates**: Automated update mechanisms
- **Evidence**: [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md), [Vulnerability Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Vulnerability_Management.md)

### Annex II Critical Products (Art. 6, 11)
- Enhanced security requirements for critical products
- Third-party conformity assessment
- Continuous monitoring obligations
- **Evidence**: [CRA Conformity Assessment Process](https://github.com/Hack23/ISMS-PUBLIC/blob/main/CRA_Conformity_Assessment_Process.md)

## GDPR Compliance

### Core Articles
- **Art. 5**: Data processing principles (lawfulness, fairness, transparency)
- **Art. 25**: Data protection by design and by default
- **Art. 32**: Security of processing
- **Art. 33**: Breach notification (72 hours)
- **Evidence**: [Data Classification Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Data_Classification_Policy.md), [Privacy Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Privacy_Policy.md)

### Swedish Dataskyddslagen
- Local DPA notification requirements
- Swedish-specific privacy considerations
- **Evidence**: [External Stakeholder Registry](https://github.com/Hack23/ISMS-PUBLIC/blob/main/External_Stakeholder_Registry.md)

## SOC 2 Type II Trust Services Criteria

### Common Criteria (CC)
- **CC1.1-1.5**: Control environment
- **CC2.1-2.3**: Communication and information
- **CC3.1-3.4**: Risk assessment
- **CC4.1-4.2**: Monitoring activities
- **CC5.1-5.3**: Control activities
- **CC6.1-6.8**: Logical/physical access controls
- **CC7.1-7.5**: System operations
- **CC8.1**: Change management
- **CC9.1-9.2**: Risk mitigation

### Trust Services Categories
- **Security**: System protected against unauthorized access
- **Availability**: System available as committed
- **Processing Integrity**: Processing complete, valid, accurate, timely
- **Confidentiality**: Confidential information protected
- **Privacy**: Personal information handled per privacy notice

## PCI DSS v4.0 (SAQ A Focus)

### SAQ A (Outsourced Card Processing)
- **Req 1-2**: Network security controls (AWS CloudFront, GitHub Pages)
- **Req 3-4**: Cardholder data protection (Stripe handles all CHD)
- **Req 5-6**: Vulnerability management (CodeQL, Dependabot)
- **Req 7-8**: Access controls (GitHub MFA, SSH keys, GPG signing)
- **Req 9**: Physical security (home office, AWS data centers)
- **Req 10-11**: Monitoring and testing (audit logs, vulnerability scanning)
- **Req 12**: Security policies (comprehensive ISMS documented)

### Key Attestation
- No CHD stored, processed, or transmitted on Hack23 systems
- All payment processing via Stripe (PCI DSS certified)
- Annual SAQ A completion with attestation

## HIPAA Security Rule (Consulting Readiness)

### Administrative Safeguards (§164.308)
- Risk analysis and management ✅
- Information access management ✅
- Security awareness training ✅
- Contingency planning ✅
- **Evidence**: [Risk Assessment Methodology](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Risk_Assessment_Methodology.md)

### Physical Safeguards (§164.310)
- Facility access controls ✅
- Workstation security ✅
- Device and media controls ✅
- **Evidence**: [Physical Security Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Physical_Security_Policy.md)

### Technical Safeguards (§164.312)
- Access controls ✅
- Audit controls ✅
- Integrity controls ✅
- Transmission security ✅
- **Evidence**: [Cryptography Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Cryptography_Policy.md)

**Note**: Hack23 AB does not currently process PHI. These mappings demonstrate consulting readiness for healthcare clients.

## Compliance Verification Workflow

### 1. Quarterly Self-Assessment
- Review [Compliance Checklist](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Compliance_Checklist.md)
- Update control implementation status
- Document gaps and remediation plans
- Record in management review

### 2. Evidence Collection
- Policy documents (version controlled)
- Configuration files (GitHub)
- Audit logs (CloudTrail, GitHub audit)
- Scan results (CodeQL, Dependabot, OpenSSF Scorecard)
- Test results (backup tests, DR exercises)

### 3. Gap Analysis
- Identify missing controls
- Prioritize by risk and regulatory requirement
- Create remediation action items
- Track in issue management system

### 4. Continuous Monitoring
- OpenSSF Scorecard (weekly)
- Dependabot alerts (real-time)
- CodeQL scans (on commit)
- Backup validation (daily)
- Incident detection (continuous)

## Audit Readiness Checklist

### Before External Audit
- [ ] All policies current (annual review completed)
- [ ] All registers updated (Asset, Risk, Stakeholder)
- [ ] Quarterly management reviews documented
- [ ] Incident log reviewed (even if no incidents)
- [ ] Evidence accessible (GitHub, CloudTrail, logs)
- [ ] Compliance Checklist current
- [ ] Known gaps documented with remediation plans
- [ ] Backups tested within last 90 days
- [ ] DR exercise completed within last year
- [ ] Vendor assessments current

### Evidence Matrix
| Control Domain | Primary Evidence | Secondary Evidence | Location |
|---------------|------------------|-------------------|----------|
| Policies | Policy documents | Approval records | GitHub repo |
| Access Control | MFA config, SSH keys | Access reviews | AWS IAM, GitHub |
| Vulnerability Mgmt | Scan results | Remediation records | CodeQL, Dependabot |
| Incident Response | IR plan | Incident logs | ISMS repo, GitHub Issues |
| BCP/DR | BCP/DR plans | Test results | ISMS repo, test logs |
| Change Management | Change records | Approval logs | GitHub PRs, commits |
| Asset Management | Asset Register | Discovery scans | ISMS repo, AWS Config |
| Monitoring | Audit logs | Alerting config | CloudTrail, GitHub audit |

## References

### Hack23 ISMS Documentation
- [Compliance Checklist](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Compliance_Checklist.md) - Master compliance mapping
- [Information Security Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Information_Security_Policy.md) - ISMS framework
- [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md) - SDLC security
- [Classification Framework](https://github.com/Hack23/ISMS-PUBLIC/blob/main/CLASSIFICATION.md) - Data and system classification
- [Risk Register](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Risk_Register.md) - Enterprise risk management

### Example Implementations
- [CIA Security Architecture](https://github.com/Hack23/cia/blob/master/SECURITY_ARCHITECTURE.md) - Full authentication implementation
- [CIA Compliance Manager Architecture](https://github.com/Hack23/cia-compliance-manager/blob/main/docs/architecture/SECURITY_ARCHITECTURE.md) - Frontend-only security
- [Riksdagsmonitor Security Architecture](https://github.com/Hack23/riksdagsmonitor/blob/main/SECURITY_ARCHITECTURE.md) - Static site security

### Framework References
- [ISO 27001:2022](https://www.iso.org/standard/27001) - Information security management
- [NIST CSF 2.0](https://www.nist.gov/cyberframework) - Cybersecurity Framework
- [CIS Controls v8.1](https://www.cisecurity.org/controls) - Security best practices
- [NIS2 Directive](https://eur-lex.europa.eu/eli/dir/2022/2555) - EU cybersecurity requirements
- [EU CRA](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act) - Cyber Resilience Act

## Remember

- **Unified Compliance**: One ISMS serves multiple frameworks
- **Evidence-Based**: Document everything, artifacts are proof
- **Continuous Monitoring**: Compliance is ongoing, not annual
- **Risk-Based**: Prioritize by business impact
- **Transparency**: Public ISMS demonstrates capability
- **Multi-Framework**: ISO + NIST + CIS + NIS2 + CRA + GDPR alignment
- **Audit Ready**: Evidence always accessible
- **Gap Management**: Know gaps, document remediation plans
