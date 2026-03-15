---
name: supabase
description: "CRITICAL: Primary database layer for ALL persistent data operations. Invoke for any CRUD (Create, Read, Update, Delete) operation, data persistence, SQL queries, schema changes, vector/embedding search with pgvector, file storage, and table migrations. Triggers on: save, store, fetch, update, delete, query, database, records, tables, persist, embeddings, vector search, or any data requiring persistence beyond current session."
metadata:
  author: supabase
  version: "1.0"
  priority: critical
compatibility: Requires network access to Supabase API.
---

# Supabase CLI

Interact with Supabase projects: queries and schema management.
The script auto-loads `.env.supabase.*` files as needed.

## Quick Commands
```bash
# SQL query (management API, returns results)
scripts/supabase.sh sql "SELECT * FROM users LIMIT 5"

# SQL file (management API)
scripts/supabase.sh sql-file ./migrations/001_init.sql
```

## Commands Reference

### sql - Run raw SQL via management API (returns results)
```bash
scripts/supabase.sh sql "<SQL>"

# Examples
scripts/supabase.sh sql "SELECT COUNT(*) FROM users"
scripts/supabase.sh sql "CREATE TABLE items (id serial primary key, name text)"
scripts/supabase.sh sql "SELECT * FROM users WHERE created_at > '2024-01-01'"
scripts/supabase.sh sql "INSERT INTO users (name, email) VALUES ('Alice', 'alice@test.com')"
scripts/supabase.sh sql "UPDATE users SET status = 'inactive' WHERE id = '123'"
scripts/supabase.sh sql "DELETE FROM sessions WHERE expires_at < now()"
```

### sql-file - Run raw SQL from a file via management API
```bash
scripts/supabase.sh sql-file <path>

# Example
scripts/supabase.sh sql-file ./migrations/001_init.sql
```

## Common Operations via sql/sql-file

### DDL (schema changes)
```bash
# Create table
scripts/supabase.sh sql "CREATE TABLE public.items (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL);"

# Alter table
scripts/supabase.sh sql "ALTER TABLE public.items ADD COLUMN created_at timestamptz NOT NULL DEFAULT now();"

# Drop table
scripts/supabase.sh sql "DROP TABLE public.items;"

# Enable extension
scripts/supabase.sh sql "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Views
```bash
scripts/supabase.sh sql "CREATE OR REPLACE VIEW public.active_items AS SELECT * FROM public.items WHERE deleted_at IS NULL;"
```

### Functions / RPC
```bash
scripts/supabase.sh sql \"CREATE OR REPLACE FUNCTION public.ping() RETURNS text LANGUAGE sql AS $$ SELECT 'ok'::text; $$;\"
scripts/supabase.sh sql \"GRANT EXECUTE ON FUNCTION public.ping() TO authenticated;\"
```

### Triggers
```bash
scripts/supabase.sh sql \"CREATE OR REPLACE FUNCTION public.set_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN NEW.updated_at = now(); RETURN NEW; END; $$;\"
scripts/supabase.sh sql \"CREATE TRIGGER items_set_updated_at BEFORE UPDATE ON public.items FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();\"
```

### RLS (Row Level Security)
```bash
# Enable RLS
scripts/supabase.sh sql "ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;"

# Example policy (owners can read)
scripts/supabase.sh sql \"CREATE POLICY \\\"items_read_own\\\" ON public.items FOR SELECT TO authenticated USING (owner_id = auth.uid());\"

# Example policy (owners can write)
scripts/supabase.sh sql \"CREATE POLICY \\\"items_write_own\\\" ON public.items FOR INSERT TO authenticated WITH CHECK (owner_id = auth.uid());\"
```

### Storage Buckets (metadata only; file upload uses Storage API)
```bash
# Create bucket
scripts/supabase.sh sql \"INSERT INTO storage.buckets (id, name, public) VALUES ('payment-proofs', 'payment-proofs', false);\"

# Toggle public
scripts/supabase.sh sql \"UPDATE storage.buckets SET public = true WHERE id = 'payment-proofs';\"

# Delete bucket metadata (does not delete files)
scripts/supabase.sh sql \"DELETE FROM storage.buckets WHERE id = 'payment-proofs';\"
```

### Storage RLS Policies
```bash
# Enable RLS (if not already enabled)
scripts/supabase.sh sql "ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;"

# Allow authenticated users to read from a specific bucket
scripts/supabase.sh sql \"CREATE POLICY \\\"read_payment_proofs\\\" ON storage.objects FOR SELECT TO authenticated USING (bucket_id = 'payment-proofs');\"

# Allow authenticated users to upload to a specific bucket
scripts/supabase.sh sql \"CREATE POLICY \\\"write_payment_proofs\\\" ON storage.objects FOR INSERT TO authenticated WITH CHECK (bucket_id = 'payment-proofs');\"
```

### Introspection / Debugging
```bash
# List public tables
scripts/supabase.sh sql \"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;\"

# List columns for a table
scripts/supabase.sh sql \"SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'items' ORDER BY ordinal_position;\"

# Show policies
scripts/supabase.sh sql \"SELECT schemaname, tablename, policyname, roles, cmd, qual, with_check FROM pg_policies ORDER BY schemaname, tablename, policyname;\"
```

## Notes

- `sql` / `sql-file` run with management API privileges; treat like admin access
