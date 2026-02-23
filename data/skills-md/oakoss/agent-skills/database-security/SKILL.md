---
name: database-security
description: 'Database security auditor specialized in Row Level Security (RLS) enforcement, Zero-Trust database architecture, and forensic audit trails. Covers Supabase RLS policies, Postgres security, Convex auth guards, PGAudit configuration, JIT access controls, and database-specific compliance validation. Use when auditing database access policies, implementing RLS in Supabase or Postgres, configuring Convex auth guards, setting up audit logging, reviewing database security, or validating database-level compliance requirements.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# Security Audit

Database security auditor specialized in Row Level Security (RLS) enforcement, Zero-Trust database architecture, and forensic audit trails. Focuses on Supabase, Postgres, and Convex data layer security. For general application security (OWASP Top 10, auth patterns, security headers, input validation), use the `security` skill instead.

## Quick Reference

| Need                 | Approach                                                       |
| -------------------- | -------------------------------------------------------------- |
| RLS enforcement      | Enable on every public table; separate policies per operation  |
| RLS performance      | Index RLS columns; wrap auth.uid() in (select ...) subselect   |
| Zero-Trust DB        | Micro-segmentation, identity propagation, TLS enforcement      |
| Supabase auth in RLS | Use (select auth.uid()) and auth.jwt(); never auth.role()      |
| Convex auth guards   | Call ctx.auth.getUserIdentity() in every public function       |
| JIT access           | Time-bound grants that expire automatically                    |
| Audit trails         | Database triggers with immutable audit_log table               |
| PGAudit              | Extension for statement-level and object-level SQL auditing    |
| Service role safety  | Never use service_role key in client-side code                 |
| Views and RLS        | Use security_invoker = true (Postgres 15+) to enforce RLS      |
| Schema segmentation  | Separate public, private, and audit schemas                    |
| Database compliance  | RLS + audit logging + encryption satisfies multiple frameworks |

## Audit Protocol

Follow this sequence when performing a database security audit:

1. **Attack Surface Mapping**: Identify all entry points to the data layer (public APIs, internal dashboards, AI agents, cron jobs)
2. **RLS Coverage Check**: Query pg_tables to verify every public schema table has RLS enabled and appropriate policies
3. **Policy Review**: Check for logical bypasses, missing WITH CHECK clauses, overly permissive FOR ALL policies
4. **Service Role Audit**: Search client code for service_role key exposure; verify it only appears in server-side code
5. **Function Audit**: Check for security definer functions in exposed schemas and Convex functions missing auth guards
6. **Access Simulation**: Execute queries as anon and authenticated roles to verify enforcement
7. **View Audit**: Verify views use security_invoker = true or are not in exposed schemas
8. **Audit Trail Verification**: Confirm triggers or PGAudit capture all security-relevant operations
9. **Compliance Validation**: Map database controls against applicable regulatory frameworks

## Security Principles

| Principle         | Database Application                                   |
| ----------------- | ------------------------------------------------------ |
| Defense in Depth  | RLS + application checks + schema segmentation         |
| Least Privilege   | Minimal GRANT per role; anon gets near-zero access     |
| Zero Trust        | Verify identity at DB level even for internal requests |
| Secure by Default | RLS enabled on creation; default-deny when no policy   |
| Fail Securely     | Postgres default-deny on RLS; generic error responses  |
| Assume Breach     | Design assuming attacker has a valid JWT               |

## Anti-Patterns

| Anti-Pattern                                | Risk                                       |
| ------------------------------------------- | ------------------------------------------ |
| Security by obscurity (UUIDs only)          | Attackers enumerate IDs via IDOR           |
| Anon role with SELECT on sensitive tables   | Public data exposure via Supabase API      |
| RLS columns without indexes                 | Production performance degradation (100x+) |
| Frontend-only permission checks             | Attackers bypass via direct API calls      |
| Standing admin privileges                   | Excessive blast radius if compromised      |
| service_role key in client-side code        | Bypasses all RLS policies completely       |
| FOR ALL policies instead of per-operation   | Unintended write access through broad rule |
| Security definer functions in public schema | Functions callable from API, bypass RLS    |
| Views without security_invoker              | Views bypass RLS silently                  |

## Common Mistakes

| Mistake                                                     | Correct Pattern                                                                |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Using auth.uid() = user_id without wrapping in (select ...) | Use (select auth.uid()) = user_id so Postgres caches the result via initPlan   |
| Using FOR ALL instead of separate per-operation policies    | Create separate SELECT, INSERT, UPDATE, DELETE policies for clarity and safety |
| Leaving anon role with SELECT on sensitive tables           | Restrict anon access; require authenticated role for sensitive data            |
| Relying on UUIDs as the only access control                 | Enforce RLS policies and explicit auth checks alongside unique identifiers     |
| No index on columns used in RLS USING clauses               | Add B-tree indexes on all columns referenced in RLS policy expressions         |
| Convex function missing ctx.auth.getUserIdentity() call     | Every public query and mutation must validate identity before accessing data   |
| Using service_role key in client-side code                  | Use anon key client-side; service_role only in server-side functions           |
| Views bypassing RLS without security_invoker                | Set security_invoker = true on views in Postgres 15+                           |
| Security definer functions in exposed schemas               | Place security definer functions in non-exposed schemas with search_path = ''  |
| No audit logging for security-relevant database events      | Use triggers and PGAudit to capture all data access and modifications          |

## Relationship to Security Skill

The `application-security` skill covers general application security: OWASP Top 10, authentication patterns, input validation, security headers, and compliance overviews. This `database-security` skill complements it by focusing on database-layer concerns: RLS policy design and performance, Supabase/Postgres-specific patterns, Convex auth guards, PGAudit configuration, and database-specific compliance implementations (SQL functions for GDPR erasure, HIPAA PHI audit triggers, etc.).

## Delegation

- **Verify RLS enforcement with access simulations**: Use `Task` agent to run anonymous and authenticated queries against every public table
- **Audit Convex functions for missing auth guards**: Use `Explore` agent to scan all query and mutation handlers for getUserIdentity calls
- **Design zero-trust database architecture**: Use `Plan` agent to map schemas, access policies, JIT grants, and audit log design
- **Generate database compliance evidence**: Use `Task` agent to run audit queries and produce compliance reports

## References

- [rls-performance.md](references/rls-performance.md) -- RLS policy performance, initPlan caching, stable functions, separate policies, EXPLAIN benchmarking
- [zero-trust-database.md](references/zero-trust-database.md) -- Micro-segmentation, identity propagation, connection security, JIT access controls
- [audit-logging.md](references/audit-logging.md) -- Trigger-based auditing, PGAudit extension and log classes, log integrity, tamper-proof storage
- [convex-security.md](references/convex-security.md) -- Identity validation, manual RLS in functions, granular functions, role-based access via JWT claims
- [threat-modeling.md](references/threat-modeling.md) -- STRIDE applied to database access, RLS bypass vectors, data layer trust boundaries
- [application-security.md](references/application-security.md) -- Service role management, schema exposure, security definer functions, views and RLS
- [compliance-frameworks.md](references/compliance-frameworks.md) -- Database-specific GDPR, HIPAA, SOC2, PCI-DSS requirements and SQL implementations
