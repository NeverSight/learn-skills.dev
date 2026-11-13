---
name: supabase
version: "3.0.0"
description: Full Supabase database toolkit - schema explorer, natural language queries, CRUD, pgvector search, RLS policies, migrations, health checks, data export, Warehouse analytics, auto-embeddings, queues, Realtime, OAuth 2.1, Storage CDN, Edge Functions.
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-supabase
homepage: https://supabase.com
triggers:
  - supabase
  - database
  - postgres
  - sql query
  - vector search
  - pgvector
  - embeddings
  - schema
  - tables
  - CRUD
  - insert row
  - update row
  - delete row
  - select from
  - RLS
  - row level security
  - migration
  - health check
  - data export
  - similarity search
  - stored procedure
  - database size
  - warehouse
  - duckdb
  - analytics
  - auto-embeddings
  - queues
  - pgmq
  - realtime
  - presence
  - broadcast
  - oauth
  - storage
  - edge functions
  - stripe sync
  - log drains
metadata:
  openclaw:
    emoji: "\U0001F7E9"
    requires:
      env:
        - SUPABASE_URL
        - SUPABASE_SERVICE_KEY
    optionalEnv:
      - SUPABASE_API_KEY
      - SUPABASE_ACCESS_TOKEN
      - SUPABASE_DB_URL
      - OPENAI_API_KEY
    primaryEnv: SUPABASE_URL
    tags:
      - database
      - postgres
      - vector-search
      - pgvector
      - supabase
      - sql
      - crud
      - schema-explorer
      - rls
      - row-level-security
      - migrations
      - health-check
      - data-export
      - embeddings
      - natural-language-query
      - csv
      - json
      - warehouse
      - duckdb
      - analytics
      - queues
      - pgmq
      - realtime
      - oauth
      - storage
      - edge-functions
      - stripe-sync
      - log-drains
---

# Supabase Database Toolkit

Full database toolkit for Supabase projects: schema explorer, natural language queries, CRUD, vector search, RLS policy helper, migrations, health checks, data export, Warehouse analytics (pg_duckdb), automatic embeddings, queues (pgmq), Realtime, OAuth 2.1, Storage CDN, and Edge Functions.

