---
name: fetch
description: Use when building typed HTTP clients with schema-validated responses or replacing unsafe fetch assertions.
---

# fetch

## Overview

Type-safe `fetch` wrapper with Standard Schema validation and typed response inference.

## When to Use

- Replacing `fetch` calls that rely on `as` type assertions
- Validating API responses at runtime with Standard Schema
- Standardizing request methods and error handling

## When Not to Use

- You do not control or validate any API responses

## Quick Reference

- Client: `api`
- Request: `api.get(url, schema)` (also `post`, `put`, `patch`, `delete`)
- Errors: `FetchError`, `ValidationError`
- Factory: create a configured client for shared base URL/auth

## Inputs to Request

- Base URL and auth details
- Response schemas and expected types
- Error handling preferences
- Required HTTP methods

## Resources

- https://www.zapstudio.dev/packages/fetch
- https://www.zapstudio.dev/llms.txt
