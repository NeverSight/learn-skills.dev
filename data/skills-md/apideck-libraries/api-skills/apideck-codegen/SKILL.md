---
name: apideck-codegen
description: Generate typed API clients from Apideck OpenAPI specs using code generators. Use when the user wants to generate custom SDK clients, typed models, API stubs, or server scaffolding from Apideck's published OpenAPI specifications. Covers openapi-generator, Speakeasy, and Postman import workflows.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Apideck Code Generation Skill

## Overview

Apideck publishes OpenAPI 3.x specifications for all unified APIs at `https://specs.apideck.com/{api-name}.yml`. These specs can be used with code generators to produce typed clients, models, server stubs, and documentation in any language.

## IMPORTANT RULES

- ALWAYS prefer the official Apideck SDKs over generated clients. Code generation is for languages/frameworks not covered by official SDKs, or for custom model generation.
- ALWAYS use the latest spec from `https://specs.apideck.com/{api-name}.yml`. Do not use cached or outdated specs.
- USE the official SDKs for: TypeScript (`@apideck/unify`), Python (`apideck-unify`), C# (`ApideckUnifySdk`), Java (`com.apideck:unify`), Go (`sdk-go`), PHP (`sdk-php`).
- When generating clients, always configure authentication headers: `Authorization`, `x-apideck-app-id`, `x-apideck-consumer-id`.

## Available OpenAPI Specs

| API | Spec URL |
|-----|----------|
| Accounting | `https://specs.apideck.com/accounting.yml` |
| CRM | `https://specs.apideck.com/crm.yml` |
| HRIS | `https://specs.apideck.com/hris.yml` |
| File Storage | `https://specs.apideck.com/file-storage.yml` |
| ATS | `https://specs.apideck.com/ats.yml` |
| E-commerce | `https://specs.apideck.com/ecommerce.yml` |
| Issue Tracking | `https://specs.apideck.com/issue-tracking.yml` |
| SMS | `https://specs.apideck.com/sms.yml` |
| Lead | `https://specs.apideck.com/lead.yml` |
| Vault | `https://specs.apideck.com/vault.yml` |
| Webhook | `https://specs.apideck.com/webhook.yml` |
| Connector | `https://specs.apideck.com/connector.yml` |

All specs are also available on GitHub: `https://github.com/apideck-libraries/openapi-specs`

## OpenAPI Generator

### Installation

```sh
# npm
npm install @openapitools/openapi-generator-cli -g

# Homebrew
brew install openapi-generator

# Docker
docker pull openapitools/openapi-generator-cli
```

### Generate a Typed Client

```sh
# TypeScript (Axios)
openapi-generator-cli generate \
  -i https://specs.apideck.com/crm.yml \
  -g typescript-axios \
  -o ./generated/crm-client \
  --additional-properties=npmName=apideck-crm,supportsES6=true,withInterfaces=true

# Python (urllib3)
openapi-generator-cli generate \
  -i https://specs.apideck.com/accounting.yml \
  -g python \
  -o ./generated/accounting-client \
  --additional-properties=packageName=apideck_accounting

# Rust
openapi-generator-cli generate \
  -i https://specs.apideck.com/crm.yml \
  -g rust \
  -o ./generated/crm-client \
  --additional-properties=packageName=apideck_crm

# Swift
openapi-generator-cli generate \
  -i https://specs.apideck.com/hris.yml \
  -g swift5 \
  -o ./generated/hris-client \
  --additional-properties=projectName=ApideckHRIS

# Kotlin
openapi-generator-cli generate \
  -i https://specs.apideck.com/crm.yml \
  -g kotlin \
  -o ./generated/crm-client \
  --additional-properties=groupId=com.apideck,artifactId=crm-client

# Dart
openapi-generator-cli generate \
  -i https://specs.apideck.com/crm.yml \
  -g dart \
  -o ./generated/crm-client
```

### Generate Models Only

When you only need typed data models without the API client:

```sh
openapi-generator-cli generate \
  -i https://specs.apideck.com/crm.yml \
  -g typescript-axios \
  -o ./generated/crm-models \
  --global-property=models

openapi-generator-cli generate \
  -i https://specs.apideck.com/accounting.yml \
  -g python \
  -o ./generated/accounting-models \
  --global-property=models
```

