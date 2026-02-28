---
title: "security-audit: Security analysis, vulnerability assessment, and security code reviews"
name: security-audit
description: Security analysis, vulnerability assessment, and security code reviews
tags:
  - sdd-workflow
  - shared-architecture
  - quality-assurance
custom_fields:
  layer: null
  artifact_type: null
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: quality-assurance
  upstream_artifacts: [SPEC, CTR]
  downstream_artifacts: []
  version: "1.0"
  last_updated: "2026-02-10T15:00:00"
---

# security-audit

**Description**: Security requirements validation, vulnerability assessment, and compliance checking

**Category**: Security & Compliance

**Complexity**: High (multi-layer security analysis)

---

## Purpose

Ensure security requirements are properly defined, implemented, and tested. Identify vulnerabilities across code, dependencies, infrastructure, and configurations. Validate compliance with security standards and best practices.

---

## Capabilities

### 1. Security Requirements Validation
- Validate security requirements from REQ documents
- Check completeness of security specifications
- Verify authentication/authorization requirements
- Validate data protection requirements
- Check encryption specifications

### 2. Code Security Scanning
- **SAST (Static Application Security Testing)**: bandit, semgrep
- **Dependency scanning**: safety, pip-audit
- **Secret detection**: detect-secrets, gitleaks
- **SQL injection detection**: Pattern matching
- **XSS vulnerability detection**: Input validation analysis
- **CSRF protection**: Token validation checking

### 3. Infrastructure Security
- IaC security scanning: checkov, tfsec
- Container security: trivy, grype
- Kubernetes security: kubesec, kube-bench
- Cloud configuration: AWS Security Hub, Azure Security Center
- Network security: Firewall rules, security groups

### 4. Dependency Vulnerability Assessment
- Known CVE detection
- License compliance
- Outdated package identification
- Transitive dependency analysis
- Vulnerability severity scoring (CVSS)

### 5. Authentication & Authorization
- JWT implementation validation
- Password policy enforcement
- Session management review
- OAuth/OIDC configuration
- Role-based access control (RBAC)

### 6. Data Protection
- Encryption at rest validation
- Encryption in transit (TLS/SSL)
- PII/sensitive data handling
- Data retention policies
- Backup security

### 7. Compliance Checking
- OWASP Top 10 coverage
- CWE mapping
- GDPR compliance (data protection)
- HIPAA compliance (healthcare)
- SOC 2 requirements
- PCI DSS (payment card data)

### 8. Threat Modeling
- STRIDE analysis
- Attack surface mapping
- Data flow diagrams
- Trust boundary identification
- Threat scenario generation

---

## Security Audit Workflow

```mermaid
graph TD
    A[Security Audit] --> B[Requirements Analysis]
    B --> C{Security REQs Complete?}
    C -->|No| D[Flag Missing Requirements]
    C -->|Yes| E[Code Security Scan]

    E --> F[SAST Analysis]
    F --> G[Dependency Scan]
    G --> H[Secret Detection]

    H --> I{Critical Issues?}
    I -->|Yes| J[Block Deployment]
    I -->|No| K[Infrastructure Scan]

    K --> L[IaC Security]
    L --> M[Container Security]
    M --> N[Cloud Config Review]

    N --> O{Security Violations?}
    O -->|Yes| P[Generate Remediation Plan]
    O -->|No| Q[Compliance Check]

    Q --> R{Compliant?}
    R -->|No| S[Flag Compliance Gaps]
    R -->|Yes| T[Threat Modeling]

    T --> U[Identify Threats]
    U --> V[Risk Assessment]
    V --> W[Generate Security Report]

    D --> W
    J --> W
    P --> W
    S --> W
```

---

## Usage Instructions

### Comprehensive Security Audit

```bash
security-audit full-audit \
  --requirements reqs/ \
  --code src/ \
  --infrastructure infrastructure/ \
  --output reports/security/
```

