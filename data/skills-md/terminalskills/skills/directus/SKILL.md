---
name: directus
description: >-
  Build backends and APIs with Directus headless CMS. Use when a user asks to
  create a headless CMS, build a content API without coding, set up a backend
  admin panel, create REST or GraphQL APIs from a database, manage content with
  roles and permissions, build a data platform with auto-generated APIs, or
  replace traditional CMS with a headless solution. Covers data modeling,
  auto-generated REST/GraphQL APIs, roles/permissions, flows (automation),
  file storage, and SDK integration.
license: Apache-2.0
compatibility: 'Node.js 18+ or Docker (any SQL database)'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - directus
    - cms
    - headless
    - api
    - backend
    - admin
---

# Directus

## Overview

Directus is an open-source headless CMS and data platform that wraps any SQL database with auto-generated REST and GraphQL APIs, a visual admin dashboard, role-based access control, file storage, and automation flows. Unlike Strapi (which defines its own schema), Directus mirrors your existing database — add columns in the admin UI or directly in SQL, and the API updates instantly. Use it for content management, internal tools, data APIs, and backend-as-a-service.

## Instructions

### Step 1: Deployment

```bash
# Docker (quickest start)
docker run -d --name directus \
  -p 8055:8055 \
  -e SECRET="your-secret-key-min-32-chars" \
  -e ADMIN_EMAIL="admin@example.com" \
  -e ADMIN_PASSWORD="your-secure-password" \
  -e DB_CLIENT="sqlite3" \
  -e DB_FILENAME="/directus/database/data.db" \
  -v directus_data:/directus/database \
  -v directus_uploads:/directus/uploads \
  directus/directus:latest

# Production with PostgreSQL
docker run -d --name directus \
  -p 8055:8055 \
  -e SECRET="your-secret-key" \
  -e ADMIN_EMAIL="admin@example.com" \
  -e ADMIN_PASSWORD="your-secure-password" \
  -e DB_CLIENT="pg" \
  -e DB_HOST="postgres" \
  -e DB_PORT="5432" \
  -e DB_DATABASE="directus" \
  -e DB_USER="directus" \
  -e DB_PASSWORD="dbpassword" \
  directus/directus:latest

# Access admin: http://localhost:8055
```

### Step 2: Data Modeling

Create collections (tables) and fields via the admin UI or REST API:

```bash
# Create a "posts" collection via API
curl -X POST http://localhost:8055/collections \
  -H 'Authorization: Bearer admin_token' \
  -H 'Content-Type: application/json' \
  -d '{
    "collection": "posts",
    "meta": { "icon": "article", "note": "Blog posts" },
    "fields": [
      { "field": "id", "type": "uuid", "meta": { "special": ["uuid"] }, "schema": { "is_primary_key": true } },
      { "field": "title", "type": "string", "meta": { "required": true } },
      { "field": "slug", "type": "string", "meta": { "interface": "input" } },
      { "field": "content", "type": "text", "meta": { "interface": "input-rich-text-html" } },
      { "field": "status", "type": "string", "meta": { "interface": "select-dropdown", "options": { "choices": [{"text":"Draft","value":"draft"},{"text":"Published","value":"published"}] } } },
      { "field": "published_at", "type": "timestamp" }
    ]
  }'
```

### Step 3: Auto-Generated APIs

Once collections exist, Directus auto-generates full CRUD APIs:

```bash
# REST — List all published posts
curl 'http://localhost:8055/items/posts?filter[status][_eq]=published&sort=-published_at&limit=10' \
  -H 'Authorization: Bearer token'

# REST — Get single post with related author
curl 'http://localhost:8055/items/posts/POST_ID?fields=*,author.name,author.avatar' \
  -H 'Authorization: Bearer token'

# REST — Create post
curl -X POST http://localhost:8055/items/posts \
  -H 'Authorization: Bearer token' \
  -H 'Content-Type: application/json' \
  -d '{"title": "My Post", "content": "<p>Hello world</p>", "status": "draft"}'

# GraphQL — Same queries
curl -X POST http://localhost:8055/graphql \
  -H 'Authorization: Bearer token' \
  -H 'Content-Type: application/json' \
  -d '{"query": "{ posts(filter: {status: {_eq: \"published\"}}, sort: [\"-published_at\"], limit: 10) { id title content published_at author { name } } }"}'
```

