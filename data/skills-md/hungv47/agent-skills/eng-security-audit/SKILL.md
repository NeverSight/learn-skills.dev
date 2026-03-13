---
name: eng-security-audit
description: This skill should be used when the user asks to "audit security", "check for vulnerabilities", "security review", "find security issues", "pentest the code", "check for SQL injection", "review auth security", or mentions security audit, vulnerability assessment, OWASP, security hardening, or penetration testing. Comprehensive security vulnerability assessment covering OWASP Top 10 and beyond.
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
---

# Security Audit Skill

## Core Principle

Never trust anything from outside your control. Every external input is a potential attack vector.

---

## Phase 1: Threat Surface Mapping

Before auditing, identify what you're protecting and where attacks can come from.

### Questions to Answer

1. What sensitive data does this app handle? (PII, payments, auth tokens, health data)
2. What are all the entry points? (APIs, forms, file uploads, webhooks, URL params)
3. What external services does it connect to? (databases, third-party APIs, cloud services)
4. Who are the user types and what should each access?
5. What's the deployment environment? (cloud provider, containers, serverless)

### Output

```markdown
## Threat Surface Map

**Sensitive Data:**
- [List all sensitive data types and where they're stored]

**Entry Points:**
- [List all ways data enters the system]

**External Connections:**
- [List all third-party integrations and data flows]

**User Roles:**
- [List roles and their intended access levels]

**Infrastructure:**
- [Deployment environment details]
```

---

## Phase 2: Vulnerability Audit Checklist

Work through each category systematically. Flag issues with severity levels.

### Severity Levels

- **CRITICAL**: Immediate exploitation possible, data breach or system takeover risk
- **HIGH**: Exploitable with some effort, significant damage potential
- **MEDIUM**: Requires specific conditions, limited impact
- **LOW**: Minor issue, defense-in-depth concern

---

### 2.1 Input Validation & Sanitization

**Check for:**

```markdown
[ ] SQL Injection
    - Are all database queries parameterized?
    - Any string concatenation in SQL statements?
    - ORMs configured to prevent raw query injection?

[ ] XSS (Cross-Site Scripting)
    - Is user input escaped before rendering in HTML?
    - Are Content-Security-Policy headers set?
    - React/Vue auto-escaping relied upon correctly?
    - Any use of dangerouslySetInnerHTML or v-html?

[ ] Command Injection
    - Any user input passed to shell commands?
    - Using child_process, exec, eval, or system calls?

[ ] Path Traversal
    - File paths constructed from user input?
    - Checking for ../ sequences?
    - Restricting file access to intended directories?

[ ] SSRF (Server-Side Request Forgery)
    - URLs accepted from users for fetching?
    - Validating/whitelisting allowed domains?
    - Blocking internal IP ranges (127.0.0.1, 10.x, 192.168.x)?

[ ] XML/JSON Injection
    - External entity processing disabled in XML parsers?
    - JSON parsing with strict mode?

[ ] Input Boundaries
    - Maximum lengths enforced on all inputs?
    - File upload size limits?
    - Rate limiting on input endpoints?
    - Type checking (expecting number, getting string)?
```

**Common Vulnerable Patterns:**

```javascript
// BAD: SQL Injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD: Parameterized
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// BAD: Command Injection
exec(`convert ${userFilename} output.png`);

// GOOD: Avoid shell, use specific args
execFile('convert', [sanitizedFilename, 'output.png']);

// BAD: Path Traversal
const file = fs.readFileSync(`./uploads/${userInput}`);

// GOOD: Validate and restrict
const safePath = path.basename(userInput);
const fullPath = path.join(UPLOAD_DIR, safePath);
if (!fullPath.startsWith(UPLOAD_DIR)) throw new Error('Invalid path');
```

---

### 2.2 Authentication

**Check for:**

