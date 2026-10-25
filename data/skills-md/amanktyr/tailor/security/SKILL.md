---
name: security
description: Enforces security engineering principles, OWASP Top 10 defenses, zero hardcoded secrets, auth, JWT, passwords, CORS, encryption, XSS, SQLi, IDOR, SSRF, and vulnerability scanning.
---

# Security Engineering & Fortification Skill

Activate this skill when designing or implementing authentication, authorization, database access, file systems, external networking, API endpoints, cryptographic routines, or conducting security audits (`/security-audit`).

> **Zero-Trust Security Law:** *Never trust client input, never assume identity without server validation, parameterize all queries, and enforce least-privilege defense-in-depth across every boundary.*

---

## 1. Automated Secret & Pattern Scanner

Before committing code or completing any task, run the automated security scanner:

```bash
# Run deterministic secret and vulnerability checks
node skills/security/scripts/scan-secrets.js
```

---

## 2. Universal Threat Matrix & Defense Implementations

### A. Zero Hardcoded Secrets & Cryptographic Randomness (CRITICAL)
* **Insecure Anti-Pattern:**
  ```ts
  const API_KEY = "sk_live_98327498234";
  const token = Math.random().toString(36).substring(2); // Insecure PRNG
  ```
* **Secure Standard:**
  ```ts
  import crypto from 'node:crypto';

  const API_KEY = process.env.API_KEY;
  if (!API_KEY) throw new Error("CRITICAL: API_KEY is required.");

  // Cryptographically secure token generation
  const secureToken = crypto.randomBytes(32).toString('hex');
  ```

---

### B. Injection Defense: SQL, NoSQL & OS Commands (CRITICAL)

#### 1. SQL Injection (SQLi)
* **Insecure (String Interpolation):**
  ```ts
  db.query(`SELECT * FROM users WHERE email = '${email}' AND status = '${status}'`);
  ```
* **Secure (Parameterized Queries):**
  ```ts
  db.query('SELECT * FROM users WHERE email = $1 AND status = $2', [email, status]);
  ```

#### 2. NoSQL Operator Injection
* **Insecure:** Directly passing unvalidated request body into MongoDB queries:
  ```ts
  db.collection('users').findOne({ email: req.body.email, password: req.body.password });
  // Attacker sends: { email: "admin@corp.com", password: { "$gt": "" } }
  ```
* **Secure:** Validate schema strictly (e.g. Zod) to ensure values are primitive strings, never objects.

#### 3. Command Injection & Safe Process Execution
* **Forbidden:** `child_process.exec(userInput)`, `eval()`, `new Function()`.
* **Secure:** Use `child_process.execFile()` with fixed executable paths and explicit argument arrays:
  ```ts
  import { execFile } from 'node:child_process';
  execFile('/usr/bin/git', ['log', '-n', '1'], { shell: false }, (err, stdout) => { ... });
  ```

---

### C. Broken Access Control, IDOR & Mass Assignment (CRITICAL)

#### 1. Insecure Direct Object References (IDOR / BOLA)
* **Insecure:**
  ```ts
  // Vulnerable: Any authenticated user can view or delete document id 123
  app.get('/api/documents/:id', async (req, res) => {
    const doc = await db.documents.findUnique({ where: { id: req.params.id } });
    res.json(doc);
  });
  ```
* **Secure:** Always scope database lookups to the authenticated user/tenant ID:
  ```ts
  app.get('/api/documents/:id', requireAuth, async (req, res) => {
    const doc = await db.documents.findFirst({
      where: { id: req.params.id, ownerId: req.user.id }
    });
    if (!doc) return res.status(404).json({ error: "Document not found" });
    res.json(doc);
  });
  ```

#### 2. Mass Assignment / Over-Posting
* **Insecure:** `db.users.update({ where: { id }, data: req.body })` (allows setting `role: 'admin'`, `isVerified: true`).
* **Secure:** Explicitly pick allowed fields using schema validation (Zod) before updating.

---

### D. Cross-Site Scripting (XSS) & HTML Sanitization (HIGH)
* **Never inject unsanitized HTML:** Avoid `dangerouslySetInnerHTML`, `innerHTML`, `v-html`.
* **Protocols:** Sanitize user-provided URLs before rendering in `<a href={url}>` to prevent `javascript:` execution:
  ```ts
  function sanitizeUrl(rawUrl: string): string {
    const parsed = new URL(rawUrl, 'https://example.com');
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
      return parsed.href;
    }
    return '#';
  }
  ```

---

