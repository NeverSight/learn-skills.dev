---
name: omni-content-explorer
description: Find, browse, and organize content in Omni Analytics — dashboards, workbooks, folders, and labels — using the REST API. Use this skill whenever someone wants to find an existing dashboard, search for content, list workbooks, browse folders, see what dashboards exist, find popular reports, download a dashboard as PDF or PNG, favorite content, manage labels on documents, or any variant of "find the dashboard about", "what reports do we have", "show me our dashboards", "where is the sales report", or "download this dashboard".
---

# Omni Content Explorer

Find, browse, and organize Omni content — dashboards, workbooks, and folders — through the REST API.

## Prerequisites

```bash
export OMNI_BASE_URL="https://yourorg.omniapp.co"
export OMNI_API_KEY="your-api-key"
```

## API Discovery

When unsure whether an endpoint or parameter exists, fetch the OpenAPI spec:

```bash
curl -L "$OMNI_BASE_URL/openapi.json" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

Use this to verify endpoints, available parameters, and request/response schemas before making calls.

## Browsing Content

### List All Content

```bash
curl -L "$OMNI_BASE_URL/api/v1/content" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

### With Counts and Labels

```bash
curl -L "$OMNI_BASE_URL/api/v1/content?include=_count,labels" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

### Filter and Sort

```bash
# By label
curl -L "$OMNI_BASE_URL/api/v1/content?labels=finance,marketing" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# By scope
curl -L "$OMNI_BASE_URL/api/v1/content?scope=organization" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Sort by popularity or recency
curl -L "$OMNI_BASE_URL/api/v1/content?sortField=favorites" \
  -H "Authorization: Bearer $OMNI_API_KEY"

curl -L "$OMNI_BASE_URL/api/v1/content?sortField=updatedAt" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

### Pagination

Responses include `pageInfo` with cursor-based pagination. Fetch next page:

```bash
curl -L "$OMNI_BASE_URL/api/v1/content?cursor={nextCursor}" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

## Working with Documents

### List Documents

```bash
curl -L "$OMNI_BASE_URL/api/v1/documents" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Filter by creator
curl -L "$OMNI_BASE_URL/api/v1/documents?creatorId={userId}" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

Each document includes: `identifier`, `name`, `type`, `scope`, `owner`, `folder`, `labels`, `updatedAt`, `hasDashboard`.

> **Important**: Always use the `identifier` field for API calls, not `id`. The `id` field is null for workbook-type documents and will cause silent failures.

### Get Document Queries

Retrieve query definitions powering a dashboard's tiles:

```bash
curl -L "$OMNI_BASE_URL/api/v1/documents/{identifier}/queries" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

Useful for understanding what a dashboard computes and re-running queries via `omni-query`.

## Folders

```bash
# List
curl -L "$OMNI_BASE_URL/api/v1/folders" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Create
curl -L -X POST "$OMNI_BASE_URL/api/v1/folders" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Q1 Reports", "scope": "organization" }'
```

## Labels

```bash
# List labels
curl -L "$OMNI_BASE_URL/api/v1/labels" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Add label to document
curl -L -X PUT "$OMNI_BASE_URL/api/v1/documents/{identifier}/labels/{labelName}" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Remove label
curl -L -X DELETE "$OMNI_BASE_URL/api/v1/documents/{identifier}/labels/{labelName}" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

## Favorites

```bash
# Favorite
curl -L -X PUT "$OMNI_BASE_URL/api/v1/documents/{identifier}/favorite" \
  -H "Authorization: Bearer $OMNI_API_KEY"

# Unfavorite
curl -L -X DELETE "$OMNI_BASE_URL/api/v1/documents/{identifier}/favorite" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

## Dashboard Downloads

```bash
# Start download (async)
curl -L -X POST "$OMNI_BASE_URL/api/v1/dashboards/{dashboardId}/download" \
  -H "Authorization: Bearer $OMNI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "format": "pdf" }'

# Poll job status
curl -L "$OMNI_BASE_URL/api/v1/jobs/{jobId}/status" \
  -H "Authorization: Bearer $OMNI_API_KEY"
```

Formats: `pdf`, `png`

## URL Patterns

Construct direct links to content:

```
Dashboard: {OMNI_BASE_URL}/dashboards/{identifier}
Workbook:  {OMNI_BASE_URL}/w/{identifier}
```

The `identifier` comes from the document's `identifier` field in API responses. Always provide the user a clickable link after finding content.

## Search Patterns

When scanning all documents for field references (e.g., for impact analysis), paginate with cursor and call `GET /api/v1/documents/{identifier}/queries` for each document. Launch multiple query-fetch calls in parallel for efficiency. For field impact analysis, prefer the content-validator approach in `omni-model-explorer`.

## Docs Reference

- [Content API](https://docs.omni.co/api/content.md) · [Documents API](https://docs.omni.co/api/documents.md) · [Folders API](https://docs.omni.co/api/folders.md) · [Labels API](https://docs.omni.co/api/labels.md) · [Dashboard Downloads](https://docs.omni.co/api/dashboard-downloads.md)

## Related Skills

- **omni-query** — run queries behind dashboards you've found
- **omni-content-builder** — create or update dashboards
- **omni-embed** — embed dashboards you've found in external apps
- **omni-admin** — manage permissions on documents and folders