Output:
```
=== Security Audit Report ===
Date: 2025-01-15
Scope: Full system audit

Overall Security Score: 72/100 (Acceptable)

CRITICAL ISSUES (2):
1. [CWE-89] SQL Injection vulnerability
   - File: src/api/users.py:145
   - Description: Direct string concatenation in SQL query
   - CVSS Score: 9.8 (Critical)
   - Fix: Use parameterized queries
   - Status: BLOCKS DEPLOYMENT ❌

2. [CWE-798] Hardcoded credentials
   - File: src/config.py:23
   - Description: Database password hardcoded in source
   - CVSS Score: 9.1 (Critical)
   - Fix: Use environment variables or secrets manager
   - Status: BLOCKS DEPLOYMENT ❌

HIGH SEVERITY (5):
3. [CWE-200] Information exposure
   - File: src/api/error_handler.py:67
   - Description: Stack traces exposed in API responses
   - CVSS Score: 7.5 (High)
   - Fix: Return generic error messages in production

4. [CVE-2023-12345] Vulnerable dependency
   - Package: requests==2.25.0
   - Vulnerability: Authentication bypass
   - CVSS Score: 8.2 (High)
   - Fix: Upgrade to requests>=2.31.0

5. [CWE-352] Missing CSRF protection
   - File: src/api/forms.py
   - Description: No CSRF tokens on state-changing operations
   - CVSS Score: 8.8 (High)
   - Fix: Implement CSRF token validation

6. [CWE-862] Missing authorization
   - File: src/api/admin.py:89
   - Description: Admin endpoint lacks authorization check
   - CVSS Score: 7.5 (High)
   - Fix: Add @require_admin decorator

7. [Container] Running as root
   - File: Dockerfile:15
   - Description: Container runs with root privileges
   - CVSS Score: 7.0 (High)
   - Fix: Create and use non-root user

MEDIUM SEVERITY (12):
... (abbreviated)

LOW SEVERITY (23):
... (abbreviated)

COMPLIANCE STATUS:
✓ OWASP Top 10: 8/10 covered
✗ SQL Injection: Not protected (A03:2021)
✗ Broken Access Control: Partial (A01:2021)
✓ Encryption: TLS 1.3 enforced
✓ Authentication: JWT properly implemented
⚠ Authorization: Missing in 3 endpoints

RECOMMENDATIONS:
1. Fix 2 critical issues immediately (block deployment)
2. Upgrade vulnerable dependencies
3. Implement CSRF protection
4. Add authorization checks to all admin endpoints
5. Review and fix information exposure
6. Container security hardening

NEXT STEPS:
1. Create remediation tickets for all HIGH+ issues
2. Schedule dependency updates
3. Conduct penetration testing after fixes
4. Re-audit in 2 weeks
```

### Requirements Security Validation

```bash
security-audit requirements \
  --input reqs/security_requirements.md \
  --output reports/security/req-validation.json
```

Output:
```json
{
  "summary": {
    "total_security_requirements": 45,
    "complete": 38,
    "incomplete": 7,
    "coverage_percentage": 84
  },
  "missing_requirements": [
    {
      "category": "Authentication",
      "requirement": "Multi-factor authentication",
      "severity": "high",
      "recommendation": "Add REQ-AUTH-MFA for critical operations"
    },
    {
      "category": "Encryption",
      "requirement": "Encryption key rotation policy",
      "severity": "medium",
      "recommendation": "Define key rotation schedule in REQ-ENC-*"
    }
  ],
  "incomplete_requirements": [
    {
      "id": "REQ-AUTH-01",
      "issue": "No password complexity specification",
      "current": "Password must be secure",
      "recommended": "Password: 8-128 chars, uppercase, lowercase, digit, special"
    }
  ]
}
```

### Dependency Vulnerability Scan

```bash
security-audit dependencies \
  --requirements requirements.txt \
  --output reports/security/dependencies.json
```

Output:
```json
{
  "total_packages": 87,
  "vulnerable_packages": 5,
  "vulnerabilities": [
    {
      "package": "requests",
      "installed_version": "2.25.0",
      "vulnerability": "CVE-2023-32681",
      "severity": "high",
      "cvss_score": 8.2,
      "description": "Proxy-Authorization header leak on cross-origin redirect",
      "fixed_in": "2.31.0",
      "recommended_action": "pip install --upgrade requests>=2.31.0"
    },
    {
      "package": "pillow",
      "installed_version": "9.0.0",
      "vulnerability": "CVE-2023-44271",
      "severity": "critical",
      "cvss_score": 9.8,
      "description": "Arbitrary code execution via crafted image",
      "fixed_in": "9.3.0",
      "recommended_action": "pip install --upgrade pillow>=9.3.0"
    }
  ],
  "license_issues": [
    {
      "package": "some-package",
      "license": "GPL-3.0",
      "issue": "Copyleft license may conflict with proprietary code",
      "recommendation": "Review license compatibility"
    }
  ]
}
```

### Secret Detection

```bash
security-audit secrets --path . --output reports/security/secrets.json
```

