---
name: apideck-go
description: Apideck Unified API integration patterns for Go. Use when building integrations with accounting software (QuickBooks, Xero, NetSuite), CRMs (Salesforce, HubSpot, Pipedrive), HRIS platforms (Workday, BambooHR), file storage (Google Drive, Dropbox, Box), ATS systems (Greenhouse, Lever), e-commerce, or any of Apideck's 200+ connectors using Go. Covers the github.com/apideck-libraries/sdk-go package, authentication, CRUD operations, pagination, error handling, and Vault connection management.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck Go SDK Skill

## Overview

The [Apideck Unified API](https://apideck.com) provides a single integration layer to connect with 200+ third-party services across accounting, CRM, HRIS, file storage, ATS, e-commerce, and more. The official Go SDK provides typed clients for all unified APIs.

## Installation

```sh
go get github.com/apideck-libraries/sdk-go
```

## IMPORTANT RULES

- ALWAYS use the `github.com/apideck-libraries/sdk-go` SDK. DO NOT make raw `net/http` calls to the Apideck API.
- ALWAYS pass security, app ID, and consumer ID via functional options when creating the client.
- USE `ServiceID` on requests to specify which downstream connector to use.
- ALWAYS check returned `error` values (idiomatic Go error handling).
- USE `sdkgo.Pointer()` helper for optional fields.
- DO NOT store API keys in source code. Use environment variables.

## Quick Start

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    sdkgo "github.com/apideck-libraries/sdk-go"
    "github.com/apideck-libraries/sdk-go/models/components"
    "github.com/apideck-libraries/sdk-go/models/operations"
)

func main() {
    ctx := context.Background()

    s := sdkgo.New(
        sdkgo.WithConsumerID("your-consumer-id"),
        sdkgo.WithAppID("your-app-id"),
        sdkgo.WithSecurity(os.Getenv("APIDECK_API_KEY")),
    )

    res, err := s.Crm.Contacts.List(ctx, operations.CrmContactsAllRequest{
        ServiceID: sdkgo.Pointer("salesforce"),
        Limit:     sdkgo.Pointer(int64(20)),
    })
    if err != nil {
        log.Fatal(err)
    }

    for _, contact := range res.GetContactsResponse.Data {
        fmt.Println(contact.Name)
    }
}
```

## SDK Patterns

### Client Setup

```go
import sdkgo "github.com/apideck-libraries/sdk-go"

s := sdkgo.New(
    sdkgo.WithConsumerID("your-consumer-id"),
    sdkgo.WithAppID("your-app-id"),
    sdkgo.WithSecurity(os.Getenv("APIDECK_API_KEY")),
)
```

### CRUD Operations

All resources follow the pattern: `s.{Api}.{Resource}.{Operation}(ctx, request)`, returning `(response, error)`.

```go
import (
    sdkgo "github.com/apideck-libraries/sdk-go"
    "github.com/apideck-libraries/sdk-go/models/components"
    "github.com/apideck-libraries/sdk-go/models/operations"
)

ctx := context.Background()

// LIST
res, err := s.Crm.Contacts.List(ctx, operations.CrmContactsAllRequest{
    ServiceID: sdkgo.Pointer("salesforce"),
    Limit:     sdkgo.Pointer(int64(20)),
    Filter: &components.ContactsFilter{
        Email: sdkgo.Pointer("john@example.com"),
    },
    Sort: &components.ContactsSort{
        By:        (*components.ContactsSortBy)(sdkgo.Pointer("updated_at")),
        Direction: (*components.SortDirection)(sdkgo.Pointer("desc")),
    },
})

// CREATE
res, err := s.Crm.Contacts.Create(ctx, operations.CrmContactsAddRequest{
    ServiceID: sdkgo.Pointer("salesforce"),
    Contact: components.ContactInput{
        FirstName: sdkgo.Pointer("John"),
        LastName:  sdkgo.Pointer("Doe"),
        Emails: []components.Email{
            {Email: sdkgo.Pointer("john@example.com"), Type: (*components.EmailType)(sdkgo.Pointer("primary"))},
        },
        PhoneNumbers: []components.PhoneNumber{
            {Number: sdkgo.Pointer("+1234567890"), Type: (*components.PhoneNumberType)(sdkgo.Pointer("mobile"))},
        },
    },
})

// GET
res, err := s.Crm.Contacts.Get(ctx, operations.CrmContactsOneRequest{
    ID:        "contact_123",
    ServiceID: sdkgo.Pointer("salesforce"),
})

