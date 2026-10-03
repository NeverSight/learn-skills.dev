---
name: authorization-implementation
description: Analyzes authorization and access-control logic across routes and resources for privilege and enforcement flaws. Use when auditing authorization, RBAC, or access control.
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

# Authorization Implementation

Analyze authorization implementation across all routes:

Check for:

1. Broken Object Level Authorization (BOLA / IDOR)

   * Verify ownership/tenant checks on all object-level routes (`GET/PUT/DELETE /:id`).
   * Ensure identifiers in URL, body, or query cannot be manipulated to access others’ data.

2. Broken Function Level Authorization

   * Confirm role/permission checks exist on every privileged route.
   * Ensure enforcement is server-side, not just in the UI.

3. Missing authorization checks on sensitive endpoints

   * Validate middleware ordering (authN → authZ → handler).
   * Confirm no endpoints are left exposed (admin tools, bulk exports, feature-flagged routes).

4. Role-based access control (RBAC) implementation

   * Map roles → permissions explicitly; enforce deny-by-default.
   * Ensure roles cannot be set/changed by the client.

5. Privilege escalation possibilities

   * Check for update endpoints allowing fields like `role`, `tenantId`, or `isAdmin`.
   * Validate multi-step workflows cannot escalate privileges indirectly.

6. JWT token validation on every protected route

   * Require `jwt.verify` with strict `algorithms`, `iss`, `aud`, `exp`.
   * Ensure no route uses `jwt.decode` or trusts unverified claims.
   * Validate `jti` or `tokenVersion` against revocation strategy.

7. Proper scope checking for API tokens

   * Verify least-privilege scopes are enforced.
   * Differentiate user tokens vs service tokens; enforce `audience` and intended route access.

---

Additional items to check for:

8. Multi-tenant isolation

   * Tenant constraints injected server-side, not client-provided.
   * List/search endpoints filtered by tenant at query time.

9. Bulk endpoint protections

   * Batch/bulk operations enforce ownership per item, not just once at entry point.

10. Field-level authorization

    * Sensitive fields (e.g., `ssn`, `apiKey`, `secrets`) excluded for non-privileged users.
    * Ensure field-level projection or serializer logic exists.

11. Error handling & resource enumeration

    * Uniform errors (`403` vs `404`) to prevent leaking resource existence.
    * Consistent status codes across owned vs non-owned resources.

12. Middleware ordering

    * Confirm routes cannot bypass authorization due to wrong order (e.g., handler before auth middleware).
    * Check nested routers for missing parent auth guards.

13. CORS & CSRF considerations

    * No wildcard origins with credentials.
    * If cookies are used for auth, CSRF defenses are in place (SameSite, CSRF token).

14. Open redirect protections

    * Verify post-login `redirect`/`next` parameters are validated against allowlists.

15. Fallback/debug routes

    * Ensure no `/seed`, `/reset`, `/debug` endpoints are left exposed without strict admin checks.

---

For each endpoint, verify:

* Who can access it (roles, scopes, tenant).
* What data they can see/modify (including hidden fields).
* Whether ownership/tenancy is properly checked (query-level filter + post-fetch check).
* That middleware enforces authN/authZ consistently (no bypass possible).


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