```markdown
[ ] Password Security
    - Passwords hashed with bcrypt/argon2/scrypt? (NOT md5/sha1)
    - Salt unique per password?
    - Minimum password complexity enforced?
    - Password breach checking (HaveIBeenPwned API)?

[ ] Session Management
    - Session tokens cryptographically random?
    - Tokens regenerated after login?
    - Session timeout implemented?
    - Secure and HttpOnly flags on session cookies?
    - SameSite attribute set?

[ ] JWT Security (if applicable)
    - Algorithm explicitly set (not 'none')?
    - Secret key strong and not hardcoded?
    - Token expiration enforced?
    - Sensitive data excluded from payload?
    - Refresh token rotation implemented?

[ ] Multi-Factor Authentication
    - Available for sensitive accounts?
    - Backup codes properly secured?
    - TOTP implementation using established libraries?

[ ] Brute Force Protection
    - Account lockout after failed attempts?
    - Progressive delays?
    - CAPTCHA after threshold?
    - IP-based rate limiting?

[ ] Password Reset
    - Reset tokens single-use and time-limited?
    - Token transmitted securely (HTTPS only)?
    - Old sessions invalidated after reset?
    - No username enumeration via reset flow?
```

**Common Vulnerable Patterns:**

```javascript
// BAD: Weak hashing
const hash = crypto.createHash('md5').update(password).digest('hex');

// GOOD: Use bcrypt
const hash = await bcrypt.hash(password, 12);

// BAD: Predictable session
const sessionId = `user_${Date.now()}`;

// GOOD: Cryptographically random
const sessionId = crypto.randomBytes(32).toString('hex');

// BAD: JWT with no expiration
const token = jwt.sign({ userId }, secret);

// GOOD: Short expiration
const token = jwt.sign({ userId }, secret, { expiresIn: '15m' });
```

---

### 2.3 Authorization (Access Control)

**Check for:**

```markdown
[ ] IDOR (Insecure Direct Object Reference)
    - Every data access checks user ownership?
    - API endpoints verify user can access requested resource?
    - No reliance on obscurity of IDs?

[ ] Privilege Escalation
    - Role checks on every privileged action?
    - Admin functions properly gated?
    - Can users modify their own role?

[ ] Horizontal Access
    - User A cannot access User B's data by changing IDs?
    - Bulk operations check permissions on all items?

[ ] Vertical Access
    - Regular users cannot access admin endpoints?
    - Role hierarchy properly enforced?

[ ] Function-Level Access
    - Every API endpoint has authorization check?
    - Default deny policy in place?
    - Middleware consistently applied?
```

**Common Vulnerable Patterns:**

```javascript
// BAD: No ownership check
app.get('/api/documents/:id', async (req, res) => {
  const doc = await Document.findById(req.params.id);
  res.json(doc);
});

// GOOD: Verify ownership
app.get('/api/documents/:id', async (req, res) => {
  const doc = await Document.findOne({
    _id: req.params.id,
    userId: req.user.id  // Must belong to requesting user
  });
  if (!doc) return res.status(404).json({ error: 'Not found' });
  res.json(doc);
});

// BAD: Role in client-controlled data
const isAdmin = req.body.isAdmin;

// GOOD: Role from verified session
const isAdmin = req.user.role === 'admin';
```

---

### 2.4 Secrets Management

**Check for:**

```markdown
[ ] No Hardcoded Secrets
    - API keys not in source code?
    - Database credentials externalized?
    - No secrets in client-side code?
    - Git history clean of committed secrets?

[ ] Environment Variables
    - .env files in .gitignore?
    - Production secrets not in version control?
    - Different secrets per environment?

[ ] Secret Storage
    - Using secret manager (AWS Secrets Manager, Vault, etc.)?
    - Secrets encrypted at rest?
    - Access to secrets audited?

[ ] Key Rotation
    - Process for rotating compromised keys?
    - Services handle rotation gracefully?

[ ] Exposure Prevention
    - Secrets not logged?
    - Error messages don't leak secrets?
    - Secrets not in URLs?
```

**Audit Commands:**

