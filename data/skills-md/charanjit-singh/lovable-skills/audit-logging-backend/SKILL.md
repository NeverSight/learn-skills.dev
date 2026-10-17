---
name: audit-logging-backend
description: >-
  Use when recording audit trails: who changed what, admin action logs, compliance
  history, or append-only event tables. Not for product analytics (use
  analytics-events) or debug console logs only.
---

# Audit logging (backend)

## `audit_logs` table (append-only)

```sql
create table public.audit_logs (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid,
  actor_id uuid references auth.users(id),
  action text not null,
  entity_type text not null,
  entity_id text,
  metadata jsonb default '{}',
  ip inet,
  created_at timestamptz not null default now()
);

create index audit_logs_org_created_idx on public.audit_logs (organization_id, created_at desc);
```

- **No update/delete** policies for clients — insert via trigger or edge function only.
- RLS: admins read org logs; members read none unless product requires.

## What to log

- Role changes, invites, billing plan changes, deletes, permission grants.
- Login failures (careful with PII retention limits).

Do not log passwords, tokens, full payment PAN.

## Write path

`auth.uid()` is only populated when the change comes through PostgREST with a user JWT (client `supabase.from(...).delete()`). For service-role writes (edge functions, cron) or `psql`, `auth.uid()` is `null` — pass the actor explicitly.

**Trigger** (PostgREST-initiated changes):

```sql
create or replace function public.audit_project_delete()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.audit_logs (organization_id, actor_id, action, entity_type, entity_id, metadata)
  values (old.organization_id, auth.uid(), 'project.deleted', 'project', old.id::text,
          jsonb_build_object('name', old.name));
  return old;
end;
$$;

create trigger projects_audit_delete
  after delete on public.projects
  for each row execute function public.audit_project_delete();
```

**Edge function** (external actions, webhook-driven, service-role writes): insert with explicit `actor_id` from verified JWT or a `system` sentinel for automated work.

```ts
await admin.from("audit_logs").insert({
  organization_id: orgId,
  actor_id: userIdFromJwt,
  action: "billing.plan_changed",
  entity_type: "subscription",
  entity_id: subscriptionId,
  metadata: { from_plan: "free", to_plan: "pro" },
});
```

## Querying

Admin UI: paginate `order by created_at desc`, filter by `entity_type`, `actor_id`.

## Retention

Cron job (`background-jobs-and-cron`) archives or deletes logs older than policy (e.g. 365 days).

## Avoid

- Client `insert` into `audit_logs` directly.
- Mutable log rows.
- Logging entire request bodies with secrets.

## Checklist

- [ ] Append-only + restricted RLS
- [ ] actor_id set on every entry
- [ ] Retention documented