> **API Key Migration (March 2026):** Supabase is deprecating legacy service keys starting March 11, 2026.
> New project-scoped keys use the `sb_publishable_` and `sb_secret_` prefixes. Get yours: Dashboard -> Settings -> API -> API Keys.
> Set `SUPABASE_API_KEY` for new projects. Legacy `SUPABASE_SERVICE_KEY` continues to work until late 2026.
> See the [Migration Guide](#api-key-migration-guide-march-2026) section below for step-by-step instructions.

> **OpenAPI spec restricted (March 11, 2026):** The auto-generated OpenAPI spec is now restricted to `service_role` keys only.
> Anon-key requests to `/rest/v1/` no longer return the spec. This hardens the default attack surface.

## Setup

```bash
# Required
export SUPABASE_URL="https://yourproject.supabase.co"
export SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIs..."  # legacy - use SUPABASE_API_KEY for new projects

# New project-scoped key (preferred, March 2026+)
export SUPABASE_API_KEY="sb_secret_..."

# Optional: for management API (org-level operations)
export SUPABASE_ACCESS_TOKEN="sbp_xxxxx"

# Optional: direct Postgres connection (enables SQL, migrations, health checks)
export SUPABASE_DB_URL="postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres"

# Optional: for generating embeddings in vector search
export OPENAI_API_KEY="sk-..."
```

## Quick Start

```bash
# List all tables in your database
{baseDir}/scripts/supabase.sh tables

# Explore a table's schema
{baseDir}/scripts/supabase.sh describe users

# Run a SQL query
{baseDir}/scripts/supabase.sh query "SELECT * FROM users LIMIT 5"

# Insert a row
{baseDir}/scripts/supabase.sh insert users '{"name": "Alice", "email": "alice@example.com"}'

# Vector similarity search
{baseDir}/scripts/supabase.sh vector-search documents "authentication setup" --limit 5

# Check database health
{baseDir}/scripts/supabase.sh health

# Export data as CSV
{baseDir}/scripts/supabase.sh export users --format csv > users.csv

# Analytics query via Warehouse (pg_duckdb)
{baseDir}/scripts/supabase.sh query "SELECT count(*) FROM analytics.events WHERE timestamp > now() - interval '7 days'"
```

---

## Supabase Warehouse / pg_duckdb

Supabase Warehouse (Feb 2026) embeds DuckDB inside Postgres via the `pg_duckdb` extension, providing up to 600x acceleration for analytics queries without moving data to a separate system.

### Key capabilities

- **600x faster analytics** - columnar scans, vectorized execution, and predicate pushdown inside Postgres
- **Analytics Buckets** - store cold/warm data in Apache Iceberg format on S3-compatible storage
- **Standard SQL** - query analytics tables with normal `SELECT` statements, no new syntax
- **Mixed workloads** - OLTP and OLAP in the same database, same connection

### Enable Warehouse

```sql
-- Enable the extension (requires Supabase Pro or higher)
CREATE EXTENSION IF NOT EXISTS pg_duckdb;
```

### Analytics Buckets (Iceberg on S3)

Analytics Buckets store large datasets in Iceberg format on S3 for cost-effective, high-performance scans.

```sql
-- Create an analytics bucket
SELECT duckdb.install_extension('iceberg');

-- Query an Iceberg table
SELECT count(*), date_trunc('hour', timestamp) as hour
FROM analytics.events
WHERE timestamp > now() - interval '7 days'
GROUP BY hour
ORDER BY hour;
```

### Example queries

```bash
# Count events in the last week
{baseDir}/scripts/supabase.sh query "SELECT count(*) FROM analytics.events WHERE timestamp > now() - interval '7 days'"

# Aggregate pageviews by path
{baseDir}/scripts/supabase.sh query "
  SELECT path, count(*) as views
  FROM analytics.pageviews
  WHERE timestamp > now() - interval '30 days'
  GROUP BY path
  ORDER BY views DESC
  LIMIT 20
"

# Join analytics data with transactional tables
{baseDir}/scripts/supabase.sh query "
  SELECT u.email, count(e.id) as event_count
  FROM public.users u
  JOIN analytics.events e ON e.user_id = u.id::text
  WHERE e.timestamp > now() - interval '7 days'
  GROUP BY u.email
  ORDER BY event_count DESC
  LIMIT 10
"
```

---

## Automatic Embeddings

Trigger-based pipeline that automatically generates vector embeddings when rows are inserted or updated. Uses pgmq queues, pg_cron (10-second batches), and Edge Functions for model-agnostic embedding generation.

### How it works

1. A trigger on your table enqueues new/updated rows into a pgmq queue
2. pg_cron polls the queue every 10 seconds
3. An Edge Function reads the batch, calls the embedding model, and writes vectors back
4. Embeddings are searchable via pgvector immediately

### Default model

OpenAI `text-embedding-3-small` (1536 dimensions). You can swap in any model by changing the Edge Function.

### Setup

```sql
-- 1. Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgmq;
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- 2. Create the embedding queue
SELECT pgmq.create('embed_queue');

-- 3. Add a trigger to enqueue rows on insert/update
CREATE OR REPLACE FUNCTION enqueue_for_embedding()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  PERFORM pgmq.send('embed_queue', jsonb_build_object(
    'table', TG_TABLE_NAME,
    'id', NEW.id,
    'content', NEW.content
  ));
  RETURN NEW;
END;
$$;

CREATE TRIGGER embed_on_change
  AFTER INSERT OR UPDATE OF content ON documents
  FOR EACH ROW
  EXECUTE FUNCTION enqueue_for_embedding();

-- 4. Schedule the batch processor (every 10 seconds)
SELECT cron.schedule('process-embeddings', '10 seconds',
  $$SELECT net.http_post(
    url := current_setting('app.settings.supabase_url') || '/functions/v1/generate-embeddings',
    headers := jsonb_build_object('Authorization', 'Bearer ' || current_setting('app.settings.service_role_key')),
    body := '{}'::jsonb
  )$$
);
```

### Example workflow

```bash
# Insert a document - embedding is auto-generated
{baseDir}/scripts/supabase.sh insert documents '{"content": "How to configure SSO with SAML providers"}'

# Wait ~10 seconds for the embedding pipeline, then search
{baseDir}/scripts/supabase.sh vector-search documents "single sign-on setup" --limit 5
```

---

## Queues / pgmq

Postgres-native message queues via the `pgmq` extension. Exactly-once delivery with configurable visibility windows.

### Key capabilities

- **Exactly-once delivery** - messages are invisible to other consumers during processing
- **Configurable visibility window** - set how long a message is locked (default 30 seconds)
- **pgmq_public schema** - safe for client-side consumers via PostgREST
- **pg_cron integration** - schedule workers to process queues on a cadence
- **Dead letter queues** - messages that fail repeatedly are moved aside

### Setup

```sql
-- Enable the extension
CREATE EXTENSION IF NOT EXISTS pgmq;

-- Create a queue
SELECT pgmq.create('my_queue');

-- Send a message
SELECT pgmq.send('my_queue', '{"task": "send_email", "to": "user@example.com"}'::jsonb);

-- Read a message (locks it for 30 seconds)
SELECT * FROM pgmq.read('my_queue', 30, 1);

-- Delete after processing
SELECT pgmq.delete('my_queue', <msg_id>);

-- Archive instead of delete (keeps history)
SELECT pgmq.archive('my_queue', <msg_id>);
```

### Client-side consumers (pgmq_public)

The `pgmq_public` schema exposes queue operations through PostgREST, so client apps can consume messages via the Supabase REST API.

```bash
# Read from queue via REST
curl "${SUPABASE_URL}/rest/v1/rpc/pgmq_public_read" \
  -H "apikey: ${SUPABASE_API_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_API_KEY}" \
  -d '{"queue_name": "my_queue", "vt": 30, "qty": 5}'
```

### Worker pattern: pgmq + pg_cron + Edge Functions

```sql
-- Schedule an Edge Function to process the queue every 10 seconds
SELECT cron.schedule('process-queue', '10 seconds',
  $$SELECT net.http_post(
    url := current_setting('app.settings.supabase_url') || '/functions/v1/process-my-queue',
    headers := jsonb_build_object('Authorization', 'Bearer ' || current_setting('app.settings.service_role_key')),
    body := '{}'::jsonb
  )$$
);
```

---

## Realtime

Supabase Realtime provides four capabilities for live data synchronization:

### Postgres Changes (WebSocket DB change notifications)

Listen to INSERT, UPDATE, DELETE events on any table via WebSocket. Respects RLS policies.

```javascript
// Client-side example (supabase-js)
const channel = supabase
  .channel('db-changes')
  .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' },
    (payload) => console.log('New message:', payload.new)
  )
  .subscribe();
```

### Broadcast (ephemeral pub/sub messaging)

Low-latency pub/sub for messages that don't need persistence. Good for typing indicators, cursor positions, game state.

```javascript
const channel = supabase.channel('room-1');
channel.on('broadcast', { event: 'cursor' }, (payload) => {
  console.log('Cursor moved:', payload);
});
channel.subscribe();
channel.send({ type: 'broadcast', event: 'cursor', payload: { x: 100, y: 200 } });
```

### Presence (shared state, online status)

Track who is online and share ephemeral state across clients.

```javascript
const channel = supabase.channel('online-users');
channel.on('presence', { event: 'sync' }, () => {
  const state = channel.presenceState();
  console.log('Online:', Object.keys(state));
});
channel.subscribe(async (status) => {
  if (status === 'SUBSCRIBED') {
    await channel.track({ user_id: 'abc', online_at: new Date().toISOString() });
  }
});
```

### Broadcast from Database (beta)

Trigger Realtime broadcasts directly from SQL using `realtime.send()`. Useful for server-side event broadcasting without client SDKs.

```sql
-- Send a broadcast from a trigger or function
SELECT realtime.send(
  'room-1',          -- channel
  'new-notification', -- event
  jsonb_build_object('message', 'You have a new order'), -- payload
  false               -- is_private
);
```

---

## Auth Enhancements

### OAuth 2.1 Server (Nov 2025 beta)

Supabase can now act as an OAuth 2.1 identity provider. Your Supabase project becomes the authorization server, issuing tokens that third-party apps can use.

- PKCE flow by default (no client secrets for public clients)
- Consent screen management in Dashboard
- Scopes and token lifetimes configurable per client
- Enable via Dashboard -> Authentication -> OAuth Applications

### X/Twitter OAuth 2.0 (Feb 2026)

Twitter/X login now uses OAuth 2.0 (replacing the legacy 1.0a flow). Update your provider configuration:

```bash
# Dashboard -> Authentication -> Providers -> Twitter
# Switch from OAuth 1.0a to OAuth 2.0
# Update Client ID and Client Secret from the X Developer Portal
```

---

## Storage Improvements (March 2026)

### Performance

- **14.8x faster object listing** on large datasets (rewritten listing engine)
- **Smart CDN** with automatic edge revalidation - no more stale cached files

### Features

- **Image Transformations** - resize, crop, and format-convert images on-the-fly via URL parameters
- **Resumable Uploads** - TUS protocol support for reliable large file uploads
- **S3 Compatibility** - use any S3-compatible client or SDK with your Supabase Storage

### Image Transformations example

```bash
# Original image
https://yourproject.supabase.co/storage/v1/object/public/images/photo.jpg

# Resize to 200x200
https://yourproject.supabase.co/storage/v1/render/image/public/images/photo.jpg?width=200&height=200

# Convert to WebP
https://yourproject.supabase.co/storage/v1/render/image/public/images/photo.jpg?format=webp&quality=80
```

### S3 Compatibility

```bash
# Use AWS CLI with Supabase Storage
aws s3 ls s3://your-bucket/ \
  --endpoint-url https://yourproject.supabase.co/storage/v1/s3

aws s3 cp ./file.pdf s3://your-bucket/uploads/ \
  --endpoint-url https://yourproject.supabase.co/storage/v1/s3
```

---

## Edge Functions

Deno-based serverless functions deployed at the edge, close to your users and database.

### Key capabilities

- **Regional invocations** - run functions near your database for lower latency
- **Rate limiting on recursive calls** (March 2026) - prevents runaway function chains
- **NPM compatibility** - import npm packages directly (`import express from "npm:express"`)
- **WASM support** - run WebAssembly modules inside Edge Functions

### Deploy and invoke

```bash
# Deploy a function
supabase functions deploy my-function

# Invoke via curl
curl -L "${SUPABASE_URL}/functions/v1/my-function" \
  -H "Authorization: Bearer ${SUPABASE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### Regional invocation

```bash
# Force execution in a specific region (near your database)
curl -L "${SUPABASE_URL}/functions/v1/my-function" \
  -H "Authorization: Bearer ${SUPABASE_API_KEY}" \
  -H "x-region: us-east-1" \
  -d '{}'
```

---

## Integrations

### Claude Connector (MCP)

32 MCP tools for Supabase - manage tables, query data, handle auth, and deploy functions directly from Claude or any MCP-compatible agent.

```bash
# Install the Supabase MCP server
npx @anthropic-ai/supabase-mcp
```

### Stripe Sync Engine

Query your Stripe data directly via SQL. The sync engine mirrors Stripe objects (customers, subscriptions, invoices) into your Supabase database.

```sql
-- Enable the Stripe sync (Dashboard -> Integrations -> Stripe)
-- Then query Stripe data with SQL
SELECT id, email, name FROM stripe.customers WHERE created > now() - interval '30 days';
SELECT subscription_id, status, current_period_end FROM stripe.subscriptions WHERE status = 'active';
```

### Log Drains (Pro plan)

Stream Supabase logs to external observability platforms:

- **Datadog** - metrics, logs, traces
- **Grafana / Loki** - log aggregation
- **Sentry** - error tracking
- **Axiom** - log analytics
- **S3** - raw log archival

Configure via Dashboard -> Settings -> Log Drains.

### PrivateLink for AWS VPC (Jan 2026)

Connect your Supabase project to your AWS VPC via AWS PrivateLink. Database traffic stays on the AWS backbone, never traversing the public internet.

Configure via Dashboard -> Settings -> Network -> PrivateLink.

---

## Database Branching

Create isolated database branches for preview environments. Each branch is a full copy of your schema with optional seed data.

```bash
# Create a branch (via Supabase CLI)
supabase branches create feat/new-feature

# Branch gets its own URL and keys
# Use in CI/CD for preview deployments
```

Branches are linked to Git branches. Merge the Git branch and the database branch is promoted or discarded.

---

## Read Replicas

Deploy read-only replicas in different regions for lower latency reads.

```bash
# Create a read replica (via Dashboard -> Settings -> Infrastructure -> Read Replicas)
# Each replica gets its own connection string

# Use in your app for read-heavy queries
export SUPABASE_DB_READ_URL="postgresql://postgres:[PASSWORD]@db-replica.[REF].supabase.co:5432/postgres"
```

---

## Supabase Vault

Encrypted secrets storage inside Postgres. Store API keys, tokens, and sensitive config without exposing them in application code.

```sql
-- Store a secret
SELECT vault.create_secret('my-api-key', 'sk-abc123...', 'API key for external service');

-- Retrieve a secret
SELECT * FROM vault.decrypted_secrets WHERE name = 'my-api-key';

-- Use in functions
CREATE OR REPLACE FUNCTION call_external_api()
RETURNS json
LANGUAGE plpgsql
AS $$
DECLARE
  api_key text;
BEGIN
  SELECT decrypted_secret INTO api_key FROM vault.decrypted_secrets WHERE name = 'my-api-key';
  -- use api_key in your request
END;
$$;
```

---

## Schema Explorer

Inspect your database structure without writing SQL. The schema explorer shows tables, columns, types, foreign key relationships, and RLS policies.

### List all tables

```bash
{baseDir}/scripts/supabase.sh tables
```

Returns all tables in the `public` schema with row counts.

### Describe a table

```bash
{baseDir}/scripts/supabase.sh describe <table>

# Examples
{baseDir}/scripts/supabase.sh describe users
{baseDir}/scripts/supabase.sh describe orders
```

Shows column names, data types, nullable status, defaults, and constraints. Also shows a sample row so you can see what the data looks like.

### Full schema dump

```bash
{baseDir}/scripts/supabase.sh schema
```

When `SUPABASE_DB_URL` is set, runs `pg_dump --schema-only` to show the complete schema including indexes, constraints, triggers, and functions. Without `SUPABASE_DB_URL`, falls back to querying `information_schema` via the REST API.

### Show foreign key relationships

```bash
{baseDir}/scripts/supabase.sh query "
  SELECT
    tc.table_name, kcu.column_name,
    ccu.table_name AS foreign_table,
    ccu.column_name AS foreign_column
  FROM information_schema.table_constraints tc
  JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
  JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
  WHERE tc.constraint_type = 'FOREIGN KEY'
"
```

### Show RLS policies on a table

```bash
{baseDir}/scripts/supabase.sh query "
  SELECT policyname, permissive, roles, cmd, qual, with_check
  FROM pg_policies
  WHERE tablename = 'your_table'
"
```

### Show indexes

```bash
{baseDir}/scripts/supabase.sh query "
  SELECT indexname, indexdef
  FROM pg_indexes
  WHERE tablename = 'your_table'
"
```

---

## Natural Language Query Builder

Describe what you want in plain English. The AI agent translates your request into SQL and runs it. No SQL knowledge required.

### How it works

When you say something like "show me all users who signed up in the last 7 days", the agent:

1. Inspects the target table's schema using `describe`
2. Builds the appropriate SQL query
3. Runs it via the `query` command
4. Returns formatted results

### Example natural language requests

| What you say | Generated SQL |
|-------------|---------------|
| "Show me all users who signed up in the last 7 days" | `SELECT * FROM users WHERE created_at > NOW() - INTERVAL '7 days'` |
| "Count orders by status" | `SELECT status, COUNT(*) FROM orders GROUP BY status` |
| "Find products under $50 sorted by price" | `SELECT * FROM products WHERE price < 50 ORDER BY price ASC` |
| "Top 10 customers by total spend" | `SELECT user_id, SUM(total) as spend FROM orders GROUP BY user_id ORDER BY spend DESC LIMIT 10` |
| "Users who haven't logged in for 30 days" | `SELECT * FROM users WHERE last_login < NOW() - INTERVAL '30 days'` |
| "Average order value by month" | `SELECT DATE_TRUNC('month', created_at) as month, AVG(total) FROM orders GROUP BY month ORDER BY month` |

### Tips for natural language queries

- Mention the table name if it's not obvious ("from the orders table...")
- Specify date ranges explicitly ("last 7 days", "since January", "in 2025")
- Ask for aggregations naturally ("count", "average", "total", "top 10")
- Request specific columns if you don't need everything ("just the name and email")

---

## CRUD Operations

### query - Run raw SQL

```bash
{baseDir}/scripts/supabase.sh query "<SQL>"

# Examples
{baseDir}/scripts/supabase.sh query "SELECT COUNT(*) FROM users"
{baseDir}/scripts/supabase.sh query "CREATE TABLE items (id serial primary key, name text, price numeric)"
{baseDir}/scripts/supabase.sh query "SELECT * FROM users WHERE created_at > '2025-01-01'"
{baseDir}/scripts/supabase.sh query "SELECT u.name, COUNT(o.id) as order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.name"
```

Raw SQL requires an `exec_sql` function in your database. If it doesn't exist, the script will tell you how to create it.

### select - Query table with filters

```bash
{baseDir}/scripts/supabase.sh select <table> [options]

Options:
  --columns <cols>    Comma-separated columns (default: *)
  --eq <col:val>      Equal filter (can use multiple)
  --neq <col:val>     Not equal filter
  --gt <col:val>      Greater than
  --lt <col:val>      Less than
  --gte <col:val>     Greater than or equal
  --lte <col:val>     Less than or equal
  --like <col:val>    Pattern match (use % for wildcard)
  --ilike <col:val>   Case-insensitive pattern match
  --is <col:val>      IS filter (for null, true, false)
  --in <col:vals>     IN filter (comma-separated values)
  --limit <n>         Limit results
  --offset <n>        Offset results
  --order <col>       Order by column
  --desc              Descending order

# Examples
{baseDir}/scripts/supabase.sh select users --eq "status:active" --limit 10
{baseDir}/scripts/supabase.sh select posts --columns "id,title,created_at" --order created_at --desc
{baseDir}/scripts/supabase.sh select products --gt "price:100" --lt "price:500"
{baseDir}/scripts/supabase.sh select orders --gte "total:1000" --order total --desc --limit 20
{baseDir}/scripts/supabase.sh select users --ilike "email:%@gmail.com"
{baseDir}/scripts/supabase.sh select items --is "deleted_at:null" --order created_at --desc
{baseDir}/scripts/supabase.sh select users --in "role:admin,moderator,editor"
```

### insert - Insert row(s)

```bash
{baseDir}/scripts/supabase.sh insert <table> '<json>'

# Single row
{baseDir}/scripts/supabase.sh insert users '{"name": "Alice", "email": "alice@test.com"}'

# Multiple rows (JSON array)
{baseDir}/scripts/supabase.sh insert users '[{"name": "Bob", "email": "bob@test.com"}, {"name": "Carol", "email": "carol@test.com"}]'

# With nested JSON
{baseDir}/scripts/supabase.sh insert events '{"type": "signup", "metadata": {"source": "landing_page", "utm": "twitter"}}'
```

### update - Update rows

```bash
{baseDir}/scripts/supabase.sh update <table> '<json>' --eq <col:val>

# Update a single row by ID
{baseDir}/scripts/supabase.sh update users '{"status": "inactive"}' --eq "id:123"

# Update multiple rows matching a filter
{baseDir}/scripts/supabase.sh update posts '{"published": true}' --eq "author_id:5"

# Update with multiple filters
{baseDir}/scripts/supabase.sh update orders '{"shipped": true}' --eq "status:paid" --gt "total:100"
```

Always requires at least one filter to prevent accidental full-table updates.

### upsert - Insert or update

```bash
{baseDir}/scripts/supabase.sh upsert <table> '<json>'

# Requires a unique constraint on the matching column
{baseDir}/scripts/supabase.sh upsert users '{"id": 1, "name": "Updated Name", "email": "new@email.com"}'

# Bulk upsert
{baseDir}/scripts/supabase.sh upsert products '[{"sku": "ABC", "price": 29.99}, {"sku": "DEF", "price": 49.99}]'
```

### delete - Delete rows

```bash
{baseDir}/scripts/supabase.sh delete <table> --eq <col:val>

# Delete by ID
{baseDir}/scripts/supabase.sh delete users --eq "id:123"

# Delete expired sessions
{baseDir}/scripts/supabase.sh delete sessions --lt "expires_at:2025-01-01"

# Delete with multiple conditions
{baseDir}/scripts/supabase.sh delete logs --eq "level:debug" --lt "created_at:2025-06-01"
```

Always requires at least one filter to prevent accidental full-table deletes.

### rpc - Call stored procedure

```bash
{baseDir}/scripts/supabase.sh rpc <function_name> '<json_params>'

# Example
{baseDir}/scripts/supabase.sh rpc get_user_stats '{"user_id": 123}'
{baseDir}/scripts/supabase.sh rpc calculate_revenue '{"start_date": "2025-01-01", "end_date": "2025-12-31"}'
{baseDir}/scripts/supabase.sh rpc search_products '{"term": "wireless", "category": "electronics"}'
```

---

## Vector Search (pgvector)

Similarity search using pgvector embeddings. Search documents, products, or any content by meaning rather than exact keywords.

### vector-search command

```bash
{baseDir}/scripts/supabase.sh vector-search <table> "<query>" [options]

Options:
  --match-fn <name>     RPC function name (default: match_<table>)
  --limit <n>           Number of results (default: 5)
  --threshold <n>       Similarity threshold 0-1 (default: 0.5)

# Examples
{baseDir}/scripts/supabase.sh vector-search documents "How to set up authentication" --limit 10
{baseDir}/scripts/supabase.sh vector-search products "comfortable running shoes" --threshold 0.7
{baseDir}/scripts/supabase.sh vector-search faq "billing questions" --match-fn search_faq --limit 20
```

Requires `OPENAI_API_KEY` for embedding generation (uses text-embedding-3-small, 1536 dimensions).

### Setup: Enable pgvector

```sql
-- 1. Enable the extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create a table with an embedding column
CREATE TABLE documents (
  id bigserial PRIMARY KEY,
  content text NOT NULL,
  metadata jsonb DEFAULT '{}',
  embedding vector(1536),
  created_at timestamptz DEFAULT now()
);

-- 3. Create the similarity search function
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1536),
  match_threshold float DEFAULT 0.5,
  match_count int DEFAULT 5
)
RETURNS TABLE (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- 4. Create an index for performance (do this after inserting data)
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### Choosing the right index

| Index Type | Best For | Trade-off |
|-----------|---------|-----------|
| `ivfflat` | Most use cases, fast queries | Approximate results, needs training data |
| `hnsw` | High recall requirements | Uses more memory, slower builds |
| None | Small tables (<1000 rows) | Exact results, slow on large tables |

```sql
-- HNSW index (better recall, more memory)
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

---

## RLS Policy Helper

Row Level Security (RLS) protects your data by restricting which rows users can access. Use natural language to describe your access rules and the agent generates the SQL policies.

### How to use

Describe your access control rules in plain English. The agent generates `CREATE POLICY` statements.

### Example policy requests and generated SQL

**"Users can only see their own profile"**

```sql
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = user_id);
```

**"Admins can do anything, regular users can only read"**

```sql
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admins full access"
  ON posts FOR ALL
  USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Users read only"
  ON posts FOR SELECT
  USING (true);
