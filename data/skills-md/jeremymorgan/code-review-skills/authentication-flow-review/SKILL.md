---
name: authentication-flow-review
description: Conducts a comprehensive authentication security review covering login, sessions, tokens, and credential handling. Use when auditing authentication for vulnerabilities.
license: CC0-1.0
metadata:
  category: security
allowed-tools: Read Grep Glob Write
disable-model-invocation: true
argument-hint: "[path or scope]"
---

**Target:** $ARGUMENTS

If no target path is given above, review the entire codebase.

---

# Authentication Flow Review

> **Stack note:** The code examples and library references below use Node.js/Express conventions (`bcrypt`, `jsonwebtoken`, `zod`/`joi`, `req.body`, etc.). If the codebase uses a different language or framework, apply the same security principles and adapt the specifics — for example: `bcrypt` → `passlib`/`Argon2id` (Python), `spring-security` (Java), `bcrypt` (Go); `jsonwebtoken` → `PyJWT`, `java-jwt`, `golang-jwt/jwt`; `mongoose.set('sanitizeFilter')` → the equivalent ORM sanitization setting. Mark any checklist item Not Applicable if the concept doesn't apply to the detected stack.

Conduct a comprehensive authentication security review:

Check for:

1. Password hashing

   * Uses `bcrypt.hash()` with salt rounds ≥ 10 (ideally 12); async, not sync; no double-hashing on updates.
   * `bcrypt.compare()` used for login.
2. JWT secret/key strength & storage

   * Secrets/keys not hardcoded; loaded from env or secret manager; separate keys for access vs refresh.
   * Strong entropy (≥256-bit for HS256) or asymmetric (RS256/ES256) with rotation plan.
3. Token settings

   * Access token TTL 5–15 minutes; refresh token TTL 7–30 days; sliding sessions bounded by a max session age.
   * JWT `algorithms`, `issuer (iss)`, `audience (aud)`, `subject (sub)`, `jti`, `iat`, `exp`, and optional `nbf` are enforced in `verify`.

4. Refresh token implementation
   * Rotation on every use and reuse detection (if old RT is presented, revoke the whole session family).
   * RTs stored in HttpOnly, Secure, SameSite cookie (not localStorage); hashed at rest if persisted; per-device tracking (`jti`, `ua`, `ip`, `expiresAt`).

5. Session invalidation

   * On password change/reset, previously issued tokens are rejected (compare `pwdChangedAt` or increment `tokenVersion` vs `jwt.iat`).

6. Brute force protection

   * Rate limit login/reset/verify endpoints; progressive backoff per username+IP in a fast store (e.g., Redis); optional CAPTCHA after threshold.

7. Account enumeration defenses

   * Generic errors and identical status/timing for “user not found” vs “bad password”; optional jitter.

8. Password reset flow security

   * Reset tokens via `crypto.randomBytes(32)`, hashed at rest (SHA-256), short TTL (≤ 15–30 min), one-time use, invalidated after success.
   * No secrets in logs; throttle reset email sender.

9. Email verification

   * One-time, short-TTL verification tokens; server-side verified; no way to mark verified via mass-assignment/body fields.

10. SQL/NoSQL injection in auth paths

    * No use of user-controlled operators in filters; query sanitization enabled; no `$where`; parameterized SQL if applicable.

11. AuthZ integrity

    * Roles/permissions loaded server-side; deny-by-default; never trust role/claims purely from the JWT payload without verification and (for sensitive ops) a DB check.

12. Cookie & CSRF configuration (if cookies used)

    * `HttpOnly`, `Secure`, `SameSite=Lax|Strict`, narrow `path`/`domain`, explicit `Max-Age`.
    * CSRF protection on state-changing endpoints and refresh route (double-submit token or same-site strategy).

13. Input validation & normalization

    * Email/username normalization; length & charset checks; password policy; strong schema validation (zod/joi/celebrate).

14. Mass assignment risks

    * Updates whitelist allowed fields; cannot set `role`, `emailVerified`, `passwordResetToken`, etc., from `req.body`.

15. JWT misuse

    * No `jwt.decode()` for authorization decisions; always `jwt.verify()` with explicit `algorithms`.

16. Logging & telemetry

    * No logging of passwords, tokens, reset links, or PII; structured logs with redaction/allowlist.

17. Dependency & crypto hygiene

    * Maintained `jsonwebtoken` and `bcrypt` versions; no custom JWT parser; Node crypto used correctly; no MD5/SHA\* for password hashing.

18. Transport & CORS

    * HTTPS enforced; CORS locked to trusted origins; no wildcard credentials; preflight handled safely.

19. Open redirect / `next` param

    * Post-login redirection restricted to vetted paths/origins; no arbitrary `next=` redirects.

20. Operational controls

    * Secret rotation procedure; key separation for environments; monitoring for suspicious auth patterns; alerting on RT reuse.

Provide:

* A structured finding report with the following for each issue:

  * Title, Severity (Critical/High/Medium/Low), CWE (if applicable), Evidence (file, function, line ranges), and a short Why it matters.
  * Exploitability notes and, where safe, a minimal PoC or reproduction steps (no real secrets).
  * Remediation: precise code-level fix or config change (snippets welcome), plus defense-in-depth guidance.
* A summary risk score (0–10) and top 3–5 prioritized fixes that reduce risk fastest.
* A checklist diff: which items from the “Check for” list are Pass/Fail/Not Applicable.

Constraints & style:

* Be concrete and cite exact code locations and identifiers.
* Prefer minimal, drop-in fix snippets over prose.
* Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Bonus (if applicable):

* Suggest hardening improvements (e.g., switching to RS256 with KMS-managed keys, adding `jti` blacklist service, adding device/session management UI, enabling `mongoose.set('sanitizeFilter', true)`).
* Provide quick tests to validate fixes (e.g., RT reuse test, password-changed invalidation test, NoSQLi payload test).


Provide specific vulnerabilities found with severity ratings.

Write this into a markdown file and place it in the audits/ folder.
