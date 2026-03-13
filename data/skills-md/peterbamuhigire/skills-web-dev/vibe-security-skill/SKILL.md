---
name: Vibe Security Skill
description: This skill helps Claude write secure web applications. Use when working on any web application to ensure security best practices are followed.
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Secure Coding Guide for Web Applications

## Overview

This skill provides comprehensive secure coding practices for web applications, mapped to OWASP Top 10 2025. As an AI assistant, your role is to approach code from a **bug hunter's perspective** and make applications **as secure as possible** without breaking functionality.

**Key Principles:**
- Defense in depth: Never rely on a single security control
- Fail securely: When something fails, fail closed (deny access)
- Least privilege: Grant minimum permissions necessary
- Input validation: Never trust user input, validate everything server-side
- Output encoding: Encode data appropriately for the context it's rendered in

**Deployment Context:** Apps deploy across Windows (dev), Ubuntu (staging), and Debian (production). Security must work on all platforms:
- File permissions differ: test upload dirs and temp paths on Linux
- Case-sensitive filesystems on Linux can expose hidden files if not careful
- Use `utf8mb4_unicode_ci` collation to prevent charset-based injection edge cases
- Never hardcode Windows paths; use `DIRECTORY_SEPARATOR` or `/`

**OWASP Top 10 2025:** A01 Broken Access Control • A02 Security Misconfiguration • A03 Supply Chain • A04 Cryptographic Failures • A05 Injection • A06 Insecure Design • A07 Authentication Failures • A08 Data Integrity Failures • A09 Logging Failures • A10 Exception Handling

📖 **See `references/owasp-mapping.md` for complete vulnerability → OWASP mapping**

---

## Critical Real-World Vulnerabilities (AI Code Generation Blind Spots)

AI-generated code often misses these fundamental security issues. **Check EVERY generated application for these before deployment:**

### 1. Plain Text Passwords & Missing Rate Limiting

**Common Mistakes:**
- Storing passwords in plain text in database
- No rate limiting on login endpoints (allows brute force attacks)
- Using weak hashing like MD5 or SHA-1

**Requirements:**
- ✅ Use Argon2id, bcrypt, or scrypt for password hashing
- ✅ Implement rate limiting: 5 failed login attempts → 15 minute lockout
- ✅ Rate limit by both IP and username
- ✅ Never store or log plain text passwords

### 2. User Data Exposure (MOST COMMON)

**The Problem:**
Almost every AI-generated app lets any logged-in user access other users' data by manipulating API requests. Example: `GET /api/users/124/profile` returns ANY user's data.

**Root Cause:**
No ownership verification in API endpoints. Authorization checks only at route level, not data level.

**Required Fix:**
```
EVERY data access endpoint must verify:
1. The current user owns the requested resource, OR
2. The current user's organization owns the resource (multi-tenant), OR
3. The current user has explicit permission to access it

Return 404 (not 403) for unauthorized access to prevent resource enumeration
```

**Multi-Tenant Apps:**
- ALL queries must be scoped to current user's organization: `WHERE org_id = ?`
- No user should ever see another organization's data
- Verify org_id on every database query

### 3. Unverified Payment Webhooks

**The Problem:**
Apps accept Stripe/PayPal webhooks without signature verification, allowing anyone to fake payment confirmations and unlock paid features.

**Attack:**
```bash
curl -X POST https://yourapp.com/webhook/stripe \
  -d '{"type":"checkout.session.completed","payment_status":"paid"}'
# App grants access without verifying this came from Stripe
```

**Required Fix:**
```
✅ ALWAYS verify webhook signatures using the provider's SDK
✅ Use webhook secret from provider dashboard (environment variable)
✅ Reject requests with invalid signatures
✅ Use idempotency keys to prevent duplicate processing
```

### 4. API Keys Hardcoded in Frontend

**The Problem:**
Secret API keys (Stripe `sk_live_*`, OpenAI `sk-proj-*`, AWS keys) visible in JavaScript bundle, HTML, or LocalStorage.

**Common Locations:**
- JavaScript bundle files
- Source maps (.map files)
- HTML data attributes
- Environment variables exposed via build tools (`NEXT_PUBLIC_*`, `REACT_APP_*`)

**Required Fix:**
```
✅ Frontend: Only use PUBLIC/PUBLISHABLE keys (Stripe pk_*, client-safe keys)
✅ Backend: All secret operations (payment processing, AI calls, etc.) server-side only
✅ Never expose: sk_*, secret keys, AWS credentials, database passwords
✅ Check compiled bundles for leaked secrets before deployment
```

### 5. No Input Validation

**The Problem:**
Forms accept any input without validation. Search bars execute JavaScript. No SQL parameterization.

**Required Fix:**
```
✅ Server-side validation on ALL inputs (never trust client-side alone)
✅ Validate data types: integers, emails, enums
✅ Whitelist allowed values for dropdowns/selections
✅ Parameterized SQL queries (NEVER string concatenation)
✅ Output encoding based on context (HTML, JS, URL, SQL)
✅ File upload validation: type, size, magic bytes
✅ PHP: Use finfo magic bytes validation (not user-supplied Content-Type)
```

