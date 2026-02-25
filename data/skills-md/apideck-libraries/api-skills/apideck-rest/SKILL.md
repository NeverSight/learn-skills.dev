---
name: apideck-rest
description: Apideck Unified REST API reference for any language. Use when building integrations with accounting software (QuickBooks, Xero, NetSuite), CRMs (Salesforce, HubSpot, Pipedrive), HRIS platforms (Workday, BambooHR), file storage (Google Drive, Dropbox, Box), ATS systems (Greenhouse, Lever), e-commerce, or any of Apideck's 200+ connectors using direct HTTP calls. Covers authentication headers, CRUD operations, cursor-based pagination, filtering, sorting, error handling, rate limiting, pass-through parameters, and webhooks. Language-agnostic — works with curl, fetch, axios, httpx, or any HTTP client.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck REST API Skill

## Overview

The [Apideck Unified API](https://apideck.com) provides a single REST endpoint to connect with 200+ third-party services across accounting, CRM, HRIS, file storage, ATS, e-commerce, and more. This skill covers direct HTTP usage for any language.

**Base URL:** `https://unify.apideck.com`

## IMPORTANT RULES

- ALWAYS include the three required headers: `Authorization`, `x-apideck-app-id`, and `x-apideck-consumer-id`.
- ALWAYS make API calls server-side to prevent token leakage.
- USE `x-apideck-service-id` to specify which downstream connector to use. Required when a consumer has multiple connections for the same API.
- USE cursor-based pagination — iterate until `meta.cursors.next` is `null`.
- USE the `filter` query parameters to narrow results server-side. DO NOT fetch all records and filter client-side.
- USE the `fields` query parameter to request only the columns you need.
- DO NOT store API keys in source code. Use environment variables.

## Authentication

Every request requires these headers:

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | `Bearer {API_KEY}` |
| `x-apideck-app-id` | Yes | Your Apideck application ID |
| `x-apideck-consumer-id` | Yes | End-user/customer ID stored in Vault |
| `x-apideck-service-id` | No | Downstream connector ID (e.g., `salesforce`, `quickbooks`) |
| `Content-Type` | Yes (POST/PATCH) | `application/json` |

## CRUD Operations

All resources follow a consistent URL pattern:

```
GET    /{api}/{resource}          → List
POST   /{api}/{resource}          → Create
GET    /{api}/{resource}/{id}     → Get
PATCH  /{api}/{resource}/{id}     → Update
DELETE /{api}/{resource}/{id}     → Delete
```

### List

```bash
curl -X GET 'https://unify.apideck.com/crm/contacts?limit=20&filter[email]=john@example.com&sort[by]=updated_at&sort[direction]=desc&fields=id,name,email' \
  -H 'Authorization: Bearer {API_KEY}' \
  -H 'x-apideck-app-id: {APP_ID}' \
  -H 'x-apideck-consumer-id: {CONSUMER_ID}' \
  -H 'x-apideck-service-id: salesforce'
```

Response:
```json
{
  "status_code": 200,
  "status": "OK",
  "service": "salesforce",
  "resource": "contacts",
  "operation": "all",
  "data": [
    { "id": "contact_123", "name": "John Doe", "email": "john@example.com" }
  ],
  "meta": {
    "items_on_page": 20,
    "cursors": {
      "previous": null,
      "current": "em9oby1jcm06Om9mZnNldDo6MA==",
      "next": "em9oby1jcm06Om9mZnNldDo6MjA="
    }
  },
  "links": {
    "previous": null,
    "current": "https://unify.apideck.com/crm/contacts?cursor=...",
    "next": "https://unify.apideck.com/crm/contacts?cursor=..."
  }
}
```

### Create

```bash
curl -X POST 'https://unify.apideck.com/crm/contacts' \
  -H 'Authorization: Bearer {API_KEY}' \
  -H 'Content-Type: application/json' \
  -H 'x-apideck-app-id: {APP_ID}' \
  -H 'x-apideck-consumer-id: {CONSUMER_ID}' \
  -H 'x-apideck-service-id: salesforce' \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "title": "VP of Engineering",
    "emails": [{"email": "john@example.com", "type": "primary"}],
    "phone_numbers": [{"number": "+1234567890", "type": "mobile"}],
    "addresses": [{
      "type": "primary",
      "street_1": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "postal_code": "94105",
      "country": "US"
    }]
  }'
```

Response: `201 Created` with `{ "data": { "id": "contact_123" } }`

### Get

```bash
curl -X GET 'https://unify.apideck.com/crm/contacts/contact_123' \
  -H 'Authorization: Bearer {API_KEY}' \
  -H 'x-apideck-app-id: {APP_ID}' \
  -H 'x-apideck-consumer-id: {CONSUMER_ID}' \
  -H 'x-apideck-service-id: salesforce'
```

### Update

```bash
curl -X PATCH 'https://unify.apideck.com/crm/contacts/contact_123' \
  -H 'Authorization: Bearer {API_KEY}' \
  -H 'Content-Type: application/json' \
  -H 'x-apideck-app-id: {APP_ID}' \
  -H 'x-apideck-consumer-id: {CONSUMER_ID}' \
  -H 'x-apideck-service-id: salesforce' \
  -d '{"title": "CTO"}'
```

### Delete

```bash
curl -X DELETE 'https://unify.apideck.com/crm/contacts/contact_123' \
  -H 'Authorization: Bearer {API_KEY}' \
  -H 'x-apideck-app-id: {APP_ID}' \
  -H 'x-apideck-consumer-id: {CONSUMER_ID}' \
  -H 'x-apideck-service-id: salesforce'
```

## Pagination

Apideck uses cursor-based pagination. Pass the `next` cursor from the response to fetch subsequent pages:

| Parameter | Type | Default | Range |
|-----------|------|---------|-------|
| `limit` | integer | 20 | 1-200 |
| `cursor` | string | — | Opaque cursor from `meta.cursors.next` |

```bash
# First page
curl 'https://unify.apideck.com/crm/contacts?limit=50' -H '...'

# Next page
curl 'https://unify.apideck.com/crm/contacts?limit=50&cursor=em9oby1jcm06Om9mZnNldDo6NTA=' -H '...'
```

When `meta.cursors.next` is `null`, you have reached the last page.

## Filtering and Sorting

### Filters

```
?filter[field_name]=value
```

Available filters vary by resource. Common examples:

| Resource | Filters |
|----------|---------|
| CRM Contacts | `filter[name]`, `filter[email]`, `filter[phone_number]`, `filter[company_id]`, `filter[owner_id]`, `filter[first_name]`, `filter[last_name]` |
| CRM Opportunities | `filter[status]`, `filter[title]`, `filter[company_id]`, `filter[owner_id]` |
| Accounting Invoices | `filter[updated_since]` (ISO 8601 datetime) |
| General | `filter[updated_since]` for incremental sync |

### Sorting

```
?sort[by]=updated_at&sort[direction]=desc
```

### Field Selection

```
?fields=id,name,email,phone_numbers
```

## Pass-Through Parameters

For connector-specific query parameters not in the unified model:

```
?pass_through[search]=overdue
```

For connector-specific fields in request bodies:

```json
{
  "first_name": "John",
  "pass_through": [
    {
      "service_id": "salesforce",
      "operation_id": "contactsAdd",
      "extend_object": {
        "custom_sf_field__c": "value"
      }
    }
  ]
}
```

## Error Handling

All errors follow this format:

```json
{
  "status_code": 400,
  "error": "Bad Request",
  "type_name": "RequestValidationError",
  "message": "Human-readable error description",
  "detail": "Parameter-specific info",
  "ref": "https://developers.apideck.com/errors#requestvalidationerror"
}
```

| Code | Meaning |
|------|---------|
| 400 | Bad Request — invalid parameters |
| 401 | Unauthorized — invalid API key |
| 402 | Payment Required — API limit reached |
| 404 | Not Found — resource does not exist |
| 422 | Unprocessable Entity — validation error |
| 429 | Too Many Requests — rate limit exceeded |
| 5xx | Server Error — Apideck or downstream failure |

## Rate Limiting

Apideck normalizes downstream rate limit headers:

| Header | Description |
|--------|-------------|
| `x-downstream-ratelimit-limit` | Total request capacity |
| `x-downstream-ratelimit-remaining` | Remaining requests |
| `x-downstream-ratelimit-reset` | Unix timestamp when limits reset |

## Raw Mode

Append `?raw=true` to include the unmodified downstream response in a `_raw` property alongside normalized data.

## Available API Endpoints

| API | URL Prefix | Resources |
|-----|-----------|-----------|
| CRM | `/crm/` | contacts, companies, leads, opportunities, activities, notes, pipelines, users |
| Accounting | `/accounting/` | invoices, bills, payments, customers, suppliers, ledger-accounts, journal-entries, tax-rates, credit-notes, purchase-orders, balance-sheet, profit-and-loss |
| HRIS | `/hris/` | employees, companies, departments, payrolls, time-off-requests |
| File Storage | `/file-storage/` | files, folders, drives, drive-groups, shared-links, upload-sessions |
| ATS | `/ats/` | applicants, applications, jobs |
| Vault | `/vault/` | connections, sessions, consumers, custom-mappings, logs |
| Webhook | `/webhook/` | webhooks, event-logs |

## Webhook Events

Events follow the pattern `{api}.{resource}.{action}`:

```
crm.contact.created / .updated / .deleted
accounting.invoice.created / .updated / .deleted
hris.employee.created / .updated / .deleted / .terminated
file-storage.file.created / .updated / .deleted
ats.applicant.created / .updated / .deleted
```

Payload:
```json
{
  "payload": {
    "event_type": "crm.contact.updated",
    "unified_api": "crm",
    "service_id": "salesforce",
    "consumer_id": "user_abc123",
    "entity_id": "contact_123",
    "entity_type": "contact",
    "occurred_at": "2024-06-15T10:30:00.000Z"
  }
}
```

Verify signatures using the `x-apideck-signature` header with HMAC-SHA256.
