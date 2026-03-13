---
name: scout
description: Interact with Scout data platform API. Use when working with Scout collections, tables, documents, agents, drive storage, syncs, or usage. Supports CRUD operations on collections/tables/documents, agent management, file uploads/downloads, data sync configuration from various sources (web, Notion, Google Drive, etc.), and usage monitoring.
---

# Scout API Skill

Interact with Scout data platform for collections, tables, documents, agents, drive storage, syncs, and usage tracking.

## Authentication

All Scout API endpoints require Bearer token authentication. You need a Scout API key.

### Getting Your API Key

1. Log in to Scout at https://scoutos.com
2. Navigate to Settings → API Keys
3. Create or copy your API key

### Using the API Key

Include the API key in the `Authorization` header for every request:

```
Authorization: Bearer YOUR_API_KEY
```

### Environment Variable (Recommended)

Store your API key in an environment variable:

```bash
export SCOUT_API_KEY="your-api-key-here"
```

Then reference it in requests:

```bash
curl -H "Authorization: Bearer $SCOUT_API_KEY" https://api.scoutos.com/v2/collections
```

---

## Base URL

```
https://api.scoutos.com
```

---

## Collections

Collections are top-level containers for organizing data in Scout.

### List Collections

```bash
GET /v2/collections
```

**Query Parameters:**
- `start_at` (string) - Pagination cursor (created_at timestamp)
- `limit` (integer) - Max results to return
- `query` (string) - Search query
- `tags` (string) - Filter by tags
- `sort` (string) - Sort order
- `drive` (boolean) - Include drive collections

**Example:**

```bash
curl -H "Authorization: Bearer $SCOUT_API_KEY" \
  "https://api.scoutos.com/v2/collections?limit=10"
```

**Response:**

```json
{
  "data": [
    {
      "collection_id": "col_abc123",
      "collection_config": {
        "collection_display_name": "My Collection",
        "collection_description": "Description here",
        "tags": ["tag1", "tag2"]
      },
      "created_at": "2024-01-15T10:30:00Z",
      "last_updated_at": "2024-01-20T14:22:00Z"
    }
  ],
  "has_more": true,
  "next_cursor": "cursor_string"
}
```

### Create Collection

```bash
POST /v2/collections
```

**Body:**

```json
{
  "collection_display_name": "My New Collection",
  "collection_description": "A description",
  "collection_img_url": "https://example.com/image.png",
  "tags": ["documentation", "project-x"],
  "table_order": []
}
```

**Example:**

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "collection_display_name": "Project Documents",
    "collection_description": "All project documentation",
    "tags": ["docs", "project"]
  }' \
  "https://api.scoutos.com/v2/collections"
```

### Get Collection

```bash
GET /v2/collections/{collection_id}
```

### Update Collection

```bash
PUT /v2/collections/{collection_id}
```

### Delete Collection

```bash
DELETE /v2/collections/{collection_id}
```

---

## Tables

Tables store structured data within a collection. Each table has a schema defining columns.

### List Tables

```bash
GET /v2/collections/{collection_id}/tables
```

**Example:**

```bash
curl -H "Authorization: Bearer $SCOUT_API_KEY" \
  "https://api.scoutos.com/v2/collections/col_abc123/tables"
```

### Create Table

```bash
POST /v2/collections/{collection_id}/tables
```

**Body:**

```json
{
  "table_display_name": "Users",
  "table_description": "User records",
  "schema": [
    {
      "column_id": "name",
      "column_display_name": "Name",
      "column_type": "text-short",
      "data_type": "string"
    },
    {
      "column_id": "email",
      "column_display_name": "Email",
      "column_type": "text-short",
      "data_type": "string"
    },
    {
      "column_id": "age",
      "column_display_name": "Age",
      "column_type": "number",
      "data_type": "number"
    },
    {
      "column_id": "status",
      "column_display_name": "Status",
      "column_type": "select",
      "data_type": "string",
      "options": [
        {"id": "active", "name": "Active", "color_hex": "#00ff00"},
        {"id": "inactive", "name": "Inactive", "color_hex": "#ff0000"}
      ]
    },
    {
      "column_id": "created_at",
      "column_display_name": "Created At",
      "column_type": "datetime",
      "data_type": "datetime"
    }
  ]
}
```

**Column Types:**

| Type | Data Type | Description |
|------|-----------|-------------|
| `text-short` | string | Single-line text |
| `text-long` | string | Multi-line text |
| `number` | number | Numeric values |
| `checkbox` | boolean | True/false |
| `select` | string | Single selection from options |
| `multi-select` | string[] | Multiple selections |
| `datetime` | datetime | Date and time |
| `url` | string | URL field |
| `markdown` | string | Markdown content |
| `json` | string | JSON data |
| `relation` | string | Link to another table |
| `people` | string[] | Organization members |

**Example:**

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "table_display_name": "Tasks",
    "schema": [
      {"column_id": "title", "column_type": "text-short", "data_type": "string"},
      {"column_id": "completed", "column_type": "checkbox", "data_type": "boolean"},
      {"column_id": "priority", "column_type": "select", "data_type": "string", "options": [
        {"id": "high", "name": "High"},
        {"id": "medium", "name": "Medium"},
        {"id": "low", "name": "Low"}
      ]}
    ]
  }' \
  "https://api.scoutos.com/v2/collections/col_abc123/tables"
```