### 6. No Row-Level Security / Privacy Rules

**The Problem:**
Database allows any authenticated user to read all data. No privacy policies enforced.

**Required Fix:**
```
✅ Database views or row-level security policies where supported
✅ Application-level: EVERY query filters by owner_id or org_id
✅ Multi-tenant: Tenant ID in every table, every query includes tenant filter
✅ Test: Can user A access user B's data? (should be NO)
```

### How to Prevent These Issues When Working with AI

**1. Security-First Prompting:**
```
❌ Bad:  "Create a login API"
✅ Good: "Create a login API with bcrypt hashing, rate limiting (5 attempts per 15min),
         CSRF protection, and authorization checks that verify resource ownership"
```

**2. Always Review AI-Generated Code For:**
- [ ] Authentication on protected endpoints
- [ ] Authorization (ownership verification) on data access
- [ ] Rate limiting on login/sensitive endpoints
- [ ] Webhook signature verification
- [ ] Parameterized SQL queries
- [ ] No secrets in frontend code
- [ ] Input validation server-side
- [ ] Output encoding for XSS prevention

**3. Test Authorization Explicitly:**
```bash
# Can user1 access user2's data? (should fail)
curl -H "Authorization: Bearer user1_token" https://api/users/user2_id/profile

# Test rate limiting
for i in {1..20}; do curl -X POST https://api/login -d "user=test&pass=wrong"; done

# Test input validation
curl -X POST https://api/search -d "q=<script>alert(1)</script>"
```

---

## OWASP Top 10 2025 - Quick Reference

### A01:2025 - Broken Access Control

**Vulnerabilities:**
- IDOR (Insecure Direct Object Reference)
- Missing authorization checks
- Privilege escalation
- Multi-tenant data leakage

**Prevention Checklist:**
- [ ] Verify resource ownership on EVERY data access
- [ ] Use UUIDs instead of sequential IDs
- [ ] Scope all queries to current user/org: `WHERE org_id = ? AND id = ?`
- [ ] Return 404 (not 403) for unauthorized access
- [ ] Test with different user roles

📖 **See `references/access-control.md` for detailed patterns**

### A02:2025 - Security Misconfiguration

**Common Issues:**
- Missing security headers
- Debug mode enabled in production
- Default credentials active
- Verbose error messages

**Prevention Checklist:**
- [ ] Disable debug mode in production
- [ ] Set all security headers (CSP, HSTS, X-Content-Type-Options, X-Frame-Options)
- [ ] Remove default accounts
- [ ] Hide server version information
- [ ] Configure Content Security Policy

### A03:2025 - Software Supply Chain Failures

**Vulnerabilities:**
- Vulnerable dependencies (outdated npm/composer packages)
- Compromised packages
- No integrity checks

**Prevention Checklist:**
- [ ] Use lock files (package-lock.json, composer.lock)
- [ ] Run `npm audit` / `composer audit` regularly
- [ ] Use Dependabot or Renovate for updates
- [ ] Implement subresource integrity (SRI) for CDN resources

### A04:2025 - Cryptographic Failures

**Vulnerabilities:**
- Plain text password storage
- Weak hashing (MD5, SHA-1)
- Missing HTTPS/HSTS
- Exposed secrets

**Prevention Checklist:**
- [ ] Use Argon2id or bcrypt for passwords
- [ ] Enforce HTTPS everywhere
- [ ] Enable HSTS header
- [ ] Encrypt sensitive data at rest (AES-256-GCM)
- [ ] Store secrets in environment variables

📖 **See `references/authentication-security.md` for detailed patterns**

### A05:2025 - Injection

**Vulnerabilities:**
- SQL Injection
- XSS (Cross-Site Scripting)
- Command Injection
- XXE (XML External Entity)

**Prevention Checklist:**
- [ ] Use parameterized queries (prepared statements)
- [ ] Output encoding (context-specific: HTML, JS, URL)
- [ ] Content Security Policy (CSP)
- [ ] Disable external entities in XML parsers
- [ ] Input validation (whitelist approach)

📖 **See `references/server-side-security.md` and `references/client-side-security.md`**

### A06:2025 - Insecure Design

**Vulnerabilities:**
- No rate limiting (brute force attacks)
- Missing authorization logic in design
- Business logic flaws

**Prevention Checklist:**
- [ ] Threat modeling before development
- [ ] Rate limiting on sensitive endpoints (login, API calls)
- [ ] Security requirements in user stories
- [ ] Test business logic thoroughly

### A07:2025 - Authentication Failures

**Vulnerabilities:**
- No rate limiting on login
- Weak password policies
- Session fixation
- Insecure password reset

**Prevention Checklist:**
- [ ] Rate limiting: 5 attempts → 15 min lockout
- [ ] Strong password requirements (min 8 chars, check haveibeenpwned)
- [ ] Regenerate session ID after login
- [ ] Implement MFA for sensitive accounts
- [ ] Secure password reset with expiring tokens

📖 **See `references/authentication-security.md`**

**PHP Session Security:** Use **php-security** skill for PHP-specific session hardening (php.ini directives, session fixation/hijacking prevention, secure cookie configuration).

