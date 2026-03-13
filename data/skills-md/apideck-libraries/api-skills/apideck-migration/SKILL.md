---
name: apideck-migration
description: Guide for migrating from direct third-party API integrations to Apideck's unified API. Use when a user wants to replace their existing Salesforce, HubSpot, QuickBooks, Xero, or other direct API integrations with Apideck, or when consolidating multiple integrations into a single unified layer.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck Migration Guide Skill

## Overview

This skill helps migrate existing direct third-party API integrations (Salesforce, HubSpot, QuickBooks, Xero, etc.) to Apideck's unified API layer. The benefit is replacing N separate integrations with a single Apideck integration that supports 200+ connectors.

## IMPORTANT RULES

- ALWAYS check connector coverage before migrating. Not all operations may be supported through the unified API.
- ALWAYS preserve existing data flows and business logic. Migration should be transparent to end-users.
- USE `pass_through` for connector-specific fields that don't map to the unified model.
- USE custom field mapping in Vault for recurring connector-specific fields.
- NEVER delete the existing integration code until the Apideck migration is verified in production.
- RECOMMEND a phased migration: start with read operations, then writes, then webhooks.

## Migration Strategy

### Phase 1: Assessment

1. **Inventory existing integrations** — List all third-party APIs currently in use
2. **Map operations** — For each integration, list the CRUD operations and fields used
3. **Check coverage** — Verify each operation is supported via the Apideck Connector API
4. **Identify gaps** — Note operations that need `pass_through` or Proxy API
5. **Plan consumer mapping** — Decide how your users/tenants map to Apideck consumer IDs

### Phase 2: Connection Setup

1. **Create Apideck account** — Get API key and App ID from the dashboard
2. **Enable connectors** — Enable the connectors you need in the Apideck dashboard
3. **Integrate Vault** — Add Vault JS to your frontend for user-managed connections
4. **Create consumers** — Map your existing users to Apideck consumer IDs
5. **Authorize connections** — Have users re-authorize via Vault (OAuth is handled automatically)

### Phase 3: Read Migration (Low Risk)

Replace read operations first since they're non-destructive:

```typescript
// BEFORE: Direct Salesforce API
const contacts = await salesforce.sobjects.Contact.find({
  Email: "john@example.com",
});

// AFTER: Apideck Unified API
const { data } = await apideck.crm.contacts.list({
  serviceId: "salesforce",
  filter: { email: "john@example.com" },
});
```

### Phase 4: Write Migration

Replace create/update/delete operations:

```typescript
// BEFORE: Direct HubSpot API
const contact = await hubspot.crm.contacts.basicApi.create({
  properties: {
    firstname: "John",
    lastname: "Doe",
    email: "john@example.com",
    company: "Acme Corp",
  },
});

// AFTER: Apideck Unified API
const { data } = await apideck.crm.contacts.create({
  serviceId: "hubspot",
  contact: {
    first_name: "John",
    last_name: "Doe",
    emails: [{ email: "john@example.com", type: "primary" }],
    company_name: "Acme Corp",
  },
});
```

### Phase 5: Webhook Migration

Replace direct webhook handlers with Apideck's unified webhooks:

```typescript
// BEFORE: Salesforce-specific webhook handler
app.post("/webhooks/salesforce", (req, res) => {
  const event = req.body;
  if (event.type === "ContactChangeEvent") {
    handleContactChange(event);
  }
});

// AFTER: Apideck unified webhook handler
app.post("/webhooks/apideck", (req, res) => {
  const signature = req.headers["x-apideck-signature"];
  if (!verifySignature(req.body, signature, secret)) {
    return res.status(401).send("Invalid signature");
  }

  const { event_type, entity_id, service_id } = req.body.payload;
  // Works for ALL connectors, not just Salesforce
  if (event_type === "crm.contact.updated") {
    handleContactChange(entity_id, service_id);
  }
  res.status(200).send("OK");
});
```

## Common Migration Patterns

### CRM: Salesforce to Apideck

| Salesforce API | Apideck Unified API |
|---------------|---------------------|
| `sobjects.Contact.create()` | `crm.contacts.create({ serviceId: "salesforce" })` |
| `sobjects.Account.find()` | `crm.companies.list({ serviceId: "salesforce" })` |
| `sobjects.Opportunity.update()` | `crm.opportunities.update({ serviceId: "salesforce" })` |
| `sobjects.Lead.create()` | `crm.leads.create({ serviceId: "salesforce" })` |
| `sobjects.Task.create()` | `crm.activities.create({ serviceId: "salesforce" })` |
| Custom fields via `custom_sf_field__c` | `pass_through: [{ service_id: "salesforce", extend_object: { custom_sf_field__c: "value" } }]` |

### CRM: HubSpot to Apideck

| HubSpot API | Apideck Unified API |
|-------------|---------------------|
| `crm.contacts.basicApi.create()` | `crm.contacts.create({ serviceId: "hubspot" })` |
| `crm.companies.basicApi.getAll()` | `crm.companies.list({ serviceId: "hubspot" })` |
| `crm.deals.basicApi.create()` | `crm.opportunities.create({ serviceId: "hubspot" })` |
| `crm.contacts.searchApi.doSearch()` | `crm.contacts.list({ serviceId: "hubspot", filter: { ... } })` |