### Step 4: SDK Integration

```javascript
// lib/directus.js — JavaScript SDK for frontend/backend integration
import { createDirectus, rest, readItems, createItem, authentication } from '@directus/sdk'

const client = createDirectus('http://localhost:8055')
  .with(authentication())
  .with(rest())

// Fetch published posts
const posts = await client.request(
  readItems('posts', {
    filter: { status: { _eq: 'published' } },
    sort: ['-published_at'],
    limit: 10,
    fields: ['id', 'title', 'slug', 'content', 'published_at', { author: ['name', 'avatar'] }],
  })
)

// Create a new post
const newPost = await client.request(
  createItem('posts', {
    title: 'New Post',
    content: '<p>Content here</p>',
    status: 'draft',
  })
)
```

### Step 5: Roles and Permissions

```bash
# Create a read-only "viewer" role
curl -X POST http://localhost:8055/roles \
  -H 'Authorization: Bearer admin_token' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Viewer", "admin_access": false}'

# Set permissions: viewer can read published posts only
curl -X POST http://localhost:8055/permissions \
  -H 'Authorization: Bearer admin_token' \
  -H 'Content-Type: application/json' \
  -d '{
    "role": "VIEWER_ROLE_ID",
    "collection": "posts",
    "action": "read",
    "permissions": { "status": { "_eq": "published" } },
    "fields": ["id", "title", "content", "published_at"]
  }'
```

### Step 6: Flows (Automation)

Directus Flows are visual automation pipelines triggered by events (like Zapier, but built-in).

```bash
# Create a flow: when a post is published, send a webhook
curl -X POST http://localhost:8055/flows \
  -H 'Authorization: Bearer admin_token' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Notify on Publish",
    "trigger": "event",
    "options": { "type": "action", "scope": ["items.update"], "collections": ["posts"] },
    "accountability": "all",
    "status": "active"
  }'
```

## Examples

### Example 1: Build a content API for a marketing website
**User prompt:** "I need a CMS backend for our marketing site — blog posts, team members, case studies, and FAQ. Non-technical editors should be able to manage content through a visual dashboard."

The agent will:
1. Deploy Directus with Docker + PostgreSQL.
2. Create collections for posts, team_members, case_studies, and faqs.
3. Set up relational fields (posts → author, case studies → tags).
4. Configure a public role with read-only access for the frontend.
5. Connect the Next.js/Astro frontend using the Directus SDK.

### Example 2: Build an internal tool for operations data
**User prompt:** "Our ops team tracks orders, suppliers, and inventory in spreadsheets. Build a proper backend with an admin panel where they can manage everything."

The agent will:
1. Deploy Directus pointing at the existing PostgreSQL database.
2. Directus auto-detects existing tables and generates APIs + admin UI.
3. Create roles: admin (full access), manager (CRUD), viewer (read-only).
4. Set up flows for notifications (new order → Slack alert).

## Guidelines

- Directus mirrors your database schema — it does not own it. You can add columns via Directus admin or directly in SQL, and both stay in sync. This makes it safe for existing databases.
- Use Directus as a backend-as-a-service for content-heavy apps. For complex business logic (multi-step workflows, custom calculations), extend with custom endpoints or use a separate API layer.
- Configure the `PUBLIC` role carefully — it defines what unauthenticated users can access. For a public blog, allow read access to published posts only.
- File uploads go to local storage by default. In production, configure S3, Cloudflare R2, or Google Cloud Storage for scalability.
- Directus supports PostgreSQL, MySQL, MariaDB, MS SQL, SQLite, CockroachDB, and OracleDB. PostgreSQL is recommended for production.