```

**"Users can insert their own rows and update them, but not delete"**

```sql
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users insert own comments"
  ON comments FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users update own comments"
  ON comments FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users view all comments"
  ON comments FOR SELECT
  USING (true);
```

**"Team members can access shared resources"**

```sql
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Team members access shared resources"
  ON resources FOR SELECT
  USING (
    team_id IN (
      SELECT team_id FROM team_members WHERE user_id = auth.uid()
    )
  );
```

### View existing policies

```bash
{baseDir}/scripts/supabase.sh query "SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual FROM pg_policies WHERE schemaname = 'public'"
```

### Common RLS patterns

| Pattern | USING clause |
|---------|-------------|
| Own data only | `auth.uid() = user_id` |
| Role-based | `auth.jwt() ->> 'role' = 'admin'` |
| Team-based | `team_id IN (SELECT team_id FROM members WHERE user_id = auth.uid())` |
| Public read | `true` (for SELECT policy) |
| Authenticated only | `auth.role() = 'authenticated'` |
| Time-based | `created_at > now() - interval '30 days'` |

### Important notes on RLS

- The `SUPABASE_SERVICE_KEY` (service role) **bypasses RLS** entirely. Use the anon key to test policies.
- Always enable RLS on tables that store user data: `ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;`
- Test policies with: `SET ROLE authenticated; SET request.jwt.claims = '{"sub": "user-uuid"}';`

---

## Migration Management

Basic migration support for tracking schema changes. Requires `SUPABASE_DB_URL` for direct Postgres access.

### Create a migration

```bash
# Generate a timestamped migration file
{baseDir}/scripts/supabase.sh migration create "add_orders_table"
# Creates: migrations/20260315120000_add_orders_table.sql
```

Edit the generated file with your SQL, then apply it:

### Apply migrations

```bash
# Run all pending migrations
{baseDir}/scripts/supabase.sh migration up

