---
name: apideck-connector-coverage
description: Check Apideck connector API coverage before building integrations. Use when determining which operations a connector supports, comparing connector capabilities, or diagnosing why an API call fails with a specific connector. Teaches agents to query the Connector API for real-time coverage data.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck Connector Coverage Skill

## Overview

Not all Apideck connectors support all operations. Before building an integration, always check connector coverage to avoid runtime errors. The Connector API provides real-time metadata about which operations each connector supports.

## IMPORTANT RULES

- ALWAYS check connector coverage before recommending an integration approach. Never assume a connector supports an operation.
- If an operation is not supported, suggest alternatives: a different connector, pass-through to the raw API, or a workaround using supported operations.
- USE the Connector API to verify coverage programmatically. Do not rely on hardcoded lists.
- When a user reports a `501 Not Implemented` or `UnsupportedOperationError`, check coverage first.

## Checking Coverage

### Using the SDK (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env["APIDECK_API_KEY"] ?? "",
  appId: "your-app-id",
  consumerId: "your-consumer-id",
});

// List all connectors for an API
const { data } = await apideck.connector.connectorResources.get({
  id: "crm",
  resourceId: "contacts",
});
// Returns coverage per connector: which operations are supported

// Get specific connector details
const { data: connector } = await apideck.connector.connectors.get({
  id: "salesforce",
});
// Returns: name, status, auth_type, supported_resources, supported_events
```

### Using the REST API

```bash
# List connectors for a unified API
curl 'https://unify.apideck.com/connector/connectors?filter[unified_api]=crm' \
  -H 'Authorization: Bearer {API_KEY}' \
  -H 'x-apideck-app-id: {APP_ID}'

# Get connector details including supported resources
curl 'https://unify.apideck.com/connector/connectors/salesforce' \
  -H 'Authorization: Bearer {API_KEY}' \
  -H 'x-apideck-app-id: {APP_ID}'

# Get API resource coverage (which connectors support what)
curl 'https://unify.apideck.com/connector/apis/crm/resources/contacts' \
  -H 'Authorization: Bearer {API_KEY}' \
  -H 'x-apideck-app-id: {APP_ID}'
```

### Using the Vault API

Check which connections a consumer has and their state:

```typescript
const { data } = await apideck.vault.connections.list({
  api: "crm",
});

for (const conn of data) {
  console.log(`${conn.serviceId}: ${conn.state} (enabled: ${conn.enabled})`);
  // state: available | callable | added | authorized | invalid
}
```

## Coverage States

Each operation on a connector has a coverage status:

| Status | Meaning |
|--------|---------|
| `supported` | Fully implemented and tested |
| `beta` | Implemented but may have edge cases |
| `not_supported` | Not available for this connector |

## Common Coverage Patterns

### Accounting API

| Operation | QuickBooks | Xero | NetSuite | Sage Intacct | FreshBooks |
|-----------|-----------|------|----------|--------------|------------|
| Invoices CRUD | Full | Full | Full | Full | Full |
| Bills CRUD | Full | Full | Full | Full | Partial |
| Payments | Full | Full | Full | Full | Full |
| Journal Entries | Full | Full | Full | Full | Limited |
| Balance Sheet | Full | Full | Full | Full | No |
| Tax Rates (read) | Full | Full | Full | Full | Full |

### CRM API

| Operation | Salesforce | HubSpot | Pipedrive | Zoho CRM | Close |
|-----------|-----------|---------|-----------|----------|-------|
| Contacts CRUD | Full | Full | Full | Full | Full |
| Companies CRUD | Full | Full | Full | Full | Full |
| Leads CRUD | Full | Full | Full | Full | Full |
| Opportunities | Full | Full | Full | Full | Full |
| Activities | Full | Full | Full | Full | Partial |
| Pipelines (read) | Full | Full | Full | Full | Full |

### HRIS API

| Operation | BambooHR | Workday | Personio | Gusto | Rippling |
|-----------|---------|---------|----------|-------|----------|
| Employees CRUD | Full | Full | Full | Full | Full |
| Departments | Full | Full | Full | Full | Full |
| Payrolls (read) | Full | Partial | Partial | Full | Full |
| Time-Off | Full | Full | Full | Full | Full |

> These tables are approximate. Always verify with the Connector API for real-time accuracy.

## Handling Unsupported Operations

When an operation isn't supported for a connector:

### 1. Use Pass-Through (Proxy API)

Make direct calls to the downstream API through Apideck's proxy:

```typescript
// Direct pass-through to the downstream API
const response = await fetch("https://unify.apideck.com/proxy", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "x-apideck-app-id": appId,
    "x-apideck-consumer-id": consumerId,
    "x-apideck-service-id": "salesforce",
    "x-apideck-downstream-url": "https://api.salesforce.com/services/data/v59.0/sobjects/CustomObject__c",
    "x-apideck-downstream-method": "GET",
    "Content-Type": "application/json",
  },
});
```

### 2. Check for Alternative Resources

Some connectors map the same data to different unified resources. For example, a "deal" in Pipedrive maps to "opportunities" in the unified CRM API.

### 3. Suggest a Different Connector

If the user's chosen connector doesn't support an operation, suggest alternatives that do. Use the Connector API to find connectors that support the specific operation.

### 4. Feature Request

If a critical operation is missing, users can request it at https://github.com/apideck-libraries or through the Apideck dashboard.

## Connector Authentication Types

| Auth Type | Description | Connectors |
|-----------|-------------|------------|
| `oauth2` | OAuth 2.0 flow (managed by Vault) | Most cloud SaaS (Salesforce, HubSpot, QuickBooks Online, etc.) |
| `apiKey` | API key authentication | Some self-hosted or simpler services |
| `basic` | Username/password | Legacy systems, on-premise |
| `custom` | Connector-specific auth | Varies |

Vault handles all OAuth flows. Users authorize via the Vault modal — you never need to implement OAuth yourself.

## Debugging Coverage Issues

When an API call fails:

1. **Check the error type** — `UnsupportedOperationError` or `501` means the operation isn't implemented
2. **Verify connection state** — Use `vault.connections.list()` to check the connection is `authorized`
3. **Check connector coverage** — Use the Connector API to verify the operation is supported
4. **Check field support** — Some connectors support an operation but not all fields. Missing fields return `null`
5. **Use raw mode** — Add `raw=true` to see the downstream response for debugging
