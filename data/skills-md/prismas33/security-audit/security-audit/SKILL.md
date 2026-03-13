---
name: security-audit
description: "Security auditing and pentesting skill. Use when asked 'analyze security', 'how would you attack', 'vulnerabilities', 'pentester mode', or 'security audit'."
metadata:
  author: Prismas33
  version: "1.0.0"
---

# Security Audit

Security auditing skill that analyzes code like a pentester, identifies vulnerabilities and suggests remediations.

---

## 🎯 When to Activate

Activate when user asks:
- "Analyze the security of..."
- "How would you attack this endpoint?"
- "Do a security audit"
- "Pentester mode"
- "Find vulnerabilities in..."
- "OWASP check"

---

## 🔍 Analysis Mode

### Approach
Think like an attacker:
1. **Reconnaissance** - What's exposed? What info leaks?
2. **Attack Vectors** - How can I exploit this?
3. **Impact** - What can I achieve if I exploit?
4. **Remediation** - How to fix?

### Expected Output
For each vulnerability found:
```markdown
### 🚨 [SEVERITY] Vulnerability Title

**Location:** `file.py:line` or `endpoint`

**What I found:**
Problem description.

**How I would attack:**
Concrete exploitation steps.

**Impact:**
What an attacker can achieve.

**Remediation:**
How to fix, with code example.
```

---

## 📋 Analysis Checklist

### 1. Authentication & Sessions
- [ ] Passwords stored with secure hash (bcrypt/argon2)?
- [ ] JWT tokens with short expiration?
- [ ] Refresh tokens implemented correctly?
- [ ] Brute force protection (rate limiting)?
- [ ] Session fixation prevented?
- [ ] Logout invalidates server-side session?

### 2. Authorization
- [ ] Permission checks on ALL endpoints?
- [ ] IDOR (Insecure Direct Object Reference) prevented?
- [ ] Privilege escalation prevented?
- [ ] Consistent role-based access control?

### 3. Injection
- [ ] SQL Injection - parameterized queries?
- [ ] NoSQL Injection prevented?
- [ ] Command Injection - inputs sanitized?
- [ ] LDAP Injection prevented?
- [ ] XPath Injection prevented?

### 4. XSS (Cross-Site Scripting)
- [ ] Output encoding on all dynamic data?
- [ ] Content-Security-Policy header?
- [ ] React/Vue auto-escaping working?
- [ ] dangerouslySetInnerHTML avoided or sanitized?

### 5. CSRF (Cross-Site Request Forgery)
- [ ] CSRF tokens in forms?
- [ ] SameSite cookies?
- [ ] Origin/Referer verification?

### 6. Sensitive Data
- [ ] HTTPS enforced?
- [ ] Sensitive data in logs?
- [ ] Hardcoded credentials in code?
- [ ] Secrets in environment variables?
- [ ] .env in .gitignore?

### 7. Security Headers
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY/SAMEORIGIN
- [ ] Strict-Transport-Security (HSTS)
- [ ] Content-Security-Policy
- [ ] X-XSS-Protection (legacy browsers)

### 8. API Security
- [ ] Rate limiting implemented?
- [ ] Input validation on all endpoints?
- [ ] Error messages don't reveal internal info?
- [ ] API versioning?
- [ ] CORS configured restrictively?

### 9. File Upload
- [ ] File type validation (not just extension)?
- [ ] Max size defined?
- [ ] Files stored outside webroot?
- [ ] Filenames sanitized?
- [ ] Antivirus scan?

### 10. Dependencies
- [ ] Dependencies updated?
- [ ] Known vulnerabilities (npm audit, pip-audit)?
- [ ] Lock files committed?

---

## 🎯 OWASP Top 10 (2021)

### A01: Broken Access Control
**Check:**
- Authentication bypass
- Access to other users' resources
- Privilege escalation
- Metadata manipulation (JWT, cookies)

### A02: Cryptographic Failures
**Check:**
- Sensitive data in plaintext
- Weak algorithms (MD5, SHA1 for passwords)
- Hardcoded keys
- Transmission without TLS

### A03: Injection
**Check:**
- SQLi, NoSQLi, Command Injection
- XSS, LDAP Injection
- Dynamic queries without parameterization

### A04: Insecure Design
**Check:**
- Missing rate limiting
- Business logic flaws
- Missing server-side validation

### A05: Security Misconfiguration
**Check:**
- Missing headers
- Debug mode in production
- Insecure defaults
- Excessive permissions

### A06: Vulnerable Components
**Check:**
- Outdated dependencies
- Known CVEs
- Abandoned libraries

### A07: Auth Failures
**Check:**
- Credential stuffing possible
- Weak password policy
- Insecure session management

### A08: Software & Data Integrity
**Check:**
- Insecure CI/CD
- Auto-update without verification
- Insecure deserialization

### A09: Logging & Monitoring
**Check:**
- Security events not logged
- Insufficient logs
- Alerts not configured

### A10: SSRF
**Check:**
- User-controlled URLs
- Internal requests exposed
- Metadata services accessible

---

## 🔧 Analysis Commands

### Python
```bash
# Dependency vulnerabilities
pip-audit

# Static analysis
bandit -r .

# Secrets in code
trufflehog .
```

### JavaScript/Node
```bash
# Dependency vulnerabilities
npm audit
pnpm audit

# Secrets
npx secretlint .
```

### General
```bash
# Secrets in git history
gitleaks detect

# General scan
trivy fs .
```

---

## 📊 Severity Levels

| Level | Description | Examples |
|-------|-------------|----------|
| 🔴 **CRITICAL** | Compromises entire system | RCE, SQLi with admin, Total auth bypass |
| 🟠 **HIGH** | Access to sensitive data | IDOR, Stored XSS, Privilege escalation |
| 🟡 **MEDIUM** | Limited impact | CSRF, Reflected XSS, Info disclosure |
| 🟢 **LOW** | Low risk | Missing headers, Verbose errors |
| ⚪ **INFO** | Best practices | Suggested improvements |

---

## 💡 Report Format

When user asks for complete audit:

```markdown
# 🔒 Security Audit Report

**Project:** [Name]
**Date:** YYYY-MM-DD
**Scope:** [What was analyzed]

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | X |
| 🟠 High | X |
| 🟡 Medium | X |
| 🟢 Low | X |

## Vulnerabilities Found

### 🔴 CRITICAL: [Title]
[Details per template above]

### 🟠 HIGH: [Title]
[...]

## Priority Recommendations

1. [Immediate action 1]
2. [Immediate action 2]
3. [Short-term action]

## Remediation Checklist

- [ ] Critical fix 1
- [ ] Critical fix 2
- [ ] ...
```

---

## 🚫 Limitations

This skill **DOES NOT replace** a professional pentest. It serves as:
- ✅ Identify obvious vulnerabilities
- ✅ Security code review
- ✅ Attack education
- ✅ Best practices checklist

**DOES NOT:**
- ❌ Real penetration testing
- ❌ Automated fuzzing
- ❌ Infrastructure scanning
- ❌ Total security guarantee
