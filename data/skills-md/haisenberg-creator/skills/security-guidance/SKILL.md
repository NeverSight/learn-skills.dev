---
name: security-guidance
description: Perform real-time or on-demand security audits, scan for top vulnerability classes (OWASP Top 10, CWE Top 25, hardcoded secrets, injection, XSS, SSRF, IDOR), and apply secure-by-default mitigations. Use when the user requests a security review, vulnerability scan, security audit, code hardening, or asks to check code for security issues.
---

# Security Guidance & Code Audit

This skill provides a multi-layer security auditing framework to detect, prevent, and remediate security vulnerabilities across code changes and project assets.

---

## 1. Core Review Tiers

When performing a security review, evaluate the target codebase or git diff across three layers:

1. **Pattern & Secret Audit (Zero-Cost Baseline)**
   - Scan for hardcoded API keys, JWT secrets, passwords, private keys, and token strings.
   - Scan for dangerous function usages (`eval()`, `exec()`, `dangerouslySetInnerHTML`, `pickle.loads()`, `child_process.exec()`, un-parameterized SQL queries).

2. **Diff & Input Boundary Review (Turn Level)**
   - Review incoming request validation (zod, joi, type guards) at system boundaries.
   - Verify proper encoding and sanitization of dynamic output values.
   - Verify access control, authentication, and authorization checks on new or modified endpoints.

3. **Agentic Deep Cross-File Audit (Commit / Release Level)**
   - Trace data flow from user inputs (HTTP parameters, body, headers, WebSocket events) to sinks (Database queries, shell commands, file paths, external API calls).
   - Check multi-tenant data isolation and object-level permissions (IDOR).

---

## 2. Key Vulnerability Classes & Detection Rules

### A. Secret Exposure & Credential Hygiene

- **High Risk**: Hardcoded API keys (e.g. `sk_live_...`, `AKIA...`), database URI password strings, OAuth secrets, RSA/EC private keys.
- **Mitigation**: Environment variables (`process.env`, `.env.local`), secret managers (AWS Secrets Manager, Vault), `.gitignore` audit for key files.

### B. Injection Attacks

- **SQL / NoSQL Injection**: String interpolation/concatenation in SQL query strings (`SELECT * FROM users WHERE id = '${id}'`).
  - _Remediation_: Parameterized queries, prepared statements, ORM bindings (Prisma, TypeORM, Drizzle).
- **Command Injection**: Passing untrusted user input to shell commands (`child_process.exec(...)`, `os.system(...)`, `subprocess.Popen(..., shell=True)`).
  - _Remediation_: Use argument vectors (`execFile`, `execFileSync`), or avoid shell calls entirely.
- **Path Traversal**: Unsanitized file path construction (`fs.readFile(path.join('/downloads', req.query.filename))`).
  - _Remediation_: Resolve absolute paths, sanitize with strict whitelist, verify `resolvedPath.startsWith(baseDir)`.

### C. Cross-Site Scripting (XSS)

- **Reflected / Stored / DOM XSS**: Rendering raw user inputs into the DOM (`element.innerHTML = input`, React `dangerouslySetInnerHTML={{ __html: input }}`).
  - _Remediation_: Use auto-escaping templates, DOMPurify (`DOMPurify.sanitize(input)`), React text nodes (`<div>{input}</div>`), and set Content-Security-Policy (CSP) headers.

### D. Server-Side Request Forgery (SSRF)

- **Unvalidated Outbound Requests**: Fetching URLs provided directly by users (`fetch(req.query.url)`).
  - _Remediation_: Validate scheme (`http`/`https`), enforce IP domain allowlists, resolve and block internal/loopback IPs (`127.0.0.1`, `10.0.0.0/8`, `169.254.169.254` Cloud Metadata endpoints).

### E. Broken Access Control & IDOR

- **Object Level Authorization**: Querying records by ID without checking if the authenticated user owns or has access to the record.
  - _Remediation_: Always scope database queries to the current authenticated user/org (`WHERE id = :id AND tenant_id = :currentTenant`).

### F. Cryptography & Session Management

- **Weak Randomness**: Using `Math.random()` for tokens, session IDs, passwords, or nonce generation.
  - _Remediation_: Use cryptographically secure pseudorandom generators (`crypto.randomUUID()`, `crypto.randomBytes()`).
- **Weak Password Hashing**: Plaintext passwords, MD5, SHA1, or un-salted hashes.
  - _Remediation_: Use Argon2id, bcrypt, or PBKDF2 with appropriate work factors.

---

## 3. Secure-by-Default Library Recommendations

When recommending dependencies or refactoring code, prefer proven secure-by-default libraries:

- **Web Security Headers**: `helmet` (Express/Node.js)
- **HTML Sanitization**: `dompurify` / `isomorphic-dompurify`
- **Input Validation**: `zod`, `valibot`, `joi`
- **Password Hashing**: `argon2`, `bcrypt`
- **Authentication**: `next-auth`, `clerk`, `passport` (with well-tested strategies)
- **Database Access**: Prisma, Kysely, Drizzle ORM (parameterized by default)

---

## 4. Audit Execution Workflow

When requested to run a security audit:

1. **Scope Determination**:
   - Identify the files/directories or git range (`git diff main...HEAD`).
2. **Scan & Identify**:
   - Trace all user input entry points (APIs, UI forms, CLI args, file uploads).
   - Check against the Vulnerability Classes listed above.
3. **Report & Prioritize**:
   - Categorize findings by severity (**Critical**, **High**, **Medium**, **Low**).
   - Provide concrete proof-of-concept snippets showing the vulnerable code alongside the secure replacement.
4. **Remediate**:
   - Apply fixes cleanly without altering intended business logic or introducing breaking changes.