```bash
# Search for potential secrets in codebase
grep -r "api_key\|apikey\|secret\|password\|token" --include="*.js" --include="*.ts" --include="*.py" --include="*.env*"

# Check git history for secrets
git log -p | grep -i "password\|secret\|api_key\|token"

# Use tools like truffleHog or git-secrets
trufflehog git file://./
```

---

### 2.5 Dependency Security

**Check for:**

```markdown
[ ] Known Vulnerabilities
    - npm audit / pip audit / cargo audit run?
    - All critical/high vulnerabilities addressed?
    - Automated scanning in CI/CD?

[ ] Dependency Hygiene
    - Lock files committed (package-lock.json, yarn.lock)?
    - Versions pinned appropriately?
    - Unused dependencies removed?

[ ] Supply Chain
    - Dependencies from trusted sources?
    - Typosquatting checks on package names?
    - Recent ownership changes investigated?
    - Minimal dependency tree preferred?

[ ] Update Policy
    - Regular update schedule?
    - Security updates prioritized?
    - Breaking changes tested before deployment?
```

**Audit Commands:**

```bash
# Node.js
npm audit
npm outdated

# Python
pip-audit
safety check

# Go
go list -m all | nancy sleuth

# General
snyk test
```

---

### 2.6 API Security

**Check for:**

```markdown
[ ] Transport Security
    - HTTPS enforced everywhere?
    - HSTS header set?
    - TLS 1.2+ only?
    - Certificate valid and not expiring soon?

[ ] Rate Limiting
    - Per-user and per-IP limits?
    - Limits on expensive operations?
    - Graduated response (warn, throttle, block)?

[ ] CORS Configuration
    - Origins explicitly whitelisted (not *)?
    - Credentials mode properly configured?
    - Preflight caching appropriate?

[ ] Request Validation
    - Schema validation on all endpoints?
    - Unexpected fields rejected or ignored?
    - Content-Type enforcement?

[ ] Response Security
    - Sensitive data filtered from responses?
    - Error messages don't leak internals?
    - Pagination prevents data dumps?
    - No stack traces in production?

[ ] API Authentication
    - Tokens transmitted in headers (not URL)?
    - Token validation on every request?
    - Scope/permission checking?
```

**Secure Headers Checklist:**

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=()
```

---

### 2.7 Database Security

**Check for:**

```markdown
[ ] Access Control
    - Application uses least-privilege database user?
    - No shared credentials between environments?
    - Database not publicly accessible?

[ ] Query Safety
    - All queries parameterized?
    - ORM configured safely?
    - Raw queries reviewed carefully?

[ ] Data Protection
    - Sensitive fields encrypted at rest?
    - PII handling compliant with regulations?
    - Backups encrypted?

[ ] Connection Security
    - SSL/TLS for database connections?
    - Connection pooling configured?
    - Idle connections terminated?
```

---

### 2.8 File Upload Security

**Check for:**

```markdown
[ ] File Validation
    - File type validated by content (magic bytes), not just extension?
    - Maximum file size enforced?
    - Filename sanitized?

[ ] Storage Security
    - Files stored outside web root?
    - No direct execution of uploaded files?
    - Unique/random filenames generated?

[ ] Malware Prevention
    - Virus scanning on uploads?
    - Image re-encoding to strip malicious payloads?

[ ] Access Control
    - Uploaded files access-controlled?
    - Signed URLs for temporary access?
```

**Dangerous File Types to Block:**

```
.exe, .dll, .bat, .cmd, .sh, .php, .jsp, .asp, .aspx,
.cgi, .pl, .py, .rb, .jar, .war, .htaccess, .config,
.svg (can contain scripts), .html, .htm
```

---

### 2.9 Error Handling & Logging

**Check for:**

```markdown
[ ] Error Messages
    - Generic errors shown to users?
    - Stack traces disabled in production?
    - No sensitive data in error responses?

[ ] Logging Security
    - Sensitive data redacted from logs?
    - Logs stored securely?
    - Log injection prevented?

