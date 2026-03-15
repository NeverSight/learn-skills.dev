---
name: security-hardening
description: Security hardening and secure coding practices. Use when user asks to "harden security", "secure coding", "OWASP vulnerabilities", "input validation", "sanitization", "SQL injection prevention", "XSS protection", "CORS security", "secure headers", "vulnerability scanning", or mentions security best practices and threat mitigation.
---

# Security Hardening & Secure Coding

Comprehensive security hardening and secure coding practices to prevent common vulnerabilities.

## OWASP Top 10 (2021)

### 1. Broken Access Control
- Implement proper authorization
- Use role-based access control (RBAC)
- Verify permissions on every request

### 2. Cryptographic Failures
- Use strong encryption (AES-256)
- Protect sensitive data in transit (TLS)
- Never hardcode secrets

### 3. Injection
- Use parameterized queries for SQL
- Validate and sanitize all inputs
- Use ORM frameworks

### 4. Insecure Design
- Threat modeling during design
- Secure by default principles
- Regular security reviews

### 5. Security Misconfiguration
- Keep dependencies updated
- Remove default credentials
- Disable unnecessary features

### 6. Vulnerable Components
- Regular dependency audits
- Use vulnerability scanning tools
- Keep frameworks and libraries updated

### 7. Authentication & Session Failures
- Strong password policies
- Multi-factor authentication
- Secure session management

### 8. Software & Data Integrity Failures
- Verify package integrity
- Use signed commits
- Implement secure CI/CD

### 9. Logging & Monitoring Failures
- Log security events
- Monitor for suspicious activity
- Regular security audits

### 10. SSRF
- Validate URLs and redirects
- Restrict outbound requests
- Network-level controls

## Secure Coding Practices

### Input Validation
```javascript
// Bad
const id = req.query.id;
const user = db.query(`SELECT * FROM users WHERE id = ${id}`);

// Good
const id = parseInt(req.query.id, 10);
if (!Number.isInteger(id) || id < 1) {
  throw new Error('Invalid ID');
}
const user = db.query('SELECT * FROM users WHERE id = ?', [id]);
```

### Output Encoding
```javascript
// Bad
const html = `<div>${userName}</div>`;

// Good (escapes HTML)
const escapeHtml = (str) => str
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');
const html = `<div>${escapeHtml(userName)}</div>`;
```

### Secure Headers
```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

## Security Checklist

- [ ] All inputs validated and sanitized
- [ ] Parameterized queries used (no SQL injection)
- [ ] Sensitive data encrypted (TLS, at-rest)
- [ ] Strong authentication (MFA, strong passwords)
- [ ] CORS properly configured
- [ ] CSRF tokens used
- [ ] Security headers set
- [ ] Dependencies audited regularly
- [ ] Error messages don't leak info
- [ ] Logging captures security events
- [ ] Secrets not in code/logs
- [ ] Regular security testing

## Tools & Utilities

- `npm audit` / `pip check` - Dependency scanning
- OWASP ZAP / Burp Suite - Penetration testing
- Snyk - Vulnerability scanning
- SonarQube - Code quality and security
- TruffleHog - Secret scanning

## References

- OWASP Top 10
- OWASP Cheat Sheets
- CWE/SANS Top 25
- NIST Cybersecurity Framework
- Google Styleguide Code Review Security
