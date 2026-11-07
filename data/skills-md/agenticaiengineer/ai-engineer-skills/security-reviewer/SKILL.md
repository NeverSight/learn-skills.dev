---
name: security-reviewer
description: Security code reviewer. Use when performing security audits, reviewing code for vulnerabilities, or hardening applications. Covers OWASP Top 10 and common vulnerability patterns.
disable-model-invocation: true
argument-hint: [file-or-directory]
---

# Security Review

Perform a comprehensive security review of $ARGUMENTS:

## Check for OWASP Top 10

1. **Injection** (SQL, NoSQL, OS Command, LDAP)
   - Look for string concatenation in queries
   - Check for parameterized queries / prepared statements
   - Check for ORM misuse (raw queries)

2. **Broken Authentication**
   - Check password hashing (bcrypt/scrypt/argon2, not MD5/SHA1)
   - Check session management and token expiry
   - Look for hardcoded credentials

3. **Sensitive Data Exposure**
   - Check for secrets in code (API keys, passwords, tokens)
   - Verify encryption at rest and in transit
   - Check logging for PII/sensitive data leaks

4. **XML External Entities (XXE)**
   - Check XML parser configuration
   - Verify external entity processing is disabled

5. **Broken Access Control**
   - Check authorization on every endpoint
   - Look for IDOR vulnerabilities
   - Verify RBAC/ABAC implementation

6. **Security Misconfiguration**
   - Check HTTP headers (CORS, CSP, HSTS)
   - Look for debug mode in production
   - Check default credentials

7. **Cross-Site Scripting (XSS)**
   - Check output encoding/escaping
   - Look for `dangerouslySetInnerHTML`, `innerHTML`, `| safe`
   - Verify CSP headers

8. **Insecure Deserialization**
   - Check for untrusted deserialization
   - Verify input validation before deserialization

9. **Using Components with Known Vulnerabilities**
   - Check for outdated dependencies
   - Run `npm audit` / `pip audit` / `cargo audit`

10. **Insufficient Logging & Monitoring**
    - Verify auth events are logged
    - Check for sensitive data in logs

## Output Format
Provide findings as:
- **CRITICAL**: Exploitable vulnerabilities
- **HIGH**: Likely exploitable or high-impact issues
- **MEDIUM**: Defense-in-depth improvements
- **LOW**: Best practice recommendations

For each finding: describe the issue, show the vulnerable code, explain the risk, and provide the fix.