### A08:2025 - Software or Data Integrity Failures

**Vulnerabilities:**
- Unverified webhook signatures
- Insecure deserialization
- No code signing

**Prevention Checklist:**
- [ ] Verify webhook signatures (Stripe, PayPal, etc.)
- [ ] Use JSON instead of native serialization
- [ ] Implement subresource integrity for CDN
- [ ] Sign code releases

### A09:2025 - Security Logging and Alerting Failures

**Vulnerabilities:**
- No logging of security events
- Logs not monitored
- Logs contain sensitive data

**Prevention Checklist:**
- [ ] Log all authentication events (success/failure)
- [ ] Log authorization failures
- [ ] Set up alerts for suspicious activity
- [ ] Never log passwords, credit cards, tokens
- [ ] Centralized logging (ELK, Splunk)

### A10:2025 - Mishandling of Exceptional Conditions

**Vulnerabilities:**
- Verbose error messages (stack traces)
- Information leakage in errors
- Unhandled exceptions

**Prevention Checklist:**
- [ ] Generic error messages for users
- [ ] Detailed logs for developers (server-side only)
- [ ] Disable debug mode in production
- [ ] Custom error pages
- [ ] Catch all exceptions

---

## Quick Security Checklists

### New Feature Checklist

When implementing any new feature, verify:

- [ ] **Authentication:** Protected endpoints require valid authentication
- [ ] **Authorization:** Users can only access their own data or org data
- [ ] **Input Validation:** All inputs validated server-side (type, format, range)
- [ ] **Output Encoding:** Data encoded based on context (HTML, JS, SQL)
- [ ] **Rate Limiting:** Sensitive operations rate limited
- [ ] **SQL Injection:** Using parameterized queries
- [ ] **XSS Protection:** User input properly encoded before rendering
- [ ] **CSRF Protection:** State-changing operations protected with CSRF tokens
- [ ] **Logging:** Security events logged (login, data access, failures)
- [ ] **Error Handling:** Generic errors to users, detailed logs server-side

### API Endpoint Checklist

For every API endpoint:

- [ ] Requires authentication (except public endpoints)
- [ ] Verifies resource ownership (authorization)
- [ ] Validates all input parameters
- [ ] Uses parameterized SQL queries
- [ ] Returns appropriate HTTP status codes
- [ ] Includes security headers in response
- [ ] Logs access attempts
- [ ] Handles errors gracefully

### Database Query Checklist

For every database query:

- [ ] Uses parameterized queries (never string concatenation)
- [ ] Includes ownership filter: `WHERE owner_id = ?`
- [ ] Multi-tenant: includes org filter: `WHERE org_id = ?`
- [ ] Uses least privilege database user
- [ ] Properly indexed for performance
- [ ] Audited for sensitive data access

---

## Security Headers Reference

Include these headers in all responses:

```http
# Enforce HTTPS
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

# Prevent XSS
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.yourdomain.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self';

# Prevent MIME sniffing
X-Content-Type-Options: nosniff

# Prevent clickjacking
X-Frame-Options: DENY

# Control referrer information
Referrer-Policy: strict-origin-when-cross-origin

# Sensitive pages
Cache-Control: no-store
```

---

## General Security Principles

When generating code, always:

1. **Validate all input server-side** — Never trust client-side validation alone
2. **Use parameterized queries** — Never concatenate user input into queries
3. **Encode output contextually** — HTML, JS, URL, CSS contexts need different encoding
4. **Apply authentication checks** — On every endpoint, not just at routing
5. **Apply authorization checks** — Verify the user can access the specific resource
6. **Use secure defaults** — Deny by default, allow explicitly
7. **Handle errors securely** — Don't leak stack traces or internal details to users
8. **Keep dependencies updated** — Use tools to track vulnerable dependencies
9. **Implement rate limiting** — On authentication and sensitive operations
10. **Log security events** — For monitoring and incident response

When unsure, choose the more restrictive/secure option and document the security consideration in comments.

---

## Additional Resources

### Detailed Reference Guides

- **`references/access-control.md`** - Complete authorization patterns, IDOR prevention, multi-tenant isolation
- **`references/client-side-security.md`** - XSS, CSRF, secret exposure, detailed prevention strategies
- **`references/server-side-security.md`** - SQL injection, SSRF, XXE, path traversal, command injection
- **`references/file-upload-security.md`** - File validation, magic bytes, polyglot files, secure storage
- **`references/authentication-security.md`** - Password hashing, MFA, session management, JWT, OAuth
- **`references/owasp-mapping.md`** - Complete OWASP Top 10 2025 mapping with examples
- **`../php-security/SKILL.md`** - PHP-specific security patterns: session hardening, input validation, type juggling, php.ini configuration

### Testing Tools

```bash
# Dependency scanning
npm audit
composer audit

# Static analysis
phpstan analyze
eslint .

# Security scanning
snyk test
trivy filesystem .
```

---

**Line Count:** ~490 lines (compliant with doc-standards.md)
**Last Updated:** 2026-02-12
**Maintained by:** Peter Bamuhigire
