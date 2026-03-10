---
name: nocobase-data-modeling
description: Create and manage NocoBase data models (collections, fields, relations) via API. Use when users want to design schemas and run collection/field operations programmatically.
argument-hint: "[collection-name] [operation: create|update|list|get]"
allowed-tools: Bash, Read
---

# Goal

Design and implement NocoBase data models through API calls.

# Workflow

1. Clarify modeling intent:
   - Create/update/list/get collections
   - Add/update/list fields
   - Configure relations
2. Ensure API authentication is ready by following `nocobase-api-call` skill rules.
3. Fetch API spec for data modeling namespace only:
   - Ask the agent to fetch Swagger using `nocobase-swagger-fetch` for `plugins%2Fdata-source-main`.
4. Parse Swagger response to identify endpoint, method, and payload schema.
5. Execute the request with `nocobase-api-call`:
   - Ask the agent to call the target endpoint and payload through `nocobase-api-call`.
6. Verify results by querying the created/updated collection or fields.
7. For complex schemas, prefer templates in `assets/collection-templates/`.

# Dependency Gate

- Required dependency skills: `nocobase-swagger-fetch`, `nocobase-api-call`.
- Never call another skill through direct script-path coupling.
- If required skills are missing, pause and ask user to install skills first (for example: `npx skills add nocobase/skills`).

# Mandatory Doc-Read Gate

- Do not construct API requests before fetching Swagger.
- Namespace is fixed to `plugins%2Fdata-source-main` for this skill.

# Resources

- `../nocobase-swagger-fetch/` - Shared swagger retrieval skill
- `../nocobase-api-call/` - Shared API execution skill
- `assets/collection-templates/` - Reusable schema templates

# Usage

```text
# 1) Read available endpoints in fixed namespace
Fetch Swagger for namespace `plugins%2Fdata-source-main`.

# 2) Inspect create collection API
Extract from returned Swagger JSON: .paths["/collections:create"]

# 3) Create collection
Ask the agent to create collection `products` via `nocobase-api-call` on endpoint `/collections:create`.

# 4) Verify
Ask the agent to verify collection `products` via `nocobase-api-call` on endpoint `/collections:get?filterByTk=products`.
```
