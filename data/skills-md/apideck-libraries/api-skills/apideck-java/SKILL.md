---
name: apideck-java
description: Apideck Unified API integration patterns for Java. Use when building integrations with accounting software (QuickBooks, Xero, NetSuite), CRMs (Salesforce, HubSpot, Pipedrive), HRIS platforms (Workday, BambooHR), file storage (Google Drive, Dropbox, Box), ATS systems (Greenhouse, Lever), e-commerce, or any of Apideck's 200+ connectors using Java. Covers the com.apideck:unify Maven package, authentication, CRUD operations, pagination, async support, and Vault connection management.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck Java SDK Skill

## Overview

The [Apideck Unified API](https://apideck.com) provides a single integration layer to connect with 200+ third-party services across accounting, CRM, HRIS, file storage, ATS, e-commerce, and more. The official Java SDK (`com.apideck:unify`) provides typed clients for all unified APIs.

## Installation

**Gradle:**
```groovy
implementation 'com.apideck:unify:0.30.3'
```

**Maven:**
```xml
<dependency>
    <groupId>com.apideck</groupId>
    <artifactId>unify</artifactId>
    <version>0.30.3</version>
</dependency>
```

Requires JDK 11 or later.

## IMPORTANT RULES

- ALWAYS use the `com.apideck:unify` SDK. DO NOT make raw HTTP calls to the Apideck API.
- ALWAYS pass `apiKey`, `appId`, and `consumerId` when building the client.
- USE `serviceId` on requests to specify which downstream connector to use.
- USE the fluent builder pattern for constructing requests.
- ALWAYS handle errors with try/catch using `ApideckError` as the base class.
- DO NOT store API keys in source code. Use environment variables.

## Quick Start

```java
import com.apideck.unify.Apideck;
import com.apideck.unify.models.operations.*;

Apideck sdk = Apideck.builder()
    .consumerId("your-consumer-id")
    .appId("your-app-id")
    .apiKey(System.getenv("APIDECK_API_KEY"))
    .build();

sdk.crm().contacts().list()
    .serviceId("salesforce")
    .limit(20)
    .callAsStream()
    .forEach(page -> {
        page.getContactsResponse().ifPresent(res ->
            res.getData().forEach(contact ->
                System.out.println(contact.getName())
            )
        );
    });
```

## SDK Patterns

### Client Setup

```java
import com.apideck.unify.Apideck;

Apideck sdk = Apideck.builder()
    .consumerId("your-consumer-id")
    .appId("your-app-id")
    .apiKey(System.getenv("APIDECK_API_KEY"))
    .build();
```

Async client:

```java
import com.apideck.unify.AsyncApideck;

AsyncApideck asyncSdk = Apideck.builder()
    .consumerId("your-consumer-id")
    .appId("your-app-id")
    .apiKey(System.getenv("APIDECK_API_KEY"))
    .build()
    .async();
```

### CRUD Operations

Uses a fluent builder pattern: `sdk.{category}().{resource}().{operation}()`.

```java
import com.apideck.unify.models.components.*;
import com.apideck.unify.models.operations.*;

// LIST
sdk.crm().contacts().list()
    .serviceId("salesforce")
    .limit(20)
    .filter(ContactsFilter.builder().email("john@example.com").build())
    .sort(ContactsSort.builder()
        .by(ContactsSortBy.UPDATED_AT)
        .direction(SortDirection.DESC)
        .build())
    .call();

// CREATE
sdk.crm().contacts().create()
    .serviceId("salesforce")
    .contact(ContactInput.builder()
        .firstName("John")
        .lastName("Doe")
        .emails(List.of(Email.builder()
            .email("john@example.com")
            .type(EmailType.PRIMARY)
            .build()))
        .phoneNumbers(List.of(PhoneNumber.builder()
            .number("+1234567890")
            .type(PhoneNumberType.MOBILE)
            .build()))
        .build())
    .call();

// GET
sdk.crm().contacts().get()
    .id("contact_123")
    .serviceId("salesforce")
    .call();

// UPDATE
sdk.crm().contacts().update()
    .id("contact_123")
    .serviceId("salesforce")
    .contact(ContactInput.builder().firstName("Jane").build())
    .call();

// DELETE
sdk.crm().contacts().delete()
    .id("contact_123")
    .serviceId("salesforce")
    .call();
```

### Pagination

Multiple approaches available:

```java
// Stream (recommended)
sdk.accounting().invoices().list()
    .serviceId("quickbooks")
    .limit(50)
    .callAsStream()
    .forEach(page -> {
        // handle page
    });

// Iterable
for (var page : sdk.accounting().invoices().list()
    .serviceId("quickbooks")
    .limit(50)
    .callAsIterable()) {
    // handle page
}

// Reactive Streams (for Project Reactor, RxJava, etc.)
var publisher = sdk.accounting().invoices().list()
    .serviceId("quickbooks")
    .limit(50)
    .callAsPublisher();
```

### Async Support

Returns `CompletableFuture<T>` for standard operations:

```java
AsyncApideck asyncSdk = sdk.async();

asyncSdk.crm().contacts().list()
    .serviceId("salesforce")
    .limit(20)
    .call()
    .thenAccept(res -> {
        // handle response
    });
```

### Error Handling

```java
import com.apideck.unify.models.errors.*;

try {
    sdk.crm().contacts().get()
        .id("invalid")
        .serviceId("salesforce")
        .call();
} catch (BadRequestResponse e) {
    System.err.println("Bad request: " + e.message());
} catch (UnauthorizedResponse e) {
    System.err.println("Invalid API key");
} catch (NotFoundResponse e) {
    System.err.println("Record not found");
} catch (PaymentRequiredResponse e) {
    System.err.println("API limit reached");
} catch (UnprocessableResponse e) {
    System.err.println("Validation error: " + e.message());
} catch (ApideckError e) {
    System.err.println("API error " + e.code() + ": " + e.message());
}
```

### Retry Configuration

```java
import com.apideck.unify.utils.BackoffStrategy;
import com.apideck.unify.utils.RetryConfig;
import java.util.concurrent.TimeUnit;

Apideck sdk = Apideck.builder()
    .retryConfig(RetryConfig.builder()
        .backoff(BackoffStrategy.builder()
            .initialInterval(1L, TimeUnit.MILLISECONDS)
            .maxInterval(50L, TimeUnit.MILLISECONDS)
            .maxElapsedTime(1000L, TimeUnit.MILLISECONDS)
            .baseFactor(1.1)
            .jitterFactor(0.15)
            .retryConnectError(false)
            .build())
        .build())
    .consumerId("your-consumer-id")
    .appId("your-app-id")
    .apiKey(System.getenv("APIDECK_API_KEY"))
    .build();
```

## API Namespaces

| Namespace | Resources |
|-----------|-----------|
| `sdk.accounting().*` | invoices, bills, payments, customers, suppliers, ledgerAccounts, journalEntries, taxRates, creditNotes, purchaseOrders, balanceSheet, profitAndLoss, and more |
| `sdk.crm().*` | contacts, companies, leads, opportunities, activities, notes, pipelines, users |
| `sdk.hris().*` | employees, companies, departments, payrolls, timeOffRequests |
| `sdk.fileStorage().*` | files, folders, drives, driveGroups, sharedLinks, uploadSessions |
| `sdk.ats().*` | applicants, applications, jobs |
| `sdk.vault().*` | connections, consumers, sessions, customMappings, logs |
| `sdk.webhook().*` | webhooks, eventLogs |