Output:
```json
{
  "secrets_found": 4,
  "files_scanned": 234,
  "secrets": [
    {
      "type": "AWS Access Key",
      "file": "scripts/deploy.sh",
      "line": 15,
      "matched_text": "AKIA...",
      "entropy": 4.5,
      "confidence": "high",
      "recommendation": "Move to AWS Secrets Manager or environment variable"
    },
    {
      "type": "Private Key",
      "file": "config/ssl/private.key",
      "line": 1,
      "matched_text": "-----BEGIN PRIVATE KEY-----",
      "confidence": "high",
      "recommendation": "Remove from Git, use secrets manager"
    },
    {
      "type": "Database Password",
      "file": "src/config.py",
      "line": 23,
      "matched_text": "password = 'SuperSecret123'",
      "confidence": "high",
      "recommendation": "Use environment variables or secrets manager"
    }
  ]
}
```

---

## Security Categories

### OWASP Top 10 (2021)

1. **A01:2021 - Broken Access Control**
   - Check: Authorization on all sensitive endpoints
   - Validate: User cannot access unauthorized resources
   - Test: Privilege escalation attempts

2. **A02:2021 - Cryptographic Failures**
   - Check: TLS 1.2+ for data in transit
   - Validate: Encryption at rest for sensitive data
   - Test: Weak cipher detection

3. **A03:2021 - Injection**
   - Check: SQL injection prevention (parameterized queries)
   - Validate: Input validation and sanitization
   - Test: Command injection, XSS, LDAP injection

4. **A04:2021 - Insecure Design**
   - Check: Threat modeling performed
   - Validate: Security controls in design
   - Test: Business logic vulnerabilities

5. **A05:2021 - Security Misconfiguration**
   - Check: Default credentials changed
   - Validate: Unnecessary features disabled
   - Test: Information disclosure through errors

6. **A06:2021 - Vulnerable Components**
   - Check: Dependencies up to date
   - Validate: No known CVEs in dependencies
   - Test: Transitive dependency vulnerabilities

7. **A07:2021 - Authentication Failures**
   - Check: Strong password policy
   - Validate: Session management secure
   - Test: Brute force protection

8. **A08:2021 - Software and Data Integrity**
   - Check: Code signing
   - Validate: Integrity checks on updates
   - Test: Supply chain attacks

9. **A09:2021 - Security Logging Failures**
   - Check: Security events logged
   - Validate: Logs tamper-proof
   - Test: Log injection prevention

10. **A10:2021 - Server-Side Request Forgery**
    - Check: URL validation
    - Validate: Whitelist approach for external requests
    - Test: SSRF attack attempts

---

## Security Testing

### Authentication Testing

```python
# Test: Weak password allowed
def test_weak_password_rejected():
    result = register_user(username="test", password="123")
    assert result.error == "Password too weak"

# Test: JWT token validation
def test_invalid_jwt_rejected():
    response = api_call(headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

# Test: Session expiration
def test_session_expires():
    token = login_user()
    time.sleep(3600)  # Wait 1 hour
    response = api_call(headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
```

### Authorization Testing

```python
# Test: User cannot access admin endpoint
def test_user_cannot_access_admin():
    user_token = login_as_user()
    response = api_call("/admin", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 403

# Test: User cannot access other user's data
def test_user_data_isolation():
    user1_token = login_as_user("user1")
    response = api_call("/users/user2/profile", headers={"Authorization": f"Bearer {user1_token}"})
    assert response.status_code == 403
```

### Injection Testing

```python
# Test: SQL injection prevented
def test_sql_injection_prevented():
    malicious_input = "admin' OR '1'='1"
    result = get_user(username=malicious_input)
    assert result is None  # Should not return admin user

# Test: XSS prevented
def test_xss_prevented():
    malicious_script = "<script>alert('XSS')</script>"
    response = create_comment(text=malicious_script)
    assert "<script>" not in response.html
    assert "&lt;script&gt;" in response.html  # Properly escaped
```

---

## Threat Modeling (STRIDE)

### STRIDE Analysis Template

