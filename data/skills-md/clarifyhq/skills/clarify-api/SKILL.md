---
name: clarify-api
description: Guidelines for working with the Clarify CRM API - includes authentication, endpoints, pagination, filtering, and CRUD operations for records
author: clarify
version: 1.0.0
---

# Clarify API

> **Note:** The Clarify API is under active development and subject to breaking changes. Contact support@clarify.ai with any questions.

## Root URL

```
https://api.clarify.ai/v1/workspaces/{slug}/*
```

The `slug` is the workspace ID assigned to the customer's organization. You can find it in the URL when logging in or by clicking your avatar in the application.

## Authentication

### API Key Authentication

1. Generate a new API key from workspace settings. Generated keys have admin level permissions to your workspace:
   - They have access to records within the workspace and can read, write, and delete data
   - They only have access to redacted email metadata, sensitive fields like bodies are not available
   - They have the same permissions for viewing meeting data as other users

2. Include this API key in the `Authorization` header with the `api-key` scheme:

```bash
curl --header "Authorization: api-key $APIKEY" \
  https://api.clarify.ai/v1/workspaces/$WORKSPACE_SLUG/schemas
```

### Partner OAuth 2.0 Authentication

Clarify uses OAuth and supports Authorization Code, Authorization Code with PKCE, and Refresh Token grants.

**OAuth Endpoints:**
- Authorization: `https://auth1.clarify.ai/oauth2/authorize`
- Token: `https://auth1.clarify.ai/oauth2/token`
- Refresh Token: `https://auth1.clarify.ai/oauth2/token`
- Scopes: `openid profile email offline_access`

**OAuth Flow:**

1. Get authorization code:
```http
GET https://auth1.clarify.ai/oauth2/authorize?response_type=code&client_id={your_client_id}&scope=openid%20profile%20email%20offline_access&redirect_uri={your_redirect_url}
```

2. Exchange for tokens:
```http
POST https://auth1.clarify.ai/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
code={your-code}
redirect_uri={your_redirect_uri}
client_id={your_client_id}
client_secret={your_client_secret}
```

3. Use access token in API calls:
```
Authorization: Bearer {access-token}
```

## API Structure

The API follows the [JSON:API spec](https://jsonapi.org/).

### Pagination

Maximum response size is 1000 items.

**Request:**
- `page[limit]={number}` — maximum number of items to return

**Response fields:**
- `data` — array of returned items
- `meta` — pagination metadata: `total_records`, `total_pages`, `offset`, `limit`
- `links` — URL references: `prev` (if available), `next` (if available)

### Ordering

Control record order with the `sortOrder` query parameter:
- `sortOrder[column]` — field name to order by
- `sortOrder[dir]` — direction: `ASC` or `DESC`

### Filtering

Filter records with `filter` query parameters. Conditions are always AND (OR not supported).

**Basic syntax:**
```
filter[{field_name}]={field_value}
```

**Advanced syntax with operators:**
```
filter[{field_name}][{operator}]={field_value}
```

**Supported operators by field type:**

| Field Type | Operators |
|------------|-----------|
| Text, Multiline Text | `Is`, `Is not`, `Contains`, `Does not contain`, `Starts with`, `Ends with` |
| Number, Currency | `Is`, `Greater than`, `Less than`, `Greater than or equal`, `Less than or equal` |
| Dates | `Is`, `Is after`, `Is before`, `Is on or after`, `Is on or before` |
| Single select | `Is`, `Is not`, `One of`, `Not one of` |
| Multi select | `Contains`, `Does not contain` |
| Checkbox | `Is`, `Is not` |
| Location | `Contains`, `Does not contain` |
| Record IDs | `Is`, `Is not` |
| Collections (Email, Domains) | `Contains`, `Does not contain` |

## Endpoints

### Get Objects & Schemas

```http
GET /schemas
```

Returns an array of schema JSONs:
- `core/*` — internal schemas referenced in other schemas
- `entities/*` — objects available: company, deal, meeting, meeting_recording, person, task, user

Each entity has its JSON Schema definition in the `attributes` field.

### Get Records

```http
GET /objects/{object}/resources
```

**Parameters:**
- `sortOrder` — field to order by with optional direction
- `filters` — one or more criteria to filter records
- `include` — comma-separated list of relationship fields to include

### Create Record

```http
POST /objects/{object}/records
```

**Request body:**
```json
{
  "data": {
    "type": "{object}",
    "attributes": {
      "{field-name}": "{field-value}"
    }
  }
}
```

**Unique fields for upsert behavior:**

| Object | Unique Field |
|--------|--------------|
| Person | `email_addresses` (any one) |
| Company | `domains` (any one) |
| Deal | `name` |
| Meeting | N/A |
| Meeting Recording | N/A |
| User | N/A |

### Get Record

```http
GET /objects/{object}/records/{id}
```

**Parameters:**
- `include` — comma-separated list of relationship fields to include

### Update Record

```http
PATCH /objects/{object}/records/{id}
```

**Request body:**
```json
{
  "data": {
    "id": "{id}",
    "type": "{object}",
    "attributes": {
      "{field-name}": "{field-value}"
    }
  }
}
```

### Bulk Upsert Records

```http
POST /objects/{object}/records/bulk
```

**Request body:**
```json
{
  "data": [{
    "type": "{entity}",
    "attributes": {
      "{field-name}": "{field-value}"
    }
  }]
}
```

### Bulk Delete Records

There is no way to bulk delete records today.

### Set Relationship

```http
PATCH /objects/{object}/records/{id}/relationships/{field-name}
```

**Request body:**
```json
{
  "data": [
    {
      "id": "{id-of-record-to-associate}",
      "type": "{object}"
    }
  ]
}
```

### Unset Relationship

```http
DELETE /objects/{object}/records/{id}/relationships/{field-name}
```

**Request body:**
```json
{
  "data": [
    {
      "id": "{id-of-record-to-disassociate}",
      "type": "{object}"
    }
  ]
}
```

### Get Recording Artifacts

```http
POST /meetings/{id}/recordings/{id}/artifacts
```

**Response:**
```json
{
  "data": {
    "videoUrl": "{signed-video-url}",
    "transcriptionUrl": "{signed-transcription-url}"
  }
}
```

## Swagger Documentation

Full API documentation: https://api.clarify.ai/swagger
