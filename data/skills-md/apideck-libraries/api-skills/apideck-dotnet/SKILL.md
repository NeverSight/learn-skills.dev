---
name: apideck-dotnet
description: Apideck Unified API integration patterns for C# and .NET. Use when building integrations with accounting software (QuickBooks, Xero, NetSuite), CRMs (Salesforce, HubSpot, Pipedrive), HRIS platforms (Workday, BambooHR), file storage (Google Drive, Dropbox, Box), ATS systems (Greenhouse, Lever), e-commerce, or any of Apideck's 200+ connectors using .NET. Covers the ApideckUnifySdk NuGet package, authentication, CRUD operations, pagination, error handling, and Vault connection management.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck .NET SDK Skill

## Overview

The [Apideck Unified API](https://apideck.com) provides a single integration layer to connect with 200+ third-party services across accounting, CRM, HRIS, file storage, ATS, e-commerce, and more. The official .NET SDK (`ApideckUnifySdk`) provides typed clients for all unified APIs.

## Installation

```sh
dotnet add package ApideckUnifySdk
```

## IMPORTANT RULES

- ALWAYS use the `ApideckUnifySdk` NuGet package. DO NOT make raw `HttpClient` calls to the Apideck API.
- ALWAYS pass `apiKey`, `appId`, and `consumerId` when initializing the client.
- USE `ServiceId` to specify which downstream connector to use (e.g., `"salesforce"`, `"quickbooks"`).
- USE async/await for all API calls — all operations return `Task<T>`.
- ALWAYS handle errors with try/catch using `BaseException` as the base class.
- DO NOT store API keys in source code. Use environment variables or a secrets manager.

## Quick Start

```csharp
using ApideckUnifySdk;
using ApideckUnifySdk.Models.Requests;

var sdk = new Apideck(
    consumerId: "your-consumer-id",
    appId: "your-app-id",
    apiKey: Environment.GetEnvironmentVariable("APIDECK_API_KEY") ?? ""
);

var res = await sdk.Crm.Contacts.ListAsync(new CrmContactsAllRequest {
    ServiceId = "salesforce",
    Limit = 20,
});

while (res != null)
{
    foreach (var contact in res.GetContactsResponse?.Data ?? [])
    {
        Console.WriteLine($"{contact.Name} - {contact.Emails?.FirstOrDefault()?.Email}");
    }
    res = await res.Next!();
}
```

## SDK Patterns

### Client Setup

```csharp
using ApideckUnifySdk;

var sdk = new Apideck(
    consumerId: "your-consumer-id",
    appId: "your-app-id",
    apiKey: Environment.GetEnvironmentVariable("APIDECK_API_KEY") ?? ""
);
```

### CRUD Operations

All resources follow the pattern: `sdk.{Api}.{Resource}.{Operation}Async(request)`.

```csharp
using ApideckUnifySdk;
using ApideckUnifySdk.Models.Requests;
using ApideckUnifySdk.Models.Components;

// LIST
var listRes = await sdk.Crm.Contacts.ListAsync(new CrmContactsAllRequest {
    ServiceId = "salesforce",
    Limit = 20,
    Filter = new ContactsFilter { Email = "john@example.com" },
    Sort = new ContactsSort {
        By = ContactsSortBy.UpdatedAt,
        Direction = SortDirection.Desc,
    },
});

// CREATE
var createRes = await sdk.Crm.Contacts.CreateAsync(new CrmContactsAddRequest {
    ServiceId = "salesforce",
    Contact = new ContactInput {
        FirstName = "John",
        LastName = "Doe",
        Emails = new List<Email> {
            new Email { EmailAddress = "john@example.com", Type = EmailType.Primary },
        },
        PhoneNumbers = new List<PhoneNumber> {
            new PhoneNumber { Number = "+1234567890", Type = PhoneNumberType.Mobile },
        },
    },
});
Console.WriteLine(createRes.CreateContactResponse?.Data?.Id);

// GET
var getRes = await sdk.Crm.Contacts.GetAsync(new CrmContactsOneRequest {
    Id = "contact_123",
    ServiceId = "salesforce",
});

// UPDATE
var updateRes = await sdk.Crm.Contacts.UpdateAsync(new CrmContactsUpdateRequest {
    Id = "contact_123",
    ServiceId = "salesforce",
    Contact = new ContactInput { FirstName = "Jane" },
});

// DELETE
await sdk.Crm.Contacts.DeleteAsync(new CrmContactsDeleteRequest {
    Id = "contact_123",
    ServiceId = "salesforce",
});
```

### Pagination

Use the `Next` method on the response. Returns `null` when no more pages:

```csharp
var res = await sdk.Accounting.Invoices.ListAsync(new AccountingInvoicesAllRequest {
    ServiceId = "quickbooks",
    Limit = 50,
});

while (res != null)
{
    foreach (var invoice in res.GetInvoicesResponse?.Data ?? [])
    {
        Console.WriteLine($"{invoice.Number}: {invoice.Total}");
    }
    res = await res.Next!();
}
```

### Error Handling

```csharp
using ApideckUnifySdk.Models.Errors;

try
{
    var res = await sdk.Crm.Contacts.GetAsync(new CrmContactsOneRequest { Id = "invalid" });
}
catch (BadRequestResponse e)
{
    Console.Error.WriteLine($"Bad request: {e.Message}");
}
catch (UnauthorizedResponse e)
{
    Console.Error.WriteLine("Invalid API key or missing credentials");
}
catch (NotFoundResponse e)
{
    Console.Error.WriteLine("Record not found");
}
catch (PaymentRequiredResponse e)
{
    Console.Error.WriteLine("API limit reached");
}
catch (UnprocessableResponse e)
{
    Console.Error.WriteLine($"Validation error: {e.Message}");
}
catch (BaseException e)
{
    Console.Error.WriteLine($"API error: {e.Message}");
    Console.Error.WriteLine($"Status: {e.Response.StatusCode}");
}
```

### Retry Configuration

```csharp
var sdk = new Apideck(
    retryConfig: new RetryConfig(
        strategy: RetryConfig.RetryStrategy.BACKOFF,
        backoff: new BackoffStrategy(
            initialIntervalMs: 1L,
            maxIntervalMs: 50L,
            maxElapsedTimeMs: 100L,
            exponent: 1.1
        ),
        retryConnectionErrors: false
    ),
    consumerId: "your-consumer-id",
    appId: "your-app-id",
    apiKey: Environment.GetEnvironmentVariable("APIDECK_API_KEY") ?? ""
);
```

## API Namespaces

| Namespace | Resources |
|-----------|-----------|
| `sdk.Accounting.*` | Invoices, Bills, Payments, Customers, Suppliers, LedgerAccounts, JournalEntries, TaxRates, CreditNotes, PurchaseOrders, BalanceSheet, ProfitAndLoss, and more |
| `sdk.Crm.*` | Contacts, Companies, Leads, Opportunities, Activities, Notes, Pipelines, Users |
| `sdk.Hris.*` | Employees, Companies, Departments, Payrolls, TimeOffRequests |
| `sdk.FileStorage.*` | Files, Folders, Drives, DriveGroups, SharedLinks, UploadSessions |
| `sdk.Ats.*` | Applicants, Applications, Jobs |
| `sdk.Vault.*` | Connections, Consumers, Sessions, CustomMappings, Logs |
| `sdk.Webhook.*` | Webhooks, EventLogs |