```markdown
## Threat Model: {Component Name}

### Spoofing
- Threat: Attacker impersonates legitimate user
- Mitigation: JWT with strong signing algorithm (RS256)
- Status: ✓ Implemented

### Tampering
- Threat: Request/response modification in transit
- Mitigation: TLS 1.3 for all communications
- Status: ✓ Implemented

### Repudiation
- Threat: User denies performing action
- Mitigation: Audit logging of all state-changing operations
- Status: ⚠ Partial (missing for some admin actions)

### Information Disclosure
- Threat: Sensitive data exposed in logs/errors
- Mitigation: Sanitize logs, generic error messages
- Status: ❌ Not implemented

### Denial of Service
- Threat: Resource exhaustion through API abuse
- Mitigation: Rate limiting, input validation
- Status: ✓ Implemented

### Elevation of Privilege
- Threat: User gains unauthorized permissions
- Mitigation: RBAC, authorization checks on all endpoints
- Status: ⚠ Partial (missing checks on 3 endpoints)
```

---

## Compliance Checklists

### GDPR Compliance

```markdown
- [ ] Data minimization implemented
- [ ] User consent mechanism
- [ ] Right to access (data export)
- [ ] Right to erasure (data deletion)
- [ ] Right to portability
- [ ] Data breach notification process
- [ ] Privacy policy published
- [ ] Data protection impact assessment
- [ ] Encryption for personal data
- [ ] Data retention policies defined
```

### OWASP ASVS (Level 2)

```markdown
Authentication:
- [x] V2.1.1: Password length 8-128 characters
- [x] V2.1.2: Password complexity requirements
- [x] V2.1.3: No password reuse (last 3)
- [ ] V2.1.11: MFA for sensitive operations

Session Management:
- [x] V3.2.1: Session tokens use secure random generator
- [x] V3.2.2: Session token entropy ≥64 bits
- [x] V3.3.1: Session timeout after inactivity
- [ ] V3.3.4: Session invalidation on logout

Access Control:
- [x] V4.1.1: Authorization checked on all endpoints
- [ ] V4.1.5: Access control failures logged
- [x] V4.2.1: Deny by default
```

---

## Security Metrics

### Vulnerability Metrics

```
Vulnerability Density = Total Vulnerabilities / KLOC
Target: <5 vulnerabilities per 1000 lines of code

Critical Vulnerability Count
Target: 0

Mean Time to Remediate (MTTR)
- Critical: <24 hours
- High: <7 days
- Medium: <30 days
- Low: <90 days
```

### Security Coverage

```
Security Test Coverage = (Security Tests / Total Tests) × 100%
Target: ≥20%

Security Requirement Coverage = (Implemented / Total) × 100%
Target: 100% for MUST requirements

Dependency Vulnerability Coverage = (Scanned Deps / Total Deps) × 100%
Target: 100%
```

---

## Tool Access

Required tools:
- `Read`: Read code, configurations, requirements
- `Bash`: Execute security scanning tools
- `Grep`: Search for security patterns
- `Glob`: Find files to scan

Required software:
- bandit: Python SAST
- safety: Dependency scanning
- semgrep: Semantic code analysis
- trivy: Container scanning
- checkov: IaC scanning
- gitleaks: Secret detection

---

## Integration Points

### With doc-flow
- Validate security requirements in REQ documents
- Check security traceability (REQ → Implementation)
- Generate security documentation

### With code-review
- Share vulnerability findings
- Coordinate security fixes
- Track security metrics

### With test-automation
- Generate security test cases
- Validate security controls
- Track security test coverage

### With devops-flow
- Security scanning in CI/CD
- Block deployments with critical issues
- Infrastructure security validation

---

## Best Practices

1. **Shift left**: Security testing early in development
2. **Defense in depth**: Multiple security layers
3. **Least privilege**: Minimal access by default
4. **Fail securely**: Secure defaults on errors
5. **Keep it simple**: Complexity is enemy of security
6. **Assume breach**: Plan for compromise
7. **Zero trust**: Verify everything
8. **Security by design**: Not an afterthought
9. **Regular audits**: Continuous security assessment
10. **Incident response**: Plan and test response procedures

---

## Limitations

1. Cannot detect all vulnerability types (e.g., business logic flaws)
2. May produce false positives (requires manual review)
3. Depends on tool database currency
4. Cannot test runtime behavior fully
5. Limited threat modeling automation

---

## Success Criteria

- Zero critical vulnerabilities in production
- <5 high severity vulnerabilities
- 100% security requirement coverage
- All dependencies with no known CVEs
- No secrets in code repository
- Security score ≥80/100
- OWASP Top 10 coverage: 10/10

---

## Notes

- Security audits run automatically in CI/CD
- Critical vulnerabilities block deployment
- Vulnerability reports saved to `reports/security/`
- Monthly comprehensive security review recommended
- Penetration testing recommended quarterly
- Security guidelines documentation for development team required

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-08 | Initial skill creation with YAML frontmatter standardization |