// UPDATE
res, err := s.Crm.Contacts.Update(ctx, operations.CrmContactsUpdateRequest{
    ID:        "contact_123",
    ServiceID: sdkgo.Pointer("salesforce"),
    Contact: components.ContactInput{
        FirstName: sdkgo.Pointer("Jane"),
    },
})

// DELETE
res, err := s.Crm.Contacts.Delete(ctx, operations.CrmContactsDeleteRequest{
    ID:        "contact_123",
    ServiceID: sdkgo.Pointer("salesforce"),
})
```

### Pagination

Use the `Next()` method on the response. Returns `nil` when no more pages:

```go
res, err := s.Accounting.Invoices.List(ctx, operations.AccountingInvoicesAllRequest{
    ServiceID: sdkgo.Pointer("quickbooks"),
    Limit:     sdkgo.Pointer(int64(50)),
})
if err != nil {
    log.Fatal(err)
}

for {
    for _, invoice := range res.GetInvoicesResponse.Data {
        fmt.Printf("%s: %v\n", *invoice.Number, *invoice.Total)
    }

    res, err = res.Next()
    if err != nil {
        log.Fatal(err)
    }
    if res == nil {
        break
    }
}
```

### Error Handling

```go
import (
    "errors"
    "github.com/apideck-libraries/sdk-go/models/apierrors"
)

res, err := s.Crm.Contacts.Get(ctx, req)
if err != nil {
    var badReq *apierrors.BadRequestResponse
    var unauthorized *apierrors.UnauthorizedResponse
    var notFound *apierrors.NotFoundResponse
    var paymentReq *apierrors.PaymentRequiredResponse
    var unprocessable *apierrors.UnprocessableResponse

    switch {
    case errors.As(err, &badReq):
        log.Printf("Bad request: %s", badReq.Error())
    case errors.As(err, &unauthorized):
        log.Printf("Unauthorized: %s", unauthorized.Error())
    case errors.As(err, &notFound):
        log.Printf("Not found: %s", notFound.Error())
    case errors.As(err, &paymentReq):
        log.Printf("Payment required: %s", paymentReq.Error())
    case errors.As(err, &unprocessable):
        log.Printf("Unprocessable: %s", unprocessable.Error())
    default:
        var apiErr *apierrors.APIError
        if errors.As(err, &apiErr) {
            log.Printf("API error %d: %s", apiErr.StatusCode, apiErr.Error())
        } else {
            log.Fatal(err)
        }
    }
}
```

### Retry Configuration

```go
import "github.com/apideck-libraries/sdk-go/retry"

// Global
s := sdkgo.New(
    sdkgo.WithRetryConfig(retry.Config{
        Strategy: "backoff",
        Backoff: &retry.BackoffStrategy{
            InitialInterval: 1,
            MaxInterval:     50,
            Exponent:        1.1,
            MaxElapsedTime:  100,
        },
        RetryConnectionErrors: false,
    }),
    sdkgo.WithConsumerID("your-consumer-id"),
    sdkgo.WithAppID("your-app-id"),
    sdkgo.WithSecurity(os.Getenv("APIDECK_API_KEY")),
)

// Per-operation
res, err := s.Crm.Contacts.List(ctx, req,
    operations.WithRetries(retry.Config{
        Strategy: "backoff",
        Backoff:  &retry.BackoffStrategy{InitialInterval: 1, MaxInterval: 50, Exponent: 1.1, MaxElapsedTime: 100},
    }),
)
```

## API Namespaces

| Namespace | Resources |
|-----------|-----------|
| `s.Accounting.*` | Invoices, Bills, Payments, Customers, Suppliers, LedgerAccounts, JournalEntries, TaxRates, CreditNotes, PurchaseOrders, BalanceSheet, ProfitAndLoss, and more |
| `s.Crm.*` | Contacts, Companies, Leads, Opportunities, Activities, Notes, Pipelines, Users |
| `s.Hris.*` | Employees, Companies, Departments, Payrolls, TimeOffRequests |
| `s.FileStorage.*` | Files, Folders, Drives, DriveGroups, SharedLinks, UploadSessions |
| `s.Ats.*` | Applicants, Applications, Jobs |
| `s.Vault.*` | Connections, Consumers, Sessions, CustomMappings, Logs |
| `s.Webhook.*` | Webhooks, EventLogs |