### E. Server-Side Request Forgery (SSRF) Defense (HIGH)
When your server fetches an external URL supplied by a user (webhooks, avatar imports, link previews):
* **Insecure:** `fetch(req.body.targetUrl)` (allows fetching `http://169.254.169.254/latest/meta-data/` or internal LAN services `http://192.168.1.1`).
* **Secure:**
  1. Resolve DNS first and verify the IP does NOT fall within private/reserved CIDRs (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1`).
  2. Enforce explicit protocol allowlist (`https:` only).
  3. Disable redirect following or re-verify target IP upon each redirect.

---

### F. Authentication, Passwords & Timing Attacks (CRITICAL)

1. **Password Hashing:** Always use `argon2id` or `bcrypt` (work factor >= 12). NEVER use MD5, SHA-1, or plain SHA-256.
2. **Constant-Time Comparison:** Never compare secrets (tokens, webhook signatures, hashes) with `===`.
   * **Insecure:** `if (receivedSignature === expectedSignature)`
   * **Secure:**
     ```ts
     import crypto from 'node:crypto';
     const isValid = crypto.timingSafeEqual(
       Buffer.from(receivedSignature),
       Buffer.from(expectedSignature)
     );
     ```
3. **JWT Handling:**
   * Always verify `algorithm` explicitly (reject `none`).
   * Store session credentials in `httpOnly`, `Secure`, `SameSite=Strict` cookies—never in `localStorage`.

---

### G. Path Traversal & Arbitrary File Uploads (HIGH)

#### 1. Path Traversal
* **Secure Directory Boundary Check:**
  ```ts
  import path from 'node:path';

  function safeResolve(baseDir: string, userPath: string): string {
    const resolved = path.resolve(baseDir, userPath);
    if (!resolved.startsWith(path.resolve(baseDir) + path.sep)) {
      throw new Error("Access denied: Path traversal detected.");
    }
    return resolved;
  }
  ```

#### 2. File Upload Hardening
* Generate unique random filenames on the server (e.g. `crypto.randomUUID() + ext`). Never use the user's raw filename.
* Whitelist allowed file extensions and verify file magic bytes / MIME types.
* Store uploads outside the web execution root or in dedicated object storage (S3) with restricted execution permissions.

---

### H. Denial of Service (ReDoS) & Resource Exhaustion (MEDIUM)
1. **Regular Expressions:** Avoid nested quantifiers (`(a+)+$`, `([a-zA-Z0-9]+)*`) that cause exponential backtracking. Test regexes with ReDoS checkers.
2. **Payload Size Limits:** Enforce strict body-parser limits (`express.json({ limit: '1mb' })`).
3. **Database Pagination:** Never execute unbounded queries (`SELECT * FROM table`). Always require `LIMIT` and cursor-based pagination.
4. **Rate Limiting:** Protect public endpoints (login, password reset, search, webhooks) with IP/token-based rate limiters.

---

### I. Prototype Pollution & Unsafe Deserialization (HIGH)
* Reject properties named `__proto__`, `constructor`, or `prototype` during recursive object merges or JSON processing.
* Use `Object.create(null)` for key-value dictionary lookup maps to prevent prototype lookup tampering.

---

### J. Security Headers & Transport Security (HIGH)
Always configure standard security headers (e.g., via `helmet` or reverse proxy):
* `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
* `X-Content-Type-Options: nosniff`
* `X-Frame-Options: DENY`
* `Content-Security-Policy: default-src 'self'; script-src 'self'; ...`
* `Referrer-Policy: strict-origin-when-cross-origin`

---

## 3. Mandatory Pre-Commit Security Checklist

Before marking any task complete, verify this defensive gate:
* [ ] **Zero Hardcoded Secrets:** No tokens, passwords, or keys in source code.
* [ ] **Zero SQL/NoSQL Injections:** All queries parameterized; no raw string concatenation.
* [ ] **Zero IDOR:** All record lookups and mutations verify user/tenant ownership server-side.
* [ ] **Zero XSS:** No raw HTML rendering; all links sanitized against `javascript:`.
* [ ] **Safe Path Resolution:** All file access confined to allowed base directories via `startsWith()`.
* [ ] **Constant-Time Verification:** All signature/token comparisons use `crypto.timingSafeEqual()`.
* [ ] **SSRF Guard:** No unvalidated external URL fetching to private network ranges.
* [ ] **Rate Limiting & Body Limits:** Payloads and authentication endpoints constrained.
* [ ] **Scanner Execution:** Ran `tailor security` or `node skills/security/scripts/scan-secrets.js` with exit code 0.