### Generate API Documentation

```sh
# HTML docs
openapi-generator-cli generate \
  -i https://specs.apideck.com/crm.yml \
  -g html2 \
  -o ./docs/crm

# Markdown docs
openapi-generator-cli generate \
  -i https://specs.apideck.com/crm.yml \
  -g markdown \
  -o ./docs/crm
```

### Available Generators

Run `openapi-generator-cli list` for all generators. Common choices:

| Language | Client Generator | Notes |
|----------|-----------------|-------|
| TypeScript | `typescript-axios`, `typescript-fetch`, `typescript-node` | `typescript-axios` recommended |
| Python | `python`, `python-pydantic-v1` | `python` uses urllib3 |
| Rust | `rust` | Uses reqwest |
| Swift | `swift5`, `swift6` | Native URLSession |
| Kotlin | `kotlin`, `kotlin-server` | Uses OkHttp |
| Dart | `dart`, `dart-dio` | `dart-dio` for Flutter |
| Ruby | `ruby` | Uses Faraday |
| Elixir | `elixir` | Uses Tesla |
| C++ | `cpp-restsdk` | Uses cpprestsdk |

### Configuration File

For repeatable generation, use a config file:

```yaml
# openapitools.json
{
  "$schema": "node_modules/@openapitools/openapi-generator-cli/config.schema.json",
  "spaces": 2,
  "generator-cli": {
    "version": "7.0.0",
    "generators": {
      "crm-ts": {
        "generatorName": "typescript-axios",
        "inputSpec": "https://specs.apideck.com/crm.yml",
        "output": "./generated/crm",
        "additionalProperties": {
          "npmName": "apideck-crm",
          "supportsES6": true,
          "withInterfaces": true
        }
      },
      "accounting-py": {
        "generatorName": "python",
        "inputSpec": "https://specs.apideck.com/accounting.yml",
        "output": "./generated/accounting",
        "additionalProperties": {
          "packageName": "apideck_accounting"
        }
      }
    }
  }
}
```

Then run: `openapi-generator-cli generate`

## Speakeasy

[Speakeasy](https://www.speakeasy.com) is the generator Apideck uses for their official SDKs.

```sh
# Install
brew install speakeasy-api/homebrew-tap/speakeasy

# Generate TypeScript SDK
speakeasy generate sdk \
  -s https://specs.apideck.com/crm.yml \
  -t typescript \
  -o ./generated/crm-sdk

# Generate Python SDK
speakeasy generate sdk \
  -s https://specs.apideck.com/accounting.yml \
  -t python \
  -o ./generated/accounting-sdk

# Generate Go SDK
speakeasy generate sdk \
  -s https://specs.apideck.com/hris.yml \
  -t go \
  -o ./generated/hris-sdk
```

## Postman Import

Import Apideck specs directly into Postman for manual testing:

```sh
# Using Portman (recommended — adds contract tests)
npx @apideck/portman -u https://specs.apideck.com/crm.yml -o ./crm.postman.json

# Direct Postman import
# 1. Open Postman → Import → Link
# 2. Paste: https://specs.apideck.com/crm.yml
# 3. Postman auto-converts the OpenAPI spec to a collection
```

## Filtering Specs

To generate a client for only a subset of endpoints, use `oas-format-filter` (used internally by Portman):

```sh
npm install -g @apideck/oas-format-filter

# Filter to only CRM contacts endpoints
oas-format-filter \
  --input https://specs.apideck.com/crm.yml \
  --output ./filtered-crm.yml \
  --filter '{"paths": ["/crm/contacts*"]}'
```

Then generate from the filtered spec.

## Authentication Configuration

When configuring generated clients, set these headers on every request:

```
Authorization: Bearer {APIDECK_API_KEY}
x-apideck-app-id: {APP_ID}
x-apideck-consumer-id: {CONSUMER_ID}
x-apideck-service-id: {SERVICE_ID}  (optional, but recommended)
```

Base URL: `https://unify.apideck.com`
