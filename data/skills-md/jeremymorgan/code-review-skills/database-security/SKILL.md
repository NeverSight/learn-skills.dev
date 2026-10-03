---
name: database-security
description: Examines all database interactions for injection, access control, encryption, and data-exposure risks. Use when auditing database and data-layer security.
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

# Database Security Audit

Examine ALL database interactions

Verify:

1. Parameterized queries or ORM usage

   * Ensure all queries use placeholders (`?`, `$1`, `:param`) or ORM bindings.
   * Flag any direct string concatenation in queries as CRITICAL.

2. Connection string security

   * No passwords or secrets hardcoded in code or committed to source control.
   * Use environment variables or a secrets manager.

3. Database user permissions (principle of least privilege)

   * Application account has only the rights it needs (e.g., no `SUPERUSER`, `DROP`, `GRANT`).
   * Separate accounts for read-only, migrations, and admin.

4. Sensitive data encryption at rest

   * Verify disk-level/database-native encryption.
   * Critical fields (e.g., SSN, tokens) use column-level encryption or tokenization.

5. PII handling compliance

   * Personally identifiable information is minimized, redacted in logs, and handled per GDPR/CCPA.
   * Retention/deletion policies exist and are enforced.

6. Query timeout configurations

   * Query/statement timeouts configured at driver and DB server level to prevent runaway queries.

7. Connection pool settings

   * Pool limits configured (min/max); no unbounded connections.
   * Idle timeouts enforced to prevent exhaustion.

8. Transaction handling for consistency

   * Transactions wrap multi-step operations.
   * Rollback paths tested to prevent partial updates.

9. Audit logging for sensitive operations

   * Log access to sensitive tables/fields, schema changes, permission changes, failed logins.
   * Logs are centralized, immutable, and monitored.

10. NoSQL injection hardening (if applicable)

    * User input never passed directly to filters.
    * `$where`, `$ne`, `$gt`, `$or` operators blocked/sanitized.
    * ORM/driver sanitization enabled (e.g., `mongoose.set('sanitizeFilter', true)`).

11. Row/Tenant isolation

    * Row-level security (Postgres RLS) or server-side ownership/tenant filters enforced.
    * Multi-tenant queries scoped by server, not client input.

12. Least-privilege networking

    * Database not publicly exposed; network ACLs, VPC, firewall/security groups in place.
    * Only whitelisted application servers can connect.

13. TLS in transit & certificate validation

    * DB connections use TLS (`sslmode=require/verify-full` or equivalent).
    * Certificates validated and rotated.

14. Secret management & rotation

    * Credentials stored in a secrets manager, rotated periodically.
    * No static passwords in `.env` files without protection.

15. Schema & integrity controls

    * Foreign keys, unique constraints, and NOT NULL enforced.
    * Ownership/tenant columns marked `NOT NULL` and validated.

16. Field-level minimization

    * Avoid `SELECT *`; fetch only required fields.
    * Reduces exposure of sensitive columns.

17. Pagination & query limits

    * Hard caps on `LIMIT`/page size; prevent unbounded queries that scan entire tables.

18. Backup/restore security

    * Backups encrypted, access-controlled, tested for restoration.
    * No unprotected dumps in CI/CD or object storage.

19. Data retention & deletion

    * Clear policies for retention, archival, and deletion of PII.
    * Secure erasure when data is removed.

20. Migrations safety

    * Migrations run with controlled privileges.
    * Destructive operations reviewed; rollback plans exist.

21. ORM raw-query escape hatch review

    * Any `queryRaw`/`sequelize.query`/`knex.raw` usage audited.
    * Must still use parameterized bindings.

22. LIKE / regex input handling

    * Special characters in user input escaped properly (`%`, `_`, regex metacharacters).
    * Prevents pattern abuse and heavy queries.

23. Query timeouts & resource guards

    * Resource caps enforced (memory, work\_mem, CPU).
    * Prevent denial-of-service via expensive queries.

24. Audit & monitoring depth

    * Privileged operations (DDL, GRANT, role changes) logged and alerted.
    * Centralized monitoring with anomaly detection.

25. PII in logs/metrics

    * ORM debug or query logs do not leak PII or secrets.
    * Redaction/allowlisting enforced.

26. Indexing of sensitive data

    * Sensitive fields (e.g., SSN, tokens) not indexed in plaintext.
    * Use hashed/indexed tokens or partial indexes where needed.

27. Service/account lifecycle

    * No shared admin accounts.
    * Time-bound, purpose-specific service accounts.
    * Periodic review of granted privileges.

28. Caching layers

    * Sensitive data not cached in plaintext unless justified.
    * Redis/Memcached require auth, not publicly exposed.

29. Analytics/ETL exports

    * PII masked or de-identified before export.
    * Exports encrypted, access-controlled, and scrubbed of secrets.

---

👉 Critical flags:

* Direct string concatenation in queries = CRITICAL.
* Passing raw user JSON into NoSQL queries without sanitization = CRITICAL.

---

## Provide:

A structured finding report with the following for each issue:

Title, Severity (Critical/High/Medium/Low), CWE (if applicable), Evidence (file, function, line ranges), and a short Why it matters.

Exploitability notes and, where safe, a minimal PoC or reproduction steps (no real secrets).

Remediation: precise code-level fix or config change (snippets welcome), plus defense-in-depth guidance.

A summary risk score (0–10) and top 3–5 prioritized fixes that reduce risk fastest.

A checklist diff: which items from the “Check for” list are Pass/Fail/Not Applicable.

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
