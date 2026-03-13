---
name: security-by-design
description: Strategic principles for integrating security from the start, not retrofitting it later
license: Apache-2.0
---

# Security by Design Skill

## Purpose

Apply security by design principles to ensure security is integrated from the earliest stages of development, not bolted on as an afterthought.

## Core Principles

### 1. Secure by Default
- **Principle**: Systems should be secure in their default configuration
- **Application**: 
  - Default to HTTPS, never HTTP
  - Default to least privilege access
  - Default to encrypted communications
  - Default to secure password policies
  - Disable unnecessary features by default

### 2. Defense in Depth
- **Principle**: Multiple layers of security controls protect against single point of failure
- **Application**:
  - Network security (TLS, firewalls, DDoS protection)
  - Application security (input validation, output encoding)
  - Access control (authentication, authorization, MFA)
  - Data security (encryption at rest and in transit)
  - Monitoring and detection (logging, SIEM, alerts)

### 3. Least Privilege
- **Principle**: Grant minimum necessary permissions to users, processes, and systems
- **Application**:
  - GitHub Actions: minimal required permissions
  - User roles: grant only needed access
  - Service accounts: scoped credentials
  - API tokens: limited scope and expiration
  - File permissions: restrictive by default

### 4. Fail Securely
- **Principle**: Failures should not compromise security
- **Application**:
  - Error messages don't leak sensitive info
  - Failed authentication locks out, doesn't grant access
  - Exception handling preserves security state
  - Graceful degradation maintains protection
  - Logs capture security-relevant failures

### 5. Don't Trust User Input
- **Principle**: All external input is untrusted and must be validated
- **Application**:
  - Validate all input formats
  - Sanitize before processing
  - Use parameterized queries
  - Encode output appropriately
  - Whitelist over blacklist

### 6. Keep Security Simple
- **Principle**: Complexity is the enemy of security
- **Application**:
  - Use well-tested libraries over custom code
  - Avoid complex cryptographic implementations
  - Clear, reviewable security logic
  - Minimize attack surface
  - Remove unused features and dependencies

### 7. Separation of Duties
- **Principle**: Critical operations require multiple parties
- **Application**:
  - Code review required before merge
  - Separate dev/prod environments
  - Different roles for different functions
  - No single person can compromise system
  - Audit trail for accountability

### 8. Economy of Mechanism
- **Principle**: Keep security mechanisms as simple as possible
- **Application**:
  - Avoid over-engineering security
  - Use standard protocols (TLS, OAuth)
  - Leverage platform security features
  - Document security architecture clearly
  - Regular security architecture reviews

## Static Website Security by Design

### Eliminate Server-Side Attack Surface
```
✅ Benefits of static HTML/CSS:
- No SQL injection (no database)
- No XSS from server-side rendering
- No CSRF tokens needed
- No session management vulnerabilities
- No server-side code execution risks
```

### Transport Layer Security
```
✅ Always enforce:
- HTTPS-only (TLS 1.3)
- HSTS headers (Strict-Transport-Security)
- Secure cookie flags (if any cookies used)
- Certificate pinning where appropriate
```

### Content Security
```
✅ Implement CSP headers:
Content-Security-Policy: default-src 'self'; 
  script-src 'self'; 
  style-src 'self' 'unsafe-inline' fonts.googleapis.com;
  font-src 'self' fonts.gstatic.com;
  img-src 'self' data:;
  connect-src 'self';

✅ Additional headers:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

### Dependency Security
```
✅ Minimize dependencies:
- Avoid JavaScript frameworks (for static sites)
- Use trusted CDNs (Google Fonts, etc.)
- Enable Subresource Integrity (SRI) for CDN assets
- Regular dependency scanning (Dependabot)
```

## CI/CD Security by Design

### Workflow Hardening
```yaml
# ✅ Security by design in GitHub Actions
permissions:
  contents: read  # Least privilege
  pull-requests: write  # Only if needed

jobs:
  secure-job:
    runs-on: ubuntu-latest
    
    steps:
      # 1. Harden the runner
      - uses: step-security/harden-runner@SHA
        with:
          egress-policy: audit
      
      # 2. Pin all actions to SHA
      - uses: actions/checkout@SHA
      
      # 3. Use secrets securely
      - env:
          TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Never echo secrets
          # Use secrets only where needed
