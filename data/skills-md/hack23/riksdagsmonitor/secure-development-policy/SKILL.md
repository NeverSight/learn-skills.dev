---
name: secure-development-policy
description: Comprehensive secure development lifecycle covering all SDLC phases, AI controls, testing, and security requirements per Hack23 ISMS
license: Apache-2.0
---

# 🛡️ Secure Development Policy Skill

## 🎯 Purpose Statement

Apply **Hack23 AB's Secure Development Policy** to demonstrate how **security-by-design creates competitive advantages** through systematic DevSecOps implementation.

**Reference:** [Hack23 Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)

This skill provides comprehensive guidance for implementing all phases of the secure development lifecycle with clear, actionable requirements following [STYLE_GUIDE.md](https://github.com/Hack23/ISMS-PUBLIC/blob/main/STYLE_GUIDE.md) icon standards.

---

## 🔄 Secure Development Lifecycle (SDLC) - All Phases

### 📋 Phase 1: Planning & Design

**Clear Requirements:**
- ✅ Complete project classification per [Classification Framework](https://github.com/Hack23/ISMS-PUBLIC/blob/main/CLASSIFICATION.md)
- ✅ Document CIA triad levels (Confidentiality, Integrity, Availability)
- ✅ Define RTO/RPO aligned with business impact
- ✅ Create SECURITY_ARCHITECTURE.md with Mermaid C4 diagrams
- ✅ Perform STRIDE threat modeling documented in THREAT_MODEL.md
- ✅ Complete risk assessment integrated with Risk Register
- ✅ Calculate security investment ROI based on classification

**Deliverables Checklist:**
- [ ] README.md includes "Project Classification" section
- [ ] SECURITY_ARCHITECTURE.md created with current state
- [ ] FUTURE_SECURITY_ARCHITECTURE.md created with roadmap
- [ ] THREAT_MODEL.md includes STRIDE analysis
- [ ] Risk assessment documented and registered
- [ ] Cost-benefit analysis approved by CEO

---

### 💻 Phase 2: Development

**Clear Requirements:**
- ✅ Follow OWASP Top 10 secure coding standards
- ✅ Implement language-specific security best practices
- ✅ Require security-focused code review for all changes
- ✅ Apply data classification to all code assets
- ✅ Use GitHub secrets, never hardcode credentials
- ✅ Implement secret rotation procedures
- ✅ Use parameterized queries (no SQL injection)
- ✅ Validate and sanitize all inputs
- ✅ Encode outputs appropriately for context
- ✅ Implement proper error handling (no information disclosure)

**Code Review Security Checklist:**
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all external data
- [ ] Output encoding prevents XSS
- [ ] Parameterized queries prevent injection
- [ ] Authentication/authorization properly implemented
- [ ] Error messages don't leak sensitive info
- [ ] Logging captures security events
- [ ] Dependencies are approved and scanned
- [ ] Code follows least privilege principle
- [ ] Sensitive data encrypted at rest and in transit

---

### 🧪 Phase 3: Security Testing

**Clear Requirements:**

#### 🔬 SAST (Static Application Security Testing)
- ✅ SonarCloud integration on every commit
- ✅ Quality gate must pass (no Critical/High vulnerabilities)
- ✅ Security hotspots reviewed and resolved
- ✅ Code coverage ≥80% lines, ≥70% branches

#### 📦 SCA (Software Composition Analysis)
- ✅ Automated dependency scanning (Dependabot/Renovate)
- ✅ SBOM generation (CycloneDX or SPDX format)
- ✅ License compliance via FOSSA scanning
- ✅ Vulnerability remediation per classification SLAs:
  - **Critical:** 24 hours
  - **High:** 7 days
  - **Medium:** 30 days
  - **Low:** 90 days

#### ⚡ DAST (Dynamic Application Security Testing)
- ✅ OWASP ZAP scanning in staging environment
- ✅ API security testing (authentication, authorization, input validation)
- ✅ Annual penetration testing for High/Critical projects

#### 🔍 Secret Scanning
- ✅ GitHub secret scanning enabled
- ✅ Pre-commit hooks prevent secret commits
- ✅ Immediate rotation for any exposed secrets

#### 🔒 Test Data Protection
- ✅ **NEVER** use production data in test environments
- ✅ Anonymize/pseudonymize/mask all test data
- ✅ Securely delete test data after use
- ✅ Restrict test environment access (least privilege)

---

### 🚀 Phase 4: Deployment

**Clear Requirements:**
- ✅ Automated CI/CD with security gates
- ✅ All GitHub Actions pinned to SHA commits
- ✅ Harden-runner enabled with egress auditing
- ✅ Least privilege permissions in workflows
- ✅ Manual approval required for production
- ✅ Deployment checklist completed
- ✅ Security metrics and monitoring configured
- ✅ Rollback plan documented and tested

**GitHub Actions Security Pattern:**
```yaml
permissions:
  contents: read  # Least privilege default

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: step-security/harden-runner@<SHA>
        with:
          egress-policy: audit
      
      - uses: actions/checkout@<SHA>
      
      # Pin ALL actions to SHA, not tags
```

---

### 🔧 Phase 5: Maintenance & Operations

**Clear Requirements:**
- ✅ Active vulnerability management per [Vulnerability Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Vulnerability_Management.md)
- ✅ Security metrics tracked per [Security Metrics](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Security_Metrics.md)
- ✅ Regular dependency updates (automated via Dependabot)
- ✅ Security patches applied per classification SLAs
- ✅ Incident response integration per [Incident Response Plan](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Incident_Response_Plan.md)
- ✅ Annual security review and threat model update
- ✅ Quarterly dependency and license audits
- ✅ Continuous monitoring and alerting

**Monitoring Requirements:**
- [ ] Security event logging enabled
- [ ] SIEM integration configured
- [ ] Vulnerability alerts routed to security team
- [ ] Performance metrics track security impact
- [ ] Compliance dashboards updated real-time

---

## 🤖 AI-Augmented Development Controls

**Clear Requirements for ALL AI-assisted development:**

### 🔐 AI as Proposal Generator Only
- ✅ All AI outputs require human review and approval
- ✅ AI cannot bypass CI/CD, security gates, or approvals
- ✅ Human developer retains accountability for all changes
- ✅ AI cannot weaken security controls
- ✅ AI cannot autonomously deploy to production

### 📋 Mandatory PR Review Process
- ✅ All AI-assisted code goes through standard PR workflow
- ✅ PR description documents AI assistance used
- ✅ Security gates enforced (no exceptions for AI)
- ✅ Human reviewer verifies security controls intact
- ✅ Testing requirements unchanged (80%+ coverage)

### 🔧 Curator-Agent Governance
- ✅ Changes to `.github/agents/*.md` require CEO approval
- ✅ Changes to `.github/copilot-mcp*.json` require CEO approval
- ✅ Changes to `.github/workflows/copilot-setup-steps.yml` require CEO approval
- ✅ Treat as Normal Changes per [Change Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Change_Management.md)
- ✅ Document risk assessment for capability expansion
- ✅ All new integrations require security review

### 🛡️ Security & Audit Requirements
- ✅ Agents operate with least-privilege tool access
- ✅ MCP configurations under change control
- ✅ All agent activities logged and auditable
- ✅ Capability expansion requires security review
- ✅ Quarterly agent ecosystem security audit

---

## 🎯 Unit Test Coverage Requirements

**Clear Requirements:**
- ✅ Minimum 80% line coverage
- ✅ Minimum 70% branch coverage
- ✅ Tests run on every commit and PR
- ✅ UnitTestPlan.md documented in repository
- ✅ Public coverage reports via badges
- ✅ Historical coverage tracking (no regression)
- ✅ Coverage reports published to public URL

**Reference Implementations:**
- 🏛️ **CIA:** [Unit Tests](https://hack23.github.io/cia/surefire.html) • [Coverage](https://hack23.github.io/cia/jacoco/) • [Plan](https://github.com/Hack23/cia/blob/master/UnitTestPlan.md)
- 🎮 **Black Trigram:** [Tests](https://blacktrigram.com/test-results/) • [Coverage](https://blacktrigram.com/coverage/) • [Plan](https://github.com/Hack23/blacktrigram/blob/main/UnitTestPlan.md)
- 📊 **CIA Compliance Manager:** [Tests](https://ciacompliancemanager.com/test-results/) • [Coverage](https://ciacompliancemanager.com/coverage/) • [Plan](https://github.com/Hack23/cia-compliance-manager/blob/main/docs/UnitTestPlan.md)

---

## 🌐 End-to-End Testing Requirements

**Clear Requirements:**
- ✅ All critical user journeys covered
- ✅ E2ETestPlan.md documented in repository
- ✅ Public Mochawesome/Cypress reports
- ✅ Cross-browser testing (Chrome, Firefox, Safari)
- ✅ Performance assertions within tests
- ✅ Authentication/authorization flows tested
- ✅ Error handling and edge cases covered

**Reference Implementations:**
- 🏛️ **CIA:** [E2E Plan](https://github.com/Hack23/cia/blob/master/E2ETestPlan.md)
- 🎮 **Black Trigram:** [E2E Tests](https://blacktrigram.com/cypress/mochawesome/) • [Plan](https://github.com/Hack23/blacktrigram/blob/main/E2ETestPlan.md)
- 📊 **CIA Compliance Manager:** [E2E Tests](https://ciacompliancemanager.com/cypress/mochawesome/) • [Plan](https://github.com/Hack23/cia-compliance-manager/blob/main/docs/E2ETestPlan.md)

---

## 🕷️ Threat Modeling Requirements

**Clear Requirements per [Threat Modeling Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Threat_Modeling.md):**

### 📋 Required Documentation
- ✅ **THREAT_MODEL.md** in repository root
- ✅ STRIDE framework application (all 6 categories)
- ✅ MITRE ATT&CK technique mapping
- ✅ Attack tree analysis with probability/impact
- ✅ Threat agent classification (external/internal/supply chain)
- ✅ Quantitative risk assessment with business impact
- ✅ Security control mapping with effectiveness validation

### 🔄 Maintenance Requirements
- ✅ Threat model created during design phase
- ✅ Updated for all architectural changes
- ✅ Annual comprehensive review
- ✅ Quarterly update cycle
- ✅ Incident-driven updates after security events

**Reference Implementations:**
- 🏛️ **CIA:** [Threat Model](https://github.com/Hack23/cia/blob/master/THREAT_MODEL.md) • [STRIDE](https://github.com/Hack23/cia/blob/master/THREAT_MODEL.md#stride-threat-analysis) • [Attack Trees](https://github.com/Hack23/cia/blob/master/THREAT_MODEL.md#attack-tree-analysis)
- 🎮 **Black Trigram:** [Threat Model](https://github.com/Hack23/blacktrigram/blob/main/THREAT_MODEL.md) • [Gaming Security](https://github.com/Hack23/blacktrigram/blob/main/THREAT_MODEL.md#gaming-specific-threats)
- 📊 **CIA Compliance Manager:** [Threat Model](https://github.com/Hack23/cia-compliance-manager/blob/main/docs/architecture/THREAT_MODEL.md) • [Risk Assessment](https://github.com/Hack23/cia-compliance-manager/blob/main/docs/architecture/THREAT_MODEL.md#quantitative-risk-assessment)

---

## 🎖️ Public Evidence Requirements

**Clear Requirements per [STYLE_GUIDE.md](https://github.com/Hack23/ISMS-PUBLIC/blob/main/STYLE_GUIDE.md):**

### Required Badges in README.md
- ✅ OpenSSF Scorecard (target: ≥7.0)
- ✅ CII Best Practices (minimum: Passing)
- ✅ SLSA Level 3 attestation
- ✅ SonarCloud Quality Gate (must be "Passed")
- ✅ Code Coverage badge (≥80%)
- ✅ License badge (OSI-approved)
- ✅ Threat Model link badge

**Example Badge Configuration:**
```markdown
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/ORG/REPO/badge)](https://scorecard.dev/viewer/?uri=github.com/ORG/REPO)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/ID/badge)](https://bestpractices.coreinfrastructure.org/projects/ID)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=ORG_REPO&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ORG_REPO)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ORG_REPO&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ORG_REPO)
[![Threat Model](https://img.shields.io/badge/Threat_Model-Documentation-blue)](https://github.com/ORG/REPO/blob/main/THREAT_MODEL.md)
```

---

## 📋 Master Verification Checklist

Use this comprehensive checklist before ANY deployment:

### Phase 1: Planning & Design ✅
- [ ] Project classification complete (CIA + RTO/RPO + Business Impact)
- [ ] SECURITY_ARCHITECTURE.md created with C4 diagrams
- [ ] FUTURE_SECURITY_ARCHITECTURE.md created with roadmap
- [ ] THREAT_MODEL.md includes STRIDE + MITRE ATT&CK
- [ ] Attack trees documented with probability/impact
- [ ] Risk assessment registered
- [ ] Cost-benefit analysis approved

### Phase 2: Development ✅
- [ ] OWASP Top 10 mitigations implemented
- [ ] Language-specific security standards followed
- [ ] Code review completed with security focus
- [ ] Asset classification applied
- [ ] No hardcoded secrets (verified with secret scanning)
- [ ] Input validation implemented
- [ ] Output encoding implemented
- [ ] Error handling doesn't leak sensitive info
- [ ] Logging captures security events

### Phase 3: Testing ✅
- [ ] SAST passed (SonarCloud quality gate green)
- [ ] SCA clean (all vulnerabilities remediated per SLA)
- [ ] DAST completed (OWASP ZAP scan clean)
- [ ] Secret scanning clean
- [ ] Test data properly anonymized
- [ ] Unit test coverage ≥80% lines, ≥70% branches
- [ ] E2E tests cover all critical paths
- [ ] UnitTestPlan.md documented
- [ ] E2ETestPlan.md documented

### Phase 4: Deployment ✅
- [ ] CI/CD security gates passed
- [ ] All GitHub Actions pinned to SHA
- [ ] Harden-runner enabled
- [ ] Least privilege permissions
- [ ] Manual approval obtained for production
- [ ] Deployment checklist complete
- [ ] Security metrics configured
- [ ] Rollback plan tested

### Phase 5: Operations ✅
- [ ] Vulnerability management active
- [ ] Security metrics monitored
- [ ] Dependency updates automated
- [ ] Incident response integrated
- [ ] Annual review scheduled
- [ ] Quarterly audits scheduled

### AI Controls ✅
- [ ] Human review for all AI outputs
- [ ] No autonomous deployments
- [ ] PR documentation complete
- [ ] Agent permissions least-privilege
- [ ] MCP config under change control
- [ ] Audit trail enabled

### Documentation ✅
- [ ] SECURITY_ARCHITECTURE.md
- [ ] FUTURE_SECURITY_ARCHITECTURE.md
- [ ] THREAT_MODEL.md
- [ ] SECURITY.md (vulnerability disclosure)
- [ ] WORKFLOWS.md (CI/CD documentation)
- [ ] UnitTestPlan.md
- [ ] E2ETestPlan.md
- [ ] CRA-ASSESSMENT.md (if applicable)
- [ ] README includes classification section
- [ ] All required badges displayed

### Public Evidence ✅
- [ ] OpenSSF Scorecard ≥7.0
- [ ] CII Best Practices (Passing+)
- [ ] SLSA Level 3 attestation
- [ ] Quality Gate passed
- [ ] Coverage ≥80%
- [ ] License compliance (FOSSA clean)

---

## 📚 Authoritative References

- **Primary Policy:** [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
- **Related Policies:**
  - [Threat Modeling](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Threat_Modeling.md)
  - [Vulnerability Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Vulnerability_Management.md)
  - [Classification Framework](https://github.com/Hack23/ISMS-PUBLIC/blob/main/CLASSIFICATION.md)
  - [Change Management](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Change_Management.md)
  - [Incident Response Plan](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Incident_Response_Plan.md)
  - [Security Metrics](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Security_Metrics.md)
- **Standards:** [STYLE_GUIDE.md](https://github.com/Hack23/ISMS-PUBLIC/blob/main/STYLE_GUIDE.md)

---

## 💡 Key Takeaways

- 🛡️ **Security by Design:** Build security in from the start, not bolt on later
- 🌟 **Transparency:** Public evidence through badges and documentation
- 🏷️ **Classification-Driven:** All decisions aligned with project classification
- 🔄 **Continuous Improvement:** Regular reviews, updates, and learning from incidents
- 🤖 **Human Accountability:** AI assists, humans decide and approve
- 📊 **Evidence-Based:** Every security claim backed by public, verifiable proof
- ✅ **Comprehensive Coverage:** ALL 5 SDLC phases with clear, actionable requirements