### Get Table

```bash
GET /v2/collections/{collection_id}/tables/{table_id}
```

### Update Table

```bash
PUT /v2/collections/{collection_id}/tables/{table_id}
```

### Delete Table

```bash
DELETE /v2/collections/{collection_id}/tables/{table_id}
```

---

## Documents

Documents are individual records within a table.

### List Documents

```bash
GET /v2/collections/{collection_id}/tables/{table_id}/documents
```

**Query Parameters:**
- `start_at` - Pagination cursor
- `limit` - Max results
- `query` - Search query
- `sort` - Sort field and direction

**Example:**

```bash
curl -H "Authorization: Bearer $SCOUT_API_KEY" \
  "https://api.scoutos.com/v2/collections/col_abc123/tables/tbl_xyz789/documents?limit=20"
```

### Create Document

```bash
POST /v2/collections/{collection_id}/tables/{table_id}/documents
```

**Query Parameters:**
- `await_completion` (boolean) - Wait for indexing (default: true)
- `mode` (string) - "merge" or "replace" (default: merge)
- `merge_fields` (boolean) - Merge only provided fields (default: false)

**Body:** JSON object matching your table schema

**Example:**

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete API documentation",
    "completed": false,
    "priority": "high"
  }' \
  "https://api.scoutos.com/v2/collections/col_abc123/tables/tbl_xyz789/documents"
```

### Create Multiple Documents

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[
    {"title": "Task 1", "completed": false},
    {"title": "Task 2", "completed": true},
    {"title": "Task 3", "completed": false}
  ]' \
  "https://api.scoutos.com/v2/collections/col_abc123/tables/tbl_xyz789/documents"
```

### Get Document

```bash
GET /v2/collections/{collection_id}/tables/{table_id}/documents/{document_id}
```

### Update Document

```bash
PUT /v2/collections/{collection_id}/tables/{table_id}/documents/{document_id}
```

**Example - Partial Update:**

```bash
curl -X PUT \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}' \
  "https://api.scoutos.com/v2/collections/col_abc123/tables/tbl_xyz789/documents/doc_123?merge_fields=true"
```

### Delete Document

```bash
DELETE /v2/collections/{collection_id}/tables/{table_id}/documents/{document_id}
```

---

## Agents

Scout agents are AI assistants that interact with your data.

### List Agents

```bash
GET /agents
```

**Example:**

```bash
curl -H "Authorization: Bearer $SCOUT_API_KEY" \
  "https://api.scoutos.com/agents"
```

**Response:**

```json
[
  {
    "id": "agent_abc123",
    "name": "Support Assistant",
    "description": "Helps with customer support questions",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:22:00Z",
    "visibility": {"type": "organization", "id": "org_xyz"}
  }
]
```

### Get Agent

```bash
GET /agents/{agent_id}
```

### Interact with Agent

```bash
POST /agents/{agent_id}/interact
```

**Body:**

```json
{
  "message": "What are the latest support tickets?",
  "conversation_id": "conv_123"
}
```

### Upsert Agent

```bash
POST /agents/{agent_id}/upsert
```

### Delete Agent

```bash
DELETE /agents/{agent_id}
```

---

## Drive

Upload and download files to Scout Drive storage.

### Upload Files

```bash
POST /drive/upload
Content-Type: multipart/form-data
```

**Parameters:**
- `files` (required) - One or more files to upload
- `metadata` (optional) - JSON string with per-file metadata

