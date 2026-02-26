---
name: memberstack-admin-api
description: Work with the Memberstack Admin API to manage members, plans, and data tables. Use this skill whenever the user mentions Memberstack, member management via API, Memberstack data tables, or wants to build integrations that create/read/update/delete members or data records in Memberstack. Also trigger when the user asks about Memberstack API endpoints, authentication, pagination, querying records, or connecting plans to members — even if they don't say "Memberstack" explicitly but reference concepts like plan connections, member metadata, or admin member APIs that align with Memberstack's domain.
license: MIT
metadata:
  author: "[Ben Sabic](https://bensabic.dev)"
  version: "1.0.0"
---

# Memberstack Admin API Skill

This skill provides guidance for interacting with the Memberstack Admin API. It covers two core domains: **Member management** and **Data Tables**.

## Quick Start

All requests require an API key passed via header:

```
x-api-key: YOUR_API_KEY
```

Base URL: `https://admin.memberstack.com`

Data Tables endpoints use the `/v2/` prefix; Member endpoints do not.

## API Key Handling

Never ask the user for their API key directly in the conversation. API keys are sensitive credentials and should never appear in chat, code snippets shown to the user, or be hardcoded in source files. Instead:

- Store the key in a `.env` file (e.g., `MEMBERSTACK_API_KEY=sk_...`) and read it via `process.env.MEMBERSTACK_API_KEY` (Node) or `os.environ["MEMBERSTACK_API_KEY"]` (Python).
- Alternatively, use the platform's secrets/environment variable management (e.g., Vercel Environment Variables, Cloudflare Secrets, AWS Secrets Manager).
- When generating code, always reference the key from an environment variable, never use a placeholder that looks like a real key.
- If the user pastes an API key in the chat, remind them to rotate it and move it to a `.env` file or secret store instead.

## When to Read Reference Files

This skill bundles the full API reference docs. Read them based on what the user needs:

- **Member operations** (list, get, create, update, delete, add/remove plans):
  Read `references/memberstack-member-actions.md`

- **Data Tables** (list tables, get table schema, create/update/delete/query records):
  Read `references/memberstack-data-tables.md`

If the task involves both members and data tables, read both files.

## API Overview

### Members API

Endpoints for managing members, their profiles, plan connections, and metadata.

| Action | Method | Endpoint |
|--------|--------|----------|
| List members | GET | `/members` |
| Get member | GET | `/members/:id_or_email` |
| Create member | POST | `/members` |
| Update member | PATCH | `/members/:id` |
| Delete member | DELETE | `/members/:id` |
| Add free plan | POST | `/members/:id/add-plan` |
| Remove free plan | POST | `/members/:id/remove-plan` |

Key concepts:
- Member IDs start with `mem_`, plan IDs with `pln_`, connection IDs with `con_`
- Members can be looked up by ID or URL-encoded email
- Pagination uses cursor-based `after` + `limit` (max 200)
- Members have `customFields`, `metaData`, `json`, `permissions`, and `planConnections`

### Data Tables API

Endpoints for managing structured data with typed fields, relationships, and querying.

| Action | Method | Endpoint |
|--------|--------|----------|
| List tables | GET | `/v2/data-tables` |
| Get table | GET | `/v2/data-tables/:tableKey` |
| Create record | POST | `/v2/data-tables/:tableKey/records` |
| Update record | PUT | `/v2/data-tables/:tableKey/records/:recordId` |
| Delete record | DELETE | `/v2/data-tables/:tableKey/records/:recordId` |
| Query records | POST | `/v2/data-tables/:tableKey/records/query` |

Key concepts:
- Tables are referenced by key (e.g., `products`) or ID (e.g., `tbl_...`)
- Records hold data as key-value pairs matching field definitions
- Querying supports `findMany` and `findUnique` with rich filtering (`equals`, `contains`, `gt`, `lt`, `in`, logical operators `AND`/`OR`/`NOT`)
- Pagination via `take` (max 100), `skip`, or cursor-based `after`
- Field types include TEXT, NUMBER, DECIMAL, BOOLEAN, DATE, EMAIL, URL, REFERENCE, and MEMBER_REFERENCE variants

## Common Patterns

### Paginating Through All Members

```javascript
let allMembers = [];
let cursor = undefined;
let hasMore = true;

while (hasMore) {
  const params = new URLSearchParams({ limit: '200' });
  if (cursor) params.set('after', cursor);

  const res = await fetch(`https://admin.memberstack.com/members?${params}`, {
    headers: { 'x-api-key': API_KEY }
  });
  const json = await res.json();

  allMembers.push(...json.data);
  hasMore = json.hasNextPage;
  cursor = json.endCursor;
}
```

### Querying Data Records with Filters

```javascript
const res = await fetch(
  'https://admin.memberstack.com/v2/data-tables/products/records/query',
  {
    method: 'POST',
    headers: {
      'x-api-key': API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: {
        findMany: {
          where: {
            AND: [
              { price: { gte: 10 } },
              { inStock: { equals: true } }
            ]
          },
          orderBy: { price: 'asc' },
          take: 50
        }
      }
    })
  }
);
```

### Creating a Member with a Plan

```javascript
const res = await fetch('https://admin.memberstack.com/members', {
  method: 'POST',
  headers: {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securePassword123',
    plans: [{ planId: 'pln_abc123' }],
    customFields: { firstName: 'Jane', country: 'Australia' }
  })
});
```

## Error Handling

The API returns errors as JSON with `code` and `message` fields. Common status codes:
- **400**: Bad request (missing required fields, invalid formats, empty data)
- **404**: Resource not found (wrong table key, nonexistent member/record)

Always check for these and surface clear messages to the user.

## Tips

- When deleting members, consider setting `deleteStripeCustomer` and `cancelStripeSubscriptions` to avoid orphaned billing records.
- Use `findUnique` with `where.id` when you know the exact record ID — it's simpler and returns a single record.
- The `_count` option in `findMany` is useful for getting totals without fetching all records.
- `select` and `include` are mutually exclusive in queries — use `include` to expand relationships, `select` to limit returned fields.