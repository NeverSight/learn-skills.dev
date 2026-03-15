---
name: apideck-php
description: Apideck Unified API integration patterns for PHP. Use when building integrations with accounting software (QuickBooks, Xero, NetSuite), CRMs (Salesforce, HubSpot, Pipedrive), HRIS platforms (Workday, BambooHR), file storage (Google Drive, Dropbox, Box), ATS systems (Greenhouse, Lever), e-commerce, or any of Apideck's 200+ connectors using PHP. Covers the apideck-libraries/sdk-php Composer package, authentication, CRUD operations, pagination, error handling, and Vault connection management.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck PHP SDK Skill

## Overview

The [Apideck Unified API](https://apideck.com) provides a single integration layer to connect with 200+ third-party services across accounting, CRM, HRIS, file storage, ATS, e-commerce, and more. The official PHP SDK provides typed clients for all unified APIs.

## Installation

```sh
composer require apideck-libraries/sdk-php
```

## IMPORTANT RULES

- ALWAYS use the `apideck-libraries/sdk-php` Composer package. DO NOT make raw `Guzzle`/`curl` calls to the Apideck API.
- ALWAYS pass security, app ID, and consumer ID via the builder when creating the client.
- USE `serviceId` on requests to specify which downstream connector to use.
- ALWAYS handle errors with try/catch using `Errors\APIException` as the base class.
- DO NOT store API keys in source code. Use environment variables.

## Quick Start

```php
<?php

use Apideck\Unify;
use Apideck\Unify\Models\Operations;
use Apideck\Unify\Models\Components;

$sdk = Unify\Apideck::builder()
    ->setConsumerId('your-consumer-id')
    ->setAppId('your-app-id')
    ->setSecurity(getenv('APIDECK_API_KEY'))
    ->build();

$request = new Operations\CrmContactsAllRequest(
    serviceId: 'salesforce',
    limit: 20,
);

$responses = $sdk->crm->contacts->list(request: $request);

foreach ($responses as $response) {
    if ($response->httpMeta->response->getStatusCode() === 200) {
        foreach ($response->getContactsResponse->data as $contact) {
            echo $contact->name . "\n";
        }
    }
}
```

## SDK Patterns

### Client Setup

```php
use Apideck\Unify;

$sdk = Unify\Apideck::builder()
    ->setConsumerId('your-consumer-id')
    ->setAppId('your-app-id')
    ->setSecurity(getenv('APIDECK_API_KEY'))
    ->build();
```

### CRUD Operations

All resources follow the pattern: `$sdk->{api}->{resource}->{operation}(request: $request)`.

```php
use Apideck\Unify\Models\Operations;
use Apideck\Unify\Models\Components;

// LIST
$request = new Operations\CrmContactsAllRequest(
    serviceId: 'salesforce',
    limit: 20,
    filter: new Components\ContactsFilter(email: 'john@example.com'),
    sort: new Components\ContactsSort(
        by: Components\ContactsSortBy::UpdatedAt,
        direction: Components\SortDirection::Desc,
    ),
);
$responses = $sdk->crm->contacts->list(request: $request);

// CREATE
$request = new Operations\CrmContactsAddRequest(
    serviceId: 'salesforce',
    contact: new Components\ContactInput(
        firstName: 'John',
        lastName: 'Doe',
        emails: [
            new Components\Email(email: 'john@example.com', type: Components\EmailType::Primary),
        ],
        phoneNumbers: [
            new Components\PhoneNumber(number: '+1234567890', type: Components\PhoneNumberType::Mobile),
        ],
    ),
);
$response = $sdk->crm->contacts->create(request: $request);

// GET
$request = new Operations\CrmContactsOneRequest(
    id: 'contact_123',
    serviceId: 'salesforce',
);
$response = $sdk->crm->contacts->get(request: $request);

// UPDATE
$request = new Operations\CrmContactsUpdateRequest(
    id: 'contact_123',
    serviceId: 'salesforce',
    contact: new Components\ContactInput(firstName: 'Jane'),
);
$response = $sdk->crm->contacts->update(request: $request);

// DELETE
$request = new Operations\CrmContactsDeleteRequest(
    id: 'contact_123',
    serviceId: 'salesforce',
);
$response = $sdk->crm->contacts->delete(request: $request);
```

### Pagination

The `list` method returns a PHP Generator. Iterate with `foreach`:

```php
$request = new Operations\AccountingInvoicesAllRequest(
    serviceId: 'quickbooks',
    limit: 50,
);

$responses = $sdk->accounting->invoices->list(request: $request);

foreach ($responses as $response) {
    if ($response->httpMeta->response->getStatusCode() === 200) {
        foreach ($response->getInvoicesResponse->data as $invoice) {
            echo "{$invoice->number}: {$invoice->total}\n";
        }
    }
}
```

### Error Handling

```php
use Apideck\Unify\Models\Errors;

try {
    $responses = $sdk->crm->contacts->list(request: $request);
    foreach ($responses as $response) {
        // handle response
    }
} catch (Errors\BadRequestResponseThrowable $e) {
    echo "Bad request: " . $e->getMessage() . "\n";
} catch (Errors\UnauthorizedResponseThrowable $e) {
    echo "Unauthorized\n";
} catch (Errors\NotFoundResponseThrowable $e) {
    echo "Not found\n";
} catch (Errors\PaymentRequiredResponseThrowable $e) {
    echo "API limit reached\n";
} catch (Errors\UnprocessableResponseThrowable $e) {
    echo "Validation error: " . $e->getMessage() . "\n";
} catch (Errors\APIException $e) {
    echo "API error: " . $e->getMessage() . "\n";
}
```

### Retry Configuration

```php
use Apideck\Unify\Utils\Retry;

// Global
$sdk = Unify\Apideck::builder()
    ->setRetryConfig(
        new Retry\RetryConfigBackoff(
            initialInterval: 1,
            maxInterval: 50,
            exponent: 1.1,
            maxElapsedTime: 100,
            retryConnectionErrors: false,
        )
    )
    ->setConsumerId('your-consumer-id')
    ->setAppId('your-app-id')
    ->setSecurity(getenv('APIDECK_API_KEY'))
    ->build();
```

## API Namespaces

| Namespace | Resources |
|-----------|-----------|
| `$sdk->accounting->*` | invoices, bills, payments, customers, suppliers, ledgerAccounts, journalEntries, taxRates, creditNotes, purchaseOrders, balanceSheet, profitAndLoss, and more |
| `$sdk->crm->*` | contacts, companies, leads, opportunities, activities, notes, pipelines, users |
| `$sdk->hris->*` | employees, companies, departments, payrolls, timeOffRequests |
| `$sdk->fileStorage->*` | files, folders, drives, driveGroups, sharedLinks, uploadSessions |
| `$sdk->ats->*` | applicants, applications, jobs |
| `$sdk->vault->*` | connections, consumers, sessions, customMappings, logs |
| `$sdk->webhook->*` | webhooks, eventLogs |