# Check migration status
{baseDir}/scripts/supabase.sh migration status
```

### Migration best practices

- One logical change per migration (don't mix table creation with data changes)
- Always test migrations on a branch database first
- Use `IF NOT EXISTS` / `IF EXISTS` for idempotent migrations
- Keep migrations small and reversible when possible

### Example migration file

```sql
-- migrations/20260315120000_add_orders_table.sql

CREATE TABLE IF NOT EXISTS orders (
  id bigserial PRIMARY KEY,
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
  total numeric(10,2) NOT NULL DEFAULT 0,
  items jsonb NOT NULL DEFAULT '[]',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own orders"
  ON orders FOR SELECT
  USING (auth.uid() = user_id);
```

---

## Health Check

Monitor your Supabase database health. Works best with `SUPABASE_DB_URL` set for direct Postgres access.

### Run health check

```bash
{baseDir}/scripts/supabase.sh health
```

Reports:
- **Connection status** - can we reach the database?
- **Database size** - total size on disk
- **Active connections** - current connection count vs max
- **Table sizes** - largest tables by row count and disk size
- **Slow queries** - currently running queries over 1 second
- **Index usage** - tables with low index hit rates (potential missing indexes)

### Individual health queries

```bash
# Database size
{baseDir}/scripts/supabase.sh query "SELECT pg_size_pretty(pg_database_size(current_database())) as db_size"

# Active connections
{baseDir}/scripts/supabase.sh query "SELECT count(*) as active, (SELECT setting FROM pg_settings WHERE name = 'max_connections') as max FROM pg_stat_activity"

# Table sizes (top 10)
{baseDir}/scripts/supabase.sh query "
  SELECT relname as table_name,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size,
    n_live_tup as row_count
  FROM pg_stat_user_tables
  ORDER BY pg_total_relation_size(relid) DESC
  LIMIT 10
"

# Slow queries (running > 1 second)
{baseDir}/scripts/supabase.sh query "
  SELECT pid, now() - pg_stat_activity.query_start as duration, query
  FROM pg_stat_activity
  WHERE state = 'active' AND now() - pg_stat_activity.query_start > interval '1 second'
  ORDER BY duration DESC
"

# Index usage (find tables that might need indexes)
{baseDir}/scripts/supabase.sh query "
  SELECT relname as table_name,
    seq_scan, idx_scan,
    CASE WHEN seq_scan + idx_scan > 0
      THEN round(100.0 * idx_scan / (seq_scan + idx_scan), 1)
      ELSE 0
    END as idx_hit_pct
  FROM pg_stat_user_tables
  WHERE seq_scan + idx_scan > 100
  ORDER BY idx_hit_pct ASC
  LIMIT 10
"

# Cache hit ratio
{baseDir}/scripts/supabase.sh query "
  SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    CASE WHEN sum(heap_blks_hit) + sum(heap_blks_read) > 0
      THEN round(sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))::numeric, 4)
      ELSE 0
    END as cache_hit_ratio
  FROM pg_statio_user_tables
