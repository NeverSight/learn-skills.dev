---
name: postgres-full-text-search
description: >-
  Use when implementing search with Postgres: tsvector, GIN indexes, search RPC,
  or replacing client-side filter of large lists. Not for external Algolia/Typesense
  setup unless migrating away from DB search.
---

# Postgres full-text search

## Generated column + GIN index

```sql
alter table public.posts add column search_vector tsvector
  generated always as (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(body, '')), 'B')
  ) stored;

create index posts_search_idx on public.posts using gin (search_vector);
```

Use simple config for mixed language products; consider `pg_trgm` for typo-tolerant name search.

## Search RPC

```sql
create or replace function public.search_posts(
  p_query text,
  p_limit int default 20
) returns setof public.posts
language sql stable as $$
  select *
  from public.posts
  where search_vector @@ websearch_to_tsquery('english', p_query)
    and deleted_at is null
  order by ts_rank(search_vector, websearch_to_tsquery('english', p_query)) desc
  limit p_limit;
$$;
```

Grant `execute` to `authenticated`; RLS still applies on underlying table.

## Client

```ts
const { data } = await supabase.rpc("search_posts", { p_query: q });
```

Debounce input 300ms; minimum query length 2.

## Trigram fallback (names)

```sql
create extension if not exists pg_trgm;
create index projects_name_trgm_idx on public.projects using gin (name gin_trgm_ops);
-- where name ilike '%' || p_query || '%' — use sparingly at scale
```

## Avoid

- `ilike '%term%'` on large tables without index.
- Loading full table to client for search.
- Ignoring RLS on search results.

## Checklist

- [ ] GIN index on search column
- [ ] RPC or filtered query with rank
- [ ] Soft-deleted rows excluded (`soft-delete-and-archiving`)
