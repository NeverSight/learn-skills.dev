---
name: supabase-postgres-best-practices
description: Postgres performance optimization and Supabase-specific best practices, adapted to EquipQR's Supabase (Postgres + RLS) workflow. Use when editing SQL, migrations, indexes, RLS policies, API security, storage buckets, realtime subscriptions, or edge functions.
license: MIT
metadata:
  author: supabase
  version: "1.1.0"
  source_repo: supabase/agent-skills
  source_ref: main
  adapted_for: EquipQR
---

# Supabase & Postgres Best Practices (adapted for EquipQR)

Comprehensive performance optimization and security guide for Postgres and Supabase. Contains Postgres rules across 8 categories prioritized by impact, plus Supabase-specific guidelines for API security, storage, realtime, and edge functions.

## EquipQR applicability notes (important)

EquipQR uses **Supabase Postgres**. When applying these rules in this repo:

- **Migrations live in**: `supabase/migrations/*.sql` (follow our migration standards: timestamped filenames, enable RLS by default, avoid overly complex RLS joins, etc.).
- **RLS is mandatory**: Never add permissive "always true" policies without explicit, documented justification.
- **Service role usage**: Edge Functions (including Google Workspace integrations) must rely on RLS by default. Use `service_role` only in narrowly scoped, backend-only functions where you (1) validate the JWT, (2) enforce `organization_id` scoping on every query, and (3) perform explicit permission checks at least as strict as equivalent RLS policies. Never use `service_role` as a shortcut to bypass RLS.
- **App code boundaries**: UI components should not issue raw SQL; changes here typically translate into migrations, RPCs, or changes to query patterns in services.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)
- Configuring Supabase Storage buckets or signed URLs
- Writing or reviewing Edge Functions
- Implementing Realtime subscriptions
- Reviewing API security (service role vs anon key usage)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## Supabase-Specific Guidelines

### RLS Patterns
- Always enable RLS on public schema tables. Use `(select auth.uid())` instead of `auth.uid()` to avoid per-row function calls.
- Specify roles with `TO authenticated` clause. Use `SECURITY DEFINER` functions for complex multi-table checks.
- Add indexes on all columns referenced in RLS policies. Use `RESTRICTIVE` policies for additional constraints.

### API Security
- Never expose the `service_role` key to the client — it bypasses RLS. Use publishable (anon) keys on the client.
- Always filter queries even when RLS is enabled (defense in depth). Validate all JWT claims.

### Storage
- Enable RLS on `storage.objects`. Configure bucket-level security (public vs private).
- Use signed URLs for private file access with short expiration times.

### Realtime
- Use private channels for sensitive data. RLS policies apply to Realtime subscriptions.
- Always clean up subscriptions on component unmount (`useEffect` cleanup).

### Edge Functions
- Always verify JWT in edge functions. Handle CORS via `_shared/cors.ts`.
- Use Supabase secrets (Dashboard) for sensitive data — never hardcode keys.

### Testing
- Test RLS policies with pgTAP (`supabase/tests/`). Isolate tests properly with transaction rollbacks.

## Detailed Reference Files

Read these files for full rule explanations with SQL examples (only read what's needed):

- **Query & connection optimization** (indexes, pooling): [references/query-connection.md](references/query-connection.md)
- **Security & schema design** (RLS, data types, partitioning): [references/security-schema.md](references/security-schema.md)
- **Concurrency, access patterns & monitoring** (locks, N+1, EXPLAIN): [references/concurrency-access-monitoring.md](references/concurrency-access-monitoring.md)
