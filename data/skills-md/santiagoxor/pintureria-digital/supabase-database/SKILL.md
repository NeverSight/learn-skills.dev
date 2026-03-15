---
name: supabase-database
description: Specialized skill for working with Supabase PostgreSQL database including queries, RLS policies, migrations, functions, and data operations. Use when implementing database queries, creating migrations, setting up RLS policies, writing SQL functions, or debugging database issues.
---

# Supabase Database

## Quick Start

When working with Supabase:

1. Always use Supabase client from `@/lib/supabase/server` or `@/lib/supabase/client`
2. Never make queries without filtering by `tenant_id` in multitenant tables
3. Always enable RLS on tables and include tenant verification in policies
4. Use prepared parameters (Supabase client methods, never string concatenation)
5. Use migrations in `supabase/migrations/` for schema changes

## Key Files

- `src/lib/supabase/` - Supabase client utilities
- `src/lib/integrations/supabase/` - Supabase integration
- `supabase/migrations/` - Database migrations
- `supabase/functions/` - Edge functions
- `src/lib/auth/enterprise-rls-utils.ts` - RLS utilities

## Common Patterns

### Basic Query with Tenant

```typescript
import { createClient } from '@/lib/supabase/server';
import { getTenantFromRequest } from '@/lib/tenant/tenant-service';

const supabase = createClient();
const tenant = await getTenantFromRequest(request);

const { data, error } = await supabase
  .from('products')
  .select('id, name, price, category_id')
  .eq('tenant_id', tenant.id)
  .eq('active', true)
  .order('created_at', { ascending: false })
  .limit(20);

if (error) {
  console.error('Query error:', error);
  return NextResponse.json({ error: error.message }, { status: 500 });
}
```

### Insert with Tenant

```typescript
const { data, error } = await supabase
  .from('products')
  .insert({
    name: 'Pintura Blanca',
    price: 5000,
    tenant_id: tenant.id,
    category_id: categoryId,
    active: true,
  })
  .select()
  .single();
```

### Update with Tenant

```typescript
const { data, error } = await supabase
  .from('products')
  .update({ price: 5500 })
  .eq('id', productId)
  .eq('tenant_id', tenant.id)
  .select()
  .single();
```

### RLS Policy Example

```sql
-- Enable RLS
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Policy for tenant isolation
CREATE POLICY "tenant_isolation_products" ON products
  FOR ALL
  USING (
    tenant_id = (
      SELECT id FROM tenants 
      WHERE slug = current_setting('app.tenant_slug', true)
    )
  );

-- Policy for public read (if needed)
CREATE POLICY "public_read_products" ON products
  FOR SELECT
  USING (active = true);
```

### Using RLS Utils

```typescript
import { executeWithRLS } from '@/lib/auth/enterprise-rls-utils';

const result = await executeWithRLS(
  enterpriseContext,
  async (client, rlsContext) => {
    return await client
      .from('products')
      .select('*')
      .eq('tenant_id', rlsContext.tenantId);
  }
);
```

### Migration Template

```sql
-- Migration: add_new_column_to_products
-- Created: 2026-01-23

BEGIN;

-- Add new column
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS new_field VARCHAR(255);

-- Create index if needed
CREATE INDEX IF NOT EXISTS idx_products_new_field 
ON products(new_field) 
WHERE new_field IS NOT NULL;

-- Update RLS policy if needed
-- (Add to existing policy or create new one)

COMMIT;
```

## Best Practices

- **Always filter by tenant_id** in multitenant tables
- **Use `.select()` with specific fields** instead of `*`
- **Enable RLS** on all tables
- **Use migrations** for all schema changes
- **Test migrations** in development first
- **Use transactions** for multiple related operations
- **Index frequently queried fields** (tenant_id, foreign keys)

## Commands

```bash
# Create new migration
supabase migration new migration_name

# Apply migrations
supabase db push

# Reset database (development)
supabase db reset

# Generate TypeScript types
supabase gen types typescript --local > src/types/database.ts
```
