---
name: Database Design
slug: database-design
description: Expert guide for database schema design, Supabase/PostgreSQL best practices, RLS policies, and optimizations. Use when designing tables, relationships, or implementing data models.
category: backend
complexity: moderate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "design database"
  - "create schema"
  - "database tables"
  - "RLS policies"
  - "data model"
  - "database optimization"
  - "migration"
  - "indexes"
tags:
  - database
  - postgresql
  - supabase
  - schema
  - rls
  - migrations
  - indexes
  - sql
---

# Database Design Skill

Comprehensive guide for designing efficient, scalable database schemas for Next.js applications with Supabase and PostgreSQL. From table design and relationships to Row Level Security policies and query optimization, this skill covers everything needed for robust data modeling.

Design normalized schemas, implement secure RLS policies, optimize query performance with proper indexing, and build maintainable data models that scale with your application.

## Core Workflows

### Workflow 1: Schema Design from Requirements
**Purpose:** Translate business requirements into database schema

**Steps:**
1. Identify entities and relationships
2. Define primary and foreign keys
3. Choose appropriate data types
4. Add constraints and defaults
5. Create indexes for performance

**Implementation:**
```sql
-- Correct data types
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT NOT NULL,                    -- Use TEXT, not VARCHAR
  age INTEGER CHECK (age >= 0),
  balance DECIMAL(10, 2),                 -- For money
  is_active BOOLEAN DEFAULT true,
  metadata JSONB,                         -- Use JSONB for JSON
  created_at TIMESTAMPTZ DEFAULT NOW()    -- Use TIMESTAMPTZ
);
```

### Workflow 2: Common Relationship Patterns
**Purpose:** Implement proper database relationships

**One-to-Many:**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
```

**Many-to-Many:**
```sql
CREATE TABLE students (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL
);

CREATE TABLE courses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL
);

CREATE TABLE enrollments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  enrolled_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(student_id, course_id)
);

CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
```

**Self-Referencing (Tree):**
```sql
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  parent_id UUID REFERENCES comments(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_comments_parent ON comments(parent_id);
```

### Workflow 3: Row Level Security (RLS)
**Purpose:** Secure data access at the database level

**Implementation:**
```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only read their own data
CREATE POLICY "Users can read own posts"
ON posts FOR SELECT
USING (auth.uid() = user_id);

-- Users can insert their own data
CREATE POLICY "Users can create posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own data
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Users can delete their own data
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
USING (auth.uid() = user_id);

-- Public read, authenticated write
CREATE POLICY "Public can read posts"
ON posts FOR SELECT
USING (true);

CREATE POLICY "Authenticated users can create posts"
ON posts FOR INSERT
WITH CHECK (auth.role() = 'authenticated');

-- Role-based access
CREATE POLICY "Admins have full access"
ON posts FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM users
    WHERE id = auth.uid() AND role = 'admin'
  )
);
```

### Workflow 4: Indexes for Performance
**Purpose:** Optimize query performance

**Implementation:**
```sql
-- Single Column Index
CREATE INDEX idx_users_email ON users(email);

-- Composite Index
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);

-- Partial Index
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- Full-Text Search Index
CREATE INDEX idx_posts_search ON posts
USING gin(to_tsvector('english', title || ' ' || content));

-- Query with full-text search
SELECT * FROM posts
WHERE to_tsvector('english', title || ' ' || content)
@@ plainto_tsquery('search term');
```

### Workflow 5: Advanced Patterns
**Purpose:** Implement common database patterns

**Soft Deletes:**
```sql
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  deleted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_posts_not_deleted ON posts(id) WHERE deleted_at IS NULL;

CREATE POLICY "Users see non-deleted posts"
ON posts FOR SELECT
USING (deleted_at IS NULL);
```

**Audit Trail:**
```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  table_name TEXT NOT NULL,
  record_id UUID NOT NULL,
  action TEXT NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
  old_data JSONB,
  new_data JSONB,
  user_id UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, user_id)
  VALUES (
    TG_TABLE_NAME,
    COALESCE(NEW.id, OLD.id),
    TG_OP,
    CASE WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD) ELSE NULL END,
    CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) ELSE NULL END,
    auth.uid()
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER posts_audit
AFTER INSERT OR UPDATE OR DELETE ON posts
FOR EACH ROW EXECUTE FUNCTION audit_trigger();
```

**Auto-update Timestamps:**
```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER posts_updated_at
BEFORE UPDATE ON posts
FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