"
```

---

## Data Export

Export table data in CSV or JSON format.

### Export commands

```bash
# Export as JSON (default)
{baseDir}/scripts/supabase.sh export <table> [--format json] [--limit N]

# Export as CSV
{baseDir}/scripts/supabase.sh export <table> --format csv [--limit N]

# Examples
{baseDir}/scripts/supabase.sh export users --format csv > users.csv
{baseDir}/scripts/supabase.sh export orders --format json --limit 1000 > orders.json
{baseDir}/scripts/supabase.sh export products --format csv --eq "active:true" > active_products.csv
```

### Export with filters

All the same filters from `select` work with `export`:

```bash
{baseDir}/scripts/supabase.sh export orders --format csv --gt "total:100" --order total --desc
{baseDir}/scripts/supabase.sh export users --format csv --eq "status:active" --columns "id,name,email"
```

### Large exports

For tables with many rows, use `--limit` and `--offset` to paginate:

```bash
# Export first 10000 rows
{baseDir}/scripts/supabase.sh export events --format csv --limit 10000

# Export next batch
{baseDir}/scripts/supabase.sh export events --format csv --limit 10000 --offset 10000
```

---

## API Key Migration Guide (March 2026)

Supabase began deprecating legacy API keys on March 11, 2026. Here is what you need to do.

### What changed

| Key Type | Old Format | New Format | Status |
|----------|-----------|------------|--------|
| Service role | `eyJhbGciOiJIUzI1NiIs...` (JWT) | `sb_secret_...` (project-scoped) | Legacy works until late 2026 |
| Publishable | `eyJhbGciOiJIUzI1NiIs...` (JWT) | `sb_publishable_...` (project-scoped) | Legacy works until late 2026 |
| Access token | `sbp_...` | No change | Already uses new format |

### Step-by-step migration

1. Go to your Supabase Dashboard -> Settings -> API -> API Keys
2. Copy your new project-scoped service key (starts with `sb_secret_`)
3. Update your environment:

```bash
# Old way (still works until late 2026)
export SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIs..."

