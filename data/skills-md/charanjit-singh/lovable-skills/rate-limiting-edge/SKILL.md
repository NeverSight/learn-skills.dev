---
name: rate-limiting-edge
description: >-
  Use when adding rate limiting to edge functions, login endpoints, signup,
  password reset, contact forms, or any abuse-prone API path. Not for static
  page caching or CDN-level limits unless implementing at the application layer.
---

# Rate limiting (edge functions)

Protect signup, login, password reset, contact forms, AI endpoints, and any unauthenticated API path.

## Approach

For Lovable + Supabase: a small DB-backed counter with a fixed window. Upgrade to Upstash Redis or a CDN limiter when traffic grows.

## DB pattern (fixed window)

```sql
create table public.rate_limits (
  key text not null,
  window_start timestamptz not null,
  count int not null default 0,
  primary key (key, window_start)
);

create index rate_limits_window_idx on public.rate_limits (window_start);
```

```ts
async function rateLimit(
  key: string,
  limit: number,
  windowSeconds: number,
): Promise<{ ok: boolean; remaining: number; retryAfter: number }> {
  const now = Date.now();
  const windowStart = new Date(Math.floor(now / (windowSeconds * 1000)) * windowSeconds * 1000);

  const { data, error } = await admin
    .from("rate_limits")
    .upsert(
      { key, window_start: windowStart.toISOString(), count: 1 },
      { onConflict: "key,window_start", ignoreDuplicates: false },
    )
    .select("count")
    .single();

  if (error) throw error;

  const count = data.count;
  const retryAfter = Math.ceil((windowStart.getTime() + windowSeconds * 1000 - now) / 1000);
  return { ok: count <= limit, remaining: Math.max(0, limit - count), retryAfter };
}
```

For atomic increment, prefer a `security definer` RPC that does `insert ... on conflict do update set count = count + 1` and returns the new count.

## Key strategy

| Endpoint | Key |
|----------|-----|
| Login | `login:ip:${ip}` and `login:email:${email}` (both) |
| Signup | `signup:ip:${ip}` |
| Password reset | `pwreset:email:${email}` |
| Contact form | `contact:ip:${ip}` |
| Authenticated API | `api:user:${userId}` |

Get IP from `req.headers.get("cf-connecting-ip") ?? req.headers.get("x-forwarded-for")?.split(",")[0]`.

## Response

```ts
const limit = await rateLimit(`login:email:${email}`, 5, 60);
if (!limit.ok) {
  return new Response(
    JSON.stringify({ error: "rate_limited", message: "Too many attempts. Try again shortly." }),
    {
      status: 429,
      headers: {
        "Content-Type": "application/json",
        "Retry-After": String(limit.retryAfter),
      },
    },
  );
}
```

Pair with `api-error-handling` for consistent shape.

## Recommended limits (starting point)

| Endpoint | Limit | Window |
|----------|-------|--------|
| Login (by email) | 5 | 60 s |
| Login (by IP) | 20 | 60 s |
| Signup | 5 | 60 s |
| Password reset | 3 | 60 s |
| Contact / public form | 5 | 60 s |
| AI / expensive endpoint | per pricing tier | per minute / day |

Tune from logs after launch.

## Cleanup

Cron job (`background-jobs-and-cron`) deletes rows older than the largest window + buffer:

```sql
delete from public.rate_limits where window_start < now() - interval '1 hour';
```

## Avoid

- Counting in memory inside the edge function — every invocation is a fresh process.
- Logging the raw IP in audit logs without privacy consideration.
- Same limit for authenticated and anonymous traffic.

## Checklist

- [ ] 429 returned with `Retry-After`.
- [ ] Both IP and identity (email/user) keyed where possible.
- [ ] Cleanup job for old rows.
- [ ] Limits documented per endpoint.