## Quick Reference

| Task | SQL Pattern |
|------|-------------|
| Create table | `CREATE TABLE name (columns)` |
| Add column | `ALTER TABLE name ADD COLUMN col TYPE` |
| Add index | `CREATE INDEX name ON table(columns)` |
| Enable RLS | `ALTER TABLE name ENABLE ROW LEVEL SECURITY` |
| Create policy | `CREATE POLICY name ON table FOR action USING (condition)` |
| Create function | `CREATE FUNCTION name() RETURNS type AS $$ ... $$` |
| Create trigger | `CREATE TRIGGER name AFTER/BEFORE action ON table` |

## Migrations with Supabase

```bash
# Create Migration
npx supabase migration new create_posts_table
```

```sql
-- supabase/migrations/20240101000000_create_posts_table.sql

CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_posts_user_id ON posts(user_id);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own posts"
ON posts FOR SELECT
USING (auth.uid() = user_id);
```

```bash
# Apply Migration
npx supabase db push
```

## Querying with Supabase

```typescript
// Select all
const { data } = await supabase.from('posts').select('*')

// Select specific columns
const { data } = await supabase.from('posts').select('id, title')

// Filter
const { data } = await supabase
  .from('posts')
  .select('*')
  .eq('user_id', userId)

// Join tables
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    users (
      id,
      name,
      email
    )
  `)

// Count
const { count } = await supabase
  .from('posts')
  .select('*', { count: 'exact', head: true })

// Pagination
const { data } = await supabase
  .from('posts')
  .select('*')
  .range(0, 9)

// Order
const { data } = await supabase
  .from('posts')
  .select('*')
  .order('created_at', { ascending: false })
```

## Best Practices

- **Use UUIDs:** Better for distributed systems and security
- **Add Timestamps:** Always include created_at and updated_at
- **Enable RLS:** On all tables by default
- **Index Foreign Keys:** Create indexes for all foreign keys
- **Use TIMESTAMPTZ:** Not TIMESTAMP for timezone awareness
- **Use TEXT:** Not VARCHAR in PostgreSQL
- **Use JSONB:** Not JSON for better performance
- **Normalize First:** Denormalize only for performance
- **Migrations Only:** Never modify schema directly in production
- **Test RLS Policies:** Verify with different user contexts
- **Use Transactions:** For related operations
- **Document Schema:** Maintain ERD diagrams

## Constraints

```sql
-- Primary Key
id UUID PRIMARY KEY DEFAULT uuid_generate_v4()

-- Foreign Key
user_id UUID REFERENCES users(id) ON DELETE CASCADE

-- Unique
email TEXT UNIQUE NOT NULL

-- Check
price DECIMAL CHECK (price > 0)
status TEXT CHECK (status IN ('active', 'inactive'))

-- Not Null
name TEXT NOT NULL
```

## Dependencies

```bash
# Supabase CLI for migrations
npm install -D supabase

# Generate types from schema
npx supabase gen types typescript --local > types/database.ts
```

## Error Handling

- **Foreign Key Violations:** Handle gracefully in application
- **Unique Constraints:** Provide user-friendly error messages
- **Check Constraints:** Validate in application before insert
- **RLS Errors:** Return 404 instead of 403 for security
- **Connection Limits:** Use connection pooling

## Performance Tips

- Use connection pooling (PgBouncer)
- Add covering indexes for common queries
- Use LIMIT and cursor pagination
- Avoid SELECT * in production
- Use prepared statements
- Monitor slow queries with pg_stat_statements
- Vacuum tables regularly
- Consider table partitioning for large datasets

## When to Use This Skill

Invoke this skill when:
- Designing new database tables
- Setting up relationships
- Creating RLS policies
- Optimizing query performance
- Implementing soft deletes
- Setting up audit trails
- Writing migrations
- Debugging database issues
- Choosing data types
- Creating indexes