```

### Supply Chain Security
```
✅ Required controls:
- Pin all GitHub Actions to SHA commits
- Enable Dependabot security updates
- Use dependency review action
- Scan with CodeQL or Semgrep
- Enable secret scanning
- Require signed commits (GPG)
```

## Secure Development Lifecycle

### Phase 1: Design
- [ ] Threat model (STRIDE analysis)
- [ ] Security requirements defined
- [ ] Compliance requirements identified
- [ ] Security architecture designed
- [ ] Risk assessment documented

### Phase 2: Development
- [ ] Secure coding standards followed
- [ ] Input validation implemented
- [ ] Output encoding applied
- [ ] Error handling secure
- [ ] Logging captures security events

### Phase 3: Testing
- [ ] SAST scanning (CodeQL)
- [ ] Dependency scanning (Dependabot)
- [ ] Secret scanning enabled
- [ ] Manual security review
- [ ] Penetration testing (if applicable)

### Phase 4: Deployment
- [ ] Secure CI/CD pipeline
- [ ] Infrastructure hardening
- [ ] Security monitoring enabled
- [ ] Incident response ready
- [ ] Rollback plan documented

### Phase 5: Operations
- [ ] Continuous monitoring
- [ ] Log analysis
- [ ] Vulnerability management
- [ ] Patch management
- [ ] Periodic security reviews

## Security Design Patterns

### Pattern: Static Site Security
```
Architecture: Static HTML/CSS on GitHub Pages

Security Controls:
✅ Attack Surface: Minimal (no server-side code)
✅ Transport: TLS 1.3 / HTTPS-only
✅ Headers: CSP, HSTS, X-Frame-Options
✅ Access: GitHub MFA, SSH keys, GPG signing
✅ Monitoring: Dependabot, CodeQL, secret scanning
✅ Recovery: Git rollback, rapid re-deploy
```

### Pattern: Defense in Depth Layers
```
Layer 1 (Network): TLS 1.3, CDN, DDoS protection
Layer 2 (Application): Static content, no dynamic processing
Layer 3 (Access Control): GitHub auth, MFA, SSH, GPG
Layer 4 (Data): Git encryption at rest, HTTPS in transit
Layer 5 (Monitoring): Logs, alerts, security scanning
Layer 6 (Response): Incident procedures, rollback capability
```

### Pattern: Least Privilege GitHub Actions
```yaml
permissions:
  # Grant only what's needed
  contents: read
  pull-requests: write  # Only if creating/updating PRs
  issues: write         # Only if managing issues
  # Deny everything else by default
```

## Security Anti-Patterns to Avoid

### ❌ Security Theater
- Don't implement controls that look secure but aren't effective
- Don't use outdated or weak crypto (MD5, SHA1, RC4)
- Don't rely on obscurity (hiding, not securing)

### ❌ Bolt-On Security
- Don't add security as afterthought
- Don't patch over insecure design
- Don't bypass security for convenience

### ❌ Over-Engineering
- Don't create complex custom security solutions
- Don't implement crypto yourself
- Don't ignore well-tested libraries

### ❌ Incomplete Implementation
- Don't secure one layer and ignore others
- Don't validate input but forget output encoding
- Don't encrypt data in transit but not at rest

## Verification Checklist

Before deploying, verify:

- [ ] **Threat Model**: STRIDE analysis complete
- [ ] **Secure Defaults**: All defaults are secure
- [ ] **Defense in Depth**: Multiple security layers
- [ ] **Least Privilege**: Minimal permissions granted
- [ ] **Input Validation**: All inputs validated
- [ ] **Output Encoding**: All outputs properly encoded
- [ ] **Error Handling**: Fails securely, no info leakage
- [ ] **Logging**: Security events captured
- [ ] **Access Control**: Authentication + authorization
- [ ] **Encryption**: Data protected in transit and at rest
- [ ] **Dependencies**: Scanned and up to date
- [ ] **Testing**: Security tests passing
- [ ] **Monitoring**: Alerts configured
- [ ] **Documentation**: Security architecture documented
- [ ] **Incident Response**: Procedures documented and tested

## Remember

- **Design First**: Security requirements before code
- **Simple is Secure**: Complexity breeds vulnerabilities
- **Layers Matter**: Defense in depth protects when one layer fails
- **Least Privilege Always**: Grant minimum necessary access
- **Fail Securely**: Errors should not compromise security
- **Trust Nothing**: Validate all external input
- **Document Everything**: Security decisions need justification

## References

- [OWASP Security by Design Principles](https://owasp.org/www-project-security-by-design-principles/)
- [NIST SP 800-160 Vol. 1](https://csrc.nist.gov/publications/detail/sp/800-160/vol-1/final)
- [Microsoft SDL](https://www.microsoft.com/en-us/securityengineering/sdl)
- [STRIDE Threat Modeling](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
