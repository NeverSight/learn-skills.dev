---
name: create-migration
description: Generate a Supabase PostgreSQL database migration with proper schema, RLS policies, indexes, triggers, and grants. Follows DaaS naming conventions and includes standard audit columns. Use when the user needs a database migration, table creation, schema change, or wants to add columns to a collection. Supabase projects only — on an Engine project it writes no file, stops, and names the skills that change structure and access there.
argument-hint: "[migration description]"
---

# Create Database Migration

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

<!-- buildpad-backend: engine -->
## On an Engine project: there are no migrations

An Engine project has no database migrations, and nothing reads a migration file there. Write no
file. Tell the developer that structure and access are changed through the Engine, and stop here:
- a table, a column, a relation or an index: the `create-collection` skill;
- who may read or change it: the `create-rbac` skill, and `relational-permissions` for nested writes;
- a workflow column: the `create-workflow` skill; multi-level data separation: `manage-scope`.
<!-- /buildpad-backend -->
<!-- buildpad-backend: supabase -->
Generate a Supabase PostgreSQL migration with proper schema, RLS policies, and indexes.

## Migration File Location

```
supabase/migrations/[YYYYMMDDHHMMSS]_[description].sql
```

## Naming Conventions

- Tables: `snake_case`, plural (`user_profiles`, `blog_posts`)
- Columns: `snake_case` (`date_created`, `user_id`)
- Primary keys: `id` (UUID)
- Foreign keys: `[referenced_table]_id` (`category_id`)
- Junction tables: `[table1]_[table2]` (`products_tags`)

## Standard Columns

```sql
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
date_created timestamptz DEFAULT now(),
date_updated timestamptz,
user_created uuid REFERENCES auth.users(id),
user_updated uuid REFERENCES auth.users(id)
```

## Migration Sections (Required)

1. **Header Comment** — description, author, date
2. **CREATE TABLE** — with data types and constraints
3. **Enable RLS** — `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
4. **RLS Policies** — SELECT, INSERT, UPDATE, DELETE
5. **Indexes** — FK columns, filtered columns, sorted columns
6. **Triggers** — `date_updated` auto-update, audit logging
7. **GRANT** — permissions for `authenticated` and `anon` roles

## Data Types

| Use Case   | PostgreSQL Type             |
| ---------- | --------------------------- |
| ID         | `uuid`                      |
| Short text | `text` or `varchar(n)`      |
| Long text  | `text`                      |
| Integer    | `integer` or `bigint`       |
| Decimal    | `numeric(precision, scale)` |
| Boolean    | `boolean`                   |
| Timestamp  | `timestamptz`               |
| JSON       | `jsonb`                     |
| Array      | `text[]`, `uuid[]`          |
| Enum       | `text` with CHECK           |

## Relationships

### One-to-Many

```sql
category_id uuid REFERENCES public.categories(id) ON DELETE SET NULL
```

### Many-to-Many (junction table)

```sql
CREATE TABLE public.products_tags (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  products_id uuid NOT NULL REFERENCES public.products(id) ON DELETE CASCADE,
  tags_id uuid NOT NULL REFERENCES public.tags(id) ON DELETE CASCADE,
  UNIQUE(products_id, tags_id)
);
```

## RLS Policy Patterns

```sql
-- Owner can CRUD their own
CREATE POLICY "users_own_data" ON public.[table]
  FOR ALL USING (auth.uid() = user_created);

-- Published items are public
CREATE POLICY "published_public" ON public.[table]
  FOR SELECT USING (status = 'published' OR auth.uid() = user_created);
```

## Commands

```bash
supabase migration new [description]
supabase db push
supabase db reset
```

## References

- [Special fields](references/special-fields.instructions.md)
<!-- /buildpad-backend -->