# New way (preferred)
export SUPABASE_API_KEY="sb_secret_..."
```

4. The skill auto-detects which key you are using. Both work during the transition period.

### Testing the new key

```bash
# Verify your connection with the new key
{baseDir}/scripts/supabase.sh tables
```

If you see your tables listed, the new key is working correctly.

---

## Error Recovery

### Connection refused

```
Error: Could not connect to SUPABASE_URL
```

- Verify `SUPABASE_URL` is correct (should be `https://[ref].supabase.co`)
- Check if your project is paused (free tier pauses after 7 days of inactivity)
- Unpause from Dashboard -> Settings -> General

### Authentication failed

```
Error: Invalid API key
```

- Check that `SUPABASE_SERVICE_KEY` or `SUPABASE_API_KEY` is set correctly
- Service keys should start with `eyJ` (legacy JWT) or `sb_secret_` (new project-scoped)
- Keys are project-specific - make sure you are using the right one

### Query errors

```
Error: relation "table_name" does not exist
```

- Table might be in a different schema (try `public.table_name`)
- Check available tables: `{baseDir}/scripts/supabase.sh tables`

```
Error: Could not find the function exec_sql
```

- Raw SQL queries require an `exec_sql` function. Create it:

```sql
CREATE OR REPLACE FUNCTION exec_sql(query text)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result json;
BEGIN
  EXECUTE query INTO result;
  RETURN result;
END;
$$;
```