### Accounting: QuickBooks to Apideck

| QuickBooks API | Apideck Unified API |
|---------------|---------------------|
| `Invoice.create()` | `accounting.invoices.create({ serviceId: "quickbooks" })` |
| `Customer.findAll()` | `accounting.customers.list({ serviceId: "quickbooks" })` |
| `Bill.create()` | `accounting.bills.create({ serviceId: "quickbooks" })` |
| `Payment.create()` | `accounting.payments.create({ serviceId: "quickbooks" })` |
| `JournalEntry.create()` | `accounting.journalEntries.create({ serviceId: "quickbooks" })` |
| `CompanyInfo.get()` | `accounting.companyInfo.get({ serviceId: "quickbooks" })` |

### Accounting: Xero to Apideck

| Xero API | Apideck Unified API |
|----------|---------------------|
| `xero.accountingApi.createInvoices()` | `accounting.invoices.create({ serviceId: "xero" })` |
| `xero.accountingApi.getContacts()` | `accounting.customers.list({ serviceId: "xero" })` |
| `xero.accountingApi.createBankTransactions()` | `accounting.payments.create({ serviceId: "xero" })` |
| `xero.accountingApi.getReportBalanceSheet()` | `accounting.balanceSheet.get({ serviceId: "xero" })` |

### HRIS: BambooHR to Apideck

| BambooHR API | Apideck Unified API |
|-------------|---------------------|
| `GET /employees/directory` | `hris.employees.list({ serviceId: "bamboohr" })` |
| `POST /employees` | `hris.employees.create({ serviceId: "bamboohr" })` |
| `GET /employees/{id}` | `hris.employees.get({ serviceId: "bamboohr", id })` |
| `PUT /employees/{id}/time_off/request` | `hris.timeOffRequests.create({ serviceId: "bamboohr" })` |

### File Storage: Google Drive to Apideck

| Google Drive API | Apideck Unified API |
|-----------------|---------------------|
| `drive.files.list()` | `fileStorage.files.list({ serviceId: "google-drive" })` |
| `drive.files.create()` | `fileStorage.files.create({ serviceId: "google-drive" })` |
| `drive.files.get()` | `fileStorage.files.get({ serviceId: "google-drive" })` |
| `drive.files.export()` | `fileStorage.files.download({ serviceId: "google-drive" })` |
| `drive.permissions.create()` | `fileStorage.sharedLinks.create({ serviceId: "google-drive" })` |

## Handling Connector-Specific Fields

### Option 1: Pass-Through (inline)

For one-off connector-specific fields in request bodies:

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
        extend_object: {
          RecordTypeId: "012000000000001",
          Custom_Score__c: 85,
        },
      },
    ],
  },
});
```

### Option 2: Custom Field Mapping (reusable)

For fields that are used repeatedly, configure custom mapping in Vault so they appear as part of the unified model:

```typescript
// Set up custom mapping via Vault API
await apideck.vault.customMappings.update({
  unifiedApi: "crm",
  serviceId: "salesforce",
  id: "mapping_123",
  customMapping: {
    value: "$.Custom_Score__c",
  },
});

// Now the field appears in custom_fields on every response
const { data } = await apideck.crm.contacts.get({
  id: "contact_123",
  serviceId: "salesforce",
});
// data.custom_fields includes { id: "mapping_123", value: 85 }
```

### Option 3: Proxy API (full control)

For operations not supported by the unified API, use the Proxy to make direct downstream calls while still using Apideck's managed authentication:

```typescript
const response = await fetch("https://unify.apideck.com/proxy", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "x-apideck-app-id": appId,
    "x-apideck-consumer-id": consumerId,
    "x-apideck-service-id": "salesforce",
    "x-apideck-downstream-url": "/services/data/v59.0/sobjects/CustomObject__c",
    "x-apideck-downstream-method": "GET",
    "Content-Type": "application/json",
  },
});
```

## Testing the Migration

1. **Run both integrations in parallel** — Shadow mode: make Apideck calls alongside existing calls and compare responses
2. **Use raw mode** — Add `raw=true` to Apideck calls to compare with the original API response
3. **Contract test with Portman** — Generate tests from OpenAPI specs and run against your staging environment
4. **Test with the API Explorer** — Use the [Apideck API Explorer](https://developers.apideck.com/api-explorer) to verify endpoints interactively
5. **Gradual rollout** — Migrate one connector at a time, starting with the lowest-traffic integration

## Post-Migration Benefits

Once migrated to Apideck:

- **Add new connectors instantly** — Enable a new connector in the dashboard, no code changes needed
- **User self-service** — End-users manage their own connections via Vault
- **Unified webhooks** — One handler for all connectors instead of N separate handlers
- **Unified error handling** — One error format instead of learning each API's error structure
- **Automatic maintenance** — Apideck handles API version changes, deprecations, and auth token refresh
