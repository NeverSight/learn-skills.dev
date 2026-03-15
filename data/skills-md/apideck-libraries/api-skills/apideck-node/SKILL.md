---
name: apideck-node
description: Apideck Unified API integration patterns for TypeScript and Node.js. Use when building integrations with accounting software (QuickBooks, Xero, NetSuite), CRMs (Salesforce, HubSpot, Pipedrive), HRIS platforms (Workday, BambooHR), file storage (Google Drive, Dropbox, Box), ATS systems (Greenhouse, Lever), e-commerce, or any of Apideck's 200+ connectors. Covers the @apideck/unify SDK, authentication, CRUD operations, pagination, filtering, webhooks, and Vault connection management.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck TypeScript SDK Skill

## Overview

The [Apideck Unified API](https://apideck.com) provides a single integration layer to connect with 200+ third-party services across accounting, CRM, HRIS, file storage, ATS, e-commerce, and more. The official TypeScript SDK (`@apideck/unify`) provides typed clients for all unified APIs.

Key capabilities:
- **Accounting** - Invoices, bills, payments, ledger accounts, journal entries, tax rates, balance sheets, P&L
- **CRM** - Contacts, companies, leads, opportunities, activities, pipelines, notes
- **HRIS** - Employees, departments, payrolls, time-off requests, schedules
- **File Storage** - Files, folders, drives, shared links, upload sessions
- **ATS** - Jobs, applicants, applications
- **Vault** - Connection management, OAuth flows, custom field mapping
- **Vault JS** - Embeddable modal UI for users to authorize connectors and manage settings
- **Webhook** - Event subscriptions and real-time notifications

## Installation

```sh
npm add @apideck/unify
```

Requires Node.js 18+. The SDK is fully typed with TypeScript definitions.

## IMPORTANT RULES

- ALWAYS use the `@apideck/unify` SDK. DO NOT make raw `fetch`/`axios` calls to the Apideck API.
- ALWAYS pass `apiKey`, `appId`, and `consumerId` when initializing the client. These are required for all API calls.
- ALWAYS set the `APIDECK_API_KEY` environment variable rather than hardcoding API keys.
- USE `serviceId` to specify which downstream connector to use (e.g., `"salesforce"`, `"quickbooks"`, `"xero"`). If a consumer has multiple connections for an API, `serviceId` is required.
- USE cursor-based pagination with `for await...of` for iterating large result sets. DO NOT implement manual pagination.
- USE the `filter` parameter to narrow results server-side. DO NOT fetch all records and filter client-side.
- USE the `fields` parameter to request only the columns you need. This reduces response size and improves performance.
- ALWAYS handle errors with try/catch. The SDK throws typed errors for different HTTP status codes.
- DO NOT store Apideck API keys, App IDs, or Consumer IDs in source code. Use environment variables or a secrets manager.

## Quick Start

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env["APIDECK_API_KEY"] ?? "",
  appId: "your-app-id",
  consumerId: "your-consumer-id",
});

// List CRM contacts
const { data } = await apideck.crm.contacts.list({
  limit: 20,
  filter: { email: "john@example.com" },
});

for (const contact of data) {
  console.log(contact.name, contact.emails);
}
```

## SDK Patterns

### Client Setup

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env["APIDECK_API_KEY"] ?? "",
  appId: "your-app-id",
  consumerId: "your-consumer-id",
});
```

The `consumerId` identifies the end-user whose connections are being used. In multi-tenant apps, set this per-request or per-user session.

### CRUD Operations

All resources follow the same pattern: `apideck.{api}.{resource}.{operation}()`.

```typescript
// LIST - retrieve multiple records
const { data } = await apideck.crm.contacts.list({
  serviceId: "salesforce",
  limit: 20,
  filter: { email: "john@example.com" },
  sort: { by: "updated_at", direction: "desc" },
  fields: "id,name,email,phone_numbers",
});

// CREATE - create a new record
const { data: created } = await apideck.crm.contacts.create({
  serviceId: "salesforce",
  contact: {
    first_name: "John",
    last_name: "Doe",
    emails: [{ email: "john@example.com", type: "primary" }],
    phone_numbers: [{ number: "+1234567890", type: "mobile" }],
  },
});
console.log(created.id); // "contact_abc123"

// GET - retrieve a single record
const { data: contact } = await apideck.crm.contacts.get({
  id: "contact_abc123",
  serviceId: "salesforce",
});

// UPDATE - modify an existing record
const { data: updated } = await apideck.crm.contacts.update({
  id: "contact_abc123",
  serviceId: "salesforce",
  contact: { first_name: "Jane" },
});

// DELETE - remove a record
await apideck.crm.contacts.delete({
  id: "contact_abc123",
  serviceId: "salesforce",
});
```

### Pagination

Use async iteration to automatically handle cursor-based pagination:

