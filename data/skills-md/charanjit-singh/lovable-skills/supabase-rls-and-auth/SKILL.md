---
name: supabase-rls-and-auth
description: >-
  Use when creating Supabase tables, row level security policies, multi-tenant
  data isolation, auth-gated routes, or fixing users seeing wrong data. Not for
  styling, forms validation only, or non-Supabase auth providers unless wiring
  sessions to Supabase.
---

# Supabase RLS and auth

For sign-in flows and OAuth, use **`supabase-auth-flows`**. This skill covers **data access** policies.

Every user-owned table must have **RLS enabled** and **policies** before shipping. Never rely on hiding UI alone.

## New table checklist

- [ ] `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`
- [ ] Policy for `SELECT` — users read only their rows (or org rows).
- [ ] Policy for `INSERT` — `auth.uid()` matches `user_id` (or membership check).
- [ ] Policy for `UPDATE` / `DELETE` — same ownership rule.
- [ ] `user_id` (or `organization_id`) column with FK to `auth.users` where applicable.
- [ ] Service-role key **never** in client code.

## Policy patterns

**Single-user ownership**

```sql
CREATE POLICY "users_select_own" ON public.posts
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "users_insert_own" ON public.posts
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

**Organization / tenant**

```sql
CREATE POLICY "members_select" ON public.projects
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.memberships m
      WHERE m.organization_id = projects.organization_id
        AND m.user_id = auth.uid()
    )
  );
```

Use `WITH CHECK` on insert/update mirroring the same rule.

## Client auth

- Use Supabase Auth session; gate routes with session check + redirect to login.
- Read `auth.uid()` in policies; do not trust client-sent `user_id` without `WITH CHECK`.
- For profile rows, create profile on signup (trigger or edge function), keyed to `auth.users.id`.

## Performance

Wrap repeated subqueries in a `security definer` helper (e.g. `is_org_member(org_id)`) — see `multi-tenant-backend`. This avoids re-evaluating membership joins per row and prevents recursion when policies reference the same table they protect.

Use `(select auth.uid())` inside policies (with the parentheses) so Postgres caches the value per statement instead of per row.

## Avoid

- Tables without RLS in production.
- `USING (true)` on user data tables.
- Storing roles only in localStorage.
- Exposing service role in Vite `VITE_*` env vars.
- Bypassing RLS with the service role from the client.

## Verify before done

Ask the user to test with **two accounts**: user A must not read/write user B's rows. Flag as "needs manual check" if you cannot run two sessions.