### pgvector not enabled

```
Error: type "vector" does not exist
```

- Enable the extension: `CREATE EXTENSION IF NOT EXISTS vector;`
- Requires Supabase Pro plan or self-hosted instance with pgvector installed

### Permission denied

```
Error: permission denied for table
```

- Service role key should bypass RLS. If you see this, check that you are using the service key, not the anon key.
- For management API operations, you need `SUPABASE_ACCESS_TOKEN`.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Project URL (`https://[ref].supabase.co`) |
| `SUPABASE_SERVICE_KEY` | Yes* | Service role key (full access, bypasses RLS) |
| `SUPABASE_API_KEY` | No* | New project-scoped key (March 2026+, replaces service key) |
| `SUPABASE_ANON_KEY` | No | Anon key (restricted access, respects RLS) |
| `SUPABASE_ACCESS_TOKEN` | No | Management API token (org-level operations) |
| `SUPABASE_DB_URL` | No | Direct Postgres connection string (enables migrations, health, schema dump) |
| `OPENAI_API_KEY` | No | For generating embeddings in vector search |

*Either `SUPABASE_SERVICE_KEY` or `SUPABASE_API_KEY` is required. The skill tries `SUPABASE_API_KEY` first, falls back to `SUPABASE_SERVICE_KEY`.

