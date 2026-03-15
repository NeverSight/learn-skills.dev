---
name: iso-27001-controls
description: ISO 27001:2022 Annex A controls for static HTML/CSS websites on GitHub Pages
license: Apache-2.0
---

# ISO 27001:2022 Controls (Static Site)

## Purpose

Implement ISO 27001:2022 Annex A controls for Riksdagsmonitor static HTML/CSS website, ensuring systematic information security management.

## When to Use

- ✅ Implementing security controls
- ✅ ISMS audits or reviews
- ✅ Security architecture changes
- ✅ ISO 27001 certification preparation

## Key Controls for Static Sites

### A.5 - Organizational Controls

**A.5.10 - Acceptable Use**
- ✅ Political data for transparency purposes only
- ✅ Data classification: Public (all content)
- ✅ External links to CIA platform (HTTPS)

**A.5.15 - Access Control**
```yaml
# GitHub repository access
Roles:
  - Admin: Security team only
  - Write: Core maintainers
  - Read: All contributors
```

**A.5.17 - Authentication**
- ✅ GitHub MFA required for all contributors
- ✅ SSH keys or Personal Access Tokens
- ✅ GPG signing for commits

**A.5.23 - Cloud Services Security**
- ✅ GitHub Pages (vetted cloud provider)
- ✅ Service Level Agreements reviewed
- ✅ Data sovereignty: EU/US compliant

### A.8 - Technical Controls

**A.8.1 - User Endpoint Devices**
- ✅ Developer workstation security standards
- ✅ Encrypted disks required
- ✅ Antivirus/EDR software

**A.8.2 - Privileged Access Rights**
- ✅ Branch protection on main
- ✅ Required reviews for PRs
- ✅ Admin actions logged (GitHub audit)

**A.8.3 - Information Access Restriction**
```yaml
# All content is PUBLIC
Classification: Public
Restrictions: None (democratic transparency)
Access: Open to all users
```

**A.8.8 - Technical Vulnerabilities**
```yaml
# .github/workflows/security-scanning.yml
- Dependabot: Weekly scans
- CodeQL: Every PR
- Secret scanning: Enabled
- Security advisories: Monitored
```

**A.8.9 - Configuration Management**
```yaml
# All configuration in git
- index.html (14 languages)
- styles.css
- .github/workflows/*.yml
- .github/copilot-mcp.json
```

**A.8.11 - Data Masking**
- ❌ NOT applicable to Riksdagsmonitor
- **Reason**: A.8.11 applies to masking sensitive data in non-production environments
- **Context**: Riksdagsmonitor processes only **public government data** (Swedish Offentlighetsprincipen)
- **Data Type**: Public officials in official capacity (MPs, ministers, voting records, parliamentary documents)
- **Legal Basis**: GDPR Article 6(1)(e) public interest, Article 9(2)(e) manifestly public political opinions
- **Journalist Exemption**: Swedish Press Freedom Act (Tryckfrihetsförordningen)
- **No Masking Needed**: All data is public, no test environments with production data copies

**More Appropriate Controls**:
- ✅ **A.5.33** - Protection of records (source attribution, audit trails via Git)
- ✅ **A.5.34** - Privacy and protection of PII (public officials, official capacity only)
- ✅ **A.8.10** - Information deletion (retention policies, no excessive storage)
- ✅ **A.8.19** - Security of information in use (HTTPS-only, CSP headers)

**A.8.23 - Web Filtering**
```html
<!-- Content Security Policy -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self'; 
               style-src 'self' 'unsafe-inline'; 
               img-src 'self' data: https:; 
               frame-ancestors 'none';">

<!-- Additional security headers via HTTP -->
<!-- X-Frame-Options: DENY -->
<!-- X-Content-Type-Options: nosniff -->
<!-- Strict-Transport-Security: max-age=31536000 -->
```

**A.8.24 - Cryptography**
- ✅ TLS 1.3 enforced (GitHub Pages)
- ✅ HTTPS-only (no HTTP allowed)
- ✅ HSTS preload enabled
- ✅ Perfect forward secrecy

**A.8.28 - Secure Coding**
- ✅ HTML5/CSS3 validation (HTMLHint, CSSLint)
- ✅ Semantic HTML (accessibility)
- ✅ No inline scripts (CSP)
- ✅ Link integrity checking (linkinator)

