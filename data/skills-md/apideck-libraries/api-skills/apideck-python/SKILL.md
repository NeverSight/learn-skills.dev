---
name: apideck-python
description: Apideck Unified API integration patterns for Python. Use when building integrations with accounting software (QuickBooks, Xero, NetSuite), CRMs (Salesforce, HubSpot, Pipedrive), HRIS platforms (Workday, BambooHR), file storage (Google Drive, Dropbox, Box), ATS systems (Greenhouse, Lever), e-commerce, or any of Apideck's 200+ connectors using Python. Covers the apideck-unify SDK, authentication, CRUD operations, pagination, filtering, async support, and Vault connection management.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck Python SDK Skill

## Overview

The [Apideck Unified API](https://apideck.com) provides a single integration layer to connect with 200+ third-party services across accounting, CRM, HRIS, file storage, ATS, e-commerce, and more. The official Python SDK (`apideck-unify`) provides typed clients for all unified APIs.

## Installation

```sh
pip install apideck-unify
```

Requires Python 3.9+. Dependencies: `httpx`, `pydantic`.

## IMPORTANT RULES

- ALWAYS use the `apideck-unify` SDK. DO NOT make raw `httpx`/`requests` calls to the Apideck API.
- ALWAYS pass `api_key`, `app_id`, and `consumer_id` when initializing the client.
- ALWAYS set the `APIDECK_API_KEY` environment variable rather than hardcoding API keys.
- USE `service_id` to specify which downstream connector to use (e.g., `"salesforce"`, `"quickbooks"`). If a consumer has multiple connections for an API, `service_id` is required.
- USE context managers (`with` / `async with`) for client lifecycle management.
- USE the `fields` parameter to request only the columns you need.
- USE the `filter_` parameter (note the trailing underscore) to narrow results server-side.
- ALWAYS handle errors with try/except using `models.ApideckError` as the base class.

## Quick Start

```python
from apideck_unify import Apideck
import os

with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    app_id="your-app-id",
    consumer_id="your-consumer-id",
) as apideck:
    res = apideck.crm.contacts.list(
        service_id="salesforce",
        limit=20,
        filter_={"email": "john@example.com"},
    )
    while res is not None:
        for contact in res.data:
            print(contact.name, contact.emails)
        res = res.next()
```

## SDK Patterns

### Client Setup

```python
from apideck_unify import Apideck
import os

with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    app_id="your-app-id",
    consumer_id="your-consumer-id",
) as apideck:
    # Make API calls here
    pass
```

The `consumer_id` identifies the end-user whose connections are being used. In multi-tenant apps, set this per-request or per-user session.

### CRUD Operations

All resources follow the same pattern: `apideck.{api}.{resource}.{operation}()`.

```python
import apideck_unify
from apideck_unify import Apideck
import os

with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    app_id="your-app-id",
    consumer_id="your-consumer-id",
) as apideck:

    # LIST - retrieve multiple records
    res = apideck.crm.contacts.list(
        service_id="salesforce",
        limit=20,
        filter_={"email": "john@example.com", "company_id": "12345"},
        sort={"by": apideck_unify.ContactsSortBy.CREATED_AT, "direction": apideck_unify.SortDirection.DESC},
        fields="id,name,email",
    )

    # CREATE - create a new record
    res = apideck.crm.contacts.create(
        service_id="salesforce",
        first_name="John",
        last_name="Doe",
        emails=[{"email": "john@example.com", "type": apideck_unify.EmailType.PRIMARY}],
        phone_numbers=[{"number": "+1234567890", "type": apideck_unify.PhoneNumberType.PRIMARY}],
    )
    print(res.create_contact_response)

    # GET - retrieve a single record
    res = apideck.crm.contacts.get(id="contact_123", service_id="salesforce")

    # UPDATE - modify an existing record
    res = apideck.crm.contacts.update(id="contact_123", service_id="salesforce", first_name="Jane")

    # DELETE - remove a record
    res = apideck.crm.contacts.delete(id="contact_123", service_id="salesforce")
```

### Pagination

Use the `.next()` method on response objects for cursor-based pagination:

```python
res = apideck.accounting.invoices.list(service_id="quickbooks", limit=50)

while res is not None:
    for invoice in res.data:
        print(invoice.number, invoice.total)
    res = res.next()
```

### Async Support

Every sync method has an `_async` counterpart. Use `async with` as context manager:

```python
import asyncio
from apideck_unify import Apideck
import os

async def main():
    async with Apideck(
        api_key=os.getenv("APIDECK_API_KEY", ""),
        app_id="your-app-id",
        consumer_id="your-consumer-id",
    ) as apideck:
        res = await apideck.crm.contacts.list_async(
            service_id="salesforce",
            limit=20,
        )
        while res is not None:
            for contact in res.data:
                print(contact.name)
            res = res.next()

asyncio.run(main())
```

### Error Handling

```python
from apideck_unify import Apideck, models

try:
    res = apideck.crm.contacts.get(id="invalid", service_id="salesforce")
except models.BadRequestResponse as e:
    print("Bad request:", e.message, e.status_code)
except models.UnauthorizedResponse as e:
    print("Invalid API key or missing credentials")
except models.NotFoundResponse as e:
    print("Record not found")
except models.PaymentRequiredResponse as e:
    print("API limit reached")
except models.UnprocessableResponse as e:
    print("Validation error:", e.message)
except models.ApideckError as e:
    print(f"API error {e.status_code}: {e.message}")
```

All exceptions inherit from `models.ApideckError` with properties: `message`, `status_code`, `headers`, `body`, `raw_response`.

### Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `service_id` | `str` | Downstream connector ID (e.g., `"quickbooks"`, `"salesforce"`) |
| `limit` | `int` | Max results per page (1-200, default 20) |
| `cursor` | `str` | Pagination cursor from previous response |
| `filter_` | `dict` | Resource-specific filter criteria (note trailing underscore) |
| `sort` | `dict` | `{"by": SortField, "direction": SortDirection}` |
| `fields` | `str` | Comma-separated field names to return |
| `pass_through` | `dict` | Pass-through query parameters for the downstream API |
| `raw` | `bool` | Include raw downstream response when `True` |
| `retry_config` | `RetryConfig` | Per-call retry override |

### Pass-Through Parameters

```python
# Query pass-through
res = apideck.accounting.invoices.list(
    service_id="quickbooks",
    pass_through={"search": "overdue"},
)

# Body pass-through for connector-specific fields
res = apideck.crm.contacts.create(
    service_id="salesforce",
    first_name="John",
    last_name="Doe",
    pass_through=[{
        "service_id": "salesforce",
        "operation_id": "contactsAdd",
        "extend_object": {"custom_sf_field__c": "value"},
    }],
)
```

### Retry Configuration

```python
from apideck_unify import Apideck
from apideck_unify.utils import BackoffStrategy, RetryConfig

with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    app_id="your-app-id",
    consumer_id="your-consumer-id",
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
) as apideck:
    pass
```

## API Namespaces

| Namespace | Resources |
|-----------|-----------|
| `apideck.accounting.*` | invoices, bills, payments, customers, suppliers, ledger_accounts, journal_entries, tax_rates, credit_notes, purchase_orders, balance_sheet, profit_and_loss, expenses, attachments, and more |
| `apideck.crm.*` | contacts, companies, leads, opportunities, activities, notes, pipelines, users |
| `apideck.hris.*` | employees, companies, departments, payrolls, time_off_requests |
| `apideck.file_storage.*` | files, folders, drives, shared_links, upload_sessions |
| `apideck.ats.*` | applicants, applications, jobs |
| `apideck.vault.*` | connections, consumers, sessions, custom_mappings, logs |
| `apideck.webhook.*` | webhooks, event_logs |
