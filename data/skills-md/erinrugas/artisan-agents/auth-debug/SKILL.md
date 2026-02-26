---
name: auth-debug
description: >-
  Debugs authentication and authorization issues. Use for login/session/token failures,
  role/permission mismatches, CORS/cookie problems, and unexpected 401/403 responses.
---

# Auth Debug Skill

## When to Apply
- Login succeeds but users appear unauthenticated.
- Requests return 401/403 unexpectedly.
- Session/cookie/token handling is inconsistent across environments.

## Workflow
1. Read auth-related requirements from `specs/specs.md` and `specs/security-spec.md`.
2. Identify auth model in use (session cookie, token, OAuth, SSO, hybrid).
3. Trace the failing request path:
   - client request headers/cookies
   - server middleware/guards
   - role/policy checks
4. Verify environment/config factors (domains, CORS, secure cookie, token expiry).
5. Propose minimal fix and include regression tests/checklist.

## Quality Bar
- No broad permission bypasses.
- Preserve least privilege.
- Include one concrete reproduction and one verification path.