### A.14 - Development Controls

**A.14.2.1 - Secure Development Policy**
- ✅ See: [Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)
- ✅ Security requirements gathering
- ✅ Threat modeling (STRIDE)
- ✅ Security testing (validation, scanning)

**A.14.2.5 - Engineering Principles**
- ✅ Defense in depth (multiple security layers)
- ✅ Least privilege (minimal GitHub permissions)
- ✅ Fail securely (static content, no dynamic errors)
- ✅ Separation of duties (PR reviews required)

**A.14.2.8 - System Security Testing**
```yaml
# Automated security testing
Testing:
  - HTML validation: HTMLHint
  - Link checking: linkinator
  - Dependency scanning: Dependabot
  - Secret scanning: GitHub
  - Security headers: manual verification
```

**A.14.2.9 - Acceptance Testing**
- ✅ All quality checks passed
- ✅ No broken links
- ✅ WCAG 2.1 AA compliance
- ✅ Security headers verified
- ✅ HTTPS-only confirmed

### A.16 - Incident Management

**A.16.1.4 - Security Events**
```markdown
## Incident Response Procedure

Severity Levels:
- CRITICAL: Site defacement, data breach
- HIGH: Security misconfiguration, XSS vulnerability
- MEDIUM: Broken links, accessibility issues
- LOW: Cosmetic issues, minor typos

Response Times:
- CRITICAL: 4 hours
- HIGH: 24 hours
- MEDIUM: 7 days
- LOW: 30 days
```

## Control Implementation Checklist

**For Each Control:**
1. ✅ Control reference documented
2. ✅ Applicability determined (static site context)
3. ✅ Implementation completed
4. ✅ Evidence collected (configs, screenshots)
5. ✅ Testing performed
6. ✅ Documentation updated

## ISMS Documentation

**Required Documents:**
- ✅ **SECURITY_ARCHITECTURE.md** - Current security design
- ✅ **FUTURE_SECURITY_ARCHITECTURE.md** - Planned improvements
- ✅ **ARCHITECTURE.md** - System architecture
- ✅ **THREAT_MODEL.md** - STRIDE analysis
- ✅ **SECURITY.md** - Security policy and reporting

**Statement of Applicability (SOA):**
- Document all Annex A controls
- Justify inclusion/exclusion
- Track implementation status

## Compliance Verification

```bash
#!/bin/bash
# iso27001-static-site-check.sh

echo "=== ISO 27001 Compliance Check (Static Site) ==="

# A.8.8 - Vulnerability scanning
echo "Checking dependencies (A.8.8)..."
npm audit
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi

# A.8.23 - Security headers
echo "Checking security headers (A.8.23)..."
curl -I https://riksdagsmonitor.com | grep -q "Strict-Transport-Security"
if [ $? -eq 0 ]; then echo "✅ PASS: HSTS"; else echo "❌ FAIL: Missing HSTS"; fi

# A.8.24 - TLS configuration
echo "Checking TLS (A.8.24)..."
echo | openssl s_client -connect riksdagsmonitor.com:443 2>&1 | grep -q "TLSv1.3"
if [ $? -eq 0 ]; then echo "✅ PASS: TLS 1.3"; else echo "❌ WARN: Check TLS version"; fi

# A.8.28 - HTML validation
echo "Validating HTML (A.8.28)..."
htmlhint index.html
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi

# A.14.2.8 - Link checking
echo "Checking links (A.14.2.8)..."
linkinator https://riksdagsmonitor.com/ --recurse --silent
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL: Broken links"; fi

echo "=== Check Complete ==="
```

## ISMS Policy References

- **Information Security Policy**: https://github.com/Hack23/ISMS-PUBLIC/blob/main/policies/information-security-policy.md
- **Risk Management Policy**: https://github.com/Hack23/ISMS-PUBLIC/blob/main/policies/risk-management-policy.md
- **All Policies**: https://github.com/Hack23/ISMS-PUBLIC/tree/main/policies

## References

- **ISO/IEC 27001:2022**: https://www.iso.org/standard/27001
- **ISO/IEC 27002:2022**: https://www.iso.org/standard/75652.html
- **SECURITY_ARCHITECTURE.md**: Current security controls
- **ARCHITECTURE.md**: System design