---

## Advanced Usage

### Combine with other skills

- Use **/parallel** to research web APIs while querying your database - compare external data against your internal records
- Use **/last30days** to pull recent social media trends, then store the results in Supabase for analysis
- Use **/supabase** to export data, then pipe it into analysis tools

### Batch operations

```bash
# Insert many rows from a JSON file
cat data.json | {baseDir}/scripts/supabase.sh insert products

# Run multiple queries from a file
while IFS= read -r sql; do
  {baseDir}/scripts/supabase.sh query "$sql"
done < queries.txt
```

### Monitoring patterns

```bash
# Daily health check
{baseDir}/scripts/supabase.sh health

# Check for tables without RLS
{baseDir}/scripts/supabase.sh query "
  SELECT tablename
  FROM pg_tables
  WHERE schemaname = 'public'
  AND tablename NOT IN (SELECT tablename FROM pg_policies)
"

# Find unused indexes
{baseDir}/scripts/supabase.sh query "
  SELECT indexrelid::regclass as index, relid::regclass as table,
    idx_scan, pg_size_pretty(pg_relation_size(indexrelid)) as size
  FROM pg_stat_user_indexes
  WHERE idx_scan = 0
  ORDER BY pg_relation_size(indexrelid) DESC
"
```

---

## Notes

- Service role key bypasses RLS (Row Level Security) - use anon key for client-side access
- Vector search requires pgvector extension and a match function in your database
- Embeddings default to OpenAI text-embedding-3-small (1536 dimensions)
- Direct SQL via `query` requires an `exec_sql` function (see Error Recovery section)
- Migrations and health checks work best with `SUPABASE_DB_URL` for direct Postgres access
- All REST API calls go through PostgREST at `SUPABASE_URL/rest/v1`
- The skill supports both legacy JWT keys and new project-scoped `sb_secret_` / `sb_publishable_` keys
- Warehouse analytics (pg_duckdb) requires Supabase Pro or higher
- Automatic embeddings pipeline uses pgmq + pg_cron + Edge Functions
- OpenAPI spec is restricted to service_role keys as of March 11, 2026