[ ] Security Event Logging
    - Authentication attempts logged?
    - Authorization failures logged?
    - Admin actions logged?
    - Logs include timestamp, user, IP, action?

[ ] Monitoring
    - Alerting on suspicious patterns?
    - Anomaly detection in place?
    - Incident response plan documented?
```

---

### 2.10 Infrastructure & Deployment

**Check for:**

```markdown
[ ] Server Hardening
    - Unnecessary services disabled?
    - Default credentials changed?
    - OS and packages updated?
    - Firewall configured?

[ ] Container Security (if applicable)
    - Base images from trusted sources?
    - Images scanned for vulnerabilities?
    - Running as non-root user?
    - Secrets not baked into images?

[ ] Cloud Configuration
    - S3 buckets not public by default?
    - IAM roles follow least privilege?
    - Security groups restrictive?
    - CloudTrail/audit logging enabled?

[ ] CI/CD Security
    - Secrets not exposed in build logs?
    - Dependencies verified during build?
    - Deployment requires approval for production?
    - Infrastructure as code reviewed?
```

---

## Phase 3: Report Generation

After completing the audit, produce a structured report.

### Report Format

```markdown
# Security Audit Report

**Project:** [Name]
**Date:** [Date]
**Auditor:** [Name/AI]
**Scope:** [What was reviewed]

## Executive Summary

[2-3 sentences on overall security posture and critical findings]

## Critical Findings

[Issues requiring immediate attention]

### Finding 1: [Title]
- **Severity:** CRITICAL
- **Location:** [File/endpoint]
- **Description:** [What's wrong]
- **Impact:** [What could happen]
- **Remediation:** [How to fix]
- **Code Example:** [Before/after if applicable]

## High Priority Findings

[Same format as critical]

## Medium Priority Findings

[Same format]

## Low Priority Findings

[Same format]

## Recommendations

[General improvements beyond specific findings]

## What's Working Well

[Positive security practices observed]
```

---

## Phase 4: Remediation Guidance

When fixing issues, follow this priority:

1. **Critical**: Fix immediately, consider taking affected systems offline
2. **High**: Fix within 24-48 hours
3. **Medium**: Fix within current sprint
4. **Low**: Add to backlog, fix opportunistically

### Remediation Principles

- Fix the root cause, not just the symptom
- Add tests that would catch the vulnerability
- Review similar code for same pattern
- Update documentation/guidelines to prevent recurrence
- Consider defense in depth (multiple layers)

---

## Quick Reference: Common Vulnerability Patterns

| Vulnerability | What to Look For | Fix |
|--------------|------------------|-----|
| SQL Injection | String concat in queries | Parameterized queries |
| XSS | User input in HTML | Escape output, CSP |
| CSRF | State-changing GET, no tokens | CSRF tokens, SameSite cookies |
| IDOR | Direct object access without auth check | Verify ownership on every request |
| Broken Auth | Weak passwords, no lockout | Strong hashing, rate limiting |
| Security Misconfiguration | Default settings, verbose errors | Harden configs, generic errors |
| Sensitive Data Exposure | Plaintext storage, weak crypto | Encryption, proper key management |
| XXE | XML parsing enabled | Disable external entities |
| Broken Access Control | Missing role checks | Default deny, check every action |
| Insecure Deserialization | Untrusted data deserialized | Avoid or sign serialized data |

---

## Tools Reference

### Static Analysis
- **JavaScript/TypeScript**: ESLint security plugins, Semgrep
- **Python**: Bandit, Safety
- **General**: SonarQube, Snyk Code

### Dependency Scanning
- npm audit, Snyk, Dependabot, OWASP Dependency-Check

### Dynamic Testing
- OWASP ZAP, Burp Suite, Nikto

### Secret Detection
- truffleHog, git-secrets, Gitleaks

### Infrastructure
- ScoutSuite (cloud), Trivy (containers), Prowler (AWS)
