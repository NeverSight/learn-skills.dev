---
name: soft-delete-and-archiving
description: >-
  Use when implementing soft deletes (deleted_at), restoring records, archiving
  instead of hard delete, or filtering active vs deleted rows in queries and RLS.
  Not for GDPR hard-delete requests that must purge data.
---

# Soft delete and archiving

## Column pattern

```sql
alter table public.projects add column deleted_at timestamptz;
create index projects_active_idx on public.projects (organization_id)
  where deleted_at is null;
```

- **Active**: `deleted_at is null`
- **Deleted**: `deleted_at is not null` (set to `now()` on delete)

Optional: `deleted_by uuid references auth.users(id)`.

## Queries

Default every app query:

```ts
.from("projects").select("*").is("deleted_at", null)
```

Views can encapsulate:

```sql
create view public.projects_active as
  select * from public.projects where deleted_at is null;
```

## RLS

Policies should exclude soft-deleted rows for normal users:

```sql
using (deleted_at is null and /* membership check */)
```

Admins may `select` deleted via separate policy or service role.

## Restore

`update projects set deleted_at = null, deleted_by = null where id = $1` — only owner/admin.

## Hard delete

Reserve for legal/GDPR: edge function + service role after retention period; document in audit log.

## Avoid

- Unique constraints broken by soft delete — use partial unique index:

```sql
create unique index projects_org_slug_active_idx
  on public.projects (organization_id, slug) where deleted_at is null;
```

- Cascading hard delete when product expects archive.

## Checklist

- [ ] All list queries filter `deleted_at is null`
- [ ] Partial unique indexes where needed
- [ ] Restore path tested