**Metadata Options:**
- `path` - Full destination path (takes precedence)
- `folder` - Destination folder
- `name` - Destination filename

**Example - Single File:**

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -F "files=@/path/to/document.pdf" \
  "https://api.scoutos.com/drive/upload"
```

**Example - Multiple Files with Metadata:**

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -F "files=@report.pdf" \
  -F "files=@image.png" \
  -F 'metadata=[{"folder": "reports"}, {"folder": "images", "name": "logo.png"}]' \
  "https://api.scoutos.com/drive/upload"
```

**Response:**

```json
{
  "data": [
    {
      "id": "file_abc123",
      "name": "document.pdf",
      "url": "https://drive.scoutos.com/file_abc123",
      "path": "/reports/document.pdf"
    }
  ]
}
```

### Download File

```bash
GET /drive/download/{file_id}
```

**Example:**

```bash
curl -H "Authorization: Bearer $SCOUT_API_KEY" \
  "https://api.scoutos.com/drive/download/file_abc123" \
  -o downloaded_file.pdf
```

---

## Syncs

Sync data from external sources into Scout tables.

### Sync Sources

| Source | Archetype ID | Description |
|--------|-------------|-------------|
| Sitemap | `com.scoutos.sitemap` | Crawl from sitemap.xml |
| Website | `com.scoutos.website` | Website crawler |
| Crawl | `com.scoutos.crawl` | Multi-page web crawl |
| Page Crawl | `com.scoutos.page_crawl` | Single page scrape |
| Notion | `com.notion.notion` | Notion pages |
| Google Drive | `com.google.drive` | Google Drive files |
| Laserfiche | `com.laserfiche.repository` | Laserfiche documents |
| Microsoft 365 | `com.microsoft.365` | SharePoint/OneDrive |
| Guided Crawl | `com.scoutos.guided_crawl` | AI-guided browser automation |

### Create Sync

```bash
POST /v2/syncs
```

**Body Structure:**

```json
{
  "sync_config": {
    "source_settings": { /* source-specific config */ },
    "destination": {
      "destination_type": "collections.v2",
      "collection_id": "col_abc123",
      "table_id": "tbl_xyz789"
    },
    "mapping": {
      "fields": [
        {"source": "title", "destination": "name"},
        {"source": "content", "destination": "body"}
      ]
    },
    "schedule": {
      "frequency": "daily",
      "enabled": true
    }
  }
}
```

### Website Crawl Example

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sync_config": {
      "source_settings": {
        "source_archetype_id": "com.scoutos.website",
        "start_urls": ["https://docs.example.com"],
        "max_depth": 3,
        "max_page_count": 100,
        "scraper": "playwright",
        "text_extractor": "trafilatura"
      },
      "destination": {
        "destination_type": "collections.v2",
        "collection_id": "col_abc123",
        "table_id": "tbl_xyz789"
      },
      "mapping": {
        "fields": [
          {"source": "title", "destination": "title"},
          {"source": "content", "destination": "content"},
          {"source": "url", "destination": "source_url"}
        ]
      }
    }
  }' \
  "https://api.scoutos.com/v2/syncs"
```

### Notion Sync Example

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sync_config": {
      "source_settings": {
        "source_archetype_id": "com.notion.notion",
        "api_key": "your-notion-integration-token",
        "filter_options": [
          {
            "field": "Page Title",
            "operator": "Contains Any Of",
            "value": ["blog", "docs"]
          }
        ]
      },
      "destination": {
        "destination_type": "collections.v2",
        "collection_id": "col_abc123",
        "table_id": "tbl_xyz789"
      },
      "mapping": {"fields": []}
    }
  }' \
  "https://api.scoutos.com/v2/syncs"
```

### Guided Crawl Example (AI Browser Automation)

For sites requiring login or complex navigation:

```bash
curl -X POST \
  -H "Authorization: Bearer $SCOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sync_config": {
      "source_settings": {
        "source_archetype_id": "com.scoutos.guided_crawl",
        "start_url": "https://portal.example.com/login",
        "instructions": "Login to the portal using credentials, navigate to Documents section, and download all PDF files",
        "requires_login": true,
        "username": "user@example.com",
        "password_secret_name": "portal_password",
        "parse_pdfs": true,
        "max_pdfs": 50
      },
      "destination": {
        "destination_type": "collections.v2",
        "collection_id": "col_abc123",
        "table_id": "tbl_xyz789"
      },
      "mapping": {"fields": []}
    }
  }' \
  "https://api.scoutos.com/v2/syncs"
```