```typescript
const result = await apideck.accounting.invoices.list({
  serviceId: "quickbooks",
  limit: 50,
});

// Automatically fetches next pages
for await (const page of result) {
  for (const invoice of page.data) {
    console.log(invoice.number, invoice.total);
  }
}
```

Or handle pagination manually:

```typescript
let cursor: string | undefined;
do {
  const { data, meta } = await apideck.accounting.invoices.list({
    serviceId: "quickbooks",
    limit: 50,
    cursor,
  });
  for (const invoice of data) {
    console.log(invoice.number);
  }
  cursor = meta?.cursors?.next ?? undefined;
} while (cursor);
```

### Error Handling

```typescript
import { Apideck } from "@apideck/unify";
import * as errors from "@apideck/unify/models/errors";

try {
  const { data } = await apideck.crm.contacts.get({ id: "invalid" });
} catch (e) {
  if (e instanceof errors.BadRequestResponse) {
    console.error("Bad request:", e.message);
  } else if (e instanceof errors.UnauthorizedResponse) {
    console.error("Invalid API key or missing credentials");
  } else if (e instanceof errors.NotFoundResponse) {
    console.error("Record not found");
  } else if (e instanceof errors.PaymentRequiredResponse) {
    console.error("API limit reached or payment required");
  } else if (e instanceof errors.UnprocessableResponse) {
    console.error("Validation error:", e.message);
  } else {
    throw e;
  }
}
```

### Common Parameters

Most list endpoints accept these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `serviceId` | `string` | Downstream connector ID (e.g., `"quickbooks"`, `"salesforce"`) |
| `limit` | `number` | Max results per page (1-200, default 20) |
| `cursor` | `string` | Pagination cursor from previous response |
| `filter` | `object` | Resource-specific filter criteria |
| `sort` | `object` | `{ by: string, direction: "asc" \| "desc" }` |
| `fields` | `string` | Comma-separated field names to return |
| `passThrough` | `object` | Pass-through query parameters for the downstream API |

### Pass-Through Parameters

When the unified model doesn't cover a connector-specific field, use `passThrough`:

```typescript
const { data } = await apideck.accounting.invoices.list({
  serviceId: "quickbooks",
  passThrough: {
    search: "overdue",
  },
});
```

For creating/updating, use `pass_through` in the request body to send connector-specific fields:

```typescript
const { data } = await apideck.crm.contacts.create({
  serviceId: "salesforce",
  contact: {
    first_name: "John",
    last_name: "Doe",
    pass_through: [
      {
        service_id: "salesforce",
        operation_id: "contactsAdd",
        extend_object: { custom_sf_field__c: "value" },
      },
    ],
  },
});
```

## API Namespaces

The SDK organizes APIs by namespace. See the reference files for detailed endpoints:

| Namespace | Reference | Resources |
|-----------|-----------|-----------|
| `apideck.accounting.*` | [references/accounting-api.md](references/accounting-api.md) | invoices, bills, payments, customers, suppliers, ledgerAccounts, journalEntries, taxRates, creditNotes, purchaseOrders, balanceSheet, profitAndLoss, and more |
| `apideck.crm.*` | [references/crm-api.md](references/crm-api.md) | contacts, companies, leads, opportunities, activities, notes, pipelines, users |
| `apideck.hris.*` | [references/hris-api.md](references/hris-api.md) | employees, companies, departments, payrolls, timeOffRequests |
| `apideck.fileStorage.*` | [references/file-storage-api.md](references/file-storage-api.md) | files, folders, drives, driveGroups, sharedLinks, uploadSessions |
| `apideck.ats.*` | [references/ats-api.md](references/ats-api.md) | applicants, applications, jobs |
| `apideck.vault.*` | [references/vault-api.md](references/vault-api.md) | connections, connectionSettings, consumers, customMappings, logs, sessions |
| `apideck.webhook.*` | [references/webhook-api.md](references/webhook-api.md) | webhooks, eventLogs |

## Vault JS (Embeddable UI)

Use [`@apideck/vault-js`](references/vault-js.md) to embed a pre-built modal that lets your users authorize connectors and manage integration settings. Session creation must happen server-side.

```typescript
// 1. Server-side: create a session
const { data } = await apideck.vault.sessions.create({
  session: {
    consumer_metadata: { account_name: "Acme Corp", user_name: "John Doe", email: "john@acme.com" },
    redirect_uri: "https://myapp.com/integrations",
    settings: { unified_apis: ["accounting", "crm"] },
    theme: { vault_name: "My App", primary_color: "#4F46E5" },
  },
});

// 2. Client-side: open the modal
import { ApideckVault } from "@apideck/vault-js";

ApideckVault.open({
  token: sessionToken,
  onConnectionChange: (connection) => console.log("Changed:", connection),
  onClose: () => console.log("Closed"),
});
```

See [references/vault-js.md](references/vault-js.md) for full configuration options, theming, React integration, and event callbacks.
