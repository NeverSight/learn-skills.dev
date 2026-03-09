---
name: testing-security
description: Test application security vulnerabilities
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Security Testing

Identify vulnerabilities, security weaknesses, and potential threats in applications and infrastructure.

## When to use me

Use this skill when:
- Developing applications handling sensitive data
- Complying with security standards (ISO 27001, SOC 2, HIPAA)
- Preparing for security audits or penetration tests
- Testing authentication and authorization systems
- Checking for common vulnerabilities (OWASP Top 10)
- Validating input validation and sanitization
- Ensuring secure configuration and deployment

## What I do

- Vulnerability scanning for known security issues
- Penetration testing to simulate real attacks
- Authentication and authorization testing
- Input validation and injection testing
- Security configuration review
- Data protection and encryption testing
- Session management and cookie security testing
- API security testing and rate limiting checks

## Examples

```bash
# Security scanning tools
npm audit                         # Node.js dependency vulnerabilities
snyk test                        # Snyk vulnerability scanning
trivy image myapp:latest         # Container vulnerability scanning
bandit -r src/                   # Python security scanner
gosec ./...                     # Go security checker

# SAST (Static Application Security Testing)
semgrep scan --config auto       # Semgrep SAST
brakeman -A -w1                  # Ruby on Rails security scanner
sonarqube scan                  # Comprehensive code analysis

# DAST (Dynamic Application Security Testing)
zap-baseline.py -t https://app.example.com  # OWASP ZAP
nikto -h https://app.example.com             # Web server scanner

# Dependency checking
npm audit fix                   # Fix Node.js vulnerabilities
bundler-audit check             # Ruby gem vulnerabilities
pip-audit                      # Python package vulnerabilities
```

## Output format

```
Security Test Results:
──────────────────────────────
Critical Vulnerabilities (3):
  ❌ SQL Injection in user search endpoint
    Risk: High | CVE-2023-12345
    Fix: Use parameterized queries
    
  ❌ Hard-coded API key in config file
    Risk: Critical | CWE-798
    Fix: Move to environment variables
    
  ❌ Missing rate limiting on login endpoint
    Risk: Medium | CWE-770
    Fix: Implement rate limiting

Medium Vulnerabilities (7):
  ⚠️ Missing security headers (CSP, HSTS)
  ⚠️ Verbose error messages expose system info
  ⚠️ Session timeout too long (24 hours)

Dependency Vulnerabilities:
  ⚠️ lodash 4.17.15: Prototype pollution (CVE-2020-8203)
  ✅ All other dependencies up to date

Summary: 3 critical, 7 medium issues found
Recommendation: Fix critical issues before release
```

## Notes

- Follow OWASP Top 10 for web application security
- Test both authenticated and unauthenticated access
- Check for business logic vulnerabilities
- Consider threat modeling during design phase
- Implement security in CI/CD pipeline
- Regular security scanning and penetration testing
- Keep dependencies updated with security patches
- Educate developers on secure coding practices