### List Syncs

```bash
GET /v2/syncs
```

### Get Sync

```bash
GET /v2/syncs/{sync_id}
```

### Run Sync

```bash
POST /v2/syncs/{sync_id}/run
```

### Delete Sync

```bash
DELETE /v2/syncs/{sync_id}
```

---

## Usage

Monitor your organization's API usage and costs.

### Get Usage

```bash
GET /v2/usage
```

**Query Parameters:**
- `start_date` (string) - Start date for usage data (ISO format)
- `end_date` (string) - End date for usage data (ISO format)

**Example:**

```bash
curl -H "Authorization: Bearer $SCOUT_API_KEY" \
  "https://api.scoutos.com/v2/usage?start_date=2024-01-01&end_date=2024-01-31"
```

**Response:**

```json
{
  "data": {
    "usage": [
      {
        "execution_date": "2024-01-15",
        "workflow_run_type": "agent",
        "block_archetype_id": "llm_block",
        "total_cost": 0.0025,
        "total_execution_duration_ms": 1500,
        "display_name": "GPT-4 Call"
      }
    ],
    "total_cost": 0.0450
  }
}
```

---

## SDK Usage

For TypeScript/JavaScript projects, use the official SDK:

### Install

```bash
npm install scoutos
# or
pnpm add scoutos
# or
yarn add scoutos
```

### Initialize Client

```typescript
import { ScoutClient } from "scoutos";

const client = new ScoutClient({ 
  apiKey: process.env.SCOUT_API_KEY 
});
```

### Example: Full Workflow

```typescript
// Create a collection
const collection = await client.collections.create({
  collection_display_name: "Knowledge Base",
  collection_description: "Documentation and articles",
  tags: ["docs", "knowledge"]
});

// Create a table
const table = await client.tables.create(collection.data.collection_id, {
  table_display_name: "Articles",
  schema: [
    { column_id: "title", column_type: "text-short", data_type: "string" },
    { column_id: "content", column_type: "text-long", data_type: "string" },
    { column_id: "url", column_type: "url", data_type: "string" },
    { column_id: "published", column_type: "datetime", data_type: "datetime" }
  ]
});

// Add documents
await client.documents.create(
  collection.data.collection_id,
  table.data.table_id,
  {
    body: {
      title: "Getting Started with Scout",
      content: "Scout is a data platform for building AI applications...",
      url: "https://docs.scoutos.com/getting-started",
      published: new Date().toISOString()
    }
  }
);

// Set up a sync from website
await client.syncs.create({
  sync_config: {
    source_settings: {
      source_archetype_id: "com.scoutos.website",
      start_urls: ["https://docs.scoutos.com"]
    },
    destination: {
      destination_type: "collections.v2",
      collection_id: collection.data.collection_id,
      table_id: table.data.table_id
    },
    mapping: { fields: [] }
  }
});

// Check usage
const usage = await client.usage.get({
  start_date: "2024-01-01",
  end_date: "2024-01-31"
});
console.log(`Total cost: $${usage.data.total_cost}`);
```

---

## Error Handling

All endpoints return standard HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing API key |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Request body validation failed |
| 429 | Rate Limited - Too many requests |
| 500 | Internal Server Error |

**Error Response Format:**

```json
{
  "detail": "Validation error",
  "errors": [
    {"field": "collection_display_name", "message": "Field required"}
  ]
}
```

---

## Rate Limits

Scout API has rate limits to ensure fair usage. If you hit a rate limit:

1. Wait for the retry window (check `Retry-After` header)
2. Implement exponential backoff in your code
3. Consider batching requests where possible

---

## Best Practices

1. **Store API keys securely** - Use environment variables, never commit to code
2. **Handle pagination** - Use `has_more` and `next_cursor` for large result sets
3. **Use async operations** - For large uploads/syncs, check job status
4. **Cache frequently accessed data** - Reduce API calls with local caching
5. **Monitor usage** - Regular checks on `/v2/usage` to track costs
6. **Batch document creates** - Send arrays for bulk inserts
7. **Use appropriate column types** - Ensures proper indexing and querying

---

## Additional Resources

- **Official Docs**: https://docs.scoutos.com
- **API Reference**: https://docs.scoutos.com/api-sdk
- **Status Page**: https://status.scoutos.com
- **Support**: support@scoutos.com